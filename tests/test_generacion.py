from copy import copy
from pathlib import Path
from zipfile import ZipFile
import runpy
import subprocess

import pytest
import pypdfium2 as pdfium
from PIL import ImageChops
from pypdf import PdfReader
from openpyxl import load_workbook
from lxml import etree

from app.planillas.generador import generar_saa1
from app.planillas.definiciones.saa1 import HERRAMIENTAS, MODELO, definicion_saa1
from app.planillas.pdf import convertir_pdf

REFERENCE = Path(__file__).parent / "referencias" / "SAA-1_v5.xlsx"


def test_generacion_reproduce_referencia_v5(tmp_path):
    result = generar_saa1({}, tmp_path / "blanca.xlsx")
    expected, actual = load_workbook(REFERENCE).active, load_workbook(result).active
    assert actual.max_row == expected.max_row == 44
    assert actual.max_column == expected.max_column == 25
    merges = {str(cell_range) for cell_range in expected.merged_cells.ranges}
    assert {str(cell_range) for cell_range in actual.merged_cells.ranges} == (
        merges - {'M7:Q7', 'R7:S7'} | {'M7:P7', 'Q7:S7'}
    )
    assert str(actual.print_area) == str(expected.print_area)
    expected.page_setup.fitToHeight = 1
    from app.planillas.impresion import MARGEN
    expected.page_margins.left = expected.page_margins.right = expected.page_margins.bottom = MARGEN
    expected.page_margins.top = 35 / 25.4
    assert actual.page_setup == expected.page_setup
    assert actual.page_margins == expected.page_margins
    assert actual.print_options == expected.print_options
    for key, dimension in expected.column_dimensions.items():
        dimension.width = 8.7
        assert dict(actual.column_dimensions[key]) == dict(dimension)
    for key, dimension in expected.row_dimensions.items():
        if key not in (5, 6, 7):
            assert dict(actual.row_dimensions[key]) == dict(dimension)
    assert [actual.row_dimensions[key].height for key in (5, 6, 7)] == [22, 22, 22]
    for row in expected:
        for cell in row:
            other = actual[cell.coordinate]
            assert other.value == cell.value
            if cell.row == 7 and 13 <= cell.column <= 19:
                continue
            assert other.font.name == ('Archivo SemiBold' if cell.font.name == 'Arial' else 'Fira Sans')
            assert (other.font.sz, other.font.bold) == (cell.font.sz, cell.font.bold)
            assert other.fill.patternType == cell.fill.patternType
            for side in ('left', 'right', 'top', 'bottom'):
                assert getattr(other.border, side).style == getattr(cell.border, side).style
            assert copy(other.alignment) == copy(cell.alignment)
            assert other.number_format == cell.number_format
    with ZipFile(result) as archive, ZipFile(REFERENCE) as reference:
        for name in reference.namelist():
            if name.startswith(("xl/media/", "xl/drawings/")):
                assert archive.read(name) == reference.read(name)


def test_carga_conserva_logos_textos_y_opciones(tmp_path):
    from app.planillas.piloto import datos_ejemplo
    datos = datos_ejemplo()
    datos["cabecera"] = {"cliente": "[Ejemplo] Planta", "fecha": "25/10/2026",
                         "numero_mantenedor": "IFI-2024-10001"}
    datos["observaciones"] = [f"[Ejemplo] Observación {i}" for i in range(1, 5)]
    posiciones = {}
    bloque = None
    reference = load_workbook(REFERENCE).active
    for row in reference:
        etiqueta = row[0].value
        if etiqueta in datos["bloques"]:
            bloque = etiqueta
        elif bloque and isinstance(etiqueta, str) and etiqueta.endswith(":"):
            posiciones[(bloque, etiqueta[:-1])] = row[0].row
    esperado = {}
    contador = 1
    for titulo, campos in definicion_saa1()["bloques"]:
        for campo in campos:
            etiqueta, opciones = campo if isinstance(campo, tuple) else (campo, None)
            if isinstance(opciones, list):
                valor = opciones[contador % len(opciones)]
                texto = "      ".join(f"{op}  {'☑' if op == valor else '☐'}" for op in opciones)
            elif isinstance(opciones, str) and opciones:
                valor = contador
                texto = f"{valor}  {opciones}"
            else:
                valor = f"[Ejemplo] Dato único {contador}"
                texto = valor
            datos["bloques"][titulo][etiqueta] = valor
            esperado[(titulo, etiqueta)] = texto
            contador += 1
    result = generar_saa1(datos, tmp_path / "carga.xlsx")
    blank = generar_saa1({}, tmp_path / "blanca.xlsx")
    actual, expected = load_workbook(result).active, load_workbook(blank).active
    assert actual["C5"].value == "[Ejemplo] Planta"
    assert actual["V4"].value == "25/10/2026"
    assert actual["Q7"].value == "IFI-2024-10001"
    for campo, valor in esperado.items():
        cell = actual[f"J{posiciones[campo]}"]
        assert cell.value == valor, campo
        assert cell.font.bold and cell.alignment.horizontal == 'center'
    for fila, valor in enumerate(datos["observaciones"], 36):
        assert actual[f"A{fila}"].value == valor
    assert actual["T3"].value == "T.C. 3 AÑOS"
    for row in expected:
        for cell in row:
            if cell.column == 1 and cell.row not in range(36, 40):
                assert actual[cell.coordinate].value == cell.value
    with ZipFile(result) as filled, ZipFile(blank) as base:
        assert set(filled.namelist()) == set(base.namelist())
        for name in base.namelist():
            if name == "docProps/core.xml":
                left, right = etree.fromstring(filled.read(name)), etree.fromstring(base.read(name))
                for tree in (left, right):
                    for child in list(tree):
                        if etree.QName(child).localname in {"created", "modified"}:
                            tree.remove(child)
                assert etree.tostring(left) == etree.tostring(right)
            elif name not in ("xl/worksheets/sheet1.xml", "xl/styles.xml"):
                assert filled.read(name) == base.read(name)


@pytest.mark.parametrize("datos", [
    {"ajeno": "dato"}, {"cabecera": {"inventado": "x"}},
    {"bloques": {"OTRO BLOQUE": {}}},
    {"bloques": {"ABASTECIMIENTO DE AGUA": {"inventado": "x"}}},
    {"bloques": {"ABASTECIMIENTO DE AGUA": {"Ubicación": "Otra"}}},
    {"observaciones": ["x"] * 5}, {"observaciones": "texto"},
    {"cabecera": {"cliente": True}}, {"cabecera": {"cliente": float("nan")}},
    {"cabecera": {"cliente": "x\x01"}},
])
def test_carga_invalida_no_genera_archivo(tmp_path, datos):
    target = tmp_path / "invalida.xlsx"
    with pytest.raises(ValueError):
        generar_saa1(datos, target)
    assert not target.exists()


def test_texto_no_se_convierte_en_formula(tmp_path):
    target = generar_saa1({"cabecera": {"cliente": "=1+1"}}, tmp_path / "texto.xlsx")
    cell = load_workbook(target).active["C5"]
    assert cell.data_type == "s" and cell.value == "=1+1"


def test_no_sobrescribe_excel(tmp_path):
    target = tmp_path / "existente.xlsx"
    target.write_bytes(b"original")
    with pytest.raises(FileExistsError):
        generar_saa1({}, target)
    assert target.read_bytes() == b"original"


def test_pdf_invoca_calc_con_perfil_aislado(tmp_path, monkeypatch):
    import app.planillas.pdf as module
    source = tmp_path / "entrada.xlsx"
    generar_saa1({}, source)
    monkeypatch.setattr(module, "localizar_libreoffice", lambda: Path("soffice"))
    def run(command, **kwargs):
        assert "--headless" in command
        assert "pdf:calc_pdf_Export" in command
        assert any(arg.startswith("-env:UserInstallation=file:") for arg in command)
        assert kwargs["timeout"] == 120
        output_dir = Path(command[command.index("--outdir") + 1])
        from pypdf import PdfWriter
        writer = PdfWriter()
        writer.add_blank_page(width=841.89, height=595.28)
        with (output_dir / 'entrada.pdf').open('wb') as stream:
            writer.write(stream)
        return subprocess.CompletedProcess(command, 0, "", "")
    monkeypatch.setattr(module.subprocess, "run", run)
    assert convertir_pdf(source, tmp_path / "salida.pdf").read_bytes().startswith(b"%PDF-")


def test_pdf_no_publica_conversion_fallida(tmp_path, monkeypatch):
    import app.planillas.pdf as module
    source = tmp_path / "entrada.xlsx"
    generar_saa1({}, source)
    monkeypatch.setattr(module, "localizar_libreoffice", lambda: Path("soffice"))
    monkeypatch.setattr(module.subprocess, "run", lambda *a, **kw: subprocess.CompletedProcess(a, 1, "", "fallo"))
    target = tmp_path / "salida.pdf"
    with pytest.raises(RuntimeError, match="código 1"):
        convertir_pdf(source, target)
    assert not target.exists()


@pytest.fixture(scope="module")
def pdfs_saa1(tmp_path_factory):
    from app.planillas.piloto import datos_ejemplo
    directory = tmp_path_factory.mktemp("pdfs_saa1")
    # La referencia v5 se conserva; solo se adapta su ajuste de impresión autorizado.
    reference_a4 = directory / "referencia_A4.xlsx"
    with ZipFile(REFERENCE) as source, ZipFile(reference_a4, "w") as output:
        tree = etree.fromstring(source.read('xl/worksheets/sheet1.xml'))
        workbook = etree.fromstring(source.read('xl/workbook.xml'))
        tree.find('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}pageSetup').set('fitToHeight', '1')
        from app.planillas.impresion import ajustar_tabla, aplicar_identidad, preparar_impresion
        ajustar_tabla(tree)
        styles = etree.fromstring(source.read('xl/styles.xml'))
        aplicar_identidad(styles)
        preparar_impresion(tree, workbook)
        for item in source.infolist():
            payload = source.read(item.filename)
            if item.filename == "xl/worksheets/sheet1.xml":
                payload = etree.tostring(tree)
            elif item.filename == 'xl/workbook.xml':
                payload = etree.tostring(workbook)
            elif item.filename == 'xl/styles.xml':
                payload = etree.tostring(styles)
            output.writestr(item, payload)
    paths = {"referencia": convertir_pdf(reference_a4, directory / "referencia.pdf")}
    for name, datos in (("blanca", {}), ("piloto", datos_ejemplo())):
        source = generar_saa1(datos, directory / f"{name}.xlsx")
        paths[name] = convertir_pdf(source, directory / f"{name}.pdf")
    return paths


def _textos_fijos_encabezado_y_pie(reader):
    """Regiones por anclas del contenido, sin coordenadas fijas de SAA-1."""
    from app.planillas.leyenda_iram import TEXTO
    encabezados,pies=[],[]
    for index,page in enumerate(reader.pages):
        spans=[]
        def visitor(text,cm,tm,font,size):
            if text.strip():spans.append((" ".join(text.split()),tm[4]*cm[0]+tm[5]*cm[2]+cm[4],tm[4]*cm[1]+tm[5]*cm[3]+cm[5],size))
        page.extract_text(visitor_text=visitor)
        dates=[span for span in spans if span[0]=="FECHA:"]
        if dates:
            date=max(dates,key=lambda span:span[2])
            header=[text for text,x,y,size in spans if y>=date[2]-date[3]*.25 and not (x>date[1] and abs(y-date[2])<date[3]*.6)]
        else:
            top=max(spans,key=lambda span:span[2])
            header=[text for text,x,y,size in spans if y>=top[2]-top[3]*.25]
        footer=[text for text,x,y,size in spans if text==TEXTO]
        if index==len(reader.pages)-1:
            legends=[span for span in spans if "CUMPLE:" in span[0]]
            assert legends,"No se encontró el ancla del pie."
            legend=max(legends,key=lambda span:span[2])
            footer=[text for text,x,y,size in spans if y<=legend[2]+legend[3]*.25]
        encabezados.append(tuple(header));pies.append(tuple(footer))
    return encabezados,pies


def test_conversion_real_con_libreoffice(pdfs_saa1):
    actual, reference = PdfReader(pdfs_saa1["piloto"]), PdfReader(pdfs_saa1["referencia"])
    assert len(actual.pages) == len(reference.pages) == 1
    assert abs(float(actual.pages[0].mediabox.width)-841.89)<.5
    assert abs(float(actual.pages[0].mediabox.height)-595.28)<.5
    assert all(len(page.images) == 2 for page in actual.pages)
    actual_text = _textos_fijos_encabezado_y_pie(actual)
    reference_text = _textos_fijos_encabezado_y_pie(reference)
    assert all(reference_text[0]) and any(reference_text[1])
    assert actual_text == reference_text


def test_blanca_identica_pixel_a_pixel_en_todas_las_paginas(pdfs_saa1):
    # La importación obligatoria de pypdfium2 hace fallar la colección si falta.
    with pdfium.PdfDocument(pdfs_saa1["referencia"]) as reference, pdfium.PdfDocument(pdfs_saa1["blanca"]) as actual:
        assert len(reference) == len(actual)
        for index in range(len(reference)):
            left_page, right_page = reference[index], actual[index]
            left_bitmap, right_bitmap = left_page.render(scale=1.8), right_page.render(scale=1.8)
            left, right = left_bitmap.to_pil().convert("RGB"), right_bitmap.to_pil().convert("RGB")
            assert left.size == right.size, f"Página {index + 1}: tamaño distinto"
            assert ImageChops.difference(left, right).getbbox() is None, f"Página {index + 1}: diferencias de píxeles"
            left.close()
            right.close()
            left_bitmap.close()
            right_bitmap.close()
            left_page.close()
            right_page.close()


def test_pdf_contiene_leyenda_iram_confirmada(pdfs_saa1):
    from app.planillas.leyenda_iram import TEXTO
    for page in PdfReader(pdfs_saa1["piloto"]).pages:
        assert page.extract_text().count(TEXTO)==1


def test_pdf_no_sobrescribe_destino(tmp_path):
    source = tmp_path / "entrada.xlsx"
    source.write_bytes(b"ejemplo")
    target = tmp_path / "salida.pdf"
    target.write_bytes(b"original")
    with pytest.raises(FileExistsError):
        convertir_pdf(source, target)
    assert target.read_bytes() == b"original"


def test_pdf_timeout_no_publica_archivo(tmp_path, monkeypatch):
    import app.planillas.pdf as module
    source = tmp_path / "entrada.xlsx"
    source.write_bytes(b"ejemplo")
    monkeypatch.setattr(module, "localizar_libreoffice", lambda: Path("soffice"))
    def run(*args, **kwargs):
        raise subprocess.TimeoutExpired("soffice", kwargs["timeout"])
    monkeypatch.setattr(module.subprocess, "run", run)
    target = tmp_path / "salida.pdf"
    with pytest.raises(subprocess.TimeoutExpired):
        convertir_pdf(source, target, timeout=1)
    assert not target.exists()



def test_titulo_pdf_toma_codigo_del_excel(tmp_path):
    from app.planillas.encabezado_pdf import reponer_logos
    from pypdf import PdfWriter
    source = generar_saa1({}, tmp_path / "codigo_original.xlsx")
    modified = tmp_path / "otro_codigo.xlsx"
    code = "SG-PEM-IFI-SAA-99"
    with ZipFile(source) as archive, ZipFile(modified, "w") as output:
        for entry in archive.infolist():
            payload = archive.read(entry.filename)
            if entry.filename == "xl/worksheets/sheet1.xml":
                payload = payload.replace(b"SG-PEM-IFI-SAA-1", code.encode("ascii"))
            output.writestr(entry, payload)
    original_pdf = tmp_path / "original.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=841.89, height=595.28)
    writer.write(original_pdf)
    result = tmp_path / "metadatos.pdf"
    reponer_logos(modified, original_pdf, result)
    metadata = PdfReader(result).metadata
    assert metadata.title == code
    assert metadata.creator == "readyproof"
    assert metadata.producer == "readyproof"
    assert metadata.author == "readyproof"



def test_regiones_independientes_de_escala_y_posicion(pdfs_saa1,tmp_path):
    from pypdf import PdfWriter,Transformation
    original=PdfReader(pdfs_saa1["piloto"])
    writer=PdfWriter();writer.clone_document_from_reader(original)
    for page in writer.pages:page.add_transformation(Transformation().scale(.9).translate(10,20))
    target=tmp_path/"desplazada.pdf"
    with target.open("wb") as output:writer.write(output)
    assert _textos_fijos_encabezado_y_pie(PdfReader(target))==_textos_fijos_encabezado_y_pie(original)
