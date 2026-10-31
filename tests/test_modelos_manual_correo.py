"""Manual de ejemplo y relaciones de correo, sin transporte SMTP."""
from datetime import timedelta
from pathlib import Path
import runpy
from uuid import UUID,uuid4

import pytest
from sqlalchemy import create_engine,func,inspect,select,text
from sqlalchemy.exc import DBAPIError,IntegrityError
from sqlalchemy.orm import Session

from app.db import crear_esquema
from app.models import Base,Carga,Envio,Intento,Manual,Planilla,Retencion,ahora


def carga_de_prueba(session,catalogo,datos_api):
    row=Carga(sistema_id=catalogo[1]["id"],planilla_id=catalogo[2]["id"],datos=datos_api)
    session.add(row);session.flush();return row


def test_saa1_relacionado_con_manual(app,client,catalogo):
    with Session(app.extensions["db_engine"]) as session:
        planilla=session.get(Planilla,catalogo[2]["id"])
        assert planilla.manual.titulo=="[Ejemplo] Sistema de Abastecimiento de Agua"
        assert planilla.manual.sistema_tipo=="SAA"
        assert planilla.manual.campos_obligatorios==[]
        assert planilla.manual.contenido.startswith("[Ejemplo] ")
        assert str(UUID(planilla.manual.id))==planilla.manual.id
        assert planilla in planilla.manual.planillas


def test_planilla_manual_nullable_y_codigo_unico(app,client,catalogo):
    with Session(app.extensions["db_engine"]) as session:
        row=Planilla(codigo="[Ejemplo] Planilla sin manual",version="v1",sistema_tipo="SAA",huella="e"*64,definicion={})
        session.add(row);session.commit();assert row.manual_id is None and row.manual is None
        source=session.get(Planilla,catalogo[2]["id"]).manual
        duplicate=Manual(codigo=source.codigo,titulo="[Ejemplo] Otra versión",sistema_tipo="SAA",contenido="[Ejemplo] Contenido ficticio",campos_obligatorios=[],version="v2")
        session.add(duplicate)
        with pytest.raises(IntegrityError):session.flush()
        session.rollback()


def test_alembic_actualiza_base_etapa4_sin_perder_planilla(database_url):
    engine=create_engine(database_url)
    root=Path(__file__).resolve().parents[1]
    try:
        key=str(uuid4())
        with engine.begin() as connection:
            runpy.run_path(str(root/"migraciones/base_etapa4.py"))["upgrade"](connection)
            assert not inspect(connection).has_table("manuales")
            connection.execute(Planilla.__table__.insert().values(id=key,codigo="SG-PEM-IFI-SAA-1",version="00-26",sistema_tipo="SAA",huella="e"*64,definicion={"cabecera":{}}))
        crear_esquema(engine)
        crear_esquema(engine)
        with Session(engine) as session:
            row=session.get(Planilla,key)
            assert row.huella=="e"*64 and row.definicion=={"cabecera":{}}
            assert row.manual.titulo=="[Ejemplo] Sistema de Abastecimiento de Agua"
            assert session.scalar(text("SELECT version_num FROM alembic_version"))=="019_fotos_carga"
            assert list(session.scalars(text("SELECT numero FROM versiones_esquema ORDER BY numero")))==list(range(1,15))+[16,17,19]
    finally:engine.dispose()


def test_envio_intento_retencion_y_uuid(app,client,catalogo,datos_api,monkeypatch):
    import smtplib
    def prohibido(*args,**kwargs):raise AssertionError("No se permite SMTP real en esta prueba.")
    monkeypatch.setattr(smtplib,"SMTP",prohibido);monkeypatch.setattr(smtplib,"SMTP_SSL",prohibido)
    with Session(app.extensions["db_engine"]) as session:
        carga=carga_de_prueba(session,catalogo,datos_api)
        envio=Envio(carga=carga,destinatario="tecnico@example.invalid")
        intento=Intento(envio=envio,numero=1,resultado="timeout",respuesta="[Ejemplo] Respuesta de prueba sin conexión SMTP.")
        retencion=Retencion(envio=envio,reintentado_en=ahora()+timedelta(minutes=15),proximos_intentos=2,razon="fallo_temporal")
        session.add_all([envio,intento,retencion]);session.commit()
        assert envio.estado=="pendiente" and envio.enviado_en is None
        assert envio.creado_en.tzinfo and intento.intentado_en.tzinfo
        assert envio.carga is carga and envio in carga.envios
        assert intento in envio.intentos and retencion in envio.retenciones
        for row in (envio,intento,retencion):assert str(UUID(row.id))==row.id


def test_envio_cascade_a_intentos_y_retenciones(app,client,catalogo,datos_api):
    engine=app.extensions["db_engine"]
    with Session(engine) as session:
        envio=Envio(carga=carga_de_prueba(session,catalogo,datos_api),destinatario="prueba@example.invalid")
        session.add_all([envio,Intento(envio=envio,numero=1,resultado="rechazado"),Retencion(envio=envio,proximos_intentos=0,razon="bloqueado")]);session.commit()
        key=envio.id
        assert len(envio.intentos)==1 and len(envio.retenciones)==1
        session.delete(envio);session.commit()
        assert session.scalar(select(func.count()).select_from(Intento).where(Intento.envio_id==key))==0
        assert session.scalar(select(func.count()).select_from(Retencion).where(Retencion.envio_id==key))==0


def test_carga_cascade_a_envios_solo_en_base_temporal(app,client,catalogo,datos_api):
    with Session(app.extensions["db_engine"]) as session:
        carga=carga_de_prueba(session,catalogo,datos_api)
        envio=Envio(carga=carga,destinatario="prueba@example.invalid")
        session.add(envio);session.commit();key=envio.id
        assert envio in carga.envios
        session.delete(carga);session.commit()
        assert session.scalar(select(func.count()).select_from(Envio).where(Envio.id==key))==0


@pytest.mark.parametrize("kind",["numero","duplicado","resultado","reintentos","razon","estado","fk"])
def test_integridad_de_modelos_correo(app,client,catalogo,datos_api,kind):
    with Session(app.extensions["db_engine"]) as session:
        envio=Envio(carga=carga_de_prueba(session,catalogo,datos_api),destinatario="prueba@example.invalid")
        session.add(envio);session.flush()
        if kind=="numero":session.add(Intento(envio=envio,numero=0,resultado="timeout"))
        elif kind=="duplicado":session.add_all([Intento(envio=envio,numero=1,resultado="timeout"),Intento(envio=envio,numero=1,resultado="timeout")])
        elif kind=="resultado":session.add(Intento(envio=envio,numero=1,resultado="desconocido"))
        elif kind=="reintentos":session.add(Retencion(envio=envio,proximos_intentos=3,razon="fallo_temporal"))
        elif kind=="razon":session.add(Retencion(envio=envio,proximos_intentos=0,razon="desconocida"))
        elif kind=="estado":envio.estado="otro"
        else:session.add(Intento(envio_id=str(uuid4()),numero=1,resultado="timeout"))
        with pytest.raises(DBAPIError):session.flush()
        session.rollback()


def test_mapeo_orm_coincide_con_migraciones(app):
    from alembic.autogenerate import compare_metadata
    from alembic.migration import MigrationContext
    with app.extensions["db_engine"].connect() as connection:
        context=MigrationContext.configure(connection)
        assert compare_metadata(context,Base.metadata)==[]
