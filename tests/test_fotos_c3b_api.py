"""API real de fotos/anotaciones y validación de C3b, sin emisión ni correo."""
from hashlib import sha256
from io import BytesIO
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
from threading import Thread

from flask import Flask
from PIL import Image
import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.exceptions import BadRequest
from werkzeug.serving import make_server

from app.auth import hash_clave
from app.fotos.anotaciones import validar_anotaciones
from app.models import Auditoria, Carga, Usuario
from tests.conftest import login_cliente

ROOT = Path(__file__).resolve().parents[1]


def marca(codigo="✓", texto="", **extra):
    return dict(x=.25, y=.5, codigo=codigo, texto=texto, **extra)


@pytest.fixture
def foto_c3b(client, catalogo, datos_api):
    _, sistema, planilla = catalogo
    def carga():
        response = client.post("/api/cargas", json=dict(sistema_id=sistema["id"], planilla_id=planilla["id"], datos=datos_api))
        assert response.status_code == 201, response.get_json()
        return response.get_json()["id"]
    carga_id = carga()
    output = BytesIO()
    Image.new("RGB", (640, 480), "white").save(output, format="JPEG")
    blob = output.getvalue()
    response = client.post(f"/api/cargas/{carga_id}/fotos", data=blob, content_type="image/jpeg")
    assert response.status_code == 201, response.get_json()
    foto = response.get_json()
    return dict(carga_id=carga_id, foto_id=foto["id"], url=f"/api/cargas/{carga_id}/fotos/{foto['id']}", blob=blob, otra_carga=carga)


def guardar(client, foto, marcas, **kwargs):
    return client.post(foto["url"] + "/anotaciones", json={"anotaciones": marcas}, **kwargs)


def test_guardar_leer_reemplazar_y_vaciar_con_auditoria(app, client, foto_c3b):
    first = guardar(client, foto_c3b, [marca("O", "[Ejemplo] Revisar", numero=88), marca("NA")])
    assert first.status_code == 200
    rows = first.get_json()
    assert [row["numero"] for row in rows] == [1, 2]
    assert rows == client.get(foto_c3b["url"] + "/anotaciones").get_json()
    second = guardar(client, foto_c3b, [marca("X", "[Ejemplo] Sin acceso")])
    assert second.status_code == 200
    assert len(second.get_json()) == 1 and second.get_json()[0]["numero"] == 1
    assert guardar(client, foto_c3b, []).get_json() == []
    with Session(app.extensions["db_engine"]) as db:
        audits = list(db.scalars(select(Auditoria).where(Auditoria.tabla == "fotos_anotacion", Auditoria.registro_id == foto_c3b["foto_id"])))
        assert len(audits) == 3
        assert all(row.usuario_id and row.accion == "UPDATE" for row in audits)
        assert audits[0].datos_anterior["anotaciones"] == []


@pytest.mark.parametrize("changes,error", [
    ({"codigo": "z"}, "código válido"), ({"codigo": "O"}, "completá el texto"),
    ({"codigo": "X"}, "completá el texto"), ({"codigo": "O", "texto": "   "}, "completá el texto"),
    ({"texto": "[Ejemplo] " + "á" * 131}, "140"),
    ({"codigo": "NA", "texto": "[Ejemplo] " + "á" * 131}, "140"),
    ({"texto": None}, "140"), ({"x": -.01}, "posición x"),
    ({"y": 1.01}, "posición y"), ({"x": True}, "posición x"),
])
def test_rechazos_no_borran_marcas_anteriores(client, foto_c3b, changes, error):
    before = guardar(client, foto_c3b, [marca()]).get_json()
    invalid = {**marca(), **changes}
    response = guardar(client, foto_c3b, [marca("NA"), invalid])
    assert response.status_code == 400
    assert error in response.get_json()["error"]
    assert client.get(foto_c3b["url"] + "/anotaciones").get_json() == before


@pytest.mark.parametrize("method,suffix", [("get", "/anotaciones"), ("post", "/anotaciones"), ("get", "/imagen")])
def test_sin_sesion_rechazado(app, foto_c3b, method, suffix):
    unauthenticated = app.test_client()
    response = getattr(unauthenticated, method)(foto_c3b["url"] + suffix, **({"json": {"anotaciones": []}} if method == "post" else {}))
    assert response.status_code == 401


@pytest.mark.parametrize("token", [None, "invalido"])
def test_csrf_obligatorio(client, foto_c3b, token):
    client.environ_base.pop("HTTP_X_CSRF_TOKEN", None)
    response = guardar(client, foto_c3b, [], headers={} if token is None else {"X-CSRF-Token": token})
    assert response.status_code == 403


@pytest.mark.parametrize("method,suffix", [("get", "/anotaciones"), ("post", "/anotaciones"), ("get", "/imagen")])
def test_foto_de_otra_carga_rechazada(client, foto_c3b, method, suffix):
    otra = foto_c3b["otra_carga"]()
    url = f"/api/cargas/{otra}/fotos/{foto_c3b['foto_id']}" + suffix
    response = getattr(client, method)(url, **({"json": {"anotaciones": []}} if method == "post" else {}))
    assert response.status_code == 404


@pytest.mark.parametrize("method,suffix", [("get", "/anotaciones"), ("post", "/anotaciones"), ("get", "/imagen")])
def test_cliente_no_asignado_no_accede(app, foto_c3b, method, suffix):
    password = secrets.token_urlsafe(24)
    with Session(app.extensions["db_engine"]) as db:
        user = Usuario(login="tecnico-c3b", nombre="[Ejemplo] Técnico sin asignación", rol="tecnico", clave_hash=hash_clave(password))
        db.add(user)
        db.commit()
    technical = login_cliente(app, "tecnico-c3b", password)
    response = getattr(technical, method)(foto_c3b["url"] + suffix, **({"json": {"anotaciones": []}} if method == "post" else {}))
    assert response.status_code == 404


def test_imagen_exacta_no_cacheable(client, foto_c3b):
    response = client.get(foto_c3b["url"] + "/imagen")
    assert response.status_code == 200 and response.mimetype == "image/jpeg"
    assert response.data == foto_c3b["blob"]
    assert sha256(response.data).hexdigest() == sha256(foto_c3b["blob"]).hexdigest()
    assert response.headers["Cache-Control"] == "no-store"
    assert response.headers["X-Content-Type-Options"] == "nosniff"


@pytest.mark.parametrize("estado", ["finalizada", "emitida"])
def test_no_editar_carga_cerrada(app, client, foto_c3b, estado):
    before = guardar(client, foto_c3b, [marca()]).get_json()
    with Session(app.extensions["db_engine"]) as db:
        db.get(Carga, foto_c3b["carga_id"]).estado = estado
        db.commit()
    response = guardar(client, foto_c3b, [marca("NA")])
    assert response.status_code == 409
    assert "desbloqueo" in response.get_json()["error"]
    assert client.get(foto_c3b["url"] + "/anotaciones").get_json() == before


def test_error_durante_reemplazo_revierte_transaccion(app, client, foto_c3b, monkeypatch):
    before = guardar(client, foto_c3b, [marca()]).get_json()
    from app.fotos import rutas
    def fallo(*args, **kwargs):
        raise RuntimeError("[Ejemplo] fallo controlado de auditoría")
    monkeypatch.setattr(rutas, "registrar_auditoria", fallo)
    with pytest.raises(RuntimeError, match="fallo controlado"):
        guardar(client, foto_c3b, [marca("NA")])
    assert client.get(foto_c3b["url"] + "/anotaciones").get_json() == before


def test_version_anterior_no_pisa_cambios(client, foto_c3b):
    version = client.get(foto_c3b["url"] + "/anotaciones").headers["ETag"]
    current = guardar(client, foto_c3b, [marca("NA")], headers={"If-Match": version})
    response = guardar(client, foto_c3b, [marca()], headers={"If-Match": version})
    assert response.status_code == 409
    assert "otro dispositivo" in response.get_json()["error"]
    assert client.get(foto_c3b["url"] + "/anotaciones").get_json() == current.get_json()


def test_reintento_equivalente_no_duplica(client, foto_c3b):
    version = client.get(foto_c3b["url"] + "/anotaciones").headers["ETag"]
    first = guardar(client, foto_c3b, [marca()], headers={"If-Match": version})
    retry = guardar(client, foto_c3b, [marca()], headers={"If-Match": version})
    assert retry.status_code == 200
    assert retry.get_json() == first.get_json() and retry.headers["ETag"] == first.headers["ETag"]


def test_140_caracteres_con_tilde(client, foto_c3b):
    text = "[Ejemplo] " + "á" * 130
    response = guardar(client, foto_c3b, [marca("O", text)])
    assert response.status_code == 200 and response.get_json()[0]["texto"] == text


@pytest.mark.parametrize("payload", [None, [], {}, {"anotaciones": {}}, {"anotaciones": [None]},
    {"anotaciones": [dict(x=".5", y=.5, codigo="✓", texto="")]},
    {"anotaciones": [dict(x=float("nan"), y=.5, codigo="✓", texto="")]},
    {"anotaciones": [dict(x=.5, y=.5, codigo="✓", texto="", extra=1)]}])
def test_validacion_estructura_y_posiciones(payload):
    with Flask(__name__).test_request_context():
        with pytest.raises(BadRequest):
            validar_anotaciones(payload)


def test_pwa_lee_imagen_y_marcas_y_guarda_en_api(app, client, foto_c3b, tmp_path):
    assert guardar(client, foto_c3b, [marca("NA")]).status_code == 200
    template = (ROOT / "app/templates/carga.html").read_text(encoding="utf-8")
    panel = template[template.index('<section id="fotos"'):template.index('<section class="card" id="firmas"')]
    bootstrap = "window.readyproofSession=fetch('/api/auth/sesion').then(r=>r.json());window.readyproofExpired=()=>{};"
    bootstrap += "window.readyproofFotosBorrador=async()=>({serverId:" + json.dumps(foto_c3b["carga_id"]) + ",pending:false,conflicto:false,estado:'borrador'});"
    bootstrap += "window.addEventListener('DOMContentLoaded',()=>window.dispatchEvent(new CustomEvent('readyproof-fotos-contexto',{detail:{localId:'c3b-local',serverId:" + json.dumps(foto_c3b["carga_id"]) + ",readOnly:false,estado:'borrador'}})));"
    html = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="/static/fotos.css"><script>' + bootstrap + '</script><script src="/static/fotos.js" defer></script></head><body>' + panel + '</body></html>'
    def servicio(environ, start_response):
        if environ["PATH_INFO"] == "/_pruebas/c3b":
            body = html.encode()
            start_response("200 OK", [("Content-Type", "text/html; charset=utf-8"), ("Content-Length", str(len(body)))])
            return [body]
        return app(environ, start_response)
    server = make_server("127.0.0.1", 0, servicio, threaded=True)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    cookie_name = app.config.get("SESSION_COOKIE_NAME", "session")
    cookie = client.get_cookie(cookie_name)
    env = dict(os.environ, RP_URL=f"http://127.0.0.1:{server.server_port}", RP_FOTO_URL=foto_c3b["url"], RP_COOKIE_NAME=cookie_name, RP_COOKIE_VALUE=cookie.value, RP_OUT=str(tmp_path))
    modules = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules"
    if modules.is_dir() and not env.get("NODE_PATH"):
        env["NODE_PATH"] = str(modules)
    try:
        result = subprocess.run([os.environ.get("READYPROOF_NODE") or shutil.which("node"), "tests/browser/fotos_c3b.cjs"], cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=150)
        assert result.returncode == 0, result.stdout + result.stderr
        rows = client.get(foto_c3b["url"] + "/anotaciones").get_json()
        assert len(rows) == 2 and rows[1]["texto"] == "[Ejemplo] Edición sin conexión"
    finally:
        server.shutdown()
        thread.join(timeout=10)
        server.server_close()
