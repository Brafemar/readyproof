# Etapa 3 — Importador y validaciones

Estado: etapa completada y aplicada al servidor privado el 28/10/2026. Jorge autorizó expresamente la transferencia del código, catálogo y ZIP a la carpeta privada del servidor. Modo piloto conservado. Jorge confirmó que la medición obligatoria se limita a verificación (`ver`).

## Reglas

`app/carga/validacion.py` ofrece `validar_item_verificacion` y `ValidationError`, compatible con el error 422 de la API.

- O exige una observación no vacía. La app utiliza el área de Observaciones existente; no crea filas ni notas automáticamente.
- En un ítem de verificación con unidad, se exige medición numérica finita para ✓, O y X. NA permite omitirla. Cero es válido; booleanos, cadenas, NaN e infinitos no lo son.
- X y NA no exigen observación. Los campos generales con unidad mantienen su comportamiento previo: no se les agrega una obligación de completar medición.
- Omitir un bloque no permite eludir las mediciones de la planilla. La selección explícita de bloques por frecuencia corresponde a una etapa posterior; no se infieren frecuencias a partir de campos vacíos.
- Los borradores admiten datos en curso. Finalización, vista previa y emisión ejecutan las reglas completas antes de modificar el estado o convertir un PDF.
- Los PDF ya emitidos se descargan sin revalidación retroactiva de estas reglas ni regeneración de su contenido. Las definiciones actuales y sus huellas permanecen sin cambios.

No se comparan mediciones con límites normativos ni se calcula automáticamente cumplimiento. Las opciones actuales ✓/O/X/NA se conservan; una modificación de estados de las grillas sigue pendiente de Martín.

## Origen e importación

`scripts/importador_planillas.py` lee una carpeta con exactamente los 79 Excel o el ZIP oficial v5. No guarda libros ni modifica `fuente/`, las herramientas originales o los archivos de Descargas.

Actualmente `fuente/planillas/` contiene cuatro JSON, no 79 Excel. Para el lote oficial se usa `--origen` con `SG-PEM-IFI_Planillas_v5.zip`. El catálogo de referencia se conserva, sin cambios de contenido, en `docs/pedido_codex_v1_1/catalogo_referencia_planillas.json`.

El extractor conserva orden de bloques e ítems, filas físicas, opciones y unidades. Compara conteos, etiquetas, secciones, opciones generales, unidades de verificación y encabezados de las grillas contra el catálogo. Las unidades generales se leen del Excel: el catálogo no contiene un campo independiente para todas ellas. Las nuevas definiciones incluyen SHA256 del original, trazabilidad por fila y una versión determinista. Se distingue la fila del encabezado OBSERVACIONES de su primera fila editable, para no sobrescribir el título.

Estados del reporte:

| Estado | Acción |
|---|---|
| YA_EXISTE | Contenido compatible ya registrado; se conserva UUID, versión, huella, definición y manual. |
| A_IMPORTAR | Código nuevo, planificado en modo de simulación. |
| IMPORTADA | Nueva definición insertada con `--aplicar`. |
| CONTENIDO_DIFERENTE | Diferencias de contenido, opciones o unidades; reporte por líneas, sin sobrescribir. |

La comparación contempla las cuatro opciones de resultado en todos los controles, no solo sus etiquetas. Para las versiones aprobadas se comprueban también la definición completa y su huella, incluidos tipos y celdas; las versiones v5 se cotejan contra su definición determinista. Si existe cualquier diferencia, no se inserta parcialmente el resto del lote. La aplicación usa una transacción y un bloqueo de importación; repetir un lote ya importado no agrega filas. Las versiones históricas adicionales no se borran para forzar un conteo de 79 filas.

Los nuevos códigos se asocian al manual exacto cuando existe. Si falta, el reporte lo indica y no inventa un manual; el modelo permite el vínculo pendiente. La habilitación para emisión debe resolver esas asociaciones y el generador en las etapas correspondientes.

La creación de las 63 definiciones se ensaya en una BD aislada en esta etapa. La importación operativa y habilitación de esas 63 se reservan para Etapa 5. Registrar definiciones no las habilita por sí solo en la API ni crea sistemas de clientes.

## Comandos

Cotejo completamente local, sin conexión a BD:

```powershell
.\.venv\Scripts\python.exe scripts\importador_planillas.py --solo-catalogo --origen "$env:USERPROFILE\Downloads\SG-PEM-IFI_Planillas_v5.zip" --catalogo docs\pedido_codex_v1_1\catalogo_referencia_planillas.json --salida out\etapa3_importador\cotejo_79_sin_bd.json
```

Para cotejar contra la base seleccionada por DATABASE_URL, omitir `--solo-catalogo`. El modo predeterminado usa transacción de solo lectura. Solo `--aplicar` habilita inserciones y no puede combinarse con `--solo-catalogo`; no actualiza registros existentes. Usar `--aplicar` en una base aislada o en la etapa operativa autorizada.

## Evidencia local disponible

- Cotejo operativo: 79 Excel, 1.539 ítems, cero diferencias; sin conexión a BD ni cambios. `out/etapa3_importador/cotejo_79_sin_bd.json`.
- Pruebas focalizadas: reglas de medición/observación, borrador parcial, rechazo de cierre, importación aislada de 63 y repetición idempotente. Se conserva el contenido de las 16 definiciones previas y se rechaza una opción perdida sin inserciones parciales.
- Suite inicial de 299 casos dividida en dos grupos secuenciales para liberar PostgreSQL temporal entre grupos en Windows: 164 aprobadas en el primero, 134 aprobadas y un fallo 503 de conversión SBC-2 en el segundo. El caso SBC-2 pasó al repetirlo aisladamente. La causa exacta del 503 original no quedó registrada y no se atribuye a las validaciones. Después se agregó un caso de tipo de campo alterado y se ejecutaron las siete pruebas finales del importador con éxito. La conciliación por identificador acredita los 300 casos actuales, sin omitidas ni fallos pendientes y sin contar dos veces los reintentos. No se presenta como 300 aprobadas en una sola invocación.
- Ruta temporal corta y NODE_PATH del runtime existente para las pruebas de LibreOffice/Playwright. No se instala una dependencia nueva ni se altera el generador para resolver el entorno de pruebas.

## Transferencia y puesta en servicio

El intento inicial de transferencia fue rechazado por la revisión automática por falta de autorización específica para ese material interno. No se ejecutó. Jorge luego autorizó expresamente código, catálogo y ZIP de los 79 Excel hacia `67.205.170.29`, en `/var/backups/readyproof/revision-etapa3`. La transferencia se completó y se verificó el SHA256 del ZIP. Carpeta 0700 y archivo ZIP 0600; no hay enlaces públicos.

El cotejo real contra la BD se ejecutó antes de instalar y se repitió con el CLI instalado: 16 YA_EXISTE, 63 A_IMPORTAR, cero cambios y cero diferencias. La transacción de la revisión previa confirmó `transaction_read_only=on`. Los 25 registros totales de plantilla incluyen versiones históricas y quedaron íntegros. No se importaron ni habilitaron las 63 pendientes.

Se conservaron las fuentes anteriores en `/var/backups/readyproof/etapa3-fuentes-previas-20261028T105338`. Se respaldó antes de actualizar, se instaló el código con permisos del usuario de servicio y se comprobaron las reglas como `readyproof` contra una definición real de la BD, usando datos ficticios solo en memoria: caso completo válido, medición omitida rechazada, NA sin medición permitido y O sin observación rechazado. Ningún caso creó cargas ni modificó usuarios.

El login responde HTTP 200. Se verificó que las seis fuentes instaladas coinciden con las probadas localmente; las 17 tablas no cambiaron durante la instalación, se conservaron los 130 binarios y todas las definiciones/versiones/manuales de planillas. Esquema Alembic sigue en `012_sistema_cliente_activo`; esta etapa no requiere una migración de datos.

El respaldo posterior bajo systemd terminó satisfactoriamente y se descargó/restauró en `readyproof_test_restore_20261028T110135`: 17 tablas, 25 versiones de plantilla, 45 cargas, 45 filas de firmas, 7 envíos, 130 binarios y 48 PDFs exportados. Su SHA256 coincide con el último respaldo en Drive. La base activa no se sustituyó por una restauración. App y timer activos; modo piloto conservado.

Evidencia local de pruebas: `out/etapa3_importador/resultado_local.json`, que conserva su estado histórico anterior a la autorización. Evidencia operativa final: `out/etapa3_importador/resultado_servidor.json`; ver también `cotejo_bd_servidor.json`, `verificacion_servidor.json` y `aplicacion_servidor.json`.

La suite inicial tuvo 299 casos; después se agregó el caso de tipos alterados y se verificó con las siete pruebas finales del importador. La conciliación por identificador acredita los 300 casos actuales. Se conserva el fallo 503 de SBC-2 en la corrida completa y su reintento aislado correcto; no se afirma que los 300 pasaron en una única invocación ni que se haya identificado la causa del 503.

Pendientes: confirmación de la etapa 4 y de sus decisiones; habilitación operativa de las otras 63 planillas en etapa 5 y transición a datos reales en etapa 6, con autorización expresa. No se cambió fuente/, no se modificaron originales de Descargas y no se usó Git.
