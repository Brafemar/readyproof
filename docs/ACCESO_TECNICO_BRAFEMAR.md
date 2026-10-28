# Acceso técnico a readyproof desde PC y Android

Usuario de aplicación: **tecnico_readyproof**. Contraseña inicial: **entregada por Jorge por separado**. La aplicación no conserva una copia recuperable de la contraseña actual y no la incluye en correos de documentación.

## Otra PC con Windows

Recibir el paquete privado individual de Jorge y descomprimirlo completo en una carpeta propia. Incluye el script y una clave restringida al acceso de readyproof; no contiene la contraseña de la aplicación ni una clave de root.

Desde PowerShell, ubicado en la carpeta descomprimida:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\abrir_readyproof_privado.ps1
```

Mantener esa consola abierta. Abrir **http://127.0.0.1:8876/login**, ingresar con el usuario indicado y la clave recibida por separado. Cambiarla en **Mi cuenta** y volver a ingresar. Ctrl+C cierra el túnel de esa consola, sin apagar el servidor.

La dirección `127.0.0.1` es del equipo donde se está navegando. No funciona en otra PC o celular porque Jorge tenga abierto un túnel en su computadora: cada dispositivo necesita su propia conexión.

## Android

Jorge debe preparar con el técnico un cliente SSH que soporte clave privada y reenvío local. Una opción documentada es [ConnectBot, guía oficial de túneles](https://connectbot.org/guides/port-forwarding/). La instalación y prueba física del cliente en Android todavía deben verificarse con el técnico.

Configurar:

| Parámetro | Valor |
|---|---|
| Servidor SSH | `67.205.170.29` |
| Puerto SSH | `22` |
| Usuario SSH | `readyproof_tunel_tecnico` |
| Autenticación | Clave individual del paquete; no usar root ni la contraseña de la app |
| Tipo de reenvío | Local |
| Puerto de origen en el celular | `8876` |
| Destino en el servidor | `127.0.0.1:8000` |

Importar la clave individual en el cliente y comparar la huella del servidor con `acceso/huella_servidor.txt`, entregada por Jorge. Mantener la conexión SSH mientras se usa el navegador del celular. La sesión SSH puede mostrar una pantalla vacía: no ofrece consola de administración. Abrir **http://127.0.0.1:8876/login**, ingresar y cambiar la contraseña en **Mi cuenta**.

La guía oficial citada explica cómo agregar un reenvío desde el menú del host. Los nombres pueden variar por versión. Si la conexión se corta al cambiar de aplicación o el navegador no abre, conservar el borrador y consultar a Jorge; no publicar puertos del servidor para resolverlo.

## Recibir las guías por correo

1. Con la app abierta, entrar a **Mi cuenta**.
2. Escribir el correo propio y pulsar **Guardar correo**.
3. Seleccionar **Enviar documentación por correo**. El remitente es `readyproof.ar@gmail.com`.
4. Revisar bandeja y spam. Se adjuntan la guía de uso y esta guía de acceso; no se adjunta la clave SSH ni la contraseña.

Si aparece «Modo de prueba: documentación archivada», no hubo transmisión. Si se informa aceptación por Gmail, todavía corresponde comprobar recepción. Ante un resultado desconocido, no repetir clics: el identificador de solicitud permite revisar el intento sin reenviar automáticamente.

## Seguridad y soporte

El usuario SSH es exclusivo del túnel; la cuenta de aplicación tiene rol técnico y cliente asignado. No compartir el paquete con otros técnicos. Para otra persona corresponde otro acceso individual. Guardar las claves y el dispositivo con acceso restringido; no mandar firmas reales en capturas.

Soporte: Jorge Sánchez por el canal acordado. El servidor sigue privado y el uso se limita a datos y firmas `[Ejemplo]`. Las guías por correo ayudan a operar la app una vez configurado el acceso; el correo por sí solo no configura el túnel del dispositivo.


## Elegir sistema y planilla

El cliente de ejemplo tiene cuatro sistemas: Abastecimiento de Agua (SAA-1), Detección de Incendios (SDI-1 a 5), Bombas Contraincendios (SBC-1 a 6) y Extinción por Agentes Limpios (SAL-1 a 4). Elegí Sistema y después Planilla; el formulario muestra sus campos y controles originales. Cargá, firmá, revisá Vista previa y finalizá antes de descargar o enviar el PDF. Las tablas mensuales/semanales se desplazan dentro del formulario en celular.


## Identificación de firmantes y documentación

En **04 Firmas**, ingresá nombre completo y DNI del responsable del cliente; el cargo es opcional. El DNI debe tener de 8 a 15 dígitos, sin puntos ni guiones. En el piloto usá nombres/cargos con `[Ejemplo] ` y DNI ficticio `00000000`. El técnico se identifica con su cuenta autenticada. Sin ambas firmas y estos datos no se puede finalizar. Revisá la identificación complementaria al pie del PDF.

**Mi cuenta → Enviar documentación por correo** abre un modal: revisá o editá el destinatario y presioná **Enviar**. Ese destinatario no cambia el correo guardado del perfil. El mensaje explica las cuatro familias y los requisitos del responsable; se registran usuario, destino y fecha. No se envían contraseñas ni claves. Ver [guía de firmantes](FIRMANTES_Y_DOCUMENTACION.md).
