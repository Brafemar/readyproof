# Identidad readyproof

Jorge autorizó sustituir la identidad anterior en toda la aplicación, documentación, kit de referencia y PDF históricos locales. El cambio incluye el subtítulo de acceso y carga: **readyproof · REGISTROS DE SERVICIO**.

Se actualizaron los textos de la interfaz, el valor predeterminado de empresa mantenedora, su validación, los metadatos PDF, los comentarios y documentos del proyecto y las imágenes de encabezado de las plantillas. Se conserva el logo readyproof suministrado; no se inventó otro. La caché PWA utiliza `readyproof-identidad-v2` para renovar los recursos guardados.

## Archivos y controles

- 20 PDF históricos locales: nombre, metadatos y logos revisados; misma cantidad de páginas y mismo contenido técnico al sustituir la identidad. Las imágenes de firmas y sellos conservan sus píxeles. Se admiten referencias PDF compartidas/repetidas a un mismo encabezado, sin tratarlas como cambios de la imagen.
- 4 plantillas Word: logos y texto actualizados; 34 páginas renderizadas con LibreOffice y revisadas visualmente.
- 12 archivos Excel: reemplazo dirigido de XML e imágenes dentro del paquete, conservando partes, fórmulas, filas y estructura. Se conserva el encabezado VML que se perdería al reconstruir las planillas con otras bibliotecas.
- 31 vistas PNG y 4 comparaciones renovadas desde los documentos actualizados. Las capturas de interfaz se renovaron con las pruebas de navegador.
- Búsqueda del nombre anterior en app/, docs/, fuente/, scripts/, tests/ y documentos raíz: sin coincidencias textuales activas.

Los originales están en `bak/identidad_previa_2026-10-26.zip`. El archivo conserva también las vistas anteriores y las definiciones previas del catálogo. Las huellas y aprobaciones históricas siguen refiriendo a esos originales; no deben interpretarse como huellas de la nueva copia con identidad actualizada. Los PDF/EML emitidos almacenados en la base y los mensajes ya enviados se conservaron como registros originales, sin reescribirlos.

## Versiones y datos existentes

El cambio de generador y modelo modifica su SHA256. Se registró la versión interna del piloto `00-26-rp1` y el catálogo JSON `v2`, manteniendo las anteriores. La revisión formal impresa de la serie no se renumeró: no se modificaron contenidos normativos.

Los cuatro JSON se actualizaron mediante las funciones del conversor del proyecto. Se verificó igualdad de campos, orden, opciones, datos y origen; cambian la versión y la huella del generador. Los manuales asociados mantienen su versión porque no cambió su contenido técnico.

La selección de planillas ofrece las versiones vigentes y conserva el acceso por identificador a registros anteriores. La prueba de regresión comprueba que registrar la identidad nueva no sobrescribe versiones previas.

La base del ejemplo local estaba detenida. Se volvió a iniciar el clúster existente con `pg_ctl`, sin reinicializarlo. Mediante los comandos existentes `init-db --ejemplos` y `cargar-planillas` se agregaron cinco versiones, pasando de 5 a 10 filas de plantillas. Se verificó que las versiones anteriores, las cuatro cargas, sus firmas y las credenciales quedaran iguales. No se usaron ediciones manuales de tablas para aplicar el cambio.

El ejemplo vuelve a estar disponible en [readyproof local](http://127.0.0.1:8765/login), con correo en modo de prueba y sin worker. Se comprobó HTTP 200 y el subtítulo actualizado. La ejecución local de esta revisión utiliza `out/identidad_readyproof/servidor_local.py` sobre la misma base; el estado de conexión queda en `out/etapa3/demo_local/servidor.json`. Para ver el cambio en una pestaña ya abierta, recargar con **Ctrl+F5**.

## Verificación final

**151 passed in 387.01s (0:06:27)**, código 0; `python -m compileall app scripts/recuperar_admin_local.py`, código 0. No se instalaron dependencias ni se usó Git, se publicaron servicios o se enviaron correos.

Los intentos de prueba con temporales largos fallaron en la limpieza del perfil de LibreOffice en Windows. Se resolvió usando una ruta temporal corta y exclusiva. La propuesta de reintentar la limpieza no resolvía esa causa y se retiró. Los primeros cuatro fallos de equivalencia JSON revelaron la huella anterior del generador; se resolvieron con el versionado y la exportación verificada, sin quitar controles ni cambiar contenido técnico.

Resultados, renders y comparación de fórmulas e imágenes en `out/identidad_readyproof/`. La recuperación de `msanchez` es una operación separada, autorizada por Jorge y pendiente de ejecución en su consola: ver `docs/DIAGNOSTICO_ACCESO_ADMIN.md`.
