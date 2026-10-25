# -*- coding: utf-8 -*-
"""fix_numpages.py <manual.docx> [manual.pdf]
Escribe en el campo NUMPAGES del pie el total real de páginas, para que el «Pág. X de Y» se vea bien
aunque el lector no actualice campos. Si no se da el PDF, renderiza el .docx con LibreOffice."""
import os, re, shutil, subprocess, sys, tempfile, zipfile


def paginas(pdf):
    out = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    return int(re.search(r'^Pages:\s+(\d+)', out, re.M).group(1))


def main(docx, pdf=None):
    tmp = tempfile.mkdtemp()
    try:
        if not pdf:
            subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp, docx],
                           capture_output=True, check=True)
            pdf = os.path.join(tmp, os.path.splitext(os.path.basename(docx))[0] + '.pdf')
        n = paginas(pdf)
        pat = re.compile(r'(NUMPAGES[^>]*>(?:<w:r>(?:<w:rPr>.*?</w:rPr>)?<w:t>))\d+(</w:t>)', re.S)
        nuevo = os.path.join(tmp, 'x.docx')
        cambios = 0
        with zipfile.ZipFile(docx) as zi, zipfile.ZipFile(nuevo, 'w', zipfile.ZIP_DEFLATED) as zo:
            for it in zi.infolist():
                data = zi.read(it.filename)
                if re.match(r'word/footer\d*\.xml$', it.filename):
                    txt, k = pat.subn(lambda m: m.group(1) + str(n) + m.group(2), data.decode('utf-8'))
                    cambios += k
                    data = txt.encode('utf-8')
                zo.writestr(it, data)
        shutil.move(nuevo, docx)
        print('%s: NUMPAGES = %d (%d campos)' % (os.path.basename(docx), n, cambios))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main(*sys.argv[1:3])
