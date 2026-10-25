"""Genera planillas SG-PEM-IFI con el formato de las planillas SDI de Martín.
El contenido se arma con openpyxl y luego se inyecta el encabezado de página original
(logo BRAFEMAR, 'SISTEMA DE GESTIÓN INTEGRADO', sello ISO), que openpyxl no soporta.
Uso como módulo: build(spec, ruta_salida, ruta_planilla_modelo)"""
import math, os, re, shutil, tempfile, zipfile
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.properties import PageSetupProperties

NCOL = 25
COLW = 5.3
thin = Side(style='thin', color='000000')
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
BLACK = PatternFill('solid', fgColor='000000')
F = lambda sz=11, b=False, color='000000', name='Calibri': Font(name=name, size=sz, bold=b, color=color)
MESES = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']


class Sheet:
    def __init__(self, ws):
        self.ws, self.r = ws, 1

    def cell(self, c1, c2, r1, r2, text='', font=None, fill=None, h='left', v='center', wrap=True, rot=0, border=True):
        ws = self.ws
        if c2 > c1 or r2 > r1:
            ws.merge_cells(start_row=r1, start_column=c1, end_row=r2, end_column=c2)
        c = ws.cell(r1, c1, text if text != '' else None)
        c.font = font or F()
        c.alignment = Alignment(horizontal=h, vertical=v, wrap_text=wrap, text_rotation=rot)
        if fill: c.fill = fill
        if border:
            for rr in range(r1, r2 + 1):
                for cc in range(c1, c2 + 1):
                    ws.cell(rr, cc).border = BOX
                    if fill: ws.cell(rr, cc).fill = fill
        return c

    def height(self, r, text, cols):
        chars = max(1, int(cols * COLW * 1.3))
        lines = max(1, math.ceil(len(text) / chars))
        self.ws.row_dimensions[r].height = max(15, 15 * lines)

    def bar(self, text, c2=NCOL, fecha=False):
        r = self.r
        if fecha:
            self.cell(1, 19, r, r, text, F(11, True, 'FFFFFF'), BLACK, 'center')
            self.cell(20, 21, r, r, 'FECHA:', F(11, True))
            self.cell(22, NCOL, r, r, '')
        else:
            self.cell(1, c2, r, r, text, F(11, True, 'FFFFFF'), BLACK, 'center')
        self.r += 1


def cabecera(s, sp):
    s.cell(1, 19, 1, 3, sp['sistema'].upper(), F(14, True, name='Arial'), h='center')
    for i, t in enumerate([sp['codigo'], 'Revisión 00-26', 'T.C. 3 AÑOS']):
        s.cell(20, NCOL, 1 + i, 1 + i, t, F(10), h='left')
    s.r = 4
    s.cell(1, 19, 4, 4, sp['titulo'].upper(), F(11, True, 'FFFFFF'), BLACK, 'center')
    s.cell(20, 21, 4, 4, 'FECHA:', F(11, True)); s.cell(22, NCOL, 4, 4, '')
    filas = [[('CLIENTE:', 2, 10), ('CUIT:', 2, 5), ('TELÉFONO:', 2, 4)],
             [('DIRECCIÓN:', 2, 10), ('EDIFICIO:', 2, 5), ('SECTOR:', 2, 4)],
             [('EMPRESA MANTENEDORA:', 4, 8), ('N.° MANTENEDOR CERTIFICADO:', 5, 2), ('INSPECTOR:', 2, 4)]]
    r = 5
    for fila in filas:
        c = 1
        for lab, wl, wv in fila:
            s.cell(c, c + wl - 1, r, r, lab, F(10 if len(lab) > 12 else 11))
            s.cell(c + wl, c + wl + wv - 1, r, r, 'BRAFEMAR' if lab.startswith('EMPRESA') else '')
            c += wl + wv
        r += 1
    s.cell(1, NCOL, r, r, 'SISTEMA / DESIGNACIÓN:', F(11)); s.r = r + 1


def general(s, sp):
    for titulo, campos in sp['bloques']:
        s.bar(titulo)
        for campo in campos:
            lab, val = campo if isinstance(campo, tuple) else (campo, None)
            r = s.r
            s.cell(1, 9, r, r, lab + ':', F(11))
            if isinstance(val, list):
                txt = '      '.join('%s  ☐' % o for o in val)
                s.cell(10, NCOL, r, r, txt, F(11))
            elif isinstance(val, str):
                s.cell(10, NCOL, r, r, '________________  ' + val, F(11))
            else:
                s.cell(10, NCOL, r, r, '')
            s.height(r, lab, 9); s.r += 1


def periodico(s, sp):
    sem = sp.get('modo') == 'semanal'
    cols = ['S1', 'S2', 'S3', 'S4', 'S5'] if sem else MESES
    span = 2 if sem else 1
    for bi, (titulo, items) in enumerate(sp['bloques']):
        s.bar(titulo)
        r0 = s.r
        s.cell(1, 8, r0, r0, 'ELEMENTOS', F(11, True), h='center')
        c = 9
        for t in cols:
            s.cell(c, c + span - 1, r0, r0, t, F(10, True), h='center'); c += span
        last = 8 + len(cols) * span
        for k, it in enumerate(items):
            r = r0 + 1 + k
            txt = it if isinstance(it, str) else '%s (%s)' % it
            s.cell(1, 8, r, r, txt, F(10))
            for cc in range(9, last + 1, span):
                s.cell(cc, cc + span - 1, r, r, '')
            s.height(r, txt, 8)
        r1 = r0 + len(items)
        s.cell(last + 1, last + 1, r0, r1, 'MES' if sem else 'AÑO', F(10, True), h='center', rot=90)
        firma = ('USUARIO (AUTOCONTROL) / ' if sem else '') + ('SUPERVISOR DEL MANTENEDOR' if bi % 2 == 0
                                                            else 'RESPONSABLE DE LA INSTALACIÓN')
        s.cell(last + 2, NCOL, r0, r1, firma, F(9, True), h='center', rot=90)
        s.r = r1 + 1


def checklist(s, sp):
    for titulo, items in sp['bloques']:
        s.bar(titulo, fecha=True)
        r0 = s.r
        for c1, c2, t in [(1, 14, 'VERIFICACIÓN'), (15, 17, 'VALOR'), (18, 19, 'CUMPLE ✓'), (20, 21, 'NO CUMPLE O'),
                          (22, 23, 'NO APREC. X'), (24, 25, 'NA')]:
            s.cell(c1, c2, r0, r0, t, F(8 if c1 > 14 else 11, True), h='center')
        for k, it in enumerate(items):
            r = r0 + 1 + k
            txt, unit = (it, '') if isinstance(it, str) else it
            s.cell(1, 14, r, r, txt, F(10))
            s.cell(15, 17, r, r, ('_____ ' + unit) if unit else '', F(9), h='right')
            for c1, c2 in [(18, 19), (20, 21), (22, 23), (24, 25)]:
                s.cell(c1, c2, r, r, '')
            s.height(r, txt, 14)
        s.r = r0 + 1 + len(items)


def pie(s, sp):
    s.bar('OBSERVACIONES:')
    for _ in range(4):
        s.cell(1, NCOL, s.r, s.r, ''); s.r += 1
    s.cell(1, NCOL, s.r, s.r, 'CUMPLE: ✓     ·     NO CUMPLE: O     ·     NO APRECIABLE: X     ·     NA: NO APLICABLE     ·     '
                               'Toda condición O o X se debe describir en observaciones.', F(9), h='center'); s.r += 1
    r = s.r
    s.cell(1, 12, r, r + 2, '', border=True); s.cell(13, NCOL, r, r + 2, '', border=True)
    s.cell(1, 12, r + 3, r + 3, 'SUPERVISOR DEL MANTENEDOR – FIRMA / ACLARACIÓN', F(10, True), h='center')
    s.cell(13, NCOL, r + 3, r + 3, 'RESPONSABLE DE LA INSTALACIÓN – FIRMA / ACLARACIÓN', F(10, True), h='center')
    s.r = r + 4


def build(sp, out, modelo):
    wb = Workbook(); ws = wb.active; ws.title = 'Hoja1'
    for c in range(1, NCOL + 1):
        ws.column_dimensions[L(c)].width = COLW
    s = Sheet(ws)
    cabecera(s, sp)
    {'general': general, 'periodico': periodico, 'checklist': checklist}[sp['tipo']](s, sp)
    pie(s, sp)
    ws.page_setup.orientation = 'landscape'; ws.page_setup.paperSize = 9
    ws.page_setup.fitToWidth = 1; ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)
    ws.page_margins.left = ws.page_margins.right = ws.page_margins.bottom = ws.page_margins.header = 0.19685
    ws.page_margins.top = 0.98425; ws.page_margins.footer = 0.31496
    ws.print_area = 'A1:%s%d' % (L(NCOL), s.r - 1)
    ws.sheet_view.view = 'pageLayout'
    tmp = out + '.tmp.xlsx'; wb.save(tmp)
    inject_header(tmp, out, modelo); os.remove(tmp)


HF = ('<headerFooter><oddHeader>&amp;L&amp;G&amp;C&amp;"Arial,Negrita"&amp;12SISTEMA DE GESTIÓN INTEGRADO'
      '&amp;"-,Normal"&amp;11&amp;R&amp;G</oddHeader></headerFooter>')


def inject_header(src, out, modelo):
    """Copia el encabezado de página con imágenes (legacyDrawingHF) de la planilla modelo de Martín."""
    m = zipfile.ZipFile(modelo)
    vml = m.read('xl/drawings/vmlDrawing1.vml')
    vml_rels = m.read('xl/drawings/_rels/vmlDrawing1.vml.rels').decode()
    imgs = {t: m.read('xl/drawings/' + t if not t.startswith('../') else 'xl/' + t[3:])
            for t in re.findall(r'Target="([^"]+)"', vml_rels)}
    z = zipfile.ZipFile(src); files = {n: z.read(n) for n in z.namelist()}
    sheet = files['xl/worksheets/sheet1.xml'].decode()
    sheet = re.sub(r'<headerFooter.*?</headerFooter>|<headerFooter/>', '', sheet, flags=re.S)
    k = sheet.index('/>', sheet.index('<pageSetup')) + 2
    sheet = sheet[:k] + HF + sheet[k:]
    if 'xmlns:r=' not in sheet[:500]:
        sheet = sheet.replace('<worksheet ', '<worksheet xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" ', 1)
    sheet = sheet.replace('</worksheet>', '<legacyDrawingHF r:id="rIdHF1"/></worksheet>')
    files['xl/worksheets/sheet1.xml'] = sheet.encode()
    rels_p = 'xl/worksheets/_rels/sheet1.xml.rels'
    rel = ('<Relationship Id="rIdHF1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/vmlDrawing" '
           'Target="../drawings/vmlDrawingHF1.vml"/>')
    if rels_p in files:
        files[rels_p] = files[rels_p].decode().replace('</Relationships>', rel + '</Relationships>').encode()
    else:
        files[rels_p] = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.'
                         'openxmlformats.org/package/2006/relationships">' + rel + '</Relationships>').encode()
    files['xl/drawings/vmlDrawingHF1.vml'] = vml
    files['xl/drawings/_rels/vmlDrawingHF1.vml.rels'] = vml_rels.encode()
    for t, data in imgs.items():
        files['xl/' + t[3:]] = data
    ct = files['[Content_Types].xml'].decode()
    for ext, typ in [('vml', 'application/vnd.openxmlformats-officedocument.vmlDrawing'), ('png', 'image/png'),
                     ('jpeg', 'image/jpeg')]:
        if 'Extension="%s"' % ext not in ct:
            ct = ct.replace('<Default ', '<Default Extension="%s" ContentType="%s"/><Default ' % (ext, typ), 1)
    files['[Content_Types].xml'] = ct.encode()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as o:
        for n, data in files.items():
            o.writestr(n, data)
