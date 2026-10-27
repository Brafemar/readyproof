"""Importación atómica e idempotente del catálogo JSON de etapa 6."""
from hashlib import sha256
import json
from pathlib import Path

from sqlalchemy import select,text
from .models import Manual,Planilla

RAIZ=Path(__file__).resolve().parent.parent
CODIGOS={"SAA-1","SDI","SBC","SAL"}
VERSION_CATALOGO="v2"


def huella_json(definicion):
    return sha256(json.dumps(definicion,sort_keys=True).encode()).hexdigest()


def objeto_sin_duplicados(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError("El JSON contiene claves duplicadas.")
        result[key]=value
    return result


def no_constante(value):
    raise ValueError("El JSON contiene una constante no válida.")


def leer_definiciones():
    directory=RAIZ/"fuente/planillas"
    paths=sorted(directory.glob("*.json"))
    if {p.stem for p in paths}!=CODIGOS:
        raise ValueError("Se requieren SAA-1.json, SDI.json, SBC.json y SAL.json; no se importa un conjunto incompleto o inesperado.")
    rows=[]
    for path in paths:
        definition=json.loads(path.read_text(encoding="utf-8"),object_pairs_hook=objeto_sin_duplicados,parse_constant=no_constante)
        code=path.stem
        if not isinstance(definition,dict) or definition.get("codigo")!=code or definition.get("version")!=VERSION_CATALOGO or definition.get("sistema_tipo")!="SG-PEM-IFI":
            raise ValueError("Los metadatos del JSON no coinciden con su código y versión.")
        if any(not isinstance(definition.get(section),dict) for section in ("cabecera","datos","firmas")):
            raise ValueError("Se requieren cabecera, datos y firmas como objetos JSON.")
        if not definition["cabecera"] or set(definition["firmas"])!={"tecnico","responsable"}:
            raise ValueError("La cabecera o las firmas de la definición no están completas.")
        sheets=definition["datos"].get("planillas")
        if not isinstance(sheets,list) or not sheets:
            raise ValueError("La definición debe conservar las planillas del grupo.")
        for sheet in sheets:
            if not isinstance(sheet,dict) or not isinstance(sheet.get("bloques"),list):raise ValueError("Planilla JSON inválida.")
            for block in sheet["bloques"]:
                if not isinstance(block,list) or len(block)!=2 or not isinstance(block[0],str) or not isinstance(block[1],list):raise ValueError("Bloque JSON inválido.")
        rows.append((code,definition,huella_json(definition)))
    return rows


def cargar_planillas_desde_json(session):
    rows=leer_definiciones()
    try:
        session.execute(text("SELECT pg_advisory_xact_lock(724006)"))
        prepared=[]
        for code,definition,digest in rows:
            manual=session.scalar(select(Manual).where(Manual.codigo==f"SG-PEM-IFI-{code}",Manual.version=="v1"))
            if manual is None:raise ValueError("Falta el manual requerido para el catálogo JSON.")
            existing=session.scalar(select(Planilla).where(Planilla.codigo==code,Planilla.version==VERSION_CATALOGO))
            if existing is not None:
                if existing.huella!=digest or existing.definicion!=definition or existing.sistema_tipo!="SG-PEM-IFI" or existing.manual_id not in (None,manual.id):
                    raise ValueError("La definición ya cargada difiere del JSON o del manual; registrar una versión nueva, sin sobrescribir la anterior.")
            prepared.append((code,definition,digest,manual,existing))
        added=0
        for code,definition,digest,manual,existing in prepared:
            if existing is None:
                session.add(Planilla(codigo=code,version=VERSION_CATALOGO,sistema_tipo="SG-PEM-IFI",huella=digest,definicion=definition,manual_id=manual.id));added+=1
            elif existing.manual_id is None:existing.manual_id=manual.id
        session.commit()
        return added
    except Exception:
        session.rollback()
        raise
