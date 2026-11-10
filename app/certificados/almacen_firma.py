"""Almacenamiento privado por versión y validación de la firma gráfica."""
import os
import re
import stat
from contextlib import contextmanager
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from PIL import Image

from ..planillas.validacion import DatosInvalidos

MAX_BYTES = 262144
PNG = b"\x89PNG\r\n\x1a\n"


def validar_png(datos):
    if not 0 < len(datos) <= MAX_BYTES or not datos.startswith(PNG):
        raise DatosInvalidos("La firma debe ser un PNG de hasta 256 KiB.")
    try:
        with Image.open(BytesIO(datos)) as imagen:
            if (imagen.format != "PNG" or getattr(imagen, "n_frames", 1) != 1
                    or not 10 <= imagen.width <= 2400 or not 10 <= imagen.height <= 1000):
                raise DatosInvalidos("Usá un PNG de un solo fotograma, de hasta 2400 × 1000 píxeles.")
            imagen.verify()
        with Image.open(BytesIO(datos)) as imagen:
            rgba = imagen.convert("RGBA")
    except (OSError, SyntaxError, Image.DecompressionBombError):
        raise DatosInvalidos("El PNG está dañado o incompleto.") from None
    minimo, maximo = rgba.getchannel("A").getextrema()
    visible = Image.alpha_composite(Image.new("RGBA", rgba.size, "white"), rgba).convert("RGB")
    if minimo != 0 or maximo == 0 or all(x == (255, 255) for x in visible.getextrema()):
        raise DatosInvalidos("La firma debe tener fondo transparente y un trazo visible.")
    salida = BytesIO()
    Image.frombytes("RGBA", rgba.size, rgba.tobytes()).save(salida, "PNG", optimize=True)
    if salida.tell() > MAX_BYTES:
        raise DatosInvalidos("El PNG normalizado supera los 256 KiB.")
    return salida.getvalue()


def comprobar(fd, modo, tipo):
    info = os.fstat(fd)
    if (not tipo(info.st_mode) or stat.S_IMODE(info.st_mode) != modo
            or info.st_uid != os.geteuid() or info.st_gid != os.getegid()):
        raise PermissionError("El almacenamiento de la firma no es privado.")


@contextmanager
def directorio_privado(instance, *, crear=False):
    # La instalación de pruebas usa Linux. Sin estas garantías el acceso falla cerrado.
    if os.name != "posix" or not hasattr(os, "O_NOFOLLOW"):
        raise PermissionError("El almacenamiento requiere permisos POSIX verificados.")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    if crear:
        Path(instance).mkdir(mode=0o700, exist_ok=True)
    padre = os.open(instance, flags)
    try:
        if crear:
            try:
                os.mkdir("firmas_certificado", 0o700, dir_fd=padre)
                os.fsync(padre)
            except FileExistsError:
                pass
        fd = os.open("firmas_certificado", flags, dir_fd=padre)
        try:
            comprobar(fd, 0o700, stat.S_ISDIR)
            yield fd
        finally:
            os.close(fd)
    finally:
        os.close(padre)


def leer_version(fd, huella):
    if not re.fullmatch(r"[0-9a-f]{64}", huella):
        raise ValueError("Huella de firma inválida.")
    archivo = os.open(huella + ".png", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
    with os.fdopen(archivo, "rb") as f:
        comprobar(f.fileno(), 0o600, stat.S_ISREG)
        datos = f.read(MAX_BYTES + 1)
    if len(datos) > MAX_BYTES or sha256(datos).hexdigest() != huella:
        raise ValueError("La firma guardada no coincide con su huella.")
    return datos


def guardar_version(fd, datos):
    huella = sha256(datos).hexdigest()
    try:
        leer_version(fd, huella)
        return huella
    except FileNotFoundError:
        pass
    temporal = f".pendiente-{uuid4().hex}"
    archivo = os.open(temporal, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                     0o600, dir_fd=fd)
    with os.fdopen(archivo, "wb") as f:
        comprobar(f.fileno(), 0o600, stat.S_ISREG)
        f.write(datos)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temporal, huella + ".png", src_dir_fd=fd, dst_dir_fd=fd)
    os.fsync(fd)
    return huella
