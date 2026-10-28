"""Autoriza Gmail en el navegador local y entrega el permiso por SSH, sin imprimir tokens."""
import argparse
import base64
from hashlib import sha256
from http.server import BaseHTTPRequestHandler,HTTPServer
import json
from pathlib import Path
import secrets
import ssl
import subprocess
import sys
import time
from urllib.parse import parse_qs,urlencode,urlsplit
from urllib.request import Request,urlopen
import webbrowser

SENDER='readyproof.ar@gmail.com'


def main():
    parser=argparse.ArgumentParser(description='Autoriza únicamente el envío Gmail de readyproof; no pide contraseñas en consola.')
    parser.add_argument('--cliente-oauth',type=Path,required=True,help='JSON privado de un cliente Google de tipo Aplicación de escritorio.')
    args=parser.parse_args()
    try:
        client=json.loads(args.cliente_oauth.read_text(encoding='utf-8-sig')).get('installed',{})
        if not client.get('client_id') or not client.get('client_secret'):
            raise ValueError('Se requiere un JSON de cliente OAuth de escritorio válido.')
        state=secrets.token_urlsafe(32);verifier=secrets.token_urlsafe(64)
        challenge=base64.urlsafe_b64encode(sha256(verifier.encode()).digest()).decode().rstrip('=')
        received={}
        class Callback(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def do_GET(self):
                parsed=urlsplit(self.path);query=parse_qs(parsed.query)
                valid=parsed.path=='/' and secrets.compare_digest(query.get('state',[''])[0].encode(),state.encode())
                self.send_response(200 if valid else 400)
                self.send_header('Content-Type','text/plain; charset=utf-8');self.send_header('Cache-Control','no-store');self.end_headers()
                if valid:
                    received['code']=query.get('code',[''])[0]
                    received['error']=bool(query.get('error'))
                    self.wfile.write('Autorización recibida. Volvé a tu consola de readyproof.'.encode())
                else:self.wfile.write(b'Solicitud no valida.')
        with HTTPServer(('127.0.0.1',0),Callback) as server:
            server.timeout=1
            redirect=f'http://127.0.0.1:{server.server_port}/'
            query={'client_id':client['client_id'],'redirect_uri':redirect,'response_type':'code',
                   'scope':'openid email https://www.googleapis.com/auth/gmail.send',
                   'access_type':'offline','prompt':'consent select_account','login_hint':SENDER,
                   'state':state,'code_challenge':challenge,'code_challenge_method':'S256'}
            print('Se abrirá Google. Elegí readyproof.ar@gmail.com y revisá el permiso de envío. La contraseña solo se escribe en Google.')
            if not webbrowser.open('https://accounts.google.com/o/oauth2/v2/auth?'+urlencode(query)):
                raise ValueError('No se pudo abrir el navegador. No se modificó el servidor.')
            deadline=time.monotonic()+600
            while not received and time.monotonic()<deadline:server.handle_request()
        if received.get('error') or not received.get('code'):
            raise ValueError('La autorización no se completó. No se modificó el servidor.')
        data={'client_id':client['client_id'],'client_secret':client['client_secret'],'code':received['code'],
              'code_verifier':verifier,'grant_type':'authorization_code','redirect_uri':redirect}
        request=Request('https://oauth2.googleapis.com/token',data=urlencode(data).encode(),headers={'Content-Type':'application/x-www-form-urlencoded'})
        with urlopen(request,timeout=20,context=ssl.create_default_context()) as response:tokens=json.loads(response.read())
        request=Request('https://openidconnect.googleapis.com/v1/userinfo',headers={'Authorization':'Bearer '+tokens['access_token']})
        with urlopen(request,timeout=15,context=ssl.create_default_context()) as response:profile=json.loads(response.read())
        if profile.get('email')!=SENDER or profile.get('email_verified') is not True or not tokens.get('refresh_token'):
            raise ValueError('Se requiere autorización renovable de readyproof.ar@gmail.com. No se modificó el servidor.')
        payload={'GMAIL_CLIENT_ID':client['client_id'],'GMAIL_CLIENT_SECRET':client['client_secret'],
                 'GMAIL_REFRESH_TOKEN':tokens['refresh_token'],'DOCUMENTACION_TRANSPORTE':'gmail_api','DOCUMENTACION_MODO_PRUEBA':'false'}
        key=Path.home()/'.ssh/readyproof_deploy_67_205_170_29'
        if not key.is_file():raise ValueError('Esta configuración la ejecuta Jorge desde su PC administradora.')
        command=['ssh','-i',str(key),'-o','IdentitiesOnly=yes','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes',
                 '-o','ConnectTimeout=15','root@67.205.170.29','python3 /root/readyproof-configurar-gmail-https.py']
        result=subprocess.run(command,input=json.dumps(payload).encode(),capture_output=True,timeout=90)
        if result.returncode:raise ValueError('No se pudo confirmar la configuración remota; consultar antes de repetir.')
        payload=tokens=data=received=None
        print('Gmail HTTPS configurado. No se mostraron ni guardaron tokens en esta consola.')
        print('No se envió ningún correo automáticamente. En Mi cuenta, guardar el destinatario y pulsar Enviar documentación por correo.')
        return 0
    except ValueError as error:
        print(str(error),file=sys.stderr);return 1
    except Exception:
        print('No se pudo completar la autorización. No compartas el JSON, códigos o tokens; revisá el procedimiento privado.',file=sys.stderr)
        return 1


if __name__=='__main__':raise SystemExit(main())
