# Configuración del modo real y piloto

La aplicación arranca en piloto si `MODO_PILOTO` no está definido. La etapa 6 se entregó en piloto. La activación posterior autorizada se registra en [TRANSICION_EXITOSA.md](TRANSICION_EXITOSA.md).

| Variable | Valor por defecto | Efecto |
|---|---|---|
| MODO_PILOTO | true | Solo clientes/datos de ejemplo; nuevos PDF rotulados PILOTO |
| EMPRESA_MANTENEDORA | [Ejemplo] readyproof | Marcador ficticio, rechazado para emitir en modo real |
| CERTIFICADO_N | IFI-2024-00000 | Marcador ficticio, rechazado para emitir en modo real |
| MAIL_MODO_PRUEBA | Valor de MODO_PILOTO si no está definida | Guarda copia sin SMTP por defecto; puede configurarse expresamente |
| DESTINATARIO_PRUEBA | Vacío | Si se define, sustituye el destinatario del PDF en piloto |
| PLANILLAS_DESTINATARIOS_PRUEBA | Vacío | Lista de direcciones autorizadas para transmisiones explícitas del piloto |

No existe una casilla de prueba predeterminada a la que se envíen mensajes reales automáticamente. Las pruebas usan archivos o transportes simulados. La dirección `prueba@test.com` se usa únicamente en una prueba sin conexión SMTP; no debe copiarse como configuración operativa.

## Piloto

Conservar `MODO_PILOTO=true`. Por defecto el correo queda en prueba. El transporte Gmail explícito ya existente permite la prueba operativa únicamente con destinatarios autorizados; no abre el envío a direcciones arbitrarias. Un cambio de lista vuelve a comprobarse en los reintentos. El correo de documentación conserva su control independiente `DOCUMENTACION_MODO_PRUEBA`.

Los nuevos PDF incluyen «Modo PILOTO» al pie y metadata `/ReadyproofModo=PILOTO`; mantienen IRAM, firmas, logos, páginas del kit, número y revisión. No se agrega la marca a PDF anteriores ni se regeneran para cambiarles el modo.

## Modo real

La configuración futura requiere `MODO_PILOTO=false`, `EMPRESA_MANTENEDORA` y `CERTIFICADO_N` confirmados. Para transmitir correos reales, además debe estar confirmado `MAIL_MODO_PRUEBA=false` y el transporte configurado. Se admite correo de prueba durante una revisión controlada del modo real: no se transmite.

La emisión y vista previa rechazan empresa/certificado vacíos, marcadores `[Ejemplo]`/`[Pendiente]`, certificado ficticio conocido o valores incompatibles con la planilla. También verifican que la cabecera coincida con la mantenedora y certificado configurados. Esa validación detecta errores de configuración; no consulta un registro externo ni certifica la vigencia legal del número, que debe confirmar una persona responsable.

En modo real se admiten nombres y textos sin prefijo de ejemplo, clientes no ficticios y sistemas asignados; se conservan tipos, opciones, mediciones, DNI, permisos, firmas y controles de versión. Los PDF nuevos incluyen «Modo REAL», mantenedora y certificado configurados. Se preservan revisión original 0, correcciones 1+ y los PDF históricos.

El cambio no convierte clientes ficticios en reales ni elimina su historial. Los documentos del piloto siguen siendo históricos y no se emiten nuevamente como reales; deben crearse cargas del cliente correspondiente. Configurar la empresa o el modo tampoco modifica documentos ya emitidos.

## Procedimiento de activación

Completar `TRANSICION_PILOTO_A_REAL.md`, obtener las confirmaciones normativas y la autorización expresa de Jorge. Entonces una persona autorizada edita el archivo privado de entorno, reinicia la aplicación y revisa la primera emisión y su destinatario. No se versiona `.env`, no se comparten valores secretos y no se confunde un commit de código con una activación del entorno. Recargar la interfaz en línea después del cambio, conservando los borradores pendientes hasta resolverlos.
