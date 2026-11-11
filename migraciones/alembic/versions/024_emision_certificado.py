"""Archivo de certificados emitidos y permiso inicial asignado por cuenta."""
from alembic import op
import sqlalchemy as sa

revision = "024_emision_certificado"
down_revision = "023_firma_certificado"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "emisiones_certificado",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("actor_id", sa.String(36), sa.ForeignKey("usuarios.id"), nullable=False),
        sa.Column("cliente_id", sa.String(36), sa.ForeignKey("clientes.id"), nullable=False),
        sa.Column("condicion", sa.String(11), nullable=False),
        sa.Column("fecha_emision", sa.Date(), nullable=False),
        sa.Column("emitido_en", sa.DateTime(timezone=True), nullable=False),
        sa.Column("pdf", sa.LargeBinary(), nullable=False),
        sa.Column("pdf_sha256", sa.String(64), nullable=False),
        sa.Column("planillas", sa.JSON(), nullable=False),
        sa.CheckConstraint("condicion IN ('APROBADO', 'NO APROBADO')", name="ck_emision_certificado_condicion"),
    )
    op.execute(sa.text("""
        UPDATE usuarios SET certificado_conjunto = true
        WHERE id = (
            SELECT min(id) FROM usuarios
            WHERE lower(trim(email)) = :correo
            HAVING count(*) = 1
        )
    """).bindparams(correo="readyproof.ar@gmail.com"))


def downgrade():
    if op.get_bind().scalar(sa.text("SELECT EXISTS (SELECT 1 FROM emisiones_certificado)")):
        raise RuntimeError("No se eliminan certificados emitidos.")
    op.drop_table("emisiones_certificado")
