"""Contrato de integración con respuestas sintéticas; nunca consulta cuentas reales."""
import json
from urllib.error import HTTPError
import pytest
from sqlalchemy import select, text

from app.contabilium import APIContabilium, ErrorContabilium, normalizar_cliente
from app.models import Cliente
from app.db import sesion


def externo(**cambios):
    return {'Id': 101, 'RazonSocial': '[Ejemplo] Cliente externo', 'TipoDoc': 'CUIT', 'NroDoc': '20-00000000-1',
            'Domicilio': '[Ejemplo] Domicilio', 'Telefono': '[Ejemplo] Sin dato', 'Email': 'contacto@example.invalid', **cambios}


def test_normalizacion_contabilium():
    row = normalizar_cliente(externo(), externo=True)
    assert row['cuit'] == '20000000001'
    assert row['contabilium_id'] == '101'
    assert row['contacto']['email'] == 'contacto@example.invalid'


@pytest.mark.parametrize('cambios', [{'NroDoc': '82000000000'}, {'Id': None}, {'Id': True}, {'RazonSocial': ''}, {'Domicilio': []}])
def test_respuesta_invalida_no_importa(cambios):
    with pytest.raises(ErrorContabilium):
        normalizar_cliente(externo(**cambios), externo=True)


def test_dni_no_se_guarda_como_cuit():
    assert normalizar_cliente(externo(TipoDoc='DNI', NroDoc='00000000'), externo=True)['cuit'] is None


def test_token_se_reutiliza_y_consulta_solo_lectura(monkeypatch):
    api = APIContabilium('[Ejemplo] correo', '[Ejemplo] clave')
    llamadas = []
    def fake(ruta, **kwargs):
        llamadas.append((ruta, kwargs))
        if ruta == '/token':
            return {'access_token': '[Ejemplo] token', 'expires_in': 3600}
        return {'Items': [externo()]}
    monkeypatch.setattr(api, 'peticion', fake)
    assert api.buscar('[Ejemplo]')[0]['nombre'].startswith('[Ejemplo]')
    api.buscar('20000000001')
    assert sum(ruta == '/token' for ruta, _ in llamadas) == 1
    assert all(ruta == '/token' or ruta.startswith('/api/clientes/search?') for ruta, _ in llamadas)


def test_arca_valida_cuit_y_rechaza_formato_desconocido(monkeypatch):
    api = APIContabilium('ejemplo', 'ejemplo')
    monkeypatch.setattr(api, 'consultar', lambda ruta: externo())
    assert api.arca('20000000001')['cuit'] == '20000000001'
    with pytest.raises(ErrorContabilium, match='CUIT consultado'):
        api.arca('27000000006')
    monkeypatch.setattr(api, 'consultar', lambda ruta: {'respuesta_no_documentada': True})
    with pytest.raises(ErrorContabilium):
        api.arca('20000000001')


@pytest.mark.parametrize('estado', [400, 401, 403])
def test_error_http_no_expone_credenciales(monkeypatch, estado):
    class Opener:
        def open(self, req, timeout):
            assert req.get_header('User-agent') == 'readyproof/1.1'
            raise HTTPError(req.full_url, estado, '[Ejemplo] secreto', {}, None)
    monkeypatch.setattr('app.contabilium.build_opener', lambda *args: Opener())
    with pytest.raises(ErrorContabilium) as caught:
        APIContabilium('ejemplo', '[Ejemplo] secreto').peticion('/token', datos={'client_secret': '[Ejemplo] secreto'})
    assert 'secreto' not in str(caught.value)


def test_limite_429_no_reintenta(monkeypatch):
    llamadas = []
    class Opener:
        def open(self, req, timeout):
            llamadas.append(req.full_url)
            raise HTTPError(req.full_url, 429, 'esperar', {}, None)
    monkeypatch.setattr('app.contabilium.build_opener', lambda *args: Opener())
    api = APIContabilium('ejemplo', 'ejemplo')
    for _ in range(2):
        with pytest.raises(ErrorContabilium) as caught:
            api.peticion('/api/clientes/search?filtro=ejemplo')
        assert caught.value.estado == 429
    assert len(llamadas) == 1


def configurar(app, monkeypatch):
    app.config.update(MODO_PILOTO=False, CONTABILIUM_CLIENT_ID='[Ejemplo] correo', CONTABILIUM_CLIENT_SECRET='[Ejemplo] clave')
    api = APIContabilium('ejemplo', 'ejemplo')
    monkeypatch.setattr(api, 'cliente', lambda identificador: normalizar_cliente(externo(), externo=True))
    monkeypatch.setattr(api, 'buscar', lambda filtro: [normalizar_cliente(externo(), externo=True)])
    monkeypatch.setattr(api, 'arca', lambda cuit: normalizar_cliente(externo(), externo=False))
    app.extensions['contabilium_api'] = api
    return api


def test_permisos_y_configuracion(app, client):
    assert client.get('/api/admin/contabilium/clientes?buscar=ejemplo').status_code == 403
    app.config.update(MODO_PILOTO=False, CONTABILIUM_CLIENT_ID='', CONTABILIUM_CLIENT_SECRET='')
    assert client.get('/api/admin/contabilium/clientes?buscar=ejemplo').status_code == 503
    assert app.test_client().get('/api/admin/contabilium/clientes?buscar=ejemplo').status_code == 401


def test_busqueda_arca_y_parametros(app, client, monkeypatch):
    configurar(app, monkeypatch)
    assert client.get('/api/admin/contabilium/clientes?buscar=ab').status_code == 400
    assert client.get('/api/admin/contabilium/clientes?buscar=ejemplo').get_json()['clientes'][0]['cuit'] == '20000000001'
    assert client.get('/api/admin/contabilium/arca?cuit=82000000000').status_code == 400
    assert client.get('/api/admin/contabilium/arca?cuit=20-00000000-1').get_json()['nombre'].startswith('[Ejemplo]')


def test_sincronizar_es_idempotente_y_no_toca_cargas(app, client, monkeypatch):
    configurar(app, monkeypatch)
    with app.app_context():
        antes = sesion().scalar(text('SELECT count(*) FROM cargas'))
    first = client.post('/api/admin/contabilium/sincronizar', json={'contabilium_id': '101'})
    assert first.status_code == 200
    second = client.post('/api/admin/contabilium/sincronizar', json={'contabilium_id': '101'})
    assert second.status_code == 200 and second.get_json()['id'] == first.get_json()['id']
    with app.app_context():
        row = sesion().scalar(select(Cliente).where(Cliente.contabilium_id == '101'))
        assert row.cuit == '20000000001' and row.contacto['email'] == 'contacto@example.invalid'
        assert row.sincronizado_en is not None and not row.es_ejemplo
        assert sesion().scalar(text('SELECT count(*) FROM cargas')) == antes


def test_sincronizar_vincula_cuit_existente(app, client, monkeypatch):
    configurar(app, monkeypatch)
    with app.app_context():
        row = Cliente(nombre='[Ejemplo] Ficha anterior', cuit='20000000001', es_ejemplo=False)
        sesion().add(row);sesion().commit();identificador = row.id
    assert client.post('/api/admin/contabilium/sincronizar', json={'contabilium_id': '101'}).get_json()['id'] == identificador


def test_sincronizar_no_transforma_cliente_piloto(app, client, monkeypatch):
    configurar(app, monkeypatch)
    with app.app_context():
        sesion().add(Cliente(nombre='[Ejemplo] Piloto', cuit='20000000001', es_ejemplo=True));sesion().commit()
    assert client.post('/api/admin/contabilium/sincronizar', json={'contabilium_id': '101'}).status_code == 409


def test_sincronizar_reconsulta_id_y_no_confia_datos_navegador(app, client, monkeypatch):
    configurar(app, monkeypatch)
    assert client.post('/api/admin/contabilium/sincronizar', json={'contabilium_id': '../otro'}).status_code == 400
    assert client.post('/api/admin/contabilium/sincronizar', json={'contabilium_id': '102'}).status_code == 502


def test_tecnico_no_consulta_contabilium(app, client, usuario_admin, monkeypatch):
    from app.models import Usuario
    configurar(app, monkeypatch)
    with app.app_context():
        sesion().get(Usuario, usuario_admin['id']).rol = 'tecnico'
        sesion().commit()
    assert client.get('/api/admin/contabilium/clientes?buscar=ejemplo').status_code == 403
