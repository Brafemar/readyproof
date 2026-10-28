# Etapa 4 — Desbloqueo y revisión pública

Autorización de Jorge: desbloqueo solo para creador o administrador; conservar ✓ / O / X / NA del kit. Continúa el modo piloto con datos ficticios. No cambia la interpretación normativa ni se modifican herramientas de fuente/.

## Uso desde la aplicación

1. Abrir una carga emitida con una plantilla vigente.
2. Elegir **Desbloquear con motivo** e indicar la corrección que se necesita realizar.
3. La carga vuelve a borrador y aumenta su revisión pública. El PDF original queda conservado en **Emisiones anteriores**.
4. Corregir los datos y volver a dibujar ambas firmas. El nombre y DNI del responsable se conservan para revisión; las imágenes de firma no se reutilizan automáticamente.
5. Revisar la vista previa, finalizar y emitir. Se mantiene el número de registro; la nueva revisión tiene un PDF independiente.
6. Descargar o enviar la revisión actual desde los botones habituales. Los envíos previos conservan sus adjuntos originales y no bloquean el envío de un PDF nuevo.

El desbloqueo y la consulta de emisiones requieren conexión y sesión vigente. Los borradores sin sincronizar permanecen en IndexedDB. No borrar los datos del sitio para actualizar la app; basta una recarga. Las versiones antiguas de plantilla que el generador actual no puede emitir continúan usando la copia A4 existente.

## API y permisos

- `POST /api/cargas/{id}/desbloquear`, JSON `{"revision":3,"motivo":"[Ejemplo] Corrección de observación"}`. La revisión solicitada es la de concurrencia devuelta por la API; no debe confundirse con `revision_publica`.
- Autenticación, CSRF y asignación al cliente obligatorios. Solo creador o admin, estado emitida y carga vigente. Rechazo de motivo vacío, estado incorrecto o revisión obsoleta antes de modificar datos.
- `GET /api/cargas/{id}/emisiones` lista revisiones conservadas.
- `GET /api/cargas/{id}/emisiones/{revision_publica}/pdf` descarga el original con control de acceso. No hay enlaces públicos.
- `GET /api/cargas/{id}/pdf` sirve únicamente la emisión actual. Durante la corrección devuelve conflicto hasta emitir de nuevo.

## Persistencia y numeración

La migración `013_desbloqueo_revision` es aditiva. Conserva UUID, JSON, firmas, PDF, envíos y revisiones anteriores. Agrega los campos solicitados a cargas, el contador singleton y la tabla de emisiones archivadas. `pdf_sha256` sigue siendo compatible con los envíos existentes; `pdf_hash` se completa con la misma huella en las emisiones nuevas.

El número global se asigna al emitir, nunca al crear un borrador. PostgreSQL bloquea la fila del contador hasta el commit. No se usa una secuencia: una transacción fallida no consume números. La numeración no se reinicia por año y la reemisión mantiene el número.

Primera emisión nueva: revisión pública 0, como el valor inicial solicitado. Cada desbloqueo aumenta una revisión; la primera corrección se reemite como revisión 1. La reemisión no vuelve a aumentarla. `Carga.revision` continúa detectando escrituras simultáneas y es independiente de la revisión pública.

Los PDF históricos no se renumeran ni se reescriben. Antes de desbloquear un histórico sin número se conserva exactamente como revisión 0; el número se asignará únicamente cuando se vuelva a emitir. El historial contiene PDF, SHA256, datos y firmantes correspondientes a cada emisión. PostgreSQL rechaza UPDATE y DELETE de emisiones archivadas. La migración inversa rechaza eliminar revisiones o desbloqueos ya registrados.

El número y la revisión se imprimen en el espacio reservado al pie; no se cambian filas, encabezados, firmas ni paginación del kit. La vista previa inicial no reserva un número. Los nuevos originales emitidos incluyen el identificador y sus metadatos.

## Grillas SDI

Se aceptan exactamente ✓, O, X y NA en las celdas respondidas de las grillas. No se exige completar períodos futuros ni se inventa la equivalencia calendario de S1–S5. Continúan las reglas de etapa 3: O requiere observación y la medición solo es obligatoria en verificación con unidad, salvo NA.

## Respaldo y aplicación

El respaldo incluye los PDF de `emisiones_carga` en el manifiesto de hashes, el dump y la exportación independiente. El restaurador sigue admitiendo respaldos antiguos que no contienen esa tabla.

El procedimiento `scripts/aplicar_etapa4_revision.py` inspecciona huellas remotas, ensaya la migración en una base nueva y solo permite aplicar después de una suite aprobada. Antes de aplicar: respaldo cifrado verificado en Drive, copia privada pre-013 y conservación de fuentes anteriores. Se detiene únicamente el servicio readyproof durante la instalación. No se sustituye la base activa por una restauración de prueba.

## Validación y aplicación verificadas — 28/10/2026

- 325 casos actuales conciliados por identificador; cero fallos pendientes, errores u omitidas. No se presenta como una sola invocación: primera tanda 187 aprobadas y dos fallos; segunda tanda 192 aprobadas y un fallo; última tanda con código final, 59 aprobadas. Los reintentos no aumentan el total.
- Incidencias corregidas: el PDF simulado del caso nuevo de correo necesitaba la leyenda IRAM; se evitó el autoflush de consultas durante la emisión para conservar una sola actualización de revisión; la prueba del diálogo móvil ahora espera la respuesta de la API. Las primeras pruebas focalizadas también ajustaron la simulación de migración y la sesión revocada al cambiar asignaciones. Se conservan logs/JUnit originales.
- Última tanda: móvil con desconexión/recarga y dos firmas, desbloqueo desde botón, conservación de datos, ambas firmas nuevas, reemisión con mismo número y revisiones 0/1, descarga original idéntica byte a byte, correo simulado de la nueva revisión sin duplicar la anterior, permisos y contador concurrente. No se enviaron correos reales.
- Compilación de app, pruebas y migraciones sin errores; revisión de secretos sin hallazgos en los archivos cambiados. Sin dependencias nuevas.
- Muestra revisada visualmente: output/pdf/SAA-1_registro_revision.pdf, una hoja A4 horizontal, cuatro imágenes, registro/revisión 0, firmas y leyenda legibles. No cambia la paginación de SDI/SBC/SAL ni las herramientas originales.
- Aplicación privada: esquema 013_desbloqueo_revision; 972 filas de 15 tablas de negocio comparadas durante la migración sin diferencias. Fuente anterior en /var/backups/readyproof/etapa4-fuentes-previas-20261028T115433. Respaldo pre-013 privado y SHA256 verificados.
- Aplicación activa como usuario readyproof; login HTTP 200; las 12 fuentes instaladas coinciden con las probadas; el JavaScript servido coincide y el Service Worker es v8. Timer de respaldo activo.
- Respaldo posterior cifrado verificado en Drive y restaurado en readyproof_test_restore_20261028T115558: esquema 013, 19 tablas, 130 binarios y 48 PDF exportados coincidentes. Se conservan 45 cargas, 45 filas de firmas, 7 envíos y 25 versiones de plantilla. La restauración no modificó la base activa.
- Evidencia: out/etapa4_revision/estado_suite.json, aplicar.json, verificacion_servidor.json, revision_secretos.json y los JUnit de cada tanda.

Etapas 5 y 6 requieren confirmación independiente. No se habilitan las 63 planillas restantes, no se incorporan datos reales ni se cambia infraestructura pública en esta etapa. La definición de establecimiento, períodos y transición real continúa con el alcance de las etapas posteriores.


Este corte cumple las tareas enumeradas de desbloqueo/revisión y cuatro estados del encargo por etapas. La selección dinámica ampliada del primer instructivo (establecimientos, listas con búsqueda/alta y precarga de equipos) no se implementó en este corte: continúa abierta y no debe darse por entregada ni omitirse antes del uso real. El estado de anulación se agregó como campo reservado; no se entrega todavía una operación de anular ni la búsqueda de etapa 6.
