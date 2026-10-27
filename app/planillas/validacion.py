"""Tipos del piloto basados en las etiquetas y opciones existentes del kit."""
from copy import deepcopy
from datetime import date
from math import isfinite

from .definiciones.saa1 import definicion_saa1
from .generador import CABECERA

FECHAS = {
    ("ABASTECIMIENTO DE AGUA", "Última prueba de abastecimiento de agua (fecha)"),
    ("BOMBAS CONTRA INCENDIO (CAPÍTULO 12)", "Registro de la última inspección (fecha)"),
}
ENTEROS = {
    ("BOMBAS CONTRA INCENDIO (CAPÍTULO 12)", "Cantidad"),
    ("TOMA DE IMPULSIÓN PARA BOMBEROS", "Cantidad"),
}


class DatosInvalidos(ValueError):
    pass


def mapa(value, nombre):
    if not isinstance(value, dict):
        raise DatosInvalidos(f"{nombre} debe ser un objeto JSON.")
    return value


def campos_permitidos(value, permitidos, nombre):
    if set(value) - set(permitidos):
        raise DatosInvalidos(f"{nombre} contiene campos desconocidos.")


def fecha(value):
    if not isinstance(value, str):
        raise DatosInvalidos("La fecha debe ser texto ISO YYYY-MM-DD.")
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        raise DatosInvalidos("La fecha debe ser válida y tener formato YYYY-MM-DD.") from None
    if parsed.isoformat() != value:
        raise DatosInvalidos("La fecha debe tener formato YYYY-MM-DD.")
    return value


def texto(value, *, ejemplo=True):
    if not isinstance(value, str) or not value.strip() or len(value) > 500:
        raise DatosInvalidos("Se requiere texto no vacío de hasta 500 caracteres.")
    if any(ord(c) < 32 and c not in "\n\r\t" for c in value):
        raise DatosInvalidos("El texto contiene caracteres de control.")
    if ejemplo and not value.startswith("[Ejemplo] "):
        raise DatosInvalidos("Esta etapa solo admite textos ficticios identificados con [Ejemplo].")
    return value


def numero(value, *, entero=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or (isinstance(value, float) and not isfinite(value)):
        raise DatosInvalidos("Se requiere un número JSON finito.")
    if entero and not isinstance(value, int):
        raise DatosInvalidos("La cantidad debe ser un número entero JSON.")
    return value


def esquema_saa1():
    spec = definicion_saa1()
    blocks = {}
    for title, fields in spec["bloques"]:
        typed = {}
        for field in fields:
            label, options = field if isinstance(field, tuple) else (field, None)
            kind = "opcion" if isinstance(options, list) else "fecha" if (title, label) in FECHAS else "entero" if (title, label) in ENTEROS else "numero" if isinstance(options, str) and options else "texto"
            typed[label] = {"tipo": kind}
            if kind == "opcion":
                typed[label]["opciones"] = list(options)
            elif isinstance(options, str) and options:
                typed[label]["unidad"] = options
        blocks[title] = typed
    return {"cabecera": {key: {"tipo": "fecha" if key == "fecha" else "texto"} for key in CABECERA}, "bloques": blocks, "observaciones": {"tipo": "lista_texto", "maximo": 4}}


def validar_datos(datos, esquema):
    datos = mapa(datos, "datos")
    campos_permitidos(datos, {"cabecera", "bloques", "observaciones"}, "datos")
    normalized = {"cabecera": {}, "bloques": {}, "observaciones": []}
    header = mapa(datos.get("cabecera", {}), "cabecera")
    campos_permitidos(header, esquema["cabecera"], "cabecera")
    for key, value in header.items():
        normalized["cabecera"][key] = fecha(value) if key == "fecha" else texto(value, ejemplo=not (key == "empresa_mantenedora" and value == "readyproof"))
    blocks = mapa(datos.get("bloques", {}), "bloques")
    campos_permitidos(blocks, esquema["bloques"], "bloques")
    for title, values in blocks.items():
        values = mapa(values, title)
        fields = esquema["bloques"][title]
        campos_permitidos(values, fields, title)
        normalized["bloques"][title] = {}
        for label, value in values.items():
            field = fields[label]
            kind = field["tipo"]
            if kind == "opcion":
                if not isinstance(value, str) or value not in field["opciones"]:
                    raise DatosInvalidos(f"Opción inválida para {label}.")
                result = value
            elif kind == "fecha":
                result = fecha(value)
            elif kind in {"numero", "entero"}:
                result = numero(value, entero=kind == "entero")
            else:
                result = texto(value)
            normalized["bloques"][title][label] = result
    observations = datos.get("observaciones", [])
    if not isinstance(observations, list) or len(observations) > 4:
        raise DatosInvalidos("observaciones debe contener hasta cuatro textos.")
    normalized["observaciones"] = ["" if value == "" else texto(value) for value in observations]
    return normalized


def datos_para_excel(datos):
    result = deepcopy(datos)
    if "fecha" in result.get("cabecera", {}):
        result["cabecera"]["fecha"] = date.fromisoformat(result["cabecera"]["fecha"])
    for title, label in FECHAS:
        if label in result.get("bloques", {}).get(title, {}):
            result["bloques"][title][label] = date.fromisoformat(result["bloques"][title][label])
    return result
