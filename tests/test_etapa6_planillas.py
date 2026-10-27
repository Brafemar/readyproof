"""Carga JSON, manuales y logo real de readyproof, sin modificar el kit."""
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import shutil

import pytest
from sqlalchemy import create_engine,func,select
from sqlalchemy.orm import Session
from PIL import Image
from pypdf import PdfReader
import pypdfium2 as pdfium

from app.carga_planillas import cargar_planillas_desde_json,huella_json
from app.catalogo import huella_saa1
from app.db import crear_esquema
from app.models import Manual,Planilla
from app.planillas.generador import generar_saa1
from app.planillas.pdf import convertir_pdf
from app.planillas.piloto import datos_ejemplo

ROOT=Path(__file__).resolve().parents[1]


def verificar_manual(app,code):
    with Session(app.extensions["db_engine"]) as session:
        row=session.scalar(select(Planilla).where(Planilla.codigo==code,Planilla.version=="v2"))
        assert row and row.manual and row.manual.titulo.startswith("[Ejemplo] ")
        assert row.manual.codigo==f"SG-PEM-IFI-{code}"
        assert row.manual.campos_obligatorios==[]


def test_sdi_vinculada_a_manual(app):verificar_manual(app,"SDI")


def test_sbc_vinculada_a_manual(app):verificar_manual(app,"SBC")


def test_sal_vinculada_a_manual(app):verificar_manual(app,"SAL")


def test_saa1_sigue_vinculada(app):
    verificar_manual(app,"SAA-1")
    with Session(app.extensions["db_engine"]) as session:
        pilot=session.scalar(select(Planilla).where(Planilla.codigo=="SG-PEM-IFI-SAA-1"))
        previous=pilot.manual_id
        assert pilot.manual.codigo=="SG-PEM-IFI-SAA-EJEMPLO"
        cargar_planillas_desde_json(session)
        session.refresh(pilot)
        assert pilot.manual_id==previous and pilot.huella==huella_saa1()


def test_todas_las_planillas_tienen_manual(app):
    with Session(app.extensions["db_engine"]) as session:
        assert session.scalar(select(func.count()).select_from(Planilla))==5
        assert session.scalar(select(func.count()).select_from(Planilla).where(Planilla.manual_id.is_(None)))==0


def test_esquema_valido_en_todas_planillas(app):
    with Session(app.extensions["db_engine"]) as session:
        for row in session.scalars(select(Planilla)):
            if row.codigo=="SG-PEM-IFI-SAA-1":
                assert set(row.definicion)=={"cabecera","bloques","observaciones"}
                assert row.huella==huella_saa1()
                continue
            document=json.loads((ROOT/"fuente/planillas"/(row.codigo+".json")).read_text(encoding="utf-8"))
            assert row.definicion==document
            assert {"cabecera","datos","firmas"}<=row.definicion.keys()
            assert row.huella==sha256(json.dumps(document,sort_keys=True).encode()).hexdigest()==huella_json(document)


def test_logo_reemplazado(tmp_path):
    asset=ROOT/"app/static/logo_readyproof.png"
    with Image.open(asset) as logo:
        assert logo.format=="PNG" and logo.width>=600 and logo.height>=150
        expected=sha256(logo.convert("RGB").tobytes()).hexdigest()
    source=generar_saa1(datos_ejemplo(),tmp_path/"SAA-1_readyproof.xlsx")
    pdf=convertir_pdf(source,tmp_path/"SAA-1_readyproof.pdf")
    reader=PdfReader(pdf)
    assert len(reader.pages)==2
    for page in reader.pages:
        hashes=[sha256(image.image.convert("RGB").tobytes()).hexdigest() for image in page.images]
        assert hashes.count(expected)==1 and len(hashes)==2
    out=ROOT/"out/etapa6";out.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(pdf,out/"SAA-1_readyproof.pdf")
    with pdfium.PdfDocument(str(pdf)) as document:
        for i in range(len(document)):
            page=document[i];bitmap=page.render(scale=1.8)
            bitmap.to_pil().save(out/f"SAA-1_pagina_{i+1}.png")
            bitmap.close();page.close()


def test_importacion_idempotente_sin_sobrescribir_version(app):
    with Session(app.extensions["db_engine"]) as session:
        before=session.scalar(select(func.count()).select_from(Planilla))
        assert cargar_planillas_desde_json(session)==0
        assert session.scalar(select(func.count()).select_from(Planilla))==before
        row=session.scalar(select(Planilla).where(Planilla.codigo=="SDI"))
        row.huella="0"*64;session.commit()
        with pytest.raises(ValueError,match="versión nueva"):cargar_planillas_desde_json(session)
        session.refresh(row);assert row.huella=="0"*64


def test_identidad_nueva_conserva_versiones_anteriores(app,client):
    from app.catalogo import registrar_ejemplos
    with Session(app.extensions['db_engine']) as session:
        active=session.scalar(select(Planilla).where(Planilla.codigo=='SG-PEM-IFI-SAA-1'))
        legacy=Planilla(codigo=active.codigo,version='00-26',sistema_tipo='SAA',huella='a'*64,definicion=active.definicion,manual_id=active.manual_id)
        group=session.scalar(select(Planilla).where(Planilla.codigo=='SDI'))
        old_group=Planilla(codigo='SDI',version='v1',sistema_tipo=group.sistema_tipo,huella='b'*64,definicion={'cabecera':{},'datos':{},'firmas':{}},manual_id=group.manual_id)
        session.add_all([legacy,old_group]);session.commit()
        ids={legacy.id,old_group.id}
        registrar_ejemplos(session)
        assert cargar_planillas_desde_json(session)==0
        assert session.get(Planilla,legacy.id).huella=='a'*64
        assert session.get(Planilla,old_group.id).huella=='b'*64
    offered={row['id'] for row in client.get('/api/planillas').get_json()}
    assert len(offered)==5 and not offered.intersection(ids)


def test_json_invalido_no_carga_datos_parciales(app,tmp_path,monkeypatch):
    import app.carga_planillas as module
    directory=tmp_path/"fuente/planillas";directory.mkdir(parents=True)
    for path in (ROOT/"fuente/planillas").glob("*.json"):shutil.copyfile(path,directory/path.name)
    (directory/"SDI.json").write_text('{"datos":null}',encoding="utf-8")
    monkeypatch.setattr(module,"RAIZ",tmp_path)
    with Session(app.extensions["db_engine"]) as session:
        before=session.scalar(select(func.count()).select_from(Planilla))
        with pytest.raises(ValueError):cargar_planillas_desde_json(session)
        assert session.scalar(select(func.count()).select_from(Planilla))==before


def test_downgrade_no_borra_manuales_vinculados(app):
    from alembic import command
    from alembic.config import Config
    engine=app.extensions["db_engine"]
    with pytest.raises(RuntimeError,match="vinculados"):
        with engine.begin() as connection:
            config=Config(str(ROOT/"alembic.ini"));config.attributes["connection"]=connection
            command.downgrade(config,"005_correo_modelos")
    with Session(engine) as session:
        assert session.scalar(select(func.count()).select_from(Manual))==5


def test_downgrade_sin_vinculos_conserva_manual_anterior(database_url):
    from alembic import command
    from alembic.config import Config
    engine=create_engine(database_url)
    try:
        crear_esquema(engine)
        with engine.begin() as connection:
            config=Config(str(ROOT/"alembic.ini"));config.attributes["connection"]=connection
            command.downgrade(config,"005_correo_modelos")
        with Session(engine) as session:
            assert [m.codigo for m in session.scalars(select(Manual))]==["SG-PEM-IFI-SAA-EJEMPLO"]
    finally:engine.dispose()
