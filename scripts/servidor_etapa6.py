"""Ensayo e instalación del corte de etapa 6, conservando el piloto y los datos."""
from datetime import datetime,timezone
import hashlib,json,os
from pathlib import Path
import subprocess,sys,tempfile

ROOT=Path('/home/readyproof')
STAGE=Path('/home/readyproof_revision_etapa5')
STORE=Path('/var/backups/readyproof')
HEAD='016_tabla_auditoria'
FILES=('app/__init__.py','app/models/__init__.py','app/config.py','app/modo.py','app/auth/rutas.py',
 'app/carga/servicios.py','app/carga/rutas.py','app/auditoria/__init__.py','app/auditoria/rutas.py',
 'app/rutas/api.py','app/correo/__init__.py','app/correo/rutas.py','app/planillas/validacion.py',
 'app/planillas/firmantes.py','app/planillas/registro_pdf.py','app/planillas/identificacion_pdf.py',
 'app/static/carga.js','app/static/sw.js','app/templates/carga.html','app/templates/admin.html',
 'migraciones/alembic/versions/016_tabla_auditoria.py','scripts/backup_readyproof.py',
 'docs/API.md','docs/AUDITORIA.md','docs/CONFIG_MODO_REAL.md','docs/TRANSICION_PILOTO_A_REAL.md')


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def run(args,**kwargs):return subprocess.run(args,check=True,capture_output=True,timeout=700,**kwargs)


def environment():
 from dotenv import load_dotenv
 from sqlalchemy import create_engine
 from sqlalchemy.engine import make_url
 load_dotenv(ROOT/'.env.local');load_dotenv(ROOT/'.env')
 url=make_url(os.environ['DATABASE_URL']);assert url.database=='readyproof' and url.host in ('localhost','127.0.0.1','::1')
 return create_engine(url),url


def snapshot(c):
 from sqlalchemy import inspect,text
 result={};quote=c.dialect.identifier_preparer.quote
 for name in sorted(inspect(c).get_table_names()):
  if name in ('alembic_version','versiones_esquema'):continue
  keys=inspect(c).get_pk_constraint(name)['constrained_columns']
  result[name]={repr(tuple(r[k] for k in keys)):hashlib.sha256(repr(tuple(r.values())).encode()).hexdigest()
   for r in c.execute(text('SELECT * FROM '+quote(name))).mappings()}
 return result


def migrate(c):
 from alembic import command
 from alembic.config import Config
 from sqlalchemy import text
 assert c.scalar(text('SELECT version_num FROM alembic_version'))=='014_habilitar_11_sistemas'
 before=snapshot(c)
 cfg=Config(str(STAGE/'alembic.ini'));cfg.set_main_option('script_location',str(STAGE/'migraciones/alembic'))
 cfg.attributes['connection']=c;command.upgrade(cfg,HEAD)
 after=snapshot(c);assert set(after)==set(before)|{'auditoria'} and not after['auditoria']
 assert all(records==after[name] for name,records in before.items())
 assert c.scalar(text('SELECT count(*) FROM versiones_esquema WHERE numero=16'))==1
 return {'schema':HEAD,'filas_anteriores_conservadas':sum(map(len,before.values())),
  'tablas_anteriores':len(before),'tablas_nuevas':['auditoria'],'auditoria_inicial':0,'datos_historicos_modificados':False}


def inspect_live():
 from sqlalchemy import text
 engine,_=environment()
 with engine.begin() as c:
  c.execute(text('SET TRANSACTION READ ONLY'))
  result={'schema':c.scalar(text('SELECT version_num FROM alembic_version')),
   'counts':{name:c.scalar(text('SELECT count(*) FROM '+name)) for name in ('cargas','planillas','sistemas','envios','firmas_carga')},
   'fuentes':{name:digest(ROOT/name) if (ROOT/name).exists() else None for name in FILES}}
 engine.dispose();return result


def rehearse():
 from sqlalchemy import create_engine
 engine,url=environment();engine.dispose()
 name='readyproof_test_etapa6_migracion_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
 with tempfile.TemporaryDirectory(prefix='.ensayo016-',dir=STORE) as work:
  p=Path(work)/'db.dump'
  with p.open('wb') as stream:
   subprocess.run(['/usr/sbin/runuser','-u','postgres','--','pg_dump','--format=custom','--no-owner','--no-acl','readyproof'],stdout=stream,stderr=subprocess.PIPE,check=True,timeout=180)
  run(['/usr/sbin/runuser','-u','postgres','--','createdb','--owner='+url.username,name])
  with p.open('rb') as stream:run(['/usr/sbin/runuser','-u','postgres','--','pg_restore','--exit-on-error','--single-transaction','--no-owner','--no-acl','--role='+url.username,'--dbname='+name],stdin=stream)
  test=create_engine(url.set(database=name))
  with test.begin() as c:report=migrate(c)
  test.dispose()
 report.update(estado='ensayo_016_OK',base_aislada=name,produccion_modificada=False)
 (STORE/'ensayo_etapa6.json').write_text(json.dumps(report,indent=2));return report


def apply(data):
 import grp,pwd,re
 from dotenv import dotenv_values
 assert data['pruebas']['fallidos']==0 and data['pruebas']['aprobados']>=541 and data['pruebas']['cobertura_lineas_python']>=85
 assert set(data['fuentes'])==set(FILES)
 for name,value in data['fuentes'].items():assert digest(STAGE/name)==value
 state=inspect_live();assert state['schema']=='014_habilitar_11_sistemas' and state['fuentes']==data['anteriores']
 assert json.loads((STORE/'ensayo_etapa6.json').read_text())['estado']=='ensayo_016_OK'
 unit=run(['systemctl','show','readyproof','--property=Environment','--value']).stdout.decode()
 import shlex
 assert all(not value.startswith('MODO_PILOTO=') or value=='MODO_PILOTO=true' for value in shlex.split(unit))
 stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S');previous=STORE/('etapa6-previas-'+stamp);previous.mkdir(mode=0o700)
 gid=grp.getgrnam('readyproof').gr_gid;uid=pwd.getpwnam('readyproof').pw_uid
 for name in FILES:
  p=ROOT/name
  if p.exists():dest=previous/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes())
 envfile=ROOT/'.env.local';env_existed=envfile.exists();env_old=envfile.read_bytes() if env_existed else b''
 (previous/'entorno_anterior_privado').write_bytes(env_old);os.chmod(previous/'entorno_anterior_privado',0o600)
 def install(name,payload):
  p=ROOT/name;assert p.resolve().is_relative_to(ROOT) and not p.is_symlink()
  if not p.parent.exists():
   p.parent.mkdir(mode=0o750);os.chown(p.parent,0,gid);os.chmod(p.parent,0o750)
  assert not p.parent.is_symlink()
  fd,temp=tempfile.mkstemp(prefix='.etapa6-',dir=p.parent)
  try:
   with os.fdopen(fd,'wb') as stream:stream.write(payload)
   os.chown(temp,0,gid);os.chmod(temp,0o640);os.replace(temp,p)
  finally:
   if os.path.exists(temp):os.unlink(temp)
 run(['systemctl','stop','readyproof'])
 try:
  run(['/var/backups/readyproof/backup_y_subida.sh'])
  backup=json.loads((STORE/'ultimo_backup.json').read_text());assert backup['schema']=='014_habilitar_11_sistemas'
  remote='readyproof-drive:readyproof-backups/pre-migrations/readyproof-pre-016-'+stamp+'.tar.enc'
  for suffix in ('','.json'):run(['rclone','--config','/etc/readyproof/rclone-backup.conf','copyto',backup['remote']+suffix,remote+suffix])
  with tempfile.TemporaryDirectory(prefix='.pre016-',dir=STORE) as work:
   p=Path(work)/'backup.enc';run(['rclone','--config','/etc/readyproof/rclone-backup.conf','copyto',remote,str(p)]);assert digest(p)==backup['cipher_sha256']
  for name in FILES:install(name,(STAGE/name).read_bytes())
  text_env=env_old.decode('utf-8-sig')
  for key in ('MODO_PILOTO','MAIL_MODO_PRUEBA'):
   pattern=r'(?m)^(?:export\s+)?'+key+r'\s*=.*$'
   text_env=re.sub(pattern,key+'=true',text_env) if re.search(pattern,text_env) else text_env.rstrip()+'\n'+key+'=true\n'
  envfile.write_text(text_env,encoding='utf-8');os.chown(envfile,uid,gid);os.chmod(envfile,0o600)
  import io
  old_values=dotenv_values(stream=io.StringIO(env_old.decode('utf-8-sig')));new_values=dotenv_values(envfile)
  assert all(new_values.get(k)==v for k,v in old_values.items() if k not in ('MODO_PILOTO','MAIL_MODO_PRUEBA'))
  os.environ['MODO_PILOTO']='true';os.environ['MAIL_MODO_PRUEBA']='true'
  engine,_=environment()
  with engine.begin() as c:report=migrate(c)
  engine.dispose()
 except Exception:
  for name in FILES:
   saved=previous/name
   if saved.exists():install(name,saved.read_bytes())
   elif (ROOT/name).exists():(ROOT/name).unlink()
  if env_existed:envfile.write_bytes(env_old)
  elif envfile.exists():envfile.unlink()
  raise
 finally:run(['systemctl','start','readyproof'])
 report.update(estado='etapa6_aplicada_en_piloto',fuentes_previas=str(previous),respaldo_previo=remote,modo_piloto=True,mail_modo_prueba=True,credenciales_modificadas=False)
 (STORE/'aplicacion_etapa6.json').write_text(json.dumps(report,indent=2));return report


def verify(data):
 import time
 from urllib.request import urlopen
 from urllib.error import HTTPError,URLError
 for name,value in data['fuentes'].items():assert digest(ROOT/name)==value
 for _ in range(20):
  try:
   with urlopen('http://127.0.0.1:8000/static/carga.js',timeout=10) as response:assert hashlib.sha256(response.read()).hexdigest()==data['fuentes']['app/static/carga.js']
   break
  except URLError:time.sleep(1)
 else:raise RuntimeError('No respondió readyproof.')
 statuses={}
 for path in ('/api/carga/buscar?numero=1','/api/auditoria'):
  try:urlopen('http://127.0.0.1:8000'+path,timeout=10)
  except HTTPError as error:statuses[path]=error.code
 assert set(statuses.values())=={401}
 smoke="import sys,json;sys.path.insert(0,'/home/readyproof');from app import create_app;a=create_app();assert a.config['MODO_PILOTO'] and a.config['MAIL_MODO_PRUEBA'];print(json.dumps({'modo_piloto':True,'mail_modo_prueba':True}))"
 flags=json.loads(run(['/usr/sbin/runuser','-u','readyproof','--',str(ROOT/'venv/bin/python'),'-c',smoke]).stdout)
 run(['systemctl','start','readyproof-backup.service']);backup=json.loads((STORE/'ultimo_backup.json').read_text());assert backup['schema']==HEAD
 restored=json.loads(run([str(ROOT/'venv/bin/python'),str(ROOT/'scripts/backup_readyproof.py'),'restore','--remote',backup['remote'],
  '--schema-esperado',HEAD,'--planillas-esperadas',str(backup['counts']['planillas']),'--prefijo-prueba','readyproof_test_etapa5']).stdout)
 assert not restored['produccion_modificada'] and restored['cipher_sha256']==backup['cipher_sha256']
 report={'estado':'etapa6_verificada','schema':HEAD,'flags':flags,'rutas_sin_sesion':statuses,'backup':backup,'restauracion':restored,
  'servicio':run(['systemctl','is-active','readyproof']).stdout.decode().strip(),'timer':run(['systemctl','is-active','readyproof-backup.timer']).stdout.decode().strip(),
  'fuentes_coinciden':True,'modo_real_activado':False,'correos_de_prueba_transmitidos':False}
 (STORE/'verificacion_etapa6.json').write_text(json.dumps(report,indent=2));return report


def main():
 assert sys.platform!='win32' and os.geteuid()==0
 sys.path.insert(0,str(STAGE));os.umask(0o077);data=json.load(sys.stdin)
 actions={'inspeccionar':inspect_live,'ensayar':rehearse,'aplicar':lambda:apply(data),'verificar':lambda:verify(data)}
 try:print(json.dumps(actions[data['accion']]()))
 except Exception as error:
  import traceback
  result={'estado':'fallo','accion':data['accion'],'tipo':type(error).__name__,'lineas':[{'archivo':f.filename,'linea':f.lineno} for f in traceback.extract_tb(error.__traceback__)]}
  (STORE/'error_etapa6.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));return 1
 return 0


if __name__=='__main__':raise SystemExit(main())
