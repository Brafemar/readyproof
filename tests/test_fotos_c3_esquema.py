"""Restricciones de anotaciones en PostgreSQL: modelo y migración 019."""
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from alembic.migration import MigrationContext
from alembic.operations import Operations
from PIL import Image
import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import Session

from app.models import FotoAnotacion, FotoCarga


@pytest.fixture(params=["modelo", "migracion019"])
def esquema_anotaciones(request, database_url):
    engine = create_engine(database_url)
    try:
        # Solo dependencias de claves foráneas; las tablas de fotos son las reales.
        with engine.begin() as connection:
            connection.execute(text("CREATE TABLE cargas (id VARCHAR(36) PRIMARY KEY)"))
            connection.execute(text("CREATE TABLE usuarios (id VARCHAR(36) PRIMARY KEY)"))
            if request.param == "modelo":
                FotoCarga.__table__.create(connection)
                FotoAnotacion.__table__.create(connection)
            else:
                connection.execute(text("CREATE TABLE versiones_esquema (numero INTEGER PRIMARY KEY, aplicada_en TIMESTAMPTZ NOT NULL)"))
                path = Path(__file__).resolve().parents[1] / "migraciones/alembic/versions/019_fotos_carga.py"
                spec = spec_from_file_location("fotos_migracion019", path)
                migration = module_from_spec(spec)
                spec.loader.exec_module(migration)
                assert migration.revision == "019_fotos_carga"
                assert migration.down_revision == "017_scc1_presion_bar"
                with Operations.context(MigrationContext.configure(connection)):
                    migration.upgrade()
                assert connection.scalar(text("SELECT numero FROM versiones_esquema")) == 19
            carga_id = str(uuid4())
            connection.execute(text("INSERT INTO cargas (id) VALUES (:id)"), {"id": carga_id})
        image = BytesIO()
        Image.new("RGB", (1, 1), "white").save(image, format="JPEG")
        jpeg = image.getvalue()
        with Session(engine) as db:
            foto = FotoCarga(carga_id=carga_id, orden=1, imagen=jpeg, ancho=1, alto=1, sha256=sha256(jpeg).hexdigest())
            db.add(foto)
            db.commit()
            foto_id = foto.id
        yield engine, foto_id
    finally:
        engine.dispose()


def guardar(esquema, codigo, texto):
    engine, foto_id = esquema
    with Session(engine) as db:
        row = FotoAnotacion(foto_id=foto_id, numero=1, x=0.25, y=0.75, codigo=codigo, texto=texto)
        db.add(row)
        db.commit()
        saved = db.get(FotoAnotacion, row.id)
        assert (saved.codigo, saved.texto, saved.x, saved.y) == (codigo, texto, 0.25, 0.75)


def test_codigo_fuera_de_lista_rechazado(esquema_anotaciones):
    with pytest.raises(IntegrityError) as error:
        guardar(esquema_anotaciones, "Z", "[Ejemplo] Observación")
    assert error.value.orig.sqlstate == "23514"
    assert error.value.orig.diag.constraint_name == "ck_anotacion_codigo"


@pytest.mark.parametrize("codigo", ["✓", "O", "X", "NA"])
def test_texto_vacio_segun_codigo(esquema_anotaciones, codigo):
    if codigo in ("✓", "NA"):
        guardar(esquema_anotaciones, codigo, "")
    else:
        with pytest.raises(IntegrityError) as error:
            guardar(esquema_anotaciones, codigo, "")
        assert error.value.orig.sqlstate == "23514"
        assert error.value.orig.diag.constraint_name == "ck_anotacion_texto"


@pytest.mark.parametrize("codigo", ["✓", "O", "X", "NA"])
def test_texto_140_caracteres_aceptado(esquema_anotaciones, codigo):
    guardar(esquema_anotaciones, codigo, "[Ejemplo] " + "á" * 130)


@pytest.mark.parametrize("codigo", ["✓", "O", "X", "NA"])
def test_texto_141_caracteres_rechazado(esquema_anotaciones, codigo):
    with pytest.raises((DataError, IntegrityError)) as error:
        guardar(esquema_anotaciones, codigo, "[Ejemplo] " + "á" * 131)
    assert error.value.orig.sqlstate in ("22001", "23514")


def test_codigo_string_dos_y_no_nulo(esquema_anotaciones):
    engine, _ = esquema_anotaciones
    column = next(c for c in inspect(engine).get_columns("fotos_anotacion") if c["name"] == "codigo")
    assert column["type"].length == 2
    assert column["nullable"] is False
    constraints = {c["name"] for c in inspect(engine).get_check_constraints("fotos_anotacion")}
    assert {"ck_anotacion_codigo", "ck_anotacion_texto"} <= constraints
    with pytest.raises(IntegrityError) as error:
        guardar(esquema_anotaciones, None, "[Ejemplo] Observación")
    assert error.value.orig.sqlstate == "23502"
