"""Control local del ensayo y la instalación privada de etapa 6."""
from hashlib import sha256
import json
from pathlib import Path
import sys

from revision_etapa5 import ssh
from servidor_etapa6 import FILES

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'out/etapa6_final'
REMOTE='/home/readyproof_revision_etapa5/scripts/servidor_etapa6.py'


def execute(action):
    script=ROOT/'scripts/servidor_etapa6.py';digest=sha256(script.read_bytes()).hexdigest()
    upload="from pathlib import Path;import sys,os,grp;p=Path("+repr(REMOTE)+");assert p.resolve()==p and not p.is_symlink();p.write_bytes(sys.stdin.buffer.read());os.chown(p,0,grp.getgrnam('readyproof').gr_gid);os.chmod(p,0o640)"
    ssh(upload,payload=script.read_bytes(),timeout=60)
    data={'accion':action,'fuentes':{name:sha256((ROOT/name).read_bytes()).hexdigest() for name in FILES}}
    if action=='aplicar':
        data.update(pruebas=json.loads((OUT/'pruebas_cobertura.json').read_text()),anteriores=json.loads((OUT/'inspeccionar.json').read_text())['fuentes'])
    code="import runpy,hashlib;from pathlib import Path;p=Path("+repr(REMOTE)+");assert hashlib.sha256(p.read_bytes()).hexdigest()=="+repr(digest)+";runpy.run_path(str(p),run_name='__main__')"
    result=json.loads(ssh(code,payload=json.dumps(data).encode(),timeout=2400))
    (OUT/(action+'.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k in ('estado','schema','counts','base_aislada','modo_piloto','mail_modo_prueba','datos_historicos_modificados')}))


if __name__=='__main__':
    assert sys.argv[1] in ('inspeccionar','ensayar','aplicar','verificar')
    execute(sys.argv[1])
