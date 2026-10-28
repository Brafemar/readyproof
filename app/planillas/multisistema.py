"""Definiciones de SDI, SBC y SAL tomadas del catálogo del kit."""
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
import json
import runpy
from uuid import uuid4

import sqlalchemy as sa

from ..carga_planillas import leer_definiciones
from .definiciones.saa1 import HERRAMIENTAS
from .generador import CABECERA

VERSION_MULTISISTEMA='00-26-ms1'
NOMBRES={'SDI':'Sistema de Detección de Incendios','SBC':'Sistema de Bombas Contraincendios','SAL':'Sistema de Extinción por Agentes Limpios'}
DESIGNACIONES={'SDI':'[Ejemplo] Detección de incendios','SBC':'[Ejemplo] Bombas contraincendios','SAL':'[Ejemplo] Extinción por agentes limpios'}
RESULTADOS=['✓','O','X','NA']


def _especificacion(group,sheet,family):
    spec=deepcopy(sheet)
    spec.update(sistema=group['nom'],codigo=f'SG-PEM-IFI-{family}-{sheet["n"]}',titulo=sheet.get('titulo',sheet['nombre']))
    spec['bloques']=[(title,[tuple(field) if isinstance(field,list) else field for field in fields]) for title,fields in spec['bloques']]
    return spec


def _tipo_general(label,options):
    if isinstance(options,list):return dict(tipo='opcion',opciones=options)
    if isinstance(options,str) and options:
        return dict(tipo='texto' if options=='V / A' else 'numero',unidad=options)
    if 'fecha' in label.lower():return dict(tipo='fecha')
    if label=='Cantidad de cilindros':return dict(tipo='entero')
    return dict(tipo='texto')


def _esquema(spec):
    from openpyxl.utils import get_column_letter
    months=runpy.run_path(str(HERRAMIENTAS/'build_planilla.py'))['MESES']
    blocks={};tables={};row=9
    for title,items in spec['bloques']:
        if title in blocks:raise ValueError('Hay bloques repetidos; revisar su identificación antes de habilitar.')
        fields={};blocks[title]=fields
        if spec['tipo']=='general':
            row+=1
            for item in items:
                label,options=item if isinstance(item,tuple) else (item,None)
                key=f'J{row}';fields[key]=dict(_tipo_general(label,options),etiqueta=label,celda=key);row+=1
        else:
            table=dict(columna_etiqueta='VERIFICACIÓN' if spec['tipo']=='checklist' else 'ELEMENTOS',columnas=['VALOR','RESULTADO'] if spec['tipo']=='checklist' else (['S1','S2','S3','S4','S5'] if spec.get('modo')=='semanal' else list(months)),filas=[])
            tables[title]=table
            if spec['tipo']=='checklist':
                key=f'V{row}';fields[key]=dict(tipo='fecha',etiqueta='FECHA:',celda=key)
            row+=2
            for item in items:
                label,unit=item if isinstance(item,tuple) else (item,'')
                cells=[]
                if spec['tipo']=='checklist':
                    value=f'O{row}';result=f'R{row}'
                    fields[value]=dict(tipo='numero' if unit else 'texto',etiqueta=label+' · VALOR',celda=value)
                    if unit:fields[value]['unidad']=unit
                    fields[result]=dict(tipo='opcion',opciones=list(RESULTADOS),etiqueta=label+' · RESULTADO',
                                        celdas_resultado={code:f'{col}{row}' for code,col in zip(RESULTADOS,['R','T','V','X'])})
                    cells=[value,result]
                else:
                    step=2 if spec.get('modo')=='semanal' else 1
                    for index,column in enumerate(table['columnas']):
                        key=f'{get_column_letter(9+index*step)}{row}'
                        fields[key]=dict(tipo='opcion',opciones=list(RESULTADOS),etiqueta=label+' · '+column,celda=key)
                        cells.append(key)
                table['filas'].append(dict(etiqueta=label+(' ('+unit+')' if unit and spec['tipo']=='periodico' else ''),campos=cells));row+=1
    schema=dict(cabecera={key:{'tipo':'fecha' if key=='fecha' else 'texto'} for key in CABECERA},
                bloques=blocks,observaciones={'tipo':'lista_texto','maximo':4},tablas=tables,
                titulo=spec['titulo'],sistema=spec['sistema'],codigo=spec['codigo'],tipo_planilla=spec['tipo'],fila_observaciones=row+1)
    return schema


@lru_cache(maxsize=1)
def definiciones_multisistema():
    result={}
    for family,document,digest in leer_definiciones():
        if family not in NOMBRES:continue
        if document['origen']['ruta']!='herramientas/planillas_data2.py' or document['generador']['ruta']!='herramientas/build_planilla.py':
            raise ValueError('El catálogo no apunta a las herramientas autorizadas.')
        if sha256((HERRAMIENTAS/'planillas_data2.py').read_bytes()).hexdigest()!=document['origen']['sha256'] or sha256((HERRAMIENTAS/'build_planilla.py').read_bytes()).hexdigest()!=document['generador']['sha256']:
            raise ValueError('La huella del catálogo no coincide con la fuente; registrar una versión nueva.')
        for sheet in document['datos']['planillas']:
            spec=_especificacion(document['datos'],sheet,family);schema=_esquema(spec)
            fingerprint=sha256(json.dumps(dict(catalogo=digest,esquema=schema),sort_keys=True,ensure_ascii=False).encode()).hexdigest()
            result[spec['codigo']]=dict(codigo=spec['codigo'],familia=family,version=VERSION_MULTISISTEMA,
                huella=fingerprint,definicion=schema,especificacion=spec,manual='SG-PEM-IFI-'+family,nombre=sheet['nombre'])
    if len(result)!=15:raise ValueError('Se requieren SDI-1 a 5, SBC-1 a 6 y SAL-1 a 4 completos.')
    return result


def ejemplo_multisistema(schema):
    sample='[Ejemplo] 1' if schema.get('origen_excel') else '[Ejemplo] Dato de prueba'
    header={key:('2026-10-25' if key=='fecha' else 'readyproof' if key=='empresa_mantenedora' else sample) for key in schema['cabecera']}
    blocks={}
    for title,fields in schema['bloques'].items():
        blocks[title]={key:(field['opciones'][0] if field['tipo']=='opcion' else 1 if field['tipo'] in ('numero','entero') else '2026-10-25' if field['tipo']=='fecha' else '[Ejemplo] 1') for key,field in fields.items()}
    return dict(cabecera=header,bloques=blocks,observaciones=['[Ejemplo] Datos y firmas ficticios.'])


def cargar_multisistema(connection):
    definitions=definiciones_multisistema()
    planillas=sa.table('planillas',sa.column('id',sa.String(36)),sa.column('codigo',sa.String),sa.column('version',sa.String),sa.column('sistema_tipo',sa.String),sa.column('huella',sa.String),sa.column('definicion',sa.JSON),sa.column('manual_id',sa.Uuid(as_uuid=False)))
    manuales=sa.table('manuales',sa.column('id',sa.Uuid(as_uuid=False)),sa.column('codigo',sa.String))
    for definition in definitions.values():
        manual=connection.scalar(sa.select(manuales.c.id).where(manuales.c.codigo==definition['manual']))
        if manual is None:raise ValueError('Falta el manual '+definition['manual'])
        previous=connection.execute(sa.select(planillas).where(planillas.c.codigo==definition['codigo'],planillas.c.version==definition['version'])).mappings().first()
        values=dict(codigo=definition['codigo'],version=definition['version'],sistema_tipo=definition['familia'],huella=definition['huella'],definicion=definition['definicion'],manual_id=manual)
        if previous:
            if any(previous[key]!=value for key,value in values.items()):raise ValueError('La versión ya registrada difiere; no se sobrescribe.')
        else:connection.execute(planillas.insert().values(id=str(uuid4()),**values))
    clientes=sa.table('clientes',sa.column('id',sa.String),sa.column('nombre',sa.String),sa.column('es_ejemplo',sa.Boolean))
    sistemas=sa.table('sistemas',sa.column('id',sa.String),sa.column('cliente_id',sa.String),sa.column('tipo',sa.String),sa.column('designacion',sa.String))
    for client_id in connection.scalars(sa.select(clientes.c.id).where(clientes.c.es_ejemplo.is_(True),clientes.c.nombre.startswith('[Ejemplo] '))):
        for family,name in DESIGNACIONES.items():
            if connection.scalar(sa.select(sistemas.c.id).where(sistemas.c.cliente_id==client_id,sistemas.c.tipo==family)) is None:
                connection.execute(sistemas.insert().values(id=str(uuid4()),cliente_id=client_id,tipo=family,designacion=name))
