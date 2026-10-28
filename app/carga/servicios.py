"""Desbloqueo y numeración dentro de la misma transacción de la carga."""
from copy import deepcopy
from hashlib import sha256

from flask import abort
from sqlalchemy import select

from ..db import sesion
from ..models import Carga, Usuario, EmisionCarga, NumeroRegistroContador, FirmaCarga
from ..planillas.validacion import DatosInvalidos


def archivar_emision(carga, firmantes):
    if not carga.pdf:
        abort(409, description='No existe el PDF original que debe conservarse.')
    digest = sha256(carga.pdf).hexdigest()
    if carga.pdf_sha256 != digest or (carga.pdf_hash and carga.pdf_hash != digest):
        abort(409, description='La integridad del PDF original requiere revisión.')
    with sesion().no_autoflush:
        existing = sesion().scalar(select(EmisionCarga).where(
            EmisionCarga.carga_id == carga.id, EmisionCarga.revision_publica == carga.revision_publica))
    if existing:
        if existing.pdf != carga.pdf or existing.pdf_sha256 != digest:
            abort(409, description='La revisión pública ya tiene un PDF diferente.')
        return existing
    row = EmisionCarga(carga_id=carga.id, numero_registro=carga.numero_registro,
        revision_publica=carga.revision_publica, pdf=carga.pdf, pdf_sha256=digest,
        datos=deepcopy(carga.datos), firmantes=deepcopy(firmantes),
        actor_id=firmantes.get('tecnico', {}).get('usuario_id') or carga.creada_por_id,
        emitida_en=carga.emitida_en)
    sesion().add(row)
    return row


def preparar_numero_emision(carga):
    """El bloqueo se mantiene hasta commit; un rollback no consume números."""
    if carga.numero_registro is None:
        contador = sesion().scalar(select(NumeroRegistroContador).where(
            NumeroRegistroContador.id == 1).with_for_update())
        if contador is None:
            raise RuntimeError('Falta inicializar el contador de emisiones mediante la migración.')
        contador.ultimo += 1
        carga.numero_registro = contador.ultimo


def desbloquear_carga(carga_id, usuario_id, motivo, *, firmantes, revision):
    db = sesion()
    carga = db.scalar(select(Carga).where(Carga.id == carga_id).with_for_update().execution_options(populate_existing=True))
    usuario = db.get(Usuario, usuario_id)
    if carga is None:
        abort(404)
    if usuario is None or not usuario.activo or (usuario.rol != 'admin' and carga.creada_por_id != usuario_id):
        abort(403, description='Solo el creador o un administrador puede desbloquear esta carga.')
    if isinstance(revision, bool) or not isinstance(revision, int):
        raise DatosInvalidos('revision debe ser un entero JSON.')
    if carga.revision != revision:
        abort(409, description='La carga cambió; consultá la revisión actual.')
    if carga.estado != 'emitida' or carga.estado_anulada:
        abort(409, description='Solo se desbloquean cargas emitidas y vigentes.')
    if not isinstance(motivo, str) or not motivo.strip() or len(motivo) > 1000 or any(ord(c) < 32 and c not in '\n\r\t' for c in motivo):
        raise DatosInvalidos('Indicá un motivo de desbloqueo de hasta 1000 caracteres.')
    archivar_emision(carga, firmantes)
    carga.estado = 'borrador'
    carga.desbloqueado_por = usuario_id
    carga.motivo_desbloqueo = motivo.strip()
    carga.revision_publica += 1
    carga.pdf = None
    carga.pdf_sha256 = None
    carga.pdf_hash = None
    carga.finalizada_en = None
    carga.emitida_en = None
    # La nueva revisión debe ser firmada de nuevo; el original conserva sus firmas en el PDF.
    firmas = db.get(FirmaCarga, carga.id)
    if firmas:
        firmas.tecnico_png = firmas.responsable_png = None
        firmas.tecnico_usuario_id = firmas.tecnico_nombre = firmas.tecnico_login = None
    return carga
