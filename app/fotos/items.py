"""Referencias a filas y campos reales del punto 2 de cada planilla."""


def items_punto2(definicion):
    result = []
    for bloque, campos in definicion.get("bloques", {}).items():
        tabla = definicion.get("tablas", {}).get(bloque)
        if tabla is not None:
            for fila in tabla.get("filas", []):
                claves = fila.get("campos", [])
                if claves and all(clave in campos for clave in claves) and isinstance(fila.get("etiqueta"), str):
                    result.append(dict(bloque=bloque, campo=claves[0], texto=fila["etiqueta"]))
        else:
            for campo, descripcion in campos.items():
                etiqueta = descripcion.get("etiqueta") or campo
                result.append(dict(bloque=bloque, campo=campo, texto=etiqueta))
    return result
