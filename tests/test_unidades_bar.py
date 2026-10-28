"""Corrección versionada de presión, sin convertir datos históricos."""
from copy import deepcopy
from io import BytesIO
from openpyxl import load_workbook
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Planilla
from app.planillas.catalogo_completo import definiciones_restantes,definiciones_habilitadas
from app.planillas.unidades_autorizadas import CODIGO,VERSION,BLOQUE,CAMPO
from app.planillas.multisistema import ejemplo_multisistema
from app.planillas.generador import generar_multisistema

def test_migracion_bar_conserva_version_anterior(app,client):
    original=definiciones_restantes()[CODIGO]
    current=definiciones_habilitadas()[CODIGO]
    expected=deepcopy(original['definicion']);expected['bloques'][BLOQUE][CAMPO]['unidad']='bar'
    assert current['definicion']==expected and current['version']==VERSION
    with Session(app.extensions['db_engine']) as db:
        rows=list(db.scalars(select(Planilla).where(Planilla.codigo==CODIGO)))
        old=next(p for p in rows if p.version=='00-26-ms1');new=next(p for p in rows if p.version==VERSION)
        assert old.definicion==original['definicion'] and old.huella==original['huella']
        assert new.definicion==current['definicion'] and new.id!=old.id and new.manual_id==old.manual_id
    offered=[p for p in client.get('/api/planillas').get_json() if p['codigo']==CODIGO]
    assert len(offered)==1 and offered[0]['version']==VERSION

def test_nuevo_excel_bar_no_reinterpreta_datos_ni_estados(tmp_path):
    current=definiciones_habilitadas()[CODIGO];original=deepcopy(definiciones_restantes()[CODIGO])
    data=ejemplo_multisistema(current['definicion']);data['bloques'][BLOQUE][CAMPO]=23
    before=deepcopy(data)
    output=tmp_path/'scc_bar.xlsx';generar_multisistema(data,output,CODIGO)
    wb=load_workbook(output);assert wb.active[CAMPO].value=='23  bar';wb.close()
    assert data==before and definiciones_restantes()[CODIGO]==original
    for code,record in definiciones_habilitadas().items():
        if code.startswith('SG-PEM-IFI-SDI-'):
            for fields in record['definicion']['bloques'].values():
                for field in fields.values():
                    if field.get('opciones') and '✓' in field['opciones']:assert field['opciones']==['✓','O','X','NA']
