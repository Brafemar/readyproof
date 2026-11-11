"""Generación local de propuestas sin emisión ni transporte externo."""
from datetime import date
from email.message import EmailMessage
from hashlib import sha256
from io import BytesIO
from uuid import UUID

from flask import Blueprint, abort, current_app, g, render_template, request, send_file
from pypdf.errors import PdfReadError
from sqlalchemy import select, text

from ..auth import csrf_token, exigir_admin
from ..db import sesion
from ..models import Auditoria, Carga, Cliente, FirmaCertificadoActiva, Planilla, Sistema, ahora
from ..planillas.validacion import DatosInvalidos
from ..rutas.api import obtener
from .almacen_firma import MAX_BYTES, directorio_privado, guardar_version, leer_version, validar_png
from .calendario import vencimiento
from .pdf import generar_propuesta

certificados = Blueprint("certificados", __name__)
MAX_PLANILLAS_PROPUESTA = 2


def exigir_propuesta():
    exigir_admin()
    if not g.usuario.certificado_conjunto:
        abort(403, description="La cuenta no tiene permiso de certificado conjunto.")
    if not current_app.config["CERTIFICADO_CONJUNTO_HABILITADO"]:
        abort(409, description="La propuesta de certificado conjunto no está habilitada.")


@certificados.get("/certificados")
def formulario():
    exigir_propuesta()
    db = sesion()
    filas = db.execute(select(Carga.id, Carga.numero_registro, Sistema.designacion,
                              Cliente.id, Cliente.nombre, Planilla.codigo)
        .join(Sistema, Carga.sistema_id == Sistema.id)
        .join(Cliente, Sistema.cliente_id == Cliente.id)
        .join(Planilla, Carga.planilla_id == Planilla.id)
        .where(Carga.estado == "emitida", Carga.pdf.is_not(None), Carga.estado_anulada.is_(False),
               Cliente.es_ejemplo.is_(True), Cliente.nombre.startswith("[Ejemplo] "))
        .order_by(Carga.emitida_en.desc())).all()
    return render_template("certificado_propuesta.html", opciones=filas, csrf=csrf_token(),
                           max_planillas=MAX_PLANILLAS_PROPUESTA)


@certificados.get("/admin/firma-certificado")
def pantalla_firma():
    exigir_admin()
    return render_template("firma_certificado.html", csrf=csrf_token())


def metadatos(firma):
    if firma is None:
        return {"activa": False}
    return {"activa": True, "sha256": firma.sha256, "tamano": firma.tamano,
            "actualizada_en": firma.actualizada_en.isoformat()}


@certificados.post("/api/admin/firma-certificado/estado")
def estado_firma():
    exigir_admin()
    return metadatos(sesion().get(FirmaCertificadoActiva, 1))


@certificados.post("/api/admin/firma-certificado")
def cargar_firma():
    exigir_admin()
    archivos = request.files.getlist("firma")
    if len(archivos) != 1:
        raise DatosInvalidos("Adjuntá un único archivo PNG.")
    datos = validar_png(archivos[0].stream.read(MAX_BYTES + 1))
    db = sesion()
    db.execute(text("SELECT pg_advisory_xact_lock(724023)"))
    activa = db.get(FirmaCertificadoActiva, 1)
    anterior = activa.sha256 if activa else None
    try:
        with directorio_privado(current_app.instance_path, crear=True) as fd:
            nueva = guardar_version(fd, datos)
    except (OSError, ValueError):
        abort(503, description="No se pudo guardar la firma en el directorio privado.")
    fecha = ahora()
    if activa is None:
        activa = FirmaCertificadoActiva(id=1)
        db.add(activa)
    activa.sha256, activa.tamano, activa.actualizada_en = nueva, len(datos), fecha
    db.add(Auditoria(tabla="firma_certificado_activa", registro_id="1", accion="UPDATE" if anterior else "INSERT",
                     usuario_id=g.usuario.id, timestamp=fecha,
                     datos_anterior={"sha256": anterior} if anterior else None,
                     datos_nuevo={"sha256": nueva, "tamano": len(datos), "resultado": "activada",
                                  "operacion": "reemplazo" if anterior else "alta"}))
    db.flush()
    g.evento_auth = "firma_certificado_actualizada"
    return metadatos(activa), 200 if anterior else 201


def firma_propuesta():
    activa = sesion().get(FirmaCertificadoActiva, 1)
    if activa is None:
        return None
    try:
        with directorio_privado(current_app.instance_path) as fd:
            datos = leer_version(fd, activa.sha256)
        return validar_png(datos)
    except (OSError, ValueError):
        abort(503, description="La firma gráfica activa no se puede validar en el almacenamiento privado.")


def dato(nombre, limite, *, obligatorio=True):
    texto = request.form.get(nombre, "").strip()
    if (obligatorio and not texto) or len(texto)>limite or any(ord(c)<32 for c in texto):
        raise DatosInvalidos(f"Revisá el campo {nombre}.")
    return texto


@certificados.post("/api/certificados/propuesta")
def propuesta():
    exigir_propuesta()
    campos_carga = [key for key in request.form if key.startswith("carga_")]
    permitidos = {f"carga_{i}" for i in range(1, MAX_PLANILLAS_PROPUESTA + 1)}
    if any(key not in permitidos or len(request.form.getlist(key)) > 1 for key in campos_carga):
        raise DatosInvalidos(f"La propuesta admite como máximo {MAX_PLANILLAS_PROPUESTA} planillas.")
    if request.form.get("confirmacion") != "si":
        raise DatosInvalidos("Confirmá las periodicidades y el dictamen.")
    try:
        fecha = date.fromisoformat(request.form.get("fecha", ""))
    except ValueError:
        raise DatosInvalidos("Indicá la fecha del certificado.") from None
    filas, cargas, sistemas, referencias = [], [], [], []
    cliente = None
    periodos = []
    for i in range(1, MAX_PLANILLAS_PROPUESTA + 1):
        raw_id = request.form.get(f"carga_{i}")
        if not raw_id:
            if i == 1:
                raise DatosInvalidos("Elegí al menos una planilla emitida.")
            continue
        try:
            cid = str(UUID(raw_id))
            unidad = request.form.get(f"unidad_{i}")
            cantidad = int(request.form.get(f"cantidad_{i}", ""))
            if unidad not in ("dias", "meses"):raise ValueError()
            hasta = vencimiento(fecha, **{unidad:cantidad})
        except (ValueError, OverflowError):
            raise DatosInvalidos("Revisá la planilla y su periodicidad confirmada.") from None
        carga = obtener(Carga, cid)
        if any(c.id == cid for c in cargas):
            raise DatosInvalidos("Una planilla no se puede seleccionar dos veces.")
        if carga.estado!="emitida" or carga.estado_anulada or not carga.pdf or sha256(carga.pdf).hexdigest()!=carga.pdf_sha256:
            raise DatosInvalidos("Elegí una planilla emitida, vigente y con un PDF íntegro.")
        sistema = obtener(Sistema, carga.sistema_id)
        actual = obtener(Cliente, sistema.cliente_id)
        if not actual.es_ejemplo or not actual.nombre.startswith("[Ejemplo] ") or (cliente and cliente.id!=actual.id):
            raise DatosInvalidos("Elegí planillas ficticias del mismo cliente.")
        cliente=actual
        planilla=obtener(Planilla,carga.planilla_id)
        filas.append(dict(sistema=f"{sistema.designacion} · {planilla.codigo}", vencimiento=hasta))
        sistemas.append(sistema.designacion)
        referencias.append(f"{planilla.codigo} / {carga.numero_registro or 's/n'} / R{carga.revision_publica}")
        periodos.append(f"{cantidad} {'día(s)' if unidad=='dias' else 'mes(es)'}")
        cargas.append(carga)
    ficha=dict(fecha=fecha,cliente=cliente.nombre,intervencion=f"{cliente.cuit or 'Sin CUIT'} · {dato('intervencion',50)}",
               establecimiento=dato("establecimiento",120),sistemas=" / ".join(dict.fromkeys(sistemas)),
               periodicidades=" / ".join(periodos),dictamen=dato("dictamen",120),
               observaciones=dato("observaciones",120,obligatorio=False),referencias=" · ".join(referencias),
               informe=dato("informe",90,obligatorio=False) or "No indicado")
    try:
        pdf=generar_propuesta([bytes(c.pdf) for c in cargas], filas, ficha, firma=firma_propuesta())
    except PdfReadError:
        raise DatosInvalidos("No se pudo leer una planilla de respaldo.") from None
    salida=request.form.get("salida","pdf")
    if salida == "correo_prueba":
        mensaje=EmailMessage()
        mensaje["From"]="readyproof@example.invalid"
        mensaje["To"]="certificado@example.invalid"
        mensaje["Subject"]="Propuesta de certificado de inspección · prueba"
        mensaje.set_content("Prueba local. Propuesta no emitida.")
        mensaje.add_attachment(pdf,maintype="application",subtype="pdf",filename="certificado_propuesta.pdf")
        contenido, tipo, nombre=mensaje.as_bytes(),"message/rfc822","certificado_prueba.eml"
    elif salida == "pdf":
        contenido, tipo, nombre=pdf,"application/pdf","certificado_propuesta.pdf"
    else:
        raise DatosInvalidos("Salida de propuesta inválida.")
    g.evento_auth="certificado_propuesta_preparada"
    respuesta=send_file(BytesIO(contenido),mimetype=tipo,as_attachment=True,download_name=nombre)
    respuesta.headers["Cache-Control"]="no-store"
    return respuesta
