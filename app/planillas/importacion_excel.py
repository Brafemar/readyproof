"""Lectura determinista de Excel del kit; nunca guarda ni modifica los originales."""
from copy import deepcopy
from difflib import unified_diff
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re
from zipfile import ZipFile

from openpyxl import load_workbook


def normalizar(value):
    return re.sub(r'\s+', ' ', str(value or '')).strip()


def unidad(value):
    return normalizar(re.sub(r'_+', '', value)) if isinstance(value, str) and '_' in value else None


def leer_excel(payload):
    book = load_workbook(BytesIO(payload), data_only=False)
    try:
        sheet = book.active
        end = next((row for row in range(9, sheet.max_row+1) if str(sheet.cell(row,1).value).startswith('OBSERVACIONES:')), None)
        if end is None:
            raise ValueError('Falta el área de observaciones del original.')
        grids = [row for row in range(9,end) if sheet.cell(row,1).value=='ELEMENTOS' and sheet.cell(row,9).value in ('ENE','S1')]
        checks = [row for row in range(9,end) if sheet.cell(row,1).value=='VERIFICACIÓN']
        kind = 'grid_m' if grids and sheet.cell(grids[0],9).value=='ENE' else 'grid_s' if grids else 'ver' if checks else 'general'
        ranges = {(r.min_row,r.min_col):r for r in sheet.merged_cells.ranges}
        blocks = []
        if kind == 'general':
            for row in range(9,end):
                label = sheet.cell(row,1).value
                merged = ranges.get((row,1))
                if not label:
                    continue
                if merged and merged.max_col==25:
                    blocks.append({'titulo':label,'fila':row,'items':[]})
                elif merged and merged.max_col==9:
                    if not blocks:
                        raise ValueError('Campo sin bloque de origen.')
                    value = sheet.cell(row,10).value or ''
                    options = [normalizar(x) for x in re.findall(r'([^☐]+)☐', value)]
                    blocks[-1]['items'].append({'fila':row,'texto':str(label).removesuffix(':'),'opciones':options,'unidad':unidad(value)})
        else:
            headers = grids or checks
            for index,header in enumerate(headers):
                stop = headers[index+1]-1 if index+1<len(headers) else end
                block = {'titulo':sheet.cell(header-1,1).value,'fila':header-1,
                         'fecha':sheet.cell(header-1,20).value=='FECHA:',
                         'columnas':[sheet.cell(header,col).value for col in range(9 if grids else 15,26) if sheet.cell(header,col).value], 'items':[]}
                for row in range(header+1,stop):
                    label = sheet.cell(row,1).value
                    merged = ranges.get((row,1))
                    if label is None or not merged or merged.max_col!=(8 if grids else 14):
                        continue
                    block['items'].append({'fila':row,'texto':label,'unidad':unidad(sheet.cell(row,15).value) if checks else None})
                blocks.append(block)
        if not blocks or any(not b['items'] for b in blocks):
            raise ValueError('El original contiene bloques vacíos o un formato no reconocido.')
        first_rows = [{'fila':cell.row, 'celda':cell.coordinate, 'texto':cell.value}
            for row in sheet.iter_rows(max_row=20) for cell in row if isinstance(cell.value, str)]
        return {'formato':kind,'bloques':blocks,'fila_observaciones':end,'primeras_filas':first_rows}
    finally:
        book.close()


def diferencias_catalogo(source, reference):
    differences = []
    expected_kind = reference['bloques'][0]['tipo'] if reference['bloques'] else 'general'
    if source['formato'] != expected_kind:
        differences.append({'tipo':'formato','excel':source['formato'],'catalogo':expected_kind})
    actual_items = [(b['titulo'],item) for b in source['bloques'] for item in b['items']]
    refs = reference['campos'] if expected_kind=='general' else [i for b in reference['bloques'] for i in b['items']]
    if len(actual_items)!=reference['items_total'] or len(refs)!=reference['items_total']:
        differences.append({'tipo':'cantidad','excel':len(actual_items),'catalogo':reference['items_total']})
    expected_rows = {i['fila']:i for i in refs}
    if set(expected_rows)!={i['fila'] for _,i in actual_items}:
        differences.append({'tipo':'filas_origen'})
    for title,item in actual_items:
        ref = expected_rows.get(item['fila'])
        if ref is None:
            continue
        if item['texto']!=ref.get('campo',ref.get('texto')):
            differences.append({'tipo':'texto','fila':item['fila'],'excel':item['texto'],'catalogo':ref.get('campo',ref.get('texto'))})
        if expected_kind=='general':
            if title!=ref['seccion'] or item['opciones']!=ref.get('opciones',[]):
                differences.append({'tipo':'seccion_opciones','fila':item['fila']})
        elif item['unidad']!=unidad(ref.get('valor')):
            differences.append({'tipo':'unidad','fila':item['fila']})
    if expected_kind!='general':
        if len(source['bloques'])!=len(reference['bloques']):
            differences.append({'tipo':'cantidad_bloques'})
        for block,ref in zip(source['bloques'],reference['bloques']):
            title = block['titulo']+(' | FECHA:' if block['fecha'] else '')
            if title!=ref['titulo'] or block['columnas']!=ref['columnas']:
                differences.append({'tipo':'cabecera_bloque','fila':block['fila']})
    return differences


def contenido(source):
    """Representación comparable con las definiciones anteriores de la aplicación."""
    blocks = []
    for block in source['bloques']:
        items = []
        for item in block['items']:
            value = {'texto':item['texto'],'unidad':normalizar(item.get('unidad')) or None}
            if source['formato']=='general':
                value['opciones'] = item.get('opciones',[])
            else:
                columns=1 if source['formato']=='ver' else 5 if source['formato']=='grid_s' else 12
                value['opciones_resultado'] = [['✓','O','X','NA'] for _ in range(columns)]
            items.append(value)
        blocks.append({'titulo':block['titulo'],'items':items})
    return {'formato':source['formato'],'bloques':blocks}


def _contenido_esquema(schema):
    if not isinstance(schema.get('bloques'),dict):
        return None
    kind = schema.get('tipo_planilla','general')
    tables = schema.get('tablas',{})
    kind = 'ver' if kind=='checklist' else ('grid_s' if next(iter(tables.values()),{}).get('columnas',[None])[0]=='S1' else 'grid_m') if kind=='periodico' else 'general'
    blocks = []
    for title,fields in schema['bloques'].items():
        items = []
        if kind=='general':
            for key,field in fields.items():
                items.append({'texto':field.get('etiqueta',key),'unidad':normalizar(field.get('unidad')) or None,'opciones':field.get('opciones',[])})
        else:
            for row in tables.get(title,{}).get('filas',[]):
                unit = fields[row['campos'][0]].get('unidad') if kind=='ver' else None
                options=[fields[key].get('opciones',[]) for key in row['campos'] if fields[key].get('tipo')=='opcion']
                items.append({'texto':row['etiqueta'],'unidad':normalizar(unit) or None,'opciones_resultado':options})
        blocks.append({'titulo':title,'items':items})
    return {'formato':kind,'bloques':blocks}


def contenido_esquema(schema):
    try:
        return _contenido_esquema(schema)
    except (AttributeError,KeyError,IndexError,TypeError):
        return None


def definicion_desde_excel(code, source, reference, file_sha):
    from .multisistema import _esquema
    family = code.split('-')[-2]
    header={cell['celda']:cell['texto'] for cell in source['primeras_filas']}
    if not header.get('A1') or not header.get('A4'):
        raise ValueError('Falta el nombre de sistema o título del encabezado original.')
    spec = {'codigo':code,'sistema':header['A1'],'titulo':header['A4'],
            'tipo':'general' if source['formato']=='general' else 'checklist' if source['formato']=='ver' else 'periodico',
            'bloques':[]}
    if source['formato'] in ('grid_s','grid_m'):
        spec['modo'] = 'semanal' if source['formato']=='grid_s' else 'mensual'
    for block in source['bloques']:
        items = []
        for item in block['items']:
            options = item.get('opciones') or item.get('unidad')
            items.append((item['texto'],options) if options else item['texto'])
        spec['bloques'].append((block['titulo'],items))
    schema = _esquema(spec)
    if contenido_esquema(schema)!=contenido(source):
        raise ValueError('El esquema construido no conserva el contenido del Excel.')
    for block in source['bloques']:
        fields=schema['bloques'][block['titulo']]
        for item in block['items']:
            column='J' if source['formato']=='general' else 'R' if source['formato']=='ver' else 'I'
            if column+str(item['fila']) not in fields:
                raise ValueError('Un control no coincide con su fila de origen.')
    if schema['fila_observaciones'] != source['fila_observaciones']+1:
        raise ValueError('La primera fila editable de observaciones no coincide con el original.')
    schema['origen_excel'] = {'archivo':reference['archivo'],'sha256':file_sha,'formato':source['formato'],
                              'fila_observaciones_encabezado':source['fila_observaciones'],
                              'bloques':deepcopy(source['bloques'])}
    fingerprint = sha256(json.dumps(schema,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    return {'codigo':code,'familia':family,'version':'v5-'+file_sha[:12]+'-'+fingerprint[:8],
            'huella':fingerprint,'definicion':schema,'especificacion':spec}


def diferencias_lineas(expected, actual):
    first=json.dumps(expected,ensure_ascii=False,sort_keys=True,indent=2).splitlines()
    second=json.dumps(actual,ensure_ascii=False,sort_keys=True,indent=2).splitlines()
    return list(unified_diff(first,second,fromfile='Excel v5',tofile='BD existente',lineterm=''))


def leer_origen(path):
    """Devuelve nombre/base y bytes; rechaza nombres ambiguos, sin extraer archivos."""
    path=Path(path)
    files={}
    if path.is_dir():
        for item in sorted(path.rglob('*.xlsx')):
            if item.name in files:raise ValueError('Hay nombres Excel repetidos en el origen.')
            files[item.name]=item.read_bytes()
    elif path.is_file() and path.suffix.lower()=='.zip':
        with ZipFile(path) as archive:
            for info in archive.infolist():
                if info.filename.lower().endswith('.xlsx') and not info.is_dir():
                    name=Path(info.filename).name
                    if name in files:raise ValueError('Hay nombres Excel repetidos en el ZIP.')
                    files[name]=archive.read(info)
    else:
        raise ValueError('Indicá una carpeta de Excel o el ZIP oficial v5.')
    return files
