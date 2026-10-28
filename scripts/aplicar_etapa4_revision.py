"""Ensayo aislado y aplicación privada de la revisión 013 autorizada."""
import argparse
import hashlib
import json
from pathlib import Path
import shlex
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'out/etapa4_revision'
FILES = ('app/models/__init__.py','app/carga/servicios.py','app/planillas/sdi_validacion.py',
    'app/planillas/registro_pdf.py','app/planillas/validacion.py','app/rutas/api.py',
    'app/correo/rutas.py','app/static/carga.js','app/static/sw.js','app/templates/carga.html',
    'migraciones/alembic/versions/013_desbloqueo_revision.py','scripts/backup_readyproof.py')

CODE = r'''
import os,sys,json,hashlib,subprocess,tempfile,stat,grp,time
from pathlib import Path
from datetime import datetime,timezone
from urllib.request import urlopen
root=Path('/home/readyproof');store=Path('/var/backups/readyproof')
sys.path.insert(0,str(root));sys.path.insert(0,str(root/'scripts'))
from dotenv import load_dotenv
from sqlalchemy import create_engine,text,inspect
from sqlalchemy.engine import make_url
from alembic import command
from alembic.config import Config
from backup_readyproof import content_manifest
data=json.load(sys.stdin);mode=data['mode']
allowed={'app/models/__init__.py','app/carga/servicios.py','app/planillas/sdi_validacion.py',
'app/planillas/registro_pdf.py','app/planillas/validacion.py','app/rutas/api.py','app/correo/rutas.py',
'app/static/carga.js','app/static/sw.js','app/templates/carga.html',
'migraciones/alembic/versions/013_desbloqueo_revision.py','scripts/backup_readyproof.py'}
assert set(data['files'])==allowed
hashes={name:hashlib.sha256((root/name).read_bytes()).hexdigest() if (root/name).exists() else None for name in sorted(allowed)}
load_dotenv(root/'.env.local',override=False);load_dotenv(root/'.env',override=False)
url=make_url(os.environ['DATABASE_URL']);assert url.database=='readyproof' and url.host in {'localhost','127.0.0.1','::1'}
engine=create_engine(url)
with engine.begin() as c:
 c.execute(text('SET TRANSACTION READ ONLY'))
 schema=c.scalar(text('SELECT version_num FROM alembic_version'))
 assert c.scalar(text('SELECT count(*) FROM clientes WHERE es_ejemplo IS NOT TRUE'))==0
 manifest=content_manifest(c)
if mode=='inspeccionar':
 print(json.dumps({'schema':schema,'hashes':hashes,'counts':manifest['counts'],'blobs':len(manifest['blobs'])}));sys.exit(0)
assert schema=='012_sistema_cliente_activo'
assert hashes==data['previous'],'Cambió el código del servidor; revisar antes de sobrescribir.'
os.umask(0o077)
gid=grp.getgrnam('readyproof').gr_gid

def snapshot(c, columns=None):
 names=sorted(inspect(c).get_table_names());result={};projection={}
 for name in names:
  if name in {'alembic_version','versiones_esquema'}:continue
  cols=columns[name] if columns else [column['name'] for column in inspect(c).get_columns(name)]
  quote=c.dialect.identifier_preparer.quote
  rows=c.execute(text('SELECT '+','.join(quote(col) for col in cols)+' FROM '+quote(name))).all()
  result[name]=sorted(hashlib.sha256(repr(tuple(row)).encode()).hexdigest() for row in rows)
  projection[name]=cols
 return result,projection

def migrate(c, path):
 config=Config(str(root/'alembic.ini'))
 # El ensayo usa los scripts vigentes y una copia privada con la nueva revisión.
 config.set_main_option('script_location',str(path))
 config.attributes['connection']=c
 before,cols=snapshot(c)
 config_before=c.scalar(text('SELECT version_num FROM alembic_version'));assert config_before=='012_sistema_cliente_activo'
 command.upgrade(config,'013_desbloqueo_revision')
 after,_=snapshot(c,{**cols,'numero_registro_contador':['id','ultimo'],'emisiones_carga':[x['name'] for x in inspect(c).get_columns('emisiones_carga')]})
 assert {name:after[name] for name in before}==before,'Cambió un dato histórico.'
 assert c.scalar(text('SELECT ultimo FROM numero_registro_contador WHERE id=1'))==0
 assert c.scalar(text('SELECT count(*) FROM emisiones_carga'))==0
 assert c.scalar(text('SELECT count(*) FROM cargas WHERE numero_registro IS NOT NULL OR revision_publica<>0 OR pdf_hash IS NOT NULL OR desbloqueado_por IS NOT NULL OR estado_anulada'))==0
 return {'filas_historicas_comparadas':sum(map(len,before.values())),'tablas_historicas':len(before)}

if mode=='ensayar':
 import shutil
 name='readyproof_test_etapa4_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
 assert name.startswith('readyproof_test_etapa4_')
 with tempfile.TemporaryDirectory(prefix='.ensayo013-',dir=store) as temporary:
  work=Path(temporary);scripts=work/'alembic';shutil.copytree(root/'migraciones/alembic',scripts)
  (scripts/'versions/013_desbloqueo_revision.py').write_text(data['files']['migraciones/alembic/versions/013_desbloqueo_revision.py'],encoding='utf-8')
  with (work/'db.dump').open('wb') as stream:
   subprocess.run(['runuser','-u','postgres','--','pg_dump','--format=custom','--no-owner','--no-acl','readyproof'],stdout=stream,stderr=subprocess.PIPE,check=True,timeout=120)
  subprocess.run(['runuser','-u','postgres','--','createdb','--owner='+url.username,name],check=True,capture_output=True,timeout=60)
  with (work/'db.dump').open('rb') as stream:
   subprocess.run(['runuser','-u','postgres','--','pg_restore','--exit-on-error','--single-transaction','--no-owner','--no-acl','--role='+url.username,'--dbname='+name],stdin=stream,check=True,capture_output=True,timeout=180)
  test_engine=create_engine(url.set(database=name))
  with test_engine.begin() as c:result=migrate(c,scripts)
  test_engine.dispose()
 result.update(estado='ensayo_013_ok',base_aislada=name,schema='013_desbloqueo_revision',produccion_modificada=False)
 (store/'ensayo_etapa4.json').write_text(json.dumps(result,indent=2))
 print(json.dumps(result));sys.exit(0)

assert mode=='aplicar'
assert json.loads((store/'ensayo_etapa4.json').read_text())['estado']=='ensayo_013_ok'
previous=store/('etapa4-fuentes-previas-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S'));previous.mkdir(mode=0o700)
for name in allowed:
 p=root/name
 if p.exists():
  saved=previous/name;saved.parent.mkdir(parents=True,exist_ok=True);saved.write_bytes(p.read_bytes())

def install(name,content):
 p=root/name;assert not p.is_symlink() and not p.parent.is_symlink()
 if not p.parent.exists():
  p.parent.mkdir(mode=0o750);os.chown(p.parent,0,gid);os.chmod(p.parent,0o750)
 old=p.stat() if p.exists() else None
 fd,temporary=tempfile.mkstemp(prefix='.etapa4-',dir=p.parent)
 try:
  with os.fdopen(fd,'w',encoding='utf-8') as stream:stream.write(content)
  os.chown(temporary,old.st_uid if old else 0,old.st_gid if old else gid)
  os.chmod(temporary,stat.S_IMODE(old.st_mode) if old else 0o640)
  os.replace(temporary,p)
 finally:
  if os.path.exists(temporary):os.unlink(temporary)

subprocess.run(['systemctl','stop','readyproof'],check=True,capture_output=True,timeout=240)
try:
 subprocess.run(['/var/backups/readyproof/backup_y_subida.sh'],check=True,capture_output=True,timeout=600)
 backup=json.loads((store/'ultimo_backup.json').read_text());assert backup['schema']=='012_sistema_cliente_activo'
 remote='readyproof-drive:readyproof-backups/pre-migrations/readyproof-pre-013-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'.tar.enc'
 for suffix in ('','.json'):
  subprocess.run(['rclone','--config','/etc/readyproof/rclone-backup.conf','copyto',backup['remote']+suffix,remote+suffix],check=True,capture_output=True,timeout=120)
 with tempfile.TemporaryDirectory(prefix='.pre013-',dir=store) as directory:
  file=Path(directory)/'copia.enc'
  subprocess.run(['rclone','--config','/etc/readyproof/rclone-backup.conf','copyto',remote,str(file)],check=True,capture_output=True,timeout=120)
  assert hashlib.sha256(file.read_bytes()).hexdigest()==backup['cipher_sha256']
 for name,content in data['files'].items():install(name,content)
 # Ejecutar imports con el mismo usuario del servicio antes de alterar el esquema.
 smoke="import sys;sys.path.insert(0,'/home/readyproof');from app import create_app;from app.models import EmisionCarga,NumeroRegistroContador;from app.planillas.sdi_validacion import ESTADOS;assert len(ESTADOS)==4;assert create_app().config['MAIL_MODO_PRUEBA']"
 subprocess.run(['runuser','-u','readyproof','--',str(root/'venv/bin/python'),'-c',smoke],check=True,capture_output=True,timeout=60)
 with engine.begin() as c:result=migrate(c,root/'migraciones/alembic')
except Exception:
 # El esquema es aditivo: restaurar las fuentes anteriores sin borrar datos ni retroceder DDL.
 for name in allowed:
  saved=previous/name
  if saved.exists():install(name,saved.read_text(encoding='utf-8'))
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
result.update(estado='etapa4_aplicada',schema='013_desbloqueo_revision',fuentes_previas=str(previous),
 respaldo_pre_migracion=remote,respaldo_sha256=backup['cipher_sha256'],login_http=200,modo_piloto=True)
(store/'aplicacion_etapa4.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
'''


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=('inspeccionar','ensayar','aplicar'))
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    files={name:(ROOT/name).read_text(encoding='utf-8') for name in FILES}
    data={'mode':args.mode,'files':files}
    if args.mode!='inspeccionar':
        data['previous']=json.loads((OUT/'inspeccionar.json').read_text())['hashes']
    if args.mode=='aplicar':
        suite=json.loads((OUT/'estado_suite.json').read_text())
        assert suite['estado']=='aprobada' and suite['fallos']==suite['errores']==suite['omitidas']==0
        assert suite['huellas_fuente']=={name:hashlib.sha256(content.encode()).hexdigest() for name,content in files.items()}, 'El código cambió después de las pruebas.'
    cmd=['ssh','-i',str(Path.home()/'.ssh/readyproof_deploy_67_205_170_29'),'-o','IdentitiesOnly=yes',
         '-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=15',
         'root@67.205.170.29','/home/readyproof/venv/bin/python -c '+shlex.quote(CODE)]
    result=subprocess.run(cmd,input=json.dumps(data).encode(),capture_output=True,timeout=1200)
    if result.returncode:
        import re
        lines=result.stderr.decode(errors='replace').splitlines()
        report={'estado':'fallo','mode':args.mode,
            'tipos':[line.split(':')[0] for line in lines if re.match(r'^[\w.]+(?:Error|Exception):',line)],
            'lineas':[line.strip() for line in lines if line.lstrip().startswith('File ')]}
        (OUT/(args.mode+'_error.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
        print(json.dumps(report));return 1
    report=json.loads(result.stdout)
    (OUT/(args.mode+'.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report));return 0


if __name__=='__main__':raise SystemExit(main())
