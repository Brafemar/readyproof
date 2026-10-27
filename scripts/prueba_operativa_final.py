"""Prueba local de SAA-1 con sesión real, evidencia y correo explícito."""
import argparse
import base64
from copy import deepcopy
from email import policy
from email.parser import BytesParser
import getpass
from hashlib import sha256
from http.cookiejar import CookieJar
from io import BytesIO
import json
from pathlib import Path
import sys
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPCookieProcessor, Request, build_opener
from uuid import uuid4
import webbrowser

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))


class ErrorPrueba(RuntimeError):
    pass


class API:
    def __init__(self,url):
        parsed=urlsplit(url)
        if parsed.scheme!='http' or parsed.hostname not in {'localhost','127.0.0.1','::1'} or parsed.username or parsed.password or parsed.path not in ('','/') or parsed.query or parsed.fragment:
            raise ErrorPrueba('Esta prueba admite únicamente el servidor HTTP local, sin claves en la URL.')
        self.url=url.rstrip('/')
        self.opener=build_opener(HTTPCookieProcessor(CookieJar()))
        self.csrf=None

    def request(self,method,path,datos=None,*,binario=False,cabeceras=None):
        headers={'Accept':'application/pdf' if binario else 'application/json'}
        if self.csrf:headers['X-CSRF-Token']=self.csrf
        headers.update(cabeceras or {})
        payload=json.dumps(datos,ensure_ascii=False).encode('utf-8') if datos is not None else None
        if payload is not None:headers['Content-Type']='application/json'
        request=Request(self.url+path,data=payload,headers=headers,method=method)
        try:
            with self.opener.open(request,timeout=180) as response:
                data=response.read()
        except HTTPError as error:
            # No se incluyen cuerpos, contraseñas ni cookies en los diagnósticos.
            raise ErrorPrueba(f'HTTP {error.code} en {method} {path}. Revisar acceso y auditoría; no se reintenta automáticamente.') from None
        return data if binario else json.loads(data)


def iniciar_sesion(api,usuario,clave):
    api.csrf=api.request('GET','/api/auth/sesion')['csrf_token']
    result=api.request('POST','/api/auth/login',{'login':usuario,'clave':clave})
    api.csrf=result['csrf_token']
    if result['usuario']['login']!=usuario.lower():
        raise ErrorPrueba('La cuenta autenticada no coincide con la solicitada.')
    return result['usuario']


def guardar(path,report):
    temporary=path.with_suffix('.tmp')
    temporary.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temporary.replace(path)


def firma_ficticia(desfase=0):
    from PIL import Image,ImageDraw
    image=Image.new('RGBA',(1000,280),(255,255,255,0))
    ImageDraw.Draw(image).line([(100,200),(210,70+desfase),(280,210),(420,110),(570,185),(730,90+desfase),(850,175)],fill=(25,35,40,255),width=5)
    output=BytesIO();image.save(output,format='PNG')
    return 'data:image/png;base64,'+base64.b64encode(output.getvalue()).decode('ascii')


def verificar_pdf(payload):
    from PIL import Image
    from pypdf import PdfReader
    if not payload.startswith(b'%PDF-'):raise ErrorPrueba('La descarga no es un PDF.')
    reader=PdfReader(BytesIO(payload))
    if len(reader.pages)!=2:raise ErrorPrueba('SAA-1 no coincide con las dos páginas de referencia.')
    if any('Planilla conforme a IRAM 3546:2011' not in page.extract_text() for page in reader.pages):
        raise ErrorPrueba('Falta la leyenda IRAM en una página.')
    if 'T.C. 3 AÑOS' not in reader.pages[0].extract_text():raise ErrorPrueba('Falta la retención en el encabezado.')
    with Image.open(ROOT/'app/static/logo_readyproof.png') as image:
        expected=sha256(image.convert('RGB').tobytes()).hexdigest()
    if any(not any(sha256(image.image.convert('RGB').tobytes()).hexdigest()==expected for image in page.images) for page in reader.pages):
        raise ErrorPrueba('El PDF no contiene el logo vigente en todas las páginas.')
    if any((reader.metadata or {}).get(key)!='readyproof' for key in ('/Author','/Creator','/Producer')):
        raise ErrorPrueba('Los metadatos no coinciden con readyproof.')
    return {'paginas':2,'logo':True,'leyenda_iram':True,'retencion':True,'metadatos':True,'sha256':sha256(payload).hexdigest(),'bytes':len(payload)}


def procesar_envio(application,envio_id,*,smtp):
    from app.correo import send_email
    from app.models import Envio,Intento
    from sqlalchemy import select
    previous=application.config['MAIL_MODO_PRUEBA']
    application.config['MAIL_MODO_PRUEBA']=not smtp
    try:
        with application.app_context(),application.extensions['db_sessions']() as session:
            row=session.get(Envio,envio_id)
            if row is None:raise ErrorPrueba('El envío no existe en esta base local.')
            send_email(session,row)
            session.expire_all();row=session.get(Envio,envio_id)
            message=BytesParser(policy=policy.default).parsebytes(row.mensaje_eml)
            attempts=list(session.scalars(select(Intento).where(Intento.envio_id==row.id).order_by(Intento.numero)))
            return {'id':str(row.id),'estado':row.estado,'modo_prueba':not smtp,'message_id':str(message['Message-ID']),
                    'intentos':[{'numero':a.numero,'resultado':a.resultado} for a in attempts],
                    'enviado_en':row.enviado_en.isoformat() if row.enviado_en else None}
    finally:
        application.config['MAIL_MODO_PRUEBA']=previous


def procesador_local(base_url,smtp):
    state=json.loads((ROOT/'out/etapa3/demo_local/servidor.json').read_text(encoding='utf-8'))
    if state['url'].rstrip('/')!=base_url.rstrip('/') or Path(state['pgdata']).resolve()!=ROOT/'out/etapa3/demo_local/data':
        raise ErrorPrueba('No se identificó la misma base del ejemplo local. No se procesa correo.')
    port=int(state['pgport'])
    if not 1024<=port<=65535:raise ErrorPrueba('Puerto de base local inválido.')
    from app import create_app
    application=create_app({'DATABASE_URL':f'postgresql+psycopg://readyproof_demo@127.0.0.1:{port}/postgres','MAIL_MODO_PRUEBA':not smtp})
    return lambda envio_id:procesar_envio(application,envio_id,smtp=smtp)


def ejecutar(api,salida,*,usuario,destinatario,procesador):
    salida=Path(salida).resolve();salida.mkdir(parents=True,exist_ok=True,mode=0o700)
    path=salida/'resultado.json'
    if path.exists():raise ErrorPrueba('Ya existe evidencia en esa carpeta. No se repite la prueba ni el POST de envío; consultar el resultado o elegir otra carpeta.')
    report={'usuario':usuario,'estado':'iniciada','recepcion_confirmada':False,'apertura_visual_confirmada':False,'flujo_completo':False}
    guardar(path,report)
    clients=api.request('GET','/api/clientes')
    clients=[c for c in clients if c.get('es_ejemplo') and c['nombre'].startswith('[Ejemplo] ')]
    if not clients:raise ErrorPrueba('No hay clientes ficticios asignados a esta cuenta.')
    pairs=[]
    for client in clients:
        systems=api.request('GET',f"/api/clientes/{client['id']}/sistemas")
        pairs.extend((client,s) for s in systems if s['tipo']=='SAA' and s['designacion'].startswith('[Ejemplo] '))
    if not pairs:raise ErrorPrueba('No hay sistema SAA ficticio asignado.')
    client,system=next((pair for pair in pairs if pair[0]['nombre']=='[Ejemplo] readyproof'),pairs[0])
    templates=api.request('GET','/api/planillas')
    template=next((p for p in templates if p['codigo']=='SG-PEM-IFI-SAA-1' and p['sistema_tipo']=='SAA'),None)
    if template is None:raise ErrorPrueba('No se encontró SAA-1 vigente.')
    data=deepcopy(api.request('GET','/api/ejemplo/saa1'))
    data['cabecera']['cliente']=client['nombre']
    data['observaciones']=['[Ejemplo] Prueba operativa final de readyproof.','[Ejemplo] Datos y firmas ficticios; no corresponde a un servicio real.']
    carga=api.request('POST','/api/cargas',{'sistema_id':system['id'],'planilla_id':template['id'],'datos':data},cabeceras={'Idempotency-Key':str(uuid4())})
    report.update(carga_id=carga['id'],cliente_id=client['id'],plantilla_version=template['version']);guardar(path,report)
    route=f"/api/cargas/{carga['id']}"
    carga=api.request('PUT',route+'/borrador',{'revision':carga['revision'],'datos':data,'firmas':{'tecnico':firma_ficticia(),'responsable':firma_ficticia(25)}})
    if not all(carga['firmas'].values()):raise ErrorPrueba('No se guardaron ambas firmas ficticias.')
    preview=api.request('POST',route+'/vista-previa',{'revision':carga['revision']},binario=True)
    verificar_pdf(preview);(salida/'vista_previa.pdf').write_bytes(preview)
    carga=api.request('POST',route+'/finalizar',{'revision':carga['revision']})
    if carga['estado']!='finalizada':raise ErrorPrueba('No se finalizó la carga.')
    carga=api.request('POST',route+'/emitir',{'revision':carga['revision']})
    if carga['estado']!='emitida':raise ErrorPrueba('No se emitió la carga.')
    pdf=api.request('GET',route+'/pdf',binario=True)
    checks=verificar_pdf(pdf)
    if checks['sha256']!=carga['pdf_sha256']:raise ErrorPrueba('La descarga no coincide con la emisión.')
    target=salida/f"SAA-1_{carga['id']}.pdf";target.write_bytes(pdf)
    report.update(estado='emitida',pdf=str(target),verificacion_pdf=checks,firmas='PNG ficticios por API; no es una prueba de canvas')
    report['estado']='solicitud_envio_iniciada_no_repetir';guardar(path,report)
    envio=api.request('POST',route+'/enviar',{'destinatario':destinatario,'asunto':'[Ejemplo] SAA-1 de readyproof','cuerpo':'[Ejemplo] Se adjunta una planilla SAA-1 con datos y firmas ficticios para revisión de recepción y formato.'})
    report.update(envio_id=envio['id'],destinatario=destinatario,estado='encolada');guardar(path,report)
    report['estado']='procesando_envio_no_repetir';guardar(path,report)
    correo=procesador(envio['id'])
    report['correo']=correo
    if correo['modo_prueba'] and correo['estado']=='pendiente' and any(a['resultado']=='ok' for a in correo['intentos']):
        report['estado']='archivo_de_prueba_sin_smtp'
    elif correo['estado']=='enviado':
        report['estado']='smtp_aceptado_pendiente_recepcion'
    else:
        report['estado']='envio_no_confirmado_revisar_sin_repetir'
    guardar(path,report)
    return report


def confirmar_recepcion(report,path,respuesta):
    correo=report.get('correo',{})
    if correo.get('modo_prueba') is not False or correo.get('estado')!='enviado':
        raise ErrorPrueba('No se confirma recepción de un envío sin aceptación SMTP real.')
    if respuesta.strip()=='RECIBIDO_Y_REVISADO':
        report.update(recepcion_confirmada=True,apertura_visual_confirmada=True,flujo_completo=True,
                      estado='recepcion_y_apertura_confirmadas_por_operador',fuente_confirmacion='Declaración manual en consola; no lectura automática del destino')
        guardar(Path(path),report)
    return report


def main(argv=None):
    parser=argparse.ArgumentParser(description='Prueba local de readyproof. Sin SMTP por defecto; contraseña solo en consola.')
    parser.add_argument('--usuario',default='msanchez')
    parser.add_argument('--base-url',default='http://127.0.0.1:8765')
    parser.add_argument('--salida',type=Path,default=ROOT/'out/prueba_operativa_final')
    parser.add_argument('--destinatario',help='Casilla de prueba autorizada; obligatorio con --smtp.')
    parser.add_argument('--smtp',action='store_true',help='Procesa únicamente este envío por SMTP real; requiere destinatario autorizado.')
    parser.add_argument('--abrir-pdf',action='store_true',help='Solicita abrir la descarga en el visor del equipo.')
    parser.add_argument('--confirmar-recepcion',type=Path,help='Confirma después una recepción pendiente, sin login ni otro envío.')
    args=parser.parse_args(argv)
    if not sys.stdin.isatty():parser.error('Ejecutá en una consola interactiva; no pases contraseñas por chat, argumentos ni archivos.')
    try:
        if args.confirmar_recepcion:
            if args.smtp:raise ErrorPrueba('La confirmación no puede volver a enviar correo.')
            path=args.confirmar_recepcion.resolve();report=json.loads(path.read_text(encoding='utf-8'))
        else:
            if (args.salida/'resultado.json').exists():
                raise ErrorPrueba('Ya existe evidencia. Para confirmar un correo recibido usá --confirmar-recepcion; no se repite el envío.')
            if args.smtp and not args.destinatario:raise ErrorPrueba('--smtp requiere --destinatario con una casilla de prueba autorizada.')
            from app.correo import direccion
            recipient=direccion(args.destinatario or 'prueba@example.invalid')
            if args.smtp and recipient.lower().endswith('.invalid'):raise ErrorPrueba('La casilla de prueba SMTP debe poder recibir correo.')
            api=API(args.base_url)
            processor=procesador_local(args.base_url,args.smtp)
            password=getpass.getpass(f'Contraseña de {args.usuario}: ')
            logged=False
            try:
                iniciar_sesion(api,args.usuario,password);logged=True;password=None
                report=ejecutar(api,args.salida,usuario=args.usuario,destinatario=recipient,procesador=processor)
            finally:
                password=None
                if logged:
                    try:api.request('POST','/api/auth/logout')
                    except Exception:pass
            path=args.salida.resolve()/'resultado.json'
        if args.abrir_pdf:
            opened=webbrowser.open(Path(report['pdf']).as_uri())
            report['apertura_solicitada']=bool(opened);guardar(path,report)
        print('PDF:',report.get('pdf','no generado'))
        print('Evidencia:',path)
        print('Estado:',report['estado'])
        correo=report.get('correo',{})
        if correo.get('modo_prueba') is False and correo.get('estado')=='enviado':
            print('Buscar en Gmail: in:sent rfc822msgid:'+correo['message_id'].strip('<>'))
            print('Confirmar solo después de recibir el adjunto y abrirlo; revisar logo, leyenda, páginas y firmas ficticias.')
            answer=input('Escribí RECIBIDO_Y_REVISADO para confirmar; Enter deja pendiente: ')
            confirmar_recepcion(report,path,answer)
            return 0 if report['flujo_completo'] else 2
        if correo.get('modo_prueba') and report['estado']=='archivo_de_prueba_sin_smtp':
            print('Se archivó una copia EML: no hubo SMTP ni recepción real. Flujo completo pendiente.')
            return 0
        return 1
    except Exception as error:
        if isinstance(error,ErrorPrueba):print(str(error),file=sys.stderr)
        else:print('La prueba se detuvo: '+type(error).__name__+'. Revisá la evidencia; no repitas un envío de estado desconocido.',file=sys.stderr)
        return 1


if __name__=='__main__':
    raise SystemExit(main())
