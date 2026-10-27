"""Envíos, intentos y programación de reintentos, sin transmisión SMTP."""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision="005_correo_modelos"
down_revision="004_manual"
branch_labels=None
depends_on=None


def upgrade():
    values=("pendiente","enviado","fallo","descartado")
    postgresql.ENUM(*values,name="estado_envio").create(op.get_bind(),checkfirst=True)
    op.create_table("envios",
        sa.Column("id",sa.Uuid(as_uuid=False),primary_key=True),
        sa.Column("carga_id",sa.String(36),sa.ForeignKey("cargas.id",ondelete="CASCADE"),nullable=False),
        sa.Column("destinatario",sa.String(255),nullable=False),
        sa.Column("enviado_en",sa.DateTime(timezone=True),nullable=True),
        sa.Column("estado",postgresql.ENUM(*values,name="estado_envio",create_type=False),nullable=False),
        sa.Column("creado_en",sa.DateTime(timezone=True),nullable=False))
    op.create_index("ix_envios_carga_id","envios",["carga_id"])
    op.create_table("intentos",
        sa.Column("id",sa.Uuid(as_uuid=False),primary_key=True),
        sa.Column("envio_id",sa.Uuid(as_uuid=False),sa.ForeignKey("envios.id",ondelete="CASCADE"),nullable=False),
        sa.Column("numero",sa.Integer,nullable=False),
        sa.Column("intentado_en",sa.DateTime(timezone=True),nullable=False),
        sa.Column("resultado",sa.String(60),nullable=False),
        sa.Column("respuesta",sa.Text,nullable=True),
        sa.UniqueConstraint("envio_id","numero",name="uq_intento_envio_numero"),
        sa.CheckConstraint("numero >= 1",name="ck_intento_numero"),
        sa.CheckConstraint("resultado IN ('ok','timeout','rechazado','bounce')",name="ck_intento_resultado"))
    op.create_index("ix_intentos_envio_id","intentos",["envio_id"])
    op.create_table("retenciones",
        sa.Column("id",sa.Uuid(as_uuid=False),primary_key=True),
        sa.Column("envio_id",sa.Uuid(as_uuid=False),sa.ForeignKey("envios.id",ondelete="CASCADE"),nullable=False),
        sa.Column("reintentado_en",sa.DateTime(timezone=True),nullable=True),
        sa.Column("proximos_intentos",sa.Integer,nullable=False),
        sa.Column("razon",sa.String(255),nullable=False),
        sa.CheckConstraint("proximos_intentos BETWEEN 0 AND 2",name="ck_retencion_intentos"),
        sa.CheckConstraint("razon IN ('fallo_temporal','correo_invalido','bloqueado')",name="ck_retencion_razon"))
    op.create_index("ix_retenciones_envio_id","retenciones",["envio_id"])
    op.get_bind().execute(sa.text("INSERT INTO versiones_esquema (numero, aplicada_en) VALUES (5,CURRENT_TIMESTAMP) ON CONFLICT (numero) DO NOTHING"))


def downgrade():
    raise RuntimeError("La migración es aditiva; no se borran envíos ni intentos.")
