"""Aplica las migraciones autorizadas después de pruebas y respaldo verificados."""
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FILES = ('app/models/__init__.py','app/utils/__init__.py','app/utils/cuit_validator.py',
         'migraciones/alembic/versions/011_cliente_cuit_opcional.py',
         'migraciones/alembic/versions/012_sistema_cliente_activo.py',
         'scripts/audit_cuit.py','scripts/backup_readyproof.py')

CODE = r'''
import json,os,sys,stat,subprocess,hashlib,tempfile,grp
from datetime import datetime,timezone
from pathlib import Path
sys.path.insert(0,'/home/readyproof');sys.path.insert(0,'/home/readyproof/scripts')
from dotenv import load_dotenv
from sqlalchemy import create_engine,text
from sqlalchemy.engine import make_url
from alembic import command
from alembic.config import Config
from backup_readyproof import content_manifest
os.umask(0o077)
root=Path('/home/readyproof');store=Path('/var/backups/readyproof')
data=json.load(sys.stdin);files=data['files']
allowed={'app/models/__init__.py','app/utils/__init__.py','app/utils/cuit_validator.py',
 'migraciones/alembic/versions/011_cliente_cuit_opcional.py','migraciones/alembic/versions/012_sistema_cliente_activo.py',
 'scripts/audit_cuit.py','scripts/backup_readyproof.py'}
assert set(files)==allowed
for name,expected in data['expected_existing'].items():
 assert hashlib.sha256((root/name).read_bytes()).hexdigest()==expected,'La fuente remota cambió; no se sobrescribe.'
for name,content in files.items():
 if name not in data['expected_existing'] and (root/name).exists():
  assert (root/name).read_text(encoding='utf-8')==content,'Hay un archivo nuevo con contenido ajeno; revisar antes de continuar.'
load_dotenv(root/'.env.local',override=False);load_dotenv(root/'.env',override=False)
url=make_url(os.environ['DATABASE_URL'])
assert url.database=='readyproof' and url.host in {'localhost','127.0.0.1','::1'}
engine=create_engine(url)
with engine.begin() as c:
 assert c.scalar(text('SELECT version_num FROM alembic_version'))=='010_firmantes'
 assert c.scalar(text('SELECT count(*) FROM clientes WHERE es_ejemplo IS NOT TRUE'))==0
assert json.loads((store/'ensayo_etapa2.json').read_text())['estado']=='ensayo_012_ok'
backup=json.loads((store/'ultimo_backup.json').read_text());assert backup['schema']=='010_firmantes'
previous=store/('etapa2-fuentes-previas-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S'));previous.mkdir(mode=0o700)
for name in files:
 p=root/name
 if p.exists():
  target=previous/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())
gid=grp.getgrnam('readyproof').gr_gid
def install(name,content):
 p=root/name
 if not p.parent.exists():
  p.parent.mkdir(mode=0o750);os.chown(p.parent,0,gid);os.chmod(p.parent,0o750)
 old=p.stat() if p.exists() else None
 fd,temporary=tempfile.mkstemp(prefix='.etapa2-',dir=p.parent)
 try:
  with os.fdopen(fd,'w',encoding='utf-8') as stream:stream.write(content)
  os.chown(temporary,old.st_uid if old else 0,old.st_gid if old else gid)
  os.chmod(temporary,stat.S_IMODE(old.st_mode) if old else 0o640)
  os.replace(temporary,p)
 finally:
  if os.path.exists(temporary):os.unlink(temporary)
subprocess.run(['systemctl','stop','readyproof'],check=True,capture_output=True,timeout=240)
committed=False
try:
 # Pausar solo readyproof permite que la copia previa incluya todas las últimas escrituras.
 subprocess.run(['/var/backups/readyproof/backup_y_subida.sh'],check=True,capture_output=True,timeout=600)
 backup=json.loads((store/'ultimo_backup.json').read_text());assert backup['schema']=='010_firmantes'
 pre_remote='readyproof-drive:readyproof-backups/pre-migrations/readyproof-pre-012-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'.tar.enc'
 with tempfile.TemporaryDirectory(prefix='.pre-012-',dir=store) as temporary:
  for suffix in ('','.json'):
   subprocess.run(['rclone','--config','/etc/readyproof/rclone-backup.conf','copyto',backup['remote']+suffix,pre_remote+suffix],check=True,capture_output=True,timeout=120)
  file=Path(temporary)/'pre-012.enc'
  subprocess.run(['rclone','--config','/etc/readyproof/rclone-backup.conf','copyto',pre_remote,str(file)],check=True,capture_output=True,timeout=120)
  assert hashlib.sha256(file.read_bytes()).hexdigest()==backup['cipher_sha256']
 for name,content in files.items():
  if name!='app/models/__init__.py':install(name,content)
 config=Config(str(root/'alembic.ini'))
 with engine.begin() as c:
  before=content_manifest(c)
  before_clients=list(c.execute(text('SELECT id,nombre,es_ejemplo FROM clientes ORDER BY id')))
  before_systems=list(c.execute(text('SELECT id,cliente_id,tipo,designacion FROM sistemas ORDER BY id')))
  config.attributes['connection']=c;command.upgrade(config,'012_sistema_cliente_activo')
  after=content_manifest(c)
  counts=dict(before['counts']);counts['versiones_esquema']+=2
  assert after['schema']=='012_sistema_cliente_activo'
  assert after['counts']==counts and after['blobs']==before['blobs']
  assert list(c.execute(text('SELECT id,nombre,es_ejemplo FROM clientes ORDER BY id')))==before_clients
  assert list(c.execute(text('SELECT id,cliente_id,tipo,designacion FROM sistemas ORDER BY id')))==before_systems
  assert c.scalar(text('SELECT count(*) FROM clientes WHERE cuit IS NOT NULL'))==0
  assert c.scalar(text('SELECT count(*) FROM sistemas WHERE activo IS NOT TRUE OR cliente_id IS NULL'))==0
 committed=True
 install('app/models/__init__.py',files['app/models/__init__.py'])
 # Sintaxis y lectura como el usuario real del servicio antes de iniciarlo.
 code="import sys;sys.path.insert(0,'/home/readyproof');from app.models import Cliente,Sistema;from app.utils.cuit_validator import validar_cuit;assert validar_cuit('20000000001')"
 subprocess.run(['runuser','-u','readyproof','--',str(root/'venv/bin/python'),'-c',code],check=True,capture_output=True,timeout=30)
except Exception:
 if not committed:
  for name in files:
   old=previous/name
   if old.exists():install(name,old.read_text(encoding='utf-8'))
   elif (root/name).exists():(root/name).unlink()
 else:
  # 011/012 son aditivas: si falla el código nuevo, volver al modelo anterior sin borrar datos.
  install('app/models/__init__.py',(previous/'app/models/__init__.py').read_text(encoding='utf-8'))
 raise
finally:
 engine.dispose()
 subprocess.run(['systemctl','start','readyproof'],check=True,capture_output=True,timeout=240)
report={'estado':'etapa2_aplicada','schema':after['schema'],'tablas_verificadas':len(after['counts']),
 'binarios_conservados':len(after['blobs']),'cargas_conservadas':after['counts']['cargas'],
 'clientes_sin_cuit':len(before_clients),'sistemas_activos':len(before_systems),
 'respaldo_pre_migracion':pre_remote,'respaldo_pre_migracion_sha256':backup['cipher_sha256'],
 'uuid_y_relaciones_conservados':True,'datos_reales_agregados':False,'fuentes_previas':str(previous)}
(store/'aplicacion_etapa2.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
'''


def main():
    log=(ROOT/'out/etapa2_cuit/pytest_completo_env.txt').read_text(encoding='utf-8',errors='replace')
    clean = re.search(r'^\d+ passed in ',log,re.M) and not re.search(r'^.*\d+ (?:failed|errors?)',log,re.M)
    if not clean:
        # Un único setup falló por espacio; solo se acepta si ese mismo caso pasó luego.
        retry=ROOT/'out/etapa2_cuit/pytest_reintento_diskfull.txt'
        retried=retry.read_text(encoding='utf-8',errors='replace') if retry.exists() else ''
        errors=re.findall(r'^ERROR (\S+)',log,re.M)
        recovered=(re.search(r'^265 passed, 1 error in ',log,re.M)
                   and errors==['tests/test_smtp_gmail.py::test_gmail_credenciales_desde_env']
                   and '(psycopg.errors.DiskFull)' in log
                   and re.search(r'^1 passed in ',retried,re.M)
                   and not re.search(r'^.*\d+ (?:failed|errors?)',retried,re.M))
        if not recovered:
            raise ValueError('Hay fallos o errores de pruebas sin resolver.')
    previous=json.loads((ROOT/'out/final_v1/archivos_final.json').read_text(encoding='utf-8'))['archivos']
    backup=json.loads((ROOT/'out/etapa1_backup/verificacion_drive_restore.json').read_text(encoding='utf-8'))
    data={'files':{name:(ROOT/name).read_text(encoding='utf-8') for name in FILES},
          'expected_existing':{'app/models/__init__.py':previous['app/models/__init__.py'],
                               'scripts/backup_readyproof.py':backup['script_sha256']}}
    cmd=['ssh','-i',str(Path.home()/'.ssh/readyproof_deploy_67_205_170_29'),'-o','IdentitiesOnly=yes',
         '-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=15',
         'root@67.205.170.29','/home/readyproof/venv/bin/python -c '+shlex.quote(CODE)]
    result=subprocess.run(cmd,input=json.dumps(data).encode(),capture_output=True,timeout=1200)
    if result.returncode:
        print('No se confirmó la aplicación de Etapa 2; consultar el estado antes de repetir.');return 1
    report=json.loads(result.stdout)
    (ROOT/'out/etapa2_cuit/aplicacion_servidor.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report));return 0


if __name__=='__main__':
    raise SystemExit(main())
