"""Anexos rasterizados con Pillow: formato, referencias y unión en memoria."""
from hashlib import sha256
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
import pytest

from app.fotos import anexo_pdf as anexo


def jpeg(size=(1600, 1200)):
    image = Image.new("RGB", size, "#e4eced")
    draw = ImageDraw.Draw(image)
    draw.rectangle((int(size[0]*.12), int(size[1]*.22), int(size[0]*.45), int(size[1]*.8)), fill="#d41120")
    if size[0] >= 1000:
        font = ImageFont.truetype(str(anexo.ruta_fuente()), 42)
        draw.text((70, 60), "[Ejemplo] Imagen ficticia de prueba", font=font, fill="#1d1d1b")
    output = BytesIO()
    image.save(output, format="JPEG", quality=80)
    return output.getvalue()


def listas(cantidad=1):
    puntos = [dict(numero=i, x=.15+i*.1, y=.3+i*.08) for i in range(1, cantidad+1)]
    refs = [dict(numero=i, codigo="O", texto=f"[Ejemplo] Revisar componente {i}.") for i in range(1, cantidad+1)]
    return puntos, refs


def abrir(pdf, paginas):
    result = PdfReader(BytesIO(pdf))
    assert len(result.pages) == paginas
    for page in result.pages:
        assert float(page.mediabox.width) == pytest.approx(anexo.A4_PT[0], abs=.001)
        assert float(page.mediabox.height) == pytest.approx(anexo.A4_PT[1], abs=.001)
    return result


def test_una_marca_pdf_a4_y_posicion():
    points, refs = listas()
    result = abrir(anexo.generar_anexo(jpeg(), points, refs), 1)
    rendered = result.pages[0].images[0].image.convert("RGB")
    width = anexo.PAGINA_PX[0] - 2 * anexo.MARGEN
    height = round(1200 * width / 1600)
    left = (anexo.PAGINA_PX[0] - width) // 2
    cx = left + round(points[0]["x"] * width)
    cy = anexo.FOTO_Y + round(points[0]["y"] * height)
    assert max(rendered.getpixel((cx-15, cy))) < 90
    assert max(rendered.getpixel((cx+60, cy))) > 150



def test_cinco_marcas_en_una_hoja():
    points, refs = listas(5)
    abrir(anexo.generar_anexo(jpeg(), points, refs), 1)


def test_texto_largo_entero_pasa_a_segunda_hoja(tmp_path):
    points = [dict(numero=1, x=.5, y=.5)]
    refs = [dict(numero=1, codigo="O", texto="[Ejemplo] " + "W" * 130)]
    pdf = abrir(anexo.generar_anexo(jpeg((600,1600)), points, refs), 2)
    assert len(pdf.pages[0].images) == len(pdf.pages[1].images) == 1
    # Conservar todas las letras al envolver, sin elipsis ni truncamiento.
    font = ImageFont.truetype(str(anexo.ruta_fuente()), 24)
    lines = anexo._lineas(refs[0]["texto"], font, anexo.ANCHO_TEXTO)
    assert "".join(lines) == refs[0]["texto"]
    assert all(font.getlength(line) <= anexo.ANCHO_TEXTO for line in lines)
    for i, page in enumerate(pdf.pages, 1):
        page.images[0].image.save(tmp_path / f"continuacion_{i}.png")


@pytest.mark.parametrize("codigo", ["✓", "NA"])
def test_codigo_sin_texto_permitido(codigo):
    points, refs = listas()
    refs[0].update(codigo=codigo, texto="")
    abrir(anexo.generar_anexo(jpeg(), points, refs), 1)


@pytest.mark.parametrize("codigo", ["O", "X"])
def test_codigo_sin_texto_rechazado(codigo):
    points, refs = listas()
    refs[0].update(codigo=codigo, texto="")
    with pytest.raises(ValueError, match="requiere texto"):
        anexo.generar_anexo(jpeg(), points, refs)


def test_union_planilla_primero_y_anexo_despues():
    original = PdfWriter()
    original.add_blank_page(width=anexo.A4_PT[0], height=anexo.A4_PT[1])
    output = BytesIO()
    original.write(output)
    planilla = output.getvalue()
    digest = sha256(planilla).hexdigest()
    points, refs = listas()
    result = abrir(anexo.unir_pdf(planilla, anexo.generar_anexo(jpeg(), points, refs)), 2)
    assert len(result.pages[0].images) == 0
    assert len(result.pages[1].images) == 1
    assert sha256(planilla).hexdigest() == digest


def test_calculo_altura_crece_y_respeta_ancho():
    _, one = listas()
    _, five = listas(5)
    assert anexo.calcular_altura_lista(five) > anexo.calcular_altura_lista(one)
    long = [dict(numero=1, codigo="O", texto="[Ejemplo] " + "W" * 130)]
    assert anexo.calcular_altura_lista(long, ancho=250) > anexo.calcular_altura_lista(long)


@pytest.mark.parametrize("foto", [None, b"[Ejemplo] No es una foto"])
def test_foto_inexistente_o_invalida(foto):
    points, refs = listas()
    with pytest.raises(ValueError, match="foto"):
        anexo.generar_anexo(foto, points, refs)


@pytest.mark.parametrize("marcas_vacias", [True, False])
def test_listas_vacias_rechazadas(marcas_vacias):
    points, refs = listas()
    with pytest.raises(ValueError, match="vacía"):
        anexo.generar_anexo(jpeg(), [] if marcas_vacias else points, refs if marcas_vacias else [])


def test_marcas_y_referencias_deben_coincidir():
    points, refs = listas()
    refs[0]["numero"] = 2
    with pytest.raises(ValueError, match="mismos números"):
        anexo.generar_anexo(jpeg(), points, refs)


def test_fuente_contiene_codigo_check():
    font = ImageFont.truetype(str(anexo.ruta_fuente()), 24)
    assert bytes(font.getmask("✓")) != bytes(font.getmask("\u0378"))


def test_generar_ejemplo_para_revision(tmp_path_factory):
    points, refs = listas(5)
    refs[0].update(codigo="✓", texto="")
    refs[1].update(codigo="O", texto="[Ejemplo] Revisar la unión señalada en la imagen.")
    refs[2].update(codigo="X", texto="[Ejemplo] No se pudo acceder al componente.")
    refs[3].update(codigo="NA", texto="")
    refs[4].update(codigo="✓", texto="[Ejemplo] Identificación visible.")
    pdf = anexo.generar_anexo(jpeg(), points, refs)
    abrir(pdf, 1)
    path = tmp_path_factory.getbasetemp() / "ejemplo_anexo.pdf"
    assert not path.exists()
    path.write_bytes(pdf)
