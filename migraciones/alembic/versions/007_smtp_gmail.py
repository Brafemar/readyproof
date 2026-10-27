"""Copia de correo, actor y reserva durable de los tres intentos máximos."""
from alembic import op
import sqlalchemy as sa

revision = "007_smtp_gmail"
down_revision = "006_etapa6_planillas"
branch_labels = None
depends_on = None


def upgrade():
    for column in (
        sa.Column("usuario_id", sa.String(36), sa.ForeignKey("usuarios.id")),
        sa.Column("asunto", sa.String(200)), sa.Column("cuerpo", sa.Text),
        sa.Column("pdf_copia", sa.LargeBinary), sa.Column("pdf_sha256", sa.String(64)),
        sa.Column("mensaje_eml", sa.LargeBinary), sa.Column("eml_sha256", sa.String(64)),
        sa.Column("retener_hasta", sa.DateTime(timezone=True)),
        sa.Column("intentos_reservados", sa.Integer, nullable=False, server_default="0"),
        sa.Column("en_proceso_desde", sa.DateTime(timezone=True)),
    ):
        op.add_column("envios", column)
    op.create_check_constraint("ck_envio_max_intentos", "envios", "intentos_reservados BETWEEN 0 AND 3")
    # Los registros anteriores conservan sus datos y no se habilitan para SMTP.
    op.execute("UPDATE envios SET intentos_reservados=LEAST(3, COALESCE((SELECT MAX(numero) FROM intentos WHERE envio_id=envios.id),0))")
    op.execute("INSERT INTO versiones_esquema (numero,aplicada_en) VALUES (7,CURRENT_TIMESTAMP)")


def downgrade():
    if op.get_bind().execute(sa.text("SELECT 1 FROM envios LIMIT 1")).first():
        raise RuntimeError("No se revierte la copia de correo mientras existan envíos.")
    op.drop_constraint("ck_envio_max_intentos", "envios", type_="check")
    for name in ("en_proceso_desde", "intentos_reservados", "retener_hasta", "eml_sha256", "mensaje_eml", "pdf_sha256", "pdf_copia", "cuerpo", "asunto", "usuario_id"):
        op.drop_column("envios", name)
    op.execute("DELETE FROM versiones_esquema WHERE numero=7")
