"""Instala las reglas probadas; conserva datos, definiciones y copias anteriores."""
import hashlib
import json
from pathlib import Path
import shlex
import subprocess

ROOT=Path(__file__).resolve().parents[1]

CODE=r'''
import json,os,sys,subprocess,stat,grp,tempfile,hashlib,time
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import urlopen
sys.path.insert(0,'/home/readyproof');sys.path.insert(0,'/home/readyproof/scripts')
from dotenv import load_dotenv
from sqlalchemy import create_engine,text
from sqlalchemy.engine import make_url
from backup_readyproof import content_manifest
root=Path('/home/readyproof');store=Path('/var/backups/readyproof');review=store/'revision-etapa3'
data=json.load(sys.stdin)
allowed={'app/carga/__init__.py','app/carga/validacion.py','app/planillas/validacion.py','app/planillas/importacion_excel.py','app/rutas/api.py','scripts/importador_planillas.py'}
assert set(data['hashes'])==allowed
for name,expected in data['hashes'].items():
 assert hashlib.sha256((review/name).read_text(encoding='utf-8').encode()).hexdigest()==expected
 if name not in data['previous'] and (root/name).exists():
  assert (root/name).read_text(encoding='utf-8')==(review/name).read_text(encoding='utf-8')
for name,expected in data['previous'].items():
 assert hashlib.sha256((root/name).read_text(encoding='utf-8').encode()).hexdigest()==expected,'La fuente activa cambió; no sobrescribir.'
report=json.loads((review/'cotejo_bd.json').read_text())
assert report['estados']=={'YA_EXISTE':16,'A_IMPORTAR':63} and not report['errores'] and report['cambios']==0
load_dotenv(root/'.env.local',override=False);load_dotenv(root/'.env',override=False)
url=make_url(os.environ['DATABASE_URL']);assert url.database=='readyproof' and url.host in {'localhost','127.0.0.1','::1'}
engine=create_engine(url)
with engine.begin() as c:
 c.execute(text('SET TRANSACTION READ ONLY'))
 assert c.scalar(text('SELECT version_num FROM alembic_version'))=='012_sistema_cliente_activo'
 assert c.scalar(text('SELECT count(*) FROM planillas'))==25
 assert c.scalar(text('SELECT count(*) FROM clientes WHERE es_ejemplo IS NOT TRUE'))==0
os.umask(0o077);gid=grp.getgrnam('readyproof').gr_gid
previous=store/('etapa3-fuentes-previas-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S'));previous.mkdir(mode=0o700)
for name in allowed:
 p=root/name
 if p.exists():
  saved=previous/name;saved.parent.mkdir(parents=True,exist_ok=True);saved.write_bytes(p.read_bytes())
def install(name,content):
 p=root/name
 assert not p.is_symlink()
 if not p.parent.exists():
  p.parent.mkdir(mode=0o750);os.chown(p.parent,0,gid);os.chmod(p.parent,0o750)
 assert not p.parent.is_symlink()
 old=p.stat() if p.exists() else None
 fd,temporary=tempfile.mkstemp(prefix='.etapa3-',dir=p.parent)
 try:
  with os.fdopen(fd,'wb') as stream:stream.write(content)
  os.chown(temporary,old.st_uid if old else 0,old.st_gid if old else gid)
  os.chmod(temporary,stat.S_IMODE(old.st_mode) if old else 0o640)
  os.replace(temporary,p)
 finally:
  if os.path.exists(temporary):os.unlink(temporary)
smoke="""import sys
sys.path.insert(0,'/home/readyproof')
from app import create_app
from app.planillas.validacion import validar_datos,DatosInvalidos
from app.carga.validacion import ValidationError,validar_item_verificacion
from app.planillas.multisistema import ejemplo_multisistema
from sqlalchemy import text
assert issubclass(ValidationError,DatosInvalidos)
app=create_app()
assert app.config['MAIL_MODO_PRUEBA']
with app.extensions['db_engine'].begin() as c:
 c.execute(text('SET TRANSACTION READ ONLY'))
 schema=c.execute(text(\"SELECT definicion FROM planillas WHERE codigo='SG-PEM-IFI-SBC-3' AND version='00-26-ms1'\")).scalar_one()
sample=ejemplo_multisistema(schema)
validar_datos(sample,schema,completo=True)
for title,table in schema['tablas'].items():
 for row in table['filas']:
  value,result=row['campos']
  if schema['bloques'][title][value].get('unidad'):
   del sample['bloques'][title][value]
   try:validar_datos(sample,schema,completo=True)
   except ValidationError:pass
   else:raise AssertionError('Se aceptó medición omitida.')
   sample['bloques'][title][result]='NA'
   validar_datos(sample,schema,completo=True)
   try:validar_item_verificacion({'resultado':'O'},{})
   except ValidationError:pass
   else:raise AssertionError('Se aceptó O sin observación.')
   print('reglas_y_permisos_ok');sys.exit(0)
raise AssertionError('Falta ítem de medición de prueba.')
"""
subprocess.run(['systemctl','stop','readyproof'],check=True,capture_output=True,timeout=240)
try:
 subprocess.run(['/var/backups/readyproof/backup_y_subida.sh'],check=True,capture_output=True,timeout=600)
 with engine.begin() as c:
  c.execute(text('SET TRANSACTION READ ONLY'));before=content_manifest(c)
  planillas_before=list(c.execute(text('SELECT id,codigo,version,huella,definicion,manual_id FROM planillas ORDER BY id')))
 for name in sorted(allowed):install(name,(review/name).read_bytes())
 subprocess.run(['runuser','-u','readyproof','--',str(root/'venv/bin/python'),'-c',smoke],check=True,capture_output=True,timeout=90)
 with engine.begin() as c:
  c.execute(text('SET TRANSACTION READ ONLY'));after=content_manifest(c)
  assert before==after
  assert list(c.execute(text('SELECT id,codigo,version,huella,definicion,manual_id FROM planillas ORDER BY id')))==planillas_before
except Exception:
 for name in allowed:
  saved=previous/name
  if saved.exists():install(name,saved.read_bytes())
  elif (root/name).exists():(root/name).unlink()
 raise
finally:
 engine.dispose();subprocess.run(['systemctl','start','readyproof'],check=True,capture_output=True,timeout=240)
for attempt in range(20):
 try:
  with urlopen('http://127.0.0.1:8000/login',timeout=10) as response:assert response.status==200
  break
 except OSError:
  if attempt==19:raise
  time.sleep(1)
result={'estado':'etapa3_aplicada','schema':after['schema'],'planillas_totales':after['counts']['planillas'],
 'planillas_ofrecidas':16,'nuevas_importadas':0,'binarios_conservados':len(after['blobs']),
 'tablas_sin_cambios':len(after['counts']),'reglas_comprobadas_como_usuario_readyproof':True,
 'login_http':200,'fuentes_previas':str(previous),'modo_piloto_conservado':True}
(store/'aplicacion_etapa3.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
'''


def main():
    report=json.loads((ROOT/'out/etapa3_importador/resultado_local.json').read_text(encoding='utf-8'))
    assert report['casos_actuales']==report['casos_cubiertos']==300 and report['fallos_pendientes']==0
    for name,value in report['huellas_fuente'].items():
        assert hashlib.sha256((ROOT/name).read_text(encoding='utf-8').encode()).hexdigest()==value
    api=(ROOT/'app/rutas/api.py').read_text(encoding='utf-8')
    new_call='validar_datos(carga.datos, planilla.definicion, completo=True)'
    old_call='validar_datos(carga.datos, planilla.definicion)'
    assert api.count(new_call)==3
    validator=(ROOT/'app/planillas/validacion.py').read_text(encoding='utf-8')
    old_validator=validator.replace('def validar_datos(datos, esquema, *, completo=False):','def validar_datos(datos, esquema):')
    old_validator=old_validator.replace('    if completo:\n        from ..carga.validacion import validar_reglas_carga\n        validar_reglas_carga(normalized, esquema)\n','')
    previous={'app/rutas/api.py':hashlib.sha256(api.replace(new_call,old_call).encode()).hexdigest(),
              'app/planillas/validacion.py':hashlib.sha256(old_validator.encode()).hexdigest()}
    data={'hashes':report['huellas_fuente'],'previous':previous}
    command=['ssh','-i',str(Path.home()/'.ssh/readyproof_deploy_67_205_170_29'),'-o','IdentitiesOnly=yes',
             '-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=15',
             'root@67.205.170.29','/home/readyproof/venv/bin/python -c '+shlex.quote(CODE)]
    result=subprocess.run(command,input=json.dumps(data).encode(),capture_output=True,timeout=1200)
    if result.returncode:
        import re
        lines=result.stderr.decode(errors='replace').splitlines()
        diagnostic={'tipos':[line.split(':')[0] for line in lines if re.match(r'^[\w.]+(?:Error|Exception):',line)],
                    'lineas':[line.strip() for line in lines if line.lstrip().startswith('File ')]}
        (ROOT/'out/etapa3_importador/diagnostico_aplicacion.json').write_text(json.dumps(diagnostic,indent=2),encoding='utf-8')
        print('No se confirmó la instalación; revisar el estado antes de repetir.');return 1
    status=json.loads(result.stdout)
    (ROOT/'out/etapa3_importador/aplicacion_servidor.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
    print(json.dumps(status));return 0


if __name__=='__main__':
    raise SystemExit(main())
