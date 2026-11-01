"""C4b: texto extraíble, fuente embebida, JPEG idéntico y vectores de marcado."""
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import os
import shutil
import subprocess

from PIL import Image, ImageDraw
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream
import pytest

from app.fotos import anexo_pdf as anexo


@pytest.fixture(scope="module")
def muestra():
    image = Image.new("RGB", (1600,1200), "#e4eced")
    ImageDraw.Draw(image).rectangle((200,250,700,950), fill="#d41120")
    stream = BytesIO()
    image.save(stream, format="JPEG", quality=80)
    jpeg = stream.getvalue()
    points = [dict(numero=i,x=.15+i*.1,y=.3+i*.08) for i in range(1,6)]
    rows = [dict(numero=1,codigo="✓",texto=""),dict(numero=2,codigo="O",texto="[Ejemplo] Revisar unión y válvula."),dict(numero=3,codigo="X",texto="[Ejemplo] Acceso no disponible."),dict(numero=4,codigo="NA",texto=""),dict(numero=5,codigo="✓",texto="[Ejemplo] Identificación legible.")]
    carga = {"datos":{"cabecera":{"cliente":"[Ejemplo] Planta C4b","sistema_designacion":"[Ejemplo] Equipo C4b","inspector":"[Ejemplo] Técnico C4b","fecha":"2026-11-01"}}}
    pdf = anexo.generar_anexo(jpeg,points,rows,carga=carga)
    return jpeg,points,rows,carga,pdf


def lector(pdf):
    return PdfReader(BytesIO(pdf))


def jpeg_pdf(pdf):
    image = lector(pdf).pages[0]["/Resources"]["/XObject"]["/RPFOTO"].get_object()
    assert image["/Filter"] == "/DCTDecode"
    return image._data


def pdftotext(pdf, path):
    path.write_bytes(pdf)
    candidates = [os.environ.get("READYPROOF_PDFTOTEXT"), shutil.which("pdftotext"),
                  Path.home()/".cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/Library/bin/pdftotext.exe",
                  Path(os.environ.get("ProgramFiles", "C:/Program Files"))/"Git/ucrt64/bin/pdftotext.exe"]
    exe = next((str(path) for path in candidates if path and Path(path).is_file()), None)
    assert exe, "Se requiere pdftotext disponible para verificar el texto del anexo."
    result = subprocess.run([exe,"-enc","UTF-8",str(path),"-"],capture_output=True,timeout=30)
    assert result.returncode == 0, result.stderr.decode("utf-8",errors="replace")
    return result.stdout.decode("utf-8")


def test_texto_extraible_con_pdftotext(muestra,tmp_path):
    text = pdftotext(muestra[4],tmp_path/"texto.pdf")
    for value in ["ANEXO FOTOGRÁFICO","[Ejemplo] Revisar unión y válvula.","[Ejemplo] Identificación legible.","[Ejemplo] Planta C4b","[Ejemplo] Equipo C4b","[Ejemplo] Técnico C4b","01/11/2026"]:
        assert value in text


def test_sha256_jpeg_igual(muestra):
    assert sha256(muestra[0]).hexdigest() == sha256(jpeg_pdf(muestra[4])).hexdigest()
    assert jpeg_pdf(muestra[4]) == muestra[0]


def test_fuente_incrustada_con_to_unicode(muestra):
    page = lector(muestra[4]).pages[0]
    fonts = list(page["/Resources"]["/Font"].get_object().values())
    assert fonts
    for reference in fonts:
        font = reference.get_object()
        assert font["/Subtype"] == "/TrueType"
        descriptor = font["/FontDescriptor"].get_object()
        assert len(descriptor["/FontFile2"].get_object().get_data()) > 1000
        assert "IBMPlexSans" in str(font["/BaseFont"])
        assert font["/ToUnicode"].get_object().get_data()


def test_cinco_marcas_una_hoja_a4(muestra):
    pdf = lector(muestra[4])
    assert len(pdf.pages)==1 and len(pdf.pages[0].images)==1
    assert float(pdf.pages[0].mediabox.width)==pytest.approx(anexo.A4_PT[0],abs=.001)
    assert float(pdf.pages[0].mediabox.height)==pytest.approx(anexo.A4_PT[1],abs=.001)
    assert pdf.pages[0]["/Resources"]["/XObject"]["/RPFOTO"]["/Width"]==1600


def test_check_trazo_vectorial_y_u2713(muestra,tmp_path):
    text = pdftotext(muestra[4],tmp_path/"check.pdf")
    assert text.count("✓")==2 and "√" not in text
    commands = lector(muestra[4]).pages[0].get_contents().get_data()
    assert b"3 Tr" in commands
    # El carácter de la serie es U+2713; la forma visible no depende de su glifo fino.
    from app.planillas.multisistema import RESULTADOS
    assert RESULTADOS[0] == "✓" and ord(RESULTADOS[0]) == 0x2713


def test_color_y_centros_vectoriales(muestra):
    pdf=lector(muestra[4]);ops=ContentStream(pdf.pages[0].get_contents(),pdf).operations
    matrix=next(values for values,op in ops if op==b"cm")
    width,_,_,height,left,bottom=map(float,matrix)
    rgb=tuple(int(anexo.COLOR_MARCAS[i:i+2],16)/255 for i in (1,3,5))
    assert any(op==b"rg" and tuple(map(float,values))==pytest.approx(rgb,abs=.00001) for values,op in ops)
    for mark in muestra[1]:
        x=left+mark["x"]*width;y=bottom+(1-mark["y"])*height
        assert any(op==b"m" and abs(float(values[0])-x-9)<.01 and abs(float(values[1])-y)<.01 for values,op in ops)


def test_datos_ausentes_son_raya(muestra):
    pdf=anexo.generar_anexo(*muestra[:3])
    assert lector(pdf).pages[0].extract_text().count("—")>=4
    assert anexo.datos_cabecera({"datos":{"cabecera":None}})==dict.fromkeys(["Cliente","Equipo","Técnico","Fecha"],"—")


def test_cabecera_desde_objeto_carga(muestra):
    from app.models import Carga
    carga=Carga(datos=muestra[3]["datos"])
    text=lector(anexo.generar_anexo(*muestra[:3],carga=carga)).pages[0].extract_text()
    assert "[Ejemplo] Técnico C4b" in text and "01/11/2026" in text


def test_pie_desde_fuentes_existentes(muestra):
    from app.planillas.leyenda_iram import TEXTO
    pie,origen=anexo.origen_pie()
    assert TEXTO in pie and origen["retencion"]!="no encontrado"
    assert "build_planilla.py" in origen["retencion"]
    assert pie in lector(muestra[4]).pages[0].extract_text()


def test_pie_no_encontrado_no_inventa(muestra,tmp_path,monkeypatch):
    from app.planillas import leyenda_iram
    monkeypatch.setattr(leyenda_iram,"TEXTO","")
    pie,origen=anexo.origen_pie(archivo_kit=tmp_path/"kit_no_disponible.py")
    assert pie=="" and origen=={"leyenda":"no encontrado","retencion":"no encontrado"}
    monkeypatch.setattr(anexo,"origen_pie",lambda config=None:(pie,origen))
    text=lector(anexo.generar_anexo(*muestra[:3])).pages[0].extract_text()
    assert "IRAM" not in text and "AÑOS" not in text


def test_pie_configurado_prevalece(muestra):
    config={"leyenda_iram":"[Ejemplo] Pie configurado","retencion":""}
    text=lector(anexo.generar_anexo(*muestra[:3],configuracion_planilla=config)).pages[0].extract_text()
    assert "[Ejemplo] Pie configurado" in text and "IRAM" not in text


def test_texto_largo_no_se_corta_y_hojas_a4(muestra,tmp_path):
    image=Image.new("RGB",(600,1600),"white");stream=BytesIO();image.save(stream,format="JPEG")
    rows=[dict(numero=1,codigo="O",texto="[Ejemplo] "+"W"*130)]
    data=anexo.generar_anexo(stream.getvalue(),[dict(numero=1,x=.5,y=.5)],rows)
    pdf=lector(data)
    assert len(pdf.pages)==2 and len(pdf.pages[1].images)==0
    assert sum(page.extract_text().count("W") for page in pdf.pages)==130
    assert pdftotext(data,tmp_path/"continuacion.pdf").count("W")==130
    assert all(float(page.mediabox.height)==pytest.approx(anexo.A4_PT[1],abs=.001) for page in pdf.pages)


@pytest.mark.parametrize("codigo",["O","X"])
def test_texto_obligatorio(muestra,codigo):
    with pytest.raises(ValueError,match="requiere texto"):
        anexo.generar_anexo(muestra[0],[dict(numero=1,x=.5,y=.5)],[dict(numero=1,codigo=codigo,texto="")])


@pytest.mark.parametrize("jpeg",[None,b"[Ejemplo] No es JPEG"])
def test_foto_invalida(muestra,jpeg):
    with pytest.raises(ValueError,match="foto"):
        anexo.generar_anexo(jpeg,*muestra[1:3])


@pytest.mark.parametrize("marcas",[True,False])
def test_lista_vacia(muestra,marcas):
    with pytest.raises(ValueError,match="vacía"):
        anexo.generar_anexo(muestra[0],[] if marcas else muestra[1],muestra[2] if marcas else [])


def test_union_conserva_orden_y_jpeg(muestra):
    writer=PdfWriter();writer.add_blank_page(*anexo.A4_PT);buf=BytesIO();writer.write(buf)
    result=lector(anexo.unir_pdf(buf.getvalue(),muestra[4]))
    assert len(result.pages)==2 and len(result.pages[0].images)==0
    assert "ANEXO FOTOGRÁFICO" in result.pages[1].extract_text()
    image=result.pages[1]["/Resources"]["/XObject"]["/RPFOTO"].get_object()
    assert sha256(image._data).hexdigest()==sha256(muestra[0]).hexdigest()


def test_ejemplo_v2_para_revision(muestra,tmp_path_factory):
    base=tmp_path_factory.getbasetemp()
    (base/"foto_estandarizada.jpg").write_bytes(muestra[0])
    path=base/"ejemplo_anexo_v2.pdf"
    assert not path.exists();path.write_bytes(muestra[4])
    texto=pdftotext(muestra[4],base/"verificacion_texto.pdf")
    (base/"pdftotext.txt").write_text(texto,encoding="utf-8")
    assert "[Ejemplo] Revisar unión y válvula." in texto

