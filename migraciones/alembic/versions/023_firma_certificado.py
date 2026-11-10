"""Puntero transaccional a la versión activa de la firma gráfica."""
from alembic import op
import sqlalchemy as sa

revision = "023_firma_certificado"
down_revision = "022_certificado_conjunto"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "firma_certificado_activa",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column("tamano", sa.Integer(), nullable=False),
        sa.Column("actualizada_en", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("id = 1", name="ck_firma_certificado_unica"),
    )


def downgrade():
    op.drop_table("firma_certificado_activa")
