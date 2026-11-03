"""Edición local de clientes, CUIT y permisos; sin sincronización externa."""
from copy import deepcopy
from hashlib import sha256
import pytest
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models import Cliente, Carga, RegistroAcceso, ahora
from tests.conftest import login_cliente
from tests.test_auth import tecnico
from tests.test_smtp_gmail import carga_emitida


def datos(nombre='[Ejemplo] Cliente de campo', cuit='20-00000000-1'):
    return dict(nombre=nombre, cuit=cuit, contacto=dict(direccion='[Ejemplo] Calle de prueba 123', telefono='0000-0000000', email='contacto@example.invalid'))


def test_alta_y_lectura_cliente_con_contacto(client):
    response=client.post('/api/admin/clientes',json=datos())
    assert response.status_code==201, response.get_json()
    row=response.get_json()
    assert row['cuit']=='20000000001' and row['contacto']==datos()['contacto']
    assert client.get('/api/admin/clientes/'+row['id']).get_json()==row
    assert row in client.get('/api/admin/clientes').get_json()


def test_editar_cliente_preserva_vinculo_y_audita(app,client):
    row=client.post('/api/admin/clientes',json=datos()).get_json()
    with Session(app.extensions['db_engine']) as db:
        c=db.get(Cliente,row['id']);c.contabilium_id='999999';c.sincronizado_en=ahora()
        c.contacto={**c.contacto,'referencia_interna':'[Ejemplo] conservar'}
        db.commit();original_fecha=c.sincronizado_en
    changed=datos('[Ejemplo] Cliente actualizado','30-00000000-7')
    changed['contacto']['direccion']='[Ejemplo] Nuevo domicilio 456'
    response=client.put('/api/admin/clientes/'+row['id'],json=changed)
    assert response.status_code==200,response.get_json()
    assert response.get_json()['cuit']=='30000000007'
    assert response.get_json()['nombre']==changed['nombre']
    assert response.get_json()['contacto']['direccion']==changed['contacto']['direccion']
    with Session(app.extensions['db_engine']) as db:
        c=db.get(Cliente,row['id'])
        assert c.contabilium_id=='999999' and c.sincronizado_en==original_fecha
        assert c.contacto['referencia_interna']=='[Ejemplo] conservar'
        assert db.scalar(select(RegistroAcceso).where(RegistroAcceso.evento=='cliente_editado',RegistroAcceso.cliente_id==c.id)) is not None


def test_cuit_duplicado_en_alta_y_edicion_rechazado(app,client,catalogo):
    assert client.post('/api/admin/clientes',json=datos()).status_code==201
    assert client.post('/api/admin/clientes',json=datos('[Ejemplo] Duplicado')).status_code==409
    other=catalogo[0]
    response=client.put('/api/admin/clientes/'+other['id'],json=datos('[Ejemplo] Otro'))
    assert response.status_code==409 and 'CUIT' in response.get_json()['error']
    with Session(app.extensions['db_engine']) as db:
        assert db.scalar(select(func.count()).select_from(Cliente).where(Cliente.cuit=='20000000001'))==1
        assert db.get(Cliente,other['id']).nombre==other['nombre']


def test_tecnico_no_puede_administrar_clientes(app,client,catalogo):
    user,password=tecnico(client,catalogo)
    tech=login_cliente(app,user['login'],password)
    key=catalogo[0]['id']
    assert tech.get('/api/admin/clientes').status_code==403
    assert tech.get('/api/admin/clientes/'+key).status_code==403
    assert tech.put('/api/admin/clientes/'+key,json=datos()).status_code==403
    assert tech.post('/api/admin/clientes',json=datos()).status_code==403


def test_sesion_y_csrf_obligatorios(app,client,catalogo):
    anonymous=app.test_client();key=catalogo[0]['id']
    assert anonymous.get('/api/admin/clientes').status_code==401
    assert anonymous.put('/api/admin/clientes/'+key,json=datos()).status_code==401
    assert client.put('/api/admin/clientes/'+key,json=datos(),headers={'X-CSRF-Token':'invalido'}).status_code==403


@pytest.mark.parametrize('cuit',['20000000000','abc'])
def test_cuit_invalido_rechazado(client,cuit):
    assert client.post('/api/admin/clientes',json=datos(cuit=cuit)).status_code==422


@pytest.mark.parametrize('contacto',[{'email':'no-es-correo'},{'telefono':123},{'campo_ajeno':'[Ejemplo] valor'}])
def test_contacto_invalido_rechazado(client,contacto):
    body=datos();body['contacto']=contacto
    assert client.post('/api/admin/clientes',json=body).status_code==422


def test_edicion_no_modifica_pdf_ni_datos_emitidos(app,client,carga_emitida,catalogo):
    with Session(app.extensions['db_engine']) as db:
        c=db.get(Carga,carga_emitida);old_pdf=bytes(c.pdf);old_datos=deepcopy(c.datos);old_hash=c.pdf_sha256
    response=client.put('/api/admin/clientes/'+catalogo[0]['id'],json=datos('[Ejemplo] Nombre nuevo'))
    assert response.status_code==200,response.get_json()
    with Session(app.extensions['db_engine']) as db:
        c=db.get(Carga,carga_emitida)
        assert c.pdf==old_pdf and c.datos==old_datos
        assert c.pdf_sha256==old_hash==sha256(old_pdf).hexdigest()


def test_modo_real_acepta_nombre_sin_prefijo(app,client):
    # Es una identidad ficticia, sin el prefijo reservado al piloto.
    app.config.update(MODO_PILOTO=False,EMPRESA_MANTENEDORA='Mantenedora ficticia',CERTIFICADO_N='PRUEBA-00001')
    response=client.post('/api/admin/clientes',json=datos('Cliente ficticio de prueba'))
    assert response.status_code==201,response.get_json()
    key=response.get_json()['id']
    assert response.get_json()['es_ejemplo'] is False
    assert client.put('/api/admin/clientes/'+key,json=datos('Cliente ficticio actualizado')).status_code==200
