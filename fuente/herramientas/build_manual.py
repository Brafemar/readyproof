"""Genera un manual SG-PEM-IFI a partir de la plantilla maestra v2 y un módulo de contenido.
Uso: python -I build_manual.py <plantilla.docx> <contenido.py> <salida.docx>
El módulo de contenido define: SIG, NOM, NOMU, CAP, PL (dict n -> nombre literal de planilla),
CONTENT(cierre) -> lista de bloques, REGISTRO_EXTRA(cierre_ref) -> lista de párrafos.
Bloques: ('h2', t) ('basado', t) ('p', t) ('h3', t) ('h4', t) ('items', [(rótulo, desc) | [viñetas]])
         ('protocol', (título, [(paso, [(rótulo, texto)])])) ('table', [[encabezados], [fila], ...])
En los textos, **x** = negrita."""
import copy, re, sys, importlib.util
from docx import Document
from docx.oxml.ns import qn
from lxml import etree

TPL, CMOD, OUT = sys.argv[1:4]
spec = importlib.util.spec_from_file_location('contenido', CMOD)
M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)

d = Document(TPL)
body = d.element.body
ch = list(body)
W14 = '{http://schemas.microsoft.com/office/word/2010/wordml}'

def txt(e): return ''.join(t.text or '' for t in e.iter(qn('w:t')))
def find(pred, start=0):
    for i in range(start, len(ch)):
        if pred(ch[i]): return i
    raise KeyError
i_h2 = find(lambda e: '{{NOMBRE DEL SISTEMA EN MAYÚSCULAS}}' in txt(e))
i_bas = find(lambda e: txt(e).startswith('(Basado en'), i_h2)
i_txt = find(lambda e: txt(e).startswith('Este apartado establece'), i_h2)
i_emp = i_txt + 1
i_h3 = find(lambda e: txt(e).strip() == 'INSPECCIÓN', i_h2)
i_h4 = find(lambda e: txt(e).startswith('Inspección {{frecuencia}}'), i_h2)
i_empkn = i_h4 + 1
i_item = find(lambda e: txt(e).startswith('{{Elemento o componente}}'), i_h2)
i_dot = find(lambda e: txt(e).startswith('{{accesorio}}'), i_h2)
i_pt = find(lambda e: txt(e).startswith('Protocolo de Ensayo'), i_h2)
i_step = find(lambda e: txt(e).startswith('{{Paso del ensayo}}'), i_h2)
i_lab = find(lambda e: txt(e).startswith('Paso a paso:'), i_h2)
i_tbl = find(lambda e: e.tag == qn('w:tbl'), i_h2)
i_reg = find(lambda e: 'REGISTRO DE INSPECCIONES' in txt(e), i_h2)
i_anx = find(lambda e: txt(e).strip() == 'ANEXOS O REGISTROS', i_reg)
i_anl = find(lambda e: txt(e).startswith('SG-PEM-IFI-{{SIGLA}}-1'), i_anx)
for k, e in enumerate(ch):  # verificación de que el empty es realmente vacío
    pass
assert txt(ch[i_emp]) == '' and txt(ch[i_empkn]) == ''

# ---------- numeración ----------
numbering = d.part.numbering_part.element
nid0 = [max(int(n.get(qn('w:numId'))) for n in numbering.findall(qn('w:num'))) + 1]
def new_num(abstract):
    nid = nid0[0]; nid0[0] += 1
    n = etree.Element(qn('w:num')); n.set(qn('w:numId'), str(nid))
    a = etree.SubElement(n, qn('w:abstractNumId')); a.set(qn('w:val'), abstract)
    lo = etree.SubElement(n, qn('w:lvlOverride')); lo.set(qn('w:ilvl'), '0')
    so = etree.SubElement(lo, qn('w:startOverride')); so.set(qn('w:val'), '1')
    numbering.findall(qn('w:num'))[-1].addnext(n)
    return nid

def rpr_of(p):
    r = p.find('.//' + qn('w:r'))
    rp = r.find(qn('w:rPr')) if r is not None else None
    rp = copy.deepcopy(rp) if rp is not None else etree.Element(qn('w:rPr'))
    for t in ('w:b', 'w:bCs'):
        for e in rp.findall(qn(t)): rp.remove(e)
    return rp

def make(idx, text, bold_all=False, num=None, prefix=None):
    """prefix: (texto, negrita) que va antes del texto."""
    p = copy.deepcopy(ch[idx]); rp = rpr_of(p)
    for e in list(p):
        if e.tag != qn('w:pPr'): p.remove(e)
    segs = []
    if prefix: segs.append(prefix)
    for i, s in enumerate(re.split(r'\*\*', text)):
        if s: segs.append((s, bold_all or i % 2 == 1))
    for s, b in segs:
        r = etree.SubElement(p, qn('w:r')); rr = copy.deepcopy(rp)
        be, bc = etree.Element(qn('w:b')), etree.Element(qn('w:bCs'))
        if not b: be.set(qn('w:val'), '0'); bc.set(qn('w:val'), '0')
        rr.insert(0, bc); rr.insert(0, be); r.append(rr)
        t = etree.SubElement(r, qn('w:t')); t.text = s
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    if num is not None:
        p.find('.//' + qn('w:numId')).set(qn('w:val'), str(num))
    return p

out = []
def empty(kn=False): out.append(copy.deepcopy(ch[i_empkn if kn else i_emp]))

def table(rows):
    rel = None
    if isinstance(rows, dict):  # {'w': [anchos relativos], 'rows': [...]}: columnas de ancho distinto, texto sin sangría
        rel, rows = rows['w'], rows['rows']
    t = copy.deepcopy(ch[i_tbl]); trs = t.findall(qn('w:tr'))
    hdr_tr, body_tr = trs[0], trs[1]
    for r in trs: t.remove(r)
    ncol = len(rows[0]); width = 9724 // ncol
    widths = [9724 * x // sum(rel) for x in rel] if rel else [width] * ncol
    grid = t.find(qn('w:tblGrid'))
    for g in list(grid): grid.remove(g)
    for wi in widths:
        g = etree.SubElement(grid, qn('w:gridCol')); g.set(qn('w:w'), str(wi))
    for ri, row in enumerate(rows):
        src = hdr_tr if ri == 0 else body_tr
        tr = copy.deepcopy(src); tcs = tr.findall(qn('w:tc'))
        for tc in tcs: tr.remove(tc)
        for ci, val in enumerate(row):
            tc = copy.deepcopy(tcs[0 if ci == 0 else 1] if ri else tcs[0])
            tc.find('.//' + qn('w:tcW')).set(qn('w:w'), str(widths[ci]))
            p = tc.find(qn('w:p'))
            for e in list(p):
                if e.tag != qn('w:pPr'): p.remove(e)
            if rel:
                ppr = p.find(qn('w:pPr'))
                for e in list(ppr):
                    if e.tag in (qn('w:ind'), qn('w:jc')): ppr.remove(e)
                ind = etree.SubElement(ppr, qn('w:ind'))
                for k in ('left', 'right', 'firstLine'): ind.set(qn('w:' + k), '0')
                jc = etree.SubElement(ppr, qn('w:jc')); jc.set(qn('w:val'), 'center' if ri == 0 or ci != 1 else 'left')
            elif ncol >= 4:  # tablas anchas: sin sangría, centradas y con letra menor para que no se corten las palabras
                ppr = p.find(qn('w:pPr'))
                for e in list(ppr):
                    if e.tag in (qn('w:ind'), qn('w:jc')): ppr.remove(e)
                ind = etree.SubElement(ppr, qn('w:ind'))
                for k in ('left', 'right', 'firstLine'): ind.set(qn('w:' + k), '0')
                jc = etree.SubElement(ppr, qn('w:jc')); jc.set(qn('w:val'), 'center')
            r = etree.SubElement(p, qn('w:r')); rp = etree.SubElement(r, qn('w:rPr'))
            if ri == 0 or ci == 0: etree.SubElement(rp, qn('w:b'))
            sz = etree.SubElement(rp, qn('w:sz')); sz.set(qn('w:val'), '20' if ncol < 4 else '18')
            tt = etree.SubElement(r, qn('w:t')); tt.text = val
            tt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            tr.append(tc)
        if rel:  # las filas no se parten entre páginas
            trpr = tr.find(qn('w:trPr'))
            if trpr is None:
                trpr = etree.Element(qn('w:trPr')); tr.insert(1 if tr.find(qn('w:tblPrEx')) is not None else 0, trpr)
            if trpr.find(qn('w:cantSplit')) is None: trpr.insert(0, etree.Element(qn('w:cantSplit')))
        t.append(tr)
    return t

INF = getattr(M, 'INFORME', 'SG-PEM-IFI-%s-IN' % M.SIG)

def cierre(k):
    return 'Los resultados deben registrarse en la planilla SG-PEM-IFI-%s-%d %s – %s.' % (M.SIG, k, M.NOM, M.PL[k])

for kind, pl in M.CONTENT(cierre):
    if kind == 'h2':
        out.append(make(i_h2, pl, True))
    elif kind == 'basado':
        out.append(make(i_bas, pl)); empty(); continue
    elif kind == 'h3':
        out.append(make(i_h3, pl, True)); empty(True); continue
    elif kind == 'h4':
        out.append(make(i_h4, pl, True)); empty(True); continue
    elif kind == 'p':
        out.append(make(i_txt, pl))
    elif kind == 'items':
        nid = new_num('153'); prev_dots = False
        for it in pl:
            if isinstance(it, list):
                empty()
                for s in it: out.append(make(i_dot, s))
                empty(); prev_dots = True
                continue
            lab, desc = it
            if desc:
                out.append(make(i_item, ' ' + desc, prefix=(lab + ':', True), num=nid))
            else:
                out.append(make(i_item, lab if lab.endswith(('.', ':')) else lab + ':', num=nid))
            prev_dots = False
        if prev_dots: continue
    elif kind == 'protocol':
        title, steps = pl
        out.append(make(i_pt, 'Protocolo de Ensayo: ' + title, True))
        nid = new_num('155')
        for st, labels in steps:
            empty(True)
            out.append(make(i_step, st, True, num=nid))
            for lab, tx in labels:
                empty()
                out.append(make(i_lab, ' ' + tx, prefix=(lab + ':', True)))
    elif kind == 'table':
        out.append(table(pl))
    else:
        raise ValueError(kind)
    empty()

# ---------- registro (texto común + extra) ----------
reg = [copy.deepcopy(e) for e in ch[i_reg:i_anx]]
# el último elemento del bloque común es vacío: insertar extra antes de él
extra = []
RET = [] if getattr(M, 'RETENCION', False) else [
    'Los registros se deben conservar como mínimo durante tres años, según los requisitos generales de la IRAM 3546:2011.']
SIN_INF = getattr(M, 'SIN_INFORME', False)
for t in M.REGISTRO_EXTRA(cierre) + RET + ([] if SIN_INF else [
        'A partir de los registros completados se emite el informe %s Informe general – %s, que consolida los '
        'resultados del período evaluado, la condición de cumplimiento normativo y las no conformidades detectadas, y se '
        'entrega al usuario junto con la copia de las planillas.' % (INF, M.NOM)]):
    extra.append(copy.deepcopy(ch[i_emp])); extra.append(make(i_txt, t))
reg = reg[:-1] + extra + reg[-1:] if txt(reg[-1]) == '' else reg + extra

anx = [copy.deepcopy(e) for e in ch[i_anx:i_anl]]
for k in sorted(M.PL):
    anx.append(make(i_anl, 'SG-PEM-IFI-%s-%d %s. %s' % (M.SIG, k, M.PL[k].upper(), M.NOM)))
if not SIN_INF: anx.append(make(i_anl, '%s INFORME GENERAL. %s' % (INF, M.NOM)))
# la lista de anexos se mantiene unida, para que la última línea no quede sola en una página
for e in anx[:-1]:
    ppr = e.find(qn('w:pPr'))
    if ppr is None: ppr = etree.SubElement(e, qn('w:pPr')); e.insert(0, ppr)
    if ppr.find(qn('w:keepNext')) is None:
        kn = etree.Element(qn('w:keepNext')); ps = ppr.find(qn('w:pStyle'))
        ppr.insert(1 if ps is not None else 0, kn)
tail_start = i_anl
while 'SG-PEM-IFI-{{SIGLA}}' in txt(ch[tail_start]): tail_start += 1
pre = ch[:i_h2]; tail = ch[tail_start:]
# ---------- alcance particular del sistema (tools/alcances.py) ----------
try:
    import os as _os
    sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    from alcances import ALCANCES, BASE as _ABASE
except Exception:
    ALCANCES = {}
AL = ALCANCES.get(M.SIG)
if AL:
    def _set(p, text):
        r0 = p.find('.//' + qn('w:r'))
        rp0 = r0.find(qn('w:rPr')) if r0 is not None else None
        rp = copy.deepcopy(rp0) if rp0 is not None else etree.Element(qn('w:rPr'))
        for e in list(p):
            if e.tag != qn('w:pPr'): p.remove(e)
        r = etree.SubElement(p, qn('w:r')); rr = copy.deepcopy(rp); r.append(rr)
        t = etree.SubElement(r, qn('w:t')); t.text = text
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    i_al = next(i for i, e in enumerate(pre) if txt(e).strip() == 'ALCANCE' and i > 20)
    i_intro = next(i for i in range(i_al, len(pre)) if txt(pre[i]).startswith('El presente procedimiento es aplicable'))
    _set(pre[i_intro], AL.get('intro') or _ABASE % (M.NOM.lower(), M.CAP))
    i_comp = next(i for i in range(i_al, len(pre)) if txt(pre[i]).startswith('Comprende, según la configuración'))
    _set(pre[i_comp], 'Comprende, según la configuración de cada instalación, la verificación y el mantenimiento de:')
    bullets = [i for i in range(i_comp, len(pre)) if pre[i].find('.//' + qn('w:pStyle')) is not None
               and pre[i].find('.//' + qn('w:pStyle')).get(qn('w:val')) == 'Estilo1VIETAPROCEDIMIENTO' and txt(pre[i]).strip()]
    model = copy.deepcopy(pre[bullets[0]])
    anchor = pre[bullets[0]]
    newb = []
    for it in AL['items']:
        q = copy.deepcopy(model); _set(q, it); newb.append(q)
    pos = bullets[0]
    for i in sorted(bullets, reverse=True): del pre[i]
    pre[pos:pos] = newb
    if AL.get('rel'):
        i_inc = next(i for i in range(i_al, len(pre)) if txt(pre[i]).startswith('Incluye las inspecciones'))
        emp = copy.deepcopy(pre[i_inc + 1]); q = copy.deepcopy(pre[i_inc]); _set(q, AL['rel'])
        pre[i_inc + 1:i_inc + 1] = [emp, q]
for e in ch: body.remove(e)
for e in pre + out + reg + anx + tail: body.append(e)
# sin párrafos vacíos al final del documento: generan una última página en blanco
while True:
    kids = list(body); last = kids[-2] if kids[-1].tag == qn('w:sectPr') else kids[-1]
    if last.tag == qn('w:p') and not txt(last).strip() and last.find('.//' + qn('w:drawing')) is None \
            and last.find('.//' + qn('w:sectPr')) is None:
        body.remove(last)
    else:
        break

# ---------- portada, encabezado, propiedades ----------
def repl(root):
    for t in root.iter(qn('w:t')):
        if t.text and '{{' in t.text:
            t.text = (t.text.replace('{{NOMBRE DEL SISTEMA}}', M.NOMU).replace('{{SIGLA}}', M.SIG)
                      .replace('{{Nombre del sistema}}', M.NOM))
repl(body); repl(d.sections[0].header.part.element)
for e in d.element.iter():
    for a in (W14 + 'paraId', W14 + 'textId'):
        if a in e.attrib: del e.attrib[a]
d.core_properties.title = 'SG-PEM-IFI-%s %s' % (M.SIG, M.NOM)
d.save(OUT)

left = re.findall(r'\{\{[^}]*\}\}|\[INSTRUCCI', etree.tostring(d.element).decode() +
                  etree.tostring(d.sections[0].header.part.element).decode())
bad = re.findall(r'\b(tu|tus|usted|deberás|notás|medís|abrís|comprobamos|usamos)\b',
                 ' '.join(txt(e) for e in out), re.I)
print('OK', OUT, '| bloques:', len(out), '| marcadores sin reemplazar:', left, '| 2a persona:', bad)
