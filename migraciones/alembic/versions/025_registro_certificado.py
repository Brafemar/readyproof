"""Correlativo compartido y revisiones del certificado emitido."""
from alembic import op
import sqlalchemy as sa

revision = "025_registro_certificado"
down_revision = "024_emision_certificado"
branch_labels = None
depends_on = None

TABLA = "emisiones_certificado"


def upgrade():
    op.add_column(TABLA, sa.Column("numero_registro", sa.Integer(), nullable=True))
    op.add_column(TABLA, sa.Column("revision", sa.Integer(), nullable=True))
    db = op.get_bind()
    ultimo = db.execute(sa.text(
        "SELECT ultimo FROM numero_registro_contador WHERE id = 1 FOR UPDATE"
    )).scalar_one()
    asignadas = db.execute(sa.text("""
        WITH ordenadas AS (
            SELECT id, row_number() OVER (ORDER BY emitido_en, id) AS orden
            FROM emisiones_certificado
        )
        UPDATE emisiones_certificado AS emision
        SET numero_registro = :ultimo + ordenadas.orden, revision = 1
        FROM ordenadas
        WHERE emision.id = ordenadas.id
    """), {"ultimo": ultimo}).rowcount
    if asignadas:
        db.execute(sa.text("UPDATE numero_registro_contador SET ultimo = :ultimo WHERE id = 1"),
                   {"ultimo": ultimo + asignadas})
    op.alter_column(TABLA, "numero_registro", nullable=False)
    op.alter_column(TABLA, "revision", nullable=False)
    op.create_check_constraint("ck_emision_certificado_numeracion", TABLA,
                               "numero_registro > 0 AND revision > 0")
    op.create_unique_constraint("uq_emision_certificado_registro_revision", TABLA,
                                ["numero_registro", "revision"])


def downgrade():
    if op.get_bind().scalar(sa.text("SELECT EXISTS (SELECT 1 FROM emisiones_certificado)")):
        raise RuntimeError("No se elimina la numeración de certificados emitidos.")
    op.drop_constraint("uq_emision_certificado_registro_revision", TABLA, type_="unique")
    op.drop_constraint("ck_emision_certificado_numeracion", TABLA, type_="check")
    op.drop_column(TABLA, "revision")
    op.drop_column(TABLA, "numero_registro")
