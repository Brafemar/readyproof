"""Metadatos de origen y control del adjunto tras incorporar fotos."""
from email import policy
from email.parser import BytesParser
from hashlib import sha256
from io import BytesIO
from types import SimpleNamespace

from pypdf import PdfReader, PdfWriter
from sqlalchemy.orm import Session

from app.correo import preparar_envio
from app.fotos.anexo_pdf import generar_anexo, unir_pdf
from app.fotos.emision import incorporar_fotos_carga
from app.models import Carga
from app.planillas.leyenda_iram import TEXTO
from tests.test_fotos_emision import jpeg_prueba
from tests.test_smtp_gmail import carga_emitida


def pdf(metadata):
    writer = PdfWriter()
    writer.add_blank_page(width=595.2756, height=841.8898)
    writer.add_metadata(metadata)
    out = BytesIO()
    writer.write(out)
    return out.getvalue()


def test_union_conserva_metadatos_de_planilla_con_varias_fotos():
    original = {'/ReadyproofIRAM': TEXTO, '/Title': '[Ejemplo] Planilla',
                '/ReadyproofRegistro': '1', '/Producer': 'readyproof'}
    result = pdf(original)
    annex = pdf({'/Title': '[Ejemplo] Anexo', '/ReadyproofIRAM': 'no sustituir'})
    for _ in range(2):
        result = unir_pdf(result, annex)
        metadata = PdfReader(BytesIO(result)).metadata
        for key, value in original.items():
            assert metadata[key] == value
    assert len(PdfReader(BytesIO(result)).pages) == 3


def test_union_no_inventa_marca_ausente():
    result = unir_pdf(pdf({'/Title': '[Ejemplo] Sin marca'}), pdf({'/ReadyproofIRAM': TEXTO}))
    assert '/ReadyproofIRAM' not in PdfReader(BytesIO(result)).metadata


def test_sin_fotos_mismos_bytes_y_hash():
    class DBVacia:
        def scalars(self, query):
            return []
    original = pdf({'/ReadyproofIRAM': TEXTO})
    result = incorporar_fotos_carga(original, SimpleNamespace(id=1), {}, DBVacia())
    assert result is original
    assert sha256(result).digest() == sha256(original).digest()


def test_preparador_acepta_anexo_y_control_corresponde_al_adjunto(app, carga_emitida, usuario_admin, tmp_path, monkeypatch):
    def prohibido(*args, **kwargs):
        raise AssertionError('Esta prueba no permite transporte de correo.')
    monkeypatch.setattr('smtplib.SMTP', prohibido)
    monkeypatch.setattr('app.gmail_https.enviar_con_token', prohibido)
    app.config['MAIL_MODO_PRUEBA'] = True
    with app.app_context(), Session(app.extensions['db_engine']) as db:
        carga = db.get(Carga, carga_emitida)
        anterior = bytes(carga.pdf)
        anterior_hash = sha256(anterior).hexdigest()
        refs = [dict(numero=1, x=.5, y=.45, codigo='O', texto='[Ejemplo] Se observa grasa.')]
        annex = generar_anexo(jpeg_prueba(), refs, refs, carga=carga.datos)
        final = unir_pdf(anterior, annex)
        assert PdfReader(BytesIO(final)).metadata['/ReadyproofIRAM'] == TEXTO
        assert len(PdfReader(BytesIO(final)).pages) == 2
        carga.pdf = final
        carga.pdf_sha256 = carga.pdf_hash = sha256(final).hexdigest()
        assert carga.pdf_hash != anterior_hash
        envio = preparar_envio(db, carga, 'cliente@example.invalid', usuario_admin['id'])
        message = BytesParser(policy=policy.default).parsebytes(envio.mensaje_eml)
        attached = list(message.iter_attachments())[0].get_payload(decode=True)
        assert attached == final
        assert envio.pdf_sha256 == sha256(attached).hexdigest()
        for kind in ('html', 'plain'):
            assert sha256(attached).hexdigest()[:16] in message.get_body(preferencelist=(kind,)).get_content()
        (tmp_path/'ejemplo_anexo_metadatos.pdf').write_bytes(final)
        assert sha256(anterior).hexdigest() == anterior_hash
        db.rollback()
