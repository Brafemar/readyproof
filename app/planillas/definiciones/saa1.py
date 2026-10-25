"""Definición piloto obtenida del kit, sin duplicar los campos de la serie."""
from copy import deepcopy
from pathlib import Path
import runpy

RAIZ = Path(__file__).resolve().parents[3]
HERRAMIENTAS = RAIZ / "fuente" / "herramientas"
MODELO = RAIZ / "fuente" / "modelos" / "SDI-1.xlsx"


def definicion_saa1():
    sistema = runpy.run_path(str(HERRAMIENTAS / "planillas_data3.py"))["SISTEMAS"]["SAA"]
    spec = deepcopy(next(p for p in sistema["planillas"] if p["n"] == 1))
    spec.update(sistema=sistema["nom"], codigo="SG-PEM-IFI-SAA-1", titulo=spec["nombre"])
    return spec
