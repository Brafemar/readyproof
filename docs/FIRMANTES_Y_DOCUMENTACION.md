# Firmantes y documentación de acceso

La sección **04 Firmas** identifica al técnico autenticado de readyproof y al responsable de la instalación del cliente. Son firmas manuscritas capturadas en pantalla; no son firmas digitales con certificado.

## Completar y finalizar

1. Elegir Cliente, Sistema y Planilla. Hay cuatro familias y 16 formularios: SAA-1, SDI-1 a 5, SBC-1 a 6 y SAL-1 a 4. SAL es Extinción por Agentes Limpios.
2. Completar la carga y dibujar las dos firmas.
3. Ingresar el nombre completo y DNI del responsable. El cargo o función es opcional. El DNI requiere **8 a 15 dígitos ASCII, sin puntos ni guiones**, según la decisión de Jorge del 27/10/2026.
4. En este piloto, los nombres y cargos son ficticios y comienzan con `[Ejemplo] `. Usar `00000000` como DNI de ejemplo. **Completar ejemplo** prepara esos datos ficticios; las firmas se dibujan por separado.
5. Revisar **Vista previa** y finalizar. El backend también rechaza la finalización sin ambos trazos y los datos obligatorios, aunque la solicitud no provenga de la pantalla.

Los borradores admiten DNI incompleto mientras se edita. Los datos se conservan en el dispositivo y se sincronizan con control de revisión. Cambiar un dato invalida la vista previa anterior.

La identidad técnica se obtiene de la sesión al guardar el trazo. No se acepta una identidad de técnico enviada como texto desde el formulario. Los nombres y documentos del responsable se guardan con las firmas y con cada revisión, bajo los mismos permisos de la carga. No se exponen imágenes de firma por un endpoint independiente.

## PDF e historial

Las firmas permanecen en sus casilleros del kit. Una franja complementaria al pie de la última página identifica al técnico y al responsable, con DNI, cargo opcional, empresas y fecha del servicio. El contenido se ajusta proporcionalmente para reservar esa franja, sin quitar filas ni agregar páginas: SAA-1 conserva una A4 horizontal y las demás mantienen la paginación del kit.

La migración `010_firmantes` agrega campos y no completa identidades históricas por suposición. Los PDF emitidos y enviados anteriormente mantienen sus bytes y huellas. Una carga antigua sin identidad técnica registrada necesita una nueva firma en un borrador antes de finalizar; un PDF histórico sigue disponible para descarga.

## Enviar documentación

En **Mi cuenta → Enviar documentación por correo**, revisar el destinatario del modal y presionar **Enviar**. El campo es editable y no modifica el correo del perfil. El remitente es `readyproof.ar@gmail.com`.

El mensaje incluye el usuario, las cuatro familias, los requisitos de las firmas y el DNI, y las dos guías adjuntas. No contiene contraseñas ni claves SSH. La auditoría conserva usuario, destinatario, fecha y resultado. Una solicitud repetida conserva su resultado; cambiar el destinatario con el mismo identificador no genera otro envío.

La configuración privada de prueba y las restricciones generales de la aplicación siguen vigentes. Un envío aceptado por Gmail no sustituye la confirmación de recepción del destinatario.
