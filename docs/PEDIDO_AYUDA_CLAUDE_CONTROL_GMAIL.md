# Pedido de ayuda a Claude: control del navegador bloqueado al configurar Gmail

Fecha del informe: 26 de octubre de 2026. Zona horaria de Jorge: Argentina, UTC−03:00.

## Estado actual al continuar después del envío correcto

| Componente | Resultado comprobado |
|---|---|
| Cuenta del MCP | readyproof.ar@gmail.com, confirmada por consulta de perfil |
| Autenticación SMTP | Correcta, código 235, incluido smtplib.login usado por readyproof |
| Seguridad de conexión | STARTTLS con validación de certificado; emisor Google Trust Services |
| Correo de prueba de texto | Aceptado por SMTP y encontrado en Enviados por Message-ID |
| Correo con PDF de muestra | Aceptado por SMTP; Enviados confirma un PDF de 204711 bytes |
| Recepción en la casilla destinataria | Pendiente de confirmación; Enviados no demuestra recepción |
| Correo con PDF desde la aplicación | Pendiente de prueba operativa |
| Navegador y consola del chat dentro del sandbox | Última comprobación fallida; no hay evidencia posterior de recuperación |
| Modo de prueba y worker | Modo de prueba conservado; worker no iniciado por estas pruebas |

**El pedido de ayuda vigente a Claude se concentra en el sandbox/control del navegador.** La conexión MCP y la autenticación SMTP ya funcionan por vías independientes; no corresponde diagnosticar nuevamente la clave anterior como si siguiera vigente. La sección 14 conserva los pasos que resolvieron el acceso Gmail. Las secciones 1 a 13 describen el incidente inicial y sus pruebas históricas; sus referencias a falta de conexión SMTP corresponden a ese momento.

Próximo paso autorizado por Jorge al pedir continuar: preparar y validar la prueba de correo con una planilla ficticia en PDF, manteniendo los límites de ejemplo, los registros y la configuración global de prueba. No se considera resuelta la recepción ni el flujo completo antes de verificarlos.

## 1. Pedido concreto

Necesito ayuda para recuperar el control del navegador de Codex en Windows. El acceso a Gmail ya se recuperó por MCP y SMTP, según el estado actual indicado arriba. No quiero seguir repitiendo reinicios o movimientos de chats sin una prueba que identifique qué cambia.

El bloqueo ocurre antes de enumerar ventanas o interactuar con Chrome. También falla la consola normal dentro del sandbox. Las lecturas mediante comandos expresamente autorizados fuera del sandbox sí funcionan.

Por favor, revisá la evidencia, diferenciá hechos de hipótesis y proponé una reparación verificable que mantenga el aislamiento y las protecciones del proyecto. No des por resuelto el problema hasta que funcionen tanto un comando dentro del sandbox del chat como el control del navegador.

## 2. Objetivo original y estado inicial de Gmail (antecedente histórico)

- Proyecto: readyproof, aplicación local en desarrollo para readyproof.
- Jorge pidió configurar la cuenta dedicada `readyproof.ar@gmail.com`, operando Chrome con el cursor.
- Jorge informó que la cuenta ya estaba abierta en Chrome. Codex no pudo comprobar visualmente esa sesión.
- El transporte SMTP ya estaba implementado: servidor `smtp.gmail.com`, STARTTLS en puerto 587, migración 007, endpoint `POST /api/cargas/<id>/enviar` y worker separado, con máximo tres intentos.
- Según el registro anterior, se creó `.env.local` en la carpeta actual con la configuración pública, `SMTP_PASSWORD` vacío y `MAIL_MODO_PRUEBA=true`. Jorge debía completar la contraseña de aplicación directamente en su equipo. No se verificó después si lo hizo y no se debe sobrescribir ese archivo.
- El ejemplo local en `127.0.0.1:8765` fuerza modo de prueba. Según los registros, no se dejó iniciado el worker de correo.
- No hubo autenticación SMTP, conexión de prueba a Gmail ni envío real durante esta operación.
- No se cambió ninguna configuración de la cuenta Google mediante las herramientas.

En esa fase, la evidencia se refería al entorno de ejecución/control de Codex y todavía no se había probado SMTP. Posteriormente se identificó y corrigió por separado una credencial SMTP inválida, como se detalla en la sección 14.

## 3. Las dos carpetas y los proyectos de Codex

Esta parte es central: se pasó de una ubicación anterior del proyecto a otra carpeta local, pero la anterior siguió presente en los permisos del chat.

| Concepto | Ubicación o nombre |
|---|---|
| Carpeta anterior | `C:\Users\jorge\Documents\ChatGPT\Readyproof` |
| Carpeta actual, donde están el código operativo y `.venv` | `C:\Users\jorge\Readyproof` |
| Proyecto anterior en la barra lateral | `Readyproof` |
| Proyecto creado para la carpeta actual | `Readyproof Actual` |
| Chat anterior, mencionado en los registros | `Copiar contenido de fuente v5` |
| Chat de esta reanudación | `Continuar configuración de Gmail` |

Los registros previos consignan que Jorge creó el proyecto **Readyproof Actual**, confió la carpeta actual y movió el chat anterior allí. No se dispone aquí del comando ni del procedimiento exacto con el que se creó o copió la carpeta física actual. No debe suponerse que se borró o movió la anterior: **ambas carpetas existen**.

Comprobaciones directas en este chat:

1. `Get-Location`, ejecutado fuera del sandbox con autorización, devolvió `C:\Users\jorge\Readyproof`.
2. Las dos carpetas son directorios y no enlaces: `LinkType` y `Target` devolvieron `null`.
3. La herramienta `list_projects` devolvió los dos proyectos locales, cada uno con su ruta correspondiente; ambos se identificaron como repositorios Git.
4. `list_threads` mostró inicialmente el chat **Continuar configuración de Gmail** con `cwd` en la carpeta actual, pero `projectId: null`.
5. Codex corrigió esa asociación mediante `move_thread_to_project`. La herramienta confirmó que el chat quedó en **Readyproof Actual**.
6. Después de esa corrección, la consola aislada y el navegador siguieron fallando.

El contexto de permisos de este chat incluye como raíces de escritura tanto la carpeta actual como la anterior, además de una carpeta de visualizaciones de la conversación. Estar trabajando en la carpeta actual o estar asociado al proyecto actual **no eliminó la raíz anterior del perfil observado**.

No se comprobó si esa raíz adicional proviene de estado persistente del chat, de la aplicación, de permisos heredados de otra operación o de otra configuración. La asociación de proyecto y el perfil efectivo de permisos no deben tratarse como si fueran necesariamente el mismo mecanismo.

## 4. Entorno comprobado

| Elemento | Resultado |
|---|---|
| Aplicación | Codex de escritorio en Windows |
| Shell | PowerShell |
| Codex CLI incluido | `codex-cli 0.164.0-alpha.11.1` |
| Ejecutable encontrado | `C:\Users\jorge\AppData\Local\OpenAI\Codex\bin\2993767bd1dfb009\codex.exe` |
| Configuración seleccionada | `[windows]` / `sandbox = "elevated"` |
| Windows: `CurrentBuild` | `26100` |
| Windows: `UBR` | `6725` |
| Windows: `DisplayVersion` | `24H2` |
| Windows: `ProductName` del registro | `Windows 10 Home Single Language` |
| Prueba de MXC | No disponible en este ejecutor |

Se transcribe `ProductName` tal como lo devolvió el registro. Hay una discrepancia aparente entre esa etiqueta y el número de build; no se resolvió ni se reinterpretó como un dato confirmado sobre la edición comercial de Windows.

## 5. Cronología de la operación y de los intentos de reparación

### A. Antecedentes, documentados en el registro del proyecto

1. Se implementó y probó el transporte Gmail sin SMTP real. Última suite registrada: **141 passed in 319.28s**, `compileall` con código 0 y `pip check` sin dependencias rotas. Esos resultados son anteriores a este diagnóstico; no se volvieron a ejecutar para comprobar el navegador.
2. Se preparó `.env.local` para que Jorge completara la contraseña de aplicación localmente.
3. Jorge pidió abrir Gmail y operar con el cursor. El control falló al preparar sus recursos: `failed to write kernel assets` y error de ruta de Windows `os error 3`.
4. Según el registro, se solicitó a Windows abrir Gmail en el navegador predeterminado. No se pudo verificar visualmente la apertura ni la cuenta activa.
5. Se comprobaron las dos rutas de Readyproof y se detectaron errores del sandbox relacionados con permisos sobre la carpeta anterior y su `.git`.
6. Jorge creó el proyecto **Readyproof Actual**, confió la carpeta actual y movió el chat anterior. El `cwd` pasó a la carpeta actual, pero siguió apareciendo la raíz anterior en el perfil.
7. Se propuso abrir una conversación nueva dentro del proyecto actual, sin copiar ni bifurcar la anterior. Se creó `docs/RETOMAR_GMAIL.md` para conservar el contexto. Los registros no permiten afirmar cómo se creó técnicamente el chat posterior ni qué permisos heredó.

### B. Reanudación en el chat Continuar configuración de Gmail

1. Jorge pidió leer `docs/RETOMAR_GMAIL.md`, continuar Gmail y comprobar primero el navegador.
2. La primera lectura mediante consola normal falló antes de iniciar el proceso.
3. `cua.getState()` falló. El reintento también falló, con salida del kernel y error de preparación del sandbox.
4. Se leyeron las instrucciones mediante consola autorizada fuera del sandbox.
5. Se intentó el control alternativo de Windows con `node_repl` y `@oai/sky`. El kernel tampoco pudo iniciar; no llegó a enumerar aplicaciones.
6. Se dejó constancia de que no hubo clics ni cambios en Gmail.

### C. Jorge pidió resolver el bloqueo

1. Se consultó la documentación oficial de OpenAI sobre Windows sandbox.
2. Se leyeron `setup_error.json`, las entradas pertinentes de configuración, las ACL y los últimos registros del sandbox.
3. Se comprobó la versión de Codex y los datos de Windows.
4. Se probó MXC con un único comando y sin guardar cambios de configuración. Falló por falta de disponibilidad del ejecutor.
5. Se probó el sandbox elevado desde la carpeta actual con el perfil `:workspace` y requisitos administrados. **Esta prueba sí funcionó**: imprimió `LEGACY_OK`, código 0.
6. Se repitió `Get-Location` con la herramienta normal del chat. **Siguió fallando**.
7. Se reinició el kernel de control del navegador y se volvió a llamar `cua.getState()`. **Siguió fallando**.
8. Se consultaron proyectos y chats. Se encontró que el chat actual no tenía proyecto asignado.
9. Se asoció el chat a **Readyproof Actual** usando la herramienta oficial de la aplicación. La operación devolvió confirmación.
10. Se volvieron a comprobar consola normal y navegador después de la asociación. **Ambos siguieron fallando**.
11. Se pidió cerrar Codex por completo y volver a abrir el chat en Readyproof Actual para comprobar si se reconstruía el perfil. Se aclaró que el resultado no estaba garantizado.

### D. Última comprobación

Jorge respondió «comprobá» después de la indicación de reinicio. No hay una observación técnica que permita certificar qué procesos de Codex se cerraron o reiniciaron; lo comprobado es el resultado de los intentos siguientes:

- `Get-Location` mediante la consola aislada: falla antes de iniciar el proceso.
- `cua.getState()`: falla antes de enumerar ventanas.
- Lectura autorizada fuera del sandbox: funciona y confirma el `cwd` actual.
- Últimas líneas disponibles del log: siguen mostrando errores de preparación sobre la carpeta anterior y su `.git`.

Por lo tanto, **ni el cambio de asociación ni la comprobación posterior al reinicio propuesto demostraron recuperación**.

## 6. Errores exactos observados

### Error inicial, tomado de los registros previos

```text
failed to write kernel assets: El sistema no puede encontrar la ruta especificada. (os error 3)
```

El diagnóstico previo también consignó `failure_kind=kernel_assets` y `sandbox_configured=true`.

### Consola normal del chat

```text
exec_command failed: CreateProcess { message: "Rejected(\"Failed to create unified exec process: helper_unknown_error: setup refresh had errors\")" }
```

### Control del navegador

```text
node_repl kernel exited unexpectedly

windows sandbox failed: helper_unknown_error: setup refresh had errors
```

Una de las primeras respuestas también fue:

```text
trusted Node process exited unexpectedly; kernel reset, rerun your request
```

### Archivo de error de preparación

Archivo: `C:\Users\jorge\.codex\.sandbox\setup_error.json`

```json
{
  "code": "helper_unknown_error",
  "message": "setup refresh had errors"
}
```

### Registro concreto del sandbox

Archivo existente leído: `C:\Users\jorge\.codex\.sandbox\sandbox.2026-10-26.log`.

Se intentó inicialmente leer `sandbox.log`, pero ese nombre sin fecha no existía en esa ubicación. Después se localizó y leyó el archivo fechado. No confundir el fallo de esa primera lectura con el error principal del sandbox.

Extracto de las últimas líneas disponibles, a las **20:46:04 UTC / 17:46:04 de Argentina**:

```text
granting write ACE to C:\Users\jorge\Documents\ChatGPT\Readyproof for sandbox group and capability SID
write ACE grant failed on C:\Users\jorge\Documents\ChatGPT\Readyproof: SetSecurityInfo failed: 5
deny ACE failed on C:\Users\jorge\Documents\ChatGPT\Readyproof\.git: SetSecurityInfo failed for C:\Users\jorge\Documents\ChatGPT\Readyproof\.git: 5
setup refresh completed with errors
setup error: setup refresh had errors
setup refresh: exited with status ExitStatus(ExitStatus(1))
```

En otras entradas del mismo archivo también apareció:

```text
failed to grant non-inheriting read-attributes ACE on user profile C:\Users\jorge:
open ACL target for root-only update (MAXIMUM_ALLOWED):
El proceso no tiene acceso al archivo porque está siendo utilizado por otro proceso. (os error 32);
continuing setup
```

Ese error 32 sobre el perfil aparece como advertencia seguida de `continuing setup`. No se demostró que fuera la causa fatal. Los errores de la lista final de preparación se refieren a la carpeta anterior y su `.git`, con error 5.

## 7. Pruebas reproducibles ya realizadas y resultados

Los siguientes comandos son evidencia de lo ejecutado; no son una autorización para cambiar configuraciones ni para repetir acciones sensibles sin revisión.

### Prueba que falla en las herramientas del chat

```powershell
Get-Location
```

Resultado con `exec_command` normal: no se crea el proceso, `helper_unknown_error: setup refresh had errors`.

La misma lectura con ejecución expresamente autorizada fuera del sandbox devuelve:

```text
C:\Users\jorge\Readyproof
```

### Prueba de MXC sin cambios persistentes

Desde `C:\Users\jorge\Readyproof`:

```powershell
codex -c windows.sandbox=mxc sandbox --include-managed-config --permission-profile :workspace -- cmd.exe /d /c echo MXC_OK
```

Resultado, código 1:

```text
Error: failed to prepare MXC sandbox: native MXC is unavailable on this executor
```

No se guardó `windows.sandbox=mxc`. No se cambió a `unelevated`.

### Prueba que sí funciona con el sandbox elevado existente

Desde `C:\Users\jorge\Readyproof`:

```powershell
codex sandbox --include-managed-config --permission-profile :workspace -- cmd.exe /d /c echo LEGACY_OK
```

Resultado, código 0:

```text
LEGACY_OK
```

Esta ejecución independiente empleó el perfil resuelto por ese comando. No se exportó ni comparó su estado completo con el del chat. El éxito no demuestra que las herramientas del chat estén reparadas ni que los dos perfiles sean idénticos.

### Control del navegador

```javascript
await cua.getState();
```

Falla antes de devolver inventario o estado de ventanas. Se reinició su kernel con `js_reset` y se repitió; no se recuperó.

### Control de Windows alternativo

Se intentó inicializar `@oai/sky` desde `node_repl` y enumerar aplicaciones:

```javascript
if (!globalThis.sky) {
  const { sky } = await import("@oai/sky");
  globalThis.sky = sky;
}
nodeRepl.write(JSON.stringify(await sky.list_apps(), null, 2));
```

El kernel no pudo iniciar por el mismo error del sandbox. No hay evidencia de que se completara el import ni de que `list_apps` llegara a ejecutarse.

## 8. ACL leídas, sin reparación manual

Para la carpeta anterior y su `.git`, `Get-Acl` devolvió:

```text
Owner: DESKTOP-6LSDVNO\jorge
AreAccessRulesProtected: False

DESKTOP-6LSDVNO\CodexSandboxUsers  Allow  ReadAndExecute, Synchronize
NT AUTHORITY\SYSTEM              Allow  FullControl
BUILTIN\Administradores          Allow  FullControl
DESKTOP-6LSDVNO\jorge             Allow  FullControl
```

Esta es una salida resumida de `Get-Acl`, no un análisis completo del token ni de todos los mecanismos de seguridad. No explica por sí sola por qué el helper recibe acceso denegado al intentar escribir las ACE. No se comprobaron exhaustivamente políticas de protección de carpetas, identidad efectiva del helper ni descriptores de seguridad completos.

No se usaron `takeown`, reseteos recursivos de permisos ni cambios manuales de ACL. Las ejecuciones normales del preparador del sandbox sí intentaron aplicar sus propias ACE, según el log; por eso no corresponde afirmar que ningún permiso del equipo pudo haber sido tocado automáticamente por Codex.

## 9. Cambios realizados y límites respetados

### Cambios documentados

- Preparación previa de `.env.local`, según el registro, sin contraseña incorporada en ese momento.
- Creación previa del proyecto **Readyproof Actual** por Jorge y trabajo en la nueva ubicación.
- Asociación del chat actual a **Readyproof Actual** mediante la herramienta oficial.
- Creación y actualización de documentación diagnóstica y del registro de cambios.

### Acciones que no se realizaron durante el diagnóstico actual

- No se leyó `.env.local` ni se copiaron contraseñas o códigos.
- No se operó Chrome, Gmail ni la cuenta Google mediante clics.
- No se enviaron correos, no se hizo autenticación SMTP y no se inició el worker.
- No se desactivó el sandbox ni se guardó otro modo de aislamiento.
- No se modificaron manualmente ACL, propiedad, firewall ni bases internas de Codex.
- No se borraron las carpetas vieja o nueva ni sus `.git`.
- No se ejecutaron comandos Git ni se modificaron `AGENTS.md`, `fuente/` o el código de aplicación.
- No se instalaron dependencias ni se desplegó o publicó el sistema.
- No se volvió a ejecutar la suite de la aplicación para esta comprobación del entorno.

## 10. Interpretación y cuestiones todavía abiertas

### Hechos establecidos

1. Hay dos ubicaciones existentes y dos proyectos registrados.
2. El chat trabaja en la carpeta actual y quedó asociado a Readyproof Actual.
3. Su perfil observado todavía incluye la carpeta anterior.
4. La preparación de ese perfil falla con error 5 sobre la carpeta anterior y su `.git`.
5. Un comando aislado con el sandbox elevado y perfil `:workspace`, desde la carpeta actual, sí puede ejecutarse.
6. Los controles del chat siguen sin arrancar.

### Hipótesis que necesitan validación

- Una raíz adicional retenida en el estado del chat o de la aplicación podría explicar la diferencia entre la prueba CLI exitosa y las herramientas fallidas.
- Puede existir un problema específico de permisos o de identidad efectiva del helper sobre la ubicación anterior.
- Puede tratarse de un defecto del mecanismo de actualización de permisos de esta versión de Codex.

Ninguna de esas hipótesis fue demostrada como causa única. No hay base para concluir que borrar una carpeta, resetear permisos o cambiar el modo del sandbox resolverá el problema.

### Lo que pido investigar

1. ¿Cómo inspeccionar y comparar, por una vía compatible, los perfiles efectivos del comando CLI exitoso y del chat fallido?
2. ¿De dónde proviene la raíz adicional anterior y cómo retirarla del chat sin editar la base interna ni ampliar accesos?
3. ¿Por qué el helper devuelve `SetSecurityInfo failed: 5` en esa carpeta si la lectura resumida de ACL muestra a Jorge como propietario con control total?
4. ¿Hace falta reparar la preparación del sandbox con un procedimiento oficial? ¿Qué cambia exactamente y cómo se revierte?
5. ¿Hay una corrección aplicable a `0.164.0-alpha.11.1`? No se comprobó la disponibilidad de actualizaciones ni se instaló otra versión.

## 11. Condiciones para cualquier reparación

- Mantener el aislamiento; no usar acceso irrestricto como solución.
- No borrar ni alterar las carpetas del proyecto, `.git`, la fuente normativa o los registros existentes.
- No cambiar ACL para eludir el fallo. Si se propone una reparación legítima de permisos, explicar evidencia, alcance exacto, riesgos y reversión, y obtener aprobación de Jorge antes de aplicarla.
- No leer ni pedir contraseñas, códigos de dos pasos o tokens por chat.
- Las credenciales las introduce Jorge directamente en su equipo.
- No automatizar cambios sensibles en Google ni enviar correos reales sin autorización específica.
- No confundir una lectura autorizada fuera del sandbox con recuperación de las herramientas aisladas.
- No repetir como solución ya comprobada el movimiento de proyecto o el reinicio: se intentaron y no demostraron recuperación.

## 12. Criterio de resolución

El bloqueo se considera resuelto solamente cuando:

1. `Get-Location` funciona mediante la herramienta normal dentro del sandbox de este chat, sin escalación.
2. `cua.getState()` o el control de Windows devuelve un inventario real y actualizado de ventanas.
3. Se puede inspeccionar Chrome y verificar la cuenta objetivo sin leer secretos.
4. Se registra qué cambio produjo la recuperación y qué permisos quedaron activos.

La configuración Gmail es un paso posterior. Recuperar el navegador no implica que SMTP esté autenticado ni que un correo haya sido entregado.

## 13. Fuentes del informe

Este documento reúne los resultados de las herramientas de este chat y los antecedentes consignados en:

- `docs/RETOMAR_GMAIL.md`
- `out/diagnostico_control/DIAGNOSTICO.md`
- `REGISTRO_DE_CAMBIOS.md`
- `PREGUNTAS_ABIERTAS.md`
- `docs/SMTP_GMAIL.md`
- `PASOS_SERVICIO_FINAL_readyproof.md`
- `C:\Users\jorge\.codex\.sandbox\setup_error.json`
- `C:\Users\jorge\.codex\.sandbox\sandbox.2026-10-26.log` — extractos pertinentes, no copia íntegra.

Documentación oficial consultada durante el diagnóstico: [Windows sandbox — OpenAI](https://learn.chatgpt.com/docs/windows/windows-sandbox).

No hace falta compartir `.env.local`, el archivo completo de configuración, historiales de navegación ni el directorio `.sandbox-secrets`. Este informe no contiene contraseñas ni tokens; sí incluye rutas locales, nombre del equipo y la dirección de correo dedicada para que el diagnóstico sea comprensible.

## 14. Actualización posterior: Gmail funciona por MCP y SMTP

- El MCP inicialmente consultó una cuenta personal. Jorge cambió la conexión a la cuenta dedicada desde la interfaz. Durante algunos reintentos get_profile falló con Unknown tool; posteriormente volvió a responder y confirmó readyproof.ar@gmail.com.
- Las primeras pruebas SMTP llegaron a STARTTLS pero terminaron durante autenticación. Un diagnóstico con AUTH LOGIN sin respuesta inicial permitió obtener 535 / 5.7.8: Gmail rechazaba las credenciales.
- Jorge encontró inicialmente que Contraseñas de aplicación no estaba disponible. Se indicó comprobar la verificación en dos pasos. Después pudo acceder a la pantalla para dar nombre a una aplicación; no se observó directamente qué ajustes de seguridad realizó.
- Jorge generó y guardó localmente una contraseña de aplicación válida. Se validó autenticación 235. Con autorización se quitaron sus espacios de agrupación de SMTP_PASSWORD, conservando todas las demás variables.
- smtplib.login también funcionó, sin cambios en el transporte de la aplicación. Un correo de prueba de texto sin adjuntos al destinatario autorizado fue aceptado por SMTP y encontrado por Message-ID en Enviados mediante MCP. No se confirmó recepción en destino ni flujo completo de PDF desde readyproof.
- No se mostraron claves ni se habilitó el worker o el envío global. El modo de prueba quedó activo. El bloqueo del navegador/sandbox sigue sin recuperación comprobada y es distinto del acceso MCP o SMTP que ahora funciona.
- Evidencia local saneada: out/diagnostico_control/resultado_auth_gmail.json y out/diagnostico_control/resultado_envio_gmail_clave_validada.json. No compartir .env.local al pedir ayuda.

## 15. Continuación: informe consolidado y prueba PDF preparada

- Se agregó el estado vigente al comienzo del informe y se distinguieron los antecedentes del pedido de ayuda actual. El bloqueo de navegador/sandbox no se considera resuelto por los accesos MCP y SMTP.
- Se inspeccionó la base de ejemplo con una transacción de solo lectura. La base estaba disponible, pero no se encontró una SAA-1 emitida con PDF íntegro y leyenda vigente que pasara los filtros de la inspección. No se cambiaron cargas, usuarios o envíos.
- Se revisaron los renders existentes de la muestra ficticia de dos páginas out/etapa_m1/SAA-1_con_leyenda.pdf. No se modificó ni se regeneró el PDF.
- Con crear_mensaje de app.correo se preparó únicamente una copia EML local: out/diagnostico_control/prueba_pdf_preparada.eml. Asunto: [Ejemplo] Prueba PDF SAA-1 de readyproof. Un adjunto application/pdf, idéntico byte por byte a la muestra revisada, 204711 bytes. Evidencia de integridad en prueba_pdf_preparada.json.
- No se transmitió este correo ni se inició el worker. La preparación del EML no equivale a probar autenticación API, emisión de una carga ni trazabilidad completa en base. Sigue pendiente una carga emitida válida para comprobar el flujo completo, además de la recepción/entregabilidad en destino.

## 16. Actualización: envío del PDF de muestra autorizado y aceptado

- Jorge autorizó explícitamente enviar el correo preparado a jorgesanchezing@gmail.com. Se transmitió una sola vez el EML previamente revisado, con su PDF ficticio sin cambios, desde readyproof.ar@gmail.com por SMTP STARTTLS.
- Antes de transmitir se comprobaron remitente, destinatario, asunto, ausencia de destinatarios adicionales, un único adjunto PDF y las huellas SHA256 de EML/PDF. Se conservó una reserva local que bloquea repetir el envío.
- Gmail aceptó la autenticación y el mensaje. El MCP confirmó la cuenta emisora y localizó el Message-ID exacto en Enviados, con readyproof-planilla.pdf de 204711 bytes, application/pdf.
- Evidencia: out/diagnostico_control/resultado_envio_pdf.json y copia original prueba_pdf_preparada.eml. No se mostró la clave ni se modificaron base, configuración global de prueba, aplicación, fuente/ o worker.
- Esto prueba el envío SMTP del PDF de muestra construido con crear_mensaje de readyproof. No prueba la recepción en la casilla destinataria, SPF/DKIM vistos en destino ni el flujo completo autenticado de API/emisión/cola en base. Estos puntos siguen pendientes, al igual que el control del navegador.
