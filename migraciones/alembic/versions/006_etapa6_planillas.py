"""Cuatro manuales ficticios para el catálogo JSON, sin modificar el piloto anterior."""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa

revision="006_etapa6_planillas"
down_revision="005_correo_modelos"
branch_labels=None
depends_on=None

MANUALES={
    "SG-PEM-IFI-SAA-1":"[Ejemplo] Sistema de Abastecimiento de Agua",
    "SG-PEM-IFI-SDI":"[Ejemplo] Sistema de Detección de Incendios",
    "SG-PEM-IFI-SBC":"[Ejemplo] Sistema de Bombas Contraincendios",
    "SG-PEM-IFI-SAL":"[Ejemplo] Sistema de Extinción por Agentes Limpios",
}
CONTENIDO="[Ejemplo] Procedimiento..."


def tabla_manual():
    return sa.table("manuales",sa.column("id",sa.Uuid(as_uuid=False)),sa.column("codigo",sa.String),sa.column("titulo",sa.String),sa.column("sistema_tipo",sa.String),sa.column("contenido",sa.Text),sa.column("campos_obligatorios",sa.JSON),sa.column("version",sa.String))


def upgrade():
    manual=tabla_manual();connection=op.get_bind()
    if connection.execute(sa.select(manual.c.id).where(manual.c.codigo.in_(MANUALES))).first():
        raise RuntimeError("Los códigos de esta migración ya existen. Revisar antes de insertar; no se sobrescriben manuales.")
    for codigo,titulo in MANUALES.items():
        connection.execute(manual.insert().values(id=str(uuid4()),codigo=codigo,titulo=titulo,sistema_tipo="SG-PEM-IFI",contenido=CONTENIDO,campos_obligatorios=[],version="v1"))
    connection.execute(sa.text("INSERT INTO versiones_esquema (numero,aplicada_en) VALUES (6,CURRENT_TIMESTAMP)"))


def downgrade():
    manual=tabla_manual();connection=op.get_bind()
    rows=list(connection.execute(sa.select(manual).where(manual.c.codigo.in_(MANUALES))).mappings())
    if len(rows)!=len(MANUALES) or any(row["titulo"]!=MANUALES[row["codigo"]] or row["version"]!="v1" or row["sistema_tipo"]!="SG-PEM-IFI" or row["contenido"]!=CONTENIDO or row["campos_obligatorios"]!=[] for row in rows):
        raise RuntimeError("La reversión no puede borrar manuales alterados o ajenos a esta revisión.")
    planillas=sa.table("planillas",sa.column("manual_id",sa.Uuid(as_uuid=False)))
    ids=[row["id"] for row in rows]
    if connection.execute(sa.select(planillas.c.manual_id).where(planillas.c.manual_id.in_(ids))).first():
        raise RuntimeError("No se revierten manuales vinculados a planillas. Se conservan datos e historial.")
    connection.execute(manual.delete().where(manual.c.id.in_(ids)))
    connection.execute(sa.text("DELETE FROM versiones_esquema WHERE numero=6"))
