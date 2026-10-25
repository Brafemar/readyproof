"""Deja los metadatos de las planillas .xlsx como los de las planillas originales de BRAFEMAR (sin «openpyxl»).
Uso: python -I limpiar_metadatos.py <carpeta>"""
import sys, os, re, zipfile, shutil, tempfile
n = 0
for root, _, files in os.walk(sys.argv[1]):
    for f in files:
        if not f.endswith('.xlsx'): continue
        p = os.path.join(root, f); z = zipfile.ZipFile(p); items = [(i, z.read(i.filename)) for i in z.infolist()]; z.close()
        out = []
        for i, data in items:
            if i.filename == 'docProps/core.xml':
                t = data.decode()
                fechas = re.findall(r'<dcterms:(created|modified)[^>]*>([^<]*)</dcterms:\1>', t)
                d = dict(fechas)
                t = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                     '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
                     'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
                     'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
                     '<dc:creator></dc:creator><cp:lastModifiedBy></cp:lastModifiedBy>'
                     + ''.join('<dcterms:%s xsi:type="dcterms:W3CDTF">%s</dcterms:%s>' % (k, d[k], k) for k in ('created', 'modified') if k in d)
                     + '</cp:coreProperties>')
                data = t.encode()
            elif i.filename == 'docProps/app.xml':
                t = data.decode()
                t = re.sub(r'<Application>[^<]*</Application>', '<Application>Microsoft Excel</Application>', t)
                t = re.sub(r'<AppVersion>[^<]*</AppVersion>', '<AppVersion>16.0300</AppVersion>', t)
                data = t.encode()
            out.append((i, data))
        tmp = p + '.tmp'
        with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as o:
            for i, data in out: o.writestr(i, data)
        shutil.move(tmp, p); n += 1
print('planillas limpiadas:', n)
