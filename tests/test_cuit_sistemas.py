"""CUIT sintéticos y migraciones aditivas de clientes/sistemas."""
from pathlib import Path
from uuid import uuid4

from alembic import command
from alembic.config import Config
import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import crear_esquema
from app.models import Cliente, Sistema
from app.utils.cuit_validator import normalizar_cuit, validar_cuit
from scripts.audit_cuit import crear_reporte


@pytest.mark.parametrize('value', ['20000000001','20-00000000-1','30000000007','27000000006','23000000000'])
def test_cuit_sintetico_formato_y_verificador(value):
    assert validar_cuit(value)
    assert len(normalizar_cuit(value)) == 11


@pytest.mark.parametrize('value', ['82000000000','20000000000','2000000000','200000000011','20.00000000.1','2-000000000-1','２０000000001','abc',None,20000000001,True,'20 00000000 1','20-0000000-01'])
def test_cuit_invalido_se_rechaza(value):
    assert not validar_cuit(value)


def test_restante_uno_no_se_convierte_en_un_verificador_inventado():
    # [Ejemplo] Diez dígitos cuyo módulo requiere 10: no hay dígito válido.
    base = '2000000001'
    assert sum(int(d)*w for d,w in zip(base,(5,4,3,2,7,6,5,4,3,2)))%11 == 1
    assert not any(validar_cuit(base+str(d)) for d in range(10))


def test_modelo_normaliza_y_no_admite_digito_invalido():
    assert Cliente(nombre='[Ejemplo] Cliente', cuit=' 20-00000000-1 ').cuit == '20000000001'
    assert Cliente(nombre='[Ejemplo] Sin CUIT', cuit=None).cuit is None
    with pytest.raises(ValueError):
        Cliente(nombre='[Ejemplo] Invalido', cuit='82000000000')


def test_unicidad_y_varios_clientes_sin_cuit(app):
    engine = app.extensions['db_engine']
    with Session(engine) as db:
        db.add_all([Cliente(nombre='[Ejemplo] A'),Cliente(nombre='[Ejemplo] B'),Cliente(nombre='[Ejemplo] C',cuit='20-00000000-1')])
        db.commit()
        db.add(Cliente(nombre='[Ejemplo] Duplicado',cuit='20000000001'))
        with pytest.raises(IntegrityError):db.flush()
        db.rollback()
        report = crear_reporte(db.connection())
        assert len(report['clientes_sin_cuit']) == 3
        assert report['cuit_duplicados'] == []


def test_sistema_activo_por_defecto_y_no_acepta_cliente_ausente(app):
    with Session(app.extensions['db_engine']) as db:
        client = Cliente(nombre='[Ejemplo] Sistemas');db.add(client);db.flush()
        row = Sistema(cliente_id=client.id,tipo='SDI',designacion='[Ejemplo] Sistema');db.add(row);db.flush()
        assert row.activo is True
        db.add(Sistema(cliente_id=None,tipo='SDI',designacion='[Ejemplo] Sin cliente'))
        with pytest.raises(IntegrityError):db.flush()


def test_reporte_detecta_verificador_invalido_sin_cambiar_datos(app):
    engine=app.extensions['db_engine']
    with engine.begin() as c:
        c.execute(text('INSERT INTO clientes(id,nombre,es_ejemplo,cuit) VALUES(:id,:nombre,true,:cuit)'),
                  {'id':str(uuid4()),'nombre':'[Ejemplo] Registro inválido de prueba','cuit':'82000000000'})
    with engine.begin() as c:
        c.execute(text('SET TRANSACTION READ ONLY'))
        before=c.scalar(text('SELECT count(*) FROM clientes'))
        report=crear_reporte(c)
        assert len(report['clientes_cuit_invalidos']) == 1
        assert report['sistemas_sin_cliente'] == []
        assert c.scalar(text('SELECT count(*) FROM clientes')) == before


def test_auditoria_identifica_duplicados_normalizados_en_base_legacy(database_url):
    engine=create_engine(database_url)
    try:
        with engine.begin() as c:
            c.execute(text('CREATE TABLE clientes(id varchar(36), cuit varchar(20))'))
            c.execute(text('CREATE TABLE sistemas(id varchar(36),cliente_id varchar(36))'))
            c.execute(text("INSERT INTO clientes VALUES ('ejemplo-a','20-00000000-1'),('ejemplo-b','20000000001')"))
        with engine.begin() as c:
            c.execute(text('SET TRANSACTION READ ONLY'))
            report=crear_reporte(c)
            assert report['cuit_duplicados'] == [{'cuit':'20000000001','cliente_ids':['ejemplo-a','ejemplo-b']}]
            assert report['clientes_cuit_no_normalizados'] == ['ejemplo-a']
    finally:engine.dispose()


def test_downgrade_no_elimina_cuit_registrado(app):
    engine=app.extensions['db_engine']
    with Session(engine) as db:
        db.add(Cliente(nombre='[Ejemplo] Conservar CUIT',cuit='20000000001'));db.commit()
    config=Config(str(Path(__file__).resolve().parents[1]/'alembic.ini'))
    with pytest.raises(RuntimeError,match='No se eliminan CUIT'):
        with engine.begin() as c:
            config.attributes['connection']=c;command.downgrade(config,'010_firmantes')
    with engine.connect() as c:
        assert c.scalar(text('SELECT cuit FROM clientes WHERE cuit IS NOT NULL')) == '20000000001'
        assert c.scalar(text('SELECT version_num FROM alembic_version')) == '023_firma_certificado'


def test_migrar_010_a_012_conserva_uuid_relaciones_y_datos(database_url):
    engine=create_engine(database_url)
    root=Path(__file__).resolve().parents[1]
    config=Config(str(root/'alembic.ini'))
    cid,sid=str(uuid4()),str(uuid4())
    try:
        crear_esquema(engine)
        # Retroceder solo la BD aislada vacía para ensayar el upgrade real desde 010.
        with engine.begin() as c:
            config.attributes['connection']=c;command.downgrade(config,'010_firmantes')
            c.execute(text('INSERT INTO clientes(id,nombre,es_ejemplo) VALUES(:id,:nombre,true)'),{'id':cid,'nombre':'[Ejemplo] Histórico'})
            c.execute(text('INSERT INTO sistemas(id,cliente_id,tipo,designacion) VALUES(:id,:cid,\'SDI\',:nombre)'),{'id':sid,'cid':cid,'nombre':'[Ejemplo] Histórico'})
        crear_esquema(engine);crear_esquema(engine)
        with engine.connect() as c:
            assert c.execute(text('SELECT id,cuit FROM clientes WHERE id=:id'),{'id':cid}).one() == (cid,None)
            assert c.execute(text('SELECT id,cliente_id,activo FROM sistemas WHERE id=:id'),{'id':sid}).one() == (sid,cid,True)
            assert c.scalar(text('SELECT version_num FROM alembic_version')) == '023_firma_certificado'
            assert next(x for x in inspect(c).get_columns('sistemas') if x['name']=='cliente_id')['nullable'] is False
    finally:
        engine.dispose()
