"""Correo ficticio: SMTP simulado, adjunto y límite durable de intentos."""
from datetime import timedelta
from email import policy
from email.parser import BytesParser
from hashlib import sha256
from io import BytesIO
import secrets
import smtplib
import ssl
from uuid import uuid4

import pytest
from pypdf import PdfWriter
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.correo import preparar_envio, reintentar_envios, send_email, registrar_bounce
from app.models import Carga, Cliente, Envio, Intento, RegistroAcceso, Retencion, Sistema, Usuario, ahora
from app.planillas.leyenda_iram import incorporar_leyenda_iram


@pytest.fixture(autouse=True)
def entorno_correo(app, monkeypatch, tmp_path):
    for name in ("SMTP_HOST","SMTP_PORT","SMTP_USER","SMTP_PASSWORD","MAIL_FROM","SMTP_FROM"):
        monkeypatch.delenv(name,raising=False)
    monkeypatch.setenv("SMTP_HOST","smtp.gmail.com")
    monkeypatch.setenv("SMTP_PORT","587")
    monkeypatch.setenv("SMTP_USER","[Ejemplo] cuenta simulada")
    monkeypatch.setenv("SMTP_PASSWORD",secrets.token_urlsafe(24))
    monkeypatch.setenv("MAIL_FROM","readyproof@example.invalid")
    app.config.update(MAIL_MODO_PRUEBA=False,PLANILLAS_DESTINATARIOS_PRUEBA="cliente@example.invalid",DIRECTORIO_CORREO=str(tmp_path/"correo"))


@pytest.fixture
def smtp(monkeypatch):
    class SMTPFalso:
        calls=[]
        error=None
        phase="send"
        def __init__(self,host,port,timeout):
            self.calls.append(("connect",host,port,timeout))
            if self.phase=="connect" and self.error:raise self.error
        def ehlo(self):self.calls.append(("ehlo",))
        def starttls(self,context):
            assert context.verify_mode==ssl.CERT_REQUIRED and context.check_hostname
            self.calls.append(("tls",))
        def login(self,user,password):self.calls.append(("login",user,password))
        def send_message(self,message,**kwargs):
            self.calls.append(("send",message,kwargs))
            if self.error:raise self.error
            return {}
        def quit(self):self.calls.append(("quit",))
        def close(self):pass
    monkeypatch.setattr(smtplib,"SMTP",SMTPFalso)
    return SMTPFalso


@pytest.fixture
def carga_emitida(app,catalogo,datos_api,usuario_admin,tmp_path):
    writer=PdfWriter();writer.add_blank_page(width=595,height=842)
    source=tmp_path/"base.pdf"
    with source.open("wb") as output:writer.write(output)
    destination=tmp_path/"emitida.pdf"
    incorporar_leyenda_iram(source,destination)
    pdf=destination.read_bytes()
    with Session(app.extensions["db_engine"],expire_on_commit=False) as session:
        row=Carga(sistema_id=catalogo[1]["id"],planilla_id=catalogo[2]["id"],creada_por_id=usuario_admin["id"],
            datos=datos_api,estado="emitida",emitida_en=ahora(),pdf=pdf,pdf_sha256=sha256(pdf).hexdigest())
        session.add(row);session.commit();return row.id


def preparar(session,key,actor):
    return preparar_envio(session,session.get(Carga,key),"cliente@example.invalid",actor,"[Ejemplo] Planilla","[Ejemplo] PDF adjunto.")


def test_envio_inmediato_real_en_modo_prueba_no_transmite(app, client, carga_emitida, monkeypatch):
    app.config.update(MODO_PILOTO=False, MAIL_MODO_PRUEBA=True, PLANILLAS_TRANSPORTE="gmail_api",
                      EMPRESA_MANTENEDORA="Empresa ficticia", CERTIFICADO_N="IFI-2099-00001")
    with Session(app.extensions["db_engine"]) as db:
        carga = db.get(Carga, carga_emitida)
        carga.numero_registro = 1
        sistema = db.get(Sistema, carga.sistema_id)
        db.get(Cliente, sistema.cliente_id).es_ejemplo = False
        db.commit()

    intentos = []
    destinatario = "cliente@example.invalid"

    def registrar(transporte, destinos=()):
        intentos.append((transporte, tuple(destinos)))
        assert all(valor.endswith("@example.invalid") for valor in destinos)

    def token_simulado():
        registrar("gmail_token")
        return "token-ficticio"

    class SMTPFalso:
        def __init__(self, *args, **kwargs):
            registrar("smtp_conexion")

        def send_message(self, mensaje, **kwargs):
            registrar("smtp_envio", (str(mensaje["To"]),))

    monkeypatch.setattr("app.gmail_https.obtener_token", token_simulado)
    monkeypatch.setattr("app.gmail_https.enviar_con_token",
                        lambda mensaje, token: registrar("gmail_envio", (str(mensaje["To"]),)))
    monkeypatch.setattr(smtplib, "SMTP", SMTPFalso)
    monkeypatch.setattr(smtplib, "SMTP_SSL", SMTPFalso)
    respuesta = client.post(f"/api/cargas/{carga_emitida}/enviar",
                            json={"destinatario": destinatario, "inmediato": True},
                            headers={"Idempotency-Key": str(uuid4())})
    assert respuesta.status_code == 202, respuesta.json
    assert respuesta.json["modo_prueba"] is True
    assert respuesta.json["estado"] == "pendiente"
    assert respuesta.json["destinatario"] == destinatario
    assert intentos == []


def test_gmail_credenciales_desde_env(app,smtp,carga_emitida,usuario_admin,monkeypatch):
    password=secrets.token_urlsafe(24);monkeypatch.setenv("SMTP_PASSWORD",password)
    with app.app_context(),Session(app.extensions["db_engine"]) as session:
        envio=send_email(session,preparar(session,carga_emitida,usuario_admin["id"]))
        assert smtp.calls[0]==("connect","smtp.gmail.com",587,30)
        assert ("login","[Ejemplo] cuenta simulada",password) in smtp.calls
        assert [c[0] for c in smtp.calls]==["connect","ehlo","tls","ehlo","login","send","quit"]
        assert envio.estado=="enviado" and envio.enviado_en
        assert password not in envio.mensaje_eml.decode()
        assert all(password not in (row.respuesta or "") for row in envio.intentos)


def test_envio_registra_intento(app,smtp,carga_emitida,usuario_admin):
    with app.app_context(),Session(app.extensions["db_engine"]) as session:
        envio=send_email(session,preparar(session,carga_emitida,usuario_admin["id"]))
        rows=list(session.scalars(select(Intento).where(Intento.envio_id==envio.id)))
        assert len(rows)==1 and rows[0].numero==1 and rows[0].resultado=="ok"
        message=BytesParser(policy=policy.default).parsebytes(envio.mensaje_eml)
        attachments=list(message.iter_attachments())
        assert len(attachments)==1 and attachments[0].get_content_type()=="application/pdf"
        assert attachments[0].get_payload(decode=True)==session.get(Carga,carga_emitida).pdf==envio.pdf_copia
        assert envio.retener_hasta.year==session.get(Carga,carga_emitida).emitida_en.year+3
        assert session.scalar(select(RegistroAcceso).where(RegistroAcceso.evento=="correo_intento")).destinatario==envio.destinatario


def test_reintentos_limite_3(app,smtp,carga_emitida,usuario_admin):
    smtp.phase="connect";smtp.error=TimeoutError("respuesta externa que no se debe registrar")
    start=ahora()
    with app.app_context(),Session(app.extensions["db_engine"]) as session:
        envio=send_email(session,preparar(session,carga_emitida,usuario_admin["id"]),fecha=start)
        key=envio.id
        assert reintentar_envios(fecha=start+timedelta(minutes=14))==0
        for minutes in (15,30):assert reintentar_envios(fecha=start+timedelta(minutes=minutes))==1
        assert reintentar_envios(fecha=start+timedelta(minutes=45))==0
        session.expire_all();envio=session.get(Envio,key)
        assert envio.intentos_reservados==3 and envio.estado=="fallo"
        rows=list(session.scalars(select(Intento).where(Intento.envio_id==key).order_by(Intento.numero)))
        assert [r.numero for r in rows]==[1,2,3] and {r.resultado for r in rows}=={"timeout"}
        retry=session.scalar(select(Retencion).where(Retencion.envio_id==key))
        assert retry.proximos_intentos==0 and retry.reintentado_en is None
        assert len([call for call in smtp.calls if call[0]=="connect"])==3
        assert all("externa" not in row.respuesta for row in rows)


@pytest.mark.parametrize("error,expected",[
    (smtplib.SMTPRecipientsRefused({"cliente@example.invalid":(550,b"external private response")}),"rechazado"),
    (smtplib.SMTPAuthenticationError(535,b"external private response"),"rechazado"),
    (TimeoutError("external private response"),"timeout"),
])
def test_fallos_permanentes_o_data_ambigua_no_reenvian(app,smtp,carga_emitida,usuario_admin,error,expected):
    smtp.error=error
    with app.app_context(),Session(app.extensions["db_engine"]) as session:
        envio=send_email(session,preparar(session,carga_emitida,usuario_admin["id"]))
        assert envio.estado=="fallo" and envio.intentos[0].resultado==expected
        assert "private" not in envio.intentos[0].respuesta
        assert reintentar_envios(fecha=ahora()+timedelta(days=1))==0


def test_modo_archivo_sin_smtp(app,carga_emitida,usuario_admin):
    app.config["MAIL_MODO_PRUEBA"]=True
    with app.app_context(),Session(app.extensions["db_engine"]) as session:
        envio=send_email(session,preparar(session,carga_emitida,usuario_admin["id"]))
        from pathlib import Path
        saved=Path(app.config["DIRECTORIO_CORREO"])/(envio.id+".eml")
        assert saved.read_bytes()==envio.mensaje_eml
        assert envio.estado=="pendiente" and envio.enviado_en is None
        app.config["MAIL_MODO_PRUEBA"]=False
        assert reintentar_envios(fecha=ahora()+timedelta(days=1))==0


def test_endpoint_encola_solo_emitidas(client,app,carga_emitida,smtp):
    response=client.post(f"/api/cargas/{carga_emitida}/enviar",json={"destinatario":"cliente@example.invalid"})
    assert response.status_code==202 and response.get_json()["estado"]=="pendiente"
    assert smtp.calls==[]
    with Session(app.extensions["db_engine"]) as session:
        carga=session.get(Carga,carga_emitida);carga.estado="borrador";session.commit()
    assert client.post(f"/api/cargas/{carga_emitida}/enviar",json={"destinatario":"cliente@example.invalid"}).status_code==409


@pytest.mark.parametrize("value",["a@example.invalid\r\nBcc: other@example.invalid","otra persona <a@example.invalid>","sin-arroba",None])
def test_endpoint_rechaza_destinatarios_invalidos(client,app,carga_emitida,value):
    response=client.post(f"/api/cargas/{carga_emitida}/enviar",json={"destinatario":value})
    assert response.status_code==422
    with Session(app.extensions["db_engine"]) as session:
        assert session.scalar(select(func.count()).select_from(Envio))==0


def test_worker_revisa_permisos_revocados(app,smtp,carga_emitida,usuario_admin):
    with app.app_context(),Session(app.extensions["db_engine"]) as session:
        envio=send_email(session,preparar(session,carga_emitida,usuario_admin["id"]),encolar=True)
        user=session.get(Usuario,usuario_admin["id"]);user.activo=False;session.commit()
        assert reintentar_envios()==0 and smtp.calls==[]
        session.refresh(envio);assert envio.estado=="fallo"


def test_bounce_posterior_bloquea_reintentos(app,smtp,carga_emitida,usuario_admin):
    with app.app_context(),Session(app.extensions["db_engine"]) as session:
        envio=send_email(session,preparar(session,carga_emitida,usuario_admin["id"]))
        registrar_bounce(session,envio.id,usuario_admin["id"])
        session.refresh(envio)
        assert envio.estado=="fallo" and envio.intentos[0].resultado=="bounce"
        assert reintentar_envios(fecha=ahora()+timedelta(days=1))==0


def test_reserva_interrumpida_no_duplica_envio(app,smtp,carga_emitida,usuario_admin):
    with app.app_context(),Session(app.extensions["db_engine"]) as session:
        envio=send_email(session,preparar(session,carga_emitida,usuario_admin["id"]),encolar=True)
        envio.intentos_reservados=1;envio.en_proceso_desde=ahora()-timedelta(minutes=16);session.commit()
        assert reintentar_envios()==0 and smtp.calls==[]
        session.refresh(envio)
        assert envio.estado=="fallo" and envio.intentos[0].numero==1 and envio.intentos[0].resultado=="timeout"


def test_testing_no_lee_archivos_env(database_url,monkeypatch):
    import app as module
    def prohibido(*args,**kwargs):raise AssertionError("No abrir archivos de credenciales durante los tests.")
    monkeypatch.setattr(module,"load_dotenv",prohibido)
    application=module.create_app({"TESTING":True,"DATABASE_URL":database_url})
    application.extensions["db_engine"].dispose()


def test_450_reintenta_y_conserva_mensaje(app,smtp,carga_emitida,usuario_admin):
    smtp.error=smtplib.SMTPRecipientsRefused({"cliente@example.invalid":(450,b"temporal")})
    with app.app_context(),Session(app.extensions["db_engine"]) as session:
        start=ahora()
        envio=send_email(session,preparar(session,carga_emitida,usuario_admin["id"]),fecha=start)
        original=envio.mensaje_eml
        smtp.error=None
        assert reintentar_envios(fecha=start+timedelta(minutes=15))==1
        session.refresh(envio)
        assert envio.estado=="enviado" and envio.mensaje_eml==original
        assert [r.numero for r in session.scalars(select(Intento).where(Intento.envio_id==envio.id).order_by(Intento.numero))]==[1,2]


def test_corte_en_quit_no_duplica_aceptacion(app,smtp,carga_emitida,usuario_admin,monkeypatch):
    def corte(self):raise smtplib.SMTPServerDisconnected("respuesta externa")
    monkeypatch.setattr(smtp,"quit",corte)
    with app.app_context(),Session(app.extensions["db_engine"]) as session:
        envio=send_email(session,preparar(session,carga_emitida,usuario_admin["id"]))
        assert envio.estado=="enviado" and envio.intentos[0].resultado=="ok"
        assert reintentar_envios(fecha=ahora()+timedelta(days=1))==0


def test_dos_workers_no_transmiten_el_mismo_envio(app,smtp,carga_emitida,usuario_admin,monkeypatch):
    original=smtp.send_message
    def segundo_worker(self,message,**kwargs):
        assert reintentar_envios()==0
        return original(self,message,**kwargs)
    monkeypatch.setattr(smtp,"send_message",segundo_worker)
    with app.app_context(),Session(app.extensions["db_engine"]) as session:
        envio=send_email(session,preparar(session,carga_emitida,usuario_admin["id"]))
        assert envio.estado=="enviado" and len(envio.intentos)==1
        assert len([c for c in smtp.calls if c[0]=="send"])==1


def test_endpoint_requiere_sesion_y_csrf(app,carga_emitida):
    response=app.test_client().post(f"/api/cargas/{carga_emitida}/enviar",json={"destinatario":"cliente@example.invalid"})
    assert response.status_code==401


def test_fallo_archivo_revierte_solicitud(client,app,carga_emitida,monkeypatch):
    import app.correo as module
    def fallar(envio):raise ValueError("Copia de correo no disponible.")
    monkeypatch.setattr(module,"archivar",fallar)
    assert client.post(f"/api/cargas/{carga_emitida}/enviar",json={"destinatario":"cliente@example.invalid"}).status_code==422
    with Session(app.extensions["db_engine"]) as session:
        assert session.scalar(select(func.count()).select_from(Envio))==0
