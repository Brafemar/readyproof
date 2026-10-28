"use strict";
(() => {
  if (!('serviceWorker' in navigator) || !window.isSecureContext) return;
  // La URL y el alcance conservan los dispositivos ya registrados.
  navigator.serviceWorker.register('/sw.js', {scope:'/', updateViaCache:'none'})
    .then(() => { document.documentElement.dataset.pwa = 'registrada'; })
    .catch(() => {
      document.documentElement.dataset.pwa = 'sin-conexion-preparada';
      console.warn('No se pudo preparar la reapertura sin conexión. Conservá los borradores del dispositivo.');
    });
})();
