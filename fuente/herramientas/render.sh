#!/bin/bash
# render.sh <docx> <outdir> : PDF + hoja de contactos
f="$1"; o="$2"; rm -rf "$o"; mkdir -p "$o"
python3 /mnt/skills/public/docx/scripts/office/soffice.py --headless --convert-to pdf --outdir "$o" "$f" >/dev/null 2>&1
cd "$o" && pdftoppm -jpeg -r 50 *.pdf p && python3 -c "
from PIL import Image;import glob
f=sorted(glob.glob('p-*.jpg'));ims=[Image.open(x) for x in f];w,h=ims[0].size;c=6;r=(len(ims)+c-1)//c
S=Image.new('RGB',(w*c,h*r),'white')
[S.paste(im,((i%c)*w,(i//c)*h)) for i,im in enumerate(ims)];S.save('sheet.jpg',quality=75);print(len(f),'páginas')"
