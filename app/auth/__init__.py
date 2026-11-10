"""Autenticación local, sesiones revocables y autorización por cliente."""
from datetime import timedelta
from functools import wraps
from hashlib import sha256
import re
import secrets

import bcrypt
from flask import abort, current_app, g, request, session
from sqlalchemy import delete, select

from ..db import sesion
from ..models import Usuario, UsuarioCliente, SesionUsuario, RegistroAcceso, ahora
from ..planillas.validacion import DatosInvalidos

_DUMMY = bcrypt.hashpw(secrets.token_bytes(32), bcrypt.gensalt())


def hash_clave(value):
    if not isinstance(value, str) or len(value) < 12 or len(value.encode("utf-8")) > 72:
        raise DatosInvalidos("La contraseña debe tener al menos 12 caracteres y como máximo 72 bytes UTF-8.")
    return bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt())


def comprobar_clave(value, hashed=None):
    if not isinstance(value, str) or len(value.encode("utf-8")) > 72:
        return False
    return bcrypt.checkpw(value.encode("utf-8"), hashed or _DUMMY) and hashed is not None


def normalizar_login(value):
    if not isinstance(value, str) or not re.fullmatch(r"[a-zA-Z0-9._-]{3,80}", value):
        raise DatosInvalidos("El usuario debe tener entre 3 y 80 letras sin tildes, números, puntos, guiones o guiones bajos.")
    return value.lower()


def csrf_token():
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(32)
    return session["csrf"]


def iniciar_sesion(usuario):
    cerrar_sesion()
    token = secrets.token_urlsafe(48)
    session["sid"] = token
    session.permanent = True
    csrf_token()
    row = SesionUsuario(token_hash=sha256(token.encode()).hexdigest(), usuario_id=usuario.id, vence_en=ahora()+timedelta(hours=8))
    sesion().add(row)
    g.usuario = usuario
    g.sesion_usuario = row


def revocar(usuario_id):
    sesion().execute(delete(SesionUsuario).where(SesionUsuario.usuario_id == usuario_id))


def cerrar_sesion():
    token = session.get("sid")
    if isinstance(token, str):
        sesion().execute(delete(SesionUsuario).where(SesionUsuario.token_hash == sha256(token.encode()).hexdigest()))
    session.clear()


def cargar_usuario():
    g.usuario = None
    g.sesion_usuario = None
    token = session.get("sid")
    if isinstance(token, str):
        row = sesion().get(SesionUsuario, sha256(token.encode()).hexdigest())
        if row is not None:
            user = sesion().get(Usuario, row.usuario_id)
            if row.vence_en > ahora() and user is not None and user.activo:
                g.usuario, g.sesion_usuario = user, row
                return
            sesion().delete(row)
            sesion().commit()
        session.clear()


def exigir_usuario():
    if g.usuario is None:
        abort(401, description="Iniciá sesión para continuar.")


def exigir_admin():
    exigir_usuario()
    if g.usuario.rol != "admin":
        abort(403, description="Esta operación requiere el rol administrador.")


def permitido(cliente_id):
    exigir_usuario()
    g.acceso_cliente_id = cliente_id
    return g.usuario.rol == "admin" or sesion().get(UsuarioCliente, (g.usuario.id, cliente_id)) is not None


def autorizar_cliente(cliente_id):
    if not permitido(cliente_id):
        abort(404, description="Registro inexistente.")


def verificar_csrf():
    origin = request.headers.get("Origin")
    if origin is not None and origin.rstrip("/") != request.host_url.rstrip("/"):
        abort(403, description="Origen de solicitud no permitido.")
    supplied = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token")
    expected = session.get("csrf")
    if not isinstance(supplied, str) or not isinstance(expected, str) or not secrets.compare_digest(supplied, expected):
        abort(403, description="La sesión del formulario cambió. Recargá antes de continuar.")


def registro(evento, *, usuario_id=None, estado=200, login_huella=None):
    row = RegistroAcceso(usuario_id=usuario_id if usuario_id is not None else getattr(g.usuario, "id", None), evento=evento,
        ruta=request.url_rule.rule if request.url_rule else "ruta_inexistente", metodo=request.method,
        estado_http=estado, cliente_id=getattr(g,"acceso_cliente_id",None), carga_id=getattr(g,"acceso_carga_id",None), login_huella=login_huella)
    sesion().add(row)
    return row


def usuario_json(usuario):
    return {"id":usuario.id,"login":usuario.login,"nombre":usuario.nombre,"rol":usuario.rol,"activo":usuario.activo,"certificado_conjunto":usuario.certificado_conjunto}
