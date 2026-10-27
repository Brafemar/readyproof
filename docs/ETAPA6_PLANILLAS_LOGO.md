# Catálogo JSON, manuales y logo — etapa 6

## Inicio e importación

En una instalación nueva, init-db aplica las migraciones y carga los cuatro JSON si la tabla planillas está vacía. La opción --ejemplos agrega además el piloto operativo y el cliente ficticio:

```powershell
.venv\Scripts\python.exe -m flask --app app init-db --ejemplos
```

Para una base local ya inicializada, aplicar init-db y después importar explícitamente:

```powershell
.venv\Scripts\python.exe -m flask --app app cargar-planillas
```

El lanzador aislado permite revisar la misma actualización sin configurar ni usar la base habitual:

```powershell
.venv\Scripts\python.exe scripts/iniciar_ejemplo.py --cargar-planillas
```

No iniciar dos servidores en el puerto 8765. Repetir la importación idéntica no duplica filas. El importador confirma su transacción; debe usarse con una sesión dedicada, sin cambios ajenos pendientes.

## Catálogo y vínculos

Los archivos SAA-1.json, SDI.json, SBC.json y SAL.json se guardan como cuatro definiciones v1, con codigo igual al nombre de archivo y sistema_tipo SG-PEM-IFI. Cada una se vincula al manual SG-PEM-IFI-{codigo}, creado con UUID aleatorio por la migración 006. Títulos y contenido siguen siendo [Ejemplo] y campos_obligatorios permanece vacío, pendiente de confirmación técnica.

La huella de estos contenedores es SHA256 del JSON canónico de json.dumps(definicion, sort_keys=True).encode(), conforme al contrato solicitado; no es el hash de los bytes con indentación del archivo. Se rechazan conjuntos incompletos, claves duplicadas, metadatos inválidos, manuales ausentes o definiciones existentes distintas. Una edición requiere nueva versión, no sobrescribir una carga previa.

El piloto anterior SG-PEM-IFI-SAA-1, versión 00-26 y sistema SAA, conserva su manual SG-PEM-IFI-SAA-EJEMPLO, huella y definición tipada. Con los cuatro contenedores habrá cinco filas en el catálogo y cinco manuales: cuatro nuevos y el anterior. No se elimina ni transforma la historia del piloto.

La carga de los contenedores SDI/SBC/SAL no habilita todavía su formulario o emisión: contienen grupos completos (5/6/4 planillas) y requieren adaptadores y cotejo de cada PDF con el generador de la serie. El flujo operativo actual sigue siendo el piloto SAA-1. las coordenadas fijas de n1 se corrigieron al incorporar M1; siguen pendientes esas comparaciones por grupo; no se afirma que la etapa 6 completa de generación haya terminado por cargar sus metadatos.

## Migración y reversión

La revisión está en migraciones/alembic/versions/006_etapa6_planillas.py, que usa la ruta Alembic ya configurada. No se crea otro directorio alembic/versions sin configurar.

El downgrade evita el borrado general por prefijo. Solo elimina los cuatro manuales de ejemplo no modificados de esta revisión si ninguno está vinculado. Si ya se importaron planillas, se bloquea la reversión y se conservan las relaciones. Los downgrades se probaron únicamente en bases temporales; no se borran datos de la revisión local.

## Logo

El logo completo procede del PNG que proporcionó Jorge, después de inspeccionar el PDF de marca. Se guardó en app/static/logo_readyproof.png con 926×312 píxeles, incluyendo marca, descriptor y Grupo BFM. El original suministrado no se modifica.

El módulo de firmas carga y valida ese PNG. El convertidor PDF lo integra mediante el restaurador de encabezado: reemplaza el recurso izquierdo, ajusta proporcionalmente al espacio original y mantiene el sello derecho. No se superpone el logo sobre la imagen antigua ni se alteran márgenes, filas o firmas. No se cambia fuente/ ni los PDF ya emitidos. Los metadatos de autor readyproof y el valor original de empresa mantenedora no se modifican: este pedido cambia el logo.

## Verificación y límites

Las siete pruebas solicitadas verifican vínculos de SDI/SBC/SAL, conservación de SAA-1, ausencia de manual_id nulo, esquemas/huellas y el PNG incorporado en un PDF real. Se agregan cuatro pruebas de integridad y reversión. La evidencia visual de dos páginas está en out/etapa6/.

Las búsquedas de password/token/smtp en código encuentran funciones legítimas de autenticación; no equivalen a secretos. La revisión busca valores nuevos de credenciales y confirma que no se agregaron. El transporte SMTP sigue sin implementarse y no se envía ningún correo. El acceso al iPhone está suspendido, la leyenda M1 está incorporada y los demás controles de uso real siguen abiertos y no se inicia etapa 7.


## Marca de agua aprobada

Después de aprobar la muestra, Jorge autorizó integrar readyproof completo e ISO como marcas de agua automáticas, centradas y al 5,5 % de opacidad. Los dos logos siguen también en el encabezado. Se reutilizan las imágenes existentes, respetando sus proporciones; no se duplican los recursos ni se alteran textos, filas o páginas.

La marca se aplica antes de las firmas, que mantienen su intensidad. Está activa en nuevas vistas previas y emisiones, sin reprocesar PDF ya almacenados. El metadato ReadyproofMarcaAgua identifica la variante y una segunda aplicación sobre el mismo PDF se rechaza. No hay cambio de fuente/, SMTP ni acceso al iPhone.
