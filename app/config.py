"""Configuración del entorno local mediante variables de entorno."""
import os
from pathlib import Path
from sqlalchemy.engine import make_url

RAIZ = Path(__file__).resolve().parents[1]
SISTEMAS_HABILITADOS = {
    'SAA':'Sistema de Abastecimiento de Agua', 'SAL':'Sistema de Extinción por Agentes Limpios',
    'SBC':'Sistema de Bombas Contraincendios', 'SDI':'Sistema de Detección de Incendios',
    'SAP':'Sistema de Agua Pulverizada', 'SCC':'Sistema Fijo de Extinción para Cocinas Comerciales',
    'SDC':'Sistema de Extinción por Dióxido de Carbono', 'SEP':'Sistema Fijo de Extinción por Polvo',
    'SGE':'Sistema Generador de Espuma', 'SHC':'Sistema de Hidrantes Contra Incendios',
    'SIM':'Simbología de Seguridad contra Incendios', 'SRA':'Sistema de Rociadores Automáticos',
    'SRE':'Sistema de Rociadores de Espuma', 'SSA':'Sistema Fijo de Extinción por Solución Acuosa',
    'STM':'Sistema de Tuberías y Mangueras',
}


def configuracion():
    raw_mode=os.environ.get('MODO_PILOTO','true').lower()
    if raw_mode not in ('true','false'):raise RuntimeError('MODO_PILOTO debe ser true o false.')
    piloto=raw_mode=='true'
    return {
        'MODO_PILOTO':piloto,
        'EMPRESA_MANTENEDORA':os.environ.get('EMPRESA_MANTENEDORA','[Ejemplo] readyproof').strip(),
        'CERTIFICADO_N':os.environ.get('CERTIFICADO_N','IFI-2024-00000').strip(),
        'DESTINATARIO_PRUEBA':os.environ.get('DESTINATARIO_PRUEBA','').strip(),
        'SISTEMAS_HABILITADOS': dict(SISTEMAS_HABILITADOS),
        "MAIL_MODO_PRUEBA": os.environ.get("MAIL_MODO_PRUEBA", "true" if piloto else "false").lower() != "false",
        "DOCUMENTACION_MODO_PRUEBA": os.environ.get("DOCUMENTACION_MODO_PRUEBA", os.environ.get("MAIL_MODO_PRUEBA", "true")).lower() != "false",
        "DOCUMENTACION_TRANSPORTE": os.environ.get("DOCUMENTACION_TRANSPORTE", "smtp"),
        "PLANILLAS_TRANSPORTE": os.environ.get("PLANILLAS_TRANSPORTE", "cola"),
        "PLANILLAS_DESTINATARIOS_PRUEBA": os.environ.get("PLANILLAS_DESTINATARIOS_PRUEBA", ""),
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
