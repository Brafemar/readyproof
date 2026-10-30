"""Tres recorridos por cada una de las 63 planillas nuevas del kit."""
from copy import deepcopy
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import os

import pytest
from pypdf import PdfReader
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Carga, EmisionCarga
from app.planillas.catalogo_completo import definiciones_restantes
from app.planillas.firmantes import ejemplo_responsable
from app.planillas.multisistema import ejemplo_multisistema
from app.planillas.validacion import validar_datos, DatosInvalidos
from scripts.prueba_operativa_final import firma_ficticia

CODES=sorted(definiciones_restantes())


@pytest.fixture
def app(database_url,tmp_path):
    """Reproduce el flujo también sobre copias efímeras de un respaldo restaurado."""
    import subprocess
    from sqlalchemy.engine import make_url
    from app import create_app
    dump=os.environ.get('READYPROOF_RESTORE_DUMP')
    if dump:
        url=make_url(database_url)
        assert url.username=='readyproof_test' and url.host=='127.0.0.1'
        assert url.port!=5432 and url.database.startswith('rp_test_')
        source=Path(dump).resolve()
        assert source.is_file() and source.is_relative_to(Path('/home/readyproof_revision_etapa5/recursos'))
        command=[str(Path(os.environ['PG_BINDIR'])/'pg_restore'),'--exit-on-error','--single-transaction',
            '--no-owner','--no-acl','--host=127.0.0.1','--port='+str(url.port),
            '--username=readyproof_test','--dbname='+url.database,str(source)]
        result=subprocess.run(command,env=dict(os.environ,PGPASSWORD=url.password),capture_output=True,timeout=120)
        assert result.returncode==0,'No se pudo cargar el respaldo en la base efímera de prueba.'
    application=create_app({'TESTING':True,'DATABASE_URL':database_url,'DIRECTORIO_TEMPORAL':str(tmp_path/'temporales')})
    try:
        if not dump:
            result=application.test_cli_runner().invoke(args=['init-db','--ejemplos'])
            assert result.exit_code==0,result.output
        yield application
    finally:application.extensions['db_engine'].dispose()


@pytest.fixture
def usuario_admin(app):
    import secrets
    from uuid import uuid4
    from app.auth import hash_clave,normalizar_login
    from app.models import Usuario
    password=secrets.token_urlsafe(24)
    with Session(app.extensions['db_engine'],expire_on_commit=False) as db:
        user=Usuario(login=normalizar_login('e5-'+uuid4().hex),nombre='[Ejemplo] Prueba etapa 5',
            rol='admin',clave_hash=hash_clave(password))
        db.add(user);db.commit()
        return {'id':user.id,'login':user.login,'clave':password}


@pytest.fixture(scope='session')
def referencias_etapa5(tmp_path_factory):
    from scripts.referencias_etapa5 import crear_referencias
    origin=Path(os.environ.get('READYPROOF_EXCEL_ORIGEN',str(Path.home()/'Downloads/SG-PEM-IFI_Planillas_v5.zip')))
    work=tmp_path_factory.mktemp('ref')
    return crear_referencias(origin,Path('out/frente_a_v2/paginacion_referencia_actual.json'),work,paginacion_actual=True)


def crear_nueva(client,code):
    definition=definiciones_restantes()[code]
    customer=client.get('/api/clientes').get_json()[0]
    system=next(s for s in client.get(f"/api/clientes/{customer['id']}/sistemas").get_json() if s['tipo']==definition['familia'])
    template=next(p for p in client.get('/api/planillas').get_json() if p['codigo']==code)
    data=ejemplo_multisistema(definition['definicion'])
    data['cabecera'].update(cliente=customer['nombre'],sistema_designacion=system['designacion'])
    response=client.post('/api/cargas',json=dict(sistema_id=system['id'],planilla_id=template['id'],datos=data,
        responsable=ejemplo_responsable(),firmas={role:firma_ficticia() for role in ('tecnico','responsable')}))
    assert response.status_code==201,response.get_json()
    return response.get_json()


@pytest.mark.parametrize('code',CODES)
def test_planilla_nueva_carga_borrador(client,code):
    row=crear_nueva(client,code)
    assert row['estado']=='borrador' and row['numero_registro'] is None and row['revision_publica']==0
    data=deepcopy(row['datos']);data['observaciones']=['[Ejemplo] Borrador de '+code]
    response=client.put(f"/api/cargas/{row['id']}/borrador",json={'revision':row['revision'],'datos':data})
    assert response.status_code==200,response.get_json()
    saved=response.get_json()
    assert saved['id']==row['id'] and saved['revision']==row['revision']+1 and saved['datos']==data
    assert client.get(f"/api/cargas/{row['id']}").get_json()['datos']==data


@pytest.mark.parametrize('code',CODES)
def test_planilla_nueva_validacion(code):
    schema=definiciones_restantes()[code]['definicion'];data=ejemplo_multisistema(schema)
    validar_datos(data,schema,completo=True)
    original=deepcopy(data)
    invalid=deepcopy(data);invalid['cabecera']['campo_inventado']='[Ejemplo] No admitido'
    with pytest.raises(DatosInvalidos):validar_datos(invalid,schema,completo=True)
    results=[(title,key) for title,fields in schema['bloques'].items() for key,field in fields.items()
        if field.get('opciones')==['✓','O','X','NA']]
    if results:
        title,key=results[0];invalid=deepcopy(data);invalid['bloques'][title][key]='O';invalid['observaciones']=[]
        with pytest.raises(DatosInvalidos,match='observación'):validar_datos(invalid,schema,completo=True)
        invalid['observaciones']=['[Ejemplo] No cumple: corrección pendiente'];validar_datos(invalid,schema,completo=True)
    else:
        options=[(title,key) for title,fields in schema['bloques'].items() for key,field in fields.items() if field['tipo']=='opcion']
        if options:
            title,key=options[0];invalid=deepcopy(data);invalid['bloques'][title][key]='OPCION_INVENTADA'
            with pytest.raises(DatosInvalidos):validar_datos(invalid,schema,completo=True)
    measured=[(title,row) for title,table in schema.get('tablas',{}).items() for row in table['filas']
        if schema['tipo_planilla']=='checklist' and schema['bloques'][title][row['campos'][0]].get('unidad')]
    if measured:
        title,row=measured[0];value,result=row['campos'];invalid=deepcopy(data);del invalid['bloques'][title][value]
        with pytest.raises(DatosInvalidos,match='medición'):validar_datos(invalid,schema,completo=True)
        invalid['bloques'][title][result]='NA';validar_datos(invalid,schema,completo=True)
    assert data==original


@pytest.mark.parametrize('code',CODES)
def test_planilla_nueva_emision(app,client,code,referencias_etapa5):
    definition=definiciones_restantes()[code];row=crear_nueva(client,code);url=f"/api/cargas/{row['id']}"
    response=client.post(url+'/finalizar',json={'revision':row['revision']})
    assert response.status_code==200,response.get_json()
    response=client.post(url+'/emitir',json={'revision':response.get_json()['revision']})
    assert response.status_code==201,response.get_json()
    emitted=response.get_json()
    assert emitted['numero_registro']>0 and emitted['revision_publica']==0 and emitted['estado']=='emitida'
    pdf=client.get(url+'/pdf');assert pdf.status_code==200
    reader=PdfReader(BytesIO(pdf.data));assert reader.pages
    assert len(reader.pages)==referencias_etapa5[code]['paginas'],code
    all_text=''.join(''.join(page.extract_text().split()) for page in reader.pages)
    if code=='SG-PEM-IFI-SCC-1':
        assert 'MPa' not in all_text and 'bar' in all_text
    for title,items in definition['especificacion']['bloques']:
        assert ''.join(title.split()) in all_text,(code,title)
        for item in items:
            label=item[0] if isinstance(item,tuple) else item
            assert ''.join(label.split()) in all_text,(code,label)
    assert ''.join(definition['especificacion']['sistema'].split()) in all_text
    assert ''.join(definition['especificacion']['titulo'].upper().split()) in all_text
    assert 'T.C.3AÑOS' in all_text
    for page in reader.pages:
        assert abs(float(page.mediabox.width)-841.89)<.5 and abs(float(page.mediabox.height)-595.28)<.5
        assert 'Planilla conforme a IRAM 3546:2011' in page.extract_text()
        assert f"Registro {emitted['numero_registro']} | Revisión 0" in page.extract_text()
        assert len(page.images)>=2
    signatures=[str(name) for page in reader.pages for name in page['/Resources']['/XObject'] if str(name).startswith('/Firma_')]
    assert sorted(signatures)==['/Firma_responsable','/Firma_tecnico']
    assert reader.metadata['/Author']==reader.metadata['/Producer']=='readyproof'
    assert reader.metadata['/ReadyproofMarcaAgua']
    assert client.get(url+'/emisiones/0/pdf').data==pdf.data
    with Session(app.extensions['db_engine']) as db:
        stored=db.get(Carga,row['id']);archived=db.scalar(select(EmisionCarga).where(EmisionCarga.carga_id==row['id']))
        assert stored.pdf==archived.pdf==pdf.data
        assert stored.pdf_hash==stored.pdf_sha256==archived.pdf_sha256==sha256(pdf.data).hexdigest()
    output=Path(os.environ.get('READYPROOF_PDF_EVIDENCIA','out/etapa5_planillas/pdf')).resolve();output.mkdir(parents=True,exist_ok=True)
    (output/(code+'.pdf')).write_bytes(pdf.data)
