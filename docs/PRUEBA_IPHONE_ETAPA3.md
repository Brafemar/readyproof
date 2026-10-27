# Revisión de etapa 3 en iPhone

## Estado

> **Preparación suspendida.** Tras la consulta de seguridad de Jorge, esta vía permanece detenida. No se instaló un certificado en el iPhone ni se habilitó el acceso de red. Solo quedó un prototipo inactivo en scripts/iphone_bridge.cs, ensayado en loopback. El procedimiento siguiente es una propuesta histórica; no ejecutarlo sin una nueva indicación expresa.

Jorge indicó que el dispositivo de revisión es un iPhone. El servidor de ejemplos responde en http://127.0.0.1:8765 desde la computadora. Esa dirección pertenece a cada dispositivo y no permite acceder desde el teléfono a la computadora.

La prueba automática táctil ya pasó; el recorrido manual en un iPhone todavía no se realizó. Este documento prepara la revisión y no declara cumplido el criterio de etapa 3.

## Acceso propuesto, pendiente de autorización

- Mantener Flask y PostgreSQL de ejemplos en loopback, sin cambiar la API ni el generador de PDF.
- Preparar un acceso HTTPS temporal a la aplicación desde la red Wi-Fi local, limitado al iPhone de prueba. No publicar en internet, usar túneles externos ni configurar el router.
- Propuesta de puerto HTTPS: 8766. Si hace falta descargar el certificado al teléfono, usar el puerto 8767 exclusivamente para su certificado público, nunca para datos ni claves.
- Usar un certificado local temporal. La instalación y la confianza en el iPhone las realiza Jorge en el teléfono. No usar un certificado de producción ni guardar claves privadas en el repositorio.
- Cualquier regla de firewall necesaria debe limitarse a la IP del iPhone, los puertos de esta prueba y el perfil privado de red. Retirarla al terminar. No desactivar el firewall ni cambiar su configuración general.
- El certificado, el mecanismo concreto de acceso y la regla temporal todavía no se crearon. No se abrió ningún puerto de red. La implementación queda pendiente de la decisión de infraestructura de Jorge y de comprobar sus requisitos locales.

El acceso HTTPS con certificado confiable es necesario para probar correctamente el service worker desde el iPhone. Aceptar una advertencia de certificado o abrir por HTTP la IP de la computadora no sustituye esta preparación para la prueba de reapertura offline.

## Información necesaria después de autorizar el acceso

1. Conectar la computadora y el iPhone a la misma red Wi-Fi privada.
2. Identificar la IPv4 local del iPhone y confirmar que la red permite comunicación entre dispositivos. No se necesitan contraseñas de Wi-Fi en el chat.
3. Preparar el acceso temporal y comunicar la URL exacta y la huella del certificado público antes de que Jorge lo instale. No cambiar la confianza de certificados automáticamente.
4. Abrir Safari en navegación normal. No utilizar datos ni firmas personales reales.

## Recorrido manual de aceptación

1. Abrir la URL local HTTPS que se prepare. Seleccionar el cliente y sistema ficticios y SAA-1.
2. Usar Completar ejemplo o cargar textos ficticios con el prefijo [Ejemplo]. Comprobar que los campos y opciones sean legibles y no haya desbordamiento horizontal.
3. Esperar el guardado en dispositivo y servidor y la preparación de recursos offline. Conservar el mismo origen y el mismo navegador durante todo el recorrido.
4. Desactivar Wi-Fi y datos móviles del iPhone, manteniendo Safari abierto. Modificar una observación y dibujar ambas firmas ficticias con el dedo. Confirmar el aviso de guardado local.
5. Recargar la página sin conexión. Verificar que se recuperen el formulario, la observación y las dos firmas. La vista previa y la emisión requieren reconectarse.
6. Reconectar al mismo Wi-Fi. Esperar sincronización y comprobar que se conserve una sola carga, sin duplicaciones ni pérdida de cambios.
7. Generar la vista previa y revisar las dos páginas, encabezado, pie y firmas. Finalizar el ejemplo y descargar el PDF. Comprobar que las firmas estén en sus espacios.
8. Registrar el resultado real, modelo del teléfono, versión de iOS y problemas observados. No declarar aprobación hasta completar el recorrido.

## Cierre

Retirar el acceso de red y las reglas temporales que se hayan creado. Jorge retira del iPhone el certificado de revisión. Conservar únicamente evidencias con datos ficticios y anotar el resultado en REGISTRO_DE_CAMBIOS.md y PREGUNTAS_ABIERTAS.md.

La leyenda M1 está resuelta; eso no habilita el uso real ni levanta la suspensión de esta prueba. No se inicia la etapa 4, no se crea playwright.config.js y no se modifica fuente/ ni Git durante esta preparación.
