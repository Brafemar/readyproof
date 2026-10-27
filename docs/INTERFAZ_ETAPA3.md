# Interfaz SAA-1 — etapa 3

Actualización de etapa 4: el recorrido ahora requiere iniciar sesión. El primer administrador se crea en la pantalla local de configuración y los técnicos necesitan clientes asignados; ver USUARIOS_ETAPA4.md. La descripción siguiente conserva el flujo de carga de etapa 3.

La interfaz se genera desde la definición vigente del kit: conserva el orden de bloques, los textos, las opciones y las unidades. Incluye selección de cliente/sistema/planilla, avance, autoguardado, observaciones, firma de prueba del técnico y del responsable, vista previa y emisión PDF de ejemplo.

## Abrir para revisión local

```powershell
.venv\Scripts\python.exe scripts/iniciar_ejemplo.py
```

Abre el servicio en http://127.0.0.1:8765. Usa un clúster PostgreSQL propio en `out/etapa3/demo_local/`, enlazado a 127.0.0.1 y con datos ficticios; no usa la base habitual ni su contraseña. No debe contener datos ni firmas personales reales. El clúster se detiene al cerrar el servidor con Ctrl+C; su carpeta se conserva para poder recuperar ejemplos en una revisión posterior. No se cambia la autenticación del servicio PostgreSQL habitual ni se publica la aplicación.

Para usar una base local configurada por una persona, `init-db --ejemplos` aplica la migración aditiva 2 y conserva las cargas de la etapa 2. Después puede iniciarse Flask como se documenta en API_ETAPA2.md.

## Carga y revisión

1. Seleccionar cliente, sistema y SAA-1. En esta etapa solo se muestran ejemplos.
2. Completar los campos o usar «Completar ejemplo». Se mantienen los tipos de fecha, número y opción; los textos ficticios llevan `[Ejemplo]`. Empresa mantenedora conserva el valor original readyproof del kit.
3. Los cambios y las firmas se guardan en el dispositivo y se sincronizan cuando hay conexión. El indicador distingue guardado local de guardado en el servidor. La lista lateral permite recuperar borradores y crear uno nuevo sin borrar los anteriores.
4. Dibujar firmas ficticias con dedo, lápiz o mouse. «Limpiar» borra solo la firma correspondiente del borrador.
5. Generar y revisar la vista previa. No finaliza ni emite. Si se modifica algún dato o firma, se debe generar otra vista previa antes de finalizar.
6. «Finalizar ejemplo» requiere las dos firmas de prueba y una vista previa actualizada. Tras emitir, la carga queda sin edición y el PDF puede descargarse.

El progreso indica campos completados, no una evaluación normativa ni una política de campos obligatorios. La API de la etapa 2 conserva la posibilidad de cargas parciales; el kit no define qué campos son obligatorios. Esa pregunta continúa pendiente para uso real.

## Trabajo sin conexión

El formulario, los recursos y el catálogo se preparan después de una primera apertura conectada. Los borradores se guardan en IndexedDB, restringido al origen del navegador; el service worker conserva únicamente la pantalla y sus recursos, nunca respuestas de API, PDF ni firmas. Una vez preparada la aplicación, se puede cargar, firmar y recargar sin red, y recuperar el mismo borrador al volver.

La sincronización de esta etapa usa un identificador local estable y revisiones del servidor para impedir creación duplicada y sobrescritura silenciosa. Ante un conflicto se conserva la copia local y se ofrece guardarla como un borrador nuevo. La cola completa de sincronización y la resolución de versiones entre distintos dispositivos siguen siendo trabajo de la etapa 8; no se consideran completadas aquí.

Las vistas previas y las emisiones necesitan conexión al servicio local, PostgreSQL y LibreOffice. La primera apertura sin haber preparado recursos ni catálogo requiere conectarse. El estado de guardado informa si el almacenamiento del navegador no está disponible o se llena; no debe cerrarse la pantalla hasta recuperar el guardado.

## Firmas y persistencia

La migración 2 agrega firmas PNG por carga y sus huellas al historial, sin borrar datos ni tocar fuente/. Se valida formato PNG, tamaño máximo de 200 KB por firma, dimensiones máximas 1200×500 y presencia de trazos; las imágenes se vuelven a codificar antes de guardarlas. No se aceptan roles distintos del técnico y el responsable.

Las firmas no tienen endpoints de descarga individuales y no se devuelven en base64 al consultar cargas o revisiones. Solo se muestran en su planilla, su vista previa y su PDF. La interfaz conserva en el dispositivo únicamente las firmas de sus propios borradores. En el servidor, se guardan en la base local y el historial contiene sus hashes, no la imagen. La identificación y permisos por usuario corresponden a la etapa 4; por eso sigue prohibido utilizar firmas personales reales en este entorno de ejemplo.

El PDF utiliza las imágenes originales de encabezado y los espacios de firma existentes. La posición de las firmas se calcula desde los rangos combinados del Excel y las etiquetas del pie en el PDF, sin cambiar filas, escalas ni leyendas del kit.

## Verificaciones

Las dependencias Python se instalan con `requirements-dev.txt`. El recorrido de navegador usa Node.js y Playwright 1.62.1 (declarado en package.json) y un Chromium, Chrome o Edge local. Para preparar esas dependencias en una máquina de desarrollo, una persona puede instalar Playwright dentro de la carpeta ignorada del entorno:

```powershell
npm install --prefix .venv/browser --no-save playwright@1.62.1
$env:NODE_PATH = (Resolve-Path .venv/browser/node_modules).Path
$env:READYPROOF_NODE = (Get-Command node).Source
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe -m compileall app
```

`READYPROOF_BROWSER` permite indicar el ejecutable de un navegador local existente. La prueba falla si falta un requisito; no se omite. Para esta entrega se reutilizaron Node.js, Playwright y el navegador ya disponibles, sin descargas nuevas.

El recorrido táctil comprueba la misma secuencia que un usuario: formulario en celular de 390×844, rechazo de texto sin prefijo, carga sin red, dos firmas mediante eventos de pantalla táctil, recarga offline, reconexión sin duplicar el borrador, vista previa, finalización y descarga. También verifica ausencia de desbordamiento a 390 y 1440 píxeles. Las pruebas de API verifican PNG inválidos, almacenamiento sin exposición de imágenes, limpieza de firmas y migración conservando datos previos.

Capturas y PDF de revisión: `out/etapa3/navegador/`. La comprobación se realiza mediante emulación de celular en un navegador real; una revisión manual en un teléfono físico queda para el técnico de prueba.

## Pendientes y alcance

La leyenda M1 se incorporó posteriormente; el entorno continúa limitado a ejemplos por los otros controles pendientes. Usuario se difirió a la etapa 4 y Envio a la etapa 5 con confirmación de Jorge; no se implementan aquí. Las coordenadas fijas de n1 se corrigieron al incorporar la leyenda; los nuevos grupos siguen pendientes de cotejo. Los criterios de campos obligatorios y las demás decisiones técnicas de Martín permanecen abiertos.
