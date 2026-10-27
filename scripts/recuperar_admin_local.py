"""Abre la recuperación autorizada contra la base del ejemplo local activo."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app import create_app


def main():
    parser = argparse.ArgumentParser(description="Recuperación de administrador del ejemplo local de readyproof.")
    parser.add_argument("--login", required=True)
    args = parser.parse_args()
    if not sys.stdin.isatty():
        parser.error("Ejecutá este comando en una consola interactiva; no envíes contraseñas por archivos o tuberías.")
    state = json.loads((ROOT / "out/etapa3/demo_local/servidor.json").read_text(encoding="utf-8"))
    if Path(state["pgdata"]).resolve() != ROOT / "out/etapa3/demo_local/data":
        parser.error("La ruta de la base local no coincide con el proyecto.")
    port = int(state["pgport"])
    if not 1024 <= port <= 65535:
        parser.error("Puerto local inválido.")
    app = create_app({"DATABASE_URL": f"postgresql+psycopg://readyproof_demo@127.0.0.1:{port}/postgres", "MAIL_MODO_PRUEBA": True})
    with app.app_context():
        app.cli.main(args=["admin-recuperar", "--login", args.login], prog_name="readyproof")


if __name__ == "__main__":
    main()
