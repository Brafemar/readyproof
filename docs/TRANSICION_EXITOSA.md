# Transición a producción real

Estado: **MODO_REAL ACTIVO**. Activación verificada: 28/10/2026 14:40:22 Argentina (UTC−03:00).

Jorge Sánchez autorizó el corte el 28/10/2026 a las 13:53 y aprobó el checklist. Confirmó mantenedora **READYPROOF**, certificado **IFI-2024-10001**, bar en campos de presión y conservación de ✓/O/X/NA en SDI.

## Configuración efectiva

Los archivos privados `/home/readyproof/.env` y `.env.local` tienen `MODO_PILOTO=false`, `MAIL_MODO_PRUEBA=false`, `EMPRESA_MANTENEDORA="READYPROOF"` y `CERTIFICADO_N="IFI-2024-10001"`. Se actualizan ambos porque systemd carga `.env` y la aplicación también lee dotenv. Se comprobaron los valores del proceso reiniciado y la aplicación respondió a `/login`. Las credenciales y los archivos de entorno no se incorporaron a Git. El acceso sigue siendo privado mediante el túnel existente, en `http://127.0.0.1:8876/login`.

## Cambios y conservación

La migración 017 agrega SCC-1 `00-26-bar1`: J21 cambia de MPa a bar. Conserva la versión anterior y no convierte valores históricos. SDI mantiene cuatro estados; no se inventan mediciones ni unidades para verificaciones cualitativas. Ver [detalle de unidades](UNIDADES_SCC1_BAR.md).

También se corrigió una carrera de cierre de sesión: una sincronización que termina después del bloqueo ya no lee un borrador retirado ni programa otro intento. La caché de interfaz pasa a v11. Recargar en línea después del corte sin borrar borradores pendientes.

Se compararon cargas, firmas, PDF archivados y usuarios antes y después del cambio de entorno. Permanecen iguales, incluidos los firmantes ficticios. Se cotejaron las huellas de `fuente/`, sin cambios. Los nuevos datos se cargan en registros nuevos; no se transforman clientes ficticios en reales.

## Verificación

- 543 pruebas finales aprobadas: 496 Ubuntu y 47 Windows; cero fallos y omisiones. Incluyen los 541 casos previos y dos nuevos de unidades.
- Compilación de aplicación, pruebas, migraciones y scripts: código 0.
- Ensayo 016→017 en base aislada y comparación de todas las filas anteriores: correcto.
- Respaldo cifrado antes de migración y otro antes del corte, conservados fuera de la rotación diaria.
- Respaldo posterior en Drive y restauración aislada: 20 tablas, 130 binarios y 48 PDF cotejados; producción no restaurada ni reemplazada.
- Transporte de planillas: Gmail por HTTPS. No se enviaron correos reales de prueba durante el corte.

## Monitoreo 24/48 horas

Responsable: Jorge Sánchez. Revisar errores, cambios de auditoría y envíos cada dos horas durante la operación. Revisar la copia nocturna y sus alertas al comenzar la jornada siguiente. Primera revisión de 24 h: **2026-10-29T14:40:22.502176-03:00**; cierre de observación de 48 h: **2026-10-30T14:40:22.502176-03:00**. No se creó una automatización nueva.

Ante un incidente, preservar los registros y avisar a Jorge antes de modificar configuración o restaurar. La configuración anterior está conservada en una carpeta privada del servidor. No regenerar documentos históricos ni repetir envíos de resultado indeterminado. El backlog ampliado sigue documentado; la autorización de transición no declara implementadas funciones que estén pendientes.

Tag solicitado: `v1.1-real-20261028T1353`. Evidencia resumida: `TRANSICION_REAL_REPORTE.json`; XML y diagnósticos conservados en `out/transicion_real_20261028/`.
