"""Registro y consulta ARCA con datos sintéticos y sin acceso a la API externa."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import pytest
from sqlalchemy import select, func
from app import create_app
from app.db import sesion
from app.models import Cliente
from app.contabilium import APIContabilium

@pytest.fixture(autouse=True)
def bloquear_api_externa(monkeypatch):
    def prohibida(*args, **kwargs):
        raise AssertionError("No se permite contactar Contabilium real en estas pruebas.")
    monkeypatch.setattr("app.contabilium.build_opener", prohibida)

def test_rutas_contabilium_registradas(app):
    rutas={rule.rule: rule.methods for rule in app.url_map.iter_rules()}
    assert "GET" in rutas["/api/admin/contabilium/clientes"]
    assert "GET" in rutas["/api/admin/contabilium/arca"]
    assert "POST" in rutas["/api/admin/contabilium/sincronizar"]

def test_configuracion_contabilium_desde_entorno(database_url, monkeypatch):
    monkeypatch.setenv("CONTABILIUM_CLIENT_ID", " ejemplo@example.invalid ")
    monkeypatch.setenv("CONTABILIUM_CLIENT_SECRET", " [Ejemplo] credencial de prueba ")
    app=create_app({"TESTING":True,"DATABASE_URL":database_url})
    try:
        assert app.config["CONTABILIUM_CLIENT_ID"]=="ejemplo@example.invalid"
        assert app.config["CONTABILIUM_CLIENT_SECRET"]=="[Ejemplo] credencial de prueba"
    finally:
        app.extensions["db_engine"].dispose()

@pytest.mark.parametrize("faltante", ["CONTABILIUM_CLIENT_ID", "CONTABILIUM_CLIENT_SECRET"])
def test_falta_configuracion_muestra_error(app, client, faltante):
    app.config.update(MODO_PILOTO=False,CONTABILIUM_CLIENT_ID="[Ejemplo] correo",CONTABILIUM_CLIENT_SECRET="[Ejemplo] clave")
    app.config[faltante]=""
    response=client.get("/api/admin/contabilium/arca?cuit=20000000001")
    assert response.status_code==503
    assert "Falta configurar" in response.json["error"]

def test_consulta_arca_no_guarda_cliente(app, client, monkeypatch):
    app.config.update(MODO_PILOTO=False,CONTABILIUM_CLIENT_ID="[Ejemplo] correo",CONTABILIUM_CLIENT_SECRET="[Ejemplo] clave")
    llamadas=[]
    def arca(self,cuit):
        llamadas.append(cuit)
        return {"nombre":"[Ejemplo] Padrón", "cuit":cuit, "contacto":{}, "contabilium_id":None}
    monkeypatch.setattr(APIContabilium,"arca",arca)
    with app.app_context():
        antes=sesion().scalar(select(func.count()).select_from(Cliente))
    response=client.get("/api/admin/contabilium/arca?cuit=20-00000000-1")
    assert response.status_code==200 and response.json["nombre"]=="[Ejemplo] Padrón"
    assert llamadas==["20000000001"]
    with app.app_context():
        assert sesion().scalar(select(func.count()).select_from(Cliente))==antes

def test_boton_arca_consulta_sin_guardar_y_muestra_error(app, client, tmp_path):
    app.config["MODO_PILOTO"]=False
    response=client.get("/admin")
    assert response.status_code==200
    html=tmp_path/"admin.html";html.write_text(response.get_data(as_text=True),encoding="utf8")
    node=os.environ.get("READYPROOF_NODE") or shutil.which("node")
    assert node, "Se requiere Node y Playwright para verificar el botón ARCA."
    result=subprocess.run([node,"tests/browser/contabilium_arca.cjs",str(html),str(Path("app/static/admin.js").resolve())],capture_output=True,text=True,timeout=60)
    assert result.returncode==0,result.stdout+result.stderr
    data=json.loads(result.stdout)
    assert data["ruta_correcta"] and data["sin_guardado_automatico"] and data["error_visible"]
