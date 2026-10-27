"""Recorrido de aceptación en navegador móvil real con eventos táctiles."""
import json
import os
from pathlib import Path
import shutil
import subprocess
from threading import Thread

from pypdf import PdfReader
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from werkzeug.serving import make_server

from app.models import Carga, FirmaCarga


def test_interfaz_movil_offline_firmas_y_pdf(app,usuario_admin):
    node = os.environ.get("READYPROOF_NODE") or shutil.which("node")
    assert node, "Se requiere Node.js y Playwright 1.62.1 para la prueba de navegador."
    server = make_server("127.0.0.1", 0, app, threaded=True)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    out = Path("out/etapa3/navegador").resolve()
    env = dict(os.environ, RP_URL=f"http://127.0.0.1:{server.server_port}", RP_OUT=str(out),RP_LOGIN=usuario_admin["login"],RP_PASSWORD=usuario_admin["clave"])
    try:
        result = subprocess.run([node, "tests/browser/interfaz.cjs"], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=240)
        assert result.returncode == 0, result.stdout + result.stderr
        report = json.loads((out / "resultado.json").read_text(encoding="utf-8"))
        assert report["offline_con_recarga"] and report["firmas_por_eventos_tactiles"] == 2
        with Session(app.extensions["db_engine"]) as session:
            assert session.scalar(select(func.count()).select_from(Carga)) == 1
            assert session.get(FirmaCarga, report["carga_id"]).tecnico_png is not None
        preview = PdfReader(out / "vista_previa.pdf")
        assert len(preview.pages) == 2
        assert [len(page.images) for page in preview.pages] == [2, 4]
        reader = PdfReader(out / "SAA-1_firmada.pdf")
        assert len(reader.pages) == 2
        assert [len(page.images) for page in reader.pages] == [2, 4]
    finally:
        server.shutdown()
        thread.join(timeout=10)



def test_administracion_y_cambio_de_cuenta_en_navegador(app,usuario_admin):
    import secrets
    node=os.environ.get("READYPROOF_NODE") or shutil.which("node")
    assert node
    server=make_server("127.0.0.1",0,app,threaded=True)
    thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    out=Path("out/etapa4/navegador").resolve()
    env=dict(os.environ,RP_URL=f"http://127.0.0.1:{server.server_port}",RP_OUT=str(out),RP_LOGIN=usuario_admin["login"],RP_PASSWORD=usuario_admin["clave"],RP_SECOND_PASSWORD=secrets.token_urlsafe(24))
    try:
        result=subprocess.run([node,"tests/browser/auth.cjs"],env=env,capture_output=True,text=True,encoding="utf-8",errors="replace",timeout=150)
        assert result.returncode==0,result.stdout+result.stderr
        report=json.loads((out/"auth_resultado.json").read_text(encoding="utf-8"))
        assert report["alta_usuario_desde_pantalla"] and report["tecnico_sin_administracion"] and report["logout_revocado"]
    finally:
        server.shutdown();thread.join(timeout=10)
