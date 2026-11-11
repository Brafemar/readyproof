"""Compone una propuesta de certificado sobre la plantilla aprobada."""
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from ..fotos.anexo_pdf import _numerar_documento
from ..planillas.validacion import DatosInvalidos

PLANTILLA = Path(__file__).with_name("plantilla_propuesta.pdf")


def separar_documentos(documentos):
    planillas, anexos = [], []
    for datos in documentos:
        lector = PdfReader(BytesIO(datos))
        if lector.is_encrypted or not lector.pages:
            raise DatosInvalidos("La planilla de respaldo no contiene un PDF legible.")
        en_anexo = False
        for page in lector.pages:
            en_anexo |= "ANEXO FOTOGRÁFICO" in (page.extract_text() or "").splitlines()
            (anexos if en_anexo else planillas).append(page)
    return planillas, anexos


def generar_propuesta(documentos, filas, ficha, *, firma=None):
    planillas, anexos = separar_documentos(documentos)
    escritor = PdfWriter()
    for page in planillas + anexos:
        escritor.add_page(page)
    certificado = escritor.add_page(PdfReader(PLANTILLA).pages[0])
    capa = BytesIO()
    lienzo = canvas.Canvas(capa, pagesize=(float(certificado.mediabox.width), float(certificado.mediabox.height)))

    def linea(x, y, texto, ancho, *, puntos=9, negrita=False, blanco=False):
        fuente = "Helvetica-Bold" if negrita else "Helvetica"
        texto = str(texto)
        medida = lienzo.stringWidth(texto, fuente, puntos)
        escala = min(1, ancho / medida) if medida else 1
        if puntos * escala < 7:
            raise DatosInvalidos("Un campo del certificado es demasiado largo para la propuesta A4.")
        lienzo.setFont(fuente, puntos * escala)
        lienzo.setFillColorRGB(*( (1, 1, 1) if blanco else (.114, .114, .106) ))
        lienzo.drawString(x, y, texto)

    fecha = ficha["fecha"].strftime("%d/%m/%Y")
    for i, fila in enumerate(filas):
        y = 370 - 37 * i
        linea(48, y, fila["sistema"], 420, puntos=11, negrita=True, blanco=True)
        linea(485, y, fecha, 120, puntos=12, blanco=True)
        linea(639, y-3, fila["vencimiento"].strftime("%d/%m/%Y"), 145, puntos=25, negrita=True, blanco=True)
    for y, dato in ((246, ficha["cliente"]), (216, ficha["intervencion"]),
                    (186, ficha["establecimiento"]), (156, ficha["sistemas"]),
                    (126, ficha["periodicidades"]), (77, fecha)):
        linea(36, y, dato, 354)
    for y, dato in ((258, ficha["dictamen"]), (209, ficha["observaciones"]),
                    (160, "Planillas: " + ficha["referencias"]),
                    (145, "Informe técnico: " + ficha["informe"]),
                    (130, f"Anexo fotográfico: {len(anexos)} página(s)"),
                    (42, "Mat. A 11576")):
        linea(420, y, dato, 383)
    total = len(escritor.pages)
    linea(693, 28, f"T.C. 3 AÑOS · Pág. {total} de {total}", 120, puntos=8)
    if firma is not None:
        lienzo.drawImage(ImageReader(BytesIO(firma)), 440, 70, width=96, height=35,
                         preserveAspectRatio=True, anchor="sw", mask="auto")
    lienzo.save()
    capa.seek(0)
    certificado.merge_page(PdfReader(capa).pages[0])
    _numerar_documento(escritor, ultima_con_numeracion_propia=True)
    salida = BytesIO()
    escritor.write(salida)
    return salida.getvalue()
