import base64
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw
from pypdf import PdfReader
import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import crear_esquema
from app.models import FirmaCarga, VersionEsquema, RegistroAcceso
from sqlalchemy import select
from tests.test_api import crear
from app.planillas.firmantes import ejemplo_responsable


def firma_ejemplo():
    image = Image.new("RGBA", (1000,280), (255,255,255,0))
    ImageDraw.Draw(image).line([(130,210),(230,65),(255,220),(350,120),(460,190),(620,100),(780,175)], fill=(20,35,40,255), width=5)
    output=BytesIO();image.save(output,format="PNG")
    return "data:image/png;base64,"+base64.b64encode(output.getvalue()).decode("ascii")


def test_pantalla_y_definicion_conservan_orden(client,catalogo):
    response=client.get("/")
    assert response.status_code==200 and b"indexedDB" not in response.data
    assert b"Firmas de prueba" in response.data
    schema=client.get(f"/api/planillas/{catalogo[2]['id']}").get_json()["definicion"]
    assert list(schema["bloques"])==["INSTALACIÓN","ABASTECIMIENTO DE AGUA","BOMBAS CONTRA INCENDIO (CAPÍTULO 12)","TOMA DE IMPULSIÓN PARA BOMBEROS"]
    assert client.get("/sw.js").headers["Service-Worker-Allowed"]=="/"
    assert client.get("/",environ_overrides={"REMOTE_ADDR":"192.0.2.1"}).status_code==403


@pytest.mark.parametrize("firmas",[{"otro":None},{"tecnico":"datos"},{"tecnico":"data:image/png;base64,%%%"},{"tecnico":1234}])
def test_firma_invalida_no_crea_carga(client,catalogo,datos_api,firmas):
    _,sistema,planilla=catalogo
    assert client.post("/api/cargas",json={"sistema_id":sistema["id"],"planilla_id":planilla["id"],"datos":datos_api,"firmas":firmas}).status_code==422


def test_firmas_guardadas_no_se_exponen_como_imagen(client,catalogo,datos_api,app):
    _,sistema,planilla=catalogo
    firma=firma_ejemplo()
    response=client.post("/api/cargas",json={"sistema_id":sistema["id"],"planilla_id":planilla["id"],"datos":datos_api,"firmas":{"tecnico":firma}})
    assert response.status_code==201
    carga=response.get_json()
    assert carga["revision"]==1 and carga["firmas"]=={"tecnico":True,"responsable":False}
    assert "base64" not in response.get_data(as_text=True)
    with Session(app.extensions["db_engine"]) as session:
        assert session.get(FirmaCarga,carga["id"]).tecnico_png.startswith(b"\x89PNG")
    result=client.put(f"/api/cargas/{carga['id']}/borrador",json={"revision":1,"datos":datos_api,"firmas":{"tecnico":None}})
    assert result.status_code==200 and result.get_json()["firmas"]["tecnico"] is False
    history=client.get(f"/api/cargas/{carga['id']}/revisiones").get_json()
    assert history[0]["firmas_huellas"]["tecnico"] and history[1]["firmas_huellas"]["tecnico"] is None


def test_vista_previa_no_finaliza_e_incorpora_firmas(client,catalogo,datos_api):
    _,sistema,planilla=catalogo
    firma=firma_ejemplo()
    carga=client.post("/api/cargas",json={"sistema_id":sistema["id"],"planilla_id":planilla["id"],"datos":datos_api,"firmas":{"tecnico":firma,"responsable":firma},"responsable":ejemplo_responsable()}).get_json()
    response=client.post(f"/api/cargas/{carga['id']}/vista-previa",json={"revision":1})
    assert response.status_code==200, response.get_data(as_text=True)[:300] if response.status_code!=200 else ""
    reader=PdfReader(BytesIO(response.data))
    assert len(reader.pages)==1
    from tests.test_marca_agua import verificar_marca_agua
    verificar_marca_agua(reader)
    assert [len(page.images) for page in reader.pages]==[4]
    after=client.get(f"/api/cargas/{carga['id']}").get_json()
    assert after["revision"]==1 and after["estado"]=="borrador" and not after["pdf_disponible"]
    out=Path("out/etapa3");out.mkdir(parents=True,exist_ok=True)
    (out/"vista_previa_firmada.pdf").write_bytes(response.data)
    assert client.post(f"/api/cargas/{carga['id']}/finalizar",json={"revision":1}).status_code==200
    emitted=client.post(f"/api/cargas/{carga['id']}/emitir",json={"revision":2})
    assert emitted.status_code==201
    pdf=client.get(f"/api/cargas/{carga['id']}/pdf")
    assert [len(page.images) for page in PdfReader(BytesIO(pdf.data)).pages]==[4]
    verificar_marca_agua(PdfReader(BytesIO(pdf.data)))
    with Session(client.application.extensions["db_engine"]) as db:
        audit=db.scalar(select(RegistroAcceso).where(RegistroAcceso.evento=="emision",RegistroAcceso.carga_id==carga["id"]))
        assert audit and audit.usuario_id and audit.planilla_codigo=="SG-PEM-IFI-SAA-1"
        assert audit.destinatario is None



def test_creacion_con_identificador_local_no_duplica(client,catalogo,datos_api):
    from uuid import uuid4
    key=str(uuid4());_,sistema,planilla=catalogo
    payload={"sistema_id":sistema["id"],"planilla_id":planilla["id"],"datos":datos_api}
    first=client.post("/api/cargas",json=payload,headers={"Idempotency-Key":key})
    second=client.post("/api/cargas",json=payload,headers={"Idempotency-Key":key})
    assert first.status_code==201 and second.status_code==200
    assert first.get_json()["id"]==second.get_json()["id"]==key
    assert len(client.get(f"/api/cargas/{key}/revisiones").get_json())==1


def test_migracion_aditiva_conserva_datos(client,catalogo,datos_api,app):
    carga=crear(client,catalogo,datos_api).get_json()
    engine=app.extensions["db_engine"]
    from alembic import command
    from alembic.config import Config
    from pathlib import Path
    with engine.begin() as connection:
        cfg=Config(str(Path(__file__).resolve().parents[1]/'alembic.ini'));cfg.attributes['connection']=connection
        command.downgrade(cfg,'013_desbloqueo_revision')
        connection.execute(text("DROP TABLE emisiones_carga"))
        connection.execute(text("DROP FUNCTION proteger_emision_readyproof()"))
        connection.execute(text("DROP TABLE numero_registro_contador"))
        for column in ('numero_registro','revision_publica','pdf_hash','desbloqueado_por','motivo_desbloqueo','estado_anulada'):
            connection.execute(text('ALTER TABLE cargas DROP COLUMN '+column))
        connection.execute(text("DELETE FROM versiones_esquema WHERE numero=13"))
        connection.execute(text("DROP TABLE firmas_carga"))
        connection.execute(text("ALTER TABLE revisiones_carga DROP COLUMN firmas_huellas"))
        connection.execute(text("DELETE FROM versiones_esquema WHERE numero=2"))
        # La simulación anterior a firmas tampoco incluye la ampliación 010.
        connection.execute(text("ALTER TABLE revisiones_carga DROP COLUMN firmantes"))
        connection.execute(text("DELETE FROM versiones_esquema WHERE numero=10"))
        # Al simular 009, retirar también las ampliaciones posteriores de clientes y sistemas.
        connection.execute(text("ALTER TABLE clientes DROP COLUMN cuit CASCADE"))
        connection.execute(text("ALTER TABLE sistemas DROP COLUMN activo"))
        connection.execute(text("DELETE FROM versiones_esquema WHERE numero IN (11,12)"))
        connection.execute(text("UPDATE alembic_version SET version_num='009_multisistema'"))
    crear_esquema(engine)
    assert client.get(f"/api/cargas/{carga['id']}").get_json()["datos"]==carga["datos"]
    with Session(engine) as session:
        assert session.get(VersionEsquema,2) is not None
