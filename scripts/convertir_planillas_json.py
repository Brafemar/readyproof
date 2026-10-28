"""Exportación reproducible de definiciones del kit, sin editar los originales."""
import argparse
import ast
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import runpy
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from app.planillas.generador import CABECERA
from app.carga_planillas import VERSION_CATALOGO


def documentos():
    tools=ROOT/"fuente/herramientas"
    generator=tools/"build_planilla.py"
    tree=ast.parse(generator.read_text(encoding="utf-8-sig"))
    footer=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=="pie")
    labels=[node.value for node in ast.walk(footer) if isinstance(node,ast.Constant) and isinstance(node.value,str) and node.value.endswith("– FIRMA / ACLARACIÓN")]
    if len(labels)!=2:raise ValueError("El generador no tiene las dos etiquetas de firma esperadas.")
    firmas={role:{"etiqueta":label,"formato":"PNG"} for role,prefix in (("tecnico","SUPERVISOR"),("responsable","RESPONSABLE")) for label in labels if label.startswith(prefix)}
    systems2=runpy.run_path(str(tools/"planillas_data2.py"))["SISTEMAS"]
    saa=runpy.run_path(str(tools/"planillas_data3.py"))["SISTEMAS"]["SAA"]
    sources={code:("planillas_data2.py",systems2[code]) for code in ("SDI","SBC","SAL")}
    saa1=deepcopy(saa);saa1["planillas"]=[p for p in saa1["planillas"] if p["n"]==1]
    if len(saa1["planillas"])!=1:raise ValueError("SAA-1 no es única en el origen.")
    sources["SAA-1"]=("planillas_data3.py",saa1)
    result={}
    for code,(module,data) in sources.items():
        result[code]={"codigo":code,"version":VERSION_CATALOGO,"sistema_tipo":"SG-PEM-IFI","origen":{"ruta":"herramientas/"+module,"sha256":sha256((tools/module).read_bytes()).hexdigest()},
            "generador":{"ruta":"herramientas/build_planilla.py","sha256":sha256(generator.read_bytes()).hexdigest()},
            "cabecera":{key:{"tipo":"fecha" if key=="fecha" else "texto","celda":cell} for key,cell in CABECERA.items()},
            "datos":deepcopy(data),"firmas":deepcopy(firmas)}
    return result


def contenido_json(document):
    return (json.dumps(document,ensure_ascii=False,indent=2,allow_nan=False)+"\n").encode("utf-8")


def main():
    parser=argparse.ArgumentParser(description="Convierte SDI/SBC/SAL y SAA-1 a JSON sin editar las definiciones Python.")
    parser.add_argument("--verificar",action="store_true",help="Comprueba la equivalencia sin escribir archivos.")
    parser.add_argument("--actualizar-version",action="store_true",help="Registra una versión nueva de metadatos y conserva los JSON anteriores en bak; rechaza cambios de contenido.")
    args=parser.parse_args()
    if args.verificar and args.actualizar_version:parser.error("Elegir verificar o actualizar versión.")
    directory=ROOT/"fuente/planillas"
    if not args.verificar:directory.mkdir(parents=True,exist_ok=True)
    for code,document in documentos().items():
        path=directory/(code+".json");expected=contenido_json(document)
        if path.exists():
            if path.read_bytes()!=expected:
                previous=json.loads(path.read_text(encoding="utf-8"))
                old_version=previous.get("version","")
                if not args.actualizar_version or old_version==VERSION_CATALOGO or not re.fullmatch(r"[A-Za-z0-9._-]+",old_version):
                    raise ValueError("El JSON existente difiere del origen; no se sobrescribe: "+path.name)
                before={key:value for key,value in previous.items() if key not in ("version","generador")}
                after=json.loads(json.dumps({key:value for key,value in document.items() if key not in ("version","generador")},ensure_ascii=False))
                if before!=after or previous.get("generador",{}).get("ruta")!=document["generador"]["ruta"]:
                    raise ValueError("Cambió el contenido de la planilla; requiere revisión técnica: "+path.name)
                backup=ROOT/"bak"/"planillas_json"/old_version/path.name
                backup.parent.mkdir(parents=True,exist_ok=True)
                payload=path.read_bytes()
                if backup.exists():
                    if backup.read_bytes()!=payload:raise ValueError("El respaldo anterior difiere: "+path.name)
                else:
                    with backup.open("xb") as file:file.write(payload)
                temporary=path.with_suffix(".json.nueva-version")
                with temporary.open("xb") as file:file.write(expected)
                temporary.replace(path)
        elif args.verificar:raise ValueError("Falta el JSON: "+path.name)
        else:
            with path.open("xb") as file:file.write(expected)
        print(path.name+": equivalente al dato Python")


if __name__=="__main__":main()
