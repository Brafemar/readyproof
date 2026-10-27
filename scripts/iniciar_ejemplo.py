"""Servidor local de revisión con una base PostgreSQL aislada y datos ficticios."""
import argparse
import json
import os
from pathlib import Path
import socket
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from werkzeug.serving import run_simple
from app import create_app


def main():
    parser = argparse.ArgumentParser(description="Abre readyproof localmente con datos de prueba.")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--cargar-planillas",action="store_true",help="Importa explícitamente los cuatro JSON en una base de ejemplos existente.")
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error("El puerto debe estar entre 1024 y 65535.")
    candidates = [Path(os.environ.get("PG_BINDIR", ""))] + [Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "PostgreSQL" / str(v) / "bin" for v in range(18,13,-1)]
    binary = next((p for p in candidates if (p / "initdb.exe").is_file()), None)
    if binary is None:
        parser.error("Se requiere PostgreSQL local; configurar PG_BINDIR si está en otra ubicación.")
    directory = ROOT / "out" / "etapa3" / "demo_local"
    directory.mkdir(parents=True, exist_ok=True)
    data = directory / "data"
    if (data / "postmaster.pid").exists():
        parser.error("La base de revisión ya está activa. Usar la instancia existente o detenerla primero.")
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", args.port))
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0)); pgport = probe.getsockname()[1]
    log = (directory / "control.log").open("a", encoding="utf-8")
    if not (data / "PG_VERSION").exists():
        subprocess.run([str(binary / "initdb.exe"), "-D", str(data), "--username=readyproof_demo", "--encoding=UTF8", "--locale=C", "--auth=trust", "--no-instructions"], stdout=log, stderr=subprocess.STDOUT, check=True, timeout=90)
    engine = None
    try:
        subprocess.run([str(binary / "pg_ctl.exe"), "-D", str(data), "-l", str(directory / "postgres.log"), "-o", f"-h 127.0.0.1 -p {pgport}", "-w", "-t", "60", "start"], stdout=log, stderr=subprocess.STDOUT, check=True, timeout=75)
        app = create_app({"MAIL_MODO_PRUEBA": True, "DATABASE_URL": f"postgresql+psycopg://readyproof_demo@127.0.0.1:{pgport}/postgres", "DIRECTORIO_TEMPORAL": str(directory / "temporales")})
        engine = app.extensions["db_engine"]
        result=app.test_cli_runner().invoke(args=["init-db","--ejemplos"])
        if result.exit_code!=0:
            raise RuntimeError("No se pudo preparar el esquema/catálogo local.") from result.exception
        if args.cargar_planillas:
            result=app.test_cli_runner().invoke(args=["cargar-planillas"])
            if result.exit_code!=0:
                raise RuntimeError("No se pudo importar el catálogo JSON.") from result.exception
            print(result.output.strip(),flush=True)
        url = f"http://127.0.0.1:{args.port}"
        (directory / "servidor.json").write_text(json.dumps({"url": url, "pid": os.getpid(), "pgport": pgport, "pgdata": str(data)}, indent=2), encoding="utf-8")
        print(f"readyproof disponible en {url} — solo datos y firmas ficticios.", flush=True)
        run_simple("127.0.0.1", args.port, app, use_reloader=False, use_debugger=False, threaded=True)
    finally:
        if engine is not None:
            engine.dispose()
        if (data / "postmaster.pid").exists():
            subprocess.run([str(binary / "pg_ctl.exe"), "-D", str(data), "-m", "fast", "-w", "stop"], stdout=log, stderr=subprocess.STDOUT, timeout=60, check=True)
        log.close()


if __name__ == "__main__":
    main()
