"""Plantilla v3: jerarquía de títulos escalonada como el modelo matriz (SDI de Martín), línea inferior en los
títulos de nivel 1 y pie de página idéntico al modelo (Autor | Pág. X de Y).
Uso: python -I upgrade_template.py <plantilla_v2.docx> <modelo_SDI_Martin.docx> <plantilla_v3.docx>"""
import re, sys, zipfile

SRC, MODELO, OUT = sys.argv[1:4]
z = zipfile.ZipFile(SRC); files = {n: z.read(n) for n in z.namelist()}
mz = zipfile.ZipFile(MODELO)

# ---- 1. numeración escalonada de 3.1 / 3.1.1 / 3.1.1.1 (abstractNum 40) ----
# Texto del cuerpo a 748 twips (1,32 cm). Números de título: nivel 1 a 748, 3.1 a 1145, 3.1.1 a 1542, 3.1.1.1 a 1939.
IND = {'1': (1825, 680), '2': (2392, 850), '3': (3016, 1077)}
nb = files['word/numbering.xml'].decode()
m = re.search(r'<w:abstractNum [^>]*w:abstractNumId="40".*?</w:abstractNum>', nb, re.S)
a = m.group(0)
for lvl, (left, hang) in IND.items():
    a = re.sub(r'(<w:lvl w:ilvl="%s".*?<w:ind )w:left="\d+" w:hanging="\d+"' % lvl,
               r'\1w:left="%d" w:hanging="%d"' % (left, hang), a, count=1, flags=re.S)
nb = nb.replace(m.group(0), a)
files['word/numbering.xml'] = nb.encode()

# ---- 2. títulos de nivel 1 (OBJETIVO, ALCANCE, PROCEDIMIENTOS, ANEXOS): alineados con el texto y con línea inferior ----
doc = files['word/document.xml'].decode()
L1 = ('<w:pPr><w:keepNext/><w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr>'
      '<w:pBdr><w:bottom w:val="single" w:sz="4" w:space="1" w:color="auto"/></w:pBdr>'
      '<w:ind w:left="1315" w:right="307" w:hanging="567"/><w:jc w:val="left"/><w:outlineLvl w:val="0"/>')
n1 = 0
def fix_l1(mm):
    global n1; n1 += 1
    return L1
doc = re.sub(r'<w:pPr><w:numPr><w:ilvl w:val="0"/><w:numId w:val="2"/></w:numPr><w:ind w:left="1701" w:right="307" '
             r'w:hanging="283"/><w:jc w:val="both"/>', fix_l1, doc)
assert n1 == 4, n1
# «(Basado en…)» alineado con el texto del 3.1
nb_ = doc.count('<w:ind w:left="2484" w:right="307"/>')
doc = doc.replace('<w:ind w:left="2484" w:right="307"/>', '<w:ind w:left="1825" w:right="307"/>')
assert nb_ >= 1, nb_
# distancia del pie como en el modelo (227), para que el pie más alto no desplace la portada
assert doc.count('w:footer="907"') == 1
doc = doc.replace('w:footer="907"', 'w:footer="113"')
files['word/document.xml'] = doc.encode()

# ---- 3. pie de página del modelo ----
rels = files['word/_rels/document.xml.rels'].decode()
ftr = re.search(r'Target="(footer\d+\.xml)"', rels).group(1)
fx = mz.read('word/footer1.xml').decode()
# Mismo pie que el modelo (tabla Autor | Pág. X de Y). Se quitan los párrafos vacíos de relleno que el modelo tiene
# antes y después de la tabla, para que el pie entre en el margen inferior de la serie sin desplazar la portada.
i = fx.index('<w:tbl>'); j = fx.index('</w:tbl>') + len('</w:tbl>')
head = fx[:fx.index('<w:p ')]
TAIL = ('<w:p><w:pPr><w:pStyle w:val="Piedepgina"/><w:spacing w:before="0" w:after="0" w:line="240" w:lineRule="auto"/>'
        '<w:rPr><w:sz w:val="4"/><w:szCs w:val="4"/></w:rPr></w:pPr></w:p>')
files['word/' + ftr] = (head + fx[i:j] + TAIL + '</w:ftr>').encode()

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as o:
    for n, data in files.items():
        o.writestr(n, data)
print('plantilla v3:', OUT, '| títulos nivel 1:', n1, '| basado:', nb_)
