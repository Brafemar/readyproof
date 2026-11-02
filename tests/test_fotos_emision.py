"""Integración del anexo en emisión: persistencia, PDF original e integridad."""
from copy import deepcopy
from hashlib import sha256
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw
from pypdf import PdfReader
import pytest
from reportlab.pdfgen.canvas import Canvas
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.fotos.emision import incorporar_fotos_carga
from app.fotos.items import items_punto2
from app.models import Carga, Cliente, EmisionCarga, Planilla, Sistema
from app.models.fotos import FotoCarga
from app.planillas.firmantes import ejemplo_responsable
from app.planillas.registro_pdf import incorporar_modo, incorporar_registro
from scripts.prueba_operativa_final import firma_ficticia

ROOT = Path(__file__).resolve().parents[1]


def lector(payload):
    return PdfReader(BytesIO(payload))


def jpeg_prueba():
    image = Image.new('RGB', (1200, 900), '#e4eced')
    draw = ImageDraw.Draw(image)
    draw.rectangle((180, 180, 1000, 700), fill='#8f969a', outline='#1b2430', width=8)
    draw.rectangle((240, 240, 940, 590), fill='#363d43')
    for x in range(260, 940, 24):
        draw.line((x, 250, x, 580), fill='#c1c8cb', width=6)
    output = BytesIO()
    image.save(output, format='JPEG', quality=70)
    return output.getvalue()


@pytest.fixture
def carga_emision(app, client, catalogo, datos_api):
    cliente, sistema, planilla = catalogo
    planilla = client.get(f"/api/planillas/{planilla['id']}").get_json()
    # Datos ficticios en REAL: no se usa una cuenta ni una base productiva.
    app.config.update(MODO_PILOTO=False, EMPRESA_MANTENEDORA='Mantenedora ficticia para pruebas',
                      CERTIFICADO_N='PRUEBA-00001')
    with Session(app.extensions['db_engine']) as db:
        db.get(Cliente, cliente['id']).es_ejemplo = False
        db.commit()
    data = deepcopy(datos_api)
    data['cabecera'].update(empresa_mantenedora=app.config['EMPRESA_MANTENEDORA'],
                            numero_mantenedor=app.config['CERTIFICADO_N'])
    response = client.post('/api/cargas', json=dict(sistema_id=sistema['id'], planilla_id=planilla['id'],
        datos=data, responsable=ejemplo_responsable(),
        firmas={role: firma_ficticia() for role in ('tecnico', 'responsable')}))
    assert response.status_code == 201, response.get_json()
    return response.get_json()['id'], data, planilla


@pytest.fixture
def conversion_fija(monkeypatch):
    import app.rutas.api as api
    buf = BytesIO()
    canvas = Canvas(buf, pagesize=(595.2756, 841.8898), invariant=1)
    canvas.drawString(50, 780, '[Ejemplo] Planilla original')
    canvas.showPage()
    canvas.save()
    original = buf.getvalue()
    def convertir(origen, destino, **kwargs):
        Path(destino).write_bytes(original)
        return Path(destino)
    monkeypatch.setattr(api, 'convertir_pdf', convertir)
    return original


def agregar_foto(client, carga, planilla, *, con_marcas=True):
    jpeg = jpeg_prueba()
    response = client.post(f'/api/cargas/{carga}/fotos', data=jpeg, content_type='image/jpeg')
    assert response.status_code == 201, response.get_json()
    foto = response.get_json()
    if con_marcas:
        item = items_punto2(planilla['definicion'])[0]
        response = client.post(f"/api/cargas/{carga}/fotos/{foto['id']}/anotaciones", json={'anotaciones': [
            dict(numero=1, x=.5, y=.45, codigo='O', texto='[Ejemplo] Se observa grasa.', item=item)]})
        assert response.status_code == 200, response.get_json()
    return jpeg, foto


def emitir(client, carga):
    current = client.get(f'/api/cargas/{carga}').get_json()
    done = client.post(f'/api/cargas/{carga}/finalizar', json={'revision': current['revision']})
    assert done.status_code == 200, done.get_json()
    return client.post(f'/api/cargas/{carga}/emitir', json={'revision': done.get_json()['revision']})


def pdf_guardado(app, carga):
    with Session(app.extensions['db_engine']) as db:
        row = db.get(Carga, carga)
        snapshot = db.scalar(select(EmisionCarga).where(EmisionCarga.carga_id == carga))
        assert snapshot is not None
        assert snapshot.pdf == row.pdf
        assert row.pdf_hash == row.pdf_sha256 == snapshot.pdf_sha256 == sha256(row.pdf).hexdigest()
        return bytes(row.pdf), row.numero_registro, row.revision_publica


def test_sin_fotos_conserva_bytes_del_flujo_anterior(app, client, carga_emision, conversion_fija):
    carga, datos, _ = carga_emision
    assert emitir(client, carga).status_code == 201
    pdf, numero, revision = pdf_guardado(app, carga)
    anterior = incorporar_modo(incorporar_registro(conversion_fija, numero, revision), 'REAL')
    assert pdf == anterior
    assert len(lector(pdf).pages) == 1
    with Session(app.extensions['db_engine']) as db:
        assert incorporar_fotos_carga(conversion_fija, db.get(Carga, carga), datos, db) is conversion_fija


@pytest.mark.parametrize('cantidad', [1, 2])
def test_emision_con_fotos_marcas_item_cabecera_y_jpeg_original(app, client, carga_emision, conversion_fija, cantidad):
    carga, datos, planilla = carga_emision
    fotos = [agregar_foto(client, carga, planilla)[0] for _ in range(cantidad)]
    assert emitir(client, carga).status_code == 201
    pdf, numero, revision = pdf_guardado(app, carga)
    pages = lector(pdf).pages
    assert len(pages) == 1 + cantidad
    assert '[Ejemplo] Planilla original' in pages[0].extract_text()
    for page, jpeg in zip(pages[1:], fotos):
        text = page.extract_text()
        for value in ('ANEXO FOTOGRÁFICO', 'Ítem:', 'Código: O (no cumple)',
                      'Observación: [Ejemplo] Se observa grasa.',
                      items_punto2(planilla['definicion'])[0]['texto'],
                      datos['cabecera']['cliente'], datos['cabecera']['inspector'], '25/10/2026',
                      f'Registro {numero}', f'Revisión {revision}', 'Modo REAL'):
            assert value in text
        image = page['/Resources']['/XObject']['/RPFOTO'].get_object()
        assert sha256(image._data).hexdigest() == sha256(jpeg).hexdigest()
        assert image['/Filter'] == '/DCTDecode'
        assert abs(float(page.mediabox.width) - 210*72/25.4) < .01


def test_foto_sin_marcas_tambien_se_incluye(app, client, carga_emision, conversion_fija):
    carga, _, planilla = carga_emision
    agregar_foto(client, carga, planilla, con_marcas=False)
    assert emitir(client, carga).status_code == 201
    pdf, _, _ = pdf_guardado(app, carga)
    assert len(lector(pdf).pages) == 2
    assert 'Sin marcas registradas.' in lector(pdf).pages[1].extract_text()


def test_foto_corrupta_no_emite_ni_archiva_pdf_parcial(app, client, carga_emision, conversion_fija):
    carga, _, planilla = carga_emision
    _, foto = agregar_foto(client, carga, planilla)
    with Session(app.extensions['db_engine']) as db:
        db.get(FotoCarga, foto['id']).sha256 = '0'*64
        db.commit()
    response = emitir(client, carga)
    assert response.status_code == 503
    with Session(app.extensions['db_engine']) as db:
        row = db.get(Carga, carga)
        assert row.estado == 'finalizada' and row.pdf is None and row.pdf_hash is None
        assert db.scalar(select(EmisionCarga).where(EmisionCarga.carga_id == carga)) is None


def test_ejemplo_emision_real_con_libreoffice(app, client, carga_emision, tmp_path):
    carga, _, planilla = carga_emision
    jpeg, _ = agregar_foto(client, carga, planilla)
    response = emitir(client, carga)
    assert response.status_code == 201, response.get_json()
    pdf, _, _ = pdf_guardado(app, carga)
    pages = lector(pdf).pages
    assert len(pages) >= 2
    assert 'ANEXO FOTOGRÁFICO' not in pages[0].extract_text()
    assert 'ANEXO FOTOGRÁFICO' in pages[-1].extract_text()
    assert pages[-1]['/Resources']['/XObject']['/RPFOTO'].get_object()._data == jpeg
    (tmp_path/'ejemplo_emision_con_anexo.pdf').write_bytes(pdf)
