# Registro de cambios: readyproof

## 2026-11-01 — C4b: anexo con texto vectorial y JPEG original

- Jorge autorizó agregar reportlab para incrustar IBM Plex Sans y generar encabezado, referencias y pie como texto seleccionable. Se fijan reportlab==5.1.0 y su dependencia charset-normalizer==3.5.2; Pillow y pypdf conservan sus versiones.
- El JPEG estandarizado se inserta como XObject DCTDecode con sus bytes originales, sin redimensionar ni recodificar la imagen. Las marcas numeradas se superponen como vectores en coordenadas normalizadas, con color configurable en COLOR_MARCAS.
- El check visible es un trazo propio; se conserva el carácter U+2713 de la serie para búsqueda y copia. El pie se lee de la leyenda existente y del kit. La cabecera usa cliente, equipo, inspector y fecha guardados en la carga; datos ausentes se muestran con raya.
- Pruebas nuevas C4b: 20 aprobadas en 0.71 s, sin fallos. Se verifican pdftotext, fuente TrueType incrustada, igualdad SHA-256 del JPEG, A4 y paginación. Primera corrida: 16 aprobadas y 4 fallidas por no detectar pdftotext; resuelto usando la copia instalada con Git, sin instalar utilidades adicionales.
- Módulo de anexo independiente: no se cambia el generador de planillas, no se integra a emisión ni se modifican PDFs emitidos, correo, Contabilium o migraciones. Sin suite completa, commit, push, tags ni despliegue; revisión visual y elección final de color pendientes de Jorge.

## 2026-10-30 — A2-3: identificación técnica según modo

- El prefijo exacto [Ejemplo] se elimina solo del nombre presentado del técnico en nuevos PDF REAL. PILOTO conserva el prefijo; identidad almacenada, historial y PDF anteriores intactos.
- Regresión con datos ficticios: presentación REAL/PILOTO y PDF REAL, 3 pruebas aprobadas en 11.09 s. Suite completa: 582 aprobadas, 0 fallos, 2793.17 s; compileall app sin errores.
- La designación indicada por Jorge se reporta en Registro 1/Revisión 0 y Registro 2/Revisión 0; no se modifica ningún registro.

## 2026-10-30 — A2-1/A2-2: paginación de copias nuevas

- Referencia SCC-2, Registro 1/Revisión 0, copiada desde Descargas con autorización; original y copia conservan SHA256 dc26a7bc31c72f5507d614fbac9f75acfed390704ab774deb7c84becd91ab34e. La referencia privada queda excluida de Git.
- Configuración XML de impresión aplicada exclusivamente a la copia temporal: una hoja cuando cabe, escala y saltos entre filas/bloques para planillas grandes, repetición de cabecera y observaciones/firmas juntas. Sin cambios de celdas o de fuente/.
- Jorge confirmó encabezado del kit con mínimo absoluto de 4 mm y cuerpo con zona segura de 10 mm. Anclas de logos antes/después idénticas con igual identificación. Pie elevado a 11 mm para respetar 10 mm también con los descendentes tipográficos.
- Corregido WinError 145 de Windows durante limpieza de un perfil de LibreOffice en una ruta larga: perfil aislado en temporal corto separado. Prueba histórica con ruta larga aprobada, sin relajar aserciones.
- Validación focalizada: 44 passed in 256.66s; regresión de perfil: 1 passed in 2.79s; histórica tras corrección: 1 passed in 40.48s. Suite completa: 579 aprobadas, 0 fallos, 2926.69 s; compileall app sin errores.
- Inventario remoto en 67.205.170.29 con REPEATABLE READ READ ONLY: 43 PDF distintos, huellas íntegras; 14 casos con observaciones y firmas en páginas distintas (13 sin número público y Registro 1/Revisión 0). Registros reales 1 y 2, revisión 0, contienen la designación señalada por Jorge. Sin modificar datos ni PDF del servidor.
- Se preservan los cambios locales ajenos. Sin push, tag, despliegue, correo ni cambios de credenciales. Evidencia en out/frente_a_v2/ y REPORTE_FRENTE_A_V2.json.

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


## 2026-10-25 — Etapa 2: modelo de datos y API de planillas

- Jorge autorizó iniciar exclusivamente la etapa 2, sin interfaz, usuarios, correo ni servicios externos. La emisión real permanece bloqueada por M1; la API se limita a datos ficticios [Ejemplo].
- Leídos AGENTS.md, la verificación de auditoría de la etapa 1 y ambos registros. n2 corregido: README indica instalar requirements-dev.txt para ejecutar pytest. n1 registrado como pendiente antes de la etapa 6, sin modificar la comparación actual.
- Comprobados Get-Command psql/postgres/pg_ctl, servicios con nombre postgres y carpeta habitual de instalación: no se encontró PostgreSQL. Consulta registrada con las dos opciones autorizables; no se instaló ningún servidor.
- Jorge eligió instalar PostgreSQL local. Se utiliza el paquete PostgreSQL.PostgreSQL.18 del catálogo de instalación, sin servicios externos. La instalación es interactiva para que las credenciales, si se solicitan, se ingresen directamente en Windows.


### Implementación y cierre de la etapa 2 — 2026-10-25

- Alcance: fábrica Flask y configuración por variables de entorno; modelos Cliente, Sistema, Planilla, Carga y RevisionCarga; esquema inicial y versión de migración; catálogo local SAA-1. Usuario (etapa 4) y Envio (etapa 5) se difieren por indicación de no implementar autenticación ni correo en esta etapa. No se implementó interfaz ni se inició la etapa 3.
- Endpoints locales para listar clientes/sistemas/planillas, consultar la definición, crear/consultar una carga, reemplazar el borrador, finalizar, emitir el PDF ficticio, descargarlo y consultar revisiones. Validación estricta de campos, fechas ISO, números JSON finitos, cantidades enteras, opciones literales y texto de ejemplo. No se agregaron campos ni valores normativos a las planillas.
- Flujo borrador → finalizada → emitida, con bloqueo de edición al finalizar, revalidación antes de finalizar/emitir y control optimista de revisiones en SQLAlchemy/PostgreSQL. Cada evento guarda una instantánea, fecha UTC y actor local ficticio sin autenticación. La autenticación e identificación real corresponden a la etapa 4.
- La versión y huella SHA256 de la plantilla quedan asociadas a cada carga. Si el generador, los datos fuente o el modelo difieren de esa versión, se bloquea finalizar/emitir. El PDF, su hash y el estado se confirman en una transacción; una conversión fallida no marca emisión ni deja un PDF registrado. El Excel se conserva solo durante la conversión.
- M1 sigue activo: sin opción para habilitar emisión real. Se admiten solo clientes y sistemas ficticios identificados, y textos [Ejemplo]; se rechazan clientes no marcados como ejemplo y nombres inconsistentes. Fechas, números y opciones conservan su tipo. No se agregó la leyenda pendiente al PDF.
- n2 corregido en README: requirements-dev.txt es necesario para las pruebas. n1 registrado para antes de la etapa 6; no se modificó la comparación de SAA-1.
- Con autorización de Jorge se instaló PostgreSQL 18.6 mediante winget, paquete PostgreSQL.PostgreSQL.18. Salida en out/etapa2/instalacion_postgresql.log: «Instalado correctamente». Servicio postgresql-x64-18 en ejecución. No se leyeron ni guardaron contraseñas; no se usaron servicios externos ni DigitalOcean.
- Jorge pidió finalizar el instalador. Se cerró exclusivamente su proceso opcional Stack Builder sin instalar componentes adicionales. La configuración inicial escuchaba en todas las interfaces; se limitó listen_addresses a localhost y se reinició únicamente el servicio recién instalado, con autorización. Verificaciones locales en out/etapa2/cierre_instalacion.json y stack_builder_cerrado.txt; el segundo archivo confirma el cierre posterior del proceso opcional.
- Las pruebas usan PostgreSQL real en un clúster temporal dentro de .venv/tmp/pytest, enlazado solo a 127.0.0.1, sin contraseña ni datos reales. Cada caso usa una base descartable; el clúster se detiene al terminar. No se utilizó SQLite ni se accedió a la base habitual de la instalación.
- Primer ensayo de arranque: PostgreSQL aceptaba conexiones pero una tubería de salida heredada por el servidor impedía terminar pg_ctl. Se detuvo únicamente el clúster temporal de ese ensayo y se corrigió la fixture para redirigir salida a archivo y garantizar el apagado. Las primeras pruebas de API corregidas terminaron con 26 passed; luego se agregaron los controles de cierre.
- Dependencias de aplicación y desarrollo conservadas, sin nuevos paquetes Python. Se reutilizan Flask, SQLAlchemy y psycopg ya fijados. La única red adicional de esta etapa fue la descarga autorizada de PostgreSQL.
- Documentación de configuración local, contrato de API, estados, tipos y limitaciones en docs/API_ETAPA2.md. init-db --ejemplos es idempotente y no duplica catálogo ni cliente ficticio.

Comando con .venv: pytest -q

Salida exacta:
```text
...................................................x...                  [100%]
54 passed, 1 xfailed in 108.84s (0:01:48)
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

- Verificación SHA256: 180 archivos de fuente/, auditorias/ y docs/aprobaciones/ idénticos al comienzo de la etapa; no se modificaron el kit, los informes de auditoría ni los entregables aprobados.
- El commit local de cierre agrupa únicamente la etapa 2 y la verificación de auditoría proporcionada por Jorge. Antes de prepararlo se revisan .gitignore, git status y el índice para excluir .env reales, .venv, cachés, datos del servidor y secretos. No se publica ni se agrega un remoto.
- Pendientes: M1 con Martín antes de emitir a clientes reales; n1 antes de la etapa 6; preguntas anteriores sobre aviso de formato, metadatos e integridad del kit. La definición no establece obligatoriedad de cada campo: no se inventó esa política y debe confirmarse antes de una emisión real. Finalizar valida los datos presentes y rechaza cargas vacías; las pruebas de flujo usan todos los campos del ejemplo.
- Etapa 2 implementada y verificada para desarrollo local con ejemplos. No se avanza a la etapa 3.


### 2026-10-25 — Aclaración del diferimiento de Usuario/Envio

- Registrado en PREGUNTAS_ABIERTAS.md el diferimiento de Usuario a la etapa 4 y Envio a la etapa 5, pendiente de confirmación de Jorge. No se implementaron los modelos ni se modificó el criterio de aceptación del encargo. Etapa 2 pendiente de confirmación de Jorge.
- README verificado: la sección de etapa 2 ya indica que no se incluyen interfaz, usuarios ni correo; se conserva sin cambios.
- .env.ejemplo: DATABASE_URL comentada con un ejemplo sin contraseña y una aclaración de que requiere autenticación local compatible; las pruebas usan su clúster temporal sin contraseña. No se cambió la autenticación del servicio instalado.
- docs/API_ETAPA2.md: se aclara que GET /api/cargas/{id}/revisiones devuelve datos como instantánea JSON completa de cada revisión.
- Cambios únicamente documentales y de comentarios de configuración, verificados por lectura; no se ejecutaron pruebas ni se alteró código. AGENTS.md, fuente/ y README sin cambios. No se ejecutaron comandos Git.


## 2026-10-25 — Etapa 3: interfaz de carga de SAA-1

- Jorge confirmó explícitamente ambos puntos: Usuario diferido a etapa 4 y Envio a etapa 5; inicio autorizado de la interfaz de etapa 3. La aclaración pendiente de etapa 2 queda aceptada.
- Alcance: selección de cliente/sistema/planilla, formulario generado desde la definición, autoguardado local, progreso y validación, vista previa antes de emitir, firmas de prueba y borradores locales para trabajar sin conexión durante la carga. M1 sigue bloqueando uso real.
- Se conserva AGENTS.md, fuente/, las auditorías y los entregables aprobados. No se inicia autenticación, correo ni la etapa 4.


### 2026-10-25 — Implementación y verificación técnica de la etapa 3

- Interfaz: agregados app/rutas/web.py, app/templates/carga.html y los recursos carga.js, carga.css, icono.svg, manifest.webmanifest y sw.js. Selección de cliente/sistema/planilla; campos generados desde la definición, orden y opciones originales, progreso, validación y autoguardado. Se conserva la documentación histórica de etapa 2 en README y se agrega la de etapa 3.
- Sin conexión: catálogo y borradores en IndexedDB; service worker limitado a la pantalla y sus recursos. Comprobada carga con la red apagada, dos firmas táctiles, recarga offline y recuperación de cambios. Reconexión con identificador estable y revisiones, sin duplicar la carga. Un conflicto conserva la copia local y permite crear otro borrador; la cola completa y conflictos entre dispositivos corresponden a etapa 8.
- Firmas: agregado app/planillas/firmas.py y modelo FirmaCarga. PNG limitado en formato, dimensiones, tamaño y trazos; se recodifica antes de guardarlo. Las revisiones guardan hashes, no imágenes. No hay descarga independiente de firmas. La migración 002_firmas_etapa3.py es aditiva y se probó conservando cargas de etapa 2. Sin usuarios ni permisos reales hasta etapa 4; solo firmas sintéticas de prueba.
- PDF: POST /api/cargas/{id}/vista-previa no finaliza ni registra una emisión. La pantalla exige vista previa actualizada y ambas firmas de prueba antes de finalizar. Las firmas se incorporan en los espacios existentes calculados desde Excel y el pie PDF; sin cambios de filas ni formato del generador. La descarga sigue siendo exclusivamente PDF. M1 no se resuelve por cuenta del desarrollo y la emisión real continúa bloqueada.
- API: metadato firmas separado de datos normativos; Idempotency-Key para recuperar una creación ya guardada; respuestas sin exposición de PNG. Se admite observación vacía para conservar filas sin inventar texto. La configuración y el servidor de ejemplos restringen acceso a loopback.
- Pruebas agregadas: tests/test_firmas.py, tests/test_interfaz.py y tests/browser/interfaz.cjs. PNG inválidos, limpieza, historial, migración, creación idempotente, vista previa sin cambio de estado y flujo completo firmado en navegador. Emulación táctil a 390×844 y revisión a 1440×1000, sin desbordamiento ni errores JavaScript; una sola carga tras reconectar. El PDF emitido y la vista previa tienen dos páginas y las imágenes esperadas [2, 4].
- La copia de evidencia obtenida inicialmente mediante response.body de Playwright quedó vacía aunque el PDF llegaba al navegador. Se reforzó la prueba para recuperar el blob que recibe la pantalla, exigir %PDF-, tamaño mayor a 1000 bytes y comprobar páginas e imágenes con pypdf. La repetición completa pasó; out/etapa3/navegador/vista_previa.pdf tiene 196634 bytes. No fue necesario modificar la funcionalidad de vista previa.
- Dependencias: ninguna dependencia Python nueva ni descarga. package.json declara Playwright 1.62.1 como dependencia de desarrollo para reproducir el recorrido; se reutilizaron Node.js, Playwright y navegador locales. Su uso se justifica por la aceptación táctil/offline que no cubren las pruebas de API. Instrucciones y variables opcionales en docs/INTERFAZ_ETAPA3.md.
- Revisión local: agregado scripts/iniciar_ejemplo.py. Comando: .venv\Scripts\python.exe -u scripts/iniciar_ejemplo.py --port 8765. Responde HTTP 200 en http://127.0.0.1:8765; PostgreSQL de ejemplos separado en out/etapa3/demo_local/, sin contraseñas y escuchando solo en 127.0.0.1. No se accede a la base habitual, no se publica ni se usa un servicio externo. El servidor se conserva abierto para revisión; el lanzador detiene su propio clúster al cerrar con Ctrl+C.
- Evidencias: capturas celular_inicio.png, firmas_celular.png y notebook.png; SAA-1_firmada.pdf, vista_previa.pdf y resultado.json en out/etapa3/navegador/. Revisado visualmente el PDF con firmas sintéticas dentro de los espacios de la serie y logos presentes. README y docs/INTERFAZ_ETAPA3.md documentan uso, preparación offline, pruebas y límites.

Comando con .venv: pytest -q
Entorno de pruebas: NODE_PATH apunta al Playwright local existente; TEMP/TMP a .venv/tmp. Sin descargas.

Salida exacta:
```text
............................................................x....        [100%]
64 passed, 1 xfailed in 129.58s (0:02:09)
```
Código de salida: 0. La única xfail es estricta y corresponde a M1, ya pendiente en la etapa 1.

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

- Integridad: comparación SHA256 de 181 archivos de fuente/, auditorias/ y docs/aprobaciones/, sin modificaciones, ausencias ni agregados. Manifiesto y resultado en out/etapa3/integridad_antes.json e integridad_verificacion.json. AGENTS.md no se modificó. No se ejecutaron comandos Git ni se hizo commit, conservando la última restricción expresa de Jorge.
- Revisión del registro: entradas previas preservadas; resultados, comandos y pendientes de esta etapa agregados al final. No se escribieron secretos ni datos personales reales.
- Estado: implementación técnica de etapa 3 lista para revisión local, con pruebas aprobadas en emulación de celular. Sigue pendiente que el técnico de prueba complete el recorrido en un teléfono físico y Jorge revise la interfaz; ese criterio manual no se declara cumplido. No se avanza a etapa 4.
- Pendientes vigentes: M1 antes de emitir a clientes reales; política de campos obligatorios antes del uso real; n1 antes de etapa 6; aviso a Martín del cambio anterior de formato, metadatos del PDF, integridad del kit y ediciones normativas autorizadas. No se tomaron decisiones nuevas sobre estos puntos.


## 2026-10-25 — Auditoría etapa 3: correcciones menores de documentación

- README.md: ampliada la sección de etapa 3 inmediatamente después de la de etapa 2, sin duplicarla; requisitos de navegador, comando local Flask, alternativa de base de ejemplos aislada, características, validación y datos de prueba. Se aclara que el acceso es al servidor local y no requiere internet, que Flask necesita la base preparada y que ambas opciones de inicio comparten puerto. El sistema se documenta con su nombre real de catálogo ficticio: [Ejemplo] Abastecimiento de agua. No se cambió el catálogo ni la API.
- docs/INTERFAZ_ETAPA3.md: ya existía; revisado y conservado sin cambios porque incluye inicio local y navegación, además de uso sin conexión y límites.
- package.json: incorporado scripts.test = playwright test, conservando Playwright 1.62.1. No se descargaron ni instalaron dependencias.
- No existe playwright.config.js. Se registró como pendiente en PREGUNTAS_ABIERTAS.md la confirmación de configuración y adaptación al runner; no se creó el archivo ni se presenta npm test como una prueba operativa. La prueba vigente de navegador continúa dentro de pytest, con el recorrido CJS existente. No se agregó al README una sección nueva de pruebas de navegador, conforme a la condición solicitada.
- Verificación documental y JSON: sección de etapa 3 única, en el orden solicitado; comandos y condiciones leídos, script comprobado. Comparación SHA256 de 204 archivos protegidos: fuente/, app/, migraciones/ y docs/INTERFAZ_ETAPA3.md sin cambios. No se ejecutó Git ni se modificó AGENTS.md. Evidencias en out/auditoria_etapa3_documentacion/.

Comando con .venv: pytest -q
Entorno: Node.js/Playwright locales; TEMP/TMP dentro de .venv/tmp. Sin descargas.

Salida exacta:
```text
............................................................x....        [100%]
64 passed, 1 xfailed in 126.15s (0:02:06)
```
Código de salida: 0. La única xfail corresponde a M1, pendiente anterior.

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

- Hallazgos menores atendidos. Continúan pendientes la configuración Playwright autorizable, la revisión manual en teléfono físico y M1 antes del uso real. Sin avance a etapa 4.


## 2026-10-25 — Preparación de la prueba física de etapa 3

- A pedido de continuar se revisaron el lanzador local, la configuración, el service worker, las reglas del encargo y el instructivo de servicio. Comprobación HTTP de http://127.0.0.1:8765: 200.
- Jorge respondió que utilizará un iPhone. Se preparó docs/PRUEBA_IPHONE_ETAPA3.md con acceso temporal propuesto, recorrido táctil/offline, reconexión, PDF y cierre. No se declara realizada la prueba física.
- Se registró en PREGUNTAS_ABIERTAS.md la decisión pendiente sobre HTTPS en Wi-Fi local y certificado de revisión. No se cambió la escucha del servidor, no se abrió un puerto, no se instaló un certificado, no se modificó el firewall ni se utilizó un servicio externo.
- Cambios de esta preparación exclusivamente documentales; lectura UTF-8 verificada. No se ejecutaron pruebas nuevas de código: la última suite registrada sigue siendo 64 passed, 1 xfailed, y compileall sin errores. No se alteraron API, PDF, fuente/ ni Git. No se avanzó a etapa 4.


## 2026-10-25 — Acceso a iPhone suspendido y verificación posterior

- Jorge autorizó inicialmente preparar HTTPS temporal y luego interrumpió el trabajo para consultar el efecto sobre la seguridad del iPhone. La vía de acceso quedó detenida; los mensajes posteriores no se interpretan como autorización para instalar certificados o abrir la red.
- Archivo creado antes de la interrupción: scripts/iphone_bridge.cs, prototipo del puente HTTPS. Ensayo exclusivamente en 127.0.0.1 con puertos efímeros; certificado y claves generados en memoria, sin instalación en almacenes de confianza ni exportación de claves privadas. La instancia de ensayo se cerró mediante Dispose.
- La escritura de los lanzadores/firewall fue interrumpida. Verificación posterior: en scripts/ solo existe iphone_bridge.cs respecto de esta preparación; no existen iniciar_prueba_iphone.ps1 ni firewall_prueba_iphone.ps1 y no hay sesiones en out/etapa3/iphone.
- Comandos de comprobación: Get-ChildItem scripts/*iphone*; Get-NetTCPConnection -State Listen filtrado a 8766/8767; Get-NetFirewallRule filtrado a readyproof-iphone-* y su nombre visible. Resultado: sin escuchas en 8766/8767 y ninguna regla de iPhone visible. No se alteró la configuración del teléfono.
- Se preserva el prototipo sin activarlo. No se cambiaron app/, fuente/, Git ni las pruebas de la aplicación. No se ejecutó nuevamente pytest/compileall porque esta intervención solo revisa el estado y actualiza documentación; los últimos resultados aprobados siguen registrados arriba.
- Para iniciar etapa 4 manteniendo pendiente la prueba física de etapa 3 hace falta que Jorge confirme expresamente ese diferimiento, como excepción a la regla de avance del encargo. No se declara realizada ni aprobada la prueba física.


## 2026-10-25 — Inicio autorizado de etapa 4

- Jorge confirmó expresamente iniciar usuarios y roles dejando pendiente la prueba física de etapa 3, como excepción de avance. No se declara realizado ese criterio ni se modifica AGENTS.md.
- Acceso al iPhone suspendido; no se habilitan puertos, certificados ni reglas de firewall. M1 sigue bloqueando el uso real. No se inicia etapa 5 ni se ejecuta Git.
- Alcance: usuarios admin/tecnico, contraseñas bcrypt, sesiones revocables, protección CSRF, asignación de clientes, administración y registro de accesos/emisiones. Sin nuevas dependencias; se reutilizan bcrypt y Flask existentes. Se preservan las cargas y revisiones anteriores mediante migración aditiva.


## 2026-10-26 — Implementación y cierre técnico de etapa 4

- Se conserva la confirmación expresa de Jorge para avanzar con la prueba física de etapa 3 diferida. No se modifica AGENTS.md ni se declara cumplido ese criterio manual. Acceso al iPhone suspendido durante toda la etapa.
- Modelos y migración: Usuario, UsuarioCliente, SesionUsuario y RegistroAcceso; migración 003_usuarios_etapa4.py y versión 3. Nuevas referencias nullable de autor en cargas y revisiones para conservar la historia anterior sin atribuirla a una persona inventada. La migración se probó sobre una carga existente, conservando sus datos y autoría histórica nula.
- Autenticación: login y logout, primer administrador desde la pantalla local de configuración sin credenciales predeterminadas, cambio de contraseña verificando la actual y restablecimiento por administrador. bcrypt con sal individual, factor 12, mínimo 12 caracteres y máximo 72 bytes UTF-8. No se escriben contraseñas en archivos ni se incluyen en respuestas, registros o capturas. Las pruebas generan claves aleatorias en memoria.
- Sesiones: token aleatorio en cookie firmada, solo su hash en PostgreSQL; vencimiento absoluto de 8 horas, cookie HttpOnly/SameSite=Lax, CSRF y rechazo de Origin distinto en escrituras. Logout y reingreso revocan el token previo; cambio/restablecimiento de contraseña, baja o edición de rol/asignaciones revocan las sesiones de la cuenta. Cinco fallos de login en 15 minutos bloquean temporalmente el usuario, con respuesta genérica. No se permite desactivar o degradar al último administrador activo.
- SECRET_KEY proviene del entorno; para la revisión local sin clave configurada se genera en memoria y reiniciar cierra las sesiones anteriores. No se acepta el valor de ejemplo ni claves de menos de 32 caracteres. Cookie Secure configurable por READYPROOF_HTTPS; el entorno actual sigue siendo HTTP restringido a loopback, sin HTTPS ni cambios de certificados.
- Autorización del servidor en toda la API: solo el administrador gestiona cuentas, clientes ficticios y auditoría. El técnico lista y usa clientes asignados. Todas las rutas de carga, historial, borrador, vista previa, finalización, emisión, descarga y recuperación idempotente verifican autorización por cliente; una URL o UUID conocido no evita el control. Las pruebas comprueban tanto consulta como creación/edición y acceso administrativo denegado.
- Interfaz: agregados login.html, cuenta.html, admin.html, cuenta.css, auth.js y admin.js; gestión de altas/bajas lógicas, roles y asignaciones, restablecimiento y creación de clientes/sistemas de ejemplo. Los borradores IndexedDB están separados por usuario; al cambiar de cuenta o vencer la sesión se bloquea la pantalla y la vista previa. Salir retira los borradores de esa cuenta del navegador con advertencia previa sobre cambios pendientes.
- Offline: se conserva el recorrido SAA-1 autenticado, firmas táctiles y recarga sin red. La sesión de la pestaña permite recuperar solo su espacio dentro de las 8 horas. No es posible conocer una revocación del servidor mientras el teléfono está sin conexión; al reconectar, sincronizar/previsualizar/emitir exige permisos vigentes. Este límite está documentado y el entorno continúa prohibido para datos o firmas reales. La cola y los conflictos completos siguen en etapa 8.
- Auditoría: accesos API y eventos de autenticación/cuenta con fecha, usuario, ruta sin cuerpo de solicitud y resultado HTTP. Revisiones con actor autenticado. Cada emisión exitosa guarda usuario, cliente, carga y código de planilla en la misma transacción del PDF; destinatario nulo porque no hay envío en esta etapa. El destinatario efectivo se incorporará con Envio en etapa 5. No se registran secretos ni imágenes de firmas. La prueba real de PDF firmado comprueba el evento de emisión.
- Pruebas: fixtures existentes adaptadas para ingresar por la API sin omitir autenticación; agregado tests/test_auth.py y tests/browser/auth.cjs. Recorrido de navegador para alta desde Administración, asignación de cliente, login técnico sin administración, cierre de sesión y retiro del espacio IndexedDB. Capturas revisadas visualmente en out/etapa4/navegador/; reporte sin errores JavaScript. El recorrido anterior sigue generando PDF firmado de dos páginas.
- Verificación inicial: se corrigió una importación entre pruebas al paquete tests. Primer bloque de API/autenticación: 48 passed in 84.06s (0:01:24). Segundo bloque de seguridad/navegador: 22 passed in 119.12s (0:01:59). Después se ejecutó la suite completa de cierre que figura a continuación.
- Dependencias: ninguna nueva; bcrypt y Flask ya estaban fijados. Sin descargas, servicios externos, correo ni publicación. README.md y docs/USUARIOS_ETAPA4.md documentan inicio, primer administrador, API, seguridad y límites; docs/INTERFAZ_ETAPA3.md remite al login de etapa 4 y .env.ejemplo agrega solo READYPROOF_HTTPS=false con explicación, sin valores reales.
- Revisión local: reiniciado exclusivamente scripts/iniciar_ejemplo.py en 127.0.0.1:8765 y su clúster de ejemplos bajo out/etapa3/demo_local/data, verificando las rutas antes de detenerlos. No se tocó el servicio PostgreSQL habitual. Comprobados esquema [1,2,3], cero cuentas creadas en esa base de revisión, GET /configuracion-inicial = 200 y GET /api/clientes sin sesión = 401. Solo hay escucha en 127.0.0.1:8765; ninguna en 8766/8767. Jorge debe crear su cuenta directamente en la pantalla, no por chat.

Comando con .venv: pytest -q
Entorno: Node.js/Playwright locales; TEMP/TMP dentro de .venv/tmp. Sin descargas.

Salida exacta:
```text
........................................................................ [ 83%]
........x.....                                                           [100%]
85 passed, 1 xfailed in 196.59s (0:03:16)
```
Código de salida: 0. La única xfail sigue siendo la leyenda M1 pendiente, sin cambiar la condición de esa prueba.

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

- Integridad SHA256: 182 archivos de fuente/, auditorias/ y docs/aprobaciones/ idénticos al inicio, sin agregados ni ausencias. Evidencias en out/etapa4/integridad_antes.json e integridad_verificacion.json. No se modificaron generadores ni el formato PDF de la serie.
- No se ejecutó Git ni se hizo commit, conservando la restricción expresa vigente. No se habilitó el prototipo de iPhone ni se cambiaron su seguridad, certificados o firewall.
- Criterio de etapa 4 satisfecho por las pruebas de permisos: técnico sin alta de usuarios ni acceso a registros de cliente no asignado. Implementación técnica lista para revisión local. No se inicia etapa 5.
- Pendientes: prueba física de etapa 3 diferida por Jorge; M1 con Martín antes de uso real; política de campos obligatorios; n1 antes de etapa 6; aviso del formato previo, metadatos, integridad del kit y ediciones normativas. Configuración del runner npm también sigue pendiente por la indicación de no crear playwright.config.js.


## 2026-10-26 — Alcance actualizado: Manual y modelos previos al correo

- Jorge reemplazó el inicio del transporte de correo por dos partes: modelo Manual y vínculo de SAA-1 primero; luego únicamente Envio, Intento y Retencion con relaciones y pruebas, sin SMTP real. La operación anterior de creación de modelos de correo fue rechazada y no dejó archivos ni cambios; comprobado app/correo.py vacío, sin migración 004 ni manifiesto de etapa 5.
- Se requiere Alembic por indicación expresa. No está instalado ni tiene una rueda local cacheada. Se justifica incorporarlo como herramienta de migraciones con versión fijada, junto con Mako, su dependencia. La descarga desde PyPI requiere la excepción de red correspondiente; no se usará ningún servicio de datos ni credenciales.
- Manual contendrá únicamente texto ficticio marcado como [Ejemplo], sin procedimientos normativos copiados. campos_obligatorios será una lista vacía pendiente de confirmación y no cambiará la validación vigente ni declarará opcionales todos los campos.


## 2026-10-26 — Manual y modelos previos al servicio de correo

- Parte 1 terminada: Manual con PK UUID nativa PostgreSQL, codigo String(60) único, titulo String(255), sistema_tipo String(12), contenido Text, campos_obligatorios JSON/lista y version String(30). Se mantiene además UNIQUE(codigo,version), exactamente como se solicitó; su redundancia y efecto sobre futuras versiones se anotan en preguntas abiertas, sin quitar restricciones por cuenta del desarrollo.
- Planilla agrega manual_id UUID/FK nullable y relación planilla.manual; Manual.planillas permite el vínculo inverso. SAA-1 existente y la de un catálogo nuevo quedan vinculadas a SG-PEM-IFI-SAA-EJEMPLO, título [Ejemplo] Sistema de Abastecimiento de Agua, versión v1. El contenido es solo un marcador ficticio, sin copia de procedimiento normativo. campos_obligatorios=[] conserva pendiente la política; no se alteran los datos fuente ni la validación vigente. manual_id deberá ser obligatorio antes del uso real.
- Parte 2 terminada al alcance pedido: Envio con UUID, carga_id, destinatario(255), enviado_en nullable, ENUM pendiente/enviado/fallo/descartado y creado_en; Intento con UUID, envio_id, numero, intentado_en, resultado(60) y respuesta Text opcional; Retencion con UUID, envio_id, reintentado_en nullable, proximos_intentos(0..2) y razon(255). Relaciones de Carga a envíos y de Envio a intentos/retenciones, con ON DELETE CASCADE en las tres FKs solicitadas. Número de intento positivo y único por envío y valores permitidos controlados por la base.
- Retencion representa la programación de reintentos según sus campos; no sustituye la conservación documental de tres años desde la emisión. Las cascadas solo se probaron en bases temporales ficticias. No se agregó ninguna ruta de borrado ni se eliminaron registros de la base de revisión.
- Alembic: agregado alembic.ini sin URL ni claves y entorno en migraciones/alembic/. Cadena 003_base_etapa4 → 004_manual → 005_correo_modelos. La base de etapa 4 preservada en migraciones/base_etapa4.py permite reconocer instalaciones existentes e iniciar bases nuevas, conservando los marcadores históricos 1..3. app/db.py aplica el bootstrap compatible y las revisiones Alembic; registra 4 y 5 sin usar create_all para incorporar silenciosamente las tablas nuevas. Downgrades destructivos bloqueados. Se comprobó la actualización desde una base de etapa 4, el vínculo de la planilla y la idempotencia.
- Dependencias justificadas por la migración pedida: Alembic==1.14.1 y Mako==1.3.10 agregadas a requirements.txt. Con autorización puntual de red, comando .venv\Scripts\python.exe -m pip --isolated install --index-url https://pypi.org/simple alembic==1.14.1 Mako==1.3.10. Resultado exacto final: Successfully installed Mako-1.3.10 alembic-1.14.1. No se actualizaron otros paquetes, no se usaron servicios externos de datos y se continuó sin red después de esa descarga.
- Pruebas nuevas en tests/test_modelos_manual_correo.py: título desde planilla.manual, nullable actual, unicidad, migración con datos previos, UUID, relaciones y cascadas, FK inválida, estados y límites de intento/retención. Comparación Alembic/ORM sin diferencias. Los constructores SMTP/SMTP_SSL están bloqueados en la prueba de creación; no se transmite nada. Primer bloque: 14 passed in 30.86s.
- Ejemplo local actualizado reiniciando solo scripts/iniciar_ejemplo.py y su clúster de out/etapa3/demo_local/data, verificando sus rutas/procesos antes de detenerlos. No se tocó el servicio PostgreSQL habitual ni las cuentas. Verificación: alembic_version=005_correo_modelos, versiones [1,2,3,4,5], SAA-1.manual.titulo correcto, cero envíos y HTTP local 200.
- Documentación: docs/MODELOS_MANUAL_CORREO.md y sección de README. PREGUNTAS_ABIERTAS.md incorpora el encabezado exacto «2026-10-26 — Inicio de etapa 5: correo y envío», los modelos y los resultados. Se conserva el historial anterior.

Comando con .venv: pytest -q
Entorno: PostgreSQL temporal, Node.js/Playwright locales y TEMP/TMP en .venv/tmp; sin SMTP ni nuevas descargas.

Salida exacta:
```text
........................................................................ [ 72%]
........x...................                                             [100%]
99 passed, 1 xfailed in 216.99s (0:03:36)
```
Código de salida: 0. La xfail sigue correspondiendo a M1.

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

- Integridad SHA256: 182 archivos protegidos de fuente/, auditorias/ y docs/aprobaciones/ sin cambios, ausencias ni agregados. Evidencias en out/modelos_manual_correo/. AGENTS.md no se modificó. No se ejecutó Git.
- No se implementó el transporte de correo: app/correo.py sigue vacío; no hay archivo .eml, reintento automático, copia de correo/PDF específica de envío ni envío SMTP/API. La etapa 5 completa permanece en progreso; esta entrega cumple solo las dos partes de modelos solicitadas. Antes de cualquier prueba real siguen pendientes M1, configuración por una persona y verificación autorizada de SPF/DKIM. El acceso al iPhone continúa suspendido y no se inicia etapa 6.


## 2026-10-26 — Etapa 6: inventario previo y diferencias detectadas

- Comando de inventario en Python: contar archivos regulares con Path('fuente').rglob('*'), localizar los cuatro nombres JSON y comprobar fuente/planillas/. Resultado: 173 archivos, carpeta ausente y ninguno de los cuatro JSON encontrados. Los 32 archivos esperados no corresponden a esta copia. Manifiesto e inventario en out/etapa6_inventario/.
- Cotejo por lectura de AGENTS.md y fuente/KIT_AGENTS.md: los títulos de SDI/SBC/SAL solicitados difieren de los códigos de la serie. Se registraron la tabla de archivos ausentes y dos consultas a Jorge sobre fuente y títulos en PREGUNTAS_ABIERTAS.md.
- Se detiene la carga y la migración hasta aclarar los datos de entrada, conforme a la regla de contradicciones del encargo. No se crean JSON, manuales, importador ni pruebas que simulen la presencia de archivos inexistentes; no se marca ✓ OK ni se promete una cantidad de pruebas sin ejecutarlas.
- Sin cambios de código de aplicación, fuente/, base de datos, Git, secretos, acceso al iPhone o servicios externos. La etapa 6 no se declara completada y el correo completo sigue pendiente según el alcance anterior.


## 2026-10-26 — Preparación etapa 6: conversión y validación JSON

- Jorge aclaró la tarea: convertir los datos Python a cuatro JSON antes de auditar/cargar etapa 6. Autorizó expresamente los agregados bajo fuente/planillas/, preservando los originales, y confirmó los títulos del kit con prefijo [Ejemplo] para los futuros manuales. Se resuelven las dos consultas del inventario previo.
- Agregado scripts/convertir_planillas_json.py. Comando con .venv: python scripts/convertir_planillas_json.py. Resultado: SDI.json, SBC.json, SAL.json y SAA-1.json creados y equivalentes al dato Python. No se sobrescriben archivos existentes distintos y --verificar no escribe.
- Convertidos SISTEMAS[SDI], SISTEMAS[SBC] y SISTEMAS[SAL] completos de planillas_data2.py: 5, 6 y 4 planillas respectivamente. SAA-1 se extrae de la definición número 1 de SISTEMAS[SAA] en planillas_data3.py. Se conserva el orden de bloques, filas, opciones y unidades; no se agregan ni interpretan requisitos normativos.
- Contenedor JSON: codigo/version v1/sistema_tipo, procedencia y huellas SHA256, cabecera común del adaptador existente, datos del sistema y firmas con las etiquetas del pie extraídas del generador mediante AST. Tuplas representadas como arrays JSON sin perder orden. Un adaptador futuro deberá recuperar los tipos estructurales para llamar al generador; no se alteró este ni se declaró generación nueva de PDF.
- Archivos creados: fuente/planillas/SAA-1.json, SDI.json, SBC.json y SAL.json. Comando python -m json.tool sobre cada archivo con salida a $null en PowerShell: los cuatro terminaron con código 0. Comando python scripts/convertir_planillas_json.py --verificar: los cuatro equivalentes al dato Python, código 0.
- Inventario: SAA-1 = 11 campos de cabecera, 22 ítems de datos y 2 firmas; SDI = 11/129/2; SBC = 11/183/2; SAL = 11/55/2. Cabecera y firmas son comunes por planilla; datos suma los ítems de los bloques del grupo sin multiplicar meses/períodos. Tabla con estado ✓ OK en PREGUNTAS_ABIERTAS.md y detalle en out/etapa6_inventario/inventario_convertido.json.
- Recuento equivalente a find fuente -type f | wc -l mediante Path.rglob/is_file: 173 originales + 4 JSON = 177 archivos. No se fuerza el número 36 porque el inventario inicial de esta copia era 173, no 32. Todos los originales mantienen SHA256 después de ejecutar la suite; los únicos cuatro agregados son los autorizados. Manifiestos y auditoría de preparación en out/etapa6_inventario/.
- Agregado tests/test_preparacion_etapa6.py: cuatro casos de JSON válido sin claves duplicadas, equivalencia con Python y hashes de procedencia/generador; un caso de cuatro archivos exactos, grupos completos y conservación de orden/cantidad de filas. Sin dependencia de archivos de out/ para ejecutar las pruebas desde una copia limpia. La suite mantiene las pruebas de usuarios, API, generación, firmas y modelos.
- Documentación de estructura, conversión y alcance en docs/PREPARACION_ETAPA6_JSON.md. PREGUNTAS_ABIERTAS.md incluye el encabezado de preparación, los títulos confirmados y Listo para etapa 6, referido a los datos JSON disponibles.

Comando con .venv: pytest -q
Entorno: dependencias locales existentes, PostgreSQL temporal y TEMP/TMP en .venv/tmp. Sin red ni SMTP.

Salida exacta:
```text
........................................................................ [ 68%]
........x........................                                        [100%]
104 passed, 1 xfailed in 253.62s (0:04:13)
```
Código de salida: 0. La xfail sigue correspondiendo a M1.

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

- Alcance de cierre: preparación JSON terminada y auditada en sintaxis/equivalencia/integridad. La migración 006, los tres manuales y el importador de etapa 6 siguen para la auditoría/carga posterior solicitada; no se modificó el catálogo de la base. No se declara completada la etapa 6 funcional ni cotejados los PDF de SDI/SBC/SAL. n1 deberá resolverse antes de comparar formatos de otras planillas.
- Sin Git, secretos, dependencias nuevas, correo real ni cambios de certificados/firewall/acceso al iPhone. M1, la prueba física diferida y el transporte de etapa 5 continúan pendientes.


## 2026-10-26 — Etapa 6: carga JSON, manuales y logo

- Jorge autorizó cargar el catálogo de cuatro JSON, vincular manuales y reemplazar el logo del PDF sin modificar fuente/. Se preserva el manifiesto inicial de 177 archivos y las auditorías/aprobaciones en out/etapa6/integridad_antes.json.
- Primero se inspeccionó el PDF indicado en Descargas con pypdf: una página y una imagen compuesta de toda la lámina. La operación de recorte siguiente fue rechazada antes de ejecutarse; después Jorge proporcionó el PNG Readyproof — Mantenimiento@2x.png y se usó ese archivo como origen definitivo. Se recortó el logo principal completo, incluyendo Mantenimiento y auditoría y Grupo BFM, sin textos explicativos ni instrucciones de la lámina. No se interpretaron sus textos como instrucciones del encargo.
- app/static/logo_readyproof.png: PNG RGB de 926×312, 24580 bytes. app/planillas/firmas.py lee y valida el archivo; convertir_pdf lo pasa a reponer_logos, que reemplaza el recurso izquierdo respetando proporción y espacio originales. El sello derecho, filas, pie, encabezado textual y fuente/ permanecen sin cambios. Los documentos ya emitidos no se reescriben.
- Migración 006_etapa6_planillas.py en migraciones/alembic/versions/, la ruta configurada por el proyecto. Inserta cuatro manuales con uuid4, títulos [Ejemplo] confirmados, sistema_tipo SG-PEM-IFI, contenido ficticio, lista vacía de campos obligatorios y versión v1. Conserva el manual anterior SG-PEM-IFI-SAA-EJEMPLO. No se usa una carpeta Alembic paralela sin configurar.
- Reversión segura: no se usa DELETE por prefijo SG-PEM-IFI-%, que también afectaría manuales de etapas previas. La reversión solo considera los cuatro códigos/versiones originales de esta revisión, exige que sigan siendo los ficticios insertados y se bloquea si están vinculados. Probada en bases temporales, conservando el manual anterior. No se borró ningún registro de la base de revisión.
- app/carga_planillas.py: cargar_planillas_desde_json(session) lee solo los cuatro JSON, valida metadatos y cabecera/datos/firmas, calcula SHA256 del JSON canónico con json.dumps(...,sort_keys=True).encode(), encuentra el manual exacto y confirma una transacción. Idempotente y sin sobrescribir definiciones existentes distintas; los conflictos requieren nueva versión. No ejecuta definiciones Python al importar JSON.
- init-db carga el catálogo si la tabla de planillas está vacía; cargar-planillas permite importación explícita en una base existente. scripts/iniciar_ejemplo.py usa el mismo inicio y ofrece --cargar-planillas. El piloto SG-PEM-IFI-SAA-1, versión 00-26, conserva su esquema, huella y manual anteriores; los cuatro contenedores JSON son filas v1 separadas. Total previsto en el ejemplo: cinco filas y ningún manual_id nulo.
- Agregadas las siete pruebas nominales pedidas en tests/test_etapa6_planillas.py y cuatro controles adicionales: idempotencia/sin sobrescritura, JSON inválido sin carga parcial y dos casos de downgrade seguro. Primer bloque: 11 passed in 33.82s. Los tests existentes seleccionan explícitamente el piloto para no confundirlo con los nuevos contenedores y verifican la idempotencia del catálogo de cinco filas.
- El PDF de prueba con logo se reabrió con pypdf y se renderizó en dos páginas con pypdfium2 local. Verificación por píxeles de la imagen incrustada y revisión visual de ambas páginas: logo completo, sin recorte/deformación ni superposición. Evidencias en out/etapa6/SAA-1_readyproof.pdf y SAA-1_pagina_1.png/2.png.


### 2026-10-26 — Verificación final de carga y logo

- Ejemplo local actualizado con scripts/iniciar_ejemplo.py --port 8765 --cargar-planillas. Se detuvo únicamente su proceso y clúster tras verificar identidad/ruta; el servicio PostgreSQL habitual no se modificó. Salida: Catálogo JSON verificado; 4 planillas nuevas. Servicio solo en 127.0.0.1:8765.
- Base local: revisión 006_etapa6_planillas. Filas v1 SAA-1/SDI/SBC/SAL con sus cuatro manuales nuevos; fila piloto SG-PEM-IFI-SAA-1 00-26 con el manual anterior. Cinco filas y cinco manuales en total; todas las planillas tienen manual_id. El término cinco vínculos del catálogo no se confunde con las cinco clases de relaciones verificadas por Jorge; ambas comprobaciones constan en auditoria_final.json.
- Inspección de FKs confirma Planilla→Manual, Envio→Carga, Intento→Envio, Retencion→Envio y los dos enlaces de UsuarioCliente a Usuario/Cliente. No se modificaron las relaciones de correo o usuarios en esta tarea.
- Revisión de secretos: búsqueda de password/token/smtp en app/*.py arroja 32 coincidencias legítimas de código. Inspección AST de asignaciones literales a nombres de credenciales: ningún candidato. Se revisaron los archivos nuevos sin valores reales; no se promete cero coincidencias de palabras que forman parte de la autenticación. No se leyeron ni publicaron valores del .env.

Comando con .venv: pytest -q
Entorno: PostgreSQL temporal, Node.js/Playwright locales y TEMP/TMP en .venv/tmp, sin SMTP ni red.

Salida exacta:
```text
........................................................................ [ 62%]
...................x........................                             [100%]
115 passed, 1 xfailed in 292.33s (0:04:52)
```
Código de salida: 0. La xfail sigue siendo M1; no se cambió ni ocultó esa prueba.

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

- Integridad: 177 archivos en fuente/ y 186 protegidos en el manifiesto completo sin diferencias, archivos ausentes ni agregados. Evidencia en out/etapa6/auditoria_final.json. Se conserva la cifra medida frente a la referencia de 32 archivos del mensaje de autorización.
- Actualizados y releídos REGISTRO_DE_CAMBIOS.md y PREGUNTAS_ABIERTAS.md, con el encabezado solicitado y los resultados. README y docs/ETAPA6_PLANILLAS_LOGO.md explican inicialización, importación de una base existente, conservación del piloto y reversión segura.
- Entregable visual: out/etapa6/SAA-1_readyproof.pdf, dos páginas con logo completo; renders comprobados en SAA-1_pagina_1.png y SAA-1_pagina_2.png. Activo estático validado y procedencia del PNG documentada. El PDF de marca y el PNG proporcionados por Jorge se conservan sin modificación.
- Sin Git, secretos, nuevas dependencias, envío de correo, publicación, alteración de fuente/ ni acceso al iPhone. No se inicia etapa 7. Se completó el alcance específico de catálogo/vínculos/logo; generación y cotejo de las planillas individuales de los nuevos grupos siguen pendientes, junto con n1, M1 y el resto ya registrado.


## 2026-10-26 — Muestra de marca de agua con readyproof e ISO

- Ante la consulta de Jorge se preparó una muestra independiente en out/etapa6/SAA-1_marca_agua.pdf. Usa el PNG completo de readyproof y el sello derecho original del modelo Excel, centrados y con opacidad 5,5 %. Se conservan los logos del encabezado.
- PDF escrito con pypdf, mezcla Multiply para preservar los textos/líneas y ajuste proporcional. Comprobaciones: dos páginas, texto extraído exactamente igual al PDF anterior, cuatro imágenes por página y hash del PDF original sin cambios. Renders revisados visualmente en marca_agua_pagina_1.png y marca_agua_pagina_2.png; no hay texto oculto ni logos recortados.
- Solo es una muestra para revisión: no se modificó la generación automática, app/, fuente/, la base de datos ni Git. Verificación específica de PDF en marca_agua_verificacion.json. No se repitió pytest/compileall porque no hubo cambios de código; los últimos resultados de aplicación siguen siendo 115 passed, 1 xfailed y compilación código 0.


## 2026-10-26 — Marca de agua aprobada e integrada

- Jorge aprobó la muestra y pidió continuar. Se incorpora automáticamente readyproof completo e ISO en todas las páginas de los nuevos PDF generados por convertir_pdf, incluida vista previa y emisión. Opacidad aprobada 5,5 %, ubicación/proporciones iguales a la muestra y mezcla Multiply para conservar textos y líneas. No se modifican PDF ya guardados.
- Agregado app/planillas/marca_agua.py. Reutiliza los recursos de imagen del encabezado en lugar de duplicar imágenes; cada logo se dibuja una vez en el encabezado y una vez en la marca de agua. Estado gráfico aislado con q/Q, indicador en metadatos y rechazo de doble aplicación.
- Flujo: conversión → encabezado con logo readyproof → marcas de agua → firmas, para que las firmas conserven su intensidad. Sin modificaciones a fuente/, formato Excel, márgenes, filas ni leyendas.
- Agregada prueba test_marca_agua.py de incorporación automática, opacidad, recursos reutilizados y protección contra doble aplicación. Las pruebas de API de firmas ahora verifican también las marcas tanto en la vista previa como en el PDF emitido. Los conteos previos de imágenes siguen válidos porque se reutilizan recursos.


### 2026-10-26 — Verificación y activación de marca de agua automática

- Bloque específico: 10 passed in 50.22s. Incluye generación automática, recursos y opacidad, rechazo de doble aplicación y verificación en vista previa/emisión con firmas. Revisadas visualmente ambas páginas renderizadas del PDF automático: mismas proporciones y ubicación de la muestra aprobada, textos y líneas legibles, sello y logo de encabezado conservados.
- Reiniciado solo scripts/iniciar_ejemplo.py y su clúster aislado, tras comprobar identidad/rutas. Servicio de revisión actualizado en 127.0.0.1:8765, HTTP 200. No se modifica PostgreSQL habitual, fuente/, permisos, cuentas, firewall ni el acceso suspendido al iPhone.
- Los PDF emitidos y almacenados en la base no se reprocesan; las muestras de out/ son artefactos de las pruebas. La marca se aplica a nuevas vistas previas y emisiones. Los mismos recursos de imagen se dibujan dos veces sin aumentar los mapas de bits: dos imágenes por página sin firmas y cuatro en la página firmada.

Comando con .venv: pytest -q
Entorno: PostgreSQL temporal, Node.js/Playwright locales y TEMP/TMP en .venv/tmp; sin red ni SMTP.

Salida exacta:
```text
........................................................................ [ 61%]
...................x.........................                            [100%]
116 passed, 1 xfailed in 257.49s (0:04:17)
```
Código de salida: 0. La única xfail sigue siendo M1.

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

- Integridad después de la suite: 177 archivos de fuente/ y 186 archivos protegidos del manifiesto anterior conservan sus huellas. Auditoría en out/etapa6/marca_agua_automatica/auditoria.json; PDF automático y renders en la misma carpeta.
- Actualizados y releídos los registros y docs/ETAPA6_PLANILLAS_LOGO.md. Sin dependencias nuevas, secretos, Git, publicación ni etapa 7. M1 y los pendientes de generación/cotejo de nuevos grupos y correo continúan abiertos.


## 2026-10-26 — Confirmación de JSON de etapa 6

- Verificados en modo lectura SAA-1.json, SDI.json, SBC.json y SAL.json en fuente/planillas/. Todos ya existían y contienen los seis apartados requeridos; codigo, version v1 y sistema_tipo SG-PEM-IFI coinciden. No se activa la conversión condicional ni se sobrescribe fuente/.
- Comando con .venv: python -m json.tool fuente/planillas/{archivo}.json, salida a $null en PowerShell. Los cuatro códigos de salida son 0.
- Comando con .venv: pytest tests/test_etapa6_planillas.py::test_todas_las_planillas_tienen_manual -v. Resultado: PASSED, 1 passed in 12.69s, código 0. Esta prueba se ejecuta en PostgreSQL temporal con cinco filas y cero manual_id nulos.
- Verificación adicional de solo lectura en el ejemplo local: cuatro contenedores JSON v1 vinculados y con sus huellas canónicas correctas, más el piloto anterior preservado; cinco planillas y ninguna sin manual. Informe en out/confirmacion_etapa6/verificacion_bd.json.
- Manifiesto inicial de los 177 archivos de fuente/ en out/confirmacion_etapa6/integridad_antes.json. El recuento real incluye los JSON; no es 32. Sin secretos, Git, datos reales ni cambios de fuente/ o de código. Se ejecuta la suite completa y compileall para registrar el cierre solicitado.


## 2026-10-26 — Recepción de tarea condicional M1

- Recibidas instrucciones para agregar la leyenda después de confirmar con Martín texto, ubicación, formato y páginas. Es una instrucción futura condicionada; aún no se recibió esa confirmación.
- No se cambia app/planillas/pdf.py, no se agrega una leyenda tentativa ni se modifica la prueba xfail. No se registra M1 como resuelto ni el PDF como apto para cliente real. Los valores de ejemplo de la instrucción no se interpretan como decisiones normativas.
- Actualizado PREGUNTAS_ABIERTAS.md con los datos a confirmar y el plan de verificación posterior. Se conserva la verificación de JSON en curso y los demás bloqueos de uso real.


### 2026-10-26 — Cierre de confirmación JSON

- Los cuatro JSON preexistentes son válidos y se confirman cinco planillas vinculadas, cero manual_id nulos y huellas correctas, tanto en la prueba como en el ejemplo local. fuente/: 177 archivos con SHA256 idénticos al inicio; no se crearon ni movieron JSON.
- Comando con .venv: pytest -q. Salida exacta:
```text
........................................................................ [ 61%]
...................x.........................                            [100%]
116 passed, 1 xfailed in 271.16s (0:04:31)
```
Código de salida: 0. Esta ejecución es anterior a implementar M1 y conserva su xfail.
- Comando con .venv: python -m compileall app. Salida exacta:
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
Código de salida: 0. Sin cambios de fuente/, código de aplicación, Git o credenciales en esta confirmación.

## 2026-10-26 — Parámetros definitivos de M1 confirmados

- Jorge informó la confirmación de Martín y respondió Correcto a la especificación completa: Planilla conforme a IRAM 3546:2011, centrada en el pie a 10 mm del borde inferior, Helvetica 8 pt, gris 50 %, todas las páginas. Quedan resueltos los datos pendientes de diseño de la leyenda.
- Se verifica el espacio antes de incorporar la leyenda y se mantendrán las filas y el formato del kit. M1 se cerrará solo después de implementar y verificar el PDF y convertir su xfail en prueba normal; los demás controles de uso real siguen vigentes.


### 2026-10-26 — Implementación M1 y ajuste del pie autorizado

- Detectada colisión real: OBSERVACIONES en primera página y=23,62 pt; la ubicación aprobada de 10 mm equivale a y=28,35 pt. Jorge autorizó explícitamente reservar el pie reduciendo proporcionalmente cerca del 5 % el contenido, sin modificar fuente/, A4, páginas ni filas.
- app/planillas/leyenda_iram.py aplica escala 0,95 al contenido y agrega al final la leyenda exacta, centrada, Helvetica 8 pt, gris 50 %, todas las páginas. El texto del pie no se escala. Se utiliza pypdf y métricas AFM Helvetica disponibles localmente, incluidas como datos para la frase fija, sin nueva dependencia de ReportLab ni red. Se rechaza la doble aplicación.
- Integrada después de logos, marcas de agua y firmas. La pantalla muestra la leyenda confirmada; los avisos obsoletos de M1 pendiente se actualizan sin quitar las validaciones que limitan el entorno a ejemplos. Se renueva la caché de pantalla del service worker.
- La xfail M1 se reemplaza por test_pdf_contiene_leyenda_iram_confirmada, con una aparición en cada página. Nuevas verificaciones de tamaño/fuente/posición/gris, espacio libre, A4, páginas, metadatos y duplicación. Bloque de M1/generación: 24 passed in 37.08s.
- n1: comparación de encabezado/pie por anclas de contenido y altura tipográfica; se eliminan límites fijos 126/70/130 pt y x=0,82 del ancho. Una prueba desplaza y escala el PDF y confirma regiones equivalentes. Se corrige la observación de coordenadas fijas; sigue pendiente generar/cotejar los otros grupos.
- Revisados visualmente ambos renders: leyenda legible en el pie, separada de OBSERVACIONES, sin recortes de filas, logos o firmas y con marcas de agua conservadas. Evidencia en out/etapa_m1/SAA-1_con_leyenda.pdf y pagina_1.png/pagina_2.png. Documentación vigente actualizada; auditorías y aprobaciones históricas no se modifican.


### 2026-10-26 — Cierre M1 resuelto

- Confirmación de texto/formato por Martín comunicada y ratificada por Jorge; ajuste del pie 5 % autorizado expresamente. Implementación y revisión visual completadas con texto exacto, pie centrado a 10 mm, Helvetica 8 pt y gris 50 %, todas las páginas, después de logos/marcas/firmas. M1 deja de ser xfail.
- Primera suite completa: 119 passed in 260.12s (0:04:20), código 0. Después se afinó la detección de doble aplicación para usar el identificador de leyenda y permitir que las observaciones contengan la frase. Regresión específica: 1 passed in 9.65s. La suite completa se repitió sobre esa versión final.
- n1: eliminadas coordenadas fijas de comparación en test_generacion; extracción por anclas FECHA/CUMPLE y tipografía con regresión de escala/posición. No cambia el generador ni afirma cotejados los PDF de otros grupos.

Comando con .venv: pytest -q
Entorno: PostgreSQL temporal, Node.js/Playwright locales y TEMP/TMP en .venv/tmp. Sin red ni SMTP.

Salida exacta:
```text
........................................................................ [ 60%]
................................................                         [100%]
120 passed in 280.99s (0:04:40)
```
Código de salida: 0. Sin xfail ni fallos.

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

- Auditoría final: leyenda una vez en cada página, fuente /Helvetica, tamaño 8 pt, y=28,346457 pt (10 mm), centrado comprobado; metadatos con texto y ajuste de pie, A4 y dos páginas. Renders pagina_1.png/pagina_2.png y texto_extraido.txt en out/etapa_m1/. Documento de revisión SAA-1_con_leyenda.pdf.
- Pantalla actualizada con la frase y avisos sin M1 pendiente, caché renovada. Restricciones de clientes/datos ficticios conservadas y mensaje de bloqueo actualizado para no atribuirlo a M1 ya resuelto. Documentación vigente ajustada y detalle en docs/LEYENDA_IRAM_M1.md; archivos de auditorías/aprobaciones históricas sin cambios.
- Reiniciado únicamente el servidor y clúster del ejemplo local, tras validar procesos/ruta; HTTP 200 en 127.0.0.1:8765. No se tocó el servicio PostgreSQL habitual, .env, cuentas ni infraestructura externa. PDF emitidos guardados no se reprocesan.
- Integridad al terminar la suite: 177 archivos de fuente/ y 186 archivos protegidos mantienen sus SHA256, sin agregados/ausencias. Sin Git, secretos ni dependencias nuevas. PREGUNTAS_ABIERTAS.md incorpora el encabezado M1 RESUELTO: 2026-10-26 y ambos registros se releen.
- M1 resuelto para la leyenda; el sistema sigue en modo de ejemplo por los demás pendientes registrados. No se declara habilitado el uso real ni se avanza de etapa automáticamente.


## 2026-10-26 — Transporte SMTP Gmail: inicio autorizado

- Jorge pidió implementar el transporte con Gmail readyproof.ar@gmail.com, contraseña de aplicación cargada por él en .env.local, endpoint y reintentos de 15 minutos con tres intentos máximos. Esta decisión explícita sustituye cPanel para esta implementación; AGENTS.md no se modifica. La numeración Etapa 7 es la del pedido actual: el encargo original llama etapa 5 al correo y etapa 7 a informes, que siguen pendientes.
- .env.local agregado a .gitignore sin abrir ni modificar su contenido. No se ejecuta Git. La aplicación leerá las variables en ejecución; el agente no muestra ni copia contraseñas. Los tests no cargarán .env.local y usarán credenciales aleatorias y SMTP simulado.
- Se conserva modo de prueba por defecto y no se realizará un envío real durante este trabajo. Activar SMTP requerirá configuración explícita y destinatario de prueba permitido; el proceso periódico será independiente y no arrancará por importar la aplicación.

### Implementación y comprobación focalizada

- Convertido el módulo vacío app/correo.py en el paquete app/correo/, con send_email(), cola, transporte STARTTLS 587, copia PDF/EML y huellas. Credenciales obtenidas solo de variables en ejecución; respuestas SMTP saneadas. La migración aditiva 007 conserva datos y agrega copias, actor, retención mínima de tres años y reserva durable del máximo de tres intentos. No instala dependencias.
- POST /api/cargas/<uuid>/enviar conserva autenticación, CSRF y acceso por cliente; exige emitida, huella PDF y leyenda confirmada, prepara el archivo y responde 202 pendiente. Los clientes siguen siendo ficticios. El worker se ejecuta aparte cada 900 segundos, con reintentos a 15 minutos y revisión de permisos; no se inicia automáticamente ni se activó aquí.
- Modo archivo por defecto y forzado en el lanzador de ejemplos. Los fallos permanentes y aceptación desconocida durante DATA quedan bloqueados, sin duplicar envíos. Un bounce posterior se registra manualmente con administrador activo; SMTP no permite detectar por sí solo la entrega final ni leer esos avisos.
- Documentados contraseña de aplicación, prioridad de variables/.env.local/.env, comandos y límites en docs/SMTP_GMAIL.md, con enlaces a las fuentes oficiales de Google consultadas públicamente. Sin acceso a cuentas ni envío real. README.md y .env.ejemplo agregan la referencia MAIL_FROM vacía; .env.local no fue abierto ni escrito.
- Prueba focalizada: python -m pytest tests/test_smtp_gmail.py tests/test_modelos_manual_correo.py -q --disable-warnings --maxfail=2. Resultado final: 30 passed in 57.00s, código 0, evidencia out/smtp_gmail/pytest_focal.log. En las iteraciones iniciales se corrigieron el nombre del helper de leyenda del fixture y la distinción entre remitente configurado/fallback ficticio; no hubo SMTP real. Luego se agregaron pruebas de concurrencia, 450, corte en QUIT, rollback y sesión, incluidas en la suite completa.
- python -m compileall app: código 0. python -m pip --isolated check: No broken requirements found., código 0. Huellas de los 186 archivos protegidos idénticas, 177 archivos de fuente/ sin cambios. Exclusión de .env.local verificada sin Git y sin abrirlo; revisión AST sin asignaciones literales a variables sensibles.

### Cierre de la implementación SMTP Gmail — 2026-10-26

Comando: .venv\Scripts\python.exe -m pytest -q

Entorno: PostgreSQL temporal aislado, SMTP sustituido y bloqueo global de conexiones SMTP en los tests; Node.js/Playwright locales. TEMP/TMP en .venv/tmp y NODE_PATH del runtime local. Sin credenciales reales ni correo real.

Salida exacta:
```text
........................................................................ [ 51%]
.....................................................................    [100%]
141 passed in 319.28s (0:05:19)
```
Código de salida: 0. Sin xfail.

Comando: .venv\Scripts\python.exe -m compileall app

Salida exacta:
```text
Listing 'app'...
Listing 'app\\auth'...
Listing 'app\\correo'...
Listing 'app\\models'...
Listing 'app\\planillas'...
Listing 'app\\planillas\\definiciones'...
Listing 'app\\rutas'...
Listing 'app\\static'...
Listing 'app\\templates'...
```
Código de salida: 0.

Comando: .venv\Scripts\python.exe -m pip --isolated check

Salida exacta:
```text
No broken requirements found.
```
Código de salida: 0.

- 21 pruebas nuevas de correo dentro del total de 141. Se cubren credenciales desde variables, TLS con certificado validado, adjunto idéntico al PDF, intentos, máximo tres, 450, rechazos/autenticación, aceptación ambigua, QUIT posterior a aceptación, concurrencia de workers, modo archivo, sesión, validación de destinatario, permisos revocados, bounce, reserva interrumpida, rollback y exclusión de los archivos de entorno durante pruebas.
- Reiniciado únicamente el ejemplo en 127.0.0.1:8765 y su clúster propio, validando antes PID, comando y ruta absoluta dentro del proyecto. Migración 007 aplicada, versiones 1 a 7 comprobadas, HTTP 200. No se tocó el servicio PostgreSQL habitual ni se inició correo-worker. El lanzador fuerza MAIL_MODO_PRUEBA=True. Los datos guardados del ejemplo se conservan; los PDF históricos no se reprocesan.
- Auditoría posterior a la suite: 177 archivos de fuente/ y 186 protegidos con SHA256 idénticos al inicio. Sin modificaciones a AGENTS.md, fuente/, auditorias/ ni docs/aprobaciones/. Sin Git, dependencias nuevas ni secretos escritos. .env.local ignorado y no abierto por las herramientas. Solo la aplicación lo carga en ejecución normal; TESTING no lo carga.
- Pendiente: prueba SMTP real a casilla de prueba expresamente autorizada, confirmar autenticación/entregabilidad Gmail y activar un proceso periódico operativo cuando corresponda. Los bounces posteriores se registran manualmente. Retener_hasta y copias no sustituyen los controles operativos de respaldo, acceso y borrado administrativo. Continúan los demás pendientes de uso real, informes -IN y planillas nuevas; no se avanza de etapa.

## 2026-10-26 — Preparación de configuración Gmail local

- A pedido de Jorge se comprobó la configuración sin mostrar credenciales. No existía .env.local en C:\Users\jorge\Readyproof. Se creó exclusivamente ese archivo con smtp.gmail.com, STARTTLS 587, la cuenta/remitente autorizados y MAIL_MODO_PRUEBA=true. SMTP_PASSWORD queda vacío para que Jorge lo complete directamente en su equipo. Exclusión .env.local comprobada en .gitignore; sin ejecutar Git.
- No hubo conexión SMTP, autenticación ni envío real. No se inició el worker ni se modificó fuente/. Esta operación solo prepara configuración: no implica que Gmail esté autenticado. Pendiente completar la contraseña de aplicación y validar luego con casilla de prueba autorizada.

## 2026-10-26 — Apertura de Gmail y límite del control de pantalla

- Jorge pidió operar con el cursor y abrir Gmail para configurar la cuenta readyproof. Se leyeron las instrucciones de control de pantalla y PASOS_SERVICIO_FINAL_readyproof.md.
- No se pudo inicializar el control de pantalla; error exacto: failed to write kernel assets: El sistema no puede encontrar la ruta especificada. (os error 3). El reinicio del kernel no resolvió el fallo. No se realizaron clics, autenticación ni cambios en la cuenta.
- Se solicitó a Windows abrir Gmail en el navegador predeterminado para la cuenta indicada, sin contraseñas ni códigos. La apertura visual y la sesión no pudieron verificarse por el fallo del control. No hubo envío de correo.

### 2026-10-26 — Nuevo intento de conexión al navegador

- Jorge confirmó que Google está abierto en la cuenta readyproof y pidió operar el navegador. La conexión directa cua.getState volvió a fallar antes de enumerar ventanas: failed to write kernel assets: El sistema no puede encontrar la ruta especificada. (os error 3). No se hicieron clics ni se cambiaron ajustes de Google.
- Verificación local de solo lectura: existen ambas rutas de Readyproof (original y actual), la carpeta .codex y el temporal del sistema; esta comprobación no identifica qué ruta interna falta. No se alteraron permisos, sandbox ni configuración. Se consultó documentación oficial de recuperación; no establece una solución específica para este error. Se propone reiniciar la aplicación como prueba de recuperación, sin garantía de resolución.

## 2026-10-26 — Diagnóstico concreto del fallo del navegador

- Se inspeccionaron rutas y registros técnicos, sin credenciales. Se comprobó que el proyecto de Codex sigue registrado en Documents\ChatGPT\Readyproof, mientras el código operativo está en C:\Users\jorge\Readyproof. Ambas rutas existen.
- El control informa kernel_assets con sandbox_configured=true; los registros muestran además helper_unknown_error: setup refresh had errors. El sandbox falla al preparar la raíz antigua con SetSecurityInfo failed: 5 y al preparar su .git. Se leyeron las ACL sin modificarlas.
- Evidencia y reparación propuesta en out/diagnostico_control/DIAGNOSTICO.md. Se requiere asociar el chat a la carpeta actual mediante la barra lateral de Codex: las herramientas disponibles no pueden conceder ese acceso adicional ni crear el proyecto local. No se alteró la base interna de Codex ni se desactivó/cambió sandbox.
- Pendiente de intervención de Jorge: agregar la carpeta actual como proyecto y mover este chat allí; luego verificar sandbox y cursor. No se declara resuelto el error hasta comprobarlo. Sin cambios en cuenta Google, secretos, fuente/, git ni código de aplicación. No se ejecutaron pruebas de aplicación porque esta operación fue diagnóstica.

## 2026-10-26 — Chat movido a Readyproof Actual; persiste acceso anterior

- Jorge creó Readyproof Actual, confió la carpeta y movió este chat. El cwd ahora es C:\Users\jorge\Readyproof. Sin embargo, el perfil de esta conversación conserva como raíz adicional Documents\ChatGPT\Readyproof.
- El reintento cua.getState cambió de error: node_repl kernel exited unexpectedly; stderr: windows sandbox failed: helper_unknown_error: setup refresh had errors. Un comando de solo lectura dentro del sandbox confirmó el mismo fallo.
- Log actualizado a 20:35 UTC: SetSecurityInfo failed: 5 en la raíz antigua y su .git. Mover este chat no eliminó la raíz antigua, por lo que esa acción no resolvió el bloqueo. No se modificaron ACL ni seguridad, ni se tocaron secretos, Gmail, fuente/ o git.
- Próximo paso propuesto: abrir una conversación nueva (no copiar ni bifurcar esta) dentro de Readyproof Actual y verificar primero el sandbox y el navegador. No se crea automáticamente un chat; la instrucción para retomar queda en docs/RETOMAR_GMAIL.md. Resolución aún no comprobada.

## 2026-10-26 — Reanudación Gmail: control del navegador aún bloqueado

- Se leyó docs/RETOMAR_GMAIL.md. El cwd comprobado es C:\Users\jorge\Readyproof; el perfil de esta conversación incluye también la raíz anterior Documents\ChatGPT\Readyproof.
- La consola dentro del sandbox falló antes de ejecutar la lectura: Failed to create unified exec process; helper_unknown_error: setup refresh had errors. La lectura local con autorización fuera del sandbox sí funcionó; esto no demuestra recuperación del entorno aislado.
- cua.getState falló en dos intentos. El segundo informó node_repl kernel exited unexpectedly, con stderr windows sandbox failed: helper_unknown_error: setup refresh had errors. El control de Windows mediante node_repl tampoco pudo iniciar por el mismo error; no se enumeraron ventanas ni se comprobó la sesión de Chrome.
- Sin clics, cambios en Gmail, acceso a .env.local, conexión SMTP ni envío de correo. Sin modificaciones de ACL, sandbox, fuente/, AGENTS.md, git o código de aplicación. No se ejecutaron pruebas de aplicación en esta comprobación del entorno.
- Pendiente: recuperar el entorno aislado y comprobar navegador antes de retomar la configuración. No se declara resuelto el bloqueo ni autenticada la cuenta Gmail.

### 2026-10-26 — Reparación solicitada: asociación de proyecto y pruebas de aislamiento

- Consultada la documentación oficial de Windows sandbox. Codex 0.164.0-alpha.11.1; Windows build 26100.6725. MXC no disponible en la prueba sin cambios persistentes.
- El sandbox elevado con perfil :workspace y requisitos administrados ejecutó el comando inocuo y devolvió LEGACY_OK, código 0, en la carpeta actual. El perfil activo del chat sigue fallando al preparar la carpeta anterior y su .git, con SetSecurityInfo failed: 5.
- La herramienta list_threads mostró este chat sin proyecto. Se corrigió su asociación mediante move_thread_to_project a Readyproof Actual. Cambio confirmado por la herramienta. No se modificó la base interna de Codex.
- Verificación posterior: Get-Location dentro del sandbox falló; reiniciar el kernel y llamar cua.getState también falló con windows sandbox failed: helper_unknown_error: setup refresh had errors. El navegador no está recuperado. Pendiente recargar la sesión de Codex para comprobar la reconstrucción del perfil; resultado no garantizado.
- Actualizados docs/RETOMAR_GMAIL.md y out/diagnostico_control/DIAGNOSTICO.md. Sin cambios manuales de ACL, modo de aislamiento, fuente/, AGENTS.md, git, código, credenciales o Gmail. Sin envío de correo ni pruebas de aplicación; intervención limitada al entorno.

### 2026-10-26 — Comprobación posterior solicitada por Jorge

- Get-Location dentro del sandbox y cua.getState fallaron otra vez antes de ejecutar: helper_unknown_error: setup refresh had errors. La lectura autorizada fuera del sandbox confirmó cwd C:\Users\jorge\Readyproof.
- El último registro del sandbox (20:46:04 UTC) sigue mostrando SetSecurityInfo failed: 5 en C:\Users\jorge\Documents\ChatGPT\Readyproof y su .git. El perfil del chat conserva la raíz anterior; la asociación al proyecto y el reinicio propuesto no han recuperado las herramientas.
- Sin interacción con Gmail, acceso a secretos ni cambios de seguridad o aplicación. El navegador sigue bloqueado. No se ejecutaron pruebas de aplicación en esta comprobación.

### 2026-10-26 — Informe para pedir ayuda a Claude

- A pedido de Jorge se creó docs/PEDIDO_AYUDA_CLAUDE_CONTROL_GMAIL.md, con el contexto de Gmail, las dos carpetas, la creación del proyecto Readyproof Actual, las asociaciones de chats, errores exactos, comandos/resultados, ACL leídas, intentos fallidos y criterio de resolución.
- Se distingue evidencia directa de antecedentes registrados e hipótesis. Se aclara que el procedimiento físico de creación/copia de la carpeta actual y el cierre de procesos durante el reinicio no se observaron directamente. Se documenta también la prueba CLI exitosa frente a las herramientas del chat fallidas.
- Informe sin contraseñas ni tokens; conserva rutas locales, nombre de equipo y correo dedicado como contexto técnico. No se envió a Claude ni a terceros. Sin cambios de aplicación ni nuevas pruebas; entrega exclusivamente documental.

### 2026-10-26 — Validación local de configuración Gmail solicitada por Jorge

- El MCP volvió a responder y confirmó la cuenta dedicada readyproof.ar@gmail.com; no se leyeron mensajes ni se enviaron correos.
- A pedido de Jorge se comprobó .env.local mediante una lectura que emite únicamente indicadores de validación, sin mostrar valores secretos. Archivo presente; SMTP_HOST, SMTP_PORT, SMTP_USER y remitente coinciden con Gmail, puerto 587 y la cuenta dedicada. SMTP_PASSWORD tiene un valor no vacío y MAIL_MODO_PRUEBA está activo.
- La comprobación no autentica contra Gmail ni demuestra que la contraseña sea válida. Sin conexión SMTP, envío de correo, arranque de worker ni cambios de configuración. El sandbox normal sigue fallando; la lectura se ejecutó con autorización fuera de él.

### 2026-10-26 — Prueba de autenticación Gmail sin envío

- Jorge autorizó probar y comprobar la configuración. Se ejecutó un diagnóstico independiente con las variables de .env.local, sin importar Flask, iniciar workers, procesar pendientes ni transmitir mensajes. Se mantuvo MAIL_MODO_PRUEBA y no se modificó configuración.
- Dos intentos autorizados: conexión a smtp.gmail.com:587 y STARTTLS con certificado validado correctos en ambos. La autenticación no quedó confirmada. El segundo diagnóstico precisó SMTPServerDisconnected en el paso autenticar; no se recibió un rechazo explícito de credenciales que permita declarar incorrecta la contraseña.
- Resultados con código de proceso 1. Sin respuestas SMTP crudas, claves ni tokens en salidas. Último resultado saneado en out/diagnostico_control/resultado_auth_gmail.json y procedimiento en out/diagnostico_control/probar_auth_gmail.py. Sin envío de correo ni cambios de aplicación o fuente/. No se repite el intento automáticamente.

### 2026-10-26 — Intento de envío SMTP a la casilla de prueba autorizada

- Jorge pidió enviar un correo a su casilla de prueba. Se preparó un mensaje de texto con asunto [Ejemplo] Prueba SMTP de readyproof, sin adjuntos ni datos de clientes, desde la cuenta dedicada. Ejecución independiente autorizada; sin activar el worker, procesar colas ni modificar MAIL_MODO_PRUEBA.
- Un único intento: conexión y certificado STARTTLS correctos; SMTPServerDisconnected durante autenticar. No se alcanzó la transmisión del mensaje ni hubo aceptación SMTP o entrega confirmada. Código de proceso 1. No se reintentó ni se sustituyó el transporte por MCP.
- Evidencia saneada en out/diagnostico_control/resultado_envio_gmail.json; script de intento único en out/diagnostico_control/enviar_prueba_gmail.py. La existencia del registro bloquea su repetición accidental. Clave usada en memoria y no mostrada. Sin cambios de configuración, aplicación o fuente/.

### 2026-10-26 — Diagnóstico SMTP: rechazo explícito de credenciales

- A pedido de Jorge se investigó el corte durante login, revisando el transporte y documentación oficial de Google/Python. Se agregó un diagnóstico independiente sin envío, con AUTH LOGIN sin respuesta inicial y espera máxima de 65 segundos, sin modificar .env.local ni el código de aplicación.
- Resultado: STARTTLS y certificado de Google Trust Services correctos; EHLO 250, NOOP 250; PLAIN, LOGIN y XOAUTH2 anunciados. AUTH LOGIN recibió 535 con código ampliado 5.7.8 en 0,69 segundos. Diagnóstico completo: 14,76 segundos; código de proceso 1. Gmail rechazó las credenciales usadas: ya no es solo una desconexión sin respuesta concluyente.
- Solo se emitieron indicadores sobre la clave: no coincide con el patrón habitual de 16 letras de una contraseña de aplicación y no contiene espacios de agrupación. No se imprimió la clave ni una respuesta SMTP cruda. No se cambiaron los valores de configuración.
- Evidencia en out/diagnostico_control/diagnostico_login_gmail.json; procedimiento en out/diagnostico_control/diagnosticar_login_gmail.py. No se envió otro correo, inició worker ni ejecutó suite de aplicación; diagnóstico externo sin cambios de aplicación o fuente/.
- Pendiente de Jorge: crear una contraseña de aplicación válida de la cuenta dedicada y guardarla directamente en SMTP_PASSWORD de .env.local. El MCP no ofrece administración de seguridad o creación de estas claves. Después se deberá validar autenticación y completar el envío de prueba ya autorizado a su casilla, sin repetir mensajes aceptados o de aceptación desconocida.

### 2026-10-26 — Nueva comprobación solicitada: persiste rechazo Gmail

- Jorge pidió volver a probar y resolver. Se ejecutó el diagnóstico con la clave local actual, sin mostrarla ni modificarla. STARTTLS, certificado Google Trust Services, EHLO 250 y NOOP 250 correctos. AUTH LOGIN recibió nuevamente 535 / 5.7.8, en 0,60 segundos; duración total 14,02 segundos, código de proceso 1.
- Continúa sin coincidir el indicador de formato habitual de contraseña de aplicación. No se afirma que el archivo no haya cambiado: se informa únicamente el nuevo rechazo del proveedor. No se transmitieron mensajes ni se arrancó el worker.
- Sigue siendo necesaria una contraseña de aplicación válida guardada por Jorge; no se puede generar mediante las herramientas Gmail disponibles. Evidencia saneada actualizada en out/diagnostico_control/diagnostico_login_gmail.json. Sin cambios de aplicación, fuente/, permisos o configuración.

### 2026-10-26 — Gmail: autenticación y envío de prueba correctos

- Jorge accedió a Contraseñas de aplicación, consultó el nombre a usar y luego pidió probar. La nueva clave local fue aceptada por Gmail con AUTH LOGIN: 235, TLS validado y certificado Google Trust Services. La contraseña no se mostró en herramientas ni se recibió por chat.
- La clave tenía espacios de agrupación. Con autorización se quitaron exclusivamente esos espacios en SMTP_PASSWORD de .env.local. Verificación de todas las demás variables sin cambios, manteniendo MAIL_MODO_PRUEBA activo. No se guardó una copia de la clave en archivos diagnósticos.
- Se comprobó después smtplib.login, el mismo método utilizado por readyproof, sin normalización adicional en memoria: autenticación 235 correcta, código de proceso 0. Evidencia en out/diagnostico_control/resultado_auth_gmail.json.
- Se completó el envío de texto sin adjuntos a la casilla de prueba que Jorge ya había autorizado. Se conservó el registro del intento anterior, fallido antes de transmitir; el nuevo intento tiene evidencia independiente y protección contra repetición. SMTP aceptó el mensaje, código de proceso 0. Evidencia en out/diagnostico_control/resultado_envio_gmail_clave_validada.json.
- El MCP confirmó nuevamente la cuenta dedicada y encontró el mensaje exacto por Message-ID en Enviados. Esto confirma el registro del envío en Gmail, no la entrega en la bandeja destinataria. No se utilizó el MCP para transmitir el mensaje: salió por SMTP con la credencial local.
- Sin cambios de código de aplicación, fuente/, AGENTS.md, git, dependencias ni servicios. No se inició worker ni se activó envío real global. No se ejecutó la suite de aplicación: intervención de configuración y prueba operativa externa. Pendientes: recepción/entregabilidad en destino y flujo con PDF desde la aplicación. El bloqueo previo del navegador no se declara resuelto por esta prueba.

### 2026-10-26 — Informe para Claude consolidado y correo PDF preparado

- Jorge pidió actualizar el informe y continuar. Se puso el estado vigente al comienzo de docs/PEDIDO_AYUDA_CLAUDE_CONTROL_GMAIL.md, conservando la cronología y distinguiendo la solución de Gmail del bloqueo del sandbox. docs/RETOMAR_GMAIL.md ahora abre con el estado vigente y advierte que las instrucciones sobre clave vacía o falta de SMTP son antecedentes.
- Inspección de solo lectura de la base PostgreSQL propia del ejemplo: disponible, sin SAA-1 emitidas aptas según los filtros de ejemplo, huella y leyenda. Evidencia out/diagnostico_control/preparacion_pdf.json. Sin modificar base ni usuarios.
- Revisados ambos renders de la muestra SAA-1 ya aprobada en etapa M1. Preparado un EML exclusivamente local con crear_mensaje de la aplicación y esa muestra ficticia: out/diagnostico_control/prueba_pdf_preparada.eml. Validaciones: dos páginas, leyenda en ambas, T.C. 3 AÑOS, datos ficticios, un único PDF y adjunto idéntico al original (204711 bytes), huellas PDF/EML registradas. Procedimiento y evidencia junto al EML.
- No se envió un segundo correo ni se inició worker. Sin cambios de fuente/, AGENTS.md, git, código de aplicación, credenciales, modo de prueba o dependencias. No se volvió a correr la suite de aplicación: preparación documental y diagnóstica sin modificar app. La validación ejecutada comprueba el mensaje local, no el flujo API/emisión en base ni recepción del destinatario.
- Siguiente acción concreta para revisión: enviar el correo preparado con el PDF de muestra al destinatario de prueba; después verificar el adjunto y la recepción. Continúa pendiente una carga emitida apta para comprobar el flujo completo de la aplicación.

### 2026-10-26 — Envío de PDF de muestra autorizado por Jorge

- Jorge respondió Sí a la revisión concreta del correo con PDF. Se ejecutó un único envío desde readyproof.ar@gmail.com a su casilla de prueba, con asunto [Ejemplo] Prueba PDF SAA-1 de readyproof. La copia EML se transmitió sin modificarla; se comprobaron huellas EML/PDF, destinatario único, remitente, asunto y tipo de adjunto antes de contactar SMTP.
- STARTTLS con certificado validado, autenticación aceptada y mensaje aceptado por SMTP; código de proceso 0. No se hizo reintento automático. La reserva de intento único bloquea repetir accidentalmente este envío. Evidencia out/diagnostico_control/resultado_envio_pdf.json y copia prueba_pdf_preparada.eml.
- El MCP confirmó la cuenta dedicada y encontró el Message-ID exacto en Enviados: un único readyproof-planilla.pdf, application/pdf, 204711 bytes. Esto no prueba recepción en la bandeja destinataria. Pendiente confirmación de Jorge y revisión de encabezados SPF/DKIM en destino.
- Informe para Claude, docs/SMTP_GMAIL.md y pendientes actualizados. Sin cambios de .env.local, modo de prueba global, base de ejemplo, usuarios, aplicación, fuente/, AGENTS.md, git, dependencias o servicios. No se inició worker ni se procesaron otras colas. Se utilizó crear_mensaje para preparar el EML, pero no se afirma probado el flujo completo API/emisión/cola en base. No se ejecutó la suite de aplicación en este envío operativo sin cambios de app.

## 2026-10-26 — Etapa 7 operativa: carga → envío Gmail → recepción

- Alcance de esta continuación: circuito operativo con datos y firmas ficticios. A pedido de Jorge, el cliente se llama [Ejemplo] readyproof y el login es tecnico-readyproof, nombre visible [Ejemplo] Técnico readyproof. No se modificó la aplicación para aceptar correo/tildes como login.
- Creados cliente y técnico de prueba en PostgreSQL local, asignación exclusiva al cliente y sistema SAA. Clave aleatoria generada, hasheada y utilizada en memoria; no impresa ni conservada. Login real por API con sesión/CSRF y logout al terminar. Para una revisión manual posterior se deberá restablecer la clave mediante el administrador.
- Flujo comprobado mediante el cliente HTTP Flask y la base persistente del ejemplo: crear carga, guardar todos los campos según definición, dos firmas PNG ficticias, vista previa, finalizar, emitir y descargar PDF. Sin simulación de generación ni SMTP. Carga 0ca07d1f-278b-49ba-bf74-0dad8ab1bf2d, plantilla SG-PEM-IFI-SAA-1, versión 00-26, estado emitida.
- Revisadas visualmente las dos páginas: encabezado/logo readyproof, marcas readyproof + ISO, T.C. 3 AÑOS, leyenda IRAM en ambas y dos firmas visibles. PDF de 209888 bytes, SHA256 ac65d9dee873700b8632c8e88531fce64331c0cefc7cfbff2cffcb3ae3bef63f.
- POST /api/cargas/0ca07d1f-278b-49ba-bf74-0dad8ab1bf2d/enviar: HTTP 202, Envio 20275994-e1d7-4fa8-879e-40266b1f876e pendiente. Se archivaron copias PDF/EML inmutables y huellas. El endpoint deja cero Intentos: el número 1 se registra al procesar, no al encolar. Finalizar produce finalizada; emitir produce emitida.
- Una única pasada manual de reintentar_envios(), sin scheduler ni worker automático. Se comprobó antes que el único envío procesable fuera el autorizado. MAIL_MODO_PRUEBA=False solo en esa instancia de proceso; sin cambiar .env.local ni el servidor de ejemplos. Resultado: un intento, número 1, ok; Envio enviado, aceptación SMTP 19:33:48 de Argentina, ningún reintento programado. Auditoría de emisión, cola e intento y copia idéntica al PDF emitido verificadas. Conservación mínima registrada hasta 26/10/2029.
- Remitente readyproof.ar@gmail.com; destinatario de prueba autorizado jorgesanchezing@gmail.com; asunto [Ejemplo] SAA-1 de readyproof. Gmail MCP confirmó cuenta, etiqueta SENT, Message-ID <20275994-e1d7-4fa8-879e-40266b1f876e@gmail.com> y un único adjunto readyproof-planilla.pdf, application/pdf, 209888 bytes. No se usó MCP para transmitir.
- Recepción y formato en destino: SÍ. Jorge respondió «Sí, llegó y se ve todo bien» a la revisión de dos páginas, leyenda, logo, marcas de agua y firmas ficticias. SPF/DKIM en encabezados recibidos no se inspeccionaron y no se declaran comprobados.
- Limitación operativa: cua.getState no pudo iniciar por windows sandbox failed: helper_unknown_error: setup refresh had errors. Esta carga se completó y firmó por API con PNG ficticios; el recorrido manual de formulario/canvas sigue pendiente. Las pruebas de navegador automatizadas son una comprobación separada y no sustituyen ese recorrido ni la prueba física de teléfono.
- Pruebas: primera ejecución, 139 passed y 2 failed in 407.74s, por Cannot find module playwright. El intento de usar la ruta histórica .venv/browser/node_modules detectó que ya no existe y se interrumpió. Se comprobó Playwright 1.62.1 ya instalado en el runtime y se ajustó únicamente NODE_PATH del proceso, con TEMP/TMP en .venv/tmp. Suite completa final: 141 passed in 462.07s (0:07:42), código 0. Sin cambios de pruebas, omisiones ni descargas. Salida en out/flujo_completo_gmail/pytest_final.txt.
- python -m compileall app: código 0; salida en out/flujo_completo_gmail/compileall.txt. SHA256 de app/ y los 177 archivos de fuente/ sin cambios. Búsqueda de valores de SMTP_PASSWORD/SECRET_KEY configurados en 138 archivos de código, pruebas, fuentes y documentación: cero coincidencias, sin mostrar valores. .env.local sigue excluido por .gitignore.
- Entregables: docs/FLUJO_COMPLETO_GMAIL.md y registros actualizados. Procedimiento, PDF, dos renders, evidencia API/BD y Gmail saneada en out/flujo_completo_gmail/. Sin Git, despliegue, nuevos servicios, dependencias o cambios de fuente/, aplicación o credenciales. No se declaran cerradas las demás etapas o habilitados clientes reales por recibir este correo.

## 2026-10-26 — Acceso administrador y recuperación local autorizada

- Diagnóstico inicial de solo lectura: tabla usuarios existente, COUNT(*)=2, admin msanchez activo y técnico tecnico-readyproof activo. jorge.admin no existía; la condición que rechazó su login fue user is None, con HTTP 401, no la validación de formato. normalizar_login('jorge.admin') válido; la clave propuesta cumple la política de 12 caracteres como mínimo y 72 bytes UTF-8 como máximo. No se almacenó esa clave en archivos.
- Corregido POST /login sin usuarios: ahora redirige por 303 a /configuracion-inicial, al igual que la detección existente por GET. Con cuentas existentes no reabre el alta inicial ni crea cuentas implícitamente. CSRF, bcrypt y limitación de intentos conservados.
- Jorge aclaró luego que tampoco podía entrar con msanchez. Auditoría de solo lectura: cuenta existente, activa, admin y hash bcrypt de formato válido; cuatro fallos 401 recientes, sin bloqueo 429 en esa inspección. La contraseña recibida no superaba su comprobación. No se probaron otras claves.
- Jorge autorizó expresamente recuperar msanchez. Implementado CLI admin-recuperar --login y scripts/recuperar_admin_local.py: confirmación, entrada oculta repetida de clave nueva, validación existente, solo admin activo, cierre de sesiones y evento admin_recuperado_local/CLI. Sin endpoint de recuperación web ni claves por argumentos o archivos. No borra el historial ni elude el bloqueo por intentos.
- Cinco pruebas de recuperación aprobadas en PostgreSQL temporal; se verifican validación, cancelación, rechazo de técnico/inexistente, auditoría sin contraseña, revocación y login con clave nueva. Se ampliaron las regresiones de primer admin, logout/login y alta de segundo administrador conservando la clave del original.
- La cuenta real no fue restablecida: Jorge confirmó que todavía no ejecutó el comando. Recuperación e ingreso real quedan pendientes de su consola. Instrucciones en docs/DIAGNOSTICO_ACCESO_ADMIN.md. Las credenciales de la base del ejemplo se verificaron sin cambios al registrar las versiones nuevas.

## 2026-10-26 — Identidad readyproof en app, kit y documentos históricos

- Jorge pidió el reemplazo integral y confirmó todo al consultar expresamente por fuente/ y PDF históricos. Autorización específica para esta actualización del kit, previamente sujeto a conservación. Respaldo íntegro antes de editar: bak/identidad_previa_2026-10-26.zip; ampliado con JSON, módulos de catálogo y vistas anteriores. No se borraron originales para perder trazabilidad.
- Aplicación y documentación propia: textos, subtítulos de acceso/carga, empresa mantenedora del ejemplo, validación y autor PDF actualizados. Subtítulo final readyproof · REGISTROS DE SERVICIO; caché PWA readyproof-identidad-v2. Sin referencias textuales de la identidad anterior en los archivos activos revisados de app/, docs/, fuente/, scripts/, tests/ y raíz.
- 20 PDF históricos locales, 4 DOCX y 12 XLSX procesados. PDF: páginas y términos técnicos conservados al sustituir el nombre; logos reemplazados en todas las páginas, metadatos actualizados y píxeles de firmas/sellos comparados con originales. Word: cuatro plantillas, 34 páginas renderizadas y revisadas. Excel: XML e imágenes editados de forma dirigida, sin reconstruir los paquetes ni perder el encabezado VML; fórmulas y estructura ZIP conservadas. Se renovaron 31 vistas PNG y cuatro comparaciones. No se editaron contenidos normativos ni se tomaron decisiones técnicas nuevas.
- El guardado de PDF puede repetir recursos de imagen idénticos para encabezado/marca de agua; se comprobó igualdad de contenido de esas imágenes y de cantidad/píxeles de firmas. No se confundió ese detalle de serialización con un cambio de firma.
- Nuevas versiones: piloto interno 00-26-rp1 y contenedores JSON v2, con SHA256 actual del generador. Los datos, campos, opciones, orden y origen de contenido de los cuatro JSON se verificaron equivalentes mediante el conversor. Las versiones anteriores se conservan y la selección de carga ofrece solo las vigentes. Regresión adicional verifica que no se sobrescriban plantillas previas.
- Ejemplo local: el proceso anterior y PostgreSQL estaban detenidos; la primera conexión no escribió datos. Se reabrió el clúster existente con pg_ctl, sin reinicializar ni borrar archivos. Comandos de la aplicación init-db --ejemplos y cargar-planillas: cinco versiones nuevas, 5 a 10 plantillas. Versiones anteriores, cuatro cargas, firmas y credenciales sin cambios. No se editaron tablas a mano ni se reescribieron PDF/EML emitidos de la base o mensajes ya enviados.
- Aplicación actualizada nuevamente disponible solo en http://127.0.0.1:8765/login, sin debugger/reloader/worker y con MAIL_MODO_PRUEBA=True en el proceso. Comprobación HTTP 200 del subtítulo readyproof, sin identidad anterior. Estado de conexión conservado en out/etapa3/demo_local/servidor.json; proceso local en out/identidad_readyproof/servidor_local.py. Recargar la pestaña con Ctrl+F5.
- Pruebas finales: 151 passed in 387.01s (0:06:27), código 0. python -m compileall app scripts/recuperar_admin_local.py: código 0. Verificación de exportación: cuatro JSON equivalentes. Inicialmente hubo interferencia por temporal compartido; luego rutas largas provocaron WinError 145 en perfiles LibreOffice. Se corrigió el entorno usando una ruta corta y exclusiva, sin ocultar fallos ni cambiar el convertidor para ignorarlos. Las cuatro diferencias de huella JSON se corrigieron con versionado; no se eliminaron controles. Salidas anteriores se conservan como diagnósticos, no como aprobaciones.
- Sin Git, publicación, nuevas dependencias, correos reales ni cambios de .env.local. Revisión de valores configurados de credenciales en entregables sin imprimirlos. Detalle del alcance, respaldo y límites en docs/IDENTIDAD_READYPROOF.md. Los otros pendientes del proyecto, incluida la recuperación real del admin, permanecen abiertos.

## 2026-10-27 — Auditoría: PNG simple y metadatos PDF

- Se comprobó la copia de trabajo: app/static/logo_readyproof.png ya existía (926×312, 24580 bytes), por lo que no se trataba de una ausencia en esta carpeta. Jorge solicitó reemplazarlo por un PNG simple de 600×150: aplicado, fondo blanco RGB y texto readyproof en Helvetica-Bold estándar PDF, 48 pt, gris #333333, sin símbolo ni subtítulos. Rasterización determinista con las bibliotecas incluidas; sin nuevas dependencias. Archivo anterior conservado en bak/logo_readyproof_previo_2026-10-27.png.
- Se comprobó app/planillas/encabezado_pdf.py: /Author, /Creator y /Producer ya eran readyproof. No se cambió una línea que ya tenía el valor solicitado. Se verificaron los tres valores tanto en el código como en un PDF SAA-1 nuevo generado por las pruebas.
- El PDF incorpora el PNG nuevo una vez en el encabezado de cada página; comparación de píxeles contra el archivo final aprobada. Se revisaron visualmente el PNG y el render PDF, manteniendo el formato de la planilla.
- python -m compileall app/ tests/: código 0. Suite completa: 151 passed in 429.45s (0:07:09), código 0. PostgreSQL temporal aislado, ruta corta exclusiva y SMTP bloqueado durante los tests. Salidas en out/auditoria_logo_20261027/.
- Sin cambios en fuente/, definiciones, credenciales, base de ejemplo, requisitos o servicios. Sin Git, envíos reales ni publicación. Los dos hallazgos quedan verificados para esta copia; el pendiente de recuperación del administrador y las otras decisiones anteriores continúan separados.

## 2026-10-27 — Guías de acceso, deployment y prueba operativa final

### Solicitud posterior de despliegue: preparación privada

### Corrección posterior de selectores y service worker

- Diagnóstico: listeners change presentes; ningún preventDefault de clicks en dropdowns. Servidor con un cliente ficticio, un sistema SAA y una planilla operativa, por lo que no había otras alternativas reales. Catálogos de grupos importados correctamente filtrados por tipo; no eran seleccionables. No se agregaron datos de ejemplo al servidor para fabricar opciones.
- Indicador accesible de cantidad de clientes/sistemas/planillas y orientación a Administración; captura de errores de cambios de selección. Caché de shell readyproof-ui-v3, updateViaCache none y service worker con Response 503 cuando faltan red y copia, copia offline sin parámetros y tolerancia a fallas de escritura de caché. Sin cambios de IndexedDB, campos, opciones normativas, generación PDF o validación de backend.
- Dos regresiones nuevas: 2 passed in 22.79s. Caso SW falla con código anterior y pasa corregido. Chromium de prueba verificó cambios de Cliente (2), Sistema (1) y Planilla (1), sincronización/recuperación IndexedDB, recarga y cero errores de página. Base temporal y SMTP bloqueado. No se inventó una prueba de la sesión real: el control de navegador de usuario falló por windows sandbox failed: helper_unknown_error: setup refresh had errors; se usó navegador aislado de pruebas.
- Desplegados cuatro archivos tras comprobar hashes previos; respaldo /root/readyproof-selectores-20261027/antes.tar.gz. Reiniciado solo readyproof, HTTP login 200, recursos actualizados servidos, servicio activo y NRestarts=0. Sin modificación de BD, datos del sitio, credenciales, SMTP, dominio/DNS, puertos, Docker/Traefik, kit ni Git remoto. Un comando de lectura grep tuvo un error de escape; se repitió solo esa lectura correctamente, sin repetir el despliegue.
- Jorge confirmó con Ctrl+F5: «Sí, abren y aparece el indicador». Dropdowns y recarga real confirmados. No se inspeccionó su consola F12; la corrección SW se comprobó por regresión y navegador aislado. Suite completa final: 158 passed in 487.56s (0:08:07), código 0; compileall app/ tests/ código 0. Cuatro hashes desplegados coincidentes y ningún valor de secreto configurado expuesto en los entregables revisados. Evidencias y límites en docs/CORRECCION_SELECTORES.md y out/correccion_selectores/.

**Resultado posterior — instalación privada completada:** Jorge autorizó expresamente el servidor compartido. Clonado el repositorio solicitado en /home/readyproof, commit 4cb1599840419b3faa18496349758b663265dcca. Instalados 72 paquetes nuevos, cero actualizados/eliminados; sin apt upgrade, reboot, cambios de firewall, DNS, Traefik o servicios Docker. Instalador limitado a 384 MB/50 % CPU, pico 299.2 MB. Nombre correcto de fuente Ubuntu: fonts-crosextra-carlito, corregido en la guía tras fallar la simulación con fonts-carlito.

Creado usuario de sistema readyproof sin login, entorno Python y Gunicorn 26.2.0. pip check y compilación aprobados. PostgreSQL 16 exclusivo del host, base readyproof y rol readyproof_user sin superusuario/crear roles/crear bases. Migraciones Alembic y catálogo ficticio por CLI oficial. Secretos de DB y sesión aleatorios generados dentro del servidor, .env root:readyproof 0640; no se copió .env.local ni se mostraron valores. Servicio readyproof.service con un worker y usuario sin privilegios, 127.0.0.1:8000; PostgreSQL en 127.0.0.1:5432. Slice conjunto MemoryHigh 384 MB y MemoryMax 512 MB; máximo medido 396546048 bytes. App máximo 384 MB/50 % CPU y PostgreSQL 128 MB/25 %. Instalación de revisión, sin datos reales ni SMTP.

msanchez creado mediante formulario HTTP normal /configuracion-inicial, con CSRF y validaciones existentes. Contraseña temporal aleatoria conservada solo en /root/readyproof-admin-inicial.json, modo 0600; no impresa ni descargada. Login real, dos firmas PNG ficticias por API, vista previa, finalización, emisión/descarga y correo en archivo aprobados en Ubuntu. Carga 1a1cfc7c-0f86-454d-810e-4be1a90e9ba9; envío 7a420378-3a2d-460d-9c00-58fc2100c3c1. PDF 122049 bytes, dos páginas, logo/IRAM/retención/metadatos/huella verificados, ambas páginas renderizadas y revisadas. Sin transmisión SMTP ni declaración de recepción. La primera comprobación HTTP coincidió con el arranque; la segunda y el reinicio controlado respondieron correctamente. El wrapper SSH de la validación tuvo un error de escape al propagar el código de salida; el unit de validación y su reporte confirmaron código 0, sin repetir el bootstrap ni la carga.

Backup diario local habilitado mediante timer, sin purga, dump de 427122 bytes restaurado en readyproof_restore_check_20261027; usuarios/cargas/envíos/intentos y huellas PDF/EML coincidentes. Copia externa pendiente. Comparación de 256 archivos de código/fuente/migraciones/pruebas/scripts contra Windows: 192 iguales y 64 con diferencia exclusiva CRLF/LF, cero diferencias de contenido. La suite local previa de 156 pruebas sigue siendo la evidencia automatizada; no se afirma haber ejecutado la fixture Windows en Linux.

Túnel privado comprobado desde Windows en http://127.0.0.1:8876/login, HTTP 200, puerto público 8000 no accesible. Dos intentos de túnel persistente fallaron por timeout/reset; comprobación efímera en un mismo proceso exitosa y túnel cerrado al terminar. Preparado scripts/abrir_readyproof_privado.ps1 para uso continuo en la consola de Jorge. Corregidos eco y codificación UTF-8 con BOM del habilitador SSH para PowerShell 5.1. Servicio app/DB/timer activos y reinicio de readyproof aprobado. Sin eventos OOM del host en la revisión; no se reiniciaron manualmente contenedores existentes. Hay un contenedor ajeno con un historial alto de reinicios, no intervenido.

Acceso, clave temporal por consulta privada, límites y pendientes documentados en docs/ACCESO_SERVIDOR_PRIVADO.md; guías y checklist actualizados. Evidencia saneada en out/despliegue_privado/. Sin cambios de código de aplicación, kit o requisitos, sin commits/push ni publicación. Pendientes: cambio de clave temporal por Jorge, revisión desde su navegador, dominio propio/HTTPS, SMTP real de servidor, destino de backup externo, capacidad, canvas/dispositivo y habilitación de datos reales. Los puntos históricos siguientes describen la preparación anterior.

- Acceso por clave SSH confirmado tras la ejecución privada de Jorge. Inspección remota de solo lectura: Ubuntu 24.04.1 LTS, hostname brafemar-server, múltiples servicios Docker activos, puertos públicos 80/443 ocupados por docker-proxy, RAM 7941 MB total y 624 MB disponible, sin swap. Sin readyproof, Nginx o PostgreSQL del host activos en esa inspección. No se instalaron paquetes, clonaron repositorios ni cambiaron servicios, firewall o DNS.
- Se detuvo la instalación antes de cualquier cambio: la IP recibida ya aloja servicios y contradice el servidor separado exigido por el encargo. Se pidió a Jorge elegir otro Droplet separado o autorizar expresamente la preparación privada compartida. No se ejecutó apt upgrade ni se tocó la infraestructura existente; dominio/publicación siguen pendientes.

- Corrección del habilitador SSH tras la ejecución de Jorge: Windows PowerShell 5.1 convertía el stderr del sondeo BatchMode en NativeCommandError por ErrorActionPreference=Stop y cortaba antes de solicitar contraseña. El sondeo ahora captura stdout/stderr mediante subprocess de Python y entrega únicamente éxito/rechazo a PowerShell. Verificados sintaxis y caso de rechazo simulado en Windows PowerShell 5.1; sin conectar ni cambiar el servidor. No se regenera una clave existente ni se alteran los pasos de autenticación interactiva.

- Jorge autorizó preparar readyproof en 67.205.170.29 con acceso root y repositorio https://github.com/Brafemar/readyproof.git. Rechazó el subdominio de la identidad anterior y eligió «Preparar en privado; dominio pendiente». No se autoriza por esta elección publicar por IP ni emitir certificados sobre ese dominio.
- Prueba SSH de solo lectura con BatchMode y verificación estricta de host: Permission denied (publickey,password). No se ingresó ninguna contraseña ni se ejecutaron comandos remotos. No se modificó el servidor.
- Preparado scripts/habilitar_acceso_despliegue.ps1 para ejecución privada por Jorge: genera una clave Ed25519 exclusiva sin imprimir la clave privada, restringe su ACL Windows e instala solo la clave pública en authorized_keys de root mediante autenticación interactiva. No modifica SSH global, no deshabilita acceso por contraseña, no instala dependencias ni publica la aplicación. Permite continuar luego con comandos sin compartir contraseñas.
- La receta recibida requiere adaptar URL de base a postgresql+psycopg, usar la fábrica app:create_app(), instalar LibreOffice/Gunicorn, crear el primer administrador por bootstrap y ejecutar el servicio con usuario dedicado. No se utilizará una contraseña documental fija, ni se publicará una contraseña temporal en el chat. Revisadas referencias oficiales Flask/Gunicorn y conexión SSH de DigitalOcean antes de proceder.
- Pendiente habilitar acceso por clave, inspeccionar sistema y servicios existentes y comprobar repositorio antes de instalar. Dominio, DNS, HTTPS y publicación quedan pendientes por decisión expresa de Jorge.

Actualización posterior: al investigar el bloqueo «Ya existe evidencia», se encontró `out/prueba_operativa_final/resultado.json` ya completado con msanchez: carga 0ab4612f-3e33-4251-b79a-825fc3bd39fd, envío 8cda4f14-a21a-4437-b429-4ebb2dbcf4bc, SMTP enviado con intento 1 ok a las 06:55:40 de Argentina y recepción/apertura confirmadas por declaración manual en consola. Se volvió a verificar el PDF de 198073 bytes y dos páginas contra la huella del reporte, logo vigente, IRAM, retención y metadatos. No se repitieron login, carga ni envío. Checklist actualizado; inspección independiente en Enviados y canvas/dispositivo siguen pendientes. Los puntos siguientes conservan el estado anterior a esta comprobación.

- Preparadas docs/GUIA_ACCESO_BRAFEMAR.md, docs/DEPLOYMENT_DIGITALOCEAN.md, docs/CHECKLIST_ENTREGA_BRAFEMAR.md y docs/MANUALES_SG-PEM-IFI.md. Marca visible readyproof; nombres de archivos conservados según el pedido. SAL se documenta como Agentes Limpios, confirmado por Jorge según el kit. README e índice de instalación enlazan los entregables.
- Guía de acceso: usuario individual y clave privada sin valor predeterminado, listas y formulario, borradores, dos firmas canvas, PDF, soporte y límites sin conexión. Se explicita que la interfaz todavía no incluye botón de correo.
- Deployment: propuesta Ubuntu/PostgreSQL/Gunicorn/Nginx, entorno privado, bootstrap por túnel, TLS, timer de backup, restauración y monitoreo. Gunicorn 26.2.0 se justifica como servidor WSGI propuesto; no se instaló ni se cambió requirements.txt. Ensayo Ubuntu, dominio, recursos, proxy/CSRF y uso con datos reales continúan pendientes. No se desplegó ni se accedió a DigitalOcean.
- Nuevo scripts/prueba_operativa_final.py: login real con clave oculta en consola, SAA-1 ficticia, dos firmas PNG por API, vista previa, finalización, emisión, descarga y comprobación de logo/leyenda/retención/metadatos/huella. Correo en archivo por defecto; SMTP requiere opción explícita y casilla de prueba autorizada. Procesa solo el envío recién creado y conserva identificadores antes de procesarlo; no inicia workers ni procesa otra cola. Un resultado existente bloquea la repetición. Recepción/apertura solo se registran por declaración manual explícita; la aceptación SMTP no completa el flujo.
- Cinco pruebas nuevas aprobaron el flujo sobre PostgreSQL temporal, PDF real y SMTP sustituido, aislamiento de otra cola, rechazo de login y confirmación de recepción. Resultado específico: 5 passed in 77.80s. Suite completa final: 156 passed in 653.01s (0:10:53), código 0; salida out/entrega_documentacion_pytest_final.txt. La ejecución anterior quedó interrumpida sin resumen y no se usa como validación.
- Compilación app/, tests/ y script: código 0. Revisión de 25 archivos de documentación/registro/script/pruebas: cero coincidencias de valores de secretos configurados y cero enlaces locales inexistentes; evidencia saneada out/entrega_documentacion_revision.json.
- Jorge confirmó acceso a msanchez y luego indicó que todavía no ejecutó el script. La prueba real nueva permanece pendiente de su consola, SMTP y recepción/apertura; no se sustituye por la evidencia del correo del 26/10. Checklist sin marcar HTTPS productivo, respaldo restaurado, despliegue o prueba nueva completa.
- Se reabrieron PostgreSQL y la aplicación del ejemplo existente solo en loopback, correo en modo archivo, sin reinicializar el esquema ni cambiar credenciales. Sin cambios en app/, fuente/, requisitos, .env.local o Git; sin correos reales, nuevas dependencias o servicios externos.


## 2026-10-27 — Entrega técnica y documentación desde Mi cuenta

- Jorge corrigió el usuario a tecnico_readyproof y confirmó otra PC/Android con acceso propio. Alta por API normal de administrador, con login/CSRF y validaciones existentes; no se usó el recuperador de administradores ni se cambiaron credenciales de msanchez. Rol técnico, un cliente ficticio asignado, login aprobado y Administración HTTP 403. Contraseña aleatoria conservada solo en /root/readyproof-tecnico-inicial.json, modo 0600, nunca impresa ni enviada en el correo de documentación.
- Prueba SAA-1 con la cuenta nueva: carga 80c7c0bf-402c-4cad-85de-314975328a3e, PDF de 121997 bytes, dos páginas, logo, leyenda, retención y metadatos comprobados. Render de ambas páginas revisado: marcas de agua y firmas ficticias visibles, sin recortes. Correo de esa prueba de PDF en archivo, sin SMTP; no se confunde con el correo posterior de guías.
- Cuenta SSH individual readyproof_tunel_tecnico y clave exclusiva de entrega. Configuración respaldada antes de agregar AllowUsers y Match específico: los usuarios existentes conservan su política. Solo reenvío local a 127.0.0.1:8000, sin comandos arbitrarios, agente, X11 o destinos alternativos. Túnel HTTP 200, puerto PostgreSQL rechazado y comando id no ejecutado; root no se comparte. Guía Android con parámetros propios; prueba física pendiente.
- Migración 008_documentacion_usuario: correo nullable de usuario y envios_documentacion con actor, destinatario, copia EML, estado e identificador durable. Mi cuenta permite guardar el correo propio y enviar guías con logo; autenticación, CSRF, rechazo de destinatarios/actores inyectados, idempotencia y límite de un minuto. Reserva antes de contactar correo, sin reintentos automáticos ante aceptación desconocida. Dos adjuntos Markdown, nombre de usuario y soporte; excluye contraseña/hash, claves SSH, OAuth y BD. Las contraseñas actuales siguen siendo hashes no recuperables.
- SMTP 587 desde el Droplet agotó cuatro segundos; HTTPS 443 conectó. DigitalOcean documenta el bloqueo SMTP. Jorge autorizó Gmail HTTPS, creó su proyecto/cliente de escritorio y completó personalmente el consentimiento en Google. Asistente con PKCE/state/retorno loopback y verificación del remitente; permiso transferido por SSH y guardado solo en .env privado 0640. Biblioteca estándar, sin nuevas dependencias. No se configuró SMTP ni se activó la cola de planillas: MAIL_MODO_PRUEBA permanece true; documentación utiliza gmail_api y modo real separado.
- 19 regresiones específicas aprobadas en 56.73s, incluido navegador móvil, doble clic, copia en archivo, SMTP simulado, Gmail HTTPS simulado, aislamiento de usuario y fallos sin filtrar secretos. Primera suite: 170 passed/1 failed por expectativa antigua de head 007, corregida a 008 conservando la prueba de datos. Segunda: 170 passed/1 error por disco lleno en PostgreSQL temporal. Retirados 12 temporales cerrados, sin PID PostgreSQL, dentro de .venv/tmp; ejemplo, backups y evidencias conservados. WAL del clúster de pruebas acotado a 128 MB y checkpoints de 30 s, sin alterar PG real. Suite definitiva sin concurrencia: 177 passed in 544.84s (0:09:04), código 0. Compilación sin errores.
- Despliegue de 15 archivos con hashes, backup de código y dump de BD antes de migrar; servicio reiniciado y HTTP 200. Fuente normativa y generadores intactos, sin Git remoto, nuevo dominio, publicación, facturación o cambios de los servicios Docker/Traefik. Posteriormente se actualizaron solo los documentos de estado y entrega.
- Prueba real por POST /api/usuario/enviar-documentacion, autenticada como tecnico_readyproof: readyproof.ar@gmail.com -> jorgesanchezing@gmail.com, 27/10/2026 12:15:42 de Argentina. Solicitud e9416e59-1c57-5b99-b678-cdcecc28e18a. Gmail API aceptó y el MCP confirmó SENT, mensaje 1a17dee776fd216c, dos guías y PNG inline. Gmail sustituyó el Message-ID reservado; el real es <CANjHx+_Hn=h9A2TuOPuqeAtzZOOKA-E2sfjZyFjLoNNM8fh24A@mail.gmail.com>. La evidencia conserva ambos; se verificó por asunto/destino cuando la búsqueda del reservado no coincidió. No hubo reenvío.
- Recepción confirmada por Jorge: «Sí, llegó con las dos guías». No se enviaron contraseñas. Documentos ENTREGA_A_BRAFEMAR.md y ACCESO_TECNICO_BRAFEMAR.md listos, con marca readyproof y usuario corregido; paquete individual privado con clave limitada, huella, script Windows, guías y PDF ficticio. Sin root, OAuth o contraseña de app dentro del ZIP. Consulta de clave inicial solo para Jorge en ADMIN_ENTREGA_TECNICO.md.
- Estado: listo para entregar el piloto privado con datos ficticios. No se marcó go-live productivo: quedan primera configuración/clave del técnico, validación física Android/canvas, dominio/HTTPS, datos reales, backup externo y capacidad. Google OAuth continúa bajo el estado/controles de prueba de su proyecto y requiere supervisar vigencia. Evidencia en out/documentacion_entrega/ y out/entrega_tecnico/.

- Auditoría final: 109 archivos locales y 80 activos del servidor revisados, cero valores de secretos expuestos en código/documentos y cero en las copias de correo; hashes de aplicación desplegada coincidentes. Gmail HTTPS real activo, planillas en modo prueba, un envío de documentación registrado. ZIP privado comprobado con identidad SSH técnica, sin root/OAuth/contraseña de app. Reportes revision_final.json y readyproof-auditoria-entrega.json.


## 2026-10-27 — Envío de PDF desde la pantalla de carga

- Agregado **Enviar PDF por correo** junto a **Descargar PDF**, con destinatario y resultado en un cuadro accesible en PC y celular.
- Integrado Gmail HTTPS autorizado con los registros Envio/Intento, copia PDF inmutable y retención existente. El transporte anterior conserva su cola y su modo de prueba.
- Restricción del piloto a los destinatarios configurados; sesión, CSRF, permisos por cliente e identificación de la solicitud. Bloqueo de duplicados y de reenvíos tras una aceptación desconocida.
- Actualización de caché del service worker conservando los borradores. Sin migraciones ni dependencias nuevas; sin cambios en fuente/ ni operaciones Git.
- Verificación local: 188 tests aprobados; compileall app/tests/scripts y sintaxis JavaScript, código 0. Gmail HTTPS simulado en las pruebas automatizadas. Actualización privada aplicada con respaldo y reinicio exclusivo de readyproof. Prueba real por API autenticada como tecnico_readyproof: carga ficticia nueva, dos firmas, PDF de 121951 bytes, un intento ok, Gmail id 1a17e6bd8e9a6df5. Enviados confirmado por MCP con el PDF adjunto; recepción en destino pendiente. Repetición de la solicitud sin nueva transmisión. Evidencia en out/envio_pdf_app/.


## 2026-10-27 — SAA-1 en una sola hoja A4, solicitado por Jorge

- Ajuste de impresión en la fuente de formato `fuente/herramientas/build_planilla.py`: SAA-1 usa A4 horizontal, una página de ancho y una de alto. Las filas, campos, textos, opciones y demás planillas no cambian. Original previo conservado en `bak/build_planilla_antes_A4_20261027.py`; informar a Martín del ajuste de impresión solicitado por Jorge.
- Nueva versión interna de la plantilla piloto `00-26-rp2`, con su huella nueva. Se registra por el comando normal `init-db --ejemplos`; las versiones, cargas, PDFs y envíos anteriores se conservan.
- Firmas posicionadas según el ancho real de la tabla impresa, con anclajes obtenidos del Excel y del PDF.
- La interfaz recupera también las definiciones de cargas históricas y ofrece **Crear copia A4**. La copia utiliza los datos y firmas disponibles en ese dispositivo, requiere vista previa y finalización y recibe identificador nuevo. El envío del PDF anterior queda deshabilitado desde ese cuadro, para usar la copia A4 revisada.
- La referencia v5 original de pruebas se conserva. La comparación de formato aplica exclusivamente el ajuste de impresión de una hoja; se mantienen las comprobaciones de filas, estilos, encabezado, pie y coincidencia visual.
- El catálogo JSON registra v3 por la nueva huella del generador; `--actualizar-version` conserva las copias v2 en `bak/planillas_json/v2/` y rechaza cambios de campos, textos u opciones. El alta en BD usa el comando normal `cargar-planillas`, sin sobrescribir las versiones anteriores.
- Verificación local: 190 tests aprobados; compileall y JavaScript código 0. Muestra A4 de una página revisada visualmente, con campos y firmas íntegros; copia histórica verificada en navegador. Desplegada en el servidor privado con respaldo y alta por CLI: piloto rp2 y catálogo v3. Verificados sin cambios los registros, firmas, credenciales, envíos e identificadores de las versiones anteriores. Prueba real: PDF de una sola A4, 119597 bytes y dos firmas ficticias, carga e91f8d38-b19d-5c38-9c62-fc365cf4cb2e, un intento ok; Gmail SENT id 1a17e9cc498e6fdc con el PDF adjunto. Recepción manual pendiente; repetición de la solicitud sin nueva transmisión. Evidencia en out/a4_una_hoja/.


## 2026-10-27 — Habilitación de SDI, SBC y SAL

- Jorge confirmó todas las planillas, agrupadas por sistema: SAA-1, SDI-1 a 5, SBC-1 a 6 y SAL-1 a 4. Confirmó la paginación del kit en A4 horizontal para las extensas; SAA-1 mantiene una sola A4. SAL conserva el nombre correcto, Extinción por Agentes Limpios.
- Diagnóstico: la base privada ya contenía diez registros de catálogo y versiones anteriores; solo existía el sistema SAA. Los grupos JSON no eran formularios individuales operativos. Se conservan los históricos y se habilitan cuatro familias / 16 planillas, sin forzar COUNT(*) a cuatro.
- Migración aditiva 009: registra las 15 nuevas planillas individuales y las asocia a los manuales existentes; agrega sistemas de ejemplo faltantes. La reversión preserva las plantillas usadas por cargas y firmas. Sin cambios de credenciales ni dependencias.
- Adaptadores de validación y carga Excel sobre el generador original, con opciones y unidades exactas del kit, matrices mensuales/semanales y listas de verificación. Nombres y asuntos de PDF según la planilla seleccionada.
- Selectores y encabezados dinámicos, tablas accesibles con desplazamiento dentro del formulario móvil, Administración con los cuatro sistemas y documentación por correo actualizada.
- Verificación local: 208 tests aprobados, compilación y JavaScript sin errores. Las 16 selecciones y formularios se probaron en navegador móvil; las 15 nuevas planillas emitieron PDF por la API normal con ambas firmas, leyenda y formato A4 del kit. Despliegue privado aplicado con respaldo y migración 009; las cargas, firmas, credenciales y envíos anteriores conservaron sus huellas. Los correos automatizados se simulan o archivan.

- Cierre: suite final **208 passed in 831.27s**, código 0; revalidación de firmas/A4/interfaz **13 passed**, compilación app/tests/migraciones/scripts y sintaxis JavaScript código 0. Los 18 tests nuevos cubren las 15 emisiones, catálogo/manuales, cambio entre las 16 planillas en navegador móvil y correo de documentación archivado.
- Revisión visual: ajuste de ubicación de firmas dentro de la parte visible de sus casilleros cuando el kit divide el recuadro entre páginas, sin cambiar el generador ni la paginación. Se revisaron las 29 páginas emitidas en Ubuntu para los 16 formularios, incluidas SBC-3 y SBC-6.
- Servidor privado: cuatro familias, 16 plantillas vigentes y 25 filas totales contando el catálogo y versiones históricas. Login HTTP 200; prueba con tecnico_readyproof por la API normal, 16 cargas ficticias emitidas y descargadas, ambas firmas/IRAM/logo/retención/formato/huellas verificados. No se transmitieron correos nuevos en esta prueba. Evidencia: out/multisistema/pytest_entrega.txt, despliegue.json y servidor/readyproof-multisistema-prueba.json. Sin cambios en fuente/, sin dependencias nuevas y sin operaciones Git.


## 2026-10-27 — Identificación de firmantes y documentación v1.0

- DNI resuelto por Jorge: 8–15 dígitos ASCII, sin puntos ni guiones. Nombre del responsable obligatorio, cargo opcional y ambas firmas exigidas por backend al finalizar y emitir. Los borradores conservan datos incompletos y guardado sin conexión.
- Migración aditiva `010_firmantes`: campos del responsable, identidad técnica capturada de la sesión y copia de identidades por revisión. No completa identidades históricas ni reescribe PDF emitidos. Acceso restringido por cliente, igual que las firmas.
- PDF con identificación complementaria al pie de la última página: técnico, responsable, DNI, cargo, empresas y fecha de servicio. Escala proporcional para reservar espacio, sin quitar filas ni cambiar orientación o paginación; SAA-1 conserva una hoja. Sin cambios en fuente/ ni dependencias nuevas. Informar a Martín de la franja adicional solicitada por Jorge.
- Documentación por correo: cuatro familias y requisitos del responsable, destinatario editable en modal sin cambiar perfil, auditoría usuario/destino/fecha, protección de doble clic e idempotencia conservada. Se adjuntan las guías sin contraseñas.
- Backlog CUIT/CUIL y numeración documentado en docs/BACKLOG_v1_1.md; sin implementar esas propuestas futuras.
- Verificación final: **232 passed in 972.26s (0:16:12)**, código 0. Compilación y JavaScript código 0; revisión sin secretos detectados. La incidencia inicial de memoria de Windows se resolvió antes de la ejecución final. La comprobación geométrica usa ahora la escala real de emisión; no cambió la ubicación de firmas para corregir ese test.

- Cierre v1.0: migración 010 aplicada en el servidor privado con respaldo; 16 planillas emitidas y descargadas como tecnico_readyproof por la API normal, con identidad técnica, nombre/DNI/cargo del responsable, empresas y fecha. Paginación original de las 16 comprobada (29 páginas), SAA-1 una hoja. Rechazo HTTP 422 sin responsable y conservación de históricos y credenciales comprobados. Correo actualizado y probado con archivo/transportes simulados, sin transmisión real nueva. Evidencia en out/final_v1/.


## 2026-10-28 — v1.1, Etapa 0: diagnóstico de planillas y respaldo

- Informe: `docs/DIAGNOSTICO_ETAPA0_V1_1.md`, con inventario de las 79 planillas y propuesta aditiva de modelos. Encargo: `INSTRUCCION_CODEX_planillas_SG-PEM-IFI_1.md` entregado por Jorge.
- Los 79 Excel oficiales coinciden entre los dos paquetes v5 y con catálogo/conteos del inventario. Las 16 definiciones habilitadas conservan 389 ítems/campos y coinciden entre local y servidor. Sin cambios de aplicación, fuente, BD, migraciones, originales ni despliegue.
- SDI-2: evidencia aislada de 36 selecciones guardadas en fila 24; las emitidas deshabilitan todos los controles. Pendientes reglas nuevas de observaciones, mediciones, visitas por período y desbloqueo. La evidencia no sustituye una prueba en teléfono físico ni una ejecución integral del arnés con salida 0.
- Respaldo observado: timer local activo; último dump leído en 009_multisistema frente a BD en 010_firmantes. No hay Drive, cifrado de archivo, retención ni alerta de fallo en el trabajo inspeccionado. Restauración actualizada pendiente.
- Decisiones de CUIT y numeración actualizadas en backlog: UUID conservado; CUIT único obligatorio en dos pasos; número solo al emitir, global, sin huecos ni reinicio anual, con contador transaccional.
- Verificación: cotejos automáticos y huellas de 16 archivos de producto sin cambios. La última suite integral registrada sigue siendo 232 passed; no se reejecutó en esta etapa documental. Evidencias en `out/diagnostico_v1_1/`.
- Se detiene después del informe conforme a la instrucción de Etapa 0. Siguiente: autorización de Drive por Jorge, respaldo y prueba de restauración antes de migrar. No se habilitó uso real.


## 2026-10-28 — Etapa 1: preparación de respaldo Drive y autorización iniciada

- Jorge volvió a autorizar expresamente OAuth de Drive y la restauración de prueba por Codex en una BD separada. Se conserva el modo piloto; no se autorizaron migraciones antes de verificar el respaldo.
- Rclone instalado desde los paquetes Ubuntu del servidor, sin actualizar otros paquetes ni reiniciar la aplicación. No existían rclone ni el remoto readyproof-drive.
- Nuevo script `scripts/autorizar_drive_backup.py`: consentimiento local con PKCE, verificación de la cuenta readyproof.ar@gmail.com, permiso drive.file, configuración remota privada y verificación de acceso sin imprimir tokens. Gmail permanece independiente.
- Preparados `scripts/backup_readyproof.py`, `scripts/servidor_backup/` y `docs/BACKUP_Y_RESTAURACION.md`: snapshot compartido entre dump y PDFs, AES-256-CBC/PBKDF2 y HMAC, descarga de comprobación, retención de 30 diarios y 12 mensuales, alerta Gmail y restauración en BD nueva con comparación de todos los conteos y hashes.
- Siete pruebas de seguridad sin red ni BD aprobadas (`tests/test_backup_drive.py`); compilación de los dos scripts Python sin errores. No se reejecutó la suite integral anterior de 232 pruebas.
- Pendiente: completar consentimiento Google, crear/custodiar clave fuera del repositorio, instalar y ejecutar el nuevo trabajo, acreditar subida/descarga y restauración 010. El timer anterior sigue intacto. No se declara completada la Etapa 1 ni se avanzó a las etapas 2–6.

- Ampliación de verificación: 8 pruebas del respaldo aprobadas; la alerta puede cargar Gmail aunque falte la clave de backup. Prueba real de OpenSSL en servidor: cifrado/descifrado correctos y archivo manipulado rechazado. Clave creada en /etc/readyproof/backup.env (0600), con copia de recuperación DPAPI CurrentUser verificada fuera del proyecto. Scripts de backup instalados; timer anterior intacto.
- Primer consentimiento Drive completado, pero la API estaba deshabilitada; Jorge informó que ya la habilitó. Se reinició la autorización con enlace local explícito porque la ventana automática no apareció. La conexión y restauración siguen pendientes hasta terminar ese consentimiento.


## 2026-10-28 — Etapa 1 completada: Drive, cifrado y restauración verificados

- OAuth de Drive finalizado para readyproof.ar@gmail.com, configuración privada 0600. El enlace local dejó de responder porque el asistente terminó correctamente; no era necesario volver a abrirlo.
- Respaldo consistente 010_firmantes subido a Drive, descargado y verificado: 25 planillas, 45 cargas, 45 firmas y 7 envíos. AES-256-CBC/PBKDF2 y HMAC; clave fuera del repositorio y recuperación DPAPI verificada en la PC administradora.
- Restauración final en readyproof_test_restore_20261028T040154: coinciden 17 tablas, 130 binarios y 48 PDFs exportados. Su huella coincide con el respaldo ejecutado bajo systemd. Evidencia: out/etapa1_backup/verificacion_drive_restore.json.
- Timer nocturno activo a las 02:00 UTC con jitter 15 minutos; retención 30 diarios/12 mensuales; OnFailure conectado a readyproof-backup-alerta.service mediante Gmail HTTPS. Ejecución real bajo systemd: success. Configuración anterior preservada.
- Ocho pruebas específicas del respaldo aprobadas; scripts compilados. No se reejecutó la suite integral de 232 pruebas. No se modificó fuente/, no se usó Git, no se aplicaron migraciones ni se reinició la aplicación. La base activa y el modo piloto permanecen sin cambios.
- Documentación: docs/BACKUP_Y_RESTAURACION.md. Pendiente siguiente etapa y sus confirmaciones según el encargo recibido; no se declara completada ninguna etapa 2–6.


## 2026-10-28 — Etapa 2 completada: CUIT opcional y sistemas activos

- Autorización expresa de Jorge para Etapa 2, manteniendo piloto y sin datos reales. Migraciones 011_cliente_cuit_opcional y 012_sistema_cliente_activo aplicadas; UUID y referencias existentes conservados, sin convertir las claves VARCHAR(36).
- Cliente.cuit opcional, único, once dígitos ASCII e índice; validación y normalización local por módulo 11 en app/utils/cuit_validator.py y en el modelo. El ejemplo 82000000000 se rechaza por verificador incorrecto; pruebas con números sintéticos. Sin atribuir el algoritmo a IRAM ni consultar padrones.
- Sistema.activo obligatorio, predeterminado true; cliente_id reafirmado NOT NULL. Downgrade protegido contra pérdida de CUIT o estados inactivos.
- scripts/audit_cuit.py ejecutado en solo lectura: 1 cliente ficticio sin CUIT, 0 duplicados/inválidos/no normalizados y 0 sistemas sin cliente; 4 sistemas activos. No se inventó el CUIT faltante ni se agregaron datos reales.
- Ensayo 010→012 en copia separada aprobado. Al aplicar, se detectó y corrigió un permiso 0700 del paquete nuevo producido por umask; quedó 0750/grupo readyproof, con importación comprobada como el usuario de la app. El modelo anterior compatible se mantuvo hasta corregirlo; migraciones no repetidas.
- Comparación histórica posterior con la copia 010 restaurada: 980 filas en 16 tablas, cero diferencias por hash; los únicos agregados fueron dos marcadores de esquema y un acceso de verificación. PDFs/firmas conservados.
- Respaldo 010 previo guardado aparte en Drive y restaurado; nuevo respaldo 012 bajo systemd descargado y restaurado en BD separada. Coinciden 17 tablas, 130 binarios y 48 PDFs exportados. Timer y aplicación activos; login HTTP 200.
- Pruebas: suite completa 265 passed + 1 error de setup por DiskFull; reintento del mismo caso: 1 passed. Total 266 casos únicos verificados, sin fallos pendientes. Se conservan los logs, incluidos intentos previos con configuración de Playwright/rutas largas. Ocho pruebas específicas del respaldo también aprobadas. Compilación: código 0.
- Evidencias: out/etapa2_cuit/resultado_etapa2.json e integridad_historica.json. Documentación: docs/ETAPA2_CUIT_Y_SISTEMAS.md y actualización de docs/BACKUP_Y_RESTAURACION.md. Sin Git, sin cambios en fuente/, sin cambiar credenciales ni activar modo real.
- Etapas 3–6 pendientes de sus confirmaciones y decisiones del encargo; CUIT NOT NULL pendiente de revisión administrativa de faltantes.


## 2026-10-28 — Etapa 3: implementación local verificada; puesta en servicio pendiente

- Jorge autorizó avanzar con medición obligatoria únicamente en verificación (ver). Nueva app/carga/validacion.py: O exige observación; ítems con unidad requieren número finito para ✓, O y X, salvo NA; general con unidad mantiene su comportamiento. Se usa el área de Observaciones original y no se completan datos automáticamente.
- Se ejecutan reglas completas al finalizar, previsualizar y emitir. Los borradores conservan carga parcial; omitir bloques no elude mediciones al cerrar. Descarga de PDFs históricos sin revalidación retroactiva ni regeneración. Las 16 definiciones existentes permanecen sin modificaciones.
- scripts/importador_planillas.py y app/planillas/importacion_excel.py: lectura determinista de directorio/ZIP, SHA256 y versión estable, cotejo de los 79 originales, filas/opciones/unidades, diferencias por líneas y transacción sin sobrescrituras ni inserción parcial. También se detectan cambios de tipos y huellas de las versiones aprobadas. --solo-catalogo opera sin conexión a BD; --aplicar inserta únicamente códigos nuevos y no los habilita en API.
- Cotejo operativo local: 79 Excel, 1.539 ítems y cero diferencias en los campos del catálogo; sin consultar BD. En PostgreSQL aislado: 16 YA_EXISTE + 63 A_IMPORTAR, creación de 63, segunda aplicación 79 YA_EXISTE y cero cambios; registros anteriores conservados. Los vínculos de manual faltantes se informan, no se inventan. Importación operativa/habilitación de las 63 reservada para Etapa 5.
- Verificación: 164 aprobadas en grupo 1; 134 aprobadas y un 503 al convertir SBC-2 en grupo 2. Reintento SBC-2: 1 aprobada. Pruebas finales del importador, con un caso adicional de tipos alterados: 7 aprobadas. Conciliación por identificador: los 300 casos actuales están cubiertos y aprobados, sin duplicar conteos ni omitir el fallo original. Su causa exacta no quedó registrada. Compilación sin errores.
- La revisión automática de aprobaciones rechazó la transferencia de código, catálogo y ZIP de 79 Excel al servidor compartido 67.205.170.29 por falta de autorización específica del destino para ese material interno. La orden no se ejecutó. Se solicitó autorización explícita para /var/backups/readyproof/revision-etapa3; pendiente de respuesta. Sin despliegue de Etapa 3 ni modificaciones de BD activa.
- Documentación: docs/ETAPA3_IMPORTADOR_Y_VALIDACIONES.md. Evidencia: out/etapa3_importador/resultado_local.json y cotejo_79_sin_bd.json, con logs/JUnit originales. Sin Git, sin cambios en fuente/ ni originales de Descargas. Modo real no habilitado.


## 2026-10-28 — Etapa 3 completada en servidor tras autorización de transferencia

- Jorge autorizó expresamente copiar código, catálogo y ZIP interno de los 79 Excel a 67.205.170.29, carpeta privada /var/backups/readyproof/revision-etapa3. Se completó la acción antes rechazada; SHA256 del ZIP verificado, carpeta 0700 y ZIP 0600. No se publicaron enlaces.
- Cotejo real en transacción de solo lectura: 79 Excel, 1.539 ítems, 16 YA_EXISTE + 63 A_IMPORTAR, cero cambios/errores. CLI instalado repetido con el mismo resultado. Se mantienen 25 registros de plantilla con sus históricos y 16 disponibles en la app.
- Reglas instaladas y comprobadas como usuario readyproof con datos ficticios en memoria y definición real: medición obligatoria en ver con unidad salvo NA; O exige observación; caso completo válido. Borradores siguen admitiendo datos en curso; PDF histórico no se revalida retroactivamente. No se crearon cargas, usuarios ni datos reales para el smoke test.
- Fuentes anteriores preservadas; seis archivos instalados coinciden con los verificados localmente. Durante la instalación, 17 tablas sin cambios, 130 binarios y las 25 definiciones/relaciones conservadas. Login HTTP 200; aplicación y timer activos. Alembic permanece en 012_sistema_cliente_activo; sin migraciones de datos en esta etapa.
- Respaldo previo y posterior verificados. Restauración posterior aislada en readyproof_test_restore_20261028T110135: esquema 012, 17 tablas y 48 PDFs exportados coincidentes; SHA256 igual al último respaldo en Drive. No se restauró sobre producción.
- Evidencia final: out/etapa3_importador/resultado_servidor.json. Pruebas: 300 casos actuales conciliados, conservando el 503 original de SBC-2 y su reintento correcto. Sin Git, sin cambios en fuente/ ni originales de Descargas, sin habilitar modo real ni las 63 planillas pendientes.
- Documentación actualizada: docs/ETAPA3_IMPORTADOR_Y_VALIDACIONES.md. Etapa 4 pendiente de confirmación según el encargo.


## 2026-10-28 — Etapa 4 autorizada: desbloqueo y revisión pública

- Jorge confirmó avanzar con desbloqueo solo para creador/admin y los cuatro estados del kit. Implementación aditiva 013: contador global transaccional, número único asignado al emitir, revisión pública independiente de la revisión optimista, huella compatible, motivo/autor de desbloqueo y estado de anulación reservado.
- Historial de emisiones con PDF y SHA256 originales, datos y firmantes; bloqueo PostgreSQL de UPDATE/DELETE. Desbloqueo con motivo obligatorio, control de cliente, CSRF, permisos y concurrencia. Las firmas deben volver a dibujarse; se conserva el PDF previo sin reescribirlo ni renumerar históricos.
- Botones Desbloquear con motivo y Emisiones anteriores; número/revisión visibles en pantalla y al pie del PDF. SW v8, sin borrar IndexedDB. Envíos deduplicados por PDF y destinatario, de modo que una revisión nueva pueda enviarse conservando la copia anterior. Gmail simulado en pruebas: no se enviaron correos reales.
- Validador SDI mantiene ✓/O/X/NA y no exige meses futuros. No cambia definiciones, filas, normas, fuente/ ni originales de Descargas. Sin nuevas dependencias ni Git.
- Respaldo ampliado para PDF del historial, con compatibilidad de restauración de esquemas anteriores. Ensayo remoto de 013 en readyproof_test_etapa4_20261028T112602: 972 filas históricas de 15 tablas sin diferencias; base activa sin cambios. Primer intento del ensayo se detuvo porque el rol supuesto no existía; se corrigió para usar el rol configurado, sin cambiar sus credenciales.
- Revisión visual de muestra ficticia: una hoja A4 horizontal, cuatro imágenes (dos logos y dos firmas), leyenda IRAM y número/revisión legibles. Compilación sin errores. Pruebas completas y aplicación: cierre pendiente de los resultados reales, que se registrarán a continuación.
- Documentación de funcionamiento y límites: docs/ETAPA4_DESBLOQUEO_Y_REVISION.md. Etapas 5 y 6 continúan pendientes de confirmación.


## 2026-10-28 — Etapa 4: desbloqueo/revisión aplicados y verificados

- Esquema 013 aplicado en el servidor privado, 972 filas históricas sin diferencias. Fuentes anteriores conservadas, respaldo pre-013 verificado. Sin carga de datos reales ni cambios de credenciales.
- Numeración solo al emitir, sin saltos de rollback; originales nuevos en revisión pública 0 y primera corrección en 1. Mismo número al reemitir; PDF anterior inmutable y accesible. Motivo, actor y revisión quedan en el historial; nueva revisión exige ambas firmas otra vez.
- Suite: 325 casos actuales cubiertos, sin fallos pendientes ni omitidas, conciliados por identificador entre tandas. Primera tanda 187 aprobadas/2 fallos; segunda 192 aprobadas/1 fallo; cierre 59 aprobadas. No se afirma una única ejecución limpia de 325. Se corrigieron el PDF simulado sin IRAM, autoflush durante emisión y espera del diálogo móvil. Pruebas iniciales de migración/sesión también ajustadas; registros originales conservados.
- Recorrido móvil y revisión visual aprobados: emisión, desbloqueo con motivo, datos conservados, firmas nuevas, reemisión, historial 0/1 y original idéntico. Envío nuevo y deduplicación probados con Gmail simulado; ningún correo real enviado en esta etapa. Compilación sin errores y revisión de secretos sin hallazgos.
- Login HTTP 200, fuentes probadas iguales a instaladas, JS nuevo servido, SW v8, usuario de servicio readyproof y timer activo. Respaldo 013 restaurado aisladamente en readyproof_test_restore_20261028T115558: 19 tablas, 130 binarios y 48 PDF exportados coincidentes. Base activa conservada.
- Documentación: docs/ETAPA4_DESBLOQUEO_Y_REVISION.md y ampliación de BACKUP_Y_RESTAURACION.md. Evidencia final: out/etapa4_revision/estado_suite.json, aplicar.json y verificacion_servidor.json.
- Este corte cubre las tareas enumeradas de desbloqueo/revisión y SDI. Datos dinámicos ampliados, establecimientos/precargas y operación de anulación continúan pendientes; no se declaran entregados. Etapas 5/6 y uso real requieren confirmación. Sin Git ni cambios en fuente/ ni originales.


## 2026-10-28 — Etapa 5: cotejo previo de solo lectura

- Autorización recibida. Cotejo ejecutado con ZIP oficial: 79 Excel, 1.539 ítems, cero diferencias; sin conexión ni cambios de BD. Reporte: out/etapa5_planillas/cotejo_79_sin_bd.json.
- Nombres del pedido y revisión inicial contradicen el kit o la regla aplicada en etapa 4. Se solicitaron las aclaraciones exigidas por AGENTS.md antes de los cambios dependientes. No se inició implementación ni se habilitaron familias.
- Total de referencia corregido: 325 actuales + 189 nuevos = 514 mínimos. Estado previo, todavía sin importación ni migración: out/etapa5_planillas/etapa5_planillas.json.


## 2026-10-28 — Etapa 5: detector estricto de siglas preparado localmente

- Nombres oficiales y revisión original 0 confirmados. Nueva extracción estricta extraer_sigla_planilla en scripts/importador_planillas.py; lectura de primeras 20 filas sin alterar bloques/definiciones ni originales. Rechaza ausencia, ambigüedad y contradicción con el nombre de archivo. Consulta de instalaciones activas por sigla y cliente conserva instalaciones múltiples y excluye otros clientes.
- Cuatro pruebas nuevas aprobadas y prueba existente de cotejo/huellas de 79 originales aprobada; compilación sin errores. Evidencia JUnit: siglas_estrictas.xml y cotejo_lector_ampliado.xml en out/etapa5_planillas.
- Auditoría literal: los 79 originales carecen de (XXX), pero los 79 códigos internos coinciden con los archivos/catálogo. Se solicitó aclaración para usar ese código como alternativa. No se cambió la regla por cuenta propia ni se fabricaron coincidencias.
- Sin importación, migración ni despliegue; etapa 5 todavía no está completa. Mínimo de casos previsto: 518 (325 + 4 + 189). Informe de estado actualizado: out/etapa5_planillas/etapa5_planillas.json.

## 2026-10-28 — Etapa 5: importación y verificación del catálogo completo

- Jorge confirmó nombres oficiales, emisión original con revisión pública 0 y primera corrección 1. Autorizó extraer siglas desde código interno, paréntesis o archivo, con cruce de al menos dos fuentes y rechazo obligatorio de paréntesis contradictorios. Los 79 originales coinciden entre código interno, archivo y catálogo; no contienen paréntesis en las primeras 20 filas. No se modificaron originales.
- Incorporadas 63 definiciones versionadas `00-26-ms1`, protegidas por huellas, origen Excel y reconstrucción determinista desde el generador. El importador conserva versiones anteriores, rechaza diferencias de contenido/cabecera y es idempotente. Se mantienen instalaciones múltiples por cliente/sigla.
- Migración aditiva 014: 63 planillas nuevas y 11 familias nuevas para clientes ficticios. Ensayo sobre copia aislada y aplicación protegida con respaldo previo. Resultado real: 16 YA_EXISTE, 63 IMPORTADA, cero diferencias; 79 códigos activos y 88 filas incluyendo versiones históricas; 15 sistemas. Todos los registros anteriores conservaron sus huellas. Reimportación de solo lectura posterior: 79 YA_EXISTE y cero cambios.
- Configuración, API, administración, selectores y correo de documentación ampliados a las 15 familias/79 planillas. Navegador: 79 formularios, 15 sistemas, cero errores. Service worker v9 servido y aplicación privada activa; modo piloto intacto. No se enviaron correos reales ni se cambiaron credenciales.
- Suite consolidada por plataforma: 525 casos únicos aprobados, 479 Ubuntu + 46 Windows. Incluye 189 recorridos nuevos (borrador/validación/emisión), ocho casos de siglas y regresiones de importación y respaldo. Se conservan los resultados iniciales y reintentos; no se presenta como una única invocación. Los fallos iniciales fueron expectativas del catálogo anterior, longitud de datos ficticios de cabecera y falta de espacio local; los casos afectados quedaron verificados sin fallos pendientes.
- Los 63 PDF nuevos suman 97 páginas; cotejo de filas, títulos, paginación contra Excel oficial, A4 horizontal, leyenda IRAM, logos, firmas, metadatos e historial. Renderizadas todas las páginas, revisadas nueve láminas y representantes de los cuatro formatos. Se acortaron solo ejemplos nuevos para evitar saltos por cabeceras artificialmente largas; formato/generador y filas intactos.
- Corregida la lista de archivos de restauración: admite también PDF de `emisiones_carga`, ya incluidos en el respaldo desde etapa 4. Nuevas pruebas de esa restauración y de rechazo de nombres de BD no autorizados.
- Respaldo posterior del esquema 014 cifrado en Drive y restauración verificada en `readyproof_test_etapa5_20261028T140301`: 19 tablas, 130 binarios y 48 PDF exportados coincidentes. Otros 189 recorridos aprobados, código 0, sobre clones efímeros de esa restauración; copia restaurada original sin cambios. Timer activo.
- Compilación de app/tests/scripts/migraciones: código 0. Sin patrones de secretos detectados en el paquete; `.env`, claves, tokens y BD excluidos de la transferencia. Transferencia privada expresamente autorizada a `/home/readyproof_revision_etapa5`, modo 0700, con manifiesto. No se agregaron dependencias, no se usó Git ni se alteraron otros servicios o `fuente/`.
- Informe: `out/etapa5_planillas/etapa5_planillas.json`; procedimiento y límites: `docs/ETAPA5_IMPORTACION_79_PLANILLAS.md`. Pendiente normativo detectado: SCC-1 oficial usa MPa donde el encargo general indica bar; consulta enviada, sin conversiones ni cambios de unidades. Se mantiene el piloto, las asociaciones de manuales reales y demás pendientes previos. Etapa 6 no iniciada.

## 2026-10-28 — Decisión confirmada sobre unidades de SCC-1

- Jorge confirma conservar MPa del kit literal, sin bloquear el cierre verificado de etapa 5 en modo piloto. No se modifica la aplicación, la BD, los Excel ni los PDF históricos.
- Generador del informe y reporte actualizado con `unidad_encontrada: MPa`, `unidad_esperada: bar`, `estado: REVISAR_CON_MARTIN`. Documentación y preguntas abiertas actualizadas para distinguir la decisión operativa resuelta de la decisión normativa pendiente.
- Martín confirma las unidades antes de etapa 6 y de habilitar uso real. Una eventual corrección queda prevista por Jorge como migración 016 independiente, sin implementarla ahora. Se conserva la evidencia de 525 pruebas y 189 recorridos sobre restauración de la entrega anterior; esta actualización solo modifica documentación e informe.


## 2026-10-28 — Índice de auditoría de las etapas v1.1 0–5

| Etapa | Alcance y migraciones reales | Documentación/evidencia |
|---|---|---|
| 0 | Diagnóstico de solo lectura; esquema 010 existente; sin migración | docs/ETAPA0_DIAGNOSTICO.md, docs/DIAGNOSTICO_ETAPA0_V1_1.md, out/diagnostico_v1_1/ |
| 1 | Backup cifrado y restauración; sin migración nueva | docs/ETAPA1_BACKUP.md, docs/BACKUP_Y_RESTAURACION.md, scripts/backup_readyproof.py, out/etapa1_backup/ |
| 2 | CUIT opcional 011_cliente_cuit_opcional.py; sistemas activos 012_sistema_cliente_activo.py | docs/ETAPA2_CUIT_Y_SISTEMAS.md, out/etapa2_cuit/ |
| 3 | Importador y validaciones; conserva esquema 012, sin nueva migración | scripts/importador_planillas.py, docs/ETAPA3_IMPORTADOR_Y_VALIDACIONES.md, out/etapa3_importador/ |
| 4 | Desbloqueo, numeración e historial inmutable: 013_desbloqueo_revision.py | docs/ETAPA4_DESBLOQUEO_Y_REVISION.md, out/etapa4_revision/ |
| 5 | 63 planillas nuevas y 11 familias: 014_habilitar_11_sistemas.py | docs/ETAPA5_IMPORTACION_79_PLANILLAS.md, out/etapa5_planillas/ |

Las seis etapas corresponden al 28/10/2026 y sus secciones anteriores contienen las comprobaciones y límites. No existe migración 015 en este corte; no se inventa una para ajustarse a un ejemplo del pedido. Los cambios históricos no se separaron en commits por etapa; por ello no se atribuyen cifras de archivos, líneas o commits a cada etapa sin una base verificable. Los manifiestos y diffs de esta auditoría registran su alcance real.

## 2026-10-28 — Auditoría punto 6 reanudada por autorización expresa

- Jorge autoriza conservar cinco diferencias necesarias en fuente/ frente a la base 4cb1599, documentadas en RECORD_CAMBIOS_FUENTE.md y CAMBIOS_AUTORIZADOS_EN_FUENTE.md. No se revierten ni se alteran generadores, JSON, unidades o datos históricos.
- Se agrega .env.*.local a .gitignore; .env y .env.local ya estaban excluidos y ninguno tiene seguimiento en el índice. La revisión de 53 referencias de secretos no identificó credenciales hardcodeadas. No se copiaron valores secretos a reportes.
- Documentación de etapas 0/1 identificada con nombres uniformes, índice de etapas completo y preguntas SCC/SDI registradas sin tomar decisiones normativas. Permisos, manifiesto, pruebas y cierre de auditoría se verifican en sus reportes; no se declaran aprobados antes de ejecutarlos.


## 2026-10-28 — Auditoría detenida ante primer fallo de pruebas

- Punto 6 estático verificado: cero secretos hardcodeados entre 53 referencias revisadas; .env sin seguimiento; .env.*.local excluido; cinco diferencias necesarias autorizadas y conservadas por SHA256; app/ corregida a 0755, carpetas privadas en 0700; compilación app código 0.
- Manifiesto histórico de etapa 5: 185 archivos del paquete original, tamaños y SHA256 verificados contra destino antes de la copia posterior de auditoría. Documentación 0/1, preguntas SCC/SDI e índice de etapas completados.
- Pruebas post-correcciones: Ubuntu 479 aprobadas, código 0. Windows: primer caso test_copia_a4_conserva_pdf_anterior falló; 45 casos no ejecutados por -x. Mensaje: page.waitForResponse: Target page, context or browser has been closed, tests/browser/a4_historica.cjs:33, propagado en tests/test_a4_historica.py:41. Causa raíz no determinada.
- Se cumple la instrucción del encargo: detener y reportar ante cualquier test fallido. Sin reintentos, cambios de aplicación/fuente/BD ni commits posteriores al fallo. No se presenta la suite anterior de 525 como resultado post-auditoría.
- Reportes: seguridad_correcciones.json (punto 6 estático completado), AUDITORIA_CORRECCIONES_FALTANTES.json y AUDITORIA_ETAPAS_0_A_5.json (AUDITORIA_CON_BLOQUEADORES). Auditoría específica de producción y cierre de los puntos 1–5 pendientes de la indicación de Jorge para diagnosticar/corregir y continuar.


## 2026-10-28 — Cierre de auditoría y corrección del recorrido A4

- Jorge autorizó diagnosticar y corregir el fallo A4. Reproducción diagnóstica sin cambio de test aprobada; se identificó una promesa de espera de emisión sin gestión inmediata que podía ocultar el error de una acción anterior al cerrar el navegador. No se atribuyó sin evidencia a corrupción del PDF ni a insuficiencia del timeout.
- Corrección específica en tests/browser/a4_historica.cjs: Promise.all para clic/respuesta de vista previa y emisión; espera de diálogo cerrado y botón habilitado; espera explícita de estado de vista previa con límite de 90 segundos. Sin pausas fijas ni reintentos automáticos; aplicación y fuente sin cambios por el arreglo. Caso focalizado: 1 aprobado en 41,24 segundos, verificando original idéntico, copia de un A4 y cuatro imágenes. Commit b750f79cbc1700b411aba245481dbd003bf2b0a5.
- Suite completa posterior: 479 Ubuntu + 46 Windows = 525 aprobadas, cero fallos y cero omitidas; dos plataformas, no una única invocación. Se conservan el primer fallo, diagnóstico, caso focalizado, JUnit de ambas tandas y reportes bloqueados anteriores en out/auditoria_punto6/.
- Código instalado: 103 archivos comprobados, 75 idénticos y 28 con diferencias exclusivas de fin de línea; cero diferencias funcionales. Esquema 014, 19 tablas, 79 planillas activas (88 filas con versiones históricas), 15 sistemas, restricciones validadas y trigger de inmutabilidad presentes. Consultas de producción solo lectura.
- Binarios actuales: 48 PDF y 82 PNG válidos, 130 en total; cero hashes inconsistentes y cero PDF sin hash persistido. No se reescribieron documentos históricos. Servicio ejecutado por readyproof, timer activo y JS servido igual al verificado.
- Respaldo nuevo cifrado en Drive y restauración aislada en readyproof_test_etapa5_20261028T151304: esquema 014, conteos de 19 tablas, 130 binarios y 48 PDF coincidentes. No se restauró sobre producción. Evidencia: out/auditoria_punto6/respaldo_restauracion_actual.json.
- Manifiesto actual de 189 archivos: 187 del paquete y dos controladores privados de prueba, sin diferencias contra destino. El manifiesto histórico de 185 se conserva aparte. No se incluyen .env, claves, tokens ni BD en el paquete transferido. Permisos finales: backups y revisión privada 0700, app/ 0755.
- Compilación final app/tests/scripts/migraciones sin errores; entornos ignorados y sin seguimiento; cinco cambios necesarios de fuente conservados por SHA256 y autorización. Documentación 0/1, preguntas SCC/SDI, índice y manifiestos completos. Veredicto de AUDITORIA_ETAPAS_0_A_5.json y AUDITORIA_CORRECCIONES_FALTANTES.json: AUDITORIA_COMPLETA_OK para este corte en modo piloto.
- El commit de seguridad/documentación incorpora .gitignore y los reportes de auditoría; no consolida otros cambios previos de la aplicación y no realiza push. Persisten los pendientes normativos y de alcance documentados; etapa 6 y modo real no se habilitan.


## 2026-10-28 — Etapa 6: búsqueda, auditoría y modo configurable

Búsqueda autenticada por número de registro y auditoría transaccional de altas, cambios, emisión y desbloqueo de cargas. Migración 016 con historial inmutable; acceso de auditoría solo admin. Modo real configurable y validado, conservado desactivado. PDF nuevos identifican PILOTO/REAL; anteriores intactos. Correo restringido por modo y destinatario de prueba.

Suite final: 541 aprobadas (494 Ubuntu, 47 Windows), sin fallos ni omisiones; cobertura de líneas Python app/ 93,04 %. Compilación código 0. Coverage 7.17.0 se agrega solo a desarrollo para medir el criterio solicitado. Se conservan los cinco cambios de fuente previamente autorizados; atributos Git preservan sus bytes y la huella del catálogo.

Despliegue privado en piloto con migración ensayada y respaldo previo. El primer arranque detectó un permiso insuficiente en app/auditoria por umask 0077; corregido a 0750 y registrado en el instalador. Verificación posterior y restauración documentadas en el reporte final. No se activa modo real, no se envían correos reales de prueba y no se publican cambios. Pendientes: empresa/certificado, decisiones de Martín y autorización final según checklist.


## 2026-10-28 — Transición autorizada a producción real

Activación efectiva: 2026-10-28T14:40:22.502176-03:00. Jorge confirmó READYPROOF, certificado IFI-2024-10001 y checklist aprobado. MODO_PILOTO=false y MAIL_MODO_PRUEBA=false en .env y .env.local privados; se verificó el proceso después de responder HTTP. No se versionan esos archivos ni se cambian credenciales.

Migración aditiva 017 y SCC-1 00-26-bar1, J21 en bar, conservando la versión en MPa y todos los valores anteriores. SDI mantiene cuatro estados. Fuente íntegra. Cargas, firmas, PDF y usuarios comparados sin cambios. La copia A4 se restringe a SAA-1 para impedir trasladar números de MPa a bar; los borradores SCC anteriores requieren una nueva carga revisada.

543 pruebas finales aprobadas (496 Linux + 47 Windows), cero fallos u omisiones; los 541 casos anteriores permanecen. Tres verificaciones posteriores de interfaz también aprobadas, sin sumarlas dos veces. Compilación código 0. Se corrigió una referencia nula al terminar la sincronización después de cerrar sesión y se agregó reproducción controlada en la prueba existente. Pie de pantalla condicionado al modo real.

La primera comprobación del entorno del proceso se hizo antes de terminar el arranque; la configuración se revirtió de forma automática. Se corrigió la sincronización del verificador para esperar HTTP antes de comprobar los cuatro parámetros. Diagnósticos preservados en out/transicion_real_20261028/ y en la carpeta privada de respaldos. Un 503 de conversión Windows no se reprodujo en la comprobación instrumentada ni en la tanda final aprobada; no se modificó el convertidor por ese episodio.

Respaldos cifrados antes de 017, antes del corte y después. Restauración posterior aislada: 20 tablas, 130 binarios y 48 PDF cotejados; 89 versiones de planilla y 79 activas. Sin restaurar producción ni enviar correos reales de prueba. Monitoreo manual de 24/48 h documentado; no se crea automatización nueva.

Documentación: docs/TRANSICION_EXITOSA.md y TRANSICION_REAL_REPORTE.json. Tag solicitado: v1.1-real-20261028T1353. Los pendientes del backlog ampliado conservan su alcance documentado.

## 2026-10-28 — PWA: preparación local pendiente de validación

Manifest JSON con cuatro iconos, metadatos de instalación compartidos, registro único en /sw.js y atajo de búsqueda con vista autenticada. Iconos PNG RP generados programáticamente con Pillow en 192 y 512, normales y maskable con fondo opaco. No se modifican fuente ni registros, firmas o credenciales.

Implementación canónica en app/static/service-worker.js: precarga de assets públicos, cache-first para esos assets, red primero para la pantalla principal, skipWaiting y clients.claim. Compatibilidad con la URL /sw.js existente; no se duplican handlers fetch. Se actualiza la regresión de worker para leer la implementación canónica. Tres tests PWA preparados y documentación en docs/PWA_INSTALACION.md.

Validación pendiente: la revisión automática de comandos no pudo completarse por límite de uso. No se ejecutaron los tests PWA ni se realizó despliegue, commits o tag de esta entrega. El modo REAL previamente verificado no fue modificado en el servidor. No afirmar HTTPS en la IP pública: el acceso actual es privado por túnel local del propio dispositivo. La guía corrige el ejemplo de reenvío a -L, puerto local 8876 y destino del servidor 127.0.0.1:8000.


## 2026-10-28 — PWA: validación local aprobada y despliegue privado autorizado

Jorge autoriza retomar sin la aserción navigator.onLine. Chrome verificó manifest, cuatro iconos, un worker activado y cero errores de instalabilidad. Con Flask apagado, la pantalla y carga.js se recuperaron de caché y la API quedó inaccesible. Tests PWA 3/3 y regresión del worker aprobados; compilación código 0. Suite aislada Linux 499 aprobados. Windows: 46 aprobados y un error DiskFull de PostgreSQL; Jorge confirma la etapa local completada y pide verificar los tres tests en el servidor.

La verificación remota será por túnel privado, sin cambiar el HTTPS público. Puerto real del servicio: 8000, destino del reenvío local 8443. Se conserva la fuente, las credenciales, el modo REAL y los registros existentes. El resultado efectivo y la publicación del tag se documentan en REPORTE_PWA_FINAL.json, sin anticipar éxito antes de las comprobaciones.


## 2026-11-04 — Alta a demanda por CUIT (copia de prueba)

Búsqueda exacta en Contabilium mediante el filtro documentado en la colección local. Acción manual en el alta: completa solo campos vacíos, conserva valores ingresados y descarta respuestas de consultas anteriores. Si no hay resultado, se ofrece la consulta ARCA manual para razón social y domicilio fiscal. No guarda automáticamente, no incorpora migraciones ni dependencias. Pruebas con datos ficticios y transporte bloqueado, incluida conservación de campos y ausencia de mutaciones desde el navegador. Contrato y funcionamiento en docs/BUSQUEDA_CUIT_CONTABILIUM.md. Sin despliegue ni llamadas reales.


## 2026-11-04 — Conservar destinatario al cargar correo

El diálogo conserva el destinatario escrito o borrado por el usuario mientras llega la configuración. El valor predeterminado se propone solo si no hubo edición. Cada apertura parte con el campo vacío y las respuestas anteriores se descartan al cerrar o volver a abrir. Se actualiza la versión de caché y se agregan cinco casos de navegador a 390 px con configuración demorada, sin envíos reales ni dependencias nuevas. Evidencia y comparación de suite en CORRECCION_DESTINATARIO.json. Sin despliegue.


## 2026-11-09 — Formato A4 de planillas emitidas

Se amplió el ancho útil en la copia de impresión, se unificaron las filas de identificación y se amplió la celda del certificado. Los resultados cargados se muestran centrados y en negrita. Se incorporó la marca vigente al encabezado y al anexo fotográfico, se reservó espacio para el sello ISO y se quitó del pie la repetición de empresa y fecha. El certificado vigente, las definiciones del kit y los PDF archivados se conservan. La numeración por sistema queda pendiente de confirmación.


## 2026-11-09 — Identidad Readyproof, manual 1.0

Las pantallas, la aplicación instalable, los correos y los PDF nuevos incorporan los recursos originales del kit de marca. Se aplican la variante horizontal, el sello reducido, la paleta BFM y las tipografías Archivo Black y Fira Sans. El correo usa Arial como alternativa prevista por el manual. La marca de agua de Readyproof deja de aplicarse a las nuevas emisiones. Los archivos de fuentes incluyen sus licencias OFL.

## 2026-11-09 — Variante principal de identidad

- Por indicación de Jorge, se usa el logotipo principal vertical original del kit en la app, planillas, anexos y correos. El favicon y los iconos instalables usan el sello reducido.
- Se ajusta la reserva de encabezado A4 y se renueva la caché de la PWA para cargar el SVG principal.

- Se amplía proporcionalmente el sello ISO en el encabezado de nuevas planillas con el logotipo principal.

- Los iconos instalables llevan fondo blanco opaco. La verificación operativa compara el logo del PDF con el PNG compuesto sobre blanco.

## Certificado conjunto de prueba

- Permiso administrable por cuenta, con asignación inicial en la migración y control en servidor.
- Se prepara una propuesta con planillas ficticias, anexos y certificado al final. Se conserva la leyenda de propuesta y el sello vectorial de la referencia.
- El correo de prueba se descarga como archivo EML. La emisión y el transporte real quedan pendientes de autorización.

## Corrección de la propuesta de certificado conjunto

- La propuesta conserva el encabezado de la referencia y el firmante aprobado. La firma se lee de la referencia V2 privada, verificada por SHA-256, y queda fuera del repositorio.
- La migración 022 crea el permiso deshabilitado para todas las cuentas. Administración registra cada habilitación o revocación en auditoría.
- El formulario de propuesta es exclusivo de Administración y bloquea una tercera planilla. La descarga verifica el permiso en el servidor.

## Almacenamiento privado de la firma de certificado

- Administración carga PNG normalizados en el directorio privado de la instancia. El puntero y la auditoría se confirman en una transacción. Se conservan las versiones anteriores.
- La migración 023 crea únicamente la tabla de metadatos. El certificado verifica la huella antes de leer la firma y la referencia V2 queda reservada a pruebas.

## Certificado conjunto con habilitación independiente

- La propuesta y su enlace de Administración requieren habilitación explícita, permiso de usuario y rol de administrador. Se conserva la etiqueta de propuesta y la restricción a planillas ficticias.
- El recurso de firma de referencia sigue disponible solo en pruebas. La carga de firma y los flujos de planillas, correo e integraciones conservan su lógica.
