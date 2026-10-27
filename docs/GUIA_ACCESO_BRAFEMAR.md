# Guía de acceso y carga de planillas en readyproof

Edición del 27/10/2026. Guía para técnicos y administradores. Esta versión permite revisar **SAA-1 con datos y firmas ficticios**. El acceso público y el uso con clientes reales siguen pendientes de habilitación. El nombre del archivo se conserva como fue solicitado; la identidad visible es readyproof.

## Acceso inicial

1. Abrir la dirección que indique Administración. En esta máquina de revisión es [readyproof local](http://127.0.0.1:8765/login). Esa dirección solo funciona en el equipo donde está iniciado el servicio; no es un acceso desde un teléfono o desde otra computadora.
2. Ingresar el usuario individual y la contraseña inicial entregados por Administración por un medio privado. **No hay contraseña predeterminada ni una clave publicada en esta guía.** No usar la contraseña de DigitalOcean, Gmail o PostgreSQL para ingresar a readyproof.
3. Seleccionar **Ingresar**. El usuario admite letras sin tildes, números, puntos, guiones y guiones bajos; no es una dirección de correo. La contraseña distingue mayúsculas.
4. Abrir **Mi cuenta** para cambiar la clave inicial por una propia: al menos 12 caracteres y hasta 72 bytes UTF-8. El cambio cierra la sesión; ingresar nuevamente.
5. Al terminar, usar **Salir**, especialmente en equipos compartidos. Antes de salir, confirmar que los cambios pendientes se sincronizaron.

La cuenta `tecnico-readyproof` existe para la revisión de ejemplo. Administración debe entregar o restablecer su contraseña antes de utilizarla; no se conserva una clave de acceso en la documentación. Cada técnico operativo deberá tener su cuenta individual para conservar la autoría de las cargas. `msanchez` es una cuenta administradora local, no una contraseña ni un acceso de DigitalOcean.

Si aparece **Usuario o contraseña incorrectos**, revisar el nombre, la distribución del teclado y el estado de la cuenta con Administración. Después de cinco intentos fallidos para el mismo usuario en 15 minutos puede aparecer un bloqueo temporal: esperar el intervalo indicado, sin repetir intentos. No crear otro primer administrador ni editar la base para recuperar acceso.

## Pantalla de trabajo

| Sector | Uso |
|---|---|
| Barra superior | Cuenta activa, Mi cuenta, Salir y estado de conexión. Administración aparece para el rol admin. |
| Panel lateral | Listas desplegables de **Cliente**, **Sistema** y **Planilla**. El técnico ve sus clientes asignados. |
| Secciones laterales | Accesos a Identificación, Información del sistema, Observaciones y Firmas. |
| Borradores del dispositivo | Recuperar una carga local o seleccionar **+ Nuevo borrador**. No representa una bandeja global de todos los equipos. |
| Formulario central | Campos y opciones en el orden de la definición de SAA-1. |
| Indicador de avance | Muestra cuánto se completó; no reemplaza la revisión técnica ni implica que un sistema cumpla. |
| Estado de guardado | Distingue guardado en el dispositivo y sincronización con el servidor. |
| Barra inferior | Guardar borrador, Vista previa, Finalizar ejemplo y, después de emitir, Descargar PDF. |

La leyenda visible es «Planilla conforme a IRAM 3546:2011» y la retención indicada es «T.C. 3 AÑOS». La interfaz no realiza por sí sola una certificación del estado de la instalación.

## Cargar SAA-1 paso a paso

1. Seleccionar un cliente ficticio asignado, su sistema de abastecimiento de agua y **SG-PEM-IFI-SAA-1**. Los grupos SDI, SBC y SAL del catálogo no equivalen todavía a formularios operativos habilitados.
2. Seleccionar **+ Nuevo borrador** si corresponde. Confirmar cliente, sistema y código antes de escribir.
3. Completar **Identificación**. En esta revisión, los textos de ejemplo comienzan con `[Ejemplo]`; la empresa mantenedora predeterminada es readyproof. Fechas y números deben ingresarse según el tipo de campo.
4. Completar **Información del sistema** sin omitir o reinterpretar sus etiquetas u opciones. El botón **Completar ejemplo** sirve solo para capacitación; no representa un resultado de inspección.
5. Completar las observaciones en sus cuatro renglones. Registrar aclaraciones técnicas necesarias sin inventar valores o frecuencias.
6. Revisar el estado de guardado. El guardado automático puede conservar datos solo en el equipo cuando no hay señal. **Guardar borrador** intenta también sincronizarlos cuando hay conexión.
7. Incorporar ambas firmas ficticias y abrir **Vista previa**.
8. Revisar las dos páginas, identificación, respuestas, observaciones, logo readyproof, leyenda IRAM y espacios de firma. Si se modifica la carga, abrir una vista previa nueva.
9. Con la carga sincronizada, ambas firmas y vista previa vigente, seleccionar **Finalizar ejemplo →**. La pantalla finaliza y solicita la emisión del PDF. Una carga emitida queda sin edición.
10. Si aparece **Reintentar emisión →**, revisar el mensaje: puede haber quedado finalizada sin PDF. No crear una copia innecesaria; pedir asistencia si el error continúa.

## Firmar en canvas

En **Firmas de prueba** hay dos recuadros: **Supervisor del mantenedor** y **Responsable de la instalación**. Dibujar un trazo con el dedo, lápiz o mouse, manteniendo el contacto hasta terminar. Un toque sin movimiento no constituye una firma.

Usar **Limpiar** en el recuadro correspondiente si hay un error y dibujar nuevamente. Esperar el guardado y comprobar ambas firmas en la vista previa. En esta revisión deben ser trazos ficticios; no usar firmas personales reales. El dibujo se incorpora únicamente a la planilla correspondiente y no equivale a una firma digital con certificado.

## Descargar y abrir el PDF

Después de la emisión aparece **Descargar PDF**. Guardar el archivo en una ubicación privada y abrirlo con el visor del equipo. Si el navegador no lo muestra en pantalla, buscarlo en Descargas. Se entrega PDF; el Excel es un paso interno.

Comparar el archivo abierto con la vista previa. Si hay una diferencia, informar código e identificador de carga antes de volver a emitir o enviar. No modificar manualmente el PDF ya emitido ni compartir enlaces internos de la aplicación con el cliente.

## Correo con adjunto

**La pantalla actual todavía no tiene un botón de envío por correo.** El circuito implementado permite que Administración prepare y procese el envío del PDF emitido mediante la herramienta operativa. El destinatario recibe el PDF adjunto, sin enlaces de descarga.

Para la prueba local, Administración puede usar `scripts/prueba_operativa_final.py`. Su modo predeterminado guarda un EML sin transmitir; el envío real requiere `--smtp` y una casilla de prueba autorizada. El procedimiento está en [la guía técnica de deployment](DEPLOYMENT_DIGITALOCEAN.md#prueba-operativa-local). El técnico entrega a Administración el identificador de la carga y el destinatario revisado por el canal interno acordado.

No repetir una solicitud para preguntar si llegó: cada POST de envío crea otro registro. **Pendiente** indica que se encoló; **enviado** indica aceptación SMTP y no demuestra recepción. La llegada y apertura del adjunto se confirman con el destinatario. Si hay un fallo o aceptación desconocida, Administración revisa la auditoría antes de reintentar.

## Trabajo sin conexión

Preparar la aplicación y su catálogo con conexión antes de salir. El borrador y las firmas de prueba pueden guardarse en IndexedDB en ese mismo equipo. Para sincronizar, previsualizar y emitir hace falta volver a conectar al servicio. El modo sin señal no envía correo.

No borrar datos del navegador, cambiar de perfil, usar limpieza automática ni cerrar sesión con cambios sin sincronizar. Los conflictos entre dispositivos y la sincronización completa de la etapa 8 siguen pendientes; ante un aviso de conflicto, conservar la copia local y consultar a Administración. La prueba física en celular y la protección de dispositivos para firmas reales requieren su revisión operativa.

## Soporte y reporte de errores

Para cuentas, asignaciones y funcionamiento, contactar a **Jorge Sánchez por el canal interno acordado**. Para interpretación de campos, criterios o normas, consultar al **Lic. Martín Sánchez**. No hay un teléfono, correo de soporte ni portal nuevo definido por esta guía.

Informar fecha y hora, usuario, código de planilla, identificador de carga o envío, paso realizado y mensaje visible. Una captura debe usar solo datos ficticios y ocultar información personal. Nunca adjuntar contraseñas, cookies, `.env.local`, códigos de dos pasos ni firmas reales.

| Situación | Acción |
|---|---|
| No aparecen clientes | Pedir a Administración que revise las asignaciones de la cuenta. |
| Formulario inválido | Revisar campo señalado, tipo de fecha/número y prefijo `[Ejemplo]` donde corresponda. |
| Finalizar deshabilitado | Verificar conexión, sincronización, dos firmas y vista previa posterior al último cambio. |
| No se genera el PDF | Conservar el borrador y avisar el identificador; el servicio requiere LibreOffice. |
| Sesión vencida | Ingresar nuevamente con la misma cuenta para recuperar sus borradores. |
| No llega el correo | Administración verifica estado, intento y Message-ID; revisar también spam. |
