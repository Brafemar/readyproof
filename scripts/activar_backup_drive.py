"""Activa el timer solo si la subida y restauración de Etapa 1 ya se verificaron."""
import json
from pathlib import Path
import shlex
import subprocess

CODE = r'''
import json,os,subprocess,sys
from pathlib import Path
from datetime import datetime,timezone
store=Path('/var/backups/readyproof')
backup=json.loads((store/'ultimo_backup.json').read_text())
restore=json.loads((store/'ultima_restauracion.json').read_text())
assert backup['estado']=='respaldo_verificado_en_drive'
assert restore['estado']=='restauracion_verificada'
assert backup['schema']==restore['schema']=='010_firmantes'
assert backup['counts']==restore['counts']
assert backup['counts']['planillas']==25
files=json.load(sys.stdin)
allowed={'readyproof-backup.service','readyproof-backup-alerta.service','readyproof-backup.timer'}
assert set(files)==allowed
os.umask(0o077)
previous=store/('config-previa-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S'))
previous.mkdir(mode=0o700)
for name,content in files.items():
 p=Path('/etc/systemd/system')/name
 if p.exists():(previous/name).write_bytes(p.read_bytes())
 temporary=p.with_suffix(p.suffix+'.readyproof-nuevo')
 temporary.write_text(content,encoding='utf-8');os.chmod(temporary,0o644);os.replace(temporary,p)
try:
 subprocess.run(['systemd-analyze','verify',*[str(Path('/etc/systemd/system')/n) for n in sorted(files)]],check=True,capture_output=True,timeout=30)
 subprocess.run(['systemctl','daemon-reload'],check=True,capture_output=True,timeout=30)
 subprocess.run(['systemctl','enable','readyproof-backup.timer'],check=True,capture_output=True,timeout=30)
 subprocess.run(['systemctl','restart','readyproof-backup.timer'],check=True,capture_output=True,timeout=30)
 p=subprocess.run(['systemctl','is-active','readyproof-backup.timer'],check=True,capture_output=True,text=True,timeout=15)
 print(json.dumps({'estado':'timer_drive_activo','timer':p.stdout.strip(),'config_previa':str(previous),'aplicacion_reiniciada':False}))
except Exception:
 for name in files:
  p=Path('/etc/systemd/system')/name
  old=previous/name
  if old.exists():p.write_bytes(old.read_bytes())
  elif p.exists():p.unlink()
 subprocess.run(['systemctl','daemon-reload'],capture_output=True,timeout=30)
 subprocess.run(['systemctl','restart','readyproof-backup.timer'],capture_output=True,timeout=30)
 print(json.dumps({'estado':'no_activado_configuracion_anterior_restaurada'}));sys.exit(1)
'''


def main():
    folder=Path(__file__).resolve().parent/'servidor_backup'
    files={p.name:p.read_text(encoding='utf-8') for p in folder.glob('*.service')}
    files['readyproof-backup.timer']=(folder/'readyproof-backup.timer').read_text(encoding='utf-8')
    cmd=['ssh','-i',str(Path.home()/'.ssh/readyproof_deploy_67_205_170_29'),'-o','IdentitiesOnly=yes',
         '-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=15',
         'root@67.205.170.29','python3 -c '+shlex.quote(CODE)]
    p=subprocess.run(cmd,input=json.dumps(files).encode(),capture_output=True,timeout=180)
    try:status=json.loads(p.stdout)
    except Exception:
        print('No se pudo verificar la activación; consultar antes de repetir.');return 1
    print(json.dumps(status));return p.returncode


if __name__=='__main__':
    raise SystemExit(main())
