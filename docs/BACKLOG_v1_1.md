# Backlog readyproof v1.1

Actualizado el 28/10/2026 según el encargo recibido. La Etapa 0 está documentada en [DIAGNOSTICO_ETAPA0_V1_1.md](DIAGNOSTICO_ETAPA0_V1_1.md). Etapas 1 y 2 completadas: respaldo Drive/restauración verificados y migraciones 011–012 aplicadas. No se habilitaron datos reales. Informe de ejecución en ETAPA2_CUIT_Y_SISTEMAS.md.

## Clientes: CUIT/CUIL único

- Incorporar CUIT/CUIL y su validación de formato y dígito verificador.
- Prever una carga inicial y revisión de los registros existentes antes de exigir `UNIQUE` y `NOT NULL`.
- Mantener trazables las relaciones de clientes, sistemas, cargas y envíos; resolver duplicados antes de migrar.
- Decisión resuelta: conservar UUID como clave primaria e incorporar CUIT normalizado de once dígitos, único y obligatorio, validando dígito verificador. No reemplazar las referencias existentes.
- Migración en dos pasos: columna inicialmente opcional y reporte de faltantes/duplicados; revisión administrativa y luego restricciones. El cliente ficticio actual no tiene CUIT en una columna propia: no inventar ese dato.

## Numeración de registros

- Agregar `numero_registro` mediante contador global de una fila con bloqueo transaccional, único y seguro ante emisiones concurrentes. No usar una secuencia para prometer ausencia de huecos.
- Mantener el UUID de carga utilizado por la sincronización y la idempotencia.
- Incorporar búsqueda por número y mostrarlo en trazabilidad y documentos cuando se apruebe su ubicación.
- Decisión resuelta: asignar solo al emitir, sin huecos y sin reinicio anual. Crear o sincronizar borradores no consume número.
- Preservar los PDF históricos; una migración no debe reescribir documentos ya emitidos.
- Separar revisión de concurrencia de revisión documental pública. Desbloquear con motivo y permiso; conservar número, todas las revisiones y sus PDF inmutables. Conservar también registros anulados.

## Formatos, visitas y catálogos

- Importador determinista desde los 79 Excel oficiales, por versiones; conservar filas, textos, opciones y unidades. No alterar los 16 históricos.
- Incorporar establecimientos, ficha general y equipos por sistema, responsables por cliente/DNI y búsquedas con permisos definidos.
- Proponer visitas por período y agregación para las matrices semanales/mensuales, compatibles con cargas históricas. Confirmar la convención S1–S5 antes de implementarla.
- Exigir observación para O y mediciones cuando correspondan salvo NA. Revisar con Martín cualquier contradicción normativa sobre estados de las grillas.
- Importar manuales reales mediante ediciones, conservando asociaciones históricas; revisar la unicidad global actual de `Manual.codigo`.
- Mantener piloto hasta autorización expresa de uso real y confirmar datos de empresa mantenedora/certificado.

## Criterios de aceptación

Migración ensayada con respaldo y datos ficticios, permisos y búsquedas probados, alta concurrente sin duplicados, trazabilidad conservada y documentación actualizada. La habilitación de uso real continúa sujeta a los pendientes generales del checklist.


## Estado después de Etapa 2 — 28/10/2026

Implementados: CUIT opcional con normalización/validación y unicidad, auditoría de faltantes y sistema activo con cliente obligatorio. CUIT obligatorio queda pendiente de completar/revisar los registros mediante un flujo autorizado; el cliente ficticio actual sigue sin CUIT. Establecimientos, datos dinámicos, numeración y revisiones públicas todavía no se implementaron. Respaldo vigente 012 y restauración separada verificados; modo piloto conservado.
