"""Respaldo consistente, cifrado y verificable de readyproof a Drive."""
import argparse
from datetime import datetime, timezone
import hashlib
import hmac
import json
import logging
import os
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path('/home/readyproof')
STORE = Path('/var/backups/readyproof')
CONFIG = '/etc/readyproof/rclone-backup.conf'
REMOTE = 'readyproof-drive:readyproof-backups'
TABLES = ('cargas', 'firmas_carga', 'envios', 'planillas', 'sistemas', 'auditoria')


def run(args, **kwargs):
    if not kwargs.get('capture_output'):
        kwargs.setdefault('stderr', subprocess.PIPE)
    return subprocess.run(args, check=True, **kwargs)


def load_environment(require_key=True):
    from dotenv import load_dotenv
    load_dotenv(ROOT/'.env.local', override=False)
    load_dotenv(ROOT/'.env', override=False)
    load_dotenv('/etc/readyproof/backup.env', override=False)
    if require_key and len(os.environ.get('READYPROOF_BACKUP_KEY', '')) < 43:
        raise ValueError('Falta clave privada de respaldo.')


def mac_file(path):
    key = hashlib.sha256(b'readyproof-backup-hmac-v1\0' + os.environ['READYPROOF_BACKUP_KEY'].encode()).digest()
    mac = hmac.new(key, digestmod=hashlib.sha256)
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            mac.update(chunk)
    return mac.hexdigest()


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def content_manifest(connection, pdf_directory=None):
    from sqlalchemy import inspect, text
    counts = {}
    quote = connection.dialect.identifier_preparer.quote
    for name in sorted(inspect(connection).get_table_names()):
        counts[name] = connection.scalar(text('SELECT count(*) FROM ' + quote(name)))
    blobs = {}
    for table, key, columns in (
        ('cargas', 'id', ('pdf',)),
        ('emisiones_carga', 'id', ('pdf',)),
        ('envios', 'id', ('pdf_copia',)),
        ('firmas_carga', 'carga_id', ('tecnico_png', 'responsable_png')),
    ):
        if table not in counts:
            continue
        names = ', '.join(quote(c) for c in (key, *columns))
        for row in connection.execute(text(f'SELECT {names} FROM {quote(table)} ORDER BY {quote(key)}')).mappings():
            for column in columns:
                value = row[column]
                if value is not None:
                    name = f'{table}/{row[key]}/{column}'
                    blobs[name] = {'bytes': len(value), 'sha256': hashlib.sha256(value).hexdigest()}
                    if pdf_directory and column in {'pdf', 'pdf_copia'}:
                        if not re.fullmatch(r'[0-9a-fA-F-]{36}', str(row[key])):
                            raise ValueError('Identificador inválido para exportar PDF.')
                        (pdf_directory/f'{table}-{row[key]}.pdf').write_bytes(value)
    return {'schema': connection.scalar(text('SELECT version_num FROM alembic_version')),
            'counts': counts, 'blobs': blobs}


def rclone(*args, **kwargs):
    return run(['rclone', '--config', CONFIG, *args], **kwargs)


def encrypt(source, target):
    run(['openssl', 'enc', '-aes-256-cbc', '-pbkdf2', '-iter', '600000', '-md', 'sha256', '-salt',
         '-pass', 'env:READYPROOF_BACKUP_KEY', '-in', str(source), '-out', str(target)], stdout=subprocess.DEVNULL)
    metadata = {'format': 'readyproof-backup-v1', 'cipher_sha256': digest(target), 'hmac_sha256': mac_file(target),
                'cipher': 'AES-256-CBC', 'kdf': 'PBKDF2-SHA256', 'iterations': 600000}
    target.with_suffix(target.suffix+'.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')


def decrypt(source, target):
    metadata = json.loads(source.with_suffix(source.suffix+'.json').read_text())
    if metadata.get('format') != 'readyproof-backup-v1' or not hmac.compare_digest(metadata.get('cipher_sha256', ''), digest(source)):
        raise ValueError('Integridad del archivo cifrado inválida.')
    if not hmac.compare_digest(metadata.get('hmac_sha256', ''), mac_file(source)):
        raise ValueError('Autenticación del archivo inválida: no se descifra.')
    run(['openssl', 'enc', '-d', '-aes-256-cbc', '-pbkdf2', '-iter', '600000', '-md', 'sha256',
         '-pass', 'env:READYPROOF_BACKUP_KEY', '-in', str(source), '-out', str(target)], stdout=subprocess.DEVNULL)


def prune():
    # Solo nombres de este trabajo y dentro de las dos subcarpetas propias.
    for folder, pattern, keep in (
        ('daily', r'readyproof-\d{4}-\d{2}-\d{2}\.tar\.enc', 30),
        ('monthly', r'readyproof-\d{4}-\d{2}\.tar\.enc', 12),
    ):
        result = rclone('lsf', f'{REMOTE}/{folder}', '--files-only', '--max-depth', '1', capture_output=True, text=True)
        names = sorted(name for name in result.stdout.splitlines() if re.fullmatch(pattern, name))
        for name in names[:-keep]:
            for suffix in ('', '.json'):
                rclone('deletefile', f'{REMOTE}/{folder}/{name}{suffix}', stdout=subprocess.DEVNULL)


def backup():
    from sqlalchemy import create_engine, text
    from sqlalchemy.engine import make_url
    url = make_url(os.environ['DATABASE_URL'])
    if url.database != 'readyproof' or url.host not in {'localhost', '127.0.0.1', '::1'}:
        raise ValueError('El respaldo requiere la BD local readyproof.')
    engine = create_engine(os.environ['DATABASE_URL'])
    now = datetime.now(timezone.utc)
    name = 'readyproof-' + now.strftime('%Y-%m-%d') + '.tar.enc'
    with tempfile.TemporaryDirectory(prefix='.backup-', dir=STORE) as temporary:
        work = Path(temporary)
        pdfs = work/'pdf'; pdfs.mkdir()
        with engine.connect().execution_options(isolation_level='REPEATABLE READ') as connection:
            with connection.begin():
                connection.execute(text('SET TRANSACTION READ ONLY'))
                snapshot = connection.scalar(text('SELECT pg_export_snapshot()'))
                manifest = content_manifest(connection, pdfs)
                with (work/'readyproof.dump').open('wb') as stream:
                    run(['runuser', '-u', 'postgres', '--', 'pg_dump', '--format=custom', '--no-owner', '--no-acl',
                         '--snapshot='+snapshot, '--dbname=readyproof'], stdout=stream)
        engine.dispose()
        manifest.update(created_utc=now.isoformat(), dump_sha256=digest(work/'readyproof.dump'))
        (work/'manifest.json').write_text(json.dumps(manifest, sort_keys=True, indent=2), encoding='utf-8')
        archive = work/'readyproof.tar'
        with tarfile.open(archive, 'w') as tar:
            for item in ('readyproof.dump', 'manifest.json', 'pdf'):
                tar.add(work/item, arcname=item)
        encrypted = work/name
        encrypt(archive, encrypted)
        for folder, remote_name in (('daily', name), ('monthly', 'readyproof-'+now.strftime('%Y-%m')+'.tar.enc')):
            for suffix in ('', '.json'):
                rclone('copyto', str(encrypted)+suffix, f'{REMOTE}/{folder}/{remote_name}{suffix}', stdout=subprocess.DEVNULL)
            # Verificación mediante descarga, independiente del resultado de copyto.
            verification = work/(folder+'.enc')
            rclone('copyto', f'{REMOTE}/{folder}/{remote_name}', str(verification), stdout=subprocess.DEVNULL)
            if digest(verification) != digest(encrypted):
                raise ValueError('La copia descargada de Drive no coincide.')
        prune()
        result = {'estado': 'respaldo_verificado_en_drive', 'remote': REMOTE+'/daily/'+name,
                   'schema': manifest['schema'], 'counts': {k: manifest['counts'][k] for k in TABLES if k in manifest['counts']},
                  'blobs': len(manifest['blobs']), 'cipher_sha256': digest(encrypted), 'created_utc': now.isoformat()}
        (STORE/'ultimo_backup.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
        logging.info('Respaldo verificado; schema=%s; blobs=%s', result['schema'], result['blobs'])
        return result


def restore(remote, expected_schema=None, expected_planillas=None, prefijo_prueba='readyproof_test_restore'):
    if prefijo_prueba not in {'readyproof_test_restore','readyproof_test_etapa5'}:
        raise ValueError('La restauración solo crea bases aisladas de prueba.')
    allowed = (re.escape(REMOTE) + r'/(?:daily/readyproof-[0-9]{4}-[0-9]{2}-[0-9]{2}'
               r'|monthly/readyproof-[0-9]{4}-[0-9]{2}'
               r'|pre-migrations/readyproof-pre-[0-9]{3}-[0-9]{8}T[0-9]{6})\.tar\.enc')
    if not re.fullmatch(allowed, remote):
        raise ValueError('Solo se restaura un respaldo diario, mensual o previo a una migración de readyproof.')
    dbname = prefijo_prueba+'_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    with tempfile.TemporaryDirectory(prefix='.restore-', dir=STORE) as temporary:
        work = Path(temporary)
        encrypted = work/'backup.enc'
        for suffix in ('', '.json'):
            rclone('copyto', remote+suffix, str(encrypted)+suffix, stdout=subprocess.DEVNULL)
        archive = work/'backup.tar'; decrypt(encrypted, archive)
        with tarfile.open(archive) as tar:
            names = tar.getnames()
            if len(names) != len(set(names)):
                raise ValueError('Archivo con nombres repetidos.')
            for member in tar:
                if member.isdir() and member.name == 'pdf':
                    (work/'pdf').mkdir(exist_ok=True)
                    continue
                if not member.isfile() or not (member.name in {'readyproof.dump', 'manifest.json'} or re.fullmatch(r'pdf/(cargas|envios|emisiones_carga)-[0-9a-fA-F-]{36}\.pdf', member.name)):
                    raise ValueError('Contenido inesperado en respaldo.')
                target = work/member.name
                target.parent.mkdir(exist_ok=True)
                with tar.extractfile(member) as source:
                    target.write_bytes(source.read())
        expected = json.loads((work/'manifest.json').read_text())
        if expected['dump_sha256'] != digest(work/'readyproof.dump'):
            raise ValueError('Dump no coincide con el manifiesto.')
        run(['runuser', '-u', 'postgres', '--', 'createdb', '--template=template0', dbname], stdout=subprocess.DEVNULL)
        # No DROP DATABASE ni restauración sobre readyproof. Si falla, conservar la BD de prueba.
        with (work/'readyproof.dump').open('rb') as stream:
            run(['runuser', '-u', 'postgres', '--', 'pg_restore', '--exit-on-error', '--single-transaction',
                 '--no-owner', '--no-acl', '--dbname='+dbname], stdin=stream, stdout=subprocess.DEVNULL)
        # Consulta por socket y peer, sin abrir permisos del directorio privado de la app.
        psql = ['runuser', '-u', 'postgres', '--', 'psql', '-X', '-qAt', '--set=ON_ERROR_STOP=1', '--dbname='+dbname]
        result = run(psql, input="SELECT json_agg(tablename ORDER BY tablename) FROM pg_tables WHERE schemaname='public';", capture_output=True, text=True)
        names = json.loads(result.stdout)
        if names != sorted(expected['counts']) or any(not re.fullmatch(r'[a-z_][a-z0-9_]*', n) for n in names):
            raise ValueError('Las tablas restauradas no coinciden.')
        counts_sql = ','.join("'"+n+"',(SELECT count(*) FROM \""+n+'\")' for n in names)
        sql = """SELECT json_build_object('schema',(SELECT version_num FROM alembic_version),
          'counts',json_build_object(COUNTS_SQL),
          'blobs',(SELECT coalesce(json_object_agg(name,json_build_object('bytes',length(value),
           'sha256',encode(sha256(value),'hex'))),'{}'::json) FROM (
           SELECT 'cargas/'||id||'/pdf' name,pdf value FROM cargas
           UNION ALL SELECT 'envios/'||id||'/pdf_copia',pdf_copia FROM envios
           UNION ALL SELECT 'firmas_carga/'||carga_id||'/tecnico_png',tecnico_png FROM firmas_carga
           UNION ALL SELECT 'firmas_carga/'||carga_id||'/responsable_png',responsable_png FROM firmas_carga
          HISTORIAL_SQL
          ) b WHERE value IS NOT NULL));""".replace('COUNTS_SQL', counts_sql).replace('HISTORIAL_SQL',
            "UNION ALL SELECT 'emisiones_carga/'||id||'/pdf',pdf FROM emisiones_carga" if 'emisiones_carga' in names else '')
        result = run(psql, input=sql, capture_output=True, text=True)
        actual = json.loads(result.stdout)
        for key in ('schema', 'counts', 'blobs'):
            if actual[key] != expected[key]:
                raise ValueError('Restauración difiere del manifiesto: '+key)
        expected_pdfs = {name.replace('/', '-').replace('-pdf_copia', '.pdf').replace('-pdf', '.pdf'): data
                         for name, data in expected['blobs'].items() if name.endswith(('/pdf', '/pdf_copia'))}
        for filename, data in expected_pdfs.items():
            pdf = work/'pdf'/filename
            if not pdf.is_file() or digest(pdf) != data['sha256']:
                raise ValueError('PDF exportado no coincide.')
        if expected_schema is not None and actual['schema'] != expected_schema:
            raise ValueError('La versión restaurada no es la esperada.')
        if expected_planillas is not None and actual['counts']['planillas'] != expected_planillas:
            raise ValueError('La cantidad de planillas restauradas no es la esperada.')
        report = {'estado': 'restauracion_verificada', 'database': dbname, 'schema': actual['schema'],
                  'remote': remote, 'cipher_sha256': digest(encrypted), 'snapshot_created_utc': expected['created_utc'],
                  'counts': {k: actual['counts'][k] for k in TABLES if k in actual['counts']}, 'tablas_comparadas': len(actual['counts']),
                  'blobs_comparados': len(actual['blobs']), 'pdf_exportados_comparados': len(expected_pdfs), 'produccion_modificada': False}
        (STORE/'ultima_restauracion.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        return report


def alert():
    from email.message import EmailMessage
    sys.path.insert(0, str(ROOT))
    from app.gmail_https import obtener_token, enviar_con_token
    mail = EmailMessage()
    mail['From'] = mail['To'] = 'readyproof.ar@gmail.com'
    mail['Subject'] = 'readyproof — Falló el respaldo automático'
    mail.set_content('No se pudo completar y verificar el respaldo de readyproof. Revisar readyproof-backup.service y /var/backups/readyproof/backup.log. No migrar hasta recuperar el respaldo. Este mensaje no contiene datos de clientes ni credenciales.')
    enviar_con_token(mail, obtener_token())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('backup', 'restore', 'alert'))
    parser.add_argument('--remote')
    parser.add_argument('--schema-esperado')
    parser.add_argument('--planillas-esperadas', type=int)
    parser.add_argument('--prefijo-prueba', choices=('readyproof_test_restore','readyproof_test_etapa5'), default='readyproof_test_restore')
    args = parser.parse_args()
    os.umask(0o077)
    logging.basicConfig(filename=STORE/'backup.log', level=logging.INFO, format='%(asctime)sZ %(levelname)s %(message)s')
    logging.Formatter.converter = __import__('time').gmtime
    try:
        load_environment(require_key=args.action != 'alert')
        if args.action == 'alert':
            alert(); return 0
        if args.action == 'backup':
            import fcntl
            with (STORE/'.backup.lock').open('a') as lock:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                result = backup()
        else:
            result = restore(args.remote or '', args.schema_esperado, args.planillas_esperadas, args.prefijo_prueba)
        print(json.dumps(result))
        return 0
    except Exception:
        # No volcar excepciones: URLs, salida de herramientas y drivers pueden contener secretos.
        logging.error('Falló %s; consultar estado de herramientas sin exponer configuración privada.', args.action)
        print(json.dumps({'estado': 'error', 'accion': args.action}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
