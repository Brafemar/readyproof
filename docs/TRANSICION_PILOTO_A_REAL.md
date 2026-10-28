# Transición del piloto al uso real

Fecha: 28/10/2026. Esta lista debe revisarse con Jorge y Martín. Tener código configurable no autoriza el uso real ni da por completado un requisito sin evidencia.

## Cliente y sistemas

- [ ] Jorge confirma el cliente, sus permisos y responsables.
- [ ] Se crea el cliente correspondiente sin convertir uno ficticio.
- [ ] CUIT normalizado y dígito verificador validado cuando se informe; su obligatoriedad no se inventa por esta lista.
- [ ] Domicilio, contacto y sector/edificio se registran en los campos existentes de la planilla.
- [ ] Se comprueba si se necesita gestión independiente de establecimientos; ese alcance ampliado no se declara implementado.
- [ ] Las 15 familias están disponibles; se crean solo las instalaciones reales que correspondan, sin inventar 15 instalaciones para un cliente.
- [ ] Cada instalación está vinculada al cliente correcto y activa.
- [ ] El técnico tiene acceso únicamente a los clientes asignados.

## Mantenedora y decisiones normativas

- [ ] Jorge confirma EMPRESA_MANTENEDORA exacta, sin marcadores ficticios.
- [ ] Jorge y el responsable técnico confirman CERTIFICADO_N y su vigencia.
- [ ] Los valores de cabecera coinciden con la configuración al emitir.
- [ ] Martín confirma SCC-1: MPa del kit frente a bar del encargo. No se cambian valores/unidades sin esa decisión.
- [ ] Si corresponde corregir SCC, se realiza una migración posterior independiente; 016 está asignada a auditoría, no a unidades.
- [ ] Martín confirma SDI y sus cuatro estados actuales (✓/O/X/NA) frente al pedido de tres.
- [ ] Se resuelven las demás decisiones normativas pendientes y asociaciones con manuales reales.
- [ ] Se decide el calendario S1–S5 sin reinterpretarlo automáticamente.

## Carga, validación y firma

- [ ] Se verifica O + observación y la medición obligatoria solo en el alcance autorizado de verificación.
- [ ] Se conservan los tipos, filas, orden y opciones del kit.
- [ ] Se comprueba el cambio entre las 79 planillas y las 15 familias disponibles.
- [ ] Se verifica guardado y recuperación de datos por sistema.
- [ ] Se decide/completa el alcance de listas dinámicas, precargas, establecimientos y anulación que siga pendiente; no se simula con ejemplos.
- [ ] Nombre, DNI de 8–15 dígitos y ambas firmas se comprueban.
- [ ] El técnico revisa una planilla completa desde el dispositivo que usará.
- [ ] El trabajo sin conexión se sincroniza y resuelve conflictos sin pérdida ni duplicados.

## Numeración y PDF

- [ ] El número se asigna al emitir y un fallo no lo consume.
- [ ] Original con revisión pública 0 y correcciones 1+ conservan el número.
- [ ] El desbloqueo exige creador/admin, cliente autorizado y motivo.
- [ ] PDF anteriores descargables e idénticos, sin reescritura.
- [ ] Nuevos PDF indican REAL y contienen mantenedora/certificado confirmados.
- [ ] Se revisan visualmente los datos reales de cabecera sin recortes; logos, IRAM, firmas y marcas de agua permanecen legibles.
- [ ] Se conserva la paginación A4 horizontal del kit.

## Búsqueda y auditoría

- [ ] GET /api/carga/buscar?numero=XXX encuentra un registro del cliente autorizado.
- [ ] Un técnico no obtiene datos de otros clientes.
- [ ] Auditoría registra INSERT, UPDATE y DESBLOQUEO con actor, snapshots y motivo.
- [ ] GET /api/auditoria es exclusivo de administradores y pagina/fíltra correctamente.
- [ ] Se conoce la limitación de cobertura: los hooks actuales registran cargas, no cualquier escritura SQL de cualquier tabla.

## Seguridad, correo y respaldo

- [ ] Credenciales fuera del repositorio; `.env` y sus variantes excluidos.
- [ ] Acceso privado cifrado/túnel propio o HTTPS autorizado, sin compartir claves de root.
- [ ] Permisos privados y usuario de servicio comprobados.
- [ ] Compilación código 0 y suite completa posterior aprobada.
- [ ] Cobertura Python medida ≥85 %, con alcance y archivo de evidencia; no se confunde con cobertura JavaScript.
- [ ] Backups diarios cifrados a Drive y alertas de fallo configurados.
- [ ] Se ejecuta un respaldo después de la última migración y se verifica la descarga.
- [ ] Se restaura una copia en una base aislada, comparando tablas, binarios y PDF.
- [ ] Se conserva una clave de recuperación accesible a las personas autorizadas.
- [ ] MAIL_MODO_PRUEBA y el transporte corresponden a la operación autorizada.
- [ ] Jorge confirma destinatarios reales antes del primer envío.
- [ ] Se revisan los envíos de resultado indeterminado sin repetirlos automáticamente.

## Autorización final y ejecución posterior

- [ ] Jorge revisó y aprobó cada punto y los pendientes que correspondan quedaron resueltos.
- [ ] Martín confirmó las decisiones normativas anteriores a la operación real.
- [ ] Se registra la autorización explícita para cambiar MODO_PILOTO a false; esta entrega no la sustituye.
- [ ] Se realiza respaldo previo y se conserva la configuración anterior de forma privada.
- [ ] Se cambian únicamente los parámetros autorizados en el entorno privado; nunca se commitea `.env`.
- [ ] Se reinicia, se recarga en línea y se verifica una primera operación con personas autorizadas.
- [ ] Se registra la transición y se crea un tag de liberación real únicamente después de verificarla; el tag de etapa 6 piloto no habilita uso real.

## Monitoreo durante los primeros días

Jorge designa una persona responsable por turno. Revisar errores y cambios de auditoría cada dos horas durante la operación, los envíos y resultados indeterminados, y el respaldo nocturno al comenzar la jornada siguiente. Registrar incidentes sin contraseñas, tokens ni firmas en capturas públicas. No se crea una automatización de avisos por este documento.

Ante inconsistencias de datos, permisos, numeración, hash o respaldo: detener nuevas emisiones/envíos, preservar evidencia y avisar a Jorge. Escalar las dudas normativas a Martín. No borrar cargas, renumerar, reenviar un resultado ambiguo ni restaurar sobre producción para probar. Una reversión de configuración debe quedar autorizada y documentada, conservando los registros y PDF ya emitidos.


## Aprobación y ejecución posterior

Jorge aprobó el checklist el 28/10/2026 y autorizó la transición con READYPROOF / IFI-2024-10001. Confirmó bar para presión y los cuatro estados de SDI. La ejecución y evidencia están en [TRANSICION_EXITOSA.md](TRANSICION_EXITOSA.md). Esta lista se conserva como plantilla de revisión; no declara implementadas funciones adicionales del backlog.
