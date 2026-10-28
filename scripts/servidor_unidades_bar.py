"""Ensayo y migración aditiva de la versión SCC-1 autorizada en bar."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,tempfile
ROOT=Path('/home/readyproof');STAGE=Path('/home/readyproof_revision_etapa5')
FILES=('app/planillas/catalogo_completo.py','app/planillas/unidades_autorizadas.py','migraciones/alembic/versions/017_scc1_presion_bar.py','app/static/carga.js','app/static/sw.js','app/templates/carga.html')

def main():
    assert os.geteuid()==0 and sys.platform!='win32'
    os.umask(0o077);sys.path.insert(0,str(STAGE))
    from servidor_etapa6 import environment,snapshot,STORE
    from sqlalchemy import create_engine,text
    from alembic import command
    from alembic.config import Config
    from datetime import datetime,timezone
    data=json.load(sys.stdin)
    for name,digest in data['fuentes'].items():assert hashlib.sha256((STAGE/name).read_bytes()).hexdigest()==digest
    assert set(data['fuentes'])==set(FILES)
    def upgrade(c):
        assert c.scalar(text('SELECT version_num FROM alembic_version'))=='016_tabla_auditoria'
        before=snapshot(c)
        cfg=Config(str(STAGE/'alembic.ini'));cfg.set_main_option('script_location',str(STAGE/'migraciones/alembic'));cfg.attributes['connection']=c
        command.upgrade(cfg,'017_scc1_presion_bar')
        after=snapshot(c);assert set(before)==set(after)
        for name,rows in before.items():
            assert all(after[name].get(key)==digest for key,digest in rows.items()),name
            assert len(after[name])==len(rows)+(1 if name=='planillas' else 0),name
        return {'schema':'017_scc1_presion_bar','historicos_modificados':False,'versiones_agregadas':1,'filas_anteriores_conservadas':sum(map(len,before.values()))}
    engine,url=environment()
    if data['accion']=='ensayar':
        name='readyproof_test_bar_'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
        with tempfile.TemporaryDirectory(dir=STORE) as work:
            p=Path(work)/'bd.dump'
            with p.open('wb') as stream:subprocess.run(['runuser','-u','postgres','--','pg_dump','--format=custom','--no-owner','--no-acl','readyproof'],stdout=stream,stderr=subprocess.PIPE,check=True,timeout=180)
            subprocess.run(['runuser','-u','postgres','--','createdb','--owner='+url.username,name],check=True,capture_output=True)
            with p.open('rb') as stream:subprocess.run(['runuser','-u','postgres','--','pg_restore','--exit-on-error','--single-transaction','--no-owner','--no-acl','--role='+url.username,'--dbname='+name],stdin=stream,capture_output=True,check=True)
            test=create_engine(url.set(database=name))
            with test.begin() as c:report=upgrade(c)
            test.dispose()
        report.update(base_aislada=name,produccion_modificada=False)
        (STORE/'ensayo_bar.json').write_text(json.dumps(report));print(json.dumps(report));return
    assert data['accion']=='aplicar' and data['tests_pasando']>=543 and not data['tests_fallidos']
    assert json.loads((STORE/'ensayo_bar.json').read_text())['schema']=='017_scc1_presion_bar'
    subprocess.run(['systemctl','start','readyproof-backup.service'],check=True,capture_output=True,timeout=700)
    backup=json.loads((STORE/'ultimo_backup.json').read_text());assert backup['schema']=='016_tabla_auditoria'
    remote='readyproof-drive:readyproof-backups/pre-migrations/readyproof-pre-017-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'.tar.enc'
    for suffix in ('','.json'):
        subprocess.run(['rclone','--config','/etc/readyproof/rclone-backup.conf','copyto',backup['remote']+suffix,remote+suffix],check=True,capture_output=True,timeout=300)
    with tempfile.TemporaryDirectory(dir=STORE) as work:
        p=Path(work)/'previo.enc'
        subprocess.run(['rclone','--config','/etc/readyproof/rclone-backup.conf','copyto',remote,str(p)],check=True,capture_output=True,timeout=300)
        assert hashlib.sha256(p.read_bytes()).hexdigest()==backup['cipher_sha256']
    saved=STORE/('unidades-bar-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S'));saved.mkdir(mode=0o700)
    import grp
    old={name:(ROOT/name).read_bytes() if (ROOT/name).exists() else None for name in FILES}
    for name,raw in old.items():
        if raw is not None:p=saved/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
    def install(name,raw):
        p=ROOT/name;p.write_bytes(raw);os.chmod(p,0o640);os.chown(p,0,grp.getgrnam('readyproof').gr_gid)
    subprocess.run(['systemctl','stop','readyproof'],check=True,capture_output=True)
    try:
        for name in FILES:install(name,(STAGE/name).read_bytes())
        with engine.begin() as c:report=upgrade(c)
    except Exception:
        for name,raw in old.items():
            if raw is None:(ROOT/name).unlink(missing_ok=True)
            else:install(name,raw)
        raise
    finally:subprocess.run(['systemctl','start','readyproof'],check=True,capture_output=True)
    engine.dispose();report.update(estado='VERSION_BAR_APLICADA',respaldo_previo=remote)
    (STORE/'aplicacion_bar.json').write_text(json.dumps(report));print(json.dumps(report))

if __name__=='__main__':
    try:main()
    except Exception as error:
        import traceback
        print(json.dumps({'estado':'fallo','tipo':type(error).__name__,'lineas':[{'archivo':f.filename,'linea':f.lineno} for f in traceback.extract_tb(error.__traceback__)]}),file=sys.stderr)
        raise SystemExit(1)
