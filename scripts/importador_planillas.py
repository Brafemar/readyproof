"""Coteja los 79 Excel y registra solo definiciones nuevas, sin sobrescribir versiones."""
import argparse
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import sys
from collections import Counter as Votos

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session
from app.config import validar_base_local
from app.models import Manual, Planilla, Sistema
from app.planillas.importacion_excel import (leer_origen, leer_excel, diferencias_catalogo,
    contenido, contenido_esquema, definicion_desde_excel, diferencias_lineas)


def validar_sigla_planilla(archivo_excel, contenido_excel, *, codigo_catalogo=None):
    """Cruza fuentes y elige la primera coincidente; contradicciones explícitas se informan."""
    name = Path(archivo_excel).name
    expected = re.match(r'^(?:SG-PEM-IFI-)?([A-Z]{3})-[0-9]+(?:[_ .-]|$)', name)
    filename = expected.group(1) if expected else None
    if not isinstance(contenido_excel, dict) or not isinstance(contenido_excel.get('primeras_filas'), list):
        raise ValueError(f'Falta la lectura de las primeras 20 filas del archivo {name}.')
    found = set(); internal = set()
    for cell in contenido_excel['primeras_filas']:
        if not isinstance(cell, dict) or not isinstance(cell.get('fila'), int) or isinstance(cell.get('fila'), bool):
            raise ValueError(f'Lectura de encabezado inválida en archivo {name}.')
        if 1 <= cell['fila'] <= 20 and isinstance(cell.get('texto'), str):
            found.update(re.findall(r'\(([A-Z]{3})\)', cell['texto']))
            internal.update(re.findall(r'\bSG-PEM-IFI-([A-Z]{3})-[0-9]+\b', cell['texto']))
    catalog = re.fullmatch(r'SG-PEM-IFI-([A-Z]{3})-[0-9]+', codigo_catalogo) if codigo_catalogo else None
    sources={'codigo_interno_SG-PEM-IFI':next(iter(internal)) if len(internal)==1 else None,
             'parentesis':next(iter(found)) if len(found)==1 else None,'nombre_archivo':filename,
             'catalogo':catalog.group(1) if catalog else None}
    votes=[sources[k] for k in ('codigo_interno_SG-PEM-IFI','nombre_archivo','catalogo') if sources[k]]
    if codigo_catalogo is None and sources['parentesis']:votes.append(sources['parentesis'])
    counts=Votos(votes);agreed=next((s for s,n in counts.items() if n>=2),None)
    if codigo_catalogo is None and len(counts)==1:agreed=next(iter(counts))
    reason=None
    if len(internal)>1:reason='Códigos internos ambiguos.'
    elif len(found)>1 or (found and agreed and found!={agreed}):reason='Paréntesis contradictorios con las demás fuentes.'
    elif not agreed:reason='No se pudo extraer sigla de código interno, paréntesis ni nombre' if not votes and not found else 'No coinciden al menos dos fuentes de sigla.'
    if reason:
        return dict(sigla_extraida=None,sigla_detectada=None,sigla_validada=False,coincide_nombre_archivo=False,
                    fuente='no_encontrada',validacion='FALLO',motivo=reason,fuentes=sources)
    source=next(k for k in ('codigo_interno_SG-PEM-IFI','parentesis','nombre_archivo') if sources[k]==agreed)
    return dict(sigla_extraida=agreed,sigla_detectada=agreed,sigla_validada=True,
        coincide_nombre_archivo=filename==agreed,fuente=source,validacion='OK',fuentes=sources,
        fuentes_discrepantes={k:v for k,v in sources.items() if v and v!=agreed})


def extraer_sigla_planilla(archivo_excel, contenido_excel):
    result=validar_sigla_planilla(archivo_excel,contenido_excel)
    if not result['sigla_validada']:raise ValueError(result['motivo']+' en archivo '+Path(archivo_excel).name)
    return result['sigla_extraida']


def sistemas_por_sigla(session, cliente_id, sigla):
    """Conserva instalaciones distintas de una familia y restringe al cliente."""
    if not isinstance(sigla, str) or not re.fullmatch(r'[A-Z]{3}', sigla):
        raise ValueError('La sigla de sistema debe contener tres letras mayúsculas.')
    return list(session.scalars(select(Sistema).where(Sistema.cliente_id == cliente_id,
        Sistema.tipo == sigla, Sistema.activo.is_(True)).order_by(Sistema.id)))


def preparar(origen, catalogo, *, version_nuevas='00-26-ms1'):
    reference = json.loads(Path(catalogo).read_text(encoding='utf-8-sig'))
    if not isinstance(reference,list) or len(reference)!=79 or len({r['codigo'] for r in reference})!=79:
        raise ValueError('Se requiere el catálogo completo y sin duplicados de las 79 planillas.')
    files=leer_origen(origen)
    if set(files)!={r['archivo'] for r in reference}:
        raise ValueError('El origen debe contener exactamente los 79 Excel del catálogo, sin faltantes ni adicionales.')
    rows=[]
    for ref in sorted(reference,key=lambda r:r['codigo']):
        if not re.fullmatch(r'SG-PEM-IFI-[A-Z]{3}-[0-9]+',ref['codigo']):
            raise ValueError('Hay un código de planilla no reconocido.')
        payload=files[ref['archivo']];source=leer_excel(payload)
        sigla=validar_sigla_planilla(ref['archivo'],source,codigo_catalogo=ref['codigo'])
        code=('SG-PEM-IFI-'+sigla['sigla_extraida']+'-'+ref['codigo'].rsplit('-',1)[1]) if sigla['sigla_validada'] else ref['codigo']
        diff=diferencias_catalogo(source,ref)
        row={'codigo':code,'codigo_catalogo':ref['codigo'],'archivo':ref['archivo'],'sha256_excel':sha256(payload).hexdigest(),
             'formato':source['formato'],'items':sum(len(b['items']) for b in source['bloques']),
             'diferencias_catalogo':diff,'contenido':contenido(source)}
        row.update(sigla)
        row['nueva']=definicion_desde_excel(code,source,ref,row['sha256_excel']) if not diff and sigla['sigla_validada'] else None
        if row['nueva']:row['nueva']['version']=version_nuevas
        rows.append(row)
    if len({row['codigo'] for row in rows})!=len(rows):
        raise ValueError('La validación cruzada produce códigos repetidos; no se importa un catálogo ambiguo.')
    return rows


def importar(session, rows, *, aplicar=False):
    """Planifica todo antes de escribir; el caller confirma o revierte la transacción."""
    if any(row['diferencias_catalogo'] or not row.get('sigla_validada') for row in rows):
        return {'aplicar':aplicar,'cambios':0,'errores':True,'planillas':[
            {'codigo':r['codigo'],'estado':'RECHAZADO' if not r.get('sigla_validada') else 'CONTENIDO_DIFERENTE' if r['diferencias_catalogo'] else 'SIN_APLICAR',
             'validacion':r.get('validacion'),'motivo':r.get('motivo'),
             'diferencias_catalogo':r['diferencias_catalogo']} for r in rows]}
    existing=list(session.scalars(select(Planilla)))
    manuals=dict(session.execute(select(Manual.codigo,Manual.id)).all())
    from app.catalogo import VERSION_PILOTO,huella_saa1
    from app.planillas.validacion import esquema_saa1
    from app.planillas.multisistema import definiciones_multisistema
    from app.planillas.catalogo_completo import definiciones_restantes
    approved={(d['codigo'],d['version']):{'definicion':d['definicion'],'huella':d['huella']} for d in definiciones_multisistema().values()}
    approved[('SG-PEM-IFI-SAA-1',VERSION_PILOTO)]={'definicion':esquema_saa1(),'huella':huella_saa1()}
    approved.update({(d['codigo'],d['version']):{'definicion':d['definicion'],'huella':d['huella']}
        for d in definiciones_restantes().values()})
    planned=[];new=[]
    for row in rows:
        definition=row['nueva'];previous=[p for p in existing if p.codigo==row['codigo']]
        # Priorizar las versiones habilitadas en la app, sin reescribir las históricas.
        preferred=[p for p in previous if p.version in ('00-26-rp2','00-26-ms1')]
        candidates=preferred or [p for p in previous if p.version==definition['version']] or previous
        def expected_record(p):
            return approved.get((p.codigo,p.version)) or ({'definicion':definition['definicion'],'huella':definition['huella']} if p.version==definition['version'] or p.version.startswith('v5-') else None)
        def intact(p):
            expected=expected_record(p)
            return expected is None or (p.definicion==expected['definicion'] and p.huella==expected['huella'])
        matching=[p for p in candidates if contenido_esquema(p.definicion)==row['contenido'] and intact(p)]
        result={k:row[k] for k in ('codigo','archivo','sha256_excel','formato','items')}
        result.update({k:row[k] for k in ('sigla_extraida','sigla_detectada','sigla_validada','coincide_nombre_archivo','fuente','validacion','fuentes','fuentes_discrepantes')})
        if matching:
            p=matching[0]
            result.update(estado='YA_EXISTE',id=p.id,version=p.version)
        elif previous:
            p=candidates[0]
            diff=diferencias_lineas(row['contenido'],contenido_esquema(p.definicion))
            if not diff:
                diff=diferencias_lineas(expected_record(p),{'definicion':p.definicion,'huella':p.huella})
            result.update(estado='CONTENIDO_DIFERENTE',diferencias_lineas=diff)
        else:
            canonical=approved.get((definition['codigo'],definition['version']))
            if canonical and (canonical['definicion']!=definition['definicion'] or canonical['huella']!=definition['huella']):
                result.update(estado='CONTENIDO_DIFERENTE',diferencias_lineas=diferencias_lineas(canonical,
                    {'definicion':definition['definicion'],'huella':definition['huella']}))
                planned.append(result);continue
            manual=manuals.get('SG-PEM-IFI-'+definition['familia'])
            result.update(estado='A_IMPORTAR',version=definition['version'],manual_asociado=manual is not None)
            new.append((definition,manual,result))
        planned.append(result)
    errors=any(p['estado']=='CONTENIDO_DIFERENTE' for p in planned)
    if aplicar and not errors:
        for definition,manual,result in new:
            record=Planilla(codigo=definition['codigo'],version=definition['version'],sistema_tipo=definition['familia'],
                           huella=definition['huella'],definicion=definition['definicion'],manual_id=manual)
            session.add(record);session.flush();result.update(estado='IMPORTADA',id=record.id)
    return {'aplicar':aplicar,'cambios':len(new) if aplicar and not errors else 0,'errores':errors,
            'total':len(rows),'items_total':sum(r['items'] for r in rows),
            'estados':dict(Counter(r['estado'] for r in planned)),'planillas':planned}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--origen',type=Path,default=ROOT/'fuente/planillas')
    parser.add_argument('--catalogo',type=Path,required=True)
    parser.add_argument('--salida',type=Path)
    parser.add_argument('--aplicar',action='store_true',help='Registra únicamente códigos nuevos; no los habilita en la API.')
    parser.add_argument('--solo-catalogo',action='store_true',help='Coteja Excel y catálogo sin abrir ninguna conexión a BD.')
    args=parser.parse_args()
    if args.solo_catalogo and args.aplicar:
        parser.error('--solo-catalogo no puede combinarse con --aplicar.')
    rows=preparar(args.origen,args.catalogo)
    if args.solo_catalogo:
        report={'base_consultada':False,'cambios':0,'total':len(rows),'items_total':sum(r['items'] for r in rows),
                'errores':any(r['diferencias_catalogo'] or not r['sigla_validada'] for r in rows),
                'planillas':[{k:r.get(k) for k in ('codigo','archivo','sha256_excel','formato','items','diferencias_catalogo',
                    'sigla_extraida','sigla_detectada','sigla_validada','coincide_nombre_archivo','fuente','validacion','motivo','fuentes','fuentes_discrepantes')} for r in rows]}
        output=json.dumps(report,ensure_ascii=False,indent=2)
        if args.salida:
            args.salida.parent.mkdir(parents=True,exist_ok=True);args.salida.write_text(output,encoding='utf-8')
        print(output)
        return 2 if report['errores'] else 0
    from dotenv import load_dotenv
    load_dotenv(ROOT/'.env.local',override=False);load_dotenv(ROOT/'.env',override=False)
    url=os.environ.get('DATABASE_URL');validar_base_local(url);engine=create_engine(url)
    try:
        with Session(engine) as session, session.begin():
            if args.aplicar:
                session.execute(text('SELECT pg_advisory_xact_lock(724303)'))
            else:
                session.execute(text('SET TRANSACTION READ ONLY'))
            report=importar(session,rows,aplicar=args.aplicar)
            if report['errores']:session.rollback()
        output=json.dumps(report,ensure_ascii=False,indent=2)
        if args.salida:
            args.salida.parent.mkdir(parents=True,exist_ok=True);args.salida.write_text(output,encoding='utf-8')
        print(output)
        return 2 if report['errores'] else 0
    finally:engine.dispose()


if __name__=='__main__':
    try:raise SystemExit(main())
    except (ValueError,OSError) as error:
        print(json.dumps({'error':str(error),'cambios':0},ensure_ascii=True),file=sys.stderr);raise SystemExit(2)
