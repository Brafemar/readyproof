"""Consolida evidencia y coordina las verificaciones privadas de etapa 5."""
import argparse
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import tarfile
import xml.etree.ElementTree as ET

from revision_etapa5 import ROOT,OUT,STAGE,ssh
from servidor_etapa5 import FILES


def recoger():
    code=r'''
from pathlib import Path
import sys,tarfile
stage=Path('/home/readyproof_revision_etapa5')
with tarfile.open(fileobj=sys.stdout.buffer,mode='w|gz') as tar:
 for relative in ('out/linux.xml','out/pytest_linux.txt','out/etapa5_planillas/paginacion_referencia.json'):
  p=stage/relative
  if p.exists():tar.add(p,arcname=p.name,recursive=False)
 for p in sorted((stage/'out/pdf').glob('*.pdf')):tar.add(p,arcname='pdf_verificados/'+p.name,recursive=False)
'''
    value=ssh(code,timeout=120)
    with tarfile.open(fileobj=BytesIO(value),mode='r:gz') as tar:
        for item in tar.getmembers():
            dest=(OUT/item.name).resolve()
            assert item.isfile() and dest.is_relative_to(OUT.resolve())
            dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(tar.extractfile(item).read())
    selection=json.loads((OUT/'seleccion_pruebas.json').read_text())
    def outcomes(path):
        return {c.attrib['classname'].replace('.','/')+'.py::'+c.attrib['name']:
            not any(c.find(tag) is not None for tag in ('failure','error','skipped'))
            for c in ET.parse(path).getroot().iter('testcase')}
    linux=outcomes(OUT/'linux.xml')
    assert set(linux)==set(selection['linux']) and all(linux.values())
    windows={}
    for name in ('windows.xml','local_restante.xml','reintento_y_formatos.xml'):
        windows.update({k:v for k,v in outcomes(OUT/name).items() if k in selection['windows']})
    assert set(windows)==set(selection['windows']) and all(windows.values())
    report={'estado':'aprobada','fallos_pendientes':0,'casos_unicos':len(linux)+len(windows),
        'ubuntu':len(linux),'windows':len(windows),'invocacion_unica':False,
        'nota':'Suite consolidada por plataforma; reintentos documentados, sin casos omitidos.'}
    (OUT/'pruebas_consolidadas.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report


def server(action):
    script=ROOT/'scripts/servidor_etapa5.py';digest=sha256(script.read_bytes()).hexdigest()
    data={'accion':action,'fuentes':{name:sha256((ROOT/name).read_bytes()).hexdigest() for name in FILES}}
    if action=='aplicar':
        data.update(pruebas=json.loads((OUT/'pruebas_consolidadas.json').read_text()),
            anteriores=json.loads((OUT/'inspeccionar.json').read_text())['hashes'])
    code="import hashlib,runpy;from pathlib import Path;p=Path("+repr(STAGE+'/scripts/servidor_etapa5.py')+");assert hashlib.sha256(p.read_bytes()).hexdigest()=="+repr(digest)+";runpy.run_path(str(p),run_name='__main__')"
    result=json.loads(ssh(code,payload=json.dumps(data).encode(),timeout=2400))
    (OUT/(action+'.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
    # Los reportes detallados se conservan en archivos; no se imprimen registros ni secretos.
    return {k:v for k,v in result.items() if k in ('estado','schema','counts','planillas_totales','sistemas_tipo','login_http','base_aislada','produccion_modificada')}


def estado():
    code=r'''
import subprocess,json
from pathlib import Path
store=Path('/var/backups/readyproof')
result={'servicios':{name:subprocess.run(['systemctl','is-active',name],capture_output=True,text=True).stdout.strip()
 for name in ('readyproof','readyproof-backup.service','readyproof-backup.timer')}}
for name in ('aplicacion_etapa5.json','verificacion_etapa5.json','error_etapa5.json','pruebas_restauradas_etapa5.json'):
 p=store/name
 if p.exists():
  data=json.loads(p.read_text());result[name]={k:v for k,v in data.items() if k in ('estado','accion','tipo','lineas','schema','planillas_totales','casos','codigo','fallos')}
p=Path('/home/readyproof_revision_etapa5/out/pytest_restaurada.txt')
if p.exists():
 import re
 result['avance_restauradas']=[line for line in p.read_text().splitlines() if re.fullmatch(r'[.FE]+(?:\s*\[.*\])?',line)][-2:]
print(json.dumps(result))
'''
    return json.loads(ssh(code,timeout=60))


def restauradas():
    path=ROOT/'scripts/prueba_restaurada_etapa5.py'
    digest=sha256(path.read_bytes()).hexdigest()
    code="import hashlib,runpy;from pathlib import Path;p=Path("+repr(STAGE+'/scripts/prueba_restaurada_etapa5.py')+");assert hashlib.sha256(p.read_bytes()).hexdigest()=="+repr(digest)+";runpy.run_path(str(p),run_name='__main__')"
    result=json.loads(ssh(code,timeout=2400))
    (OUT/'pruebas_restauradas.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return {k:v for k,v in result.items() if k in ('estado','casos','fallos','codigo','base_restaurada_sin_cambios')}


def catalogo_final():
    code=r'''
import sys,json
sys.path.insert(0,'/home/readyproof')
from pathlib import Path
from collections import Counter
from sqlalchemy import select,text
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
load_dotenv('/home/readyproof/.env.local');load_dotenv('/home/readyproof/.env')
from app.models import Planilla,Sistema
from app.config import SISTEMAS_HABILITADOS
from app.catalogo import huella_saa1
from app.planillas.catalogo_completo import definiciones_habilitadas
from scripts.importador_planillas import preparar,importar
engine=create_engine(os.environ['DATABASE_URL']);definitions=definiciones_habilitadas()
rows=preparar(Path('/home/readyproof_revision_etapa5/recursos/originales_v5.zip'),Path('/home/readyproof_revision_etapa5/docs/pedido_codex_v1_1/catalogo_referencia_planillas.json'))
with Session(engine) as db,db.begin():
 db.execute(text('SET TRANSACTION READ ONLY'))
 valid=[]
 for p in db.scalars(select(Planilla)):
  d=definitions.get(p.codigo)
  if (p.codigo=='SG-PEM-IFI-SAA-1' and p.huella==huella_saa1()) or (d and p.version==d['version'] and p.huella==d['huella']):valid.append(p)
 assert len(valid)==len({p.codigo for p in valid})==79
 types=set(db.scalars(select(Sistema.tipo).where(Sistema.activo.is_(True))))
 assert types==set(SISTEMAS_HABILITADOS)
 repeat=importar(db,rows,aplicar=False);assert not repeat['errores'] and repeat['estados']=={'YA_EXISTE':79} and repeat['cambios']==0
 result={'planillas_activas':len(valid),'familias':dict(sorted(Counter(p.sistema_tipo for p in valid).items())),
   'nombres_sistemas':SISTEMAS_HABILITADOS,'sistemas_activos':len(types),'reimportacion':repeat['estados'],
   'cambios_reimportacion':0,'consulta_solo_lectura':True}
engine.dispose();print(json.dumps(result))
'''
    result=json.loads(ssh(code,timeout=120))
    (OUT/'sistemas_finales.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('accion',choices=('recoger','inspeccionar','ensayar','aplicar','verificar','estado','restauradas','catalogo-final'))
    args=parser.parse_args()
    print(json.dumps(recoger() if args.accion=='recoger' else estado() if args.accion=='estado' else restauradas() if args.accion=='restauradas' else catalogo_final() if args.accion=='catalogo-final' else server(args.accion)))
