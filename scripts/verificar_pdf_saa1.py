"""Regenera imágenes de revisión; las verificaciones pertenecen a pytest."""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw
from pypdf import PdfReader
import pypdfium2 as pdfium


def render(path):
    document = pdfium.PdfDocument(path)
    images = []
    for page in document:
        images.append(page.render(scale=1.8).to_pil().convert("RGB"))
        page.close()
    document.close()
    return images


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--referencia", type=Path, required=True)
    parser.add_argument("--blanca", type=Path, required=True)
    parser.add_argument("--piloto", type=Path, required=True)
    parser.add_argument("--salida", type=Path, required=True)
    args = parser.parse_args()
    args.salida.mkdir(parents=True, exist_ok=False)
    paths = {"referencia": args.referencia, "blanca": args.blanca, "piloto": args.piloto}
    readers = {key: PdfReader(path) for key, path in paths.items()}
    counts = {key: len(reader.pages) for key, reader in readers.items()}
    renders = {key: render(path) for key, path in paths.items()}
    for key, images in renders.items():
        for index, image in enumerate(images, 1):
            image.save(args.salida / f"{key}_pagina_{index}.png")
    left, right = renders["referencia"][0], renders["piloto"][0]
    top = 38
    comparison = Image.new("RGB", (left.width + right.width + 24, max(left.height, right.height) + top), "#dddddd")
    comparison.paste(left, (0, top))
    comparison.paste(right, (left.width + 24, top))
    draw = ImageDraw.Draw(comparison)
    draw.text((14, 12), "Referencia oficial v5", fill="black")
    draw.text((left.width + 38, 12), "readyproof - datos ficticios [Ejemplo]", fill="black")
    comparison.save(args.salida / "comparacion_pagina_1.png")
    summary = {
        "paginas": counts,
        "logos_por_pagina": {key: [len(page.images) for page in reader.pages] for key, reader in readers.items()},
        "archivos": {key: str(path) for key, path in paths.items()},
        "validacion": "Ejecutar pytest -q: comparación de todas las páginas, encabezados y pies.",
    }
    (args.salida / "resultado.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
