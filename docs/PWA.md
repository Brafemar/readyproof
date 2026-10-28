# PWA de readyproof

Ver [instalación, acceso privado, funcionamiento offline y verificación](PWA_INSTALACION.md).

Esta entrega agrega manifest JSON, metadatos compartidos, cuatro iconos RP, registro común y acceso de búsqueda. Mantiene un único worker con alcance raíz y la URL registrada `/sw.js`. Los iconos se generan con `python scripts/generar_iconos_pwa.py` utilizando Pillow, ya incluido en el proyecto. Los iconos maskable tienen fondo opaco y margen de seguridad.

Verificación local aprobada: Chrome sin errores de instalabilidad, un único worker y recursos accesibles desde caché con Flask apagado y la API inaccesible. Tests PWA: 3/3 aprobados. Suite aislada Linux: 499 aprobados. La regresión Windows quedó en 46 aprobados y un error de PostgreSQL por falta de espacio; no se presenta como fallo de la PWA ni como suite completa aprobada. El resultado del despliegue remoto se registra en REPORTE_PWA_FINAL.json.
