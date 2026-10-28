"""Reporte de CUIT y relaciones; no modifica clientes ni sistemas."""
import argparse
from collections import defaultdict
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sqlalchemy import create_engine, inspect, text
from app.config import validar_base_local
from app.utils.cuit_validator import normalizar_cuit, validar_cuit


def crear_reporte(connection):
    has_cuit = any(c['name'] == 'cuit' for c in inspect(connection).get_columns('clientes'))
    columns = 'id, cuit' if has_cuit else 'id, NULL AS cuit'
    missing, invalid, non_normalized = [], [], []
    groups = defaultdict(list)
    count = 0
    for row in connection.execute(text('SELECT '+columns+' FROM clientes ORDER BY id')).mappings():
        count += 1
        if row['cuit'] is None or row['cuit'] == '':
            missing.append(row['id']); continue
        try:
            normalized = normalizar_cuit(row['cuit'])
        except ValueError:
            invalid.append(row['id']); continue
        groups[normalized].append(row['id'])
        if normalized != row['cuit']:
            non_normalized.append(row['id'])
        if not validar_cuit(normalized):
            invalid.append(row['id'])
    orphans = list(connection.execute(text('SELECT s.id FROM sistemas s LEFT JOIN clientes c ON c.id=s.cliente_id WHERE c.id IS NULL ORDER BY s.id')).scalars())
    return {'solo_lectura': True, 'columna_cuit_existe': has_cuit, 'clientes_total': count,
            'clientes_sin_cuit': missing, 'clientes_cuit_invalidos': invalid,
            'clientes_cuit_no_normalizados': non_normalized,
            'cuit_duplicados': [{'cuit': cuit, 'cliente_ids': ids} for cuit, ids in sorted(groups.items()) if len(ids)>1],
            'sistemas_sin_cliente': orphans}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--salida', type=Path)
    args = parser.parse_args()
    from dotenv import load_dotenv
    load_dotenv(ROOT/'.env.local', override=False)
    load_dotenv(ROOT/'.env', override=False)
    url = os.environ.get('DATABASE_URL')
    validar_base_local(url)
    engine = create_engine(url)
    try:
        with engine.begin() as connection:
            connection.execute(text('SET TRANSACTION READ ONLY'))
            report = crear_reporte(connection)
        output = json.dumps(report, ensure_ascii=False, indent=2)
        if args.salida:
            args.salida.parent.mkdir(parents=True, exist_ok=True)
            args.salida.write_text(output, encoding='utf-8')
            os.chmod(args.salida, 0o600)
        print(output)
        return 0
    finally:
        engine.dispose()


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception:
        print('No se pudo completar la auditoría. Revisar conexión y esquema sin compartir credenciales.', file=sys.stderr)
        raise SystemExit(1)
