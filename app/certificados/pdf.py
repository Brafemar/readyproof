"""Compone propuestas y certificados emitidos sobre la plantilla aprobada."""
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

from ..fotos.anexo_pdf import _numerar_documento
from ..planillas.validacion import DatosInvalidos

PLANTILLA = Path(__file__).with_name("plantilla_propuesta.pdf")

LEYENDAS_PROPUESTA = (
    "PROPUESTA / NO EMITIDO",
    "CONDICI\x02N FINAL: PENDIENTE DE VALIDACI\x02N T\x03CNICA",
    "Fechas ilustrativas.",
    "Registro [NNNN]",
    "VIGENCIA POR SISTEMA / INSPECCI",
    "Dictamen y vigencias por sistema o inspecci",
    "PERIODICIDAD POR INSPECCI",
    "PROPUESTA DE DISE\x08O",
)


def quitar_leyendas_propuesta(pagina):
    contenido = pagina.get_contents()
    conservadas = []
    retiradas = []
    divisores = 0
    operaciones = contenido.operations
    for indice, (operandos, operador) in enumerate(operaciones):
        if operador == b"Tj" and str(operandos[0]).startswith(LEYENDAS_PROPUESTA):
            retiradas.append(str(operandos[0]))
        elif indice >= 2 and operador == b"S" and operaciones[indice - 2] == ([48, 355], b"m") and (
            operaciones[indice - 1][1] == b"l" and operaciones[indice - 1][0][1] == 355
        ):
            # Termina el trazado sin dibujar el divisor de la segunda fila.
            conservadas.append(([], b"n"))
            divisores += 1
        else:
            conservadas.append((operandos, operador))
    if divisores != 1 or any(sum(texto.startswith(leyenda) for texto in retiradas) != 1
                            for leyenda in LEYENDAS_PROPUESTA):
        raise DatosInvalidos("La plantilla no permite generar el certificado emitido.")
    contenido.operations = conservadas
    pagina.replace_contents(contenido)


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


def generar_propuesta(documentos, filas, ficha, *, firma=None, condicion=None, numeracion=None):
    planillas, anexos = separar_documentos(documentos)
    escritor = PdfWriter()
    for page in planillas + anexos:
        escritor.add_page(page)
    certificado = escritor.add_page(PdfReader(PLANTILLA).pages[0])
    if condicion is not None:
        quitar_leyendas_propuesta(certificado)
    capa = BytesIO()
    lienzo = canvas.Canvas(capa, pagesize=(float(certificado.mediabox.width), float(certificado.mediabox.height)))

    def linea(x, y, texto, ancho, *, puntos=9, negrita=False, blanco=False):
        fuente = "Helvetica-Bold" if negrita else "Helvetica"
        texto = str(texto)
        medida = lienzo.stringWidth(texto, fuente, puntos)
        escala = min(1, ancho / medida) if medida else 1
        if puntos * escala < 7:
            raise DatosInvalidos("Un campo del certificado es demasiado largo para el formato A4.")
        lienzo.setFont(fuente, puntos * escala)
        lienzo.setFillColorRGB(*( (1, 1, 1) if blanco else (.114, .114, .106) ))
        lienzo.drawString(x, y, texto)

    if condicion is not None:
        linea(730, 534, "EMITIDO", 65, puntos=10, negrita=True)
        linea(36, 427, f"CONDICIÓN FINAL: {condicion}", 600, puntos=10, negrita=True)
        numero, revision = numeracion
        linea(641, 514, f"Registro {numero:04d} · Revisión {revision}", 166, puntos=9)
        linea(36, 446, "Dictamen y vigencia confirmados por el responsable técnico.", 700, puntos=11)
        linea(48, 396, "VIGENCIA CONJUNTA", 420, puntos=9, negrita=True, blanco=True)
        linea(36, 138, "PERIODICIDAD CONFIRMADA", 354, puntos=8, negrita=True)
        linea(36, 302, "Vigencia conjunta de las inspecciones incluidas.", 700, puntos=8)

    fecha = ficha["fecha"].strftime("%d/%m/%Y")
    for i, fila in enumerate(filas):
        y = 355 if condicion is not None else 370 - 37 * i
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
