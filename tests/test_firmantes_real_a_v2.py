"""Identificación técnica ficticia: REAL sin prefijo y PILOTO con prefijo."""
from copy import deepcopy

from flask import Flask
from pypdf import PdfReader
import pytest

from app.planillas.firmantes import nombre_tecnico_segun_modo
from app.planillas.identificacion_pdf import lineas_firmantes
from app.planillas.generador import generar_saa1
from app.planillas.pdf import convertir_pdf
from tests.test_paginacion_a_v2 import firmantes


@pytest.mark.parametrize('piloto', [False, True])
def test_prefijo_tecnico_segun_modo_sin_alterar_identidad(piloto):
    app=Flask(__name__);app.config['MODO_PILOTO']=piloto
    datos=firmantes();datos['tecnico']['nombre']='[Ejemplo] Administración'
    original=deepcopy(datos)
    with app.app_context():
        tecnico=lineas_firmantes(datos,370)[0]
        assert any('Administración' in line for line in tecnico)
        assert ('[Ejemplo]' in '\n'.join(tecnico)) == piloto
        assert nombre_tecnico_segun_modo('Técnico de prueba') == 'Técnico de prueba'
    assert datos == original


def test_pdf_real_sin_prefijo_en_bloque_tecnico(tmp_path):
    app=Flask(__name__);app.config['MODO_PILOTO']=False
    datos=firmantes();datos['tecnico']['nombre']='[Ejemplo] Administración'
    original=deepcopy(datos)
    with app.app_context():
        excel=generar_saa1({},tmp_path/'planilla.xlsx')
        pdf=convertir_pdf(excel,tmp_path/'planilla.pdf',firmantes=datos)
    reader=PdfReader(pdf)
    bloque=reader.pages[-1].extract_text().split('TÉCNICO DE READYPROOF',1)[1].split('RESPONSABLE DE LA INSTALACIÓN',1)[0]
    assert 'Administración' in bloque and '[Ejemplo]' not in bloque
    assert datos == original
