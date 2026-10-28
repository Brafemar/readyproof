"""Cuatro estados del kit para las celdas respondidas de la grilla mensual SDI."""
from .validacion import DatosInvalidos

ESTADOS = ('✓', 'O', 'X', 'NA')


def validar_sdi_grilla_mensual(carga_dict, esquema):
    """No exige completar meses futuros ni interpreta frecuencias del kit."""
    blocks = carga_dict.get('bloques', {})
    if not isinstance(blocks, dict):
        raise DatosInvalidos('bloques debe ser un objeto.')
    for title, fields in esquema['bloques'].items():
        values = blocks.get(title, {})
        if not isinstance(values, dict):
            raise DatosInvalidos(f'{title} debe ser un objeto.')
        for key, value in values.items():
            field = fields.get(key, {})
            if field.get('tipo') == 'opcion' and set(field.get('opciones', [])) == set(ESTADOS):
                if not isinstance(value, str) or value not in ESTADOS:
                    raise DatosInvalidos(f'{title} · {key}: usá ✓, O, X o NA.')
    return carga_dict
