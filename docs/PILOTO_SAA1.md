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

Los destinos existentes se rechazan para no sobrescribir una carga anterior. Las pruebas de conversión real requieren LibreOffice; el resto de las pruebas corre sin él. `LIBREOFFICE_BIN` puede indicar la ruta local del ejecutable si no está en PATH ni en las ubicaciones habituales de Windows.

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

El script `scripts/verificar_pdf_saa1.py` requiere pypdf, pypdfium2 y Pillow; para esta revisión se usa el Python de herramientas incluido en Codex, sin agregarlos como dependencias de la aplicación. La inspección visual y la aprobación de Jorge completan la aceptación de la etapa.

## Encabezado y conversión

LibreOffice 26.8.1.1 omite las imágenes VML de los encabezados al exportar estos Excel. El conversor repone los dos logos después de la exportación con pypdf y Pillow, usando los archivos de imagen y las medidas del encabezado original: no se redibujan ni se sustituyen por versiones externas. Las coordenadas proceden de los márgenes y anclas del Excel, y se conserva la paginación de Calc. Si una versión futura de LibreOffice ya produce imágenes, la conversión se detiene para evitar superponer logos sin revisión.

En la revisión local de esta etapa, tanto la referencia oficial convertida como el piloto tienen dos páginas. Las firmas y observaciones permanecen en la segunda, tal como ocurre con el Excel oficial. No se cambia la escala para forzarlos a una página.

Los archivos finales de revisión están en `out/etapa1/pdf_con_logos/`, y la comparación de la página 1 y los renderizados de ambas páginas están en `out/etapa1/revision_con_logos/`. Los PDF de diagnóstico sin logos en `out/etapa1/pdf/` no son entregables.
