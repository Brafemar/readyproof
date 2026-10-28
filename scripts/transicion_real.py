"""Activación controlada del entorno privado; nunca versiona su configuración."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib,io,json,os,re,subprocess,sys,tempfile

VALUES={'MODO_PILOTO':'false','MAIL_MODO_PRUEBA':'false','EMPRESA_MANTENEDORA':'READYPROOF','CERTIFICADO_N':'IFI-2024-10001'}

def main():
    assert sys.platform!='win32' and os.geteuid()==0
    from dotenv import dotenv_values
    root=Path('/home/readyproof');store=Path('/var/backups/readyproof')
    data=json.load(sys.stdin)
    assert data['tests_pasando']>=541 and data['tests_fallidos']==0
    assert data['unidades_resueltas'] is True
    os.umask(0o077)
    def run(args,timeout=90):
        return subprocess.run(args,check=True,capture_output=True,timeout=timeout)
    # No imprimir Environment: puede contener secretos de otros parámetros.
    import shlex
    unit=shlex.split(run(['systemctl','show','readyproof','--property=Environment','--value']).stdout.decode())
    assert all(not v.startswith(tuple(k+'=' for k in VALUES)) for v in unit), 'Revisar precedencia systemd antes de editar dotenv.'
    paths=[root/'.env.local',root/'.env']
    assert run(['systemctl','show','readyproof','--property=EnvironmentFiles','--value']).stdout.decode().strip()=='/home/readyproof/.env (ignore_errors=no)'
    effective={}
    for path in reversed(paths):
        if path.exists():effective.update(dotenv_values(path))
    assert str(effective.get('MODO_PILOTO','true')).lower()=='true'
    assert str(effective.get('MAIL_MODO_PRUEBA','true')).lower()=='true'
    from sqlalchemy import create_engine,text
    engine=create_engine(effective['DATABASE_URL'])
    def historic_snapshot():
        result={}
        with engine.connect() as connection:
            assert connection.scalar(text('SELECT version_num FROM alembic_version'))=='017_scc1_presion_bar'
            schema=connection.scalar(text("SELECT definicion FROM planillas WHERE codigo='SG-PEM-IFI-SCC-1' AND version='00-26-bar1'"))
            assert schema['bloques']['DATOS DE LA PLANILLA IRAM 3546-16A']['J21']['unidad']=='bar'
            for name in ('cargas','firmas_carga','emisiones_carga','usuarios'):
                result[name]=sorted(hashlib.sha256(repr(tuple(row)).encode()).hexdigest()
                    for row in connection.execute(text('SELECT * FROM '+name)))
        return result
    def source_snapshot():
        return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (root/'fuente').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    source_before=source_snapshot()
    old={};edited={}
    for env in paths:
        assert env.is_file() and not env.is_symlink()
        old[env]=env.read_bytes();old_values=dotenv_values(stream=io.StringIO(old[env].decode('utf-8-sig')))
        value_env=old[env].decode('utf-8-sig')
        for key,value in VALUES.items():
            line=key+'='+('"'+value+'"' if key in ('EMPRESA_MANTENEDORA','CERTIFICADO_N') else value)
            pattern=r'(?m)^(?:export\s+)?'+re.escape(key)+r'\s*=.*$'
            value_env=re.sub(pattern,line,value_env) if re.search(pattern,value_env) else value_env.rstrip()+'\n'+line+'\n'
        new_values=dotenv_values(stream=io.StringIO(value_env))
        assert all(new_values.get(k)==v for k,v in old_values.items() if k not in VALUES)
        assert all(new_values.get(k)==v for k,v in VALUES.items())
        edited[env]=value_env.encode('utf-8')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    backup=store/('transicion-real-'+stamp);backup.mkdir(mode=0o700)
    for env,payload in old.items():(backup/(env.name+'.anterior')).write_bytes(payload)
    # El respaldo cifrado queda fuera de la rotación diaria antes del corte.
    run(['systemctl','start','readyproof-backup.service'],timeout=700)
    previous=json.loads((store/'ultimo_backup.json').read_text())
    remote='readyproof-drive:readyproof-backups/pre-migrations/readyproof-pre-real-'+stamp+'.tar.enc'
    for suffix in ('','.json'):
        run(['rclone','--config','/etc/readyproof/rclone-backup.conf','copyto',previous['remote']+suffix,remote+suffix],timeout=300)
    with tempfile.TemporaryDirectory(dir=backup) as work:
        p=Path(work)/'previo.enc'
        run(['rclone','--config','/etc/readyproof/rclone-backup.conf','copyto',remote,str(p)],timeout=300)
        assert hashlib.sha256(p.read_bytes()).hexdigest()==previous['cipher_sha256']
    import pwd,grp
    def replace(env,payload):
        fd,tmp=tempfile.mkstemp(prefix='.transicion-',dir=root)
        try:
            with os.fdopen(fd,'wb') as stream:stream.write(payload)
            os.chmod(tmp,0o600);os.chown(tmp,pwd.getpwnam('readyproof').pw_uid,grp.getgrnam('readyproof').gr_gid)
            os.replace(tmp,env)
        finally:
            if os.path.exists(tmp):os.unlink(tmp)
    run(['systemctl','stop','readyproof'])
    try:
        before=historic_snapshot()
        for env,payload in edited.items():replace(env,payload)
        code="import sys,json;sys.path.insert(0,'/home/readyproof');from app import create_app;from app.modo import validar_configuracion_real;a=create_app();ctx=a.app_context();ctx.push();validar_configuracion_real();assert not a.config['MODO_PILOTO'] and not a.config['MAIL_MODO_PRUEBA'];assert a.config['EMPRESA_MANTENEDORA']=='READYPROOF' and a.config['CERTIFICADO_N']=='IFI-2024-10001';print(json.dumps({k:a.config[k] for k in ('MODO_PILOTO','MAIL_MODO_PRUEBA','EMPRESA_MANTENEDORA','CERTIFICADO_N')}))"
        flags=json.loads(run(['/usr/sbin/runuser','-u','readyproof','--',str(root/'venv/bin/python'),'-c',code]).stdout)
        assert before==historic_snapshot() and source_before==source_snapshot()
        run(['systemctl','start','readyproof'])
        from urllib.request import urlopen
        import time
        for attempt in range(20):
            try:
                with urlopen('http://127.0.0.1:8000/login',timeout=5) as response:assert response.status==200
                break
            except (OSError,AssertionError):
                if attempt==19:raise
                time.sleep(1)
        pid=int(run(['systemctl','show','readyproof','--property=MainPID','--value']).stdout)
        process_env=dict(v.decode().split('=',1) for v in Path(f'/proc/{pid}/environ').read_bytes().split(b'\0') if b'=' in v)
        observed={k:process_env.get(k) for k in VALUES}
        if observed!=VALUES:
            diagnostic={'proceso':observed,'archivos':{p.name:{k:dotenv_values(p).get(k) for k in VALUES} for p in paths}}
            (backup/'diagnostico_parametros_no_secretos.json').write_text(json.dumps(diagnostic))
        assert observed==VALUES
    except Exception:
        for env,payload in old.items():replace(env,payload)
        run(['systemctl','reset-failed','readyproof']);run(['systemctl','restart','readyproof'])
        raise
    engine.dispose()
    result={'estado':'MODO_REAL_ACTIVO','fecha_utc':datetime.now(timezone.utc).isoformat(),'configuracion':flags,
      'backup_previo':remote,'configuracion_anterior_privada':str(backup),'fuente_modificada':False,
      'historicos_modificados':False,'firmantes_modificados':False,'correos_prueba_enviados':False}
    (store/'transicion_real.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

if __name__=='__main__':
    try:main()
    except Exception as error:
        import traceback
        report={'estado':'TRANSICION_NO_CONFIRMADA','tipo':type(error).__name__,'lineas':[{'archivo':f.filename,'linea':f.lineno} for f in traceback.extract_tb(error.__traceback__)]}
        p=Path('/var/backups/readyproof/error_transicion_real.json');p.write_text(json.dumps(report));os.chmod(p,0o600)
        print(json.dumps(report))
        raise SystemExit(1)
