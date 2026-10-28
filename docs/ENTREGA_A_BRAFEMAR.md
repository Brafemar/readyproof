# Entrega de readyproof al técnico

readyproof permite cargar registros SG-PEM-IFI, conservar borradores, incorporar las firmas en pantalla del técnico y del responsable, revisar una vista previa y emitir un PDF con identificación, leyenda IRAM y marcas de agua. Esta entrega habilita SAA-1, SDI-1 a 5, SBC-1 a 6 y SAL-1 a 4 en un servidor privado de revisión, exclusivamente con datos y firmas ficticios. El nombre del archivo se conserva según el pedido; la aplicación y la documentación visible se identifican como readyproof.

## Acceso

- Servidor privado: `67.205.170.29`; servicio accesible únicamente por túnel propio.
- Navegador, con el túnel activo en ese dispositivo: **http://127.0.0.1:8876/login**.
- Usuario de la aplicación: **tecnico_readyproof**.
- Contraseña temporal: entregada por Jorge por un canal privado o correo separado. No figura en este documento ni en los adjuntos automáticos.
- Primer ingreso: cambiar la clave en **Mi cuenta**, ingresar nuevamente y guardar el correo propio.
- Paquete para otra PC: script de túnel, clave exclusiva del técnico y huella del servidor. Nunca usar ni compartir la clave root de Jorge.
- Android: configurar su propio túnel con un cliente SSH compatible; parámetros en [Acceso técnico](ACCESO_TECNICO_BRAFEMAR.md).

## Carga rápida

1. Elegir Cliente, Sistema y Planilla. Solo aparecen los registros habilitados y asignados; actualmente hay un cliente ficticio y cuatro sistemas con 16 planillas.
2. Completar los datos `[Ejemplo]`, guardar y dibujar las dos firmas. Abrir **Vista previa**, revisar y finalizar.
3. Seleccionar **Descargar PDF** y revisar las hojas A4 horizontales. SAA-1 usa una hoja; las otras conservan la paginación del kit. No entregar el Excel interno.
4. Seleccionar **Enviar PDF por correo**, revisar el destinatario autorizado del piloto y confirmar. Una carga del formato anterior se recupera con **Crear copia A4**, vista previa y finalización.

En **Mi cuenta**, guardar el correo y seleccionar **Enviar documentación por correo**. El mensaje incluye el usuario y dos guías; no incluye contraseñas ni claves SSH. Ese botón envía documentación de acceso, no el PDF de una carga.

## Soporte y alcance

Soporte: **Jorge Sánchez**, por el canal acordado para esta entrega. Para criterios técnicos/normativos, consultar al Lic. Martín Sánchez. Informar paso, mensaje e identificador de carga; no enviar claves, cookies ni archivos `.env`.

La cuenta técnica tiene acceso al cliente asignado y no puede abrir Administración. Se comprobaron login, permisos y PDF con su cuenta, incluidas las 16 planillas en A4 horizontal con logo, leyenda IRAM, marcas de agua y ambas firmas; SAA-1 usa una hoja y las demás conservan la paginación del kit. La suite completa final aprobó **232 pruebas**, con compilación sin errores.

El botón de documentación quedó activo mediante **Gmail HTTPS**. La prueba desde readyproof.ar@gmail.com hacia la casilla de prueba autorizada por Jorge se encontró en Enviados con las dos guías; Jorge confirmó su recepción. La dirección guardada en la cuenta técnica es actualmente una casilla de prueba de Jorge: el técnico deberá reemplazarla por su dirección propia en Mi cuenta al recibir el acceso.

**Estado de la entrega: piloto privado operativo.** No equivale a go-live productivo: siguen pendientes dominio/HTTPS, habilitación de datos reales, respaldo externo, revisión del dispositivo Android y dimensionamiento de uso concurrente. Los borradores y la operación sin conexión requieren preparar previamente el dispositivo; emisión y correo necesitan conexión al servicio.


## Identificación de firmantes y documentación

En **04 Firmas**, ingresá nombre completo y DNI del responsable del cliente; el cargo es opcional. El DNI debe tener de 8 a 15 dígitos, sin puntos ni guiones. En el piloto usá nombres/cargos con `[Ejemplo] ` y DNI ficticio `00000000`. El técnico se identifica con su cuenta autenticada. Sin ambas firmas y estos datos no se puede finalizar. Revisá la identificación complementaria al pie del PDF.

**Mi cuenta → Enviar documentación por correo** abre un modal: revisá o editá el destinatario y presioná **Enviar**. Ese destinatario no cambia el correo guardado del perfil. El mensaje explica las cuatro familias y los requisitos del responsable; se registran usuario, destino y fecha. No se envían contraseñas ni claves. Ver [guía de firmantes](FIRMANTES_Y_DOCUMENTACION.md).
