"""Persistencia de JPEG recibidos del canvas, sin guardar originales."""
from hashlib import sha256
from io import BytesIO
from uuid import UUID

from flask import Blueprint, abort, g, jsonify, request
from PIL import Image, UnidentifiedImageError
from sqlalchemy import select

from . import MAX_FOTO_BYTES
from ..carga.servicios import registrar_auditoria
from ..db import sesion
from ..models import Carga, FotoCarga
from ..models.fotos import MAX_FOTOS_POR_CARGA
from ..rutas.api import obtener

fotos_api = Blueprint('fotos', __name__, url_prefix='/api/cargas')
FORMATO = 'Formato no soportado: se acepta JPEG. Vuelva a elegir la foto desde la app.'
TAMANO = 'La foto supera 2 MB: vuelva a intentar con la foto de la app'


def metadata(foto):
    return dict(id=foto.id, orden=foto.orden, ancho=foto.ancho, alto=foto.alto,
                sha256=foto.sha256, bytes=len(foto.imagen))


def validar_jpeg(data):
    if not data.startswith(b'\xff\xd8\xff'):
        abort(400, description=FORMATO)
    try:
        with Image.open(BytesIO(data)) as image:
            if image.format != 'JPEG':
                abort(400, description=FORMATO)
            width, height = image.size
            image.verify()
        if not data.endswith(b'\xff\xd9'):
            raise ValueError('JPEG incompleto')
    except (UnidentifiedImageError, OSError, ValueError, Image.DecompressionBombError):
        abort(400, description=FORMATO)
    if min(width, height) < 1 or max(width, height) > 1600:
        abort(400, description='La foto debe tener hasta 1600 px de lado mayor: vuelva a elegirla desde la app.')
    return width, height


@fotos_api.get('/<carga_id>/fotos')
def listar(carga_id):
    obtener(Carga, carga_id)
    rows = sesion().scalars(select(FotoCarga).where(FotoCarga.carga_id == carga_id).order_by(FotoCarga.orden))
    return jsonify([metadata(row) for row in rows])


@fotos_api.post('/<carga_id>/fotos')
def subir(carga_id):
    obtener(Carga, carga_id)
    db = sesion()
    carga = db.scalar(select(Carga).where(Carga.id == carga_id).with_for_update().execution_options(populate_existing=True))
    if carga.estado != 'borrador':
        abort(409, description='La planilla ya está finalizada o emitida: solicite su desbloqueo antes de agregar fotos.')
    if request.content_length is not None and request.content_length > MAX_FOTO_BYTES:
        abort(413, description=TAMANO)
    data = request.stream.read(MAX_FOTO_BYTES + 1)
    if len(data) > MAX_FOTO_BYTES:
        abort(413, description=TAMANO)
    width, height = validar_jpeg(data)
    digest = sha256(data).hexdigest()
    key = request.headers.get('Idempotency-Key')
    if key:
        try:
            key = str(UUID(key))
        except ValueError:
            abort(400, description='Identificador de foto inválido: vuelva a elegir la foto desde la app.')
        previous = db.get(FotoCarga, key)
        if previous:
            if previous.carga_id != carga_id or previous.sha256 != digest:
                abort(409, description='El identificador ya corresponde a otra foto: vuelva a elegirla desde la app.')
            return jsonify(metadata(previous)), 200
    orders = list(db.scalars(select(FotoCarga.orden).where(FotoCarga.carga_id == carga_id).order_by(FotoCarga.orden)))
    if len(orders) >= MAX_FOTOS_POR_CARGA:
        abort(409, description='La planilla ya tiene 20 fotos: no se pueden agregar más.')
    if orders != list(range(1, len(orders) + 1)):
        abort(409, description='El orden de las fotos requiere revisión: contacte a administración.')
    values = dict(carga_id=carga_id, orden=len(orders) + 1, imagen=data, ancho=width, alto=height,
                  sha256=digest, creado_por_id=g.usuario.id)
    if key:
        values['id'] = key
    foto = FotoCarga(**values)
    db.add(foto)
    db.flush()
    result = metadata(foto)
    registrar_auditoria('foto_carga', foto.id, 'INSERT', g.usuario.id, None, dict(result, carga_id=carga_id))
    db.commit()
    return jsonify(result), 201
