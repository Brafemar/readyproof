"""Integridad y límites del respaldo, sin red ni base de producción."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

spec = importlib.util.spec_from_file_location('backup_readyproof', Path(__file__).resolve().parents[1]/'scripts/backup_readyproof.py')
backup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backup)


def test_cambio_de_clave_no_autentica_el_mismo_respaldo(tmp_path, monkeypatch):
    file = tmp_path/'backup.enc'; file.write_bytes(b'contenido cifrado de ejemplo')
    monkeypatch.setenv('READYPROOF_BACKUP_KEY', 'a'*64)
    original = backup.mac_file(file)
    monkeypatch.setenv('READYPROOF_BACKUP_KEY', 'b'*64)
    assert backup.mac_file(file) != original


def test_alerta_puede_cargar_gmail_aunque_falte_clave_backup(monkeypatch):
    monkeypatch.setattr('dotenv.load_dotenv', lambda *args, **kwargs: None)
    monkeypatch.delenv('READYPROOF_BACKUP_KEY', raising=False)
    backup.load_environment(require_key=False)
    with pytest.raises(ValueError, match='Falta clave'):
        backup.load_environment()


def test_manipulacion_rechazada_antes_de_descifrar(tmp_path, monkeypatch):
    file = tmp_path/'backup.enc'; file.write_bytes(b'contenido de ejemplo')
    monkeypatch.setenv('READYPROOF_BACKUP_KEY', 'a'*64)
    meta = {'format':'readyproof-backup-v1', 'cipher_sha256':backup.digest(file), 'hmac_sha256':backup.mac_file(file)}
    file.with_suffix('.enc.json').write_text(json.dumps(meta))
    file.write_bytes(b'contenido alterado')
    monkeypatch.setattr(backup, 'run', lambda *a, **k: pytest.fail('No debe ejecutar openssl'))
    with pytest.raises(ValueError, match='Integridad'):
        backup.decrypt(file, tmp_path/'no_crear.tar')


def test_sha_recalculado_sin_clave_tampoco_autentica(tmp_path, monkeypatch):
    file = tmp_path/'backup.enc'; file.write_bytes(b'contenido de ejemplo')
    monkeypatch.setenv('READYPROOF_BACKUP_KEY', 'a'*64)
    mac = backup.mac_file(file)
    file.write_bytes(b'contenido alterado')
    file.with_suffix('.enc.json').write_text(json.dumps({'format':'readyproof-backup-v1','cipher_sha256':backup.digest(file),'hmac_sha256':mac}))
    monkeypatch.setattr(backup, 'run', lambda *a, **k: pytest.fail('No debe ejecutar openssl'))
    with pytest.raises(ValueError, match='Autenticación'):
        backup.decrypt(file, tmp_path/'no_crear.tar')


@pytest.mark.parametrize('remote', ['readyproof', 'otro-drive:readyproof-backups/daily/a.enc', backup.REMOTE+'/daily/../../produccion.enc'])
def test_restore_rechaza_destinos_ajenos(remote, monkeypatch):
    monkeypatch.setattr(backup, 'run', lambda *a, **k: pytest.fail('No debe ejecutar comandos'))
    with pytest.raises(ValueError, match='Solo se restaura'):
        backup.restore(remote)


def test_retencion_no_borra_archivos_ajenos_y_conserva_30_y_12(monkeypatch):
    deleted = []

    def fake(*args, **kwargs):
        if args[0] == 'lsf':
            if '/daily' in args[1]:
                names = [f'readyproof-2026-10-{day:02}.tar.enc' for day in range(1,32)]
            else:
                names = ['readyproof-2025-12.tar.enc'] + [f'readyproof-2026-{month:02}.tar.enc' for month in range(1,13)]
            return SimpleNamespace(stdout='\n'.join(names+['otro-proyecto.enc','archivo_personal.pdf','../otro.enc']))
        deleted.append(args[1])
    monkeypatch.setattr(backup, 'rclone', fake)
    backup.prune()
    assert deleted == [backup.REMOTE+'/daily/readyproof-2026-10-01.tar.enc',
                       backup.REMOTE+'/daily/readyproof-2026-10-01.tar.enc.json',
                       backup.REMOTE+'/monthly/readyproof-2025-12.tar.enc',
                       backup.REMOTE+'/monthly/readyproof-2025-12.tar.enc.json']


def test_restore_no_acepta_nombre_de_produccion(monkeypatch):
    monkeypatch.setattr(backup,'run',lambda *a,**kw:pytest.fail('No debe ejecutar comandos'))
    with pytest.raises(ValueError,match='bases aisladas'):
        backup.restore(backup.REMOTE+'/daily/readyproof-2026-10-28.tar.enc',prefijo_prueba='readyproof')


def test_restore_acepta_pdf_de_emision_archivada(tmp_path,monkeypatch):
    from io import BytesIO
    import tarfile,hashlib
    monkeypatch.setattr(backup,'STORE',tmp_path)
    dump=b'[Ejemplo] dump de prueba sin datos de produccion'
    manifest={'dump_sha256':hashlib.sha256(dump).hexdigest()}
    archive=BytesIO()
    with tarfile.open(fileobj=archive,mode='w') as tar:
        for name,value in {'readyproof.dump':dump,'manifest.json':json.dumps(manifest).encode(),
                'pdf/emisiones_carga-00000000-0000-4000-8000-000000000001.pdf':b'%PDF-1.4 [Ejemplo]'}.items():
            info=tarfile.TarInfo(name);info.size=len(value);tar.addfile(info,BytesIO(value))
    monkeypatch.setattr(backup,'rclone',lambda *a,**kw:None)
    monkeypatch.setattr(backup,'decrypt',lambda source,target:target.write_bytes(archive.getvalue()))
    class ExtraccionVerificada(Exception):pass
    def execute(args,**kwargs):
        if 'pg_restore' in args:
            extracted=list(tmp_path.glob('.restore-*/pdf/emisiones_carga-*.pdf'))
            assert len(extracted)==1 and extracted[0].read_bytes()==b'%PDF-1.4 [Ejemplo]'
            raise ExtraccionVerificada()
        assert 'createdb' in args
        assert args[-1].startswith('readyproof_test_etapa5_')
    monkeypatch.setattr(backup,'run',execute)
    with pytest.raises(ExtraccionVerificada):
        backup.restore(backup.REMOTE+'/daily/readyproof-2026-10-28.tar.enc',prefijo_prueba='readyproof_test_etapa5')
