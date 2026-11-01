"""Validación del conjunto completo de marcas, antes de alterar la foto."""
from flask import abort

from ..planillas.multisistema import RESULTADOS
from .items import items_punto2


def validar_anotaciones(payload, definicion=None):
    if not isinstance(payload, dict) or set(payload) != {"anotaciones"} or not isinstance(payload["anotaciones"], list):
        abort(400, description="Enviá un objeto con la lista anotaciones; usá Guardar marcas desde la app.")
    result = []
    for numero, marca in enumerate(payload["anotaciones"], 1):
        prefix = f"Marca {numero}: "
        if not isinstance(marca, dict) or set(marca) - {"id", "numero", "x", "y", "codigo", "texto", "item"}:
            abort(400, description=prefix + "enviá posición, código y texto desde el editor de fotos.")
        for name in ("x", "y"):
            value = marca.get(name)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 1:
                abort(400, description=prefix + f"la posición {name} debe estar entre 0 y 1; volvé a colocar la marca.")
        codigo = marca.get("codigo")
        if not isinstance(codigo, str) or codigo not in RESULTADOS:
            abort(400, description=prefix + "elegí un código válido: ✓, O, X o NA.")
        texto = marca.get("texto")
        if not isinstance(texto, str) or len(texto) > 140 or "\x00" in texto:
            abort(400, description=prefix + "el texto debe tener hasta 140 caracteres válidos; corregí la observación.")
        if codigo in ("O", "X") and not texto.strip():
            abort(400, description=prefix + f"completá el texto de la observación para el código {codigo}.")
        value = dict(numero=numero, x=float(marca["x"]), y=float(marca["y"]), codigo=codigo, texto=texto)
        item = marca.get("item")
        if item is not None:
            if not isinstance(item, dict) or set(item) - {"bloque", "campo", "texto"}:
                abort(400, description=prefix + "elegí un ítem válido del punto 2.")
            opciones = items_punto2(definicion or {})
            referencia = next((r for r in opciones if r["bloque"] == item.get("bloque") and r["campo"] == item.get("campo")), None)
            if referencia is None or ("texto" in item and item["texto"] != referencia["texto"]):
                abort(400, description=prefix + "el ítem no pertenece a esta planilla o su texto cambió; volvé a elegirlo.")
            value["item"] = referencia
        result.append(value)
    return result
