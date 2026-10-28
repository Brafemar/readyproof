"""Simula en móvil el modo real con datos ficticios y base temporal."""
import json,os,shutil,subprocess
from pathlib import Path
from threading import Thread
from werkzeug.serving import make_server
from tests.test_modo_operacion import real
from tests.test_desbloqueo_revision import pdf_simulado


def test_modo_real_navegador(app,client,catalogo,datos_api,usuario_admin,pdf_simulado):
    row=real(app,client,catalogo,datos_api)
    record=dict(localId=row['id'],serverId=row['id'],clienteId=row['datos']['cabecera']['cliente'],sistemaId=row['sistema_id'],planillaId=row['planilla_id'],revision=row['revision'],estado='borrador',datos=row['datos'],firmas={},firmasServidor=row['firmas'],responsable=row['responsable'],pending=False,conflicto=False,editVersion=0,actualizado=row['actualizada_en'])
    customers=client.get('/api/clientes').get_json();record['clienteId']=next(c['id'] for c in customers if c['nombre']==row['datos']['cabecera']['cliente'])
    server=make_server('127.0.0.1',0,app,threaded=True);thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    output=Path('out/etapa6_final/real_navegador.json').resolve();output.parent.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,RP_URL=f'http://127.0.0.1:{server.server_port}',RP_LOGIN=usuario_admin['login'],RP_PASSWORD=usuario_admin['clave'],RP_BORRADOR=json.dumps(record),RP_RESULTADO=str(output))
    try:
        result=subprocess.run([shutil.which('node'),'tests/browser/modo_real.cjs'],env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=150)
        assert result.returncode==0,result.stdout+result.stderr
        report=json.loads(output.read_text());assert report['id']==row['id'] and report['datos_ficticios']
        assert client.get(f"/api/cargas/{row['id']}").get_json()['estado']=='emitida'
    finally:server.shutdown();thread.join(timeout=10)
