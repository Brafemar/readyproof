"""Autoría nullable para conservar las cargas y revisiones anteriores."""
from sqlalchemy import text


def upgrade(connection):
    connection.execute(text("ALTER TABLE cargas ADD COLUMN IF NOT EXISTS creada_por_id VARCHAR(36) REFERENCES usuarios(id)"))
    connection.execute(text("ALTER TABLE revisiones_carga ADD COLUMN IF NOT EXISTS actor_id VARCHAR(36) REFERENCES usuarios(id)"))
