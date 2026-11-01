"""Anexo A4 independiente: páginas rasterizadas con Pillow y unión con pypdf."""
from functools import lru_cache
from io import BytesIO
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError

DPI = 150
A4_PT = (210 * 72 / 25.4, 297 * 72 / 25.4)
PAGINA_PX = tuple(round(value * DPI / 72) for value in A4_PT)
MARGEN = round(15 * DPI / 25.4)
FOTO_Y = MARGEN + 105
FOTO_ALTO_MAX = 1260
PIE_Y = PAGINA_PX[1] - MARGEN - 30
LISTA_FIN = PIE_Y - 28
COLUMNA_TEXTO = 155
ANCHO_TEXTO = PAGINA_PX[0] - 2 * MARGEN - COLUMNA_TEXTO
CODIGOS = ("✓", "O", "X", "NA")
TEXTO_MAX = 140


def ruta_fuente(fuente=None):
    """Prefiere la fuente distribuida; no copia ni redistribuye Arial."""
    if fuente is not None:
        result = Path(fuente)
    else:
        result = Path(__file__).resolve().parents[1] / "fuentes/IBMPlexSans[wdth,wght].ttf"
        if not result.is_file():
            result = Path(os.environ.get("SystemRoot", "C:/Windows")) / "Fonts/arial.ttf"
    if not result.is_file():
        raise ValueError("No se encontró la fuente TrueType del anexo: configurá una fuente disponible antes de generar el PDF.")
    return result.resolve()


@lru_cache(maxsize=24)
def _fuente(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError as error:
        raise ValueError("No se pudo abrir la fuente del anexo: revisá el archivo TrueType.") from error


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

def _observaciones(observaciones, path, ancho):
    if not isinstance(observaciones, list) or not observaciones:
        raise ValueError("La lista de observaciones está vacía: agregá al menos una referencia para generar el anexo.")
    font = _fuente(path, 24)
    linea = sum(font.getmetrics()) + 3
    result, numbers = [], set()
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
        lines = _lineas(text, font, ancho)
        result.append(dict(numero=number, codigo=code, texto=text, lineas=lines, alto=max(1, len(lines)) * linea + 20))
        numbers.add(number)
    return sorted(result, key=lambda row: row["numero"]), linea


def calcular_altura_lista(observaciones, *, ancho=ANCHO_TEXTO, fuente=None):
    """Altura en píxeles a 150 dpi, incluida la cabecera de columnas."""
    rows, _ = _observaciones(observaciones, str(ruta_fuente(fuente)), ancho)
    return 42 + sum(row["alto"] for row in rows)


def _foto(jpeg):
    if not isinstance(jpeg, bytes) or not jpeg:
        raise ValueError("La foto no existe: cargá una foto estandarizada antes de generar el anexo.")
    try:
        with Image.open(BytesIO(jpeg)) as image:
            if image.format != "JPEG":
                raise ValueError("La foto debe ser el JPEG estandarizado de la carga.")
            image.load()
            if max(image.size) > 1600:
                raise ValueError("La foto supera 1600 px: usá la versión estandarizada por la app.")
            return image.convert("RGB")
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

def _paginar(rows, first_y):
    pages, current, y = [], [], first_y + 42
    for row in rows:
        if y + row["alto"] > LISTA_FIN:
            pages.append(current)
            current, y = [], MARGEN + 105 + 42
        if y + row["alto"] > LISTA_FIN:
            raise ValueError("Una observación no cabe en una hoja: revisá el texto antes de generar el anexo.")
        current.append(row)
        y += row["alto"]
    pages.append(current)
    return pages


def generar_anexo(jpeg, marcas, observaciones, *, fuente=None):
    """Devuelve bytes PDF A4; no emite ni altera la planilla original."""
    path = str(ruta_fuente(fuente))
    photo = _foto(jpeg)
    rows, line = _observaciones(observaciones, path, ANCHO_TEXTO)
    points = _marcas(marcas, rows)
    ratio = min((PAGINA_PX[0] - 2 * MARGEN) / photo.width, FOTO_ALTO_MAX / photo.height)
    size = tuple(max(1, round(value * ratio)) for value in photo.size)
    photo = photo.resize(size, Image.Resampling.LANCZOS)
    left = (PAGINA_PX[0] - photo.width) // 2
    first_y = FOTO_Y + photo.height + 28
    pages = _paginar(rows, first_y)
    writer = PdfWriter()
    for index, references in enumerate(pages):
        page = Image.new("RGB", PAGINA_PX, "white")
        draw = ImageDraw.Draw(page)
        draw.text((MARGEN, MARGEN), "ANEXO FOTOGRÁFICO", font=_fuente(path, 34), fill="#1d1d1b")
        draw.text((MARGEN, MARGEN + 48), "Foto y referencias" if index == 0 else "Referencias (continuación)", font=_fuente(path, 23), fill="#444444")
        draw.line((MARGEN, MARGEN + 88, PAGINA_PX[0] - MARGEN, MARGEN + 88), fill="#d41120", width=3)
        y = first_y if index == 0 else MARGEN + 105
        if index == 0:
            page.paste(photo, (left, FOTO_Y))
            for number, mark in points.items():
                x = left + round(mark["x"] * photo.width)
                cy = FOTO_Y + round(mark["y"] * photo.height)
                draw.ellipse((x-20, cy-20, x+20, cy+20), fill="#1d1d1b", outline="white", width=3)
                draw.ellipse((x-22, cy-22, x+22, cy+22), outline="#1d1d1b", width=1)
                font_size = 26
                while _fuente(path, font_size).getlength(str(number)) > 31 and font_size > 8:
                    font_size -= 1
                draw.text((x, cy), str(number), font=_fuente(path, font_size), anchor="mm", fill="white")
        if references:
            for x, title in ((MARGEN, "N.°"), (MARGEN + 54, "Código"), (MARGEN + COLUMNA_TEXTO, "Observación")):
                draw.text((x, y), title, font=_fuente(path, 20), fill="#555555")
            y += 42
            for row in references:
                draw.text((MARGEN, y), str(row["numero"]), font=_fuente(path, 24), fill="#1d1d1b")
                draw.text((MARGEN + 54, y), row["codigo"], font=_fuente(path, 24), fill="#1d1d1b")
                for offset, text in enumerate(row["lineas"]):
                    draw.text((MARGEN + COLUMNA_TEXTO, y + offset * line), text, font=_fuente(path, 24), fill="#1d1d1b")
                y += row["alto"]
        else:
            draw.text((MARGEN, y), "Referencias en la página siguiente.", font=_fuente(path, 22), fill="#444444")
        draw.line((MARGEN, PIE_Y - 10, PAGINA_PX[0] - MARGEN, PIE_Y - 10), fill="#cccccc", width=1)
        draw.text((MARGEN, PIE_Y), "Planilla conforme a IRAM 3546:2011 · T.C. 3 AÑOS", font=_fuente(path, 18), fill="#555555")
        draw.text((PAGINA_PX[0]-MARGEN, PIE_Y), f"Pág. {index+1} de {len(pages)}", font=_fuente(path, 18), anchor="ra", fill="#555555")
        buffer = BytesIO()
        page.save(buffer, format="PDF", resolution=DPI, title="Anexo fotográfico", author="readyproof")
        pdf_page = writer.add_page(PdfReader(BytesIO(buffer.getvalue())).pages[0])
        pdf_page.scale_to(*A4_PT)
    writer.add_metadata({"/Title": "Anexo fotográfico", "/Author": "readyproof"})
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

