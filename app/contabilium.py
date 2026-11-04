"""Consulta selectiva de clientes y padrón a través de la API de Contabilium."""
import json
import threading
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import HTTPRedirectHandler, Request, build_opener

from flask import Blueprint, abort, current_app, g, jsonify, request
from sqlalchemy import select

from .auth import exigir_admin
from .db import sesion
from .models import Cliente, ahora
from .modo import es_piloto
from .utils.cuit_validator import normalizar_cuit, validar_cuit

contabilium = Blueprint('contabilium', __name__, url_prefix='/api/admin/contabilium')


class ErrorContabilium(Exception):
    def __init__(self, mensaje, estado=502):
        self.estado = estado
        super().__init__(mensaje)


class SinRedireccion(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


class APIContabilium:
    BASE = 'https://rest.contabilium.com'

    def __init__(self, correo, clave):
        self.correo, self.clave = correo, clave
        self.token, self.vence, self.bloqueado_hasta = None, 0, 0
        self.lock = threading.Lock()

    def peticion(self, ruta, *, datos=None, token=None):
        if time.monotonic() < self.bloqueado_hasta:
            raise ErrorContabilium('Contabilium pidió esperar. Volvé a intentar en un minuto.', 429)
        headers = {'Accept': 'application/json', 'User-Agent': 'readyproof/1.1'}
        if token:
            headers['Authorization'] = 'Bearer ' + token
        if datos is not None:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        req = Request(self.BASE + ruta, data=urlencode(datos).encode() if datos else None, headers=headers)
        try:
            with build_opener(SinRedireccion()).open(req, timeout=15) as response:
                content = response.read(2_000_001)
            if len(content) > 2_000_000:
                raise ErrorContabilium('La respuesta de Contabilium supera el tamaño admitido.')
            return json.loads(content)
        except HTTPError as error:
            if error.code == 429:
                self.bloqueado_hasta = time.monotonic() + 60
                raise ErrorContabilium('Contabilium pidió esperar. Volvé a intentar en un minuto.', 429) from None
            if error.code in (401, 403) or (error.code == 400 and ruta == '/token'):
                self.token = None
                raise ErrorContabilium('Contabilium rechazó el acceso. Revisá las credenciales y el plan habilitado.', 503) from None
            if error.code == 404:
                raise ErrorContabilium('No se encontraron datos en Contabilium.', 404) from None
            raise ErrorContabilium('Contabilium no pudo completar la consulta.') from None
        except (URLError, TimeoutError, OSError, ValueError):
            raise ErrorContabilium('No se pudo consultar Contabilium. Los datos actuales se conservan.') from None

    def consultar(self, ruta):
        with self.lock:
            if not self.token or self.vence <= time.monotonic():
                result = self.peticion('/token', datos={'grant_type': 'client_credentials', 'client_id': self.correo, 'client_secret': self.clave})
                if not isinstance(result, dict) or not isinstance(result.get('access_token'), str) or not result['access_token']:
                    raise ErrorContabilium('Contabilium no devolvió un token válido.')
                self.token = result['access_token']
                try:
                    duration = max(0, int(result.get('expires_in', 0)) - 60)
                except (ValueError, TypeError):
                    duration = 0
                self.vence = time.monotonic() + duration
            token = self.token
        return self.peticion(ruta, token=token)

    def buscar(self, filtro):
        result = self.consultar('/api/clientes/search?' + urlencode({'pageSize': 0, 'filtro': filtro}))
        if not isinstance(result, dict) or not isinstance(result.get('Items'), list):
            raise ErrorContabilium('Contabilium devolvió un listado con formato no reconocido.')
        return [normalizar_cliente(row, externo=True) for row in result['Items'][:50]]

    def cliente(self, identificador):
        return normalizar_cliente(self.consultar('/api/clientes/?' + urlencode({'id': identificador})), externo=True)

    def buscar_por_cuit(self, cuit):
        if not validar_cuit(cuit):
            raise ErrorContabilium('Ingresá un CUIT válido de once dígitos.', 400)
        cuit = normalizar_cuit(cuit)
        result = self.consultar('/api/clientes/search?' + urlencode({'pageSize': 50, 'filtro': cuit}))
        if not isinstance(result, dict) or not isinstance(result.get('Items'), list):
            raise ErrorContabilium('Contabilium devolvió un listado con formato no reconocido.')
        coincidencias = []
        for row in result['Items']:
            if not isinstance(row, dict):
                raise ErrorContabilium('Contabilium devolvió un listado con formato no reconocido.')
            if str(row.get('TipoDoc', '')).strip().upper() == 'CUIT' and validar_cuit(row.get('NroDoc')):
                if normalizar_cuit(row['NroDoc']) == cuit:
                    coincidencias.append(row)
        if len(coincidencias) > 1:
            raise ErrorContabilium('Hay más de un cliente con ese CUIT en Contabilium. Revisá el duplicado en origen.', 409)
        # El filtro admite coincidencias parciales; un lote truncado no prueba ausencia ni unicidad.
        total = result.get('TotalItems', len(result['Items']))
        if isinstance(total, bool) or not str(total).isdigit() or int(total) > len(result['Items']):
            raise ErrorContabilium('La búsqueda devolvió resultados incompletos. No se completaron datos.')
        return normalizar_cliente(coincidencias[0], externo=True) if coincidencias else None

    def arca(self, cuit):
        result = self.consultar('/api/clientes/datosAfip?' + urlencode({'documento': cuit}))
        # La documentación no publica un ejemplo de respuesta del padrón.
        # Se aceptan solo los campos documentados de cliente; otro formato se informa.
        row = normalizar_cliente(result, externo=False)
        if row['cuit'] != cuit:
            raise ErrorContabilium('El padrón no devolvió el CUIT consultado. No se completaron datos.')
        return row


def normalizar_cliente(data, *, externo):
    if not isinstance(data, dict):
        raise ErrorContabilium('Contabilium devolvió datos con formato no reconocido.')
    nombre = data.get('RazonSocial')
    if not isinstance(nombre, str) or not nombre.strip() or len(nombre.strip()) > 200:
        raise ErrorContabilium('Contabilium no devolvió una razón social válida. No se completaron datos.')
    raw_id = data.get('Id')
    if externo and (isinstance(raw_id, bool) or len(str(raw_id)) > 20 or not str(raw_id).isascii() or not str(raw_id).isdigit() or int(raw_id) <= 0):
        raise ErrorContabilium('Contabilium no devolvió un identificador válido.')
    cuit = None
    if str(data.get('TipoDoc', '')).upper() in ('CUIT', 'CUIL'):
        raw = data.get('NroDoc')
        if not validar_cuit(raw):
            raise ErrorContabilium('El CUIT informado por Contabilium no es válido. Revisalo en origen.')
        cuit = normalizar_cuit(raw)
    contacto = {}
    for destino, origen, maximo in (('direccion', 'Domicilio', 500), ('telefono', 'Telefono', 120), ('email', 'Email', 500)):
        value = data.get(origen)
        if value is not None and (not isinstance(value, str) or len(value.strip()) > maximo):
            raise ErrorContabilium('Contabilium devolvió datos de contacto con formato no reconocido.')
        if value and value.strip():
            contacto[destino] = value.strip()
    return {'contabilium_id': str(int(raw_id)) if externo else None, 'nombre': nombre.strip(), 'cuit': cuit, 'contacto': contacto}


def servicio():
    exigir_admin()
    if es_piloto():
        abort(403, description='La consulta de datos reales de Contabilium requiere modo REAL.')
    correo = current_app.config.get('CONTABILIUM_CLIENT_ID', '')
    clave = current_app.config.get('CONTABILIUM_CLIENT_SECRET', '')
    if not correo or not clave:
        raise ErrorContabilium('Falta configurar el correo API y la API Key de Contabilium en el servidor.', 503)
    if 'contabilium_api' not in current_app.extensions:
        current_app.extensions['contabilium_api'] = APIContabilium(correo, clave)
    return current_app.extensions['contabilium_api']


@contabilium.errorhandler(ErrorContabilium)
def error_contabilium(error):
    return jsonify(error=str(error)), error.estado


@contabilium.get('/clientes')
def buscar():
    api = servicio()
    filtro = request.args.get('buscar', '').strip()
    if not 3 <= len(filtro) <= 200:
        abort(400, description='Ingresá al menos tres caracteres del nombre o CUIT.')
    return jsonify(clientes=api.buscar(filtro))


@contabilium.get('/cliente-por-cuit')
def buscar_por_cuit():
    api = servicio()
    cuit = request.args.get('cuit', '').strip()
    if not validar_cuit(cuit):
        abort(400, description='Ingresá un CUIT válido de once dígitos.')
    cliente = api.buscar_por_cuit(normalizar_cuit(cuit))
    return jsonify(encontrado=cliente is not None, cliente=cliente)


@contabilium.get('/arca')
def consultar_arca():
    api = servicio()
    cuit = request.args.get('cuit', '').strip()
    if not validar_cuit(cuit):
        abort(400, description='Ingresá un CUIT válido de once dígitos.')
    return jsonify(api.arca(normalizar_cuit(cuit)))


@contabilium.post('/sincronizar')
def sincronizar():
    api = servicio()
    data = request.get_json(silent=True)
    externo = data.get('contabilium_id') if isinstance(data, dict) else None
    if not isinstance(externo, str) or not externo.isascii() or not externo.isdigit() or len(externo) > 20 or int(externo) <= 0:
        abort(400, description='Seleccioná un cliente de Contabilium.')
    row = api.cliente(externo)
    if row['contabilium_id'] != str(int(externo)):
        raise ErrorContabilium('Contabilium devolvió otro cliente. No se guardaron cambios.')
    db = sesion()
    cliente = db.scalar(select(Cliente).where(Cliente.contabilium_id == row['contabilium_id']).with_for_update())
    if not cliente and row['cuit']:
        cliente = db.scalar(select(Cliente).where(Cliente.cuit == row['cuit']).with_for_update())
        if cliente and cliente.contabilium_id and cliente.contabilium_id != row['contabilium_id']:
            abort(409, description='El CUIT ya está vinculado a otro cliente de Contabilium.')
    if not cliente:
        cliente = Cliente(es_ejemplo=False)
        db.add(cliente)
    elif cliente.es_ejemplo:
        abort(409, description='Los clientes del piloto se conservan. Revisá el CUIT antes de vincular.')
    cliente.nombre, cliente.cuit = row['nombre'], row['cuit'] or cliente.cuit
    cliente.contacto = {**(cliente.contacto or {}), **row['contacto']}
    cliente.contabilium_id, cliente.sincronizado_en = row['contabilium_id'], ahora()
    db.flush()
    g.evento_auth = 'cliente_sincronizado_contabilium'
    return jsonify(id=cliente.id, **row, sincronizado_en=cliente.sincronizado_en.isoformat())
