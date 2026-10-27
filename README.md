# readyproof

La identidad del proyecto, sus plantillas y los documentos locales se actualizaron a readyproof por autorización de Jorge. El catálogo vigente es v2 y el piloto usa la versión interna 00-26-rp1; las versiones anteriores se conservan. El ejemplo local está disponible en http://127.0.0.1:8765/login. Ver [alcance, respaldo y verificaciones](docs/IDENTIDAD_READYPROOF.md) y [recuperación de acceso de administrador](docs/DIAGNOSTICO_ACCESO_ADMIN.md).

Aplicación para cargar y emitir planillas SG-PEM-IFI de readyproof. El técnico carga la planilla en el navegador, la firma en pantalla, y el sistema emite el PDF con el formato de la serie y lo envía por correo al cliente.

## Documentos del proyecto

- `AGENTS.md`: encargo técnico y reglas de trabajo.
- `PASOS_SERVICIO_FINAL_readyproof.md`: accesos y puesta en marcha.
- `fuente/`: copia de las herramientas y datos del kit interno SG-PEM-IFI v5. Solo lectura.
- `REGISTRO_DE_CAMBIOS.md`: historial de cada etapa.
- `PREGUNTAS_ABIERTAS.md`: decisiones pendientes.
- `docs/INSTALACION.md`: instalación (se completa en la etapa 9).

## Requisitos

- Python 3.11 o superior.
- LibreOffice (para generar PDF), a partir de la etapa 1.
- Navegador moderno, a partir de la etapa 3 (interfaz de carga).
- PostgreSQL, a partir de la etapa 2.

## Desarrollo local (etapa 0)

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
pytest -q
```

En Linux o macOS, activar con `source .venv/bin/activate`.

## Configuración

Copiar `.env.ejemplo` a `.env` y completar los valores. El archivo `.env` nunca se versiona.

## Piloto SAA-1 (etapa 1)

El adaptador local genera SAA-1 con los datos del kit y convierte el Excel interno a PDF con LibreOffice. Se conservan los logos del encabezado y se rechazan destinos existentes. Ejecución con datos ficticios:

```powershell
.venv\Scripts\python.exe -m app.planillas.piloto --salida out/nueva_revision_saa1
```

El procedimiento, el contrato de datos y la validación se describen en `docs/PILOTO_SAA1.md`. La aceptación de esta etapa requiere revisar el PDF y aprobar el formato antes de continuar a la etapa 2.


## Modelo de datos y API local (etapa 2)

La API de SAA-1 permite crear y guardar borradores, finalizar, emitir PDF con datos ficticios y descargarlo. PostgreSQL es local; las pruebas crean y cierran un clúster temporal separado. Se requiere instalar `requirements-dev.txt`, además de disponer de PostgreSQL y LibreOffice, para ejecutar la suite completa.

El contrato de los endpoints, la configuración local y las reglas de validación están en `docs/API_ETAPA2.md`. La leyenda está confirmada e incorporada; el uso real permanece bloqueado por los controles pendientes. No se incluyen interfaz, usuarios ni correo.

## Interfaz de carga (etapa 3)

La interfaz permite cargar, guardar, revisar y emitir planillas SAA-1 con firmas táctiles en el navegador. En esta etapa se usan exclusivamente datos y firmas ficticios; el entorno permanece limitado a datos y firmas de ejemplo.

Requisitos:

- Servidor Flask ejecutándose (ver abajo).
- Navegador moderno (Chrome, Firefox, Safari, Edge) en desktop o celular. La verificación automática se realizó en Chromium; la revisión manual en teléfono físico sigue pendiente.
- Conexión al servidor local para la primera apertura, sincronizar, generar la vista previa y emitir. No se necesita acceso a internet; después de preparar la aplicación, la carga puede continuar sin conexión.

### Inicio local

Con una base PostgreSQL local configurada mediante `DATABASE_URL` y preparada con `init-db --ejemplos` (ver `docs/API_ETAPA2.md`):

```powershell
.venv\Scripts\python.exe -m flask --app app run --host=127.0.0.1 --port=8765
```

Luego abrir http://127.0.0.1:8765 en el navegador. Para revisar con una base de ejemplos aislada, sin configurar la base habitual, usar como alternativa:

```powershell
.venv\Scripts\python.exe scripts/iniciar_ejemplo.py
```

Usar una sola opción de inicio a la vez, porque ambas emplean el puerto 8765. La dirección 127.0.0.1 corresponde al equipo donde se ejecuta el servidor.

### Características

- Formulario generado desde la definición de SAA-1.
- Guardado automático de borradores en el dispositivo (IndexedDB).
- Firma en pantalla del técnico y del responsable (canvas táctil).
- Vista previa PDF antes de emitir.
- Sincronización automática de la carga activa cuando hay conexión al servidor.
- Funciona sin conexión tras una primera apertura conectada: los borradores permanecen en el dispositivo y la carga activa se sincroniza al volver la conexión. La cola completa entre cargas y dispositivos corresponde a la etapa 8.

### Validación

- Los campos de texto deben comenzar con `[Ejemplo] ` (excepto `empresa_mantenedora=readyproof`).
- Las firmas deben ser PNG válidas con trazos, de 10 a 1200 px de ancho y de 10 a 500 px de alto, con un máximo de 200 KB por firma.
- Ambas firmas y una vista previa actualizada son obligatorias en la interfaz antes de finalizar.

### Datos de prueba

- Cliente: [Ejemplo] Planta de prueba.
- Sistema: [Ejemplo] Abastecimiento de agua (nombre actual del catálogo local).
- Borradores guardados en IndexedDB del navegador, sin persistencia en el servidor hasta la sincronización.

Las instrucciones de navegación, preparación offline y pruebas están en `docs/INTERFAZ_ETAPA3.md`. Usuario y Envio siguen diferidos a las etapas 4 y 5, respectivamente.


## Usuarios y roles (etapa 4)

La API y la interfaz ahora requieren sesión. Al abrir el ejemplo local por primera vez, crear el primer administrador en la pantalla de configuración; no hay credenciales predeterminadas. Elegir y escribir la contraseña directamente allí, sin compartirla por chat.

Administración permite crear cuentas admin/tecnico, asignar clientes, dar de baja usuarios, restablecer contraseñas y consultar accesos. Mi cuenta permite cambiar la contraseña; Salir cierra la sesión y retira los borradores locales de esa cuenta. Los técnicos solo acceden a sus clientes asignados, también al consultar o descargar una carga por URL.

El inicio sigue siendo `scripts/iniciar_ejemplo.py`, usando exclusivamente la base local de ejemplos. La migración conserva los datos anteriores. Los detalles de sesiones, configuración, API, privacidad offline y pruebas están en `docs/USUARIOS_ETAPA4.md`. El acceso al iPhone permanece suspendido; su prueba física sigue pendiente por confirmación de Jorge. M1 está resuelto para la leyenda; el uso real sigue pendiente de habilitación y el transporte de correo sigue pendiente.


## Manual y modelos de correo (inicio de etapa 5)

SAA-1 está vinculada a un Manual ficticio mediante `planilla.manual`. El contenido y los campos obligatorios reales siguen pendientes de confirmación; no cambió la definición normativa ni la validación de la planilla.

Se agregaron Envio, Intento y Retencion con UUID, relaciones y migraciones Alembic aditivas. Esta entrega cubre los modelos: todavía no envía correo, genera archivos .eml ni programa reintentos. Retencion representa reintentos y no reemplaza la conservación de registros por tres años. Esquema, actualización y límites en `docs/MODELOS_MANUAL_CORREO.md`.


## Catálogo JSON y logo (etapa 6)

Los cuatro contenedores SAA-1/SDI/SBC/SAL se importan con `flask --app app cargar-planillas` después de preparar el esquema. En una instalación nueva se cargan durante `init-db`. El ejemplo aislado se actualiza con `scripts/iniciar_ejemplo.py --cargar-planillas`.

Se vinculan cuatro manuales ficticios y se conserva el piloto SAA-1 anterior con su manual. El PDF del piloto usa el logo readyproof completo proporcionado por Jorge. La carga de metadatos no habilita todavía generar los grupos nuevos; ver `docs/ETAPA6_PLANILLAS_LOGO.md` para el contrato, la actualización y los pendientes.


## Leyenda IRAM confirmada (M1)

Los nuevos PDF llevan «Planilla conforme a IRAM 3546:2011» en todas las páginas, centrada a 10 mm del borde inferior, Helvetica 8 pt y gris 50 %, según lo confirmado por Martín a través de Jorge. Se aplica una reducción proporcional del contenido del 5 % autorizada por Jorge para reservar el pie sin tapar filas. A4 y el número de páginas se mantienen; fuente/ no se modifica. La pantalla de carga muestra el mismo texto.

M1 deja de ser xfail y se verifica como prueba normal. Esto no habilita por sí solo datos reales: continúan los demás controles y el entorno de ejemplos. Detalles en `docs/LEYENDA_IRAM_M1.md`.


## Transporte SMTP Gmail

Cuenta elegida por Jorge: readyproof.ar@gmail.com. La API prepara envíos con PDF adjunto y el proceso independiente reintenta cada 15 minutos, con tres intentos máximos. Modo de prueba por defecto, sin enviar mensajes reales. Ver [configuración, comandos y límites](docs/SMTP_GMAIL.md). `.env.local` queda fuera de Git; no se incluyen credenciales.
