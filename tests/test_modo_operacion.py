"""Modo real desactivado por defecto y simulaciones sin datos ni correos reales."""
from copy import deepcopy
from io import BytesIO
from pathlib import Path
from uuid import uuid4
from email import policy
from email.parser import BytesParser
import pytest
from pypdf import PdfReader
from sqlalchemy.orm import Session
from app.config import configuracion
from app.models import Carga,Envio
from app.planillas.firmantes import ejemplo_responsable
from scripts.prueba_operativa_final import firma_ficticia
from tests.test_api import crear
from tests.test_desbloqueo_revision import emitir,pdf_simulado

EMPRESA='Mantenedora de ensayo [Ejemplo]'
CERTIFICADO='IFI-2099-99999'


def real(app,client,catalogo,datos_api):
    app.config.update(MODO_PILOTO=False,EMPRESA_MANTENEDORA=EMPRESA,CERTIFICADO_N=CERTIFICADO,MAIL_MODO_PRUEBA=True)
    customer=client.post('/api/admin/clientes',json={'nombre':'Instalación de ensayo [Ejemplo]'}).get_json()
    assert customer['es_ejemplo'] is False
    system=client.post(f"/api/admin/clientes/{customer['id']}/sistemas",json={'tipo':'SAA','designacion':'Abastecimiento de ensayo [Ejemplo]'}).get_json()
    data=deepcopy(datos_api);data['cabecera'].update(cliente=customer['nombre'],sistema_designacion=system['designacion'],empresa_mantenedora=EMPRESA,numero_mantenedor=CERTIFICADO)
    response=client.post('/api/cargas',json={'sistema_id':system['id'],'planilla_id':catalogo[2]['id'],'datos':data,
        'responsable':ejemplo_responsable(),'firmas':{role:firma_ficticia() for role in ('tecnico','responsable')}})
    assert response.status_code==201,response.get_json()
    return response.get_json()


def test_modo_piloto_verdadero(app,client,catalogo,datos_api,pdf_simulado,monkeypatch,tmp_path):
    monkeypatch.delenv('MODO_PILOTO',raising=False);monkeypatch.delenv('MAIL_MODO_PRUEBA',raising=False)
    assert configuracion()['MODO_PILOTO'] is True and configuracion()['MAIL_MODO_PRUEBA'] is True
    app.config.update(DESTINATARIO_PRUEBA='prueba@test.com',MAIL_MODO_PRUEBA=True,DIRECTORIO_CORREO=str(tmp_path/'correo'))
    row=emitir(client,crear(client,catalogo,datos_api).get_json())
    result=client.post(f"/api/cargas/{row['id']}/enviar",json={'destinatario':'otro@example.invalid'})
    assert result.status_code==202
    with Session(app.extensions['db_engine']) as db:
        envio=db.get(Envio,result.get_json()['id'])
        assert envio.destinatario=='prueba@test.com'
        assert str(BytesParser(policy=policy.default).parsebytes(envio.mensaje_eml)['To'])=='prueba@test.com'
    assert list((tmp_path/'correo').glob('*.eml'))


def test_modo_piloto_falso_sin_empresa(app,client,catalogo,datos_api):
    row=real(app,client,catalogo,datos_api)
    app.config['EMPRESA_MANTENEDORA']='[Ejemplo] No confirmada'
    response=client.post(f"/api/cargas/{row['id']}/vista-previa",json={'revision':row['revision']})
    assert response.status_code==422 and 'EMPRESA_MANTENEDORA' in response.get_json()['error']
    assert client.get(f"/api/cargas/{row['id']}").get_json()['numero_registro'] is None


def test_modo_piloto_falso_sin_certificado(app,client,catalogo,datos_api):
    row=real(app,client,catalogo,datos_api);app.config['CERTIFICADO_N']='IFI-2024-00000'
    finalized=client.post(f"/api/cargas/{row['id']}/finalizar",json={'revision':row['revision']}).get_json()
    response=client.post(f"/api/cargas/{row['id']}/emitir",json={'revision':finalized['revision']})
    assert response.status_code==422 and 'CERTIFICADO_N' in response.get_json()['error']
    assert client.get(f"/api/cargas/{row['id']}").get_json()['numero_registro'] is None


def test_modo_piloto_falso_empresa_real(app,client,catalogo,datos_api,pdf_simulado,monkeypatch,tmp_path):
    monkeypatch.setenv('MODO_PILOTO','false');monkeypatch.delenv('MAIL_MODO_PRUEBA',raising=False)
    assert configuracion()['MODO_PILOTO'] is False and configuracion()['MAIL_MODO_PRUEBA'] is False
    row=emitir(client,real(app,client,catalogo,datos_api))
    assert row['estado']=='emitida' and row['numero_registro']==1 and row['revision_publica']==0
    page=client.get('/').data.decode('utf-8')
    assert 'data-modo-piloto="false"' in page and 'Modo REAL' in page
    app.config.update(PLANILLAS_TRANSPORTE='gmail_api',DIRECTORIO_CORREO=str(tmp_path/'correo'))
    response=client.post(f"/api/cargas/{row['id']}/enviar",json={'destinatario':'destino@example.invalid','inmediato':True},headers={'Idempotency-Key':str(uuid4())})
    assert response.status_code==202 and response.get_json()['modo_prueba'] is True
    assert response.get_json()['estado']=='pendiente' and list((tmp_path/'correo').glob('*.eml'))
    app.config['MODO_PILOTO']=True
    assert client.post(f"/api/cargas/{row['id']}/desbloquear",json={'revision':row['revision'],'motivo':'[Ejemplo] Motivo'}).status_code==403


def test_pdf_leyenda_piloto(app,client,catalogo,datos_api):
    row=emitir(client,crear(client,catalogo,datos_api).get_json())
    payload=client.get(f"/api/cargas/{row['id']}/pdf").data
    output=Path('out/etapa6_final/pdf');output.mkdir(parents=True,exist_ok=True);(output/'PILOTO.pdf').write_bytes(payload)
    reader=PdfReader(BytesIO(payload))
    assert reader.metadata['/ReadyproofModo']=='PILOTO'
    assert all('Modo PILOTO' in page.extract_text() for page in reader.pages)
    assert len(reader.pages)==1 and len(reader.pages[0].images)==4
    assert 'Planilla conforme a IRAM 3546:2011' in reader.pages[0].extract_text()


def test_pdf_leyenda_real(app,client,catalogo,datos_api):
    row=emitir(client,real(app,client,catalogo,datos_api))
    payload=client.get(f"/api/cargas/{row['id']}/pdf").data;reader=PdfReader(BytesIO(payload))
    output=Path('out/etapa6_final/pdf');output.mkdir(parents=True,exist_ok=True);(output/'REAL_datos_ficticios.pdf').write_bytes(payload)
    assert reader.metadata['/ReadyproofModo']=='REAL' and all('Modo REAL' in page.extract_text() for page in reader.pages)
    text=reader.pages[0].extract_text()
    assert EMPRESA in text and CERTIFICADO in ''.join(text.split())
    assert len(reader.pages)==1 and len(reader.pages[0].images)==4
    assert client.get(f"/api/cargas/{row['id']}/emisiones/0/pdf").data==payload
