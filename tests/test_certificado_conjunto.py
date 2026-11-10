"""Certificado conjunto con planillas y firmas exclusivamente ficticias."""
from datetime import date
from email import policy
from email.parser import BytesParser
from hashlib import sha256
from io import BytesIO
import json
import os
from pathlib import Path
import shutil
import subprocess
from threading import Thread

from PIL import Image, ImageDraw
from pypdf import PdfReader
from reportlab.pdfgen import canvas
from sqlalchemy.orm import Session
from werkzeug.serving import make_server

from app.certificados.calendario import vencimiento
from app.models import Carga, Usuario
from tests.test_smtp_gmail import carga_emitida


def firma_ficticia():
    img = Image.new("RGBA", (160, 60))
    ImageDraw.Draw(img).line([(5, 40), (35, 10), (70, 45), (105, 18), (150, 28)], fill="black", width=3)
    out = BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


def configurar(app, usuario_admin, carga_emitida):
    out = BytesIO()
    pdf = canvas.Canvas(out)
    for texto in ("PLANILLA FICTICIA", "ANEXO FOTOGRÁFICO"):
        pdf.drawString(36, 720, texto)
        pdf.showPage()
    pdf.save()
    payload = out.getvalue()
    with Session(app.extensions["db_engine"]) as db:
        db.get(Usuario, usuario_admin["id"]).certificado_conjunto = True
        carga = db.get(Carga, carga_emitida)
        carga.pdf = payload
        carga.pdf_sha256 = sha256(payload).hexdigest()
        db.commit()


def datos(carga):
    return dict(carga_1=carga, unidad_1="meses", cantidad_1="1", fecha="2028-01-31",
                intervencion="2028-01-30", establecimiento="[Ejemplo] Sede ficticia",
                dictamen="[Ejemplo] Dictamen de prueba", confirmacion="si",
                firma=(BytesIO(firma_ficticia()), "firma.png"))


def test_vencimiento_calendario():
    assert vencimiento(date(2028, 1, 31), meses=1) == date(2028, 2, 29)
    assert vencimiento(date(2027, 1, 31), meses=1) == date(2027, 2, 28)
    assert vencimiento(date(2027, 12, 31), dias=7) == date(2028, 1, 7)


def test_permiso_en_servidor_y_propuesta(app, client, usuario_admin, carga_emitida):
    ruta = "/api/certificados/propuesta"
    assert client.get("/certificados").status_code == 403
    assert client.post(ruta, data=datos(carga_emitida)).status_code == 403
    assert client.get(f"/api/cargas/{carga_emitida}/pdf").status_code == 200
    configurar(app, usuario_admin, carga_emitida)
    assert client.get("/certificados").status_code == 200
    assert client.post(ruta, data=datos(carga_emitida) | {"confirmacion": ""}).status_code == 422
    resultado = client.post(ruta, data=datos(carga_emitida))
    assert resultado.status_code == 200, resultado.get_json()
    paginas = PdfReader(BytesIO(resultado.data)).pages
    assert len(paginas) == 3
    assert "PLANILLA FICTICIA" in paginas[0].extract_text()
    assert "ANEXO FOTOGRÁFICO" in paginas[1].extract_text()
    assert "Pág. 2 de 3" in paginas[1].extract_text()
    texto = paginas[2].extract_text()
    assert all(t in texto for t in ("CERTIFICADO DE INSPECCIÓN", "PROPUESTA / NO EMITIDO", "29/02/2028"))
    assert "Grupo BFM" not in texto
    correo = client.post(ruta, data=datos(carga_emitida) | {"salida": "correo_prueba"})
    assert correo.status_code == 200
    mensaje = BytesParser(policy=policy.default).parsebytes(correo.data)
    assert mensaje["To"] == "certificado@example.invalid"
    assert len(list(mensaje.iter_attachments())) == 1
    app.config["MODO_PILOTO"] = False
    assert client.post(ruta, data=datos(carga_emitida)).status_code == 409


def test_administrador_habilita_y_revoca(client, usuario_admin):
    ruta = "/api/admin/usuarios/" + usuario_admin["id"]
    respuesta = client.put(ruta, json=dict(rol="admin", activo=True, cliente_ids=[], certificado_conjunto=True))
    assert respuesta.status_code == 200 and respuesta.json["certificado_conjunto"] is True
    from tests.conftest import login_cliente
    app = client.application
    nuevo = login_cliente(app, usuario_admin["login"], usuario_admin["clave"])
    assert nuevo.get("/certificados").status_code == 200
    respuesta = nuevo.put(ruta, json=dict(rol="admin", activo=True, cliente_ids=[], certificado_conjunto=False))
    assert respuesta.status_code == 200 and respuesta.json["certificado_conjunto"] is False
    nuevo = login_cliente(app, usuario_admin["login"], usuario_admin["clave"])
    assert nuevo.get("/certificados").status_code == 403


def test_certificado_navegador(app, usuario_admin, carga_emitida, tmp_path):
    configurar(app, usuario_admin, carga_emitida)
    path = tmp_path / "firma_ficticia.png"
    path.write_bytes(firma_ficticia())
    server = make_server("127.0.0.1", 0, app, threaded=True)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    salida = Path(os.environ.get("RP_CERT_EVIDENCIA", str(tmp_path))).resolve()
    salida.mkdir(parents=True, exist_ok=True)
    try:
        result = subprocess.run([os.environ.get("READYPROOF_NODE") or shutil.which("node"),
                                 "tests/browser/certificado_conjunto.cjs"],
            input=json.dumps(dict(url=f"http://127.0.0.1:{server.server_port}", usuario=usuario_admin,
                                  firma=str(path), salida=str(salida))), text=True, capture_output=True, timeout=90)
        assert result.returncode == 0, result.stderr
        assert len(PdfReader(salida / "propuesta_conjunta.pdf").pages) == 3
    finally:
        server.shutdown()
        thread.join(timeout=10)
        server.server_close()
