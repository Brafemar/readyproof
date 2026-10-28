# Cambios preexistentes de fuente — revisión de auditoría

Fecha Argentina: 2026-10-28T11:28:46.980160-03:00
Base de comparación Git: `4cb1599840419b3faa18496349758b663265dcca`.

La auditoría encontró cinco diferencias respecto de HEAD. No son cambios introducidos por esta auditoría. El registro anterior documenta el ajuste A4 solicitado por Jorge y la actualización de las huellas del generador. No se revierten automáticamente porque no son diferencias accidentales confirmadas.

El encargo de auditoría exige: «ACCIÓN MANUAL: Si cambios "necesarios" → detener y reportar para Jorge». Se detiene la remediación y se solicita indicación para conservar estos cambios y continuar con los demás puntos. No se modifica fuente, la aplicación ni la base de datos.

## fuente/herramientas/build_planilla.py

Solo SAA-1 se ajusta a una hoja A4 horizontal; las demás mantienen altura libre y paginación del kit.

REGISTRO_DE_CAMBIOS.md:1205; bak/build_planilla_antes_A4_20261027.py; pedido previo de Jorge de PDF SAA-1 en una hoja.

Diferencia: +2/-1 líneas. SHA256 actual: `523cb7af043fee003c2b92c1b70f65a6fa81704d50a9a6f0655f7fe61ca213bb`. SHA256 HEAD: `5be50cae29ff3ffbab3531b9aec187121c25c426173fd306b8c85e9670c56055`.

## fuente/planillas/SAA-1.json

Actualización v2 a v3 y huella del generador; resto del contenido JSON idéntico a HEAD.

REGISTRO_DE_CAMBIOS.md: ajuste A4 27/10/2026 y regeneración de JSON; datos vinculados al generador vigente.

Diferencia: +2/-2 líneas. SHA256 actual: `21b55c626bb1e2dd536887a5c0d8b43b3c0a6bbe6d5b990f4dee6a003bea111e`. SHA256 HEAD: `6d2e2d10680db907a04d073b939c030b81c1dd9e64fe3e9c7fbc547dabda16a3`.

## fuente/planillas/SAL.json

Actualización v2 a v3 y huella del generador; resto del contenido JSON idéntico a HEAD.

REGISTRO_DE_CAMBIOS.md: ajuste A4 27/10/2026 y regeneración de JSON; datos vinculados al generador vigente.

Diferencia: +2/-2 líneas. SHA256 actual: `c9663926de80698763bc9e57974b4b875d6d7a29ed9a18d070ddb8c0f3267cfd`. SHA256 HEAD: `a6894f4822f8ccbafa4dfa083340eff719c5dc6ffada479b822665f5c34a72bf`.

## fuente/planillas/SBC.json

Actualización v2 a v3 y huella del generador; resto del contenido JSON idéntico a HEAD.

REGISTRO_DE_CAMBIOS.md: ajuste A4 27/10/2026 y regeneración de JSON; datos vinculados al generador vigente.

Diferencia: +2/-2 líneas. SHA256 actual: `d743b871ccf4cc30215cd6f5928674fd9ba53fe62f13390b552aa956cfbf91f3`. SHA256 HEAD: `dcd25901769d622bb89687b6349f7b66a12effc16b2364612c4eb2d371261c94`.

## fuente/planillas/SDI.json

Actualización v2 a v3 y huella del generador; resto del contenido JSON idéntico a HEAD.

REGISTRO_DE_CAMBIOS.md: ajuste A4 27/10/2026 y regeneración de JSON; datos vinculados al generador vigente.

Diferencia: +2/-2 líneas. SHA256 actual: `e3062e44ac5c607e4288241c955ef57ba3ab74e46dd930273298bd329ffc2020`. SHA256 HEAD: `1600f32552ae55761b7e3c8efb43bc37d24c762300e18479ad28cd7d80e74a07`.

## Consecuencia de revertir sin evaluación

El generador volvería a permitir páginas adicionales en SAA-1 y los JSON volverían a declarar versión/huella anteriores. Las cargas y definiciones versionadas comprueban esas huellas; una reversión aislada puede bloquear emisiones o invalidar el catálogo. No corresponde declarar fuente intacta respecto de HEAD ni atribuir estas diferencias a la etapa 5.

## Pendiente de indicación

Conservar las cinco diferencias documentadas y continuar con .gitignore, permisos, documentación, manifiesto, pruebas y commits solicitados. No se propone cambiar unidades de SCC, filas del kit ni datos históricos.


## Decisión final de Jorge — 28/10/2026

Jorge autorizó expresamente conservar las cinco diferencias documentadas, sin revertirlas. La pausa administrativa queda resuelta y se retoma la auditoría de los demás puntos. El detalle consolidado está en CAMBIOS_AUTORIZADOS_EN_FUENTE.md. Esta decisión no autoriza nuevas modificaciones de fuente ni cambios normativos.
