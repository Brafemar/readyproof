"""Cotejo de originales y transacciones del importador, sin sobrescrituras."""
from collections import Counter
from copy import deepcopy
from hashlib import sha256
import json
import os
from pathlib import Path

import pytest
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Planilla
from app.planillas.importacion_excel import contenido_esquema, diferencias_catalogo
from scripts.importador_planillas import preparar, importar

ROOT=Path(__file__).resolve().parents[1]


@pytest.fixture
def app(app):
    """Ensaya la importación sobre el catálogo previo, en una BD aislada sin cargas."""
    from alembic import command
    from alembic.config import Config
    with app.extensions['db_engine'].begin() as connection:
        config=Config(str(ROOT/'alembic.ini'));config.attributes['connection']=connection
        command.downgrade(config,'013_desbloqueo_revision')
    yield app


@pytest.fixture(scope='module')
def originales():
    origin=Path(os.environ.get('READYPROOF_EXCEL_ORIGEN',str(Path.home()/'Downloads/SG-PEM-IFI_Planillas_v5.zip')))
    catalog=ROOT/'docs/pedido_codex_v1_1/catalogo_referencia_planillas.json'
    if not origin.exists():pytest.fail('Configurar READYPROOF_EXCEL_ORIGEN con los 79 Excel oficiales o su ZIP; no se omite el cotejo.')
    return preparar(origin,catalog)


def test_79_excel_vs_catalogo_sin_diferencias_y_esquemas_reproducibles(originales):
    assert len(originales)==79
    assert sum(row['items'] for row in originales)==1539
    assert Counter(r['formato'] for r in originales)=={'general':14,'grid_s':8,'grid_m':11,'ver':46}
    for row in originales:
        assert not row['diferencias_catalogo']
        assert len(row['sha256_excel'])==len(row['nueva']['huella'])==64
        assert len(row['nueva']['version'])<=30
        assert contenido_esquema(row['nueva']['definicion'])==row['contenido']
        schema=row['nueva']['definicion']
        assert schema['fila_observaciones']==schema['origen_excel']['fila_observaciones_encabezado']+1


def registros(session):
    return {p.id:(p.codigo,p.version,p.huella,deepcopy(p.definicion),p.manual_id) for p in session.scalars(select(Planilla))}


def test_simulacion_16_existentes_63_pendientes_no_escribe(app,originales):
    with Session(app.extensions['db_engine']) as db:
        before=registros(db)
        report=importar(db,originales)
        assert report['estados']=={'YA_EXISTE':16,'A_IMPORTAR':63}
        assert not report['errores'] and report['cambios']==0
        db.commit()
        assert registros(db)==before


def test_no_importa_encabezado_nuevo_alterado_aunque_campos_coincidan(app,originales):
    rows=deepcopy(originales)
    row=next(r for r in rows if r['codigo']=='SG-PEM-IFI-SAP-1')
    row['nueva']['definicion']['sistema']='[Ejemplo] Encabezado ajeno al kit'
    row['nueva']['huella']=sha256(json.dumps(row['nueva']['definicion'],sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    with Session(app.extensions['db_engine']) as db:
        before=registros(db);report=importar(db,rows,aplicar=True)
        assert report['errores'] and report['cambios']==0
        assert next(p for p in report['planillas'] if p['codigo']==row['codigo'])['estado']=='CONTENIDO_DIFERENTE'
        db.commit();assert registros(db)==before


def test_importacion_aislada_atomica_idempotente_y_sin_sobrescribir(app,originales):
    with Session(app.extensions['db_engine']) as db:
        before=registros(db)
        report=importar(db,originales,aplicar=True);db.commit()
        assert report['cambios']==63 and report['estados']=={'YA_EXISTE':16,'IMPORTADA':63}
        after=registros(db)
        assert len(after)==len(before)+63
        assert all(after[key]==value for key,value in before.items())
        again=importar(db,originales,aplicar=True);db.commit()
        assert again['cambios']==0 and again['estados']=={'YA_EXISTE':79}
        assert registros(db)==after


def test_diferencia_en_bd_se_reporta_por_lineas_y_evita_importacion_parcial(app,originales):
    with Session(app.extensions['db_engine']) as db:
        p=db.scalar(select(Planilla).where(Planilla.codigo=='SG-PEM-IFI-SDI-5',Planilla.version=='00-26-ms1'))
        schema=deepcopy(p.definicion);title=next(iter(schema['tablas']))
        schema['tablas'][title]['filas'][0]['etiqueta']='[Ejemplo] Alteración de prueba'
        p.definicion=schema;db.commit()
        before=registros(db)
        report=importar(db,originales,aplicar=True);db.commit()
        differences=[r for r in report['planillas'] if r['estado']=='CONTENIDO_DIFERENTE']
        assert len(differences)==1 and differences[0]['diferencias_lineas']
        assert report['errores'] and report['cambios']==0
        assert registros(db)==before


def test_perdida_de_opcion_en_un_control_tambien_es_diferencia(app,originales):
    with Session(app.extensions['db_engine']) as db:
        p=db.scalar(select(Planilla).where(Planilla.codigo=='SG-PEM-IFI-SDI-3',Planilla.version=='00-26-ms1'))
        schema=deepcopy(p.definicion);title=next(iter(schema['tablas']))
        result=schema['tablas'][title]['filas'][0]['campos'][-1]
        schema['bloques'][title][result]['opciones'].remove('O')
        p.definicion=schema;db.commit()
        before=registros(db);report=importar(db,originales,aplicar=True);db.commit()
        assert report['errores'] and report['cambios']==0
        assert next(r for r in report['planillas'] if r['codigo']==p.codigo)['estado']=='CONTENIDO_DIFERENTE'
        assert registros(db)==before


def test_catalogo_alterado_no_autoriza_escrituras(app,originales):
    changed=deepcopy(originales)
    changed[-1]['diferencias_catalogo']=[{'tipo':'texto','fila':11}]
    with Session(app.extensions['db_engine']) as db:
        before=registros(db);report=importar(db,changed,aplicar=True);db.commit()
        assert report['errores'] and report['cambios']==0
        assert registros(db)==before


def test_tipo_de_medicion_alterado_no_se_da_por_existente(app,originales):
    with Session(app.extensions['db_engine']) as db:
        p=db.scalar(select(Planilla).where(Planilla.codigo=='SG-PEM-IFI-SBC-3',Planilla.version=='00-26-ms1'))
        schema=deepcopy(p.definicion)
        field=next(field for fields in schema['bloques'].values() for field in fields.values() if field.get('unidad'))
        assert field['tipo']=='numero';field['tipo']='texto'
        p.definicion=schema;db.commit()
        before=registros(db);report=importar(db,originales,aplicar=True);db.commit()
        row=next(r for r in report['planillas'] if r['codigo']==p.codigo)
        assert row['estado']=='CONTENIDO_DIFERENTE' and row['diferencias_lineas']
        assert report['cambios']==0 and registros(db)==before
