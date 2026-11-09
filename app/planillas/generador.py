"""Carga SAA-1 sobre el generador del kit conservando su paquete Excel."""
from collections.abc import Mapping
from datetime import date
from math import isfinite
from pathlib import Path
import runpy
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from lxml import etree

from .definiciones.saa1 import HERRAMIENTAS, MODELO, definicion_saa1

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
CABECERA = {
    "fecha": "V4", "cliente": "C5", "cuit": "O5", "telefono": "V5",
    "direccion": "C6", "edificio": "O6", "sector": "V6",
    "empresa_mantenedora": "E7", "numero_mantenedor": "R7", "inspector": "V7",
    "sistema_designacion": "A8",
}


def _texto(valor):
    if isinstance(valor, date):
        return valor.strftime("%d/%m/%Y")
    if isinstance(valor, bool) or not isinstance(valor, (str, int, float)):
        raise ValueError("El valor debe ser texto, número finito o fecha.")
    if isinstance(valor, float) and not isfinite(valor):
        raise ValueError("El número debe ser finito.")
    text = str(valor)
    if any(ord(c) < 32 and c not in "\n\r\t" for c in text):
        raise ValueError("El texto contiene caracteres de control no admitidos.")
    if len(text) > 500:
        raise ValueError("El valor supera los 500 caracteres admitidos en el piloto.")
    return text


def _mapa(valor, nombre):
    if not isinstance(valor, Mapping):
        raise ValueError(f"{nombre} debe ser un diccionario.")
    return valor


def _carga(datos, spec):
    datos = _mapa(datos, "datos")
    if set(datos) - {"cabecera", "bloques", "observaciones"}:
        raise ValueError("La carga contiene apartados desconocidos.")
    cabecera = _mapa(datos.get("cabecera", {}), "cabecera")
    if set(cabecera) - CABECERA.keys():
        raise ValueError("La cabecera contiene campos desconocidos.")
    cambios = {CABECERA[k]: _texto(v) for k, v in cabecera.items()}
    if "sistema_designacion" in cabecera:
        cambios["A8"] = "SISTEMA / DESIGNACIÓN: " + cambios["A8"]
    bloques = _mapa(datos.get("bloques", {}), "bloques")
    if set(bloques) - {titulo for titulo, _ in spec["bloques"]}:
        raise ValueError("La carga contiene bloques desconocidos.")
    fila = 9
    for titulo, campos in spec["bloques"]:
        valores = _mapa(bloques.get(titulo, {}), titulo)
        nombres = {campo[0] if isinstance(campo, tuple) else campo for campo in campos}
        if set(valores) - nombres:
            raise ValueError(f"El bloque {titulo} contiene campos desconocidos.")
        fila += 1
        for campo in campos:
            etiqueta, opciones = campo if isinstance(campo, tuple) else (campo, None)
            if etiqueta in valores:
                text = _texto(valores[etiqueta])
                if isinstance(opciones, list):
                    if text not in opciones:
                        raise ValueError(f"Opción no admitida para {etiqueta}.")
                    text = "      ".join(f"{op}  {'☑' if op == text else '☐'}" for op in opciones)
                elif isinstance(opciones, str) and opciones:
                    text = f"{text}  {opciones}"
                cambios[f"J{fila}"] = text
            fila += 1
    observaciones = datos.get("observaciones", [])
    if not isinstance(observaciones, list) or len(observaciones) > 4:
        raise ValueError("observaciones debe ser una lista de hasta cuatro líneas.")
    for i, valor in enumerate(observaciones, 1):
        cambios[f"A{fila + i}"] = _texto(valor)
    return cambios


def generar_saa1(datos, destino):
    """Genera un Excel interno; rechaza campos ajenos y no sobrescribe archivos."""
    spec = definicion_saa1()
    cambios = _carga(datos, spec)
    return _generar_paquete(spec, cambios, destino)


def _generar_paquete(spec, cambios, destino):
    destino = Path(destino).resolve()
    if destino.suffix.lower() != ".xlsx":
        raise ValueError("El destino debe tener extensión .xlsx.")
    destino.parent.mkdir(parents=True, exist_ok=True)
    if destino.exists():
        raise FileExistsError(destino)
    build = runpy.run_path(str(HERRAMIENTAS / "build_planilla.py"))["build"]
    with TemporaryDirectory(prefix="saa1-", dir=destino.parent) as temporal:
        base = Path(temporal) / "base.xlsx"
        build(spec, str(base), str(MODELO))
        with ZipFile(base) as source:
            tree = etree.fromstring(source.read("xl/worksheets/sheet1.xml"))
            styles = etree.fromstring(source.read('xl/styles.xml'))
            from .impresion import ajustar_tabla, aplicar_identidad, destacar_resultados
            ajustar_tabla(tree)
            aplicar_identidad(styles)
            cambios = {'Q7' if address == 'R7' else address: value
                       for address, value in cambios.items()}
            destacar_resultados(tree, styles, cambios)
            for coordenada, valor in cambios.items():
                cell = tree.find(f".//{NS}c[@r='{coordenada}']")
                if cell is None:
                    raise RuntimeError(f"El kit cambió; no existe la celda {coordenada}.")
                for child in list(cell):
                    cell.remove(child)
                cell.set("t", "inlineStr")
                text = etree.SubElement(etree.SubElement(cell, NS + "is"), NS + "t")
                text.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                text.text = valor
            workbook = etree.fromstring(source.read('xl/workbook.xml'))
            from .impresion import preparar_impresion
            preparar_impresion(tree, workbook, titulos=[title for title, _ in spec['bloques']],
                               mantener_bloques=spec['tipo'] == 'checklist')
            filled = Path(temporal) / "cargada.xlsx"
            with ZipFile(filled, "w") as output:
                for entry in source.infolist():
                    data = (etree.tostring(tree) if entry.filename == 'xl/worksheets/sheet1.xml' else
                            etree.tostring(workbook) if entry.filename == 'xl/workbook.xml' else
                            etree.tostring(styles) if entry.filename == 'xl/styles.xml' else source.read(entry.filename))
                    output.writestr(entry, data)
            payload = filled.read_bytes()
    with destino.open("xb") as output:
        output.write(payload)
    return destino


def generar_multisistema(datos,destino,codigo):
    from .catalogo_completo import definiciones_habilitadas as definiciones_multisistema
    from .validacion import validar_datos
    definition=definiciones_multisistema().get(codigo)
    if definition is None:raise ValueError("Planilla no habilitada.")
    schema=definition['definicion'];data=validar_datos(datos,schema)
    changes={CABECERA[key]:_texto(date.fromisoformat(value) if key=='fecha' else value) for key,value in data['cabecera'].items()}
    if 'sistema_designacion' in data['cabecera']:changes['A8']='SISTEMA / DESIGNACIÓN: '+data['cabecera']['sistema_designacion']
    for title,fields in data['bloques'].items():
        for key,value in fields.items():
            field=schema['bloques'][title][key]
            if 'celdas_resultado' in field:
                changes[field['celdas_resultado'][value]]=value
            else:
                if field['tipo']=='fecha':value=date.fromisoformat(value)
                text=_texto(value)
                if field['tipo']=='opcion' and definition['especificacion']['tipo']=='general':
                    text='      '.join(f"{option}  {'☑' if option==value else '☐'}" for option in field['opciones'])
                if field.get('unidad'):text+='  '+field['unidad']
                changes[field['celda']]=text
    for index,value in enumerate(data['observaciones']):changes['A'+str(schema['fila_observaciones']+index)]=_texto(value) if value else ''
    return _generar_paquete(definition['especificacion'],changes,destino)
