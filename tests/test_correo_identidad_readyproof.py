"""Identidad del correo, imágenes originales y hash del PDF sin transmisión."""
from email import policy
from email.parser import BytesParser
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4
from zipfile import ZipFile
import re

from PIL import Image
from pypdf import PdfWriter
import pytest
from sqlalchemy.orm import Session

from app.correo import crear_mensaje, preparar_envio
from app.correo.emision import contenido_emision, renderizar_emision
from app.models import Carga
from app.models.fotos import FotoCarga
from tests.test_email_emision_b import contexto_render, datos_correo
from tests.test_smtp_gmail import carga_emitida

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def sin_transporte_real(monkeypatch):
    def prohibido(*args, **kwargs):
        raise AssertionError('Estas pruebas solo preparan MIME; no se permite transporte real.')
    monkeypatch.setattr('app.gmail_https.obtener_token', prohibido)
    monkeypatch.setattr('app.gmail_https.enviar_con_token', prohibido)


@pytest.mark.parametrize('cantidad', [0, 1, 3])
def test_identidad_y_linea_condicional(contexto_render, cantidad):
    data = datos_correo()
    data['cantidad_fotos'] = cantidad
    result = renderizar_emision(data)
    html = result['html']
    assert '#D41120' in html and '#1B2430' in html
    assert '#0f2f4f' not in html.lower() and '#d32f2f' not in html.lower()
    assert 'font-family:Arial,Helvetica,sans-serif' in html
    assert '@font-face' not in html
    assert re.findall(r'<img[^>]+src="([^"]+)"', html) == ['cid:logo-readyproof', 'cid:sello-iso']
    for value in (html, result['cuerpo']):
        assert ('Fotos de campo:' in value) == (cantidad > 0)
        assert ('anexo incluido en el PDF' in value) == (cantidad > 0)
    if cantidad:
        assert f'Fotos de campo: {cantidad} (anexo incluido en el PDF)' in result['cuerpo']


@pytest.mark.parametrize('cantidad', [True, -1, 1.5])
def test_cantidad_invalida_rechazada(contexto_render, cantidad):
    data = datos_correo()
    data['cantidad_fotos'] = cantidad
    with pytest.raises(ValueError, match='cantidad de fotos'):
        renderizar_emision(data)


def test_mime_cid_bytes_originales_y_control_del_adjunto(contexto_render, monkeypatch):
    contexto_render.config['MAIL_MODO_PRUEBA'] = True
    monkeypatch.setenv('MAIL_FROM', 'readyproof@example.invalid')
    writer = PdfWriter()
    writer.add_blank_page(width=595, height=842)
    buffer = BytesIO()
    writer.write(buffer)
    pdf = buffer.getvalue()
    data = datos_correo()
    data['pdf_hash'] = sha256(pdf).hexdigest()
    result = renderizar_emision(data)
    envio = SimpleNamespace(id=str(uuid4()), destinatario='cliente@example.invalid',
        asunto=result['asunto'], cuerpo=result['cuerpo'], pdf_copia=pdf)
    mime = crear_mensaje(envio, html=result['html'], nombre_adjunto=result['nombre_adjunto'])
    mail = BytesParser(policy=policy.default).parsebytes(mime)
    assert mail.get_content_type() == 'multipart/mixed'
    assert mail.get_body(preferencelist=('html',)).get_content_type() == 'text/html'
    assert any(part.get_content_type() == 'multipart/related' for part in mail.walk())
    images = {part['Content-ID']: part for part in mail.walk() if part.get_content_maintype() == 'image'}
    assert set(images) == {'<logo-readyproof>', '<sello-iso>'}
    with ZipFile(ROOT/'fuente/modelos/SDI-1.xlsx') as archive:
        expected = {'<logo-readyproof>': (ROOT/'app/static/correo/logo_readyproof_principal.png').read_bytes(),
                    '<sello-iso>': archive.read('xl/media/image2.jpeg')}
    for cid, part in images.items():
        assert part.get_content_disposition() == 'inline'
        assert part.get_payload(decode=True) == expected[cid]
    attachments = list(mail.iter_attachments())
    assert len(attachments) == 1 and attachments[0].get_content_type() == 'application/pdf'
    attached = attachments[0].get_payload(decode=True)
    assert attached == pdf
    for kind in ('html', 'plain'):
        assert sha256(attached).hexdigest()[:16] in mail.get_body(preferencelist=(kind,)).get_content()


def test_cantidad_se_consulta_en_la_carga(app, carga_emitida):
    with app.app_context(), Session(app.extensions['db_engine']) as db:
        carga = db.get(Carga, carga_emitida)
        assert 'Fotos de campo:' not in contenido_emision(db, carga)['cuerpo']
        image = BytesIO()
        Image.new('RGB', (32, 24), 'white').save(image, format='JPEG')
        jpeg = image.getvalue()
        db.add_all(FotoCarga(carga_id=carga.id, orden=n, imagen=jpeg, ancho=32, alto=24,
                            sha256=sha256(jpeg).hexdigest()) for n in (1, 2))
        db.flush()
        result = contenido_emision(db, carga)
        assert 'Fotos de campo: 2 (anexo incluido en el PDF)' in result['cuerpo']
        assert sha256(bytes(carga.pdf)).hexdigest()[:16] in result['cuerpo']


def test_preparador_usa_hash_real_y_conserva_pdf(app, carga_emitida, usuario_admin):
    with app.app_context(), Session(app.extensions['db_engine']) as db:
        carga = db.get(Carga, carga_emitida)
        envio = preparar_envio(db, carga, 'cliente@example.invalid', usuario_admin['id'])
        mail = BytesParser(policy=policy.default).parsebytes(envio.mensaje_eml)
        attached = list(mail.iter_attachments())[0].get_payload(decode=True)
        assert attached == bytes(carga.pdf)
        assert envio.pdf_sha256 == sha256(attached).hexdigest()
        for kind in ('plain', 'html'):
            assert sha256(attached).hexdigest()[:16] in mail.get_body(preferencelist=(kind,)).get_content()


def test_pdf_alterado_se_rechaza_antes_de_preparar(app, carga_emitida, usuario_admin):
    with app.app_context(), Session(app.extensions['db_engine']) as db:
        carga = db.get(Carga, carga_emitida)
        carga.pdf = bytes(carga.pdf) + b'\n% [Ejemplo] alterado'
        with pytest.raises(ValueError, match='huella del PDF'):
            preparar_envio(db, carga, 'cliente@example.invalid', usuario_admin['id'])
