"""Estado activo de sistemas sin cambiar la identidad ni las relaciones existentes."""
from alembic import op
import sqlalchemy as sa

revision = '012_sistema_cliente_activo'
down_revision = '011_cliente_cuit_opcional'
branch_labels = None
depends_on = None


def upgrade():
    if op.get_bind().execute(sa.text('SELECT 1 FROM sistemas WHERE cliente_id IS NULL LIMIT 1')).first():
        raise RuntimeError('Hay sistemas sin cliente: revisar el reporte antes de migrar; no se asignan clientes automáticamente.')
    op.add_column('sistemas', sa.Column('activo', sa.Boolean(), nullable=False, server_default=sa.true()))
    op.alter_column('sistemas', 'cliente_id', existing_type=sa.String(36), nullable=False)
    op.execute('INSERT INTO versiones_esquema (numero,aplicada_en) VALUES (12,CURRENT_TIMESTAMP)')


def downgrade():
    if op.get_bind().execute(sa.text('SELECT 1 FROM sistemas WHERE activo IS FALSE LIMIT 1')).first():
        raise RuntimeError('No se descarta el estado de sistemas inactivos.')
    op.drop_column('sistemas', 'activo')
    op.execute('DELETE FROM versiones_esquema WHERE numero=12')
