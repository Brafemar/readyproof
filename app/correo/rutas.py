"""Solicitud autenticada: cola y envío manual del PDF por Gmail HTTPS."""
from flask import Blueprint, abort, current_app, g, jsonify, request
from hashlib import sha256
from uuid import UUID
from sqlalchemy import select, text
from ..db import sesion
from ..models import Carga, Envio, Planilla
from ..rutas.api import obtener, objeto
from ..planillas.validacion import DatosInvalidos
from . import preparar_envio, send_email, direccion, resolver_destinatario
from ..modo import es_piloto

correo_api=Blueprint("correo_api",__name__,url_prefix="/api")


@correo_api.post("/cargas/<uuid:carga_id>/enviar")
def enviar(carga_id):
    carga=obtener(Carga,str(carga_id))
    if carga.estado!="emitida":abort(409,description="Solo se puede enviar una carga emitida.")
    data=objeto({"destinatario"},{"asunto","cuerpo","inmediato"})
    if "inmediato" in data and not isinstance(data["inmediato"],bool):
        raise DatosInvalidos("inmediato debe ser verdadero o falso.")
    if data.get("inmediato"):
        return enviar_inmediato(carga,data)
    try:
        envio=preparar_envio(sesion(),carga,data["destinatario"],g.usuario.id,
            data.get("asunto","[Ejemplo] Planilla readyproof"),data.get("cuerpo","[Ejemplo] Se adjunta la planilla PDF emitida."))
        send_email(sesion(),envio,encolar=True)
    except ValueError as error:
        sesion().rollback();raise DatosInvalidos(str(error)) from None
    return jsonify(id=envio.id,carga_id=envio.carga_id,estado=envio.estado,modo_prueba=current_app.config["MAIL_MODO_PRUEBA"]),202


def destinatarios_prueba():
    values=[value.strip() for value in current_app.config["PLANILLAS_DESTINATARIOS_PRUEBA"].split(",") if value.strip()]
    if current_app.config.get('DESTINATARIO_PRUEBA'):values.append(current_app.config['DESTINATARIO_PRUEBA'])
    return list(dict.fromkeys(values))


@correo_api.get("/correo/configuracion")
def configuracion_correo():
    allowed=destinatarios_prueba()
    return jsonify(habilitado=current_app.config["PLANILLAS_TRANSPORTE"]=="gmail_api" and (not es_piloto() or bool(allowed)),
                   destinatarios=allowed if es_piloto() else [], modo_piloto=es_piloto(),modo_prueba=current_app.config['MAIL_MODO_PRUEBA'])


def resumen(envio):
    return dict(id=envio.id,carga_id=envio.carga_id,destinatario=envio.destinatario,estado=envio.estado,
                pdf_sha256=envio.pdf_sha256,
                enviado_en=envio.enviado_en.isoformat() if envio.enviado_en else None)


@correo_api.get("/cargas/<uuid:carga_id>/envios")
def consultar_envios(carga_id):
    carga=obtener(Carga,str(carga_id))
    rows=sesion().scalars(select(Envio).where(Envio.carga_id==carga.id).order_by(Envio.creado_en.desc())).all()
    return jsonify([resumen(row) for row in rows])


def enviar_inmediato(carga,data):
    if current_app.config["PLANILLAS_TRANSPORTE"]!="gmail_api":
        abort(503,description="El envío desde la pantalla todavía no está configurado.")
    try:
        recipient=resolver_destinatario(data["destinatario"])
        key=request.headers.get("Idempotency-Key","")
        if str(UUID(key))!=key:raise ValueError("Se requiere un identificador de solicitud UUID válido.")
    except ValueError as error:raise DatosInvalidos(str(error)) from None
    if es_piloto() and recipient not in destinatarios_prueba():
        abort(403,description="Este piloto admite únicamente los destinatarios de prueba habilitados por Administración.")
    db=sesion()
    lock=int.from_bytes(sha256(("planilla:"+carga.id).encode()).digest()[:8],"big",signed=True)
    db.execute(text("SELECT pg_advisory_xact_lock(:key)"),{"key":lock})
    previous=db.get(Envio,key)
    if previous:
        if previous.carga_id!=carga.id or previous.usuario_id!=g.usuario.id:abort(404)
        if previous.destinatario!=recipient:abort(409,description="La solicitud ya corresponde a otro destinatario.")
        if previous.pdf_sha256!=carga.pdf_sha256:abort(409,description="La solicitud corresponde a un PDF anterior; iniciá un envío para la revisión actual.")
    else:
        # La misma copia y destinatario no se transmiten otra vez tras una recarga o un corte.
        previous=db.scalar(select(Envio).where(Envio.carga_id==carga.id,Envio.destinatario==recipient,Envio.pdf_sha256==carga.pdf_sha256)
                           .order_by(Envio.creado_en.desc()).limit(1))
    if previous:
        return jsonify(**resumen(previous),repetido=True,modo_prueba=False),200 if previous.estado=="enviado" else 409
    try:
        envio=preparar_envio(db,carga,recipient,g.usuario.id,
            data.get("asunto","[Ejemplo] "+db.get(Planilla,carga.planilla_id).codigo.removeprefix("SG-PEM-IFI-")+" de readyproof"),
            data.get("cuerpo","[Ejemplo] Se adjunta la planilla PDF emitida y firmada en readyproof."),envio_id=key)
        send_email(db,envio,transporte="gmail_api")
    except ValueError as error:
        db.rollback();raise DatosInvalidos(str(error)) from None
    return jsonify(**resumen(envio),modo_prueba=bool(current_app.config['MAIL_MODO_PRUEBA'] and not es_piloto())),200 if envio.estado=="enviado" else 202 if current_app.config['MAIL_MODO_PRUEBA'] and not es_piloto() and envio.estado=='pendiente' else 502
