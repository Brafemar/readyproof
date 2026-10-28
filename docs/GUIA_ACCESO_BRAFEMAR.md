# Guía de acceso y carga de planillas en readyproof

Edición de entrega de etapa 5 (28/10/2026), para publicar junto con el catálogo ampliado verificado. Uso piloto: solo datos y firmas ficticios. El acceso público y el uso con clientes reales requieren habilitación independiente.

## Ingresar y cambiar la contraseña

1. Abrir el acceso privado con el túnel propio de ese equipo activo: http://127.0.0.1:8876/login. Otra PC o Android necesita su propia configuración; seguir ACCESO_TECNICO_BRAFEMAR.md. No compartir la clave SSH de Administración.
2. Ingresar el usuario individual y la contraseña entregados por Administración por un canal privado. No se usan contraseñas de Gmail, del servidor ni de PostgreSQL para entrar a readyproof.
3. El usuario admite letras sin tildes, números, puntos, guiones y guiones bajos. La contraseña distingue mayúsculas.
4. En Mi cuenta se puede cambiar la clave (al menos 12 caracteres, hasta 72 bytes UTF-8). Después del cambio se cierran las sesiones y debe ingresarse de nuevo.
5. Al terminar, sincronizar los cambios pendientes y usar Salir. No hay contraseñas predeterminadas ni publicadas en esta guía.

Si no se puede ingresar, revisar usuario, teclado y estado de la cuenta con Administración. No editar la BD ni crear otro primer administrador para recuperar acceso.

## Pantalla de trabajo

- Barra superior: cuenta, Mi cuenta, Salir y conexión. Administración aparece para el rol admin.
- Panel lateral: Cliente, Sistema y Planilla. Solo se muestran clientes asignados al técnico y sistemas activos. Dos instalaciones del mismo tipo se eligen por separado.
- Borradores del dispositivo: recupera las cargas de ese usuario en ese navegador; no es una bandeja global de todos los equipos.
- Formulario central: conserva campos, orden, opciones y secciones del kit.
- Indicador de avance: orienta sobre campos completados; no certifica el estado de la instalación.
- Barra inferior: Guardar borrador, Vista previa, Finalizar ejemplo; después de emitir, Descargar PDF, Enviar PDF por correo y, con permiso, Desbloquear con motivo. Emisiones anteriores conserva los PDF emitidos.

Leyenda visible: «Planilla conforme a IRAM 3546:2011». Retención mínima indicada: «T.C. 3 AÑOS».

## Sistemas y planillas

El catálogo ampliado incluye 79 planillas individuales, agrupadas en 15 sistemas:

- **SAA**: Sistema de Abastecimiento de Agua.
- **SAL**: Sistema de Extinción por Agentes Limpios.
- **SBC**: Sistema de Bombas Contraincendios.
- **SDI**: Sistema de Detección de Incendios.
- **SAP**: Sistema de Agua Pulverizada.
- **SCC**: Sistema Fijo de Extinción para Cocinas Comerciales.
- **SDC**: Sistema de Extinción por Dióxido de Carbono.
- **SEP**: Sistema Fijo de Extinción por Polvo.
- **SGE**: Sistema Generador de Espuma.
- **SHC**: Sistema de Hidrantes Contra Incendios.
- **SIM**: Simbología de Seguridad contra Incendios.
- **SRA**: Sistema de Rociadores Automáticos.
- **SRE**: Sistema de Rociadores de Espuma.
- **SSA**: Sistema Fijo de Extinción por Solución Acuosa.
- **STM**: Sistema de Tuberías y Mangueras.

SAA incluye SAA-1 a SAA-6; SDI, SDI-1 a SDI-5; SBC, SBC-1 a SBC-6; SAL, SAL-1 a SAL-4. Las demás familias aparecen con sus planillas correspondientes. SAL significa Agentes Limpios y SIM Simbología; no son planillas de alumbrado.

## Cargar, firmar y emitir

1. Seleccionar Cliente, la instalación en Sistema y el código de Planilla correcto. Usar Nuevo borrador cuando corresponda.
2. Completar Identificación e Información del sistema. En el piloto los textos ficticios comienzan con [Ejemplo]. Completar ejemplo es solo una ayuda de capacitación.
3. Respetar las opciones del formulario. En resultados se mantienen ✓, O, X y NA. O requiere una observación. En verificación con unidad se exige medición numérica, salvo NA. No se inventan frecuencias ni equivalencias calendario para S1–S5.
4. Revisar Guardado en el dispositivo y en el servidor. Guardar borrador conserva la carga e intenta sincronizar cuando hay conexión.
5. Completar nombre y DNI del responsable de la instalación; cargo opcional. DNI: de 8 a 15 dígitos, sin puntos ni guiones. En el piloto usar identidades ficticias.
6. Dibujar las firmas del técnico y del responsable en sus respectivos canvas con dedo, lápiz o mouse. Un toque sin trazo no constituye firma. Limpiar permite volver a dibujarla.
7. Abrir Vista previa y revisar identificación, respuestas, observaciones, logo readyproof, leyenda IRAM, marcas de agua y ambas firmas.
8. Seleccionar Finalizar ejemplo. La carga debe estar sincronizada y la vista previa debe corresponder al último cambio. Si queda finalizada sin PDF, Reintentar emisión conserva esa carga; no crear otra por este motivo.
9. Descargar PDF y abrirlo en un visor. SAA-1 ocupa una hoja A4 horizontal; las demás conservan la paginación del kit en A4 horizontal. El Excel es un paso interno y no se entrega al cliente.

El número de registro se asigna en el servidor al emitir. El original lleva revisión pública 0. La firma en pantalla no equivale a firma digital con certificado.

## Corregir una emisión

Solo el creador o un administrador puede seleccionar Desbloquear con motivo. El motivo es obligatorio. La carga vuelve a borrador y conserva el número; al reemitir utiliza la revisión siguiente (primera corrección: 1).

El PDF anterior permanece sin cambios en Emisiones anteriores. Revisar los datos y volver a dibujar ambas firmas antes de emitir la corrección. Las versiones históricas de plantilla que requieren Crear copia A4 conservan su PDF original.

## Enviar el PDF por correo

Después de emitir, seleccionar Enviar PDF por correo, revisar el destinatario autorizado del piloto y confirmar. El correo sale desde readyproof.ar@gmail.com con el PDF firmado adjunto, sin enlaces de descarga. No se envían contraseñas.

La pantalla consulta los envíos de ese PDF para evitar duplicados al recargar o repetir un clic. Una revisión nueva se puede enviar de nuevo; los adjuntos anteriores permanecen conservados. Si hubo un corte, consultar el resultado antes de repetir. Aceptación del proveedor no confirma recepción: revisar llegada y apertura con el destinatario, incluyendo spam.

El botón Enviar documentación por correo de Mi cuenta envía las guías de uso/acceso; es una acción distinta del envío de una planilla. La contraseña se cambia en Mi cuenta y no se adjunta ni se recupera para el correo.

## Trabajar sin conexión

Abrir la aplicación y cargar su catálogo con conexión antes de salir. Los borradores y firmas se conservan en IndexedDB, asociados al usuario y navegador. Para sincronizar, previsualizar, finalizar, emitir y enviar es necesario reconectar al servicio privado.

No borrar datos del sitio ni cerrar sesión con cambios sin sincronizar. Ante un conflicto entre dispositivos, conservar la copia local y pedir asistencia. Para recibir una actualización basta recargar cuando corresponda; no es necesario borrar IndexedDB.

## Soporte y errores

Contactar a Jorge Sánchez por el canal interno acordado para acceso, asignaciones y funcionamiento. Las interpretaciones técnicas o normativas corresponden al Lic. Martín Sánchez.

Informar fecha/hora, usuario, código de planilla, identificador de carga/envío, paso y mensaje visible. Las capturas deben contener solo datos ficticios. No compartir contraseñas, cookies, .env, códigos de dos pasos ni firmas reales.
