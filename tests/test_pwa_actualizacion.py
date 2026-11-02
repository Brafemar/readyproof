"""Actualización explícita y protección de guardados, con datos ficticios."""
import os
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def run_node(mode, tmp_path):
    node = os.environ.get("READYPROOF_NODE") or shutil.which("node")
    assert node, "Se requiere Node para comprobar la actualización PWA."
    env = dict(os.environ, RP_OUT=str(tmp_path))
    modules = Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules"
    env.setdefault("NODE_PATH", str(modules))
    result = subprocess.run([node, "tests/browser/pwa_actualizacion.cjs", mode], cwd=ROOT,
                            env=env, capture_output=True, text=True, encoding="utf-8", timeout=90)
    assert result.returncode == 0, result.stdout + result.stderr


def test_guardas_reales_de_carga_y_fotos(tmp_path):
    run_node("guardas", tmp_path)


def test_aviso_recarga_solo_explicita_en_navegador_movil(tmp_path):
    run_node("navegador", tmp_path)
