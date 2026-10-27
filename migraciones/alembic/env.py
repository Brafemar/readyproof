"""Migraciones PostgreSQL locales sin URL ni credenciales en archivos de configuración."""
import os
from alembic import context
from dotenv import load_dotenv
from sqlalchemy import create_engine
from app.config import RAIZ,validar_base_local
from app.models import Base

config=context.config


def run(connection):
    context.configure(connection=connection,target_metadata=Base.metadata,compare_type=True)
    with context.begin_transaction():context.run_migrations()


if context.is_offline_mode():
    raise RuntimeError("Estas migraciones de datos requieren una conexión PostgreSQL local.")
connection=config.attributes.get("connection")
if connection is not None:
    run(connection)
else:
    load_dotenv(RAIZ/".env")
    url=os.environ.get("DATABASE_URL")
    validar_base_local(url)
    engine=create_engine(url)
    try:
        with engine.begin() as connection:run(connection)
    finally:engine.dispose()
