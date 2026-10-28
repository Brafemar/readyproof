"""Renderiza los PDF de prueba y prepara láminas para inspección visual."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess

from PIL import Image,ImageDraw
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'out/etapa5_planillas'


def render(pdf):
    target=OUT/'revision_visual'/pdf.stem;target.mkdir(parents=True,exist_ok=True)
    subprocess.run([shutil.which('pdftoppm'),'-scale-to','1400','-png',str(pdf),str(target/'pagina')],
        check=True,capture_output=True,timeout=120)
    reader=PdfReader(pdf)
    return {'codigo':pdf.stem,'paginas':len(reader.pages),'sha256':sha256(pdf.read_bytes()).hexdigest(),
        'imagenes':[str(p.relative_to(OUT)) for p in sorted(target.glob('pagina-*.png'))]}


def main():
    files=sorted((OUT/'pdf_verificados').glob('*.pdf'));assert len(files)==63
    with ThreadPoolExecutor(max_workers=3) as pool:reports=list(pool.map(render,files))
    pages=[(row['codigo'],n,p) for row in reports for n,p in enumerate(row['imagenes'],1)]
    for offset in range(0,len(pages),12):
        sheet=Image.new('RGB',(1800,990),'#b6b6b6');draw=ImageDraw.Draw(sheet)
        for index,(code,number,path) in enumerate(pages[offset:offset+12]):
            x=(index%4)*450;y=(index//4)*330
            draw.text((x+8,y+5),f'{code} / {number}',fill='black')
            with Image.open(OUT/path) as im:
                im.thumbnail((444,304));sheet.paste(im,(x+(450-im.width)//2,y+24))
        sheet.save(OUT/'revision_visual'/f'lamina-{offset//12+1:02}.png')
    (OUT/'revision_visual/indice.json').write_text(json.dumps(reports,indent=2),encoding='utf-8')
    print(json.dumps({'pdf':len(reports),'paginas':len(pages),'laminas':(len(pages)+11)//12}))


if __name__=='__main__':main()
