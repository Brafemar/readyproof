"""Habilita las planillas individuales SDI, SBC y SAL y sus sistemas de ejemplo."""
from alembic import op
import sqlalchemy as sa
revision='009_multisistema'
down_revision='008_documentacion_usuario'
branch_labels=None
depends_on=None


def upgrade():
    from app.planillas.multisistema import cargar_multisistema
    cargar_multisistema(op.get_bind())
    op.execute(sa.text('INSERT INTO versiones_esquema (numero,aplicada_en) VALUES (9,CURRENT_TIMESTAMP)'))


def downgrade():
    from app.planillas.multisistema import definiciones_multisistema,VERSION_MULTISISTEMA
    definitions=definiciones_multisistema();connection=op.get_bind()
    planillas=sa.table('planillas',sa.column('id',sa.String(36)),sa.column('codigo',sa.String),sa.column('version',sa.String),sa.column('huella',sa.String),sa.column('definicion',sa.JSON))
    rows=list(connection.execute(sa.select(planillas).where(planillas.c.codigo.in_(definitions),planillas.c.version==VERSION_MULTISISTEMA)).mappings())
    if len(rows)!=len(definitions) or any(row['huella']!=definitions[row['codigo']]['huella'] or row['definicion']!=definitions[row['codigo']]['definicion'] for row in rows):
        raise RuntimeError('No se borran plantillas alteradas o de otra versión.')
    cargas=sa.table('cargas',sa.column('planilla_id',sa.String(36)));ids=[row['id'] for row in rows]
    if connection.scalar(sa.select(cargas.c.planilla_id).where(cargas.c.planilla_id.in_(ids)).limit(1)):
        raise RuntimeError('Se conservan las plantillas vinculadas a cargas y firmas; no se revierte su habilitación.')
    connection.execute(planillas.delete().where(planillas.c.id.in_(ids)))
    connection.execute(sa.text('DELETE FROM versiones_esquema WHERE numero=9'))
