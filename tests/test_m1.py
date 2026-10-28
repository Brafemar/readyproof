"""Texto, fuente, posición y espacio del pie confirmados para M1."""
from pathlib import Path
import shutil

import pytest
from pypdf import PdfReader
from pypdf.generic import ContentStream
import pypdfium2 as pdfium

from app.planillas.generador import generar_saa1
from app.planillas.pdf import convertir_pdf
from app.planillas.piloto import datos_ejemplo
from app.planillas.leyenda_iram import TEXTO,TAMANIO,PIE_PT,ancho_leyenda,incorporar_leyenda_iram


def test_m1_parametros_y_espacio_confirmados(tmp_path):
    source=generar_saa1(datos_ejemplo(),tmp_path/"SAA-1.xlsx")
    result=convertir_pdf(source,tmp_path/"SAA-1_con_leyenda.pdf")
    reader=PdfReader(result);assert len(reader.pages)==1
    text=[]
    for index,page in enumerate(reader.pages):
        assert 841<float(page.mediabox.width)<843 and 595<float(page.mediabox.height)<596
        matches=[];observations=[]
        def visitor(value,cm,tm,font,size):
            x=tm[4]*cm[0]+tm[5]*cm[2]+cm[4];y=tm[4]*cm[1]+tm[5]*cm[3]+cm[5]
            if value.strip()==TEXTO:matches.append((x,y,size,font["/BaseFont"]))
            if value.strip()=="OBSERVACIONES:":observations.append(y)
        extracted=page.extract_text(visitor_text=visitor);text.append(extracted)
        assert extracted.count(TEXTO)==1 and len(matches)==1
        x,y,size,font=matches[0]
        assert font=="/Helvetica" and size==TAMANIO==8
        assert abs(y-PIE_PT)<.001
        assert abs(x+ancho_leyenda()/2-float(page.mediabox.width)/2)<.001
        assert all(top>PIE_PT+TAMANIO+4 for top in observations)
        operations=ContentStream(page.get_contents(),reader).operations
        assert any(op==b"g" and abs(float(args[0])-.5)<1e-6 for args,op in operations)
    assert reader.metadata["/ReadyproofIRAM"]==TEXTO
    with pytest.raises(RuntimeError,match="ya contiene"):
        incorporar_leyenda_iram(result,tmp_path/"duplicada.pdf")
    assert not (tmp_path/"duplicada.pdf").exists()
    out=Path("out/etapa_m1");out.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(result,out/"SAA-1_con_leyenda.pdf")
    (out/"texto_extraido.txt").write_text("\n\n".join(text),encoding="utf-8")
    with pdfium.PdfDocument(str(result)) as document:
        for index in range(len(document)):
            page=document[index];bitmap=page.render(scale=1.8);bitmap.to_pil().save(out/f"pagina_{index+1}.png");bitmap.close();page.close()



def test_frase_en_observaciones_no_se_confunde_con_leyenda(tmp_path):
    source=generar_saa1({"observaciones":["[Ejemplo] "+TEXTO]},tmp_path/"observacion.xlsx")
    result=convertir_pdf(source,tmp_path/"observacion.pdf")
    reader=PdfReader(result)
    assert reader.metadata["/ReadyproofIRAM"]==TEXTO
    assert sum(page.extract_text().count(TEXTO) for page in reader.pages)==len(reader.pages)+1
