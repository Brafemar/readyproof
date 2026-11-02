"""Numeración global sin restos de numeración local ni recodificación JPEG."""
from io import BytesIO
from pypdf import PdfReader, PdfWriter
import pytest
from app.fotos.anexo_pdf import generar_anexo, unir_pdf
from tests.test_fotos_emision import jpeg_prueba

@pytest.mark.parametrize('cantidad', [1, 2])
def test_paginas_numeradas_sobre_documento_completo(cantidad):
    out = BytesIO()
    writer = PdfWriter()
    writer.add_blank_page(width=595.2756, height=841.8898)
    writer.add_metadata({'/ReadyproofIRAM': 'Planilla conforme a IRAM 3546:2011'})
    writer.write(out)
    result = out.getvalue()
    jpeg = jpeg_prueba()
    refs = [dict(numero=1, x=.5, y=.45, codigo='O', texto='[Ejemplo] Se observa grasa.')]
    annex = generar_anexo(jpeg, refs, refs)
    assert 'Pág. 1 de 1' in PdfReader(BytesIO(annex)).pages[0].extract_text()
    for _ in range(cantidad):
        result = unir_pdf(result, annex)
    reader = PdfReader(BytesIO(result))
    for index, page in enumerate(reader.pages, 1):
        text = page.extract_text()
        assert text.count('Pág.') == 1
        assert f'Pág. {index} de {cantidad+1}' in text
        assert 'Pág. 1 de 1' not in text
    for page in reader.pages[1:]:
        assert page['/Resources']['/XObject']['/RPFOTO'].get_object()._data == jpeg
    assert reader.metadata['/ReadyproofIRAM'] == 'Planilla conforme a IRAM 3546:2011'
