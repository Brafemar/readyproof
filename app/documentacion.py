"""Documentación de la cuenta por correo, sin contraseñas ni claves de servidor."""
from datetime import timedelta
from email import policy
from email.message import EmailMessage
from email.utils import format_datetime
from hashlib import sha256
from html import escape
import os
from pathlib import Path
import smtplib
import ssl
from uuid import UUID,uuid4

from flask import Blueprint,abort,current_app,g,jsonify,request
from sqlalchemy import select,text

from .auth import exigir_usuario
from .config import RAIZ, SISTEMAS_HABILITADOS
from .correo import direccion
from .db import sesion
from .models import EnvioDocumentacion,ahora
from .planillas.validacion import DatosInvalidos
from .rutas.api import objeto

documentacion=Blueprint('documentacion',__name__)
REMITENTE='readyproof.ar@gmail.com'


def mensaje(usuario,key,destinatario=None):
    mail=EmailMessage(policy=policy.SMTP)
    mail['From']=REMITENTE;mail['To']=direccion(destinatario or usuario.email)
    mail['Subject']='readyproof - Documentación de acceso'
    mail['Date']=format_datetime(ahora());mail['Message-ID']=f'<documentacion-{key}@gmail.com>'
    sistemas=' · '.join(code+': '+name for code,name in SISTEMAS_HABILITADOS.items())
    guide=(f'Hola {usuario.nombre}\n\nTu usuario: {usuario.login}\n'
           'Acceder: http://127.0.0.1:8876/login, con el túnel privado activo en ese equipo.\n\n'
           '1. Cargá una de las 79 planillas: elegí Cliente, Sistema y Planilla; completá y guardá la carga.\n'
           f'{sistemas}.\n'
           '2. Para finalizar se requieren ambas firmas y nombre completo y DNI del responsable de tu empresa; cargo opcional. DNI: de 8 a 15 dígitos, sin puntos ni guiones. Revisá la vista previa y finalizá.\n'
           '3. Descargá y revisá el PDF. En esta instalación usá solo datos y firmas ficticios.\n\n'
           'Se adjuntan la guía de uso y las instrucciones de acceso desde PC y Android.\n'
           'La contraseña no se recupera ni se envía por correo. Cambiala en Mi cuenta.\n'
           'La clave temporal inicial se entrega por un canal privado separado.\n'
           'Soporte: Jorge Sánchez, por el canal interno acordado.\n')
    mail.set_content(guide)
    mail.add_alternative('<html lang="es-AR"><body style="font-family:Arial,Helvetica,sans-serif;color:#1D1D1B"><img src="cid:logo-readyproof" alt="Readyproof" width="176" style="height:auto;max-width:100%">'
                         f'<p>Hola {escape(usuario.nombre)}</p><p>Tu usuario: <strong>{escape(usuario.login)}</strong></p>'
                         '<p>Acceder con el túnel privado activo: <a href="http://127.0.0.1:8876/login">readyproof</a>.</p>'
                         f'<p>{escape(sistemas)}</p>'
                         '<ol><li>Cargá una de las 79 planillas: elegí el sistema y la planilla y completá la carga.</li><li>Se requieren ambas firmas, nombre completo y DNI del responsable de tu empresa. DNI de 8 a 15 dígitos, sin puntos ni guiones; cargo opcional. Revisá la vista previa y finalizá.</li>'
                         '<li>Descargá y revisá el PDF.</li></ol><p>Usá solo datos y firmas ficticios.</p>'
                         '<p>Adjuntamos las guías. La contraseña se cambia en Mi cuenta y no se envía por correo.</p>'
                         '<p>Soporte: Jorge Sánchez, por el canal interno acordado.</p></body></html>',subtype='html')
    mail.get_payload()[1].add_related((RAIZ/'app/static/correo/logo_readyproof_principal.png').read_bytes(),maintype='image',subtype='png',cid='<logo-readyproof>')
    for source,name in [('GUIA_ACCESO_BRAFEMAR.md','readyproof-guia-de-uso.md'),('ACCESO_TECNICO_BRAFEMAR.md','readyproof-acceso-tecnico.md')]:
        body=(RAIZ/'docs'/source).read_text(encoding='utf-8').replace('`tecnico_readyproof`',f'`{usuario.login}`')
        mail.add_attachment(body,subtype='markdown',filename=name)
    return mail


@documentacion.put('/api/usuario/correo')
def guardar_correo():
    exigir_usuario();data=objeto({'email'})
    try:email=direccion(data['email'])
    except ValueError as error:raise DatosInvalidos(str(error)) from None
    g.usuario.email=email;g.evento_auth='correo_usuario_actualizado'
    return jsonify(email=email)


def resultado(row):
    if row.estado in ('enviado','archivado'):
        return jsonify(estado=row.estado,solicitud_id=row.id,message_id=row.message_id,destinatario=row.destinatario)
    return jsonify(estado=row.estado,solicitud_id=row.id,error='El envío no está confirmado. No lo repitas; consultá a Administración.'),409


@documentacion.post('/api/usuario/enviar-documentacion')
def enviar_documentacion():
    exigir_usuario()
    data=objeto(set(),{'destinatario'}) if request.get_data() else {}
    try:destinatario=direccion(data.get('destinatario',g.usuario.email))
    except ValueError:raise DatosInvalidos('Ingresá un destinatario válido o guardá tu correo en Mi cuenta.') from None
    key=request.headers.get('Idempotency-Key') or str(uuid4())
    try:
        if str(UUID(key))!=key:raise ValueError
    except (ValueError,AttributeError):raise DatosInvalidos('Idempotency-Key debe ser un UUID válido.') from None
    db=sesion()
    lock=int.from_bytes(sha256(('documentacion:'+g.usuario.id).encode()).digest()[:8],'big',signed=True)
    db.execute(text('SELECT pg_advisory_xact_lock(:key)'),{'key':lock})
    previous=db.get(EnvioDocumentacion,key)
    if previous:
        if previous.usuario_id!=g.usuario.id:abort(404)
        if previous.destinatario!=destinatario:abort(409,description='Esta solicitud ya pertenece a otro destinatario. No se repite el envío.')
        return resultado(previous)
    recent=db.scalar(select(EnvioDocumentacion).where(EnvioDocumentacion.usuario_id==g.usuario.id,
                     EnvioDocumentacion.creado_en>ahora()-timedelta(minutes=1)).limit(1))
    if recent:abort(429,description='Ya solicitaste documentación hace menos de un minuto. Revisá el resultado anterior antes de repetir.')
    try:mail=mensaje(g.usuario,key,destinatario)
    except (OSError,ValueError):abort(503,description='La documentación no está disponible. Avisá a Administración.')
    row=EnvioDocumentacion(id=key,usuario_id=g.usuario.id,destinatario=destinatario,estado='preparado',
                          message_id=str(mail['Message-ID']),mensaje_eml=mail.as_bytes(),creado_en=ahora())
    db.add(row);db.commit()  # Reserva durable antes de contactar SMTP; no reintenta automáticamente.
    connection=None;data_started=False;accepted=False;failure=False
    try:
        if current_app.config['DOCUMENTACION_MODO_PRUEBA']:
            directory=Path(current_app.config['DIRECTORIO_CORREO'])
            directory.mkdir(parents=True,exist_ok=True,mode=0o700)
            path=directory/f'documentacion-{key}.eml'
            with path.open('xb') as stream:
                os.chmod(path,0o600);stream.write(row.mensaje_eml)
            row.estado='archivado';g.evento_auth='documentacion_prueba'
        else:
            if current_app.config['DOCUMENTACION_TRANSPORTE']=='gmail_api':
                from .gmail_https import obtener_token,enviar_con_token
                token=obtener_token()
                data_started=True;enviar_con_token(mail,token);token=None
            elif current_app.config['DOCUMENTACION_TRANSPORTE']=='smtp':
                if (os.getenv('SMTP_HOST')!='smtp.gmail.com' or os.getenv('SMTP_PORT','587')!='587'
                        or os.getenv('SMTP_USER')!=REMITENTE or not os.getenv('SMTP_PASSWORD')):
                    raise ValueError('Configuración Gmail incompleta.')
                connection=smtplib.SMTP('smtp.gmail.com',587,timeout=30)
                connection.ehlo();connection.starttls(context=ssl.create_default_context());connection.ehlo()
                connection.login(REMITENTE,os.environ['SMTP_PASSWORD'])
                data_started=True
                refused=connection.send_message(mail,from_addr=REMITENTE,to_addrs=[row.destinatario])
                if refused:raise smtplib.SMTPRecipientsRefused(refused)
            else:raise ValueError('Transporte de documentación no configurado.')
            accepted=True;row.estado='enviado';row.enviado_en=ahora();g.evento_auth='documentacion_enviada'
    except (smtplib.SMTPResponseException,smtplib.SMTPRecipientsRefused,ValueError):
        failure=True;row.estado='fallo';g.evento_auth='documentacion_fallo'
    except (OSError,smtplib.SMTPException):
        failure=True;row.estado='indeterminado' if data_started else 'fallo';g.evento_auth='documentacion_fallo'
    finally:
        if connection is not None:
            try:connection.quit()
            except (OSError,smtplib.SMTPException):
                try:connection.close()
                except (OSError,smtplib.SMTPException):pass
    db.commit()
    if failure and not accepted:
        return jsonify(estado=row.estado,solicitud_id=key,error='No se pudo confirmar el correo. Consultá a Administración; no hay reintento automático.'),502
    return resultado(row)
