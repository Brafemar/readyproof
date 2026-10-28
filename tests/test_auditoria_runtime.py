"""Eventos atómicos, filtros administrativos y conservación del historial."""
from datetime import datetime
from uuid import uuid4
import pytest
from sqlalchemy import select,text
from sqlalchemy.orm import Session
from sqlalchemy.exc import DBAPIError
from tests.test_api import crear
from tests.test_desbloqueo_revision import emitir,pdf_simulado
from tests.test_auth import tecnico
from tests.conftest import login_cliente
from app.models import Auditoria,Carga


def registros(client,**filters):
    result=client.get('/api/auditoria',query_string=filters)
    assert result.status_code==200,result.get_json()
    return result.get_json()['registros']


def test_auditoria_crear_carga(client,catalogo,datos_api,usuario_admin):
    row=crear(client,catalogo,datos_api).get_json()
    records=registros(client,registro_id=row['id'])
    assert len(records)==1
    event=records[0]
    assert event['accion']=='INSERT' and event['tabla']=='carga' and event['usuario_id']==usuario_admin['id']
    assert event['datos_anterior'] is None and event['datos_nuevo']['datos']==row['datos']
    assert event['datos_nuevo']['estado']=='borrador' and 'pdf' not in event['datos_nuevo']
    assert not any(k in event['datos_nuevo'] for k in ('clave_hash','tecnico_png','responsable_png'))
    key=str(uuid4());payload=dict(sistema_id=catalogo[1]['id'],planilla_id=catalogo[2]['id'],datos=datos_api)
    first=client.post('/api/cargas',json=payload,headers={'Idempotency-Key':key})
    repeated=client.post('/api/cargas',json=payload,headers={'Idempotency-Key':key})
    assert first.status_code==201 and repeated.status_code==200
    assert len(registros(client,registro_id=key))==1


def test_auditoria_emitir_carga(app,client,catalogo,datos_api,pdf_simulado,monkeypatch):
    row=emitir(client,crear(client,catalogo,datos_api).get_json())
    event=registros(client,registro_id=row['id'],accion='UPDATE')[0]
    assert event['datos_anterior']['estado']=='finalizada' and event['datos_nuevo']['estado']=='emitida'
    assert event['datos_anterior']['numero_registro'] is None and event['datos_nuevo']['numero_registro']==row['numero_registro']
    assert event['datos_nuevo']['pdf_hash']==row['pdf_sha256']
    pending=crear(client,catalogo,datos_api).get_json()
    pending=client.post(f"/api/cargas/{pending['id']}/finalizar",json={'revision':pending['revision']}).get_json()
    before=registros(client,registro_id=pending['id'])
    import app.rutas.api as api
    def fallo(*args):raise RuntimeError('Fallo de conversión simulado')
    monkeypatch.setattr(api,'generar_pdf_carga',fallo)
    assert client.post(f"/api/cargas/{pending['id']}/emitir",json={'revision':pending['revision']}).status_code==503
    assert registros(client,registro_id=pending['id'])==before
    assert client.get(f"/api/cargas/{pending['id']}").get_json()['estado']=='finalizada'


def test_auditoria_desbloqueo(client,catalogo,datos_api,pdf_simulado):
    row=emitir(client,crear(client,catalogo,datos_api).get_json());url=f"/api/cargas/{row['id']}"
    original=client.get(url+'/pdf').data
    assert client.post(url+'/desbloquear',json={'revision':row['revision'],'motivo':'[Ejemplo] Corregir dato'}).status_code==200
    event=registros(client,registro_id=row['id'],accion='DESBLOQUEO')[0]
    assert event['datos_anterior']['estado']=='emitida' and event['datos_nuevo']['estado']=='borrador'
    assert event['datos_nuevo']['revision_publica']==1 and event['datos_nuevo']['motivo_desbloqueo']=='[Ejemplo] Corregir dato'
    assert event['datos_anterior']['pdf_hash'] and event['datos_nuevo']['pdf_hash'] is None
    assert client.get(url+'/emisiones/0/pdf').data==original


def test_auditoria_filtros(app,client,catalogo,datos_api,usuario_admin):
    first=crear(client,catalogo,datos_api).get_json();second=crear(client,catalogo,datos_api).get_json()
    result=registros(client,tabla='carga',registro_id=first['id'],accion='INSERT',usuario_id=usuario_admin['id'])
    assert len(result)==1 and result[0]['registro_id']==first['id']
    assert registros(client,tabla='sistema')==[]
    assert client.get('/api/auditoria?limit=1&offset=1').get_json()['total']==2
    for query in ('limit=0','limit=501','offset=-1','registro_id=no-uuid','usuario_id=no-uuid','accion=DROP','tabla=x%27','limit=1&limit=2','desconocido=1'):
        assert client.get('/api/auditoria?'+query).status_code==422
    assert app.test_client().get('/api/auditoria').status_code==401
    user,password=tecnico(client,catalogo)
    assert login_cliente(app,user['login'],password).get('/api/auditoria').status_code==403


def test_auditoria_timestamp_orden(app,client,catalogo,datos_api):
    for _ in range(3):crear(client,catalogo,datos_api)
    rows=registros(client)
    assert [r['timestamp'] for r in rows]==sorted((r['timestamp'] for r in rows),reverse=True)
    assert all(datetime.fromisoformat(r['timestamp']).tzinfo for r in rows)
    with app.extensions['db_engine'].connect() as connection:
        with pytest.raises(DBAPIError):connection.execute(text("UPDATE auditoria SET accion='DELETE'"))
        connection.rollback()
        with pytest.raises(DBAPIError):connection.execute(text('DELETE FROM auditoria'))
        connection.rollback()
    assert len(registros(client))==3
