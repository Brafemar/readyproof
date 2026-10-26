"""SQLAlchemy sin servicios externos ni creación implícita de bases."""
from flask import current_app, g
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from .models import Base, VersionEsquema


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
    with engine.begin() as connection:
        Base.metadata.create_all(connection)
        if connection.execute(select(VersionEsquema.numero).where(VersionEsquema.numero == 1)).first() is None:
            connection.execute(VersionEsquema.__table__.insert().values(numero=1))
