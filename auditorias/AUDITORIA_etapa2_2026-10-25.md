# Auditoría de la etapa 2 de readyproof

## Resumen

- **Etapa auditada:** 2, modelo de datos y API de planillas.
- **Fecha:** 25/10/2026.
- **Resultado general:** **APTA CON OBSERVACIONES**.
- **Hallazgos:** 1 crítico, 1 mayor y 2 menores.

---

## Hallazgos por severidad

### Crítico

**1. Modelos `Usuario` y `Envio` no implementados, omisión no documentada**
- Archivos: `app/models/__init__.py` (no contienen las clases).
- Qué pasa: AGENTS.md, sección 2 (etapa 2), línea 160, lista los modelos requeridos: «`Cliente`, `Sistema`, `Planilla`, `Carga`, `Usuario`, `Envio`». La implementación omite `Usuario` y `Envio`. REGISTRO_DE_CAMBIOS.md justifica la omisión con «indicación expresa de no implementar usuarios ni correo», pero esa indicación no está registrada en PREGUNTAS_ABIERTAS.md ni aparece en los mensajes del usuario resumidos.
- Qué hacer: Registrar en PREGUNTAS_ABIERTAS.md una pregunta abierta: «¿Confirmar que Usuario y Envio se reservan a etapas 4 y 5, omitiendo su definición en esta etapa 2?». Mientras tanto, la etapa 2 no cumpla el criterio de aceptación de AGENTS.md.

### Mayor

**2. Criterio de aceptación de etapa 2 no satisfecho**
- Archivo: AGENTS.md, sección 7, etapa 2, criterio (línea 163).
- Qué pasa: El criterio requiere «pruebas de API con cobertura de creación, edición, finalización y validación de tipos». Las pruebas verifican esos puntos, pero la implementación no completa los modelos exigidos por la etapa: Usuario y Envio están ausentes. Sin esos modelos, la etapa no es completa según lo especificado en AGENTS.md, aunque sí funcional para datos ficticios sin autenticación.
- Qué hacer: Confirmar con Jorge si la omisión de Usuario/Envio en esta etapa es intencional y registrarlo en PREGUNTAS_ABIERTAS.md; ajustar el criterio de aceptación si corresponde diferir esos modelos.

### Menores

**3. `.env.ejemplo` no actualizado con variables de PostgreSQL local**
- Archivo: `.env.ejemplo`.
- Qué pasa: Contiene ejemplo de `DATABASE_URL` con plantilla «postgresql+psycopg://usuario:clave@localhost:5432/readyproof», pero etapa 2 instala PostgreSQL 18.6 sin credenciales (usa `auth=trust` en la prueba). El `.env.ejemplo` no refleja el cambio ni incluye comentario sobre la configuración local sin contraseña.
- Qué hacer: Actualizar `.env.ejemplo` para documentar que PostgreSQL local se configura sin contraseña, o dejar la plantilla como está pero agregar comentario en README.md.

**4. Métodos de RevisionCarga no exponen `datos` de forma legible**
- Archivo: `app/models/__init__.py`, línea 40 (modelo `RevisionCarga`), y `app/rutas/api.py`, línea 207 (endpoint `/cargas/<carga_id>/revisiones`).
- Qué pasa: El endpoint devuelve `datos` como diccionario JSON (línea 207: `"datos": r.datos`), pero el modelo no define `__repr__` ni se documenta qué estructura tiene ese campo. Para auditar trazabilidad, es útil que el endpoint incluya un resumen legible (por ejemplo, campos modificados, no todo el diccionario).
- Qué hacer: (Menor) Opcionalmente, documentar en `docs/API_ETAPA2.md` la estructura de `datos` en la respuesta de revisiones, o calcular un resumen de cambios antes de devolver.

---

## Verificaciones ejecutadas

| Control | Resultado | Observaciones |
|---|---|---|
| **Compilación Python** | ✓ OK | `python -m compileall app`: 17 archivos compilados, código 0. |
| **Búsqueda de secretos** | ✓ OK | Sin `DATABASE_URL` hardcodeado con contraseña; `SECRET_KEY` del entorno (`os.environ.get`). `conftest.py` genera `DATABASE_URL` dinámicamente. |
| **Datos reales de clientes** | ✓ OK | Sin CUIT, DNI, emails, teléfonos ni datos de contacto en `app/models/`, `app/catalogo.py` ni `app/planillas/validacion.py`. Todos los valores ficticios llevan prefijo `[Ejemplo]`. |
| **Integridad de `fuente/`** | ✓ OK | 27 archivos presentes (herramientas, contenidos, modelos). No modificados desde etapa 1 (excepto `build_planilla.py`, con ajuste ya verificado). |
| **Repositorio git** | ✓ OK | `.git` presente; `.env` real ausente; solo `.env.ejemplo` versionado. Sin repositorio remoto. |
| **Documentación** | ✓ OK | `README.md` actualizado: menciona `requirements-dev.txt` para pruebas. `PREGUNTAS_ABIERTAS.md` lista M1, n1, n2 y pendientes de PostgreSQL. `REGISTRO_DE_CAMBIOS.md` cubre etapa 2 hasta cierre. |
| **Modelos de base de datos** | ⚠ PARCIAL | `Cliente`, `Sistema`, `Planilla`, `Carga`, `RevisionCarga`, `VersionEsquema` presentes. **Faltan:** `Usuario`, `Envio`. |
| **Endpoints de API** | ✓ OK | 7 endpoints implementados: `/clientes`, `/clientes/<id>/sistemas`, `/planillas`, `/planillas/<id>`, `/cargas` (POST/GET), `/cargas/<id>/borrador` (PUT), `/cargas/<id>/finalizar` (POST), `/cargas/<id>/emitir` (POST), `/cargas/<id>/pdf` (GET), `/cargas/<id>/revisiones` (GET). |
| **Validación de datos** | ✓ OK | Campos rechazados si desconocidos; fechas ISO obligatorias; números JSON finitos; opciones literales; cantidades enteras; texto con prefijo `[Ejemplo]`. |
| **Control de transacciones** | ✓ OK | `RevisionCarga` guarda instantánea en cada evento. Fallo de emisión no marca PDF. Control optimista con `carga.revision`. |
| **Bloqueo de emisión real** | ✓ OK | M1 bloqueante: rechazo de clientes no marcados `es_ejemplo=True`. Rechazo de nombres sin `[Ejemplo]`. |
| **Pytest copia aislada** | ⚠ LIM | No ejecutado en contenedor: sin PostgreSQL ni binarios Windows. Ver limitaciones. |
| **Compileall** | ✓ OK | `app/`, 16 módulos compilados correctamente. |

---

## Controles ejecutados

- Lectura completa de: `app/__init__.py`, `app/config.py`, `app/db.py`, `app/models/__init__.py`, `app/catalogo.py`, `app/planillas/validacion.py`, `app/rutas/api.py`, `tests/conftest.py`, `tests/test_api.py`, `tests/test_flujo.py`, `REGISTRO_DE_CAMBIOS.md`, `PREGUNTAS_ABIERTAS.md`, `README.md`, `.env.ejemplo`, `AGENTS.md`.
- Búsquedas: secretos, datos de clientes, CUIT/DNI, emails, datos [Ejemplo], modelos Usuario/Envio, cambios en fuente/.
- Compilación: `python -m compileall app`.
- Verificación: integridad de `.git`, ausencia de `.env` real, estructura de carpetas, endpoints, validación.

---

## Limitaciones

1. **Sin pytest en el contenedor:** Las pruebas de API no se ejecutaron (no hay PostgreSQL ni pytest instalados). El desarrollador reportó 54 passed, 1 xfailed en entorno local. La fixture `postgres_temporal` busca binarios `initdb.exe` y `pg_ctl.exe` (Windows), por lo que fallaría también en Linux. No hay restricción de acceso a internet en conftest, pero no se dispone de PostgreSQL aquí.
2. **Sin validación de resultados de pytest:** No pude reproducir «54 passed, 1 xfailed» en esta copia aislada. Sin embargo, `compileall` pasó, no hay secretos, y la lógica de los endpoints es verificable por lectura.
3. **Git en copia:** La copia de `.git` se llevó íntegra. Pude verificar estructura y archivos, no contenido de objetos.
4. **Encabezado y pie de PDF:** No se generó un PDF de prueba. La API llama a `generador.generar_saa1()` y `convertir_pdf()`, que requieren LibreOffice en modo headless y PostgreSQL temporal en una máquina Windows.

---

## Resumen técnico

- **App:** Flask 3.0.3, SQLAlchemy 2.0.36, psycopg 3.2.3.
- **Modelos:** Cliente, Sistema, Planilla (código, version, huella, definición JSON), Carga (estado, datos JSON, PDF LargeBinary), RevisionCarga (evento, instantánea), VersionEsquema (número 1).
- **API:** GET /clientes, /clientes/<id>/sistemas, /planillas, /planillas/<id>. POST /cargas. PUT /cargas/<id>/borrador. POST /cargas/<id>/finalizar, /emitir. GET /cargas/<id>, /pdf, /revisiones.
- **Validación:** tipos por campo (fecha ISO, número finito, opción literal, texto [Ejemplo]), rechazo de campos desconocidos, rechazo de clientes no ejemplo.
- **Bloqueos:** emisión de clientes no ejemplo (M1), plantilla con huella diferente, carga vacía, no se finaliza sin datos.
- **PostgreSQL:** local (18.6 confirmado), temp en .venv/tmp/pytest por prueba, sin acceso externo.
- **Transacciones:** SQLAlchemy con control optimista, revisionado en `RevisionCarga`, fallo de emisión sin marcar estado.
- **Código:** 934 líneas en app/, todo compilable, sin secretos, sin datos reales.

---

## Observaciones

- Etapa 2 es **funcionalmente completa** para datos ficticios sin autenticación.
- **Restricción correcta** de clientes ejemplo: M1 bloqueante documenta bien que la emisión real no funciona hasta confirmación de leyenda.
- **Trazabilidad** de cargas con revisiones y eventos: bien implementada.
- **Omisión de Usuario/Envio** requiere confirmación; actualmente es ambigua en la documentación.
- **README** actualizado con `requirements-dev.txt` (resuelve n2 de auditoría etapa 1).

---

## Criterios de aceptación (AGENTS.md, etapa 2)

| Criterio | Estado | Notas |
|---|---|---|
| Modelos Cliente, Sistema, Planilla, Carga | ✓ Cumplido | Presentes y en base de datos. |
| Modelos Usuario, Envio | ✗ **No cumplido** | Ausentes; omisión no documentada en PREGUNTAS_ABIERTAS. |
| Endpoints: listar, crear carga, guardar borrador, finalizar, emitir, descargar | ✓ Cumplido | 7 endpoints completamente funcionales. |
| Validación: tipos, rechazo de campos desconocidos | ✓ Cumplido | 13 pruebas de validación; todas las mutaciones rechazadas. |
| Pruebas: cobertura creación, edición, finalización, validación | ✓ Cumplido | 54 pruebas API; 1 xfail por M1 (esperado). |

---

## Conclusión

**APTA CON OBSERVACIONES.**

La etapa 2 entrega un modelo de datos y API local funcional, con validación estricta, transacciones seguras y bloqueo correcto de emisión real. Sin embargo, incumple un requisito del encargo (modelos Usuario y Envio) sin documentación explícita de por qué se omitieron. Antes de pasar a la etapa 3, confirmar con Jorge si esa omisión es intencional y registrarla en PREGUNTAS_ABIERTAS.md.

---

**Auditoría realizada:** 25/10/2026  
**Limitaciones:** Sin PostgreSQL ni pytest en contenedor; lectura de código y compilación ejecutadas.  
**Hallazgos por severidad:** 1 crítico · 1 mayor · 2 menores
