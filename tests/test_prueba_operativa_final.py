"""Flujo del script sobre API y PostgreSQL temporales; correo siempre sustituido."""
import json
import secrets
from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Carga,Envio,Intento
from scripts.prueba_operativa_final import ErrorPrueba,confirmar_recepcion,ejecutar,iniciar_sesion,procesar_envio


class APIPrueba:
    def __init__(self,app):
        self.client=app.test_client();self.csrf=None

    def request(self,method,path,datos=None,*,binario=False,cabeceras=None):
        headers=dict(cabeceras or {})
        if self.csrf:headers['X-CSRF-Token']=self.csrf
        response=self.client.open(path,method=method,json=datos,headers=headers)
        if response.status_code>=400:raise ErrorPrueba(f'HTTP {response.status_code}')
        return response.data if binario else response.get_json()


@pytest.mark.parametrize('smtp',[False,True])
def test_flujo_archivo_o_smtp_sustituido_sin_procesar_otra_cola(app,usuario_admin,tmp_path,monkeypatch,smtp):
    app.config['DIRECTORIO_CORREO']=str(tmp_path/'eml')
    monkeypatch.setenv('MAIL_FROM','readyproof@example.invalid')
    monkeypatch.setenv('SMTP_HOST','smtp.gmail.com')
    monkeypatch.setenv('SMTP_PORT','587')
    monkeypatch.setenv('SMTP_USER','readyproof@example.invalid')
    monkeypatch.setenv('SMTP_PASSWORD',secrets.token_urlsafe(24))
    messages=[]
    class SMTPFalso:
        def __init__(self,*args,**kwargs):pass
        def ehlo(self):pass
        def starttls(self,context):assert context.check_hostname
        def login(self,*args):pass
        def send_message(self,message,**kwargs):messages.append(message);return {}
        def quit(self):pass
    monkeypatch.setattr('smtplib.SMTP',SMTPFalso)
    api=APIPrueba(app)
    iniciar_sesion(api,usuario_admin['login'],usuario_admin['clave'])
    other=[]
    def processor(key):
        with Session(app.extensions['db_engine']) as db:
            carga_id=db.get(Envio,key).carga_id
        queued=api.request('POST',f'/api/cargas/{carga_id}/enviar',{'destinatario':'otra@example.invalid'})
        other.append(queued['id'])
        return procesar_envio(app,key,smtp=smtp)
    target=tmp_path/'operativa'
    report=ejecutar(api,target,usuario=usuario_admin['login'],destinatario='prueba@example.invalid',procesador=processor)
    assert report['verificacion_pdf']['logo'] and report['verificacion_pdf']['leyenda_iram']
    assert Path(report['pdf']).read_bytes().startswith(b'%PDF-')
    assert not report['flujo_completo'] and not report['recepcion_confirmada']
    assert report['correo']['modo_prueba'] is not smtp
    assert report['correo']['estado']==('enviado' if smtp else 'pendiente')
    assert len(messages)==int(smtp)
    with Session(app.extensions['db_engine']) as db:
        assert db.get(Carga,report['carga_id']).estado=='emitida'
        assert db.get(Envio,other[0]).estado=='pendiente'
        assert not list(db.scalars(select(Intento).where(Intento.envio_id==other[0])))
        assert len(list(db.scalars(select(Intento).where(Intento.envio_id==report['envio_id']))))==1
    saved=(target/'resultado.json').read_text(encoding='utf-8')
    assert usuario_admin['clave'] not in saved and 'csrf_token' not in saved
    with pytest.raises(ErrorPrueba,match='Ya existe evidencia'):
        ejecutar(api,target,usuario=usuario_admin['login'],destinatario='prueba@example.invalid',procesador=processor)
    assert len(other)==1


def test_no_declara_recepcion_de_modo_archivo(tmp_path):
    report={'correo':{'modo_prueba':True,'estado':'pendiente'},'flujo_completo':False}
    with pytest.raises(ErrorPrueba,match='SMTP real'):
        confirmar_recepcion(report,tmp_path/'resultado.json','RECIBIDO_Y_REVISADO')
    assert not report['flujo_completo'] and not (tmp_path/'resultado.json').exists()


def test_recepcion_real_requiere_confirmacion_manual_exacta(tmp_path):
    report={'correo':{'modo_prueba':False,'estado':'enviado'},'flujo_completo':False}
    path=tmp_path/'resultado.json'
    confirmar_recepcion(report,path,'')
    assert not report['flujo_completo'] and not path.exists()
    confirmar_recepcion(report,path,'RECIBIDO_Y_REVISADO')
    assert json.loads(path.read_text())['recepcion_confirmada']
    assert 'manual' in report['fuente_confirmacion']


def test_login_rechazado_no_crea_cargas(app,usuario_admin):
    api=APIPrueba(app)
    with pytest.raises(ErrorPrueba,match='401'):
        iniciar_sesion(api,usuario_admin['login'],secrets.token_urlsafe(24))
    with Session(app.extensions['db_engine']) as db:
        assert not list(db.scalars(select(Carga)))
