"""Restituye en el PDF las imágenes VML omitidas por LibreOffice."""
from io import BytesIO
from pathlib import PurePosixPath
import posixpath
import re
from zipfile import ZipFile

from lxml import etree
from openpyxl import load_workbook
from PIL import Image
from pypdf import PdfReader, PdfWriter

from .impresion import es_planilla_sdi
from pypdf.generic import (
    ArrayObject, DecodedStreamObject, DictionaryObject, NameObject, NumberObject,
)

S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
P = "{http://schemas.openxmlformats.org/package/2006/relationships}"
V = "{urn:schemas-microsoft-com:vml}"
O = "{urn:schemas-microsoft-com:office:office}"


def _xml(payload):
    return etree.fromstring(payload, parser=etree.XMLParser(resolve_entities=False, no_network=True))


def _ruta(base, target):
    return posixpath.normpath(posixpath.join(posixpath.dirname(base), target))


def _rels(archive, part):
    path = PurePosixPath(part)
    name = str(path.parent / "_rels" / (path.name + ".rels"))
    return {e.get("Id"): e.get("Target") for e in _xml(archive.read(name)).findall(P + "Relationship")}


def _pt(value):
    if not re.fullmatch(r"\d+(?:\.\d+)?pt", value):
        raise ValueError("La dimensión del logo no está expresada en puntos.")
    return float(value[:-2])


def logos_del_excel(origen):
    """Lee imágenes, anclas y medidas de la primera hoja del Excel del kit."""
    with ZipFile(origen) as archive:
        part = "xl/worksheets/sheet1.xml"
        sheet = _xml(archive.read(part))
        drawing = sheet.find(S + "legacyDrawingHF")
        if drawing is None:
            return [], {}
        margins = {key: float(value) * 72 for key, value in sheet.find(S + "pageMargins").attrib.items()}
        vml = _ruta(part, _rels(archive, part)[drawing.get(R + "id")])
        relationships = _rels(archive, vml)
        logos = []
        for shape in _xml(archive.read(vml)).findall(V + "shape"):
            anchor = shape.get("id")
            if anchor not in {"LH", "RH", "CH"}:
                raise ValueError(f"Ancla de encabezado no admitida: {anchor}.")
            style = dict(item.strip().split(":", 1) for item in shape.get("style").split(";") if ":" in item)
            width, height = _pt(style["width"]), _pt(style["height"])
            relation = shape.find(V + "imagedata").get(O + "relid")
            image = archive.read(_ruta(vml, relationships[relation]))
            logos.append((anchor, width, height, image))
        return logos, margins


def _imagen_pdf(payload, writer):
    with Image.open(BytesIO(payload)) as original:
        rgba = original.convert("RGBA")
        rgb = Image.new("RGB", rgba.size, "white")
        rgb.paste(rgba, mask=rgba.getchannel("A"))
        obj = DecodedStreamObject()
        obj.set_data(rgb.tobytes())
        obj.update({
            NameObject("/Type"): NameObject("/XObject"),
            NameObject("/Subtype"): NameObject("/Image"),
            NameObject("/Width"): NumberObject(rgb.width),
            NameObject("/Height"): NumberObject(rgb.height),
            NameObject("/ColorSpace"): NameObject("/DeviceRGB"),
            NameObject("/BitsPerComponent"): NumberObject(8),
        })
    return writer._add_object(obj.flate_encode())



def codigo_de_planilla(origen_excel):
    """Obtiene el código de la celda original del encabezado, sin alterar el Excel."""
    workbook = load_workbook(origen_excel, read_only=True, data_only=True)
    try:
        codigo = workbook.active["T1"].value
    finally:
        workbook.close()
    if not isinstance(codigo, str) or not codigo.strip():
        raise ValueError("El Excel no contiene un código de planilla en el encabezado.")
    return codigo.strip()


def reponer_logos(origen_excel, origen_pdf, destino_pdf, *, logo_izquierdo=None):
    """Usa las medidas del Excel; no cambia filas, escala ni contenido del PDF."""
    logos, margins = logos_del_excel(origen_excel)
    if logo_izquierdo is not None:
        if sum(anchor=="LH" for anchor,_,_,_ in logos)!=1:
            raise RuntimeError("No hay un único espacio izquierdo para el logo readyproof.")
        logos=[(anchor,width,height,logo_izquierdo if anchor=="LH" else payload) for anchor,width,height,payload in logos]
    reader = PdfReader(origen_pdf)
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    codigo = codigo_de_planilla(origen_excel)
    sdi = es_planilla_sdi(codigo)
    writer.add_metadata({"/Title": codigo, "/Author": "readyproof", "/Creator": "readyproof", "/Producer": "readyproof"})
    refs = [_imagen_pdf(logo[3], writer) for logo in logos]
    for page in writer.pages:
        if logos and list(page.images):
            raise RuntimeError("LibreOffice ya exportó imágenes; revisar el encabezado antes de superponer logos.")
        original_resources = page.get("/Resources")
        resources = DictionaryObject(dict(original_resources.get_object()) if original_resources is not None else {})
        page[NameObject("/Resources")] = resources
        original_xobjects = resources.get("/XObject")
        xobjects = DictionaryObject(dict(original_xobjects.get_object()) if original_xobjects is not None else {})
        resources[NameObject("/XObject")] = xobjects
        commands = []
        for i, ((anchor, width, height, _), reference) in enumerate(zip(logos, refs)):
            name = NameObject(f"/RPLogo{i}")
            if name in xobjects:
                raise RuntimeError("El PDF ya contiene una imagen con el identificador reservado del encabezado.")
            xobjects[name] = reference
            page_width, page_height = float(page.mediabox.width), float(page.mediabox.height)
            if anchor == "RH":
                iso_height = (63 if sdi else 72) if logo_izquierdo is not None else min(height, 32)
                width, height = width * iso_height / height, iso_height
            if anchor == "LH" and logo_izquierdo is not None:
                with Image.open(BytesIO(logo_izquierdo)) as image:
                    width = 122 if sdi else 140
                    height = width * image.height / image.width
            x = margins["left"] if anchor == "LH" else (page_width - margins["right"] - width if anchor == "RH" else (page_width - width) / 2)
            header = margins["header"]
            if not sdi and anchor == "LH" and logo_izquierdo is not None:
                header = min(header, 8)
            y = page_height - header - height
            commands.append(f"q {width:.5f} 0 0 {height:.5f} {x:.5f} {y:.5f} cm {name} Do Q\n")
        if commands:
            content = DecodedStreamObject()
            content.set_data("".join(commands).encode("ascii"))
            content_ref = writer._add_object(content)
            old = page.get("/Contents")
            resolved = old.get_object() if old is not None else None
            contents = ArrayObject(list(resolved) if isinstance(resolved, ArrayObject) else ([old] if old is not None else []))
            contents.append(content_ref)
            page[NameObject("/Contents")] = contents
    with open(destino_pdf, "xb") as stream:
        writer.write(stream)
