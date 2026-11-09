from copy import deepcopy
from io import BytesIO
from uuid import uuid4
from pathlib import Path

import pytest
from pypdf import PdfReader
from sqlalchemy import select

from app.models import FirmaCarga,EnvioDocumentacion,Usuario
from app.planillas.firmantes import validar_responsable,ejemplo_responsable
from app.planillas.validacion import DatosInvalidos
from scripts.prueba_operativa_final import firma_ficticia


@pytest.mark.parametrize('dni',['00000000','00000000000','000000000000000'])
def test_dni_valido(dni):
    assert validar_responsable(dict(ejemplo_responsable(),dni_firmante=dni),completo=True)['dni_firmante']==dni


@pytest.mark.parametrize('dni',['','0000000','0'*16,'00.000.000','00-000000','abcdefgh','１２３４５６７８','00000000\n',None,12345678])
def test_dni_invalido(dni):
    with pytest.raises(DatosInvalidos):validar_responsable(dict(ejemplo_responsable(),dni_firmante=dni),completo=True)


@pytest.mark.parametrize('nombre',['','   ',None])
def test_nombre_responsable_obligatorio(nombre):
    with pytest.raises(DatosInvalidos):validar_responsable(dict(ejemplo_responsable(),nombre_firmante=nombre),completo=True)


def crear_borrador(client,catalogo,datos,*,firmas=None,responsable=None):
    payload=dict(sistema_id=catalogo[1]['id'],planilla_id=catalogo[2]['id'],datos=datos)
    if firmas is not None:payload['firmas']=firmas
    if responsable is not None:payload['responsable']=responsable
    response=client.post('/api/cargas',json=payload);assert response.status_code==201,response.json
    return response.json


@pytest.mark.parametrize('falta',['tecnico','responsable','nombre','dni'])
def test_no_finaliza_sin_firmas_y_datos(client,catalogo,datos_api,falta):
    firmas={role:firma_ficticia() for role in ('tecnico','responsable')};responsable=ejemplo_responsable()
    if falta in firmas:del firmas[falta]
    else:responsable['nombre_firmante' if falta=='nombre' else 'dni_firmante']=''
    row=crear_borrador(client,catalogo,datos_api,firmas=firmas,responsable=responsable)
    result=client.post('/api/cargas/'+row['id']+'/finalizar',json=dict(revision=1))
    assert result.status_code==422
    saved=client.get('/api/cargas/'+row['id']).json
    assert saved['estado']=='borrador' and saved['revision']==1


def test_identidad_tecnico_historial_y_pdf(client,catalogo,datos_api,app,usuario_admin):
    row=crear_borrador(client,catalogo,datos_api,firmas={role:firma_ficticia() for role in ('tecnico','responsable')},responsable=ejemplo_responsable())
    assert row['firmantes']['tecnico']['usuario_id']==usuario_admin['id']
    route='/api/cargas/'+row['id']
    updated=dict(ejemplo_responsable(),cargo_firmante='')
    saved=client.put(route+'/borrador',json=dict(revision=1,datos=datos_api,responsable=updated))
    assert saved.status_code==200
    history=client.get(route+'/revisiones').json
    assert history[0]['firmantes']['responsable']['cargo_firmante']=='[Ejemplo] Encargado'
    assert history[1]['firmantes']['responsable']['cargo_firmante']==''
    final=client.post(route+'/finalizar',json=dict(revision=saved.json['revision']));assert final.status_code==200
    emitted=client.post(route+'/emitir',json=dict(revision=final.json['revision']));assert emitted.status_code==201,emitted.json
    payload=client.get(route+'/pdf').data;reader=PdfReader(BytesIO(payload));assert len(reader.pages)==1
    text=reader.pages[0].extract_text()
    assert 'Fecha del servicio:' not in text and 'Empresa: readyproof' not in text
    for value in ['[Ejemplo] Responsable de prueba','DNI: 00000000','Cargo: No informado',usuario_admin['login']]:
        assert value in text,value
    assert reader.metadata['/ReadyproofFirmantes']
    out=Path('out/final_v1/pdf');out.mkdir(parents=True,exist_ok=True);(out/'SAA-1_firmantes.pdf').write_bytes(payload)
    with app.extensions['db_sessions']() as db:
        identity=db.get(FirmaCarga,row['id']);assert identity.tecnico_usuario_id==usuario_admin['id'] and identity.nombre_firmante==updated['nombre_firmante']


def test_documentacion_destino_editable_auditado(client,app,tmp_path):
    app.config.update(DOCUMENTACION_MODO_PRUEBA=True,DIRECTORIO_CORREO=str(tmp_path/'correo'))
    key=str(uuid4());headers={'Idempotency-Key':key}
    response=client.post('/api/usuario/enviar-documentacion',json=dict(destinatario='destino@example.invalid'),headers=headers)
    assert response.status_code==200,response.json
    repeated=client.post('/api/usuario/enviar-documentacion',json=dict(destinatario='destino@example.invalid'),headers=headers)
    assert repeated.json==response.json
    assert client.post('/api/usuario/enviar-documentacion',json=dict(destinatario='otro@example.invalid'),headers=headers).status_code==409
    with app.extensions['db_sessions']() as db:
        sent=db.get(EnvioDocumentacion,key);assert sent.destinatario=='destino@example.invalid' and sent.creado_en and sent.usuario_id
        assert db.get(Usuario,sent.usuario_id).email is None
        from email.parser import BytesParser
        from email import policy
        mail=BytesParser(policy=policy.default).parsebytes(sent.mensaje_eml)
        body=mail.get_body(preferencelist=('plain',)).get_content()
        assert 'DNI' in body and '8 a 15' in body and 'ambas firmas' in body and 'Agentes Limpios' in body


def test_responsable_no_admite_identidad_tecnico_inyectada(client,catalogo,datos_api):
    response=client.post('/api/cargas',json=dict(sistema_id=catalogo[1]['id'],planilla_id=catalogo[2]['id'],datos=datos_api,responsable=dict(ejemplo_responsable(),tecnico_usuario_id=str(uuid4()))))
    assert response.status_code==422


def test_identificacion_larga_permanece_dentro_del_pie():
    from app.planillas.identificacion_pdf import preparar_identificacion,FUENTE,BASE
    from pypdf._codecs.core_font_metrics import CORE_FONT_METRICS
    data=dict(tecnico=dict(nombre='[Ejemplo] '+'M'*110,login='w'*80),
              responsable=dict(nombre_firmante='[Ejemplo] '+'W'*110,dni_firmante='0'*15,cargo_firmante='[Ejemplo] '+'@'*110),
              empresa='[Ejemplo] '+'Ñ'*190,fecha='2026-10-25')
    columnas,top,escala=preparar_identificacion(data,841.89,595.28)
    widths=CORE_FONT_METRICS['Helvetica'].character_widths
    assert max(widths.values())<=1020
    for columna in columnas:
        for line in columna:
            assert sum(widths.get(char,widths['default']) for char in line)*FUENTE/1000<=(841.89-100)/2
    assert .70<=escala<=.95 and BASE>28.35+8+2
    assert 'W'*110 in ''.join(columnas[1]) and '@'*110 in ''.join(columnas[1])
