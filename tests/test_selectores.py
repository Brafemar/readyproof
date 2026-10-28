"""Regresiones de selección y de respuestas del service worker, sin datos reales."""
import json
import os
from pathlib import Path
import shutil
import subprocess
from threading import Thread

from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.serving import make_server

from app.models import Planilla


def test_service_worker_sin_respuestas_invalidas():
    node=os.environ.get('READYPROOF_NODE') or shutil.which('node')
    assert node
    result=subprocess.run([node,'tests/browser/service_worker.cjs'],capture_output=True,text=True,timeout=30)
    assert result.returncode==0,result.stdout+result.stderr


def test_selectores_cambian_cliente_sistema_y_planilla(app,client,usuario_admin,catalogo):
    first,system,template=catalogo
    other=client.post('/api/admin/clientes',json={'nombre':'[Ejemplo] Segunda planta'}).get_json()
    other_system=client.post(f"/api/admin/clientes/{other['id']}/sistemas",json={'tipo':'SAA','designacion':'[Ejemplo] SAA de segunda planta'}).get_json()
    second_system=client.post(f"/api/admin/clientes/{first['id']}/sistemas",json={'tipo':'SAA','designacion':'[Ejemplo] Z segundo abastecimiento'}).get_json()
    with Session(app.extensions['db_engine']) as session:
        pilot=session.get(Planilla,template['id'])
        alternative=Planilla(codigo=pilot.codigo,version=pilot.version+'-prueba-ui',sistema_tipo=pilot.sistema_tipo,
                             huella=pilot.huella,definicion=pilot.definicion,manual_id=pilot.manual_id)
        session.add(alternative);session.commit()
        alternative_id=alternative.id
    server=make_server('127.0.0.1',0,app,threaded=True)
    thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    out=Path('out/selectores_navegador').resolve();out.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,RP_URL=f'http://127.0.0.1:{server.server_port}',RP_OUT=str(out),
             RP_LOGIN=usuario_admin['login'],RP_PASSWORD=usuario_admin['clave'],
             RP_SELECTION=json.dumps({'cliente':first['id'],'otro_cliente':other['id'],'otro_sistema':other_system['id'],
                                      'segundo_sistema':second_system['id'],'otra_planilla':alternative_id}))
    node=os.environ.get('READYPROOF_NODE') or shutil.which('node')
    assert node
    try:
        result=subprocess.run([node,'tests/browser/selectores.cjs'],env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120)
        assert result.returncode==0,result.stdout+result.stderr
    finally:
        server.shutdown();thread.join(timeout=10)
