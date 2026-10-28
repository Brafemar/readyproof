"""Nueva versión SCC-1 en bar; conserva el catálogo original en MPa."""
from alembic import op
import sqlalchemy as sa
revision='017_scc1_presion_bar'
down_revision='016_tabla_auditoria'
branch_labels=None
depends_on=None

def upgrade():
    from app.planillas.unidades_autorizadas import cargar_version_bar
    cargar_version_bar(op.get_bind())
    op.execute('INSERT INTO versiones_esquema (numero,aplicada_en) VALUES (17,CURRENT_TIMESTAMP)')

def downgrade():
    c=op.get_bind()
    rows=c.execute(sa.text("SELECT id FROM planillas WHERE codigo='SG-PEM-IFI-SCC-1' AND version='00-26-bar1'")).scalars().all()
    if rows and c.scalar(sa.text('SELECT count(*) FROM cargas WHERE planilla_id=ANY(:ids)'),{'ids':rows}):
        raise RuntimeError('Se conserva la versión en bar vinculada a cargas históricas.')
    c.execute(sa.text('DELETE FROM planillas WHERE id=ANY(:ids)'),{'ids':rows})
    op.execute('DELETE FROM versiones_esquema WHERE numero=17')
