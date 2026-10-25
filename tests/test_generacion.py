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
    assert str(actual.merged_cells) == str(expected.merged_cells)
    assert str(actual.print_area) == str(expected.print_area)
    assert actual.page_setup == expected.page_setup
    assert actual.page_margins == expected.page_margins
    assert actual.print_options == expected.print_options
    for key, dimension in expected.column_dimensions.items():
        assert dict(actual.column_dimensions[key]) == dict(dimension)
    for key, dimension in expected.row_dimensions.items():
        assert dict(actual.row_dimensions[key]) == dict(dimension)
    for row in expected:
        for cell in row:
            other = actual[cell.coordinate]
            assert other.value == cell.value
            assert copy(other.font) == copy(cell.font)
            assert copy(other.fill) == copy(cell.fill)
            assert copy(other.border) == copy(cell.border)
            assert copy(other.alignment) == copy(cell.alignment)
            assert other.number_format == cell.number_format
    with ZipFile(result) as archive, ZipFile(REFERENCE) as reference:
        for name in reference.namelist():
            if name.startswith(("xl/media/", "xl/drawings/")):
                assert archive.read(name) == reference.read(name)


def test_carga_conserva_logos_textos_y_opciones(tmp_path):
    from app.planillas.piloto import datos_ejemplo
    datos = datos_ejemplo()
    datos["cabecera"] = {"cliente": "[Ejemplo] Planta", "fecha": "25/10/2026"}
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
    for campo, valor in esperado.items():
        assert actual[f"J{posiciones[campo]}"].value == valor, campo
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
            elif name != "xl/worksheets/sheet1.xml":
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
    paths = {"referencia": convertir_pdf(REFERENCE, directory / "referencia.pdf")}
    for name, datos in (("blanca", {}), ("piloto", datos_ejemplo())):
        source = generar_saa1(datos, directory / f"{name}.xlsx")
        paths[name] = convertir_pdf(source, directory / f"{name}.pdf")
    return paths


def _textos_fijos_encabezado_y_pie(reader):
    """Compara todo el texto fijo; la fecha de V4 se controla como dato cargado."""
    encabezados, pies = [], []
    for index, page in enumerate(reader.pages):
        header, footer = [], []
        height, width = float(page.mediabox.height), float(page.mediabox.width)
        def visitor(text, cm, tm, font, size):
            if not text.strip():
                return
            x = tm[4] * cm[0] + tm[5] * cm[2] + cm[4]
            y = tm[4] * cm[1] + tm[5] * cm[3] + cm[5]
            top_limit = height - (126 if index == 0 else 70)
            # V4 es la fecha variable, a la derecha de FECHA, en la fila 4.
            is_date_value = index == 0 and x > width * 0.82 and height - 126 <= y < height - 112
            if y >= top_limit and not is_date_value:
                header.append(" ".join(text.split()))
            # El pie de SAA-1 comienza después de los cuatro renglones de observaciones.
            if index == len(reader.pages) - 1 and y <= height - 130:
                footer.append(" ".join(text.split()))
        page.extract_text(visitor_text=visitor)
        encabezados.append(tuple(header))
        pies.append(tuple(footer))
    return encabezados, pies


def test_conversion_real_con_libreoffice(pdfs_saa1):
    actual, reference = PdfReader(pdfs_saa1["piloto"]), PdfReader(pdfs_saa1["referencia"])
    assert len(actual.pages) == len(reference.pages)
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


@pytest.mark.xfail(reason="leyenda pendiente de confirmación de Martín", strict=True, raises=AssertionError)
def test_pdf_contiene_leyenda_iram_pendiente(pdfs_saa1):
    text = "\n".join(page.extract_text() for page in PdfReader(pdfs_saa1["piloto"]).pages)
    assert "Planilla conforme a IRAM 3546:2011" in text


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
