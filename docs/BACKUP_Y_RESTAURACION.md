# Backup y restauración de readyproof

## Estado de implementación — 28/10/2026

Etapa 1 completada y verificada. Rclone autorizado para `readyproof.ar@gmail.com`; respaldo cifrado subido y descargado desde Drive; restauración en una base separada; timer nuevo activo y ejecución bajo systemd satisfactoria. Durante Etapa 1 no se restauró sobre producción ni se reinició la aplicación. Actualización de Etapa 2: 011–012 aplicadas, modelo activo y modo piloto conservado; el respaldo y su restauración posteriores están verificados en esquema 012.

Evidencia: `out/etapa1_backup/verificacion_drive_restore.json`. Copia verificada: `daily/readyproof-2026-10-28.tar.enc`, esquema `010_firmantes`. Restauración final: `readyproof_test_restore_20261028T040154`; 17 tablas, 25 planillas, 45 cargas, 45 filas de firmas y 7 envíos. Coincidieron los 130 binarios y los 48 PDFs exportados. La huella del cifrado restaurado coincide con la del último respaldo ejecutado bajo systemd.

La clave está en el servidor con permisos 0600; su copia de recuperación está cifrada con DPAPI CurrentUser y verificada en `C:\Users\jorge\.ssh\readyproof_backup_key.dpapi`. La configuración anterior del timer y servicio se conserva en `/var/backups/readyproof/config-previa-20261028T040036`. El aviso de fallos está conectado mediante OnFailure; no se provocó una falla ficticia ni se envió una alerta de prueba presentada como un incidente real.

## Cuenta y secretos

Jorge autoriza `readyproof.ar@gmail.com` en Google. El cliente OAuth de escritorio se lee desde su archivo privado; no copiarlo al repositorio ni compartir códigos, tokens o contraseñas por chat. El permiso `drive.file` limita Drive a los archivos creados por esta autorización. Gmail conserva su configuración independiente. La API Google Drive debe estar habilitada en el proyecto de ese cliente.

El remoto `readyproof-drive` usa `/etc/readyproof/rclone-backup.conf`, modo 0600. La clave de respaldo se almacena fuera del repositorio en `/etc/readyproof/backup.env`, modo 0600, como `READYPROOF_BACKUP_KEY`. Generarla con 48 bytes aleatorios mediante `secrets.token_urlsafe(48)`, sin imprimirla. No reemplazar una clave existente: las copias anteriores la necesitan. Guardar además una copia de recuperación en el gestor de contraseñas de Jorge o protegida para su usuario de Windows. La copia DPAPI requiere el usuario y las credenciales de Windows que la protegieron; no se puede descifrar simplemente copiándola a otra PC. Para recuperación independiente del equipo, Jorge debe conservar además la clave en su gestor de contraseñas. Sin una copia recuperable, perder el servidor y la PC administradora podría hacer irrecuperable el respaldo cifrado.

La autorización de Gmail existente no autoriza Drive. Si el proyecto OAuth está en pruebas, revisar la duración del permiso renovable antes de depender de él para respaldos desatendidos; una autorización que venza debe renovarse y verificarse.

## Contenido y consistencia

El proceso abre una transacción de lectura repetible y exporta su snapshot PostgreSQL. `pg_dump` y la exportación de PDFs usan ese mismo snapshot. El archivo contiene:

- `readyproof.dump`, formato custom sin propietarios ni ACL;
- `manifest.json`: esquema, conteos de todas las tablas, tamaño y SHA256 de PDFs y firmas;
- `pdf/`: PDFs canónicos de cargas y copias de envíos obtenidos de la BD.

Las firmas PNG permanecen dentro del dump y se verifican por hash en la restauración. No se toma una carpeta temporal como sustituto del archivo completo de PDFs.

El tar se cifra con AES-256-CBC, sal aleatoria y PBKDF2-SHA256 de 600.000 iteraciones. Se agrega HMAC-SHA256 con clave derivada y SHA256 del cifrado. La restauración verifica ambos antes de descifrar. Los archivos temporales sin cifrar tienen acceso privado y se eliminan al terminar.

## Destino, retención y ejecución

Destino: `readyproof-drive:readyproof-backups/daily/` y `monthly/`. Cada copia tiene archivo `.tar.enc` y metadatos `.tar.enc.json`. Se verifica la subida descargando el archivo cifrado y comparando su hash.

Se conserva la última copia de cada día, hasta treinta días con respaldo, y la última de cada mes, hasta doce meses. Repetir en el mismo día actualiza esa copia diaria y la del mes. La retención solo actúa sobre nombres propios dentro de esas subcarpetas; no purga otros archivos ni vacía la papelera de Drive. Controlar el espacio disponible de la cuenta.

Un bloqueo evita dos respaldos simultáneos. El timer ejecuta a las 02:00 UTC (23:00 de Argentina) con hasta quince minutos de demora y recuperación de ejecuciones omitidas. El servicio registra en `/var/backups/readyproof/backup.log`, sin credenciales ni contenido de clientes. `OnFailure` llama a Gmail HTTPS para avisar a `readyproof.ar@gmail.com`; si el propio aviso falla, queda visible en systemd y requiere revisión.

Una vez instalada y probada la configuración:

```bash
systemctl start readyproof-backup.service
systemctl status readyproof-backup.service readyproof-backup.timer
systemctl list-timers readyproof-backup.timer
cat /var/backups/readyproof/ultimo_backup.json
```

Los archivos `ultimo_backup.json` y `ultima_restauracion.json` contienen evidencia saneada, no contraseñas.

## Restauración manual de prueba

Usar una copia ya verificada y una clave recuperada de la custodia privada. Ejecutar como administrador del servidor:

```bash
cd /home/readyproof
venv/bin/python scripts/backup_readyproof.py restore \
  --remote readyproof-drive:readyproof-backups/daily/readyproof-AAAA-MM-DD.tar.enc --schema-esperado 012_sistema_cliente_activo --planillas-esperadas 25
```

El comando descarga el cifrado y sus metadatos desde Drive; verifica HMAC y SHA256; descifra; valida miembros del tar y hash del dump; crea una BD nueva `readyproof_test_restore_<fechaUTC>`; restaura en una transacción y compara esquema, tablas, todos los conteos, PDFs y firmas contra el manifiesto del snapshot.

No elimina una BD existente ni restaura encima de `readyproof`. La BD de prueba se conserva para revisión. No levantar la aplicación ni procesos de envío contra esa BD. La comprobación es local, sin exposición de red de la restauración.

Usar en `--schema-esperado` la versión del respaldo que se quiere recuperar: `010_firmantes` para la evidencia de Etapa 1 y `012_sistema_cliente_activo` para las copias posteriores a Etapa 2. La comparación del manifiesto completo siempre es obligatoria. `--planillas-esperadas` permite además exigir el conteo previsto. No reutilizar una copia vieja de 009 como evidencia de 010 o 012.

Una recuperación de producción es una operación distinta: primero restaurar y comprobar una BD separada; luego planificar el cambio de conexión y el reinicio con autorización explícita, conservando la BD original. El script no realiza ese cambio.

## Verificación del código

`tests/test_backup_drive.py`: ocho casos sin red ni BD, sobre autenticación, manipulación de archivos, destinos rechazados y límites de retención. La subida, descarga y restauración operativas están acreditadas en la evidencia indicada. Las ocho pruebas unitarias pasaron y se compiló el código sin errores; la suite integral anterior no se presenta como reejecutada en esta etapa.


## Actualización Etapa 2

El último respaldo verificado está en `012_sistema_cliente_activo`, y fue restaurado separadamente en `readyproof_test_restore_20261028T050215`. Evidencia actual: `out/etapa2_cuit/resultado_etapa2.json`. El archivo diario se actualiza durante el día; sus huellas históricas no deben confundirse con la última copia disponible.

La copia 010 previa a la migración se preservó aparte en `pre-migrations/readyproof-pre-012-20261028T045106.tar.enc` y también se restauró correctamente. El comando restore admite únicamente nombres propios controlados dentro de daily, monthly y pre-migrations. Para esta copia previa usar `--schema-esperado 010_firmantes`; para la actual, `--schema-esperado 012_sistema_cliente_activo`. En ambos casos, `--planillas-esperadas 25`. Las copias de pre-migrations no se purgan por el límite de treinta diarios/doce mensuales: su eliminación requiere una decisión específica.


## Actualización Etapa 3

Código de validación e importador aplicados sin cambiar el esquema 012 ni las definiciones existentes. Respaldo y restauración posteriores verificados en readyproof_test_restore_20261028T110135, con 17 tablas y 130 binarios coincidentes. Evidencia más reciente de este cierre: out/etapa3_importador/resultado_servidor.json. Se conserva el procedimiento de recuperación y la copia previa de Etapa 2.


## Verificación posterior a 013 — 28/10/2026

El respaldo incorpora también las emisiones PDF inmutables de emisiones_carga: copia binaria independiente, SHA256 y dump completo. La restauración sigue reconociendo respaldos 010/012 sin esa tabla.

Última prueba: readyproof_test_restore_20261028T115558, esquema 013_desbloqueo_revision; 19 tablas, 130 binarios y 48 PDFs exportados comparados. Se verificaron los conteos de 45 cargas, 45 filas de firmas, 7 envíos y 25 versiones de plantilla. El SHA256 descargado coincide con el respaldo cifrado en Drive; la BD activa no se restauró ni sustituyó. Evidencia: out/etapa4_revision/verificacion_servidor.json. Existe además una copia privada pre-013 preservada fuera de la rotación diaria/mensual.
