"""CUIT opcional, normalizado y único sin modificar UUID ni datos históricos."""
from alembic import op
import sqlalchemy as sa

revision = '011_cliente_cuit_opcional'
down_revision = '010_firmantes'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('clientes', sa.Column('cuit', sa.String(11), nullable=True))
    op.create_unique_constraint('uq_clientes_cuit', 'clientes', ['cuit'])
    op.create_index('ix_cliente_cuit', 'clientes', ['cuit'])
    op.create_check_constraint('ck_cliente_cuit_formato', 'clientes', "cuit IS NULL OR cuit ~ '^[0-9]{11}$'")
    op.execute('INSERT INTO versiones_esquema (numero,aplicada_en) VALUES (11,CURRENT_TIMESTAMP)')


def downgrade():
    if op.get_bind().execute(sa.text('SELECT 1 FROM clientes WHERE cuit IS NOT NULL LIMIT 1')).first():
        raise RuntimeError('No se eliminan CUIT registrados; exportar y resolver antes de revertir.')
    op.drop_constraint('ck_cliente_cuit_formato', 'clientes', type_='check')
    op.drop_index('ix_cliente_cuit', table_name='clientes')
    op.drop_constraint('uq_clientes_cuit', 'clientes', type_='unique')
    op.drop_column('clientes', 'cuit')
    op.execute('DELETE FROM versiones_esquema WHERE numero=11')
