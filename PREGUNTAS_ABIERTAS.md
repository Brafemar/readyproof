# Preguntas abiertas: readyproof

1. **NFPA 17A y NFPA 10:** falta la edición vigente de ambas. Las copias que circulan no son de fuente autorizada y no se citan ni se copian. Pendiente de compra o de acceso legítimo de readyproof. Ver `AGENTS.md`, decisión 19.
2. **Leyenda visible:** confirmar con el Lic. Martín Sánchez el texto exacto de «Planilla conforme a IRAM 3546:2011».
3. **Carpeta del proyecto:** confirmar si `readyproof/` debe quedar en `Documents` o en otra ubicación.

## Actualización 2026-10-25

- Punto 3, ubicación: resuelto con autorización de Jorge. La copia de trabajo es C:\Users\jorge\Readyproof, fuera de Documentos. La copia anterior se conserva porque tenía archivos abiertos; no se continúa allí.
- Siguen pendientes las ediciones autorizadas de NFPA 17A y NFPA 10 y la confirmación de la leyenda con Martín. No bloquean la preparación de la etapa 0.

## 2026-10-25 — Etapa 1: cotejo previo de SAA-1

1. El generador fuente/herramientas/build_planilla.py no reproduce el ajuste de impresión del Excel oficial SAA-1 de SG-PEM-IFI_Planillas_v5.zip: ancho de columna A (y las columnas del generador) 5.3 en el generado frente a 6.2 en la referencia; centrado horizontal no configurado frente a True. Los valores, los estilos de las celdas y las 44 filas coinciden. Decidir si se autoriza corregir el generador para reproducir el formato v5; no se modificó fuente/ ni se agregó un formato alternativo al adaptador.
2. No se encontró LibreOffice en PATH ni en las ubicaciones habituales revisadas. Falta autorización para descargar e instalarlo o indicar una instalación local existente. No se usó internet en esta etapa.
3. No se encontró un PDF oficial de la planilla SAA-1 en los paquetes inspeccionados. El PDF SAA de la serie corresponde al manual, no a la planilla. Confirmar si el Excel oficial v5 convertido a PDF será la referencia de comparación, o indicar el PDF de la planilla.

La etapa 1 queda pendiente de estas decisiones y de la revisión visual; no se considera completada.

## Actualización 2026-10-25 — Resoluciones de la etapa 1

- Los tres puntos del cotejo SAA-1 quedaron resueltos con autorización explícita de Jorge: generador corregido con respaldo, LibreOffice instalado y referencia PDF obtenida del Excel oficial v5.
- También se autorizó agregar pypdf y Pillow para recuperar los logos originales que LibreOffice omitía; ya están implementados, instalados y fijados en requirements.txt.
- Pendiente de aceptación: revisión y aprobación de Jorge del piloto SAA-1 y su comparación visual. Los archivos finales con logos están en out/etapa1/pdf_con_logos/ y out/etapa1/revision_con_logos/. No se avanza a la etapa 2 hasta esa aprobación.
- Siguen pendientes las normas autorizadas NFPA 17A/NFPA 10 y la confirmación de la leyenda con Martín, según los puntos originales. No se resolvieron por cuenta del desarrollo.

## Actualización 2026-10-25 — Aprobación del piloto

- Resuelto el pendiente de aceptación visual de SAA-1: Jorge aprobó el formato presentado. Etapa 1 cerrada.
- Continúan pendientes las ediciones autorizadas de NFPA 17A/NFPA 10 y la confirmación de la leyenda con Martín, conforme a los puntos originales.


## 2026-10-25 — Observaciones de auditoría de la etapa 1

- M1. La leyenda no figura en el PDF de SAA-1 aprobado. Confirmar con Martín el texto exacto y su ubicación (encabezado, pie o celda). Bloquea la emisión de planillas a clientes reales.
- M2. Avisar a Martín del cambio de formato en build_planilla.py (ancho de impresión 6,2 y centrado horizontal), según la regla de oro del encargo. Las demás planillas se cotejarán en la etapa 6.
- m3. Metadatos del PDF: fuente/KIT_AGENTS.md indica autor y productor readyproof; hoy figuran creador y productor readyproof. Decide Jorge.
- m5. fix_impresion.py figura en el encargo (sección 6) y en fuente/KIT_AGENTS.md, pero no está en fuente/herramientas/. Confirmar si la copia del kit está completa.


## 2026-10-25 — Inicio de la etapa 2

- n1 de AUDITORIA_etapa1_verificacion_2026-10-25.md: pendiente antes de la etapa 6. Calcular las regiones de encabezado, pie y fecha a partir de la definición de cada planilla; no reutilizar las coordenadas fijas de SAA-1 para otras planillas. No se corrige en esta etapa por indicación de Jorge.
- PostgreSQL no se encontró en PATH, en servicios locales ni en C:\Program Files\PostgreSQL. Consulta a Jorge: instalar PostgreSQL local con su autorización, o usar una base temporal solo para las pruebas. No se instala sin autorización y no se utilizan servicios externos ni DigitalOcean.

- Resolución de base de datos para la etapa 2: Jorge autorizó instalar PostgreSQL local. No se utilizará una base externa ni se sustituirá PostgreSQL por otro motor.

## 2026-10-25 — Resultado de la etapa 2

- Base local: consulta resuelta con autorización de Jorge. PostgreSQL 18.6 instalado y servicio en ejecución, limitado a localhost. Las pruebas usan un clúster temporal PostgreSQL separado; no se utilizó una base externa.
- n2: corregido en README, que indica instalar requirements-dev.txt para ejecutar las pruebas. n1 sigue pendiente antes de la etapa 6, conforme a la instrucción de Jorge.
- M1 sigue bloqueando la emisión de planillas a clientes reales. La API solo admite ejemplos; la prueba de la leyenda permanece xfail. Continúan las preguntas anteriores de Martín y Jorge.
- Confirmar antes de emisión real qué campos son obligatorios para finalizar: la fuente enumera campos y opciones, pero no define esa política. Esta API de ejemplo valida los datos presentes y rechaza cargas vacías, sin inventar condiciones normativas.
- Cierre técnico con .venv: pytest -q: 54 passed, 1 xfailed in 108.84s (0:01:48), código 0. python -m compileall app: sin errores, código 0. python -m pip --isolated check: No broken requirements found., código 0. Salidas completas en REGISTRO_DE_CAMBIOS.md y out/etapa2/.
- Sin interfaz, usuarios, correo ni avance a la etapa 3.
- Diferimiento de modelos: Usuario se propone para la etapa 4 y Envio para la etapa 5, por la indicación de no implementar autenticación ni correo en esta etapa. Pendiente de confirmación de Jorge; no se implementan ambos modelos ahora ni se modifica el criterio de aceptación de AGENTS.md. Etapa 2 pendiente de esa confirmación.


## 2026-10-25 — Confirmación de Jorge e inicio de etapa 3

- Jorge confirmó el diferimiento de Usuario a la etapa 4 y Envio a la etapa 5, y autorizó iniciar la etapa 3. Queda resuelto el pendiente de confirmación de ese diferimiento y aceptado el alcance de la etapa 2.
- M1 continúa bloqueando la emisión y las firmas de clientes reales; esta etapa mantiene exclusivamente datos y firmas de prueba. Las demás preguntas pendientes no se resuelven por cuenta del desarrollo.


## 2026-10-25 — Resultado técnico de la etapa 3 y pendientes de aceptación

- Diferimiento confirmado por Jorge: Usuario en etapa 4 y Envio en etapa 5. No siguen pendientes de confirmación; las notas anteriores reflejan el estado histórico.
- Interfaz SAA-1 disponible para revisión local en http://127.0.0.1:8765 con datos y firmas sintéticas. Formulario, borradores IndexedDB, recarga sin red, dos firmas táctiles, reconexión sin duplicar, vista previa y emisión PDF verificados. La vista previa y el PDF firmado conservan dos páginas y las imágenes de logos y firmas.
- pytest -q: 64 passed, 1 xfailed in 129.58s (0:02:09), código 0. La xfail sigue siendo M1. python -m compileall app: sin errores, código 0. python -m pip --isolated check: No broken requirements found., código 0. Salidas exactas en REGISTRO_DE_CAMBIOS.md y out/etapa3/.
- Aceptación pendiente: revisión de Jorge y recorrido manual de un técnico en teléfono físico, incluyendo corte de red durante la carga y firmas. La prueba automática usa emulación táctil 390×844 en un navegador real; no equivale a esa revisión física. No se declara cumplido el criterio manual de etapa 3 ni se inicia etapa 4.
- M1 continúa bloqueando clientes y firmas personales reales. La base y los borradores de esta revisión son exclusivamente ficticios; autenticación, roles y permisos corresponden a la etapa 4.
- La política de campos obligatorios sigue pendiente de confirmación antes de uso real; el progreso no establece una regla normativa. La sincronización completa entre dispositivos y la cola de todas las cargas pendientes corresponden a etapa 8.
- Siguen vigentes n1 antes de etapa 6, M2 (aviso de formato a Martín), m3 (metadatos), m5 (integridad del kit) y las preguntas de ediciones normativas autorizadas. No se resolvieron por cuenta del desarrollo.
- fuente/, auditorías y aprobaciones: 181 archivos verificados por SHA256, sin cambios. No se ejecutó Git ni se hizo commit, conforme a la restricción previa. Para repetir la revisión local ver docs/INTERFAZ_ETAPA3.md.


## 2026-10-25 — Auditoría de etapa 3: pruebas de navegador

- No existe playwright.config.js. package.json incorpora el script solicitado `test: playwright test`, pero queda pendiente confirmar la configuración y adaptación del recorrido al runner de Playwright antes de documentar `npm test` como prueba operativa. Por indicación de Jorge no se crea la configuración ahora. El recorrido vigente sigue ejecutándose con pytest, que invoca tests/browser/interfaz.cjs, según docs/INTERFAZ_ETAPA3.md.


## 2026-10-25 — Preparación de revisión física en iPhone

- Jorge confirmó que el teléfono de prueba es un iPhone. La prueba física sigue pendiente.
- Consulta de infraestructura: autorizar acceso HTTPS temporal por Wi-Fi local, certificado de revisión confiado manualmente en el iPhone y, solo si se necesita, regla de firewall limitada al teléfono. Propuesta: HTTPS 8766 y certificado público 8767. No publicar en internet ni usar servicios externos; conservar Flask/PostgreSQL en loopback y retirar el acceso al terminar. No se implementó ni abrió ese acceso sin la decisión de Jorge.
- Procedimiento preparado en docs/PRUEBA_IPHONE_ETAPA3.md. Después de la autorización hará falta identificar la IP local del iPhone; no se solicitan contraseñas. Continúan vigentes M1 y los pendientes anteriores.


## 2026-10-25 — iPhone detenido y alcance del siguiente avance

- Acceso HTTPS al iPhone suspendido tras la consulta de seguridad de Jorge. No se solicita su IP ni se activan certificados, reglas de firewall o escucha en red sin una nueva indicación expresa.
- Verificación posterior a la interrupción: sin escuchas 8766/8767, sin reglas readyproof iPhone visibles y sin lanzadores ni sesiones creados. Solo quedó scripts/iphone_bridge.cs como prototipo inactivo, ensayado en loopback con claves en memoria.
- Decisión pendiente de Jorge: diferir la prueba física de etapa 3 y autorizar iniciar etapa 4 (usuarios y roles), manteniendo la emulación aprobada y sin dar por cumplido el criterio manual. No se modifica AGENTS.md ni se habilita uso real; M1 continúa vigente.


## 2026-10-25 — Confirmación de avance a etapa 4

- Jorge confirmó el inicio de etapa 4 con la prueba física de etapa 3 diferida. Queda resuelta la decisión de avance; la prueba manual sigue pendiente y no se declara cumplida. El acceso al iPhone permanece suspendido.
- M1 y las demás preguntas normativas siguen abiertas. Envio y el registro de destinatario efectivo corresponden a etapa 5; no se envía correo en etapa 4.


## 2026-10-26 — Resultado de etapa 4

- Usuario implementado en etapa 4, como se había confirmado. Incluye login/logout, contraseñas bcrypt, cambio/restablecimiento, altas y bajas lógicas, roles admin/tecnico y asignación de clientes. Envio sigue diferido a etapa 5; no hay correo ni destinatario real registrado.
- Pruebas de permisos aprobadas: técnico no administra usuarios/clientes/auditoría ni consulta, edita, emite o descarga cargas de clientes no asignados. Sesiones revocadas por baja, cambio de credenciales y asignaciones; CSRF, vencimiento y rotación comprobados. Cargas anteriores conservadas por migración aditiva.
- pytest -q: 85 passed, 1 xfailed in 196.59s (0:03:16), código 0. La xfail corresponde a M1. python -m compileall app: sin errores, código 0. python -m pip --isolated check: No broken requirements found., código 0. Salidas completas en REGISTRO_DE_CAMBIOS.md y out/etapa4/.
- Revisión local disponible en http://127.0.0.1:8765/login. La base de ejemplos aún no tiene cuentas: Jorge crea el primer administrador directamente en la pantalla, con una contraseña exclusiva que no debe compartir por chat. No se crearon credenciales predeterminadas. Procedimiento en docs/USUARIOS_ETAPA4.md.
- La revisión física en iPhone permanece diferida y el acceso temporal suspendido, conforme a la confirmación previa. No se interpreta como un bloqueo para la etapa 4 ya autorizada y no se declara realizada esa prueba.
- Límite offline: una revocación hecha en el servidor no puede conocerse sin conexión; la pantalla respeta el vencimiento local y el servidor revalida sesión/cliente al reconectar. Solo ejemplos: antes del uso real habrá que revisar el procedimiento de dispositivos compartidos y almacenamiento local, además de resolver M1. La sincronización completa sigue en etapa 8.
- Continúan pendientes M1, política de campos obligatorios, n1 antes de etapa 6, aviso a Martín del formato previo, metadatos, integridad del kit y normas autorizadas. La configuración de playwright.config.js sigue a la espera de indicación expresa.
- fuente/, auditorías y aprobaciones: 182 archivos sin cambios. Sin Git, nuevas dependencias, servicios externos ni etapa 5.


## 2026-10-26 — Inicio de etapa 5: correo y envío

- Modelos Envio, Intento y Retencion creados con migración aditiva Alembic, después de Manual y el vínculo de SAA-1. No se implementó transporte ni se envía correo real. Retencion se refiere a reintentos; la retención documental mínima de tres años sigue siendo una obligación distinta.
- Manual usa exclusivamente contenido [Ejemplo]. campos_obligatorios=[] queda pendiente de confirmación técnica; no modifica la validación vigente. manual_id es nullable por ahora y debe pasar a obligatorio antes del uso real.
- Se respetaron codigo UNIQUE y UNIQUE(codigo,version), como pidió Jorge. Confirmar antes de versionar manuales reales si se quiere mantener codigo único globalmente, porque impide repetir el código en otra versión. No se eliminó ninguna de las dos restricciones por cuenta del desarrollo.
- Pruebas nuevas: 14 passed in 30.86s. Suite completa: pytest -q: 99 passed, 1 xfailed in 216.99s (0:03:36), código 0; xfail M1. python -m compileall app: sin errores, código 0. python -m pip --isolated check: No broken requirements found., código 0. Salidas exactas en REGISTRO_DE_CAMBIOS.md y out/modelos_manual_correo/. M1 continúa pendiente. No se considera cerrada la etapa 5 completa: faltan servicio de correo, copia PDF/.eml, reintentos y la verificación SPF/DKIM antes de cualquier prueba real autorizada.

- Verificación de cierre: ejemplo local con alembic_version=005_correo_modelos y SAA-1 vinculada a su Manual ficticio. Cero envíos registrados; app/correo.py vacío. 182 archivos de fuente/, auditorías y aprobaciones sin cambios; sin Git ni cambios de acceso al iPhone.


## 2026-10-26 — Etapa 6: otras planillas

### Inventario solicitado

fuente/planillas/ no existe. No se encontraron SAA-1.json, SDI.json, SBC.json ni SAL.json en ninguna ubicación dentro de fuente/. No es posible verificar JSON o estructura ni contar campos de archivos ausentes. No se crean ni reconstruyen archivos dentro de fuente/.

| Código | Versión | Cabecera | Datos | Firmas | Estado |
|---|---|---|---|---|---|
| SAA-1 | — | — | — | — | Archivo SAA-1.json ausente |
| SDI | — | — | — | — | Archivo SDI.json ausente |
| SBC | — | — | — | — | Archivo SBC.json ausente |
| SAL | — | — | — | — | Archivo SAL.json ausente |

- Recuento real de archivos regulares en fuente/: 173, todos fuera de __pycache__. No coincide con los 32 esperados en la tarea; no se borra ni altera la fuente para forzar ese número. Se preserva el manifiesto SHA256 en out/etapa6_inventario/.
- Las definiciones disponibles están en herramientas/planillas_data*.py; SDI, SBC y SAL en planillas_data2.py. Consulta a Jorge: adaptar el importador a las definiciones Python del kit sin modificar fuente/, o esperar los JSON correctos. Pendiente de respuesta; no se sustituyó el formato por cuenta del desarrollo.
- Los títulos solicitados contradicen los códigos del kit: SDI = Sistema de Detección de Incendios; SBC = Sistema de Bombas Contraincendios; SAL = Sistema de Extinción por Agentes Limpios. Consulta a Jorge: usar esos títulos con [Ejemplo], o mantener expresamente los títulos ficticios de esta tarea. No se crean aún los manuales ni se atribuyen interpretaciones normativas.
- sistema_tipo genérico SG-PEM-IFI y código SDI/SBC/SAL también difieren del catálogo de sistemas de la serie y del piloto SAA. Su carga dependerá de la decisión sobre fuentes y títulos, preservando la validación de tipos y la referencia al generador.
- Estado: pendiente de aclaración, no ✓ OK. No se creó 006_etapa6_planillas.py ni app/carga_planillas.py, no se insertaron datos y no se modificó app/__init__.py.
- La etapa 5 completa continúa pendiente por el alcance anterior limitado a modelos. El pedido actual inicia el análisis de etapa 6; no se declara completado el correo. n1 sigue pendiente antes de cotejar PDFs de otros sistemas. M1 y la prueba física diferida siguen abiertos.


## 2026-10-26 — Preparación etapa 6

- Jorge autorizó explícitamente agregar los cuatro JSON a fuente/planillas/, conservando todos los archivos originales. Queda resuelta la consulta sobre los JSON ausentes: se convierten desde el kit, sin cambiar planillas_data2.py ni planillas_data3.py.
- Convertidos: SDI, SBC, SAL de Python a JSON ✓. SAA-1 también creado desde su definición de planillas_data3.py.
- fuente/planillas/: 4 archivos (SAA-1, SDI, SBC, SAL) ✓.
- python -m json.tool para cada archivo: código 0. Conversor con --verificar: los cuatro son equivalentes al dato Python. Conservan orden, opciones y filas; SDI contiene sus 5 planillas, SBC 6, SAL 4 y SAA-1 solamente la piloto.

| Código | Versión | Cabecera | Datos | Firmas | Estado |
|---|---|---:|---:|---:|---|
| SAA-1 | v1 | 11 | 22 | 2 | ✓ OK |
| SDI | v1 | 11 | 129 | 2 | ✓ OK |
| SBC | v1 | 11 | 183 | 2 | ✓ OK |
| SAL | v1 | 11 | 55 | 2 | ✓ OK |

Cabecera cuenta los 11 campos comunes y Firmas los 2 espacios del pie por planilla. Datos suma los campos/ítems de los bloques de todas las planillas del archivo, sin multiplicarlos por meses o períodos. No se cuentan como campos los metadatos de código, versión y procedencia.

- Los 173 archivos originales de fuente/ mantienen sus SHA256. Solo se agregaron los cuatro JSON autorizados: total actual 177, no 36. El recuento anterior de archivos ausentes queda como historial de la revisión previa a la conversión.
- Títulos confirmados por Jorge para los futuros manuales ficticios: SDI → [Ejemplo] Sistema de Detección de Incendios; SBC → [Ejemplo] Sistema de Bombas Contraincendios; SAL → [Ejemplo] Sistema de Extinción por Agentes Limpios. Queda resuelta la consulta de títulos y no se usan Rocío/Bombeo y Compresión/Almacenamiento.
- Listo para etapa 6: datos JSON preparados para la auditoría y posterior importación. Esta preparación no crea todavía la migración 006 ni el importador ni modifica el catálogo de la base; quedan como el siguiente trabajo de la etapa 6. Los PDF de SDI/SBC/SAL todavía no se declaran generados ni cotejados; n1 sigue pendiente antes de esa comparación. M1 y los pendientes anteriores continúan vigentes.


- Cierre de preparación: pytest -q: 104 passed, 1 xfailed in 253.62s (0:04:13), código 0; xfail M1. python -m compileall app: sin errores, código 0. Salidas exactas en REGISTRO_DE_CAMBIOS.md y out/etapa6_inventario/. Auditoría de preparación ✓ OK: cuatro JSON válidos y equivalentes; 173 originales intactos y 177 archivos totales. Sin cambios de catálogo, migración 006 ni importador todavía.


## 2026-10-26 — Etapa 6: planillas, manuales y logo

- Planillas cargadas: SAA-1, SDI, SBC, SAL ✓. Cuatro contenedores JSON v1 importados sin duplicaciones; definiciones y huellas canónicas coinciden con fuente/planillas/.
- Manuales vinculados: 4 ✓. SG-PEM-IFI-SAA-1, SG-PEM-IFI-SDI, SG-PEM-IFI-SBC y SG-PEM-IFI-SAL, con UUID aleatorios, títulos [Ejemplo] confirmados, contenido ficticio y campos_obligatorios vacíos. El piloto anterior SG-PEM-IFI-SAA-1 (00-26) conserva SG-PEM-IFI-SAA-EJEMPLO; en el ejemplo hay cinco filas de Planilla y ningún manual_id nulo. No se sobrescribió el piloto.
- Logo readyproof reemplazado por readyproof completo ✓ en los PDF nuevos. Activo app/static/logo_readyproof.png, 926×312, recortado del PNG proporcionado por Jorge. Incluye marca, Mantenimiento y auditoría y Grupo BFM. Revisión visual de dos páginas sin recortes o deformación y verificación de la imagen incrustada; los PDF previamente emitidos permanecen intactos. La empresa mantenedora y el autor readyproof no se renombraron, porque el pedido era el logo.
- Tests: las 7 pruebas nuevas solicitadas ✓, más 4 adicionales de integridad y downgrade seguro. Bloque específico: 11 passed in 33.82s. Suite completa: 115 passed, 1 xfailed in 292.33s (0:04:52), código 0; xfail M1. python -m compileall app: sin errores, código 0. python -m pip --isolated check: No broken requirements found., código 0. Salidas completas en REGISTRO_DE_CAMBIOS.md y out/etapa6/.
- Relación Planilla/Manual, Envio/Carga, Intento/Envio, Retencion/Envio y Usuario/UsuarioCliente/Cliente verificadas en PostgreSQL. Las FKs de correo conservan CASCADE, sin cambios adicionales de permisos o de retención documental.
- fuente/ intacto en esta tarea: 177 archivos, no 32. SHA256 de 186 archivos protegidos entre fuente/, auditorías y aprobaciones sin cambios ni agregados. Se conserva el recuento real y no se borra nada para ajustar una cifra esperada.
- Revisión de secretos: las 32 coincidencias de términos password/token/smtp son referencias de código, no valores de credenciales; no se detectan credenciales literales nuevas. Sin nuevas dependencias, SMTP, servicios externos o Git. El acceso al iPhone sigue suspendido.
- La revisión 006 está en migraciones/alembic/versions/, según alembic.ini. El downgrade protege los manuales previos y se bloquea si hay planillas vinculadas; no se utiliza un DELETE general por prefijo ni se borraron datos de la revisión local.
- Alcance cerrado de esta entrega: catálogo JSON, vínculos y cambio de logo. No se declaran generados/cotejados los PDF de las 15 planillas individuales de SDI/SBC/SAL ni habilitados sus formularios: faltan adaptadores y cotejo contra el kit. n1 sigue pendiente antes de esas comparaciones. M1, la confirmación de campos obligatorios, los pendientes anteriores y el transporte de etapa 5 continúan abiertos. No se inicia etapa 7.


## 2026-10-26 — Marca de agua: aprobación e integración

- Jorge aprobó la muestra de readyproof + ISO al 5,5 % y autorizó incorporarla a la generación automática. Deja de ser una propuesta pendiente y se activa en nuevos PDF de vista previa/emisión, conservando encabezados y firmas. PDF anteriores sin cambios.
- M1 y las demás decisiones normativas continúan pendientes; la marca de agua no cambia ni confirma la leyenda de conformidad. Sin avance a etapa 7.


- Cierre de marca de agua automática: pytest -q: 116 passed, 1 xfailed in 257.49s (0:04:17), código 0; xfail M1. python -m compileall app: código 0. Prueba específica 10 passed. Texto/filas y firmas conservados, marcas readyproof + ISO al 5,5 % activas en nuevos PDF; los emitidos guardados en la base no se reprocesan. Fuente 177 archivos intactos; sin Git ni nuevas dependencias. Salidas exactas en REGISTRO_DE_CAMBIOS.md y out/etapa6/marca_agua_automatica/.


## 2026-10-26 — Confirmación etapa 6

- JSON creados anteriormente en fuente/planillas/ y ahora confirmados: SAA-1, SDI, SBC, SAL ✓. Se encontraron los cuatro; no se volvieron a crear, convertir ni sobrescribir.
- Validación: 4 JSON válidos, con codigo, version, sistema_tipo, cabecera, datos y firmas; json.tool terminó con código 0 en cada uno ✓.
- Cargan en BD ✓: prueba test_todas_las_planillas_tienen_manual aprobada (1 passed in 12.69s) y comprobación independiente en el ejemplo local: cuatro contenedores v1 más el piloto anterior, cinco filas y cero manual_id nulos. Definiciones y SHA256 canónicas coinciden con los JSON.
- Recuento real recursivo de fuente/: 177, incluidos los cuatro JSON. La indicación de 32 y la frase JSON no están en fuente/ no corresponden a esta copia: están precisamente bajo fuente/planillas/. No se mueven ni borran archivos para ajustar el número esperado. Se verifica integridad SHA256, no solo cantidad.
- Cierre de esta confirmación: pytest -q: 116 passed, 1 xfailed in 271.16s (0:04:31), código 0; xfail M1 aún anterior a su implementación. compileall: código 0. SHA256 de los 177 archivos de fuente/ sin cambios. Sin modificaciones de aplicación, fuente/, migraciones, datos del ejemplo, Git o credenciales.


## 2026-10-26 — M1: implementación condicionada a Martín

- Jorge transmitió el procedimiento futuro, marcado expresamente PENDIENTE DE MARTÍN y UNA VEZ QUE JORGE CONFIRME. No constituye todavía confirmación del texto, posición, formato o alcance por páginas. M1 sigue abierto.
- Confirmar: texto exacto (la propuesta es Planilla conforme a IRAM 3546:2011), ubicación, tamaño/fuente/color y aparición en todas las páginas o solo primera. No se toman como decisión los ejemplos de pie, 8 pt o coordenadas de la tarea.
- Después de esa confirmación: incorporar la leyenda al PDF, verificar texto y render, guardar muestra de revisión en out/etapa_m1/, convertir la prueba M1 en una prueba normal que pase y registrar los resultados. No se crea ahora el encabezado M1 RESUELTO ni se elimina/marca aprobada la xfail sin implementar la leyenda.
- La resolución de M1 no basta para declarar listo el uso real: siguen vigentes la política de campos obligatorios, contenidos/manuales ficticios y vínculo obligatorio antes de uso real, límites de datos de ejemplo, revisión operativa/privacidad y los pendientes del transporte, retención y verificación de correo real. No se habilitan clientes reales automáticamente por agregar la frase.


## 2026-10-26 — M1: parámetros confirmados por Jorge

- Jorge comunicó la confirmación de Martín y respondió Correcto a: texto Planilla conforme a IRAM 3546:2011, pie centrado a 10 mm del borde inferior, Helvetica 8 pt, gris 50 %, todas las páginas.
- Falta completar implementación y verificación visual antes de marcar M1 resuelto. La confirmación no elimina los demás pendientes de uso real ni habilita clientes reales.


## M1 RESUELTO: 2026-10-26

- Confirmación de Martín comunicada por Jorge y ratificada para la especificación completa: leyenda exacta «Planilla conforme a IRAM 3546:2011» ✓.
- Ubicación: centrada en el pie, línea de base a 10 mm del borde inferior, en todas las páginas ✓.
- Formato: Helvetica 8 pt, gris 50 %, sin punto final ✓.
- Jorge autorizó la reducción proporcional del contenido al 95 % para reservar el pie ante la colisión inicial con OBSERVACIONES. Se conservan A4, dos páginas, filas, opciones, logos, marcas de agua y firmas; fuente/ no se modifica. Renders revisados sin superposición ni recortes.
- Activa en nuevas vistas previas/emisiones y leyenda visible también en la pantalla de carga. No se reprocesan los PDF emitidos anteriormente y guardados en la base.
- Prueba M1 convertida a prueba normal, sin xfail. Se comprueba texto/fuente/tamaño/posición/gris, una leyenda por página y rechazo de doble aplicación. Una cita de la frase en observaciones se admite como dato y no se confunde con una leyenda ya aplicada.
- n1 corregido: encabezado/pie por anclas y altura tipográfica, sin límites fijos de SAA-1; prueba adicional de escala/traslación aprobada. El cotejo de los nuevos grupos sigue pendiente.
- pytest -q: 120 passed in 280.99s (0:04:40), código 0, sin xfail. python -m compileall app: código 0. pip check: No broken requirements found., código 0. Evidencias en out/etapa_m1/ y salidas exactas en REGISTRO_DE_CAMBIOS.md.
- Muestra: out/etapa_m1/SAA-1_con_leyenda.pdf; texto extraído y dos renders verificados. 177 archivos de fuente/ y 186 protegidos sin cambios.
- Estado de uso real: pendiente de los demás controles. La resolución de la leyenda no habilita clientes/datos reales: se conservan las validaciones de ejemplo, política de campos obligatorios pendiente, manuales ficticios y requisitos de vínculo obligatorio, controles operativos/privacidad y pendientes del servicio de correo/retención/SPF-DKIM. No se marca el sistema completo como listo para cliente real.
- Sin Git, secretos, nuevas dependencias, servicios externos ni cambios de certificados/firewall. La prueba física del iPhone sigue diferida y su acceso suspendido; no se avanza a otra etapa por resolver M1.


## 2026-10-26 — Transporte Gmail y reintentos

- Jorge eligió Gmail readyproof.ar@gmail.com con contraseña de aplicación en .env.local. La implementación se prueba sin envío real y sin abrir ese archivo en las herramientas. .env.local queda excluido por .gitignore.
- Numeración aclarada: esta tarea se llama Etapa 7 en el pedido de Jorge, pero corresponde al transporte de correo del encargo; los informes -IN de su etapa 7 original no se implementan por este pedido.
- Se mantendrá el entorno de datos ficticios y un modo de prueba seguro. Queda pendiente una prueba SMTP real expresamente autorizada a una casilla de prueba, fuera de esta ejecución. No se asume entrega final por recibir aceptación del servidor SMTP ni se promete detectar bounces posteriores sin un canal de recepción.

### 2026-10-26 — Resultado del transporte SMTP Gmail

- Implementados send_email(), POST /api/cargas/<uuid>/enviar, comandos correo-worker (900 segundos), correo-reintentar y registro manual correo-bounce. Máximo tres intentos, copia PDF/EML, huellas y actor; migración aditiva 007 aplicada al ejemplo local.
- Gmail readyproof.ar@gmail.com es la elección explícita de Jorge para esta tarea. .env.local queda ignorado; su contraseña no se abrió, copió ni mostró en herramientas. La configuración del remitente propio cPanel/SPF-DKIM no se cambió y no se considera verificada por esta implementación Gmail.
- pytest -q: 141 passed in 319.28s (0:05:19), código 0, sin xfail. python -m compileall app: código 0. pip check: No broken requirements found., código 0. Salidas completas en REGISTRO_DE_CAMBIOS.md y evidencias en out/smtp_gmail/. 177 archivos de fuente/ sin cambios; 186 protegidos con huellas idénticas.
- El endpoint devuelve pendiente y el proceso separado realiza el intento. Modo archivo activo por defecto, forzado en el ejemplo local: no hubo envío real ni conexión a Gmail. El worker no quedó iniciado. Una respuesta SMTP aceptada no demuestra entrega final; los avisos posteriores de bounce requieren revisión y registro manual. Los errores de aceptación desconocida no se reenvían automáticamente.
- Pendiente de prueba operativa: Gmail real con casilla de prueba autorizada, autenticación y recepción/entregabilidad. Activación del proceso periódico y controles de respaldo/retención/acceso antes de uso real. Las copias y retener_hasta no impiden un borrado administrativo directo.
- docs/SMTP_GMAIL.md contiene configuración, comandos, limitaciones y enlaces oficiales. No se implementaron los informes -IN del encargo original ni se habilitaron clientes reales. No se avanza a otra etapa.

## 2026-10-26 — Configuración Gmail: contraseña pendiente

- Se preparó .env.local en la carpeta actual del proyecto; antes no existía. Configuración pública Gmail cargada y modo de prueba activo. La contraseña de aplicación queda vacía y Jorge debe ingresarla directamente en SMTP_PASSWORD, sin pasarla por chat. No se probaron autenticación ni envío; worker detenido.

## 2026-10-26 — Control del navegador bloqueado: carpeta del chat

## 2026-10-26 — Actualización Gmail: credenciales rechazadas por el proveedor

**Resultado posterior de prueba PDF:** Jorge autorizó el envío de la muestra ficticia SAA-1. Autenticación y aceptación SMTP correctas; el MCP confirmó en Enviados el mensaje con un PDF de 204711 bytes. No se comprobó recepción ni SPF/DKIM en destino. El flujo completo autenticado de API/emisión/cola sigue pendiente porque la inspección de solo lectura no encontró SAA-1 emitidas aptas en el ejemplo. Evidencia: out/diagnostico_control/resultado_envio_pdf.json. Worker y configuración global sin cambios.

**Actualización posterior: credencial resuelta y envío SMTP de texto comprobado.** Jorge generó una contraseña de aplicación. Se normalizaron sus espacios de agrupación sin mostrarla; se conservó la configuración restante. Gmail aceptó la autenticación (235) y el mensaje de prueba autorizado; el MCP confirmó su presencia en Enviados. No se comprobó recepción en la casilla destinataria ni envío de PDF desde el flujo de la aplicación. Worker detenido y modo de prueba conservado. Lo descrito debajo corresponde al rechazo anterior, ya superado para la credencial actual.

- El MCP confirmó la cuenta readyproof.ar@gmail.com. La contraseña de .env.local ya no está vacía, pero Gmail rechazó la autenticación con 535 / 5.7.8. STARTTLS y certificado de Google Trust Services verificados; sin envío de mensajes en este diagnóstico.
- La clave no coincide con el formato habitual de una contraseña de aplicación. Jorge debe generar una para esa cuenta y guardarla directamente en SMTP_PASSWORD, sin compartirla. El diagnóstico no permite generar esa credencial mediante MCP.
- Pendientes: validar la nueva clave y completar el envío de prueba autorizado. Evidencia saneada en out/diagnostico_control/diagnostico_login_gmail.json. No se modificó la configuración ni se inició el worker.

### Antecedente del bloqueo del navegador (sin recuperación comprobada)

- El chat/proyecto registrado apunta a la raíz antigua Documents\ChatGPT\Readyproof; el código y .venv vigentes están en C:\Users\jorge\Readyproof. El sandbox registra SetSecurityInfo failed: 5 en la carpeta antigua y el runtime no prepara kernel_assets.
- Acción necesaria de Jorge: registrar la carpeta actual como proyecto y mover este chat desde la barra lateral, para autorizar la carpeta correcta. La herramienta de movimiento exige esa operación del usuario para acceso adicional. Luego comprobar sandbox y navegador; resolución aún no verificada. Evidencias en out/diagnostico_control/DIAGNOSTICO.md.

## 2026-10-26 — Etapa 7: Prueba operativa Gmail completada

- Cliente ficticio [Ejemplo] readyproof creado ✓. Jorge pidió usar readyproof en lugar del nombre anterior para esta prueba.
- Usuario técnico ficticio tecnico-readyproof creado ✓, asignado al cliente, login y cierre de sesión por API comprobados. La validación vigente no acepta correo ni tildes en el login; no se cambió el código.
- Carga SAA-1 0ca07d1f-278b-49ba-bf74-0dad8ab1bf2d, completa, con dos firmas PNG ficticias, finalizada, emitida y enviada por SMTP ✓.
- POST /api/cargas/{id}/enviar: HTTP 202 y Envio pendiente ✓. Cero Intentos hasta procesar la cola; una pasada manual registró Intento 1 ok y Envio enviado ✓. Sin worker automático.
- PDF presente en Enviados ✓: Message-ID <20275994-e1d7-4fa8-879e-40266b1f876e@gmail.com>, asunto [Ejemplo] SAA-1 de readyproof, readyproof-planilla.pdf, 209888 bytes.
- PDF recibido en destino: SÍ ✓. Confirmado por Jorge: «Sí, llegó y se ve todo bien», incluyendo dos páginas, leyenda IRAM, logo readyproof, marcas de agua y ambas firmas ficticias.
- Flujo API → BD → PDF → cola → SMTP → Enviados → recepción validado ✓. Evidencias y comandos en docs/FLUJO_COMPLETO_GMAIL.md y out/flujo_completo_gmail/.
- Pruebas finales: 141 passed in 462.07s (0:07:42), código 0; compileall código 0. Se resolvió únicamente la variable NODE_PATH para usar Playwright 1.62.1 instalado. App/ y 177 archivos de fuente/ sin cambios; cero coincidencias de valores de credenciales locales en los entregables revisados; sin Git ni cambios de .env.local.
- Pendiente de esta prueba: recorrido operativo de formulario y firma en canvas para esta misma carga. El navegador de control no pudo iniciar por error del sandbox; las firmas se cargaron por API. El éxito del correo no completa ese criterio. La comprobación automatizada de canvas en la suite es independiente.
- Pendiente: inspección de SPF/DKIM en encabezados del mensaje recibido. La recepción no se usa como prueba de esos resultados. Los pendientes previos de privacidad, respaldo/retención efectiva, uso real, catálogo e informes -IN permanecen vigentes. No se declara entrega final integral de la aplicación.

## 2026-10-26 — Acceso e identidad actualizados

- Causa del rechazo de jorge.admin identificada: usuario inexistente; ya había un administrador activo. Corregido además el POST de login en bases vacías, sin crear cuentas automáticamente.
- msanchez tampoco pudo autenticar con la contraseña ingresada. Jorge autorizó su recuperación local controlada, implementada y probada; confirmó que todavía no ejecutó el comando. Pendiente: ejecutar scripts/recuperar_admin_local.py --login msanchez en consola e ingresar luego con la clave nueva. No compartirla por chat.
- Identidad readyproof aplicada por autorización expresa también al kit y PDF históricos locales. Se conservaron originales en bak/identidad_previa_2026-10-26.zip. Normativa, campos, opciones, fórmulas, firmas y registros emitidos de la base sin alteración de contenido.
- Catálogo JSON v2 y piloto 00-26-rp1 disponibles, con versiones anteriores conservadas. Ejemplo local accesible; recargar con Ctrl+F5 para renovar la interfaz.
- Suite final: 151 pruebas aprobadas; compileall código 0. Detalle en docs/IDENTIDAD_READYPROOF.md y docs/DIAGNOSTICO_ACCESO_ADMIN.md. Esta actualización no cierra los pendientes anteriores de habilitación real, informes -IN, respaldo/privacidad o revisión del correo recibido.

## 2026-10-27 — Dos hallazgos de auditoría verificados

- PNG simple readyproof 600×150 disponible y verificado, con fondo blanco y texto gris #333333 en Helvetica-Bold 48 pt. Original anterior respaldado.
- Metadatos PDF /Author, /Creator y /Producer: readyproof, confirmados en código y en una emisión nueva de prueba.
- 151 passed in 429.45s (0:07:09); compileall app/ tests/ código 0. Sin pendiente nuevo de estos dos hallazgos. Continúan los pendientes anteriores del proyecto.

## 2026-10-27 — Documentación de entrega y nueva prueba operativa

**Corrección posterior de selectores:** se confirmó que el servidor ofrece un cliente ficticio, un sistema y una planilla operativa. Los listeners ya existían. Se agregó indicador de disponibilidad, manejo de errores de selección y corrección reproducible del service worker ante falta de red/caché. Cuatro archivos aplicados con respaldo y reinicio exclusivo de readyproof, sin borrar IndexedDB ni agregar datos al servidor. Jorge confirmó luego de Ctrl+F5 que las listas abren y el indicador aparece. Suite final: 158 passed in 487.56s, compileall código 0; cuatro hashes desplegados coincidentes y sin valores de secretos expuestos. La consola personal F12 no fue inspeccionada; el service worker quedó validado mediante pruebas aisladas. No se requiere borrar datos del navegador. Detalle en docs/CORRECCION_SELECTORES.md.

**Estado vigente de servidor privado:** Jorge autorizó expresamente compartir 67.205.170.29. Instalación privada completada en /home/readyproof, servicio sin root en 127.0.0.1:8000, PostgreSQL exclusivo loopback, claves aleatorias generadas en el servidor y msanchez creado por formulario HTTP normal. Login y flujo SAA-1/PDF/EML sin SMTP comprobados en Ubuntu; backup diario local y restauración en base separada aprobados. Túnel temporal respondió HTTP 200 desde Windows y se cerró al finalizar. No se publicaron puertos, dominio o HTTPS ni se tocaron Docker/Traefik existentes. El bloqueo previo de decisión de servidor queda resuelto por esa autorización. Instrucciones: docs/ACCESO_SERVIDOR_PRIVADO.md. Pendientes: Jorge abre su túnel, consulta la clave temporal solo por consola y la cambia; dominio propio/publicación, SMTP real del servidor, backup externo, datos reales y revisión de dispositivo/canvas.

Actualización de infraestructura: acceso SSH por clave confirmado. La inspección de 67.205.170.29 encontró brafemar-server, varios servicios Docker, 80/443 ocupados y solo 624 MB de RAM disponible sin swap. No es el servidor separado previsto. Instalación detenida sin cambios remotos; pendiente elección expresa de Jorge entre otro Droplet o preparación privada compartida. El bloqueo anterior de acceso SSH queda superado; no se hicieron instalaciones.

Despliegue solicitado posteriormente: Jorge eligió preparar en privado el servidor 67.205.170.29, sin dominio ni publicación. No utilizar readyproof.brafemar.com.ar. El acceso SSH sin contraseña interactiva fue rechazado; debe ejecutar scripts/habilitar_acceso_despliegue.ps1 en su consola privada para autorizar una clave. No se efectuaron cambios remotos. Luego corresponde inspeccionar el servidor y preparar instalación privada; dominio propio/HTTPS siguen pendientes.

Actualización posterior: el reporte local de la nueva prueba ya registra ejecución con msanchez, SMTP enviado (un intento ok) y recepción/apertura declaradas manualmente por el operador. PDF y huella comprobados nuevamente, sin repetir el envío. Queda resuelto el pendiente de ejecución/confirmación por consola descrito debajo; permanecen pendientes la inspección independiente del mensaje nuevo en Enviados, canvas/dispositivo y producción. Evidencia: `out/prueba_operativa_final/resultado.json`; carga `0ab4612f-3e33-4251-b79a-825fc3bd39fd`.

- SAL resuelto para el resumen: Jorge confirmó «Sistema de Extinción por Agentes Limpios», según el kit. No corresponde a alumbrado.
- Acceso administrador: Jorge confirmó que ya tiene acceso a msanchez. Esta declaración actualiza el pendiente histórico de recuperación; no se volvió a cambiar su clave ni se solicitó por chat.
- Jorge indicó que todavía no ejecutó el nuevo script `scripts/prueba_operativa_final.py`. Pendiente: ejecución interactiva con su cuenta, PDF descargado, aceptación SMTP y confirmación de recepción/apertura. La prueba recibida el 26/10 conserva su evidencia independiente y no se usa para aprobar esta ejecución nueva.
- Documentos preparados: guía de acceso, deployment DigitalOcean, checklist y resumen de manuales. La guía de acceso explica que todavía no existe botón de correo en la interfaz y diferencia las firmas canvas de los PNG ficticios por API.
- No hay despliegue, HTTPS productivo, backup restaurado ni monitoreo configurados en esta tarea. Dominio, tamaño/región/costo del Droplet, destino externo cifrado de respaldo y operadores requieren definición/aprobación de Jorge antes de instalar. Continúan pendientes el ensayo Ubuntu, proxy/CSRF y la habilitación para datos reales.
- Gunicorn 26.2.0 se documenta únicamente como dependencia justificada del servicio WSGI propuesto. No se agregó a requisitos ni se instaló en Windows. No se crearon servicios, cuentas ni recursos externos.
- Validación documental/local cerrada: 156 pruebas aprobadas, compileall código 0 y revisión sin valores de secretos expuestos ni enlaces locales rotos. Evidencias en out/entrega_documentacion_pytest_final.txt y out/entrega_documentacion_revision.json. No modifica los pendientes operativos o productivos enumerados arriba.

## 2026-10-27 — Entrega técnica y Gmail HTTPS resueltos para el piloto

- Usuario definitivo tecnico_readyproof creado y probado; no se creó tecnico_brafemar. Clave temporal solo en archivo root 0600, canal privado separado, y cambio en Mi cuenta al primer ingreso. Casilla guardada para esta prueba: jorgesanchezing@gmail.com; reemplazar por el correo propio del técnico al entregar.
- Acceso individual de otra PC/Android preparado con readyproof_tunel_tecnico y clave restringida; sin compartir root. Paquete y guías listos. Túnel y restricciones comprobados desde Windows; configuración/prueba física de Android y canvas siguen pendientes del técnico/Jorge.
- Botón de documentación activo en Mi cuenta, correo propio y controles de duplicación/CSRF. No envía contraseñas ni claves. Gmail HTTPS autorizado y configurado por decisión de Jorge para superar el bloqueo SMTP del proveedor; no se activó correo real de planillas.
- Prueba real readyproof.ar@gmail.com -> jorgesanchezing@gmail.com: dos guías y logo, SENT verificado por MCP y recepción confirmada por Jorge. Mensaje Gmail 1a17dee776fd216c. No repetir para verificar; Gmail reescribe el Message-ID y se conserva el identificador real en la evidencia.
- Validación final: 177 pruebas aprobadas, compileall código 0. Entrega privada de prueba lista; READY FOR GO-LIVE productivo no corresponde todavía. Continúan datos ficticios, dominio/HTTPS pendiente, backup externo pendiente, capacidad y demás decisiones abiertas de la serie.
- Revisar vigencia/renovación y estado de publicación del OAuth de Google antes de comprometer operación continua; la autorización inicial se realizó como aplicación propia en prueba. Los secretos permanecen fuera del código, adjuntos y paquete técnico. Procedimiento GMAIL_HTTPS.md; entrega y acceso en ENTREGA_A_BRAFEMAR.md y ACCESO_TECNICO_BRAFEMAR.md.


## 2026-10-27 — PDF por correo desde la carga

Botón instalado en la app privada, envío a la casilla de prueba de Jorge aceptado por Gmail y PDF confirmado en Enviados. Recepción manual de esta nueva prueba pendiente; no repetir por ese motivo. Resuelto por pedido de Jorge: SAA-1 se emite en una sola A4 horizontal, versión rp2, con copia de cargas históricas. Verificado en servidor y en Gmail Enviados. La recepción manual de la nueva prueba A4 sigue pendiente. Informar a Martín del ajuste de impresión; no cambian filas, campos ni contenido normativo.


## 2026-10-27 — Alcance de las cuatro familias

Resuelto por Jorge: habilitar todas las planillas de SDI (5), SBC (6) y SAL (4), junto a SAA-1. Conservar la paginación del kit en A4 horizontal para las nuevas, sin reducirlas obligatoriamente a una hoja. SAL es Agentes Limpios. Cuatro familias equivalen a 16 planillas operativas; los contenedores y versiones previas permanecen en la base. Resuelto y verificado: migración 009 aplicada en el servidor privado, 16 formularios y PDF descargados por la API normal con datos ficticios; 208 tests aprobados. Se conservan 25 registros totales por el historial. Sin pendientes bloqueantes para esta habilitación; siguen vigentes los pendientes generales de producción y de revisión normativa de la serie.


## 2026-10-27 — Firmantes: DNI y alcance v1.0

Resuelto por Jorge: DNI de 8 a 15 dígitos, sin puntos ni guiones. Se agregan nombre y DNI obligatorios del responsable, cargo opcional y la identidad autenticada del técnico, con sus datos visibles en PDF. Se mantiene SAL como Agentes Limpios y las 16 planillas agrupadas por sistema. CUIT/CUIL y numeración quedan en el backlog v1.1, sujetos a las decisiones allí enumeradas. Resuelto y verificado: 232 tests aprobados, migración 010 aplicada, 16 PDF con identidades y rechazo de finalización incompleta comprobados en el servidor privado. No se transmitieron correos nuevos. Sin bloqueos de esta ampliación; siguen los pendientes generales del piloto y las decisiones de backlog v1.1.


## 2026-10-28 — Diagnóstico v1.1 y decisiones del nuevo encargo

- Resuelto por el encargo recibido: mantener UUID de cliente y agregar CUIT normalizado, validado, único y obligatorio; migrar en dos pasos sin inventar datos faltantes.
- Resuelto: número global únicamente al emitir, sin reinicio anual ni huecos; contador con bloqueo transaccional, UUID e históricos conservados. Los borradores sincronizados no consumen número.
- Resuelto el alcance de las 63 pendientes: cinco SAA y 58 de once sistemas aún no habilitados. SAL sigue siendo Agentes Limpios.
- Antes de migrar: Jorge debe autorizar Drive de readyproof.ar@gmail.com; luego completar respaldo cifrado, retención, aviso de fallos y restauración separada de la versión vigente. El dump observado contiene 009 y la BD consultada está en 010. La restauración antigua no acredita esta versión.
- Antes de exigir CUIT: completar y revisar el cliente ficticio existente mediante flujo administrativo; actualmente no existe columna CUIT en clientes. No se informó una comprobación de duplicados inexistente.
- Antes de modelar visitas semanales: confirmar la convención calendario S1–S5 para no inventar una sexta columna o equivalencia ISO. Propuesta de coexistencia con matrices históricas en `docs/DIAGNOSTICO_ETAPA0_V1_1.md`.
- Antes de cambiar opciones de las grillas: resolver con Martín cualquier contradicción entre tres estados pedidos y las leyendas del kit; conservar versiones previas.
- Antes de ampliar altas dinámicas: definir permisos del técnico para cliente, establecimiento, sistema y responsables. Antes de uso real: confirmar empresa mantenedora/certificado y autorización expresa de Jorge. Piloto no se cambia en esta etapa.
- Sigue pendiente la prueba física en teléfono; la evidencia Chromium aislada no equivale a Android o iPhone reales. La recepción humana del último correo A4 no está confirmada en su evidencia, aunque existe envío real previo por Gmail HTTPS.
- Cierre: Etapa 0 completada sin cambios de aplicación ni de datos. La instrucción recibida exige detenerse y reportar; no se inició la Etapa 1.


## 2026-10-28 — Resuelto: respaldo externo y restauración 010

- Drive fue autorizado por Jorge para readyproof.ar@gmail.com. Copia cifrada externa y restauración final verificadas contra el mismo snapshot: esquema 010, 17 tablas y todos los hashes de PDF/firmas coincidentes. El respaldo anterior 009 deja de ser el único respaldo observado.
- Timer nuevo activo y probado bajo systemd. Retención 30 diarios/12 mensuales y aviso Gmail configurados. Evidencia en out/etapa1_backup/verificacion_drive_restore.json.
- Clave generada con aleatoriedad criptográfica en archivo privado del servidor; copia DPAPI verificada para el usuario Windows de Jorge, fuera del repositorio. Para recuperación independiente de esa PC, custodiar además en el gestor de contraseñas; no compartirla por chat.
- Siguen pendientes las decisiones de etapas posteriores del nuevo encargo: alcance de mediciones obligatorias; confirmación de Martín sobre 3/4 estados; datos definitivos de mantenedora/certificado y autorización expresa del modo real. No se habilitó modo real ni se aplicaron migraciones.


## 2026-10-28 — Etapa 2 completada

- Resuelto: CUIT opcional normalizado, único y validado en modelo; migraciones 011–012 aplicadas. UUID/referencias preservados y sistemas activos con cliente obligatorio.
- Auditoría real de solo lectura: un cliente ficticio sin CUIT; ningún duplicado, inválido, no normalizado ni sistema sin cliente. El faltante es esperado en esta migración opcional; no se inventa ni se hace NOT NULL todavía. Alta/edición de CUIT en interfaz y revisión administrativa siguen pendientes de etapas posteriores.
- Respaldo actual en 012, descargado y restaurado en base separada. Copia previa 010 preservada y recuperable. Integridad: 980 filas históricas sin diferencias. Modo piloto conservado; no se cargó dato real.
- Aclaración del ejemplo del encargo: 82000000000 no pasa módulo 11 (verificador calculado 7). Se usa como caso inválido, sin debilitar la validación. No se atribuye CUIT a IRAM ni se acredita inscripción ante ARCA.
- Para Etapa 3: confirmar si la medición obligatoria corresponde solo a ítems de verificación (ver) con unidad o también a todos los campos generales con unidad. O sin observación debe rechazarse; no se inventa texto para completarla.
- Para etapas siguientes se mantienen pendientes la confirmación de Martín sobre estados de grillas, datos definitivos de mantenedora/certificado y autorización de modo real. Verificar además vigencia renovable del consentimiento OAuth antes de depender de respaldos desatendidos a largo plazo.


## 2026-10-28 — Etapa 3: decisión confirmada y cierre local

- Resuelto por Jorge: mediciones obligatorias solo en verificación (ver) con unidad, salvo NA. O sin observación se rechaza; no se completa automáticamente. General con unidad no recibe obligatoriedad nueva. Implementado y probado localmente.
- Código del importador validado con los 79 originales y catálogo (1.539 ítems, cero diferencias). Simulación e idempotencia verificadas en BD aislada; los 16 existentes no se sobrescriben y los históricos no se eliminan para ajustar conteos.
- Pendiente operativo: autorización específica para transferir código, catálogo y ZIP interno al servidor compartido 67.205.170.29, ruta privada /var/backups/readyproof/revision-etapa3. La revisión automática rechazó el intento por ese motivo; no hubo transferencia ni despliegue de Etapa 3. Consulta enviada a Jorge; no se infiere aprobación por tiempo transcurrido.
- Pruebas actuales: 300 casos conciliados por identificador; SBC-2 tuvo un 503 de conversión en la corrida completa y pasó aisladamente. Causa exacta original no registrada. Se conservan ambas evidencias para no ocultar la incidencia.
- Los 63 códigos nuevos aún no se importaron en la base activa ni se habilitaron; quedan para Etapa 5. Sus manuales deben asociarse cuando existan las ediciones correctas; no se crean contenidos ficticios para simular manuales reales.
- Siguen pendientes las confirmaciones de Martín sobre estados de grilla y demás decisiones de las etapas 4–6. El servidor conserva el último estado operativo confirmado de Etapa 2 hasta completar la autorización, comprobaciones y aplicación de Etapa 3.


## 2026-10-28 — Etapa 3 aplicada; autorización de transferencia resuelta

- Resuelto: Jorge autorizó expresamente código, catálogo y los 79 Excel al servidor 67.205.170.29 en revisión privada. Se ejecutó y verificó; ya no está pendiente aquella aprobación automática.
- Reglas e importador instalados y comprobados. Cotejo real: 16 existentes y 63 pendientes, sin cambios. No se sobrescribieron definiciones ni se habilitaron nuevas familias. Fuente/ y originales sin modificaciones.
- Backups y restauración posteriores al código nuevo verificados, esquema 012 y datos íntegros. Evidencia en out/etapa3_importador/resultado_servidor.json; los resultados locales anteriores conservan su estado histórico.
- Para Etapa 4: confirmar avance con permisos de desbloqueo creador/admin y si se mantienen cuatro estados del kit (✓/O/X/NA). Reducir a tres requiere la confirmación de Martín prevista por el encargo, conservar versiones históricas y evitar una reinterpretación automática.
- Siguen pendientes calendario S1–S5, manuales reales/asociaciones para las familias nuevas, habilitación de 63 en Etapa 5 y autorización/configuración del modo real en Etapa 6. Ninguno se dio por resuelto por esta instalación.


## 2026-10-28 — Etapa 4: decisiones confirmadas por Jorge

- Resuelto: avanzar con desbloqueo solo para creador/admin; conservar ✓/O/X/NA del kit. No se reduce a tres estados ni se reinterpretan frecuencias.
- El PDF anterior se conserva de forma independiente antes de desbloquear. El registro se asigna únicamente al emitir y se mantiene en reemisiones; no se modifica la numeración de documentos históricos.
- Pendientes: cierre de verificaciones de esta etapa; confirmación independiente de Etapa 5 para importar/habilitar las 63 restantes; calendario S1–S5, asociaciones de manuales reales y transición a modo real con mantenedora/certificado autorizados.


## 2026-10-28 — Cierre verificado de desbloqueo y revisión

- Resuelto: tareas enumeradas de etapa 4 aplicadas en 013, cuatro estados conservados, historial PDF inmutable, permisos y motivo comprobados. Backup y restauración posteriores verificados; 325 casos actuales conciliados sin fallos pendientes.
- Alcance todavía abierto del instructivo ampliado: establecimientos, listas dinámicas con búsqueda/alta, precarga de equipos/datos fijos y operación de anulación. No se implementaron en este corte y no se declaran resueltos. Debe acordarse/completarse ese alcance antes de dar por entregada la etapa ampliada o habilitar uso real.
- Confirmación de etapa 5 aún pendiente: importar y habilitar las otras 63. No se avanzó automáticamente. Continúan S1–S5, manuales reales/asociaciones y autorización/configuración de modo real.


## 2026-10-28 — Etapa 5 autorizada; discrepancias pendientes de aclaración

- Jorge autorizó importar las 63 restantes, habilitar 11 familias, agregar 189 pruebas y verificar respaldo/restauración. Revisión previa sin código ni BD modificados: 79 Excel oficiales del ZIP, 1.539 ítems y cero diferencias con el catálogo. Fuente/planillas contiene cuatro JSON; los originales completos están en el ZIP verificado, que el importador ya admite sin extracción.
- El pedido contiene nombres incompatibles con el kit: SAP es Agua Pulverizada, SDC Dióxido de Carbono, SEP Extinción por Polvo, SGE Generador de Espuma, SIM Simbología de Seguridad contra Incendios, SRA Rociadores Automáticos, SRE Rociadores de Espuma, SSA Extinción por Solución Acuosa y STM Tuberías y Mangueras. SCC y SHC deben usar sus denominaciones completas del kit. Consulta enviada a Jorge para confirmar conservar los nombres oficiales; no se aplicaron denominaciones ajenas a las planillas.
- Consulta pendiente: la etapa 4 usa original revisión pública 0 y primera corrección 1; el pedido nuevo exige 1 al emitir. No se cambia esta regla ni se reescriben históricos hasta recibir la aclaración.
- Corrección aritmética: 325 casos actuales + 189 nuevos = 514 mínimos, no 421. Se conservarán los casos existentes; tres por planilla es el mínimo autorizado.
- El pedido indica versión 00-26-ms1 para las nuevas, mientras el importador actual genera versiones v5 basadas en SHA. Al implementar se debe respetar la nueva versión solicitada sin sobrescribir las 16 aprobadas ni debilitar el cotejo determinista y de huellas.
- Evidencia previa: out/etapa5_planillas/cotejo_79_sin_bd.json y etapa5_planillas.json. No se declara completada la importación, migración, habilitación, pruebas nuevas ni restauración de etapa 5.


## 2026-10-28 — Etapa 5: nombres/revisión resueltos; siglas originales sin paréntesis

- Jorge confirmó nombres oficiales del kit y consistencia histórica: original revisión pública 0, primera corrección 1. Las dos consultas anteriores quedan resueltas.
- Nuevo requisito de Jorge: extraer (XXX) de primeras 20 filas, comparar con nombre del archivo, rechazar ausencia o contradicción y mapear instalaciones por tipo.
- Auditoría de los 79 originales: 0 contienen (XXX) en las primeras 20 filas; los 79 sí contienen su código interno SG-PEM-IFI-XXX-N, coincidente con catálogo y archivo. No se corrigieron ni reescribieron originales para fabricar coincidencias. Evidencia: out/etapa5_planillas/auditoria_siglas_originales.json.
- Pendiente respuesta: autorizar el código interno como alternativa únicamente ante ausencia de paréntesis, rechazando siempre siglas contradictorias, o mantener el requisito literal y esperar nuevos originales. Se consultó conforme a la regla de AGENTS.md de detener cambios contradictorios con el kit. No se infiere autorización por la confirmación anterior, que no contemplaba esta ausencia comprobada.
- Trabajo independiente: detector estricto y consulta de sistemas activos por sigla/cliente implementados localmente; cuatro pruebas nuevas aprobadas. El detector aún no se conecta a la importación real, que rechazaría los 79 con la regla literal. La ampliación del lector conserva contenido, definiciones y huellas: prueba existente de los 79 aprobada. Compilación sin errores.
- Conteo mínimo corregido por la tarea nueva: 325 previas + 4 de siglas + 189 por planilla = 518; las cinco ejecuciones de este corte incluyen una prueba existente y no agregan cinco casos nuevos. No se declara la suite completa ejecutada ni las 63 importadas.

## 2026-10-28 — Etapa 5: importación verificada y pendientes vigentes

- Resueltas por Jorge: nombres oficiales del kit; revisión original 0/corrección 1; siglas desde código interno, paréntesis o archivo con coincidencia de al menos dos fuentes y rechazo de paréntesis contradictorios. Los 79 originales se validaron sin alteraciones: código interno, archivo y catálogo coinciden.
- Resuelta la autorización específica de transferencia: Jorge autorizó código, pruebas, catálogo y documentación interna hacia `/home/readyproof_revision_etapa5` en 67.205.170.29, acceso privado 0700 y manifiesto, excluyendo secretos y bases. La revisión automática había rechazado el intento anterior por falta de esa autorización específica; después de obtenerla se completó la transferencia. No queda bloqueada por aquella revisión.
- Importación/migración 014 verificadas: 63 nuevas, 16 existentes, cero diferencias; 79 activas, 88 filas históricas y 15 familias. Suite consolidada 525/525; respaldo Drive y restauración aislada verificados. Los 189 recorridos adicionales sobre clones de la restauración aprobaron sin modificar su base original.
- Las nuevas planillas mantienen `manual_id` pendiente cuando no existe la edición real correspondiente. No se inventaron manuales ni vínculos para simular cobertura documental. Asociarlos a los manuales correctos antes de la entrega definitiva de ese alcance.
- **Unidades de SCC:** la revisión visual de SCC-1 oficial muestra presiones en MPa, mientras el encargo general indica bar para SCC. Se conserva el dato fuente literal; no se convirtieron valores ni se modificaron unidades. Se consultó a Jorge si se mantiene esa fidelidad en el piloto y se deja a Martín la corrección antes del uso real. La diferencia normativa no se declara resuelta por las pruebas de importación.
- Continúan abiertos: calendario S1–S5, normas/confirmaciones de Martín, establecimientos, datos dinámicos con búsqueda/alta, precargas y operación de anulación del instructivo ampliado. La etapa 5 no resuelve ese alcance previo.
- El modo real permanece deshabilitado. Etapa 6 y puesta en marcha real requieren confirmación independiente. Se conservaron los tres recorridos mínimos por planilla y se agregaron regresiones específicas; no se redujo la suite a 421 casos.

## 2026-10-28 — SCC-1: conservación literal confirmada por Jorge

- Resuelta la consulta operativa: conservar MPa tal como aparece en el Excel oficial, sin alterar unidades ni valores. Jorge confirma que esta inconsistencia reportada no bloquea la etapa 5 en modo piloto.
- Reporte: `unidad_encontrada: MPa`, `unidad_esperada: bar`, `estado: REVISAR_CON_MARTIN`. La unidad esperada proviene del encargo general; no constituye una corrección normativa aprobada.
- Antes de etapa 6 y de habilitar uso real, Martín debe confirmar MPa vs bar. Si confirma que corresponde corregir, Jorge indica una migración 016 independiente; no se implementa ahora ni se reescriben documentos históricos.


## 2026-10-28 — Auditoría: cambios necesarios conservados y decisiones normativas

- Resuelto por Jorge: conservar las cinco diferencias de fuente/ frente a la base Git, ajuste A4 SAA-1 y versiones/huellas de cuatro JSON. No son accidentales ni cambios de etapa 5. Se reanuda la auditoría sin revertirlas; ver CAMBIOS_AUTORIZADOS_EN_FUENTE.md.

### SCC-1: unidad MPa vs bar (migración 016 si corresponde)

Excel oficial: MPa. Encargo general: bar. Se conserva el kit literal. Martín confirma si corresponde corregir antes de etapa 6 y de habilitar uso real; una eventual migración 016 no se implementa en esta auditoría.

### SDI: 3 vs 4 estados en grillas (validación si corresponde)

Implementado: cuatro estados del kit (✓/O/X/NA), mantenidos por decisión de Jorge. Pendiente: Martín confirma si corresponden tres o cuatro antes del uso real. No se reducen ni reinterpretan estados ni se reescriben registros históricos.


## 2026-10-28 — Auditoría 0–5 cerrada en piloto

- Resuelto el bloqueo por test A4: corrección de promesas y sincronización, caso focalizado aprobado y suite posterior completa de 525 casos aprobada sin omisiones. Ver docs/DIAGNOSTICO_TEST_A4_HISTORICA.md y AUDITORIA_ETAPAS_0_A_5.json. La traza inicial no conservó el disparador primario de la intermitencia; esa limitación queda documentada, sin atribuirlo a datos dañados.
- Resueltos los controles técnicos auditados: exclusión de entornos, permisos, conservación autorizada de fuente, código/migraciones, BD, binarios, respaldo/restauración y documentación. Los resultados iniciales se conservan como evidencia histórica.
- Permanecen SCC-1 MPa vs bar y SDI tres/cuatro estados para Martín, manuales reales/asociaciones, S1–S5 y el alcance ampliado ya registrado. La auditoría técnica no autoriza etapa 6 ni uso real. Los commits de auditoría no consolidan automáticamente todo el trabajo previo pendiente del proyecto.


## 2026-10-28 — Etapa 6: transición real pendiente

La habilitación configurable está implementada; el servidor permanece en piloto y correo de prueba. Antes de activarla, Jorge debe confirmar empresa mantenedora y certificado reales y aprobar el checklist de docs/TRANSICION_PILOTO_A_REAL.md. Martín debe resolver SCC-1 MPa vs bar y confirmar los cuatro estados SDI. La migración 016 corresponde a auditoría; una eventual corrección normativa usará el siguiente número disponible. Establecimientos, catálogos dinámicos avanzados y anulación siguen sujetos al backlog; esta entrega no los da por implementados.


## 2026-10-28 — Confirmación final de transición y unidades

Jorge autoriza modo REAL, confirma mantenedora READYPROOF y certificado IFI-2024-10001 y aprueba el checklist. Comunica decisión de Martín: bar en presión. Aclara conservar los cuatro estados SDI y crear las versiones necesarias antes del corte. Se resuelve SCC-1 mediante versión 00-26-bar1 y migración 017, sin tocar fuente ni datos históricos. SDI no incorpora mediciones nuevas ni pierde estados. El alcance ampliado del backlog no se declara implementado por esta autorización.


## 2026-11-09 — Certificado en planillas por sistema

Confirmar con Jorge y Martín si el certificado debe variar por sistema y cuál es el identificador oficial completo de cada uno. Hasta recibir esa confirmación, la emisión conserva el certificado vigente.
