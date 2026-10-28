"""Consulta de registros con el mismo aislamiento por cliente que las cargas."""
import re
from flask import Blueprint, abort, g, jsonify, request
from sqlalchemy import select
from ..auth import autorizar_cliente
from ..db import sesion
from ..models import Carga, Cliente, Planilla, Sistema

carga_api = Blueprint('carga_consulta', __name__, url_prefix='/api/carga')


@carga_api.get('/buscar')
def buscar_carga():
    value = request.args.get('numero', '').strip()
    if not value:
        return jsonify(error='numero requerido'), 400
    if len(request.args.getlist('numero')) != 1 or not re.fullmatch(r'[0-9]{1,10}', value) or int(value) > 2147483647:
        return jsonify(error='numero debe ser entero entre 0 y 2147483647'), 400
    row = sesion().execute(select(Carga, Sistema, Cliente, Planilla)
        .join(Sistema, Carga.sistema_id == Sistema.id).join(Cliente, Sistema.cliente_id == Cliente.id)
        .join(Planilla, Carga.planilla_id == Planilla.id).where(Carga.numero_registro == int(value))).one_or_none()
    if row is None:
        abort(404, description='Registro inexistente.')
    carga, sistema, cliente, planilla = row
    autorizar_cliente(cliente.id)
    g.acceso_carga_id = carga.id
    return jsonify(numero_registro=carga.numero_registro, cliente=cliente.nombre, sistema=sistema.tipo,
        planilla=planilla.codigo, estado=carga.estado, revision_publica=carga.revision_publica,
        fecha_emision=carga.emitida_en.isoformat() if carga.emitida_en else None,
        pdf_hash=carga.pdf_hash, desbloqueado_por=carga.desbloqueado_por)
