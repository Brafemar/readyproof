"""Carga de fotos: contenido, límites, persistencia y recorrido PWA."""
from hashlib import sha256
from io import BytesIO
import json
import os
from pathlib import Path
import shutil
import subprocess
from threading import Thread
from uuid import uuid4

from PIL import Image
import pytest
from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.serving import make_server

from app.models import Carga, FotoCarga, Auditoria


@pytest.fixture
def carga_foto(client, catalogo, datos_api):
    _, sistema, planilla = catalogo
    response=client.post('/api/cargas', json=dict(sistema_id=sistema['id'],planilla_id=planilla['id'],datos=datos_api))
    assert response.status_code==201,response.get_json()
    return response.get_json()['id']


def jpeg(size=(32,24), noise=False):
    image=Image.effect_noise(size,60).convert('RGB') if noise else Image.new('RGB',size,'white')
    output=BytesIO();image.save(output,format='JPEG',quality=90)
    return output.getvalue()


def subir(client,carga,data,**headers):
    return client.post(f'/api/cargas/{carga}/fotos',data=data,content_type='image/jpeg',headers=headers)


@pytest.mark.parametrize('data',[b'[Ejemplo] texto renombrado.jpg',b'\x89PNG\r\n\x1a\n',b'\xff\xd8\xffincompleto'])
def test_rechaza_contenido_no_jpeg(client,carga_foto,data):
    response=subir(client,carga_foto,data)
    assert response.status_code==400
    assert 'Formato no soportado: se acepta JPEG' in response.get_json()['error']
    assert client.get(f'/api/cargas/{carga_foto}/fotos').get_json()==[]


def test_rechaza_mas_de_dos_mb(client,carga_foto):
    response=subir(client,carga_foto,b'\xff\xd8\xff'+b'x'*(2*1024*1024-2))
    assert response.status_code==413
    assert response.get_json()['error']=='La foto supera 2 MB: vuelva a intentar con la foto de la app'


def test_rechaza_foto_21(app,client,carga_foto):
    data=jpeg()
    with Session(app.extensions['db_engine']) as db:
        db.add_all([FotoCarga(carga_id=carga_foto,orden=i,imagen=data,ancho=32,alto=24,sha256=sha256(data).hexdigest()) for i in range(1,21)])
        db.commit()
    response=subir(client,carga_foto,data)
    assert response.status_code==409 and '20 fotos' in response.get_json()['error']
    assert len(client.get(f'/api/cargas/{carga_foto}/fotos').get_json())==20


def test_acepta_jpeg_y_guarda_dimensiones_y_actor(app,client,carga_foto,usuario_admin):
    response=subir(client,carga_foto,jpeg())
    assert response.status_code==201,response.get_json()
    result=response.get_json()
    assert (result['ancho'],result['alto'],result['orden'])==(32,24,1)
    with Session(app.extensions['db_engine']) as db:
        foto=db.get(FotoCarga,result['id'])
        assert foto.creado_por_id==usuario_admin['id']
        audit=db.scalar(select(Auditoria).where(Auditoria.registro_id==foto.id,Auditoria.tabla=='foto_carga'))
        assert audit and audit.accion=='INSERT'


def test_orden_consecutivo_sin_huecos(client,carga_foto):
    for i in range(1,4):
        response=subir(client,carga_foto,jpeg((32+i,24)))
        assert response.status_code==201 and response.get_json()['orden']==i
    assert [row['orden'] for row in client.get(f'/api/cargas/{carga_foto}/fotos').get_json()]==[1,2,3]


def test_sha256_corresponde_exactamente_a_bytes_guardados(app,client,carga_foto):
    data=jpeg();result=subir(client,carga_foto,data).get_json()
    with Session(app.extensions['db_engine']) as db:
        row=db.get(FotoCarga,result['id'])
        assert bytes(row.imagen)==data
        assert row.sha256==result['sha256']==sha256(bytes(row.imagen)).hexdigest()


def test_acepta_foto_mayor_que_limite_general(app,client,carga_foto):
    data=jpeg((1400,1400),noise=True)
    assert 768*1024<len(data)<=2*1024*1024
    assert app.config['MAX_CONTENT_LENGTH']==768*1024
    assert subir(client,carga_foto,data).status_code==201


@pytest.mark.parametrize('estado',['finalizada','emitida'])
def test_bloquea_subida_fuera_de_borrador(app,client,carga_foto,estado):
    with Session(app.extensions['db_engine']) as db:
        db.get(Carga,carga_foto).estado=estado;db.commit()
    response=subir(client,carga_foto,jpeg())
    assert response.status_code==409 and 'desbloqueo' in response.get_json()['error']


def test_reintento_no_duplica_la_foto(client,carga_foto):
    key=str(uuid4());data=jpeg()
    first=subir(client,carga_foto,data,**{'Idempotency-Key':key})
    second=subir(client,carga_foto,data,**{'Idempotency-Key':key})
    assert first.status_code==201 and second.status_code==200
    assert first.get_json()==second.get_json()
    assert len(client.get(f'/api/cargas/{carga_foto}/fotos').get_json())==1


def test_fotos_exigen_sesion(app,carga_foto):
    assert subir(app.test_client(),carga_foto,jpeg()).status_code==401


def test_fotos_exigen_csrf(client,carga_foto):
    assert subir(client,carga_foto,jpeg(),**{'X-CSRF-Token':'invalido'}).status_code==403


def test_canvas_offline_y_jpeg_sin_metadatos(app,usuario_admin):
    node=os.environ.get('READYPROOF_NODE') or shutil.which('node');assert node
    out=Path('out/fotos_c2/navegador').resolve();out.mkdir(parents=True,exist_ok=True)
    source=out/'foto_ficticia_original.jpg'
    image=Image.effect_noise((2400,1800),60).convert('RGB')
    exif=Image.Exif();exif[270]='[Ejemplo] metadatos';exif[34853]={1:'N',2:(1.,2.,3.),3:'E',4:(1.,2.,3.)}
    image.save(source,format='JPEG',quality=95,exif=exif)
    assert Image.open(source).getexif().get(34853)
    server=make_server('127.0.0.1',0,app,threaded=True)
    thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    env=dict(os.environ,RP_URL=f'http://127.0.0.1:{server.server_port}',RP_OUT=str(out),RP_LOGIN=usuario_admin['login'],RP_PASSWORD=usuario_admin['clave'],RP_FOTO=str(source))
    try:
        result=subprocess.run([node,'tests/browser/fotos_c2.cjs'],env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
        assert result.returncode==0,result.stdout+result.stderr
        report=json.loads((out/'resultado.json').read_text(encoding='utf-8'))
        with Session(app.extensions['db_engine']) as db:
            rows=list(db.scalars(select(FotoCarga).where(FotoCarga.carga_id==report['carga_id']).order_by(FotoCarga.orden)))
            assert len(rows)==2 and [row.orden for row in rows]==[1,2]
            for row in rows:
                with Image.open(BytesIO(row.imagen)) as saved:
                    assert saved.format=='JPEG' and saved.size==(1600,1200) and not saved.getexif()
                assert len(row.imagen)<=2*1024*1024 and sha256(row.imagen).hexdigest()==row.sha256
            report.update(bytes_antes=source.stat().st_size,bytes_despues=len(rows[0].imagen),ancho=rows[0].ancho,alto=rows[0].alto,exif_gps_eliminado=True)
            (out/'resultado.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            assert report['bytes_despues']<report['bytes_antes']
    finally:
        server.shutdown();thread.join(timeout=10)
