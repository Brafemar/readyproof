"""Emisión local con decisiones y firmas ficticias."""
from datetime import date
from hashlib import sha256
from io import BytesIO
import os
from pathlib import Path

from alembic import command
from alembic.config import Config
from pypdf import PdfReader
import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import hash_clave
from app.carga.servicios import preparar_numero_emision
from app.db import sesion
from app.models import Carga, EmisionCertificado, NumeroRegistroContador, Sistema, Usuario
from tests.conftest import login_cliente
from tests.test_certificado_conjunto import datos
from tests.test_firma_certificado import cargar, dos_cargas, firma, habilitar, privado
from tests.test_smtp_gmail import carga_emitida

EMITIR = "/api/certificados/emitir"


@pytest.mark.parametrize("condicion", ["APROBADO", "NO APROBADO"])
def test_emite_certificado_con_vigencia(app, client, privado, usuario_admin, carga_emitida, condicion):
    app.config.update(MODO_PILOTO=False, CERTIFICADO_CONJUNTO_HABILITADO=True)
    segunda = dos_cargas(app, carga_emitida)
    client = habilitar(app, client, usuario_admin)
    assert cargar(client, firma()).status_code == 201
    formulario = datos(carga_emitida) | {
        "carga_2": segunda, "cantidad_2": "7", "unidad_2": "dias",
        "condicion": condicion,
    }
    if condicion == "APROBADO":
        for campo in ("cantidad_1", "unidad_1", "cantidad_2", "unidad_2"):
            del formulario[campo]
        formulario["periodicidad"] = "mensual"
    assert client.post(EMITIR, data=formulario | {"periodicidad": "7"}).status_code == 422
    respuesta = client.post(EMITIR, data=formulario)
    assert respuesta.status_code == 200, respuesta.json
    assert respuesta.mimetype == "application/pdf"
    paginas = PdfReader(BytesIO(respuesta.data)).pages
    assert len(paginas) == 5
    texto = paginas[4].extract_text()
    assert "EMITIDO" in texto.splitlines()
    assert f"CONDICIÓN FINAL: {condicion}" in texto.splitlines()
    assert "PROPUESTA / NO EMITIDO" not in texto and "SIN VALIDEZ DE EMISIÓN" not in texto
    assert texto.splitlines().count("29/02/2028") == 1
    assert "06/03/2028" not in texto and "28/02/2028" not in texto
    assert "Mensual (30 días)" in texto and "VIGENCIA CONJUNTA" in texto
    assert "[Ejemplo] Dictamen de prueba" in texto
    assert "T.C. 3 AÑOS · Pág. 5 de 5" in texto
    assert "[NNNN]" not in texto and "[R]" not in texto
    assert any(im.image.size == (160, 60) for im in paginas[4].images)
    with Session(app.extensions["db_engine"]) as db:
        registro = db.scalars(select(EmisionCertificado)).one()
        assert f"Registro {registro.numero_registro:04d} · Revisión 1" in texto
        assert registro.revision == 1
        assert registro.actor_id == usuario_admin["id"] and registro.condicion == condicion
        assert registro.fecha_emision == date(2028, 1, 31)
        assert registro.planillas == [carga_emitida, segunda]
        assert registro.pdf == respuesta.data and registro.pdf_sha256 == sha256(respuesta.data).hexdigest()
    if salida := os.environ.get("RP_EMISION_EVIDENCIA"):
        carpeta = Path(salida)
        carpeta.mkdir(parents=True, exist_ok=True)
        (carpeta / f"emitido_{condicion.lower().replace(' ', '_')}.pdf").write_bytes(respuesta.data)


def test_registro_global_y_reemision(app, client, privado, usuario_admin, carga_emitida):
    app.config["CERTIFICADO_CONJUNTO_HABILITADO"] = True
    client = habilitar(app, client, usuario_admin)
    assert cargar(client, firma()).status_code == 201
    engine = app.extensions["db_engine"]
    with app.app_context():
        db = sesion()
        planilla = db.get(Carga, carga_emitida)
        preparar_numero_emision(planilla)
        anterior = planilla.numero_registro
        db.commit()

    formulario = datos(carga_emitida) | {"condicion": "APROBADO"}
    assert b'name="registro"' in client.get("/certificados").data
    primera = client.post(EMITIR, data=formulario)
    segunda = client.post(EMITIR, data=formulario)
    assert client.post(EMITIR, data=formulario | {"registro": str(anterior)}).status_code == 404
    tercera = client.post(EMITIR, data=formulario | {"registro": str(anterior + 1), "condicion": "NO APROBADO"})
    for respuesta, numero, revision in (
        (primera, anterior + 1, 1), (segunda, anterior + 2, 1), (tercera, anterior + 1, 2),
    ):
        assert respuesta.status_code == 200
        texto = PdfReader(BytesIO(respuesta.data)).pages[-1].extract_text()
        assert f"Registro {numero:04d} · Revisión {revision}" in texto
        assert "[NNNN]" not in texto and "[R]" not in texto

    with Session(engine) as db:
        filas = db.scalars(select(EmisionCertificado).order_by(
            EmisionCertificado.numero_registro, EmisionCertificado.revision)).all()
        assert [(r.numero_registro, r.revision, r.pdf) for r in filas] == [
            (anterior + 1, 1, primera.data), (anterior + 1, 2, tercera.data),
            (anterior + 2, 1, segunda.data),
        ]
        assert db.get(NumeroRegistroContador, 1).ultimo == anterior + 2


def test_permiso_firma_y_revocacion(app, client, privado, carga_emitida):
    app.config["CERTIFICADO_CONJUNTO_HABILITADO"] = True
    formulario = datos(carga_emitida) | {"condicion": "APROBADO", "dictamen": ""}
    clave = "clave-ficticia-emision"
    with Session(app.extensions["db_engine"], expire_on_commit=False) as db:
        tecnico = Usuario(login="emisor-ejemplo", nombre="[Ejemplo] Emisor", rol="tecnico",
                          clave_hash=hash_clave(clave))
        db.add(tecnico)
        carga = db.get(Carga, carga_emitida)
        cliente_id = db.get(Sistema, carga.sistema_id).cliente_id
        db.commit()
    ruta = f"/api/admin/usuarios/{tecnico.id}"
    cambios = dict(rol="tecnico", activo=True, cliente_ids=[cliente_id], certificado_conjunto=True)
    sin_permiso = login_cliente(app, tecnico.login, clave)
    assert b"Emitir certificado" not in sin_permiso.get("/certificados").data
    assert b'href="/certificados"' not in sin_permiso.get("/").data
    assert sin_permiso.post(EMITIR, data=formulario).status_code == 403
    assert sin_permiso.put(ruta, json=cambios).status_code == 403
    assert client.put(ruta, json=cambios).json["certificado_conjunto"] is True
    autorizado = login_cliente(app, tecnico.login, clave)
    vista = autorizado.get("/certificados")
    assert vista.status_code == 200 and b">Emitir certificado</button>" in vista.data
    assert autorizado.post(EMITIR, data=formulario).status_code == 503
    assert autorizado.post(EMITIR, data=formulario | {"condicion": ""}).status_code == 422
    assert cargar(client, firma()).status_code == 201
    assert autorizado.post(EMITIR, data=formulario).status_code == 200
    assert client.put(ruta, json=cambios | {"certificado_conjunto": False}).json["certificado_conjunto"] is False
    revocado = login_cliente(app, tecnico.login, clave)
    assert b"Emitir certificado" not in revocado.get("/certificados").data
    assert revocado.post(EMITIR, data=formulario).status_code == 403
    with Session(app.extensions["db_engine"]) as db:
        assert db.scalars(select(EmisionCertificado)).one().actor_id == tecnico.id


@pytest.mark.parametrize("duplicado", [False, True])
def test_permiso_inicial_vinculado_por_id(app, duplicado):
    engine = app.extensions["db_engine"]
    cfg = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
    with engine.begin() as connection:
        cfg.attributes["connection"] = connection
        command.downgrade(cfg, "023_firma_certificado")
    with Session(engine) as db:
        hash_prueba = hash_clave("clave-ficticia-inicial")
        for login, email in (
            ("emisor-inicial", "Readyproof.Ar@gmail.com"),
            ("otra-cuenta", "readyproof.ar@gmail.com" if duplicado else "otra@example.invalid"),
        ):
            db.add(Usuario(login=login, nombre="[Ejemplo] Cuenta", email=email, rol="admin",
                           clave_hash=hash_prueba))
        db.commit()
    with engine.begin() as connection:
        cfg.attributes["connection"] = connection
        command.upgrade(cfg, "head")
    with Session(engine) as db:
        cuenta, otra = db.scalars(select(Usuario).order_by(Usuario.login)).all()
        assert cuenta.certificado_conjunto is (not duplicado)
        assert otra.certificado_conjunto is False
        cuenta.email = "emisor@example.invalid"
        otra.email = "readyproof.ar@gmail.com"
        db.commit()
        assert cuenta.certificado_conjunto is (not duplicado)
        assert otra.certificado_conjunto is False
