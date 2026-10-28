"""Reglas nuevas con datos ficticios, sin autocompletar observaciones ni mediciones."""
from copy import deepcopy
from io import BytesIO

import pytest
from pypdf import PdfWriter
from sqlalchemy.orm import Session
from app.models import Carga

from app.carga.validacion import ValidationError, validar_item_verificacion, validar_reglas_carga
from app.planillas.multisistema import definiciones_multisistema, ejemplo_multisistema
from app.planillas.validacion import validar_datos
from app.planillas.firmantes import ejemplo_responsable
from scripts.prueba_operativa_final import firma_ficticia


@pytest.mark.parametrize('result', ['✓','O','X'])
def test_medir_cuando_hay_unidad_salvo_na(result):
    item={'resultado':result,'valor':0,'observacion':'[Ejemplo] Observación de prueba'}
    previous=deepcopy(item)
    assert validar_item_verificacion(item,{'unidad':'bar','formato':'ver'})==item
    assert item==previous
    del item['valor']
    with pytest.raises(ValidationError,match='medición'):
        validar_item_verificacion(item,{'unidad':'bar','formato':'ver'})


@pytest.mark.parametrize('observation', [None,'','   '])
def test_o_sin_observacion_rechazado(observation):
    with pytest.raises(ValidationError,match='requiere una observación'):
        validar_item_verificacion({'resultado':'O','observacion':observation},{})


@pytest.mark.parametrize('result', ['✓','X','NA'])
def test_observacion_opcional_para_los_otros_estados(result):
    validar_item_verificacion({'resultado':result},{})


def test_na_admite_omitir_medicion_y_general_no_exige_medicion():
    validar_item_verificacion({'resultado':'NA'},{'unidad':'bar','formato':'ver'})
    validar_item_verificacion({'resultado':'✓'},{'unidad':'bar','formato':'general'})


@pytest.mark.parametrize('value', [True,'1',float('nan'),float('inf'),float('-inf')])
def test_medicion_invalida_se_rechaza(value):
    with pytest.raises(ValidationError,match='número finito'):
        validar_item_verificacion({'resultado':'✓','valor':value},{'unidad':'bar'})


@pytest.mark.parametrize('value', ['',None,'SI','NO','o','✔'])
def test_estados_ajenos_no_se_aceptan(value):
    with pytest.raises(ValidationError,match='resultado válido'):
        validar_item_verificacion({'resultado':value},{})


def esquema_con_medicion():
    schema=definiciones_multisistema()['SG-PEM-IFI-SBC-3']['definicion']
    for title,table in schema['tablas'].items():
        for row in table['filas']:
            value,result=row['campos']
            if schema['bloques'][title][value].get('unidad'):
                return schema,title,value,result
    raise AssertionError('El original de prueba debe contener una medición.')


def test_borrador_incompleto_se_guarda_pero_no_puede_cerrarse():
    schema,title,value,result=esquema_con_medicion()
    data=ejemplo_multisistema(schema)
    del data['bloques'][title][value]
    assert validar_datos(data,schema)['bloques'][title][result]=='✓'
    with pytest.raises(ValidationError,match='medición'):
        validar_datos(data,schema,completo=True)
    data['bloques'][title][result]='NA'
    validar_datos(data,schema,completo=True)


def test_cierre_exige_observacion_existente_y_no_la_inventa():
    schema,title,value,result=esquema_con_medicion()
    data=ejemplo_multisistema(schema);data['bloques'][title][result]='O';data['observaciones']=[]
    before=deepcopy(data)
    with pytest.raises(ValidationError,match='observación'):
        validar_datos(data,schema,completo=True)
    assert data==before
    data['observaciones']=['[Ejemplo] Pérdida observada en el equipo inspeccionado.']
    validar_datos(data,schema,completo=True)


def test_omitir_el_bloque_no_evade_mediciones_al_cerrar():
    schema,title,value,result=esquema_con_medicion()
    data=ejemplo_multisistema(schema);data['bloques'][title]={}
    validar_datos(data,schema)
    with pytest.raises(ValidationError):
        validar_datos(data,schema,completo=True)


def crear_incompleta(client,catalogo):
    schema,title,value,result=esquema_con_medicion()
    planilla=next(p for p in client.get('/api/planillas').json if p['codigo']==schema['codigo'])
    system=next(p for p in client.get('/api/clientes/'+catalogo[0]['id']+'/sistemas').json if p['tipo']=='SBC')
    data=ejemplo_multisistema(schema);del data['bloques'][title][value]
    data['cabecera']['cliente']=catalogo[0]['nombre']
    data['cabecera']['sistema_designacion']=system['designacion']
    response=client.post('/api/cargas',json={'planilla_id':planilla['id'],'sistema_id':system['id'],'datos':data,
        'firmas':{role:firma_ficticia() for role in ('tecnico','responsable')},'responsable':ejemplo_responsable()})
    assert response.status_code==201,response.json
    return response.json,title,value


def test_api_no_finaliza_medicion_incompleta_y_conserva_borrador(client,catalogo):
    record,title,value=crear_incompleta(client,catalogo);url='/api/cargas/'+record['id']
    rejected=client.post(url+'/finalizar',json={'revision':record['revision']})
    assert rejected.status_code==422 and 'medición' in rejected.json['error']
    saved=client.get(url).json
    assert saved['estado']=='borrador' and saved['revision']==record['revision']
    assert value not in saved['datos']['bloques'][title]


def test_vista_previa_rechaza_antes_de_convertir_pdf(client,catalogo,monkeypatch):
    record,title,value=crear_incompleta(client,catalogo)
    def unexpected(*args,**kwargs):raise AssertionError('No debe generar un PDF inválido.')
    monkeypatch.setattr('app.rutas.api.generar_pdf_carga',unexpected)
    response=client.post('/api/cargas/'+record['id']+'/vista-previa',json={'revision':record['revision']})
    assert response.status_code==422 and 'medición' in response.json['error']


def test_pdf_historico_no_se_revalida_con_reglas_nuevas(app,client,catalogo):
    record,title,value=crear_incompleta(client,catalogo)
    writer=PdfWriter();writer.add_blank_page(width=841.89,height=595.28)
    stream=BytesIO();writer.write(stream);previous=stream.getvalue()
    with Session(app.extensions['db_engine']) as db:
        row=db.get(Carga,record['id']);row.estado='emitida';row.pdf=previous;db.commit()
    response=client.get('/api/cargas/'+record['id']+'/pdf')
    assert response.status_code==200 and response.data==previous
