"""Verificación privada de fuentes, servicio y restauración posterior a 013."""
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.aplicar_etapa4_revision import FILES, ROOT, OUT

CODE=r'''
import sys,json,hashlib,subprocess
from pathlib import Path
from urllib.request import urlopen
root=Path('/home/readyproof');store=Path('/var/backups/readyproof')
data=json.load(sys.stdin)
for name,digest in data['hashes'].items():
 assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest
assert subprocess.run(['systemctl','is-active','readyproof'],check=True,capture_output=True,text=True).stdout.strip()=='active'
assert subprocess.run(['systemctl','show','readyproof','-p','User','--value'],check=True,capture_output=True,text=True).stdout.strip()=='readyproof'
assert subprocess.run(['systemctl','is-active','readyproof-backup.timer'],check=True,capture_output=True,text=True).stdout.strip()=='active'
with urlopen('http://127.0.0.1:8000/login',timeout=15) as response:assert response.status==200
with urlopen('http://127.0.0.1:8000/static/carga.js',timeout=15) as response:
 assert hashlib.sha256(response.read()).hexdigest()==data['hashes']['app/static/carga.js']
with urlopen('http://127.0.0.1:8000/sw.js',timeout=15) as response:assert b'readyproof-ui-v8' in response.read()
subprocess.run(['systemctl','start','readyproof-backup.service'],check=True,capture_output=True,timeout=700)
backup=json.loads((store/'ultimo_backup.json').read_text());assert backup['schema']=='013_desbloqueo_revision'
restored=subprocess.run([str(root/'venv/bin/python'),str(root/'scripts/backup_readyproof.py'),'restore',
 '--remote',backup['remote'],'--schema-esperado','013_desbloqueo_revision','--planillas-esperadas',str(backup['counts']['planillas'])],
 check=True,capture_output=True,text=True,timeout=700)
restore=json.loads(restored.stdout);assert restore['produccion_modificada'] is False
assert restore['cipher_sha256']==backup['cipher_sha256']
report={'estado':'etapa4_verificada','fuentes_coinciden':True,'servicio_activo':True,'usuario_servicio':'readyproof',
 'login_http':200,'javascript_nuevo_servido':True,'service_worker':'v8','timer_activo':True,'backup':backup,'restauracion':restore}
(store/'verificacion_etapa4.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
'''


def main():
    data={'hashes':{name:hashlib.sha256((ROOT/name).read_text(encoding='utf-8').encode()).hexdigest() for name in FILES}}
    cmd=['ssh','-i',str(Path.home()/'.ssh/readyproof_deploy_67_205_170_29'),'-o','IdentitiesOnly=yes',
         '-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=15',
         'root@67.205.170.29','/home/readyproof/venv/bin/python -c '+shlex.quote(CODE)]
    result=subprocess.run(cmd,input=json.dumps(data).encode(),capture_output=True,timeout=1500)
    if result.returncode:
        import re
        lines=result.stderr.decode(errors='replace').splitlines()
        report={'estado':'fallo_verificacion','tipos':[line.split(':')[0] for line in lines if re.match(r'^[\w.]+(?:Error|Exception):',line)],
            'lineas':[line.strip() for line in lines if line.lstrip().startswith('File ')]}
        (OUT/'verificacion_error.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report));return 1
    report=json.loads(result.stdout)
    (OUT/'verificacion_servidor.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report));return 0


if __name__=='__main__':raise SystemExit(main())
