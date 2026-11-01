"""Referencia opcional al ítem del kit, sin alterar las marcas existentes."""
from alembic import op
import sqlalchemy as sa

revision = "020_foto_anotacion_item"
down_revision = "019_fotos_carga"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("fotos_anotacion_item",
        sa.Column("anotacion_id", sa.String(36), sa.ForeignKey("fotos_anotacion.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("bloque", sa.Text(), nullable=False),
        sa.Column("campo", sa.String(80), nullable=False),
        sa.Column("texto", sa.Text(), nullable=False),
        sa.CheckConstraint("char_length(bloque) > 0 AND char_length(campo) > 0 AND char_length(texto) > 0", name="ck_anotacion_item_referencia"))
    op.execute("INSERT INTO versiones_esquema (numero,aplicada_en) VALUES (20,CURRENT_TIMESTAMP)")


def downgrade():
    if op.get_bind().scalar(sa.text("SELECT count(*) FROM fotos_anotacion_item")):
        raise RuntimeError("No se eliminan referencias de ítems guardadas en las marcas.")
    op.drop_table("fotos_anotacion_item")
    op.execute("DELETE FROM versiones_esquema WHERE numero=20")
