# Prueba operativa Gmail de readyproof — 26/10/2026

Se comprobó el circuito API → PostgreSQL → emisión PDF → cola → SMTP Gmail → Enviados → recepción. Jorge confirmó: «Sí, llegó y se ve todo bien». La aplicación, sus generadores y las herramientas de fuente/ permanecieron sin cambios. No se inició scheduler ni worker automático, ni se utilizó Git.

La prueba fue local y exclusivamente ficticia. A pedido de Jorge se usaron cliente `[Ejemplo] readyproof` y usuario `tecnico-readyproof`, con nombre visible `[Ejemplo] Técnico readyproof`. El login vigente admite letras sin tildes, números, puntos, guiones y guiones bajos; no admite direcciones de correo. No se modificó esa validación.

## Alcance y pendientes

Las peticiones se ejecutaron con el cliente HTTP de Flask, contra la aplicación real y PostgreSQL persistente del ejemplo local, sin sustituir autenticación, permisos, generación PDF ni SMTP. Esto verifica las rutas y la persistencia; no equivale a un recorrido manual por el formulario en pantalla.

El control del navegador no pudo iniciar por `windows sandbox failed: helper_unknown_error: setup refresh had errors`. Las dos firmas son trazos PNG ficticios enviados por API y conservados en FirmaCarga, visibles en el PDF. **La firma operativa en canvas para esta misma carga queda pendiente.** Los tests de navegador constituyen una comprobación separada. La aprobación de este correo no cierra los pendientes anteriores de la aplicación ni habilita datos de clientes reales.

## Evidencia de esta ejecución

| Dato | Resultado |
|---|---|
| Cliente | `[Ejemplo] readyproof` — `bcf23cf1-7646-4536-9227-e9410abef52e` |
| Técnico | `tecnico-readyproof` — `96824d3d-617f-4040-b9ff-f2d8932ac441` |
| Carga | `0ca07d1f-278b-49ba-bf74-0dad8ab1bf2d`, estado `emitida` |
| Plantilla | `SG-PEM-IFI-SAA-1`, versión `00-26` |
| Envío | `20275994-e1d7-4fa8-879e-40266b1f876e`, estado `enviado` |
| Intento | Número `1`, resultado `ok` |
| Remitente | `readyproof.ar@gmail.com` |
| Destinatario de prueba autorizado | `jorgesanchezing@gmail.com` |
| Asunto | `[Ejemplo] SAA-1 de readyproof` |
| Message-ID | `<20275994-e1d7-4fa8-879e-40266b1f876e@gmail.com>` |
| Adjunto | `readyproof-planilla.pdf`, `application/pdf`, 209.888 bytes, 2 páginas |
| SHA256 PDF | `ac65d9dee873700b8632c8e88531fce64331c0cefc7cfbff2cffcb3ae3bef63f` |
| Aceptación SMTP | 26/10/2026, 19:33:48, Argentina |
| Conservación mínima registrada | Hasta 26/10/2029 desde la emisión |
| Recepción y formato | SÍ, confirmados por Jorge |

Archivos de evidencia local, excluidos de Git por estar bajo `out/flujo_completo_gmail/`: `resultado.json`, `gmail_mcp.json`, `datos_ficticios.json`, `SAA-1_emitida.pdf`, `vista_previa.pdf`, `pagina_1.png`, `pagina_2.png`, `integridad_inicial.json`, salidas de pytest y compileall. El EML inmutable se guarda además en `out/correo_prueba/20275994-e1d7-4fa8-879e-40266b1f876e.eml` y en la base, junto con la copia PDF y las huellas.

## Pasos ejecutados y comandos

Desde `C:\Users\jorge\Readyproof`, se utilizó la base PostgreSQL local ya activa indicada en `out/etapa3/demo_local/servidor.json`. El procedimiento comprueba su ruta antes de conectarse. No toca otras bases ni configura infraestructura.

```powershell
.venv\Scripts\python.exe out/flujo_completo_gmail/operacion.py preparar
```

Este comando **ya se ejecutó y no debe repetirse para consultar resultados**. Crea o reutiliza el cliente ficticio y su sistema SAA mediante los modelos existentes. Da de alta el técnico con `hash_clave(secrets.token_urlsafe(32))` y le asigna únicamente ese cliente mediante UsuarioCliente. La clave se genera y usa en memoria; no se imprime ni guarda. Si el usuario ya existe, se detiene sin reemplazar su clave. Para una posterior prueba manual, un administrador debe asignarle otra clave mediante el flujo existente de restablecimiento.

Secuencia exacta posterior al alta:

1. `GET /api/auth/sesion`; obtiene CSRF.
2. `POST /api/auth/login`; autentica al técnico y renueva CSRF.
3. `GET /api/clientes` y `GET /api/clientes/{id}/sistemas`; verifica acceso asignado.
4. `GET /api/planillas/{id}`; toma campos, orden y opciones de la definición vigente.
5. `POST /api/cargas`, con datos ficticios e `Idempotency-Key` único; HTTP 201.
6. `PUT /api/cargas/{id}/borrador`, con revisión y dos firmas PNG ficticias; HTTP 200.
7. `POST /api/cargas/{id}/vista-previa`; HTTP 200, PDF guardado para revisión.
8. `POST /api/cargas/{id}/finalizar`; HTTP 200, estado **finalizada**.
9. `POST /api/cargas/{id}/emitir`; HTTP 201, estado **emitida**. Finalizar y emitir son operaciones distintas.
10. `GET /api/cargas/{id}/pdf`; HTTP 200. Verifica huella, 2 páginas, leyenda IRAM en ambas, T.C. 3 AÑOS, marcas de agua y firmas. Renderiza y revisa ambas páginas.
11. `POST /api/cargas/{id}/enviar`; HTTP 202, Envio **pendiente** y copia PDF/EML archivada.
12. `POST /api/auth/logout`; HTTP 200.

URL del envío en el servidor local:

```text
http://127.0.0.1:8765/api/cargas/0ca07d1f-278b-49ba-bf74-0dad8ab1bf2d/enviar
```

Contrato de la solicitud, con sesión autenticada y cabecera `X-CSRF-Token` vigente:

```json
{
  "destinatario": "jorgesanchezing@gmail.com",
  "asunto": "[Ejemplo] SAA-1 de readyproof",
  "cuerpo": "[Ejemplo] Se adjunta SAA-1 de readyproof con datos y firmas ficticios. Prueba operativa autorizada; no corresponde a un servicio real."
}
```

**No repetir este POST para consultar o reintentar:** cada solicitud crea otro Envio. En esta implementación el POST encola y deja **cero Intentos**; el Intento número 1 se crea al procesar SMTP. No se inventó un intento previo para ajustar la evidencia al pedido.

Tras revisar el PDF se ejecutó una única pasada:

```powershell
.venv\Scripts\python.exe out/flujo_completo_gmail/operacion.py enviar
```

El procedimiento verifica que el único envío procesable sea el autorizado y reserva evidencia antes de transmitir para impedir repeticiones accidentales. Ejecuta `reintentar_envios()` dentro de `app.app_context()`, con `MAIL_MODO_PRUEBA=False` únicamente en esa instancia del proceso. `.env.local` y el servidor local conservan su configuración de prueba. Si hay otro mensaje procesable se detiene. No inicia el worker ni crea endpoints nuevos.

El comando general existente para una pasada es `python -m flask --app app correo-reintentar`; requiere contexto y configuración de base correctos y procesa la cola global. No usarlo a ciegas para repetir esta prueba. La expresión `from app.correo import reintentar_envios; reintentar_envios()` sin contexto Flask no basta.

Resultado comprobado: un intento SMTP, estado `enviado`, `enviado_en` completo, Intento 1 `ok`, ningún reintento programado y registros de auditoría de emisión, encolado e intento. No se reenvió la muestra del diagnóstico anterior.

## Verificar Gmail y destino

El MCP confirmó la cuenta remitente y buscó:

```text
in:sent rfc822msgid:20275994-e1d7-4fa8-879e-40266b1f876e@gmail.com
```

Encontró un mensaje con etiqueta SENT y el PDF de 209.888 bytes. La lectura de metadatos confirmó el Message-ID, remitente, destinatario y asunto exactos. [Abrir el mensaje en la cuenta remitente](https://mail.google.com/mail/u/?authuser=readyproof.ar%40gmail.com#all/1a17a592875072cd).

Jorge abrió su casilla destinataria y confirmó recepción y revisión correcta de las dos páginas, leyenda, logo, marcas de agua y firmas ficticias. SPF/DKIM en los encabezados del mensaje recibido no se revisaron en esta ejecución y no se dan por confirmados por la sola recepción.

## Controles de cierre

`python -m compileall app`: código 0. Comparación SHA256 de app/ y fuente/ contra el inicio, sin cambios. `.env.local` excluido por `.gitignore`; búsqueda de valores de credenciales locales en código, pruebas y documentación sin imprimir secretos. Resultado de la suite final y pendientes detallados en REGISTRO_DE_CAMBIOS.md.

La primera suite informó 139 passed y 2 failed por no resolver Playwright; el problema era de configuración del entorno. La ruta histórica `.venv/browser/node_modules` no existe en esta máquina. Playwright 1.62.1 está disponible en el runtime local; para ejecutar los tests aquí:

```powershell
$env:NODE_PATH = 'C:/Users/jorge/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules'
$env:TEMP = (Resolve-Path .venv/tmp).Path
$env:TMP = $env:TEMP
.venv\Scripts\python.exe -m pytest -q --tb=short
.venv\Scripts\python.exe -m compileall app
```

No se instalaron paquetes, no se cambiaron claves, no se publicaron servicios y no se consideran cerrados los informes -IN ni las demás etapas del encargo por esta prueba de correo.

Resultado final con el entorno local corregido: **141 passed in 462.07s (0:07:42)**, código 0.
