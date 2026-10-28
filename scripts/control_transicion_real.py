"""Control de ensayo, corte y verificación de la transición autorizada."""
from hashlib import sha256
import json,sys,xml.etree.ElementTree as ET
from pathlib import Path
from revision_etapa5 import ssh
from servidor_unidades_bar import FILES
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'out/transicion_real_20261028'
STAGE='/home/readyproof_revision_etapa5'

def tests():
    selection=json.loads((OUT/'final/seleccion_pruebas.json').read_text())
    total=0
    for platform in ('linux','windows'):
        cases=list(ET.parse(OUT/'final'/f'{platform}.xml').iter('testcase'))
        assert len(cases)==len(selection[platform])
        actual={c.attrib['classname'].replace('.','/')+'.py::'+c.attrib['name'] for c in cases}
        assert actual==set(selection[platform])
        assert all(c.find('failure') is None and c.find('error') is None and c.find('skipped') is None for c in cases)
        total+=len(cases)
    assert total==543
    previous=json.loads((ROOT/'out/etapa6_final/seleccion_pruebas.json').read_text())
    assert set(previous['linux']+previous['windows'])<=set(selection['linux']+selection['windows'])
    focused=list(ET.parse(OUT/'final/interfaz_posterior.xml').iter('testcase'))
    assert {c.attrib['name'] for c in focused}=={'test_copia_a4_conserva_pdf_anterior','test_administracion_y_cambio_de_cuenta_en_navegador','test_modo_real_navegador'}
    assert all(c.find('failure') is None and c.find('error') is None and c.find('skipped') is None for c in focused)
    return {'tests_pasando':total,'tests_fallidos':0}

def execute(action):
    data={'accion':action,'fuentes':{name:sha256((ROOT/name).read_bytes()).hexdigest() for name in FILES}}
    if action not in ('ensayar','verificar'):data.update(tests())
    if action in ('ensayar','aplicar'):name='servidor_unidades_bar.py'
    elif action=='activar':name='transicion_real.py';data.update(unidades_resueltas=True)
    else:name=None
    if name:
        digest=sha256((ROOT/'scripts'/name).read_bytes()).hexdigest()
        code="import sys,runpy,hashlib;from pathlib import Path;sys.path.insert(0,"+repr(STAGE+'/scripts')+");p=Path("+repr(STAGE+'/scripts/'+name)+");assert hashlib.sha256(p.read_bytes()).hexdigest()=="+repr(digest)+";runpy.run_path(str(p),run_name='__main__')"
        if action=='activar':
            code=code.replace(";runpy.run_path(str(p),run_name='__main__')", "\ntry:\n runpy.run_path(str(p),run_name='__main__')\nexcept SystemExit as error:\n if error.code not in (None,0,1):raise\n")
    else:
        code='''
from pathlib import Path
import json,subprocess,sys,hashlib
sys.path.insert(0,'/home/readyproof')
from app import create_app
from urllib.request import urlopen
root=Path('/home/readyproof');store=Path('/var/backups/readyproof');app=create_app()
assert app.config['MODO_PILOTO'] is False and app.config['MAIL_MODO_PRUEBA'] is False
assert app.config['EMPRESA_MANTENEDORA']=='READYPROOF' and app.config['CERTIFICADO_N']=='IFI-2024-10001'
with urlopen('http://127.0.0.1:8000/login',timeout=10) as response:assert response.status==200
source={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'fuente').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
subprocess.run(['systemctl','start','readyproof-backup.service'],capture_output=True,check=True,timeout=700)
backup=json.loads((store/'ultimo_backup.json').read_text());assert backup['schema']=='017_scc1_presion_bar'
r=subprocess.run([str(root/'venv/bin/python'),str(root/'scripts/backup_readyproof.py'),'restore','--remote',backup['remote'],'--schema-esperado','017_scc1_presion_bar','--planillas-esperadas','89'],capture_output=True,check=True,timeout=700)
restored=json.loads(r.stdout);assert not restored['produccion_modificada']
assert restored['cipher_sha256']==backup['cipher_sha256'] and restored['counts']['planillas']==89
print(json.dumps({'estado':'MODO_REAL_VERIFICADO','modo_piloto':False,'mail_modo_prueba':False,'empresa_mantenedora':'READYPROOF','certificado_n':'IFI-2024-10001','backup':backup,'restauracion':restored,'fuente_sha256':source,'timer':subprocess.run(['systemctl','is-active','readyproof-backup.timer'],capture_output=True,check=True,text=True).stdout.strip()}))
'''
    result=json.loads(ssh(code,payload=json.dumps(data).encode(),timeout=1800))
    if action=='verificar':assert result['fuente_sha256']==json.loads((OUT/'preparacion.json').read_text())['fuente_sha256']
    (OUT/(action+'.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k in ('estado','schema','base_aislada','produccion_modificada','modo_piloto','mail_modo_prueba')}))
    if result.get('estado')=='TRANSICION_NO_CONFIRMADA':
        print(json.dumps({'tipo':result.get('tipo'),'lineas':result.get('lineas')}))
        raise RuntimeError('La activación no quedó confirmada; diagnóstico estructurado conservado.')

if __name__=='__main__':
    assert sys.argv[1] in ('ensayar','aplicar','activar','verificar')
    execute(sys.argv[1])
