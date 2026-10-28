"""readyproof: API local de planillas con datos ficticios."""
import click
from datetime import timedelta
import os
import secrets
from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort, render_template, g
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import StaleDataError
from werkzeug.exceptions import HTTPException

from .config import RAIZ, configuracion, validar_base_local
from .db import preparar_db, crear_esquema, sesion
from .planillas.validacion import DatosInvalidos


def create_app(test_config=None):
    if not (test_config and test_config.get("TESTING")):
        load_dotenv(RAIZ / ".env.local", override=False)
        load_dotenv(RAIZ / ".env", override=False)
    app = Flask(__name__)
    app.config.update(configuracion())
    app.json.sort_keys = False
    app.config["MAX_CONTENT_LENGTH"] = 768 * 1024
    if test_config:
        app.config.update(test_config)
    validar_base_local(app.config["DATABASE_URL"])
    app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_urlsafe(48)
    if app.secret_key == "cambiar-por-un-valor-largo-y-aleatorio" or len(app.secret_key) < 32:
        raise RuntimeError("SECRET_KEY debe tener al menos 32 caracteres y no ser el valor de ejemplo.")
    app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("READYPROOF_HTTPS", "false").lower()=="true",
        PERMANENT_SESSION_LIFETIME=timedelta(hours=8), SESSION_REFRESH_EACH_REQUEST=False)
    preparar_db(app)
    from .rutas.api import api
    app.register_blueprint(api)
    from .correo.rutas import correo_api
    app.register_blueprint(correo_api)
    from .rutas.web import web
    app.register_blueprint(web)
    from .auth.rutas import auth
    from .auth import cargar_usuario, exigir_usuario, verificar_csrf, registro
    app.register_blueprint(auth)
    from .documentacion import documentacion
    app.register_blueprint(documentacion)
    @app.before_request
    def acceso_local():
        if request.remote_addr not in {"127.0.0.1", "::1"}:
            abort(403, description="El entorno de pruebas admite únicamente acceso local.")
        if request.path.startswith("/static/") or request.path == "/sw.js":
            return
        cargar_usuario()
        if request.path.startswith("/api/") and request.path not in {"/api/auth/sesion", "/api/auth/login"}:
            exigir_usuario()
        if request.method not in {"GET","HEAD","OPTIONS"}:
            verificar_csrf()
    @app.after_request
    def cabeceras_locales(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "same-origin"
        if not request.path.startswith("/static/"):
            response.headers["Cache-Control"] = "no-store"
        if request.path.startswith("/api/") or request.path in {"/login","/cuenta","/configuracion-inicial"}:
            try:
                from flask import g
                if not hasattr(g,"usuario"): g.usuario=None
                registro(getattr(g,"evento_auth","acceso"), estado=response.status_code, login_huella=getattr(g,"login_huella",None))
                sesion().commit()
            except SQLAlchemyError:
                sesion().rollback()
                response = jsonify(error="No se pudo registrar el acceso. Intentá nuevamente.")
                response.status_code = 503
                response.headers["Cache-Control"] = "no-store"
        return response
    def respuesta_error(message, code):
        from .auth import csrf_token
        if request.method == "POST" and request.endpoint in {"auth.login","auth.inicial"}:
            return render_template("login.html", inicial=request.endpoint=="auth.inicial", csrf=csrf_token(), error=message), code
        if request.method == "POST" and request.endpoint=="auth.cuenta" and getattr(g,"usuario",None):
            return render_template("cuenta.html", usuario=g.usuario, csrf=csrf_token(), error=message), code
        return jsonify(error=message), code
    @app.errorhandler(DatosInvalidos)
    def datos_invalidos(error):
        return respuesta_error(str(error), 422)
    @app.errorhandler(HTTPException)
    def error_http(error):
        return respuesta_error(error.description, error.code)
    @app.errorhandler(StaleDataError)
    def conflicto(error):
        sesion().rollback()
        return jsonify(error="La carga cambió; volver a consultarla antes de guardar."), 409
    @app.errorhandler(IntegrityError)
    def integridad(error):
        sesion().rollback()
        return jsonify(error="La operación entra en conflicto con los registros existentes."), 409
    @app.errorhandler(SQLAlchemyError)
    def base_no_disponible(error):
        sesion().rollback()
        return jsonify(error="No se pudo completar la operación en la base local."), 503
    @app.cli.command("init-db")
    @click.option("--ejemplos", is_flag=True, help="Registra el catálogo SAA-1 y un cliente ficticio.")
    def init_db(ejemplos):
        crear_esquema(app.extensions["db_engine"])
        from sqlalchemy import select,func
        from .models import Planilla
        from .carga_planillas import cargar_planillas_desde_json
        cargar_planillas_desde_json(sesion())
        if ejemplos:
            from .catalogo import registrar_ejemplos
            registrar_ejemplos(sesion())
        click.echo("Esquema local preparado.")
    @app.cli.command("cargar-planillas")
    def cargar_planillas():
        from .carga_planillas import cargar_planillas_desde_json
        count=cargar_planillas_desde_json(sesion())
        click.echo(f"Catálogo JSON verificado; {count} planillas nuevas.")
    @app.cli.command("correo-reintentar")
    def correo_reintentar():
        from .correo import reintentar_envios
        click.echo(f"Intentos procesados: {reintentar_envios()}")

    @app.cli.command("admin-recuperar")
    @click.option("--login", required=True, help="Administrador existente autorizado para recuperación local.")
    def admin_recuperar(login):
        """Restablece una cuenta admin desde una consola local autorizada."""
        click.echo("Recuperación local: se cambiará la clave del administrador indicado y se cerrarán sus sesiones.")
        click.confirm("¿Confirmás la recuperación autorizada de esta cuenta?", abort=True)
        nueva = click.prompt("Nueva contraseña", hide_input=True, confirmation_prompt="Repetir contraseña")
        from .auth.recuperacion import recuperar_admin
        try:
            recuperar_admin(login, nueva)
        except DatosInvalidos as error:
            sesion().rollback()
            raise click.ClickException(str(error)) from None
        finally:
            nueva = None
        click.echo("Administrador recuperado. Sesiones cerradas y operación registrada. Ingresá con la clave nueva.")

    @app.cli.command("correo-bounce")
    @click.option("--envio", required=True, type=click.UUID)
    @click.option("--actor", required=True, type=click.UUID)
    def correo_bounce(envio, actor):
        from .correo import registrar_bounce
        try:
            registrar_bounce(sesion(), str(envio), str(actor))
        except ValueError as error:
            raise click.ClickException(str(error)) from None
        click.echo("Aviso de no entrega registrado; reintentos bloqueados.")

    @app.cli.command("correo-worker")
    def correo_worker():
        """Procesa la cola cada 15 minutos. Finaliza con Ctrl+C."""
        from .correo import reintentar_envios
        import time
        click.echo("Proceso de correo iniciado; intervalo 15 minutos. Ctrl+C para detener.")
        while True:
            reintentar_envios()
            time.sleep(900)
    return app
