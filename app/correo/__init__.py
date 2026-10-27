"""Cola de correo con adjunto inmutable, STARTTLS y registro de intentos."""
from datetime import timedelta
from email import policy
from email.message import EmailMessage
from email.parser import BytesParser
from email.utils import format_datetime
from hashlib import sha256
from io import BytesIO
import os
from pathlib import Path
import re
import smtplib
import ssl

from flask import current_app
from pypdf import PdfReader
from sqlalchemy import select

from ..models import Carga, Cliente, Envio, Intento, Planilla, RegistroAcceso, Retencion, Sistema, Usuario, UsuarioCliente, ahora

INTERVALO = timedelta(minutes=15)
MAX_INTENTOS = 3


def direccion(value):
    if not isinstance(value, str) or len(value)>254 or not re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?\.[A-Za-z]{2,63}", value):
        raise ValueError("Se requiere una dirección de correo simple válida, sin nombre ni saltos de línea.")
    return value


def modo_prueba():
    return current_app.config["MAIL_MODO_PRUEBA"]


def autorizado(session, envio):
    user=session.get(Usuario, envio.usuario_id) if envio.usuario_id else None
    carga=session.get(Carga, envio.carga_id)
    sistema=session.get(Sistema, carga.sistema_id)
    cliente=session.get(Cliente, sistema.cliente_id)
    permiso=user and user.activo and (user.rol=="admin" or session.get(UsuarioCliente,(user.id,cliente.id)))
    return bool(permiso and cliente.es_ejemplo and cliente.nombre.startswith("[Ejemplo] ")
        and sistema.designacion.startswith("[Ejemplo] ") and carga.estado=="emitida")


def programacion(session, envio):
    row=session.scalar(select(Retencion).where(Retencion.envio_id==envio.id))
    if row is None:
        row=Retencion(envio_id=envio.id,proximos_intentos=0,razon="bloqueado")
        session.add(row)
    return row


def preparar_envio(session, carga, destinatario, usuario_id, asunto, cuerpo):
    direccion(destinatario)
    if not isinstance(asunto,str) or not asunto.strip() or len(asunto)>200 or any(c in asunto for c in "\r\n"):
        raise ValueError("El asunto debe tener entre 1 y 200 caracteres, sin saltos de línea.")
    if not isinstance(cuerpo,str) or not cuerpo.strip() or len(cuerpo)>20000:
        raise ValueError("El cuerpo debe tener entre 1 y 20000 caracteres.")
    if carga.estado!="emitida" or not carga.pdf or not carga.emitida_en:
        raise ValueError("Solo se puede enviar una carga emitida con PDF.")
    if sha256(carga.pdf).hexdigest()!=carga.pdf_sha256:
        raise ValueError("La huella del PDF emitido no coincide.")
    try:
        pdf=PdfReader(BytesIO(carga.pdf))
        if not pdf.metadata or pdf.metadata.get("/ReadyproofIRAM")!="Planilla conforme a IRAM 3546:2011":
            raise ValueError("El PDF debe haberse emitido con la leyenda confirmada; no se reprocesan copias históricas.")
        if not pdf.pages or any("Planilla conforme a IRAM 3546:2011" not in page.extract_text() for page in pdf.pages):
            raise ValueError("El PDF emitido no contiene la leyenda confirmada en todas las páginas.")
    except ValueError:
        raise
    except Exception:
        raise ValueError("No se pudo validar el PDF emitido.") from None
    envio=Envio(carga_id=carga.id,usuario_id=usuario_id,destinatario=destinatario,
        asunto=asunto,cuerpo=cuerpo,pdf_copia=bytes(carga.pdf),pdf_sha256=carga.pdf_sha256,estado="pendiente")
    session.add(envio);session.flush()
    if not autorizado(session,envio):
        raise ValueError("No se autoriza este envío: se mantienen las restricciones de datos de ejemplo y de acceso por cliente.")
    emission=carga.emitida_en
    try: envio.retener_hasta=emission.replace(year=emission.year+3)
    except ValueError: envio.retener_hasta=emission.replace(year=emission.year+3,month=3,day=1)
    return envio


def crear_mensaje(envio):
    configured=os.getenv("MAIL_FROM") or os.getenv("SMTP_FROM") or os.getenv("SMTP_USER")
    if not modo_prueba() and not configured:
        raise ValueError("Configurar MAIL_FROM para SMTP.")
    sender=direccion(configured or "readyproof@example.invalid")
    message=EmailMessage(policy=policy.SMTP)
    message["From"]=sender;message["To"]=direccion(envio.destinatario)
    message["Subject"]=envio.asunto
    message["Date"]=format_datetime(ahora())
    message["Message-ID"]=f"<{envio.id}@{sender.split('@')[1]}>"
    message.set_content(envio.cuerpo)
    message.add_attachment(envio.pdf_copia,maintype="application",subtype="pdf",filename="readyproof-planilla.pdf")
    return message.as_bytes()


def archivar(envio):
    directory=Path(current_app.config["DIRECTORIO_CORREO"])
    directory.mkdir(parents=True,exist_ok=True)
    path=directory/(str(envio.id)+".eml")
    from tempfile import NamedTemporaryFile
    temporary=None
    try:
        with NamedTemporaryFile(dir=directory,suffix=".tmp",delete=False) as output:
            temporary=Path(output.name)
            output.write(envio.mensaje_eml);output.flush();os.fsync(output.fileno())
        try:os.link(temporary,path)
        except FileExistsError:
            if sha256(path.read_bytes()).hexdigest()!=envio.eml_sha256:
                raise ValueError("La copia de correo existente no coincide; se bloqueó el envío.")
    finally:
        if temporary is not None:temporary.unlink(missing_ok=True)
    return path


def registrar(session, envio, evento):
    carga=session.get(Carga,envio.carga_id);sistema=session.get(Sistema,carga.sistema_id)
    session.add(RegistroAcceso(usuario_id=envio.usuario_id,evento=evento,ruta="correo-worker",metodo="WORKER",
        estado_http=200,cliente_id=sistema.cliente_id,carga_id=carga.id,
        planilla_codigo=session.get(Planilla,carga.planilla_id).codigo,destinatario=envio.destinatario))


def send_email(session, envio, *, encolar=False, fecha=None):
    """Reserva antes de contactar SMTP; nunca registra credenciales ni respuestas crudas.

    Encolar prepara la copia y devuelve pendiente. La llamada del worker transmite.
    Un corte durante DATA es ambiguo: queda bloqueado para revisión, sin reenvío automático.
    """
    fecha=fecha or ahora()
    envio_id=envio.id if isinstance(envio,Envio) else envio
    session.flush()
    envio=session.scalar(select(Envio).where(Envio.id==envio_id).with_for_update(skip_locked=True).execution_options(populate_existing=True))
    if envio is None:session.rollback();return None
    retry=programacion(session,envio)
    if envio.estado in {"enviado","descartado"} or not autorizado(session,envio):
        if envio.estado not in {"enviado","descartado"}:envio.estado="fallo";retry.razon="bloqueado";retry.reintentado_en=None
        session.commit();return envio
    if envio.en_proceso_desde:
        if fecha-envio.en_proceso_desde>=INTERVALO:
            session.add(Intento(envio_id=envio.id,numero=envio.intentos_reservados,resultado="timeout",respuesta="Proceso interrumpido; aceptación SMTP desconocida. Revisión manual requerida."))
            envio.estado="fallo";envio.en_proceso_desde=None;retry.razon="bloqueado";retry.reintentado_en=None;retry.proximos_intentos=0
        session.commit();return envio
    bloqueado = envio.mensaje_eml is not None and retry.reintentado_en is None and not encolar
    if bloqueado or envio.intentos_reservados>=MAX_INTENTOS or (retry.reintentado_en is not None and retry.reintentado_en>fecha):
        session.commit();return envio
    if not envio.mensaje_eml:
        envio.mensaje_eml=crear_mensaje(envio);envio.eml_sha256=sha256(envio.mensaje_eml).hexdigest()
    if sha256(envio.mensaje_eml).hexdigest()!=envio.eml_sha256 or sha256(envio.pdf_copia).hexdigest()!=envio.pdf_sha256:
        raise ValueError("La copia inmutable del envío no coincide con su huella.")
    archivar(envio)
    if encolar:
        retry.razon="fallo_temporal";retry.reintentado_en=fecha;retry.proximos_intentos=2
        registrar(session,envio,"correo_encolado");session.commit();return envio
    envio.intentos_reservados+=1;numero=envio.intentos_reservados
    envio.en_proceso_desde=fecha;session.commit()
    resultado="ok";respuesta="Copia de prueba guardada; sin conexión SMTP."
    temporal=False;aceptado=False;data_iniciada=False;connection=None
    try:
        if not modo_prueba():
            host=os.getenv("SMTP_HOST","");user=os.getenv("SMTP_USER","");password=os.getenv("SMTP_PASSWORD","")
            if host!="smtp.gmail.com" or os.getenv("SMTP_PORT","587")!="587" or not user or not password:
                raise ValueError("Configuración SMTP incompleta o no corresponde a Gmail STARTTLS 587.")
            connection=smtplib.SMTP(host,587,timeout=30)
            connection.ehlo();connection.starttls(context=ssl.create_default_context());connection.ehlo()
            connection.login(user,password)
            message=BytesParser(policy=policy.SMTP).parsebytes(envio.mensaje_eml)
            data_iniciada=True
            refused=connection.send_message(message,from_addr=str(message["From"]),to_addrs=[envio.destinatario])
            if refused:raise smtplib.SMTPRecipientsRefused(refused)
            aceptado=True;respuesta="SMTP aceptó el mensaje; no confirma entrega en destino."
    except smtplib.SMTPRecipientsRefused as error:
        codes=[value[0] for value in error.recipients.values()]
        temporal=bool(codes) and all(400<=code<500 for code in codes)
        resultado="rechazado";respuesta="SMTP rechazó al destinatario temporalmente." if temporal else "SMTP rechazó al destinatario permanentemente."
    except smtplib.SMTPResponseException as error:
        temporal=400<=error.smtp_code<500
        resultado="rechazado";respuesta=f"SMTP {error.smtp_code}: respuesta temporal." if temporal else f"SMTP {error.smtp_code}: rechazo permanente."
    except (TimeoutError,OSError,smtplib.SMTPServerDisconnected):
        resultado="timeout";temporal=not data_iniciada
        respuesta="Conexión interrumpida antes de transmitir; reintento programado." if temporal else "Aceptación SMTP desconocida; revisión manual requerida."
    except (ValueError,smtplib.SMTPException):
        resultado="rechazado";respuesta="Configuración, autenticación o capacidad TLS inválida; revisar localmente."
    finally:
        if connection is not None:
            try:connection.quit()
            except (OSError,smtplib.SMTPException):
                try:connection.close()
                except OSError:pass
    session.expire_all()
    envio=session.scalar(select(Envio).where(Envio.id==envio_id).with_for_update())
    retry=programacion(session,envio)
    session.add(Intento(envio_id=envio.id,numero=numero,intentado_en=fecha,resultado=resultado,respuesta=respuesta))
    envio.en_proceso_desde=None
    envio.estado="enviado" if aceptado else ("pendiente" if resultado=="ok" else "fallo")
    if aceptado:envio.enviado_en=ahora()
    retry.proximos_intentos=MAX_INTENTOS-numero if temporal and numero<MAX_INTENTOS else 0
    retry.reintentado_en=fecha+INTERVALO if retry.proximos_intentos else None
    retry.razon="fallo_temporal" if retry.proximos_intentos else ("correo_invalido" if resultado=="rechazado" else "bloqueado")
    registrar(session,envio,"correo_prueba" if modo_prueba() else "correo_intento")
    session.commit();return envio


def reintentar_envios(*, fecha=None):
    fecha=fecha or ahora();count=0
    factory=current_app.extensions["db_sessions"]
    with factory() as session:
        ids=list(session.scalars(select(Envio.id).where(Envio.usuario_id.is_not(None),Envio.mensaje_eml.is_not(None),Envio.estado.in_(("pendiente","fallo")))))
    for key in ids:
        with factory() as session:
            envio=session.get(Envio,key)
            before=envio.intentos_reservados
            try:result=send_email(session,envio,fecha=fecha)
            except (ValueError,OSError):
                session.rollback()
                envio=session.get(Envio,key);envio.estado="fallo"
                row=programacion(session,envio);row.razon="bloqueado";row.reintentado_en=None;row.proximos_intentos=0
                registrar(session,envio,"correo_bloqueado");session.commit();continue
            if result and result.intentos_reservados>before:count+=1
    return count


def registrar_bounce(session, envio_id, actor_id):
    """Registra un aviso de no entrega revisado por un administrador, sin leer Gmail."""
    actor=session.get(Usuario,actor_id)
    if not actor or not actor.activo or actor.rol!="admin":
        raise ValueError("Se requiere un administrador activo para registrar un aviso de no entrega.")
    envio=session.scalar(select(Envio).where(Envio.id==envio_id).with_for_update())
    if not envio or envio.estado!="enviado":
        raise ValueError("Solo se registra bounce de un mensaje previamente aceptado por SMTP.")
    intento=session.scalar(select(Intento).where(Intento.envio_id==envio_id).order_by(Intento.numero.desc()))
    intento.resultado="bounce"
    intento.respuesta="SMTP aceptó el mensaje; un administrador registró posteriormente un aviso de no entrega."
    envio.estado="fallo"
    retry=programacion(session,envio);retry.razon="correo_invalido";retry.reintentado_en=None;retry.proximos_intentos=0
    carga=session.get(Carga,envio.carga_id);sistema=session.get(Sistema,carga.sistema_id)
    session.add(RegistroAcceso(usuario_id=actor.id,evento="correo_bounce",ruta="correo-bounce",metodo="CLI",estado_http=200,
        cliente_id=sistema.cliente_id,carga_id=carga.id,destinatario=envio.destinatario))
    session.commit()
    return envio
