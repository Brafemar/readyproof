# Leyenda IRAM: confirmación e implementación M1

Jorge comunicó la confirmación de Martín y aceptó expresamente esta especificación:

- Texto exacto: Planilla conforme a IRAM 3546:2011.
- Ubicación: centrada, línea de base a 10 mm del borde inferior de cada página.
- Fuente: Helvetica de 8 pt.
- Color: gris 50 %.
- Aparición: todas las páginas.

La puntuación de la lista no forma parte del texto: la leyenda no lleva punto final. Se usa el texto exacto guardado en app/planillas/leyenda_iram.py.

## Espacio del pie

Antes del cambio, OBSERVACIONES de la primera página estaba a 23,62 pt del borde inferior y se superponía con la leyenda a 28,35 pt. Se informó a Jorge, quien autorizó reservar el pie reduciendo proporcionalmente el contenido del PDF cerca del 5 %, sin modificar fuente/.

La implementación aplica escala 0,95 con el contenido centrado horizontalmente y anclado cerca del borde superior. Conserva A4, dos páginas, orden de filas, opciones, encabezados, logos, marcas de agua y firmas. La leyenda se inserta después del ajuste y no se escala: mantiene exactamente 8 pt y 10 mm. El cambio de escala es una excepción de formato expresamente autorizada para permitir el pie; no se modificó el generador original ni el Excel interno.

## Flujo y verificación

Conversión → logos → marcas de agua → firmas → reserva del pie y leyenda. Se usa pypdf y Helvetica estándar del PDF, sin instalar dependencias ni fuentes. Las métricas AFM de los caracteres de la frase permiten centrarla; no se depende de ReportLab en la aplicación. El recurso tipográfico y la leyenda quedan identificados en el PDF y se rechaza una segunda aplicación.

Se comprueba texto extraído, una aparición por página, fuente/tamaño, posición, gris, A4, dos páginas, espacio libre respecto de OBSERVACIONES y rechazo de duplicación. La prueba antes xfail pasa a ser normal. La comparación de encabezado y pie se calcula por anclas FECHA/CUMPLE y altura tipográfica, sin coordenadas fijas de SAA-1; una prueba adicional desplaza/escala el PDF y verifica que la extracción siga siendo equivalente. Esto corrige el hallazgo n1 sobre esas coordenadas; el cotejo de los grupos SDI/SBC/SAL sigue pendiente.

Muestra y renders de revisión en out/etapa_m1/. El texto extraído se conserva en texto_extraido.txt. Los PDF ya emitidos y almacenados no se reprocesan; la leyenda se incorpora en nuevas vistas previas y emisiones.

## Estado de uso real

M1 se refiere a la leyenda y queda resuelto tras las verificaciones. No constituye habilitación automática de clientes reales ni certificación adicional del sistema. Se mantienen las restricciones de ejemplo, política de campos obligatorios pendiente, manuales ficticios, controles operativos/privacidad y pendientes del transporte/retención/correo. La prueba física del iPhone sigue diferida y su acceso suspendido. No se modifican .env ni credenciales, fuente/, Git o infraestructura externa.
