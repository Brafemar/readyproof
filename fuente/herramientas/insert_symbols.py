"""Reemplaza los marcadores §sym:clave§ de las tablas por la imagen del símbolo y ajusta el ancho de columnas.
Uso: python -I insert_symbols.py <manual.docx> <carpeta_png>"""
import os, re, sys
from docx import Document
from docx.shared import Cm
from docx.oxml.ns import qn
F, D = sys.argv[1:3]
d = Document(F); n = 0; miss = []
W = [2400, 3650, 3674]
for t in d.tables:
    marked = any('§sym:' in c.text for r in t.rows for c in r.cells)
    if not marked: continue
    grid = t._tbl.find(qn('w:tblGrid'))
    for g, w in zip(grid.findall(qn('w:gridCol')), W): g.set(qn('w:w'), str(w))
    for r in t.rows:
        for c, w in zip(r.cells, W):
            c._tc.find('.//' + qn('w:tcW')).set(qn('w:w'), str(w))
        cell = r.cells[0]
        m = re.search(r'§sym:([\w]+)§', cell.text)
        if not m: continue
        key = m.group(1); png = os.path.join(D, key + '.png')
        if not os.path.exists(png): miss.append(key); continue
        p = cell.paragraphs[0]
        for run in p.runs: run.text = ''
        p.alignment = 1
        p.add_run().add_picture(png, height=Cm(1.3)); n += 1
d.save(F)
assert not miss, miss
print('símbolos insertados:', n)
