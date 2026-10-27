# Diagnóstico de acceso de administrador — 26/10/2026

La consulta de solo lectura sobre la base PostgreSQL del ejemplo local confirmó que la tabla usuarios existe y contiene dos cuentas: un administrador activo (`msanchez`) y un técnico activo (`tecnico-readyproof`). No existe `jorge.admin` al momento del diagnóstico. Hay un acceso fallido por `/login`, HTTP 401, a las 19:56:13 de Argentina, asociado a ese nombre de usuario.

La condición que rechaza el intento es `user is None` en `autenticar()` de `app/auth/rutas.py`. No es un rechazo del formato de usuario ni de la longitud mínima de contraseña. `normalizar_login('jorge.admin')` devuelve ese mismo nombre. La clave propuesta por Jorge tiene 14 caracteres ASCII y cumple la política: al menos 12 caracteres y hasta 72 bytes UTF-8, sin requisitos adicionales de composición. Se verificó bcrypt con una muestra aleatoria de 14 caracteres; no se guardó ni se probó contra una cuenta inexistente la contraseña compartida por chat.

El mensaje público continúa siendo «Usuario o contraseña incorrectos.» para no distinguir cuentas existentes de inexistentes en la pantalla de acceso. La causa específica se registra en este diagnóstico y su evidencia local; no se imprimen claves ni hashes.

## Acceder y crear la cuenta por el flujo normal

Después de recuperar el acceso al administrador existente, abrir [Administración local](http://127.0.0.1:8765/admin), ingresar como `msanchez` y usar **Crear usuario**:

- Usuario: `jorge.admin`.
- Nombre ficticio: `[Ejemplo] Administración readyproof`.
- Rol: **Administrador**.
- Contraseña inicial: ingresarla directamente en pantalla, al menos 12 caracteres y hasta 72 bytes UTF-8.
- Clientes asignados: puede quedar vacío para un administrador.
- Acción: **Guardar usuario**.

Cerrar sesión e ingresar como `jorge.admin` con la clave elegida. El alta se realiza mediante `POST /api/admin/usuarios`, con sesión admin y CSRF, conservando las validaciones. No modificar tablas ni hashes directamente ni volver a abrir la configuración inicial. Si se acumulan cinco accesos fallidos para el mismo nombre en 15 minutos, la aplicación responde HTTP 429 y debe esperarse ese intervalo.

No se cambió la contraseña del administrador existente ni se creó `jorge.admin` en la base persistente durante el diagnóstico. La creación e ingreso se verifican separadamente en una base temporal de pruebas. La comprobación operativa de esa nueva cuenta en la base del ejemplo requiere completar los pasos anteriores.

## Recuperación de msanchez autorizada por Jorge

Jorge aclaró que tampoco puede ingresar con `msanchez` y autorizó explícitamente su recuperación controlada. La consulta de solo lectura confirmó cuenta existente, activa, rol admin y hash bcrypt con formato válido. Hay cuatro rechazos HTTP 401 en los 15 minutos anteriores a la inspección, sin eventos 429 en ese momento. Para esos intentos la condición de fallo es la comprobación de la contraseña recibida; no la inexistencia de la cuenta, el rol o una baja. No se probaron otras contraseñas ni se imprimieron hashes.

Se agregó el comando local `admin-recuperar --login`, sin endpoint web ni contraseña predeterminada. Exige confirmación y entrada oculta de la clave nueva dos veces, aplica normalizar_login/hash_clave, admite solo un administrador existente y activo, revoca sus sesiones y registra `admin_recuperado_local` con método CLI. No crea usuarios, activa cuentas dadas de baja, cambia roles, elimina intentos de acceso ni deshabilita CSRF, bcrypt o límites de intentos.

Para recuperar la cuenta del ejemplo local activo, Jorge debe abrir PowerShell y ejecutar:

```powershell
cd C:\Users\jorge\Readyproof
.\.venv\Scripts\python.exe .\scripts\recuperar_admin_local.py --login msanchez
```

La contraseña se ingresa únicamente en esa consola interactiva y no se pasa por argumentos, archivos, variables de entorno ni chat. El lanzador valida la ruta de la base del ejemplo y el puerto, mantiene el correo en modo prueba y llama al comando de la aplicación. No ejecuta migraciones ni modifica tablas mediante comandos manuales. El proceso web no necesita reiniciarse para reconocer la clave nueva o las sesiones revocadas; comparte la base local.

Después, abrir [Ingresar a readyproof](http://127.0.0.1:8765/login) con `msanchez` y la clave nueva. Si se acumularon cinco fallos en 15 minutos, esperar que transcurra el intervalo correspondiente: la recuperación no borra ni elude ese bloqueo. Una vez dentro, crear `jorge.admin` mediante Administración si se desea.

Estado confirmado por Jorge al preparar la entrega: **todavía no ejecutó el comando**. La recuperación real y el login posterior siguen pendientes. Las cinco pruebas de recuperación pasaron con cuentas y claves aleatorias en PostgreSQL temporal; no se reemplazó la clave real para ejecutar pruebas.

## Corrección acotada

Se encontró además un caso independiente: GET `/login` detectaba cero usuarios y redirigía a `/configuracion-inicial`, mientras que POST intentaba autenticar antes de comprobarlo. Ahora ambas rutas detectan la base vacía; POST usa HTTP 303 para abrir la pantalla de creación por GET, sin trasladar contraseñas en la URL ni crear cuentas implícitamente.

Con usuarios existentes, la configuración inicial sigue cerrada. Un intento con un nombre inexistente conserva HTTP 401 y nunca crea usuarios ni otorga permisos. Se conservan CSRF, bcrypt, limitación de intentos y restricciones de acceso.

La base y el esquema ya existen: no se agregó creación automática ni ejecución de migraciones al iniciar la aplicación. El comando `init-db` y el lanzador local existentes siguen siendo los responsables de preparar el esquema.

La corrección estará disponible al reiniciar el proceso local con el lanzador habitual; no se reinició el servidor durante esta revisión ni se alteraron sus sesiones.

Pruebas agregadas: redirección GET/POST sin usuarios sin crear cuentas; rechazo de usuario inexistente con configuración inicial cerrada; alta de otro admin desde una sesión admin e ingreso posterior conservando la clave del admin original. Se amplió la prueba del primer administrador con logout/login posterior. Resultados exactos en REGISTRO_DE_CAMBIOS.md y `out/diagnostico_admin/`.

Suite completa de cierre con la identidad actualizada: **151 passed in 387.01s (0:06:27)**, código 0; compileall código 0. El ejemplo local volvió a abrirse en http://127.0.0.1:8765/login. La recuperación real de msanchez sigue pendiente de la consola de Jorge; las claves no se modificaron durante esta revisión.
