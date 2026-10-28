# Instalación y operación de readyproof en DigitalOcean

**Actualización posterior del 27/10/2026:** Jorge autorizó una instalación privada en el servidor compartido 67.205.170.29, sin dominio/publicación. Esa instalación y sus verificaciones reales están en [Acceso al servidor privado](ACCESO_SERVIDOR_PRIVADO.md). La receta siguiente conserva el diseño inicial para un Droplet separado y no describe literalmente el servicio privado instalado.

Documento preparado el 27/10/2026. **No se ejecutó un despliegue ni se accedió a DigitalOcean en esta tarea.** Los comandos son instrucciones para la persona responsable de la instalación. No constituyen evidencia de HTTPS, respaldo o monitoreo activos.

## Estado y condiciones previas

La aplicación actual es un entorno local con datos ficticios. Antes de una publicación hay que resolver y verificar:

- Restricción de solicitudes a loopback en `app/__init__.py` y origen/CSRF en `app/auth/__init__.py`, con el proxy concreto y HTTPS. Gunicorn puede reconstruir el esquema a partir de cabeceras confiables; debe comprobarse con una petición real. No deshabilitar CSRF ni confiar en cabeceras de cualquier origen.
- La configuración de proxy y la obtención de la IP real. Agregar `ProxyFix(x_for=1)` sin revisar el filtro actual de `remote_addr` puede provocar rechazos de solicitudes. [Flask explica cómo definir los proxies confiables](https://flask.palletsprojects.com/en/stable/deploying/proxy_fix/).
- Habilitación técnica de datos reales, campos obligatorios, acceso y protección de firmas/dispositivos, exportación/borrado cuando corresponda, respaldo y retención. Las validaciones actuales siguen admitiendo solo ejemplos.
- Prueba del paquete en Ubuntu. Las pruebas locales actuales emplean una fixture PostgreSQL con ejecutables Windows `.exe`; el resultado de Windows no acredita por sí solo una ejecución equivalente en Linux. Preparar el runner Linux antes de marcar esa verificación.
- Dominio, DNS, tamaño/región/costo del Droplet, operador, destino de respaldo fuera del servidor y permisos aprobados por Jorge. No tocar el otro proyecto de la cuenta.

La instalación de ejemplo puede prepararse en un servidor **nuevo y separado**, sin exponer todavía la aplicación. El uso público con clientes reales permanece bloqueado hasta la aprobación correspondiente. Los accesos y aprobaciones siguen el instructivo `PASOS_SERVICIO_FINAL_readyproof.md`; las contraseñas y códigos de dos pasos no pasan por chat.

## Requisitos de referencia

| Componente | Referencia y verificación |
|---|---|
| Sistema | Ubuntu 24.04 LTS, como base de este procedimiento; imagen definitiva pendiente de aprobación. |
| Python | 3.12 de esa distribución; proyecto requiere Python 3.11 o superior. |
| Aplicación | Flask y dependencias fijadas en `requirements.txt`; PostgreSQL vía SQLAlchemy/psycopg. |
| Base | PostgreSQL local al nuevo Droplet; no usar la base del otro proyecto. El código actual rechaza conexiones PostgreSQL a hosts remotos. |
| WSGI | Gunicorn 26.2.0, versión fija de referencia publicada; validar integración antes de aprobar la instalación. No se agregó ni instaló en esta máquina Windows. |
| Proxy y TLS | Nginx, Certbot y un dominio aprobado que resuelva al servidor. |
| PDF | LibreOffice Calc headless y fuentes compatibles con la serie; comparar páginas y diseño contra referencia. |
| Correo | Transporte implementado Gmail, STARTTLS en 587. La implementación actual no admite simplemente sustituirlo por cPanel. |
| Servicio | systemd, usuario de sistema sin login y directorios privados. |

[Flask requiere un servidor apropiado para producción](https://flask.palletsprojects.com/en/stable/deploying/). [Gunicorn recomienda ejecutarse detrás de un proxy y sin usuario root](https://flask.palletsprojects.com/en/stable/deploying/gunicorn/); la [versión de referencia está publicada en PyPI](https://pypi.org/project/gunicorn/26.2.0/). La receta de [preparación de Droplets de DigitalOcean](https://docs.digitalocean.com/products/droplets/getting-started/recommended-droplet-setup/) es una referencia para SSH, firewall y opciones iniciales, no una autorización para crear recursos con costo.

## 1 Preparar el servidor aprobado

Estos pasos se ejecutan únicamente en el Droplet nuevo autorizado. Usar SSH con clave; mantener un operador con sudo y un usuario separado para la aplicación. Revisar cada cambio de firewall y DNS con Jorge antes de aplicarlo.

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip postgresql postgresql-client libreoffice-calc fonts-crosextra-carlito nginx certbot python3-certbot-nginx
sudo useradd --system --home-dir /var/lib/readyproof --create-home --shell /usr/sbin/nologin readyproof
sudo install -d -o root -g readyproof -m 0750 /opt/readyproof /etc/readyproof
sudo install -d -o readyproof -g readyproof -m 0700 /opt/readyproof/out
```

Copiar una entrega revisada a `/opt/readyproof`, incluyendo `app/`, `fuente/`, `migraciones/`, `alembic.ini` y requisitos. **No copiar** `.env.local`, la base de revisión Windows, `.venv`, `out/`, cookies o datos de pruebas como si fueran producción. No clonar ni crear repositorios externos sin autorización.

Crear el entorno e instalar versiones fijadas:

```bash
sudo python3 -m venv /opt/readyproof/.venv
sudo /opt/readyproof/.venv/bin/python -m pip install -r /opt/readyproof/requirements.txt 'gunicorn==26.2.0'
sudo /opt/readyproof/.venv/bin/python -m pip check
sudo chown -R root:readyproof /opt/readyproof
sudo chmod -R g-w,o-rwx /opt/readyproof
sudo chown -R readyproof:readyproof /opt/readyproof/out
sudo chmod 0700 /opt/readyproof/out
```

Gunicorn es necesario para el servicio propuesto; por eso se incluye en estas instrucciones. No se cambian las dependencias del entorno local por redactar el deployment. Registrar la versión efectivamente aprobada y el resultado del ensayo Ubuntu antes de publicar.

## 2 Crear PostgreSQL y configuración privada

En una base nueva, los siguientes comandos piden la contraseña en la consola; no incluirla en argumentos o historial:

```bash
sudo -u postgres createuser --no-superuser --no-createdb --no-createrole --pwprompt readyproof
sudo -u postgres createdb --owner=readyproof readyproof
```

No ejecutarlos para reemplazar una base existente. En una actualización, realizar primero un dump, identificar la revisión de esquema y aplicar solo las migraciones correspondientes. No borrar usuarios o cargas para resolver problemas de acceso.

Crear `/etc/readyproof/readyproof.env`, propietario `root:readyproof`, modo `0640`. Completar allí los valores privados; este bloque está deliberadamente incompleto:

```ini
DATABASE_URL=
SECRET_KEY=
READYPROOF_HTTPS=false
MAIL_MODO_PRUEBA=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=readyproof.ar@gmail.com
SMTP_PASSWORD=
MAIL_FROM=readyproof.ar@gmail.com
LIBREOFFICE_BIN=/usr/bin/soffice
```

`DATABASE_URL` usa el formato `postgresql+psycopg://readyproof:CLAVE_CODIFICADA@127.0.0.1:5432/readyproof`, con la clave codificada como componente URL. El ejemplo de formato no es una credencial utilizable. `SECRET_KEY` debe ser aleatoria, persistente, exclusiva del servicio y de al menos 32 caracteres; no dejar que cada worker genere una distinta. Guardar claves solo en el archivo privado o gestor autorizado. No copiar el valor de ejemplo del repositorio.

`READYPROOF_HTTPS=false` se usa **solo para el bootstrap privado por túnel**. Cambiarlo a `true` antes de habilitar la web HTTPS. `MAIL_MODO_PRUEBA=true` mantiene el transporte en archivo durante la preparación. No activar envío real ni worker por esta documentación.

Inicializar el esquema y el catálogo del entorno de prueba privado mediante el CLI de la aplicación. El cargador dotenv interpreta los valores sin ejecutarlos como comandos de shell:

```bash
cd /opt/readyproof
sudo -u readyproof /opt/readyproof/.venv/bin/python -c "from dotenv import load_dotenv; load_dotenv('/etc/readyproof/readyproof.env'); from flask.cli import main; main(args=['--app','app','init-db','--ejemplos'])"
```

`--ejemplos` identifica expresamente esta instalación de revisión. No habilita clientes reales. En bases existentes, el cargador conserva las versiones anteriores y no sobrescribe definiciones incompatibles. El correo y los usuarios de DigitalOcean son independientes de las cuentas de readyproof.

## 3 Servicio Gunicorn privado y primer administrador

Guardar `/etc/systemd/system/readyproof.service`:

```ini
[Unit]
Description=readyproof
After=network.target postgresql.service
ConditionPathExists=/etc/readyproof/INSTALACION_AUTORIZADA

[Service]
User=readyproof
Group=readyproof
WorkingDirectory=/opt/readyproof
EnvironmentFile=/etc/readyproof/readyproof.env
Environment=HOME=/var/lib/readyproof
ExecStartPre=/opt/readyproof/.venv/bin/python -c "import os; assert len(os.environ.get('SECRET_KEY','')) >= 32, 'Configurar SECRET_KEY persistente'; assert os.environ.get('DATABASE_URL'), 'Configurar DATABASE_URL'"
ExecStart=/opt/readyproof/.venv/bin/gunicorn --workers 2 --bind 127.0.0.1:8000 --timeout 180 --forwarded-allow-ips 127.0.0.1 --access-logfile - --error-logfile - app:create_app()
Restart=on-failure
RestartSec=5
UMask=0077
NoNewPrivileges=true
PrivateTmp=true
ProtectHome=true
ProtectSystem=strict
ReadWritePaths=/opt/readyproof/out /var/lib/readyproof

[Install]
WantedBy=multi-user.target
```

Los dos workers son una configuración inicial de ensayo, no un dimensionamiento aprobado. Medir RAM y concurrencia de LibreOffice antes de elegir el tamaño final. El timeout debe permitir la conversión PDF; no resolver demoras aumentando procesos sin medir.

Solo después de la autorización de instalación, una persona crea el marcador y activa el servicio:

```bash
sudo install -m 0600 /dev/null /etc/readyproof/INSTALACION_AUTORIZADA
sudo systemctl daemon-reload
sudo systemctl enable --now readyproof
sudo systemctl status readyproof
```

**Crear el primer admin antes de exponer la aplicación.** Desde el equipo del operador, abrir un túnel SSH al puerto privado:

```bash
ssh -L 8765:127.0.0.1:8000 OPERADOR@IP_APROBADA
```

Abrir `http://127.0.0.1:8765/login`, crear el primer administrador con contraseña escrita solo en el formulario y verificar que `/configuracion-inicial` quede cerrado. Si ya existen cuentas, ingresar con una administradora o usar el procedimiento de recuperación local autorizado; nunca reabrir el bootstrap eliminando usuarios. El servicio WSGI sigue enlazado a loopback y no debe exponerse directamente. [Configuración de despliegue de Gunicorn](https://gunicorn.org/deploy/).

## 4 Nginx y HTTPS después de la aprobación

El dominio aún debe elegirse y aprobarse. `readyproof.example.invalid` es un marcador documental, no un dominio registrado. No guardar registros DNS ni solicitar certificados sobre un nombre sin autorización.

Preparar `/var/www/letsencrypt` y un virtual host HTTP que, hasta obtener TLS, sirva únicamente el desafío ACME y devuelva mantenimiento para la aplicación:

```nginx
server {
    listen 80;
    server_name readyproof.example.invalid;
    location /.well-known/acme-challenge/ {
        root /var/www/letsencrypt;
    }
    location / { return 503; }
}
```

Sustituir los marcadores por el dominio y contacto aprobados, revisar `nginx -t`, DNS y firewall. El procedimiento de certificado utiliza el webroot autorizado:

```bash
sudo certbot certonly --webroot -w /var/www/letsencrypt -d DOMINIO_APROBADO
sudo certbot renew --dry-run
```

La emisión y la prueba de renovación no se ejecutaron aquí. [Certbot documenta la renovación automática y sus pruebas](https://eff-certbot.readthedocs.io/en/stable/using.html#automated-renewals).

El virtual host HTTPS posterior debe usar sus archivos reales de certificado y reenviar únicamente a Gunicorn privado. Fragmento de referencia:

```nginx
server {
    listen 443 ssl;
    server_name readyproof.example.invalid;
    ssl_certificate /etc/letsencrypt/live/DOMINIO_APROBADO/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/DOMINIO_APROBADO/privkey.pem;
    client_max_body_size 768k;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_read_timeout 190s;
    }
}
```

Cambiar `READYPROOF_HTTPS=true` en el archivo privado y reiniciar readyproof. Probar desde HTTPS login, cookie Secure, Origin/CSRF, roles, firma, generación y descarga. Si aparece 403 por esquema/origen o por IP, revisar la configuración de proxy y el filtro local; **no eliminar esos controles para que el formulario pase**. Mantener cerrada la publicación hasta aprobar la integración.

Revisar renovación, redirección HTTP a HTTPS y exposición exclusiva de SSH, HTTP/HTTPS según el plan aprobado. PostgreSQL y Gunicorn no deben ser puertos públicos. Que exista esta configuración de ejemplo no autoriza marcar «HTTPS configurado» en el checklist.

## 5 Backup automático y restauración

El respaldo lógico incluye datos, usuarios, firmas, PDF emitidos y copias EML guardadas en PostgreSQL. Respaldar por separado configuración privada y archivos auxiliares bajo control del responsable. **Un ZIP del código o del logo no es un respaldo de la base.**

En el servidor futuro, guardar como `/usr/local/sbin/readyproof-backup`, propietario root, ejecutable y sin contraseñas:

```bash
#!/usr/bin/env bash
set -euo pipefail
umask 077
dest=/var/backups/readyproof
stamp=$(date -u +%Y%m%dT%H%M%SZ)
dump="$dest/readyproof-$stamp.dump"
pg_dump --format=custom --dbname=readyproof --file="$dump"
pg_restore --list "$dump" > "$dump.toc"
sha256sum "$dump" > "$dump.sha256"
```

Crear `/var/backups/readyproof` con propietario postgres y modo `0700`. El servicio utiliza el usuario local postgres y autenticación local del servidor; no se copia una contraseña al script. [PostgreSQL describe el dump como una instantánea lógica consistente](https://www.postgresql.org/docs/16/backup-dump.html) y el [formato de archivo para restaurar con pg_restore](https://www.postgresql.org/docs/16/app-pgdump.html).

`/etc/systemd/system/readyproof-backup.service`:

```ini
[Unit]
Description=Respaldo PostgreSQL de readyproof
After=postgresql.service

[Service]
Type=oneshot
User=postgres
ExecStart=/usr/local/sbin/readyproof-backup
UMask=0077
```

`/etc/systemd/system/readyproof-backup.timer`:

```ini
[Unit]
Description=Respaldo diario de readyproof

[Timer]
OnCalendar=*-*-* 02:00:00 UTC
Persistent=true
RandomizedDelaySec=600

[Install]
WantedBy=timers.target
```

Después de revisar propietario, rutas, permisos y espacio, la persona instaladora habilita el timer y ejecuta una primera copia. [Semántica de timers systemd](https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html).

```bash
sudo systemctl daemon-reload
sudo systemctl start readyproof-backup.service
sudo systemctl enable --now readyproof-backup.timer
sudo systemctl list-timers readyproof-backup.timer
sudo journalctl -u readyproof-backup.service --no-pager
```

Comprobar el checksum y **restaurar en una base temporal vacía**, nunca sobre readyproof:

```bash
sudo -u postgres createdb readyproof_restore_check_FECHA
sudo -u postgres pg_restore --exit-on-error --no-owner --no-privileges --dbname=readyproof_restore_check_FECHA /var/backups/readyproof/ARCHIVO_SELECCIONADO.dump
```

Comparar recuentos e integridad de cargas/PDF/firmas y documentar resultado y responsable sin publicar sus contenidos. Esta prueba sigue pendiente; no confundir `pg_restore --list` con una restauración verificada.

La copia debe salir también del Droplet a un destino aprobado, cifrada y con acceso restringido. Definir con Jorge destino, responsable y política; no crear una cuenta de almacenamiento ni transferir datos por esta guía. Conservar registros al menos tres años desde la emisión. No se propone una purga automática de archivos. Los [backups de Droplets](https://docs.digitalocean.com/products/backups/how-to/create-and-restore/) son un mecanismo adicional de recuperación del servidor, no prueba de restaurabilidad lógica de la aplicación.

## 6 Monitoreo y mantenimiento

- Revisar `systemctl status readyproof postgresql nginx`, errores de servicio con `journalctl -u readyproof` y errores Nginx. No pegar variables de entorno ni cuerpos de login en reportes.
- Medir RAM, CPU, espacio libre, reinicios, latencia de emisión PDF y cantidad de conexiones PostgreSQL. Confirmar que `/opt/readyproof/out` no queda expuesto como directorio web.
- Verificar fecha y resultado del último backup, espacio disponible y una restauración periódica documentada. Comprobar timers y renovación TLS.
- Revisar cola e intentos de correo. Un envío en modo archivo puede quedar pendiente deliberadamente; no cambiar el modo ni repetir POST para intentar transmitirlo.
- Mantener paquetes y dependencias mediante una entrega validada, con respaldo previo y plan de reversión. No copiar una versión nueva encima de registros emitidos.

El servicio de [Monitoring de DigitalOcean](https://docs.digitalocean.com/products/monitoring/) permite métricas y alertas cuando se habilita su agente. No fue instalado ni configurado en esta tarea. Destinatarios y umbrales deben acordarse con el responsable.

## 7 Troubleshooting

| Síntoma | Revisar |
|---|---|
| Gunicorn no inicia | DATABASE_URL local válida, SECRET_KEY persistente, permisos del `.env`, entorno virtual, marcador de autorización y journal. |
| Nginx 502 | Estado de Gunicorn y coincidencia de `proxy_pass` con el puerto privado. |
| Login 401 | Usuario creado, cuenta activa y contraseña ingresada; no resetear ni borrar cuentas sin autorización. |
| Login 429 | Cinco fallos recientes; esperar el intervalo. No eludir el registro. |
| Escritura 403 | Origen HTTPS, CSRF, cookie Secure, esquema transmitido y política de proxy/loopback. |
| PDF 503 | LibreOffice instalado, fuentes, HOME y temporales privados escribibles, espacio y timeout. |
| Plantilla incompatible | Versión/huella y archivos del kit de esa entrega; registrar una versión nueva, no sobrescribir historia. |
| Envío pendiente | Determinar si es modo archivo o cola real. Procesar el envío identificado y revisar Intento; no repetir POST. |
| SMTP rechazado o aceptación desconocida | Revisar categorías/códigos saneados, casilla autorizada y Enviados. No reintentar una aceptación ambigua automáticamente. |
| Backup fallido | Journal, espacio, acceso PostgreSQL y ruta privada. No marcar éxito por existir un archivo vacío. |

## Prueba operativa local

El script nuevo **no despliega**, no inicia workers y no abre cuentas. Consume la API del ejemplo local y procesa solo el envío que acaba de crear. Su contraseña se solicita de forma oculta en una consola interactiva.

Sin correo real:

```powershell
cd C:\Users\jorge\Readyproof
.\.venv\Scripts\python.exe scripts\prueba_operativa_final.py --usuario msanchez --salida out\prueba_operativa_archivo --abrir-pdf
```

Para una prueba SMTP expresamente autorizada, la casilla elegida en esta revisión es la de Jorge:

```powershell
.\.venv\Scripts\python.exe scripts\prueba_operativa_final.py --usuario msanchez --smtp --destinatario jorgesanchezing@gmail.com --salida out\prueba_operativa_final --abrir-pdf
```

El script guarda identificadores, PDF, verificación de logo/leyenda/retención/metadatos y resultado del intento en la carpeta de salida. No guarda clave, cookies ni CSRF. Sus firmas son PNG ficticios por API; la prueba del canvas se hace por la [guía de acceso](GUIA_ACCESO_BRAFEMAR.md), no se declara resuelta por este script.

Después de recibir y abrir el adjunto, escribir `RECIBIDO_Y_REVISADO` en la consola. La recepción es una declaración del operador, no una lectura automática de Gmail. El Message-ID permite verificar Enviados sin confundirlo con recepción. Si se confirma más tarde:

```powershell
.\.venv\Scripts\python.exe scripts\prueba_operativa_final.py --confirmar-recepcion out\prueba_operativa_final\resultado.json --abrir-pdf
```

Ese comando no vuelve a enviar. No repetir el POST ni borrar evidencias para reenviar. Para otra prueba independiente, elegir una carpeta nueva y revisar destinatario. Código 0 significa ejecución correcta del modo elegido: en modo archivo **no implica entrega real**. Con SMTP, código 2 deja pendiente la confirmación de recepción/apertura; código 1 indica que hay un error que revisar antes de repetir acciones.

El 27/10/2026 Jorge confirmó acceso a msanchez, pero indicó que todavía no ejecutó este script. La prueba real nueva queda pendiente hasta disponer de su reporte y confirmación; la prueba de correo anterior del 26/10 conserva su evidencia separada.
