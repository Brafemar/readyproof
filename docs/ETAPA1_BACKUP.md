# Etapa 1 — Respaldo y restauración

Fecha: 28/10/2026.

## Cambios

Respaldo consistente de PostgreSQL y binarios, cifrado antes de subir a Drive, verificación de descarga, timer systemd y restauración en una base separada. Se mantuvieron las credenciales fuera del repositorio y los respaldos privados. Esta etapa no agregó una migración: partió del esquema 010 existente.

La documentación técnica completa está en `BACKUP_Y_RESTAURACION.md`. Los componentes se encuentran en `scripts/backup_readyproof.py` y `scripts/servidor_backup/`.

## Integridad

Evidencia inicial: `out/etapa1_backup/verificacion_drive_restore.json`; 17 tablas, 25 filas de planillas, 45 cargas, 45 firmas y 7 envíos; 130 binarios y 48 PDF exportados coincidentes. La restauración se realizó fuera de producción. Las etapas posteriores ampliaron el esquema y el contenido verificado; sus informes no sustituyen el registro histórico inicial.

## Siguiente

Cada modificación de esquema debe terminar con un respaldo actualizado y una restauración aislada. La etapa 5 documenta esquema 014, 19 tablas, 88 filas de planillas y 15 sistemas. Mantener claves recuperables y verificar periódicamente la restauración sin sobrescribir producción.
