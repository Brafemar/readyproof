"""Contacto y vínculo de clientes con Contabilium, sin cambiar cargas."""
from alembic import op
import sqlalchemy as sa

revision = '018_contacto_contabilium'
down_revision = '017_scc1_presion_bar'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('clientes', sa.Column('contacto', sa.JSON(), nullable=True))
    op.add_column('clientes', sa.Column('contabilium_id', sa.String(40), nullable=True))
    op.add_column('clientes', sa.Column('sincronizado_en', sa.DateTime(timezone=True), nullable=True))
    op.create_unique_constraint('uq_clientes_contabilium_id', 'clientes', ['contabilium_id'])
    op.execute('INSERT INTO versiones_esquema (numero,aplicada_en) VALUES (18,CURRENT_TIMESTAMP)')


def downgrade():
    c = op.get_bind()
    if c.scalar(sa.text('SELECT count(*) FROM clientes WHERE contacto IS NOT NULL OR contabilium_id IS NOT NULL')):
        raise RuntimeError('No se eliminan contactos ni vínculos de clientes registrados.')
    op.drop_constraint('uq_clientes_contabilium_id', 'clientes', type_='unique')
    for name in ('sincronizado_en', 'contabilium_id', 'contacto'):
        op.drop_column('clientes', name)
    op.execute('DELETE FROM versiones_esquema WHERE numero=18')
