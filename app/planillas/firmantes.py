"""Identificación de firmantes y validación previa a la finalización."""
import re
from .validacion import DatosInvalidos,campos_permitidos,mapa

CAMPOS=('nombre_firmante','dni_firmante','cargo_firmante')


def nombre_tecnico_segun_modo(value):
    """Presenta la identidad guardada sin alterar el nombre ni su historial."""
    from ..modo import es_piloto
    nombre=value or ''
    return nombre if es_piloto() else nombre.removeprefix('[Ejemplo] ')


def validar_responsable(value,*,completo=False):
    from ..modo import es_piloto
    value=mapa(value,'responsable');campos_permitidos(value,CAMPOS,'responsable')
    result={}
    for key in CAMPOS:
        text=value.get(key,'')
        if not isinstance(text,str):raise DatosInvalidos('Los datos del responsable deben ser texto.')
        if any(ord(char)<32 for char in text):raise DatosInvalidos('Los datos del responsable no admiten saltos de línea ni caracteres de control.')
        try:text.encode('cp1252')
        except UnicodeEncodeError:raise DatosInvalidos('Los datos del responsable deben usar caracteres latinos compatibles con la planilla.') from None
        text=text if key=='dni_firmante' else text.strip()
        if len(text)>(15 if key=='dni_firmante' else 120):raise DatosInvalidos('Un dato del responsable supera el largo permitido.')
        if key=='dni_firmante':
            if not re.fullmatch(r'[0-9]{0,15}',text):raise DatosInvalidos('El DNI admite solo dígitos, sin puntos ni guiones.')
            if completo and not re.fullmatch(r'[0-9]{8,15}',text):raise DatosInvalidos('El DNI del responsable debe tener de 8 a 15 dígitos.')
        elif text and es_piloto() and not text.startswith('[Ejemplo] '):raise DatosInvalidos('Usá datos ficticios del responsable que comiencen con [Ejemplo].')
        result[key]=text
    if completo and not result['nombre_firmante']:raise DatosInvalidos('El nombre del responsable es obligatorio.')
    return result


def ejemplo_responsable():
    return dict(nombre_firmante='[Ejemplo] Responsable de prueba',dni_firmante='00000000',cargo_firmante='[Ejemplo] Encargado')
