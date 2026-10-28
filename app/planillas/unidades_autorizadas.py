"""Versión SCC-1 en bar autorizada por Jorge y Martín el 28/10/2026."""
from copy import deepcopy
from hashlib import sha256
import json

CODIGO='SG-PEM-IFI-SCC-1'
VERSION='00-26-bar1'
BLOQUE='DATOS DE LA PLANILLA IRAM 3546-16A'
CAMPO='J21'

def scc_en_bar(original):
    from .multisistema import _esquema
    assert original['codigo']==CODIGO and original['version']=='00-26-ms1'
    assert original['definicion']['bloques'][BLOQUE][CAMPO]['unidad']=='MPa'
    result=deepcopy(original);spec=result['especificacion'];changed=0
    blocks=[]
    for title,items in spec['bloques']:
        updated=[]
        for item in items:
            if title==BLOQUE and isinstance(item,tuple) and item==('Presión normal a 20 °C','MPa'):
                item=(item[0],'bar');changed+=1
            updated.append(item)
        blocks.append((title,updated))
    assert changed==1,'El campo aprobado no coincide con la versión del kit.'
    spec['bloques']=blocks
    schema=_esquema(spec)
    schema['origen_excel']=deepcopy(original['definicion']['origen_excel'])
    expected=deepcopy(original['definicion']);expected['bloques'][BLOQUE][CAMPO]['unidad']='bar'
    assert schema==expected,'No se autorizaron otras diferencias de contenido.'
    result.update(version=VERSION,definicion=schema,
        huella=sha256(json.dumps(schema,sort_keys=True,ensure_ascii=False).encode()).hexdigest())
    return result

def cargar_version_bar(connection):
    import sqlalchemy as sa
    from uuid import uuid4
    from ..models import Planilla
    from .catalogo_completo import definiciones_restantes
    original=definiciones_restantes()[CODIGO];new=scc_en_bar(original);table=Planilla.__table__
    previous=connection.execute(sa.select(table).where(table.c.codigo==CODIGO,table.c.version==original['version'])).mappings().one()
    assert previous['huella']==original['huella'] and previous['definicion']==original['definicion']
    existing=connection.execute(sa.select(table).where(table.c.codigo==CODIGO,table.c.version==VERSION)).mappings().first()
    if existing:
        assert existing['huella']==new['huella'] and existing['definicion']==new['definicion']
        return
    connection.execute(table.insert().values(id=str(uuid4()),codigo=CODIGO,version=VERSION,sistema_tipo='SCC',
        huella=new['huella'],definicion=new['definicion'],manual_id=previous['manual_id']))
