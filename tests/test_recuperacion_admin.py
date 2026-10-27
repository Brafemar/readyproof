"""Recuperación local autorizada sin exposición de claves ni altas implícitas."""
import secrets

import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import comprobar_clave
from app.models import RegistroAcceso, SesionUsuario, Usuario
from tests.conftest import login_cliente


def test_recuperacion_admin_revoca_sesiones_y_audita_sin_clave(app, usuario_admin):
    browser = login_cliente(app, usuario_admin['login'], usuario_admin['clave'])
    nueva = secrets.token_urlsafe(24)
    result = app.test_cli_runner().invoke(args=['admin-recuperar', '--login', usuario_admin['login']], input=f'y\n{nueva}\n{nueva}\n')
    assert result.exit_code == 0, result.output
    assert nueva not in result.output and usuario_admin['clave'] not in result.output
    assert browser.get('/api/clientes').status_code == 401
    with Session(app.extensions['db_engine']) as db:
        user = db.get(Usuario, usuario_admin['id'])
        assert user.activo and user.rol == 'admin'
        assert comprobar_clave(nueva, user.clave_hash)
        assert not comprobar_clave(usuario_admin['clave'], user.clave_hash)
        assert not list(db.scalars(select(SesionUsuario).where(SesionUsuario.usuario_id == user.id)))
        events = list(db.scalars(select(RegistroAcceso).where(RegistroAcceso.evento == 'admin_recuperado_local')))
        assert len(events) == 1 and events[0].usuario_id == user.id and events[0].metodo == 'CLI'
    assert login_cliente(app, usuario_admin['login'], nueva).get('/admin').status_code == 200


@pytest.mark.parametrize('target', ['inexistente', 'tecnico'])
def test_recuperacion_no_crea_cuentas_ni_asciende_tecnicos(app, usuario_admin, target):
    with Session(app.extensions['db_engine']) as db:
        user = db.get(Usuario, usuario_admin['id'])
        if target == 'tecnico':
            user.rol = 'tecnico'
            db.commit()
        original = bytes(user.clave_hash)
    nueva = secrets.token_urlsafe(24)
    login = 'cuenta-inexistente' if target == 'inexistente' else usuario_admin['login']
    result = app.test_cli_runner().invoke(args=['admin-recuperar', '--login', login], input=f'y\n{nueva}\n{nueva}\n')
    assert result.exit_code != 0
    assert 'existente y activo' in result.output
    assert nueva not in result.output
    with Session(app.extensions['db_engine']) as db:
        assert bytes(db.get(Usuario, usuario_admin['id']).clave_hash) == original
        assert len(list(db.scalars(select(Usuario)))) == 1
        assert not list(db.scalars(select(RegistroAcceso).where(RegistroAcceso.evento == 'admin_recuperado_local')))


def test_recuperacion_respeta_validacion_de_clave(app, usuario_admin):
    with Session(app.extensions['db_engine']) as db:
        original = bytes(db.get(Usuario, usuario_admin['id']).clave_hash)
    result = app.test_cli_runner().invoke(args=['admin-recuperar', '--login', usuario_admin['login']], input='y\ncorta\ncorta\n')
    assert result.exit_code != 0
    assert 'al menos 12' in result.output
    with Session(app.extensions['db_engine']) as db:
        assert bytes(db.get(Usuario, usuario_admin['id']).clave_hash) == original


def test_recuperacion_cancelada_conserva_credenciales(app, usuario_admin):
    result = app.test_cli_runner().invoke(args=['admin-recuperar', '--login', usuario_admin['login']], input='n\n')
    assert result.exit_code != 0
    with Session(app.extensions['db_engine']) as db:
        assert comprobar_clave(usuario_admin['clave'], db.get(Usuario, usuario_admin['id']).clave_hash)
