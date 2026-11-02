"""Recursos originales de la cabecera, leídos sin transformar imágenes."""
from pathlib import Path
from zipfile import ZipFile

from ..planillas.definiciones.saa1 import MODELO


def imagenes_cabecera():
    logo = Path(__file__).resolve().parents[1] / 'static/correo/logo_readyproof_principal.png'
    with ZipFile(MODELO) as archivo:
        iso = archivo.read('xl/media/image2.jpeg')
    return (
        dict(cid='logo-readyproof', nombre='logo_readyproof.png', subtipo='png', bytes=logo.read_bytes()),
        dict(cid='sello-iso', nombre='sello_iso.jpeg', subtipo='jpeg', bytes=iso),
    )
