"""Manuales de ejemplo y vínculo nullable con las planillas existentes."""
from uuid import uuid4
from alembic import op
import sqlalchemy as sa

revision="004_manual"
down_revision="003_base_etapa4"
branch_labels=None
depends_on=None


def upgrade():
    op.create_table("manuales",
        sa.Column("id",sa.Uuid(as_uuid=False),primary_key=True),
        sa.Column("codigo",sa.String(60),nullable=False),
        sa.Column("titulo",sa.String(255),nullable=False),
        sa.Column("sistema_tipo",sa.String(12),nullable=False),
        sa.Column("contenido",sa.Text(),nullable=False),
        sa.Column("campos_obligatorios",sa.JSON(),nullable=False),
        sa.Column("version",sa.String(30),nullable=False),
        sa.UniqueConstraint("codigo",name="uq_manual_codigo"),
        sa.UniqueConstraint("codigo","version",name="uq_manual_codigo_version"))
    op.add_column("planillas",sa.Column("manual_id",sa.Uuid(as_uuid=False),nullable=True))
    op.create_foreign_key("fk_planilla_manual","planillas","manuales",["manual_id"],["id"])
    manual=sa.table("manuales",sa.column("id",sa.Uuid(as_uuid=False)),sa.column("codigo",sa.String),sa.column("titulo",sa.String),sa.column("sistema_tipo",sa.String),sa.column("contenido",sa.Text),sa.column("campos_obligatorios",sa.JSON),sa.column("version",sa.String))
    key=str(uuid4())
    op.get_bind().execute(manual.insert().values(id=key,codigo="SG-PEM-IFI-SAA-EJEMPLO",titulo="[Ejemplo] Sistema de Abastecimiento de Agua",sistema_tipo="SAA",contenido="[Ejemplo] Contenido de prueba. Procedimiento y campos obligatorios pendientes de confirmación técnica.",campos_obligatorios=[],version="v1"))
    op.get_bind().execute(sa.text("UPDATE planillas SET manual_id=:key WHERE codigo='SG-PEM-IFI-SAA-1' AND sistema_tipo='SAA' AND manual_id IS NULL"),{"key":key})
    op.get_bind().execute(sa.text("INSERT INTO versiones_esquema (numero, aplicada_en) VALUES (4,CURRENT_TIMESTAMP) ON CONFLICT (numero) DO NOTHING"))


def downgrade():
    raise RuntimeError("La migración es aditiva; no se borran manuales ni relaciones.")
