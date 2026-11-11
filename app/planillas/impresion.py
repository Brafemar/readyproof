"""Formato y paginación de la copia interna de emisión, sin cambiar el kit."""
from copy import deepcopy
from math import floor
import re

from lxml import etree
from openpyxl.utils.cell import get_column_letter, range_boundaries
from reportlab.pdfbase.pdfmetrics import stringWidth

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
MARGEN = 10 / 25.4
ESCALA_UNA_HOJA = .70
# Fira Sans 11 pt alcanza 8,184 px en el dígito más ancho a 96 ppp.
ANCHO_DIGITO_PX = 9
MINIMO_PT_SDI = 9
FUENTE_EXCEL_SDI = 12
ANCHO_COLUMNA_SDI = 5.25
DIGITO_SDI_PX = 7.5
MARGEN_BORDE_SDI_MM = 8.5
MARGEN_SUPERIOR_SDI_MM = 42
MARGEN_INFERIOR_TABLA_SDI_MM = 18
ESCALA_SDI = 90


def es_planilla_sdi(codigo):
    return re.fullmatch(r"SG-PEM-IFI-SDI-[1-5]", codigo or "") is not None


def ampliar_rotulos_sdi(sheet):
    merges = sheet.find(NS+'mergeCells')
    for fila, izquierda, centro, derecha in ((6, 'A', 'C', 'L'), (5, 'T', 'V', 'Y'), (7, 'T', 'V', 'Y')):
        siguiente = get_column_letter(range_boundaries(f'{centro}{fila}')[0] + 1)
        anterior = get_column_letter(range_boundaries(f'{centro}{fila}')[0] - 1)
        for original, ampliado in (
            (f'{izquierda}{fila}:{anterior}{fila}', f'{izquierda}{fila}:{centro}{fila}'),
            (f'{centro}{fila}:{derecha}{fila}', f'{siguiente}{fila}:{derecha}{fila}'),
        ):
            merges.find(f"{NS}mergeCell[@ref='{original}']").set('ref', ampliado)
        row = sheet.find(f"{NS}sheetData/{NS}row[@r='{fila}']")
        dato = row.find(f"{NS}c[@r='{centro}{fila}']")
        contigua = row.find(f"{NS}c[@r='{siguiente}{fila}']")
        fondo = deepcopy(contigua)
        fondo.set('r', f'{centro}{fila}')
        copia = deepcopy(dato)
        copia.set('r', f'{siguiente}{fila}')
        row.replace(dato, fondo)
        row.replace(contigua, copia)


def ajustar_legibilidad_sdi(sheet, styles):
    """Ajusta las alturas de la copia una vez cargados todos los textos."""
    ampliar_rotulos_sdi(sheet)
    for column in sheet.findall(NS+'cols/'+NS+'col'):
        column.set('width', str(ANCHO_COLUMNA_SDI))
    fonts = styles.find(NS+'fonts')
    formats = styles.find(NS+'cellXfs')
    for font in fonts:
        size = font.find(NS+'sz')
        if size is not None and float(size.get('val')) < FUENTE_EXCEL_SDI:
            size.set('val', str(FUENTE_EXCEL_SDI))

    anchos = {}
    for fusion in sheet.findall(NS+'mergeCells/'+NS+'mergeCell'):
        izquierda, arriba, derecha, _ = range_boundaries(fusion.get('ref'))
        anchos[f"{get_column_letter(izquierda)}{arriba}"] = derecha - izquierda + 1
    for row in sheet.findall(NS+'sheetData/'+NS+'row'):
        numero = int(row.get('r'))
        altura = 22 if numero in (5, 6, 7) else 15
        for cell in row.findall(NS+'c'):
            texto = ''.join(cell.itertext())
            if not texto:
                continue
            estilo = formats[int(cell.get('s', '0'))]
            alineacion = estilo.find(NS+'alignment')
            if alineacion is not None and alineacion.get('textRotation', '0') != '0':
                continue
            font = fonts[int(estilo.get('fontId', '0'))]
            puntos = float(font.find(NS+'sz').get('val'))
            fuente = 'Helvetica-Bold' if font.find(NS+'b') is not None else 'Helvetica'
            # Presupuesto conservador para la sustitución de fuentes de Calc.
            ancho = 33 * anchos.get(cell.get('r'), 1) - 4
            lineas = 1
            linea = ''
            for parrafo in texto.splitlines() or ['']:
                if linea:
                    lineas += 1
                    linea = ''
                for palabra in parrafo.split():
                    candidata = f'{linea} {palabra}'.strip()
                    if linea and stringWidth(candidata, fuente, puntos) > ancho:
                        lineas += 1
                        linea = palabra
                    else:
                        linea = candidata
                    while stringWidth(linea, fuente, puntos) > ancho:
                        parte = 1
                        while parte < len(linea) and stringWidth(linea[:parte+1], fuente, puntos) <= ancho:
                            parte += 1
                        linea = linea[parte:]
                        if linea:
                            lineas += 1
            altura = max(altura, lineas * (puntos + 2) + 2)
        row.set('ht', str(altura))
        row.set('customHeight', '1')


def dividir_fusiones_periodicas(sheet, fusiones, saltos):
    """Repite las etiquetas verticales cuando su bloque continúa en otra página."""
    celdas = {c.get('r'): c for c in sheet.findall(NS+'sheetData/'+NS+'row/'+NS+'c')}
    merges = sheet.find(NS+'mergeCells')
    for fusion in fusiones:
        izquierda, inicio, derecha, fin = range_boundaries(fusion.get('ref'))
        letra = get_column_letter(izquierda)
        etiqueta = celdas[f'{letra}{inicio}']
        for corte in (r for r in saltos if inicio <= r < fin):
            fusion.set('ref', f'{letra}{inicio}:{get_column_letter(derecha)}{corte}')
            inicio = corte + 1
            nueva = deepcopy(etiqueta)
            nueva.set('r', f'{letra}{inicio}')
            anterior = celdas[nueva.get('r')]
            anterior.getparent().replace(anterior, nueva)
            fusion = etree.SubElement(merges, NS+'mergeCell',
                                       ref=f'{letra}{inicio}:{get_column_letter(derecha)}{fin}')
    merges.set('count', str(len(merges)))


def aplicar_identidad(styles):
    """Aplica la marca en la salida sin editar los estilos del kit fuente."""
    for font in styles.find(NS+'fonts'):
        name = font.find(NS+'name')
        if name is not None:
            # El Archivo-Black.ttf entregado tiene peso 900 y familia interna Archivo SemiBold.
            name.set('val', 'Archivo SemiBold' if name.get('val') == 'Arial' else 'Fira Sans')
        scheme = font.find(NS+'scheme')
        if scheme is not None:
            font.remove(scheme)
    for node in styles.iter():
        if node.get('rgb') in {'00000000', 'FF000000'}:
            node.set('rgb', 'FF1D1D1B')


def ajustar_tabla(sheet):
    """Ajusta el ancho y la cabecera solo en la copia interna de emisión."""
    header = sheet.find(NS+'headerFooter/'+NS+'oddHeader')
    if header is not None and header.text:
        header.text = header.text.replace('Arial,Negrita', 'Fira Sans,Negrita')
    for column in sheet.findall(NS+'cols/'+NS+'col'):
        column.set('width', '8.7')
    for number in (5, 6, 7):
        row = sheet.find(f"{NS}sheetData/{NS}row[@r='{number}']")
        row.set('ht', '22')
        row.set('customHeight', '1')
    merges = sheet.find(NS+'mergeCells')
    merges.find(f"{NS}mergeCell[@ref='M7:Q7']").set('ref', 'M7:P7')
    merges.find(f"{NS}mergeCell[@ref='R7:S7']").set('ref', 'Q7:S7')
    row = sheet.find(f"{NS}sheetData/{NS}row[@r='7']")
    row.remove(row.find(f"{NS}c[@r='Q7']"))
    row.find(f"{NS}c[@r='R7']").set('r', 'Q7')


def destacar_resultados(sheet, styles, cambios):
    """Aplica el estilo solo a valores cargados en el cuerpo de la planilla."""
    fonts = styles.find(NS+'fonts')
    formats = styles.find(NS+'cellXfs')
    replacements = {}
    for cell in sheet.findall('.//'+NS+'c'):
        address = cell.get('r', '')
        match = re.fullmatch(r'([A-Z]+)(\d+)', address)
        if address not in cambios or not match or match[1] == 'A' or int(match[2]) < 9:
            continue
        original = int(cell.get('s', '0'))
        if original not in replacements:
            style = deepcopy(formats[original])
            font = deepcopy(fonts[int(style.get('fontId', '0'))])
            bold = font.find(NS+'b')
            if bold is None:
                bold = etree.SubElement(font, NS+'b')
            bold.set('val', '1')
            style.set('fontId', str(len(fonts)))
            style.set('applyFont', '1')
            fonts.append(font)
            alignment = style.find(NS+'alignment')
            if alignment is None:
                alignment = etree.SubElement(style, NS+'alignment')
            alignment.set('horizontal', 'center')
            alignment.set('vertical', 'center')
            style.set('applyAlignment', '1')
            replacements[original] = str(len(formats))
            formats.append(style)
        cell.set('s', replacements[original])
    fonts.set('count', str(len(fonts)))
    formats.set('count', str(len(formats)))


def preparar_impresion(sheet, workbook, *, titulos=(), mantener_bloques=False,
                        sdi=False, periodica=False, pie_sdi_pt=0):
    rows = sheet.findall(NS+'sheetData/'+NS+'row')
    last = max(int(row.get('r')) for row in rows)
    heights = {int(row.get('r')): float(row.get('ht', '15')) for row in rows}
    height = lambda start, end: sum(heights.get(i, 15) for i in range(start, end+1))
    margins = sheet.find(NS+'pageMargins')
    if sdi:
        for key in ('left', 'right', 'header'):
            margins.set(key, str(MARGEN_BORDE_SDI_MM / 25.4))
        margins.set('bottom', str(MARGEN_INFERIOR_TABLA_SDI_MM / 25.4))
        margins.set('top', str(MARGEN_SUPERIOR_SDI_MM / 25.4))
    else:
        for key in ('left', 'right', 'bottom'):
            margins.set(key, str(max(MARGEN, float(margins.get(key, '0')))))
        margins.set('top', str(max(66 / 25.4, float(margins.get('top', '0')))))
    page = sheet.find(NS+'pageSetup')
    page.set('orientation', 'landscape'); page.set('paperSize', '9')
    page.set('fitToWidth', '1'); page.attrib.pop('scale', None)
    available = 210/25.4*72 - (float(margins.get('top'))+float(margins.get('bottom')))*72
    if sdi:
        available -= 4  # Holgura para el redondeo de alturas de LibreOffice.
    props = sheet.find(NS+'sheetPr')
    if props is None:
        props = etree.Element(NS+'sheetPr'); sheet.insert(0, props)
    setup = props.find(NS+'pageSetUpPr')
    if setup is None: setup = etree.SubElement(props, NS+'pageSetUpPr')
    for tag in ('rowBreaks', 'colBreaks'):
        element = sheet.find(NS+tag)
        if element is not None: sheet.remove(element)
    names = workbook.find(NS+'definedNames')
    if names is None: names = etree.SubElement(workbook, NS+'definedNames')
    for item in list(names):
        if item.get('localSheetId') == '0' and item.get('name') in ('_xlnm.Print_Area', '_xlnm.Print_Titles'):
            names.remove(item)
    title = workbook.find(NS+'sheets/'+NS+'sheet').get('name').replace("'", "''")
    etree.SubElement(names, NS+'definedName', name='_xlnm.Print_Area', localSheetId='0').text = f"'{title}'!$A$1:$Y${last}"
    if not sdi and (page.get('fitToHeight') == '1' or available / height(1, last) >= ESCALA_UNA_HOJA):
        setup.set('fitToPage', '1'); setup.set('autoPageBreaks', '0')
        page.set('fitToHeight', '1')
        return
    # Los saltos manuales requieren escala explícita: fitToPage puede ignorarlos.
    forbidden = set()
    fusiones_periodicas = []
    for merged in sheet.findall(NS+'mergeCells/'+NS+'mergeCell'):
        izquierda, inicio, _, fin = range_boundaries(merged.get('ref'))
        if sdi and periodica and izquierda >= 19 and inicio >= 9 and inicio < fin:
            if fin - inicio > 2:
                fusiones_periodicas.append(merged)
                continue
        forbidden.update(range(inicio, fin))
    observations = None
    headings = []
    for row in rows:
        number = int(row.get('r'))
        first = row.find(f"{NS}c[@r='A{number}']")
        label = ''.join(first.itertext()) if first is not None else ''
        if 'OBSERVACIONES:' in label: observations = number
        if label in titulos:
            headings.append(number)
            forbidden.add(number)
            if mantener_bloques or (sdi and periodica):
                forbidden.add(number + 1)
    if observations is not None:
        if sdi:
            forbidden.add(observations)
            forbidden.update(range(last - 4, last))
        else:
            forbidden.update(range(observations, last))
    header = height(1, 8)
    filas_repetidas = 5 if sdi else 8
    header_continuacion = height(1, filas_repetidas)
    digit = DIGITO_SDI_PX if sdi else ANCHO_DIGITO_PX
    widths = sum((floor((256*float(col.get('width', '13'))+floor(128/digit))/256*digit)+5)
                 *(int(col.get('max'))-int(col.get('min'))+1)
                 for col in sheet.findall(NS+'cols/'+NS+'col'))*.75
    available_width = 297/25.4*72-(float(margins.get('left'))+float(margins.get('right')))*72
    width_percent = min(100, floor(100*available_width/widths))
    if sdi:
        width_percent = min(width_percent, ESCALA_SDI)
    if (mantener_bloques and not sdi) or (sdi and periodica):
        ends = headings[1:] + [observations or last + 1]
        for start, end in zip(headings, ends):
            if (header_continuacion + height(start, end - 1)) * width_percent / 100 <= available:
                forbidden.update(range(start, end - 1))
    groups = []; start = 9
    for end in range(9, last+1):
        if end not in forbidden:
            groups.append((start, end)); start = end+1
    if start <= last: groups.append((start, last))
    largest = max(height(start, end) for start, end in groups)
    alto_minimo = max(header + height(*groups[0]), header_continuacion + largest)
    percent = min(width_percent, floor(100 * available / alto_minimo))
    if sdi and percent < ESCALA_SDI:
        raise ValueError('Una sección de SDI supera el área imprimible sin reducir la letra.')
    if percent < 10: raise ValueError('Un bloque indivisible supera el área imprimible a la escala mínima de Excel.')
    setup.set('fitToPage', '0'); setup.set('autoPageBreaks', '0')
    page.set('scale', str(percent)); page.set('fitToHeight', '0')
    etree.SubElement(names, NS+'definedName', name='_xlnm.Print_Titles', localSheetId='0').text = f"'{title}'!$1:${filas_repetidas}"
    breaks = []; used = header
    capacity = available/(percent/100)
    reserva_ultima = max(0, pie_sdi_pt - float(margins.get('bottom')) * 72) if sdi else 0
    ultima_capacidad = capacity - reserva_ultima / (percent / 100)
    if header_continuacion + height(*groups[-1]) > ultima_capacidad + 1e-6:
        raise ValueError('El pie y las firmas exceden el espacio de la última página.')
    for start, end in groups:
        required = height(start, end)
        limite = ultima_capacidad if end == last else capacity
        if used+required > limite+1e-6:
            breaks.append(start-1); used = header_continuacion
        used += required
    if fusiones_periodicas:
        dividir_fusiones_periodicas(sheet, fusiones_periodicas, breaks)
    if breaks:
        element = etree.Element(NS+'rowBreaks', count=str(len(breaks)), manualBreakCount=str(len(breaks)))
        for row in breaks: etree.SubElement(element, NS+'brk', id=str(row), min='0', max='16383', man='1')
        following = sheet.find(NS+'legacyDrawingHF')
        sheet.insert(sheet.index(following) if following is not None else len(sheet), element)
