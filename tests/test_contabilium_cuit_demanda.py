"""Alta a demanda con datos ficticios y transporte externo bloqueado."""
import json
import os
from pathlib import Path
import shutil
import subprocess
from urllib.parse import parse_qs, urlsplit

import pytest
from sqlalchemy import func, select
from app.contabilium import APIContabilium, ErrorContabilium
from app.db import sesion
from app.models import Cliente


def externo(**cambios):
    return dict(Id=101, RazonSocial='[Ejemplo] Cliente', TipoDoc='CUIT', NroDoc='20-00000000-1',
                Email='contacto@example.invalid', Telefono='0000', Domicilio='[Ejemplo] Calle', **cambios)


@pytest.fixture(autouse=True)
def bloquear_red(monkeypatch):
    def prohibido(*args, **kwargs):
        raise AssertionError('Sin acceso a Contabilium real.')
    monkeypatch.setattr('app.contabilium.build_opener', prohibido)


def test_filtro_documentado_y_coincidencia_exacta(monkeypatch):
    api = APIContabilium('[Ejemplo]', '[Ejemplo]')
    llamadas = []
    def consultar(ruta):
        llamadas.append(ruta)
        return {'Items': [externo(), {**externo(), 'Id': 102, 'NroDoc': '27-00000000-6'}], 'TotalItems': 2}
    monkeypatch.setattr(api, 'consultar', consultar)
    row = api.buscar_por_cuit('20-00000000-1')
    assert row['cuit'] == '20000000001'
    assert row['contacto']['email'] == 'contacto@example.invalid'
    assert len(llamadas) == 1
    assert urlsplit(llamadas[0]).path == '/api/clientes/search'
    assert parse_qs(urlsplit(llamadas[0]).query) == {'filtro': ['20000000001'], 'pageSize': ['50']}


@pytest.mark.parametrize('items', [[], [{**externo(), 'TipoDoc': 'DNI'}], [{**externo(), 'NroDoc': '27-00000000-6'}]])
def test_no_encontrado_no_confunde_documentos(monkeypatch, items):
    api = APIContabilium('[Ejemplo]', '[Ejemplo]')
    monkeypatch.setattr(api, 'consultar', lambda ruta: {'Items': items})
    assert api.buscar_por_cuit('20000000001') is None


def test_cuit_invalido_no_consulta(monkeypatch):
    api = APIContabilium('[Ejemplo]', '[Ejemplo]')
    monkeypatch.setattr(api, 'consultar', lambda ruta: pytest.fail('No debe consultar'))
    with pytest.raises(ErrorContabilium) as error:
        api.buscar_por_cuit('82000000000')
    assert error.value.estado == 400


@pytest.mark.parametrize('result', [{'Items': [externo(), externo()]}, {'Items': [], 'TotalItems': 60}, {'Items': [externo()], 'TotalItems': 51}, {'sin_items': []}])
def test_duplicados_incompletos_y_formato_no_completan(monkeypatch, result):
    api = APIContabilium('[Ejemplo]', '[Ejemplo]')
    monkeypatch.setattr(api, 'consultar', lambda ruta: result)
    with pytest.raises(ErrorContabilium):
        api.buscar_por_cuit('20000000001')


def configurar(app, monkeypatch, resultado):
    app.config.update(MODO_PILOTO=False, CONTABILIUM_CLIENT_ID='[Ejemplo]', CONTABILIUM_CLIENT_SECRET='[Ejemplo]')
    api = APIContabilium('[Ejemplo]', '[Ejemplo]')
    monkeypatch.setattr(api, 'consultar', lambda ruta: resultado)
    app.extensions['contabilium_api'] = api
    return api


@pytest.mark.parametrize('encontrado', [True, False])
def test_consulta_no_guarda_ficha(app, client, monkeypatch, encontrado):
    configurar(app, monkeypatch, {'Items': [externo()] if encontrado else []})
    with app.app_context():
        antes = sesion().scalar(select(func.count()).select_from(Cliente))
    response = client.get('/api/admin/contabilium/cliente-por-cuit?cuit=20-00000000-1')
    assert response.status_code == 200
    assert response.json['encontrado'] is encontrado
    with app.app_context():
        assert sesion().scalar(select(func.count()).select_from(Cliente)) == antes


def test_error_api_y_cuit_invalido(app, client, monkeypatch):
    api = configurar(app, monkeypatch, {})
    llamadas = []
    def fallo(ruta):
        llamadas.append(ruta)
        raise ErrorContabilium('No se pudo consultar Contabilium.', 502)
    monkeypatch.setattr(api, 'consultar', fallo)
    assert client.get('/api/admin/contabilium/cliente-por-cuit?cuit=82000000000').status_code == 400
    assert llamadas == []
    response = client.get('/api/admin/contabilium/cliente-por-cuit?cuit=20000000001')
    assert response.status_code == 502 and len(llamadas) == 1


def test_permisos(app, client):
    assert client.get('/api/admin/contabilium/cliente-por-cuit?cuit=20000000001').status_code == 403
    assert app.test_client().get('/api/admin/contabilium/cliente-por-cuit?cuit=20000000001').status_code == 401


def test_alta_navegador_con_mock(app, client, tmp_path):
    app.config['MODO_PILOTO'] = False
    html = tmp_path / 'admin.html'
    html.write_text(client.get('/admin').get_data(as_text=True), encoding='utf8')
    node = os.environ.get('READYPROOF_NODE') or shutil.which('node')
    assert node, 'Se requiere Node y Playwright.'
    result = subprocess.run([node, 'tests/browser/contabilium_cuit_demanda.cjs', str(html),
                             str(Path('app/static/admin.js').resolve())], capture_output=True, text=True, timeout=90)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)['sin_guardado_automatico']
