# readyproof: instalación privada en DigitalOcean

Estado al 27/10/2026. Instalación de revisión autorizada por Jorge en el servidor compartido `67.205.170.29`. **Sin dominio, publicación por IP, Nginx nuevo ni certificado HTTPS.** No se alteraron las rutas de Traefik ni los servicios Docker existentes. La aplicación admite datos ficticios, no instalaciones reales.

## Ingresar desde esta computadora

La pantalla de ingreso se verificó mediante un túnel SSH temporal, cerrado al terminar. Para utilizarla, abrir el túnel en tu propia consola con el comando de esta sección. La dirección es:

**http://127.0.0.1:8876/login**

Ese puerto corresponde al servidor remoto. El ejemplo anterior de Windows sigue siendo otro entorno, en el puerto 8765. El túnel cifra el transporte entre la computadora y el servidor; HTTP se usa solo en ambos extremos loopback. No hay una dirección pública de readyproof.

Cuenta administradora del servidor: **msanchez**, creada por el formulario HTTP de configuración inicial. No se copió ni cambió la contraseña de la cuenta local de Windows. El login del administrador fue comprobado por HTTP y se cerró la sesión al terminar la prueba.

Para consultar la contraseña temporal **solo en tu propia consola PowerShell**, ejecutar:

```powershell
ssh -i "$env:USERPROFILE\.ssh\readyproof_deploy_67_205_170_29" -o IdentitiesOnly=yes -o StrictHostKeyChecking=yes root@67.205.170.29 "cat /root/readyproof-admin-inicial.json"
```

No pegar la salida en el chat ni adjuntarla a reportes. Ingresar con esa clave y cambiarla en **Mi cuenta**. La clave queda en un archivo de root con modo 0600; la del servidor es temporal y distinta de la local. Después del cambio corresponde retirar esa copia temporal por un procedimiento privado.

Abrir el túnel desde la raíz del proyecto y mantener esa consola abierta:

```powershell
cd C:\Users\jorge\Readyproof
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\abrir_readyproof_privado.ps1
```

No abrir un segundo túnel si el puerto 8876 ya funciona. Ctrl+C cierra el túnel iniciado en esa consola; no apaga la aplicación del servidor. La clave SSH es privada de esta cuenta Windows y no debe copiarse a otra persona.

## Configuración instalada

| Componente | Estado |
|---|---|
| Código | `/home/readyproof`, repositorio solicitado por Jorge, commit `4cb1599840419b3faa18496349758b663265dcca`. |
| Sistema | Ubuntu 24.04.1 LTS; sin actualización general, reinicio del host ni cambio de firewall. |
| Dependencias | 72 paquetes nuevos, cero paquetes actualizados o eliminados; PostgreSQL 16, LibreOffice Calc y `fonts-crosextra-carlito`. |
| Python | Entorno `/home/readyproof/venv`, requisitos fijados y Gunicorn 26.2.0; `pip check` y compilación sin errores. |
| Servicio | `readyproof.service`, usuario sin login `readyproof`, un worker, escucha exclusiva `127.0.0.1:8000`. |
| PostgreSQL | Base `readyproof`, rol exclusivo `readyproof_user` sin superusuario ni permiso de crear roles/bases; escucha exclusiva `127.0.0.1:5432`. |
| Esquema | Migraciones Alembic hasta head y catálogo/cliente ficticio por CLI `init-db --ejemplos`. |
| Configuración | `.env` root:readyproof, modo 0640; claves de BD y sesión aleatorias generadas dentro del servidor. |
| Recursos | Slice conjunto: MemoryHigh 384 MB, MemoryMax 512 MB y CPUQuota 100 % de un CPU. App hasta 384 MB/50 %; PostgreSQL hasta 128 MB/25 %. Son límites, no capacidad reservada. |
| Correo | `MAIL_MODO_PRUEBA=true`, contraseña SMTP vacía; copia EML sin transmisión, sin worker ni scheduler de correo. |
| Backup | Dump diario local, permisos privados y restauración de prueba comprobada. Copia externa pendiente. |

Estos límites permiten la revisión inicial; el servidor comparte memoria con otras aplicaciones y no tiene swap. No acreditan capacidad para usuarios simultáneos. La instalación no cambió hostname, recursos contratados, DNS o certificados del servidor.

## Evidencias

- 256 archivos de app, fuentes, migraciones, pruebas y scripts del repositorio comparados contra la copia local: 192 idénticos y 64 con diferencia exclusiva CRLF/LF; ninguna diferencia de contenido. Los scripts locales de acceso SSH/túnel son auxiliares adicionales, no cambios al código desplegado.
- Suite local previa: 156 pruebas aprobadas. No se afirma haber ejecutado las 156 en Linux: su fixture PostgreSQL usa binarios Windows. En Ubuntu se verificó el recorrido real HTTP y generación con LibreOffice.
- Bootstrap de msanchez por HTTP, login, carga SAA-1, dos PNG de firma ficticia, vista previa, finalización, emisión y descarga aprobados. Canvas/dispositivo siguen siendo otra prueba.
- Carga `1a1cfc7c-0f86-454d-810e-4be1a90e9ba9`; envío de archivo `7a420378-3a2d-460d-9c00-58fc2100c3c1`. Un intento de archivo ok; no hubo SMTP ni recepción real en esta instalación.
- PDF de Ubuntu: dos páginas, 122049 bytes; logo vigente, leyenda IRAM en ambas, retención y metadatos verificados. SHA256 `f4978d1ac6d853e395afd7d01dfcc2fb061648cc7300d09f524036213873a87f`. Ambas páginas renderizadas y revisadas visualmente, con marcas de agua y firmas ficticias visibles.
- Evidencia local saneada: `out/despliegue_privado/resultado_ubuntu.json`, `comparacion_codigo.json`, `restauracion.json` y `acceso_privado.json`. No contienen contraseñas.

## Backup y operación

El servicio `readyproof-backup.service` ejecuta `pg_dump` en formato custom como usuario postgres; `readyproof-backup.timer` lo programa a las 02:00 UTC, con hasta diez minutos de demora aleatoria. Directorio `/var/backups/readyproof`, modo 0700, con dump, índice y SHA256. Sin purga automática.

Primera copia `readyproof-20261027T110423Z.dump`, 427122 bytes. Restaurada en la base separada `readyproof_restore_check_20261027`; recuentos coincidentes de un usuario, una carga, un envío y un intento, y huellas coincidentes de PDF/EML. La base restaurada se conserva como evidencia privada; no se restauró encima de la base activa.

La copia sigue dentro del mismo servidor: falta un destino externo autorizado y el procedimiento de conservación y recuperación fuera del Droplet. No se considera resuelta por esto la retención productiva integral de tres años.

Verificaciones de mantenimiento, sin mostrar configuración privada:

```bash
systemctl status readyproof postgresql@16-main readyproof-backup.timer
systemctl list-timers readyproof-backup.timer
journalctl -u readyproof --no-pager -n 30
systemctl show readyproof.slice -p MemoryCurrent -p MemoryPeak -p MemoryMax
```

Para detener solo la aplicación: `systemctl stop readyproof`. No detener Docker, Traefik, los PostgreSQL de contenedores ni el host. No eliminar bases o respaldos para resolver un error.

## Pendientes

Actualización posterior: usuario técnico tecnico_readyproof creado con cliente asignado y acceso SSH propio restringido, sin compartir root. Botón de documentación en Mi cuenta activo mediante Gmail HTTPS, con envío y recepción comprobados. Guías de entrega en `ENTREGA_A_BRAFEMAR.md` y `ACCESO_TECNICO_BRAFEMAR.md`. El correo de planillas permanece en modo de prueba; la activación de documentación no habilitó esa cola.

Jorge debe cambiar la clave temporal y revisar el acceso desde su navegador. Siguen pendientes dominio propio, HTTPS/publicación autorizada, correo real en este servidor, copia externa de respaldo, prueba de dispositivo/canvas, capacidad/concurrencia y habilitación de datos reales. No se declara producción ni entrega integral terminada.
