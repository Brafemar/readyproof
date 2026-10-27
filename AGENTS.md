# Encargo final: readyproof, aplicación de carga y emisión de planillas SG-PEM-IFI (readyproof)

> Documento de encargo para un agente de IA de programación. Está escrito para ser autosuficiente: no depende de ninguna conversación previa. Leelo completo antes de tocar código. Si algo contradice este documento y los archivos del kit, **detenete y preguntá**.

---

## 0. Cómo usar este documento (para el agente)

1. Leé este encargo completo.
2. Leé `fuente/KIT_AGENTS.md`. Es la guía del proyecto de manuales y planillas (copia del `AGENTS.md` del kit interno v5): contiene las reglas normativas, el formato y las decisiones abiertas. **Las reglas de ese archivo rigen también esta aplicación.** Este archivo, `AGENTS.md`, es el encargo.
3. Leé `fuente/herramientas/` del kit: ahí están los generadores de planillas y el origen de los datos.
4. Trabajá por **etapas** (sección 7). No avances a la etapa siguiente sin cumplir los criterios de aceptación de la actual.
5. Ante la duda sobre una decisión de negocio, normativa o de infraestructura, **no la decidas**: listala en `PREGUNTAS_ABIERTAS.md` y seguí con lo que no dependa de ella.

---

## 1. Contexto

- **Empresa:** readyproof, Mendoza, Argentina. Inspección, prueba y mantenimiento de instalaciones fijas contra incendios.
- **Responsable técnico de la serie:** Lic. Martín Sánchez. **Toda interpretación normativa la confirma él.**
- **Administración:** Jorge Sánchez.
- **Serie de referencia:** manuales SG-PEM-IFI basados en la IRAM 3546:2011, complementados con normas NFPA y UL. Cada manual tiene planillas Excel de registro y un informe general en Word (`-IN`).
- **Qué existe hoy:** los 15 manuales (SDI, SRA, SAP, SRE, SGE, STM, SBC, SAA, SHC, SEP, SSA, SCC, SAL, SDC, SIM), 79 planillas `.xlsx` generadas por script, 15 informes `-IN` y los PDF. Todo se genera desde código Python a partir de datos declarativos.
- **Qué falta:** una aplicación que el técnico use en campo para cargar la planilla, que la guarde, emita el PDF o Excel con el formato de la serie y la envíe al cliente.

## 2. Objetivo

Construir una aplicación web que permita:

1. **Autenticar** técnicos y administradores (usuario y contraseña, roles).
2. **Seleccionar** un cliente y un sistema, y elegir una planilla de las disponibles.
3. **Cargar** la planilla con los mismos campos, opciones y secciones que la planilla impresa de la serie.
4. **Guardar** la planilla cargada, con trazabilidad (quién, cuándo, qué versión).
5. **Emitir** la planilla terminada **solo en PDF**, con el encabezado, logos, pie y firma de la serie. El .xlsx es un paso interno y no se entrega al cliente.
6. **Enviar** el PDF por correo al destinatario indicado, como adjunto y sin enlaces de descarga, y guardar copia.
7. **Conservar** los registros al menos **3 años** (regla de la serie: «T.C. 3 AÑOS»).

- **Firma en pantalla:** el técnico y el responsable del cliente firman con el dedo o el mouse, y la firma aparece en el PDF.

**No es objetivo de esta etapa:** facturación, turnos, stock de matafuegos, geolocalización, firma digital con certificado.

## 3. Reglas que no se rompen

Estas reglas vienen del proyecto de manuales y aplican a todo lo que se genere:

### 3.1 Normativas y de contenido
- **No inventar valores, frecuencias ni campos.** Cada campo de una planilla existe en el dato fuente (`planillas_data*.py`) o en la norma. Si falta algo, preguntar.
- **No cambiar las filas de una planilla.** Una planilla de la norma puede tener filas agregadas, nunca quitadas ni reordenadas. Las opciones (✓ / O / X / NA; SI / NO) se mantienen tal cual.
- **Codificación de tres símbolos:** ✓ cumple · **O** no cumple · X no apreciable · NA no aplicable. La «O» es un símbolo, no la conjunción «o».
- **«T.C. 3 AÑOS»** debe figurar en el encabezado de cada planilla emitida.
- **Leyenda visible:** «Planilla conforme a IRAM 3546:2011» en la pantalla de carga y en el PDF. Confirmar el texto exacto con Martín.
- **Copias de normas:** no incluir normas ni fragmentos extensos de normas en el código, en la base de datos ni en los PDF. Solo se pueden usar citas breves que ya están en las planillas.

### 3.2 Datos y privacidad
- **No hay datos reales de clientes en el repositorio, en las pruebas ni en los ejemplos.** Usar datos ficticios marcados como `[Ejemplo]`.
- **No hay marcas, modelos ni nombres de clientes** dentro del código o de la interfaz, salvo que la decisión venga de Jorge.
- Las firmas son datos personales: se guardan cifradas o con acceso restringido, y solo se muestran dentro de la planilla a la que pertenecen.
- Las credenciales, claves y tokens **nunca** van en el código. Se leen de variables de entorno (archivo `.env` que no se versiona).
- El sistema debe cumplir la **Ley 25.326 de protección de datos personales** (Argentina): acceso restringido, registro de quién accede, posibilidad de exportar y borrar datos de un cliente cuando corresponda.

### 3.3 Calidad del entregable
- **Sin rastros de generación automática** en textos visibles para el usuario ni en comentarios de los archivos entregados.
- El PDF emitido debe coincidir con la planilla de la serie: mismo encabezado, mismas filas, mismo pie.
- Textos en **español rioplatense técnico**, con tildes también en mayúsculas.

### 3.4 Restricciones de herramientas
- **No agregar repositorios de GitHub, ni crear cuentas en servicios externos, ni publicar nada en internet** sin autorización explícita de Jorge.
- **No instalar ni desplegar** en un servidor real. Solo preparar el código y las instrucciones de instalación.
- **No enviar correos reales** durante las pruebas. Usar un servidor de correo de prueba o un registro en archivo.

## 4. Stack tecnológico (propuesto; confirmar al inicio)

| Capa | Elección | Motivo |
|---|---|---|
| Lenguaje y backend | **Python 3.11+**, **Flask** (o FastAPI si Jorge lo prefiere) | Las herramientas de generación ya están en Python. |
| Base de datos | **PostgreSQL**, con acceso vía SQLAlchemy. Puede ser un servicio gestionado en DigitalOcean o instalado en el mismo servidor | Las planillas tienen datos relacionados (cliente → sistema → planilla → carga) y validación estricta; PostgreSQL lo maneja mejor que MongoDB. **No usar MongoDB** salvo decisión expresa de Jorge. |
| Frontend | HTML, CSS y JavaScript sin framework pesado. Diseño responsive (celular y notebook) | Liviano, fácil de mantener. |
| Modo sin conexión | **PWA** con service worker e IndexedDB. **Obligatorio**: los técnicos a veces trabajan sin señal | Desde la etapa 3, los borradores se guardan en el dispositivo y se sincronizan al volver la conexión. |
| Firma | Canvas con eventos de puntero (mouse, dedo, lápiz). Imagen guardada en PNG dentro de la base | Sin dependencias externas. |
| Generación Excel | **openpyxl**, reutilizando `build_planilla.py` y los datos de `planillas_data*.py` | Ya existe y está probado. |
| Generación PDF | **LibreOffice en modo headless** (`soffice --convert-to pdf`) sobre el .xlsx emitido | Es lo que ya se usa para generar la serie. |
| Informes -IN | **python-docx**, reutilizando `build_informe.py` | Ya existe. |
| Correo | **SMTP de la cuenta cPanel de readyproof** (webmail existente), con **SPF y DKIM** configurados en el dominio. Configuración por variables de entorno | Ya existe, sin costo adicional. Un Gmail dedicado queda como respaldo si el cPanel da problemas de entregabilidad. |
| Autenticación | Contraseñas con **bcrypt** o **argon2**, sesión con cookie segura, roles `tecnico` y `admin` | Estándar y sencillo. |
| Pruebas | **pytest** | Pruebas de generación, de API y de flujo. |
| Alojamiento | **DigitalOcean**, en un Droplet propio, separado del proyecto que ya está en curso en esa cuenta | No tocar el otro proyecto: mismo proveedor, servidor distinto. |
| Empaquetado | `requirements.txt` fijado con versiones exactas, `README.md` con instalación | Reproducible. |

**No usar** frameworks de frontend pesados, ni servicios de terceros para datos de clientes, ni dependencias que no sean necesarias.

## 5. Estructura de carpetas sugerida

```
app/
  __init__.py              fábrica de la aplicación Flask
  config.py                lectura de variables de entorno
  auth/                    login, sesiones, roles
  models/                  modelos de base de datos (cliente, sistema, planilla, carga, usuario, envío)
  planillas/
    definiciones/          datos de cada planilla (importados de fuente/herramientas/planillas_data*.py)
    generador.py           adaptador sobre build_planilla.py: datos cargados → .xlsx
    pdf.py                 .xlsx → PDF con LibreOffice
  correo.py                envío con adjunto y registro
  rutas/                   endpoints (API) y vistas
  static/                  JS, CSS, íconos, PWA
  templates/               HTML
migraciones/               cambios de base de datos
tests/
  test_generacion.py       cada planilla emitida se compara con la de la serie
  test_api.py
  test_flujo.py
docs/
  INSTALACION.md
PREGUNTAS_ABIERTAS.md         en la raíz del proyecto
REGISTRO_DE_CAMBIOS.md       en la raíz del proyecto
requirements.txt
.env.ejemplo              sin valores reales
README.md
```

## 6. Fuentes de datos existentes (kit interno v5)

Ruta de referencia: `SG-PEM-IFI_Kit_interno_v5/fuente/`

| Recurso | Uso |
|---|---|
| `herramientas/planillas_data.py` | Definición de SEP-1 a 3, CAP 1 y otras planillas. |
| `herramientas/planillas_data2.py` | SDI, SBC, SAL. |
| `herramientas/planillas_data3.py` | SRA, STM, SAA, SHC, SDC, SIM. |
| `herramientas/planillas_data4.py` | SCC (SCC-1 a 5 y SCC-IN). |
| `herramientas/build_planilla.py` | Genera cada .xlsx a partir de la definición. Función `build(sp, out, modelo)`. |
| `herramientas/run_planillas.py` | Orquestador: `python -I run_planillas.py <herramientas> <salida> <modelo.xlsx> [módulo]`. |
| `herramientas/build_informe.py` | Genera informes -IN. |
| `herramientas/fix_impresion.py` | Ajusta centrado y ancho de columnas de impresión. Ya integrado en `build_planilla.py` para planillas nuevas. |
| `herramientas/fix_numpages.py` | Total de páginas en el pie de los manuales. No aplica a planillas. |
| `modelos/SDI-1.xlsx` | Modelo de encabezado con logos. Se copia el encabezado de página con `inject_header()`. |
| `modelos/SG-PEM-IFI_Plantilla_Maestra_v2.docx` | Plantilla de manuales (no se usa en la app). |
| `contenidos/content_*.py` | Textos de los manuales (no se usan en la app, sirven para verificar nombres y códigos). |

**Regla de oro:** el generador de planillas es la única fuente de verdad del formato. La aplicación **no reescribe** el formato: lo llama. Si hace falta un cambio de formato, se hace en `build_planilla.py` y se avisa a Martín.

## 7. Etapas de trabajo

Cada etapa termina con: código, pruebas que pasan, `REGISTRO_DE_CAMBIOS.md` actualizado y una nota de qué quedó pendiente. **No avanzar sin cumplir los criterios.**

### Etapa 0. Preparación
- Crear la estructura de carpetas (sección 5) en una carpeta local.
- Copiar el kit interno a `fuente/` dentro del proyecto (solo lectura; no modificar las herramientas originales sin avisar). Incluir `fuente/KIT_AGENTS.md` (copia del `AGENTS.md` del kit).
- Crear en la **raíz del proyecto** `requirements.txt`, `.env.ejemplo`, `README.md`, `REGISTRO_DE_CAMBIOS.md` y `PREGUNTAS_ABIERTAS.md`. Crear también `docs/INSTALACION.md` con el texto «pendiente de la etapa 9».
- Registrar en `PREGUNTAS_ABIERTAS.md` las preguntas pendientes de la sección 9 bis.
- **Criterio:** `pytest` corre sin errores aunque no haya tests todavía.

### Etapa 1. Generación de la planilla piloto (SAA-1)
- Crear un módulo que reciba un diccionario con los datos cargados de SAA-1 y genere el .xlsx usando `build_planilla.py`.
- Convertir el .xlsx a PDF con LibreOffice.
- Test: con datos ficticios, el PDF tiene el mismo número de páginas que el de referencia (`out_v4/pdf/SG-PEM-IFI-SAA ...pdf` del kit) y el encabezado y el pie son iguales.
- **Criterio:** el PDF de SAA-1 con datos ficticios se revisa visualmente y se aprueba. Se entrega una imagen comparativa de la página 1.

### Etapa 2. Modelo de datos y API de planillas
- Modelos: `Cliente`, `Sistema`, `Planilla` (tipo, versión de la plantilla), `Carga` (datos JSON validados contra la definición), `Usuario`, `Envio`.
- Endpoints para: listar clientes y sistemas, crear una carga, guardar un borrador, finalizar, emitir PDF y descargarlo.
- Validación: cada campo se valida según su tipo (fecha, número, opción, texto), y **no se acepta un campo que no esté en la definición**.
- **Criterio:** pruebas de API con cobertura de creación, edición, finalización y validación de tipos.

### Etapa 3. Interfaz de carga
- Pantalla de selección de cliente, sistema y planilla.
- Formulario generado a partir de la definición (mismo orden y textos que la planilla).
- Guardado de borrador automático, indicador de avance y validación antes de finalizar.
- Vista previa del PDF antes de emitir.
- Responsive: funciona en celular y notebook.
- Firma en pantalla del técnico y del responsable del cliente, que se incorpora al PDF.
- Borradores guardados en el dispositivo (IndexedDB) desde esta etapa, para el uso sin señal.
- **Criterio:** un técnico de prueba puede completar SAA-1 de punta a punta desde el navegador en un celular, con firma, y con la red apagada durante la carga.

### Etapa 4. Usuarios y roles
- Login, cierre de sesión, cambio de contraseña, alta y baja de usuarios por el admin.
- Roles: `tecnico` (carga y emite), `admin` (además administra usuarios y clientes).
- Registro de acceso y de cada emisión (quién, cuándo, qué planilla, a qué destinatario).
- **Criterio:** pruebas de permisos: un técnico no puede dar de alta usuarios ni ver registros de otro cliente si no tiene asignado.

### Etapa 5. Envío por correo y registros
- Envío del PDF por correo con asunto, cuerpo y adjunto configurables.
- Guardado de copia del PDF emitido y del envío, con fecha, para la retención de 3 años.
- Reintento ante fallo de envío y registro del error.
- Envío por SMTP de cPanel. En pruebas, el correo se redirige a un registro en archivo o a una cuenta de prueba, nunca a un destinatario real.
- Verificar SPF y DKIM antes de la primera prueba real.
- **Criterio:** la prueba de envío deja un archivo de registro con el PDF adjunto y el destinatario.

### Etapa 6. Resto de las planillas
- Agregar las planillas de los demás sistemas de a grupos (por ejemplo, SDI y SBC; luego SAL y SEP; después el resto).
- Por cada grupo: test de generación contra la planilla de la serie.
- **Criterio:** cada planilla emitida coincide en encabezado, filas y pie con la de la serie. Las diferencias se listan en `PREGUNTAS_ABIERTAS.md`.

### Etapa 7. Informes -IN
- Generación de informes desde los datos cargados, reutilizando `build_informe.py`.
- **Criterio:** el informe generado para SAA tiene los mismos apartados que `SG-PEM-IFI-SAA-IN`.

### Etapa 8. Modo sin conexión (obligatorio)
- Completar lo iniciado en la etapa 3: service worker para abrir la aplicación sin red, cola de cargas pendientes y sincronización al volver la conexión, sin duplicar registros.
- Resolver conflictos si el mismo borrador se edita en dos dispositivos: se avisa al técnico y no se pierde ninguna versión.
- **Criterio:** una carga hecha sin conexión se sincroniza sin duplicarse, con pruebas que simulan la desconexión.

### Etapa 9. Documentación de instalación
- `docs/INSTALACION.md`: requisitos (Python, LibreOffice), pasos, variables de entorno, creación del primer admin, copias de seguridad.
- **Criterio:** una persona que no participó en el desarrollo puede levantar la aplicación en una máquina limpia siguiendo solo el documento.

## 8. Cómo verificar el trabajo

- **Antes de cada entrega:** `pytest -q` sin fallos; `python -m compileall app` sin errores; revisión del `REGISTRO_DE_CAMBIOS.md`.
- **Generación:** comparar el PDF emitido con la planilla de referencia de la serie (número de páginas, texto del encabezado y del pie, filas).
- **Seguridad:** buscar en el código credenciales, claves y datos de ejemplo reales. Ningún secreto en el repositorio.
- **Texto:** buscar palabras prohibidas en la interfaz (marcas, nombres de clientes) y revisar tildes.
- **Entrega:** un resumen de cada etapa con lo hecho, lo probado, lo pendiente y las preguntas abiertas.

## 9. Decisiones tomadas por Jorge

| # | Tema | Decisión |
|---|---|---|
| 1 | Conectividad en campo | **A veces sin señal.** El modo sin conexión es obligatorio (etapa 8, con base en la etapa 3). |
| 2 | Entrega al cliente | **Correo simple y ágil**, con el PDF adjunto. Sin enlaces ni portal en esta etapa. |
| 3 | Correo de salida | **SMTP de la cuenta cPanel de readyproof.** Si da problemas de entregabilidad, se usa una cuenta Gmail dedicada solo para esto. |
| 4 | Firma | **En pantalla, y la firma aparece en el PDF.** Ver sección 3.2 sobre cómo se guarda. |
| 5 | Alojamiento | **DigitalOcean.** Se instala en un servidor propio, separado del proyecto que ya está en curso en esa cuenta. |
| 6 | Base de datos | **PostgreSQL** (confirmado). MongoDB no se usa. |
| 7 | Formato de salida | **Solo PDF.** |
| 8 | Retención | **3 años**, desde la emisión. |
| 10 | Nombre y leyenda | **Nombre de la aplicación: readyproof.** **Leyenda: «Planilla conforme a IRAM 3546:2011».** |

## 9 bis. Pendientes (no decidir sin Jorge o Martín)

1. **Normas pendientes:** edición vigente de la NFPA 17A y de la NFPA 10 (decisión 19 de `AGENTS.md`). Hasta comprarlas, **no citar** ni copiar texto de las copias no autorizadas que circulan. Los criterios de revisión ya extraídos están en `AGENTS.md` («Criterios NFPA 17A»). Si readyproof consigue las ediciones vigentes, se incorporan al SCC.
2. ~~Unidad de presión en SCC~~ **Resuelto por Jorge: bar.** Las planillas de SCC usan bar; el SSA sigue en MPa.
3. ~~Nombre de la aplicación~~ **Resuelto por Jorge: readyproof.** Falta confirmar el texto exacto de la leyenda con Martín.

## 10. Qué entregar al final

- Código completo en la estructura de la sección 5, con el PDF como único formato de salida al cliente.
- La aplicación se llama **readyproof**: usar ese nombre en la interfaz, el PDF, la documentación, el nombre del proyecto y los servicios externos (por ejemplo, `/opt/readyproof`, base `readyproof`).
- `README.md` y `docs/INSTALACION.md`.
- `REGISTRO_DE_CAMBIOS.md` con cada etapa.
- `PREGUNTAS_ABIERTAS.md` actualizado.
- Un resumen en español de máximo una página: qué funciona, qué se probó, qué falta, qué decisiones se tomaron por defecto y cuáles quedaron pendientes.
- **No** desplegar ni publicar. Eso lo hace una persona de confianza siguiendo `docs/INSTALACION.md`.

## 10 bis. Accesos y puesta en marcha

Los accesos externos (DigitalOcean, cPanel, GitHub) y los pasos de servicio están en `PASOS_SERVICIO_FINAL_readyproof.md`. Reglas:

- Las etapas 0 a 4 se hacen **sin accesos externos**, con datos ficticios.
- Los accesos recién se usan en la etapa 5 (correo de prueba) y en la puesta en marcha, con las credenciales que carga una persona de readyproof en el gestor de contraseñas.
- La operación en pantalla requiere aprobación de Jorge en cada acción sensible, según la sección 0 de ese instructivo.
- Las contraseñas y códigos de dos pasos nunca pasan por el chat.

## 11. Lo que no hacer

- No modificar los generadores de planillas sin avisar: son la fuente del formato de toda la serie.
- No tomar decisiones normativas, de precios, de datos de clientes ni de infraestructura.
- No agregar dependencias sin justificarlas en `REGISTRO_DE_CAMBIOS.md`.
- No guardar datos reales en pruebas, fixtures ni capturas.
- No crear repositorios públicos, cuentas de servicios ni dominios.
- No dar por terminada una etapa con pruebas fallando o con preguntas abiertas que bloqueen lo que se entregó.
