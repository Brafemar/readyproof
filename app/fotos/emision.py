"""Incorpora a la emisión las fotos y referencias persistidas de la carga."""
from hashlib import sha256

from sqlalchemy import select

from .anexo_pdf import generar_anexo, unir_pdf
from ..models.fotos import FotoCarga, FotoAnotacion, FotoAnotacionItem


def incorporar_fotos_carga(planilla_pdf, carga, datos, db):
    """Sin fotos conserva los bytes; con fotos agrega anexos antes del hash."""
    fotos = list(db.scalars(select(FotoCarga).where(
        FotoCarga.carga_id == carga.id).order_by(FotoCarga.orden)))
    if not fotos:
        return planilla_pdf
    payload = planilla_pdf
    for foto in fotos:
        jpeg = bytes(foto.imagen)
        if sha256(jpeg).hexdigest() != foto.sha256:
            raise RuntimeError(f"La integridad de la foto {foto.orden} requiere revisión; no se emitió el PDF.")
        referencias = []
        rows = db.execute(select(FotoAnotacion, FotoAnotacionItem).outerjoin(
            FotoAnotacionItem, FotoAnotacionItem.anotacion_id == FotoAnotacion.id).where(
            FotoAnotacion.foto_id == foto.id).order_by(FotoAnotacion.numero))
        for marca, item in rows:
            referencia = dict(numero=marca.numero, x=marca.x, y=marca.y,
                              codigo=marca.codigo, texto=marca.texto)
            if item is not None:
                referencia['item'] = dict(bloque=item.bloque, campo=item.campo, texto=item.texto)
            referencias.append(referencia)
        try:
            anexo = generar_anexo(jpeg, referencias, referencias, carga=datos,
                                 permitir_sin_marcas=True)
            payload = unir_pdf(payload, anexo)
        except ValueError as error:
            raise RuntimeError(f"No se pudo generar el anexo de la foto {foto.orden}: {error}") from error
    return payload
