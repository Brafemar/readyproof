const CACHE = "readyproof-ui-v10";
const SHELL = ["/", "/static/carga.css", "/static/carga.js", "/static/auth.js", "/static/cuenta.css", "/static/icono.svg", "/static/manifest.webmanifest"];
self.addEventListener("install", event => event.waitUntil(caches.open(CACHE).then(cache => cache.addAll(SHELL)).then(() => self.skipWaiting())));
self.addEventListener("activate", event => event.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(key => key.startsWith("readyproof-") && key !== CACHE).map(key => caches.delete(key)))).then(() => self.clients.claim())));
self.addEventListener("fetch", event => {
  const url = new URL(event.request.url);
  if (event.request.method !== "GET" || url.origin !== self.location.origin || url.pathname.startsWith("/api/") || !SHELL.includes(url.pathname)) return;
  event.respondWith((async () => {
    try {
      const response = await fetch(event.request);
      if (response.ok) {
        // Una falla de caché no debe impedir usar una respuesta válida de la red.
        try { await (await caches.open(CACHE)).put(event.request, response.clone()); } catch {}
      }
      return response;
    } catch {
      let cached;
      try { cached = await (await caches.open(CACHE)).match(event.request, {ignoreSearch:true}); } catch {}
      return cached || new Response("El recurso no está disponible sin conexión. Volvé a conectar y recargá la pantalla.", {
        status:503, headers:{"Content-Type":"text/plain; charset=utf-8"}
      });
    }
  })());
});
