# Alta de cliente por CUIT a demanda

Contrato confirmado sin red en la colección pública guardada en
`out/grillas_firmas/contabilium_publico_580119.json`,
`$.item[8].item[0].request.urlObject.query[1]`: `filtro` permite buscar
por CUIT, número de documento, razón social y nombre. El método es
`GET /api/clientes/search`; la respuesta es `Items`, con `TipoDoc` y
`NroDoc`. El adaptador anterior usa ese parámetro en `APIContabilium.buscar`.

En Agregar cliente, ingresar el CUIT y tocar Buscar CUIT en Contabilium.
Se hace una sola búsqueda con `filtro` y `pageSize=50`. La respuesta debe
contener una única coincidencia exacta normalizada de tipo CUIT. Un resultado
incompleto o duplicado genera un error y conserva lo cargado. Se mantiene
el timeout de 15 segundos y el manejo de errores sin reintentos del adaptador.

Solo se completan nombre, domicilio, teléfono y correo vacíos. Los valores
manuales se conservan, incluso si se escribieron durante la consulta. Si no
hay coincidencia, se informa que puede usarse Consultar ARCA; esa acción
manual completa razón social y domicilio fiscal vacíos. El resto se carga
a mano. Ninguna consulta crea ni modifica la ficha: Guardar cliente sigue
siendo una acción manual. No se consulta Contabilium al abrir la página.

El endpoint local `GET /api/admin/contabilium/cliente-por-cuit?cuit=...`
requiere administrador y modo REAL, y responde `encontrado` y `cliente`.
Conserva la auditoría de accesos existente de la aplicación, que escribe en
su base al atender rutas API. Esta preparación no hace requests a producción.

Las pruebas usan transporte simulado y PostgreSQL temporal de pruebas.
No se consultó la API real para verificar el filtro ni se desplegó el cambio.
