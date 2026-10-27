"""Pruebas sobre PostgreSQL local aislado, sin credenciales persistentes."""
import os
import secrets
from pathlib import Path
import socket
import subprocess
from uuid import uuid4

import psycopg
from psycopg import sql
import pytest
from sqlalchemy.orm import Session

from app import create_app
from app.catalogo import registrar_ejemplos
from app.db import crear_esquema
from app.planillas.piloto import datos_ejemplo
from app.planillas.validacion import FECHAS, ENTEROS


@pytest.fixture(scope="session")
def postgres_temporal(tmp_path_factory):
    candidates = [Path(os.environ.get("PG_BINDIR", ""))]
    candidates += [Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "PostgreSQL" / str(version) / "bin" for version in range(18, 13, -1)]
    binary = next((p for p in candidates if (p / "initdb.exe").is_file()), None)
    if binary is None:
        pytest.fail("Se requieren binarios PostgreSQL locales para las pruebas de la etapa 2.")
    directory = tmp_path_factory.mktemp("postgres_local")
    data = directory / "data"
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    init = subprocess.run([str(binary / "initdb.exe"), "-D", str(data), "--username=readyproof_test", "--encoding=UTF8", "--locale=C", "--auth=trust", "--no-instructions"], capture_output=True, text=True, timeout=90)
    assert init.returncode == 0, "No se pudo inicializar el clúster temporal de pruebas: " + init.stderr
    log = (directory / "control.log").open("w", encoding="utf-8")
    try:
        start = subprocess.run([str(binary / "pg_ctl.exe"), "-D", str(data), "-l", str(directory / "postgres.log"), "-o", f"-h 127.0.0.1 -p {port} -F", "-w", "-t", "60", "start"], stdout=log, stderr=subprocess.STDOUT, timeout=75)
        assert start.returncode == 0, "No se pudo iniciar PostgreSQL temporal; revisar control.log."
        yield {"host": "127.0.0.1", "port": port, "user": "readyproof_test"}
    finally:
        if (data / "postmaster.pid").exists():
            stop = subprocess.run([str(binary / "pg_ctl.exe"), "-D", str(data), "-m", "fast", "-w", "stop"], stdout=log, stderr=subprocess.STDOUT, timeout=60)
            assert stop.returncode == 0, "No se pudo detener el clúster de pruebas."
        log.close()



@pytest.fixture
def database_url(postgres_temporal):
    name = "rp_test_" + uuid4().hex
    with psycopg.connect(**postgres_temporal, dbname="postgres", autocommit=True) as connection:
        connection.execute(sql.SQL("CREATE DATABASE {} TEMPLATE template0").format(sql.Identifier(name)))
    yield f"postgresql+psycopg://readyproof_test@127.0.0.1:{postgres_temporal['port']}/{name}"
    with psycopg.connect(**postgres_temporal, dbname="postgres", autocommit=True) as connection:
        connection.execute(sql.SQL("DROP DATABASE {} WITH (FORCE)").format(sql.Identifier(name)))


@pytest.fixture
def app(database_url, tmp_path):
    application = create_app({"TESTING": True, "DATABASE_URL": database_url, "DIRECTORIO_TEMPORAL": str(tmp_path / "temporales")})
    engine = application.extensions["db_engine"]
    result=application.test_cli_runner().invoke(args=["init-db","--ejemplos"])
    assert result.exit_code==0,result.output
    yield application
    engine.dispose()


@pytest.fixture
def usuario_admin(app):
    from app.auth import hash_clave
    from app.models import Usuario
    password=secrets.token_urlsafe(24)
    with Session(app.extensions["db_engine"],expire_on_commit=False) as session:
        user=Usuario(login="admin-ejemplo",nombre="[Ejemplo] Administración",rol="admin",clave_hash=hash_clave(password))
        session.add(user);session.commit()
        return {"id":user.id,"login":user.login,"clave":password}


def login_cliente(app,login,clave):
    client=app.test_client()
    csrf=client.get("/api/auth/sesion").get_json()["csrf_token"]
    response=client.post("/api/auth/login",json={"login":login,"clave":clave},headers={"X-CSRF-Token":csrf})
    assert response.status_code==200
    client.environ_base["HTTP_X_CSRF_TOKEN"]=response.get_json()["csrf_token"]
    return client


@pytest.fixture
def client(app,usuario_admin):
    return login_cliente(app,usuario_admin["login"],usuario_admin["clave"])


@pytest.fixture
def catalogo(client):
    cliente = client.get("/api/clientes").get_json()[0]
    sistema = client.get(f"/api/clientes/{cliente['id']}/sistemas").get_json()[0]
    planilla = next(p for p in client.get("/api/planillas").get_json() if p["codigo"]=="SG-PEM-IFI-SAA-1")
    return cliente, sistema, planilla


@pytest.fixture
def datos_api():
    data = datos_ejemplo()
    data["cabecera"]["fecha"] = "2026-10-25"
    for title, label in FECHAS:
        data["bloques"][title][label] = "2026-10-25"
    for title, label in ENTEROS:
        data["bloques"][title][label] = 1
    return data


@pytest.fixture(autouse=True)
def impedir_smtp_real(monkeypatch):
    import smtplib
    def prohibido(*args, **kwargs):
        raise AssertionError("Los tests no pueden contactar un servidor SMTP real.")
    monkeypatch.setattr(smtplib,"SMTP",prohibido)
    monkeypatch.setattr(smtplib,"SMTP_SSL",prohibido)
