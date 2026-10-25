# Auditoría de la etapa 1 de readyproof: planilla piloto SAA-1

## Resumen

- **Etapa auditada:** 1, generación de la planilla piloto SAA-1 (encargo, sección 7).
- **Fecha:** 25/10/2026.
- **Proyecto:** `C:\Users\jorge\Readyproof`.
- **Resultado general:** **APTA CON OBSERVACIONES**.
- **Hallazgos:** 0 críticos, 4 mayores y 7 menores.

Se cumplen los criterios de aceptación de la etapa 1:

- el módulo genera el .xlsx con `build_planilla.py` y lo convierte a PDF con LibreOffice;
- el PDF piloto tiene la misma cantidad de páginas que la referencia;
- la planilla en blanco coincide con la referencia v5;
- Jorge aprobó el PDF por escrito, según el registro, y está la imagen comparativa de la página 1.

No hay secretos, copias de normas ni datos reales de clientes. Las observaciones mayores son cuatro: falta en el PDF la leyenda «Planilla conforme a IRAM 3546:2011»; se cambió el generador del kit sin constancia de aviso a Martín; la verificación píxel a píxel no se puede reproducir con el entorno del proyecto; y el proyecto no tiene historial de versiones.

---

## Hallazgos

### Mayores (corregir antes de la etapa 2)

**M1. Falta la leyenda «Planilla conforme a IRAM 3546:2011» en el PDF emitido**
- Archivos: `app/planillas/generador.py` (no la incorpora), `out/etapa1/pdf_con_logos/SAA-1_ejemplo.pdf` (no la contiene), `tests/test_generacion.py` (ninguna prueba la exige).
- Qué pasa: la sección 3.1 del encargo exige la leyenda en la pantalla de carga y en el PDF. El texto extraído del PDF aprobado no la tiene, y tampoco aparece en ninguna celda ni en el encabezado o el pie del Excel generado. El texto exacto está pendiente de Martín (`PREGUNTAS_ABIERTAS.md`, punto 2). Sin embargo, no quedó registrado que el PDF aprobado se emite sin la leyenda ni que eso bloquea emitir planillas a clientes.
- Qué hacer: registrar en `PREGUNTAS_ABIERTAS.md` que la leyenda falta en el PDF y que eso bloquea la emisión real. Definir con Martín el texto y dónde va en la hoja. Cuando esté confirmado, agregarla y sumar una prueba que verifique su presencia en el PDF.

**M2. Se modificó un archivo de `fuente/` sin constancia de aviso a Martín**
- Archivo: `fuente/herramientas/build_planilla.py`, línea 13 (`PRINT_COLW = 6.2`) y líneas 155 y 156 (ancho de columna y centrado horizontal).
- Qué pasa: es el único archivo de `fuente/` modificado. Su fecha de modificación es posterior a la copia del kit, y la de todos los demás archivos coincide con la copia original. El cambio está autorizado por Jorge, registrado y respaldado en `bak/build_planilla_antes_ajuste_v5.py`. Además coincide con lo que hace `fix_impresion.py` según `fuente/KIT_AGENTS.md`. Pero:
  - la regla de oro (sección 6) y la sección 11 del encargo piden avisar a Martín de todo cambio de formato en el generador, y no hay constancia de ese aviso;
  - el cambio afecta a las 79 planillas de la serie, no solo a SAA-1, y solo se verificó contra SAA-1.
- Qué hacer: registrar el aviso a Martín, o dejarlo como pregunta abierta. Anotar que el cambio alcanza a toda la serie y que las demás planillas se cotejarán en la etapa 6.

**M3. La verificación píxel a píxel no se puede reproducir con el entorno del proyecto**
- Archivo: `scripts/verificar_pdf_saa1.py`, línea 8 (`import pypdfium2`); `docs/PILOTO_SAA1.md`, línea 39.
- Qué pasa: `pypdfium2` no está en `requirements.txt` ni instalado en `.venv`. La documentación dice que el script se ejecutó con un intérprete externo al proyecto. La prueba de que «el encabezado y el pie son iguales» en el PDF, y la imagen comparativa entregada, dependen de ese script. Con el entorno del proyecto no se pueden volver a generar `out/etapa1/revision_con_logos/resultado.json` ni la imagen.
- Qué hacer: declarar las dependencias de verificación en un archivo de dependencias de desarrollo con versiones exactas, o pasar la comparación a `pytest` con dependencias declaradas. Documentar cómo se regenera la imagen comparativa.

**M4. El proyecto no tiene historial de versiones**
- Archivos: `.git/refs/heads/` (vacío) y `.gitignore`, línea 7 (`out/`).
- Qué pasa: el repositorio git no tiene ramas ni commits. Solo hay referencias internas de la herramienta de desarrollo. Por eso `git log` y `git diff` no muestran nada, y no hay forma de saber con certeza qué cambió en la etapa 1 ni de volver atrás. Además, `.gitignore` excluye `out/`, que es donde están el PDF aprobado y la imagen comparativa, es decir, los entregables del criterio de aceptación.
- Qué hacer: hacer un commit local por etapa: uno para la etapa 0 y uno para el cierre de la etapa 1. Es un commit local, sin publicar ni crear un repositorio remoto. Guardar los entregables aprobados en una carpeta versionada, por ejemplo `docs/aprobaciones/etapa1/`.

### Menores

**m1. Rastros de herramientas de generación automática en documentos entregables**
- Archivos: `docs/PILOTO_SAA1.md`, línea 39 («Python de herramientas incluido en Codex»); `REGISTRO_DE_CAMBIOS.md`, líneas 6, 15, 19, 20 y 196 (menciones a Codex y al sandbox).
- Qué pasa: la sección 3.3 del encargo pide que no haya rastros de generación automática en los archivos entregados. Los dos son entregables según la sección 10.
- Qué hacer: reescribir esas líneas en términos neutros, por ejemplo «entorno de desarrollo» o «herramienta de verificación local».

**m2. Las pruebas no verifican la ubicación de cada dato ni el encabezado y el pie del PDF**
- Archivo: `tests/test_generacion.py`, líneas 58 a 60 y 143 a 162.
- Qué pasa: `test_carga_conserva_logos_textos_y_opciones` busca los valores cargados en cualquier celda de la hoja, no en la fila del campo correspondiente. Si dos campos se intercambiaran dentro de un bloque, la prueba no lo detectaría. `test_conversion_real_con_libreoffice` comprueba la cantidad de páginas, los logos y cuatro rótulos, pero no compara el encabezado y el pie completos contra la referencia. Las pruebas sí detectan problemas reales: al alterar a propósito el desplazamiento de filas y el ancho de columna en una copia, fallaron.
- Qué hacer: verificar que cada valor quede en la celda de su etiqueta y comparar el texto del encabezado y del pie del PDF contra la referencia.

**m3. Los metadatos del PDF están fijos para SAA-1 y no siguen la regla de la serie**
- Archivo: `app/planillas/encabezado_pdf.py`, línea 90.
- Qué pasa: el título está escrito como `SG-PEM-IFI-SAA-1` para cualquier planilla. Creador y productor dicen «readyproof», mientras que `fuente/KIT_AGENTS.md` (sección de identidad) indica «autor y productor BRAFEMAR».
- Qué hacer: tomar el título del código de la planilla y confirmar con Jorge qué valores de creador y productor corresponden.

**m4. Datos de ejemplo sin el prefijo `[Ejemplo]`**
- Archivo: `app/planillas/piloto.py`, líneas 30 a 33.
- Qué pasa: los campos con unidad se cargan con `1` y los de opción con la primera opción. En el PDF de ejemplo aparecen sin prefijo, por ejemplo «1 m³». Es inevitable en campos numéricos y de opción, pero no está documentado como excepción.
- Qué hacer: anotar la excepción en `docs/PILOTO_SAA1.md`, o usar valores evidentemente ficticios.

**m5. Falta `fix_impresion.py`, que citan el encargo y el kit**
- Archivos: `AGENTS.md`, sección 6, y `fuente/KIT_AGENTS.md`, línea 206; no existe en `fuente/herramientas/`.
- Qué pasa: el encargo dice que ese ajuste ya está integrado en `build_planilla.py`, pero no lo estaba, y por eso hubo que modificar el generador (M2). La falta del archivo no se registró en `PREGUNTAS_ABIERTAS.md`.
- Qué hacer: registrarla y confirmar si la copia del kit está completa.

**m6. Hay dos referencias distintas de SAA-1**
- Archivo: `referencias/SAA-1/SG-PEM-IFI-SAA-1_INFORMACION_GENERAL_SAA_referencia.pdf`.
- Qué pasa: este PDF se generó con LibreOffice 24.2 y no tiene logos (0 imágenes por página). Las pruebas no lo usan: convierten en el momento `tests/referencias/SAA-1_v5.xlsx` y reponen los logos. No queda claro cuál es la referencia oficial.
- Qué hacer: dejar una sola referencia y documentar su origen y cómo se obtuvo.

**m7. La aplicación importa `lxml` directamente pero no lo declara**
- Archivos: `app/planillas/generador.py`, línea 10, y `app/planillas/encabezado_pdf.py`, línea 8.
- Qué pasa: `lxml` llega como dependencia de python-docx y figura en `requirements.lock.txt`, pero no en `requirements.txt`. Si en el futuro se quitara python-docx, el generador dejaría de funcionar.
- Qué hacer: agregar `lxml` con versión exacta a `requirements.txt`. Ya está justificado en el registro.

---

## Criterios de la etapa 1 (sección 7 del encargo)

| Criterio | Estado | Evidencia |
|---|---|---|
| Módulo que recibe un diccionario de SAA-1 y genera el .xlsx con `build_planilla.py` | Cumple | `generar_saa1()` llama a `build()` del kit. Los datos del piloto quedan en las filas de sus etiquetas (filas 10 a 34) y las observaciones en las filas 36 y 37. |
| Conversión del .xlsx a PDF con LibreOffice | Cumple | `convertir_pdf()` usa `soffice --headless --convert-to pdf` con un perfil aislado. |
| Prueba: el PDF con datos ficticios tiene la misma cantidad de páginas que la referencia | Cumple | `test_conversion_real_con_libreoffice`: 2 páginas contra 2. La referencia es el Excel oficial v5 convertido, en lugar del PDF de `out_v4`; el cambio está autorizado por Jorge y registrado. |
| Prueba: encabezado y pie iguales | Cumple con observación | A nivel Excel, la comparación celda por celda con la referencia es completa. A nivel PDF, la prueba verifica rótulos, y la igualdad píxel a píxel solo la verifica el script no reproducible (M3 y m2). |
| El PDF se revisa visualmente y se aprueba | Cumple | `REGISTRO_DE_CAMBIOS.md`, entrada «Aprobación y cierre de la etapa 1». También revisé la imagen comparativa: mismas filas, logos y encabezado. |
| Se entrega la imagen comparativa de la página 1 | Cumple | `out/etapa1/revision_con_logos/comparacion_pagina_1.png`. Está en una carpeta que git no versiona (M4). |

## Reglas del encargo (sección 3)

| Regla | Estado |
|---|---|
| No se cambiaron filas ni opciones | Cumple. La planilla en blanco y la referencia v5 no tienen diferencias de valores (44 filas, 25 columnas). Las opciones se conservan todas y solo se marca la elegida. Una opción o un campo inexistente se rechaza. |
| «T.C. 3 AÑOS» en el encabezado | Cumple. Está en la celda T3 y en el texto del PDF. |
| Leyenda «Planilla conforme a IRAM 3546:2011» | No cumple (M1). |
| Sin rastros de generación automática | Parcial (m1). El código no tiene ninguno; dos documentos sí. |
| Nombre «readyproof» en los textos visibles | Cumple. No queda ninguna mención a «twinloop». |
| Sin copias de normas | Cumple. Solo se usan los textos de la planilla de la serie. |
| Datos ficticios con `[Ejemplo]` | Cumple, con la salvedad m4. |
| Credenciales fuera del código | Cumple. `.env.ejemplo` tiene solo valores de ejemplo o vacíos, y `.env` no existe y está excluido en `.gitignore`. |

## Documentación y registro

- `REGISTRO_DE_CAMBIOS.md`: tiene entradas fechadas de la etapa 1 (inicio, ejecución, verificación, entrega y aprobación), con lo hecho y lo pendiente. Las dependencias nuevas, pypdf y Pillow, están justificadas. Las fechas de modificación de los archivos son coherentes con la afirmación de que el código no cambió después de la última validación.
- `PREGUNTAS_ABIERTAS.md`: existe y está actualizado. Faltan la ausencia de la leyenda en el PDF (M1), el aviso a Martín (M2) y la falta de `fix_impresion.py` (m5).

---

## Controles ejecutados

| Control | Resultado |
|---|---|
| `git log` y `git diff` | No se pudieron usar: el repositorio no tiene ramas ni commits (M4). |
| Comparación de `fuente/` | Por fechas de modificación, solo cambió `build_planilla.py`. Comparé ese archivo con `bak/build_planilla_antes_ajuste_v5.py` y la diferencia es de 3 líneas (13, 155 y 156). |
| `pytest -q` (copia aislada, pytest 9.1.1, LibreOffice 24.2) | `20 passed in 5.23s`, código 0. Ninguna prueba omitida: la de conversión real con LibreOffice se ejecutó. |
| `python -m compileall app` | Código 0, sin errores. |
| Mutación: fila inicial 9 → 10 en el generador | `1 failed, 19 passed`: la prueba lo detecta. |
| Mutación: ancho de impresión 6.2 → 5.3 | `1 failed, 19 passed`: la prueba lo detecta. |
| Generación de la planilla en blanco y del piloto, comparadas con `tests/referencias/SAA-1_v5.xlsx` | Ninguna diferencia de valores en la planilla en blanco. En el piloto, los datos quedan en la fila de su etiqueta. |
| Texto y metadatos del PDF aprobado | 2 páginas, 2 logos por página. Contiene «T.C. 3 AÑOS» y no contiene «IRAM 3546:2011». Título fijo SAA-1; creador y productor «readyproof». |
| Revisión visual de `comparacion_pagina_1.png` | Mismas filas, mismo encabezado con logos y datos ficticios legibles. |
| Búsqueda de secretos (contraseña, token, clave, URL con credenciales, clave privada) | Ninguno en el código, las pruebas, la documentación ni la configuración. |
| Búsqueda de rastros de herramientas automáticas | Dos documentos con menciones (m1). |
| Búsqueda de «twinloop» | Sin resultados. |
| Búsqueda de nombres de clientes, marcas o modelos | Ninguno en el código, las pruebas ni los datos de ejemplo. «BRAFEMAR» aparece solo como empresa mantenedora, que viene de la planilla de la serie. |

## Limitaciones

- **Entorno de prueba distinto del proyecto:** no pude ejecutar `pytest` en el `.venv` de Windows porque el acceso a la terminal de la computadora es solo de lectura y clic. Ejecuté las pruebas en una copia aislada con pytest 9.1.1, pypdf 6.17, Pillow 12.3 y LibreOffice 24.2, no con las versiones fijadas del proyecto (pytest 8.3.4, pypdf 6.21.2, Pillow 13.0.0, LibreOffice 26.8.1.1). El resultado coincide con el registrado: 20 pruebas aprobadas.
- **Sin historial git:** no se puede reconstruir qué cambió en la etapa. Usé las fechas de modificación y el respaldo en `bak/`.
- **Sin el kit original:** no pude verificar el SHA256 de `fuente/` contra el kit. La conclusión se basa en las fechas de modificación.
- **Alcance de la revisión:** no revisé los archivos ajenos a la etapa que hay en la raíz (`auditoria_SCC.md`, `Cambios_manuales_Martin.md`, `Cotejo_y_dudas.md`, `PROMPT_Manuales_SG-PEM-IFI.md`), ni `fuente/contenidos` excepto SAA, ni `fuente/modelos` excepto `SDI-1.xlsx`.
- **Acceso externo:** no hubo acceso a internet, DigitalOcean, cPanel ni GitHub, y la etapa 1 no lo requiere.
