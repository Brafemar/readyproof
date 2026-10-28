"""Ensayo y aplicación privada de etapa 5, con protección de los registros previos."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from urllib.request import urlopen

FILES=('app/config.py','app/catalogo.py','app/auth/rutas.py','app/rutas/api.py','app/documentacion.py',
    'app/planillas/generador.py','app/planillas/multisistema.py','app/planillas/importacion_excel.py',
    'app/planillas/catalogo_completo.py','app/planillas/definiciones/restantes_v5.json',
    'app/static/carga.js','app/static/sw.js','app/templates/admin.html',
    'migraciones/alembic/versions/014_habilitar_11_sistemas.py','scripts/importador_planillas.py',
    'scripts/backup_readyproof.py','docs/GUIA_ACCESO_BRAFEMAR.md')
ROOT=Path('/home/readyproof')
STAGE=Path('/home/readyproof_revision_etapa5')
STORE=Path('/var/backups/readyproof')
HEAD='014_habilitar_11_sistemas'


def run(args,**kwargs):
    return subprocess.run(args,check=True,capture_output=True,timeout=700,**kwargs)


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def environment():
    from dotenv import load_dotenv
    from sqlalchemy import create_engine
    from sqlalchemy.engine import make_url
    load_dotenv(ROOT/'.env.local',override=False);load_dotenv(ROOT/'.env',override=False)
    url=make_url(os.environ['DATABASE_URL'])
    assert url.database=='readyproof' and url.host in {'localhost','127.0.0.1','::1'}
    return create_engine(url),url


def snapshot(connection):
    from sqlalchemy import inspect,text
    result={};quote=connection.dialect.identifier_preparer.quote
    for name in sorted(inspect(connection).get_table_names()):
        if name in ('alembic_version','versiones_esquema'):continue
        keys=inspect(connection).get_pk_constraint(name)['constrained_columns']
        rows=connection.execute(text('SELECT * FROM '+quote(name))).mappings()
        result[name]={repr(tuple(row[k] for k in keys)):hashlib.sha256(repr(tuple(row.values())).encode()).hexdigest() for row in rows}
    return result


def migrate(connection):
    from sqlalchemy import text
    from sqlalchemy.orm import Session
    from alembic import command
    from alembic.config import Config
    from scripts.importador_planillas import preparar,importar
    from app.config import SISTEMAS_HABILITADOS
    before=snapshot(connection)
    assert connection.scalar(text('SELECT version_num FROM alembic_version'))=='013_desbloqueo_revision'
    rows=preparar(STAGE/'recursos/originales_v5.zip',STAGE/'docs/pedido_codex_v1_1/catalogo_referencia_planillas.json')
    assert len(rows)==79 and all(row['sigla_validada'] and row['coincide_nombre_archivo'] and not row['fuentes_discrepantes'] for row in rows)
    with Session(bind=connection,join_transaction_mode='create_savepoint') as db:
        report=importar(db,rows,aplicar=True)
        assert report['estados']=={'YA_EXISTE':16,'IMPORTADA':63} and report['cambios']==63 and not report['errores']
        db.commit()
    config=Config(str(STAGE/'alembic.ini'));config.set_main_option('script_location',str(STAGE/'migraciones/alembic'))
    config.attributes['connection']=connection;command.upgrade(config,HEAD)
    after=snapshot(connection)
    assert set(before)==set(after)
    for name,records in before.items():
        assert all(after[name].get(key)==value for key,value in records.items()),'Cambió un registro anterior: '+name
        if name not in ('planillas','sistemas'):assert len(after[name])==len(records)
    assert len(after['planillas'])-len(before['planillas'])==63
    assert connection.scalar(text("SELECT count(DISTINCT codigo) FROM planillas WHERE codigo LIKE 'SG-PEM-IFI-%'"))>=79
    types=set(connection.scalars(text('SELECT DISTINCT tipo FROM sistemas')))
    assert types==set(SISTEMAS_HABILITADOS)
    assert connection.scalar(text('SELECT count(*) FROM clientes WHERE es_ejemplo IS NOT TRUE'))==0
    report.update(schema=HEAD,filas_historicas_conservadas=sum(map(len,before.values())),
        sistemas_agregados=len(after['sistemas'])-len(before['sistemas']),sistemas_tipo=len(types),
        planillas_totales=len(after['planillas']),datos_reales_agregados=False)
    return report


def inspect_live():
    from sqlalchemy import text
    engine,_=environment()
    with engine.begin() as c:
        c.execute(text('SET TRANSACTION READ ONLY'))
        head=c.scalar(text('SELECT version_num FROM alembic_version'))
        counts={table:c.scalar(text('SELECT count(*) FROM '+table)) for table in ('planillas','sistemas','cargas','firmas_carga','envios')}
    engine.dispose()
    return {'schema':head,'counts':counts,'hashes':{name:digest(ROOT/name) if (ROOT/name).exists() else None for name in FILES}}


def rehearse():
    engine,url=environment();name='readyproof_test_etapa5_migracion_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    with tempfile.TemporaryDirectory(prefix='.ensayo014-',dir=STORE) as directory:
        dump=Path(directory)/'db.dump'
        with dump.open('wb') as stream:
            subprocess.run(['/usr/sbin/runuser','-u','postgres','--','pg_dump','--format=custom','--no-owner','--no-acl','readyproof'],stdout=stream,stderr=subprocess.PIPE,check=True,timeout=180)
        run(['/usr/sbin/runuser','-u','postgres','--','createdb','--owner='+url.username,name])
        with dump.open('rb') as stream:
            run(['/usr/sbin/runuser','-u','postgres','--','pg_restore','--exit-on-error','--single-transaction','--no-owner','--no-acl','--role='+url.username,'--dbname='+name],stdin=stream)
        from sqlalchemy import create_engine
        test=create_engine(url.set(database=name))
        with test.begin() as c:report=migrate(c)
        test.dispose()
    engine.dispose();report.update(estado='ensayo_014_ok',base_aislada=name,produccion_modificada=False)
    (STORE/'ensayo_etapa5.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report


def apply(data):
    import grp,time
    assert data['pruebas']['estado']=='aprobada' and data['pruebas']['fallos_pendientes']==0
    assert set(data['fuentes'])==set(FILES)
    for name,value in data['fuentes'].items():assert digest(STAGE/name)==value
    previous_state=inspect_live();assert previous_state['schema']=='013_desbloqueo_revision'
    assert previous_state['hashes']==data['anteriores']
    assert json.loads((STORE/'ensayo_etapa5.json').read_text())['estado']=='ensayo_014_ok'
    os.umask(0o077);gid=grp.getgrnam('readyproof').gr_gid
    previous=STORE/('etapa5-fuentes-previas-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S'));previous.mkdir(mode=0o700)
    for name in FILES:
        p=ROOT/name
        if p.exists():
            saved=previous/name;saved.parent.mkdir(parents=True,exist_ok=True);saved.write_bytes(p.read_bytes())
    def install(name,payload):
        target=ROOT/name;assert target.resolve().is_relative_to(ROOT) and not target.is_symlink()
        assert not target.parent.is_symlink()
        if not target.parent.exists():target.parent.mkdir(mode=0o750);os.chown(target.parent,0,gid);os.chmod(target.parent,0o750)
        fd,temporary=tempfile.mkstemp(prefix='.etapa5-',dir=target.parent)
        try:
            with os.fdopen(fd,'wb') as stream:stream.write(payload)
            os.chown(temporary,0,gid);os.chmod(temporary,0o640);os.replace(temporary,target)
        finally:
            if os.path.exists(temporary):os.unlink(temporary)
    run(['systemctl','stop','readyproof'])
    try:
        run(['/var/backups/readyproof/backup_y_subida.sh'])
        backup=json.loads((STORE/'ultimo_backup.json').read_text());assert backup['schema']=='013_desbloqueo_revision'
        remote='readyproof-drive:readyproof-backups/pre-migrations/readyproof-pre-014-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'.tar.enc'
        for suffix in ('','.json'):
            run(['rclone','--config','/etc/readyproof/rclone-backup.conf','copyto',backup['remote']+suffix,remote+suffix])
        with tempfile.TemporaryDirectory(prefix='.pre014-',dir=STORE) as directory:
            p=Path(directory)/'backup.enc';run(['rclone','--config','/etc/readyproof/rclone-backup.conf','copyto',remote,str(p)])
            assert digest(p)==backup['cipher_sha256']
        for name in FILES:install(name,(STAGE/name).read_bytes())
        smoke="import sys;sys.path.insert(0,'/home/readyproof');from app import create_app;from app.planillas.catalogo_completo import definiciones_habilitadas;assert len(definiciones_habilitadas())==78;assert create_app().config['MAIL_MODO_PRUEBA']"
        run(['/usr/sbin/runuser','-u','readyproof','--',str(ROOT/'venv/bin/python'),'-c',smoke])
        engine,_=environment()
        with engine.begin() as c:report=migrate(c)
        engine.dispose()
    except Exception:
        for name in FILES:
            old=previous/name
            if old.exists():install(name,old.read_bytes())
            elif (ROOT/name).exists():(ROOT/name).unlink()
        raise
    finally:run(['systemctl','start','readyproof'])
    for attempt in range(20):
        try:
            with urlopen('http://127.0.0.1:8000/login',timeout=10) as response:assert response.status==200
            break
        except OSError:
            if attempt==19:raise
            time.sleep(1)
    report.update(estado='etapa5_aplicada',fuentes_previas=str(previous),respaldo_pre_migracion=remote,
        respaldo_pre_migracion_sha256=backup['cipher_sha256'],login_http=200,modo_piloto=True)
    (STORE/'aplicacion_etapa5.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report


def verify(data):
    for name,value in data['fuentes'].items():assert digest(ROOT/name)==value
    assert run(['systemctl','is-active','readyproof']).stdout.strip()==b'active'
    assert run(['systemctl','is-active','readyproof-backup.timer']).stdout.strip()==b'active'
    with urlopen('http://127.0.0.1:8000/static/carga.js',timeout=20) as response:
        assert hashlib.sha256(response.read()).hexdigest()==data['fuentes']['app/static/carga.js']
    with urlopen('http://127.0.0.1:8000/sw.js',timeout=20) as response:assert b'readyproof-ui-v9' in response.read()
    run(['systemctl','start','readyproof-backup.service'])
    backup=json.loads((STORE/'ultimo_backup.json').read_text());assert backup['schema']==HEAD
    restored=run([str(ROOT/'venv/bin/python'),str(ROOT/'scripts/backup_readyproof.py'),'restore','--remote',backup['remote'],
        '--schema-esperado',HEAD,'--planillas-esperadas',str(backup['counts']['planillas']),'--prefijo-prueba','readyproof_test_etapa5'])
    result=json.loads(restored.stdout);assert not result['produccion_modificada'] and result['cipher_sha256']==backup['cipher_sha256']
    report={'estado':'etapa5_respaldo_restauracion_verificados','backup':backup,'restauracion':result,
        'fuentes_coinciden':True,'app_activa':True,'timer_activo':True,'service_worker':'v9'}
    (STORE/'verificacion_etapa5.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    return report


def main():
    assert sys.platform!='win32' and os.geteuid()==0
    sys.path.insert(0,str(STAGE));os.umask(0o077)
    data=json.load(sys.stdin)
    operations={'inspeccionar':inspect_live,'ensayar':rehearse,'aplicar':lambda:apply(data),'verificar':lambda:verify(data)}
    assert data['accion'] in operations
    try:print(json.dumps(operations[data['accion']]()))
    except Exception as error:
        import traceback
        report={'estado':'fallo','accion':data['accion'],'tipo':type(error).__name__,
            'lineas':[{'archivo':f.filename,'linea':f.lineno} for f in traceback.extract_tb(error.__traceback__)]}
        (STORE/'error_etapa5.json').write_text(json.dumps(report,indent=2));print(json.dumps(report));return 1
    return 0


if __name__=='__main__':raise SystemExit(main())
