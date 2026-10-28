"""Copia privada de pruebas de etapa 5; nunca usa la BD ni el entorno de producción."""
import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
import shlex
import subprocess
import tarfile

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'out/etapa5_planillas'
STAGE='/home/readyproof_revision_etapa5'


def ssh(code,*,payload=b'',timeout=1800):
    cmd=['ssh','-i',str(Path.home()/'.ssh/readyproof_deploy_67_205_170_29'),'-o','IdentitiesOnly=yes',
        '-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=15','root@67.205.170.29',
        '/home/readyproof/venv/bin/python -c '+shlex.quote(code)]
    result=subprocess.run(cmd,input=payload,capture_output=True,timeout=timeout)
    if result.returncode:
        import re
        lines=result.stderr.decode(errors='replace').splitlines()
        print(json.dumps({'estado':'fallo','tipos':[l.split(':')[0] for l in lines if re.match(r'^[\w.]+(?:Error|Exception):',l)],
            'lineas':[l.strip() for l in lines if l.lstrip().startswith('File ')]}))
        raise RuntimeError('No se confirmó la operación remota; revisar evidencia privada.')
    return result.stdout


PREPARAR=r'''
from pathlib import Path,PurePosixPath
import sys,tarfile,io,json,os,grp,pwd,shutil,hashlib
stage=Path('/home/readyproof_revision_etapa5');gid=grp.getgrnam('readyproof').gr_gid;uid=pwd.getpwnam('readyproof').pw_uid
assert not stage.is_symlink()
stage.mkdir(mode=0o700,exist_ok=True);os.chown(stage,uid,gid);os.chmod(stage,0o700)
with tarfile.open(fileobj=io.BytesIO(sys.stdin.buffer.read()),mode='r:gz') as tar:
 for item in tar.getmembers():
  name=PurePosixPath(item.name)
  assert item.isfile() and not name.is_absolute() and '..' not in name.parts and '.env' not in name.parts
  assert name.parts[0] in {'app','tests','scripts','migraciones','docs','alembic.ini','requirements.txt','seleccion_pruebas.json'}
  p=stage/str(name);assert p.resolve().is_relative_to(stage) and not p.is_symlink()
  chain=[];parent=p.parent
  while parent!=stage:
   assert not parent.is_symlink();chain.append(parent);parent=parent.parent
  for directory in reversed(chain):
   if not directory.exists():directory.mkdir(mode=0o750);os.chown(directory,0,gid);os.chmod(directory,0o750)
  p.write_bytes(tar.extractfile(item).read());os.chown(p,0,gid);os.chmod(p,0o640)
for relative in ('herramientas','planillas'):
 source=Path('/home/readyproof/fuente')/relative
 for p in source.iterdir():
  if p.is_file() and p.suffix in {'.py','.json'}:
   dest=stage/'fuente'/relative/p.name;dest.parent.mkdir(parents=True,exist_ok=True)
   shutil.copyfile(p,dest);os.chown(dest,0,gid);os.chmod(dest,0o640)
dest=stage/'fuente/modelos/SDI-1.xlsx';dest.parent.mkdir(parents=True,exist_ok=True)
shutil.copyfile('/home/readyproof/fuente/modelos/SDI-1.xlsx',dest);os.chown(dest,0,gid);os.chmod(dest,0o640)
dest=stage/'recursos/originales_v5.zip';dest.parent.mkdir(parents=True,exist_ok=True)
shutil.copyfile('/var/backups/readyproof/revision-etapa3/originales_v5.zip',dest);os.chown(dest,0,gid);os.chmod(dest,0o640)
for dirname in ('fuente','fuente/herramientas','fuente/planillas','fuente/modelos','recursos'):
 p=stage/dirname;os.chown(p,0,gid);os.chmod(p,0o750)
for dirname in ('out','pruebas'):
 p=stage/dirname;p.mkdir(exist_ok=True);os.chown(p,uid,gid);os.chmod(p,0o700)
print(json.dumps({'estado':'copia_privada_preparada','ruta':str(stage),'secretos_copiados':False,
 'sha_zip':hashlib.sha256(dest.read_bytes()).hexdigest()}))
'''

PRUEBAS=r'''
from pathlib import Path
import json,subprocess,os,time
stage=Path('/home/readyproof_revision_etapa5')
selection=json.loads((stage/'seleccion_pruebas.json').read_text())
base=stage/'pruebas'/('pg_'+str(time.time_ns()));assert not base.exists()
for name in ('linux.xml','pytest_linux.txt'):
 old=stage/'out'/name
 if old.exists():old.rename(old.with_name(old.stem+'_'+str(time.time_ns())+old.suffix))
env={'PATH':'/home/readyproof/venv/bin:/usr/local/bin:/usr/bin:/bin','HOME':'/home/readyproof','LANG':'C.UTF-8',
 'PYTHONPATH':str(stage),'PYTHONDONTWRITEBYTECODE':'1','READYPROOF_EXCEL_ORIGEN':str(stage/'recursos/originales_v5.zip'),
 'PG_BINDIR':'/usr/lib/postgresql/16/bin','READYPROOF_PDF_EVIDENCIA':str(stage/'out/pdf')}
with (stage/'out/pytest_linux.txt').open('w') as log:
 os.chown(log.name,__import__('pwd').getpwnam('readyproof').pw_uid,__import__('grp').getgrnam('readyproof').gr_gid)
 result=subprocess.run(['/usr/sbin/runuser','-u','readyproof','--','/home/readyproof/venv/bin/python','-u','-m','pytest',
  '-q','-p','no:cacheprovider','--basetemp',str(base),'--junitxml',str(stage/'out/linux.xml'),*selection['linux']],
  cwd=stage,env=env,stdout=log,stderr=subprocess.STDOUT)
print(json.dumps({'estado':'pruebas_ejecutadas','codigo':result.returncode,'casos_solicitados':len(selection['linux']),
 'junit':str(stage/'out/linux.xml'),'log':str(stage/'out/pytest_linux.txt')}))
'''

ESTADO=r'''
from pathlib import Path
import json,re,stat,xml.etree.ElementTree as ET
stage=Path('/home/readyproof_revision_etapa5');log=stage/'out/pytest_linux.txt'
lines=log.read_text(errors='replace').splitlines() if log.exists() else []
progress=[line for line in lines if re.fullmatch(r'[.FE]+(?:\s*\[.*\])?',line)]
report={'modo_carpeta':oct(stat.S_IMODE(stage.stat().st_mode)),'avance':progress[-2:]}
p=stage/'out/linux.xml'
if p.exists():
 cases=list(ET.parse(p).getroot().iter('testcase'))
 failed=[c.attrib['classname']+'::'+c.attrib['name'] for c in cases if c.find('failure') is not None or c.find('error') is not None]
 report.update(casos=len(cases),cantidad_fallos=len(failed),primeros_fallos=failed[:8])
print(json.dumps(report))
'''


def preparar(*, enviar=True):
    nodes=[line for line in (OUT/'coleccion.txt').read_text(encoding='utf-8').splitlines() if line.startswith('tests/') and '::' in line]
    windows_files={'tests/test_generacion.py','tests/test_etapa6_planillas.py','tests/test_marca_agua.py','tests/test_m1.py',
        'tests/test_interfaz.py','tests/test_selectores.py','tests/test_a4_historica.py'}
    windows_names={'test_selectores_funcionan','test_boton_documentacion_en_navegador_movil','test_vista_previa_no_finaliza_e_incorpora_firmas','test_modo_real_navegador'}
    windows=[n for n in nodes if n.split('::')[0] in windows_files or n.split('::')[1] in windows_names]
    linux=[n for n in nodes if n not in windows]
    assert len(nodes)==len(set(nodes))==len(windows)+len(linux)
    selection={'total':len(nodes),'windows':windows,'linux':linux}
    (OUT/'seleccion_pruebas.json').write_text(json.dumps(selection,indent=2),encoding='utf-8')
    paths=[]
    for directory in ('app','tests','scripts','migraciones','docs'):
        for p in (ROOT/directory).rglob('*'):
            if not p.is_file() or p.is_symlink() or '__pycache__' in p.parts:continue
            if directory=='docs' and p.suffix not in ('.md','.json'):continue
            if directory=='scripts' and p.suffix not in ('.py','.ps1','.sh','.service','.timer'):continue
            if p.name.startswith('.env') or p.suffix in ('.pyc','.db'):continue
            paths.append(p)
    paths += [ROOT/'alembic.ini',ROOT/'requirements.txt']
    payload=BytesIO()
    with tarfile.open(fileobj=payload,mode='w:gz') as tar:
        for p in sorted(paths):tar.add(p,arcname=p.relative_to(ROOT).as_posix(),recursive=False)
        info=tarfile.TarInfo('seleccion_pruebas.json');value=json.dumps(selection).encode();info.size=len(value);tar.addfile(info,BytesIO(value))
    package=payload.getvalue();(OUT/'revision_privada.tar.gz').write_bytes(package)
    manifest={'archivos':[str(p.relative_to(ROOT)).replace('\\','/') for p in sorted(paths)],
        'sha256':hashlib.sha256(package).hexdigest(),'bytes':len(package),'destino':STAGE,
        'casos_linux':len(linux),'casos_windows':len(windows),'secretos_incluidos':False}
    (OUT/'manifiesto_transferencia.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    if not enviar:
        print(json.dumps({k:v for k,v in manifest.items() if k!='archivos'}));return
    result=json.loads(ssh(PREPARAR,payload=payload.getvalue()))
    result.update(archivos=len(paths),casos_linux=len(linux),casos_windows=len(windows))
    (OUT/'preparacion_servidor.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('accion',choices=('empaquetar','preparar','pruebas','estado'))
    args=parser.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    if args.accion in ('preparar','empaquetar'):preparar(enviar=args.accion=='preparar')
    elif args.accion=='estado':print(ssh(ESTADO,timeout=60).decode())
    else:
        result=json.loads(ssh(PRUEBAS,timeout=3600));(OUT/'ejecucion_linux.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result))


if __name__=='__main__':main()
