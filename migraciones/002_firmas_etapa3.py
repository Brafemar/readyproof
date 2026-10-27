"""Migración aditiva de firmas y huellas de firma en el historial."""
from sqlalchemy import text


def upgrade(connection):
    connection.execute(text("ALTER TABLE revisiones_carga ADD COLUMN IF NOT EXISTS firmas_huellas JSON"))
