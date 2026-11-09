"""Conservación del destinatario ante configuración demorada, sin envíos."""
import json
import os
from pathlib import Path
import shutil
import subprocess
from threading import Thread

import pytest
from werkzeug.serving import make_server, WSGIRequestHandler
from tests.test_smtp_gmail import carga_emitida


@pytest.mark.parametrize('caso', ['vacio', 'predeterminado', 'borrado', 'sin_edicion', 'reapertura'])
def test_destinatario_se_conserva_durante_carga(app, client, usuario_admin, carga_emitida, catalogo, caso, monkeypatch):
    def prohibido(*args, **kwargs):
        raise AssertionError('Esta prueba no permite transporte externo.')
    monkeypatch.setattr('app.contabilium.build_opener', prohibido)
    monkeypatch.setattr('app.gmail_https.obtener_token', prohibido)
    monkeypatch.setattr('app.gmail_https.enviar_con_token', prohibido)
    node = os.environ.get('READYPROOF_NODE') or shutil.which('node')
    assert node, 'Se requiere Node y Playwright.'
    class QuietHandler(WSGIRequestHandler):
        def log(self, *args, **kwargs):
            pass
    server = make_server('127.0.0.1', 0, app, threaded=True, request_handler=QuietHandler)
    thread = Thread(target=server.serve_forever, daemon=True); thread.start()
    output = Path('out/correccion_destinatario') / caso
    output.mkdir(parents=True, exist_ok=True)
    emitted = client.get('/api/cargas/' + carga_emitida)
    assert emitted.status_code == 200
    payload = dict(url=f'http://127.0.0.1:{server.server_port}', out=str(output.resolve()),
        caso=caso, usuario=usuario_admin, carga=emitted.get_json(), cliente_id=catalogo[0]['id'],
        sistema_id=catalogo[1]['id'], planilla_id=catalogo[2]['id'])
    try:
        result = subprocess.run([node, 'tests/browser/correo_destinatario_carga.cjs'],
            input=json.dumps(payload), capture_output=True, text=True, timeout=100)
        assert result.returncode == 0, result.stdout + result.stderr
        evidence = json.loads((output / 'resultado.json').read_text())
        assert evidence['destinatario_conservado'] and evidence['sin_envios']
        assert evidence['ancho_px'] == 390
    finally:
        server.shutdown(); thread.join(timeout=10); server.server_close()
