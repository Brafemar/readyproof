"""Vigencia del certificado en días corridos."""
from datetime import timedelta


PERIODICIDADES = {
    "mensual": ("Mensual", 30),
    "trimestral": ("Trimestral", 90),
    "semestral": ("Semestral", 180),
    "anual": ("Anual", 365),
}

PERIODICIDADES_LEGADAS = {
    (("dias", 7), ("meses", 1)): "mensual",
    (("meses", 1),): "mensual",
    (("meses", 3),): "trimestral",
    (("meses", 6),): "semestral",
    (("meses", 12),): "anual",
    **{(("dias", dias),): clave for clave, (_, dias) in PERIODICIDADES.items()},
}


def vigencia_emision(fecha_emision, periodicidad):
    _, dias = PERIODICIDADES[periodicidad]
    return fecha_emision + timedelta(days=dias - 1)
