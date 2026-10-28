"""La interfaz conserva una emisión histórica y crea su copia A4 mediante la API."""
import json,os,shutil,subprocess
from pathlib import Path
from threading import Thread
from io import BytesIO
from base64 import b64decode
from uuid import uuid4
from pypdf import PdfWriter,PdfReader
from sqlalchemy.orm import Session
from werkzeug.serving import make_server
from app.models import Planilla,Carga,FirmaCarga,ahora
from app.catalogo import VERSION_PILOTO
from scripts.prueba_operativa_final import firma_ficticia


def test_copia_a4_conserva_pdf_anterior(app,usuario_admin,catalogo,datos_api):
    writer=PdfWriter();writer.add_blank_page(width=841.89,height=595.28);writer.add_blank_page(width=841.89,height=595.28)
    buffer=BytesIO();writer.write(buffer);previous_pdf=buffer.getvalue()
    signatures={'tecnico':firma_ficticia(),'responsable':firma_ficticia(25)}
    with Session(app.extensions['db_engine']) as db:
        current=db.get(Planilla,catalogo[2]['id'])
        old=Planilla(codigo=current.codigo,version='ejemplo-anterior-A4',sistema_tipo=current.sistema_tipo,
                    huella='a'*64,definicion=current.definicion,manual_id=current.manual_id)
        db.add(old);db.flush()
        record=Carga(sistema_id=catalogo[1]['id'],planilla_id=old.id,creada_por_id=usuario_admin['id'],datos=datos_api,
                     estado='emitida',emitida_en=ahora(),pdf=previous_pdf)
        db.add(record);db.flush()
        db.add(FirmaCarga(carga_id=record.id,tecnico_png=b64decode(signatures['tecnico'].split(',')[1]),responsable_png=b64decode(signatures['responsable'].split(',')[1])))
        legacy=dict(localId=record.id,clienteId=catalogo[0]['id'],sistemaId=record.sistema_id,planillaId=old.id,
                    serverId=record.id,revision=record.revision,estado='emitida',datos=datos_api,firmas=signatures,
                    firmasServidor={'tecnico':True,'responsable':True},pending=False,conflicto=False,editVersion=0,
                    actualizado='2026-10-26T00:00:00Z')
        db.commit();previous_id=record.id
    server=make_server('127.0.0.1',0,app,threaded=True);thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    out=Path('out/a4_una_hoja/historica').resolve();out.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,RP_URL=f'http://127.0.0.1:{server.server_port}',RP_OUT=str(out),RP_LOGIN=usuario_admin['login'],
             RP_PASSWORD=usuario_admin['clave'],RP_HISTORICA=json.dumps(legacy))
    try:
        result=subprocess.run([shutil.which('node'),'tests/browser/a4_historica.cjs'],env=env,capture_output=True,text=True,
                              encoding='utf-8',errors='replace',timeout=150)
        assert result.returncode==0,result.stdout+result.stderr
        report=json.loads((out/'resultado.json').read_text())
        with Session(app.extensions['db_engine']) as db:
            assert db.get(Carga,previous_id).pdf==previous_pdf
            emitted=db.get(Carga,report['carga_id'])
            assert emitted.id!=previous_id and emitted.estado=='emitida'
            assert db.get(Planilla,emitted.planilla_id).version==VERSION_PILOTO
            assert len(PdfReader(BytesIO(emitted.pdf)).pages)==1
            assert len(PdfReader(BytesIO(emitted.pdf)).pages[0].images)==4
    finally:server.shutdown();thread.join(timeout=10)
