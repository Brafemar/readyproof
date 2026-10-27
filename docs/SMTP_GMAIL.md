# Transporte SMTP Gmail de readyproof

Cuenta elegida por Jorge: `readyproof.ar@gmail.com`. Sustituye cPanel para esta implementación. Esta tarea se denomina etapa 7 en el pedido actual; los informes -IN de la etapa 7 del encargo original siguen pendientes.

### Comprobación operativa del 26/10/2026

**Prueba adicional con PDF:** Jorge autorizó enviar la muestra ficticia SAA-1 al mismo destinatario de prueba. SMTP aceptó el mensaje con un único PDF y el MCP confirmó el mensaje exacto en Enviados, con readyproof-planilla.pdf de 204711 bytes. Se utilizó la copia EML preparada con crear_mensaje y se verificaron sus huellas antes de transmitir. Evidencia: `out/diagnostico_control/resultado_envio_pdf.json`. No se inició el worker ni se alteró la base o el modo de prueba global. Sigue pendiente recepción y revisión de SPF/DKIM en destino, además del flujo completo de API/emisión/cola con una carga emitida apta.

**Actualización: autenticación y envío SMTP de texto comprobados.** Jorge generó una contraseña de aplicación válida. Se quitaron únicamente sus espacios de agrupación en .env.local; las demás variables quedaron iguales, incluido el modo de prueba. Se validó autenticación 235 con AUTH LOGIN y con smtplib.login, el método de la aplicación. Un mensaje de prueba sin adjuntos al destinatario autorizado fue aceptado por SMTP y localizado en Enviados mediante el MCP de la cuenta dedicada. Esto no confirma la recepción en la casilla destinataria ni el flujo completo de emisión/envío de PDF. No se inició el worker ni se habilitaron clientes reales. Evidencia: `out/diagnostico_control/resultado_auth_gmail.json` y `out/diagnostico_control/resultado_envio_gmail_clave_validada.json`. Los párrafos siguientes conservan antecedentes del diagnóstico; la credencial rechazada fue reemplazada por Jorge.

Diagnóstico posterior: AUTH LOGIN sin respuesta inicial permitió obtener un rechazo explícito **535 / 5.7.8**. STARTTLS, certificado emitido por Google Trust Services, EHLO y NOOP correctos. La contraseña local no coincide con el patrón habitual de 16 letras de una contraseña de aplicación, tampoco contiene espacios de agrupación. No se mostró su contenido. Se requiere que Jorge genere una contraseña de aplicación válida para la cuenta dedicada y reemplace únicamente SMTP_PASSWORD en .env.local; no compartirla por chat. No se cambió la configuración ni el transporte de la aplicación. Evidencia: `out/diagnostico_control/diagnostico_login_gmail.json`. Este resultado reemplaza la incertidumbre de los primeros intentos descritos debajo: Gmail rechazó las credenciales usadas en esta prueba.

El MCP confirmó la cuenta dedicada. La configuración local tiene una contraseña no vacía. Se realizaron dos pruebas independientes de autenticación, sin envío: conexión y STARTTLS con certificado validado correctos, pero la sesión se cortó durante la autenticación (`SMTPServerDisconnected`). No se confirmó que Gmail aceptara la clave y no hubo rechazo explícito que pruebe que sea incorrecta. No se cambió el modo de prueba ni se inició el worker. Evidencia saneada: `out/diagnostico_control/resultado_auth_gmail.json`. Las referencias posteriores a ausencia de conexión describen el estado al cerrar la implementación original.

## Contraseña de aplicación y configuración

La persona responsable activa la verificación en dos pasos de Google, abre [Contraseñas de aplicación](https://myaccount.google.com/apppasswords), crea una para readyproof y guarda la clave directamente en `.env.local` en la raíz del proyecto. No se usa la contraseña habitual de Google y no se comparte la clave por chat. Según [la ayuda oficial de Google](https://support.google.com/accounts/answer/185833?hl=es), las contraseñas de aplicación requieren verificación en dos pasos y se revocan al cambiar la contraseña de la cuenta. Algunas políticas de cuenta pueden impedir crearlas.

`.env.local` ya está excluido por `.gitignore`. Jorge mantiene ese archivo; la aplicación lo lee al arrancar. Las variables del proceso tienen prioridad; luego `.env.local` y finalmente `.env` completan valores ausentes. Reiniciar el proceso al cambiar la configuración. Los tests con `TESTING=True` no cargan esos archivos.

Configuración de referencia (la contraseña queda vacía aquí, nunca se copia a la documentación):

```ini
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=readyproof.ar@gmail.com
SMTP_PASSWORD=
MAIL_FROM=readyproof.ar@gmail.com
MAIL_MODO_PRUEBA=true
```

Según la [documentación SMTP de Google](https://developers.google.com/workspace/gmail/imap/imap-smtp), smtp.gmail.com admite TLS en 587. El transporte exige STARTTLS en 587, verificación del certificado y autenticación después de TLS; no admite degradación a texto plano. `SMTP_FROM` se mantiene como alternativa compatible si falta `MAIL_FROM`. No se agregan dependencias.

## Preparar la base

Desde la raíz, con las variables de PostgreSQL local configuradas:

```powershell
.venv\Scripts\python.exe -m flask --app app init-db
```

La migración aditiva `007_smtp_gmail` conserva los registros anteriores y agrega actor, asunto, cuerpo, copia PDF, mensaje EML, huellas, fecha mínima de conservación y reserva de intentos. Los envíos anteriores sin actor/copia no se transmiten automáticamente. La reversión se bloquea si existen envíos, para proteger sus copias.

## API

`POST /api/cargas/<uuid>/enviar`, con sesión autenticada y `X-CSRF-Token`, requiere acceso al cliente y una carga `emitida`, con PDF íntegro y leyenda aprobada en todas las páginas. Siguen habilitados solamente clientes y datos ficticios.

```json
{
  "destinatario": "cliente@example.invalid",
  "asunto": "[Ejemplo] Planilla readyproof",
  "cuerpo": "[Ejemplo] Se adjunta la planilla PDF emitida."
}
```

Solo `destinatario` es obligatorio; se admiten asunto y cuerpo personalizados. Se rechazan campos desconocidos, destinatarios múltiples y saltos de línea en encabezados. Respuesta HTTP 202: `id`, `carga_id`, `estado: pendiente`, `modo_prueba`. La solicitud prepara y archiva el mensaje mediante `send_email(..., encolar=True)`; no espera a Gmail. Cada nueva solicitud crea un envío independiente: no repetir el POST para consultar el estado ni para reintentar.

El PDF adjunto es una copia inmutable del emitido, sin enlaces de descarga. El EML y sus huellas se guardan en la base; se deja también `out/correo_prueba/<id>.eml`, fuera de Git. La copia contiene datos personales y firmas: requiere acceso restringido de Windows y respaldo igual que la base. `retener_hasta` representa al menos tres años desde la emisión; no hay purga automática. No reemplaza la política de copias de seguridad ni impide por sí sola un borrado administrativo directo de la base.

## Procesar y reintentar

Ejecutar en una terminal independiente:

```powershell
.venv\Scripts\python.exe -m flask --app app correo-worker
```

Procesa inmediatamente y vuelve a revisar cada 900 segundos; detener con Ctrl+C. No se inicia al importar Flask ni desde el recargador. No se instaló un servicio de Windows ni se dejó este proceso ejecutándose durante el desarrollo. Para una pasada manual:

```powershell
.venv\Scripts\python.exe -m flask --app app correo-reintentar
```

Con `MAIL_MODO_PRUEBA=true` (valor por defecto), se genera el EML y un Intento `ok` que indica explícitamente que no hubo SMTP; el Envio conserva `pendiente`, `enviado_en` vacío y queda sin reintentos. Cambiar de modo no transmite esas copias ya procesadas. El lanzador `scripts/iniciar_ejemplo.py` fuerza este modo seguro.

Para una prueba real posterior, Jorge debe elegir una casilla de prueba, configurar `MAIL_MODO_PRUEBA=false` en el proceso correspondiente y generar una nueva solicitud. Durante esta implementación no se conectó Gmail ni se enviaron mensajes reales. La cuenta/contraseña cargada por Jorge todavía no se validó contra el proveedor.

Máximo tres intentos totales, primero más dos reintentos; los fallos temporales antes de transmitir y los rechazos explícitos 4xx se programan para 15 minutos después. Se revisan nuevamente usuario activo y acceso al cliente. La reserva se confirma en PostgreSQL antes del contacto SMTP para evitar duplicación entre procesos. Una reserva interrumpida se bloquea para revisión al superar 15 minutos. Los fallos permanentes, autenticación inválida y cortes durante DATA sin respuesta concluyente no se reenvían automáticamente. Los reintentos conservan el mismo Message-ID y adjunto. Las respuestas guardadas son categorías/códigos saneados; no se registran credenciales ni respuestas crudas.

`enviado` indica aceptación SMTP, no entrega en la bandeja del destinatario. Un bounce posterior exige revisar el aviso en Gmail: no se conectó IMAP ni se automatizó lectura de la cuenta. Un administrador activo puede registrar el aviso revisado mediante:

```powershell
.venv\Scripts\python.exe -m flask --app app correo-bounce --envio UUID_DEL_ENVIO --actor UUID_DEL_ADMIN
```

La herramienta local cambia el último Intento a `bounce`, conserva la fecha de aceptación, registra al administrador y bloquea reintentos. No genera otro intento de transmisión.

## Verificación sin correo real

```powershell
.venv\Scripts\python.exe -m pytest tests/test_smtp_gmail.py -q
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m compileall app
```

SMTP está sustituido en los tests. Se verifican credenciales desde variables temporales, TLS validado, intentos, adjunto exacto, modo archivo, reintentos, permisos revocados, errores, reserva interrumpida y registro manual de bounce. Las credenciales de prueba se generan en memoria y no proceden de `.env.local`.
