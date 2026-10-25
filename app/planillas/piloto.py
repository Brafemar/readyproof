"""Ejemplo local SAA-1 con datos ficticios para revisión visual."""
import argparse
from datetime import date
from pathlib import Path

from .definiciones.saa1 import definicion_saa1
from .generador import generar_saa1
from .pdf import convertir_pdf


def datos_ejemplo():
    datos = {
        "cabecera": {
            "fecha": date(2026, 10, 25), "cliente": "[Ejemplo] Planta de prueba",
            "cuit": "[Ejemplo] Sin dato", "telefono": "[Ejemplo] Sin dato",
            "direccion": "[Ejemplo] Calle de prueba", "edificio": "[Ejemplo] Nave 1",
            "sector": "[Ejemplo] Sector 1", "inspector": "[Ejemplo] Técnico",
            "sistema_designacion": "[Ejemplo] Abastecimiento de agua",
        },
        "bloques": {},
        "observaciones": [
            "[Ejemplo] Todos los datos cargados son ficticios.",
            "[Ejemplo] Documento piloto para revisión de formato.",
        ],
    }
    for titulo, campos in definicion_saa1()["bloques"]:
        valores = {}
        for campo in campos:
            etiqueta, opciones = campo if isinstance(campo, tuple) else (campo, None)
            if isinstance(opciones, list):
                valor = opciones[0]
            elif isinstance(opciones, str) and opciones:
                valor = 1
            else:
                valor = "[Ejemplo] Dato de prueba"
            valores[etiqueta] = valor
        datos["bloques"][titulo] = valores
    return datos


def main():
    parser = argparse.ArgumentParser(description="Genera el piloto ficticio SAA-1 de readyproof.")
    parser.add_argument("--salida", type=Path, default=Path("out/etapa1/piloto"))
    parser.add_argument("--solo-excel", action="store_true")
    args = parser.parse_args()
    xlsx = args.salida / "SAA-1_ejemplo.xlsx"
    pdf = args.salida / "SAA-1_ejemplo.pdf"
    if xlsx.exists() or (not args.solo_excel and pdf.exists()):
        parser.error("El destino ya contiene un piloto; indicar otra carpeta para no sobrescribirlo.")
    generar_saa1(datos_ejemplo(), xlsx)
    print(xlsx.resolve())
    if not args.solo_excel:
        convertir_pdf(xlsx, pdf)
        print(pdf.resolve())


if __name__ == "__main__":
    main()
