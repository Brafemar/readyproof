# Etapa 2 — CUIT y sistemas activos

Fecha: 28/10/2026. Etapa completada: migraciones 011 y 012 aplicadas y modelo nuevo activo en el servidor. El modo piloto permanece activo.

## Cambios

- Migración `011_cliente_cuit_opcional`: columna `clientes.cuit`, once caracteres, opcional, restricción de unicidad, índice `ix_cliente_cuit` y control de almacenamiento de once dígitos ASCII.
- Migración `012_sistema_cliente_activo`: `sistemas.activo` obligatorio, predeterminado `true` también para los existentes; reafirma `cliente_id NOT NULL`. Si hubiera sistemas sin cliente, la migración se detiene en lugar de asignar uno arbitrariamente.
- Los identificadores conservan sus UUID y la representación `VARCHAR(36)` existente. No se convierte el tipo SQL de claves ni se cambian referencias.
- `app/utils/cuit_validator.py`: normalización de once dígitos o formato `XX-XXXXXXXX-X`; comprobación del dígito mediante módulo 11. `validar_cuit` devuelve booleano. `normalizar_cuit` rechaza tipos y formatos incorrectos con `ValueError`.
- El modelo `Cliente` normaliza y valida al asignar CUIT. `None` conserva el dato ausente de esta primera migración. No se admite una cadena vacía como CUIT válido.
- Los downgrades se detienen si quitaran CUIT registrados o el estado de sistemas inactivos. No se ejecutan downgrades en la base activa.

No se agrega un dato real, no se completa el cliente existente ni se habilita modo real. Esta etapa prepara el modelo; no incorpora todavía formularios de alta/edición de CUIT ni controles para activar/desactivar sistemas.

## Alcance del validador

La comprobación es de formato y dígito, sin consulta de existencia, inscripción o titularidad. No se agregan restricciones de prefijos no solicitadas. No se atribuye el algoritmo a IRAM: esa referencia del encargo no corresponde a la norma de las planillas.

El ejemplo `82000000000` del pedido es inválido: la suma ponderada de sus primeros diez dígitos es 48 y el verificador calculado es 7. Por eso se prueba como rechazo. Los casos positivos usan números sintéticos marcados como ejemplo; no son constancias fiscales.

Referencia de alcance: [ARCA: once dígitos y consistencia del verificador](https://www.afip.gob.ar/simplificacionregistral/alta-ya/ayuda/documentos/Errores-frecuentes-CUIL-o-CUIT-inexistente.pdf). El alcance local no acredita inscripción ante ARCA.

## Auditoría de solo lectura

Ejecutar desde `/home/readyproof`: `venv/bin/python scripts/audit_cuit.py --salida /var/backups/readyproof/audit_cuit_etapa2.json`.

El script usa una transacción PostgreSQL de solo lectura. Devuelve JSON con cantidad de clientes, IDs sin CUIT, inválidos, no normalizados, grupos duplicados y sistemas sin cliente. Puede auditar también una tabla anterior sin columna CUIT. No corrige ni elimina registros. Si se comparte un reporte de una base real, restringir el acceso: el listado de duplicados puede contener identificadores fiscales.

## Pruebas y ensayo

Las pruebas cubren normalización, longitudes y tipos, caracteres Unicode, guiones mal ubicados, verificador inválido, resto sin dígito representable, unicidad en PostgreSQL, varios NULL permitidos, estado activo predeterminado, cliente obligatorio, auditoría sin escrituras, duplicados normalizados en un esquema anterior y protección del downgrade.

El ensayo en una copia separada de la restauración 010 terminó correctamente: `readyproof_etapa2_ensayo_20261028T041207`, esquema 012, 45 cargas y 130 binarios conservados. Coinciden UUID, relaciones y conteos (salvo dos registros nuevos de versión de esquema). Evidencia: `out/etapa2_cuit/ensayo_servidor.json`.

La primera ejecución integral se interrumpió al detectar que faltaba `NODE_PATH` para Playwright. El siguiente intento reveló rutas temporales demasiado largas para el perfil de LibreOffice en Windows. El caso aislado pasó con `--basetemp .venv/tmp/j`, sin cambiar la aplicación; la suite final usa `.venv/tmp/k` y el runtime Node existente. Los intentos anteriores se conservan como diagnóstico. El resultado final fue 265 pruebas aprobadas y un error de preparación por `DiskFull`. Ese mismo caso se repitió con una base nueva y pasó: 266 casos únicos verificados, sin fallos pendientes. Los logs originales se conservan; no se presenta el resultado como 266 aprobadas en una única ejecución integral.

## Antes de exigir CUIT obligatorio

Revisar el reporte, completar faltantes mediante un flujo administrativo autorizado y resolver duplicados. Solo después corresponde una migración separada a NOT NULL. No inventar CUIT para cumplir una restricción ni usarlo como reemplazo del UUID.


## Resultado operativo

- Esquema: `012_sistema_cliente_activo`; CUIT opcional y único con índice; sistema con cliente obligatorio y activo predeterminado verdadero.
- Auditoría ejecutada en transacción de solo lectura: un cliente ficticio sin CUIT; ningún duplicado, CUIT inválido o no normalizado; ningún sistema sin cliente. Cuatro sistemas activos. No se agregó dato real ni se completó un CUIT automáticamente.
- Integridad: 980 filas históricas de 16 tablas comparadas por SHA256 de JSONB normalizado en UTC y clave primaria, cero diferencias. Se excluyeron solo las columnas nuevas al comparar con 010; la versión Alembic se verificó por separado. Se agregaron los dos marcadores de versión y un acceso normal al login.
- PDFs y firmas: los 130 binarios se conservaron. Se verificaron 48 PDFs exportados al restaurar los respaldos.
- Servicio: activo; login HTTP 200 y marca readyproof presente. Las siete fuentes desplegadas coinciden con los archivos locales normalizados.
- Durante la instalación, la máscara privada del proceso dejó el paquete utils en 0700. La prueba como usuario readyproof lo detectó y conservó el modelo anterior compatible. Se corrigió exclusivamente ese directorio a 0750 con grupo readyproof, se comprobó la importación como el usuario real y se cargó el modelo nuevo. No se repitieron migraciones ni se repararon datos manualmente; el instalador quedó corregido.
- Copia previa 010 independiente y restaurada: `readyproof-drive:readyproof-backups/pre-migrations/readyproof-pre-012-20261028T045106.tar.enc`. Se conserva fuera de la rotación diaria/mensual; no purgar sin una decisión de retención.
- Copia posterior 012 ejecutada bajo systemd, descargada y restaurada en `readyproof_test_restore_20261028T050215`. Su SHA256 coincide con el respaldo de Drive. Timer activo y último trabajo satisfactorio. La base activa no fue reemplazada por una restauración.
- Compilación: código 0. Revisión de claves privadas y tokens Google: cero coincidencias en 59 archivos Python, sin leer .env. No se usó Git ni se modificó fuente/.

Evidencia principal: `out/etapa2_cuit/resultado_etapa2.json`; auditoría en `out/etapa2_cuit/verificacion_modelos_api.json`; comparación histórica en `out/etapa2_cuit/integridad_historica.json`; logs de pytest en esa misma carpeta. En el servidor, el reporte de CUIT está en `/var/backups/readyproof/audit_cuit_etapa2.json`.
