"""Genera los cuatro iconos públicos RP, con margen para máscaras del sistema."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]

def main():
    candidates=[Path('C:/Windows/Fonts/arialbd.ttf'),Path('/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf')]
    font_path=next((p for p in candidates if p.is_file()),None)
    if font_path is None:raise FileNotFoundError('Se requiere Arial Bold o Liberation Sans Bold para generar los iconos.')
    dest=ROOT/'app/static/icons';dest.mkdir(exist_ok=True)
    for size in (192,512):
        for maskable in (False,True):
            scale=3;side=size*scale
            image=Image.new('RGB',(side,side),'#1d4ed8');draw=ImageDraw.Draw(image)
            font=ImageFont.truetype(str(font_path),int(side*(.43 if maskable else .52)))
            left,top,right,bottom=draw.textbbox((0,0),'RP',font=font)
            draw.text(((side-(right-left))/2-left,(side-(bottom-top))/2-top),'RP',font=font,fill='white')
            image=image.resize((size,size),Image.Resampling.LANCZOS)
            name=f'icon-maskable-{size}.png' if maskable else f'icon-{size}x{size}.png'
            image.save(dest/name,optimize=True)

if __name__=='__main__':main()
