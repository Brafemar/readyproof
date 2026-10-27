"""SQLAlchemy sin servicios externos ni creación implícita de bases."""
from pathlib import Path
import runpy
from flask import current_app, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def preparar_db(app):
    engine = create_engine(app.config["DATABASE_URL"], pool_pre_ping=True)
    app.extensions["db_engine"] = engine
    app.extensions["db_sessions"] = sessionmaker(bind=engine, expire_on_commit=False)
    @app.teardown_appcontext
    def cerrar(error=None):
        session = g.pop("db_session", None)
        if session is not None:
            session.close()


def sesion():
    if "db_session" not in g:
        g.db_session = current_app.extensions["db_sessions"]()
    return g.db_session


def crear_esquema(engine):
    from alembic import command
    from alembic.config import Config
    root=Path(__file__).resolve().parents[1]
    with engine.begin() as connection:
        runpy.run_path(str(root/"migraciones"/"base_etapa4.py"))["upgrade"](connection)
        config=Config(str(root/"alembic.ini"))
        config.attributes["connection"]=connection
        command.upgrade(config,"head")
