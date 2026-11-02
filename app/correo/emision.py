"""Presentación de correos a partir de la copia de la emisión."""
from datetime import datetime
from hashlib import sha256
import re
import unicodedata
from zoneinfo import ZoneInfo

from flask import current_app
from jinja2 import StrictUndefined
from sqlalchemy import func, select

from ..models import EmisionCarga, FirmaCarga, Planilla
from ..models.fotos import FotoCarga
from ..modo import es_piloto


def componente_archivo(value, limite=100):
    text=unicodedata.normalize('NFKD',str(value)).encode('ascii','ignore').decode()
    return re.sub(r'[^A-Za-z0-9._-]+','_',text).strip('._-')[:limite] or 'cliente'


def renderizar_emision(contexto):
    from . import direccion
    data=dict(contexto)
    for key,value in data.items():
        if isinstance(value,str):
            data[key]=' '.join((value if es_piloto() else value.replace('[Ejemplo]','')).split())
    phone=current_app.config.get('CONTACTO_TELEFONO','').strip()
    mail=current_app.config.get('CONTACTO_CORREO','').strip()
    if not phone or not mail:
        raise ValueError('Configurar CONTACTO_TELEFONO y CONTACTO_CORREO antes de preparar el correo de emisión.')
    if len(phone)>80 or any(ord(c)<32 for c in phone):
        raise ValueError('CONTACTO_TELEFONO no es válido.')
    if not es_piloto() and '[Ejemplo]' in phone:
        raise ValueError('El contacto de una emisión REAL no admite el prefijo de ejemplo.')
    data.update(contacto_telefono=phone,contacto_correo=direccion(mail))
    emitted=data.pop('emitida_en')
    if isinstance(emitted,datetime):
        if emitted.tzinfo is not None:emitted=emitted.astimezone(ZoneInfo('America/Argentina/Buenos_Aires'))
        emitted=emitted.date()
    data['fecha_emision']=emitted.strftime('%d/%m/%Y')
    number=data['numero_registro']
    if number is None and not es_piloto():raise ValueError('La emisión REAL requiere un número de registro.')
    data['numero_registro']=f'{number:04d}' if number is not None else 'Sin número'
    data.setdefault('contacto_nombre','')
    data.setdefault('cantidad_fotos',None)
    if data['cantidad_fotos'] is not None and (isinstance(data['cantidad_fotos'],bool) or not isinstance(data['cantidad_fotos'],int) or data['cantidad_fotos']<0):
        raise ValueError('La cantidad de fotos debe ser un entero mayor o igual a cero.')
    digest=data.pop('pdf_hash')
    if not re.fullmatch('[0-9a-f]{64}',digest):raise ValueError('La emisión requiere una huella SHA-256 válida.')
    data['pdf_sha256_corto']=digest[:16]
    subject=f"{data['codigo']} · Reg. {data['numero_registro']} · Rev. {data['revision']} · {data['cliente_razon_social']} · {data['fecha_emision']}"
    if len(subject)>200:raise ValueError('El asunto descriptivo supera los 200 caracteres admitidos.')
    filename=(f"{componente_archivo(data['codigo'],60)}_Reg{componente_archivo(data['numero_registro'])}"
              f"_Rev{data['revision']}_{componente_archivo(data['cliente_razon_social'])}_{emitted.isoformat()}.pdf")
    data['nombre_adjunto']=filename
    env=current_app.jinja_env.overlay(undefined=StrictUndefined)
    plain=env.get_template('correo/emision.txt').render(**data)
    html=env.get_template('correo/emision.html').render(**data)
    return dict(asunto=subject,cuerpo=plain,html=html,nombre_adjunto=filename)


def contenido_emision(session,carga):
    digest=sha256(bytes(carga.pdf)).hexdigest()
    if digest!=carga.pdf_sha256 or (carga.pdf_hash and digest!=carga.pdf_hash):
        raise ValueError('La huella del PDF emitido no coincide.')
    planilla=session.get(Planilla,carga.planilla_id)
    archived=session.scalar(select(EmisionCarga).where(EmisionCarga.carga_id==carga.id,
        EmisionCarga.revision_publica==carga.revision_publica,EmisionCarga.pdf_sha256==carga.pdf_sha256))
    header=(archived.datos if archived else carga.datos).get('cabecera',{})
    identity=archived.firmantes if archived else {}
    stored=session.get(FirmaCarga,carga.id) if not archived else None
    technician=identity.get('tecnico',{}).get('nombre') or (stored.tecnico_nombre if stored else '') or header.get('inspector','')
    responsible=identity.get('responsable',{}).get('nombre_firmante') or (stored.nombre_firmante if stored else '') or ''
    return renderizar_emision(dict(
        codigo=planilla.codigo.removeprefix('SG-PEM-IFI-'),
        nombre_planilla=planilla.definicion.get('titulo',''),
        numero_registro=archived.numero_registro if archived else carga.numero_registro,
        revision=archived.revision_publica if archived else carga.revision_publica,
        cliente_razon_social=header.get('cliente',''),cliente_cuit=header.get('cuit',''),
        instalacion_direccion=header.get('direccion',''),sistema_codigo=planilla.sistema_tipo,
        sistema_nombre=header.get('sistema_designacion',''),
        emitida_en=archived.emitida_en if archived else carga.emitida_en,
        firmante_mantenedor=technician,firmante_instalacion=responsible,
        certificado_n=header.get('numero_mantenedor') or current_app.config.get('CERTIFICADO_N',''),
        pdf_hash=carga.pdf_sha256,
        cantidad_fotos=session.scalar(select(func.count(FotoCarga.id)).where(FotoCarga.carga_id==carga.id))))
