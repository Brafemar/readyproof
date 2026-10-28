"""Formato y dígito verificador CUIT/CUIL; sin consultar padrones externos."""
import re


def normalizar_cuit(cuit_str):
    """Acepta once dígitos ASCII o XX-XXXXXXXX-X y devuelve once dígitos."""
    if not isinstance(cuit_str, str):
        raise ValueError('El CUIT debe ser texto de once dígitos.')
    value = cuit_str.strip()
    if not re.fullmatch(r'(?:[0-9]{11}|[0-9]{2}-[0-9]{8}-[0-9])', value):
        raise ValueError('El CUIT debe tener once dígitos, con o sin los guiones de formato.')
    return value.replace('-', '')


def validar_cuit(cuit_str):
    """Valida formato y módulo 11; no acredita inscripción ni titularidad."""
    try:
        value = normalizar_cuit(cuit_str)
    except ValueError:
        return False
    total = sum(int(digit)*weight for digit, weight in zip(value[:10], (5,4,3,2,7,6,5,4,3,2)))
    verifier = 11 - total % 11
    if verifier == 11:
        verifier = 0
    return verifier < 10 and verifier == int(value[-1])
