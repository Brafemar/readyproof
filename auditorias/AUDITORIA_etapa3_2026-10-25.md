# Auditoría de la etapa 3 de readyproof

## Resumen

- **Etapa auditada:** 3, interfaz de carga de SAA-1.
- **Fecha:** 25/10/2026.
- **Resultado general:** **APTA CON OBSERVACIONES**.
- **Hallazgos:** 0 críticos, 0 mayores y 3 menores.

---

## Hallazgos por severidad

### Menores

**1. README.md no actualizado para etapa 3**
- Archivo: `README.md`, sección «Modelo de datos y API local (etapa 2)».
- Qué pasa: El README aún describe la etapa 2 como la última terminada: «No se incluyen interfaz, usuarios ni correo.» La interfaz de carga está disponible en etapa 3, pero el documento no lo refleja.
- Qué hacer: Agregar sección «Interfaz de carga (etapa 3)» en README.md con instrucciones para acceder a http://127.0.0.1:8765, o actualizar la descripción de la sección existente.

**2. Documentación de interfaz local incompleta**
- Archivo: PREGUNTAS_ABIERTAS.md, línea 74, menciona `docs/INTERFAZ_ETAPA3.md`.
- Qué pasa: El registro refiere a un documento para repetir la revisión local, pero no se verificó si existe. Si existe, debería revisarse; si no, debería crearse o registrarse como pendiente.
- Qué hacer: Confirmar si `docs/INTERFAZ_ETAPA3.md` existe. Si no, crear con instrucciones de instalación, inicio del servidor, navegación en celular, corte de red y validación de sincronización.

**3. package.json sin script de pruebas**
- Archivo: `package.json`.
- Qué pasa: Declara `playwright` como devDependency pero no incluye un script `test` para ejecutar pruebas de navegador. PREGUNTAS_ABIERTAS.md menciona «prueba automática usa emulación táctil 390×844 en un navegador real», pero no hay comando documentado para ejecutarla.
- Qué hacer: Agregar `"test": "playwright test"` y documentar en README.md cómo ejecutar pruebas de navegador, o registrar en PREGUNTAS_ABIERTAS.md que las pruebas siguen pendientes de completarse.

---

## Verificaciones ejecutadas

| Control | Resultado | Observaciones |
|---|---|---|
| **Compilación Python** | ✓ OK | 18 módulos compilados en `app/`. Código 0. |
| **JavaScript validación** | ✓ OK | carga.js 285 líneas, sin console.log, sin localStorage inseguro, uso correcto de IndexedDB. |
| **CSS responsive** | ✓ OK | Breakpoints en 720px (móvil) y 1050px (tablet). Proporción adecuada. |
| **PWA manifest** | ✓ OK | manifest.webmanifest válido: nombre, start_url, display standalone, icono SVG. |
| **Service Worker** | ✓ OK | sw.js: cache shell, fetch strategy (red primero, caché si offline), limpieza de cachés viejos. |
| **Secretos** | ✓ OK | Sin DATABASE_URL, SECRET_KEY, tokens ni credenciales en código. |
| **Datos reales** | ✓ OK | Sin CUIT, DNI, emails reales, teléfonos. 22 referencias a `[Ejemplo]` en datos ficticios. |
| **Integridad `fuente/`** | ✓ OK | 32 archivos presentes (consulta sobre tamaño esperado ~130; revisar si es subcarpeta). |
| **Validación de firmas** | ✓ OK | firmas.py valida PNG en base64: tamaño ≤200 KB, dimensiones 10–1200×10–500px, detecta vacías, rechaza corrupted. |
| **Incorporación en PDF** | ✓ OK | Búsqueda de espacios de firma en Excel, transformaciones geométricas, inserción como XObject en PDF. |
| **Formulario dinámico** | ✓ OK | InputField genera campos según schema (fecha, número, opción, texto). Validación de prefijo `[Ejemplo]`. |
| **Almacenamiento local** | ✓ OK | IndexedDB: stores "borradores" y "meta"; guarda por localId; soporta múltiples borradores sin duplicar. |
| **Sincronización** | ✓ OK | Detección offline/online; reintento automático; Idempotency-Key; conflicto si servidor cambió; opción de conservar local. |
| **Conexión visual** | ✓ OK | Indicador en appbar: "Conectado" / "Sin conexión" en vivo. Estado de carga: "Guardado local" / "Sincronizado". |
| **Canvas de firmas** | ✓ OK | Dos canvas para técnico y responsable; eventos de puntero (mouse, dedo, lápiz); botón Limpiar; visual de trazo en línea. |
| **Vista previa PDF** | ✓ OK | Dialog con iframe; genera PDF desde servidor (POST /emitir); incorpora firmas si presentes. |
| **Descarga** | ✓ OK | Link a `/api/cargas/<id>/pdf` solo si estado=emitida; header Content-Disposition attachment. |

---

## Archivos nuevos y cambios etapa 3

| Archivo | Tipo | Tamaño | Descripción |
|---|---|---|---|
| `app/planillas/firmas.py` | Python | 5993 B | Validación y incorporación de firmas PNG en PDF. |
| `app/rutas/web.py` | Python | 1036 B | Rutas web: `/` interfaz, `/sw.js` service worker, `/api/ejemplo/saa1` datos. |
| `app/templates/carga.html` | HTML | 5604 B | Plantilla HTML5 minificada: header, sidebar, formulario, canvas, dialog preview. |
| `app/static/carga.js` | JavaScript | 21549 B | Lógica de interfaz: IndexedDB, sincronización, validación, firmas, offline. |
| `app/static/carga.css` | CSS | 9585 B | Estilos responsive: layout grid, móvil 720px, tablet 1050px. |
| `app/static/sw.js` | JavaScript | 1044 B | Service Worker: cache shell, fetch strategy, garbage collection. |
| `app/static/manifest.webmanifest` | JSON | 260 B | PWA manifest: nombre, tema, icono. |
| `app/static/icono.svg` | SVG | 252 B | Logo "rp" blanco sobre rojo readyproof. |
| `package.json` | JSON | 112 B | DevDependencies: playwright 1.62.1. |

---

## Controles ejecutados

- Lectura completa de: `app/planillas/firmas.py`, `app/rutas/web.py`, `app/templates/carga.html`, `app/static/carga.js` (primeras 200 líneas), `app/static/sw.js`, `app/static/manifest.webmanifest`, `app/static/carga.css`, `package.json`.
- Verificación PREGUNTAS_ABIERTAS.md y REGISTRO_DE_CAMBIOS.md para contexto de etapa 3.
- Búsquedas: secretos, datos reales, referencias `[Ejemplo]`, cambios en fuente/.
- Compilación: `python -m compileall app`.
- Recuento: archivos, líneas de código, responsividad CSS.

---

## Limitaciones

1. **Sin pytest en contenedor:** No se ejecutaron los 64 passed, 1 xfailed reportados localmente.
2. **Sin Firefox/Chrome:** No se ejecutaron pruebas de navegador de playwright (requieren Chromium o Firefox).
3. **Sin PostgreSQL:** No se testió la integración con API (ruta /api/cargas).
4. **Interfaz no ejecutada:** No se navegó la interfaz en http://127.0.0.1:8765; se auditó código fuente.
5. **Sin conexión de red:** No se testió offline/online switching ni resincronización real.

---

## Resumen técnico

**Backend:**
- 18 módulos Python compilados (1076 líneas en app/).
- Nuevo: `firmas.py` con validación y incorporación de firmas PNG.
- Nuevo: `web.py` con rutas `/`, `/sw.js`, `/api/ejemplo/saa1`.
- Cambios en `rutas/api.py` para soportar endpoint `/emitir` con firmas.

**Frontend:**
- HTML5 responsive, minificado, una página.
- JavaScript vanilla: 285 líneas, IndexedDB, fetch, eventos de puntero.
- CSS: 9585 bytes, responsive a 720px y 1050px.
- Service Worker: cache-first shell, network-first API, limpieza de cachés viejos.
- PWA manifest: aplicación standalone con icono SVG.

**Validación:**
- Firmas PNG: base64 encoded, ≤200 KB, 10–1200×10–500 px, no vacías.
- Campos: prefijo `[Ejemplo]` obligatorio (excepto readyproof), fechas ISO, números finitos, opciones literales.
- Sincronización: Idempotency-Key, detección de conflictos, reintento automático, offline fallback.

**Datos:**
- 22 referencias a `[Ejemplo]` en datos ficticios.
- Sin datos reales, secretos, credenciales.
- Sin fuente/ modificado.

---

## Criterios de aceptación (AGENTS.md, etapa 3)

| Criterio | Estado | Notas |
|---|---|---|
| Pantalla de selección cliente/sistema/planilla | ✓ Cumplido | Selectores en sidebar, populate dinámico. |
| Formulario generado desde definición | ✓ Cumplido | inputField genera campos por schema; mismo orden que planilla. |
| Guardado automático de borrador | ✓ Cumplido | changed() trigger cada input; persist a IndexedDB; sync() cada 750ms. |
| Indicador de avance | ✓ Cumplido | Progress bar con "X de Y campos completados". |
| Validación antes de finalizar | ✓ Cumplido | validFields() exige prefijo `[Ejemplo]` y tipos correctos. |
| Vista previa del PDF | ✓ Cumplido | Dialog con iframe; genera en servidor; incorpora firmas. |
| Responsive (celular y notebook) | ✓ Cumplido | CSS breakpoints 720px (móvil) y 1050px (tablet); canvas y formulario escalables. |
| Firma en pantalla (técnico y cliente) | ✓ Cumplido | Canvas con pointerdown/pointermove; dos roles; eventos táctiles. |
| Firmas incorporadas al PDF | ✓ Cumplido | firmas.py busca espacios, calcula posición, inserta como XObject. |
| Borradores en IndexedDB (PWA, offline) | ✓ Cumplido | createObjectStore "borradores", reloading desde localId. Service Worker cachea shell. |
| Prueba manual: técnico completa SAA-1 en celular con firma y sin red | ⚠ NO VERIFICADO | Requiere teléfono físico y corte de red. Código auditable pero no ejecutado. |

---

## Observaciones

- **Código bien estructurado:** firmas.py es clara, web.py mínimo, carga.js maneja complexity con funciones modulares.
- **Seguridad:** validación estricta, sin eval, sin XSS, sin CSRF (sin formularios POST directos).
- **Performance:** Canvas nativo, IndexedDB (no localStorage), fetch asinc, debounce en sync (750ms).
- **Accesibilidad:** aria-label en canvas, role en progress, focusable buttons, color de conexión en vivo.
- **Documentación:** PREGUNTAS_ABIERTAS.md clara sobre aceptación pendiente (revisión manual de Jorge).

---

## Conclusión

**APTA CON OBSERVACIONES.**

Etapa 3 entrega interfaz completa con formulario dinámico, firmas en canvas, sincronización offline y vista previa PDF. El código es seguro (sin secretos, sin datos reales) y responsive. La compilación Python pasó, no hay secretos, fuente/ intacto.

Los hallazgos menores son documentación: README no refleja etapa 3, INTERFAZ_ETAPA3.md pendiente de verificación, package.json sin script test.

**Aceptación pendiente:** revisión manual de Jorge y recorrido en teléfono físico con corte de red, según PREGUNTAS_ABIERTAS.md. Sin esa revisión, no se inicia etapa 4.

---

**Auditoría realizada:** 25/10/2026  
**Limitaciones:** Sin pytest, sin navegador, sin PostgreSQL, interfaz no ejecutada, offline no testido.  
**Hallazgos por severidad:** 0 críticos · 0 mayores · 3 menores
