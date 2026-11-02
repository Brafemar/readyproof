"""API de la etapa 2, exclusivamente local y con datos ficticios."""
from copy import deepcopy
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess
from uuid import UUID

from flask import Blueprint, abort, current_app, g, jsonify, request, send_file
from sqlalchemy import select, or_

from ..catalogo import huella_saa1
from ..carga_planillas import CODIGOS, VERSION_CATALOGO
from ..db import sesion
from ..models import Cliente, Sistema, Planilla, Carga, RevisionCarga, FirmaCarga, UsuarioCliente, RegistroAcceso, EmisionCarga, ahora
from ..carga.servicios import desbloquear_carga, preparar_numero_emision, archivar_emision, snapshot_carga, registrar_auditoria
from ..auth import autorizar_cliente
from ..planillas.generador import generar_saa1, generar_multisistema
from ..planillas.multisistema import ejemplo_multisistema
from ..planillas.catalogo_completo import definiciones_habilitadas as definiciones_multisistema
from ..planillas.pdf import convertir_pdf
from ..planillas.firmas import validar_firmas, ROLES
from ..planillas.firmantes import validar_responsable, CAMPOS
from ..planillas.validacion import DatosInvalidos, campos_permitidos, mapa, validar_datos, datos_para_excel
from ..modo import es_piloto, validar_emision_modo

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
    if model is Cliente:
        autorizar_cliente(value.id)
    elif model is Sistema:
        autorizar_cliente(value.cliente_id)
    elif model is Carga:
        sistema = sesion().get(Sistema, value.sistema_id)
        autorizar_cliente(sistema.cliente_id)
        g.acceso_carga_id = value.id
    return value


def revisar_revision(carga, value):
    if isinstance(value, bool) or not isinstance(value, int):
        raise DatosInvalidos("revision debe ser un entero JSON.")
    if value != carga.revision:
        abort(409, description="La carga cambió; consultar la revisión actual.")


def plantilla_actual(carga):
    planilla = obtener(Planilla, carga.planilla_id)
    definition=definiciones_multisistema().get(planilla.codigo)
    vigente=(planilla.codigo=="SG-PEM-IFI-SAA-1" and planilla.huella==huella_saa1()) or (definition is not None and planilla.version==definition['version'] and planilla.huella==definition['huella'] and planilla.definicion==definition['definicion'])
    if not vigente:
        abort(409, description="La versión de plantilla no coincide con el generador actual.")
    return planilla


def ejemplo_relacionado(carga, datos, *, emitir=False, historico=False):
    sistema = obtener(Sistema, carga.sistema_id)
    cliente = obtener(Cliente, sistema.cliente_id)
    if es_piloto() and (not cliente.es_ejemplo or not cliente.nombre.startswith("[Ejemplo] ") or not sistema.designacion.startswith("[Ejemplo] ")):
        abort(403, description="El uso real no está habilitado; solo se admiten clientes y datos de ejemplo.")
    if not es_piloto() and cliente.es_ejemplo and not historico:
        abort(403, description='En modo REAL usá un cliente real; las cargas del piloto se conservan como históricas.')
    name = datos.get("cabecera", {}).get("cliente")
    if name is not None and name != cliente.nombre:
        raise DatosInvalidos("El cliente de la cabecera debe coincidir con el cliente del sistema.")
    if emitir and name != cliente.nombre:
        raise DatosInvalidos("La emisión requiere identificar al cliente del sistema en la cabecera.")
    if emitir and not historico:validar_emision_modo(datos)


def firmas_guardadas(carga):
    row = sesion().get(FirmaCarga, carga.id) if carga.id else None
    return {role: getattr(row, role + "_png") if row else None for role in ROLES}


def guardar_firmas(carga, cambios):
    if cambios is None:
        return
    row = sesion().get(FirmaCarga, carga.id)
    if row is None:
        row = FirmaCarga(carga_id=carga.id)
        sesion().add(row)
    for role, value in cambios.items():
        if role == 'tecnico' and (value != row.tecnico_png or (value and not row.tecnico_usuario_id)):
            row.tecnico_usuario_id = g.usuario.id if value else None
            row.tecnico_nombre = g.usuario.nombre if value else None
            row.tecnico_login = g.usuario.login if value else None
        setattr(row, role + "_png", value)


def responsable_guardado(carga):
    row = sesion().get(FirmaCarga, carga.id) if carga.id else None
    return {key: (getattr(row, key) or '') if row else '' for key in CAMPOS}


def guardar_responsable(carga, value):
    if value is None:
        return
    row = sesion().get(FirmaCarga, carga.id)
    if row is None:
        row = FirmaCarga(carga_id=carga.id)
        sesion().add(row)
    for key, text in value.items():
        setattr(row, key, text or None)


def firmantes_guardados(carga):
    row = sesion().get(FirmaCarga, carga.id) if carga.id else None
    return dict(responsable=responsable_guardado(carga), tecnico=dict(
        usuario_id=row.tecnico_usuario_id if row else None,
        nombre=row.tecnico_nombre if row else None, login=row.tecnico_login if row else None))


def exigir_firmantes(carga):
    if not all(firmas_guardadas(carga).values()):
        raise DatosInvalidos('Se requieren las firmas del técnico y del responsable para finalizar.')
    validar_responsable(responsable_guardado(carga), completo=True)
    if not firmantes_guardados(carga)['tecnico']['usuario_id']:
        raise DatosInvalidos('Volvé a firmar como técnico en un borrador para registrar tu identidad.')


def registrar(carga, evento, anterior=None):
    if evento != "creada":
        carga.actualizada_en = ahora()
    sesion().flush()
    snapshot_firmantes = firmantes_guardados(carga)
    if evento == 'desbloqueada':
        snapshot_firmantes['desbloqueo'] = dict(motivo=carga.motivo_desbloqueo,
            numero_registro=carga.numero_registro, revision_publica=carga.revision_publica)
    sesion().add(RevisionCarga(carga_id=carga.id, numero=carga.revision, evento=evento, datos=deepcopy(carga.datos), actor_id=g.usuario.id, actor=g.usuario.login, firmas_huellas={role: sha256(value).hexdigest() if value else None for role, value in firmas_guardadas(carga).items()}, firmantes=snapshot_firmantes))
    if evento == "emitida":
        sistema = obtener(Sistema, carga.sistema_id)
        sesion().add(RegistroAcceso(usuario_id=g.usuario.id, evento="emision", ruta=request.url_rule.rule,
            metodo=request.method, estado_http=201, cliente_id=sistema.cliente_id, carga_id=carga.id,
            planilla_codigo=obtener(Planilla,carga.planilla_id).codigo, destinatario=None))
    registrar_auditoria('carga', carga.id, 'INSERT' if evento == 'creada' else 'DESBLOQUEO' if evento == 'desbloqueada' else 'UPDATE',
        g.usuario.id, anterior, snapshot_carga(carga), motivo=carga.motivo_desbloqueo if evento == 'desbloqueada' else None)
    sesion().commit()


def serializar(carga):
    planilla = obtener(Planilla, carga.planilla_id)
    return {"id": carga.id, "sistema_id": carga.sistema_id, "planilla_id": carga.planilla_id,
            "version_plantilla": planilla.version, "huella_plantilla": planilla.huella,
            "estado": carga.estado, "revision": carga.revision, "datos": carga.datos,
            "numero_registro": carga.numero_registro, "revision_publica": carga.revision_publica,
            "puede_desbloquear": carga.estado == 'emitida' and not carga.estado_anulada and (g.usuario.rol == 'admin' or carga.creada_por_id == g.usuario.id),
            "creada_en": carga.creada_en.isoformat(), "actualizada_en": carga.actualizada_en.isoformat(),
            "firmas": {role: bool(value) for role, value in firmas_guardadas(carga).items()},
            "responsable": responsable_guardado(carga), "firmantes": firmantes_guardados(carga),
            "pdf_disponible": carga.pdf is not None, "pdf_sha256": carga.pdf_sha256}


@api.get("/clientes")
def clientes():
    query = select(Cliente).where(or_(not es_piloto(), Cliente.es_ejemplo.is_(True) & Cliente.nombre.startswith("[Ejemplo] "))).order_by(Cliente.nombre)
    if g.usuario.rol != "admin":
        query = query.join(UsuarioCliente,UsuarioCliente.cliente_id==Cliente.id).where(UsuarioCliente.usuario_id==g.usuario.id)
    return jsonify([{ "id":c.id,"nombre":c.nombre,"es_ejemplo":c.es_ejemplo } for c in sesion().scalars(query)])


@api.get("/clientes/<cliente_id>/sistemas")
def sistemas(cliente_id):
    cliente = obtener(Cliente, cliente_id)
    if es_piloto() and (not cliente.es_ejemplo or not cliente.nombre.startswith("[Ejemplo] ")):
        abort(403, description="Solo se admiten clientes ficticios en esta etapa.")
    return jsonify([{ "id": s.id, "cliente_id": s.cliente_id, "tipo": s.tipo, "designacion": s.designacion } for s in sesion().scalars(select(Sistema).where(Sistema.cliente_id == cliente_id, Sistema.activo.is_(True), or_(not es_piloto(), Sistema.designacion.startswith("[Ejemplo] "))).order_by(Sistema.designacion))])


@api.get("/planillas")
def planillas():
    definitions=definiciones_multisistema()
    offered=[]
    for p in sesion().scalars(select(Planilla).order_by(Planilla.codigo,Planilla.version)):
        definition=definitions.get(p.codigo)
        if (p.codigo=="SG-PEM-IFI-SAA-1" and p.huella==huella_saa1()) or (definition and p.version==definition['version'] and p.huella==definition['huella']):
            offered.append(dict(id=p.id,codigo=p.codigo,version=p.version,sistema_tipo=p.sistema_tipo,huella=p.huella,
                                nombre=definition['nombre'] if definition else "Información general",familia=p.sistema_tipo))
    return jsonify(offered)


@api.get("/planillas/<planilla_id>")
def definicion(planilla_id):
    p = obtener(Planilla, planilla_id)
    payload=dict(id=p.id,codigo=p.codigo,version=p.version,huella=p.huella,definicion=p.definicion)
    if p.codigo in definiciones_multisistema():payload['ejemplo']=ejemplo_multisistema(p.definicion)
    return jsonify(payload)


@api.post("/cargas")
def crear_carga():
    data = objeto({"sistema_id", "planilla_id", "datos"}, {"firmas", "responsable"})
    firmas = validar_firmas(data["firmas"]) if "firmas" in data else None
    responsable = validar_responsable(data['responsable']) if 'responsable' in data else None
    local_key = request.headers.get("Idempotency-Key")
    if local_key:
        try:
            if str(UUID(local_key)) != local_key:
                raise ValueError
        except ValueError:
            raise DatosInvalidos("Idempotency-Key debe ser un UUID canónico.") from None
        existing = sesion().get(Carga, local_key)
        if existing:
            existing = obtener(Carga, existing.id)
            ejemplo_relacionado(existing, existing.datos)
            if existing.sistema_id != data["sistema_id"] or existing.planilla_id != data["planilla_id"]:
                abort(409, description="El identificador local pertenece a otra carga.")
            return jsonify(serializar(existing)), 200
    for key in ("sistema_id", "planilla_id"):
        if not isinstance(data[key], str):
            raise DatosInvalidos(f"{key} debe ser texto.")
    sistema = obtener(Sistema, data["sistema_id"])
    planilla = obtener(Planilla, data["planilla_id"])
    if sistema.tipo != planilla.sistema_tipo:
        raise DatosInvalidos("El tipo de sistema no coincide con la planilla.")
    carga = Carga(creada_por_id=g.usuario.id, sistema_id=sistema.id, planilla_id=planilla.id, datos=validar_datos(data["datos"], planilla.definicion))
    plantilla_actual(carga)
    ejemplo_relacionado(carga, carga.datos)
    if local_key:
        carga.id = local_key
    sesion().add(carga)
    sesion().flush()
    guardar_firmas(carga, firmas)
    guardar_responsable(carga, responsable)
    registrar(carga, "creada")
    return jsonify(serializar(carga)), 201


@api.get("/cargas/<carga_id>")
def consultar_carga(carga_id):
    carga = obtener(Carga, carga_id)
    ejemplo_relacionado(carga, carga.datos, historico=True)
    return jsonify(serializar(carga))


@api.put("/cargas/<carga_id>/borrador")
def guardar_borrador(carga_id):
    data = objeto({"revision", "datos"}, {"firmas", "responsable"})
    firmas = validar_firmas(data["firmas"]) if "firmas" in data else None
    responsable = validar_responsable(data['responsable']) if 'responsable' in data else None
    carga = obtener(Carga, carga_id)
    anterior = snapshot_carga(carga)
    revisar_revision(carga, data["revision"])
    if carga.estado != "borrador":
        abort(409, description="Una carga finalizada o emitida no admite edición.")
    planilla = plantilla_actual(carga)
    datos = validar_datos(data["datos"], planilla.definicion)
    ejemplo_relacionado(carga, datos)
    carga.datos = datos
    guardar_firmas(carga, firmas)
    guardar_responsable(carga, responsable)
    registrar(carga, "borrador_guardado", anterior)
    return jsonify(serializar(carga))


@api.post("/cargas/<carga_id>/finalizar")
def finalizar(carga_id):
    data = objeto({"revision"})
    carga = obtener(Carga, carga_id)
    anterior = snapshot_carga(carga)
    revisar_revision(carga, data["revision"])
    if carga.estado != "borrador":
        abort(409, description="Solo se finalizan borradores.")
    planilla = plantilla_actual(carga)
    validated = validar_datos(carga.datos, planilla.definicion, completo=True)
    if not validated["cabecera"] and not any(validated["bloques"].values()) and not validated["observaciones"]:
        raise DatosInvalidos("No se puede finalizar una carga vacía.")
    ejemplo_relacionado(carga, validated)
    exigir_firmantes(carga)
    carga.estado = "finalizada"
    carga.finalizada_en = ahora()
    registrar(carga, "finalizada", anterior)
    return jsonify(serializar(carga))


@api.post("/cargas/<carga_id>/emitir")
def emitir(carga_id):
    data = objeto({"revision"})
    carga = obtener(Carga, carga_id)
    anterior = snapshot_carga(carga)
    revisar_revision(carga, data["revision"])
    if carga.estado != "finalizada":
        abort(409, description="Solo se emiten cargas finalizadas.")
    planilla = plantilla_actual(carga)
    datos = validar_datos(carga.datos, planilla.definicion, completo=True)
    ejemplo_relacionado(carga, datos, emitir=True)
    exigir_firmantes(carga)
    try:
        with sesion().no_autoflush:
            preparar_numero_emision(carga)
            payload = generar_pdf_carga(carga, datos)
            carga.pdf = payload
            carga.pdf_sha256 = sha256(payload).hexdigest()
            carga.pdf_hash = carga.pdf_sha256
            carga.emitida_en = ahora()
            carga.estado = "emitida"
            snapshot = archivar_emision(carga, firmantes_guardados(carga))
            snapshot.actor_id = g.usuario.id
    except (RuntimeError, OSError, subprocess.TimeoutExpired):
        sesion().rollback()
        return jsonify(error="No se pudo generar el PDF; la carga continúa finalizada."), 503
    except Exception:
        sesion().rollback()
        raise
    registrar(carga, "emitida", anterior)
    return jsonify(serializar(carga)), 201


@api.post('/cargas/<carga_id>/desbloquear')
def desbloquear(carga_id):
    data = objeto({'revision', 'motivo'})
    carga = obtener(Carga, carga_id)
    anterior = snapshot_carga(carga)
    plantilla_actual(carga)
    ejemplo_relacionado(carga, carga.datos)
    with sesion().no_autoflush:
        carga = desbloquear_carga(carga_id, g.usuario.id, data['motivo'],
            revision=data['revision'], firmantes=firmantes_guardados(carga))
    registrar(carga, 'desbloqueada', anterior)
    return jsonify(serializar(carga))


@api.get('/cargas/<carga_id>/emisiones')
def emisiones(carga_id):
    carga = obtener(Carga, carga_id)
    rows = list(sesion().scalars(select(EmisionCarga).where(EmisionCarga.carga_id == carga.id).order_by(EmisionCarga.revision_publica)))
    return jsonify([dict(revision_publica=row.revision_publica, numero_registro=row.numero_registro,
        pdf_sha256=row.pdf_sha256, emitida_en=row.emitida_en.isoformat() if row.emitida_en else None,
        url=f'/api/cargas/{carga.id}/emisiones/{row.revision_publica}/pdf') for row in rows])


@api.get('/cargas/<carga_id>/emisiones/<int:revision_publica>/pdf')
def descargar_emision(carga_id, revision_publica):
    carga = obtener(Carga, carga_id)
    row = sesion().scalar(select(EmisionCarga).where(EmisionCarga.carga_id == carga.id,
        EmisionCarga.revision_publica == revision_publica))
    if row is None:
        abort(404)
    response = send_file(BytesIO(row.pdf), mimetype='application/pdf', as_attachment=True,
        download_name=f'readyproof_{carga.id}_revision_{revision_publica}.pdf', etag=row.pdf_sha256, max_age=0)
    response.headers['Cache-Control'] = 'no-store'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    return response


@api.get("/cargas/<carga_id>/pdf")
def descargar(carga_id):
    carga = obtener(Carga, carga_id)
    if carga.estado != "emitida" or carga.pdf is None:
        abort(409, description="La carga todavía no tiene un PDF emitido.")
    validar_datos(carga.datos, obtener(Planilla, carga.planilla_id).definicion)
    ejemplo_relacionado(carga, carga.datos, emitir=True, historico=True)
    response = send_file(BytesIO(carga.pdf), mimetype="application/pdf", as_attachment=True, download_name=f"{obtener(Planilla,carga.planilla_id).codigo.removeprefix('SG-PEM-IFI-')}_{carga.id}.pdf", etag=carga.pdf_sha256, max_age=0)
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@api.get("/cargas/<carga_id>/revisiones")
def revisiones(carga_id):
    carga = obtener(Carga, carga_id)
    ejemplo_relacionado(carga, carga.datos)
    return jsonify([{ "numero": r.numero, "evento": r.evento, "datos": r.datos, "actor": r.actor, "actor_id": r.actor_id, "firmas_huellas": r.firmas_huellas, "firmantes": r.firmantes, "fecha": r.fecha.isoformat() } for r in sesion().scalars(select(RevisionCarga).where(RevisionCarga.carga_id == carga_id).order_by(RevisionCarga.numero))])



def generar_pdf_carga(carga, datos):
    temporary = Path(current_app.config["DIRECTORIO_TEMPORAL"])
    temporary.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="emision-", dir=temporary) as directory:
        planilla=obtener(Planilla,carga.planilla_id)
        source=(generar_saa1(datos_para_excel(datos),Path(directory)/"planilla.xlsx") if planilla.codigo=="SG-PEM-IFI-SAA-1"
                else generar_multisistema(datos,Path(directory)/"planilla.xlsx",planilla.codigo))
        identidad=firmantes_guardados(carga)
        identidad.update(empresa=obtener(Cliente, obtener(Sistema,carga.sistema_id).cliente_id).nombre,
                         fecha=datos.get('cabecera',{}).get('fecha',carga.creada_en.date().isoformat()))
        if not es_piloto():identidad['empresa_mantenedora']=current_app.config['EMPRESA_MANTENEDORA']
        result = convertir_pdf(source, Path(directory) / "planilla.pdf", firmas=firmas_guardadas(carga), firmantes=identidad)
        payload = result.read_bytes()
        from ..fotos.emision import incorporar_fotos_carga
        payload = incorporar_fotos_carga(payload, carga, datos, sesion())
        if carga.numero_registro is not None:
            from ..planillas.registro_pdf import incorporar_registro
            payload = incorporar_registro(payload, carga.numero_registro, carga.revision_publica)
        from ..planillas.registro_pdf import incorporar_modo
        payload = incorporar_modo(payload, 'PILOTO' if es_piloto() else 'REAL')
        from ..fotos.anexo_pdf import numerar_pdf
        return numerar_pdf(payload)


@api.post("/cargas/<carga_id>/vista-previa")
def vista_previa(carga_id):
    data = objeto({"revision"})
    carga = obtener(Carga, carga_id)
    revisar_revision(carga, data["revision"])
    planilla = plantilla_actual(carga)
    datos = validar_datos(carga.datos, planilla.definicion, completo=True)
    ejemplo_relacionado(carga, datos, emitir=True)
    try:
        payload = generar_pdf_carga(carga, datos)
    except (RuntimeError, OSError, subprocess.TimeoutExpired):
        sesion().rollback()
        return jsonify(error="No se pudo generar la vista previa."), 503
    response = send_file(BytesIO(payload), mimetype="application/pdf", as_attachment=False, download_name=planilla.codigo.removeprefix("SG-PEM-IFI-")+"_vista_previa.pdf", max_age=0)
    response.headers["Cache-Control"] = "no-store"
    return response
