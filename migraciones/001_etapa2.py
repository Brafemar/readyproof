"""Migración inicial local: clientes, sistemas, planillas, cargas y revisiones."""
from app.db import crear_esquema


def upgrade(engine):
    crear_esquema(engine)
