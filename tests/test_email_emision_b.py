"""Formato, seguridad y conservación de correos con datos ficticios."""
from copy import deepcopy
from datetime import datetime,timezone
from email import policy
from email.parser import BytesParser
from hashlib import sha256
from pathlib import Path
import smtplib
from uuid import uuid4

from flask import Flask
import pytest
from sqlalchemy.orm import Session

from app.correo import preparar_envio,send_email,reintentar_envios
from app.correo.emision import renderizar_emision
from app.models import Carga,Cliente,EmisionCarga,Envio,Sistema
from tests.test_smtp_gmail import carga_emitida

ROOT=Path(__file__).resolve().parents[1]


@pytest.fixture
def contexto_render():
    app=Flask('correo-prueba',template_folder=str(ROOT/'app/templates'))
    app.config.update(MODO_PILOTO=False,CONTACTO_TELEFONO='0000-0000000',CONTACTO_CORREO='contacto@example.invalid')
    with app.app_context():yield app


def datos_correo():
    return dict(codigo='SCC-2',nombre_planilla='[Ejemplo] Inspección mensual',numero_registro=7,revision=2,
        cliente_razon_social='[Ejemplo] Planta Álamo',cliente_cuit='00000000000',instalacion_direccion='[Ejemplo] Calle 123',
        sistema_codigo='SCC',sistema_nombre='[Ejemplo] Cocina',emitida_en=datetime(2026,10,31,1,20,tzinfo=timezone.utc),
        firmante_mantenedor='[Ejemplo] Técnico',firmante_instalacion='[Ejemplo] Responsable',
        certificado_n='IFI-2099-99999',pdf_hash='ab'*32,cantidad_fotos=None)


@pytest.mark.parametrize('piloto',[False,True])
def test_render_formato_y_prefijo_por_modo(contexto_render,piloto):
    contexto_render.config['MODO_PILOTO']=piloto
    data=datos_correo();before=deepcopy(data)
    result=renderizar_emision(data)
    client='[Ejemplo] Planta Álamo' if piloto else 'Planta Álamo'
    assert result['asunto']==f'SCC-2 · Reg. 0007 · Rev. 2 · {client} · 30/10/2026'
    assert result['nombre_adjunto']==f"SCC-2_Reg0007_Rev2_{'Ejemplo_' if piloto else ''}Planta_Alamo_2026-10-30.pdf"
    for key in ('html','cuerpo'):
        assert '{{' not in result[key] and '}}' not in result[key]
        assert 'abababababababab' in result[key]
        assert 'contacto@example.invalid' in result[key] and '0000-0000000' in result[key]
        assert 'Fotos del anexo' not in result[key]
        assert ('[Ejemplo]' in result[key]) == piloto
        assert 'firmada digitalmente' not in result[key]
    assert data==before


def test_html_escapado_y_nombre_sin_rutas(contexto_render):
    data=datos_correo();data['cliente_razon_social']='[Ejemplo] Álamo / <b>ensayo</b>'
    result=renderizar_emision(data)
    assert '<b>ensayo</b>' not in result['html'] and '&lt;b&gt;ensayo&lt;/b&gt;' in result['html']
    assert '/' not in result['nombre_adjunto'] and '\\' not in result['nombre_adjunto']
    assert result['nombre_adjunto'].isascii()


@pytest.mark.parametrize('key',['CONTACTO_TELEFONO','CONTACTO_CORREO'])
def test_sin_contactos_no_se_prepara_correo(contexto_render,key):
    contexto_render.config[key]=''
    with pytest.raises(ValueError,match='Configurar CONTACTO_TELEFONO y CONTACTO_CORREO'):
        renderizar_emision(datos_correo())


def test_cantidad_fotos_solo_si_existe_anexo(contexto_render):
    data=datos_correo();data['cantidad_fotos']=3
    result=renderizar_emision(data)
    assert 'Fotos del anexo: 3' in result['cuerpo']
    assert 'Fotos del anexo' in result['html']


def test_real_requiere_numero_y_huella(contexto_render):
    for key,value in [('numero_registro',None),('pdf_hash','huella-invalida')]:
        data=datos_correo();data[key]=value
        with pytest.raises(ValueError):renderizar_emision(data)


def habilitar_real(app,db,carga):
    app.config.update(MODO_PILOTO=False,EMPRESA_MANTENEDORA='Mantenedora de ensayo [Ejemplo]',
        CERTIFICADO_N='IFI-2099-99999',MAIL_MODO_PRUEBA=True,PLANILLAS_TRANSPORTE='gmail_api')
    system=db.get(Sistema,carga.sistema_id)
    db.get(Cliente,system.cliente_id).es_ejemplo=False
    carga.numero_registro=99;carga.pdf_hash=carga.pdf_sha256
    data=deepcopy(carga.datos);data['cabecera']['cliente']='[Ejemplo] Planta Álamo'
    carga.datos=data;db.commit()


def prohibir_smtp(monkeypatch):
    def prohibido(*args,**kwargs):raise AssertionError('No se permite correo real en estas pruebas.')
    monkeypatch.setattr(smtplib,'SMTP',prohibido)
    monkeypatch.setattr(smtplib,'SMTP_SSL',prohibido)


def test_mime_congelado_y_primer_envio_tras_recargar(app,carga_emitida,usuario_admin,monkeypatch):
    prohibir_smtp(monkeypatch)
    with app.app_context(),Session(app.extensions['db_engine']) as db:
        carga=db.get(Carga,carga_emitida);habilitar_real(app,db,carga)
        original_pdf=bytes(carga.pdf)
        envio=preparar_envio(db,carga,'cliente@example.invalid',usuario_admin['id'],'[Ejemplo] Antiguo','[Ejemplo] Antiguo')
        before=bytes(envio.mensaje_eml);key=envio.id
        mail=BytesParser(policy=policy.default).parsebytes(before)
        assert mail.get_body(preferencelist=('html',)).get_content_type()=='text/html'
        assert mail.get_body(preferencelist=('plain',)).get_content_type()=='text/plain'
        assert '[Ejemplo]' not in str(mail['Subject'])
        for kind in ('html','plain'):assert '[Ejemplo]' not in mail.get_body(preferencelist=(kind,)).get_content()
        attachment=list(mail.iter_attachments())[0]
        assert attachment.get_filename().startswith('SAA-1_Reg0099_Rev0_Planta_Alamo_')
        assert attachment.get_payload(decode=True)==original_pdf
        assert carga.pdf_hash[:16] in mail.get_body(preferencelist=('html',)).get_content()
        assert envio.eml_sha256==sha256(before).hexdigest()
        assert envio.intentos_reservados==0
        db.commit()
    app.config['CONTACTO_TELEFONO']='otro teléfono de prueba'
    with app.app_context(),Session(app.extensions['db_engine']) as db:
        result=send_email(db,key)
        assert result.intentos_reservados==1 and result.mensaje_eml==before
        assert db.get(Carga,carga_emitida).pdf==original_pdf
        assert reintentar_envios()==0


@pytest.mark.parametrize('inmediato',[False,True])
def test_rutas_real_generan_mensaje_sin_ejemplo(app,client,carga_emitida,monkeypatch,inmediato):
    prohibir_smtp(monkeypatch)
    with Session(app.extensions['db_engine']) as db:
        habilitar_real(app,db,db.get(Carga,carga_emitida))
    response=client.post(f'/api/cargas/{carga_emitida}/enviar',json=dict(destinatario='cliente@example.invalid',inmediato=inmediato),
        headers={'Idempotency-Key':str(uuid4())})
    assert response.status_code==202,response.get_json()
    with Session(app.extensions['db_engine']) as db:
        envio=db.get(Envio,response.get_json()['id'])
        assert '[Ejemplo]' not in envio.asunto and '[Ejemplo]' not in envio.cuerpo
        mail=BytesParser(policy=policy.default).parsebytes(envio.mensaje_eml)
        assert '[Ejemplo]' not in mail.get_body(preferencelist=('html',)).get_content()


def test_correo_usa_datos_y_firmantes_de_la_emision(app,carga_emitida,usuario_admin,monkeypatch):
    prohibir_smtp(monkeypatch)
    with app.app_context(),Session(app.extensions['db_engine']) as db:
        carga=db.get(Carga,carga_emitida);habilitar_real(app,db,carga)
        snapshot=deepcopy(carga.datos);snapshot['cabecera']['cliente']='[Ejemplo] Cliente Histórico'
        db.add(EmisionCarga(carga_id=carga.id,numero_registro=99,revision_publica=0,pdf=carga.pdf,
            pdf_sha256=carga.pdf_sha256,datos=snapshot,emitida_en=carga.emitida_en,
            firmantes=dict(tecnico=dict(nombre='[Ejemplo] Técnico histórico'),
                responsable=dict(nombre_firmante='[Ejemplo] Responsable histórico'))))
        db.flush()
        envio=preparar_envio(db,carga,'cliente@example.invalid',usuario_admin['id'])
        assert 'Cliente Histórico' in envio.asunto and 'Planta Álamo' not in envio.asunto
        assert 'Técnico histórico' in envio.cuerpo and 'Responsable histórico' in envio.cuerpo


def test_contactos_se_leen_del_entorno(monkeypatch):
    from app.config import configuracion
    monkeypatch.setenv('CONTACTO_TELEFONO','0000-0000000')
    monkeypatch.setenv('CONTACTO_CORREO','contacto@example.invalid')
    config=configuracion()
    assert config['CONTACTO_TELEFONO']=='0000-0000000'
    assert config['CONTACTO_CORREO']=='contacto@example.invalid'
