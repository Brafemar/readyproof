const CACHE = 'readyproof-ui-v33-catalogo-carga';
const STATIC = [
  '/static/fotos.js','/static/fotos.css','/static/carga.css','/static/carga.js','/static/auth.js','/static/cuenta.css',
  '/static/admin.js','/static/cuenta.js','/static/pwa.css','/static/pwa.js','/static/buscar.js',
  '/static/marca/identidad.css','/static/marca/principal-color.svg',
  '/static/marca/Archivo-Black.ttf','/static/marca/FiraSans-Regular.ttf',
  '/static/marca/FiraSans-SemiBold.ttf','/static/marca/FiraSans-Bold.ttf',
  '/static/icono.svg','/static/manifest.json','/static/manifest.webmanifest',
  '/static/icons/icon-192x192.png','/static/icons/icon-512x512.png',
  '/static/icons/icon-maskable-192.png','/static/icons/icon-maskable-512.png'
];
self.addEventListener('install',event=>event.waitUntil(
  caches.open(CACHE).then(cache=>cache.addAll(STATIC)).then(()=>self.skipWaiting())
));
self.addEventListener('activate',event=>event.waitUntil(
  caches.keys().then(keys=>Promise.all(keys.filter(key=>key.startsWith('readyproof-ui-')&&key!==CACHE).map(key=>caches.delete(key))))
    .then(()=>self.clients.claim())
));
self.addEventListener('fetch',event=>{
  const url=new URL(event.request.url);
  if(event.request.method!=='GET'||url.origin!==self.location.origin)return;
  const asset=STATIC.includes(url.pathname),home=url.pathname==='/';
  // API, firmas, PDF, perfiles y resultados de búsqueda quedan fuera de Cache Storage.
  if(!asset&&!home)return;
  event.respondWith((async()=>{
    let cache;try{cache=await caches.open(CACHE);}catch{}
    if(asset){
      try{const cached=await cache?.match(event.request,{ignoreSearch:true});if(cached)return cached;}catch{}
    }
    try{
      const response=await fetch(event.request);
      if(response.ok&&!response.redirected){
        try{await cache?.put(home?'/':event.request,response.clone());}catch{}
      }
      return response;
    }catch{
      let cached;try{cached=await cache?.match(home?'/':event.request,{ignoreSearch:true});}catch{}
      return cached||new Response('El recurso no está disponible sin conexión. Volvé a conectar y recargá la pantalla.',{
        status:503,headers:{'Content-Type':'text/plain; charset=utf-8'}
      });
    }
  })());
});
