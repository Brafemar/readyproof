"""Registro de cambios autenticados, sin alterar las cargas anteriores."""
from alembic import op
import sqlalchemy as sa

revision = '016_tabla_auditoria'
down_revision = '014_habilitar_11_sistemas'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('auditoria',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('tabla', sa.String(50), nullable=False),
        sa.Column('registro_id', sa.String(36), nullable=False),
        sa.Column('accion', sa.String(20), nullable=False),
        sa.Column('usuario_id', sa.String(36), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('datos_anterior', sa.JSON(), nullable=True),
        sa.Column('datos_nuevo', sa.JSON(), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("accion IN ('INSERT','UPDATE','DELETE','DESBLOQUEO')", name='ck_auditoria_accion'))
    for column in ('timestamp', 'registro_id', 'tabla', 'usuario_id'):
        op.create_index('ix_auditoria_'+column, 'auditoria', [column])
    op.execute("""CREATE FUNCTION proteger_auditoria_readyproof() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN RAISE EXCEPTION 'Los registros de auditoría no se modifican ni se eliminan'; END; $$""")
    op.execute('CREATE TRIGGER auditoria_inmutable BEFORE UPDATE OR DELETE ON auditoria FOR EACH ROW EXECUTE FUNCTION proteger_auditoria_readyproof()')
    op.execute('INSERT INTO versiones_esquema (numero,aplicada_en) VALUES (16,CURRENT_TIMESTAMP)')


def downgrade():
    if op.get_bind().scalar(sa.text('SELECT count(*) FROM auditoria')):
        raise RuntimeError('Se conserva la auditoría existente; no se elimina mediante downgrade.')
    op.drop_table('auditoria')
    op.execute('DROP FUNCTION proteger_auditoria_readyproof()')
    op.execute('DELETE FROM versiones_esquema WHERE numero=16')
