"""Anexo A4 vectorial con fuente incrustada y JPEG original sin recodificar."""
import ast
from collections.abc import Mapping
from datetime import date, datetime
from functools import lru_cache
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import re

from PIL import Image, UnidentifiedImageError
from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError
from pypdf.generic import ArrayObject, DecodedStreamObject, DictionaryObject, EncodedStreamObject, NameObject, NumberObject
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

A4_PT = (210 * 72 / 25.4, 297 * 72 / 25.4)
MARGEN = 15 * 72 / 25.4
ANCHO_TEXTO = A4_PT[0] - 2 * MARGEN - 75
PIE_Y = A4_PT[1] - MARGEN - 10
LISTA_FIN = PIE_Y - 25
COLOR_MARCAS = "#D41120"
BORDE_BLANCO_PT = 2.5
ANILLO_OSCURO = "#1B2430"
ANILLO_OSCURO_PT = 0.8
RADIO_MARCA_PT = 9
TAMANIO_TEXTO = 11
INTERLINEADO = 15
CODIGOS = ("✓", "O", "X", "NA")
TEXTO_MAX = 140
SIGNIFICADOS = {"✓": "cumple", "O": "no cumple", "X": "no apreciable", "NA": "no aplicable"}


def ruta_fuente(fuente=None):
    result = Path(fuente) if fuente is not None else Path(__file__).resolve().parents[1] / "fuentes/IBMPlexSans[wdth,wght].ttf"
    if not result.is_file():
        raise ValueError("No se encontró IBM Plex Sans: revisá la fuente TrueType incluida en app/fuentes.")
    return result.resolve()


@lru_cache(maxsize=8)
def _registrar_fuente(path):
    name = "ReadyproofPlex_" + sha256(Path(path).read_bytes()).hexdigest()[:12]
    pdfmetrics.registerFont(TTFont(name, path))
    return name


class _Metrica:
    def __init__(self, name, size):
        self.name, self.size = name, size

    def getlength(self, text):
        return pdfmetrics.stringWidth(text, self.name, self.size)


def _lineas(texto, font, ancho):
    if ancho <= 0:
        raise ValueError("El ancho de las referencias debe ser mayor que cero.")
    result = []
    for paragraph in texto.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        if not paragraph:
            result.append("")
        while paragraph:
            size = 0
            while size < len(paragraph) and font.getlength(paragraph[:size + 1]) <= ancho:
                size += 1
            if not size:
                raise ValueError("El texto no cabe en el ancho disponible: aumentá el área de referencias.")
            if size < len(paragraph):
                space = paragraph.rfind(" ", 0, size)
                if space > 0:
                    size = space + 1
            result.append(paragraph[:size])
            paragraph = paragraph[size:]
    return result


def _observaciones(observaciones, font, ancho):
    if not isinstance(observaciones, list) or not observaciones:
        raise ValueError("La lista de observaciones está vacía: agregá al menos una referencia para generar el anexo.")
    rows, numbers = [], set()
    detalle_items = any(isinstance(row, dict) and row.get("item") is not None for row in observaciones)
    for row in observaciones:
        if not isinstance(row, dict):
            raise ValueError("Cada observación debe indicar número, código y texto.")
        number = row.get("numero")
        if isinstance(number, bool) or not isinstance(number, int) or number < 1 or number in numbers:
            raise ValueError("Los números de las observaciones deben ser enteros positivos, sin repetidos.")
        code, text = row.get("codigo"), row.get("texto", "")
        if code not in CODIGOS or not isinstance(text, str) or len(text) > TEXTO_MAX or "\x00" in text:
            raise ValueError("Corregí la referencia: código ✓, O, X o NA y texto de hasta 140 caracteres.")
        if code in ("O", "X") and not text.strip():
            raise ValueError(f"La observación {number} con código {code} requiere texto: completalo antes de generar el anexo.")
        visible = text
        if detalle_items:
            item = row.get("item")
            if item is not None and (not isinstance(item, dict) or not isinstance(item.get("texto"), str) or not item["texto"].strip() or "\x00" in item["texto"]):
                raise ValueError("El ítem debe incluir el texto de la planilla: volvé a elegirlo antes de generar el anexo.")
            visible = f"Ítem: {item['texto'] if item else '—'}\nCódigo: {code} ({SIGNIFICADOS[code]})\nObservación: {text or '—'}"
        lines = _lineas(visible, _Metrica(font, TAMANIO_TEXTO), ancho)
        rows.append(dict(numero=number, codigo=code, texto=text, detalle_item=detalle_items, lineas=lines, alto=max(1, len(lines))*INTERLINEADO+8))
        numbers.add(number)
    return sorted(rows, key=lambda row: row["numero"])


def calcular_altura_lista(observaciones, *, ancho=ANCHO_TEXTO, fuente=None):
    """Altura en puntos PDF, incluida la cabecera de columnas."""
    font = _registrar_fuente(str(ruta_fuente(fuente)))
    return 20 + sum(row["alto"] for row in _observaciones(observaciones, font, ancho))


def _foto(jpeg):
    if not isinstance(jpeg, bytes) or not jpeg:
        raise ValueError("La foto no existe: cargá una foto estandarizada antes de generar el anexo.")
    try:
        with Image.open(BytesIO(jpeg)) as photo:
            if photo.format != "JPEG" or photo.mode not in ("RGB", "L"):
                raise ValueError("Usá la foto JPEG RGB estandarizada de la app; el anexo no convierte ni recodifica imágenes.")
            if max(photo.size) > 1600:
                raise ValueError("La foto supera 1600 px: usá la versión estandarizada por la app.")
            size, mode = photo.size, photo.mode
            photo.verify()
            return size, mode
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as error:
        raise ValueError("No se pudo abrir la foto: volvé a cargar el JPEG estandarizado.") from error


def _marcas(marcas, rows):
    if not isinstance(marcas, list) or not marcas:
        raise ValueError("La lista de marcas está vacía: agregá al menos una marca antes de generar el anexo.")
    result = {}
    for mark in marcas:
        if not isinstance(mark, dict):
            raise ValueError("Cada marca debe indicar número y posición sobre la foto.")
        number = mark.get("numero")
        if isinstance(number, bool) or not isinstance(number, int) or number < 1 or number in result:
            raise ValueError("Los números de las marcas deben ser enteros positivos, sin repetidos.")
        for key in ("x", "y"):
            value = mark.get(key)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 1:
                raise ValueError("La posición de cada marca debe estar entre 0 y 1: revisá el marcado de la foto.")
        result[number] = mark
    if set(result) != {row["numero"] for row in rows}:
        raise ValueError("Las marcas y las referencias deben tener los mismos números: revisá la lista de observaciones.")
    return result


def origen_pie(configuracion=None, *, archivo_kit=None):
    """Lee el texto existente; no aporta texto normativo de respaldo."""
    config = configuracion or {}
    if "leyenda_iram" in config:
        leyenda, origen_leyenda = config["leyenda_iram"] or "", "configuracion.leyenda_iram"
    else:
        from ..planillas import leyenda_iram
        leyenda = getattr(leyenda_iram, "TEXTO", "")
        origen_leyenda = "app/planillas/leyenda_iram.py:TEXTO" if leyenda else "no encontrado"
    if "retencion" in config:
        retencion, origen_retencion = config["retencion"] or "", "configuracion.retencion"
    else:
        kit = Path(archivo_kit) if archivo_kit is not None else Path(__file__).resolve().parents[2] / "fuente/herramientas/build_planilla.py"
        try:
            tree = ast.parse(kit.read_text(encoding="utf-8-sig"))
            values = {node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, str) and re.fullmatch(r"T\.C\.\s+\d+\s+AÑOS", node.value)}
        except (OSError, SyntaxError):
            values = set()
        retencion = next(iter(values)) if len(values) == 1 else ""
        origen_retencion = str(kit) + ":cabecera" if retencion else "no encontrado"
    return " · ".join(value for value in (leyenda, retencion) if value), {"leyenda": origen_leyenda, "retencion": origen_retencion}


def datos_cabecera(carga=None):
    """Usa la identificación almacenada en la carga, sin completar por contexto de sesión."""
    value = carga if isinstance(carga, Mapping) else getattr(carga, "datos", {})
    datos = value.get("datos", value) if isinstance(value, Mapping) else {}
    cabecera = datos.get("cabecera", {}) if isinstance(datos, Mapping) else {}
    if not isinstance(cabecera, Mapping):
        cabecera = {}
    def text(value):
        return str(value).strip() if value is not None and str(value).strip() else "—"
    fecha = cabecera.get("fecha")
    if isinstance(fecha, (date, datetime)):
        fecha = fecha.strftime("%d/%m/%Y")
    elif isinstance(fecha, str):
        try:
            fecha = date.fromisoformat(fecha).strftime("%d/%m/%Y")
        except ValueError:
            pass
    return {"Cliente": text(cabecera.get("cliente")), "Equipo": text(cabecera.get("sistema_designacion")), "Técnico": text(cabecera.get("inspector")), "Fecha": text(fecha)}


def _texto(canvas, font, x, top, text, size=11):
    canvas.setFont(font, size)
    canvas.drawString(x, A4_PT[1] - top - size, text)


def _cabecera(canvas, font, campos):
    canvas.setFillColor(HexColor("#1D1D1B"))
    _texto(canvas, font, MARGEN, MARGEN, "ANEXO FOTOGRÁFICO", 17)
    top = MARGEN + 30
    width = (A4_PT[0] - 2*MARGEN - 20)/2
    for names in (("Cliente", "Equipo"), ("Técnico", "Fecha")):
        max_height = 0
        for index, name in enumerate(names):
            x = MARGEN + index*(width+20)
            lines = _lineas(campos[name], _Metrica(font, 10.5), width)
            _texto(canvas, font, x, top, name.upper(), 8)
            for offset, line in enumerate(lines):
                _texto(canvas, font, x, top+13+offset*13, line, 10.5)
            max_height = max(max_height, 13+len(lines)*13)
        top += max_height+8
    canvas.setStrokeColor(HexColor("#D41120"))
    canvas.setLineWidth(.8)
    canvas.line(MARGEN, A4_PT[1]-top, A4_PT[0]-MARGEN, A4_PT[1]-top)
    return top+12


def _check(canvas, font, x, top):
    # Copiar/buscar conserva U+2713; la forma visible es un trazo propio, no el glifo fino de Plex.
    y = A4_PT[1]-top-11
    text = canvas.beginText(x, y)
    text.setFont(font, 11)
    text.setTextRenderMode(3)
    text.textOut("✓")
    text.setTextRenderMode(0)
    canvas.drawText(text)
    canvas.setStrokeColor(HexColor("#1D1D1B"))
    canvas.setLineWidth(1.5)
    canvas.setLineCap(1)
    path = canvas.beginPath()
    path.moveTo(x+.5, y+4)
    path.lineTo(x+3.5, y+1)
    path.lineTo(x+10, y+9)
    canvas.drawPath(path)


def _insertar_jpeg(writer, jpeg, size, mode, box):
    page = writer.pages[0]
    image = EncodedStreamObject()
    image._data = jpeg
    image.update({NameObject("/Type"): NameObject("/XObject"), NameObject("/Subtype"): NameObject("/Image"), NameObject("/Filter"): NameObject("/DCTDecode"), NameObject("/Width"): NumberObject(size[0]), NameObject("/Height"): NumberObject(size[1]), NameObject("/ColorSpace"): NameObject("/DeviceRGB" if mode == "RGB" else "/DeviceGray"), NameObject("/BitsPerComponent"): NumberObject(8)})
    resource = page["/Resources"].get_object()
    images = DictionaryObject(dict(resource.get("/XObject", DictionaryObject()).get_object()))
    images[NameObject("/RPFOTO")] = writer._add_object(image)
    resource[NameObject("/XObject")] = images
    x, top, width, height = box
    stream = DecodedStreamObject()
    stream.set_data(f"q {width:.6f} 0 0 {height:.6f} {x:.6f} {A4_PT[1]-top-height:.6f} cm /RPFOTO Do Q\n".encode("ascii"))
    original = page.get("/Contents")
    resolved = original.get_object() if original is not None else None
    contents = list(resolved) if isinstance(resolved, ArrayObject) else [original] if original is not None else []
    page[NameObject("/Contents")] = ArrayObject([writer._add_object(stream), *contents])


def generar_anexo(jpeg, marcas, observaciones, *, fuente=None, carga=None, configuracion_planilla=None, permitir_sin_marcas=False):
    """Texto vectorial y fuente incrustada; la foto conserva todos sus bytes JPEG."""
    size, mode = _foto(jpeg)
    font = _registrar_fuente(str(ruta_fuente(fuente)))
    sin_marcas = permitir_sin_marcas and marcas == [] and observaciones == []
    rows = [] if sin_marcas else _observaciones(observaciones, font, ANCHO_TEXTO)
    points = {} if sin_marcas else _marcas(marcas, rows)
    campos = datos_cabecera(carga)
    pie, _ = origen_pie(configuracion_planilla)
    # Medir la cabecera con las mismas métricas usadas en el dibujo.
    scratch = Canvas(BytesIO(), pagesize=A4_PT, initialFontName=font)
    photo_top = _cabecera(scratch, font, campos)
    max_height = LISTA_FIN-photo_top-70
    if max_height < 100:
        raise ValueError("La cabecera ocupa demasiado espacio: revisá la identificación antes de generar el anexo.")
    ratio = min((A4_PT[0]-2*MARGEN)/size[0], max_height/size[1])
    width, height = size[0]*ratio, size[1]*ratio
    left = (A4_PT[0]-width)/2
    first_y = photo_top+height+14
    pages, current, y = [], [], first_y+20
    for row in rows:
        if y+row["alto"] > LISTA_FIN:
            pages.append(current)
            current, y = [], photo_top+20
        if y+row["alto"] > LISTA_FIN:
            raise ValueError("La referencia no cabe en una hoja: revisá el texto de la observación.")
        current.append(row)
        y += row["alto"]
    pages.append(current)
    buffer = BytesIO()
    canvas = Canvas(buffer, pagesize=A4_PT, initialFontName=font, initialFontSize=11, pageCompression=1)
    canvas.setTitle("Anexo fotográfico")
    canvas.setAuthor("readyproof")
    for index, references in enumerate(pages):
        _cabecera(canvas, font, campos)
        y = first_y if index == 0 else photo_top
        if index == 0:
            for number, mark in points.items():
                x, cy = left+mark["x"]*width, A4_PT[1]-photo_top-mark["y"]*height
                canvas.setFillColor(HexColor(COLOR_MARCAS))
                canvas.setStrokeColor(HexColor("#FFFFFF"))
                canvas.setLineWidth(BORDE_BLANCO_PT)
                canvas.circle(x, cy, RADIO_MARCA_PT, fill=1, stroke=1)
                canvas.setStrokeColor(HexColor(ANILLO_OSCURO))
                canvas.setLineWidth(ANILLO_OSCURO_PT)
                # Anillo tangente al borde blanco: no reduce su espesor visible.
                exterior = RADIO_MARCA_PT + BORDE_BLANCO_PT/2 + ANILLO_OSCURO_PT/2
                canvas.circle(x, cy, exterior, fill=0, stroke=1)
                canvas.setFillColor(HexColor("#FFFFFF"))
                text = str(number)
                font_size = 11
                while pdfmetrics.stringWidth(text, font, font_size)>14 and font_size>5:
                    font_size -= 1
                canvas.setFont(font, font_size)
                canvas.drawCentredString(x, cy-font_size*.33, text)
        canvas.setFillColor(HexColor("#1D1D1B"))
        if references:
            titulos = ((MARGEN,"N.°"),(MARGEN+75,"Ítem, código y observación")) if references[0]["detalle_item"] else ((MARGEN,"N.°"),(MARGEN+25,"Código"),(MARGEN+75,"Observación"))
            for x, title in titulos:
                _texto(canvas,font,x,y,title,9)
            y += 20
            for row in references:
                _texto(canvas,font,MARGEN,y,str(row["numero"]))
                if not row["detalle_item"]:
                    if row["codigo"] == "✓":
                        _check(canvas,font,MARGEN+25,y)
                    else:
                        _texto(canvas,font,MARGEN+25,y,row["codigo"])
                for offset, line in enumerate(row["lineas"]):
                    top=y+offset*INTERLINEADO
                    if row["detalle_item"] and line.startswith("Código: ✓"):
                        x=MARGEN+75
                        _texto(canvas,font,x,top,"Código: ")
                        x+=pdfmetrics.stringWidth("Código: ",font,TAMANIO_TEXTO)
                        _check(canvas,font,x,top)
                        _texto(canvas,font,x+12,top," (cumple)")
                    else:
                        _texto(canvas,font,MARGEN+75,top,line)
                y += row["alto"]
        else:
            _texto(canvas,font,MARGEN,y,"Sin marcas registradas." if sin_marcas else "Referencias en la página siguiente.",10)
        canvas.setFillColor(HexColor("#555555"))
        if pie:
            pie_lines = _lineas(pie, _Metrica(font,8), A4_PT[0]-2*MARGEN-65)
            if len(pie_lines)>2:
                raise ValueError("El pie configurado es demasiado extenso: revisá la configuración de planilla.")
            for offset,line in enumerate(pie_lines):
                _texto(canvas,font,MARGEN,PIE_Y+offset*10,line,8)
        canvas.setFont(font,8)
        canvas.drawRightString(A4_PT[0]-MARGEN,A4_PT[1]-PIE_Y-8,f"Pág. {index+1} de {len(pages)}")
        canvas.showPage()
    canvas.save()
    writer = PdfWriter()
    writer.clone_document_from_reader(PdfReader(BytesIO(buffer.getvalue())))
    _insertar_jpeg(writer,jpeg,size,mode,(left,photo_top,width,height))
    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def unir_pdf(planilla_pdf, anexo_pdf):
    """Planilla primero, anexo después; devuelve un PDF nuevo en memoria."""
    writer = PdfWriter()
    for data, nombre in ((planilla_pdf,"planilla"),(anexo_pdf,"anexo")):
        if not isinstance(data,bytes) or not data:
            raise ValueError(f"Falta el PDF de {nombre}: generá ambos documentos antes de unirlos.")
        try:
            reader = PdfReader(BytesIO(data))
            if reader.is_encrypted or not reader.pages:
                raise ValueError(f"El PDF de {nombre} está protegido o vacío: usá un PDF legible.")
            writer.append(reader)
        except (PdfReadError,OSError,TypeError) as error:
            raise ValueError(f"No se pudo abrir el PDF de {nombre}: revisá el documento antes de unirlo.") from error
    output = BytesIO()
    writer.write(output)
    return output.getvalue()
