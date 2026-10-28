"""Catálogo verificado de 79 planillas, conservando las 16 definiciones previas."""
from copy import deepcopy
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
from uuid import uuid4

import sqlalchemy as sa

from ..config import SISTEMAS_HABILITADOS

HUELLA_RESTANTES = '522d5cab76b4194843626c08abf3e68fa54a8b8f649791ef86f2c683e02fa387'


@lru_cache(maxsize=1)
def definiciones_restantes():
    from .definiciones.saa1 import HERRAMIENTAS
    from .multisistema import _esquema
    path=Path(__file__).parent/'definiciones/restantes_v5.json'
    payload=path.read_bytes()
    if sha256(payload).hexdigest()!=HUELLA_RESTANTES:
        raise ValueError('El catálogo ampliado no coincide con la versión verificada.')
    bundle=json.loads(payload)
    if sha256((HERRAMIENTAS/'build_planilla.py').read_bytes()).hexdigest()!=bundle['generador_sha256']:
        raise ValueError('El generador cambió: cotejar las plantillas antes de emitir.')
    result={}
    for record in bundle['planillas']:
        schema=record['definicion'];spec=record['especificacion']
        spec['bloques']=[(title,[tuple(item) if isinstance(item,list) else item for item in items]) for title,items in spec['bloques']]
        expected=_esquema(spec)
        expected['origen_excel']=deepcopy(schema['origen_excel'])
        if expected!=schema or sha256(json.dumps(schema,sort_keys=True,ensure_ascii=False).encode()).hexdigest()!=record['huella']:
            raise ValueError('Una definición ampliada no conserva el contenido aprobado.')
        if record['familia'] not in SISTEMAS_HABILITADOS or record['version']!='00-26-ms1' or record['codigo'] in result:
            raise ValueError('Código o versión no permitido en el catálogo ampliado.')
        result[record['codigo']]=record
    if len(result)!=63:raise ValueError('Se requieren las 63 planillas restantes completas.')
    return result


@lru_cache(maxsize=1)
def definiciones_habilitadas():
    from .multisistema import definiciones_multisistema
    old=definiciones_multisistema();new=definiciones_restantes()
    if old.keys() & new.keys():raise ValueError('No se sobrescriben las planillas existentes.')
    result={**old,**new}
    from .unidades_autorizadas import CODIGO,scc_en_bar
    result[CODIGO]=scc_en_bar(new[CODIGO])
    return result


def cargar_restantes(connection):
    from ..models import Planilla, Manual
    table=Planilla.__table__;manuals=Manual.__table__
    for record in definiciones_restantes().values():
        previous=connection.execute(sa.select(table).where(table.c.codigo==record['codigo'])).mappings().all()
        if previous:
            if not any(p['version']==record['version'] and p['huella']==record['huella'] and p['definicion']==record['definicion'] for p in previous):
                raise ValueError('Existe una plantilla distinta: no se sobrescribe '+record['codigo'])
            continue
        manual=connection.scalar(sa.select(manuals.c.id).where(manuals.c.codigo==record['manual']))
        connection.execute(table.insert().values(id=str(uuid4()),codigo=record['codigo'],version=record['version'],
            sistema_tipo=record['familia'],huella=record['huella'],definicion=record['definicion'],manual_id=manual))


def completar_sistemas_ejemplo(connection):
    from ..models import Cliente, Sistema
    clients=Cliente.__table__;systems=Sistema.__table__
    for client_id in connection.scalars(sa.select(clients.c.id).where(clients.c.es_ejemplo.is_(True),clients.c.nombre.startswith('[Ejemplo] '))):
        for code,name in SISTEMAS_HABILITADOS.items():
            if connection.scalar(sa.select(systems.c.id).where(systems.c.cliente_id==client_id,systems.c.tipo==code)) is None:
                connection.execute(systems.insert().values(id=str(uuid4()),cliente_id=client_id,tipo=code,
                    designacion='[Ejemplo] '+name,activo=True))
