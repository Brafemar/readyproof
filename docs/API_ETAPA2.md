# API local de planillas — etapa 2

La API usa Flask y PostgreSQL local con SQLAlchemy. Su catálogo inicial contiene únicamente SAA-1. No incluye interfaz, administración de usuarios, autenticación ni correo, según el alcance indicado por Jorge. Es un entorno de desarrollo local con datos ficticios y no debe publicarse. El uso real sigue bloqueado por los controles pendientes; la leyenda M1 se incorporó posteriormente.

## Preparación y pruebas

PostgreSQL 18.6 está instalado localmente. El servicio habitual escucha en localhost. Para las pruebas basta disponer de sus binarios; no se usa ni se modifica su base de datos habitual ni se necesita su contraseña.

```powershell
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m compileall app
```

Las pruebas crean un clúster PostgreSQL descartable dentro de `.venv/tmp/pytest/`, escuchando solo en 127.0.0.1 y un puerto libre. Ese clúster de datos ficticios admite conexiones locales sin contraseña únicamente durante la prueba; se detiene al terminar. Cada prueba de API tiene su propia base y la elimina al finalizar. No se utiliza SQLite. `PG_BINDIR` permite indicar la carpeta local de binarios si la instalación no está en la ubicación habitual.

Para usar la API manualmente, una persona debe crear una base PostgreSQL local vacía y configurar `DATABASE_URL` en su entorno. El valor no se incluye en documentación ni registros. Se admite únicamente el controlador `postgresql+psycopg` y un host local; no hay conexión externa ni sustitución automática por otro motor.

```powershell
.venv\Scripts\python.exe -m flask --app app:create_app init-db --ejemplos
.venv\Scripts\python.exe -m flask --app app:create_app run --host 127.0.0.1
```

`init-db` aplica el esquema inicial y registra su versión 1. `--ejemplos` agrega un cliente ficticio, un sistema SAA y la plantilla SAA-1; repetirlo no duplica registros. La migración inicial está en `migraciones/001_etapa2.py`. No actualiza esquemas antiguos mediante cambios destructivos ni ejecuta migraciones al recibir solicitudes.

## Endpoints

| Método | Ruta | Resultado |
|---|---|---|
| GET | `/api/clientes` | Clientes de ejemplo |
| GET | `/api/clientes/{id}/sistemas` | Sistemas del cliente ficticio |
| GET | `/api/planillas` | Catálogo de códigos, versiones y huellas |
| GET | `/api/planillas/{id}` | Definición y tipos admitidos |
| POST | `/api/cargas` | Crear un borrador con `sistema_id`, `planilla_id`, `datos` |
| GET | `/api/cargas/{id}` | Consultar datos, revisión y estado |
| PUT | `/api/cargas/{id}/borrador` | Reemplazar el borrador completo con `revision` y `datos` |
| POST | `/api/cargas/{id}/finalizar` | Finalizar el borrador con `revision` |
| POST | `/api/cargas/{id}/emitir` | Generar y almacenar el PDF ficticio con `revision` |
| GET | `/api/cargas/{id}/pdf` | Descargar el PDF emitido como adjunto |
| GET | `/api/cargas/{id}/revisiones` | Consultar las instantáneas y eventos |

`GET /api/cargas/{id}/revisiones` devuelve en el campo `datos` la instantánea JSON completa de cada revisión, no solo las diferencias respecto de la anterior. Incluye `cabecera`, `bloques` y `observaciones` tal como se guardaron en ese evento, junto con `numero`, `evento`, `actor` y `fecha`.

Los cuerpos son objetos JSON. Se rechazan los campos desconocidos tanto en el cuerpo de la solicitud como en cada bloque de datos. Los identificadores se obtienen del catálogo; no se codifican en el cliente.

## Datos y tipos

`datos` conserva la estructura del adaptador de la etapa 1: `cabecera`, `bloques` y `observaciones`. Los títulos de bloques y etiquetas deben coincidir literalmente con la definición del kit. La definición se expone en el endpoint de planilla; no se agregan filas ni opciones.

- Fechas: texto ISO `YYYY-MM-DD`, con validación de calendario. Incluye la fecha del encabezado y las dos etiquetas de inspección/prueba que declaran fecha.
- Números: números JSON finitos para los campos con unidad. Las dos cantidades de equipos/unidades son enteros JSON. No se aceptan booleanos ni números escritos como texto.
- Opciones: una de las cadenas exactas del kit; no se agregan opciones.
- Texto: cadena no vacía de hasta 500 caracteres, identificada con `[Ejemplo] `. La empresa mantenedora readyproof puede conservar el valor original del kit.
- Observaciones: hasta cuatro textos identificados como ejemplo, en el orden original.

Los números, fechas y opciones no llevan el prefijo, porque deben conservar su tipo. Los textos y el cliente relacionado identifican la carga ficticia. No se asignan límites de aceptación normativa ni frecuencias nuevas.

Los borradores pueden ser parciales. Finalizar revalida los datos presentes y rechaza una carga completamente vacía; no inventa obligatoriedad de campos que el kit no define. Esa política debe confirmarse antes de permitir emisión real. Emitir requiere además que la cabecera identifique al mismo cliente ficticio del sistema. No existe una opción para habilitar datos reales en esta etapa.

## Estados, consistencia y trazabilidad

El flujo es `borrador → finalizada → emitida`. Solo se editan borradores. Toda escritura posterior a la creación exige la revisión entera actual; una revisión vencida devuelve 409. El control optimista también se aplica en PostgreSQL para evitar que dos escrituras simultáneas se sobrescriban.

Cada carga referencia una versión de plantilla y su huella SHA256. La definición, los generadores y el modelo originales se verifican antes de finalizar o emitir: si cambió la plantilla, la operación se bloquea hasta registrar una versión nueva. Las revisiones guardan la instantánea JSON, el evento y la fecha UTC. El actor se identifica como API local ficticia sin autenticación; la identificación de personas y los roles corresponden a la etapa 4.

El Excel es temporal y no se expone por API. El PDF y su SHA256 se guardan en la misma transacción que el cambio a emitida. Si la conversión falla, la carga sigue finalizada, sin PDF ni revisión de emisión. La descarga lleva `Cache-Control: no-store`. No hay rutas de borrado ni envío de correo.

## Respuestas de error

- 400/415: JSON mal formado o tipo de contenido incorrecto.
- 403: registro que no es de ejemplo; uso real no habilitado.
- 404: identificador inexistente.
- 409: revisión vencida, estado incompatible o plantilla distinta.
- 422: campo, tipo, valor u opción inválidos.
- 503: base local o conversión no disponible. No se devuelven credenciales ni detalles internos de conexión.

## Fuera de alcance y pendientes

Usuario y Envio, así como sus operaciones, quedan reservados para las etapas de usuarios y correo por la restricción expresa de esta tarea. Tampoco se implementaron pantallas, firmas, PWA ni sincronización. M1 y las coordenadas fijas de n1 se corrigieron posteriormente; ver LEYENDA_IRAM_M1.md. El aviso a Martín sobre el formato, los metadatos y la integridad del kit conservan sus preguntas abiertas.
