# Usuarios y roles — etapa 4

## Alcance y revisión local

La aplicación permanece restringida a 127.0.0.1/::1 y a datos y firmas ficticios. No se habilitan accesos al iPhone, certificados, red Wi-Fi ni firewall. La leyenda M1 está resuelta; el uso real sigue bloqueado por los demás controles pendientes. Usuario está implementado; Envio y el correo quedan para etapa 5.

Desde la raíz del proyecto:

```powershell
.venv\Scripts\python.exe scripts/iniciar_ejemplo.py
```

Abrir http://127.0.0.1:8765. El lanzador conserva su base PostgreSQL de ejemplos, aplica las migraciones aditivas y no utiliza la base habitual ni su contraseña. No iniciar otra instancia si el puerto ya está ocupado.

## Primer administrador

Al ingresar sin cuentas existentes, la pantalla de acceso lleva a /configuracion-inicial. Elegir un usuario y una contraseña exclusiva para esta revisión, escribirla y repetirla directamente en el formulario. No enviarla por chat ni guardarla en documentación. No existe una contraseña predeterminada. La pantalla inicial se cierra permanentemente después del alta de la primera cuenta. El nombre de prueba del primer administrador es [Ejemplo] Administración.

Los usuarios admiten de 3 a 80 letras ASCII, números, puntos, guiones y guiones bajos; no distinguen mayúsculas. La contraseña requiere al menos 12 caracteres y un máximo de 72 bytes UTF-8, límite de bcrypt. Se almacena solo el hash bcrypt con sal individual y factor 12. Ni la contraseña ni los tokens de sesión se incluyen en respuestas de administración, registros o capturas.

## Administración

1. Ingresar con una cuenta administradora y abrir Administración.
2. Crear un usuario con nombre ficticio [Ejemplo], rol tecnico o admin, contraseña inicial y clientes asignados.
3. El administrador puede acceder a todos los clientes de ejemplo. El técnico solo puede listar y usar los que tenga asignados.
4. Editar la cuenta permite modificar rol, asignaciones y estado activo. Desmarcar Cuenta activa realiza la baja lógica; se conserva la identidad histórica. No se permite dejar al sistema sin un administrador activo.
5. Al modificar una cuenta o restablecer su contraseña se revocan sus sesiones; debe ingresar nuevamente. El formulario de restablecimiento usa la contraseña nueva escrita directamente por el administrador, sin enviarla por correo.
6. Se pueden crear clientes ficticios y sus sistemas SAA desde la misma pantalla. Los nombres empiezan con [Ejemplo]. No se modifica el contenido normativo del catálogo.
7. El listado de accesos muestra los últimos 200 eventos. Los registros completos permanecen en la base; no hay una ruta de borrado.

El técnico no puede crear ni editar usuarios, administrar clientes ni consultar la auditoría. Una URL directa o un identificador de carga de otro cliente no elude la restricción: consulta, borrador, historial, vista previa, finalización, emisión, descarga y recuperación idempotente verifican el cliente en el servidor.

## Sesión y contraseña

Mi cuenta permite cambiar la contraseña verificando la actual. El cambio cierra todas las sesiones de esa cuenta, incluida la actual. Salir revoca la sesión del servidor y retira los borradores de esa cuenta del navegador, previa advertencia sobre cambios pendientes.

La sesión absoluta dura 8 horas. El servidor conserva únicamente el hash del token aleatorio y comprueba en cada solicitud el usuario activo y sus permisos. Reingresar rota el token y revoca el anterior. Las cookies son HttpOnly y SameSite=Lax; cada escritura exige CSRF y rechaza un Origin distinto. Cinco intentos fallidos para el mismo usuario en 15 minutos bloquean temporalmente nuevos intentos. La respuesta no distingue cuenta inexistente, inactiva o contraseña incorrecta.

En este entorno HTTP exclusivo de loopback, la cookie no usa Secure para poder ingresar localmente. READYPROOF_HTTPS=true permite marcarla Secure en un entorno HTTPS preparado posteriormente; no se habilita ni prepara HTTPS aquí. No usar el servidor local como instalación de producción.

SECRET_KEY se lee del entorno. Si no está definida se genera una clave efímera en memoria para esta ejecución local; reiniciar cierra las sesiones anteriores. El valor de muestra y claves de menos de 32 caracteres se rechazan. Para una configuración persistente, una persona debe proporcionar una clave aleatoria por variable de entorno, nunca incorporarla al repositorio. El ejemplo de entorno no contiene una clave real.

## Borradores y trabajo sin conexión

IndexedDB usa un espacio separado por usuario. La sesión activa de la pestaña conserva solo el contexto necesario para recuperar su propio borrador offline dentro del plazo de sesión. Al cambiar de cuenta se bloquean las otras pestañas y al salir se retiran los borradores de la cuenta. Un vencimiento bloquea la pantalla, conservando los borradores para recuperarlos después de autenticar nuevamente con la misma cuenta.

El catálogo online solo incluye los clientes actualmente asignados y la pantalla oculta los borradores de otros clientes. Fuera de línea no puede conocerse una baja o revocación realizada en el servidor; al reconectar, el servidor exige sesión y autorización vigentes antes de sincronizar, previsualizar o emitir. El bloqueo por tiempo de sesión se aplica también a la pantalla offline. La recuperación entre dispositivos y la cola completa de sincronización siguen siendo parte de etapa 8.

Los datos locales no se presentan como almacenamiento apto para firmas reales o equipos compartidos en producción. La revisión usa exclusivamente ejemplos; la protección operativa y el procedimiento de dispositivos deberán revisarse antes del uso real. Las pruebas físicas en iPhone siguen pendientes por decisión de Jorge.

## Trazabilidad y migración

La migración 003 agrega las tablas de usuarios, asignaciones, sesiones y accesos y las referencias nullable de autor en cargas/revisiones. Conserva las cargas anteriores, sus datos, firmas y revisiones; no inventa un autor para la historia previa. Las revisiones nuevas registran el usuario autenticado.

Los accesos API y los eventos de login, logout y cambios de cuenta se registran con fecha, usuario cuando existe, ruta sin datos de solicitud y resultado HTTP. Las emisiones exitosas agregan un evento con usuario, cliente, carga y código de planilla en la misma transacción que registra el PDF. El destinatario permanece vacío porque todavía no hay envío; se incorporará en etapa 5 al realizarlo. No se registran contraseñas, cookies, cuerpos de solicitud ni imágenes de firmas.

Si no es posible persistir el registro de acceso, la operación devuelve 503. Los errores de conversión no registran una emisión exitosa.

## API de autenticación y administración

- GET /api/auth/sesion: usuario actual o null, CSRF y vencimiento. Permite obtener CSRF antes del login.
- POST /api/auth/login: login y clave. Devuelve la nueva sesión y un CSRF renovado.
- POST /api/auth/logout: revoca la sesión.
- POST /api/auth/clave: actual y nueva; revoca todas las sesiones.
- GET/POST /api/admin/usuarios: listado o alta; el alta recibe login, nombre, rol, clave y cliente_ids.
- PUT /api/admin/usuarios/{id}: rol, activo y cliente_ids; baja lógica mediante activo=false.
- POST /api/admin/usuarios/{id}/clave: nueva; restablecimiento y revocación.
- POST /api/admin/clientes: nombre ficticio.
- POST /api/admin/clientes/{id}/sistemas: tipo SAA y designacion ficticia.
- GET /api/admin/accesos: últimos 200 accesos, solo administrador.

Las escrituras requieren la cookie de sesión y X-CSRF-Token. Los formularios HTML incluyen su campo CSRF. No se implementa un interruptor para omitir autenticación.

## Verificación

Con requirements-dev.txt y Node.js/Playwright locales preparados según INTERFAZ_ETAPA3.md:

```powershell
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m compileall app
```

Las pruebas usan PostgreSQL temporal separado, contraseñas aleatorias en memoria y ningún cliente real. Verifican permisos en todas las rutas de carga, CSRF, expiración, revocación, baja, último administrador, límites de login, migración conservando datos, auditoría y recorridos reales de navegador para alta administrativa, login técnico y cierre de sesión. El recorrido offline de SAA-1 se mantiene autenticado y firmado. La configuración del runner npm sigue pendiente; el navegador se ejecuta desde pytest.
