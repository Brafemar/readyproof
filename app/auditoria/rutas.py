"""Auditoría administrativa paginada, con filtros validados."""
import re
from uuid import UUID
from flask import Blueprint, jsonify, request
from sqlalchemy import func, select
from ..auth import exigir_admin
from ..db import sesion
from ..models import Auditoria, Usuario
from ..planillas.validacion import DatosInvalidos

auditoria_api = Blueprint('auditoria', __name__, url_prefix='/api')


@auditoria_api.get('/auditoria')
def listar_auditoria():
    exigir_admin()
    filters = []
    for key in request.args:
        if key not in ('tabla', 'registro_id', 'accion', 'usuario_id', 'limit', 'offset') or len(request.args.getlist(key)) != 1:
            raise DatosInvalidos('Filtro de auditoría desconocido o repetido.')
    for key in ('tabla', 'registro_id', 'accion', 'usuario_id'):
        value = request.args.get(key)
        if value is None:
            continue
        if key in ('registro_id', 'usuario_id'):
            try:
                if str(UUID(value)) != value:raise ValueError()
            except ValueError:raise DatosInvalidos(key+' debe ser un UUID válido.') from None
        elif key == 'tabla' and not re.fullmatch(r'[a-z][a-z0-9_]{0,49}', value):
            raise DatosInvalidos('tabla no es válida.')
        elif key == 'accion' and value not in ('INSERT', 'UPDATE', 'DELETE', 'DESBLOQUEO'):
            raise DatosInvalidos('accion no es válida.')
        filters.append(getattr(Auditoria, key) == value)
    pagination = {}
    for key, default, maximum in (('limit', '100', 500), ('offset', '0', 2147483647)):
        value = request.args.get(key, default)
        if not re.fullmatch(r'[0-9]{1,10}', value) or int(value) > maximum or (key == 'limit' and int(value) == 0):
            raise DatosInvalidos(key+' fuera del rango admitido.')
        pagination[key] = int(value)
    db = sesion()
    total = db.scalar(select(func.count()).select_from(Auditoria).where(*filters))
    rows = db.execute(select(Auditoria, Usuario.nombre).join(Usuario, Auditoria.usuario_id == Usuario.id)
        .where(*filters).order_by(Auditoria.timestamp.desc(), Auditoria.id.desc())
        .limit(pagination['limit']).offset(pagination['offset'])).all()
    return jsonify(total=total, registros=[dict(id=row.id, tabla=row.tabla, registro_id=row.registro_id,
        accion=row.accion, usuario=nombre, usuario_id=row.usuario_id, timestamp=row.timestamp.isoformat(),
        datos_anterior=row.datos_anterior, datos_nuevo=row.datos_nuevo) for row,nombre in rows])
