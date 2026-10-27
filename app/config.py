"""Configuración del entorno local mediante variables de entorno."""
import os
from pathlib import Path
from sqlalchemy.engine import make_url

RAIZ = Path(__file__).resolve().parents[1]


def configuracion():
    return {
        "MAIL_MODO_PRUEBA": os.environ.get("MAIL_MODO_PRUEBA", "true").lower() != "false",
        "DIRECTORIO_CORREO": str(RAIZ / "out" / "correo_prueba"),
        "DATABASE_URL": os.environ.get("DATABASE_URL"),
        "DIRECTORIO_TEMPORAL": str(RAIZ / "out" / "api_temporales"),
        "MAX_CONTENT_LENGTH": 512 * 1024,
    }


def validar_base_local(url):
    if not url:
        raise RuntimeError("Configurar DATABASE_URL con una base PostgreSQL local.")
    parsed = make_url(url)
    if parsed.drivername != "postgresql+psycopg" or parsed.host not in {"localhost", "127.0.0.1", "::1"}:
        raise RuntimeError("Esta etapa admite únicamente PostgreSQL local con psycopg.")
