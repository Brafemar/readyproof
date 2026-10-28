# Selectores y caché de readyproof

Corrección del 27/10/2026, aplicada al servidor privado 67.205.170.29.

## Diagnóstico

Los selectores Cliente, Sistema y Planilla tenían listeners `change` y no tenían un `preventDefault()` que impidiera abrirlos. Los once elementos select de la pantalla incluyen también opciones del formulario; su cantidad no indica una falla de eventos. El servidor de revisión tenía un único cliente, `[Ejemplo] Planta de prueba`, un único sistema SAA y una planilla piloto habilitada para carga. Los cuatro grupos importados del catálogo usan otro tipo y no se ofrecían como formularios operativos: no eran la causa.

Jorge confirmó el nombre del único cliente mostrado. No se crearon clientes o sistemas adicionales en el servidor para simular disponibilidad. La interfaz informa ahora la cantidad real de opciones y remite a Administración para administrar clientes y sistemas ficticios.

En el service worker se identificó un caso reproducible: una falla de red sin copia en caché resolvía la respuesta con `undefined`; el navegador exige un objeto Response. Una URL de recurso con parámetros tampoco encontraba la copia sin parámetros. No se obtuvo el texto completo del error original de consola, por lo que este hallazgo no se presenta como identificación inequívoca de aquel mensaje.

## Cambios

- `carga.js`: indicador de disponibilidad, captura de errores en los cambios de selección y registro del service worker con `updateViaCache: none`.
- `sw.js`: caché `readyproof-ui-v3`; respuestas válidas aun sin red/caché, búsqueda de copia sin parámetros, y fallas de escritura de caché que no impiden usar la respuesta de red. La API y las operaciones de escritura siguen excluidas.
- `carga.html` y `carga.css`: texto de ayuda accesible bajo los selectores. Campos normativos, opciones de la planilla y firmas sin cambios.

No se borraron bases IndexedDB, borradores o datos del sitio. La activación renueva solo las cachés de recursos readyproof anteriores. No hace falta usar Ctrl+Shift+Delete: Ctrl+F5 obtiene la pantalla actualizada conservando los borradores.

## Verificación y despliegue

Dos regresiones nuevas aprobadas en 22.79 segundos:

1. Prueba del service worker: falta de red/caché devuelve 503, copia con parámetros disponible offline, falla de escritura no rompe red y API excluida. La misma regresión falla contra el código anterior y pasa con el nuevo.
2. Navegador Chromium con PostgreSQL temporal: dos clientes, varios sistemas y una segunda versión de planilla con igual definición, exclusivamente en pruebas. Cliente cambió dos veces; Sistema y Planilla una vez cada uno; se comprobaron los identificadores del borrador de IndexedDB y su sincronización, recarga, copia offline con parámetros y cero errores de página.

Aplicados cuatro archivos, previa comparación con la versión desplegada. Respaldo privado en `/root/readyproof-selectores-20261027/antes.tar.gz`, resultado en la misma carpeta. Reiniciado únicamente `readyproof.service`; login HTTP 200, caché nueva y elemento de ayuda servidos, servicio activo sin reinicios inesperados. No se modificaron registros de negocio, SMTP, dominio, puertos, servicios Docker o Traefik.

Jorge confirmó después de Ctrl+F5: **«Sí, abren y aparece el indicador»**. Quedan confirmados los dropdowns y la recarga en su navegador real. La consola F12 de esa sesión no se inspeccionó: Jorge indicó que no sabía revisarla. La corrección del service worker quedó verificada por regresión y por navegador aislado, sin afirmar una inspección de la consola personal.

Suite completa final: **158 passed in 487.56s (0:08:07), código 0**. `compileall app/ tests/`: código 0. Los cuatro hashes desplegados coinciden con la copia local y no se encontraron valores de secretos configurados en los entregables revisados.

Evidencias locales: `out/selectores_navegador/resultado.json`, `out/selectores_navegador/selectores.png`, `out/correccion_selectores/servidor.json`, `out/correccion_selectores/regresion_sw_anterior.txt`, `out/correccion_selectores/pytest_completo.txt` y `out/correccion_selectores/revision.json`.
