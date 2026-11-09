"""Formato y paginación de la copia interna de emisión, sin cambiar el kit."""
from copy import deepcopy
from math import floor
import re

from lxml import etree

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
MARGEN = 10 / 25.4
ESCALA_UNA_HOJA = .70


def ajustar_tabla(sheet):
    """Ajusta el ancho y la cabecera solo en la copia interna de emisión."""
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


def preparar_impresion(sheet, workbook, *, titulos=(), mantener_bloques=False):
    rows = sheet.findall(NS+'sheetData/'+NS+'row')
    last = max(int(row.get('r')) for row in rows)
    heights = {int(row.get('r')): float(row.get('ht', '15')) for row in rows}
    height = lambda start, end: sum(heights.get(i, 15) for i in range(start, end+1))
    margins = sheet.find(NS+'pageMargins')
    for key in ('left', 'right', 'bottom'):
        margins.set(key, str(max(MARGEN, float(margins.get(key, '0')))))
    margins.set('top', str(max(29 / 25.4, float(margins.get('top', '0')))))
    page = sheet.find(NS+'pageSetup')
    page.set('orientation', 'landscape'); page.set('paperSize', '9')
    page.set('fitToWidth', '1'); page.attrib.pop('scale', None)
    available = 210/25.4*72 - (float(margins.get('top'))+float(margins.get('bottom')))*72
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
    if page.get('fitToHeight') == '1' or available / height(1, last) >= ESCALA_UNA_HOJA:
        setup.set('fitToPage', '1'); setup.set('autoPageBreaks', '0')
        page.set('fitToHeight', '1')
        return
    # Los saltos manuales requieren escala explícita: fitToPage puede ignorarlos.
    forbidden = set()
    for merged in sheet.findall(NS+'mergeCells/'+NS+'mergeCell'):
        limits = re.findall(r'\d+', merged.get('ref'))
        if len(limits) == 2:
            forbidden.update(range(int(limits[0]), int(limits[1])))
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
            if mantener_bloques:
                forbidden.add(number + 1)
    if observations is not None:
        forbidden.update(range(observations, last))
    header = height(1, 8)
    widths = sum((floor((256*float(col.get('width', '13'))+floor(128/7))/256*7)+5)*(int(col.get('max'))-int(col.get('min'))+1) for col in sheet.findall(NS+'cols/'+NS+'col'))*.75
    available_width = 297/25.4*72-(float(margins.get('left'))+float(margins.get('right')))*72
    width_percent = min(100, floor(100*available_width/widths))
    if mantener_bloques:
        ends = headings[1:] + [observations or last + 1]
        for start, end in zip(headings, ends):
            if (header + height(start, end - 1)) * width_percent / 100 <= available:
                forbidden.update(range(start, end - 1))
    groups = []; start = 9
    for end in range(9, last+1):
        if end not in forbidden:
            groups.append((start, end)); start = end+1
    if start <= last: groups.append((start, last))
    largest = max(height(start, end) for start, end in groups)
    percent = min(width_percent, floor(100*available/(header+largest)))
    if percent < 10: raise ValueError('Un bloque indivisible supera el área imprimible a la escala mínima de Excel.')
    setup.set('fitToPage', '0'); setup.set('autoPageBreaks', '0')
    page.set('scale', str(percent)); page.set('fitToHeight', '0')
    etree.SubElement(names, NS+'definedName', name='_xlnm.Print_Titles', localSheetId='0').text = f"'{title}'!$1:$8"
    breaks = []; used = header
    capacity = available/(percent/100)
    for start, end in groups:
        required = height(start, end)
        if used+required > capacity+1e-6:
            breaks.append(start-1); used = header
        used += required
    if breaks:
        element = etree.Element(NS+'rowBreaks', count=str(len(breaks)), manualBreakCount=str(len(breaks)))
        for row in breaks: etree.SubElement(element, NS+'brk', id=str(row), min='0', max='16383', man='1')
        following = sheet.find(NS+'legacyDrawingHF')
        sheet.insert(sheet.index(following) if following is not None else len(sheet), element)
