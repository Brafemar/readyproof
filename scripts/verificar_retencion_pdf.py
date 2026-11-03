"""Compara PDF de modelos: solo admite T.C. 2 años -> T.C. 3 AÑOS."""
import argparse
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re

from pypdf import PdfReader

RETENCION_ANTERIOR = re.compile(r'T\.C\.\s*2\s*AÑOS', re.IGNORECASE)
RETENCION_NUEVA = 'T.C. 3 AÑOS'


def comparar_retencion_pdf(antes, despues):
    def reader(value):
        return PdfReader(BytesIO(value) if isinstance(value, bytes) else value)
    old, new = reader(antes), reader(despues)
    if old.is_encrypted or new.is_encrypted or not old.pages or not new.pages:
        raise ValueError('Los PDF deben ser legibles, sin cifrar y con páginas.')
    if len(old.pages) != len(new.pages):
        raise ValueError('Cambió la cantidad de páginas del PDF.')
    pages, changes = [], 0
    for number, (a, b) in enumerate(zip(old.pages, new.pages), 1):
        text_a, text_b = a.extract_text() or '', b.extract_text() or ''
        expected, count = RETENCION_ANTERIOR.subn(RETENCION_NUEVA, text_a)
        if expected != text_b:
            raise ValueError(f'El PDF tiene diferencias de texto ajenas a la retención en la página {number}.')
        if list(a.mediabox) != list(b.mediabox):
            raise ValueError(f'Cambiaron las dimensiones de la página {number}.')
        images_a = [sha256(image.data).hexdigest() for image in a.images]
        images_b = [sha256(image.data).hexdigest() for image in b.images]
        if images_a != images_b:
            raise ValueError(f'Cambiaron imágenes en la página {number}.')
        pages.append(dict(pagina=number, reemplazos=count, texto_solo_cambia_retencion=True,
                          imagenes_identicas=True, imagenes_sha256=images_a,
                          ancho_pt=float(a.mediabox.width), alto_pt=float(a.mediabox.height)))
        changes += count
    if not changes:
        raise ValueError('No se encontró el cambio esperado de T.C. 2 años a T.C. 3 AÑOS.')
    return dict(comprobador='pypdf', paginas=pages, reemplazos_totales=changes,
                solo_cambio_texto_retencion=True,
                metadatos='No se comparan fechas ni identificadores internos; no son contenido visible.')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('antes',type=Path);parser.add_argument('despues',type=Path)
    parser.add_argument('--salida',type=Path)
    args=parser.parse_args()
    result=comparar_retencion_pdf(args.antes,args.despues)
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if args.salida:
        with args.salida.open('x',encoding='utf-8') as output:output.write(text)
    print(text)


if __name__=='__main__':main()
