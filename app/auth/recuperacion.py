"""Recuperación local explícita de una cuenta administradora existente."""
from sqlalchemy import delete, select, text

from . import hash_clave, normalizar_login
from ..db import sesion
from ..models import RegistroAcceso, SesionUsuario, Usuario
from ..planillas.validacion import DatosInvalidos


def recuperar_admin(login, nueva):
    login = normalizar_login(login)
    database = sesion()
    database.execute(text("SELECT pg_advisory_xact_lock(724004)"))
    user = database.scalar(select(Usuario).where(Usuario.login == login).with_for_update())
    if user is None or user.rol != "admin" or not user.activo:
        raise DatosInvalidos("La recuperación requiere un administrador existente y activo.")
    user.clave_hash = hash_clave(nueva)
    database.execute(delete(SesionUsuario).where(SesionUsuario.usuario_id == user.id))
    database.add(RegistroAcceso(usuario_id=user.id, evento="admin_recuperado_local",
        ruta="admin-recuperar", metodo="CLI", estado_http=200))
    database.commit()
