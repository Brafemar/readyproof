"""Correo de documentación propio, sin contraseñas y con reserva durable."""
from datetime import timedelta
from email import policy
from email.parser import BytesParser
import os
from pathlib import Path
import secrets
import shutil
import smtplib
import subprocess
from threading import Thread
from uuid import uuid4

import pytest
from sqlalchemy import func,select
from sqlalchemy.orm import Session
from werkzeug.serving import make_server

from app.models import EnvioDocumentacion,Usuario


@pytest.fixture
def smtp_documentacion(app,monkeypatch,tmp_path):
    app.config.update(DOCUMENTACION_MODO_PRUEBA=False,DIRECTORIO_CORREO=str(tmp_path/'correo'))
    monkeypatch.setenv('SMTP_HOST','smtp.gmail.com');monkeypatch.setenv('SMTP_PORT','587')
    monkeypatch.setenv('SMTP_USER','readyproof.ar@gmail.com');monkeypatch.setenv('SMTP_PASSWORD',secrets.token_urlsafe(24))
    class SMTPFalso:
        mensajes=[]
        error=None
        quit_error=False
        def __init__(self,*args,**kwargs):pass
        def ehlo(self):pass
        def starttls(self,context):assert context.check_hostname
        def login(self,user,password):assert user=='readyproof.ar@gmail.com' and password
        def send_message(self,message,**kwargs):
            if self.error:raise self.error
            self.mensajes.append((message,kwargs));return {}
        def quit(self):
            if self.quit_error:raise OSError('detalle privado de red')
        def close(self):pass
    monkeypatch.setattr('smtplib.SMTP',SMTPFalso)
    return SMTPFalso


def guardar_email(client):
    response=client.put('/api/usuario/correo',json={'email':'tecnico@example.invalid'})
    assert response.status_code==200


def test_documentacion_requiere_sesion_csrf_y_correo(app,client):
    assert app.test_client().post('/api/usuario/enviar-documentacion').status_code==401
    assert client.post('/api/usuario/enviar-documentacion',headers={'X-CSRF-Token':'invalido'}).status_code==403
    assert client.post('/api/usuario/enviar-documentacion').status_code==422


@pytest.mark.parametrize('email',['no-es-correo','x@example.invalid\r\nBcc: otra@example.invalid','a@b',''])
def test_correo_propio_rechaza_valores_invalidos(client,email):
    assert client.put('/api/usuario/correo',json={'email':email}).status_code==422


def test_usuario_no_puede_elegir_otro_actor_o_destinatario(client):
    guardar_email(client)
    assert client.put('/api/usuario/correo',json={'email':'otra@example.invalid','usuario_id':str(uuid4())}).status_code==422
    assert client.post('/api/usuario/enviar-documentacion',json={'destinatario':'correo-invalido'}).status_code==422


def test_documentacion_smtp_incluye_guias_logo_usuario_pero_no_clave(app,client,usuario_admin,smtp_documentacion):
    guardar_email(client)
    key=str(uuid4())
    response=client.post('/api/usuario/enviar-documentacion',headers={'Idempotency-Key':key})
    assert response.status_code==200 and response.json['estado']=='enviado'
    mail,options=smtp_documentacion.mensajes[0]
    assert str(mail['From'])=='readyproof.ar@gmail.com' and str(mail['To'])=='tecnico@example.invalid'
    assert options['to_addrs']==['tecnico@example.invalid']
    assert len(list(mail.iter_attachments()))==2
    assert {part.get_filename() for part in mail.iter_attachments()}=={'readyproof-guia-de-uso.md','readyproof-acceso-tecnico.md'}
    assert any(part.get_content_type()=='image/png' for part in mail.walk())
    assert usuario_admin['login'] in mail.get_body(preferencelist=('plain',)).get_content()
    assert usuario_admin['clave'].encode() not in mail.as_bytes()
    assert os.environ['SMTP_PASSWORD'].encode() not in mail.as_bytes()
    again=client.post('/api/usuario/enviar-documentacion',headers={'Idempotency-Key':key})
    assert again.json==response.json and len(smtp_documentacion.mensajes)==1
    assert client.post('/api/usuario/enviar-documentacion').status_code==429
    with Session(app.extensions['db_engine']) as db:
        row=db.get(EnvioDocumentacion,key)
        assert row.estado=='enviado' and row.usuario_id==usuario_admin['id'] and row.enviado_en
        assert db.get(Usuario,usuario_admin['id']).email=='tecnico@example.invalid'


def test_archivo_no_declara_envio_smtp(app,client,tmp_path):
    app.config.update(DOCUMENTACION_MODO_PRUEBA=True,DIRECTORIO_CORREO=str(tmp_path/'correo'))
    guardar_email(client)
    response=client.post('/api/usuario/enviar-documentacion')
    assert response.status_code==200 and response.json['estado']=='archivado'
    files=list((tmp_path/'correo').glob('documentacion-*.eml'))
    assert len(files)==1
    assert BytesParser(policy=policy.default).parsebytes(files[0].read_bytes())['To']=='tecnico@example.invalid'


@pytest.mark.parametrize('error,estado',[(smtplib.SMTPAuthenticationError(535,b'detalle privado'),'fallo'),(TimeoutError('detalle privado'),'indeterminado')])
def test_fallo_no_filtra_detalles_ni_reintenta(app,client,smtp_documentacion,error,estado):
    guardar_email(client);smtp_documentacion.error=error;key=str(uuid4())
    response=client.post('/api/usuario/enviar-documentacion',headers={'Idempotency-Key':key})
    assert response.status_code==502 and response.json['estado']==estado
    assert 'detalle privado' not in response.get_data(as_text=True)
    assert client.post('/api/usuario/enviar-documentacion',headers={'Idempotency-Key':key}).status_code==409
    assert not smtp_documentacion.mensajes


def test_corte_quit_no_convierte_aceptacion_en_fallo(client,smtp_documentacion):
    guardar_email(client);smtp_documentacion.quit_error=True
    assert client.post('/api/usuario/enviar-documentacion').json['estado']=='enviado'
    assert len(smtp_documentacion.mensajes)==1


@pytest.mark.parametrize('timeout',[False,True])
def test_ruta_gmail_https_sin_contactar_smtp(app,client,smtp_documentacion,monkeypatch,timeout):
    guardar_email(client);app.config['DOCUMENTACION_TRANSPORTE']='gmail_api'
    monkeypatch.setattr('app.gmail_https.obtener_token',lambda:'[Ejemplo] token')
    def send_fake(mail,token):
        assert str(mail['To'])=='tecnico@example.invalid' and token=='[Ejemplo] token'
        if timeout:raise OSError('detalle privado')
        return 'mensaje-ficticio'
    monkeypatch.setattr('app.gmail_https.enviar_con_token',send_fake)
    response=client.post('/api/usuario/enviar-documentacion')
    assert response.status_code==(502 if timeout else 200)
    assert response.json['estado']==('indeterminado' if timeout else 'enviado')
    assert not smtp_documentacion.mensajes


def test_solicitud_de_otro_usuario_no_se_filtra(app,client,usuario_admin):
    guardar_email(client)
    with Session(app.extensions['db_engine']) as db:
        row=EnvioDocumentacion(id=str(uuid4()),usuario_id=usuario_admin['id'],destinatario='tecnico@example.invalid',
                              estado='preparado',message_id='<prueba@example.invalid>',mensaje_eml=b'copia ficticia')
        db.add(row);db.commit();key=row.id
    other=client.post('/api/admin/usuarios',json={'login':'otro-tecnico','nombre':'[Ejemplo] Otro técnico','rol':'tecnico','clave':secrets.token_urlsafe(24),'cliente_ids':[]})
    assert other.status_code==201
    with Session(app.extensions['db_engine']) as db:
        db.get(EnvioDocumentacion,key).usuario_id=other.json['id'];db.commit()
    assert client.post('/api/usuario/enviar-documentacion',headers={'Idempotency-Key':key}).status_code==404


def test_boton_documentacion_en_navegador_movil(app,usuario_admin,tmp_path):
    app.config.update(DOCUMENTACION_MODO_PRUEBA=True,DIRECTORIO_CORREO=str(tmp_path/'correo'))
    node=os.environ.get('READYPROOF_NODE') or shutil.which('node');assert node
    server=make_server('127.0.0.1',0,app,threaded=True)
    thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    out=Path('out/documentacion_navegador').resolve();out.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,RP_URL=f'http://127.0.0.1:{server.server_port}',RP_OUT=str(out),RP_LOGIN=usuario_admin['login'],RP_PASSWORD=usuario_admin['clave'])
    try:
        result=subprocess.run([node,'tests/browser/documentacion.cjs'],env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=90)
        assert result.returncode==0,result.stdout+result.stderr
        with Session(app.extensions['db_engine']) as db:
            assert db.scalar(select(func.count()).select_from(EnvioDocumentacion))==1
    finally:
        server.shutdown();thread.join(timeout=10)
