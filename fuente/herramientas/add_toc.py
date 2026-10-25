"""Agrega el «Índice de Contenido» (campo TOC niveles 1 a 3, como el modelo de Martín) después de la portada.
Las entradas y los números de página se precargan: se renderiza el documento con LibreOffice y se ubica cada
título en el PDF. Word puede actualizar el índice con «Actualizar campo».
Uso: python -I add_toc.py <manual.docx>"""
import copy, os, re, subprocess, sys, tempfile
from docx import Document
from docx.oxml.ns import qn
from lxml import etree

F = sys.argv[1]
SOFFICE = '/mnt/skills/public/docx/scripts/office/soffice.py'
W = lambda t: qn('w:' + t)
RIGHT_TAB = 10470

def txt(p): return ''.join(t.text or '' for t in p.iter(W('t')))
def el(tag, **at):
    e = etree.Element(W(tag))
    for k, v in at.items(): e.set(W(k), str(v))
    return e

def headings(body):
    """Devuelve [(párrafo, nivel, número, texto)] de los títulos del cuerpo."""
    res, c1, c2, c3 = [], 0, 0, 0
    started = False
    for p in body.iter(W('p')):
        pPr = p.find(W('pPr'))
        if pPr is None: continue
        st = pPr.find(W('pStyle')); st = st.get(W('val')) if st is not None else ''
        np_ = pPr.find(W('numPr'))
        nid = np_.find(W('numId')).get(W('val')) if np_ is not None and np_.find(W('numId')) is not None else None
        il = np_.find(W('ilvl')).get(W('val')) if np_ is not None and np_.find(W('ilvl')) is not None else None
        t = txt(p).strip()
        if not t: continue
        if nid == '2' and il == '0' and pPr.find(W('pBdr')) is not None:
            started = True; c1 += 1; c2 = c3 = 0
            res.append((p, 1, '%d.' % c1, t))
        elif started and st == 'titulo2' and (np_ is None or il == '1'):
            c2 += 1; c3 = 0; res.append((p, 2, '%d.%d.' % (c1, c2), t))
        elif started and st == 'titulo2' and il == '2':
            c3 += 1; res.append((p, 3, '%d.%d.%d.' % (c1, c2, c3), t))
    return res

def mark(p, lvl, k):
    pPr = p.find(W('pPr'))
    for e in pPr.findall(W('outlineLvl')): pPr.remove(e)
    ol = el('outlineLvl', val=lvl - 1)
    # outlineLvl va antes de rPr / sectPr / pPrChange
    anchor = pPr.find(W('rPr'))
    if anchor is not None: anchor.addprevious(ol)
    else: pPr.append(ol)
    name = '_Toc%09d' % (900000000 + k)
    bs = el('bookmarkStart', id=7000 + k, name=name); be = el('bookmarkEnd', id=7000 + k)
    pPr.addnext(bs); p.append(be)
    return name

def run(text, bold=False, tab=False, size=24):
    r = el('r'); rp = etree.SubElement(r, W('rPr'))
    f = etree.SubElement(rp, W('rFonts'))
    for a in ('ascii', 'hAnsi', 'cs'): f.set(W(a), 'Times New Roman')
    if bold: etree.SubElement(rp, W('b'))
    etree.SubElement(rp, W('noProof'))
    s = etree.SubElement(rp, W('sz')); s.set(W('val'), str(size))
    if tab: r.append(el('tab'))
    else:
        t = etree.SubElement(r, W('t')); t.text = text
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    return r

def fld(kind, instr=None):
    r = el('r')
    if instr is not None:
        it = etree.SubElement(r, W('instrText')); it.text = instr
        it.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    else:
        r.append(el('fldChar', fldCharType=kind))
    return r

def entry(lvl, num, text, page, anchor):
    p = el('p'); pPr = etree.SubElement(p, W('pPr'))
    tabs = etree.SubElement(pPr, W('tabs'))
    left = 748 + (lvl - 1) * 397; numw = [567, 680, 850][lvl - 1]
    tabs.append(el('tab', val='left', pos=left + numw))
    tabs.append(el('tab', val='right', leader='dot', pos=RIGHT_TAB))
    pPr.append(el('spacing', after=100))
    pPr.append(el('ind', left=left + numw, right=307, hanging=numw))
    h = el('hyperlink', anchor=anchor, history=1)
    for r in (run(num), run('', tab=True), run(text), run('', tab=True), run(str(page))):
        h.append(r)
    p.append(h)
    return p

def build(d, hs, pages, first):
    body = d.element.body
    # título del índice
    tp = el('p'); tpp = etree.SubElement(tp, W('pPr'))
    tpp.append(el('pageBreakBefore')); tpp.append(el('ind', left=748))
    tp.append(run('Índice de Contenido', size=28))
    blocks = [tp, el('p')]
    ents = [entry(l, n, t, pages[i], a) for i, (l, n, t, a) in enumerate(hs)]
    ents[0].insert(1, fld('begin')); ents[0].insert(2, fld(None, ' TOC \\o "1-3" \\h \\z \\u '))
    ents[0].insert(3, fld('separate'))
    endp = el('p'); endp.append(fld('end'))
    blocks += ents + [endp]
    for b in blocks: first.addprevious(b)
    fpp = first.find(W('pPr'))
    if fpp.find(W('pageBreakBefore')) is None:
        prev = [e for e in fpp if e.tag in (W('pStyle'), W('keepNext'), W('keepLines'))]
        if prev: prev[-1].addnext(el('pageBreakBefore'))
        else: fpp.insert(0, el('pageBreakBefore'))

def pdf_pages(docx):
    tmp = tempfile.mkdtemp()
    subprocess.run(['python3', SOFFICE, '--headless', '--convert-to', 'pdf', '--outdir', tmp, docx],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    pdf = os.path.join(tmp, os.path.splitext(os.path.basename(docx))[0] + '.pdf')
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    out = []
    for i in range(1, n + 1):
        t = subprocess.run(['pdftotext', '-f', str(i), '-l', str(i), pdf, '-'], capture_output=True, text=True).stdout
        out.append(re.sub(r'\s+', '', t))
    return out

def locate(pages, hs):
    norm = lambda s: re.sub(r'\s+', '', s)
    toc_end = max(i for i, t in enumerate(pages) if 'ÍndicedeContenido' in t)
    # el índice puede ocupar más de una página: saltar todas las páginas con líneas de puntos del índice
    start = toc_end + 1
    while start < len(pages) and '.....' in pages[start]: start += 1
    res, cur = [], start
    for _, n, t, _a in hs:
        key = norm(n + t)
        for j in range(cur, len(pages)):
            if key in pages[j] or (norm(t) in pages[j] and norm(n) in pages[j]):
                res.append(j + 1); cur = j; break
        else:
            raise SystemExit('No se encontró el título en el PDF: %s %s' % (n, t))
    return res

d = Document(F)
raw = headings(d.element.body)
assert raw and raw[0][3] == 'OBJETIVO', raw[:2]
hs = [(l, n, t, mark(p, l, k)) for k, (p, l, n, t) in enumerate(raw)]
build(d, hs, ['0'] * len(hs), raw[0][0]); d.save(F)
pages = locate(pdf_pages(F), hs)
d = Document(F)
# reescribir los números de página
ents = [p for p in d.element.body.iter(W('p')) if p.find(W('hyperlink')) is not None and
        (p.find(W('hyperlink')).get(W('anchor')) or '').startswith('_Toc9')]
assert len(ents) == len(hs), (len(ents), len(hs))
for p, pg in zip(ents, pages):
    p.find(W('hyperlink')).findall(W('r'))[-1].find(W('t')).text = str(pg)
d.save(F)
chk = locate(pdf_pages(F), hs)
print('Índice:', os.path.basename(F), '| entradas:', len(hs), '| páginas OK' if chk == pages else '| AJUSTE: %s' % chk)
if chk != pages:
    d = Document(F)
    ents = [p for p in d.element.body.iter(W('p')) if p.find(W('hyperlink')) is not None and
            (p.find(W('hyperlink')).get(W('anchor')) or '').startswith('_Toc9')]
    for p, pg in zip(ents, chk):
        p.find(W('hyperlink')).findall(W('r'))[-1].find(W('t')).text = str(pg)
    d.save(F)
