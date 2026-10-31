"""Fotos de campo y anotaciones de cargas, sin modificar cargas existentes."""
from alembic import op
import sqlalchemy as sa

revision = '019_fotos_carga'
down_revision = '017_scc1_presion_bar'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('fotos_carga',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('carga_id', sa.String(36), sa.ForeignKey('cargas.id'), nullable=False),
        sa.Column('orden', sa.Integer(), nullable=False),
        sa.Column('imagen', sa.LargeBinary(), nullable=False),
        sa.Column('ancho', sa.Integer(), nullable=False),
        sa.Column('alto', sa.Integer(), nullable=False),
        sa.Column('sha256', sa.String(64), nullable=False),
        sa.Column('creado_por_id', sa.String(36), sa.ForeignKey('usuarios.id'), nullable=True),
        sa.Column('creada_en', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('carga_id', 'orden', name='uq_foto_carga_orden'),
        sa.CheckConstraint('orden >= 1', name='ck_foto_orden'),
        sa.CheckConstraint('ancho > 0 AND alto > 0', name='ck_foto_dimensiones'),
        sa.CheckConstraint('char_length(sha256) = 64', name='ck_foto_sha256'))
    op.create_index('ix_fotos_carga_carga_id', 'fotos_carga', ['carga_id'])
    op.create_table('fotos_anotacion',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('foto_id', sa.String(36), sa.ForeignKey('fotos_carga.id'), nullable=False),
        sa.Column('numero', sa.Integer(), nullable=False),
        sa.Column('x', sa.Float(), nullable=False),
        sa.Column('y', sa.Float(), nullable=False),
        sa.Column('texto', sa.String(140), nullable=False),
        sa.Column('creada_en', sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint('foto_id', 'numero', name='uq_anotacion_foto_numero'),
        sa.CheckConstraint('numero >= 1', name='ck_anotacion_numero'),
        sa.CheckConstraint('x BETWEEN 0 AND 1 AND y BETWEEN 0 AND 1', name='ck_anotacion_posicion'),
        sa.CheckConstraint('char_length(texto) BETWEEN 1 AND 140', name='ck_anotacion_texto'))
    op.create_index('ix_fotos_anotacion_foto_id', 'fotos_anotacion', ['foto_id'])
    op.execute('INSERT INTO versiones_esquema (numero,aplicada_en) VALUES (19,CURRENT_TIMESTAMP)')


def downgrade():
    if op.get_bind().scalar(sa.text('SELECT count(*) FROM fotos_carga')):
        raise RuntimeError('No se eliminan fotos de cargas registradas.')
    op.drop_table('fotos_anotacion')
    op.drop_table('fotos_carga')
    op.execute('DELETE FROM versiones_esquema WHERE numero=19')
