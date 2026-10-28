"""Correo propio y registro durable del envío de documentación."""
from alembic import op
import sqlalchemy as sa

revision='008_documentacion_usuario'
down_revision='007_smtp_gmail'
branch_labels=None
depends_on=None


def upgrade():
    op.add_column('usuarios',sa.Column('email',sa.String(254),nullable=True))
    op.create_table('envios_documentacion',
        sa.Column('id',sa.String(36),primary_key=True),
        sa.Column('usuario_id',sa.String(36),sa.ForeignKey('usuarios.id'),nullable=False),
        sa.Column('destinatario',sa.String(254),nullable=False),
        sa.Column('estado',sa.String(20),nullable=False),
        sa.Column('message_id',sa.String(200),nullable=False),
        sa.Column('mensaje_eml',sa.LargeBinary(),nullable=False),
        sa.Column('creado_en',sa.DateTime(timezone=True),nullable=False),
        sa.Column('enviado_en',sa.DateTime(timezone=True)),
        sa.CheckConstraint("estado IN ('preparado','enviado','archivado','fallo','indeterminado')",name='ck_documentacion_estado'))
    op.create_index('ix_envios_documentacion_usuario_id','envios_documentacion',['usuario_id'])
    op.execute('INSERT INTO versiones_esquema (numero,aplicada_en) VALUES (8,CURRENT_TIMESTAMP)')


def downgrade():
    if op.get_bind().execute(sa.text('SELECT 1 FROM envios_documentacion LIMIT 1')).first():
        raise RuntimeError('No se eliminan registros de documentación enviada.')
    op.drop_index('ix_envios_documentacion_usuario_id',table_name='envios_documentacion')
    op.drop_table('envios_documentacion')
    op.drop_column('usuarios','email')
    op.execute('DELETE FROM versiones_esquema WHERE numero=8')
