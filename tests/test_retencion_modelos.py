"""El comprobador acepta solo el cambio de retención autorizado."""
from io import BytesIO
import pytest
from PIL import Image
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from scripts.verificar_retencion_pdf import comparar_retencion_pdf


def pdf(retencion, *, extra='[Ejemplo] Modelo', paginas=1, color=None):
    out=BytesIO();canvas=Canvas(out,pagesize=(595,842),invariant=1)
    for _ in range(paginas):
        canvas.drawString(40,800,extra);canvas.drawString(400,780,retencion)
        if color:canvas.drawImage(ImageReader(Image.new('RGB',(20,20),color)),40,700,20,20)
        canvas.showPage()
    canvas.save();return out.getvalue()


@pytest.mark.parametrize('viejo',['T.C. 2 años','T.C. 2 AÑOS'])
def test_acepta_solo_retencion(viejo):
    result=comparar_retencion_pdf(pdf(viejo),pdf('T.C. 3 AÑOS'))
    assert result['reemplazos_totales']==1 and result['solo_cambio_texto_retencion']


def test_rechaza_otro_texto():
    with pytest.raises(ValueError,match='texto ajenas'):
        comparar_retencion_pdf(pdf('T.C. 2 años'),pdf('T.C. 3 AÑOS',extra='[Ejemplo] Otro contenido'))


def test_rechaza_cambio_de_paginas():
    with pytest.raises(ValueError,match='cantidad de páginas'):
        comparar_retencion_pdf(pdf('T.C. 2 años'),pdf('T.C. 3 AÑOS',paginas=2))


def test_rechaza_imagen_distinta():
    with pytest.raises(ValueError,match='imágenes'):
        comparar_retencion_pdf(pdf('T.C. 2 años',color='red'),pdf('T.C. 3 AÑOS',color='blue'))


def test_rechaza_ausencia_del_cambio():
    with pytest.raises(ValueError,match='No se encontró'):
        comparar_retencion_pdf(pdf('T.C. 3 AÑOS'),pdf('T.C. 3 AÑOS'))
