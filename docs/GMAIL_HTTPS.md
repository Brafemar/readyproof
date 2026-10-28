# Gmail HTTPS para documentación de readyproof

Jorge autorizó preparar este transporte el 27/10/2026. Remitente: **readyproof.ar@gmail.com**. Destinatario de la prueba autorizada: **jorgesanchezing@gmail.com**. Cuenta de aplicación: **tecnico_readyproof**. No se incluyen contraseñas en el correo.

## Motivo y estado

El servidor 67.205.170.29 no logró conectar a smtp.gmail.com:587; HTTPS a Google:443 sí conectó. [DigitalOcean documenta el bloqueo de SMTP 25/465/587](https://docs.digitalocean.com/products/droplets/details/limits/). La contraseña de aplicación Gmail usada localmente no habilita la API HTTPS; hace falta una autorización OAuth propia.

**Activado el 27/10/2026.** Jorge creó el proyecto y cliente de escritorio, autorizó readyproof.ar@gmail.com en Google y el servidor verificó el remitente antes de guardar el permiso privado. La prueba por el endpoint de la app se envió a jorgesanchezing@gmail.com con logo y dos guías, sin contraseñas. El MCP confirmó el mensaje en Enviados y Jorge respondió «Sí, llegó con las dos guías».

Solicitud `e9416e59-1c57-5b99-b678-cdcecc28e18a`, mensaje Gmail `1a17dee776fd216c`. Gmail sustituyó el Message-ID reservado del MIME por `<CANjHx+_Hn=h9A2TuOPuqeAtzZOOKA-E2sfjZyFjLoNNM8fh24A@mail.gmail.com>`; la evidencia conserva ambos. Para revisar aceptación indeterminada, buscar también por asunto, destinatario y fecha: no asumir que Gmail conserva el Message-ID previo al transporte. Evidencia en `out/documentacion_entrega/prueba_real.json` y `gmail_confirmado.json`.

## Configuración o reautorización desde la PC administradora de Jorge

Usar la cuenta de Google que administra readyproof, sin compartir su contraseña ni códigos. En [Google Cloud Console](https://console.cloud.google.com/), elegir un proyecto propio de readyproof o preparar uno para esta integración, sin habilitar facturación ni servicios adicionales.

1. Habilitar **Gmail API** en la [biblioteca de APIs](https://console.cloud.google.com/apis/library/gmail.googleapis.com).
2. Configurar Google Auth Platform con nombre readyproof y contacto de soporte propio. Para un piloto de audiencia externa en modo de prueba, agregar readyproof.ar@gmail.com como usuario de prueba. Respetar los controles y las verificaciones que indique Google.
3. Crear un cliente OAuth de tipo **Aplicación de escritorio** en [Clientes](https://console.cloud.google.com/auth/clients). El asistente usa ese tipo y retorno local; no necesita dominio público.
4. Descargar su JSON en una carpeta privada. No ponerlo en el repositorio ni pegar su contenido en el chat. El tipo del JSON debe ser `installed`.
5. Ejecutar en PowerShell, ajustando solo la ruta del archivo:

```powershell
cd C:\Users\jorge\Readyproof
.\.venv\Scripts\python.exe scripts\autorizar_gmail_https.py --cliente-oauth "C:\RUTA_PRIVADA\cliente_oauth_readyproof.json"
```

El asistente abre el navegador de Google. Seleccionar **readyproof.ar@gmail.com** y revisar el permiso de envío de Gmail y de identificación de esa cuenta. La contraseña se escribe únicamente en Google. El código de retorno se recibe en un puerto loopback temporal; no se copia por chat. El asistente valida la cuenta y envía el permiso renovable al servidor mediante el SSH administrador existente. No imprime ni guarda tokens en archivos del proyecto.

El servidor vuelve a verificar el remitente antes de activar el permiso. Guarda las variables OAuth solo en `.env` privado, conserva un respaldo root de la configuración anterior y reinicia únicamente readyproof. **El asistente no envía ningún correo automáticamente.** No copiar el cliente OAuth ni su permiso al paquete del técnico o al celular: pertenecen al servicio de correo, no a cada usuario. La autorización inicial se completó y se probó; estos pasos quedan para recuperación o renovación.

## Prueba desde la app

Con el acceso privado ya activo, ingresar con tecnico_readyproof. En **Mi cuenta**, guardar **jorgesanchezing@gmail.com** como dirección de prueba y pulsar **Enviar documentación por correo**. El usuario puede cambiar después ese campo por su correo real autorizado.

El mensaje debe salir desde readyproof.ar@gmail.com con asunto «readyproof - Documentación de acceso», logo y dos guías Markdown adjuntas. Incluye el nombre de usuario; excluye contraseña, hash, clave SSH, credenciales de base y tokens. Se guarda un identificador de solicitud y Message-ID para comprobar Enviados sin repetir una aceptación desconocida.

La aceptación de Gmail no prueba recepción: Jorge debe revisar bandeja/spam y abrir las guías. Si se informa un resultado indeterminado, consultar antes de repetir. El correo de planillas sigue en su modo de prueba; este cambio afecta únicamente documentación.

## Operación

Variables privadas: `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`, `DOCUMENTACION_TRANSPORTE=gmail_api` y `DOCUMENTACION_MODO_PRUEBA=false`. No se incluyeron valores utilizables en esta guía. No se agregó ninguna dependencia: el cliente utiliza HTTPS de la biblioteca estándar.

Google puede caducar o revocar permisos; en particular, las autorizaciones de aplicaciones externas en modo de prueba pueden tener duración limitada. Revisar la vigencia del proyecto y su publicación con Google antes de prometer operación continua. La app falla de forma explícita y no reenvía automáticamente si no puede confirmar el resultado.

Referencias de implementación: [OAuth para escritorio, PKCE y retorno local](https://developers.google.com/identity/protocols/oauth2/native-app), [envío de MIME mediante Gmail API](https://developers.google.com/workspace/gmail/api/guides/sending) e [identificación de la cuenta autorizada](https://developers.google.com/identity/openid-connect/openid-connect).


## Envío manual de planillas desde la pantalla

El botón **Enviar PDF por correo** aparece junto a **Descargar PDF** cuando la carga está emitida. Usa el mismo consentimiento OAuth de Gmail ya autorizado, sin ampliar permisos.

Configuración privada del piloto:

```dotenv
PLANILLAS_TRANSPORTE=gmail_api
PLANILLAS_DESTINATARIOS_PRUEBA=casilla-autorizada@example.invalid
```

`MAIL_FROM` debe coincidir con readyproof.ar@gmail.com. La lista de casillas se carga en el `.env` privado; nunca se incorpora una contraseña o token a la interfaz. `MAIL_MODO_PRUEBA=true` se conserva para la cola anterior y no habilita envíos masivos.

La pantalla consulta `GET /api/correo/configuracion` y `GET /api/cargas/{id}/envios`. Al confirmar, llama a `POST /api/cargas/{id}/enviar` con `destinatario`, `inmediato: true`, CSRF e `Idempotency-Key` UUID. Se valida sesión, asignación al cliente, estado emitida, copia PDF, leyenda y destinatario permitido. El registro Envio, su copia inmutable y la reserva del intento quedan guardados antes de contactar Gmail. El resultado e identificador de Gmail se registran en Intento. Una aceptación desconocida se bloquea para revisión; no hay reintento automático de este envío. La cola SMTP anterior conserva su comportamiento.

No hay migración ni dependencias nuevas para este cambio. El service worker cambia la versión de su caché sin eliminar los borradores de IndexedDB. Después de actualizar, recargar con Ctrl+F5 sin borrar datos del sitio.


Las nuevas emisiones SAA-1 de la versión `00-26-rp2` se adjuntan en una sola hoja A4 horizontal. Para una carga emitida anteriormente, usar **Crear copia A4**, revisar y finalizar antes de enviarla. Los correos históricos y sus PDFs se conservan sin reprocesar.
