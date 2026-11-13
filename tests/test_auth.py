"""Sesiones, permisos por cliente, auditoría y conservación de datos."""
from copy import deepcopy
from datetime import timedelta
import secrets

import pytest
from sqlalchemy import delete, select, text
from sqlalchemy.orm import Session

from app.auth import hash_clave
from app.db import crear_esquema
from app.models import (Carga, Cliente, RegistroAcceso, RevisionCarga, SesionUsuario,
    Sistema, Usuario, UsuarioCliente, VersionEsquema, ahora)
from tests.conftest import login_cliente


def tecnico(client,catalogo):
    password=secrets.token_urlsafe(24)
    response=client.post("/api/admin/usuarios",json={"login":"tecnico-ejemplo","nombre":"[Ejemplo] Técnico","rol":"tecnico","clave":password,"cliente_ids":[catalogo[0]["id"]]})
    assert response.status_code==201
    return response.get_json(),password


def test_api_exige_sesion_y_csrf(app,client):
    anonymous=app.test_client()
    assert anonymous.get("/api/clientes").status_code==401
    assert anonymous.get("/api/planillas").status_code==401
    assert anonymous.get("/api/catalogo-carga").status_code==401
    assert anonymous.get("/api/catalogo-carga/definiciones").status_code==401
    assert anonymous.post("/api/cargas",json={}).status_code==401
    assert client.post("/api/admin/clientes",json={"nombre":"[Ejemplo] Otro"},headers={"X-CSRF-Token":"invalido"}).status_code==403
    assert client.post("/api/admin/clientes",json={"nombre":"[Ejemplo] Otro"},headers={"Origin":"https://otro.invalid"}).status_code==403
    cookie=client.get_cookie("session")
    assert cookie.http_only and cookie.same_site=="Lax"


def test_tecnico_no_admin_y_solo_clientes_asignados(app,client,catalogo):
    user,password=tecnico(client,catalogo)
    other=client.post("/api/admin/clientes",json={"nombre":"[Ejemplo] Otra planta"}).get_json()
    tech=login_cliente(app,user["login"],password)
    assert [c["id"] for c in tech.get("/api/clientes").get_json()]==[catalogo[0]["id"]]
    assert tech.get(f"/api/clientes/{other['id']}/sistemas").status_code==404
    agrupado=tech.get("/api/catalogo-carga").get_json()
    assert [c["id"] for c in agrupado["clientes"]]==[catalogo[0]["id"]]
    assert set(agrupado["sistemas"])=={catalogo[0]["id"]}
    assert tech.get("/api/admin/usuarios").status_code==403
    assert tech.get("/api/admin/accesos").status_code==403
    assert tech.get("/admin").status_code==403
    assert tech.post("/api/admin/usuarios",json={}).status_code==403
    assert tech.post("/api/admin/clientes",json={}).status_code==403


@pytest.mark.parametrize("route,method",[("","GET"),("/revisiones","GET"),("/pdf","GET"),("/borrador","PUT"),("/finalizar","POST"),("/emitir","POST"),("/vista-previa","POST")])
def test_ninguna_ruta_de_carga_filtra_otro_cliente(app,client,catalogo,datos_api,route,method):
    user,password=tecnico(client,catalogo)
    other=client.post("/api/admin/clientes",json={"nombre":"[Ejemplo] Otra planta"}).get_json()
    system=client.post(f"/api/admin/clientes/{other['id']}/sistemas",json={"tipo":"SAA","designacion":"[Ejemplo] Otro SAA"}).get_json()
    data=deepcopy(datos_api);data["cabecera"]["cliente"]=other["nombre"]
    row=client.post("/api/cargas",json={"sistema_id":system["id"],"planilla_id":catalogo[2]["id"],"datos":data}).get_json()
    tech=login_cliente(app,user["login"],password)
    body={"revision":1,"datos":data} if method=="PUT" else {"revision":1}
    assert tech.open(f"/api/cargas/{row['id']}"+route,method=method,json=body if method!="GET" else None).status_code==404
    assert tech.post("/api/cargas",json={"sistema_id":system["id"],"planilla_id":catalogo[2]["id"],"datos":data},headers={"Idempotency-Key":row["id"]}).status_code==404
    assert tech.post("/api/cargas",json={"sistema_id":system["id"],"planilla_id":catalogo[2]["id"],"datos":data}).status_code==404


def test_baja_revoca_sesiones_inmediatamente(app,client,catalogo):
    user,password=tecnico(client,catalogo);tech=login_cliente(app,user["login"],password)
    assert tech.get("/api/clientes").status_code==200
    assert client.put(f"/api/admin/usuarios/{user['id']}",json={"rol":"tecnico","activo":False,"cliente_ids":[]}).status_code==200
    assert tech.get("/api/clientes").status_code==401
    anonymous=app.test_client();csrf=anonymous.get("/api/auth/sesion").get_json()["csrf_token"]
    assert anonymous.post("/api/auth/login",json={"login":user["login"],"clave":password},headers={"X-CSRF-Token":csrf}).status_code==401


def test_cambio_clave_cierra_todas_las_sesiones(app,client,catalogo):
    user,password=tecnico(client,catalogo);first=login_cliente(app,user["login"],password);second=login_cliente(app,user["login"],password)
    new=secrets.token_urlsafe(24)
    assert first.post("/api/auth/clave",json={"actual":password,"nueva":new}).status_code==200
    assert first.get("/api/clientes").status_code==401 and second.get("/api/clientes").status_code==401
    assert login_cliente(app,user["login"],new).get("/api/clientes").status_code==200
    with Session(app.extensions["db_engine"]) as db:
        stored=db.get(Usuario,user["id"]).clave_hash
        assert stored!=new.encode() and stored.startswith(b"$2b$")


def test_logout_expiracion_y_cookie_fijada(app,client,catalogo):
    user,password=tecnico(client,catalogo);tech=login_cliente(app,user["login"],password)
    cookie=tech.get_cookie("session").value
    assert tech.post("/api/auth/logout").status_code==200
    replay=app.test_client();replay.set_cookie("session",cookie)
    assert replay.get("/api/clientes").status_code==401
    tech=login_cliente(app,user["login"],password)
    with Session(app.extensions["db_engine"]) as db:
        for row in db.scalars(select(SesionUsuario).where(SesionUsuario.usuario_id==user["id"])):row.vence_en=ahora()-timedelta(seconds=1)
        db.commit()
    assert tech.get("/api/clientes").status_code==401


def test_no_puede_darse_baja_ultimo_admin(client,usuario_admin):
    assert client.put(f"/api/admin/usuarios/{usuario_admin['id']}",json={"rol":"tecnico","activo":True,"cliente_ids":[]}).status_code==409
    assert client.put(f"/api/admin/usuarios/{usuario_admin['id']}",json={"rol":"admin","activo":False,"cliente_ids":[]}).status_code==409


def test_limite_login_sin_filtrar_usuario(app,usuario_admin):
    anonymous=app.test_client();csrf=anonymous.get("/api/auth/sesion").get_json()["csrf_token"]
    for _ in range(5):
        assert anonymous.post("/api/auth/login",json={"login":usuario_admin["login"],"clave":secrets.token_urlsafe(24)},headers={"X-CSRF-Token":csrf}).status_code==401
    assert anonymous.post("/api/auth/login",json={"login":usuario_admin["login"],"clave":usuario_admin["clave"]},headers={"X-CSRF-Token":csrf}).status_code==429


def test_primer_admin_sin_clave_predeterminada(app):
    browser=app.test_client()
    response=browser.get("/configuracion-inicial")
    assert response.status_code==200
    csrf=browser.get("/api/auth/sesion").get_json()["csrf_token"]
    password=secrets.token_urlsafe(24)
    response=browser.post("/configuracion-inicial",data={"csrf_token":csrf,"login":"jorge.admin","clave":password,"confirmacion":password})
    assert response.status_code==303
    assert browser.get("/api/auth/sesion").get_json()["usuario"]["rol"]=="admin"
    assert browser.get("/configuracion-inicial").status_code==404
    assert password not in response.get_data(as_text=True)
    csrf=browser.get("/api/auth/sesion").get_json()["csrf_token"]
    assert browser.post("/api/auth/logout",headers={"X-CSRF-Token":csrf}).status_code==200
    assert login_cliente(app,"jorge.admin",password).get("/api/auth/sesion").get_json()["usuario"]["rol"]=="admin"


@pytest.mark.parametrize("method",["GET","POST"])
def test_login_sin_usuarios_redirige_a_alta_sin_crear_cuentas(app,method):
    browser=app.test_client()
    csrf=browser.get("/api/auth/sesion").get_json()["csrf_token"]
    response=browser.open("/login",method=method,data={"csrf_token":csrf,"login":"jorge.admin","clave":secrets.token_urlsafe(24)} if method=="POST" else None)
    assert response.status_code==(303 if method=="POST" else 302)
    assert response.headers["Location"]=="/configuracion-inicial"
    with Session(app.extensions["db_engine"]) as db:
        assert list(db.scalars(select(Usuario)))==[]


def test_login_usuario_inexistente_no_reabre_alta_inicial(app,usuario_admin):
    browser=app.test_client()
    csrf=browser.get("/api/auth/sesion").get_json()["csrf_token"]
    response=browser.post("/login",data={"csrf_token":csrf,"login":"jorge.admin","clave":secrets.token_urlsafe(24)})
    assert response.status_code==401
    assert "Usuario o contraseña incorrectos." in response.get_data(as_text=True)
    assert browser.get("/configuracion-inicial").status_code==404
    with Session(app.extensions["db_engine"]) as db:
        assert [u.id for u in db.scalars(select(Usuario))]==[usuario_admin["id"]]


def test_admin_existente_crea_otro_admin_y_permite_login(app,client,usuario_admin):
    with Session(app.extensions["db_engine"]) as db:
        original_hash=bytes(db.get(Usuario,usuario_admin["id"]).clave_hash)
    password=secrets.token_urlsafe(10)
    assert len(password)==14
    response=client.post("/api/admin/usuarios",json={"login":"jorge.admin","nombre":"[Ejemplo] Administración readyproof","rol":"admin","clave":password,"cliente_ids":[]})
    assert response.status_code==201
    browser=login_cliente(app,"jorge.admin",password)
    assert browser.get("/api/auth/sesion").get_json()["usuario"]["rol"]=="admin"
    assert browser.get("/admin").status_code==200
    with Session(app.extensions["db_engine"]) as db:
        assert bytes(db.get(Usuario,usuario_admin["id"]).clave_hash)==original_hash


def test_migracion_conserva_autoria_historica(client,catalogo,datos_api,app):
    row=client.post("/api/cargas",json={"sistema_id":catalogo[1]["id"],"planilla_id":catalogo[2]["id"],"datos":datos_api}).get_json()
    engine=app.extensions["db_engine"]
    with engine.begin() as connection:
        connection.execute(text("ALTER TABLE cargas DROP COLUMN creada_por_id"))
        connection.execute(text("ALTER TABLE revisiones_carga DROP COLUMN actor_id"))
        connection.execute(text("DELETE FROM versiones_esquema WHERE numero=3"))
    crear_esquema(engine)
    with Session(engine) as db:
        assert db.get(VersionEsquema,3)
        assert db.get(Carga,row["id"]).datos==row["datos"]
        assert db.get(Carga,row["id"]).creada_por_id is None
        assert db.scalar(select(RevisionCarga).where(RevisionCarga.carga_id==row["id"])).actor_id is None


def test_auditoria_identifica_lecturas_denegaciones_y_autoria(app,client,catalogo,datos_api,usuario_admin):
    row=client.post("/api/cargas",json={"sistema_id":catalogo[1]["id"],"planilla_id":catalogo[2]["id"],"datos":datos_api}).get_json()
    client.get(f"/api/cargas/{row['id']}")
    with Session(app.extensions["db_engine"]) as db:
        revision=db.scalar(select(RevisionCarga).where(RevisionCarga.carga_id==row["id"]))
        assert revision.actor_id==usuario_admin["id"]
        assert db.get(Carga,row["id"]).creada_por_id==usuario_admin["id"]
        accesses=list(db.scalars(select(RegistroAcceso).where(RegistroAcceso.carga_id==row["id"],RegistroAcceso.metodo=="GET")))
        assert accesses and accesses[0].usuario_id==usuario_admin["id"]
        assert "clave" not in accesses[0].ruta



def test_login_rota_token_y_revoca_cookie_anterior(app,client,usuario_admin):
    old=client.get_cookie("session").value
    response=client.post("/api/auth/login",json={"login":usuario_admin["login"],"clave":usuario_admin["clave"]})
    assert response.status_code==200
    assert client.get_cookie("session").value!=old
    copied=app.test_client();copied.set_cookie("session",old)
    assert copied.get("/api/clientes").status_code==401


def test_asignacion_retirada_revoca_y_restringe(app,client,catalogo):
    user,password=tecnico(client,catalogo);tech=login_cliente(app,user["login"],password)
    assert client.put(f"/api/admin/usuarios/{user['id']}",json={"rol":"tecnico","activo":True,"cliente_ids":[]}).status_code==200
    assert tech.get("/api/clientes").status_code==401
    fresh=login_cliente(app,user["login"],password)
    assert fresh.get("/api/clientes").get_json()==[]
    assert fresh.get(f"/api/clientes/{catalogo[0]['id']}/sistemas").status_code==404


def test_restaurar_clave_admin_y_nombre_de_usuario_unico(app,client,catalogo):
    user,password=tecnico(client,catalogo);tech=login_cliente(app,user["login"],password)
    duplicate=client.post("/api/admin/usuarios",json={"login":user["login"].upper(),"nombre":"[Ejemplo] Duplicado","rol":"tecnico","clave":secrets.token_urlsafe(24),"cliente_ids":[]})
    assert duplicate.status_code==409
    new=secrets.token_urlsafe(24)
    assert client.post(f"/api/admin/usuarios/{user['id']}/clave",json={"nueva":new}).status_code==200
    assert tech.get("/api/clientes").status_code==401
    assert login_cliente(app,user["login"],new).get("/api/clientes").status_code==200
