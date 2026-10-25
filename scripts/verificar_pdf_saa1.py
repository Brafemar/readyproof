"""Cotejo visual local del piloto con el Excel oficial convertido a PDF."""
import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw
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
    args.salida.mkdir(parents=True, exist_ok=True)
    paths = {"referencia": args.referencia, "blanca": args.blanca, "piloto": args.piloto}
    readers = {key: PdfReader(path) for key, path in paths.items()}
    counts = {key: len(reader.pages) for key, reader in readers.items()}
    assert len(set(counts.values())) == 1, counts
    assert all(len(page.images) == 2 for reader in readers.values() for page in reader.pages)
    texts = {key: "\n".join(page.extract_text() for page in reader.pages) for key, reader in readers.items()}
    for key, text in texts.items():
        for label in ("SG-PEM-IFI-SAA-1", "T.C. 3 AÑOS", "SUPERVISOR DEL MANTENEDOR", "RESPONSABLE DE LA INSTALACIÓN", "OBSERVACIONES"):
            assert label in text, (key, label)
    assert "[Ejemplo]" in texts["piloto"]
    renders = {key: render(path) for key, path in paths.items()}
    equal = []
    for left, right in zip(renders["referencia"], renders["blanca"]):
        assert left.size == right.size
        equal.append(ImageChops.difference(left, right).getbbox() is None)
    assert all(equal), "El PDF sin carga difiere visualmente de la referencia v5."
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
    summary = {"paginas": counts, "blanca_identica_pixel_a_pixel": equal, "encabezados_y_pies_presentes": True, "logos_por_pagina": 2}
    (args.salida / "resultado.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
