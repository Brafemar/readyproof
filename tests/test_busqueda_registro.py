"""Búsqueda autenticada y aislada por cliente."""
from uuid import uuid4
from tests.test_api import crear
from tests.test_desbloqueo_revision import emitir, pdf_simulado
from tests.test_auth import tecnico
from tests.conftest import login_cliente
from app.models import UsuarioCliente
from sqlalchemy.orm import Session


def test_buscar_carga_valida(app,client,catalogo,datos_api,pdf_simulado):
    emitted=emitir(client,crear(client,catalogo,datos_api).get_json())
    response=client.get('/api/carga/buscar',query_string={'numero':str(emitted['numero_registro'])})
    assert response.status_code==200
    result=response.get_json()
    assert result['cliente']==catalogo[0]['nombre'] and result['sistema']==catalogo[1]['tipo']
    assert result['planilla']==catalogo[2]['codigo'] and result['estado']=='emitida'
    assert result['revision_publica']==0 and result['fecha_emision'] and result['pdf_hash']
    user,password=tecnico(client,catalogo);tech=login_cliente(app,user['login'],password)
    assert tech.get('/api/carga/buscar?numero=1').status_code==200
    with Session(app.extensions['db_engine']) as db:
        db.delete(db.get(UsuarioCliente,(user['id'],catalogo[0]['id'])));db.commit()
    hidden=tech.get('/api/carga/buscar?numero=1')
    assert hidden.status_code==404 and 'cliente' not in hidden.get_json()


def test_buscar_carga_no_existe(client):
    assert client.get('/api/carga/buscar?numero=2147483647').status_code==404


def test_buscar_carga_invalido(client):
    for value in ('abc','-1','1.5','1 OR 1=1','9'*500,'2147483648','²'):
        assert client.get('/api/carga/buscar',query_string={'numero':value}).status_code==400
    assert client.get('/api/carga/buscar?numero=1&numero=2').status_code==400


def test_buscar_carga_sin_parametro(app,client):
    assert client.get('/api/carga/buscar').status_code==400
    assert client.get('/api/carga/buscar?numero=%20').status_code==400
    assert app.test_client().get('/api/carga/buscar?numero=1').status_code==401
