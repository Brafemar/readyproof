"""Leyenda confirmada por Martín y pie reservado con autorización de Jorge."""
from pypdf import PdfReader,PdfWriter,Transformation
from pypdf.generic import ArrayObject,DecodedStreamObject,DictionaryObject,NameObject

TEXTO="Planilla conforme a IRAM 3546:2011"
TAMANIO=8
GRIS=0.5
PIE_PT=10*72/25.4
ESCALA_CONTENIDO=0.95
METRICAS_HELVETICA={' ': 278, '0': 556, '1': 556, '2': 556, '3': 556, '4': 556, '5': 556, '6': 556, ':': 278, 'A': 667, 'I': 278, 'M': 833, 'P': 667, 'R': 722, 'a': 556, 'c': 500, 'e': 556, 'f': 278, 'i': 222, 'l': 222, 'm': 833, 'n': 556, 'o': 556, 'r': 333}


def ancho_leyenda():
    return sum(METRICAS_HELVETICA[c] for c in TEXTO)*TAMANIO/1000


def incorporar_leyenda_iram(origen,destino):
    reader=PdfReader(origen)
    if reader.metadata and reader.metadata.get("/ReadyproofIRAM")==TEXTO:
        raise RuntimeError("El PDF ya contiene la leyenda IRAM; no se aplica dos veces.")
    writer=PdfWriter();writer.clone_document_from_reader(reader)
    font=DictionaryObject({NameObject("/Type"):NameObject("/Font"),NameObject("/Subtype"):NameObject("/Type1"),NameObject("/BaseFont"):NameObject("/Helvetica"),NameObject("/Encoding"):NameObject("/WinAnsiEncoding")})
    font_ref=writer._add_object(font)
    for page in writer.pages:
        width,height=float(page.mediabox.width),float(page.mediabox.height)
        transform=Transformation().scale(ESCALA_CONTENIDO).translate((1-ESCALA_CONTENIDO)*width/2,(1-ESCALA_CONTENIDO)*(height-8))
        page.add_transformation(transform)
        resources=DictionaryObject(dict(page["/Resources"].get_object()));page[NameObject("/Resources")]=resources
        fonts=DictionaryObject(dict(resources.get("/Font",DictionaryObject()).get_object()))
        if "/RPIRAM" in fonts:raise RuntimeError("El PDF ya tiene un recurso reservado para la leyenda.")
        fonts[NameObject("/RPIRAM")]=font_ref;resources[NameObject("/Font")]=fonts
        x=(width-ancho_leyenda())/2
        commands=f"q {GRIS} g BT /RPIRAM {TAMANIO} Tf 1 0 0 1 {x:.6f} {PIE_PT:.6f} Tm <{TEXTO.encode('cp1252').hex()}> Tj ET Q\n"
        stream=DecodedStreamObject();stream.set_data(commands.encode("ascii"))
        original=page.get("/Contents");resolved=original.get_object() if original is not None else None
        contents=ArrayObject(list(resolved) if isinstance(resolved,ArrayObject) else [original] if original is not None else [])
        contents.append(writer._add_object(stream));page[NameObject("/Contents")]=contents
    writer.add_metadata({"/ReadyproofIRAM":TEXTO,"/ReadyproofAjustePie":"escala proporcional 0.95; pie 10 mm; Helvetica 8 pt; gris 50%; todas las páginas"})
    with open(destino,"xb") as output:writer.write(output)
