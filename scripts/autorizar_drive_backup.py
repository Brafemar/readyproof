"""Autoriza Drive para respaldos; no imprime códigos ni tokens."""
import argparse
import base64
import configparser
from hashlib import sha256
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import secrets
import subprocess
import sys
import time
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import Request, urlopen
import webbrowser

REMOTE = r'''
import configparser,json,os,subprocess,sys,tempfile
from pathlib import Path
data=json.load(sys.stdin)
directory=Path('/etc/readyproof')
directory.mkdir(mode=0o700,exist_ok=True)
target=directory/'rclone-backup.conf'
if target.exists():
 print(json.dumps({'estado':'configuracion_existente_no_modificada'}));sys.exit(2)
config=configparser.ConfigParser(interpolation=None)
config['readyproof-drive']={'type':'drive','scope':'drive.file','client_id':data['client_id'],
 'client_secret':data['client_secret'],'token':json.dumps(data['token'])}
fd,name=tempfile.mkstemp(prefix='.rclone-',dir=directory)
try:
 os.fchmod(fd,0o600)
 with os.fdopen(fd,'w') as stream:config.write(stream)
 p=subprocess.run(['rclone','--config',name,'lsf','readyproof-drive:', '--max-depth','1'],capture_output=True,timeout=60)
 if p.returncode:
  text=p.stderr.decode(errors='replace').lower()
  reason='habilitar_drive_api' if any(x in text for x in ('accessnotconfigured','has not been used','service_disabled','is disabled')) else 'autorizacion_no_verificada'
  print(json.dumps({'estado':reason}));sys.exit(3)
 os.replace(name,target)
 print(json.dumps({'estado':'drive_autorizado','cuenta':'readyproof.ar@gmail.com','config':'/etc/readyproof/rclone-backup.conf'}))
finally:
 if os.path.exists(name):os.unlink(name)
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cliente-oauth', type=Path, required=True)
    args = parser.parse_args()
    client = json.loads(args.cliente_oauth.read_text(encoding='utf-8-sig')).get('installed', {})
    if not client.get('client_id') or not client.get('client_secret'):
        raise ValueError('Se necesita el cliente OAuth de escritorio de readyproof.')
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(sha256(verifier.encode()).digest()).decode().rstrip('=')
    received = {}

    class Callback(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            parsed = urlsplit(self.path)
            if parsed.path == '/iniciar':
                self.send_response(302)
                self.send_header('Location', authorization_url)
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                return
            query = parse_qs(parsed.query)
            valid = parsed.path == '/' and secrets.compare_digest(query.get('state', [''])[0], state)
            self.send_response(200 if valid else 400)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            if valid:
                received.update(code=query.get('code', [''])[0], error=bool(query.get('error')))
                self.wfile.write('Autorización de Drive recibida. Volvé al chat de readyproof.'.encode())
            else:
                self.wfile.write(b'Solicitud no valida.')

    with HTTPServer(('127.0.0.1', 0), Callback) as server:
        server.timeout = 1
        redirect = f'http://127.0.0.1:{server.server_port}/'
        query = dict(client_id=client['client_id'], redirect_uri=redirect, response_type='code',
                     scope='openid email https://www.googleapis.com/auth/drive.file',
                     access_type='offline', prompt='consent select_account', login_hint='readyproof.ar@gmail.com',
                     state=state, code_challenge=challenge, code_challenge_method='S256')
        authorization_url = 'https://accounts.google.com/o/oauth2/v2/auth?' + urlencode(query)
        local_url = f'http://127.0.0.1:{server.server_port}/iniciar'
        status_path = Path(__file__).resolve().parents[1]/'out/drive_backup_oauth_estado.json'
        status_path.parent.mkdir(exist_ok=True)
        status_path.write_text(json.dumps({'url_local': local_url, 'estado': 'esperando_consentimiento'}), encoding='utf-8')
        print('Abrir autorización de Drive: '+local_url, flush=True)
        print('Elegí readyproof.ar@gmail.com. No compartas códigos.', flush=True)
        webbrowser.open(local_url)
        deadline = time.monotonic() + 900
        while not received and time.monotonic() < deadline:
            server.handle_request()
    if received.get('error') or not received.get('code'):
        raise ValueError('La autorización de Drive no se completó. Gmail no se modificó.')
    payload = dict(client_id=client['client_id'], client_secret=client['client_secret'],
                   code=received['code'], code_verifier=verifier, grant_type='authorization_code', redirect_uri=redirect)
    request = Request('https://oauth2.googleapis.com/token', data=urlencode(payload).encode())
    with urlopen(request, timeout=30) as response:
        token = json.load(response)
    request = Request('https://openidconnect.googleapis.com/v1/userinfo', headers={'Authorization': 'Bearer ' + token['access_token']})
    with urlopen(request, timeout=30) as response:
        profile = json.load(response)
    if profile.get('email') != 'readyproof.ar@gmail.com' or profile.get('email_verified') is not True or not token.get('refresh_token'):
        raise ValueError('Se requiere autorización renovable de readyproof.ar@gmail.com.')
    if 'https://www.googleapis.com/auth/drive.file' not in token.get('scope', '').split():
        raise ValueError('No se concedió el permiso de archivos de Drive.')
    from datetime import datetime, timedelta, timezone
    token['expiry'] = (datetime.now(timezone.utc) + timedelta(seconds=token.pop('expires_in', 3600))).isoformat()
    token.pop('id_token', None)
    data = dict(client_id=client['client_id'], client_secret=client['client_secret'], token=token)
    import shlex
    command = ['ssh', '-i', str(Path.home()/'.ssh/readyproof_deploy_67_205_170_29'),
               '-o', 'IdentitiesOnly=yes', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes',
               '-o', 'ConnectTimeout=15', 'root@67.205.170.29', 'python3 -c ' + shlex.quote(REMOTE)]
    result = subprocess.run(command, input=json.dumps(data).encode(), capture_output=True, timeout=100)
    try:
        status = json.loads(result.stdout)
    except Exception:
        raise ValueError('No se pudo verificar Drive en el servidor; no repetir sin revisar.') from None
    print(json.dumps(status, ensure_ascii=True), flush=True)
    status_path.write_text(json.dumps(status), encoding='utf-8')
    return result.returncode


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception:
        print('No se completó la autorización de Drive. No compartas archivos, códigos ni tokens.', file=sys.stderr)
        raise SystemExit(1)
