"""Gmail HTTPS con respuestas simuladas; no se usan tokens ni mensajes reales."""
import base64
from email.message import EmailMessage
from io import BytesIO
import json
from urllib.error import HTTPError

import pytest

from app.gmail_https import obtener_token,enviar_con_token


class Response(BytesIO):
    def __enter__(self):return self
    def __exit__(self,*args):self.close()


def test_token_y_remitente_verificado(monkeypatch):
    for name in ('CLIENT_ID','CLIENT_SECRET','REFRESH_TOKEN'):monkeypatch.setenv('GMAIL_'+name,'[Ejemplo] '+name)
    calls=[]
    def open_fake(request,**kwargs):
        calls.append(request);assert kwargs['context'].check_hostname
        if request.full_url.endswith('/token'):return Response(json.dumps({'access_token':'[Ejemplo] access'}).encode())
        return Response(json.dumps({'email':'readyproof.ar@gmail.com','email_verified':True}).encode())
    monkeypatch.setattr('app.gmail_https.urlopen',open_fake)
    assert obtener_token()=='[Ejemplo] access'
    assert len(calls)==2 and calls[1].get_header('Authorization')=='Bearer [Ejemplo] access'


def test_cuenta_google_distinta_se_rechaza_sin_filtrar_token(monkeypatch):
    for name in ('CLIENT_ID','CLIENT_SECRET','REFRESH_TOKEN'):monkeypatch.setenv('GMAIL_'+name,'[Ejemplo] privado')
    def open_fake(request,**kwargs):
        return Response(json.dumps({'access_token':'[Ejemplo] secreto'} if request.full_url.endswith('/token') else {'email':'otra@example.invalid','email_verified':True}).encode())
    monkeypatch.setattr('app.gmail_https.urlopen',open_fake)
    with pytest.raises(ValueError) as error:obtener_token()
    assert 'secreto' not in str(error.value) and 'otra@example.invalid' not in str(error.value)


def test_envio_mime_por_https(monkeypatch):
    mail=EmailMessage();mail['From']='readyproof.ar@gmail.com';mail['To']='tecnico@example.invalid';mail.set_content('[Ejemplo] Guía')
    def open_fake(request,**kwargs):
        assert request.full_url=='https://gmail.googleapis.com/gmail/v1/users/me/messages/send'
        raw=base64.urlsafe_b64decode(json.loads(request.data)['raw'])
        assert b'tecnico@example.invalid' in raw and b'token-ficticio' not in raw
        assert request.get_header('Authorization')=='Bearer token-ficticio'
        return Response(b'{"id":"mensaje-ficticio"}')
    monkeypatch.setattr('app.gmail_https.urlopen',open_fake)
    assert enviar_con_token(mail,'token-ficticio')=='mensaje-ficticio'


def test_respuesta_5xx_se_considera_indeterminada(monkeypatch):
    def open_fake(request,**kwargs):raise HTTPError(request.full_url,503,'detalle privado',{},None)
    monkeypatch.setattr('app.gmail_https.urlopen',open_fake)
    with pytest.raises(OSError,match='desconocida'):enviar_con_token(EmailMessage(),'token-ficticio')
