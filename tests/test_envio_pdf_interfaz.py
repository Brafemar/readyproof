"""Envío de PDF desde la pantalla, con Gmail simulado y PostgreSQL aislado."""
from concurrent.futures import ThreadPoolExecutor
from email import policy
from email.parser import BytesParser
from uuid import uuid4
import secrets
import time

import pytest
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import Carga, Envio, Intento, Retencion, Usuario
from app.correo import reintentar_envios
from tests.conftest import login_cliente
from tests.test_smtp_gmail import carga_emitida

DESTINO='tecnico@example.invalid'

@pytest.fixture
def gmail(app,monkeypatch,tmp_path):
    app.config.update(PLANILLAS_TRANSPORTE='gmail_api',PLANILLAS_DESTINATARIOS_PRUEBA=DESTINO,
                      MAIL_MODO_PRUEBA=True,DIRECTORIO_CORREO=str(tmp_path/'correos'))
    monkeypatch.setenv('MAIL_FROM','readyproof.ar@gmail.com')
    monkeypatch.setattr('app.gmail_https.obtener_token',lambda:'[Ejemplo] token simulado')
    messages=[]
    def enviar(mail,token):
        assert token=='[Ejemplo] token simulado'
        messages.append(mail)
        return 'ejemplo-gmail-id'
    monkeypatch.setattr('app.gmail_https.enviar_con_token',enviar)
    return messages


def solicitar(client,carga,key=None,**values):
    return client.post(f'/api/cargas/{carga}/enviar',json=dict(destinatario=DESTINO,inmediato=True,**values),
                       headers={'Idempotency-Key':key or str(uuid4())})


def test_envio_pdf_gmail_adjunta_copia_y_registra(app,client,carga_emitida,gmail):
    response=solicitar(client,carga_emitida)
    assert response.status_code==200,response.get_json()
    result=response.get_json();assert result['estado']=='enviado' and result['modo_prueba'] is False
    assert len(gmail)==1
    mail=gmail[0];assert mail['From']=='readyproof.ar@gmail.com' and mail['To']==DESTINO
    attachments=list(mail.iter_attachments());assert len(attachments)==1
    assert attachments[0].get_content_type()=='application/pdf'
    with Session(app.extensions['db_engine']) as db:
        envio=db.get(Envio,result['id']);carga=db.get(Carga,carga_emitida)
        assert attachments[0].get_payload(decode=True)==carga.pdf==envio.pdf_copia
        assert envio.enviado_en and envio.retener_hasta.year==carga.emitida_en.year+3
        attempt=db.scalar(select(Intento).where(Intento.envio_id==envio.id))
        assert attempt.resultado=='ok' and 'ejemplo-gmail-id' in attempt.respuesta
        assert 'token simulado' not in envio.mensaje_eml.decode()
    assert client.get(f'/api/cargas/{carga_emitida}/envios').get_json()[0]['estado']=='enviado'


def test_repeticion_y_recarga_no_duplican(app,client,carga_emitida,gmail):
    key=str(uuid4());first=solicitar(client,carga_emitida,key)
    assert first.status_code==200
    assert solicitar(client,carga_emitida,key).get_json()['id']==first.get_json()['id']
    assert solicitar(client,carga_emitida).get_json()['id']==first.get_json()['id']
    assert len(gmail)==1
    with Session(app.extensions['db_engine']) as db:
        assert db.scalar(select(func.count()).select_from(Envio))==1


def test_fallo_ambiguo_no_reenvia(app,client,carga_emitida,gmail,monkeypatch):
    def timeout(mail,token):gmail.append(mail);raise TimeoutError('[Ejemplo] respuesta sensible')
    monkeypatch.setattr('app.gmail_https.enviar_con_token',timeout)
    key=str(uuid4());response=solicitar(client,carga_emitida,key)
    assert response.status_code==502 and response.get_json()['estado']=='fallo'
    assert solicitar(client,carga_emitida,key).status_code==409
    assert solicitar(client,carga_emitida).status_code==409
    with app.app_context():assert reintentar_envios()==0
    assert len(gmail)==1
    with Session(app.extensions['db_engine']) as db:
        attempt=db.scalar(select(Intento));retry=db.scalar(select(Retencion))
        assert attempt.resultado=='timeout' and 'sensible' not in attempt.respuesta
        assert retry.proximos_intentos==0 and retry.reintentado_en is None


@pytest.mark.parametrize('case',['destino','csrf','uuid','tipo','deshabilitado','borrador'])
def test_rechaza_solicitud_invalida(app,client,carga_emitida,gmail,case):
    body=dict(destinatario=DESTINO,inmediato=True);headers={'Idempotency-Key':str(uuid4())}
    expected=422
    if case=='destino':body['destinatario']='otro@example.invalid';expected=403
    if case=='csrf':headers['X-CSRF-Token']='invalido';expected=403
    if case=='uuid':headers['Idempotency-Key']='no-es-uuid'
    if case=='tipo':body['inmediato']='true'
    if case=='deshabilitado':app.config['PLANILLAS_TRANSPORTE']='cola';expected=503
    if case=='borrador':
        with Session(app.extensions['db_engine']) as db:
            db.get(Carga,carga_emitida).estado='borrador';db.commit()
        expected=409
    response=client.post(f'/api/cargas/{carga_emitida}/enviar',json=body,headers=headers)
    assert response.status_code==expected,response.get_json()
    assert not gmail


def test_sin_sesion_y_sin_asignacion(app,client,carga_emitida,gmail):
    assert app.test_client().get(f'/api/cargas/{carga_emitida}/envios').status_code==401
    from app.auth import hash_clave
    password=secrets.token_urlsafe(24)
    with Session(app.extensions['db_engine']) as db:
        db.add(Usuario(login='ejemplo-sin-cliente',nombre='[Ejemplo] Técnico',rol='tecnico',clave_hash=hash_clave(password)));db.commit()
    other=login_cliente(app,'ejemplo-sin-cliente',password)
    assert solicitar(other,carga_emitida).status_code==404
    assert other.get(f'/api/cargas/{carga_emitida}/envios').status_code==404
    assert not gmail


def test_clicks_concurrentes_una_transmision(app,usuario_admin,carga_emitida,gmail,monkeypatch):
    def lento(mail,token):gmail.append(mail);time.sleep(.3);return 'ejemplo-concurrente'
    monkeypatch.setattr('app.gmail_https.enviar_con_token',lento)
    clients=[login_cliente(app,usuario_admin['login'],usuario_admin['clave']) for _ in range(2)]
    with ThreadPoolExecutor(max_workers=2) as pool:
        responses=list(pool.map(lambda client:solicitar(client,carga_emitida),clients))
    assert sorted(r.status_code for r in responses) in ([200,200],[200,409])
    assert any(r.get_json()['estado']=='enviado' for r in responses)
    assert len({r.get_json()['id'] for r in responses})==1 and len(gmail)==1
