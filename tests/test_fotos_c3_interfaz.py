"""Marcado local de fotos: validación y navegador sin base ni correo reales."""
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
import json
import os
from pathlib import Path
import shutil
import subprocess
from threading import Thread

from PIL import Image
import pytest

ROOT = Path(__file__).resolve().parents[1]


def entorno_node(**extra):
    env = dict(os.environ, **extra)
    modules = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules"
    if modules.is_dir() and not env.get("NODE_PATH"):
        env["NODE_PATH"] = str(modules)
    return env


def node():
    executable = os.environ.get("READYPROOF_NODE") or shutil.which("node")
    assert executable, "Se requiere Node disponible para las pruebas de fotos."
    return executable


@pytest.mark.parametrize("codigo,texto,x,y,error", [
    ("✓", "", 0, 1, None), ("NA", "", 1, 0, None),
    ("O", "[Ejemplo] Revisar", .2, .8, None), ("X", "[Ejemplo] Sin acceso", .5, .5, None),
    ("O", "", .5, .5, "Completá el texto"), ("X", "", .5, .5, "Completá el texto"),
    ("O", "   ", .5, .5, "Completá el texto"),
    ("✓", "[Ejemplo] " + "á" * 130, .5, .5, None),
    ("✓", "[Ejemplo] " + "á" * 131, .5, .5, "hasta 140"),
    ("O", "[Ejemplo] " + "á" * 131, .5, .5, "hasta 140"),
    ("o", "[Ejemplo] Texto", .5, .5, "Elegí un código válido"),
    ("", "", .5, .5, "Elegí un código válido"),
    ("✓", "", -.01, .5, "posición"), ("NA", "", .5, 1.01, "posición"),
    ("✓", "", None, .5, "posición"), ("✓", None, .5, .5, "hasta 140"),
])
def test_validacion_marcas_c3(codigo, texto, x, y, error):
    payload = {"marcas": [{"codigo": codigo, "texto": texto, "x": x, "y": y}]}
    result = subprocess.run([node(), "tests/browser/fotos_c3.cjs", "validar"], cwd=ROOT,
                            env=entorno_node(RP_CASO=json.dumps(payload)), capture_output=True, text=True, encoding="utf-8", timeout=15)
    assert result.returncode == 0, result.stdout + result.stderr
    response = json.loads(result.stdout)
    if error:
        assert response["ok"] is False
        assert error in response["error"]
    else:
        assert response["ok"] is True
        assert response["marcas"][0]["numero"] == 1
        assert response["marcas"][0]["texto"] == texto


def test_numeracion_automatica_sin_numeros_del_usuario():
    payload = {"numerar": True, "marcas": [{"id": "primera", "numero": 99}, {"id": "tercera", "numero": 3}]}
    result = subprocess.run([node(), "tests/browser/fotos_c3.cjs", "validar"], cwd=ROOT,
                            env=entorno_node(RP_CASO=json.dumps(payload)), capture_output=True, text=True, encoding="utf-8", timeout=15)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["marcas"] == [{"id": "primera", "numero": 1}, {"id": "tercera", "numero": 2}]


@pytest.mark.parametrize("movil", [True, False], ids=["movil", "escritorio"])
def test_marcado_fotos_en_navegador(tmp_path, movil):
    template = (ROOT / "app/templates/carga.html").read_text(encoding="utf-8")
    start = template.index('<section id="fotos"')
    end = template.index('<section class="card" id="firmas"', start)
    panel = template[start:end]
    bootstrap = """window.readyproofSession=Promise.resolve({usuario:{id:new URL(location.href).searchParams.get('usuario')||'c3-usuario'},csrf_token:'[Ejemplo] csrf'});
window.readyproofFotosBorrador=async()=>({serverId:'c3-carga',pending:false,conflicto:false,estado:'borrador'});
window.readyproofExpired=()=>{};
window.c3Contexto=(readOnly=false)=>window.dispatchEvent(new CustomEvent('readyproof-fotos-contexto',{detail:{localId:'c3-borrador',serverId:'c3-carga',readOnly,estado:readOnly?'emitida':'borrador'}}));
window.addEventListener('DOMContentLoaded',()=>window.c3Contexto());"""
    html = '<!doctype html><html lang="es-AR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="/static/carga.css"><link rel="stylesheet" href="/static/fotos.css"><script>' + bootstrap + '</script><script src="/static/fotos.js" defer></script></head><body>' + panel + '</body></html>'
    photos, requests = [], []
    annotations, image_blobs = {}, {}

    class Handler(BaseHTTPRequestHandler):
        def send(self, body, content_type, etag=None):
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            if etag is not None:
                self.send_header("ETag", etag)
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path.startswith("/static/"):
                name = self.path.split("/")[-1]
                assert name in ("carga.css", "fotos.css", "fotos.js")
                content_type = "text/css" if name.endswith(".css") else "application/javascript"
                self.send((ROOT / "app/static" / name).read_bytes(), content_type + "; charset=utf-8")
            elif self.path.startswith("/api/"):
                requests.append(("GET", self.path))
                if self.path == "/api/cargas/c3-carga/fotos":
                    self.send(json.dumps(photos).encode(), "application/json")
                elif self.path == "/api/cargas/c3-carga/fotos/items":
                    self.send(b"[]", "application/json")
                elif self.path.endswith("/anotaciones"):
                    key = self.path.split("/")[-2]
                    marks = annotations.get(key, [])
                    etag = '"' + sha256(json.dumps(marks, sort_keys=True).encode()).hexdigest() + '"'
                    self.send(json.dumps(marks).encode(), "application/json", etag)
                else:
                    assert self.path.endswith("/imagen")
                    self.send(image_blobs[self.path.split("/")[-2]], "image/jpeg")
            else:
                self.send(html.encode(), "text/html; charset=utf-8")

        def do_POST(self):
            requests.append(("POST", self.path))
            blob = self.rfile.read(int(self.headers["Content-Length"]))
            if self.path.endswith("/anotaciones"):
                key = self.path.split("/")[-2]
                marks = [dict(row, numero=i) for i, row in enumerate(json.loads(blob)["anotaciones"], 1)]
                annotations[key] = marks
                etag = '"' + sha256(json.dumps(marks, sort_keys=True).encode()).hexdigest() + '"'
                self.send(json.dumps(marks).encode(), "application/json", etag)
                return
            assert self.path == "/api/cargas/c3-carga/fotos"
            with Image.open(BytesIO(blob)) as image:
                assert image.format == "JPEG"
                width, height = image.size
            row = dict(id=self.headers["Idempotency-Key"], orden=len(photos)+1, ancho=width, alto=height, sha256=sha256(blob).hexdigest(), bytes=len(blob))
            photos.append(row)
            image_blobs[row["id"]] = blob
            self.send(json.dumps(row).encode(), "application/json")

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        result = subprocess.run([node(), "tests/browser/fotos_c3.cjs"], cwd=ROOT,
                                env=entorno_node(RP_URL=f"http://127.0.0.1:{server.server_port}", RP_OUT=str(tmp_path), RP_MOVIL="1" if movil else "0"),
                                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=150)
        assert result.returncode == 0, result.stdout + result.stderr
        report = json.loads((tmp_path / "resultado.json").read_text(encoding="utf-8"))
        assert report["marcas"] == 2 and report["errores"] == []
        assert len(photos) == 1
        allowed = {"/api/cargas/c3-carga/fotos", "/api/cargas/c3-carga/fotos/items", f"/api/cargas/c3-carga/fotos/{photos[0]['id']}/anotaciones", f"/api/cargas/c3-carga/fotos/{photos[0]['id']}/imagen"}
        assert all(path in allowed for _, path in requests)
    finally:
        server.shutdown()
        thread.join(timeout=10)
        server.server_close()
