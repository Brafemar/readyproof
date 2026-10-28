# PWA — Instalación en celular

readyproof puede abrirse en una ventana independiente y tener un icono en la pantalla de inicio, sin APK. El código incluye manifest, cuatro iconos PNG y un único service worker. Los tres tests PWA y la verificación de Chrome local están aprobados. La instalación física en Android/iPhone debe comprobarse en el dispositivo del técnico; la evidencia remota se registra en REPORTE_PWA_FINAL.json.

## Acceso privado actual

Cada celular necesita su propio túnel SSH, con la clave individual del técnico. El túnel abierto en la PC de Jorge no sirve para el navegador del celular. Mantener la conexión mientras se consulta el servidor o se sincronizan borradores.

Configurar **reenvío local**: escuchar en `127.0.0.1:8876` del celular y reenviar a `127.0.0.1:8000` del servidor `67.205.170.29`, usando `readyproof_tunel_tecnico`. No entregar la clave de root. Ver [acceso técnico](ACCESO_TECNICO_BRAFEMAR.md).

Si el cliente SSH del dispositivo ofrece consola, la forma equivalente es:

```bash
ssh -N -L 127.0.0.1:8876:127.0.0.1:8000 -i RUTA_CLAVE_INDIVIDUAL readyproof_tunel_tecnico@67.205.170.29
```

Abrir **http://127.0.0.1:8876/login en el mismo celular**. Se usa `-L`, no `-R`: el navegador necesita el puerto local. `localhost` y `127.0.0.1` tienen la excepción de contexto seguro admitida para PWA; otras direcciones requieren HTTPS. No se verificó ni configuró un certificado HTTPS para la IP pública en esta entrega. No acceder a HTTP por la IP pública ni cambiar la dirección por la IP de la PC.

## Android — Chrome

1. Conectar el túnel propio y abrir readyproof en Chrome normal, fuera de incógnito.
2. Iniciar sesión y dejar cargar la aplicación con conexión.
3. Abrir el menú ⋮ y elegir **Instalar aplicación** o **Agregar a pantalla principal**, según la versión de Chrome.
4. Confirmar y abrir el icono readyproof desde la pantalla de inicio.

La opción depende del navegador y del dispositivo. Si no aparece, revisar el contexto seguro, el manifest y el registro del worker; no borrar los datos del sitio si hay borradores pendientes.

## iOS — Safari

1. Preparar el acceso privado propio del dispositivo y abrir readyproof en Safari.
2. Tocar **Compartir → Agregar a pantalla de inicio**.
3. Mantener **Abrir como app web** si Safari ofrece esa opción y confirmar.
4. Abrir el icono creado. La sesión y el almacenamiento de la app instalada pueden ser independientes de la pestaña de Safari.

## Sin conexión y actualizaciones

El worker cachea los assets públicos de interfaz y permite reabrir la pantalla principal después de una primera carga autenticada con conexión. Los borradores siguen en IndexedDB por cuenta, con las reglas existentes de sesión y sincronización. No se archivan respuestas de API, contraseñas, firmas ni PDF en Cache Storage. Emisión PDF, búsqueda, envío de correo e inicio de sesión requieren conexión al servidor. La instalación no mantiene por sí sola el túnel SSH.

Se conserva la dirección `/sw.js` y el alcance `/`; la implementación está en `app/static/service-worker.js`. El archivo antiguo importa la implementación. No se agregan dos handlers `fetch` con `respondWith` para una misma petición. La nueva caché es `readyproof-ui-v12`; su actualización no borra IndexedDB ni los borradores. Las páginas de perfil, administración y resultados de búsqueda no se cachean.

## Verificación

```bash
pytest tests/test_pwa.py -v
```

Resultado local verificado: **3 passed**. La prueba de navegador comprobó los recursos cacheados con el servidor local apagado; no depende del indicador navigator.onLine.

En Chrome DevTools, abrir **Application → Manifest** y comprobar nombre, modo standalone, cuatro iconos y atajos. En **Service Workers**, comprobar un único registro `/sw.js`, alcance `/`, estado activado y control de la página. En **Cache Storage**, revisar que solo haya assets y la pantalla principal, sin `/api/` ni PDF. Cargar primero con conexión; activar Offline, recargar `/`, editar un borrador y volver a Online para comprobar la sincronización. Verificar en un celular real la instalación, apertura desde el icono y persistencia de borradores. No usar datos ni correos reales para estas pruebas.

Referencias: [requisitos de instalación](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable), [iconos y zona segura](https://web.dev/learn/pwa/web-app-manifest), [Safari en iPhone](https://support.apple.com/en-lb/guide/iphone/iphea86e5236/27/ios/27).


## Verificación remota de esta entrega

El puerto real de Gunicorn en el servidor es **8000**. Para verificar en el puerto local 8443, usar reenvío local `127.0.0.1:8443 → 127.0.0.1:8000` y abrir `http://127.0.0.1:8443`. No reenviar a 5000, que corresponde únicamente al servidor Flask local de prueba. El puerto habitual 8876 del técnico continúa siendo válido; cada puerto/origen conserva su propia sesión y almacenamiento.

El código se publica antes del pull para que los archivos nuevos existan en origin. La instalación anterior tenía modificaciones autorizadas de etapas previas; antes de reconciliar Git se comparan con los commits conocidos, se respaldan código e índice, y se conserva fuente sin escrituras. Un cambio desconocido bloquea el despliegue. Luego se ejecuta pull ff-only y se reinicia exclusivamente readyproof. No se versionan ni reemplazan .env o .env.local.
