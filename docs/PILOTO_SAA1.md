# Piloto SAA-1 de readyproof

La etapa 1 genera un Excel interno y lo convierte a PDF con LibreOffice Calc. El archivo que se entrega al cliente es únicamente el PDF. La revisión del piloto usa datos ficticios identificados con `[Ejemplo]`.

## Ejecución local

Desde la raíz, con las dependencias instaladas y LibreOffice disponible:

```powershell
.venv\Scripts\python.exe -m app.planillas.piloto --salida out/revision_saa1
```

Para producir únicamente el Excel de diagnóstico:

```powershell
.venv\Scripts\python.exe -m app.planillas.piloto --salida out/revision_excel --solo-excel
```

Los destinos existentes se rechazan para no sobrescribir una carga anterior. Las pruebas de aceptación requieren LibreOffice y las dependencias de desarrollo; si faltan, la verificación falla. `LIBREOFFICE_BIN` puede indicar la ruta local del ejecutable si no está en PATH ni en las ubicaciones habituales de Windows.

## Contrato del adaptador

`app.planillas.generador.generar_saa1(datos, destino)` recibe un diccionario con tres apartados opcionales:

- `cabecera`: claves `fecha`, `cliente`, `cuit`, `telefono`, `direccion`, `edificio`, `sector`, `empresa_mantenedora`, `numero_mantenedor`, `inspector` y `sistema_designacion`, correspondientes a los espacios del encabezado original.
- `bloques`: claves con el título literal de cada bloque de `planillas_data3.py`; cada valor es un diccionario que usa las etiquetas literales de sus campos. Las opciones deben pertenecer a la lista del kit. El adaptador conserva todas las opciones y marca solo la seleccionada.
- `observaciones`: hasta cuatro textos, uno por renglón del original.

Se permiten cargas parciales para borradores y ejemplos. La validación de obligatoriedad, fechas, unidades y reglas del flujo se implementa en la etapa 2. Los valores se guardan como texto, incluso cuando comienzan con `=`, evitando que una entrada se ejecute como fórmula. El piloto no incorpora firmas manuscritas; esa integración corresponde a la etapa 3.

La definición se obtiene del kit sin duplicar los campos. El formato permanece en `fuente/herramientas/build_planilla.py`; el adaptador solo completa valores en el XML del Excel para conservar logos y partes del encabezado. Se conservaron las alturas originales y se corrigieron únicamente el ancho de impresión a 6.2 y el centrado horizontal, con autorización de Jorge. El respaldo anterior se guarda en `bak/`.

## Verificación

`tests/referencias/SAA-1_v5.xlsx` procede de la planilla oficial de `SG-PEM-IFI_Planillas_v5.zip`. No contiene datos de clientes. Las pruebas verifican contenido, estilos, dimensiones, impresión, logos, rechazo de campos desconocidos, opciones inválidas y errores de conversión.

La comparación visual convierte la referencia y una planilla sin carga con el mismo LibreOffice. Luego compara todas sus páginas píxel por píxel y coteja la cantidad de páginas del piloto cargado, el código, la retención y las leyendas del pie. Se genera una imagen de la página 1 con la referencia a la izquierda y el piloto a la derecha.

La verificación se ejecuta con el `.venv` del proyecto: `requirements-dev.txt` incluye las dependencias de aplicación y fija `pypdfium2==5.14.0`. La prueba de pytest compara todos los píxeles de todas las páginas de la planilla en blanco con la referencia, convertidas en la misma ejecución con el mismo LibreOffice. Si falta pypdfium2, la colección de pruebas falla; no se omite el control. El script `scripts/verificar_pdf_saa1.py` solo regenera las imágenes y su resumen de archivos, y rechaza carpetas de salida existentes.

## Encabezado y conversión

LibreOffice 26.8.1.1 omite las imágenes VML de los encabezados al exportar estos Excel. El conversor repone los dos logos después de la exportación con pypdf y Pillow, usando los archivos de imagen y las medidas del encabezado original: no se redibujan ni se sustituyen por versiones externas. Las coordenadas proceden de los márgenes y anclas del Excel, y se conserva la paginación de Calc. Si una versión futura de LibreOffice ya produce imágenes, la conversión se detiene para evitar superponer logos sin revisión.

En la revisión local de esta etapa, tanto la referencia oficial convertida como el piloto tienen dos páginas. Las firmas y observaciones permanecen en la segunda, tal como ocurre con el Excel oficial. No se cambia la escala para forzarlos a una página.

Los archivos finales de revisión están en `out/etapa1/pdf_con_logos/`, y la comparación de la página 1 y los renderizados de ambas páginas están en `out/etapa1/revision_con_logos/`. Los PDF de diagnóstico sin logos en `out/etapa1/pdf/` no son entregables.


## Reproducción de la revisión con el entorno del proyecto

La única referencia oficial de aceptación es `tests/referencias/SAA-1_v5.xlsx`, convertida en el momento de la prueba. El archivo `referencias/SAA-1/SG-PEM-IFI-SAA-1_INFORMACION_GENERAL_SAA_referencia.pdf` es un diagnóstico sin logos generado con otra versión de LibreOffice; se conserva como antecedente y no se usa para aceptar.

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe -m pytest -q
```

Para crear nuevas imágenes sin sobrescribir la revisión aprobada, se convierten los tres Excel con el conversor del proyecto y se usa la siguiente orden desde la raíz. El directorio de salida debe ser nuevo:

```powershell
.venv\Scripts\python.exe scripts/verificar_pdf_saa1.py --referencia out/etapa1/pdf_reproducible/referencia.pdf --blanca out/etapa1/pdf_reproducible/blanca.pdf --piloto out/etapa1/pdf_reproducible/piloto.pdf --salida out/etapa1/revision_reproducible
```

Los PDF se regeneran de esta manera, usando un directorio de salida nuevo si ya existe:

```python
from pathlib import Path
from app.planillas.generador import generar_saa1
from app.planillas.pdf import convertir_pdf
from app.planillas.piloto import datos_ejemplo

salida = Path("out/etapa1/pdf_reproducible")
referencia = Path("tests/referencias/SAA-1_v5.xlsx")
blanca = generar_saa1({}, salida / "blanca.xlsx")
piloto = generar_saa1(datos_ejemplo(), salida / "piloto.xlsx")
convertir_pdf(referencia, salida / "referencia.pdf")
convertir_pdf(blanca, salida / "blanca.pdf")
convertir_pdf(piloto, salida / "piloto.pdf")
```

El resumen `out/etapa1/revision_reproducible/resultado.json` describe los archivos renderizados, la cantidad de páginas y los logos por página. La aprobación automática de igualdad pertenece a pytest, no al script de imágenes. Las copias inalteradas de los entregables aprobados están versionadas en `docs/aprobaciones/etapa1/`.

## Alcance de los datos ficticios y pendientes

Los campos numéricos y de opción del piloto no pueden llevar el prefijo `[Ejemplo]`: el valor `1` y la primera opción de cada lista son ficticios y no expresan una medición, un criterio normativo ni un resultado real. Los textos y las observaciones identifican la carga como ejemplo.

Las pruebas comparan el texto fijo completo del encabezado y del pie del PDF con la referencia. La fecha variable de V4 se verifica como dato cargado, sin exigir que coincida con una referencia en blanco. También se comprueba cada campo en la columna J de la fila de su etiqueta y las cuatro observaciones en A36:A39.

La leyenda «Planilla conforme a IRAM 3546:2011» se incorporó después de la confirmación de Martín comunicada por Jorge: pie centrado a 10 mm, Helvetica 8 pt, gris 50 %, todas las páginas, con ajuste proporcional de pie autorizado. La prueba ahora es normal, sin xfail. El uso real sigue sujeto a los otros controles pendientes; ver LEYENDA_IRAM_M1.md. Los valores de creador y productor se mantienen en readyproof hasta la decisión de Jorge.
