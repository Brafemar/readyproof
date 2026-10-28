"""Activación completa de las cuatro familias, formularios y PDF por planilla."""
from base64 import b64decode
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from io import BytesIO
import json,os,shutil,subprocess
from pathlib import Path
from threading import Thread

import pytest
from openpyxl import load_workbook
from pypdf import PdfReader
from sqlalchemy import select,func
from sqlalchemy.orm import Session
from werkzeug.serving import make_server

from app.models import Planilla,Carga
from app.planillas.multisistema import definiciones_multisistema,ejemplo_multisistema,cargar_multisistema
from app.planillas.generador import generar_multisistema
from scripts.prueba_operativa_final import firma_ficticia

from app.planillas.firmantes import ejemplo_responsable

CODES=sorted(definiciones_multisistema())


def test_todas_planillas_cargan(app,client,catalogo):
    offered=client.get('/api/planillas').get_json()
    assert len(offered)==79
    assert Counter(row['sistema_tipo'] for row in offered)==dict(SAA=6,SDI=5,SBC=6,SAL=4,SAP=5,SCC=5,SDC=5,SEP=3,SGE=7,SHC=3,SIM=2,SRA=9,SRE=7,SSA=4,STM=8)
    systems=client.get('/api/clientes/'+catalogo[0]['id']+'/sistemas').get_json()
    assert {row['tipo'] for row in systems}==set(__import__('app.config',fromlist=['SISTEMAS_HABILITADOS']).SISTEMAS_HABILITADOS)
    with Session(app.extensions['db_engine']) as db:
        assert db.scalar(select(func.count()).select_from(Planilla))==83
        for row in offered:
            if row['codigo'] not in CODES:continue
            p=db.get(Planilla,row['id']);assert p.manual.codigo=='SG-PEM-IFI-'+row['sistema_tipo']
    with app.extensions['db_engine'].begin() as connection:cargar_multisistema(connection)
    assert len(client.get('/api/planillas').get_json())==79


@pytest.mark.parametrize('code',CODES)
def test_pdf_sdi_sbc_sal_genera(app,client,catalogo,code,tmp_path):
    definition=definiciones_multisistema()[code]
    sheet=next(row for row in client.get('/api/planillas').get_json() if row['codigo']==code)
    system=next(row for row in client.get('/api/clientes/'+catalogo[0]['id']+'/sistemas').get_json() if row['tipo']==definition['familia'])
    data=ejemplo_multisistema(definition['definicion']);data['cabecera']['cliente']=catalogo[0]['nombre'];data['cabecera']['sistema_designacion']=system['designacion']
    signatures={'tecnico':firma_ficticia(),'responsable':firma_ficticia(25)}
    response=client.post('/api/cargas',json=dict(sistema_id=system['id'],planilla_id=sheet['id'],datos=data,firmas=signatures,responsable=ejemplo_responsable()))
    assert response.status_code==201,response.get_json()
    record=response.get_json();url='/api/cargas/'+record['id']
    invalid=deepcopy(data);title=next(iter(invalid['bloques']));invalid['bloques'][title]['inventado']='[Ejemplo] No válido'
    assert client.put(url+'/borrador',json=dict(revision=record['revision'],datos=invalid)).status_code==422
    record=client.post(url+'/finalizar',json=dict(revision=record['revision'])).get_json()
    emitted=client.post(url+'/emitir',json=dict(revision=record['revision']))
    assert emitted.status_code==201,emitted.get_json()
    pdf=client.get(url+'/pdf');assert pdf.status_code==200
    assert code.removeprefix('SG-PEM-IFI-') in pdf.headers['Content-Disposition']
    reader=PdfReader(BytesIO(pdf.data));assert reader.pages
    text=''.join(''.join(page.extract_text().split()) for page in reader.pages)
    for title,items in definition['especificacion']['bloques']:
        assert ''.join(title.split()) in text
        for item in items:
            label=item[0] if isinstance(item,tuple) else item
            assert ''.join(label.split()) in text,(code,label)
    assert 'T.C.3AÑOS' in text
    for page in reader.pages:
        assert abs(float(page.mediabox.width)-841.89)<.5 and abs(float(page.mediabox.height)-595.28)<.5
        assert 'Planilla conforme a IRAM 3546:2011' in page.extract_text()
        assert len(page.images)>=2
    assert sum(sum(str(name).startswith('/Firma_') for name in page['/Resources']['/XObject']) for page in reader.pages)==2
    assert reader.metadata['/Author']==reader.metadata['/Producer']=='readyproof'
    assert any('/Firma_tecnico' in page['/Resources']['/XObject'] for page in reader.pages)
    assert any('/Firma_responsable' in page['/Resources']['/XObject'] for page in reader.pages)
    assert reader.metadata['/ReadyproofMarcaAgua']
    from app.planillas.leyenda_iram import PIE_PT,TAMANIO
    escala=float(reader.metadata['/ReadyproofAjustePie'].split(';')[0].split()[-1])
    positions=[]
    for page in reader.pages:
        def operand(op,args,cm,tm):
            if op==b'Do' and str(args[0]).startswith('/Firma_'):
                positions.append((str(args[0]),list(cm),float(page.mediabox.height)))
        page.extract_text(visitor_operand_before=operand)
    assert {name for name,cm,height in positions}=={'/Firma_tecnico','/Firma_responsable'}
    for name,cm,height in positions:
        top=(height-.98425*72)*escala+(1-escala)*(height-8)
        assert cm[5]>PIE_PT+TAMANIO+2
        assert cm[5]+cm[3]<top,(code,name,cm)

    # El Excel conserva todos los rótulos y solo completa las celdas del kit.
    excel=generar_multisistema(data,tmp_path/'carga.xlsx',code)
    workbook=load_workbook(excel);worksheet=workbook.active
    for title,fields in definition['definicion']['bloques'].items():
        for key,field in fields.items():
            coordinate=field.get('celda') or field['celdas_resultado']['✓']
            assert worksheet[coordinate].value is not None
    out=Path('out/multisistema/pdf');out.mkdir(parents=True,exist_ok=True)
    (out/(code+'.pdf')).write_bytes(pdf.data)
    with Session(app.extensions['db_engine']) as db:
        saved=db.get(Carga,record['id']);assert saved.pdf_sha256==sha256(pdf.data).hexdigest()


def test_selectores_funcionan(app,usuario_admin):
    server=make_server('127.0.0.1',0,app,threaded=True);thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    out=Path('out/multisistema/navegador').resolve();out.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,RP_URL=f'http://127.0.0.1:{server.server_port}',RP_OUT=str(out),RP_LOGIN=usuario_admin['login'],RP_PASSWORD=usuario_admin['clave'])
    try:
        result=subprocess.run([shutil.which('node'),'tests/browser/multisistema.cjs'],env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=600)
        assert result.returncode==0,result.stdout+result.stderr
        assert json.loads((out/'resultado.json').read_text())['formularios']==79
    finally:server.shutdown();thread.join(timeout=10)


def test_documentacion_incluye_cuatro_sistemas(app,client,monkeypatch,tmp_path):
    app.config.update(DOCUMENTACION_MODO_PRUEBA=True,DIRECTORIO_CORREO=str(tmp_path/'correo'))
    assert client.put('/api/usuario/correo',json={'email':'tecnico@example.invalid'}).status_code==200
    result=client.post('/api/usuario/enviar-documentacion');assert result.status_code==200
    from app.models import EnvioDocumentacion
    from email import policy
    from email.parser import BytesParser
    with Session(app.extensions['db_engine']) as db:
        mail=BytesParser(policy=policy.default).parsebytes(db.get(EnvioDocumentacion,result.get_json()['solicitud_id']).mensaje_eml)
        body=mail.get_body(preferencelist=('plain',)).get_content()
        assert '79 planillas' in body
        from app.config import SISTEMAS_HABILITADOS
        assert all(code+':' in body for code in SISTEMAS_HABILITADOS)
