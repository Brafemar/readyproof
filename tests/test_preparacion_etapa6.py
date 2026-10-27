"""Fidelidad de las cuatro exportaciones JSON respecto de los datos del kit."""
from hashlib import sha256
import json
from pathlib import Path
import runpy

import pytest
from scripts.convertir_planillas_json import documentos

ROOT=Path(__file__).resolve().parents[1]


def sin_claves_duplicadas(pairs):
    result={}
    for key,value in pairs:
        assert key not in result,"El JSON contiene una clave duplicada."
        result[key]=value
    return result


@pytest.mark.parametrize("code",["SAA-1","SDI","SBC","SAL"])
def test_json_valido_y_equivalente_al_python(code):
    path=ROOT/"fuente/planillas"/(code+".json")
    document=json.loads(path.read_text(encoding="utf-8"),object_pairs_hook=sin_claves_duplicadas)
    expected=json.loads(json.dumps(documentos()[code],ensure_ascii=False))
    assert document==expected
    assert document["codigo"]==code and document["version"]=="v2"
    assert set(("cabecera","datos","firmas"))<=document.keys()
    assert len(document["cabecera"])==11
    assert list(document["firmas"])==["tecnico","responsable"]
    assert all(row["formato"]=="PNG" for row in document["firmas"].values())
    assert isinstance(document["datos"]["planillas"],list) and document["datos"]["planillas"]
    for key in ("origen","generador"):
        source=ROOT/"fuente"/document[key]["ruta"]
        assert sha256(source.read_bytes()).hexdigest()==document[key]["sha256"]


def test_cuatro_archivos_y_grupos_completos_sin_reordenar():
    directory=ROOT/"fuente/planillas"
    assert sorted(p.name for p in directory.iterdir())==["SAA-1.json","SAL.json","SBC.json","SDI.json"]
    original=runpy.run_path(str(ROOT/"fuente/herramientas/planillas_data2.py"))["SISTEMAS"]
    for code in ("SDI","SBC","SAL"):
        document=json.loads((directory/(code+".json")).read_text(encoding="utf-8"))
        assert [p["n"] for p in document["datos"]["planillas"]]==[p["n"] for p in original[code]["planillas"]]
        assert document["datos"]["nom"]==original[code]["nom"]
        assert sum(len(fields) for p in document["datos"]["planillas"] for _,fields in p["bloques"])==sum(len(fields) for p in original[code]["planillas"] for _,fields in p["bloques"])
