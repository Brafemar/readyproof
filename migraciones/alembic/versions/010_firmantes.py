"""Identificación de firmantes sin alterar registros ni PDF anteriores."""
from alembic import op
import sqlalchemy as sa

revision='010_firmantes'
down_revision='009_multisistema'
branch_labels=None
depends_on=None


def upgrade():
    for name,length in [('nombre_firmante',120),('dni_firmante',15),('cargo_firmante',120),('tecnico_nombre',120),('tecnico_login',80)]:
        op.add_column('firmas_carga',sa.Column(name,sa.String(length),nullable=True))
    op.add_column('firmas_carga',sa.Column('tecnico_usuario_id',sa.String(36),sa.ForeignKey('usuarios.id',name='fk_firma_tecnico_usuario'),nullable=True))
    op.add_column('revisiones_carga',sa.Column('firmantes',sa.JSON(),nullable=True))
    op.execute('INSERT INTO versiones_esquema (numero,aplicada_en) VALUES (10,CURRENT_TIMESTAMP)')


def downgrade():
    connection=op.get_bind()
    if connection.execute(sa.text('SELECT 1 FROM firmas_carga WHERE nombre_firmante IS NOT NULL OR dni_firmante IS NOT NULL OR cargo_firmante IS NOT NULL OR tecnico_usuario_id IS NOT NULL LIMIT 1')).first() or connection.execute(sa.text('SELECT 1 FROM revisiones_carga WHERE firmantes IS NOT NULL LIMIT 1')).first():
        raise RuntimeError('No se eliminan identidades ni revisiones de firmantes registradas.')
    op.drop_column('revisiones_carga','firmantes')
    op.drop_constraint('fk_firma_tecnico_usuario','firmas_carga',type_='foreignkey')
    for name in ['nombre_firmante','dni_firmante','cargo_firmante','tecnico_nombre','tecnico_login','tecnico_usuario_id']:
        op.drop_column('firmas_carga',name)
    op.execute('DELETE FROM versiones_esquema WHERE numero=10')
