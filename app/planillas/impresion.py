"""Paginación de la copia Excel sin modificar celdas, filas ni el kit."""
from math import floor
import re

from lxml import etree

NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
MARGEN = 10 / 25.4
ESCALA_UNA_HOJA = .70


def preparar_impresion(sheet, workbook, *, titulos=()):
    rows = sheet.findall(NS+'sheetData/'+NS+'row')
    last = max(int(row.get('r')) for row in rows)
    heights = {int(row.get('r')): float(row.get('ht', '15')) for row in rows}
    height = lambda start, end: sum(heights.get(i, 15) for i in range(start, end+1))
    margins = sheet.find(NS+'pageMargins')
    for key in ('left', 'right', 'bottom'):
        margins.set(key, str(max(MARGEN, float(margins.get(key, '0')))))
    margins.set('top', str(max(MARGEN, float(margins.get('top', '0')))))
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
    for row in rows:
        number = int(row.get('r'))
        label = ''.join(row.itertext())
        if 'OBSERVACIONES:' in label: observations = number
        if any(label == value for value in titulos): forbidden.add(number)
    if observations is not None:
        forbidden.update(range(observations, last))
    groups = []; start = 9
    for end in range(9, last+1):
        if end not in forbidden:
            groups.append((start, end)); start = end+1
    if start <= last: groups.append((start, last))
    header = height(1, 8)
    largest = max(height(start, end) for start, end in groups)
    widths = sum((floor((256*float(col.get('width', '13'))+floor(128/7))/256*7)+5)*(int(col.get('max'))-int(col.get('min'))+1) for col in sheet.findall(NS+'cols/'+NS+'col'))*.75
    available_width = 297/25.4*72-(float(margins.get('left'))+float(margins.get('right')))*72
    percent = min(100, floor(100*available_width/widths), floor(100*available/(header+largest)))
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
