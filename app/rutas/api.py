"""API de la etapa 2, exclusivamente local y con datos ficticios."""
from copy import deepcopy
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess

from flask import Blueprint, abort, current_app, jsonify, request, send_file
from sqlalchemy import select

from ..catalogo import huella_saa1
from ..db import sesion
from ..models import Cliente, Sistema, Planilla, Carga, RevisionCarga, ahora
from ..planillas.generador import generar_saa1
from ..planillas.pdf import convertir_pdf
from ..planillas.validacion import DatosInvalidos, campos_permitidos, mapa, validar_datos, datos_para_excel

api = Blueprint("api", __name__, url_prefix="/api")


def objeto(required, optional=()):
    data = mapa(request.get_json(), "solicitud")
    campos_permitidos(data, set(required) | set(optional), "solicitud")
    if set(required) - set(data):
        raise DatosInvalidos("La solicitud no contiene todos los campos requeridos.")
    return data


def obtener(model, key):
    value = sesion().get(model, key)
    if value is None:
        abort(404, description="Registro inexistente.")
    return value


def revisar_revision(carga, value):
    if isinstance(value, bool) or not isinstance(value, int):
        raise DatosInvalidos("revision debe ser un entero JSON.")
    if value != carga.revision:
        abort(409, description="La carga cambió; consultar la revisión actual.")


def plantilla_actual(carga):
    planilla = obtener(Planilla, carga.planilla_id)
    if planilla.codigo != "SG-PEM-IFI-SAA-1" or planilla.huella != huella_saa1():
        abort(409, description="La versión de plantilla no coincide con el generador actual.")
    return planilla


def ejemplo_relacionado(carga, datos, *, emitir=False):
    sistema = obtener(Sistema, carga.sistema_id)
    cliente = obtener(Cliente, sistema.cliente_id)
    if not cliente.es_ejemplo or not cliente.nombre.startswith("[Ejemplo] ") or not sistema.designacion.startswith("[Ejemplo] "):
        abort(403, description="M1: la emisión y carga de clientes reales está bloqueada; solo se admiten ejemplos.")
    name = datos.get("cabecera", {}).get("cliente")
    if name is not None and name != cliente.nombre:
        raise DatosInvalidos("El cliente de la cabecera debe coincidir con el cliente del sistema.")
    if emitir and name != cliente.nombre:
        raise DatosInvalidos("La emisión de ejemplo requiere identificar al cliente ficticio en la cabecera.")


def registrar(carga, evento):
    carga.actualizada_en = ahora()
    sesion().flush()
    sesion().add(RevisionCarga(carga_id=carga.id, numero=carga.revision, evento=evento, datos=deepcopy(carga.datos)))
    sesion().commit()


def serializar(carga):
    planilla = obtener(Planilla, carga.planilla_id)
    return {"id": carga.id, "sistema_id": carga.sistema_id, "planilla_id": carga.planilla_id,
            "version_plantilla": planilla.version, "huella_plantilla": planilla.huella,
            "estado": carga.estado, "revision": carga.revision, "datos": carga.datos,
            "creada_en": carga.creada_en.isoformat(), "actualizada_en": carga.actualizada_en.isoformat(),
            "pdf_disponible": carga.pdf is not None, "pdf_sha256": carga.pdf_sha256}


@api.get("/clientes")
def clientes():
    return jsonify([{ "id": c.id, "nombre": c.nombre, "es_ejemplo": c.es_ejemplo } for c in sesion().scalars(select(Cliente).where(Cliente.es_ejemplo.is_(True), Cliente.nombre.startswith("[Ejemplo] ")).order_by(Cliente.nombre))])


@api.get("/clientes/<cliente_id>/sistemas")
def sistemas(cliente_id):
    cliente = obtener(Cliente, cliente_id)
    if not cliente.es_ejemplo or not cliente.nombre.startswith("[Ejemplo] "):
        abort(403, description="Solo se admiten clientes ficticios en esta etapa.")
    return jsonify([{ "id": s.id, "cliente_id": s.cliente_id, "tipo": s.tipo, "designacion": s.designacion } for s in sesion().scalars(select(Sistema).where(Sistema.cliente_id == cliente_id, Sistema.designacion.startswith("[Ejemplo] ")).order_by(Sistema.designacion))])


@api.get("/planillas")
def planillas():
    return jsonify([{ "id": p.id, "codigo": p.codigo, "version": p.version, "sistema_tipo": p.sistema_tipo, "huella": p.huella } for p in sesion().scalars(select(Planilla).order_by(Planilla.codigo))])


@api.get("/planillas/<planilla_id>")
def definicion(planilla_id):
    p = obtener(Planilla, planilla_id)
    return jsonify(id=p.id, codigo=p.codigo, version=p.version, huella=p.huella, definicion=p.definicion)


@api.post("/cargas")
def crear_carga():
    data = objeto({"sistema_id", "planilla_id", "datos"})
    for key in ("sistema_id", "planilla_id"):
        if not isinstance(data[key], str):
            raise DatosInvalidos(f"{key} debe ser texto.")
    sistema = obtener(Sistema, data["sistema_id"])
    planilla = obtener(Planilla, data["planilla_id"])
    if sistema.tipo != planilla.sistema_tipo:
        raise DatosInvalidos("El tipo de sistema no coincide con la planilla.")
    carga = Carga(sistema_id=sistema.id, planilla_id=planilla.id, datos=validar_datos(data["datos"], planilla.definicion))
    plantilla_actual(carga)
    ejemplo_relacionado(carga, carga.datos)
    sesion().add(carga)
    registrar(carga, "creada")
    return jsonify(serializar(carga)), 201


@api.get("/cargas/<carga_id>")
def consultar_carga(carga_id):
    carga = obtener(Carga, carga_id)
    ejemplo_relacionado(carga, carga.datos)
    return jsonify(serializar(carga))


@api.put("/cargas/<carga_id>/borrador")
def guardar_borrador(carga_id):
    data = objeto({"revision", "datos"})
    carga = obtener(Carga, carga_id)
    revisar_revision(carga, data["revision"])
    if carga.estado != "borrador":
        abort(409, description="Una carga finalizada o emitida no admite edición.")
    planilla = plantilla_actual(carga)
    datos = validar_datos(data["datos"], planilla.definicion)
    ejemplo_relacionado(carga, datos)
    carga.datos = datos
    registrar(carga, "borrador_guardado")
    return jsonify(serializar(carga))


@api.post("/cargas/<carga_id>/finalizar")
def finalizar(carga_id):
    data = objeto({"revision"})
    carga = obtener(Carga, carga_id)
    revisar_revision(carga, data["revision"])
    if carga.estado != "borrador":
        abort(409, description="Solo se finalizan borradores.")
    planilla = plantilla_actual(carga)
    validated = validar_datos(carga.datos, planilla.definicion)
    if not validated["cabecera"] and not any(validated["bloques"].values()) and not validated["observaciones"]:
        raise DatosInvalidos("No se puede finalizar una carga vacía.")
    ejemplo_relacionado(carga, validated)
    carga.estado = "finalizada"
    carga.finalizada_en = ahora()
    registrar(carga, "finalizada")
    return jsonify(serializar(carga))


@api.post("/cargas/<carga_id>/emitir")
def emitir(carga_id):
    data = objeto({"revision"})
    carga = obtener(Carga, carga_id)
    revisar_revision(carga, data["revision"])
    if carga.estado != "finalizada":
        abort(409, description="Solo se emiten cargas finalizadas.")
    planilla = plantilla_actual(carga)
    datos = validar_datos(carga.datos, planilla.definicion)
    ejemplo_relacionado(carga, datos, emitir=True)
    temporary = Path(current_app.config["DIRECTORIO_TEMPORAL"])
    temporary.mkdir(parents=True, exist_ok=True)
    try:
        with TemporaryDirectory(prefix="emision-", dir=temporary) as directory:
            source = generar_saa1(datos_para_excel(datos), Path(directory) / "planilla.xlsx")
            result = convertir_pdf(source, Path(directory) / "planilla.pdf")
            payload = result.read_bytes()
    except (RuntimeError, OSError, subprocess.TimeoutExpired):
        sesion().rollback()
        return jsonify(error="No se pudo generar el PDF; la carga continúa finalizada."), 503
    carga.pdf = payload
    carga.pdf_sha256 = sha256(payload).hexdigest()
    carga.emitida_en = ahora()
    carga.estado = "emitida"
    registrar(carga, "emitida")
    return jsonify(serializar(carga)), 201


@api.get("/cargas/<carga_id>/pdf")
def descargar(carga_id):
    carga = obtener(Carga, carga_id)
    if carga.estado != "emitida" or carga.pdf is None:
        abort(409, description="La carga todavía no tiene un PDF emitido.")
    validar_datos(carga.datos, obtener(Planilla, carga.planilla_id).definicion)
    ejemplo_relacionado(carga, carga.datos, emitir=True)
    response = send_file(BytesIO(carga.pdf), mimetype="application/pdf", as_attachment=True, download_name=f"SAA-1_{carga.id}.pdf", etag=carga.pdf_sha256, max_age=0)
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@api.get("/cargas/<carga_id>/revisiones")
def revisiones(carga_id):
    carga = obtener(Carga, carga_id)
    ejemplo_relacionado(carga, carga.datos)
    return jsonify([{ "numero": r.numero, "evento": r.evento, "datos": r.datos, "actor": r.actor, "fecha": r.fecha.isoformat() } for r in sesion().scalars(select(RevisionCarga).where(RevisionCarga.carga_id == carga_id).order_by(RevisionCarga.numero))])
