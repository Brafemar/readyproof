# Instrucción para Codex — readyproof: clientes por CUIT, sistemas, 79 planillas, desbloqueo, datos dinámicos, numeración y backup

**Proyecto:** readyproof (Flask + PostgreSQL), repositorio `Brafemar/readyproof`, copia local en `C:\Users\jorge\Readyproof`.
**Usuarios de la app:** readyproof (ver sección 1.0). **Empresa que usa la app:** BRAFEMAR.
**Fecha:** 27/10/2026 (actualizada después de la migración `010_firmantes`, 232 pruebas).
**Solicitante:** Jorge Sánchez.

---

## 0. Punto de partida (estado verificado el 27/10/2026)

Esto ya existe y **se construye encima, no se rehace**:

- **16 planillas habilitadas** (migración `009_multisistema`): SAA-1, SDI-1 a 5, SBC-1 a 6 y SAL-1 a 4, con manuales asociados. El formulario ya maneja ENE–DIC, S1–S5 y ✓/O/X/NA con valor y fecha por bloque.
- **Asignación de sistemas a clientes**: `GET /api/clientes/{id}/sistemas`.
- **Firmantes** (migración `010_firmantes`): nombre y DNI obligatorios, cargo opcional, DNI de 8 a 15 dígitos sin puntos ni guiones (decisión de Jorge). Las dos firmas se exigen en el backend.
- **Estados de carga**: `borrador`, `finalizada`, `emitida`, con control de revisión (`Carga.revision` y `RevisionCarga`).
- **Envío de documentación por correo** con auditoría.
- **Service Worker** `readyproof-ui-v3` con `updateViaCache: none`.
- **232 pruebas aprobadas.**
- `docs/BACKLOG_v1_1.md`: las decisiones pendientes que figuran ahí sobre CUIT y numeración quedan resueltas en las secciones 1.1 y 1.3.

Lo que **no** existe todavía: CUIT/CUIL en `Cliente`, establecimientos, numeración de registros, estado `anulada`, desbloqueo, búsqueda de planillas, backup externo y las 63 planillas restantes.

**Modo piloto:** hoy la app solo acepta datos ficticios (nombres que empiezan con `[Ejemplo] ` y DNI `00000000`). Esa restricción tiene que pasar a ser una **configuración "modo piloto / modo real"**, que solo cambia el administrador. **Pasar a modo real requiere la aprobación explícita de Jorge**: no se habilita como parte de este pedido.

## 1. Objetivo

Este pedido tiene seis partes principales, que se hacen en el orden de la sección 8, más los puntos de continuidad y pendientes de las secciones 1.5 y 1.6:

1. **Backup automático** de la base de datos y de los PDF a Google Drive, todas las noches.
2. **Clientes por CUIT/CUIL:** alta, búsqueda y edición de la razón social, con el CUIT/CUIL como identificador único.
3. **Sistemas del cliente:** a cada cliente se le agregan los sistemas que tiene instalados, y sus datos quedan guardados para las visitas siguientes.
4. **Las 79 planillas de los 15 sistemas:** que todas se puedan completar desde la app, con los ítems tal cual figuran en los Excel oficiales, y que cada una emita su PDF. Hoy hay 16 habilitadas (ver sección 0); faltan 63.
5. **Numeración y búsqueda** de planillas.
6. **Desbloqueo de planillas y datos dinámicos:** que las planillas se puedan editar (con control y registro) y que los datos se elijan de listas, no se escriban a mano cada vez (secciones 1.5 y 1.7).

## 1.0 Quién es quién (no confundir)

| Actor | Qué es | Dato que lo identifica |
|---|---|---|
| **readyproof** | La empresa y la aplicación. **Todos los usuarios de la app (técnicos y administradores) son usuarios de readyproof.** | Usuario y contraseña de la app |
| **Cliente (razón social)** | La empresa a la que se le hace el mantenimiento | **CUIT/CUIL** |
| **Firmante / responsable** | Empleado del cliente que firma la planilla | **DNI** (obligatorio) |
| **BRAFEMAR** | Empresa que usa readyproof para sus trabajos | — |

- En todo el código, las pantallas, los correos y la documentación, el usuario se presenta como **usuario de readyproof**, nunca como usuario de BRAFEMAR.
- Los Excel traen **"EMPRESA MANTENEDORA: BRAFEMAR"** escrito fijo. En la app ese campo **no va fijo en el código**: sale de una configuración editable por el administrador, junto con el "N.° mantenedor certificado". **Confirmar con Jorge qué valor lleva antes de emitir planillas reales.**

Hay un problema reportado: en la planilla **SG-PEM-IFI-SDI-2 (Prueba mensual)** no se puede marcar el ítem **"Detectores de humo"** (fila 24 del Excel). Hay que encontrar la causa y corregirla de raíz, no solo para ese ítem.

## 1.1 Clientes por CUIT/CUIL

- **Cliente = razón social.** El CUIT/CUIL es su identificador **único** y obligatorio. **Se conserva el identificador interno actual como clave primaria**, y el CUIT/CUIL va como campo `UNIQUE` (resuelve la decisión pendiente del backlog).
  - Migración en dos pasos: primero se agrega el campo admitiendo vacíos y se revisan los clientes existentes; recién después se exige `NOT NULL` y `UNIQUE`.
  - Validar el formato (11 dígitos, se acepta escrito con o sin guiones y se guarda normalizado) y el **dígito verificador**.
  - No se puede crear un cliente con un CUIT que ya existe: si ya está cargado, la app lo muestra y ofrece abrirlo.
  - Restricción de unicidad también en la base de datos, no solo en el formulario.
- Datos del cliente: razón social, CUIT/CUIL, teléfono, correo de envío de planillas, dirección. Un cliente puede tener **varios establecimientos** (dirección, edificio, sector), porque la planilla pide esos tres datos.
- **Búsqueda** de clientes por CUIT (completo o parcial) o por razón social.
- **Edición** con registro de quién cambió qué y cuándo. El CUIT no se edita libremente: si hay un error, el cambio lo hace un administrador y queda registrado.
- **Técnicos asignados:** respetar los permisos por cliente de la etapa 4 (un técnico solo ve los clientes que tiene asignados; el administrador ve todos).
- Al abrir una planilla, el encabezado (Cliente, CUIT, Teléfono, Dirección, Edificio, Sector) se **completa solo** con los datos del cliente y del establecimiento elegidos.
- No confundir con el firmante: el **CUIT/CUIL es de la razón social** y el **DNI es del responsable que firma** (ya implementado en `FirmaCarga`, no se toca).

## 1.2 Sistemas del cliente

- A cada cliente (y establecimiento) se le **agregan** los sistemas que tiene, elegidos de los 15 de la sección 3. Se pueden agregar, desactivar (no borrar) y editar.
- Un cliente puede tener **más de un sistema del mismo tipo** (por ejemplo, dos bombas o dos centrales de detección). Cada uno se distingue por el campo **Sistema / Designación** de la planilla.
- La **Información general** (planilla `-1` de cada sistema) pertenece a ese sistema del cliente: se carga al agregarlo y se reutiliza en todas las visitas (ver sección 4).
- Cada carga queda vinculada a **cliente + establecimiento + sistema del cliente + planilla + período**. Así, el mes siguiente el técnico busca el cliente y encuentra todo lo anterior sin volver a cargarlo.

## 1.3 Numeración y búsqueda de planillas

- Cada planilla recibe un **número único y correlativo** (formato sugerido `000001`) **al emitirse**. El número no se reutiliza ni se cambia, aunque la planilla se anule o se desbloquee. No se reinicia por año ni por cliente: hay una sola serie.
- **Sin saltos:** como una secuencia de PostgreSQL puede dejar huecos, el número se toma de una **tabla contador con bloqueo de fila**, dentro de la misma transacción que emite. Si la emisión falla, el número no se consume.
- Se mantiene el UUID de carga que usan la sincronización y la idempotencia.
- Como hay carga offline, el número **lo asigna siempre el servidor**, nunca el dispositivo. Hasta la emisión, la carga muestra "sin número".
- Los PDF ya emitidos no se reescriben para agregarles un número.
- El número aparece en la app y en el PDF.
- **Búsqueda** de planillas por: número, cliente (CUIT o razón social), sistema, planilla, frecuencia y rango de fechas. Desde el resultado se ve quién la cargó, quién la firmó (nombre y DNI) y se puede volver a descargar el PDF.

## 1.4 Backup automático a Google Drive

- Todas las noches, el servidor hace una copia de la base PostgreSQL (`pg_dump`, comprimida) y de la carpeta de PDF emitidos, y la sube a **Google Drive de la cuenta `readyproof.ar@gmail.com`** (gratis, 15 GB). Herramienta sugerida: `rclone`, que es gratuita.
- **El backup no se guarda en la misma base ni solo en el mismo servidor:** si el servidor falla, la copia tiene que estar afuera.
- **Cifrado:** la copia tiene datos personales (DNI de firmantes), así que se cifra antes de subirla. La clave no va en el repositorio. Se documenta dónde la guarda Jorge.
- **Retención:** las últimas 30 copias diarias y una por mes de los últimos 12 meses. Las más viejas se borran solas.
- **Aviso:** si la copia falla, se manda un correo a Jorge por el Gmail que ya funciona.
- **Prueba de restauración obligatoria:** restaurar una copia en una base aparte y comprobar que tiene los mismos clientes, cargas y PDF. Documentar el procedimiento paso a paso en `docs/`.
- La autorización de Google Drive la tiene que hacer Jorge una sola vez: **detenerse y pedírsela**, no buscar contraseñas por su cuenta.

## 1.5 Continuidad entre visitas y comportamiento de la app

- **Datos fijos precargados:** al abrir una planilla nueva para un cliente y sistema que ya tienen cargas, se completan solos el encabezado, el Sistema / Designación, la Información general y los datos de equipos (marca, modelo, ubicación). **Los resultados de la visita no se copian:** estados ✓/O/X/NA, valores medidos, observaciones y firmas arrancan vacíos.
- **Estados de una planilla y desbloqueo:**
  - **Borrador:** se edita libremente, todas las veces que haga falta, online u offline.
  - Se agrega el estado **`anulada`** a los que ya existen. Para el historial de cambios se usa `RevisionCarga`.
  - **Emitida:** queda bloqueada para proteger lo que se envió al cliente, pero **se puede desbloquear** para corregirla. Pueden desbloquear el administrador y el técnico que la cargó (el administrador puede cambiar esta regla en la configuración). Hay que indicar un **motivo obligatorio**.
  - Al desbloquearla vuelve a ser editable. Al reemitirla **conserva su número** y pasa a la **revisión siguiente** (`000045 – Rev. 1`), con un PDF nuevo que muestra la revisión. **La versión anterior no se borra:** queda guardada con su PDF, y se registra quién desbloqueó, cuándo, por qué y qué campos cambiaron.
  - Si la planilla ya se había enviado al cliente, la app ofrece reenviarla con la revisión nueva.
  - **Anular** sigue existiendo para una planilla que no corresponde. La anulada queda visible en la búsqueda como "Anulada" y su número no se reutiliza.
  - En pantalla tiene que quedar claro **en qué estado está** la planilla y, si está bloqueada, el botón **"Desbloquear para editar"**. Nunca un formulario que no responde sin explicar por qué.
- **Actualizaciones de la app:** cada versión nueva del formulario tiene que llegar a los dispositivos sin que el usuario borre el caché a mano. Versionar el Service Worker y las definiciones de planillas, avisar "Hay una versión nueva, recargar", y que una carga offline empezada con una versión anterior se pueda terminar y sincronizar sin perder datos.

## 1.6 Pendientes de entrega a BRAFEMAR (verificar y reportar el estado)

- Envío real de una planilla por correo **desde el servidor** (el Gmail se probó en local en la etapa 7).
- Prueba física de carga offline y sincronización en **iPhone** (pendiente desde la etapa 3).
- Verificar el **usuario técnico de readyproof** (`tecnico_readyproof`) y sus clientes asignados.
- **Guía de entrega:** cómo entrar (acceso privado actual por túnel SSH, `docs/ACCESO_SERVIDOR_PRIVADO.md`), buscar un cliente, agregar sistemas, cargar, firmar, emitir, desbloquear, enviar y buscar planillas.

## 1.7 Datos dinámicos: elegir en vez de escribir

**Todo dato que ya existe en la base se elige de una lista; no se escribe de nuevo.** La lista permite buscar mientras se escribe y, si el dato no existe, ofrece **"Agregar nuevo"** sin salir de la planilla.

| Dato | De dónde sale la lista |
|---|---|
| Cliente | Clientes por CUIT o razón social (1.1) |
| Establecimiento (dirección, edificio, sector) | Establecimientos de ese cliente |
| Sistema / Designación | Sistemas de ese cliente (1.2) |
| Planilla | Planillas de ese sistema, con su frecuencia (sección 5) |
| Inspector / técnico | Usuarios de readyproof asignados a ese cliente |
| Firmante responsable (nombre, DNI, cargo) | Firmantes ya usados en ese cliente. El DNI se valida y no se duplica por cliente. |
| Opciones `☐` de Información general | Las opciones exactas del Excel (catálogo, campo `opciones`) |
| Estado de cada ítem | ✓ / O / X (grillas) o ✓ / O / X / NA (verificación), según la sección 4 |
| Equipos (marca, modelo, ubicación) | Los ya cargados en la Información general de ese sistema |

Reglas:
- **Todos los controles responden** al tocarlos en celular, tablet y PC, online y offline. Un ítem, lista o campo que no se puede seleccionar es un error que se corrige y se cubre con una prueba (es el caso de "Detectores de humo").
- Las listas funcionan **offline** con los datos que el dispositivo tenía en la última sincronización. Lo agregado offline se sincroniza después **sin crear duplicados**: el CUIT y el DNI se verifican en el servidor.
- Elegir un cliente o un sistema **completa solos** los campos que dependen de él (encabezado, Información general, equipos).

## 2. Fuente única de verdad

| Archivo | Uso |
|---|---|
| `SG-PEM-IFI_Planillas_v5.zip` (79 `.xlsx`) | **Fuente oficial.** Todo ítem, texto, orden y unidad sale de acá. |
| `SG-PEM-IFI_Serie_completa_v5.zip` | Mismos 79 Excel (idénticos byte a byte), más los 15 manuales `.docx`, los 14 informes generales `.docx` y los PDF. Usar para los manuales. |
| `catalogo_referencia_planillas.json` | Catálogo extraído de los Excel v5: planilla → bloques → ítems (con fila de origen y unidad), y campos de Información general con sus opciones ☐. **Es para verificar, no reemplaza al Excel.** |
| `Inventario_planillas_SG-PEM-IFI.xlsx` | Resumen por sistema y detalle de las 79 planillas (frecuencia, formato, cantidad de ítems). |

**No usar** los zip sueltos `SG-PEM-IFI-SCC_Cocinas_comerciales.zip`: son versiones anteriores (06:14 y 07:25 del 24/10). La v5 (16:43 del 24/10) es la vigente y corrige el gas expelente (nitrógeno seco) y agrega las filas del fusible de prueba en SCC-3 y SCC-4.

**Prohibido** inventar, resumir, reordenar o "mejorar" ítems. El texto va literal del Excel. Si algo del Excel es ambiguo, se reporta; no se interpreta.

## 3. Los 15 sistemas y sus 79 planillas

| Sigla | Sistema | Planillas |
|---|---|---|
| SAA | Sistema de Abastecimiento de Agua | 6 |
| SAL | Sistema de Extinción por Agentes Limpios | 4 |
| SAP | Sistema de Agua Pulverizada | 5 |
| SBC | Sistema de Bombas Contraincendios | 6 |
| SCC | Sistema Fijo de Extinción para Cocinas Comerciales | 5 |
| SDC | Sistema de Extinción por Dióxido de Carbono | 5 |
| SDI | Sistema de Detección de Incendios | 5 |
| SEP | Sistema Fijo de Extinción por Polvo | 3 |
| SGE | Sistema Generador de Espuma | 7 |
| SHC | Sistema de Hidrantes Contra Incendios | 3 |
| SIM | Simbología de Seguridad contra Incendios | 2 |
| SRA | Sistema de Rociadores Automáticos | 9 |
| SRE | Sistema de Rociadores de Espuma | 7 |
| SSA | Sistema Fijo de Extinción por Solución Acuosa | 4 |
| STM | Sistema de Tuberías y Mangueras | 8 |
| | **Total** | **79** |

El detalle de cada planilla (código, nombre, frecuencia, formato, cantidad de ítems) está en la hoja **Inventario** del Excel adjunto.

## 4. Los cuatro formatos que tiene que resolver el formulario

Todas las planillas comparten el encabezado (Cliente, CUIT, Teléfono, Dirección, Edificio, Sector, Empresa mantenedora, N.° mantenedor certificado, Inspector, Sistema/Designación, Fecha), observaciones, firmas y la leyenda **CUMPLE ✓ · NO CUMPLE O · NO APRECIABLE X**. Lo que cambia es el cuerpo:

| Formato | Planillas | Cómo se reconoce en el Excel | Cómo se carga en readyproof |
|---|---|---|---|
| **A. Datos generales** | 14 (todas las `-1` de Información general) | Etiquetas `Campo:` y opciones con `☐` | Texto o número según el campo. Si hay `☐`, selector con esas opciones exactas (135 campos tienen opciones). |
| **B. Grilla semanal** | 8 | Columnas `S1 … S5`, `MES` | Por ítem, selector de 3 estados (✓ / O / X) para la semana que se carga. |
| **C. Grilla mensual** | 11 | Columnas `ENE … DIC`, `AÑO` | Por ítem, selector de 3 estados (✓ / O / X) para el mes que se carga. |
| **D. Verificación** | 46 | Columnas `VERIFICACIÓN`, `VALOR`, `CUMPLE ✓`, `NO CUMPLE O`, `NO APREC. X`, `NA` | Por ítem, selector de 4 estados (✓ / O / X / NA). Si la fila trae `_____ unidad` (229 ítems: V, A, MPa, L/min, kg, °C, %, mm…), además un **campo numérico obligatorio** con esa unidad, salvo que el estado sea NA. |

Reglas comunes:
- **Cada ítem tiene que poder marcarse.** Un ítem sin control de estado es un error de importación (es la causa probable del caso de los detectores de humo).
- Los **bloques** se respetan: cada planilla se divide en bloques con su título (por ejemplo, en SDI-3: PRUEBA TRIMESTRAL / PRUEBA SEMESTRAL / PRUEBA ANUAL; en SBC-6: CAUDAL CERO / CAUDAL NOMINAL / CAUDAL MÁXIMO…). Si el bloque trae `FECHA:`, ese bloque tiene su propia fecha.
- En una planilla con varias frecuencias (por ejemplo, SDI-3 trimestral, semestral y anual), el técnico elige qué bloques realiza en esa visita; los demás quedan vacíos y no son obligatorios.
- Un ítem marcado **O (No cumple)** obliga a escribir una observación.
- No se guarda ni se emite una planilla con ítems obligatorios sin marcar; el formulario muestra cuáles faltan.

### Grillas semanales y mensuales (decisión por defecto)
- **Mensual:** una carga por mes. El PDF arma la grilla anual (ENE–DIC) con las cargas ya emitidas de ese cliente, sistema, planilla y año.
- **Semanal:** una carga por semana. El PDF arma el mes (S1–S5) con las cargas de ese mes.
- Si esto complica el modelo actual, **detenerse y proponer alternativa antes de implementar.**

### Información general (formato A)
Se completa al dar de alta el sistema de un cliente y queda guardada para las cargas siguientes, con historial de cambios (quién y cuándo). No se vuelve a pedir en cada visita.

## 5. Navegación en la app

1. El técnico busca el **cliente** por CUIT o razón social (o lo da de alta si no existe) y elige el establecimiento.
2. Elige el **sistema** de un desplegable con **los sistemas que tiene ese cliente**. Desde ahí mismo puede agregar un sistema nuevo de los 15.
3. Aparecen las **planillas de ese sistema**, cada una con su frecuencia visible (Semanal, Mensual, Trimestral, Semestral, Anual, 3 años, Quinquenal, etc.) y la fecha de la última carga.
4. Elige la planilla y completa el formulario. El encabezado y la Información general ya vienen cargados.

## 6. Manuales

Hoy los manuales de la migración 006 son ficticios. Reemplazarlos por los **15 manuales reales** de la Serie v5 (`SG-PEM-IFI-<SIGLA> <Nombre>.docx`) y vincular cada planilla con el manual de su sistema por la sigla. Esto se hace con una migración aditiva y sin borrar datos.

## 7. Cómo implementarlo

**No cargar planillas a mano.** Escribir un **importador** que lea los 79 Excel v5 y genere las definiciones (JSON o tablas), con estas condiciones:
- Determinístico e idempotente: correrlo dos veces da el mismo resultado y no duplica nada (respetar el lock que ya existe).
- Guarda la **fila de origen** del Excel en cada ítem, para auditoría.
- Detecta el formato por los encabezados de columna (sección 4), no por el nombre del archivo.
- Al terminar, compara contra `catalogo_referencia_planillas.json`: por planilla, cantidad de bloques e ítems, texto de cada ítem y unidades. **Toda diferencia se reporta**: no se ajusta el importador para que "dé igual" sin explicar quién tiene razón, si el Excel o el catálogo.
- Las 16 definiciones actuales (SAA-1, SDI, SBC y SAL) se **comparan** con lo que genera el importador. Las diferencias se documentan y se corrigen como versión nueva, sin romper cargas ni PDF históricos.

## 8. Etapas y puntos de control

**Etapa 0 — Diagnóstico (sin modificar código). Detenerse y reportar.**
1. Listar qué planillas existen hoy en la app y de dónde salen.
2. Para cada una de las 15 de SDI, SBC y SAL, más SAA-1: comparar ítem por ítem contra el Excel v5 y decir qué falta, qué sobra y qué ítems no tienen control para marcar.
3. Confirmar si **"Detectores de humo" en SDI-2** ya se puede marcar desde la migración 009. Cuando Jorge lo reportó, el servidor solo tenía habilitada SAA-1 para el cliente de prueba. Si sigue fallando, explicar la causa exacta.
4. Proponer los cambios de modelo que hagan falta para los 4 formatos (estado de 3 o 4 valores, valor numérico con unidad, bloques con fecha, opciones ☐, grillas acumuladas).
5. Describir cómo están hoy los modelos `Cliente` y `Sistema` y cómo se adaptan a las secciones 1.1 a 1.3: CUIT único, establecimientos, sistemas del cliente, numeración.
6. Informar si hoy existe algún backup en el servidor y dónde.

**Etapa 1 — Backup a Google Drive** (sección 1.4). Va primero para proteger los datos antes de cualquier migración. Detenerse para que Jorge autorice Drive, y entregar la prueba de restauración.

**Etapa 2 — Clientes, establecimientos y sistemas del cliente** (secciones 1.1 y 1.2), más la numeración (sección 1.3). Los datos que ya existen se migran sin perderse. Si hay clientes sin CUIT o con CUIT repetido, **se reportan y no se inventan**.

**Etapa 3 — Importador y verificación de las 16 existentes.** Construir el importador (sección 7) y compararlo contra las 16 planillas ya habilitadas y contra el catálogo. Las diferencias se corrigen como **versión nueva** de la planilla. Nunca se reescribe una versión que ya tiene cargas.

**Etapa 4 — Desbloqueo, datos dinámicos y validación con SDI.** Validar SDI-1 a SDI-5 de punta a punta: buscar cliente por CUIT, elegir su sistema, cargar, guardar offline, sincronizar (con número asignado), PDF y envío. Detenerse y mostrar los PDF.

**Etapa 5 — Las 63 planillas restantes** (los 11 sistemas que faltan) con el mismo importador.

**Etapa 6 — Búsqueda de planillas** (sección 1.3), **continuidad y actualizaciones** (sección 1.5), **pendientes de entrega** (sección 1.6) y **auditoría final** (sección 10).

> El **desbloqueo** (1.5) y los **datos dinámicos** (1.7) no son una etapa aparte: se construyen junto con el formulario en la Etapa 4 y se validan en el piloto de SDI, antes de pasar al resto.

## 9. Restricciones (no negociables)

- Migraciones **solo aditivas.** No borrar ni alterar cargas, envíos ni usuarios existentes.
- No romper las **232 pruebas** actuales.
- No modificar `fuente/` (32 archivos).
- Mantener lo que ya funciona: logo y marcas de agua de readyproof, leyenda IRAM ("Planilla conforme a IRAM 3546:2011", ambas páginas), firmas en canvas, DNI obligatorio del firmante responsable, carga offline (IndexedDB) y envío por Gmail.
- **No desplegar** en el servidor DigitalOcean (67.205.170.29) sin aprobación explícita de Jorge.
- Sin infraestructura ni servicios pagos nuevos.
- No inventar ítems ni textos normativos.

## 10. Pruebas obligatorias

1. **Por planilla (79):** se renderiza el formulario, cada ítem tiene su control, la cantidad de ítems coincide con el Excel y se genera el PDF con datos de ejemplo.
2. **SDI-2:** test específico de que "Detectores de humo" acepta ✓, O y X, se guarda y sale en el PDF.
3. **Valores:** un ítem con `_____ MPa` no se puede guardar sin valor (salvo NA) y el valor sale en el PDF con su unidad.
4. **No cumple:** un ítem en O exige observación.
5. **Grillas:** tres cargas mensuales de la misma planilla y el mismo cliente generan un PDF con los tres meses en la grilla anual.
6. **Importador:** dos corridas seguidas no cambian nada.
7. **CUIT:** rechaza formato inválido y dígito verificador incorrecto, y no deja crear un cliente con un CUIT repetido, tampoco escrito con o sin guiones.
8. **Sistemas del cliente:** un cliente con dos sistemas del mismo tipo los muestra por separado, y la Información general de uno no se mezcla con la del otro.
9. **Continuidad:** una carga del mes siguiente encuentra al cliente, su sistema y su Información general sin volver a cargarlos.
10. **Numeración:** dos cargas offline que sincronizan al mismo tiempo reciben números distintos y correlativos, sin saltos ni repetidos.
11. **Búsqueda:** encuentra una planilla por número, por CUIT y por rango de fechas.
12. **Backup:** se genera, se cifra, se sube y se restaura en una base aparte con los mismos datos. Si la copia falla, sale el aviso.
13. **Precarga:** una carga nueva trae los datos fijos de la anterior y deja vacíos los estados, valores, observaciones y firmas.
14. **Desbloqueo:** una planilla emitida se desbloquea con motivo, se edita y se reemite con el mismo número y la revisión siguiente. La versión anterior y su PDF siguen disponibles, y queda registrado quién, cuándo, por qué y qué cambió. Un usuario sin permiso no puede desbloquearla.
15. **Anulación:** la planilla anulada queda visible como "Anulada" y su número no se reutiliza.
16. **Datos dinámicos:** cada lista de la sección 1.7 carga sus opciones, filtra mientras se escribe, permite "Agregar nuevo" y funciona offline. Lo agregado offline no duplica CUIT ni DNI al sincronizar.
17. **Usuarios:** ninguna pantalla, correo ni PDF presenta a los usuarios como de BRAFEMAR. "Empresa mantenedora" sale de la configuración y no está fijo en el código.
18. **Actualización:** tras publicar una versión nueva del formulario, el dispositivo la recibe sin borrar caché, y una carga offline vieja sincroniza sin perder datos.
19. Suite completa en verde y `compileall` sin errores.

## 11. Entregables

1. Informe de la Etapa 0 (antes de tocar código).
2. Tabla de las 79 planillas con: código, formato detectado, bloques, ítems importados, ítems en el catálogo, diferencias y estado (Cargada / Con observaciones / Pendiente).
3. Lista de diferencias entre el importador y el catálogo, con la explicación de cada una.
4. Un PDF de ejemplo por sistema (15).
5. Resultado de las pruebas (cantidad aprobada, fallida y omitida).
6. Lista de archivos modificados y migraciones nuevas.
7. `docs/BACKUP_Y_RESTAURACION.md` con el procedimiento probado.
8. Listado de clientes existentes con su CUIT y los problemas encontrados (faltantes o repetidos).
9. Estado de cada pendiente de la sección 1.6 y la guía de entrega para BRAFEMAR.

## 12. Cuándo detenerse y preguntar

- Al terminar la Etapa 0, la Etapa 1 (para autorizar Drive) y la Etapa 4.
- Antes de pasar de modo piloto a modo real (sección 0).
- Si hay clientes existentes sin CUIT o con CUIT repetido.
- Antes de emitir planillas reales: confirmar con Jorge el valor de "Empresa mantenedora" y "N.° mantenedor certificado" (sección 1.0).
- Si el Excel tiene algo ambiguo: una fila sin estado claro, una unidad rara, celdas combinadas que confundan el orden.
- Si un cambio de modelo obliga a modificar datos existentes.
- Si una prueba existente falla y la corrección cambia un comportamiento ya aprobado.
