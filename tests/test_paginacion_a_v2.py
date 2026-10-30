"""Paginación con datos ficticios, márgenes y preservación del kit."""
from base64 import b64decode
from copy import deepcopy
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import runpy
import shutil
import subprocess
from tempfile import gettempdir
from zipfile import ZipFile

from lxml import etree
from openpyxl import load_workbook
from PIL import Image
from pypdf import PdfReader
import pytest

from app.planillas.generador import _generar_paquete
from app.planillas.pdf import convertir_pdf
from app.planillas.registro_pdf import incorporar_modo, incorporar_registro
from app.planillas.firmantes import ejemplo_responsable
from scripts.prueba_operativa_final import firma_ficticia

ROOT = Path(__file__).resolve().parents[1]
N = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'


def especificacion(kind, large=False):
    spec = dict(codigo='SG-PEM-IFI-PRUEBA-1', sistema='[Ejemplo] Sistema de prueba', titulo='[Ejemplo] Paginación',
                tipo='general' if kind == 'general' else 'checklist' if kind == 'ver' else 'periodico')
    if kind.startswith('grid'): spec['modo'] = 'semanal' if kind == 'grid_s' else 'mensual'
    spec['bloques'] = [(f'[Ejemplo] BLOQUE {i}', [f'[Ejemplo] Control {i}-{j}' for j in range(4)]) for i in range(12 if large else 1)]
    return spec


def firmantes():
    return dict(tecnico=dict(nombre='[Ejemplo] Técnico',login='tecnico-ejemplo'), responsable=ejemplo_responsable(),
                empresa='[Ejemplo] Planta', fecha='2026-10-30')


@pytest.mark.parametrize('kind', ['general', 'grid_s', 'grid_m', 'ver'])
@pytest.mark.parametrize('large', [False, True])
def test_paginacion_por_formato(tmp_path, kind, large):
    spec = especificacion(kind, large)
    excel = _generar_paquete(spec, {}, tmp_path/'planilla.xlsx')
    sheet = load_workbook(excel).active
    assert all(getattr(sheet.page_margins, key) >= 10/25.4 for key in ('left','right','bottom','top'))
    assert sheet.print_area.endswith(f'$Y${sheet.max_row}') or f'$Y${sheet.max_row}' in sheet.print_area
    if large:
        assert sheet.print_title_rows == '$1:$8'
        assert sheet.row_breaks.brk
        for brk in sheet.row_breaks.brk:
            assert not any(r.min_row <= brk.id < r.max_row for r in sheet.merged_cells.ranges)
            observation = next(c.row for c in sheet['A'] if c.value == 'OBSERVACIONES:')
            assert not observation <= brk.id < sheet.max_row
    else:
        assert sheet.sheet_properties.pageSetUpPr.fitToPage
        assert sheet.page_setup.fitToWidth == sheet.page_setup.fitToHeight == 1
    signatures = {role:b64decode(firma_ficticia(offset).split(',')[1]) for role,offset in [('tecnico',0),('responsable',25)]}
    pdf = convertir_pdf(excel, tmp_path/'planilla.pdf', firmas=signatures, firmantes=firmantes())
    payload = incorporar_modo(incorporar_registro(pdf.read_bytes(), 9999, 0), 'REAL')
    marked = tmp_path/'registrada.pdf'; marked.write_bytes(payload)
    reader = PdfReader(BytesIO(payload))
    page_texts = [page.extract_text() for page in reader.pages]
    for title, items in spec['bloques']:
        assert title in '\n'.join(page_texts)
        assert all(sum(item in value for value in page_texts) == 1 for item in items)
        if kind != 'general':
            assert any(title in value and all(item in value for item in items) for value in page_texts)
    assert (len(reader.pages) > 1) if large else (len(reader.pages) == 1)
    assert sum(str(name).startswith('/Firma_') for p in reader.pages for name in p['/Resources']['/XObject']) == 2
    for page in reader.pages:
        text = page.extract_text()
        assert all(value in text for value in ('Registro 9999','Modo REAL','Planilla conforme a IRAM 3546:2011'))
        assert '/RPLogo0' in page['/Resources']['/XObject']
        assert '/RPLogo1' in page['/Resources']['/XObject']
        if large: assert '[Ejemplo] Sistema de prueba'.upper() in text
    last_text = reader.pages[-1].extract_text()
    assert 'OBSERVACIONES:' in last_text and 'FIRMA / ACLARACIÓN' in last_text
    subprocess.run([shutil.which('pdftoppm'), '-r','100','-png',str(marked),str(tmp_path/'raster')], check=True, capture_output=True)
    for path in tmp_path.glob('raster-*.png'):
        with Image.open(path) as image:
            gray = image.convert('L')
            # Encabezado oficial exceptuado del mínimo de 10 mm, con mínimo 4 mm.
            mask = gray.point(lambda v:255 if v < 230 else 0)
            box = mask.getbbox()
            assert min(box[0], box[1], gray.width-box[2], gray.height-box[3]) >= 16
            body = gray.crop((0, 115, gray.width, gray.height))
            bbox = body.point(lambda v:255 if v < 230 else 0).getbbox()
            assert bbox[0] >= 39 and body.width-bbox[2] >= 39
            assert body.height-bbox[3] >= 39


def test_scc2_referencia_real_una_pagina_sin_modificar_original(tmp_path):
    reference = ROOT/'docs/referencias/SCC-2_Registro1_Revision0.pdf'
    before = sha256(reference.read_bytes()).hexdigest() if reference.exists() else None
    if reference.exists():
        original = PdfReader(reference)
        assert original.metadata['/ReadyproofRegistro'] == '1'
        assert original.metadata['/ReadyproofRevision'] == '0'
        assert len(original.pages) == 2
    group = runpy.run_path(str(ROOT/'fuente/herramientas/planillas_data4.py'))['SISTEMAS']['SCC']
    spec = deepcopy(next(row for row in group['planillas'] if row['n'] == 2))
    spec.update(codigo='SG-PEM-IFI-SCC-2', sistema=group['nom'], titulo=spec['nombre'])
    excel = _generar_paquete(spec, {'C5':'[Ejemplo] Planta de prueba'}, tmp_path/'scc2.xlsx')
    pdf = convertir_pdf(excel, tmp_path/'scc2.pdf', firmantes=firmantes())
    reader = PdfReader(pdf)
    assert len(reader.pages) == 1
    assert 'OBSERVACIONES:' in reader.pages[0].extract_text()
    assert 'FIRMA / ACLARACIÓN' in reader.pages[0].extract_text()
    if reference.exists(): assert sha256(reference.read_bytes()).hexdigest() == before


def test_perfil_libreoffice_fuera_del_directorio_de_impresion(tmp_path, monkeypatch):
    from pypdf import PdfWriter
    import app.planillas.pdf as module
    nested = tmp_path/('ruta_impresion_'*5)
    excel = _generar_paquete(especificacion('general'), {}, nested/'entrada.xlsx')
    observed = []
    def convert(command, **kwargs):
        uri = next(value.split('=',1)[1] for value in command if value.startswith('-env:UserInstallation='))
        assert uri.startswith(Path(gettempdir()).resolve().as_uri()+'/lo-')
        assert not uri.startswith(nested.resolve().as_uri())
        observed.append(uri)
        directory = Path(command[command.index('--outdir')+1])
        writer = PdfWriter(); writer.add_blank_page(width=841.89,height=595.28)
        writer.write(directory/'entrada.pdf')
        return subprocess.CompletedProcess(command,0,'','')
    monkeypatch.setattr(module,'localizar_libreoffice',lambda:Path('soffice'))
    monkeypatch.setattr(module.subprocess,'run',convert)
    for index in range(2):
        assert convertir_pdf(excel,nested/f'salida{index}.pdf').exists()
    assert len(set(observed)) == 2
