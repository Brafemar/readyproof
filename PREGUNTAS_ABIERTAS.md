# Preguntas abiertas: readyproof

1. **NFPA 17A y NFPA 10:** falta la edición vigente de ambas. Las copias que circulan no son de fuente autorizada y no se citan ni se copian. Pendiente de compra o de acceso legítimo de BRAFEMAR. Ver `AGENTS.md`, decisión 19.
2. **Leyenda visible:** confirmar con el Lic. Martín Sánchez el texto exacto de «Planilla conforme a IRAM 3546:2011».
3. **Carpeta del proyecto:** confirmar si `readyproof/` debe quedar en `Documents` o en otra ubicación.

## Actualización 2026-10-25

- Punto 3, ubicación: resuelto con autorización de Jorge. La copia de trabajo es C:\Users\jorge\Readyproof, fuera de Documentos. La copia anterior se conserva porque tenía archivos abiertos; no se continúa allí.
- Siguen pendientes las ediciones autorizadas de NFPA 17A y NFPA 10 y la confirmación de la leyenda con Martín. No bloquean la preparación de la etapa 0.

## 2026-10-25 — Etapa 1: cotejo previo de SAA-1

1. El generador fuente/herramientas/build_planilla.py no reproduce el ajuste de impresión del Excel oficial SAA-1 de SG-PEM-IFI_Planillas_v5.zip: ancho de columna A (y las columnas del generador) 5.3 en el generado frente a 6.2 en la referencia; centrado horizontal no configurado frente a True. Los valores, los estilos de las celdas y las 44 filas coinciden. Decidir si se autoriza corregir el generador para reproducir el formato v5; no se modificó fuente/ ni se agregó un formato alternativo al adaptador.
2. No se encontró LibreOffice en PATH ni en las ubicaciones habituales revisadas. Falta autorización para descargar e instalarlo o indicar una instalación local existente. No se usó internet en esta etapa.
3. No se encontró un PDF oficial de la planilla SAA-1 en los paquetes inspeccionados. El PDF SAA de la serie corresponde al manual, no a la planilla. Confirmar si el Excel oficial v5 convertido a PDF será la referencia de comparación, o indicar el PDF de la planilla.

La etapa 1 queda pendiente de estas decisiones y de la revisión visual; no se considera completada.

## Actualización 2026-10-25 — Resoluciones de la etapa 1

- Los tres puntos del cotejo SAA-1 quedaron resueltos con autorización explícita de Jorge: generador corregido con respaldo, LibreOffice instalado y referencia PDF obtenida del Excel oficial v5.
- También se autorizó agregar pypdf y Pillow para recuperar los logos originales que LibreOffice omitía; ya están implementados, instalados y fijados en requirements.txt.
- Pendiente de aceptación: revisión y aprobación de Jorge del piloto SAA-1 y su comparación visual. Los archivos finales con logos están en out/etapa1/pdf_con_logos/ y out/etapa1/revision_con_logos/. No se avanza a la etapa 2 hasta esa aprobación.
- Siguen pendientes las normas autorizadas NFPA 17A/NFPA 10 y la confirmación de la leyenda con Martín, según los puntos originales. No se resolvieron por cuenta del desarrollo.

## Actualización 2026-10-25 — Aprobación del piloto

- Resuelto el pendiente de aceptación visual de SAA-1: Jorge aprobó el formato presentado. Etapa 1 cerrada.
- Continúan pendientes las ediciones autorizadas de NFPA 17A/NFPA 10 y la confirmación de la leyenda con Martín, conforme a los puntos originales.
