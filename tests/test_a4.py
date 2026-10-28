"""Formato A4 de una página, filas intactas y firmas centradas en su tabla."""
from base64 import b64decode
from pathlib import Path
from openpyxl import load_workbook
from pypdf import PdfReader
from pypdf.generic import ContentStream
from app.planillas.generador import generar_saa1
from app.planillas.piloto import datos_ejemplo
from app.planillas.pdf import convertir_pdf
from scripts.prueba_operativa_final import firma_ficticia,verificar_pdf


def test_a4_unica_con_datos_firmas_y_casilleros(tmp_path):
    excel=generar_saa1(datos_ejemplo(),tmp_path/'SAA-1.xlsx')
    sheet=load_workbook(excel).active
    assert str(sheet.page_setup.paperSize)=='9' and sheet.page_setup.orientation=='landscape'
    assert sheet.page_setup.fitToWidth==sheet.page_setup.fitToHeight==1
    assert sheet.max_row==44 and sheet.max_column==25
    signatures={role:b64decode(firma_ficticia(offset).split(',')[1]) for role,offset in [('tecnico',0),('responsable',25)]}
    pdf=convertir_pdf(excel,tmp_path/'SAA-1_A4.pdf',firmas=signatures)
    checks=verificar_pdf(pdf.read_bytes());assert checks['paginas']==1
    reader=PdfReader(pdf);page=reader.pages[0];anchors={}
    def visitor(text,cm,tm,font,size):
        if text.strip() in ('CLIENTE:','TELÉFONO:'):
            anchors[text.strip()]=tm[4]*cm[0]+tm[5]*cm[2]+cm[4]
    text=page.extract_text(visitor_text=visitor)
    assert all(label in text for label in ('INSTALACIÓN','ABASTECIMIENTO DE AGUA','BOMBAS CONTRA INCENDIO','TOMA DE IMPULSIÓN PARA BOMBEROS','OBSERVACIONES:','SUPERVISOR DEL MANTENEDOR','RESPONSABLE DE LA INSTALACIÓN'))
    width=(anchors['TELÉFONO:']-anchors['CLIENTE:'])/(19/25);left=anchors['CLIENTE:']
    matrices={}
    def operand(op,args,cm,tm):
        if op==b'Do' and str(args[0]).startswith('/Firma_'):
            matrices[str(args[0])]=[float(value) for value in cm]
    page.extract_text(visitor_operand_before=operand)
    assert len(matrices)==2
    for role,start,span in [('tecnico',0,12/25),('responsable',12/25,13/25)]:
        a,b,c,d,x,y=matrices['/Firma_'+role]
        assert left+width*start<x<x+a<left+width*(start+span)+2
        assert abs(x+a/2-(left+width*(start+span/2)))<2
        assert 0<y<y+d<float(page.mediabox.height)
