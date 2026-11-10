"""Login, cuenta y administración local de usuarios y clientes ficticios."""
from datetime import timedelta
from hashlib import sha256

from flask import Blueprint, abort, g, jsonify, redirect, render_template, request, session
from sqlalchemy import delete, func, select, text

from . import (autorizar_cliente, cerrar_sesion, comprobar_clave, csrf_token, exigir_admin, exigir_usuario,
    hash_clave, iniciar_sesion, normalizar_login, revocar, usuario_json)
from ..db import sesion
from ..models import Auditoria, Cliente, RegistroAcceso, Sistema, Usuario, UsuarioCliente, ahora
from ..planillas.validacion import DatosInvalidos
from ..rutas.api import objeto, obtener
from ..config import SISTEMAS_HABILITADOS
from ..modo import es_piloto

auth = Blueprint("auth", __name__)


def ejemplo_texto(value, maximum=120):
    if not es_piloto():
        from ..planillas.validacion import texto
        result=texto(value,ejemplo=False)
        if len(result)>maximum:raise DatosInvalidos('El nombre supera el largo admitido.')
        return result
    if not isinstance(value,str) or not value.startswith("[Ejemplo] ") or not value[10:].strip() or len(value)>maximum:
        raise DatosInvalidos("Usá un nombre ficticio que comience con [Ejemplo].")
    return value


def autenticar(login, clave):
    normalized = login.lower() if isinstance(login,str) else ""
    fingerprint = sha256(normalized.encode()).hexdigest()
    g.login_huella = fingerprint
    lock = int.from_bytes(bytes.fromhex(fingerprint)[:8], "big", signed=True)
    sesion().execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key":lock})
    count = sesion().scalar(select(func.count()).select_from(RegistroAcceso).where(RegistroAcceso.login_huella==fingerprint, RegistroAcceso.evento=="login_fallido", RegistroAcceso.fecha>ahora()-timedelta(minutes=15)))
    if count >= 5:
        g.evento_auth = "login_bloqueado"
        abort(429,description="Demasiados intentos. Esperá 15 minutos antes de volver a intentar.")
    user = sesion().scalar(select(Usuario).where(Usuario.login==normalized)) if len(normalized)<=80 else None
    valid = comprobar_clave(clave, user.clave_hash if user else None)
    if user is None or not valid or not user.activo:
        g.evento_auth = "login_fallido"
        abort(401,description="Usuario o contraseña incorrectos.")
    iniciar_sesion(user)
    g.evento_auth = "login"
    return user


@auth.get("/api/auth/sesion")
def estado_sesion():
    return jsonify(usuario=usuario_json(g.usuario) if g.usuario else None, csrf_token=csrf_token(), vence_en=g.sesion_usuario.vence_en.isoformat() if g.sesion_usuario else None)


@auth.post("/api/auth/login")
def login_api():
    data=objeto({"login","clave"})
    user=autenticar(data["login"],data["clave"])
    return jsonify(usuario=usuario_json(user),csrf_token=csrf_token(),vence_en=g.sesion_usuario.vence_en.isoformat())


@auth.post("/api/auth/logout")
def logout_api():
    exigir_usuario(); cerrar_sesion();g.evento_auth="logout"
    return jsonify(mensaje="Sesión cerrada.")


@auth.route("/login",methods=["GET","POST"])
def login():
    if sesion().scalar(select(func.count()).select_from(Usuario))==0:
        return redirect("/configuracion-inicial",code=303 if request.method=="POST" else 302)
    if request.method=="POST":
        autenticar(request.form.get("login"),request.form.get("clave"))
        return redirect("/",code=303)
    if g.usuario:return redirect("/")
    return render_template("login.html",csrf=csrf_token())


@auth.route("/configuracion-inicial",methods=["GET","POST"])
def inicial():
    if request.method=="POST":
        sesion().execute(text("SELECT pg_advisory_xact_lock(724004)"))
    if sesion().scalar(select(func.count()).select_from(Usuario))!=0:
        abort(404,description="La configuración inicial ya está cerrada.")
    if request.method=="GET":return render_template("login.html",inicial=True,csrf=csrf_token())
    if request.form.get("clave")!=request.form.get("confirmacion"):
        raise DatosInvalidos("Las contraseñas no coinciden.")
    user=Usuario(login=normalizar_login(request.form.get("login")),nombre="[Ejemplo] Administración",rol="admin",clave_hash=hash_clave(request.form.get("clave")))
    sesion().add(user);sesion().flush();iniciar_sesion(user);g.evento_auth="primer_admin"
    return redirect("/",code=303)


@auth.route("/cuenta",methods=["GET","POST"])
def cuenta():
    if g.usuario is None:return redirect("/login")
    if request.method=="GET":return render_template("cuenta.html",usuario=g.usuario,csrf=csrf_token())
    if not comprobar_clave(request.form.get("actual"),g.usuario.clave_hash):
        abort(401,description="La contraseña actual es incorrecta.")
    if request.form.get("nueva")!=request.form.get("confirmacion"):
        raise DatosInvalidos("Las contraseñas nuevas no coinciden.")
    g.usuario.clave_hash=hash_clave(request.form.get("nueva"));revocar(g.usuario.id);cerrar_sesion();g.evento_auth="clave_cambiada"
    return redirect("/login?cambio=1",code=303)


@auth.post("/api/auth/clave")
def cambiar_clave():
    exigir_usuario();data=objeto({"actual","nueva"})
    if not comprobar_clave(data["actual"],g.usuario.clave_hash):abort(401,description="La contraseña actual es incorrecta.")
    g.usuario.clave_hash=hash_clave(data["nueva"]);revocar(g.usuario.id);cerrar_sesion();g.evento_auth="clave_cambiada"
    return jsonify(mensaje="Contraseña cambiada. Iniciá sesión nuevamente.")


@auth.get("/admin")
def administracion():
    if g.usuario is None:return redirect("/login")
    exigir_admin();return render_template("admin.html",usuario=g.usuario,csrf=csrf_token(),sistemas_habilitados=SISTEMAS_HABILITADOS)


def clientes_asignados(user):
    return list(sesion().scalars(select(UsuarioCliente.cliente_id).where(UsuarioCliente.usuario_id==user.id)))


def vista_usuario(user):
    return dict(usuario_json(user),cliente_ids=clientes_asignados(user))


def validar_asignaciones(ids):
    if not isinstance(ids,list) or len(ids)>200 or any(not isinstance(i,str) for i in ids) or len(set(ids))!=len(ids):
        raise DatosInvalidos("cliente_ids debe ser una lista de identificadores distintos.")
    for key in ids:
        client=obtener(Cliente,key)
        if es_piloto() and not client.es_ejemplo:abort(403,description="Solo se administran clientes ficticios en piloto.")
    return ids


def asignar(user,ids):
    sesion().execute(delete(UsuarioCliente).where(UsuarioCliente.usuario_id==user.id))
    sesion().add_all([UsuarioCliente(usuario_id=user.id,cliente_id=key) for key in ids])


@auth.get("/api/admin/usuarios")
def usuarios():
    exigir_admin();return jsonify([vista_usuario(u) for u in sesion().scalars(select(Usuario).order_by(Usuario.login))])


@auth.post("/api/admin/usuarios")
def crear_usuario():
    exigir_admin();data=objeto({"login","nombre","rol","clave","cliente_ids"})
    if data["rol"] not in ("admin","tecnico"):raise DatosInvalidos("Rol inválido.")
    ids=validar_asignaciones(data["cliente_ids"])
    user=Usuario(login=normalizar_login(data["login"]),nombre=ejemplo_texto(data["nombre"]),rol=data["rol"],clave_hash=hash_clave(data["clave"]))
    sesion().add(user);sesion().flush();asignar(user,ids);g.evento_auth="usuario_creado"
    return jsonify(vista_usuario(user)),201


@auth.put("/api/admin/usuarios/<usuario_id>")
def editar_usuario(usuario_id):
    exigir_admin();data=objeto({"rol","activo","cliente_ids"},{"certificado_conjunto"})
    if "certificado_conjunto" in data and not isinstance(data["certificado_conjunto"], bool):
        raise DatosInvalidos("El permiso de certificado debe ser verdadero o falso.")
    if data["rol"] not in ("admin","tecnico") or not isinstance(data["activo"],bool):raise DatosInvalidos("Rol o estado inválido.")
    sesion().execute(text("SELECT pg_advisory_xact_lock(724004)"))
    user=obtener(Usuario,usuario_id);sesion().refresh(user)
    if user.rol=="admin" and user.activo and (data["rol"]!="admin" or not data["activo"]):
        count=sesion().scalar(select(func.count()).select_from(Usuario).where(Usuario.rol=="admin",Usuario.activo.is_(True)))
        if count<=1:abort(409,description="Debe quedar al menos un administrador activo.")
    ids=validar_asignaciones(data["cliente_ids"])
    permiso = data.get("certificado_conjunto", user.certificado_conjunto)
    if permiso != user.certificado_conjunto:
        sesion().add(Auditoria(tabla="usuarios", registro_id=user.id, accion="UPDATE",
                               usuario_id=g.usuario.id,
                               datos_anterior={"certificado_conjunto": user.certificado_conjunto},
                               datos_nuevo={"certificado_conjunto": permiso}))
        user.certificado_conjunto = permiso
    user.rol=data["rol"];user.activo=data["activo"];asignar(user,ids);revocar(user.id);g.evento_auth="usuario_actualizado"
    return jsonify(vista_usuario(user))


@auth.post("/api/admin/usuarios/<usuario_id>/clave")
def restablecer_clave(usuario_id):
    exigir_admin();data=objeto({"nueva"});user=obtener(Usuario,usuario_id)
    user.clave_hash=hash_clave(data["nueva"]);revocar(user.id);g.evento_auth="clave_restablecida"
    return jsonify(mensaje="Contraseña reemplazada; sesiones del usuario cerradas.")


def cliente_json(cliente):
    return dict(id=cliente.id, nombre=cliente.nombre, es_ejemplo=cliente.es_ejemplo,
                cuit=cliente.cuit, contacto=cliente.contacto or {})


def guardar_datos_cliente(cliente, data):
    nombre = ejemplo_texto(data['nombre'], 200)
    cuit = cliente.cuit
    if 'cuit' in data:
        from ..utils.cuit_validator import normalizar_cuit, validar_cuit
        value = data['cuit']
        if value is None or isinstance(value, str) and not value.strip():
            cuit = None
        else:
            if not validar_cuit(value):
                raise DatosInvalidos('Ingresá un CUIT válido de once dígitos, con o sin guiones.')
            cuit = normalizar_cuit(value)
        if cuit and sesion().scalar(select(Cliente.id).where(Cliente.cuit == cuit, Cliente.id != cliente.id)):
            abort(409, description='El CUIT ya está registrado en otro cliente; revisá el dato.')
    contacto = dict(cliente.contacto or {})
    if 'contacto' in data:
        incoming = data['contacto']
        limits = {'direccion': 500, 'telefono': 120, 'email': 254}
        if not isinstance(incoming, dict) or set(incoming) - set(limits):
            raise DatosInvalidos('El contacto admite dirección, teléfono y correo; revisá los campos enviados.')
        for key, value in incoming.items():
            if not isinstance(value, str) or len(value.strip()) > limits[key]:
                raise DatosInvalidos(f'El campo {key} debe ser texto de hasta {limits[key]} caracteres.')
            value = value.strip()
            if key == 'email' and value:
                from ..correo import direccion
                try: direccion(value)
                except ValueError: raise DatosInvalidos('Ingresá un correo de contacto válido.') from None
            contacto[key] = value
    cliente.nombre, cliente.cuit, cliente.contacto = nombre, cuit, contacto


@auth.get('/api/admin/clientes')
def listar_clientes_admin():
    exigir_admin()
    query = select(Cliente).order_by(Cliente.nombre)
    if es_piloto(): query = query.where(Cliente.es_ejemplo.is_(True))
    return jsonify([cliente_json(c) for c in sesion().scalars(query)])


@auth.get('/api/admin/clientes/<cliente_id>')
def consultar_cliente_admin(cliente_id):
    exigir_admin(); cliente = obtener(Cliente, cliente_id)
    if es_piloto() and not cliente.es_ejemplo: abort(403)
    return jsonify(cliente_json(cliente))


@auth.put('/api/admin/clientes/<cliente_id>')
def editar_cliente(cliente_id):
    exigir_admin(); cliente = obtener(Cliente, cliente_id)
    if es_piloto() and not cliente.es_ejemplo: abort(403)
    data = objeto({'nombre'}, {'cuit', 'contacto'})
    guardar_datos_cliente(cliente, data)
    sesion().flush(); g.evento_auth = 'cliente_editado'; g.acceso_cliente_id = cliente.id
    return jsonify(cliente_json(cliente))


@auth.post("/api/admin/clientes")
def crear_cliente():
    exigir_admin(); data = objeto({'nombre'}, {'cuit', 'contacto'})
    cliente = Cliente(es_ejemplo=es_piloto())
    guardar_datos_cliente(cliente, data)
    cliente.contacto = {key: value for key, value in cliente.contacto.items() if value.strip()}
    sesion().add(cliente); sesion().flush(); g.evento_auth = 'cliente_creado'
    return jsonify(cliente_json(cliente)), 201


@auth.post("/api/admin/clientes/<cliente_id>/sistemas")
def crear_sistema(cliente_id):
    exigir_admin();client=obtener(Cliente,cliente_id);data=objeto({"designacion","tipo"})
    if (es_piloto() and not client.es_ejemplo) or not isinstance(data['tipo'],str) or data['tipo'] not in SISTEMAS_HABILITADOS:raise DatosInvalidos("Seleccioná uno de los 15 sistemas habilitados.")
    system=Sistema(cliente_id=client.id,tipo=data["tipo"],designacion=ejemplo_texto(data["designacion"],200));sesion().add(system);sesion().flush();g.evento_auth="sistema_creado"
    return jsonify(id=system.id,cliente_id=client.id,tipo=system.tipo,designacion=system.designacion),201


@auth.get("/api/admin/accesos")
def accesos():
    exigir_admin()
    return jsonify([{"id":r.id,"usuario_id":r.usuario_id,"fecha":r.fecha.isoformat(),"evento":r.evento,"ruta":r.ruta,"metodo":r.metodo,"estado_http":r.estado_http,"cliente_id":r.cliente_id,"carga_id":r.carga_id,"planilla_codigo":r.planilla_codigo,"destinatario":r.destinatario} for r in sesion().scalars(select(RegistroAcceso).order_by(RegistroAcceso.fecha.desc(),RegistroAcceso.id).limit(200))])
