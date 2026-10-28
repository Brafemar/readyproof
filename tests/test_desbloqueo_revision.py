"""Reemisión sin perder el original, permisos y contador transaccional PostgreSQL."""
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from hashlib import sha256
from io import BytesIO
from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter
from sqlalchemy import select, text
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import Session

from app.carga.servicios import preparar_numero_emision
from app.models import Carga, EmisionCarga, NumeroRegistroContador
from app.planillas.multisistema import definiciones_multisistema, ejemplo_multisistema
from app.planillas.sdi_validacion import validar_sdi_grilla_mensual
from app.planillas.validacion import DatosInvalidos, validar_datos
from app.planillas.firmantes import ejemplo_responsable
from scripts.prueba_operativa_final import firma_ficticia
from tests.conftest import login_cliente
from tests.test_api import crear
from tests.test_auth import tecnico
from tests.test_envio_pdf_interfaz import gmail, solicitar


def pdf_vacio():
    writer = PdfWriter(); writer.add_blank_page(width=841.89, height=595.28)
    output = BytesIO(); writer.write(output)
    return output.getvalue()


def emitir(client, row):
    response = client.post(f"/api/cargas/{row['id']}/finalizar", json={'revision':row['revision']})
    assert response.status_code == 200, response.get_json()
    response = client.post(f"/api/cargas/{row['id']}/emitir", json={'revision':response.get_json()['revision']})
    assert response.status_code == 201, response.get_json()
    return response.get_json()


@pytest.fixture
def pdf_simulado(monkeypatch,tmp_path):
    import app.rutas.api as api
    from app.planillas.registro_pdf import incorporar_registro
    from app.planillas.leyenda_iram import incorporar_leyenda_iram
    source=tmp_path/'base.pdf';source.write_bytes(pdf_vacio())
    ready=tmp_path/'con_leyenda.pdf';incorporar_leyenda_iram(source,ready)
    payload=ready.read_bytes()
    monkeypatch.setattr(api, 'generar_pdf_carga', lambda carga, datos: incorporar_registro(
        payload, carga.numero_registro, carga.revision_publica))


def test_desbloqueo_reemision_conserva_pdf_numero_y_dos_firmas_nuevas(client,catalogo,datos_api,app,pdf_simulado):
    row = emitir(client, crear(client,catalogo,datos_api).get_json())
    assert row['numero_registro'] == 1 and row['revision_publica'] == 0
    original = client.get(f"/api/cargas/{row['id']}/pdf").data
    result = client.post(f"/api/cargas/{row['id']}/desbloquear",json={'revision':row['revision'],'motivo':'[Ejemplo] Corregir observación'})
    assert result.status_code == 200, result.get_json()
    unlocked = result.get_json()
    assert unlocked['estado'] == 'borrador' and unlocked['revision_publica'] == 1
    assert unlocked['numero_registro'] == 1 and not unlocked['pdf_disponible']
    assert not any(unlocked['firmas'].values())
    audit=client.get(f"/api/cargas/{row['id']}/revisiones").get_json()[-1]
    assert audit['evento'] == 'desbloqueada'
    assert audit['firmantes']['desbloqueo'] == {'motivo':'[Ejemplo] Corregir observación','numero_registro':1,'revision_publica':1}
    assert client.get(f"/api/cargas/{row['id']}/pdf").status_code == 409
    assert client.post(f"/api/cargas/{row['id']}/finalizar", json={'revision':unlocked['revision']}).status_code == 422
    assert client.get(f"/api/cargas/{row['id']}/emisiones/0/pdf").data == original
    saved = client.put(f"/api/cargas/{row['id']}/borrador", json={'revision':unlocked['revision'],
        'datos':unlocked['datos'], 'responsable':ejemplo_responsable(),
        'firmas':{role:firma_ficticia() for role in ('tecnico','responsable')}}).get_json()
    reissued = emitir(client,saved)
    assert reissued['numero_registro'] == 1 and reissued['revision_publica'] == 1
    history = client.get(f"/api/cargas/{row['id']}/emisiones").get_json()
    assert [r['revision_publica'] for r in history] == [0,1]
    assert client.get(history[0]['url']).data == original
    assert client.get(history[1]['url']).data != original
    with Session(app.extensions['db_engine']) as db:
        carga = db.get(Carga,row['id'])
        assert carga.pdf_hash == carga.pdf_sha256 == sha256(carga.pdf).hexdigest()
        assert carga.motivo_desbloqueo == '[Ejemplo] Corregir observación'
        assert db.get(NumeroRegistroContador,1).ultimo == 1
        from scripts.backup_readyproof import content_manifest
        manifest = content_manifest(db.connection())
        assert len([key for key in manifest['blobs'] if key.startswith('emisiones_carga/')]) == 2


@pytest.mark.parametrize('motivo', ['', '   ', None, 5, 'x'*1001, 'x\x00'])
def test_desbloqueo_exige_motivo_sin_cambiar_original(client,catalogo,datos_api,app,pdf_simulado,motivo):
    row = emitir(client,crear(client,catalogo,datos_api).get_json())
    result = client.post(f"/api/cargas/{row['id']}/desbloquear", json={'revision':row['revision'],'motivo':motivo})
    assert result.status_code == 422
    assert client.get(f"/api/cargas/{row['id']}").get_json()['estado'] == 'emitida'


def test_desbloqueo_borrador_y_revision_obsoleta_rechazados(client,catalogo,datos_api,pdf_simulado):
    row = crear(client,catalogo,datos_api).get_json()
    url=f"/api/cargas/{row['id']}/desbloquear"
    assert client.post(url,json={'revision':row['revision'],'motivo':'[Ejemplo] Motivo'}).status_code == 409
    row = emitir(client,row)
    assert client.post(url,json={'revision':1,'motivo':'[Ejemplo] Motivo'}).status_code == 409


def test_desbloqueo_solo_creador_admin_y_cliente_asignado(app,client,catalogo,datos_api,pdf_simulado):
    user,password=tecnico(client,catalogo)
    tech=login_cliente(app,user['login'],password)
    own=emitir(tech,crear(tech,catalogo,datos_api).get_json())
    admin=emitir(client,crear(client,catalogo,datos_api).get_json())
    assert tech.get(f"/api/cargas/{admin['id']}").get_json()['puede_desbloquear'] is False
    assert tech.post(f"/api/cargas/{admin['id']}/desbloquear",json={'revision':admin['revision'],'motivo':'[Ejemplo] Motivo'}).status_code == 403
    assert tech.post(f"/api/cargas/{own['id']}/desbloquear",json={'revision':own['revision'],'motivo':'[Ejemplo] Motivo'}).status_code == 200
    assert client.post(f"/api/cargas/{admin['id']}/desbloquear",json={'revision':admin['revision'],'motivo':'[Ejemplo] Motivo'}).status_code == 200
    assert app.test_client().get(f"/api/cargas/{admin['id']}/emisiones/1/pdf").status_code == 401
    assert client.put(f"/api/admin/usuarios/{user['id']}",json={'rol':'tecnico','activo':True,'cliente_ids':[]}).status_code == 200
    assert tech.get(f"/api/cargas/{own['id']}/emisiones").status_code == 401
    tech=login_cliente(app,user['login'],password)
    for suffix in ('/emisiones','/emisiones/1/pdf'):
        assert tech.get(f"/api/cargas/{own['id']}"+suffix).status_code == 404


def test_emision_fallida_no_consume_numero(client,catalogo,datos_api,app,monkeypatch):
    import app.rutas.api as api
    row=crear(client,catalogo,datos_api).get_json()
    row=client.post(f"/api/cargas/{row['id']}/finalizar",json={'revision':row['revision']}).get_json()
    def fail(*args):raise RuntimeError('Fallo deliberado de conversión')
    monkeypatch.setattr(api,'generar_pdf_carga',fail)
    assert client.post(f"/api/cargas/{row['id']}/emitir",json={'revision':row['revision']}).status_code == 503
    with Session(app.extensions['db_engine']) as db:
        assert db.get(NumeroRegistroContador,1).ultimo == 0
        assert db.get(Carga,row['id']).numero_registro is None
        assert list(db.scalars(select(EmisionCarga))) == []


def test_archivo_inmutable_en_base_y_original_legacy(client,catalogo,datos_api,app,pdf_simulado):
    row=crear(client,catalogo,datos_api).get_json()
    original=pdf_vacio()
    with Session(app.extensions['db_engine']) as db:
        carga=db.get(Carga,row['id']);carga.estado='emitida';carga.pdf=original;carga.pdf_sha256=sha256(original).hexdigest();db.commit()
    row=client.get(f"/api/cargas/{row['id']}").get_json()
    assert row['numero_registro'] is None and row['revision_publica'] == 0
    assert client.post(f"/api/cargas/{row['id']}/desbloquear",json={'revision':row['revision'],'motivo':'[Ejemplo] Histórico'}).status_code == 200
    assert client.get(f"/api/cargas/{row['id']}/emisiones/0/pdf").data == original
    for action in ('UPDATE emisiones_carga SET pdf=decode(\'00\',\'hex\')','DELETE FROM emisiones_carga'):
        with pytest.raises(DBAPIError,match='no se modifica'):
            with app.extensions['db_engine'].begin() as c:c.execute(text(action))


def test_contador_concurrente_y_rollback(app):
    def next_number(commit):
        with app.app_context():
            from app.db import sesion
            carga=Carga()
            preparar_numero_emision(carga)
            value=carga.numero_registro
            if commit:sesion().commit()
            else:sesion().rollback()
            return value
    assert next_number(False) == 1
    with ThreadPoolExecutor(max_workers=4) as pool:
        assert sorted(pool.map(next_number,[True]*8)) == list(range(1,9))
    assert next_number(False) == 9


def test_correo_nueva_revision_y_clave_anterior_rechazada(client,catalogo,datos_api,pdf_simulado,gmail):
    from uuid import uuid4
    key=str(uuid4())
    row=emitir(client,crear(client,catalogo,datos_api).get_json())
    assert solicitar(client,row['id'],key).status_code == 200
    unlocked=client.post(f"/api/cargas/{row['id']}/desbloquear",json={'revision':row['revision'],'motivo':'[Ejemplo] Corrección'}).get_json()
    saved=client.put(f"/api/cargas/{row['id']}/borrador",json={'revision':unlocked['revision'],'datos':unlocked['datos'],
        'firmas':{role:firma_ficticia() for role in ('tecnico','responsable')}}).get_json()
    revised=emitir(client,saved)
    assert solicitar(client,row['id'],key).status_code == 409
    response=solicitar(client,row['id'])
    assert response.status_code == 200
    assert response.get_json()['pdf_sha256'] == revised['pdf_sha256']
    assert len(gmail) == 2
    first=next(gmail[0].iter_attachments()).get_payload(decode=True)
    second=next(gmail[1].iter_attachments()).get_payload(decode=True)
    assert first != second
    assert solicitar(client,row['id']).status_code == 200 and len(gmail) == 2


@pytest.mark.parametrize('state',['✓','O','X','NA','SI','NO','o','N/A',True,1,[],None])
def test_sdi_grilla_mensual_cuatro_estados(state):
    schema=definiciones_multisistema()['SG-PEM-IFI-SDI-2']['definicion']
    data=ejemplo_multisistema(schema)
    title=next(iter(schema['bloques']));key=next(iter(schema['bloques'][title]))
    data['bloques'][title][key]=state
    if isinstance(state,str) and state in ('✓','O','X','NA'):
        assert validar_sdi_grilla_mensual(data,schema) == data
        validar_datos(data,schema,completo=True)
    else:
        with pytest.raises(DatosInvalidos):validar_datos(data,schema)
