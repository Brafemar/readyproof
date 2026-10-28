"""Transporte Gmail HTTPS con OAuth y remitente verificado, sin registrar tokens."""
import base64
import json
import os
import ssl
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request,urlopen

REMITENTE='readyproof.ar@gmail.com'


def obtener_token():
    values={key:os.getenv('GMAIL_'+key.upper(),'') for key in ('client_id','client_secret','refresh_token')}
    if not all(values.values()):raise ValueError('Configurar autorización de Gmail HTTPS.')
    values['grant_type']='refresh_token'
    request=Request('https://oauth2.googleapis.com/token',data=urlencode(values).encode(),headers={'Content-Type':'application/x-www-form-urlencoded'})
    try:
        with urlopen(request,timeout=15,context=ssl.create_default_context()) as response:
            token=json.loads(response.read())['access_token']
        request=Request('https://openidconnect.googleapis.com/v1/userinfo',headers={'Authorization':'Bearer '+token})
        with urlopen(request,timeout=15,context=ssl.create_default_context()) as response:
            profile=json.loads(response.read())
        if profile.get('email')!=REMITENTE or profile.get('email_verified') is not True:
            raise ValueError('La cuenta autorizada no coincide con readyproof.')
        return token
    except (OSError,KeyError,ValueError,TypeError):
        raise ValueError('No se pudo renovar o verificar la autorización de Gmail HTTPS.') from None


def enviar_con_token(mail,token):
    payload=json.dumps({'raw':base64.urlsafe_b64encode(mail.as_bytes()).decode('ascii')}).encode()
    request=Request('https://gmail.googleapis.com/gmail/v1/users/me/messages/send',data=payload,
                    headers={'Content-Type':'application/json','Authorization':'Bearer '+token})
    try:
        with urlopen(request,timeout=20,context=ssl.create_default_context()) as response:
            data=json.loads(response.read())
        if not data.get('id'):raise OSError('Gmail no confirmó un identificador de mensaje.')
        return data['id']
    except HTTPError as error:
        if 400<=error.code<500:raise ValueError('Gmail rechazó la solicitud.') from None
        raise OSError('Aceptación Gmail desconocida.') from None
    except (ValueError,KeyError,TypeError):
        raise OSError('No se pudo confirmar la respuesta de Gmail.') from None
