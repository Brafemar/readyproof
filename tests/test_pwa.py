"""Recursos públicos de instalación PWA, sin datos ni correos reales."""
import json
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]

def test_manifest_json_valid(client):
    response=client.get('/static/manifest.json')
    assert response.status_code==200
    assert response.mimetype=='application/manifest+json'
    data=json.loads(response.data)
    assert data['name']=='readyproof' and data['display']=='standalone'
    assert data['scope']==data['start_url']=='/'
    assert len(data['icons'])==4
    assert {(i['sizes'],i['purpose']) for i in data['icons']}=={
        ('192x192','any'),('512x512','any'),('192x192','maskable'),('512x512','maskable')}
    assert any(shortcut['url']=='/buscar' for shortcut in data['shortcuts'])

def test_service_worker_registered(client):
    response=client.get('/sw.js')
    assert response.status_code==200 and response.headers['Service-Worker-Allowed']=='/'
    assert response.data.count(b"addEventListener('install'")==1
    assert response.data.count(b"addEventListener('activate'")==1
    assert response.data.count(b"addEventListener('fetch'")==1
    assert b'skipWaiting' in response.data and b'clients.claim' in response.data
    assert client.get('/service-worker.js').data==response.data
    legacy=client.get('/static/sw.js')
    assert legacy.status_code==200 and b'Service Worker' in legacy.data
    script=client.get('/static/pwa.js').data
    assert b"serviceWorker.register('/sw.js'" in script
    page=client.get('/').get_data(as_text=True)
    assert page.count('src="/static/pwa.js"')==1
    for expected in ('/static/manifest.json','mobile-web-app-capable','apple-touch-icon','theme-color'):
        assert expected in page
    assert client.get('/buscar').status_code==200

def test_icons_exist():
    for size in (192,512):
        for name in (f'icon-{size}x{size}.png',f'icon-maskable-{size}.png'):
            path=ROOT/'app/static/icons'/name
            assert path.is_file()
            with Image.open(path) as image:
                assert image.format=='PNG' and image.size==(size,size)
                rgba=image.convert('RGBA')
                assert rgba.getextrema()[3]==(255,255)
                assert len(image.getcolors(maxcolors=size*size))>1
