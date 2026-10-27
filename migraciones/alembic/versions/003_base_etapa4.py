"""Punto de partida compatible con las instalaciones de etapas anteriores."""
from pathlib import Path
import runpy
from alembic import op

revision="003_base_etapa4"
down_revision=None
branch_labels=None
depends_on=None


def upgrade():
    base=Path(__file__).resolve().parents[2]/"base_etapa4.py"
    runpy.run_path(str(base))["upgrade"](op.get_bind())


def downgrade():
    raise RuntimeError("No se elimina el esquema histórico mediante un downgrade.")
