# Diagnóstico del recorrido A4 histórico

Fecha: 28/10/2026. Corrección autorizada por Jorge después de la detención de auditoría.

La prueba real es `tests/test_a4_historica.py::test_copia_a4_conserva_pdf_anterior`; el navegador se controla desde `tests/browser/a4_historica.cjs`. No está en `tests/test_desbloqueo.py`.

## Qué verifica

La fixture guarda un PDF histórico ficticio de dos páginas en PostgreSQL temporal, con firmas ficticias. El navegador entra por el login normal, recupera esa carga desde IndexedDB, comprueba sus controles de solo lectura y crea una copia actual. Completa los datos del responsable, solicita vista previa y emite. Al terminar, la prueba exige que el PDF anterior siga siendo idéntico byte a byte, que la copia tenga otro ID y use la versión actual, y que el nuevo PDF tenga una hoja A4 horizontal y cuatro imágenes.

## Fallo y evidencia

La primera tanda Windows falló en `tests/test_a4_historica.py:41`, al recibir código 1 de Node. El mensaje fue `page.waitForResponse: Target page, context or browser has been closed`, referido a la espera de `/emitir`.

El navegador se cierra en el bloque `finally` del script. La espera de respuesta se creaba antes del clic y recién se esperaba después de que el clic terminara. Si una acción anterior falla, el `finally` cierra el navegador y esa promesa pendiente puede rechazar sin manejador, sustituyendo el error original por el cierre del contexto. La vista previa usaba el mismo patrón.

Se realizó una sola reproducción diagnóstica sin cambiar el test, con `NODE_OPTIONS=--unhandled-rejections=warn` para evitar que ese rechazo secundario impidiera observar un eventual error original. Esa ejecución pasó. Por lo tanto, el disparador inicial de la intermitencia no quedó recuperado en la traza; no se atribuye sin evidencia a lentitud de LibreOffice, bloqueo del PDF o corrupción de datos.

## Corrección

- Espera de respuesta y clic se gestionan juntos con `Promise.all`, tanto en vista previa como en emisión.
- Antes de emitir, se espera que el diálogo de vista previa esté oculto y el botón Finalizar habilitado.
- La espera de «Vista previa lista» usa el timeout de 90 segundos explícitamente en el tercer argumento de `waitForFunction`, consistente con el límite de respuesta ya existente.
- Se mantienen los límites de 90 segundos para las respuestas, 30 segundos por defecto para las acciones y 150 segundos para el proceso Node. No se agregan pausas fijas, reintentos automáticos ni excepciones ignoradas.
- Se conserva el `finally` para liberar el navegador; las promesas quedan gestionadas y un fallo futuro conserva su error correspondiente.

La aplicación, el generador, las planillas fuente, las validaciones y los documentos históricos no se modifican por esta corrección.

## Validación y trazabilidad

Primera ejecución normal tras la corrección: **1 passed en 41,24 segundos**, con las comprobaciones del PDF anterior y la copia nueva intactas. La tanda completa Windows posterior aprobó **46 casos en 379,47 segundos**. La tanda Linux posterior también aprobó sus 479 casos. Resultado consolidado posterior al arreglo: **525 aprobadas, cero fallos y cero omitidas**, en dos plataformas, documentado en `AUDITORIA_ETAPAS_0_A_5.json`. No es una sola invocación ni una reutilización de la suite anterior al arreglo.

Commit del arreglo: `b750f79cbc1700b411aba245481dbd003bf2b0a5`, «Fix: corregir test_copia_a4 — timeout/sincronización». Ambos archivos de prueba estaban sin seguimiento previo; el commit los incorpora y conserva las aserciones de integridad. La auditoría mantiene el primer fallo y la reproducción diagnóstica en `out/auditoria_punto6/`, además de los JUnit posteriores.
