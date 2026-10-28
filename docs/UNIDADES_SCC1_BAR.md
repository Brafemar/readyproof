# SCC-1: nueva versión en bar

Autorización: Jorge Sánchez, 28/10/2026; decisión de Martín comunicada por Jorge. Se confirma bar para los campos de presión y se conservan los cuatro estados de SDI (✓/O/X/NA).

La migración 017 agrega SCC-1 `00-26-bar1`. Su única diferencia de contenido frente a `00-26-ms1` es la unidad del campo J21 «Presión normal a 20 °C», del bloque «DATOS DE LA PLANILLA IRAM 3546-16A»: MPa pasa a bar. El otro campo de presión de SCC-1 ya indicaba bar. No se agregan unidades a verificaciones cualitativas; SDI conserva sus filas y estados. Esta corrección no cambia unidades de otros sistemas, como SSA.

La aplicación usa el generador existente con una especificación versionada. No se modifica ningún archivo de `fuente/`, ni el catálogo original congelado. La migración inserta una fila de plantilla y un marcador de esquema; conserva íntegramente las filas anteriores, los PDF, las firmas y los valores cargados. No cambia el certificado ni las cabeceras de documentos históricos.

Las cargas nuevas de SCC-1 usan la versión en bar. Los valores deben ingresarse en bar; no se copian ni convierten automáticamente mediciones históricas en MPa. Los borradores antiguos vinculados a SCC-1 en MPa no se reinterpretan como bar: requieren una carga nueva revisada por el técnico. Los PDF emitidos anteriormente conservan su contenido y acceso autorizado.

Las pruebas verifican ambas versiones, sus identificadores distintos, la única diferencia del esquema, el selector y un valor 23 que permanece 23 bar en el Excel nuevo. La emisión completa de SCC-1 comprueba además que el PDF nuevo contiene bar y no MPa. Un ensayo de migración sobre una copia aislada compara todas las filas anteriores antes de aplicar a la instalación activa.
