"""Vencimientos por meses calendario o días explícitos, sin asignar frecuencias."""
from datetime import date, timedelta
from calendar import monthrange

def vencimiento(fecha_certificado, *, meses=None, dias=None):
    if (meses is None)==(dias is None):
        raise ValueError('Indicar meses o días, exclusivamente.')
    valor=meses if meses is not None else dias
    if isinstance(valor,bool) or not isinstance(valor,int) or valor<=0:
        raise ValueError('El intervalo debe ser un entero positivo confirmado.')
    if dias is not None: return fecha_certificado+timedelta(days=dias)
    total=fecha_certificado.year*12+fecha_certificado.month-1+meses
    year,month=divmod(total,12); month+=1
    return date(year,month,min(fecha_certificado.day,monthrange(year,month)[1]))
