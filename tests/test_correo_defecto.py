"""Contrato por defecto de la emisión: plantilla, remitente y PDF íntegro."""
from email import policy
from email.parser import BytesParser
from hashlib import sha256
from io import BytesIO
from types import SimpleNamespace

import pytest
from sqlalchemy.orm import Session
from pypdf import PdfReader

from app.config import configuracion
from app.correo import crear_mensaje, preparar_envio, send_email
from app.correo.emision import contenido_emision
from app.fotos.anexo_pdf import numerar_pdf
from app.models import Carga
from tests.test_smtp_gmail import carga_emitida


@pytest.fixture(autouse=True)
def sin_red(monkeypatch):
    def prohibido(*args, **kwargs):
        raise AssertionError('No se permite transmitir correo en estas pruebas.')
    monkeypatch.setattr('smtplib.SMTP', prohibido)
    monkeypatch.setattr('smtplib.SMTP_SSL', prohibido)
    monkeypatch.setattr('app.gmail_https.obtener_token', prohibido)
    monkeypatch.setattr('app.gmail_https.enviar_con_token', prohibido)


def limpiar_remitente(monkeypatch):
    for key in ('MAIL_FROM', 'SMTP_FROM', 'SMTP_USER'):
        monkeypatch.delenv(key, raising=False)


def test_remitente_por_defecto_config_y_mime(app, monkeypatch):
    limpiar_remitente(monkeypatch)
    assert configuracion()['MAIL_FROM'] == 'readyproof.ar@gmail.com'
    monkeypatch.setenv('SMTP_USER', 'autenticacion@example.invalid')
    app.config.pop('MAIL_FROM', None)
    with app.app_context():
        envio = SimpleNamespace(id='prueba', destinatario='cliente@example.invalid',
            asunto='[Ejemplo] Prueba', cuerpo='[Ejemplo] Texto', pdf_copia=b'%PDF-ficticio')
        message = BytesParser(policy=policy.default).parsebytes(crear_mensaje(envio))
    assert str(message['From']) == 'readyproof.ar@gmail.com'


@pytest.mark.parametrize('mail,smtp,esperado', [
    ('remitente@example.invalid', 'alternativo@example.invalid', 'remitente@example.invalid'),
    (None, 'alternativo@example.invalid', 'alternativo@example.invalid')])
def test_remitente_configurable_por_entorno(app, monkeypatch, mail, smtp, esperado):
    limpiar_remitente(monkeypatch)
    if mail: monkeypatch.setenv('MAIL_FROM', mail)
    monkeypatch.setenv('SMTP_FROM', smtp)
    assert configuracion()['MAIL_FROM'] == esperado
    with app.app_context():
        envio = SimpleNamespace(id='prueba', destinatario='cliente@example.invalid',
            asunto='[Ejemplo] Prueba', cuerpo='[Ejemplo] Texto', pdf_copia=b'%PDF-ficticio')
        message = BytesParser(policy=policy.default).parsebytes(crear_mensaje(envio))
    assert str(message['From']) == esperado


def test_preparador_por_defecto_usa_plantilla_y_cid(app, carga_emitida, usuario_admin, monkeypatch):
    limpiar_remitente(monkeypatch)
    app.config.pop('MAIL_FROM', None)
    with app.app_context(), Session(app.extensions['db_engine']) as db:
        carga = db.get(Carga, carga_emitida)
        envio = preparar_envio(db, carga, 'cliente@example.invalid', usuario_admin['id'],
            '[Ejemplo] Asunto heredado', '[Ejemplo] Cuerpo heredado')
        message = BytesParser(policy=policy.default).parsebytes(envio.mensaje_eml)
        assert str(message['From']) == 'readyproof.ar@gmail.com'
        html = message.get_body(preferencelist=('html',)).get_content()
        assert '#D41120' in html and '#1B2430' in html
        assert 'font-family:Arial,Helvetica,sans-serif' in html
        assert 'Asunto heredado' not in str(message['Subject'])
        assert 'Cuerpo heredado' not in html
        assert {str(p['Content-ID']) for p in message.walk() if p.get_content_maintype() == 'image'} == {'<logo-readyproof>', '<sello-iso>'}
        attached = list(message.iter_attachments())[0].get_payload(decode=True)
        assert attached == carga.pdf
        assert sha256(attached).hexdigest() == carga.pdf_sha256
        assert carga.pdf_sha256[:16] in html


def test_cola_sin_mime_tambien_usa_plantilla(app, carga_emitida, usuario_admin):
    with app.app_context(), Session(app.extensions['db_engine']) as db:
        carga = db.get(Carga, carga_emitida)
        envio = preparar_envio(db, carga, 'cliente@example.invalid', usuario_admin['id'])
        envio.mensaje_eml = None
        envio.asunto = '[Ejemplo] Antiguo'
        envio.cuerpo = '[Ejemplo] Antiguo'
        result = send_email(db, envio, encolar=True)
        message = BytesParser(policy=policy.default).parsebytes(result.mensaje_eml)
        html = message.get_body(preferencelist=('html',)).get_content()
        assert '#D41120' in html and 'cid:logo-readyproof' in html and 'cid:sello-iso' in html
        assert 'Antiguo' not in str(message['Subject'])
        assert sha256(result.mensaje_eml).hexdigest() == result.eml_sha256


def test_control_exige_hash_de_emision_valido(app, carga_emitida):
    with app.app_context(), Session(app.extensions['db_engine']) as db:
        carga = db.get(Carga, carga_emitida)
        carga.pdf = bytes(carga.pdf) + b'\n% [Ejemplo] alterado'
        with pytest.raises(ValueError, match='huella del PDF'):
            contenido_emision(db, carga)


def test_pdf_sin_fotos_numerado_conserva_iram(app, carga_emitida):
    with Session(app.extensions['db_engine']) as db:
        original = bytes(db.get(Carga, carga_emitida).pdf)
    result = numerar_pdf(original)
    reader = PdfReader(BytesIO(result))
    assert reader.metadata['/ReadyproofIRAM'] == 'Planilla conforme a IRAM 3546:2011'
    assert 'Pág. 1 de 1' in reader.pages[0].extract_text()
    assert reader.metadata['/ReadyproofPaginas'] == '1'
    assert numerar_pdf(result) == result
