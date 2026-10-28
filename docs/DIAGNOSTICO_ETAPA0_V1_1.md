# Diagnóstico Etapa 0 — readyproof v1.1

Fecha de cierre: 28/10/2026. Consulta del servidor: 27/10/2026, 22:16, Argentina.

## Resultado y alcance

Diagnóstico terminado. No se modificaron código de aplicación, generadores, definiciones, migraciones, originales ni datos de negocio. No se desplegó ni se enviaron correos nuevos. Se produjeron este informe y evidencias de lectura bajo `out/diagnostico_v1_1/`.

El encargo recibido dice: «Etapa 0 — Diagnóstico (sin modificar código). Detenerse y reportar.» Por eso este cierre no inicia las migraciones ni la habilitación de uso real. La siguiente etapa es respaldo externo con autorización de Drive por Jorge y prueba de restauración.

## Fuentes y cotejo

Se leyeron la instrucción `INSTRUCCION_CODEX_planillas_SG-PEM-IFI_1.md`, el catálogo JSON y el inventario XLSX de Descargas. `Paquete_Codex_planillas_1.zip` contiene esos documentos de encargo, no los Excel de las planillas.

Los 79 originales se localizaron en `SG-PEM-IFI_Planillas_v5.zip` y también en `SG-PEM-IFI_Serie_completa_v5.zip`. Los 79 archivos coinciden byte a byte entre ambos paquetes. El segundo contiene además los 15 manuales. No se extrajeron ni alteraron los originales. Las huellas individuales están en `cotejo_excel.json`.

Los 79 Excel, el catálogo y los conteos del inventario coinciden: 1.539 ítems/campos, distribuidos en 14 formatos generales, 8 semanales, 11 mensuales y 46 listas de verificación. Hay 135 campos generales con opciones, 93 campos generales con unidad y 229 mediciones en listas de verificación. El inventario trae estados anteriores (1 cargada, 15 a confirmar y 63 pendientes); no se modificó ese archivo.

Hay 16 definiciones habilitadas y 25 filas totales en `planillas`, incluyendo versiones históricas. Las 16 definiciones locales coinciden con las vigentes del servidor por huella y contenido. Sus 389 ítems/campos conservan orden, bloques, opciones, unidades y controles respecto de los Excel. No hay filas faltantes ni sobrantes. En SBC-2, filas 11, 36 y 37, el texto y la unidad se guardan separados y se reúnen al mostrar el campo; no es pérdida de contenido.

Procedencia de la app: SAA-1 se obtiene mediante `app/planillas/definiciones/saa1.py` de `fuente/herramientas/planillas_data3.py`. Las quince SDI/SBC/SAL se cargan mediante `app/planillas/multisistema.py` y `app/carga_planillas.py`, verificando las huellas del catálogo contra `fuente/herramientas/planillas_data2.py` y `build_planilla.py`. La migración `009_multisistema` habilita sus definiciones individuales y los sistemas de ejemplo. El modelo de encabezado es `fuente/modelos/SDI-1.xlsx`; los originales del kit no se modificaron.

| Planilla | Versión vigente | Formato | Bloques | Ítems/campos | Diferencias de contenido | Sin control |
|---|---|---|---:|---:|---:|---:|
| SAA-1 | 00-26-rp2 | general | 4 | 22 | 0 | 0 |
| SAL-1 | 00-26-ms1 | general | 4 | 18 | 0 | 0 |
| SAL-2 | 00-26-ms1 | grid_m | 1 | 5 | 0 | 0 |
| SAL-3 | 00-26-ms1 | ver | 3 | 25 | 0 | 0 |
| SAL-4 | 00-26-ms1 | ver | 1 | 7 | 0 | 0 |
| SBC-1 | 00-26-ms1 | general | 5 | 21 | 0 | 0 |
| SBC-2 | 00-26-ms1 | grid_s | 3 | 27 | 0 | 0 |
| SBC-3 | 00-26-ms1 | ver | 5 | 46 | 0 | 0 |
| SBC-4 | 00-26-ms1 | ver | 2 | 12 | 0 | 0 |
| SBC-5 | 00-26-ms1 | ver | 5 | 34 | 0 | 0 |
| SBC-6 | 00-26-ms1 | ver | 6 | 43 | 0 | 0 |
| SDI-1 | 00-26-ms1 | general | 8 | 26 | 0 | 0 |
| SDI-2 | 00-26-ms1 | grid_m | 3 | 29 | 0 | 0 |
| SDI-3 | 00-26-ms1 | ver | 4 | 45 | 0 | 0 |
| SDI-4 | 00-26-ms1 | ver | 2 | 12 | 0 | 0 |
| SDI-5 | 00-26-ms1 | grid_s | 1 | 17 | 0 | 0 |

## SDI-2: detectores de humo

La fila 24 corresponde a los controles mensuales I24:T24 (ENE a DIC). Se verificaron las 36 combinaciones de doce meses por tres estados (✓, O, X) con HTML y JavaScript reales, API simulada y navegador móvil aislado de 390 × 844. La selección y el payload de guardado se registraron en todos los casos; no se registraron errores JavaScript. El toque sobre el selector no quedó bloqueado por una superposición.

Al simular una carga emitida, los 348 selectores quedan deshabilitados por la lógica actual de solo lectura. No existe todavía desbloqueo con motivo y nueva revisión pública. En un borrador nuevo no se reprodujo un bloqueo particular de detectores de humo. Esto no identifica por sí solo la causa de una sesión anterior del usuario.

Evidencias: `sdi2_navegador.json`, `SDI-2_detectores_borrador.png` y `validacion_actual.json`. La prueba aislada llegó a las aserciones y guardó evidencia; no se presenta como ejecución integral con salida 0: un cierre anterior del arnés falló y la repetición sufrió problemas de recursos. No es una validación física de Android o iPhone, ni una prueba del service worker o de sincronización contra producción.

## Diferencias funcionales con v1.1

- La validación actual acepta O sin observación y un resultado sin valor medido. El encargo exige observación para O y medición cuando corresponda, salvo NA. Hay que implementar y probar esas reglas antes de dar v1.1 por habilitada.
- Las grillas mensuales y semanales ofrecen hoy ✓, O, X y NA. El nuevo encargo solicita tres estados en esas grillas. Debe introducirse como definición versionada, preservando datos anteriores; cualquier contradicción normativa con la leyenda del kit debe resolverla Martín.
- Cada carga actual contiene una matriz completa. No existen una visita por período y su PDF acumulado anual/mensual, selección de bloques por frecuencia ni continuidad selectiva de información general/equipamiento.
- Los datos dinámicos, las búsquedas, el catálogo persistente de responsables por DNI y el desbloqueo con motivo son trabajo pendiente. No se deben copiar observaciones, resultados, mediciones ni firmas de una visita a otra.
- El service worker vigente usa `readyproof-ui-v7`, no v3. El DNI ya acepta 8–15 dígitos ASCII; `00000000` es un ejemplo y no el único valor permitido.
- Ya existe envío real por Gmail HTTPS desde el servidor y evidencia previa en Enviados. La última prueba A4 registrada tiene un PDF de 119.597 bytes; su confirmación humana de recepción sigue pendiente en esa evidencia. No se repitió el envío.

## Clientes, establecimientos, sistemas y responsables

La consulta se hizo en transacción PostgreSQL de solo lectura. Existe un cliente ficticio, `[Ejemplo] Planta de prueba`, y cuatro sistemas SAA, SDI, SBC y SAL. `tecnico_readyproof` está activo con rol técnico y tiene ese cliente asignado. SAL es Extinción por Agentes Limpios.

La tabla clientes tiene UUID, nombre y marca de ejemplo; no tiene columna CUIT, contacto, correo, domicilio ni establecimientos. Por eso no puede informarse una validación de CUIT o de duplicados existentes: falta cargar y revisar ese dato sin inventarlo.

El modelo de sistema ya permite varios sistemas del mismo tipo por cliente. La API limita los tipos a las cuatro familias actuales y el alta a administradores. Faltan las quince familias, establecimientos, estado activo y ficha de información general/equipos. Ampliar permisos de alta a técnicos requiere definir el alcance antes de implementarlo.

Propuesta aditiva:

1. Conservar UUID como clave primaria de cliente. Incorporar CUIT normalizado de once dígitos, validación del dígito verificador y unicidad. Migrar en dos pasos: columna inicialmente opcional y reporte de faltantes/duplicados; luego revisión administrativa y restricción obligatoria. Nunca derivar un CUIT ficticio de otros datos.
2. Agregar establecimiento relacionado con cliente; sistema relacionado con establecimiento y cliente, tipo, designación y activo. Conservar sistemas y cargas históricos. Incorporar ficha general y equipos con versiones o auditoría de cambios.
3. Agregar responsable del cliente, único por cliente y DNI normalizado. Mantener la identidad y las firmas como instantáneas en cada emisión; el cambio de un responsable no debe alterar PDFs anteriores.
4. Mantener configuración piloto/real auditada y separada del transporte de correo. `MAIL_MODO_PRUEBA` no sustituye una política completa de datos reales. No activar REAL en este encargo. Datos de empresa mantenedora y certificado requieren confirmación de Jorge antes del uso real.

## Formatos y períodos: alternativa propuesta antes de implementar

Usar un importador determinista desde Excel que conserve código, edición, fila de origen, bloque, opciones, unidad y formato. Comparar su resultado con el catálogo; rechazar diferencias y publicar versiones nuevas sin alterar definiciones usadas por cargas históricas.

| Formato | Modelo propuesto para las nuevas versiones |
|---|---|
| General | Ficha versionada por sistema, campos tipados y opciones exactas del Excel; continuidad de información estática autorizada. |
| Semanal | Visita vinculada a sistema, planilla, año, mes y semana S1–S5; resultado por ítem. PDF acumulado mensual obtenido de visitas válidas. |
| Mensual | Visita vinculada a sistema, planilla, año y mes; PDF acumulado anual obtenido de visitas válidas. |
| Verificación | Visita con bloques/frecuencias seleccionados, fecha por bloque, resultado y medición con unidad cuando exista. |

La periodicidad complica el modelo actual de carga de matriz completa. Se propone agregar una entidad de visita/período para nuevas versiones y una vista de agregación de emisiones vigentes, sin reinterpretar ni transformar automáticamente las matrices históricas. Antes de implementarla hay que confirmar cómo se asignan los días a S1–S5; no se inventa una semana ISO ni una sexta columna. La agregación debe excluir anuladas y evitar contar dos revisiones del mismo registro.

## Numeración, revisiones y manuales

El encargo resuelve conservar los UUID y asignar número global, sin reinicio anual y sin huecos, únicamente al emitir. Los borradores y su sincronización no consumen número. Prevalece esta regla explícita de la sección 1.3 frente a la mención abreviada a número al sincronizar en los pasos de prueba.

Propuesta: contador de una fila bloqueada dentro de la misma transacción que confirma la emisión; no usar secuencia PostgreSQL para prometer ausencia de huecos. Agregar una entidad de emisión con número, revisión pública, PDF inmutable, hash, actor y fecha. La revisión actual de `Carga` sirve al control de concurrencia y no reemplaza una revisión documental. Desbloquear exige autorización del creador o administrador y motivo; una nueva emisión conserva número e incrementa revisión, guardando el PDF anterior. Anular debe conservar trazabilidad y número.

Hay cinco manuales de contenido ficticio en la BD. Los quince manuales v5 están en el paquete oficial. `Manual.codigo` es único globalmente: hay que diseñar una tabla de ediciones o ajustar la unicidad por código/versión antes de importar manuales reales, manteniendo intactas las asociaciones históricas. No sobrescribir el contenido ficticio para simular una edición nueva.

## Respaldo real y siguiente etapa

El servicio está activo y la BD está en `010_firmantes`. El timer local está activo, programado a las 02:00 UTC (23:00 de Argentina), con demora aleatoria prevista. El último resultado del servicio es satisfactorio. La carpeta `/var/backups/readyproof` tiene permisos 0700 y contiene seis dumps.

Última copia observada: `readyproof-20261028T002831Z.dump`, 4.795.724 bytes, 27/10/2026 21:28:34 de Argentina. Su índice es legible por `pg_restore`, pero el dato `alembic_version` del archivo es **009_multisistema**, anterior al esquema 010 en servicio. No constituye un respaldo actualizado de la entrega actual.

El trabajo de backup inspeccionado usa pg_dump, sin subida a Drive, cifrado de archivo, purga por retención ni aviso de fallo configurados. Los permisos locales restringen acceso, pero no equivalen a cifrado del respaldo. Existe una restauración antigua documentada en una BD separada; no demuestra la restauración de 010 con todos sus datos.

Los PDF canónicos, copias de envíos y firmas PNG están en PostgreSQL. Las carpetas temporales de PDF no son un archivo completo. La etapa siguiente debe producir un dump consistente y, si se requiere también una carpeta de PDF, exportarla desde el mismo respaldo consistente, con inventario y hashes. Luego cifrar, subir al Drive autorizado de readyproof, conservar 30 diarios y 12 mensuales, avisar por Gmail ante fallos y restaurar en una BD separada verificando esquema, cantidades, relaciones, firmas y hashes de PDFs. No migrar antes de esa prueba.

Jorge debe autorizar Google Drive con `readyproof.ar@gmail.com`; no se buscaron contraseñas ni tokens para suplir esa autorización. No se cambió el trabajo de respaldo durante esta etapa de diagnóstico.

## Verificaciones y límites

El cotejo completo confirma 79 archivos, cero diferencias con el catálogo, 16 definiciones servidor/local coincidentes y 389 ítems con controles. Se verificaron también las huellas del código respecto del manifiesto de la entrega anterior; el detalle queda en `verificacion_cierre.json`.

La última ejecución integral guardada tiene 232 pruebas aprobadas (`out/final_v1/pytest_completo.txt`). No se volvió a ejecutar pytest completo ni compileall en este diagnóstico de lectura y documentación, y no se atribuyen esos 232 resultados a una ejecución nueva. No se validaron un teléfono físico, una restauración actualizada, dominio público, HTTPS ni habilitación de datos reales en esta etapa.

## Inventario de las 79 planillas

«Habilitada» significa disponible actualmente; no certifica cumplimiento de todas las reglas nuevas de v1.1. Las 63 pendientes incluyen cinco SAA y 58 planillas de once sistemas aún no habilitados, no 63 pertenecientes solamente a esos once sistemas.

Formatos: general = información general; grid_s = semanal; grid_m = mensual; ver = lista de verificación. La columna unidades cuenta campos con unidad del original, no valores cargados.

| Código | Formato | Bloques | Ítems Excel/catálogo/inventario | Campos con unidad | Estado actual |
|---|---|---:|---:|---:|---|
| SAA-1 | general | 4 | 22 / 22 / 22 | 4 | Habilitada |
| SAA-2 | grid_s | 2 | 5 / 5 / 5 | 0 | Pendiente |
| SAA-3 | grid_m | 1 | 7 / 7 / 7 | 0 | Pendiente |
| SAA-4 | ver | 3 | 13 / 13 / 13 | 2 | Pendiente |
| SAA-5 | ver | 1 | 13 / 13 / 13 | 0 | Pendiente |
| SAA-6 | ver | 2 | 11 / 11 / 11 | 2 | Pendiente |
| SAL-1 | general | 4 | 18 / 18 / 18 | 3 | Habilitada |
| SAL-2 | grid_m | 1 | 5 / 5 / 5 | 0 | Habilitada |
| SAL-3 | ver | 3 | 25 / 25 / 25 | 2 | Habilitada |
| SAL-4 | ver | 1 | 7 / 7 / 7 | 3 | Habilitada |
| SAP-1 | general | 5 | 24 / 24 / 24 | 5 | Pendiente |
| SAP-2 | grid_s | 1 | 13 / 13 / 13 | 0 | Pendiente |
| SAP-3 | grid_m | 5 | 34 / 34 / 34 | 0 | Pendiente |
| SAP-4 | ver | 4 | 26 / 26 / 26 | 5 | Pendiente |
| SAP-5 | ver | 2 | 7 / 7 / 7 | 1 | Pendiente |
| SBC-1 | general | 5 | 21 / 21 / 21 | 7 | Habilitada |
| SBC-2 | grid_s | 3 | 27 / 27 / 27 | 0 | Habilitada |
| SBC-3 | ver | 5 | 46 / 46 / 46 | 30 | Habilitada |
| SBC-4 | ver | 2 | 12 / 12 / 12 | 0 | Habilitada |
| SBC-5 | ver | 5 | 34 / 34 / 34 | 3 | Habilitada |
| SBC-6 | ver | 6 | 43 / 43 / 43 | 23 | Habilitada |
| SCC-1 | general | 12 | 58 / 58 / 58 | 20 | Pendiente |
| SCC-2 | grid_m | 1 | 15 / 15 / 15 | 0 | Pendiente |
| SCC-3 | ver | 3 | 69 / 69 / 69 | 4 | Pendiente |
| SCC-4 | ver | 7 | 69 / 69 / 69 | 5 | Pendiente |
| SCC-5 | ver | 11 | 80 / 80 / 80 | 17 | Pendiente |
| SDC-1 | general | 5 | 18 / 18 / 18 | 8 | Pendiente |
| SDC-2 | ver | 2 | 15 / 15 / 15 | 8 | Pendiente |
| SDC-3 | ver | 3 | 21 / 21 / 21 | 3 | Pendiente |
| SDC-4 | ver | 12 | 60 / 60 / 60 | 48 | Pendiente |
| SDC-5 | ver | 1 | 7 / 7 / 7 | 1 | Pendiente |
| SDI-1 | general | 8 | 26 / 26 / 26 | 3 | Habilitada |
| SDI-2 | grid_m | 3 | 29 / 29 / 29 | 0 | Habilitada |
| SDI-3 | ver | 4 | 45 / 45 / 45 | 2 | Habilitada |
| SDI-4 | ver | 2 | 12 / 12 / 12 | 0 | Habilitada |
| SDI-5 | grid_s | 1 | 17 / 17 / 17 | 0 | Habilitada |
| SEP-1 | general | 5 | 18 / 18 / 18 | 6 | Pendiente |
| SEP-2 | grid_m | 1 | 9 / 9 / 9 | 0 | Pendiente |
| SEP-3 | ver | 4 | 18 / 18 / 18 | 5 | Pendiente |
| SGE-1 | general | 7 | 26 / 26 / 26 | 6 | Pendiente |
| SGE-2 | grid_s | 1 | 4 / 4 / 4 | 0 | Pendiente |
| SGE-3 | grid_m | 1 | 9 / 9 / 9 | 0 | Pendiente |
| SGE-4 | ver | 1 | 4 / 4 / 4 | 0 | Pendiente |
| SGE-5 | ver | 3 | 9 / 9 / 9 | 2 | Pendiente |
| SGE-6 | ver | 1 | 9 / 9 / 9 | 5 | Pendiente |
| SGE-7 | ver | 3 | 3 / 3 / 3 | 0 | Pendiente |
| SHC-1 | general | 7 | 25 / 25 / 25 | 6 | Pendiente |
| SHC-2 | ver | 5 | 30 / 30 / 30 | 6 | Pendiente |
| SHC-3 | ver | 2 | 12 / 12 / 12 | 1 | Pendiente |
| SIM-1 | ver | 5 | 18 / 18 / 18 | 0 | Pendiente |
| SIM-2 | ver | 6 | 20 / 20 / 20 | 0 | Pendiente |
| SRA-1 | general | 9 | 37 / 37 / 37 | 9 | Pendiente |
| SRA-2 | grid_s | 2 | 10 / 10 / 10 | 0 | Pendiente |
| SRA-3 | grid_m | 2 | 11 / 11 / 11 | 0 | Pendiente |
| SRA-4 | ver | 4 | 16 / 16 / 16 | 6 | Pendiente |
| SRA-5 | ver | 1 | 5 / 5 / 5 | 1 | Pendiente |
| SRA-6 | ver | 7 | 26 / 26 / 26 | 7 | Pendiente |
| SRA-7 | ver | 2 | 6 / 6 / 6 | 3 | Pendiente |
| SRA-8 | ver | 2 | 4 / 4 / 4 | 1 | Pendiente |
| SRA-9 | ver | 3 | 9 / 9 / 9 | 0 | Pendiente |
| SRE-1 | general | 6 | 16 / 16 / 16 | 3 | Pendiente |
| SRE-2 | grid_s | 1 | 5 / 5 / 5 | 0 | Pendiente |
| SRE-3 | grid_m | 1 | 9 / 9 / 9 | 0 | Pendiente |
| SRE-4 | ver | 1 | 5 / 5 / 5 | 0 | Pendiente |
| SRE-5 | ver | 2 | 11 / 11 / 11 | 2 | Pendiente |
| SRE-6 | ver | 3 | 16 / 16 / 16 | 5 | Pendiente |
| SRE-7 | ver | 3 | 19 / 19 / 19 | 5 | Pendiente |
| SSA-1 | general | 4 | 17 / 17 / 17 | 3 | Pendiente |
| SSA-2 | grid_m | 1 | 9 / 9 / 9 | 0 | Pendiente |
| SSA-3 | ver | 3 | 13 / 13 / 13 | 0 | Pendiente |
| SSA-4 | ver | 3 | 17 / 17 / 17 | 0 | Pendiente |
| STM-1 | general | 8 | 29 / 29 / 29 | 10 | Pendiente |
| STM-2 | grid_s | 1 | 4 / 4 / 4 | 0 | Pendiente |
| STM-3 | grid_m | 1 | 8 / 8 / 8 | 0 | Pendiente |
| STM-4 | ver | 5 | 23 / 23 / 23 | 2 | Pendiente |
| STM-5 | ver | 2 | 10 / 10 / 10 | 3 | Pendiente |
| STM-6 | ver | 2 | 12 / 12 / 12 | 10 | Pendiente |
| STM-7 | ver | 4 | 11 / 11 / 11 | 0 | Pendiente |
| STM-8 | ver | 3 | 13 / 13 / 13 | 6 | Pendiente |
