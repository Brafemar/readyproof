"""Solicitud autenticada de envío: creación y preparación, sin SMTP en la petición."""
from flask import Blueprint, abort, current_app, g, jsonify
from ..db import sesion
from ..models import Carga
from ..rutas.api import obtener, objeto
from ..planillas.validacion import DatosInvalidos
from . import preparar_envio, send_email

correo_api=Blueprint("correo_api",__name__,url_prefix="/api")


@correo_api.post("/cargas/<uuid:carga_id>/enviar")
def enviar(carga_id):
    carga=obtener(Carga,str(carga_id))
    if carga.estado!="emitida":abort(409,description="Solo se puede enviar una carga emitida.")
    data=objeto({"destinatario"},{"asunto","cuerpo"})
    try:
        envio=preparar_envio(sesion(),carga,data["destinatario"],g.usuario.id,
            data.get("asunto","[Ejemplo] Planilla readyproof"),data.get("cuerpo","[Ejemplo] Se adjunta la planilla PDF emitida."))
        send_email(sesion(),envio,encolar=True)
    except ValueError as error:
        sesion().rollback();raise DatosInvalidos(str(error)) from None
    return jsonify(id=envio.id,carga_id=envio.carga_id,estado=envio.estado,modo_prueba=current_app.config["MAIL_MODO_PRUEBA"]),202
