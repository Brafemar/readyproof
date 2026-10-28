"""Firmas de prueba en PNG y su incorporación en los espacios del original."""
import base64
import binascii
from io import BytesIO
from math import isfinite
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, DecodedStreamObject, DictionaryObject, NameObject

from .encabezado_pdf import _imagen_pdf
from .validacion import DatosInvalidos, mapa, campos_permitidos

ROLES = ("tecnico", "responsable")
ETIQUETAS = {"tecnico": "SUPERVISOR DEL MANTENEDOR", "responsable": "RESPONSABLE DE LA INSTALACIÓN"}


def logo_readyproof():
    path=Path(__file__).resolve().parents[1]/"static"/"logo_readyproof.png"
    payload=path.read_bytes()
    with Image.open(BytesIO(payload)) as image:
        if image.format!="PNG" or image.width<600 or image.height<150:
            raise RuntimeError("El logo readyproof debe ser un PNG completo con resolución suficiente.")
        image.verify()
    return payload


def validar_firmas(value):
    value = mapa(value, "firmas")
    campos_permitidos(value, ROLES, "firmas")
    result = {}
    for role, encoded in value.items():
        if encoded is None:
            result[role] = None
            continue
        if not isinstance(encoded, str) or not encoded.startswith("data:image/png;base64,") or len(encoded) > 280000:
            raise DatosInvalidos("La firma debe ser un PNG de hasta 200 KB.")
        try:
            payload = base64.b64decode(encoded.split(",", 1)[1], validate=True)
            if len(payload) > 200000:
                raise ValueError("tamaño")
            with Image.open(BytesIO(payload)) as image:
                if image.format != "PNG" or not (10 <= image.width <= 1200 and 10 <= image.height <= 500) or getattr(image, "n_frames", 1) != 1:
                    raise ValueError("dimensiones")
                image.load()
                rgba = image.convert("RGBA")
                background = Image.new("RGB", rgba.size, "white")
                background.paste(rgba, mask=rgba.getchannel("A"))
                if all(low == high == 255 for low, high in background.getextrema()):
                    raise ValueError("vacía")
                output = BytesIO()
                rgba.save(output, format="PNG")
                result[role] = output.getvalue()
        except (ValueError, OSError, binascii.Error, Image.DecompressionBombError):
            raise DatosInvalidos("Firma inválida: debe contener trazos en un PNG de prueba válido.") from None
    return result


def incorporar_firmas(excel, pdf, destino, firmas):
    workbook = load_workbook(excel)
    sheet = workbook.active
    boxes = {}
    widths = [sheet.column_dimensions[get_column_letter(i)].width for i in range(1, sheet.max_column + 1)]
    header_fractions = {}
    for row in sheet:
        for cell in row:
            if not isinstance(cell.value, str):
                continue
            if cell.value in {"CLIENTE:", "TELÉFONO:"}:
                header_fractions[cell.value] = sum(widths[:cell.column - 1]) / sum(widths)
            for role, label in ETIQUETAS.items():
                if cell.value.startswith(label) and "FIRMA" in cell.value:
                    merged = next(r for r in sheet.merged_cells.ranges if r.min_row < cell.row and r.max_row == cell.row - 1 and r.min_col == cell.column)
                    boxes[role] = (cell.value, sum(widths[:merged.min_col - 1]) / sum(widths), sum(widths[merged.min_col - 1:merged.max_col]) / sum(widths), sum(sheet.row_dimensions[i].height or 15 for i in range(merged.min_row, merged.max_row + 1)), cell.font.sz)
    margins = sheet.page_margins
    workbook.close()
    reader = PdfReader(pdf)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    found = set()
    for page_index, page in enumerate(writer.pages):
        anchors = {}
        header = {}
        def visitor(text, cm, tm, font, size):
            if text.strip() in {"CLIENTE:", "TELÉFONO:"}:
                header[text.strip()] = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
            for role, box in boxes.items():
                if box[0] in text:
                    y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
                    anchors[role] = (y, size)
        page.extract_text(visitor_text=visitor)
        if not anchors:
            continue
        for role, payload in firmas.items():
            if not payload or role not in anchors:
                continue
            _, left_fraction, width_fraction, height_rows, font_original = boxes[role]
            y, font_actual = anchors[role]
            scale = font_actual / font_original
            available = float(page.mediabox.width) - (margins.left + margins.right) * 72
            table_left = margins.left * 72
            if set(header) == set(header_fractions) == {"CLIENTE:", "TELÉFONO:"}:
                # Ambas etiquetas tienen el mismo margen de celda; su separación fija el ancho impreso.
                available = (header["TELÉFONO:"] - header["CLIENTE:"]) / (header_fractions["TELÉFONO:"] - header_fractions["CLIENTE:"])
                table_left = header["CLIENTE:"] - available * header_fractions["CLIENTE:"]
            x = table_left + available * left_fraction + 5
            bottom = y + font_actual * 1.2
            width = available * width_fraction - 10
            # Un casillero puede continuar desde la página anterior; usar solo su parte visible.
            table_top = float(page.mediabox.height) - margins.top * 72
            full_height = height_rows * scale - 6
            height = min(full_height, table_top - bottom - 3)
            target = page
            if page_index and height < full_height:
                previous_page = writer.pages[page_index - 1]
                legends = []
                def previous_text(text, cm, tm, font, size):
                    if "CUMPLE:" in text:
                        legends.append((tm[4] * cm[1] + tm[5] * cm[3] + cm[5], size))
                previous_page.extract_text(visitor_text=previous_text)
                if legends:
                    legend_y, legend_size = min(legends)
                    previous_bottom = margins.bottom * 72 + 3
                    previous_height = min(full_height, legend_y - legend_size * .75 - previous_bottom)
                    if previous_height > height:
                        target = previous_page;bottom = previous_bottom;height = previous_height
            with Image.open(BytesIO(payload)) as image:
                ratio = min(width / image.width, height / image.height)
                iw, ih = image.width * ratio, image.height * ratio
            if not all(isfinite(v) and v > 0 for v in (iw, ih, width, height)):
                raise RuntimeError("No se pudo ubicar la firma en el espacio original.")
            _pegar_firma(writer,target,role,payload,x+(width-iw)/2,bottom+(height-ih)/2,iw,ih)
            found.add(role)
    if set(role for role, value in firmas.items() if value) - found:
        raise RuntimeError("No se encontró el espacio de firma de la planilla.")
    with open(destino, "xb") as output:
        writer.write(output)


def _pegar_firma(writer,page,role,payload,x,y,width,height):
    resources=DictionaryObject(dict(page["/Resources"].get_object()))
    objects=DictionaryObject(dict(resources.get("/XObject",DictionaryObject()).get_object()))
    resources[NameObject("/XObject")]=objects;page[NameObject("/Resources")]=resources
    name=NameObject("/Firma_"+role)
    objects[name]=_imagen_pdf(payload,writer)
    stream=DecodedStreamObject()
    stream.set_data(f"q {width:.5f} 0 0 {height:.5f} {x:.5f} {y:.5f} cm {name} Do Q\n".encode("ascii"))
    original=page.get("/Contents");resolved=original.get_object() if original is not None else None
    contents=ArrayObject(list(resolved) if isinstance(resolved,ArrayObject) else [original] if original is not None else [])
    contents.append(writer._add_object(stream));page[NameObject("/Contents")]=contents
