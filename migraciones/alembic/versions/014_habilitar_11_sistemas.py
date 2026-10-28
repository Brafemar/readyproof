"""Agrega las 63 planillas verificadas y los sistemas de clientes ficticios."""
from alembic import op
import sqlalchemy as sa

revision='014_habilitar_11_sistemas'
down_revision='013_desbloqueo_revision'
branch_labels=None
depends_on=None


def upgrade():
    from app.planillas.catalogo_completo import cargar_restantes, completar_sistemas_ejemplo
    cargar_restantes(op.get_bind())
    completar_sistemas_ejemplo(op.get_bind())
    op.execute('INSERT INTO versiones_esquema (numero,aplicada_en) VALUES (14,CURRENT_TIMESTAMP)')


def downgrade():
    from app.planillas.catalogo_completo import definiciones_restantes
    from app.config import SISTEMAS_HABILITADOS
    c=op.get_bind();definitions=definiciones_restantes()
    rows=list(c.execute(sa.text('SELECT id,codigo,version,huella,definicion FROM planillas WHERE codigo=ANY(:codes)'),{'codes':list(definitions)}).mappings())
    if any(p['version']!='00-26-ms1' or p['huella']!=definitions[p['codigo']]['huella'] or p['definicion']!=definitions[p['codigo']]['definicion'] for p in rows):
        raise RuntimeError('No se eliminan versiones ampliadas alteradas ni históricas.')
    ids=[p['id'] for p in rows]
    if c.execute(sa.text('SELECT 1 FROM cargas WHERE planilla_id=ANY(:ids) LIMIT 1'),{'ids':ids}).first():
        raise RuntimeError('Se conservan las plantillas vinculadas a cargas y sus PDF.')
    families=[code for code in SISTEMAS_HABILITADOS if code not in ('SAA','SDI','SBC','SAL')]
    systems=list(c.execute(sa.text('SELECT s.id,s.tipo,s.designacion FROM sistemas s JOIN clientes c ON c.id=s.cliente_id WHERE c.es_ejemplo IS TRUE AND c.nombre LIKE :prefix AND s.tipo=ANY(:types)'),{'prefix':'[Ejemplo] %','types':families}).mappings())
    system_ids=[s['id'] for s in systems if s['designacion']=='[Ejemplo] '+SISTEMAS_HABILITADOS[s['tipo']]]
    if c.execute(sa.text('SELECT 1 FROM cargas WHERE sistema_id=ANY(:ids) LIMIT 1'),{'ids':system_ids}).first():
        raise RuntimeError('Se conservan los sistemas vinculados a cargas.')
    c.execute(sa.text('DELETE FROM sistemas WHERE id=ANY(:ids)'),{'ids':system_ids})
    c.execute(sa.text('DELETE FROM planillas WHERE id=ANY(:ids)'),{'ids':ids})
    op.execute('DELETE FROM versiones_esquema WHERE numero=14')
