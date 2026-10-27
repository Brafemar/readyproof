"""Marca de agua automática sin duplicar imágenes ni alterar texto o firmas."""
from pathlib import Path
import shutil

import pytest
from pypdf import PdfReader
from pypdf.generic import ContentStream
import pypdfium2 as pdfium

from app.planillas.generador import generar_saa1
from app.planillas.pdf import convertir_pdf
from app.planillas.marca_agua import incorporar_marca_agua,OPACIDAD,ESTADO


def verificar_marca_agua(reader):
    assert reader.metadata["/ReadyproofMarcaAgua"]=="readyproof + ISO; opacidad 0.055"
    for page in reader.pages:
        state=page["/Resources"]["/ExtGState"][ESTADO].get_object()
        assert abs(float(state["/ca"])-OPACIDAD)<1e-6
        assert state["/BM"]=="/Multiply"
        operations=ContentStream(page.get_contents(),reader).operations
        names=[str(args[0]) for args,op in operations if op==b"Do"]
        assert names.count("/RPLogo0")==2 and names.count("/RPLogo1")==2


def test_marca_agua_automatica_y_sin_doble_aplicacion(tmp_path):
    source=generar_saa1({},tmp_path/"blanca.xlsx")
    result=convertir_pdf(source,tmp_path/"SAA-1.pdf")
    reader=PdfReader(result);verificar_marca_agua(reader)
    assert len(reader.pages)==2 and all(len(page.images)==2 for page in reader.pages)
    with pytest.raises(RuntimeError,match="ya tiene"):
        incorporar_marca_agua(source,result,tmp_path/"duplicada.pdf")
    assert not (tmp_path/"duplicada.pdf").exists()
    out=Path("out/etapa6/marca_agua_automatica");out.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(result,out/"SAA-1.pdf")
    with pdfium.PdfDocument(str(result)) as document:
        for i in range(len(document)):
            page=document[i];bitmap=page.render(scale=1.8);bitmap.to_pil().save(out/f"pagina_{i+1}.png");bitmap.close();page.close()
