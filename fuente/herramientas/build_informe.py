"""Genera el informe general prediseñado SG-PEM-IFI-<SIGLA>-IN clonando el SG-PEM-IFI-SDI-2-IN de Martín.
Uso: python -I build_informe.py <SDI-2-IN.docx> <carpeta_tools> <carpeta_salida>"""
import copy, re, sys
sys.path.insert(0, sys.argv[2])
from docx import Document
from docx.oxml.ns import qn
from lxml import etree
import importlib
_m = importlib.import_module(sys.argv[4]) if len(sys.argv) > 4 else None
if _m:
    SISTEMAS, INFORMES = _m.SISTEMAS, _m.INFORMES
else:
    from planillas_data import SISTEMAS
    from informes_data import INFORMES
CODES = {'SAL': 'SG-PEM-IFI-SAL-1-IN'}

SRC, OUT = sys.argv[1], sys.argv[3]
W14 = '{http://schemas.microsoft.com/office/word/2010/wordml}'


def txt(e): return ''.join(t.text or '' for t in e.iter(qn('w:t')))


def set_runs(p, segs):
    """segs: [(texto, negrita)] manteniendo el formato del primer run."""
    r0 = p.find('.//' + qn('w:r'))
    rp = copy.deepcopy(r0.find(qn('w:rPr'))) if r0 is not None and r0.find(qn('w:rPr')) is not None else etree.Element(qn('w:rPr'))
    for t in ('w:b', 'w:bCs'):
        for e in rp.findall(qn(t)): rp.remove(e)
    for e in list(p):
        if e.tag != qn('w:pPr'): p.remove(e)
    for s, b in segs:
        r = etree.SubElement(p, qn('w:r')); rr = copy.deepcopy(rp)
        if b: rr.insert(0, etree.Element(qn('w:b')))
        r.append(rr); t = etree.SubElement(r, qn('w:t')); t.text = s
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    return p


def set_cell(tc, text):
    p = tc.find(qn('w:p'))
    for extra in tc.findall(qn('w:p'))[1:]: tc.remove(extra)
    set_runs(p, [(text, False)] if text else [])


for sig, S in SISTEMAS.items():
    if sig not in INFORMES: continue
    I = INFORMES[sig]; code = CODES.get(sig, 'SG-PEM-IFI-%s-IN' % sig); nom = S['nom']; cap = S['cap']
    d = Document(SRC); body = d.element.body; ch = list(body)
    ex = {k: ch[i] for k, i in dict(title=0, sub=1, empty=2, h1a=3, emptyc=4, t1=5, sp=6, h1b=7, empty2=8, t2=9,
                                    h1=11, p=12, h2=16, li=41, anx=54).items()}
    C = lambda k: copy.deepcopy(ex[k])
    new = []
    new.append(set_runs(C('title'), [('INFORME GENERAL – %s' % nom.upper(), True)]))
    new.append(set_runs(C('sub'), [('Procedimiento SG-PEM-IFI-%s · IRAM 3546:2011, capítulo %s' % (sig, cap), True)]))
    new.append(C('empty'))
    t1 = C('t1')
    if 'periodo' in I:  # opciones de período propias del sistema
        for tt in t1.iter(qn('w:t')):
            if tt.text and 'TRIMESTRAL' in tt.text: tt.text = I['periodo']
    new.append(C('h1a')); new.append(C('emptyc')); new.append(t1); new.append(C('sp'))
    new.append(C('h1b')); new.append(C('empty2'))
    # tabla de identificación del sistema
    t2 = C('t2'); trs = t2.findall(qn('w:tr')); first, model = trs[0], trs[1]
    for r in trs: t2.remove(r)
    tcs = first.findall(qn('w:tc'))
    for tc, val in zip(tcs, I['equipo']): set_cell(tc, val)
    t2.append(first)
    for lab, val in I['ident']:
        r = copy.deepcopy(model); a, b = r.findall(qn('w:tc'))
        set_cell(a, lab); set_cell(b, val); t2.append(r)
    new.append(t2); new.append(C('sp'))
    n = 3
    def h1(t):
        global n
        new.append(set_runs(C('h1'), [('%d. %s' % (n, t), True)])); n += 1
    P = lambda t: new.append(set_runs(C('p'), [(t, False)]))
    h1('OBJETIVO')
    P('Evaluar el estado de funcionamiento, confiabilidad y disponibilidad operativa del %s, conforme a los requisitos de '
      'inspección, prueba y mantenimiento establecidos en el capítulo %s de la IRAM 3546:2011 y en el procedimiento '
      'SG-PEM-IFI-%s.' % (nom.lower(), cap, sig))
    h1('ALCANCE')
    P('El presente informe integra las actividades de inspección, prueba y mantenimiento del %s, incluyendo %s, conforme a '
      'los registros completados en el período evaluado.' % (nom.lower(), I['alcance']))
    h1('RESULTADOS DE LA EVALUACIÓN')
    for k, (tit, frases) in enumerate(I['resultados'], 1):
        new.append(set_runs(C('h2'), [('%d.%d %s' % (n - 1, k, tit), True)]))
        for f in frases: P(f)
    h1('ANÁLISIS TÉCNICO INTEGRADO')
    P('De la evaluación conjunta, el sistema presenta un nivel de conformidad del [______ %], con [______] desvíos registrados.')
    P('Las desviaciones detectadas afectan principalmente [%s], impactando en la disponibilidad operativa del sistema.'
      % ' / '.join(t for t, _ in I['resultados'][1:]))
    h1('CONDICIÓN DE CUMPLIMIENTO NORMATIVO')
    P('En función de los resultados obtenidos, el sistema se clasifica como:')
    P('[CONFORME / PARCIALMENTE CONFORME / NO CONFORME] respecto de los requisitos establecidos por la IRAM 3546:2011, '
      'capítulo %s, en base a:' % cap)
    for c in I['criterios']:
        new.append(set_runs(C('li'), [(c, False)]))
    h1('NO CONFORMIDADES DETECTADAS')
    for k in (1, 2, 3):
        P(I.get('nc', 'NC-%02d: ______ → Incumplimiento IRAM 3546:2011, capítulo {cap}, ítem ______').replace('{cap}', cap) % k)
    h1('CONCLUSIÓN')
    P('El sistema presenta un nivel de desempeño [ADECUADO / DEFICIENTE], requiriendo [ACCIONES CORRECTIVAS: ______] para su '
      'adecuación normativa.')
    P('Se recomienda la implementación de las medidas correctivas a fin de garantizar el cumplimiento de la IRAM 3546:2011 y '
      'asegurar la disponibilidad operativa del sistema desde el primer momento en que deba actuar.')
    h1('ANEXOS (EVIDENCIA DOCUMENTAL)')
    P('Se adjuntan los siguientes registros como respaldo de la presente evaluación:')
    for p in S['planillas']:
        new.append(set_runs(C('anx'), [('SG-PEM-IFI-%s-%d %s %s' % (sig, p['n'], p['nombre'], sig), False)]))
    sect = ch[-1]
    for e in ch: body.remove(e)
    for e in new + [sect]: body.append(e)
    # encabezado: código del informe
    hdr = d.sections[0].header.part.element
    ts = [t for t in hdr.iter(qn('w:t'))]
    i0 = next(i for i, t in enumerate(ts) if (t.text or '').startswith('SG-'))
    i1 = next(i for i in range(i0, len(ts)) if (ts[i].text or '').endswith('-IN'))
    ts[i0].text = code
    for t in ts[i0 + 1:i1 + 1]: t.text = ''
    for t in hdr.iter(qn('w:t')):
        if t.text and 'ESPECIFICO' in t.text: t.text = t.text.replace('ESPECIFICO', 'ESPECÍFICO')
    for e in d.element.iter():
        for a in (W14 + 'paraId', W14 + 'textId'):
            if a in e.attrib: del e.attrib[a]
    d.core_properties.title = '%s Informe general %s' % (code, nom)
    import os; os.makedirs('%s/%s' % (OUT, sig), exist_ok=True)
    fn = '%s/%s/%s_INFORME_GENERAL_DEL_%s.docx' % (OUT, sig, code, sig)
    d.save(fn); print(fn)
