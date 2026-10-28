"""Servidor Flask 5000 y aceptación PWA sobre PostgreSQL y usuario efímeros."""
import json,os,secrets,shutil,socket,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import urlopen
from uuid import uuid4

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'out/pwa_final'/datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')

def main():
    sys.path.insert(0,str(ROOT))
    from tests import conftest as fixtures
    OUT.mkdir(parents=True)
    base=ROOT/'.venv/tmp'/('pwa'+uuid4().hex[:6]);assert not base.exists();base.mkdir()
    (OUT.parent/'ultimo.json').write_text(json.dumps({'carpeta':str(OUT)}))
    class Factory:
        def mktemp(self,name):
            path=base/(name+uuid4().hex[:4]);path.mkdir();return path
    with socket.socket() as probe:probe.bind(('127.0.0.1',5000))
    pg=fixtures.postgres_temporal.__wrapped__(Factory());settings=next(pg)
    database=fixtures.database_url.__wrapped__(settings);url=next(database)
    application=None;server=None
    try:
        application=fixtures.app.__wrapped__(url,base);app=next(application)
        user=fixtures.usuario_admin.__wrapped__(app)
        env=dict(os.environ,DATABASE_URL=url,SECRET_KEY=secrets.token_urlsafe(48),MODO_PILOTO='true',MAIL_MODO_PRUEBA='true',DOCUMENTACION_MODO_PRUEBA='true',READYPROOF_HTTPS='false',FLASK_DEBUG='0')
        with (OUT/'flask_5000.log').open('w',encoding='utf-8') as log:
            server=subprocess.Popen([sys.executable,'-m','flask','--app','app:create_app','run','--host=127.0.0.1','--port=5000','--no-reload'],cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT)
            for _ in range(60):
                if server.poll() is not None:raise RuntimeError('Flask terminó antes de responder.')
                try:
                    with urlopen('http://127.0.0.1:5000/login',timeout=2) as response:
                        if response.status==200:break
                except OSError:time.sleep(.5)
            else:raise RuntimeError('Flask 5000 no respondió.')
            browser_env=dict(env,RP_URL='http://127.0.0.1:5000',RP_LOGIN=user['login'],RP_PASSWORD=user['clave'],RP_OUT=str(OUT),
                NODE_PATH=str(Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules'))
            node=shutil.which('node') or str(Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe')
            with (OUT/'navegador.log').open('w',encoding='utf-8') as browser_log:
                browser=subprocess.Popen([node,'tests/browser/pwa.cjs'],cwd=ROOT,env=browser_env,stdout=browser_log,stderr=subprocess.STDOUT)
                deadline=time.monotonic()+180
                while browser.poll() is None:
                    if (OUT/'desconectar.request').exists() and not (OUT/'desconectado.ok').exists():
                        server.terminate();server.wait(timeout=15)
                        (OUT/'desconectado.ok').write_text('Servidor de prueba detenido; no existe respuesta de red local.')
                    if time.monotonic()>deadline:
                        browser.terminate();browser.wait(timeout=15);raise RuntimeError('Tiempo de verificación agotado.')
                    time.sleep(.1)
            result=(OUT/'navegador.log').read_text(encoding='utf-8')
            if browser.returncode:
                print(result[-3500:]);raise RuntimeError('Verificación PWA fallida; detener según encargo.')
            print(result)
    finally:
        if server is not None:
            server.terminate()
            try:server.wait(timeout=15)
            except subprocess.TimeoutExpired:server.kill();server.wait()
        if application is not None:
            try:next(application)
            except StopIteration:pass
        try:next(database)
        except StopIteration:pass
        try:next(pg)
        except StopIteration:pass

if __name__=='__main__':main()
