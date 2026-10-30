"""Inventario remoto de PDF emitidos, con transacción PostgreSQL de solo lectura."""
import json
from pathlib import Path
import subprocess

REMOTE = r'''
import json, os
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from pypdf import PdfReader

root = Path('/home/readyproof')
load_dotenv(root/'.env.local', override=False)
load_dotenv(root/'.env', override=False)
url = os.environ['DATABASE_URL']
parsed = make_url(url)
assert parsed.database == 'readyproof' and parsed.host in {'localhost','127.0.0.1','::1'}
engine = create_engine(url, connect_args={'connect_timeout': 10})
query = text("""
SELECT c.numero_registro, c.revision_publica, p.codigo, c.pdf, c.pdf_sha256,
       c.datos, 'cargas' AS origen
FROM cargas c JOIN planillas p ON p.id=c.planilla_id WHERE c.pdf IS NOT NULL
UNION ALL
SELECT e.numero_registro, e.revision_publica, p.codigo, e.pdf, e.pdf_sha256,
       e.datos, 'emisiones_carga' AS origen
FROM emisiones_carga e JOIN cargas c ON c.id=e.carga_id
JOIN planillas p ON p.id=c.planilla_id
""")
records = {}
with engine.connect() as connection:
    connection.execute(text('SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY'))
    assert connection.scalar(text('SHOW transaction_read_only')) == 'on'
    for row in connection.execute(query).mappings():
        digest = sha256(row['pdf']).hexdigest()
        key = (row['numero_registro'], row['revision_publica'], digest)
        if key in records:
            records[key]['origenes'].append(row['origen'])
            continue
        reader = PdfReader(BytesIO(row['pdf']))
        pages = [page.extract_text() or '' for page in reader.pages]
        labels = ('SUPERVISOR DEL MANTENEDOR', 'RESPONSABLE DE LA INSTALACIÓN')
        split = len(pages) > 1 and 'OBSERVACIONES:' in '\n'.join(pages[:-1]) and all(label in pages[-1] for label in labels) and 'OBSERVACIONES:' not in pages[-1]
        designation = (row['datos'] or {}).get('cabecera',{}).get('sistema_designacion','')
        records[key] = {
            'numero_registro': row['numero_registro'], 'revision': row['revision_publica'],
            'codigo': row['codigo'], 'paginas': len(pages), 'pdf_sha256': digest,
            'huella_integra': digest == row['pdf_sha256'], 'origenes': [row['origen']],
            'observaciones_y_firmas_en_paginas_distintas': split,
            'modo_real': reader.metadata.get('/ReadyproofModo') == 'REAL' if reader.metadata else False,
            'designacion_contiene_ejemplo': 'EJEMPLO' in str(designation).upper(),
            'designacion_solicitada': str(designation).strip().upper() == 'BURGER KING EJEMPLO',
            'prefijo_ejemplo_tecnico_en_pdf': '[Ejemplo] Administración' in '\n'.join(pages),
        }
    connection.rollback()
engine.dispose()
print(json.dumps({'servidor':'67.205.170.29','solo_lectura':True,'pdf_modificados':False,
    'registros':list(records.values()),'criterio_paginacion':'Observaciones en páginas previas y firmas finales en página sin encabezado de observaciones; requiere decisión sobre cada emisión histórica.'},ensure_ascii=False))
'''


def main():
    root = Path(__file__).resolve().parents[1]
    target = root / 'out/frente_a_v2/inventario_emitidos_servidor.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    command = ['ssh', '-i', str(Path.home()/'.ssh/readyproof_deploy_67_205_170_29'),
        '-o', 'IdentitiesOnly=yes', '-o', 'BatchMode=yes', '-o', 'StrictHostKeyChecking=yes',
        '-o', 'ConnectTimeout=15', 'root@67.205.170.29',
        'cd /home/readyproof && PYTHONDONTWRITEBYTECODE=1 /home/readyproof/venv/bin/python -']
    process = subprocess.run(command, input=REMOTE.encode(), capture_output=True, timeout=90)
    if process.returncode:
        print('{"estado":"inventario_remoto_no_completado","pdf_modificados":false}')
        return 1
    report = json.loads(process.stdout)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'servidor':report['servidor'], 'solo_lectura':report['solo_lectura'],
        'pdf_modificados':False, 'pdf_distintos':len(report['registros']),
        'huellas_integras':all(row['huella_integra'] for row in report['registros']),
        'registros_numerados':[row for row in report['registros'] if row['numero_registro'] is not None]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
