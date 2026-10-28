# Auditoría runtime

La migración aditiva `016_tabla_auditoria` parte de `014_habilitar_11_sistemas`. Agrega la tabla `auditoria`, índices por fecha, registro, tabla y usuario, y una protección PostgreSQL contra UPDATE/DELETE de sus eventos. No altera ni genera retrospectivamente eventos de las cargas existentes. La futura corrección de unidades SCC, si Martín la aprueba, deberá usar la siguiente migración disponible; 016 identifica esta auditoría.

## Acciones registradas

- INSERT al crear una carga autenticada.
- UPDATE al guardar borrador, finalizar o emitir: snapshots anterior y nuevo.
- DESBLOQUEO al desbloquear una emisión: estado/revisión previos y nuevos, actor y motivo.

Se conserva además la trazabilidad anterior de `revisiones_carga` y `registros_acceso`. El registro nuevo no sustituye los PDF inmutables ni sus hashes. Los eventos toman el usuario de la sesión, no de un parámetro suministrado por el navegador.

Carga, revisión y evento se confirman en la misma transacción. Una emisión fallida revierte número, cambios y auditoría; una repetición idempotente de creación no agrega otro INSERT. Las lecturas y denegaciones quedan en el registro de acceso, sin generar recursivamente eventos de modificación.

## Consulta y permisos

Usar `GET /api/auditoria` con sesión administrativa. Los técnicos reciben 403. Filtros y paginación están documentados en `API.md`. Los snapshots incluyen datos del formulario; solo deben consultarlos administradores autorizados. Se excluyen binarios de firma/PDF, contraseñas y tokens. El registro restringido se incluye en el respaldo cifrado junto con las demás tablas.

La auditoría cubre las operaciones de cargas enumeradas. No se presenta como un registro automático de todas las escrituras SQL ni de cambios de clientes, sistemas o usuarios que no tengan hooks implementados. DELETE es una acción reservada; no habilita eliminación de evidencia.

## Conservación y migraciones

Los eventos no se editan ni eliminan por la aplicación. El downgrade solo permite retirar una tabla vacía; con eventos se detiene para conservarlos. Una necesidad de retención, exportación o tratamiento legal requiere un procedimiento expresamente autorizado, sin borrar silenciosamente trazabilidad.

Antes de aplicar: respaldo cifrado, ensayo de la migración en copia aislada y comparación de filas/binaros anteriores. Después: comprobar versión 016, índices/trigger, servicio, búsqueda/auditoría con datos ficticios en pruebas y restauración separada del respaldo actualizado. No se escriben eventos falsos para simular el historial anterior.
