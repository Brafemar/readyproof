# Retomar configuración Gmail

## Estado vigente: Gmail autenticado y correo de texto aceptado

El MCP confirmó readyproof.ar@gmail.com. Jorge creó una contraseña de aplicación y la guardó localmente; se quitaron únicamente sus espacios de agrupación con autorización, conservando las demás variables. Gmail aceptó AUTH LOGIN y smtplib.login con código 235. El correo de prueba de texto al destinatario autorizado fue aceptado por SMTP y localizado en Enviados. No se confirmó recepción en destino ni envío de PDF mediante el flujo completo de la aplicación. MAIL_MODO_PRUEBA sigue activo y no se inició el worker. No volver a tratar la clave como vacía o inválida basándose en antecedentes. No abrirla para mostrarla ni sobrescribirla.

Evidencia: out/diagnostico_control/resultado_auth_gmail.json y resultado_envio_gmail_clave_validada.json. El script de envío bloquea repeticiones: no eliminar su evidencia para repetir mensajes. El bloqueo del navegador es un problema separado y sigue sin recuperación comprobada.

Los párrafos y el punto 6 siguientes conservan el estado histórico del diagnóstico inicial; la afirmación de ausencia de conexión Gmail ya no describe el estado actual. Informe actualizado para ayuda externa: docs/PEDIDO_AYUDA_CLAUDE_CONTROL_GMAIL.md.

Estado comprobado en la última reparación (2026-10-26): el chat Continuar configuración de Gmail fue asociado por herramienta a Readyproof Actual; antes figuraba sin proyecto. El sandbox elevado aislado a la carpeta actual imprime LEGACY_OK, pero las herramientas del chat todavía fallan al preparar la raíz antigua. MXC no está disponible. Pendiente recargar la sesión de la aplicación y verificar primero consola y navegador; no se declara reparado. Ver out/diagnostico_control/DIAGNOSTICO.md. No modificar ACL ni debilitar el aislamiento.

Trabajar en C:\Users\jorge\Readyproof, proyecto Readyproof Actual.

1. Leer AGENTS.md, fuente/KIT_AGENTS.md, PASOS_SERVICIO_FINAL_readyproof.md y las últimas entradas de REGISTRO_DE_CAMBIOS.md y PREGUNTAS_ABIERTAS.md.
2. Comprobar el cwd y las raíces autorizadas de esta conversación. La conversación anterior retuvo Documents\ChatGPT\Readyproof y el sandbox fallaba allí con SetSecurityInfo failed: 5. No debilitar el sandbox ni cambiar ACL para eludirlo.
3. Verificar primero un comando inocuo dentro del sandbox y luego el control del navegador. No dar por resuelto el problema antes de comprobarlo.
4. Jorge quiere operar Gmail con el cursor para configurar readyproof.ar@gmail.com; informa que ya está abierta esa cuenta en Chrome. Respetar las reglas de confirmación y credenciales del instructivo. No automatizar contraseñas ni códigos ni enviar correos reales sin autorización específica.
5. El transporte Gmail está implementado: migración 007, endpoint /api/cargas/<id>/enviar y worker independiente con máximo tres intentos. Última suite: 141 passed; compileall 0. Ver docs/SMTP_GMAIL.md.
6. Se creó .env.local con configuración pública y SMTP_PASSWORD vacío, MAIL_MODO_PRUEBA=true. No mostrar ni copiar contraseñas. No sobrescribir valores que Jorge haya completado después. El ejemplo de 127.0.0.1:8765 fuerza modo de prueba; no se inició el worker ni se hizo conexión Gmail.
7. Mantener fuente/, AGENTS.md y git sin modificaciones. No avanzar a otra etapa. Registrar resultado comprobado y pendientes sin secretos.
