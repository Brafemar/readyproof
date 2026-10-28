"""Ejecuta los 189 recorridos sobre clones efímeros de la restauración verificada."""
from datetime import datetime,timezone
import json
import os
from pathlib import Path
import pwd
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

STAGE=Path('/home/readyproof_revision_etapa5')
STORE=Path('/var/backups/readyproof')


def run(args,**kwargs):return subprocess.run(args,check=True,capture_output=True,timeout=180,**kwargs)


def counts(name):
    base=['/usr/sbin/runuser','-u','postgres','--','psql','-X','-qAt','--set=ON_ERROR_STOP=1','--dbname='+name]
    tables=json.loads(run(base,input="SELECT json_agg(tablename ORDER BY tablename) FROM pg_tables WHERE schemaname='public';",text=True).stdout)
    assert all(re.fullmatch('[a-z_]+',t) for t in tables)
    sql="SELECT json_build_object("+','.join("'"+t+"',(SELECT count(*) FROM \""+t+'\")' for t in tables)+');'
    return json.loads(run(base,input=sql,text=True).stdout)


def main():
    assert sys.platform!='win32' and os.geteuid()==0
    os.umask(0o077)
    restored=json.loads((STORE/'verificacion_etapa5.json').read_text())['restauracion']
    name=restored['database'];assert re.fullmatch(r'readyproof_test_etapa5_[0-9]{8}T[0-9]{6}',name)
    assert restored['schema']=='014_habilitar_11_sistemas' and not restored['produccion_modificada']
    before=counts(name)
    dump=STAGE/'recursos/prueba_restaurada.dump';assert not dump.is_symlink()
    with dump.open('wb') as stream:
        subprocess.run(['/usr/sbin/runuser','-u','postgres','--','pg_dump','--format=custom','--no-owner','--no-acl',name],
            stdout=stream,stderr=subprocess.PIPE,check=True,timeout=180)
    uid=pwd.getpwnam('readyproof').pw_uid;os.chown(dump,uid,-1);os.chmod(dump,0o600)
    env={'PATH':'/home/readyproof/venv/bin:/usr/local/bin:/usr/bin:/bin','HOME':'/home/readyproof','LANG':'C.UTF-8',
        'PYTHONPATH':str(STAGE),'PYTHONDONTWRITEBYTECODE':'1','PG_BINDIR':'/usr/lib/postgresql/16/bin',
        'READYPROOF_RESTORE_DUMP':str(dump),'READYPROOF_EXCEL_ORIGEN':str(STAGE/'recursos/originales_v5.zip'),
        'READYPROOF_PDF_EVIDENCIA':str(STAGE/'out/pdf_restaurados')}
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S');base=STAGE/'pruebas'/('restore_'+stamp);assert not base.exists()
    xml=STAGE/'out/restaurada.xml';log=STAGE/'out/pytest_restaurada.txt'
    for p in (xml,log):
        if p.exists():p.rename(p.with_name(p.stem+'_'+stamp+p.suffix))
    with log.open('w') as stream:
        os.chown(log,uid,-1)
        result=subprocess.run(['/usr/sbin/runuser','-u','readyproof','--','/home/readyproof/venv/bin/python','-u','-m','pytest',
            '-q','-p','no:cacheprovider','--basetemp',str(base),'--junitxml',str(xml),'tests/test_etapa5_planillas.py'],
            cwd=STAGE,env=env,stdout=stream,stderr=subprocess.STDOUT)
    cases=list(ET.parse(xml).getroot().iter('testcase'))
    failures=[c.attrib['name'] for c in cases if any(c.find(t) is not None for t in ('failure','error','skipped'))]
    after=counts(name)
    report={'estado':'pruebas_restauradas_aprobadas' if not failures and result.returncode==0 else 'fallo',
        'casos':len(cases),'fallos':failures,'codigo':result.returncode,'base_restaurada':name,
        'base_restaurada_sin_cambios':before==after,'base_de_pruebas':'clones efímeros en clúster temporal, un clon por caso con BD',
        'counts':after,'credenciales_produccion_en_tests':False}
    assert len(cases)==189 and before==after
    (STORE/'pruebas_restauradas_etapa5.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report));return result.returncode


if __name__=='__main__':raise SystemExit(main())
