"""Construye la plantilla maestra SG-PEM-IFI a partir del manual SBC (plantilla nueva).
Conserva portada, encabezado, pie, estilos, numeración y textos comunes; reemplaza el
contenido específico del sistema por un esqueleto con marcadores {{...}} e [INSTRUCCIÓN]."""
import copy, sys, re
from docx import Document
from docx.oxml.ns import qn
from lxml import etree

SRC, OUT = sys.argv[1], sys.argv[2]
d = Document(SRC)
body = d.element.body
ch = list(body)
X = lambda i: copy.deepcopy(ch[i])

# ---------- numeración: listas que reinician en a) / 1) ----------
numbering = d.part.numbering_part.element
def abstract_of(num_id):
    for n in numbering.findall(qn('w:num')):
        if n.get(qn('w:numId')) == str(num_id):
            return n.find(qn('w:abstractNumId')).get(qn('w:val'))
next_id = [max(int(n.get(qn('w:numId'))) for n in numbering.findall(qn('w:num'))) + 1]
def new_num(template_num_id):
    a = abstract_of(template_num_id)
    nid = next_id[0]; next_id[0] += 1
    n = etree.Element(qn('w:num')); n.set(qn('w:numId'), str(nid))
    numbering.findall(qn('w:num'))[-1].addnext(n)
    e = etree.SubElement(n, qn('w:abstractNumId')); e.set(qn('w:val'), a)
    lo = etree.SubElement(n, qn('w:lvlOverride')); lo.set(qn('w:ilvl'), '0')
    so = etree.SubElement(lo, qn('w:startOverride')); so.set(qn('w:val'), '1')
    return nid

# ---------- helpers de párrafo ----------
def base_rpr(p):
    r = p.find('.//' + qn('w:r'))
    rp = r.find(qn('w:rPr')) if r is not None else None
    rp = copy.deepcopy(rp) if rp is not None else etree.Element(qn('w:rPr'))
    for tag in ('w:b', 'w:bCs'):
        for e in rp.findall(qn(tag)): rp.remove(e)
    return rp

def para(ex_idx, segments, num_id=None):
    """segments: lista de (texto, negrita)."""
    p = X(ex_idx); rp = base_rpr(p)
    for r in list(p):
        if r.tag != qn('w:pPr'): p.remove(r)
    for text, bold in segments:
        if not text: continue
        r = etree.SubElement(p, qn('w:r')); rr = copy.deepcopy(rp)
        b = etree.Element(qn('w:b')); bc = etree.Element(qn('w:bCs'))
        if not bold: b.set(qn('w:val'), '0'); bc.set(qn('w:val'), '0')
        rr.insert(0, bc); rr.insert(0, b); r.append(rr)
        t = etree.SubElement(r, qn('w:t')); t.text = text
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    if num_id is not None:
        np_ = p.find('.//' + qn('w:numId')); np_.set(qn('w:val'), str(num_id))
    return p

# ejemplares (índices de párrafo del manual SBC)
H31, BASADO, VACIO, CUERPO, H311, H3111 = 85, 86, 89, 88, 112, 116
ITEM, VINETA, PROTO, PASO, ETIQ, TABLA, REG, ANEXO = 94, 122, 197, 199, 490, 345, 533, 540
ITEM_NUM, PASO_NUM = 205, 261

new = []
def add(p): new.append(p)
def vacio(): add(X(VACIO))
def cuerpo(text): add(para(CUERPO, [(text, False)])); vacio()
def instr(text): add(para(CUERPO, [('[INSTRUCCIÓN: ' + text + ']', False)])); vacio()
def keep_next(p):
    ppr = p.find(qn('w:pPr'))
    if ppr.find(qn('w:keepNext')) is None:
        kn = etree.Element(qn('w:keepNext'))
        st = ppr.find(qn('w:pStyle'))
        (st.addnext(kn) if st is not None else ppr.insert(0, kn))
    return p
def vacio_kn(): add(keep_next(X(VACIO)))
def h(idx, text): add(keep_next(para(idx, [(text, True)]))); vacio_kn()
def lista(items, label_bold=True):
    nid = new_num(ITEM_NUM)
    for lab, txt in items:
        add(para(ITEM, [(lab, label_bold), (txt, False)], nid))
    vacio()
def vinetas(items):
    for lab, txt in items:
        add(para(VINETA, [(lab, True), (txt, False)] if lab else [(txt, False)]))
    vacio()
def etiqueta(lab, txt): add(para(ETIQ, [(lab, True), (' ' + txt, False)])); vacio()

def bloque_frecuencia(titulo, intro_verbo, n_planilla):
    h(H3111, titulo)
    cuerpo('{{Frase de finalidad: Las <actividades> <frecuencia> tienen como finalidad / permiten / están orientadas a verificar …}}')
    cuerpo(intro_verbo)
    lista([('{{Elemento o componente}}: ', '{{verbo en infinitivo (verificar, comprobar, controlar, registrar) + qué se controla + criterio de aceptación con el valor exacto de la norma}}.'),
           ('{{Elemento o componente}}: ', '{{…}}.')])
    cuerpo('{{Criterio o acción ante desvío, si la norma lo indica: Si <condición medida> <supera / es menor que> <valor>, se debe <acción>.}}')
    cuerpo('Los resultados deben registrarse en la planilla SG-PEM-IFI-{{SIGLA}}-' + n_planilla + ' {{Nombre del sistema}} – {{Tipo de planilla}}.')

# ---------- esqueleto del capítulo del sistema ----------
add(keep_next(para(H31, [('{{NOMBRE DEL SISTEMA EN MAYÚSCULAS}}', True)])))
add(para(BASADO, [('(Basado en IRAM 3546:2011 – Capítulo {{N}})', False)])); vacio()
cuerpo('Este apartado establece los requisitos mínimos para la inspección, prueba y mantenimiento del {{nombre del sistema}}, con el objetivo de asegurar que {{resultado operativo que debe garantizar el sistema}} en condiciones de emergencia.')
cuerpo('{{Descripción general del sistema: qué es, cómo actúa ante un incendio y por qué su funcionamiento es crítico.}}')
cuerpo('El equipamiento del sistema incluye:')
lista([('{{Componente}}: ', '{{función del componente}}.'), ('{{Componente}}: ', '{{función del componente}}.'),
       ('Equipos auxiliares, tales como:', '')])
vinetas([('', '{{accesorio}};'), ('', '{{accesorio}}.')])
instr('Si el sistema actúa con una secuencia automática (detección, alarma, retardo, descarga, funciones auxiliares), describirla aquí en uno o dos párrafos. Si no aplica, borrar esta instrucción.')
cuerpo('Antes de realizar cualquier actividad de inspección o prueba que pueda generar alarmas o descargas, se deberá notificar previamente al responsable del sistema o al servicio de monitoreo correspondiente.')

h(H311, '  INSPECCIÓN')
cuerpo('La inspección consiste en la verificación visual del sistema y de sus componentes, con el fin de comprobar que se encuentran en condiciones aparentes de funcionamiento, sin daños físicos, obstrucciones o alteraciones que puedan afectar su operatividad. Se realiza recorriendo las zonas protegidas.')
cuerpo('Las inspecciones de frecuencia menor a un mes pueden ser completadas por el usuario de la instalación como inspecciones de autocontrol; el mantenedor debe verificar su correcto cumplimiento, dejando constancia de los hallazgos.')
bloque_frecuencia('Inspección {{frecuencia}}', 'Durante esta inspección se debe verificar:', '{{n}}')
instr('Repetir el bloque anterior (subtítulo 3.1.1.x) para cada frecuencia de inspección de la norma, en el mismo orden que la norma: diaria, semanal, mensual, trimestral, semestral, anual, cada N años.')

h(H311, '  PRUEBA')
cuerpo('Las pruebas consisten en verificaciones funcionales destinadas a comprobar el correcto funcionamiento de los equipos y dispositivos del sistema, y permiten detectar fallas operativas que no pueden observarse únicamente mediante inspección visual. Cuando durante las pruebas se detecten fallas o anomalías, se debe proceder inmediatamente a su reparación o mantenimiento.')
bloque_frecuencia('Prueba {{frecuencia}}', 'Durante estas pruebas se debe verificar:', '{{n}}')
add(keep_next(para(PROTO, [('Protocolo de Ensayo: {{nombre del ensayo}}', True)]))); vacio_kn()
pn = new_num(PASO_NUM)
add(keep_next(para(PASO, [('{{Paso del ensayo}}', True)], pn))); vacio_kn()
etiqueta('Paso a paso:', '{{cómo se ejecuta, qué instrumento se usa y dónde se mide}}.')
etiqueta('Justificación técnica:', '{{qué falla o riesgo detecta este paso y por qué el valor límite importa}}.')
etiqueta('Criterio de aceptación:', '{{valor o condición que debe cumplirse, tomado de la norma o del fabricante}}.')
add(keep_next(para(PASO, [('{{Paso del ensayo}}', True)], pn))); vacio_kn()
etiqueta('Paso a paso:', '{{…}}.')
etiqueta('Justificación técnica:', '{{…}}.')
instr('El protocolo de ensayo se incluye sólo para pruebas con mediciones o maniobras (arranques, caudales, presiones, descargas simuladas, estanqueidad). Repetir el bloque de prueba para cada frecuencia de la norma.')
t = X(TABLA)
rows = t.findall(qn('w:tr'))
for r in rows[2:]: t.remove(r)
for ri, r in enumerate(t.findall(qn('w:tr'))):
    for ci, tc in enumerate(r.findall(qn('w:tc'))):
        ts = tc.findall('.//' + qn('w:t'))
        for k, tt in enumerate(ts): tt.text = ('{{Encabezado}}' if ri == 0 else '{{Valor}}') if k == 0 else ''
add(para(CUERPO, [('[INSTRUCCIÓN: tabla opcional para valores de referencia. Borrar si no se usa.]', False)])); add(t); vacio()

h(H311, '  MANTENIMIENTO')
cuerpo('El mantenimiento comprende las tareas destinadas a conservar los equipos y componentes del sistema en condiciones adecuadas de funcionamiento y confiabilidad. Estas tareas deben realizarse inmediatamente después de detectar fallas durante las inspecciones o pruebas.')
bloque_frecuencia('Mantenimiento {{frecuencia}}', 'Durante estas tareas se debe realizar:', '{{n}}')

h(H311, '  {{SECCIÓN COMPLEMENTARIA}}')
instr('Agregar sólo si la norma o el tipo de sistema lo justifica, una sección por tema, en este orden: Ensayos de largo plazo (cada 3, 5, 20 o 50 años); Procedimiento posterior a una descarga o actuación; Seguridad y salud ocupacional; Control de cambios; Responsabilidades. Si no corresponde ninguna, borrar este subtítulo.')

h(H311, '  REGISTRO DE INSPECCIONES, PRUEBAS Y MANTENIMIENTO')
cuerpo('Todos los resultados obtenidos durante las tareas de inspección, prueba y mantenimiento deben registrarse en las planillas correspondientes del presente procedimiento, las cuales constituyen evidencia documental del mantenimiento del sistema y deben contener al menos:')
lista([('Fecha de la actividad.', ''), ('Nombre del inspector.', ''), ('Resultados de la inspección, prueba o mantenimiento.', '')], label_bold=False)
cuerpo('Las planillas deben incluir la identificación de la empresa como mantenedor certificado. Las tareas que no resulten aplicables a la instalación deben indicarse con la leyenda «NO APLICABLE» o la abreviatura «NA». Se debe entregar al usuario una copia de cada planilla completada, bajo constancia de recepción.')

# ---------- armado del cuerpo ----------
sect = ch[-1]
tail = [X(538), X(539)]
for k in (1, 2):
    tail.append(para(ANEXO, [('SG-PEM-IFI-{{SIGLA}}-%d {{NOMBRE DE LA PLANILLA}}. {{Nombre del sistema}}' % k, False)]))
tail += [X(i) for i in range(543, 547)]
for e in ch: body.remove(e)
for e in ch[:85] + new + tail + [sect]: body.append(e)

# ---------- portada y encabezado ----------
def set_text(p, text):
    rs = p.findall('.//' + qn('w:r'))
    ts = [t for r in rs for t in r.findall(qn('w:t'))]
    ts[0].text = text
    for t in ts[1:]: t.text = ''
paras = body.findall(qn('w:p'))
for p in paras[:6]:
    txt = ''.join(t.text or '' for t in p.iter(qn('w:t')))
    if 'BOMBAS' in txt: set_text(p, '{{NOMBRE DEL SISTEMA}}')
    elif txt.startswith('SG-'): set_text(p, 'SG-PEM-IFI-{{SIGLA}}')
for hdr in d.sections[0].header.part.element.iter(qn('w:t')):
    if hdr.text == '-SBC': hdr.text = '-{{SIGLA}}'
    if hdr.text and 'Sistema de Bombas' in hdr.text: hdr.text = ' ({{Nombre del sistema}})'

# ---------- quitar imágenes del cuerpo que ya no se usan ----------
used = set(re.findall(r'r:(?:embed|id)="([^"]+)"', etree.tostring(d.element).decode()))
for rid, rel in list(d.part.rels.items()):
    if 'image' in rel.reltype and rid not in used:
        d.part.drop_rel(rid)


# ---------- correcciones de la auditoría ----------
W14 = '{http://schemas.microsoft.com/office/word/2010/wordml}'
for e in d.element.iter():
    for a in (W14 + 'paraId', W14 + 'textId'):
        if a in e.attrib: del e.attrib[a]
st = d.styles.element
for s_ in st.findall(qn('w:style')):
    if s_.get(qn('w:styleId')) == 'titulo2':
        ppr = s_.find(qn('w:pPr'))
        etree.SubElement(ppr, qn('w:keepNext')); jc = etree.SubElement(ppr, qn('w:jc')); jc.set(qn('w:val'), 'left')
        # orden de esquema: keepNext antes de numPr, jc al final
        ppr.remove(ppr[-2]); ppr.insert(0, etree.Element(qn('w:keepNext')))
def fix_text(root):
    for t in root.iter(qn('w:t')):
        if t.text in ('REALIZO', 'REVISO', 'APROBO'): t.text = t.text[:-1] + 'Ó'
        elif t.text == 'RE' : pass
        if t.text and 'ESPECIFICO' in t.text: t.text = t.text.replace('ESPECIFICO', 'ESPECÍFICO')
        if t.text and 'ANEXOS Y REGISTROS' in t.text: t.text = t.text.replace('ANEXOS Y REGISTROS', 'ANEXOS O REGISTROS')
        if t.text == ' Y REGISTROS': t.text = ' O REGISTROS'
fix_text(d.element)
for hp in (d.sections[0].header, d.sections[0].footer): fix_text(hp.part.element)
# REVISO partido en dos runs ('RE','VISO')
for t in d.element.iter(qn('w:t')):
    if t.text == 'VISO': t.text = 'VISÓ'
# cap. 4 en 12 pt
for p in body.findall(qn('w:p')):
    if 'ANEXOS O REGISTROS' in ''.join(x.text or '' for x in p.iter(qn('w:t'))):
        for sz in p.iter(qn('w:sz')): sz.set(qn('w:val'), '24')
# tabla de ejemplo dentro de la sangría del texto (748 izq., ancho útil 9724)
for tbl in body.findall(qn('w:tbl')):
    tp = tbl.find(qn('w:tblPr'))
    for e in tp.findall(qn('w:tblInd')): tp.remove(e)
    tw = tp.find(qn('w:tblW'))
    ind = etree.Element(qn('w:tblInd')); ind.set(qn('w:type'), 'dxa')
    anchor = next((tp.find(qn(t)) for t in ('w:tblCellSpacing', 'w:jc') if tp.find(qn(t)) is not None), tw)
    anchor.addnext(ind); tw.set(qn('w:type'), 'dxa')
    tp.find(qn('w:tblW')).set(qn('w:w'), '9724'); tp.find(qn('w:tblInd')).set(qn('w:w'), '748')
    cols = tbl.find(qn('w:tblGrid')).findall(qn('w:gridCol'))
    for c in cols: c.set(qn('w:w'), str(9724 // len(cols)))
    for tc in tbl.iter(qn('w:tcW')): tc.set(qn('w:w'), str(9724 // len(cols))); tc.set(qn('w:type'), 'dxa')
d.core_properties.title = ''

d.save(OUT)
print('ok', len(new), 'párrafos de esqueleto')
