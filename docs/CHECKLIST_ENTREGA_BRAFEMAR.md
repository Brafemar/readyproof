# Checklist de entrega de readyproof

Estado revisado al 27/10/2026. Una casilla se marca solo con evidencia del entorno indicado. **Preparación local no equivale a entrega de producción aprobada.** El nombre de archivo se conserva como fue solicitado; la marca visible es readyproof.

## Entrega técnica privada — 27/10/2026

- [x] App operativa en DigitalOcean, 67.205.170.29, únicamente por túnel privado.
- [x] PostgreSQL exclusivo conectado; migración aditiva 008 aplicada sin cambiar claves ni cargas previas.
- [x] **190 pruebas aprobadas**, compilación código 0; reemplaza el total previo de 158.
- [x] Usuario **tecnico_readyproof** creado por API normal de administrador, login y cliente asignado comprobados; Administración devuelve 403.
- [x] Prueba técnica SAA-1 actual: una sola A4 horizontal, 119597 bytes, logo, leyenda IRAM, marcas de agua y dos firmas ficticias; enviada por Gmail HTTPS y PDF confirmado en Enviados.
- [x] Acceso SSH propio `readyproof_tunel_tecnico`, sin compartir root; abre solo 127.0.0.1:8000, bloquea PostgreSQL y comandos arbitrarios.
- [x] Documentos `ENTREGA_A_BRAFEMAR.md` y `ACCESO_TECNICO_BRAFEMAR.md` preparados para PC y Android.
- [x] Paquete privado individual con clave restringida, huella, script y guías preparado; sin contraseña de app, claves root, OAuth, SMTP o BD.
- [x] Botón **Enviar documentación por correo** disponible en Mi cuenta, correo propio, CSRF, autenticación, límites e idempotencia verificados.
- [x] Gmail HTTPS activo: readyproof.ar@gmail.com → jorgesanchezing@gmail.com, dos guías y logo, sin contraseñas; Enviados comprobado y recepción confirmada por Jorge.
- [x] Botón **Enviar PDF por correo** en la carga emitida; Gmail HTTPS real y PDF adjunto en Enviados comprobados, un intento sin duplicados. Recepción manual de esta prueba pendiente.
- [x] **LISTO PARA ENTREGA DEL PILOTO PRIVADO**, con datos y firmas ficticios.
- [ ] Cambiar la clave temporal al primer ingreso y entregar el paquete al técnico por un canal privado.
- [ ] Configurar y probar físicamente el Android del técnico, incluidas firmas canvas. El navegador móvil automatizado es una comprobación separada.
- [ ] **READY FOR GO-LIVE productivo:** pendiente de dominio/HTTPS, habilitación de datos reales, backup externo, capacidad y demás controles de producción.

Los puntos históricos de las secciones siguientes conservan sus evidencias originales; esta sección contiene el estado de la entrega actual.

## Antecedentes de aplicación y documentación local

- [x] Aplicación base verificada: 151 pruebas aprobadas en la última auditoría de logo/metadatos; compilación de app/ y tests/ código 0. Evidencia: `out/auditoria_logo_20261027/resultado.json`.
- [x] Identidad readyproof: PNG 600×150 presente, Helvetica-Bold 48 pt, gris #333333, fondo blanco y metadatos PDF readyproof.
- [x] Usuario administrador local creado: msanchez; acceso recuperado confirmado por Jorge el 27/10. No se publica su contraseña ni se considera una cuenta del futuro servidor.
- [x] Usuario técnico de ejemplo creado: tecnico-readyproof, con cliente ficticio asignado. La entrega/restablecimiento de su clave corresponde a Administración.
- [x] Guía de acceso preparada: `GUIA_ACCESO_BRAFEMAR.md`, con pantallas y límites actuales.
- [x] Guía técnica preparada: `DEPLOYMENT_DIGITALOCEAN.md`, con configuración, respaldo, monitoreo y puntos previos a publicación.
- [x] Script `scripts/prueba_operativa_final.py` preparado y ayuda CLI verificada. Cinco pruebas específicas aprobadas con PostgreSQL temporal y SMTP sustituido.
- [x] Resumen de SAA-1, SDI, SBC y SAL preparado en `MANUALES_SG-PEM-IFI.md`; SAL confirmado como Agentes Limpios.
- [x] Suite completa con el nuevo script: 156 passed in 653.01s (0:10:53), código 0. Compilación de app/, tests/ y script código 0. Evidencia: `out/entrega_documentacion_pytest_final.txt` y `out/entrega_documentacion_revision.json`.

## Prueba operativa

- [x] Antecedente de correo del 26/10: emisión/carga ficticia por API, SMTP, mensaje en Enviados y recepción/apertura confirmadas por Jorge. Ver `FLUJO_COMPLETO_GMAIL.md`. Sus firmas se cargaron por API.
- [x] Script nuevo con msanchez ejecutado; evidencia en `out/prueba_operativa_final/resultado.json`, carga `0ab4612f-3e33-4251-b79a-825fc3bd39fd`, plantilla `00-26-rp1`. PDF descargado de 198073 bytes, dos páginas, huella y verificaciones de logo, leyenda, retención y metadatos comprobadas nuevamente.
- [x] Resultado SMTP del envío nuevo registrado como enviado: intento 1 ok, 27/10/2026 06:55:40 de Argentina; Message-ID `<8cda4f14-a21a-4437-b429-4ebb2dbcf4bc@gmail.com>`.
- [ ] Verificar independientemente el Message-ID del envío nuevo y su adjunto en Enviados de Gmail.
- [x] Recepción y apertura del PDF nuevo registradas por declaración manual explícita del operador en la consola. Fuente: `resultado.json`; no constituye lectura automática de la bandeja destinataria.
- [ ] Completar el recorrido manual de formulario y firmas canvas; verificar en el dispositivo del técnico. Las pruebas automatizadas y los PNG por API son evidencias separadas.
- [ ] Entregar acceso técnico individual y comprobar cliente asignado y permisos desde esa cuenta.

**Prueba operativa por script: completada según el reporte local y su confirmación manual de recepción.** Continúan pendientes la comprobación independiente en Enviados y el recorrido manual de canvas/dispositivo. La ejecución en modo archivo o un test con SMTP sustituido no completa estos ítems reales.

## Puesta en producción

Se completó posteriormente una **instalación privada de revisión** en el servidor compartido, autorizada por Jorge; ver [acceso y evidencia](ACCESO_SERVIDOR_PRIVADO.md). Cuenta msanchez, servicio loopback, PostgreSQL exclusivo, PDF real Ubuntu, backup local/restauración y túnel SSH comprobados. Esto no marca los ítems de dominio, HTTPS, datos reales o copia externa de producción que siguen debajo.

- [ ] Accesos DigitalOcean disponibles y verificados por Jorge, sin compartir contraseñas o códigos por chat.
- [ ] Droplet nuevo, proyecto, región y costo aprobados, separado del proyecto existente.
- [ ] Ensayo Ubuntu y configuración revisada de Gunicorn/Nginx/proxy/Origin/CSRF.
- [ ] Dominio y DNS aprobados; HTTPS configurado y certificado válido, renovación probada, cookie Secure y login por HTTPS verificados.
- [ ] Base de producción inicializada y usuarios administradores creados mediante bootstrap privado; bootstrap cerrado antes de exposición pública.
- [ ] Base de producción respaldada: dump íntegro, restauración en otra base vacía, recuentos e integridad comprobados y copia externa cifrada en destino autorizado.
- [ ] Backup automático habilitado y primera ejecución exitosa registrada. El ZIP de archivos del proyecto no reemplaza este respaldo.
- [ ] Monitoreo y alertas acordados, logs privados y verificación de espacio, servicio, correo, backups y TLS.
- [ ] Retención mínima de tres años, controles de privacidad/firmas y procedimientos operativos aprobados.
- [ ] Habilitación técnica de datos reales y alcance de planillas/informes aprobados. El código actual sigue limitado a ejemplos.
- [ ] Aprobación final de Jorge y responsables técnicos, con fecha, evidencias y pendientes aceptados.

Hay evidencia de instalación privada, backup local/restauración y envío real de documentación por Gmail HTTPS. Eso no acredita HTTPS público, copia externa de la base ni habilitación de datos reales para producción.

## Acta de cierre

Responsable de revisión: ____________________  Fecha: ____________________

Versión de código/plantilla y evidencia de pruebas: ____________________

URL y entorno autorizados: ____________________

Reporte de prueba operativa y confirmación de destino: ____________________

Respaldo/restauración comprobados y responsable: ____________________

Decisión final y pendientes aceptados: ____________________


## Actualización privada — 27/10/2026: cuatro familias

- [x] Migración 009 aplicada con respaldo y registros/credenciales previos conservados.
- [x] Cuatro sistemas habilitados: SAA (1), SDI (5), SBC (6), SAL (4); 16 formularios vigentes. SAL: Extinción por Agentes Limpios.
- [x] Cambio entre las 16 planillas verificado en navegador móvil, con formularios y validaciones propios.
- [x] Los 16 PDF emitidos y descargados como tecnico_readyproof por la API normal del servidor Ubuntu; 29 páginas revisadas visualmente.
- [x] A4 horizontal, paginación del kit, logo readyproof, marcas de agua, retención, leyenda IRAM y dos firmas ficticias verificados. SAA-1: una hoja.
- [x] Documentación y correo de acceso actualizados para las cuatro familias; envío simulado/archivado comprobado, sin repetir correos reales.
- [x] Suite final: 208 pruebas aprobadas; compilación y JavaScript código 0; revisión sin secretos detectados.

Evidencia: `out/multisistema/`. Estado: piloto privado operativo; los pendientes de producción anteriores continúan vigentes.


## Cierre v1.0 — Firmantes y documentación

- [x] Migración 010 aplicada con respaldo; usuarios, claves, cargas, revisiones, firmas y PDF históricos conservados.
- [x] Nombre y DNI obligatorios del responsable; cargo opcional. DNI de 8 a 15 dígitos sin puntos ni guiones, según Jorge.
- [x] Ambas firmas e identidad autenticada del técnico exigidas por backend al finalizar y emitir.
- [x] Guardado local/sin conexión y trazabilidad de identidades por revisión probados.
- [x] Los 16 PDF con datos de firmantes emitidos y descargados en Ubuntu; misma paginación, A4 horizontal, logo, IRAM, marcas de agua y dos firmas.
- [x] Modal de destinatario editable para documentación, sin modificar el perfil; auditoría e idempotencia verificadas.
- [x] Email con cuatro familias y requisitos del responsable; pruebas archivadas y transportes simulados sin nuevo correo real.
- [x] Backlog v1.1 documentado; CUIT/CUIL y numeración no se implementan en esta ampliación.
- [x] Suite final: **232 passed in 972.26s (0:16:12)**; compilación y JavaScript sin errores, sin secretos detectados.

Evidencia: `out/final_v1/`. Continúa como piloto privado con datos ficticios y los pendientes generales de producción vigentes.
