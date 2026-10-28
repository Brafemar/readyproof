"""Conversión local de Excel a PDF mediante LibreOffice, con perfil aislado."""
import os
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory

from .encabezado_pdf import reponer_logos


def localizar_libreoffice():
    configured = os.environ.get("LIBREOFFICE_BIN")
    if configured:
        path = Path(configured)
        if path.is_file():
            return path.resolve()
        raise FileNotFoundError("LIBREOFFICE_BIN no apunta a un ejecutable existente.")
    for name in ("soffice.com", "soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            return Path(found)
    for base in (os.environ.get("ProgramFiles"), os.environ.get("ProgramFiles(x86)")):
        if base:
            for name in ("soffice.com", "soffice.exe"):
                candidate = Path(base) / "LibreOffice" / "program" / name
                if candidate.is_file():
                    return candidate
    raise FileNotFoundError("LibreOffice no está instalado o no se encuentra en PATH.")


def convertir_pdf(origen, destino, *, timeout=120, firmas=None,firmantes=None):
    """Convierte con Calc; publica el PDF solo si la conversión finaliza correctamente."""
    origen, destino = Path(origen).resolve(), Path(destino).resolve()
    if not origen.is_file() or origen.suffix.lower() != ".xlsx":
        raise ValueError("Se requiere un archivo .xlsx existente.")
    if destino.suffix.lower() != ".pdf":
        raise ValueError("El destino debe tener extensión .pdf.")
    if destino.exists():
        raise FileExistsError(destino)
    executable = localizar_libreoffice()
    destino.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="pdf-", dir=destino.parent) as temp:
        temp = Path(temp)
        profile = (temp / "perfil").as_uri()
        result = subprocess.run(
            [str(executable), f"-env:UserInstallation={profile}", "--headless",
             "--nologo", "--nodefault", "--norestore", "--convert-to", "pdf:calc_pdf_Export",
             "--outdir", str(temp), str(origen)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=timeout, check=False,
        )
        output = temp / (origen.stem + ".pdf")
        if result.returncode != 0 or not output.is_file():
            raise RuntimeError(f"LibreOffice no produjo el PDF (código {result.returncode}): {result.stdout} {result.stderr}")
        final = temp / 'con_logos.pdf'
        from .firmas import logo_readyproof
        reponer_logos(origen, output, final, logo_izquierdo=logo_readyproof())
        from .marca_agua import incorporar_marca_agua
        marked=temp/"con_marca_agua.pdf"
        incorporar_marca_agua(origen,final,marked)
        final=marked
        if firmas and any(firmas.values()):
            from .firmas import incorporar_firmas
            signed = temp / 'con_firmas.pdf'
            incorporar_firmas(origen, final, signed, firmas)
            final = signed
        from .leyenda_iram import incorporar_leyenda_iram
        declared=temp/"con_leyenda_iram.pdf"
        incorporar_leyenda_iram(final,declared,firmantes=firmantes)
        final=declared
        payload = final.read_bytes()
        if not payload.startswith(b"%PDF-"):
            raise RuntimeError("LibreOffice produjo un archivo que no es PDF.")
        with destino.open("xb") as stream:
            stream.write(payload)
    return destino
