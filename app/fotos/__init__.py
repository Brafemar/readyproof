"""Carga de fotos estandarizadas, con acceso restringido por cliente."""
from flask import Request

MAX_FOTO_BYTES = 2 * 1024 * 1024


class SolicitudConFotos(Request):
    @property
    def max_content_length(self):
        if self.endpoint == 'fotos.subir':
            return MAX_FOTO_BYTES + 1
        return super().max_content_length
