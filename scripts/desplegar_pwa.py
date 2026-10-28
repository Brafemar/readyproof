"""Actualiza readyproof por Git preservando el estado operativo previo al pull."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys

ROOT=Path('/home/readyproof');STORE=Path('/var/backups/readyproof')

def main():
    assert sys.platform!='win32' and os.geteuid()==0
    os.umask(0o077);data=json.load(sys.stdin)
    assert len(data['base'])==len(data['destino'])==40
    def run(args,timeout=180,**kwargs):
        return subprocess.run(args,cwd=ROOT,check=True,capture_output=True,timeout=timeout,**kwargs)
    def git(*args):
        return run(['git','-c','safe.directory='+str(ROOT),'-c','core.hooksPath=/dev/null',*args],env=dict(os.environ,GIT_TERMINAL_PROMPT='0'),umask=0o022).stdout
    assert git('branch','--show-current').strip()==b'main'
    assert not git('diff','--cached','--name-only').strip()
    old=git('rev-parse','HEAD').decode().strip()
    git('fetch','origin','main')
    assert git('rev-parse','origin/main').decode().strip()==data['destino']
    git('merge-base','--is-ancestor',old,data['base'])
    git('merge-base','--is-ancestor',data['base'],data['destino'])
    def tree(ref):
        result={}
        for row in git('ls-tree','-r','-z',ref).split(b'\0'):
            if not row:continue
            meta,name=row.split(b'\t',1);mode,kind,oid=meta.decode().split()
            assert kind=='blob' and mode in ('100644','100755')
            name=name.decode();assert not Path(name).is_absolute() and '..' not in Path(name).parts
            assert Path(name).name not in ('.env','.env.local')
            result[name]=(oid,mode)
        return result
    previous=tree(old);base=tree(data['base']);target=tree(data['destino'])
    assert set(base)<=set(target),'La entrega no debe eliminar archivos históricos.'
    blobs={}
    def blob(oid):
        if oid not in blobs:blobs[oid]=git('cat-file','blob',oid)
        return blobs[oid]
    def same(first,second):
        return first==second or (b'\0' not in first and b'\0' not in second and first.replace(b'\r\n',b'\n')==second.replace(b'\r\n',b'\n'))
    unknown=[]
    for name,(oid,mode) in target.items():
        path=ROOT/name
        assert not path.is_symlink() and path.resolve().is_relative_to(ROOT)
        if name.startswith('fuente/'):
            assert path.is_file() and path.read_bytes()==blob(oid),'Fuente debe permanecer idéntica: '+name
        elif path.exists():
            assert path.is_file()
            choices=[blob(v[0]) for v in (base.get(name),previous.get(name),target.get(name)) if v]
            if not any(same(path.read_bytes(),value) for value in choices):unknown.append(name)
    assert not unknown,'Cambios ajenos a los commits verificados: '+','.join(unknown)
    if data['accion']=='inspeccionar':
        print(json.dumps({'estado':'PLAN_GIT_VALIDADO','head_anterior':old,'base_verificada':data['base'],'destino':data['destino'],'archivos_objetivo':len(target),'cambios_desconocidos':unknown}));return
    assert data['accion']=='aplicar'
    from dotenv import dotenv_values
    flags={};private={}
    for path in (ROOT/'.env',ROOT/'.env.local'):
        private[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
        flags.update(dotenv_values(path))
    assert flags['MODO_PILOTO']=='false' and flags['MAIL_MODO_PRUEBA']=='false'
    assert flags['EMPRESA_MANTENEDORA']=='READYPROOF' and flags['CERTIFICADO_N']=='IFI-2024-10001'
    def source_hashes():
        return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'fuente').rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    source=source_hashes()
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    saved=STORE/('pwa-previas-'+stamp);saved.mkdir(mode=0o700)
    names=[name for name in target if not name.startswith('fuente/')]
    original={}
    for name in names:
        p=ROOT/name;original[name]=p.read_bytes() if p.exists() else None
        if p.exists():
            destination=saved/'archivos'/name;destination.parent.mkdir(parents=True,exist_ok=True);destination.write_bytes(original[name])
    shutil.copy2(ROOT/'.git/index',saved/'index_anterior')
    (saved/'estado.json').write_text(json.dumps({'head':old,'existentes':[n for n,v in original.items() if v is not None]},indent=2))
    run(['systemctl','start','readyproof-backup.service'],timeout=700)
    backup=json.loads((STORE/'ultimo_backup.json').read_text())
    assert backup['schema']=='017_scc1_presion_bar'
    remote='readyproof-drive:readyproof-backups/pre-migrations/readyproof-pre-pwa-'+stamp+'.tar.enc'
    for suffix in ('','.json'):
        run(['rclone','--config','/etc/readyproof/rclone-backup.conf','copyto',backup['remote']+suffix,remote+suffix],timeout=300)
    run(['systemctl','stop','readyproof'])
    try:
        sys.path.insert(0,'/home/readyproof_revision_etapa5/scripts')
        from servidor_etapa6 import snapshot,environment
        engine,_=environment()
        with engine.connect() as c:before=snapshot(c)
        # Hidratar el commit ya validado reconcilia las etapas desplegadas sin
        # revertir fuente ni tocar archivos privados. El pull posterior es ff-only.
        import grp
        gid=grp.getgrnam('readyproof').gr_gid
        def parent_directory(path):
            missing=[]
            while not path.exists():missing.append(path);path=path.parent
            for path in reversed(missing):
                path.mkdir();os.chown(path,0,gid);os.chmod(path,0o755)
        for name,(oid,mode) in base.items():
            if name.startswith('fuente/'):continue
            p=ROOT/name;parent_directory(p.parent)
            p.write_bytes(blob(oid));os.chmod(p,0o755 if mode=='100755' else 0o644)
            os.chown(p,0,gid)
        git('reset','--mixed',data['base'])
        assert not git('status','--porcelain','--untracked-files=no').strip(),'La base reconciliada debe quedar limpia.'
        output=git('pull','--ff-only','origin','main').decode()
        assert git('rev-parse','HEAD').decode().strip()==data['destino']
        assert not git('status','--porcelain','--untracked-files=no').strip()
        assert source==source_hashes()
        assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in private.items())
        with engine.connect() as c:assert before==snapshot(c)
        engine.dispose()
        run(['systemctl','restart','readyproof'])
        from urllib.request import urlopen
        import time
        for attempt in range(30):
            try:
                with urlopen('http://127.0.0.1:8000/static/manifest.json',timeout=5) as response:
                    assert json.load(response)['name']=='readyproof'
                break
            except OSError:
                if attempt==29:raise
                time.sleep(1)
    except Exception:
        for name,raw in original.items():
            p=ROOT/name
            if raw is None:p.unlink(missing_ok=True)
            else:p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
        git('update-ref','refs/heads/main',old)
        shutil.copy2(saved/'index_anterior',ROOT/'.git/index')
        run(['systemctl','reset-failed','readyproof']);run(['systemctl','restart','readyproof'])
        raise
    result={'estado':'PWA_DESPLEGADA','fecha_utc':datetime.now(timezone.utc).isoformat(),'commit':data['destino'],'pull':output,
        'backup_previo':remote,'copia_codigo_anterior':str(saved),'fuente_modificada':False,'entornos_modificados':False,'historicos_modificados':False,
        'modo_piloto':False,'mail_modo_prueba':False,'servicio':run(['systemctl','is-active','readyproof']).stdout.decode().strip()}
    (STORE/'despliegue_pwa.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

if __name__=='__main__':
    try:main()
    except Exception as error:
        import traceback
        report={'estado':'ERROR_DESPLIEGUE_PWA','tipo':type(error).__name__,'motivo':str(error) if isinstance(error,AssertionError) else 'Ver diagnóstico privado.',
            'lineas':[{'archivo':f.filename,'linea':f.lineno} for f in traceback.extract_tb(error.__traceback__)]}
        print(json.dumps(report));raise SystemExit(1)
