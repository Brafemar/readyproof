"""Observaciones y mediciones usando los campos existentes de las planillas."""
from math import isfinite

from ..planillas.validacion import DatosInvalidos


class ValidationError(DatosInvalidos):
    pass


def validar_item_verificacion(item_resultado, item_def):
    """Valida un resultado sin completar ni modificar los datos recibidos."""
    if not isinstance(item_resultado, dict) or not isinstance(item_def, dict):
        raise ValidationError('El resultado y la definición deben ser objetos.')
    result = item_resultado.get('resultado')
    label = item_def.get('etiqueta', 'Ítem')
    if result not in ('✓', 'O', 'X', 'NA'):
        raise ValidationError(f'{label}: indicá un resultado válido (✓, O, X o NA).')
    observation = item_resultado.get('observacion')
    if observation is not None and not isinstance(observation, str):
        raise ValidationError(f'{label}: la observación debe ser texto.')
    if result == 'O' and (not observation or not observation.strip()):
        raise ValidationError(f'{label}: O (no cumple) requiere una observación.')
    value = item_resultado.get('valor')
    measured = item_def.get('formato', 'ver') == 'ver' and bool(item_def.get('unidad'))
    if measured and result != 'NA' and value is None:
        raise ValidationError(f'{label}: indicá la medición en {item_def["unidad"]}, salvo NA.')
    if measured and value is not None:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or (isinstance(value, float) and not isfinite(value)):
            raise ValidationError(f'{label}: la medición debe ser un número finito.')
    return item_resultado


def validar_reglas_carga(datos, esquema):
    """Aplica reglas al cerrar; los borradores pueden permanecer incompletos."""
    observation = '\n'.join(value for value in datos.get('observaciones', []) if value.strip())
    if esquema.get('tipo_planilla') == 'checklist':
        for title, table in esquema.get('tablas', {}).items():
            values = datos.get('bloques', {}).get(title, {})
            fields = esquema['bloques'][title]
            for row in table['filas']:
                value_key, result_key = row['campos']
                unit = fields[value_key].get('unidad')
                if not unit and value_key not in values and result_key not in values:
                    continue
                validar_item_verificacion(
                    {'resultado': values.get(result_key), 'valor': values.get(value_key), 'observacion': observation},
                    {'unidad': unit, 'formato': 'ver', 'etiqueta': title+' · '+row['etiqueta']},
                )
    else:
        for title, values in datos.get('bloques', {}).items():
            for key, value in values.items():
                field = esquema['bloques'][title][key]
                if field.get('tipo') == 'opcion' and value == 'O':
                    validar_item_verificacion({'resultado': value, 'observacion': observation},
                        {'formato': 'general', 'etiqueta': field.get('etiqueta', key)})
