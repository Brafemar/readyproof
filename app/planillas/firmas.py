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
    for row in sheet:
        for cell in row:
            if not isinstance(cell.value, str):
                continue
            for role, label in ETIQUETAS.items():
                if cell.value.startswith(label) and "FIRMA" in cell.value:
                    merged = next(r for r in sheet.merged_cells.ranges if r.min_row < cell.row and r.max_row == cell.row - 1 and r.min_col == cell.column)
                    widths = [sheet.column_dimensions[get_column_letter(i)].width for i in range(1, sheet.max_column + 1)]
                    boxes[role] = (cell.value, sum(widths[:merged.min_col - 1]) / sum(widths), sum(widths[merged.min_col - 1:merged.max_col]) / sum(widths), sum(sheet.row_dimensions[i].height or 15 for i in range(merged.min_row, merged.max_row + 1)), cell.font.sz)
    margins = sheet.page_margins
    workbook.close()
    reader = PdfReader(pdf)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    found = set()
    for page in writer.pages:
        anchors = {}
        def visitor(text, cm, tm, font, size):
            for role, box in boxes.items():
                if box[0] in text:
                    y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
                    anchors[role] = (y, size)
        page.extract_text(visitor_text=visitor)
        if not anchors:
            continue
        resources = DictionaryObject(dict(page["/Resources"].get_object()))
        objects = DictionaryObject(dict(resources.get("/XObject", DictionaryObject()).get_object()))
        resources[NameObject("/XObject")] = objects
        page[NameObject("/Resources")] = resources
        commands = []
        for role, payload in firmas.items():
            if not payload or role not in anchors:
                continue
            _, left_fraction, width_fraction, height_rows, font_original = boxes[role]
            y, font_actual = anchors[role]
            scale = font_actual / font_original
            available = float(page.mediabox.width) - (margins.left + margins.right) * 72
            x = margins.left * 72 + available * left_fraction + 5
            bottom = y + font_actual * 1.2
            width, height = available * width_fraction - 10, height_rows * scale - 6
            with Image.open(BytesIO(payload)) as image:
                ratio = min(width / image.width, height / image.height)
                iw, ih = image.width * ratio, image.height * ratio
            if not all(isfinite(v) and v > 0 for v in (iw, ih, width, height)):
                raise RuntimeError("No se pudo ubicar la firma en el espacio original.")
            name = NameObject("/Firma_" + role)
            objects[name] = _imagen_pdf(payload, writer)
            commands.append(f"q {iw:.5f} 0 0 {ih:.5f} {x + (width - iw) / 2:.5f} {bottom + (height - ih) / 2:.5f} cm {name} Do Q\n")
            found.add(role)
        if commands:
            stream = DecodedStreamObject()
            stream.set_data("".join(commands).encode("ascii"))
            original = page.get("/Contents")
            resolved = original.get_object() if original is not None else None
            contents = ArrayObject(list(resolved) if isinstance(resolved, ArrayObject) else ([original] if original else []))
            contents.append(writer._add_object(stream))
            page[NameObject("/Contents")] = contents
    if set(role for role, value in firmas.items() if value) - found:
        raise RuntimeError("No se encontró el espacio de firma de la planilla.")
    with open(destino, "xb") as output:
        writer.write(output)
