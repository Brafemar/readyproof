"""Integración de la firma gráfica ficticia con PostgreSQL y el disco privado."""
from hashlib import sha256
from io import BytesIO
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
from threading import Thread

from PIL import Image, ImageDraw
from pypdf import PdfReader
import pytest
from reportlab.pdfgen import canvas
from sqlalchemy import event, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from werkzeug.serving import make_server

from app.auth import hash_clave
from app.certificados.pdf import PLANTILLA
from app.models import Auditoria, Carga, FirmaCertificadoActiva, Usuario
from tests.conftest import login_cliente
from tests.test_certificado_conjunto import datos
from tests.test_smtp_gmail import carga_emitida

RUTA = "/api/admin/firma-certificado"


@pytest.fixture
def privado(app, tmp_path):
    app.instance_path = str(tmp_path / "instance")
    return Path(app.instance_path) / "firmas_certificado"


def codificar(imagen, formato="PNG", **opciones):
    buffer = BytesIO()
    imagen.save(buffer, formato, **opciones)
    return buffer.getvalue()


def firma(y=21):
    imagen = Image.new("RGBA", (160, 60))
    ImageDraw.Draw(imagen).line([(5, y), (43, 9), (80, 49), (150, 22)], fill="black", width=3)
    return codificar(imagen)


def cargar(client, datos):
    return client.post(RUTA, data={"firma": (BytesIO(datos), "firma.png", "image/png")})


def estado(client):
    return client.post(RUTA + "/estado").json


def info(path):
    st = path.stat()
    return {"modo": format(stat.S_IMODE(st.st_mode), "04o"), "uid": st.st_uid, "gid": st.st_gid,
            "propietario": path.owner(), "grupo": path.group()}


def evidencia(nombre, contenido):
    salida = os.environ.get("RP_FIRMA_EVIDENCIA")
    if salida:
        destino = Path(salida)
        destino.mkdir(parents=True, exist_ok=True)
        with (destino / nombre).open("x", encoding="utf-8") as f:
            json.dump(contenido, f, ensure_ascii=False, indent=2)


def test_alta_y_reemplazo_real(app, client, privado, usuario_admin):
    assert estado(client) == {"activa": False}
    primera = cargar(client, firma())
    assert primera.status_code == 201, primera.json
    h1 = primera.json["sha256"]
    anterior = privado / (h1 + ".png")
    assert sha256(anterior.read_bytes()).hexdigest() == h1
    segunda = cargar(client, firma(31))
    assert segunda.status_code == 200
    h2 = segunda.json["sha256"]
    nueva = privado / (h2 + ".png")
    assert h2 != h1 and sha256(nueva.read_bytes()).hexdigest() == h2
    assert sha256(anterior.read_bytes()).hexdigest() == h1
    assert estado(client)["sha256"] == h2
    datos_disco = {key: info(path) for key,path in (("directorio", privado), ("anterior", anterior), ("nueva", nueva))}
    assert [item["modo"] for item in datos_disco.values()] == ["0700", "0600", "0600"]
    assert all((item["uid"],item["gid"])==(os.geteuid(),os.getegid()) for item in datos_disco.values())
    with Session(app.extensions["db_engine"]) as db:
        filas = db.scalars(select(Auditoria).where(Auditoria.tabla == "firma_certificado_activa")
                           .order_by(Auditoria.timestamp)).all()
        assert len(filas) == 2
        assert all(row.usuario_id == usuario_admin["id"] and row.timestamp for row in filas)
        assert filas[0].datos_anterior is None and filas[0].datos_nuevo["sha256"] == h1
        assert filas[1].datos_anterior == {"sha256":h1}
        assert filas[1].datos_nuevo == {"sha256":h2,"tamano":nueva.stat().st_size,
                                       "resultado":"activada","operacion":"reemplazo"}
    evidencia("permisos_hashes.json", {"permisos":datos_disco, "hash_anterior":h1, "hash_nuevo":h2,
                                     "version_anterior_conservada":True, "auditoria_eventos":2})


def invalido(caso):
    if caso == "jpeg":
        return codificar(Image.new("RGB", (20,20)), "JPEG")
    if caso == "truncado":
        return firma()[:35]
    if caso == "tamano":
        return firma() + b"0" * 262144
    if caso == "dimensiones":
        return codificar(Image.new("RGBA", (2401, 10)))
    if caso == "opaco":
        return codificar(Image.new("RGBA", (20,20), "black"))
    im = Image.new("RGBA", (20,20))
    if caso == "transparente":
        return codificar(im)
    if caso == "blanco":
        im.putpixel((8,8),(255,255,255,255))
        return codificar(im)
    assert caso == "animado"
    im.putpixel((8,8),(0,0,0,255))
    return codificar(im, save_all=True, append_images=[Image.new("RGBA",(20,20),"red")], duration=100)


@pytest.mark.parametrize("caso", ["jpeg","truncado","tamano","dimensiones","opaco","transparente","blanco","animado"])
def test_png_invalido_no_escribe(client, privado, caso):
    assert cargar(client, invalido(caso)).status_code == 422
    assert not privado.exists()


def test_tecnico_no_escribe(app, privado):
    with Session(app.extensions["db_engine"]) as db:
        db.add(Usuario(login="tecnico-firma",nombre="[Ejemplo] Técnico",rol="tecnico",
                       clave_hash=hash_clave("clave-ficticia-solo-pruebas")))
        db.commit()
    client = login_cliente(app, "tecnico-firma", "clave-ficticia-solo-pruebas")
    assert client.get("/admin/firma-certificado").status_code == 403
    assert client.post(RUTA + "/estado").status_code == 403
    assert cargar(client, firma()).status_code == 403
    assert not privado.exists()


def test_admin_sin_csrf_no_escribe(client, privado):
    client.environ_base.pop("HTTP_X_CSRF_TOKEN")
    assert client.post(RUTA + "/estado").status_code == 403
    assert cargar(client, firma()).status_code == 403
    assert not privado.exists()


def test_auditoria_fallida_no_activa(app, client, privado):
    inicial = cargar(client, firma())
    assert inicial.status_code == 201
    h1 = inicial.json["sha256"]

    def falla_auditoria(session, *_):
        if any(isinstance(row, Auditoria) and row.tabla=="firma_certificado_activa" for row in session.new):
            raise SQLAlchemyError("Fallo de auditoría simulado")

    factory = app.extensions["db_sessions"]
    event.listen(factory, "before_flush", falla_auditoria)
    try:
        assert cargar(client, firma(35)).status_code == 503
    finally:
        event.remove(factory, "before_flush", falla_auditoria)
    assert estado(client)["sha256"] == h1
    assert sha256((privado / (h1 + ".png")).read_bytes()).hexdigest() == h1
    with Session(app.extensions["db_engine"]) as db:
        assert db.get(FirmaCertificadoActiva, 1).sha256 == h1
        assert len(db.scalars(select(Auditoria).where(Auditoria.tabla == "firma_certificado_activa")).all()) == 1


def pdf_prueba(numero):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    for texto in (f"PLANILLA FICTICIA {numero}", "ANEXO FOTOGRÁFICO",):
        pdf.drawString(36, 720, texto)
        if texto.startswith("ANEXO"):
            pdf.drawString(36, 700, f"ANEXO FICTICIO {numero}")
        pdf.showPage()
    pdf.save()
    return buffer.getvalue()


def dos_cargas(app, carga_emitida):
    with Session(app.extensions["db_engine"],expire_on_commit=False) as db:
        primera = db.get(Carga, carga_emitida)
        primera.pdf = pdf_prueba(1)
        primera.pdf_sha256 = sha256(primera.pdf).hexdigest()
        payload = pdf_prueba(2)
        segunda = Carga(sistema_id=primera.sistema_id, planilla_id=primera.planilla_id,
                        creada_por_id=primera.creada_por_id, estado="emitida", datos=primera.datos,
                        emitida_en=primera.emitida_en, pdf=payload, pdf_sha256=sha256(payload).hexdigest())
        db.add(segunda)
        db.commit()
        return segunda.id


def habilitar(app, client, usuario):
    r = client.put("/api/admin/usuarios/" + usuario["id"], json={
        "rol":"admin","activo":True,"cliente_ids":[],"certificado_conjunto":True})
    assert r.status_code==200 and r.json["certificado_conjunto"]
    return login_cliente(app, usuario["login"], usuario["clave"])


def verificar_pdf(payload):
    paginas = PdfReader(BytesIO(payload)).pages
    assert len(paginas) == 5
    for i, valor in enumerate(("PLANILLA FICTICIA 1","PLANILLA FICTICIA 2",
                               "ANEXO FICTICIO 1","ANEXO FICTICIO 2","CERTIFICADO DE INSPECCIÓN")):
        assert valor in paginas[i].extract_text()
    texto = paginas[-1].extract_text()
    assert "PROPUESTA / NO EMITIDO" in texto and "Mat. A 11576" in texto and "Mat. “A” 11576" not in texto
    assert texto.splitlines().count("29/02/2028") == 1 and "07/02/2028" not in texto
    assert "Mensual (30 días)" in texto and "VIGENCIA CONJUNTA" in texto
    assert "Lic. Martín Marcos A. Sánchez" in texto
    plantilla = PdfReader(PLANTILLA).pages[0]
    assert [(imagen.name, imagen.data) for imagen in paginas[-1].images] == [
        (imagen.name, imagen.data) for imagen in plantilla.images
    ]


def test_propuesta_dos_planillas_y_permiso(app, client, privado, usuario_admin, carga_emitida):
    segunda = dos_cargas(app, carga_emitida)
    app.config.update(MODO_PILOTO=False, CERTIFICADO_CONJUNTO_HABILITADO=True)
    cuerpo = datos(carga_emitida) | {"carga_2":segunda,"cantidad_2":"7","unidad_2":"dias"}
    ruta = "/api/certificados/propuesta"
    assert client.post(ruta, data=cuerpo).status_code == 403
    client = habilitar(app,client,usuario_admin)
    r=client.post(ruta,data=cuerpo)
    assert r.status_code==200, r.json
    verificar_pdf(r.data)
    assert not privado.exists()
    with Session(app.extensions["db_engine"]) as db:
        db.get(Usuario, usuario_admin["id"]).rol = "tecnico"
        db.commit()
    tecnico = login_cliente(app, usuario_admin["login"], usuario_admin["clave"])
    assert tecnico.get("/certificados").status_code == 200
    assert tecnico.post(ruta, data=cuerpo).status_code == 403


def test_propuesta_firma_activa_opcional(app, client, privado, usuario_admin, carga_emitida):
    segunda = dos_cargas(app, carga_emitida)
    app.config.update(MODO_PILOTO=False, CERTIFICADO_CONJUNTO_HABILITADO=True)
    client = habilitar(app, client, usuario_admin)
    cuerpo = datos(carga_emitida) | {"carga_2": segunda, "cantidad_2": "7", "unidad_2": "dias"}
    ruta = "/api/certificados/propuesta"
    sin_firma = client.post(ruta, data=cuerpo)
    assert sin_firma.status_code == 200
    verificar_pdf(sin_firma.data)
    assert not privado.exists()

    imagen = firma()
    alta = cargar(client, imagen)
    assert alta.status_code == 201
    assert info(privado)["modo"] == "0700"
    assert info(privado / (alta.json["sha256"] + ".png"))["modo"] == "0600"
    con_firma = client.post(ruta, data=cuerpo)
    assert con_firma.status_code == 200
    paginas = PdfReader(BytesIO(con_firma.data)).pages
    assert len(paginas) == 5
    assert paginas[4].extract_text() == PdfReader(BytesIO(sin_firma.data)).pages[4].extract_text()
    base = len(PdfReader(PLANTILLA).pages[0].images)
    assert len(paginas[4].images) == base + 1
    esperada = Image.open(BytesIO(imagen)).convert("RGBA")
    assert any(im.image.convert("RGBA").size == esperada.size and
               im.image.convert("RGBA").tobytes() == esperada.tobytes() for im in paginas[4].images)
    assert estado(client)["sha256"] == alta.json["sha256"]
    salida = os.environ.get("RP_FIRMA_EVIDENCIA")
    if salida:
        out = Path(salida)
        out.mkdir(parents=True, exist_ok=True)
        (out / "propuesta_con_firma.pdf").write_bytes(con_firma.data)
        (out / "propuesta_sin_firma.pdf").write_bytes(sin_firma.data)


@pytest.mark.parametrize("caso", ["jpeg", "truncado", "tamano", "dimensiones",
                                 "opaco", "transparente", "blanco", "animado"])
def test_propuesta_rechaza_firma_activa_invalida(app, client, privado, usuario_admin, carga_emitida, caso):
    app.config.update(MODO_PILOTO=False, CERTIFICADO_CONJUNTO_HABILITADO=True)
    client = habilitar(app, client, usuario_admin)
    assert cargar(client, firma()).status_code == 201
    contenido = invalido(caso)
    huella = sha256(contenido).hexdigest()
    archivo = privado / (huella + ".png")
    with archivo.open("xb") as stream:
        stream.write(contenido)
    archivo.chmod(0o600)
    with Session(app.extensions["db_engine"]) as db:
        activa = db.get(FirmaCertificadoActiva, 1)
        activa.sha256, activa.tamano = huella, len(contenido)
        db.commit()
    respuesta = client.post("/api/certificados/propuesta", data=datos(carga_emitida))
    assert respuesta.status_code == 503
    assert respuesta.mimetype == "application/json"
    assert archivo.read_bytes() == contenido


@pytest.mark.parametrize("caso", ["directorio", "archivo", "huella", "ausente"])
def test_propuesta_rechaza_almacen_firma_inseguro(app, client, privado, usuario_admin, carga_emitida, caso):
    app.config.update(MODO_PILOTO=False, CERTIFICADO_CONJUNTO_HABILITADO=True)
    client = habilitar(app, client, usuario_admin)
    alta = cargar(client, firma())
    assert alta.status_code == 201
    archivo = privado / (alta.json["sha256"] + ".png")
    if caso == "directorio":
        privado.chmod(0o755)
    elif caso == "archivo":
        archivo.chmod(0o644)
    elif caso == "huella":
        archivo.write_bytes(b"archivo modificado")
    else:
        with Session(app.extensions["db_engine"]) as db:
            db.get(FirmaCertificadoActiva, 1).sha256 = "0" * 64
            db.commit()
    respuesta = client.post("/api/certificados/propuesta", data=datos(carga_emitida))
    assert respuesta.status_code == 503
    assert respuesta.mimetype == "application/json"


def test_navegador_firma_y_certificado(app, client, privado, usuario_admin, carga_emitida, tmp_path):
    segunda = dos_cargas(app, carga_emitida)
    app.config.update(MODO_PILOTO=False, CERTIFICADO_CONJUNTO_HABILITADO=True)
    habilitar(app,client,usuario_admin)
    salida = Path(os.environ.get("RP_FIRMA_EVIDENCIA", str(tmp_path))).resolve()
    salida.mkdir(parents=True,exist_ok=True)
    server=make_server("127.0.0.1",0,app,threaded=True)
    thread=Thread(target=server.serve_forever,daemon=True)
    thread.start()
    try:
        result=subprocess.run([os.environ.get("READYPROOF_NODE") or shutil.which("node"),
                               "tests/browser/certificado_conjunto.cjs"],input=json.dumps({
            "url":f"http://127.0.0.1:{server.server_port}","usuario":usuario_admin,"salida":str(salida),
            "verificarFirmaVacia":True,"primera":carga_emitida,"segunda":segunda}),
            text=True,capture_output=True,timeout=100)
        assert result.returncode==0,result.stderr
        verificar_pdf((salida/"propuesta_conjunta.pdf").read_bytes())
        assert not privado.exists()
    finally:
        server.shutdown()
        thread.join(timeout=10)
        server.server_close()
