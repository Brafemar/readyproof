"""Siglas del encabezado: coincidencia, rechazo y aislamiento entre clientes."""
import pytest
from sqlalchemy.orm import Session

from app.models import Cliente, Sistema
from scripts.importador_planillas import extraer_sigla_planilla, sistemas_por_sigla, validar_sigla_planilla


def encabezado(texto, fila=1):
    return {'primeras_filas':[{'fila':fila,'celda':f'A{fila}','texto':texto}]}


def test_extraer_sigla_valida():
    data=encabezado('Sistema de Abastecimiento de Agua (SAA)')
    assert extraer_sigla_planilla('SAA-1.xlsx',data) == 'SAA'
    assert extraer_sigla_planilla('SG-PEM-IFI-SAA-1_INFORMACION_GENERAL.xlsx',data) == 'SAA'


def test_extraer_sigla_invalida():
    with pytest.raises(ValueError,match='contradictorios|coinciden'):
        extraer_sigla_planilla('SAA-1.xlsx',encabezado('Sistema (SBC)'))
    with pytest.raises(ValueError,match='contradictorios'):
        extraer_sigla_planilla('SAA-1.xlsx',encabezado('Sistema (SAA), otro sistema (SBC)'))


def test_extraer_sigla_ausente():
    with pytest.raises(ValueError,match='No se pudo extraer sigla'):
        extraer_sigla_planilla('sin_codigo.xlsx',encabezado('Sistema de Cocinas Comerciales'))
    assert extraer_sigla_planilla('SAA-1.xlsx',encabezado('Sistema (SBC)',fila=21)) == 'SAA'


def test_sigla_codigo_interno_prioritario_y_fuente_reportada():
    result=validar_sigla_planilla('SAA-1.xlsx',encabezado('SG-PEM-IFI-SAA-1'),codigo_catalogo='SG-PEM-IFI-SAA-1')
    assert result['sigla_extraida']=='SAA' and result['fuente']=='codigo_interno_SG-PEM-IFI'
    assert result['validacion']=='OK' and result['sigla_validada'] and result['coincide_nombre_archivo']


def test_sigla_nombre_archivo_con_catalogo():
    result=validar_sigla_planilla('SAL-1.xlsx',encabezado('Agentes limpios'),codigo_catalogo='SG-PEM-IFI-SAL-1')
    assert result['fuente']=='nombre_archivo' and result['sigla_extraida']=='SAL'
    assert result['validacion']=='OK'


def test_parentesis_contradictorios_rechazados_aunque_tres_fuentes_coincidan():
    result=validar_sigla_planilla('SDI-1.xlsx',encabezado('SG-PEM-IFI-SDI-1 (SBC)'),codigo_catalogo='SG-PEM-IFI-SDI-1')
    assert result['validacion']=='FALLO' and not result['sigla_validada']


def test_dos_fuentes_de_tres_reportan_discrepancia():
    result=validar_sigla_planilla('SAP-1.xlsx',encabezado('SG-PEM-IFI-SAA-1'),codigo_catalogo='SG-PEM-IFI-SAP-1')
    assert result['sigla_extraida']=='SAP' and result['fuente']=='nombre_archivo'
    assert result['fuentes_discrepantes']=={'codigo_interno_SG-PEM-IFI':'SAA'}


def test_sigla_mapea_sistema(app):
    with Session(app.extensions['db_engine']) as db:
        a=Cliente(nombre='[Ejemplo] Planta A');b=Cliente(nombre='[Ejemplo] Planta B')
        db.add_all([a,b]);db.flush()
        rows=[Sistema(cliente_id=a.id,tipo='SAP',designacion='[Ejemplo] SAP 1'),
              Sistema(cliente_id=a.id,tipo='SAP',designacion='[Ejemplo] SAP 2'),
              Sistema(cliente_id=a.id,tipo='SAP',designacion='[Ejemplo] Inactivo',activo=False),
              Sistema(cliente_id=b.id,tipo='SAP',designacion='[Ejemplo] Otro cliente')]
        db.add_all(rows);db.flush()
        found=sistemas_por_sigla(db,a.id,extraer_sigla_planilla('SAP-1.xlsx',encabezado('Agua Pulverizada (SAP)')))
        assert {row.id for row in found} == {rows[0].id,rows[1].id}
        assert all(row.tipo=='SAP' and row.cliente_id==a.id for row in found)
