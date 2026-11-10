"""Permiso administrable para certificados conjuntos."""
from alembic import op
import sqlalchemy as sa

revision = "022_certificado_conjunto"
down_revision = "021_union_018_020"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("usuarios", sa.Column("certificado_conjunto", sa.Boolean(),
                                         server_default=sa.false(), nullable=False))
    usuarios = sa.table("usuarios", sa.column("login"), sa.column("certificado_conjunto"))
    op.execute(usuarios.update().where(usuarios.c.login == "msanchez").values(certificado_conjunto=True))


def downgrade():
    op.drop_column("usuarios", "certificado_conjunto")
