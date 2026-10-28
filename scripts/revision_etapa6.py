"""Pruebas de etapa 6 en PostgreSQL temporal y carpeta privada autorizada."""
import argparse
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import subprocess
import sys

import revision_etapa5 as prior

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'out/etapa6_final'
STAGE='/home/readyproof_revision_etapa5'


def preparar():
    OUT.mkdir(parents=True,exist_ok=True)
    collection=subprocess.run([sys.executable,'-m','pytest','--collect-only','-q','-p','no:cacheprovider'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',check=True)
    (OUT/'coleccion.txt').write_text(collection.stdout,encoding='utf-8')
    prior.OUT=OUT;prior.preparar()
    files={name:(ROOT/name).read_text(encoding='utf-8') for name in ('.coveragerc','requirements-dev.txt')}
    code=r'''
from pathlib import Path
import sys,json,subprocess,grp,os
stage=Path('/home/readyproof_revision_etapa5');gid=grp.getgrnam('readyproof').gr_gid;values=json.load(sys.stdin)
assert set(values)=={'.coveragerc','requirements-dev.txt'}
for name,value in values.items():
 p=stage/name;assert not p.is_symlink();p.write_text(value);os.chown(p,0,gid);os.chmod(p,0o640)
deps=stage/'deps_etapa6';assert not deps.is_symlink()
if not (deps/'coverage').exists():
 result=subprocess.run(['/home/readyproof/venv/bin/python','-m','pip','install','--disable-pip-version-check','--no-input','--target',str(deps),'coverage==7.17.0'],capture_output=True,timeout=240)
 if result.returncode:raise RuntimeError('No se pudo preparar coverage privado; no se modificó el entorno productivo.')
for base,dirs,files in os.walk(deps):
 os.chown(base,0,gid);os.chmod(base,0o750)
 for name in files:os.chown(Path(base)/name,0,gid);os.chmod(Path(base)/name,0o640)
p=stage/'out/cobertura';p.mkdir(exist_ok=True);os.chown(p,__import__('pwd').getpwnam('readyproof').pw_uid,gid);os.chmod(p,0o700)
print(json.dumps({'estado':'preparado','coverage':'7.17.0','dependencia_solo_pruebas':True,'produccion_modificada':False}))
'''
    result=json.loads(prior.ssh(code,payload=json.dumps(files).encode(),timeout=300))
    (OUT/'entorno_pruebas.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))


def linux():
    runner=prior.PRUEBAS.replace('linux.xml','etapa6_linux_final.xml').replace('pytest_linux.txt','pytest_etapa6_linux_final_final.txt')
    runner=runner.replace("'PYTHONPATH':str(stage)","'PYTHONPATH':str(stage/'deps_etapa6')+':'+str(stage)")
    runner=runner.replace("'PG_BINDIR':'/usr/lib/postgresql/16/bin'","'COVERAGE_FILE':str(stage/'out/cobertura/.coverage.linux'),'PG_BINDIR':'/usr/lib/postgresql/16/bin'")
    runner=runner.replace("'-u','-m','pytest'","'-u','-m','coverage','run','--rcfile',str(stage/'.coveragerc'),'-m','pytest'")
    runner=runner.replace("'-q','-p'","'-v','--tb=short','-x','-p'").replace("str(stage/'out/pdf')","str(stage/'out/etapa6_pdf')")
    runner+="\n(stage/'out/etapa6_linux_final_resultado.json').write_text(json.dumps({'codigo':result.returncode,'casos_solicitados':len(selection['linux'])}))\n"
    code=r'''
from pathlib import Path
import os,sys,grp,json,subprocess
stage=Path('/home/readyproof_revision_etapa5');p=stage/'scripts/runner_etapa6_final.py'
assert not p.is_symlink();p.write_bytes(sys.stdin.buffer.read());os.chown(p,0,grp.getgrnam('readyproof').gr_gid);os.chmod(p,0o640)
assert not (stage/'out/etapa6_linux_final_resultado.json').exists()
with (stage/'out/control_etapa6.txt').open('wb') as log:
 child=subprocess.Popen(['/home/readyproof/venv/bin/python',str(p)],cwd=stage,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,close_fds=True)
print(json.dumps({'estado':'iniciado','pid':child.pid}))
'''
    print(prior.ssh(code,payload=runner.encode(),timeout=60).decode())


def windows():
    selection=json.loads((OUT/'seleccion_pruebas.json').read_text());base=ROOT/'.venv/tmp/zu';assert not base.exists()
    cov=OUT/'cobertura/full';cov.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,NODE_PATH=str(Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules'),COVERAGE_FILE=str(cov/'.coverage.windows'))
    with (OUT/'pytest_windows.txt').open('w',encoding='utf-8') as log:
        result=subprocess.run([sys.executable,'-m','coverage','run','-m','pytest','-v','--tb=short','-x','-p','no:cacheprovider',
            '--basetemp',str(base),'--junitxml',str(OUT/'windows.xml'),*selection['windows']],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
    report={'codigo':result.returncode,'casos_solicitados':len(selection['windows'])}
    (OUT/'resultado_windows.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));raise SystemExit(result.returncode)


def estado():
    code=r'''
from pathlib import Path
import json
base=Path('/home/readyproof_revision_etapa5/out');p=base/'etapa6_linux_final_resultado.json';log=base/'pytest_etapa6_linux_final_final.txt'
lines=log.read_text(errors='replace').splitlines() if log.exists() else []
print(json.dumps({'resultado':json.loads(p.read_text()) if p.exists() else None,'avance':[s for s in lines if '%' in s][-1:]}))
'''
    print(prior.ssh(code,timeout=60).decode())


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('accion',choices=('preparar','linux','windows','estado'))
    args=parser.parse_args();{'preparar':preparar,'linux':linux,'windows':windows,'estado':estado}[args.accion]()
