"""Generación local de propuestas sin emisión ni transporte externo."""
from base64 import b64encode
from datetime import date
from email.message import EmailMessage
from hashlib import sha256
from io import BytesIO
from uuid import UUID

from flask import Blueprint, abort, g, render_template, request, send_file
from pypdf.errors import PdfReadError
from sqlalchemy import select

from ..auth import csrf_token, exigir_usuario, permitido
from ..db import sesion
from ..models import Carga, Cliente, Planilla, Sistema
from ..modo import es_piloto
from ..planillas.firmas import validar_firmas
from ..planillas.validacion import DatosInvalidos
from ..rutas.api import obtener
from .calendario import vencimiento
from .pdf import generar_propuesta

certificados = Blueprint("certificados", __name__)


def exigir_propuesta():
    exigir_usuario()
    if not g.usuario.certificado_conjunto:
        abort(403, description="La cuenta no tiene permiso de certificado conjunto.")
    if not es_piloto():
        abort(409, description="La emisión del certificado sigue pendiente de aprobación.")


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
    opciones = [r for r in filas if permitido(r[3])]
    return render_template("certificado_propuesta.html", opciones=opciones, csrf=csrf_token())


def dato(nombre, limite, *, obligatorio=True):
    texto = request.form.get(nombre, "").strip()
    if (obligatorio and not texto) or len(texto)>limite or any(ord(c)<32 for c in texto):
        raise DatosInvalidos(f"Revisá el campo {nombre}.")
    return texto


@certificados.post("/api/certificados/propuesta")
def propuesta():
    exigir_propuesta()
    if request.form.get("confirmacion") != "si":
        raise DatosInvalidos("Confirmá las periodicidades y el dictamen.")
    try:
        fecha = date.fromisoformat(request.form.get("fecha", ""))
    except ValueError:
        raise DatosInvalidos("Indicá la fecha del certificado.") from None
    filas, cargas, sistemas, referencias = [], [], [], []
    cliente = None
    periodos = []
    for i in (1, 2):
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
    subida=request.files.get("firma")
    raw=subida.stream.read(200001) if subida else b""
    if not raw or len(raw)>200000:
        raise DatosInvalidos("Adjuntá una firma gráfica ficticia PNG de hasta 200 KB.")
    firma=validar_firmas({"tecnico":"data:image/png;base64,"+b64encode(raw).decode("ascii")})["tecnico"]
    ficha=dict(fecha=fecha,cliente=cliente.nombre,intervencion=f"{cliente.cuit or 'Sin CUIT'} · {dato('intervencion',50)}",
               establecimiento=dato("establecimiento",120),sistemas=" / ".join(dict.fromkeys(sistemas)),
               periodicidades=" / ".join(periodos),dictamen=dato("dictamen",120),
               observaciones=dato("observaciones",120,obligatorio=False),referencias=" · ".join(referencias),
               informe=dato("informe",90,obligatorio=False) or "No indicado",firmante=g.usuario.nombre)
    try:
        pdf=generar_propuesta([bytes(c.pdf) for c in cargas], filas, ficha, firma)
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
