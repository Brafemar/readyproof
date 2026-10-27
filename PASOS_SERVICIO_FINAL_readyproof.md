# Pasos de servicio para readyproof

## 0. Modo de operación: el agente opera en pantalla con aprobación

El agente puede hacer los pasos de servicio por pantalla (DigitalOcean, cPanel, GitHub) o por comandos. Cuando hay comando, se usa comando. Cuando no lo hay, se usa pantalla, con estas reglas:

**Preparación (la hace una persona, una vez)**
- Computadora vinculada a la sesión desde la app de escritorio de Claude.
- Navegador exclusivo para el agente, con un perfil nuevo que no tenga cuentas personales abiertas. Ahí se inician sesión en DigitalOcean y cPanel.
- Autenticación en dos pasos activa en esas cuentas.

**Reglas de la operación**
1. **Las contraseñas y los códigos de dos pasos los escribe la persona, nunca el agente.**
2. **Antes de cada acción que cree, pague, cambie o borre algo**, el agente muestra en el chat: la pantalla, la acción exacta, el costo y el recurso afectado. Espera el «sí» de Jorge.
3. **Ningún pago** sin confirmación del monto y del producto.
4. **Ningún cambio de DNS** sin que Jorge vea el registro antes de guardarlo.
5. **Si la cuenta, el proyecto o la región no coinciden** con los del paso, el agente se detiene y avisa.
6. **Si una pantalla no es la esperada**, el agente no improvisa: describe lo que ve y espera instrucciones.
7. **Cada paso queda registrado** en `REGISTRO_DE_CAMBIOS.md` con fecha, acción y resultado, sin valores secretos.
8. Jorge puede cortar en cualquier momento. Al cortar, el agente deja el estado anotado para retomar.

**Qué conviene scriptear en lugar de hacer en pantalla**
- Crear y configurar el Droplet, la base y el firewall: comandos o la API del proveedor con el token de la sección A2.
- Registrar SPF y DKIM: pantalla, con revisión de Jorge.

Este instructivo acompaña al encargo `AGENTS.md` (copia de `ENCARGO_FINAL_readyproof.md`). Separa lo que hace una persona de readyproof (una sola vez) de lo que hace el agente. Los comandos y las pantallas de los proveedores cambian con el tiempo: **antes de ejecutar cada paso, el agente debe verificarlo en la documentación vigente del proveedor** y anotar cualquier diferencia en `REGISTRO_DE_CAMBIOS.md`.

---

## A. Lo que hace una persona (una sola vez, unos 30 minutos)

Ninguna de estas tareas se hace con el agente, porque implican pagos, identidad o cambios en el dominio de la empresa.

| # | Tarea | Dónde | Entregable al agente |
|---|---|---|---|
| A1 | Crear un proyecto nuevo en DigitalOcean llamado `readyproof`, separado del proyecto en curso | DigitalOcean | Nombre del proyecto |
| A2 | Generar un **token de API** con permiso de lectura y escritura solo sobre ese proyecto | DigitalOcean → API | Token, cargado en el gestor de contraseñas |
| A3 | Crear la casilla de correo dedicada (por ejemplo `noreply@<dominio>`) con contraseña propia | cPanel → Cuentas de correo | Usuario y contraseña, cargados en el gestor de contraseñas |
| A4 | Cargar los registros **SPF** y **DKIM** del dominio para esa casilla, si cPanel los ofrece | cPanel → Zona DNS | Confirmación de carga |
| A5 | Activar autenticación en dos pasos en DigitalOcean y en cPanel | Cada cuenta | Confirmación |
| A6 | Crear un **repositorio privado** en GitHub solo si Jorge lo decide (ver regla de la serie) | GitHub | URL y token de solo lectura/escritura sobre ese repositorio |

**Regla:** las contraseñas y tokens nunca se pegan en el chat. Se cargan en el gestor de contraseñas de readyproof, y el agente los toma de allí o de variables de entorno en el servidor.

---

## B. Lo que hace el agente

Cada bloque termina con una **verificación** y un registro en `REGISTRO_DE_CAMBIOS.md`.

### B1. Entorno local (etapas 0 a 4, sin accesos externos)
1. Crear la estructura de carpetas del encargo, sección 5.
2. Crear `requirements.txt` con versiones fijadas, `.env.ejemplo` sin valores reales y `README.md`.
3. Instalar dependencias en un entorno virtual (`python3 -m venv .venv`).
4. Correr `pytest -q` y `python -m compileall app`.
- **Verificación:** las pruebas pasan sin conexión a internet.

### B2. Servidor (solo cuando la etapa 5 esté lista y con aprobación de Jorge)
1. Crear un Droplet en el proyecto `readyproof`, con Ubuntu LTS, el tamaño más chico que permita LibreOffice y PostgreSQL.
   - **Aprobación requerida:** el costo mensual antes de crearlo.
2. Crear una clave SSH para el agente, registrarla en el Droplet y deshabilitar el acceso por contraseña.
3. Instalar paquetes: Python 3, `libreoffice-calc` en modo sin entorno gráfico, PostgreSQL, Nginx y `ufw` (abrir solo los puertos 22, 80 y 443).
4. Crear un usuario del sistema para la aplicación, sin permisos de administrador.
5. Crear el archivo `.env` en el servidor con las credenciales. **No se versiona.**
- **Verificación:** `ufw status` muestra solo los puertos permitidos; el usuario de la aplicación no puede usar `sudo`.

### B3. Base de datos (PostgreSQL)
1. Crear la base `readyproof` y un usuario propio con permisos solo sobre esa base.
2. Ejecutar las migraciones del proyecto.
3. Programar copias de seguridad diarias (`pg_dump`) guardadas fuera del servidor, con retención de 3 años para los registros de planillas.
- **Verificación:** una copia de prueba se restaura en una base temporal y los conteos coinciden.

### B4. Aplicación y web
1. Clonar o copiar el código a `/opt/readyproof`.
2. Configurar el servicio con `systemd` (arranque automático y reinicio ante fallos).
3. Configurar Nginx como proxy hacia la aplicación.
4. Obtener el certificado HTTPS con Let's Encrypt (certbot).
- **Verificación:** la página responde por HTTPS, el certificado es válido y el servicio se reinicia solo al matarlo.

### B5. Correo (etapa 5)
1. Configurar en `.env` el servidor SMTP de cPanel, el usuario y la contraseña de la casilla dedicada.
2. Enviar un correo de prueba **solo a una dirección de prueba de readyproof**, con un PDF adjunto.
3. Revisar en el correo recibido que no caiga en spam y que el remitente y el adjunto sean correctos.
- **Verificación:** el correo llega, con el PDF adjunto, y el encabezado tiene SPF y DKIM en «pass». **Ningún envío real a clientes hasta que Jorge lo apruebe por escrito.**

### B6. Operación continua
1. Revisar una vez por semana los registros del servicio (`journalctl`) y el espacio en disco.
2. Actualizar paquetes de seguridad del sistema.
3. Probar la restauración de una copia de seguridad cada tres meses.

---

## C. Aprobaciones que el agente no puede dar solo

- Crear o cambiar recursos con costo (Droplets, bases administradas, servicios de correo).
- Cambiar registros DNS del dominio principal.
- Borrar cualquier recurso, copia o planilla emitida.
- Dar acceso a una persona nueva o a un token nuevo.
- Enviar un correo a un cliente real.
- Publicar el sistema en una dirección accesible desde internet, antes de que Jorge lo apruebe.

## D. Si algo falla

- El agente se detiene, registra el error en `REGISTRO_DE_CAMBIOS.md` y avisa a Jorge con el mensaje exacto.
- No prueba al azar con otras credenciales ni cambia configuraciones ajenas al paso que falló.
