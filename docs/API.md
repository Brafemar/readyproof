# API de readyproof

Las rutas requieren sesión vigente. Las operaciones de escritura requieren `X-CSRF-Token`. El entorno privado conserva el control de clientes asignados; no se entregan firmas ni credenciales en estas consultas.

## Búsqueda por número de registro

`GET /api/carga/buscar?numero=12345`

Devuelve `numero_registro`, `cliente` (nombre), `sistema` (sigla), `planilla` (código SG-PEM-IFI), `estado`, `revision_publica`, `fecha_emision` (ISO con zona horaria o null), `pdf_hash` y `desbloqueado_por` (UUID o null).

- 200: registro encontrado y cliente autorizado.
- 400: parámetro ausente, vacío, repetido, no entero decimal ASCII o fuera del rango 0–2147483647.
- 401: sesión ausente o vencida.
- 404: no encontrado o cliente no asignado al técnico. La respuesta no permite distinguir ambas situaciones.

El administrador puede consultar todos los clientes; el técnico, únicamente los asignados. El número se asigna al emitir; los borradores y los documentos históricos anteriores a esa numeración pueden no tener número. No se renumeran ni reescriben documentos anteriores para hacerlos buscables.

## Auditoría de cambios

`GET /api/auditoria?tabla=carga&registro_id=<uuid>&accion=DESBLOQUEO&usuario_id=<uuid>&limit=100&offset=0`

Exclusivo de administradores. Retorna `total` de coincidencias antes de paginar y `registros`, con `id`, `tabla`, `registro_id`, `accion`, `usuario`, `usuario_id`, `timestamp`, `datos_anterior` y `datos_nuevo`.

Filtros opcionales combinados con AND: `tabla`, `registro_id`, `accion`, `usuario_id`. Acciones admitidas: INSERT, UPDATE, DELETE y DESBLOQUEO; DELETE queda reservado, sin habilitar una operación de borrado de cargas.

Orden: timestamp descendente y UUID descendente como desempate. `limit`: 1–500 (100 por defecto); `offset`: 0–2147483647 (0 por defecto). UUID inválido, filtro desconocido/repetido o paginación inválida: 422. Sin sesión: 401; técnico autenticado: 403.

Los snapshots contienen los datos de la carga y su estado, IDs, revisiones, fechas y hash. No contienen los bytes del PDF, imágenes de firma, contraseñas ni tokens. Deben tratarse como información restringida. Ver `AUDITORIA.md`.

## Operación y correo

Se conservan las rutas existentes `/api/cargas`, `/api/cargas/{id}/borrador`, `/finalizar`, `/emitir`, `/desbloquear`, `/pdf`, `/emisiones` y `/enviar`. No se crea una segunda implementación de envío en una ruta singular: el envío continúa en `POST /api/cargas/{id}/enviar`.

`GET /api/correo/configuracion` informa disponibilidad, destinatarios de prueba, `modo_piloto` y `modo_prueba`. En piloto, las transmisiones explícitas usan solo la lista autorizada; `DESTINATARIO_PRUEBA`, si se configura, sustituye el destinatario solicitado. En modo real con correo de prueba activo, se conserva una copia local sin transmisión. Ver `CONFIG_MODO_REAL.md`.
