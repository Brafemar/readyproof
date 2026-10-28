"""Validaciones de configuración y datos para el modo de operación."""
import re
from flask import current_app, has_app_context


def es_piloto():
    return current_app.config.get('MODO_PILOTO', True) if has_app_context() else True


def validar_configuracion_real():
    from .planillas.validacion import DatosInvalidos
    if es_piloto():return
    for key in ('EMPRESA_MANTENEDORA', 'CERTIFICADO_N'):
        value=current_app.config.get(key, '')
        if (not isinstance(value,str) or not value.strip() or len(value)>200 or
            any(ord(c)<32 for c in value) or value.strip().lower().startswith(('[ejemplo]','[pendiente')) or
            (key=='CERTIFICADO_N' and (value=='IFI-2024-00000' or re.fullmatch(r'IFI-[0-9]{4}-0+',value)))):
            raise DatosInvalidos('Modo REAL requiere '+key+' confirmado, sin valores ficticios.')
        try:value.encode('cp1252')
        except UnicodeEncodeError:raise DatosInvalidos(key+' debe ser compatible con la escritura de la planilla.') from None


def validar_emision_modo(datos):
    from .planillas.validacion import DatosInvalidos
    validar_configuracion_real()
    if not es_piloto():
        for campo,key in (('empresa_mantenedora','EMPRESA_MANTENEDORA'),('numero_mantenedor','CERTIFICADO_N')):
            if datos.get('cabecera',{}).get(campo)!=current_app.config[key]:
                raise DatosInvalidos('La cabecera debe conservar '+key+' configurado para esta emisión.')
