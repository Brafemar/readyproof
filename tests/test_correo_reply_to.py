"""Encabezados del correo de emisión, sin transmisión de mensajes."""
from email import policy
from email.parser import BytesParser
from types import SimpleNamespace
from uuid import uuid4

from flask import Flask
import pytest

from app.correo import crear_mensaje


@pytest.mark.parametrize("contacto,esperado", [
    ("contacto@example.invalid", "contacto@example.invalid"),
    (None, "informes@readyproof.ar"),
    ("", "informes@readyproof.ar"),
])
def test_reply_to_configurado_o_predeterminado_sin_cambiar_from(monkeypatch, contacto, esperado):
    monkeypatch.delenv("MAIL_FROM", raising=False)
    monkeypatch.delenv("SMTP_FROM", raising=False)
    app = Flask(__name__)
    app.config["MAIL_FROM"] = "readyproof.ar@gmail.com"
    if contacto is not None:
        app.config["CONTACTO_CORREO"] = contacto
    envio = SimpleNamespace(id=uuid4(), destinatario="prueba@example.invalid",
                            asunto="[Ejemplo] Emisión de prueba", cuerpo="[Ejemplo] Planilla.",
                            pdf_copia=b"%PDF-1.4\n[Ejemplo] adjunto ficticio")
    with app.app_context():
        raw = crear_mensaje(envio)
    mensaje = BytesParser(policy=policy.default).parsebytes(raw)
    assert mensaje.get_all("Reply-To") == [esperado]
    assert str(mensaje["From"]) == "readyproof.ar@gmail.com"
    assert str(mensaje["To"]) == "prueba@example.invalid"
    assert next(mensaje.iter_attachments()).get_payload(decode=True) == envio.pdf_copia
