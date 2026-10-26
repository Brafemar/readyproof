"""readyproof: API local de planillas con datos ficticios."""
import click
from dotenv import load_dotenv
from flask import Flask, jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import StaleDataError
from werkzeug.exceptions import HTTPException

from .config import RAIZ, configuracion, validar_base_local
from .db import preparar_db, crear_esquema, sesion
from .planillas.validacion import DatosInvalidos


def create_app(test_config=None):
    load_dotenv(RAIZ / ".env")
    app = Flask(__name__)
    app.config.update(configuracion())
    if test_config:
        app.config.update(test_config)
    validar_base_local(app.config["DATABASE_URL"])
    preparar_db(app)
    from .rutas.api import api
    app.register_blueprint(api)
    @app.errorhandler(DatosInvalidos)
    def datos_invalidos(error):
        return jsonify(error=str(error)), 422
    @app.errorhandler(HTTPException)
    def error_http(error):
        return jsonify(error=error.description), error.code
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
        if ejemplos:
            from .catalogo import registrar_ejemplos
            registrar_ejemplos(sesion())
        click.echo("Esquema local preparado.")
    return app
