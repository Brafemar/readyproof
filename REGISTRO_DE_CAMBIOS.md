# Registro de cambios: readyproof

## 2026-10-25 · Etapa 0 · Preparación

- Carpeta `fuente/` verificada. Contiene directamente `KIT_AGENTS.md`, `herramientas/`, `contenidos/`, `modelos/` y `simbolos_png/`. Dentro de `herramientas/` están `build_planilla.py`, `build_informe.py`, `run_planillas.py`, `planillas_data.py`, `planillas_data2.py`, `planillas_data3.py` y `planillas_data4.py`. `modelos/` contiene `SDI-1.xlsx`. No hay carpetas `fuente` anidadas.
- Este registro se creó mediante una intervención externa al entorno de desarrollo, porque la creación original falló. El registro continúa desde aquí.
- Entorno virtual en `C:\Users\jorge\venv_readyproof` (fuera de Documents: Windows bloquea la creación de carpetas nuevas dentro de `Readyproof`).
- Dependencias de `requirements.txt` instaladas con Python 3.13: OK.
- `pytest -q -p no:cacheprovider`: 1 passed. Sintaxis de `app/*.py`: OK.
- Pendiente de la etapa 0: `.env.ejemplo` (no creado todavía). Estructura de carpetas de la sección 5 del encargo y `docs/INSTALACION.md`: revisar en la etapa 1.
- Nota: `.pytest_cache` y `__pycache__` no pudieron crearse dentro de `Readyproof`. Revisar Acceso controlado a carpetas de Windows.

## 2026-10-25 — Recuperación del acceso de escritura

- Diagnóstico: Windows Defender, Acceso controlado a carpetas, bloquea al preparador del entorno de pruebas aislado y a Python dentro de Documentos (eventos 1123; SetSecurityInfo failed: 5).
- Con autorización de Jorge, se intentó trasladar Readyproof a C:\Users\jorge\Readyproof. Move-Item falló: The process cannot access the file because it is being used by another process.
- Se copió el proyecto a C:\Users\jorge\Readyproof sin sobrescribir archivos. Se verificaron 439 archivos con SHA256 idéntico. El original en Documentos se conserva; continuar únicamente en la nueva copia.
- En la nueva carpeta se creó _prueba_escritura.txt con contenido exacto prueba, se leyó y se eliminó correctamente.
- No se modificaron Defender, las excepciones de seguridad ni la configuración del entorno de pruebas aislado. No se accedió a internet.
- Pendiente: abrir la nueva carpeta como proyecto en el entorno de desarrollo para que el entorno de pruebas aislado use esa ubicación y continuar la etapa 0 desde el registro.
- Creado y leído .env.ejemplo en la nueva raíz con el contenido de ejemplo indicado por Jorge, sin credenciales reales.

## 2026-10-25 — Continuación y cierre de la etapa 0

- Paso 0. Comandos Set-Content, Get-Content y Remove-Item sobre _prueba_escritura.txt en la nueva raíz: creación, lectura exacta de prueba y eliminación correctas. Se continúa en C:\Users\jorge\Readyproof mediante comandos autorizados; el chat todavía conserva la ruta anterior para el entorno de pruebas aislado.
- Lectura del encargo AGENTS.md, PASOS_SERVICIO_FINAL_readyproof.md y ambos registros: completada. No se sobrescriben archivos existentes ni se modifica fuente/.
- Paso 1. Test-Path AGENTS.md: presente, conservado.
- Paso 1. Test-Path README.md: presente, conservado.
- Paso 1. Test-Path requirements.txt: presente, conservado.
- Paso 1. Test-Path .gitignore: presente, conservado.
- Paso 1. Test-Path app/__init__.py: presente, conservado.
- Paso 1. Test-Path tests/test_base.py: presente, conservado.
- Paso 1. Test-Path migraciones/.gitkeep: presente, conservado.
- Paso 1. Test-Path docs/INSTALACION.md: presente, conservado.
- Paso 2. Test-Path .env.ejemplo: presente; se conserva el archivo de ejemplo creado y verificado en la recuperación, sin registrar sus valores.
- Paso 3. New-Item -ItemType Directory app/auth: creado.
- Paso 3. New-Item -ItemType Directory app/models: creado.
- Paso 3. New-Item -ItemType Directory app/planillas/definiciones: creado.
- Paso 3. New-Item -ItemType Directory app/rutas: creado.
- Paso 3. New-Item -ItemType Directory app/static: creado.
- Paso 3. New-Item -ItemType Directory app/templates: creado.
- Paso 3. New-Item -ItemType File app/config.py: creado vacío, sin funcionalidad.
- Paso 3. New-Item -ItemType File app/correo.py: creado vacío, sin funcionalidad.
- Paso 3. New-Item -ItemType File app/auth/__init__.py: creado vacío, sin funcionalidad.
- Paso 3. New-Item -ItemType File app/models/__init__.py: creado vacío, sin funcionalidad.
- Paso 3. New-Item -ItemType File app/rutas/__init__.py: creado vacío, sin funcionalidad.
- Paso 3. New-Item -ItemType File app/planillas/__init__.py: creado vacío, sin funcionalidad.
- Paso 3. New-Item -ItemType File app/planillas/definiciones/__init__.py: creado vacío, sin funcionalidad.
- Paso 3. New-Item -ItemType File app/planillas/generador.py: creado vacío, sin funcionalidad.
- Paso 3. New-Item -ItemType File app/planillas/pdf.py: creado vacío, sin funcionalidad.
- Paso 3. New-Item -ItemType File app/static/.gitkeep: creado vacío, sin funcionalidad.
- Paso 3. New-Item -ItemType File app/templates/.gitkeep: creado vacío, sin funcionalidad.
- Paso 3. New-Item -ItemType File tests/test_generacion.py: creado vacío, sin funcionalidad.
- Paso 3. New-Item -ItemType File tests/test_api.py: creado vacío, sin funcionalidad.
- Paso 3. New-Item -ItemType File tests/test_flujo.py: creado vacío, sin funcionalidad.
- Paso 4. python -m venv .venv: código de salida 0.
- Paso 4. Dependencias existentes conservadas: Flask (backend), SQLAlchemy y psycopg (PostgreSQL), openpyxl (generador del kit), python-docx (informes del kit), bcrypt (contraseñas), python-dotenv (configuración) y pytest (pruebas). Se respetan las versiones exactas de requirements.txt, sin agregar dependencias directas.
- Paso 4. Se autoriza red únicamente para el siguiente proceso pip, con índice PyPI, sin caché y sin comprobar actualizaciones de pip. No se modifican ajustes de red, firewall ni Defender.

Comando: .venv\Scripts\python.exe -m pip --isolated install --index-url https://pypi.org/simple --disable-pip-version-check --no-cache-dir -r requirements.txt
Código de salida: 0

Collecting Flask==3.0.3 (from -r requirements.txt (line 1))
  Downloading flask-3.0.3-py3-none-any.whl.metadata (3.2 kB)
Collecting SQLAlchemy==2.0.36 (from -r requirements.txt (line 2))
  Downloading SQLAlchemy-2.0.36-cp313-cp313-win_amd64.whl.metadata (9.9 kB)
Collecting psycopg==3.2.3 (from psycopg[binary]==3.2.3->-r requirements.txt (line 3))
  Downloading psycopg-3.2.3-py3-none-any.whl.metadata (4.3 kB)
Collecting openpyxl==3.1.5 (from -r requirements.txt (line 4))
  Downloading openpyxl-3.1.5-py2.py3-none-any.whl.metadata (2.5 kB)
Collecting python-docx==1.1.2 (from -r requirements.txt (line 5))
  Downloading python_docx-1.1.2-py3-none-any.whl.metadata (2.0 kB)
Collecting bcrypt==4.2.1 (from -r requirements.txt (line 6))
  Downloading bcrypt-4.2.1-cp39-abi3-win_amd64.whl.metadata (10 kB)
Collecting python-dotenv==1.0.1 (from -r requirements.txt (line 7))
  Downloading python_dotenv-1.0.1-py3-none-any.whl.metadata (23 kB)
Collecting pytest==8.3.4 (from -r requirements.txt (line 8))
  Downloading pytest-8.3.4-py3-none-any.whl.metadata (7.5 kB)
Collecting Werkzeug>=3.0.0 (from Flask==3.0.3->-r requirements.txt (line 1))
  Downloading werkzeug-3.1.9-py3-none-any.whl.metadata (4.1 kB)
Collecting Jinja2>=3.1.2 (from Flask==3.0.3->-r requirements.txt (line 1))
  Downloading jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)
Collecting itsdangerous>=2.1.2 (from Flask==3.0.3->-r requirements.txt (line 1))
  Downloading itsdangerous-2.2.0-py3-none-any.whl.metadata (1.9 kB)
Collecting click>=8.1.3 (from Flask==3.0.3->-r requirements.txt (line 1))
  Downloading click-8.5.0-py3-none-any.whl.metadata (2.6 kB)
Collecting blinker>=1.6.2 (from Flask==3.0.3->-r requirements.txt (line 1))
  Downloading blinker-1.9.0-py3-none-any.whl.metadata (1.6 kB)
Collecting typing-extensions>=4.6.0 (from SQLAlchemy==2.0.36->-r requirements.txt (line 2))
  Downloading typing_extensions-4.16.0-py3-none-any.whl.metadata (3.3 kB)
Collecting tzdata (from psycopg==3.2.3->psycopg[binary]==3.2.3->-r requirements.txt (line 3))
  Downloading tzdata-2026.5-py2.py3-none-any.whl.metadata (1.4 kB)
Collecting et-xmlfile (from openpyxl==3.1.5->-r requirements.txt (line 4))
  Downloading et_xmlfile-2.0.0-py3-none-any.whl.metadata (2.7 kB)
Collecting lxml>=3.1.0 (from python-docx==1.1.2->-r requirements.txt (line 5))
  Downloading lxml-6.1.3-cp313-cp313-win_amd64.whl.metadata (3.4 kB)
Collecting colorama (from pytest==8.3.4->-r requirements.txt (line 8))
  Downloading colorama-0.4.6-py2.py3-none-any.whl.metadata (17 kB)
Collecting iniconfig (from pytest==8.3.4->-r requirements.txt (line 8))
  Downloading iniconfig-2.3.1-py3-none-any.whl.metadata (2.8 kB)
Collecting packaging (from pytest==8.3.4->-r requirements.txt (line 8))
  Downloading packaging-26.3-py3-none-any.whl.metadata (3.5 kB)
Collecting pluggy<2,>=1.5 (from pytest==8.3.4->-r requirements.txt (line 8))
  Downloading pluggy-1.7.0-py3-none-any.whl.metadata (5.0 kB)
Collecting psycopg-binary==3.2.3 (from psycopg[binary]==3.2.3->-r requirements.txt (line 3))
  Downloading psycopg_binary-3.2.3-cp313-cp313-win_amd64.whl.metadata (2.9 kB)
Collecting MarkupSafe>=2.0 (from Jinja2>=3.1.2->Flask==3.0.3->-r requirements.txt (line 1))
  Downloading markupsafe-3.0.4-cp313-cp313-win_amd64.whl.metadata (2.8 kB)
Downloading flask-3.0.3-py3-none-any.whl (101 kB)
Downloading SQLAlchemy-2.0.36-cp313-cp313-win_amd64.whl (2.1 MB)
   ---------------------------------------- 2.1/2.1 MB 26.4 MB/s eta 0:00:00
Downloading psycopg-3.2.3-py3-none-any.whl (197 kB)
Downloading openpyxl-3.1.5-py2.py3-none-any.whl (250 kB)
Downloading python_docx-1.1.2-py3-none-any.whl (244 kB)
Downloading bcrypt-4.2.1-cp39-abi3-win_amd64.whl (153 kB)
Downloading python_dotenv-1.0.1-py3-none-any.whl (19 kB)
Downloading pytest-8.3.4-py3-none-any.whl (343 kB)
Downloading psycopg_binary-3.2.3-cp313-cp313-win_amd64.whl (2.9 MB)
   ---------------------------------------- 2.9/2.9 MB 27.5 MB/s eta 0:00:00
Downloading pluggy-1.7.0-py3-none-any.whl (27 kB)
Downloading blinker-1.9.0-py3-none-any.whl (8.5 kB)
Downloading click-8.5.0-py3-none-any.whl (125 kB)
Downloading itsdangerous-2.2.0-py3-none-any.whl (16 kB)
Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
Downloading lxml-6.1.3-cp313-cp313-win_amd64.whl (4.0 MB)
   ---------------------------------------- 4.0/4.0 MB 25.2 MB/s eta 0:00:00
Downloading markupsafe-3.0.4-cp313-cp313-win_amd64.whl (14 kB)
Downloading typing_extensions-4.16.0-py3-none-any.whl (45 kB)
Downloading werkzeug-3.1.9-py3-none-any.whl (228 kB)
Downloading colorama-0.4.6-py2.py3-none-any.whl (25 kB)
Downloading et_xmlfile-2.0.0-py3-none-any.whl (18 kB)
Downloading iniconfig-2.3.1-py3-none-any.whl (7.6 kB)
Downloading packaging-26.3-py3-none-any.whl (129 kB)
Downloading tzdata-2026.5-py2.py3-none-any.whl (347 kB)
Installing collected packages: tzdata, typing-extensions, python-dotenv, psycopg-binary, pluggy, packaging, MarkupSafe, lxml, itsdangerous, iniconfig, et-xmlfile, colorama, click, blinker, bcrypt, Werkzeug, SQLAlchemy, python-docx, pytest, psycopg, openpyxl, Jinja2, Flask

Successfully installed Flask-3.0.3 Jinja2-3.1.6 MarkupSafe-3.0.4 SQLAlchemy-2.0.36 Werkzeug-3.1.9 bcrypt-4.2.1 blinker-1.9.0 click-8.5.0 colorama-0.4.6 et-xmlfile-2.0.0 iniconfig-2.3.1 itsdangerous-2.2.0 lxml-6.1.3 openpyxl-3.1.5 packaging-26.3 pluggy-1.7.0 psycopg-3.2.3 psycopg-binary-3.2.3 pytest-8.3.4 python-docx-1.1.2 python-dotenv-1.0.1 typing-extensions-4.16.0 tzdata-2026.5
- Paso 4. Finalizado el proceso pip con acceso a red. Los pasos restantes se ejecutan sin operaciones de red; no se cambió ninguna configuración persistente de conectividad.
- Paso 5. Creado pytest.ini: testpaths=tests limita la recolección a las pruebas del proyecto y pythonpath=. permite importar app al ejecutar pytest -q desde su lanzador del entorno virtual. No se modifica la prueba existente.

### Paso 5 — pytest -q

Fecha: 2026-10-25. Entorno: .venv local. Sin operaciones de red.

Salida exacta:
```text
.                                                                        [100%]
1 passed in 0.03s
```

Código de salida: 0.

### Paso 5 — python -m compileall app

Fecha: 2026-10-25. Entorno: .venv local. Sin operaciones de red.

Salida exacta:
```text
Listing 'app'...
Listing 'app\\auth'...
Compiling 'app\\auth\\__init__.py'...
Compiling 'app\\config.py'...
Compiling 'app\\correo.py'...
Listing 'app\\models'...
Compiling 'app\\models\\__init__.py'...
Listing 'app\\planillas'...
Compiling 'app\\planillas\\__init__.py'...
Listing 'app\\planillas\\definiciones'...
Compiling 'app\\planillas\\definiciones\\__init__.py'...
Compiling 'app\\planillas\\generador.py'...
Compiling 'app\\planillas\\pdf.py'...
Listing 'app\\rutas'...
Compiling 'app\\rutas\\__init__.py'...
Listing 'app\\static'...
Listing 'app\\templates'...
```

Código de salida: 0.

- Paso 5. python -m pip --isolated check: No broken requirements found.. Código de salida: 0.

### Paso 6 — Revisión final del registro y estado de la etapa 0

Fecha: 2026-10-25.

- Revisados REGISTRO_DE_CAMBIOS.md y PREGUNTAS_ABIERTAS.md. Se conserva el historial anterior; las notas antiguas sobre .env.ejemplo y el entorno externo quedan superadas por esta continuación.
- Estructura de la sección 5 completa. Los archivos de funcionalidad pendientes quedaron vacíos; no se inició la etapa 1.
- README.md, requirements.txt, .gitignore, AGENTS.md, PASOS_SERVICIO_FINAL_readyproof.md, app/__init__.py, tests/test_base.py, migraciones/.gitkeep y docs/INSTALACION.md conservan sus hashes SHA256 respecto de la copia original.
- Comparación SHA256 de todos los archivos de fuente/ contra el original: idénticos; no se modificó el kit.
- .env.ejemplo presente con los valores de ejemplo solicitados; .env real no creado. Sin credenciales reales ni copias nuevas de normas.
- Entorno activo para las verificaciones: C:\Users\jorge\Readyproof\.venv, creado en esta etapa; el entorno externo anterior no se modificó.
- pytest -q: 1 passed in 0.03s, código 0. La prueba existente valida la importación de app; las pruebas funcionales corresponden a etapas siguientes.
- python -m compileall app: código 0. python -m pip --isolated check: No broken requirements found., código 0.
- Uso de internet limitado al proceso de instalación desde PyPI. No se cambió ningún ajuste persistente de red o seguridad.
- Etapa 0 completada en la nueva copia. No avanzar a la etapa 1 sin confirmación de Jorge.
- Pendiente de la aplicación de desarrollo: abrir C:\Users\jorge\Readyproof como proyecto para que los comandos ordinarios usen el entorno de pruebas aislado sobre la nueva ubicación. Este chat sigue asociado a Documentos; los comandos de esta continuación fueron autorizados fuera del entorno de pruebas aislado y dirigidos expresamente a la nueva copia.

## 2026-10-25 — Etapa 1: inicio y cotejo previo de SAA-1

- Autorizado el inicio de la etapa 1 por Jorge. Leído el generador original y la definición SAA-1 en planillas_data3.py. No se modificó fuente/.
- Extraída exclusivamente la planilla oficial SAA-1 del archivo local SG-PEM-IFI_Planillas_v5.zip a out/etapa1/SAA-1_referencia_v5.xlsx.
- Ejecutado build(sp, out, modelo) del kit con la definición SAA-1, sin datos cargados, para producir out/etapa1/SAA-1_generador_sin_carga.xlsx. Es un archivo de diagnóstico, no una planilla emitida.
- Cotejo con openpyxl: valores y estilos de celdas idénticos; ambos tienen 44 filas y 25 columnas, área de impresión A1:Y44 y los mismos márgenes. Diferencia de impresión: ancho A 6.2 y centrado horizontal True en la referencia; ancho A 5.3 y centrado horizontal no configurado en el generado.
- El encargo AGENTS.md exige que el PDF coincida con la serie y que el generador sea la fuente única de formato. Ante esta discrepancia y la instrucción de no modificar fuente/, se detiene la implementación para consultar. No se implementó un ajuste alternativo en la aplicación.
- No se encontró LibreOffice en PATH ni en las ubicaciones habituales. El PDF SAA disponible en la serie es el manual completo; falta referencia PDF de la planilla o aprobación para usar el Excel v5 convertido.
- Preguntas registradas en PREGUNTAS_ABIERTAS.md. Sin acceso a internet, sin nuevas dependencias y sin cambios de seguridad. Etapa 1 incompleta.

Comando: pytest -q. Código de salida: 0.
Salida exacta:
```text
.                                                                        [100%]
1 passed in 0.03s
```

Comando: python -m compileall app. Código de salida: 0.
Salida exacta:
```text
Listing 'app'...
Listing 'app\\auth'...
Listing 'app\\models'...
Listing 'app\\planillas'...
Listing 'app\\planillas\\definiciones'...
Listing 'app\\rutas'...
Listing 'app\\static'...
Listing 'app\\templates'...
```

## 2026-10-25 — Etapa 1: ejecución autorizada

- Jorge autorizó explícitamente corregir el generador (ancho 6.2 y centrado), descargar e instalar LibreOffice y usar el Excel oficial v5 convertido a PDF como referencia.
- Se inicia instalación local de LibreOffice mediante winget, paquete TheDocumentFoundation.LibreOffice, con verificación del instalador a cargo de winget. Excepción de red autorizada solo para obtener e instalar LibreOffice. No se modifican Defender ni el entorno de pruebas aislado.
- Implementados definición SAA-1 desde el kit, adaptador con validación de campos y opciones y escritura XML que conserva logos, y conversor LibreOffice con perfil aislado y sin sobrescritura. Ajuste autorizado del generador: ancho de impresión 6.2 y centrado horizontal; se conserva COLW=5.3 para el cálculo original de alturas. Respaldo en bak/build_planilla_antes_ajuste_v5.py. lxml, dependencia ya instalada de python-docx, se reutiliza para conservar namespaces del XML; no se añaden paquetes.
- Comando: winget install --id TheDocumentFoundation.LibreOffice --exact --source winget --silent --accept-package-agreements --accept-source-agreements --disable-interactivity. Código de salida: -1978334964. Salida completa: out/etapa1/instalacion_libreoffice.log.
- Primer ensayo del adaptador: 16 pruebas pasan y 1 detecta una diferencia en las dimensiones de columna. Se investiga antes de dar por válido el cotejo; no se entrega como aprobado.
- Instalación LibreOffice por winget: el hash del instalador se verificó, pero la instalación terminó con «Ha cancelado la instalación», código del instalador 1602. No se reintenta ni se usa un método alternativo; queda pendiente completar la instalación autorizada. Salida exacta en out/etapa1/instalacion_libreoffice.log.
- Jorge pidió reintentar la instalación y confirmó que aceptará la elevación de Windows. Comando winget install TheDocumentFoundation.LibreOffice (mismos argumentos). Código de salida: 0. Registro: out/etapa1/instalacion_libreoffice_reintento.log.
- Reintento de instalación de LibreOffice completado: versión 26.8.1.1. Se generaron los tres PDF; referencia, blanco y piloto tienen 2 páginas. El blanco coincide píxel por píxel con la referencia en ambas páginas.
- La inspección visual detectó ausencia de logos en ambos PDF: LibreOffice no exportó las imágenes VML del encabezado del Excel. Se comprobó que los PDF tenían 0 imágenes por página y que los Excel conservaban los logos originales. No se da por aprobado ese resultado.
- Jorge autorizó agregar pypdf y Pillow y descargarlos desde PyPI para reponer las imágenes originales después de la conversión, leyendo tamaños y posiciones del encabezado del Excel. No se rediseña la planilla ni se cambian los datos del kit.
- Dependencias PDF instaladas y fijadas: pypdf==6.21.2, Pillow==13.0.0. pypdf compone los XObject del PDF; Pillow lee los PNG/JPEG originales del encabezado. Sin otras operaciones de red.

### Verificación final de la etapa 1 — 2026-10-25

Comando: pytest -q
Salida exacta:
```text
....................                                                     [100%]
20 passed in 22.72s
```
Código de salida: 0.

Comando: python -m compileall app
Salida exacta:
```text
Listing 'app'...
Listing 'app\\auth'...
Listing 'app\\models'...
Listing 'app\\planillas'...
Listing 'app\\planillas\\definiciones'...
Listing 'app\\rutas'...
Listing 'app\\static'...
Listing 'app\\templates'...
```
Código de salida: 0.

### Resultado técnico y entrega para revisión — 2026-10-25

- Implementados app/planillas/definiciones/saa1.py, generador.py, pdf.py, encabezado_pdf.py y piloto.py. El adaptador recibe un diccionario, completa los espacios originales y rechaza campos y opciones desconocidos. No sobrescribe cargas ni PDF existentes.
- Único archivo del kit modificado: fuente/herramientas/build_planilla.py, con el ajuste de impresión autorizado. Comparación SHA256 contra el original: todos los demás archivos de fuente/ permanecen idénticos. Respaldo del generador original verificado en bak/build_planilla_antes_ajuste_v5.py. AGENTS.md sin cambios.
- LibreOffice 26.8.1.1 instalado. pypdf==6.21.2 y Pillow==13.0.0 incorporados con autorización y justificación; requirements.lock.txt registra también las versiones transitivas instaladas, sin modificar las versiones directas anteriores.
- Pruebas finales: pytest -q, 20 passed in 22.72s, código 0, sin pruebas omitidas. Incluyen conversión real con LibreOffice, mismo número de páginas que la referencia, dos logos por página, leyendas de encabezado y pie, equivalencia Excel, validación de opciones/campos, entradas como texto, protección contra sobrescritura y manejo de fallo/timeout.
- python -m compileall app: código 0. python -m pip --isolated check: No broken requirements found., código 0.
- Cotejo automático con referencia oficial convertida: referencia 2 páginas, blanco 2 páginas, piloto 2 páginas; blanco idéntico píxel por píxel a la referencia en ambas páginas. Se verificaron ambos logos en todas las páginas y las leyendas de encabezado/pie. Resultado en out/etapa1/revision_con_logos/resultado.json.
- Inspección visual realizada de las dos páginas finales: logos presentes y sin superposición, datos ficticios legibles, mismas filas, mismas posiciones de observaciones y firmas que la referencia. La segunda página del original contiene observaciones y firmas; se conservó esa paginación.
- Entregable para revisión: out/etapa1/pdf_con_logos/SAA-1_ejemplo.pdf. Comparación de página 1: out/etapa1/revision_con_logos/comparacion_pagina_1.png. Los archivos sin logos en out/etapa1/pdf/ son diagnósticos superados y no deben entregarse al cliente.
- Documentación en docs/PILOTO_SAA1.md y sección agregada a README.md. Pruebas y temporales dentro del proyecto. No se implementaron usuarios, API, envío de correos ni captura de firmas: corresponden a las etapas siguientes.
- Registro y preguntas abiertas revisados. Implementación de la etapa 1 lista para revisión de Jorge; aceptación pendiente de su aprobación visual. No se inicia la etapa 2.

## 2026-10-25 — Aprobación y cierre de la etapa 1

- Jorge aprobó explícitamente el formato del piloto SAA-1 presentado: «esta aprobado».
- La aprobación corresponde a out/etapa1/pdf_con_logos/SAA-1_ejemplo.pdf y su comparación visual con la referencia oficial v5, con los logos originales y dos páginas.
- Con esta aprobación se cumple el criterio de aceptación visual y queda cerrada la etapa 1. La última validación técnica registrada fue de 20 pruebas aprobadas y compileall sin errores; no se modificó código después de esa validación.
- No se inició la etapa 2 en este paso.


## 2026-10-25 — Etapa 1: corrección de observaciones de auditoría

Alcance limitado a las observaciones solicitadas. No se inició la etapa 2. No se modificó ningún archivo de fuente/ ni el informe auditorias/AUDITORIA_etapa1_2026-10-25.md.

- M1. Agregada la ausencia de la leyenda y el bloqueo de emisión real en PREGUNTAS_ABIERTAS.md. Creada la prueba de presencia en PDF con pytest.mark.xfail, motivo «leyenda pendiente de confirmación de Martín», strict=True y limitada a AssertionError. No se agregó la leyenda al PDF ni se omitió la prueba.
- M2. El cambio previamente autorizado de build_planilla.py replica el ajuste de fix_impresion.py descrito en fuente/KIT_AGENTS.md: ancho de impresión 6,2 y centrado horizontal, conservando el cálculo de alturas. Afecta a las 79 planillas de la serie, no solo SAA-1. Se registró como pendiente avisar a Martín; las otras planillas se cotejarán en la etapa 6. No se revirtió ni se amplió el cambio del generador.
- M3. Creado requirements-dev.txt con pypdfium2==5.14.0 e instalado en .venv. La comparación de todos los píxeles de todas las páginas pasa a pytest, convirtiendo referencia y blanco con el mismo LibreOffice. Una importación obligatoria hace fallar la colección si falta pypdfium2. El script solo regenera imágenes y resultado.json; documentación actualizada para ejecutar con el entorno del proyecto. Se regeneró out/etapa1/revision_reproducible/ sin sobrescribir revisiones previas. requirements.lock.txt actualizado para reflejar el entorno instalado.
- M4. Identidad de Git configurada solo en este repositorio con los datos indicados por Jorge, sin --global. Primer commit local b922971, «Etapa 1: piloto SAA-1 aprobado», realizado antes de las correcciones. Se copiaron, sin mover originales, el PDF y la comparación aprobados a docs/aprobaciones/etapa1/. Se verificaron sus SHA256. El segundo commit agrupa únicamente las correcciones de esta tarea. No se creó ni se utilizó un repositorio remoto.
- m1. Reescritas en términos neutros las menciones señaladas en docs/PILOTO_SAA1.md y REGISTRO_DE_CAMBIOS.md, incluidas las demás ocurrencias del mismo término en esos documentos, sin borrar ni cambiar el sentido del historial.
- m2. La prueba de carga verifica todos los campos del piloto en J de la fila de su etiqueta, con valores distintos para detectar intercambios, y los cuatro renglones de observaciones A36:A39. La prueba de conversión compara el texto fijo completo del encabezado y pie con la referencia en todas las páginas; la fecha variable V4 se comprueba como dato cargado.
- m3. El título del PDF se obtiene del código de la planilla en T1, en lugar de usar SAA-1 fijo. Una prueba con otro código verifica el título dinámico y que creador/productor siguen siendo readyproof. Se registró la decisión pendiente de Jorge sobre esos dos metadatos.
- m4. Documentada la excepción de los valores ficticios numéricos y de opción (1 y primera opción), que no pueden llevar el prefijo [Ejemplo]. No se cambiaron los datos del piloto aprobado.
- m5. Registrada la falta de fix_impresion.py y la consulta sobre la integridad de la copia del kit. No se creó el archivo ni se modificó fuente/.
- m6. Documentada como única referencia oficial tests/referencias/SAA-1_v5.xlsx, convertida durante las pruebas. El PDF de referencias/SAA-1/ se identifica como diagnóstico sin logos generado con otra versión de LibreOffice, sin uso para aceptar. No se borró ningún archivo.
- m7. Declarado lxml==6.1.3 en requirements.txt porque la aplicación lo importa directamente; la versión instalada ya era 6.1.3.

### Comandos y resultados

- git config --local user.name y git config --local user.email: completados con los datos indicados por Jorge; configuración exclusivamente local.
- git status --short, revisión de .gitignore y git check-ignore para .env, .venv, __pycache__, .pytest_cache y out/: exclusiones verificadas antes del primer commit. Revisión de candidatos: sin .env real, cachés, entorno virtual ni patrones de secretos detectados. .env.ejemplo conserva solo valores de ejemplo.
- git add --all y git commit -m "Etapa 1: piloto SAA-1 aprobado": código 0, commit b922971 con el estado previo a esta tarea.
- .venv\Scripts\python.exe -m pip --isolated install --index-url https://pypi.org/simple --disable-pip-version-check --no-cache-dir -r requirements-dev.txt: código 0. Se instaló pypdfium2==5.14.0; lxml==6.1.3 ya estaba instalado. Único uso de red en esta tarea, limitado a los paquetes autorizados de PyPI. Salida en out/auditoria_etapa1/instalacion_dev.log.
- Regeneración de referencia, blanco y piloto con app.planillas.pdf.convertir_pdf desde .venv: completada, dos páginas y dos logos por página en cada documento. Nuevos PDF en out/etapa1/pdf_reproducible/.
- .venv\Scripts\python.exe scripts/verificar_pdf_saa1.py --referencia out/etapa1/pdf_reproducible/referencia.pdf --blanca out/etapa1/pdf_reproducible/blanca.pdf --piloto out/etapa1/pdf_reproducible/piloto.pdf --salida out/etapa1/revision_reproducible: código 0. Imágenes y resultado.json regenerados con .venv; inspección visual de ambas páginas sin cambios de formato respecto de la revisión aprobada. Salida en out/auditoria_etapa1/imagenes.log.

Comando con .venv: pytest -q

Salida exacta:
```text
...................x...                                                  [100%]
22 passed, 1 xfailed in 33.17s
```
Código de salida: 0.

Comando con .venv: python -m compileall app

Salida exacta:
```text
Listing 'app'...
Listing 'app\\auth'...
Listing 'app\\models'...
Listing 'app\\planillas'...
Listing 'app\\planillas\\definiciones'...
Listing 'app\\rutas'...
Listing 'app\\static'...
Listing 'app\\templates'...
```
Código de salida: 0.

Comando con .venv: python -m pip --isolated check

Salida exacta:
```text
No broken requirements found.
```
Código de salida: 0.

- Verificación SHA256 al cierre: 173 archivos de fuente/ idénticos al estado anterior a esta tarea; informe de auditoría idéntico. Las dos copias de aprobaciones coinciden con sus originales. Manifiesto y resultado en out/auditoria_etapa1/sha256_antes.json y sha256_verificacion.json.
- Antes del segundo commit se revisan git status, .gitignore y el índice: no se admiten .env reales, entorno virtual, cachés ni secretos. Mensaje del segundo commit local: «Etapa 1: corrección de observaciones de auditoría».
- Pendientes: texto y ubicación de la leyenda con Martín (bloquea emitir a clientes reales), aviso a Martín del cambio de formato y cotejo del resto en etapa 6, decisión de Jorge sobre creador/productor del PDF, y confirmación de la integridad del kit por la falta de fix_impresion.py. Las preguntas originales sobre NFPA 17A/NFPA 10 siguen vigentes. No se contactó a terceros ni se tomaron esas decisiones.
