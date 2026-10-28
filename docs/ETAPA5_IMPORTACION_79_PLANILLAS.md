# Etapa 5 — Catálogo completo de planillas

Fecha: 28/10/2026. Entorno privado de readyproof, en modo piloto y con datos `[Ejemplo]`.

Se habilitaron las 79 planillas del kit en 15 familias: SAA, SAL, SBC, SDI, SAP, SCC, SDC, SEP, SGE, SHC, SIM, SRA, SRE, SSA y STM. Se usan sus nombres oficiales; SAL corresponde a Agentes Limpios y SIM a Simbología de Seguridad contra Incendios.

## Importación y conservación

- Migración aditiva `014_habilitar_11_sistemas`, posterior a `013_desbloqueo_revision`.
- Resultado del importador: 16 `YA_EXISTE`, 63 `IMPORTADA`, cero diferencias con el catálogo; 1.539 ítems cotejados.
- Las nuevas definiciones usan versión `00-26-ms1`. Las versiones anteriores no se sobrescriben.
- La base activa tiene 88 filas de planillas, correspondientes a 79 códigos habilitados y sus versiones históricas; 15 tipos de sistema.
- Ensayo previo en una copia aislada de la base activa. Verificación de huellas de todos los registros anteriores antes y después de la migración: sin cambios.
- Los originales Excel y `fuente/` se conservan intactos. El generador del kit sigue siendo la fuente del formato.

## Siglas

Se examinan las primeras 20 filas. La prioridad es código interno `SG-PEM-IFI-XXX-N`, paréntesis `(XXX)` y nombre de archivo. La aceptación requiere coincidencia entre al menos dos de código interno, archivo y catálogo; los paréntesis contradictorios siempre rechazan el archivo. El reporte identifica fuentes y discrepancias.

Los 79 originales carecen de siglas entre paréntesis en esas filas. Jorge autorizó expresamente usar sus códigos internos: las 79 coinciden con archivo y catálogo. No se alteraron los Excel para agregar paréntesis.

## Uso y documentación

Seleccionar Cliente → Sistema → Planilla. El selector recarga el formulario correspondiente y conserva las opciones del kit, incluyendo ✓ / O / X / NA. Una O requiere observación; la medición obligatoria cuando hay unidad se limita a los formatos de verificación autorizados. No se reinterpretan frecuencias ni calendarios.

El correo de documentación enumera los 15 sistemas y las 79 planillas. Se conserva el botón de envío desde la aplicación y el transporte ya configurado. Las pruebas de esta etapa no enviaron correos reales ni modificaron credenciales.

## Pruebas y PDF

La suite reúne 525 casos únicos aprobados: 479 en Ubuntu y 46 en Windows. Es un resultado consolidado por plataforma, no una única invocación. Los reintentos y los resultados iniciales se conservan en los JUnit de `out/etapa5_planillas/`.

Hay tres recorridos por cada una de las 63 planillas nuevas: borrador, validación y emisión. Se comparan filas, encabezado, textos, páginas contra los Excel oficiales, A4 horizontal, logos, leyenda IRAM, firmas, metadatos, numeración e historial PDF. Esto cubre las 63 planillas; no implica una medición del 100 % de líneas de código.

Las 63 emisiones nuevas suman 97 páginas. Se renderizaron todas y se revisaron las nueve láminas de contacto. Se conserva la paginación del kit, incluyendo continuaciones con observaciones o firmas. No se comprimen las planillas extensas a una hoja. La revisión original sigue siendo 0 y su primera corrección 1.

Algunos datos ficticios de cabecera provocaban saltos adicionales por longitud: se acortaron solo los ejemplos de las 63 nuevas. También se corrigió la lista de archivos admitidos por la restauración para incluir los PDF históricos de `emisiones_carga`.

## Respaldo y restauración

Antes de aplicar se guardaron los archivos anteriores y un respaldo cifrado del esquema 013 en Drive. Después de aplicar se ejecutó el servicio de respaldo y se descargó y restauró el esquema 014 en una base separada. Se compararon 19 tablas, 130 binarios y 48 PDF exportados, sin diferencias. El timer permanece activo; la aplicación responde en el acceso privado.

La repetición adicional de los 189 recorridos sobre clones efímeros de la base restaurada terminó con 189 aprobados y código 0, en 373,36 segundos. Está documentada en `out/etapa5_planillas/pruebas_restauradas.json` y `restaurada.xml`. La copia restaurada original quedó sin cambios. No se ejecutan pruebas destructivas sobre producción ni sobre la copia restaurada que conserva la evidencia.

## Evidencia y reproducción

- Informe final: `out/etapa5_planillas/etapa5_planillas.json`.
- Importación aplicada y conservación: `aplicar.json`; ensayo: `ensayar.json`.
- Suite consolidada: `pruebas_consolidadas.json`, `linux.xml`, `windows.xml`, `local_restante.xml`, `reintento_y_formatos.xml`.
- Navegador: `out/multisistema/navegador/resultado.json` — 79 formularios, 15 sistemas, cero errores.
- PDF y revisión: `pdf_verificados/`, `revision_visual/indice.json` y `revision_visual/lamina-*.png`.
- Copia privada: `manifiesto_transferencia.json`; destino autorizado `/home/readyproof_revision_etapa5`, modo 0700. Se excluyeron `.env`, claves, tokens y bases de datos del paquete transferido.
- Respaldo y restauración: `verificar.json`.

Ejecutar localmente, con PostgreSQL, LibreOffice y las dependencias instaladas:

```powershell
.\.venv\Scripts\python.exe -m compileall -q app tests scripts migraciones
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
.\.venv\Scripts\python.exe scripts\importador_planillas.py --help
```

El importador admite el ZIP oficial sin modificarlo. `--solo-catalogo` permite cotejar sin acceder a la base. Antes de usar `--aplicar`, revisar el reporte y confirmar el entorno local correcto; nunca se ejecuta contra una base ajena a readyproof. Los controladores de servidor están destinados al despliegue privado autorizado de esta entrega y verifican hashes y estado previo.

## Pendientes fuera de este cierre

Continúa el modo piloto. Los manuales reales y las asociaciones de las 63 nuevas requieren cargar sus ediciones correctas; no se inventaron registros para simularlos. Permanecen los pendientes normativos con Martín, el calendario S1–S5 y el alcance ampliado de establecimientos, datos dinámicos, precargas y anulación. La etapa 6 y la transición a uso real requieren confirmación independiente.

En la revisión visual se detectó que el Excel oficial SCC-1 rotula algunas presiones en MPa, mientras el encargo general indica bar para SCC. Jorge confirmó conservar el kit literal: no se convierten valores ni se cambian unidades, y esta diferencia no bloquea el cierre de etapa 5 en modo piloto. El reporte registra `unidad_encontrada: MPa`, `unidad_esperada: bar` y `estado: REVISAR_CON_MARTIN`. Martín debe confirmar si es un error del kit o una unidad válida antes de etapa 6 y de habilitar uso real. Si corresponde corregir, Jorge indicó una migración 016 independiente; no se crea ni ejecuta en esta etapa. La decisión de conservar el original está resuelta; la decisión normativa continúa pendiente.
