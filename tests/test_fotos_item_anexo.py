"""Ítem de la marca: fuente del kit, persistencia, migración y anexo."""
from copy import deepcopy
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from io import BytesIO
import json
from pathlib import Path
import subprocess
from uuid import uuid4

from alembic.migration import MigrationContext
from alembic.operations import Operations
from PIL import Image
from pypdf import PdfReader
import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session
from werkzeug.exceptions import BadRequest

from app.fotos.anotaciones import validar_anotaciones
from app.fotos.items import items_punto2
from app.fotos.anexo_pdf import generar_anexo
from app.models import Carga, Planilla, Sistema
from app.models.fotos import FotoAnotacionItem
from app.planillas.multisistema import ejemplo_multisistema
from app.planillas.catalogo_completo import definiciones_habilitadas
from app.planillas.validacion import esquema_saa1
from tests.test_fotos_c3b_api import foto_c3b, guardar, marca
from tests.test_fotos_c3_interfaz import node, entorno_node
from tests.test_fotos_c4b_anexo import pdftotext

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTO = json.loads((ROOT/'app/planillas/definiciones/restantes_v5.json').read_text(encoding='utf-8'))
SCC = next(p for p in DOCUMENTO['planillas'] if p['codigo']=='SG-PEM-IFI-SCC-2')
DEFINICION = SCC['definicion']
ITEM = next(r for r in items_punto2(DEFINICION) if r['campo']=='I16')


def test_items_provienen_del_json_sin_cambiar_texto():
    items = items_punto2(DEFINICION)
    rows = DEFINICION['tablas']['INSPECCIÓN MENSUAL']['filas']
    assert len(items)==len(rows)==15
    assert [i['texto'] for i in items]==[r['etiqueta'] for r in rows]
    assert [i['campo'] for i in items]==[r['campos'][0] for r in rows]


@pytest.mark.parametrize('alteracion', ['campo', 'texto', 'bloque'])
def test_rechaza_referencia_ajena_o_texto_inventado(alteracion):
    item={**ITEM, alteracion:'inexistente'}
    with pytest.raises(BadRequest):
        validar_anotaciones({'anotaciones':[marca('O','Se observa grasa.',item=item)]}, DEFINICION)


def test_referencia_no_asigna_codigo():
    with pytest.raises(BadRequest):
        validar_anotaciones({'anotaciones':[marca('', '', item=ITEM)]}, DEFINICION)


def test_item_se_guarda_y_recupera_sin_alterar_resultados(app,client,foto_c3b):
    engine=app.extensions['db_engine']
    with Session(engine) as db:
        carga=db.get(Carga,foto_c3b['carga_id'])
        planilla=db.scalar(select(Planilla).where(Planilla.codigo=='SG-PEM-IFI-SCC-2'))
        assert planilla is not None
        db.get(Sistema,carga.sistema_id).tipo='SCC'
        carga.planilla_id=planilla.id;carga.datos=ejemplo_multisistema(planilla.definicion)
        original=deepcopy(carga.datos);db.commit()
    opts=client.get(f"/api/cargas/{foto_c3b['carga_id']}/fotos/items")
    assert opts.status_code==200 and ITEM in opts.get_json()
    first=guardar(client,foto_c3b,[marca('O','Se observa grasa.',item={'bloque':ITEM['bloque'],'campo':ITEM['campo']})])
    assert first.status_code==200,first.get_json()
    assert first.get_json()[0]['item']==ITEM
    read=client.get(foto_c3b['url']+'/anotaciones')
    assert read.get_json()==first.get_json()
    with Session(engine) as db:
        ref=db.get(FotoAnotacionItem,first.get_json()[0]['id'])
        assert ref.campo==ITEM['campo'] and ref.texto==ITEM['texto']
        assert db.get(Carga,foto_c3b['carga_id']).datos==original
    # Repetir un envio confirmado con un ETag anterior conserva la referencia.
    duplicate=guardar(client,foto_c3b,[marca('O','Se observa grasa.',item=ITEM)],headers={'If-Match':'"anterior"'})
    assert duplicate.status_code==200
    assert duplicate.get_json()==first.get_json()
    assert guardar(client,foto_c3b,[]).status_code==200
    with Session(engine) as db:
        assert db.get(FotoAnotacionItem,first.get_json()[0]['id']) is None


def test_migracion_020_reversible_y_no_elimina_referencias(database_url):
    engine=create_engine(database_url)
    try:
        path=ROOT/'migraciones/alembic/versions/020_foto_anotacion_item.py'
        spec=spec_from_file_location('migracion020_prueba',path);mod=module_from_spec(spec);spec.loader.exec_module(mod)
        assert mod.down_revision=='019_fotos_carga'
        with engine.begin() as c:
            c.execute(text('CREATE TABLE fotos_anotacion(id VARCHAR(36) PRIMARY KEY)'))
            c.execute(text('CREATE TABLE versiones_esquema(numero INTEGER PRIMARY KEY,aplicada_en TIMESTAMPTZ NOT NULL)'))
            with Operations.context(MigrationContext.configure(c)):
                mod.upgrade();assert c.scalar(text('SELECT numero FROM versiones_esquema'))==20
                mod.downgrade();mod.upgrade()
            c.execute(text("INSERT INTO fotos_anotacion VALUES ('ejemplo')"))
            c.execute(text("INSERT INTO fotos_anotacion_item VALUES ('ejemplo',:bloque,:campo,:texto)"),ITEM)
            with Operations.context(MigrationContext.configure(c)):
                with pytest.raises(RuntimeError,match='No se eliminan'):mod.downgrade()
            assert c.scalar(text('SELECT count(*) FROM fotos_anotacion_item'))==1
    finally:engine.dispose()


def test_anexo_muestra_item_codigo_y_observacion(tmp_path):
    image=BytesIO();Image.new('RGB',(800,600),'#e4eced').save(image,format='JPEG',quality=70)
    mark=dict(numero=1,x=.5,y=.5,codigo='O',texto='Se observa grasa.',item=ITEM)
    pdf=generar_anexo(image.getvalue(),[mark],[mark])
    text_content=pdftotext(pdf,tmp_path/'item.pdf')
    for expected in ['Ítem: Filtros de la campana colocados y sin acumulación excesiva de grasa','Código: O (no cumple)','Observación: Se observa grasa.']:
        assert expected in ' '.join(text_content.split())
    reader=PdfReader(BytesIO(pdf));assert len(reader.pages)==1
    embedded=reader.pages[0]['/Resources']['/XObject']['/RPFOTO'].get_object()._data
    assert sha256(embedded).digest()==sha256(image.getvalue()).digest()


def test_selector_primero_item_sin_resultado_automatico():
    opciones=items_punto2(DEFINICION)
    result=subprocess.run([node(),'tests/browser/fotos_item.cjs'],cwd=ROOT,env=entorno_node(RP_ITEMS=json.dumps([ITEM,opciones[0]])),capture_output=True,text=True,encoding='utf-8',timeout=40)
    assert result.returncode==0,result.stdout+result.stderr


@pytest.mark.parametrize("planilla", DOCUMENTO["planillas"], ids=lambda p: p["codigo"])
def test_punto2_de_cada_planilla_del_json(planilla):
    definicion = planilla["definicion"]
    items = items_punto2(definicion)
    assert items, planilla["codigo"]
    for item in items:
        campos = definicion["bloques"][item["bloque"]]
        assert item["campo"] in campos
        tabla = definicion.get("tablas", {}).get(item["bloque"])
        if tabla is not None:
            assert any(fila["etiqueta"] == item["texto"] and fila["campos"][0] == item["campo"] for fila in tabla["filas"])
        else:
            assert item["texto"] == (campos[item["campo"]].get("etiqueta") or item["campo"])
    for bloque, campos in definicion["bloques"].items():
        tabla = definicion.get("tablas", {}).get(bloque)
        expected = {fila["campos"][0] for fila in tabla["filas"]} if tabla is not None else set(campos)
        assert {item["campo"] for item in items if item["bloque"] == bloque} == expected


def test_punto2_en_catalogo_completo(app, client):
    with Session(app.extensions["db_engine"]) as db:
        response = client.get("/api/planillas")
        assert response.status_code == 200
        ofrecidas = response.get_json()
        listado = json.loads((ROOT/"LISTADO_ITEMS_PUNTO2.json").read_text(encoding="utf-8"))
        assert {p["codigo"] for p in ofrecidas} == {p["codigo"] for p in listado["planillas"]}
        planillas = list(db.scalars(select(Planilla).where(Planilla.id.in_([p["id"] for p in ofrecidas]))))
        for planilla in planillas:
            assert items_punto2(planilla.definicion), planilla.codigo


LISTADO = json.loads((ROOT/"LISTADO_ITEMS_PUNTO2.json").read_text(encoding="utf-8"))
ESQUEMAS = {codigo: row["definicion"] for codigo, row in definiciones_habilitadas().items()}
ESQUEMAS["SG-PEM-IFI-SAA-1"] = esquema_saa1()


@pytest.mark.parametrize("planilla", LISTADO["planillas"], ids=lambda p: p["codigo"])
def test_selector_coincide_con_listado_autorizado(planilla):
    actual = items_punto2(ESQUEMAS[planilla["codigo"]])
    esperado = [{k: item[k] for k in ("bloque", "campo", "texto")} for item in planilla["items"]]
    assert actual == esperado
    assert len(actual) == planilla["cantidad_items"]
