from copy import deepcopy
from io import BytesIO
from hashlib import sha256

import pytest
from pypdf import PdfReader
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import StaleDataError

from app import create_app
from app.models import Carga, Cliente, Sistema, RevisionCarga, VersionEsquema


def crear(client, catalogo, datos):
    _, sistema, planilla = catalogo
    return client.post("/api/cargas", json={"sistema_id": sistema["id"], "planilla_id": planilla["id"], "datos": datos})


def test_catalogo_y_esquema_postgresql(client, catalogo, app):
    cliente, sistema, planilla = catalogo
    assert cliente["nombre"].startswith("[Ejemplo]")
    assert sistema["cliente_id"] == cliente["id"]
    assert planilla["codigo"] == "SG-PEM-IFI-SAA-1"
    response = client.get(f"/api/planillas/{planilla['id']}")
    assert response.get_json()["definicion"]["cabecera"]["fecha"]["tipo"] == "fecha"
    with Session(app.extensions["db_engine"]) as session:
        assert session.get(VersionEsquema, 1) is not None


def test_creacion_consulta_borrador_y_trazabilidad(client, catalogo, datos_api):
    created = crear(client, catalogo, datos_api)
    assert created.status_code == 201
    carga = created.get_json()
    assert carga["revision"] == 1 and carga["estado"] == "borrador"
    datos = deepcopy(carga["datos"])
    datos["observaciones"] = ["[Ejemplo] Revisión de borrador"]
    response = client.put(f"/api/cargas/{carga['id']}/borrador", json={"revision": 1, "datos": datos})
    assert response.status_code == 200
    assert response.get_json()["revision"] == 2
    assert client.get(f"/api/cargas/{carga['id']}").get_json()["datos"] == datos
    revisions = client.get(f"/api/cargas/{carga['id']}/revisiones").get_json()
    assert [r["evento"] for r in revisions] == ["creada", "borrador_guardado"]
    assert revisions[0]["datos"] != revisions[1]["datos"]
    stale = client.put(f"/api/cargas/{carga['id']}/borrador", json={"revision": 1, "datos": datos_api})
    assert stale.status_code == 409


@pytest.mark.parametrize("mutation", [
    lambda d: d.update(ajeno="[Ejemplo] Campo"),
    lambda d: d["cabecera"].update(inventado="[Ejemplo] Campo"),
    lambda d: d["cabecera"].update(fecha="2026-02-30"),
    lambda d: d["cabecera"].update(fecha="25/10/2026"),
    lambda d: d["cabecera"].update(telefono=1234),
    lambda d: d["cabecera"].update(cliente="Cliente sin identificador ficticio"),
    lambda d: d["bloques"]["ABASTECIMIENTO DE AGUA"].update(Capacidad="1"),
    lambda d: d["bloques"]["ABASTECIMIENTO DE AGUA"].update(Capacidad=True),
    lambda d: d["bloques"]["ABASTECIMIENTO DE AGUA"].update(Capacidad=float("inf")),
    lambda d: d["bloques"]["ABASTECIMIENTO DE AGUA"].update(Ubicación="Otra"),
    lambda d: d["bloques"]["BOMBAS CONTRA INCENDIO (CAPÍTULO 12)"].update(Cantidad=1.5),
    lambda d: d.update(observaciones=["[Ejemplo] Línea"] * 5),
    lambda d: d["bloques"].update(OTRO={}),
    lambda d: d["bloques"]["INSTALACIÓN"].update(inventado="[Ejemplo] Campo"),
])
def test_validacion_no_guarda_datos_invalidos(client, catalogo, datos_api, mutation, app):
    mutation(datos_api)
    assert crear(client, catalogo, datos_api).status_code == 422
    with Session(app.extensions["db_engine"]) as session:
        assert list(session.scalars(select(Carga))) == []


def test_edicion_invalida_conserva_revision(client, catalogo, datos_api):
    carga = crear(client, catalogo, datos_api).get_json()
    datos_api["cabecera"]["fecha"] = 1234
    response = client.put(f"/api/cargas/{carga['id']}/borrador", json={"revision": 1, "datos": datos_api})
    assert response.status_code == 422
    assert client.get(f"/api/cargas/{carga['id']}").get_json()["revision"] == 1


def test_finalizacion_y_bloqueo_de_edicion(client, catalogo, datos_api):
    carga = crear(client, catalogo, datos_api).get_json()
    response = client.post(f"/api/cargas/{carga['id']}/finalizar", json={"revision": 1})
    assert response.status_code == 200 and response.get_json()["estado"] == "finalizada"
    assert client.put(f"/api/cargas/{carga['id']}/borrador", json={"revision": 2, "datos": datos_api}).status_code == 409
    assert client.post(f"/api/cargas/{carga['id']}/finalizar", json={"revision": 2}).status_code == 409


def test_borrador_vacio_y_transiciones_invalidas(client, catalogo):
    carga = crear(client, catalogo, {}).get_json()
    assert client.post(f"/api/cargas/{carga['id']}/finalizar", json={"revision": 1}).status_code == 422
    assert client.post(f"/api/cargas/{carga['id']}/emitir", json={"revision": 1}).status_code == 409
    assert client.get(f"/api/cargas/{carga['id']}/pdf").status_code == 409


def test_json_invalido_y_referencia_inexistente(client, catalogo, datos_api):
    assert client.post("/api/cargas", data="{", content_type="application/json").status_code == 400
    assert client.post("/api/cargas", json=[]).status_code == 422
    assert client.get("/api/cargas/no-existe").status_code == 404
    assert client.get("/api/clientes/no-existe/sistemas").status_code == 404


def test_bloqueo_cliente_no_ejemplo(client, catalogo, datos_api, app):
    cliente, _, _ = catalogo
    with Session(app.extensions["db_engine"]) as session:
        session.get(Cliente, cliente["id"]).es_ejemplo = False
        session.commit()
    assert crear(client, catalogo, datos_api).status_code == 403


def test_plantilla_modificada_no_se_usa(client, catalogo, datos_api, monkeypatch):
    import app.rutas.api as module
    monkeypatch.setattr(module, "huella_saa1", lambda: "otra")
    assert crear(client, catalogo, datos_api).status_code == 409


def test_control_optimista_en_base(client, catalogo, datos_api, app):
    carga = crear(client, catalogo, datos_api).get_json()
    with Session(app.extensions["db_engine"]) as first, Session(app.extensions["db_engine"]) as second:
        a, b = first.get(Carga, carga["id"]), second.get(Carga, carga["id"])
        a.datos = {"observaciones": ["[Ejemplo] Primera revisión"]}
        first.commit()
        b.datos = {"observaciones": ["[Ejemplo] Segunda revisión"]}
        with pytest.raises(StaleDataError):
            second.commit()


def test_sin_base_externa_ni_sustitucion_silenciosa():
    with pytest.raises(RuntimeError):
        create_app({"DATABASE_URL": "sqlite:///:memory:"})
    with pytest.raises(RuntimeError):
        create_app({"DATABASE_URL": "postgresql+psycopg://localhost.invalid/readyproof"})


def test_fallo_emision_no_finaliza_transaccion(client, catalogo, datos_api, monkeypatch):
    import app.rutas.api as module
    carga = crear(client, catalogo, datos_api).get_json()
    client.post(f"/api/cargas/{carga['id']}/finalizar", json={"revision": 1})
    def failure(*args, **kwargs):
        raise RuntimeError("fallo de prueba")
    monkeypatch.setattr(module, "convertir_pdf", failure)
    assert client.post(f"/api/cargas/{carga['id']}/emitir", json={"revision": 2}).status_code == 503
    result = client.get(f"/api/cargas/{carga['id']}").get_json()
    assert result["estado"] == "finalizada" and result["revision"] == 2
    assert not result["pdf_disponible"]



def test_cliente_no_ejemplo_no_se_consulta_ni_emite(client, catalogo, datos_api, app):
    carga = crear(client, catalogo, datos_api).get_json()
    client.post(f"/api/cargas/{carga['id']}/finalizar", json={"revision": 1})
    with Session(app.extensions["db_engine"]) as session:
        session.get(Cliente, catalogo[0]["id"]).es_ejemplo = False
        session.commit()
    assert client.get("/api/clientes").get_json() == []
    assert client.get(f"/api/clientes/{catalogo[0]['id']}/sistemas").status_code == 403
    assert client.get(f"/api/cargas/{carga['id']}").status_code == 403
    assert client.get(f"/api/cargas/{carga['id']}/revisiones").status_code == 403
    assert client.post(f"/api/cargas/{carga['id']}/emitir", json={"revision": 2}).status_code == 403
    with Session(app.extensions["db_engine"]) as session:
        assert session.get(Carga, carga["id"]).pdf is None


def test_finalizacion_revalida_el_json_guardado(client, catalogo, datos_api, app):
    carga = crear(client, catalogo, datos_api).get_json()
    with Session(app.extensions["db_engine"]) as session:
        row = session.get(Carga, carga["id"])
        invalid = deepcopy(row.datos)
        invalid["cabecera"]["fecha"] = "2026-02-30"
        row.datos = invalid
        session.commit()
        revision = row.revision
    assert client.post(f"/api/cargas/{carga['id']}/finalizar", json={"revision": revision}).status_code == 422


@pytest.mark.parametrize("revision", [True, 1.0, "1"])
def test_revision_exige_entero(client, catalogo, datos_api, revision):
    carga = crear(client, catalogo, datos_api).get_json()
    assert client.post(f"/api/cargas/{carga['id']}/finalizar", json={"revision": revision}).status_code == 422


def test_init_db_es_idempotente(app, client):
    result = app.test_cli_runner().invoke(args=["init-db", "--ejemplos"])
    assert result.exit_code == 0
    assert len(client.get("/api/clientes").get_json()) == 1
    assert len(client.get("/api/planillas").get_json()) == 5
