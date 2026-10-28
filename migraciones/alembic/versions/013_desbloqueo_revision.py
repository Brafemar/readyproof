"""Revisión pública, numeración transaccional y conservación de cada PDF emitido."""
from alembic import op
import sqlalchemy as sa

revision = '013_desbloqueo_revision'
down_revision = '012_sistema_cliente_activo'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('numero_registro_contador',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('ultimo', sa.Integer(), nullable=False, server_default='0'),
        sa.CheckConstraint('id = 1 AND ultimo >= 0', name='ck_contador_unico'))
    op.execute('INSERT INTO numero_registro_contador (id,ultimo) VALUES (1,0)')
    op.add_column('cargas', sa.Column('numero_registro', sa.Integer(), nullable=True))
    op.create_unique_constraint('uq_cargas_numero_registro', 'cargas', ['numero_registro'])
    op.add_column('cargas', sa.Column('revision_publica', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('cargas', sa.Column('pdf_hash', sa.String(64), nullable=True))
    op.add_column('cargas', sa.Column('desbloqueado_por', sa.String(36), sa.ForeignKey('usuarios.id'), nullable=True))
    op.add_column('cargas', sa.Column('motivo_desbloqueo', sa.Text(), nullable=True))
    op.add_column('cargas', sa.Column('estado_anulada', sa.Boolean(), nullable=False, server_default=sa.false()))
    op.create_table('emisiones_carga',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('carga_id', sa.String(36), sa.ForeignKey('cargas.id'), nullable=False, index=True),
        sa.Column('numero_registro', sa.Integer(), nullable=True),
        sa.Column('revision_publica', sa.Integer(), nullable=False),
        sa.Column('pdf', sa.LargeBinary(), nullable=False),
        sa.Column('pdf_sha256', sa.String(64), nullable=False),
        sa.Column('datos', sa.JSON(), nullable=False),
        sa.Column('firmantes', sa.JSON(), nullable=False),
        sa.Column('actor_id', sa.String(36), sa.ForeignKey('usuarios.id'), nullable=True),
        sa.Column('emitida_en', sa.DateTime(timezone=True), nullable=True),
        sa.Column('archivada_en', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('carga_id', 'revision_publica'))
    op.execute("""CREATE FUNCTION proteger_emision_readyproof() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN RAISE EXCEPTION 'Una emisión archivada no se modifica ni se elimina'; END; $$""")
    op.execute('CREATE TRIGGER emisiones_inmutables BEFORE UPDATE OR DELETE ON emisiones_carga FOR EACH ROW EXECUTE FUNCTION proteger_emision_readyproof()')
    op.execute('INSERT INTO versiones_esquema (numero,aplicada_en) VALUES (13,CURRENT_TIMESTAMP)')


def downgrade():
    connection = op.get_bind()
    if connection.execute(sa.text('SELECT 1 FROM emisiones_carga LIMIT 1')).first() or connection.execute(sa.text(
        'SELECT 1 FROM cargas WHERE numero_registro IS NOT NULL OR revision_publica<>0 OR desbloqueado_por IS NOT NULL OR estado_anulada LIMIT 1')).first():
        raise RuntimeError('No se eliminan emisiones, revisiones ni desbloqueos registrados.')
    op.drop_table('emisiones_carga')
    op.execute('DROP FUNCTION proteger_emision_readyproof()')
    for name in ('estado_anulada', 'motivo_desbloqueo', 'desbloqueado_por', 'pdf_hash', 'revision_publica', 'numero_registro'):
        op.drop_column('cargas', name)
    op.drop_table('numero_registro_contador')
    op.execute('DELETE FROM versiones_esquema WHERE numero=13')
