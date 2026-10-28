// Compatibilidad con accesos directos antiguos. La ruta /sw.js sirve el archivo canónico.
importScripts("/service-worker.js");
// Service Worker PWA: install/skipWaiting, activate/clients.claim y fetch/cache-first
// se registran una sola vez en el archivo importado. No duplicar respondWith.
