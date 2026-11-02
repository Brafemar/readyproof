"use strict";
(() => {
  if (!('serviceWorker' in navigator) || !window.isSecureContext) return;
  let controller = navigator.serviceWorker.controller, notice, button, status, updating = false;
  const formsWithChanges = new Set();
  document.addEventListener('input', event => {
    const form = event.target.closest('form');
    if (form && form.id !== 'formulario') formsWithChanges.add(form);
  });
  document.addEventListener('reset', event => formsWithChanges.delete(event.target));
  function available() {
    if (notice) return;
    notice = document.createElement('aside');
    notice.className = 'pwa-actualizacion';
    notice.setAttribute('aria-label', 'Actualización de readyproof');
    const title = document.createElement('strong');
    title.textContent = 'Nueva versión disponible';
    status = document.createElement('p');
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    status.textContent = 'Guardá y sincronizá tus cambios antes de actualizar.';
    button = document.createElement('button');
    button.type = 'button';
    button.textContent = 'Actualizar readyproof';
    button.onclick = update;
    notice.append(title, status, button);
    document.body.prepend(notice);
  }
  async function update() {
    if (updating) return;
    updating = true;
    button.disabled = true;
    const dialog = document.createElement('dialog');
    dialog.className = 'pwa-actualizacion-dialog';
    dialog.textContent = 'Comprobando que los cambios estén guardados…';
    dialog.addEventListener('cancel', event => event.preventDefault());
    document.body.append(dialog);
    dialog.showModal();
    try {
      if ([...formsWithChanges].some(form => form.isConnected))
        throw new Error('Terminá el formulario abierto y volvé a la pantalla de trabajo antes de actualizar.');
      for (const [element, guard] of [['formulario', 'readyproofActualizacionCarga'], ['fotos', 'readyproofActualizacionFotos']]) {
        if (!document.getElementById(element)) continue;
        if (typeof window[guard] !== 'function') throw new Error('Esperá a que termine de abrir la planilla antes de actualizar.');
        let timeout;
        let reason;
        try {
          reason = await Promise.race([
            Promise.resolve().then(() => window[guard]()),
            new Promise((_, reject) => { timeout = setTimeout(() => reject(new Error('No se pudo comprobar el guardado en 15 segundos. Volvé a intentar; la pantalla no se recargó.')), 15000); })
          ]);
        } finally { clearTimeout(timeout); }
        if (reason) throw new Error(reason);
      }
      window.location.reload();
    } catch (error) {
      status.textContent = error.message || 'No se pudo comprobar el guardado. No se actualizó la pantalla.';
      dialog.close();
      dialog.remove();
      button.disabled = false;
      updating = false;
      button.focus();
    }
  }
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    const previous = controller;
    controller = navigator.serviceWorker.controller;
    if (previous && controller && previous !== controller) available();
  });
  // El worker conserva su activación existente; la pantalla se recarga solo con el botón.
  navigator.serviceWorker.register('/sw.js', {scope:'/', updateViaCache:'none'})
    .then(() => { document.documentElement.dataset.pwa = 'registrada'; })
    .catch(() => {
      document.documentElement.dataset.pwa = 'sin-conexion-preparada';
      console.warn('No se pudo preparar la reapertura sin conexión. Conservá los borradores del dispositivo.');
    });
})();
