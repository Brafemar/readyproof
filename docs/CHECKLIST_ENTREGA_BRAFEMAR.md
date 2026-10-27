# Checklist de entrega de readyproof

Estado revisado al 27/10/2026. Una casilla se marca solo con evidencia del entorno indicado. **Preparación local no equivale a entrega de producción aprobada.** El nombre de archivo se conserva como fue solicitado; la marca visible es readyproof.

## Aplicación y documentación local

- [x] Aplicación base verificada: 151 pruebas aprobadas en la última auditoría de logo/metadatos; compilación de app/ y tests/ código 0. Evidencia: `out/auditoria_logo_20261027/resultado.json`.
- [x] Identidad readyproof: PNG 600×150 presente, Helvetica-Bold 48 pt, gris #333333, fondo blanco y metadatos PDF readyproof.
- [x] Usuario administrador local creado: msanchez; acceso recuperado confirmado por Jorge el 27/10. No se publica su contraseña ni se considera una cuenta del futuro servidor.
- [x] Usuario técnico de ejemplo creado: tecnico-readyproof, con cliente ficticio asignado. La entrega/restablecimiento de su clave corresponde a Administración.
- [x] Guía de acceso preparada: `GUIA_ACCESO_BRAFEMAR.md`, con pantallas y límites actuales.
- [x] Guía técnica preparada: `DEPLOYMENT_DIGITALOCEAN.md`, con configuración, respaldo, monitoreo y puntos previos a publicación.
- [x] Script `scripts/prueba_operativa_final.py` preparado y ayuda CLI verificada. Cinco pruebas específicas aprobadas con PostgreSQL temporal y SMTP sustituido.
- [x] Resumen de SAA-1, SDI, SBC y SAL preparado en `MANUALES_SG-PEM-IFI.md`; SAL confirmado como Agentes Limpios.
- [ ] Registrar el resultado de la suite completa que incluye el nuevo script antes de cerrar esta entrega documental.

## Prueba operativa

- [x] Antecedente de correo del 26/10: emisión/carga ficticia por API, SMTP, mensaje en Enviados y recepción/apertura confirmadas por Jorge. Ver `FLUJO_COMPLETO_GMAIL.md`. Sus firmas se cargaron por API.
- [ ] Ejecutar el **script nuevo con msanchez** y datos `[Ejemplo]`, conservar `resultado.json` y el PDF descargado. Jorge informó que todavía no lo ejecutó.
- [ ] Confirmar SMTP del envío nuevo, un único adjunto PDF y Message-ID en Enviados.
- [ ] Confirmar recepción y apertura del PDF nuevo en destino, con logo vigente, leyenda IRAM y firmas ficticias. La aceptación SMTP sola no marca este punto.
- [ ] Completar el recorrido manual de formulario y firmas canvas; verificar en el dispositivo del técnico. Las pruebas automatizadas y los PNG por API son evidencias separadas.
- [ ] Entregar acceso técnico individual y comprobar cliente asignado y permisos desde esa cuenta.

**Prueba operativa actual OK: pendiente.** La ejecución en modo archivo o un test con SMTP sustituido no completa estos ítems reales.

## Puesta en producción

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

No hay evidencia en esta tarea para marcar HTTPS de producción, base productiva respaldada o despliegue concluido. Esta guía y sus configuraciones son entregables de preparación; no se crearon recursos ni servicios externos.

## Acta de cierre

Responsable de revisión: ____________________  Fecha: ____________________

Versión de código/plantilla y evidencia de pruebas: ____________________

URL y entorno autorizados: ____________________

Reporte de prueba operativa y confirmación de destino: ____________________

Respaldo/restauración comprobados y responsable: ____________________

Decisión final y pendientes aceptados: ____________________
