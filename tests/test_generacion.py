from copy import copy
from pathlib import Path
from zipfile import ZipFile
import runpy
import subprocess

import pytest
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
    datos = {
        "cabecera": {"cliente": "[Ejemplo] Planta", "fecha": "25/10/2026"},
        "bloques": {"ABASTECIMIENTO DE AGUA": {"Capacidad": 40, "Ubicación": "A superficie"}},
        "observaciones": ["[Ejemplo] Carga ficticia para revisión."],
    }
    result = generar_saa1(datos, tmp_path / "carga.xlsx")
    blank = generar_saa1({}, tmp_path / "blanca.xlsx")
    actual, expected = load_workbook(result).active, load_workbook(blank).active
    assert actual["C5"].value == "[Ejemplo] Planta"
    assert actual["V4"].value == "25/10/2026"
    assert any(c.value == "40  m³" for row in actual for c in row)
    choices = next(c.value for row in actual for c in row if isinstance(c.value, str) and "A superficie  ☑" in c.value)
    assert "Enterrado  ☐" in choices and "Nivel  ☐" in choices
    assert actual["T3"].value == "T.C. 3 AÑOS"
    for row in expected:
        for cell in row:
            if cell.column == 1 and cell.row != 36:
                assert actual[cell.coordinate].value == cell.value
    with ZipFile(result) as filled, ZipFile(blank) as base:
        assert set(filled.namelist()) == set(base.namelist())
        for name in base.namelist():
            if name == "docProps/core.xml":
                left, right = etree.fromstring(filled.read(name)), etree.fromstring(base.read(name))
                for root in (left, right):
                    for child in list(root):
                        if etree.QName(child).localname in {"created", "modified"}:
                            root.remove(child)
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


def test_conversion_real_con_libreoffice(tmp_path):
    from app.planillas.pdf import localizar_libreoffice
    try:
        localizar_libreoffice()
    except FileNotFoundError:
        pytest.skip("Prueba de integración: requiere LibreOffice instalado.")
    from app.planillas.piloto import datos_ejemplo
    source = generar_saa1(datos_ejemplo(), tmp_path / "piloto.xlsx")
    result = convertir_pdf(source, tmp_path / "piloto.pdf")
    assert result.read_bytes().startswith(b"%PDF-")
    assert result.stat().st_size > 1000
    from pypdf import PdfReader
    actual = PdfReader(result)
    reference = PdfReader(convertir_pdf(REFERENCE, tmp_path / "referencia.pdf"))
    assert len(actual.pages) == len(reference.pages)
    assert all(len(page.images) == 2 for page in actual.pages)
    for document in (actual, reference):
        text = "\n".join(page.extract_text() for page in document.pages)
        for label in ("SG-PEM-IFI-SAA-1", "T.C. 3 AÑOS", "SUPERVISOR DEL MANTENEDOR", "RESPONSABLE DE LA INSTALACIÓN"):
            assert label in text


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
