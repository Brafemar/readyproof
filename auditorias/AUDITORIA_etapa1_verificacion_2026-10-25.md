# Verificación de las correcciones de la etapa 1 de readyproof

## Resumen

- **Etapa auditada:** 1, planilla piloto SAA-1. Esta es la segunda revisión: verifica las correcciones de los hallazgos de `AUDITORIA_etapa1_2026-10-25.md`.
- **Fecha:** 25/10/2026.
- **Resultado general:** **APTA CON OBSERVACIONES**.
- **Hallazgos nuevos:** 0 críticos, 0 mayores y 2 menores.

Los once hallazgos de la primera auditoría están corregidos, o bien registrados como decisión pendiente de Jorge o de Martín, como se pidió.

Esas decisiones pendientes no son defectos de la etapa 1, pero **M1 bloquea la emisión a clientes reales** mientras Martín no confirme la leyenda.

---

## Estado de los hallazgos anteriores

| Hallazgo | Estado | Verificación |
|---|---|---|
| M1. Leyenda IRAM ausente en el PDF | Registrado como pendiente de Martín | Está en `PREGUNTAS_ABIERTAS.md` como bloqueo de la emisión real. La prueba `test_pdf_contiene_leyenda_iram_pendiente` es `xfail` estricta: cuando se agregue la leyenda, la prueba va a avisar que hay que quitar la marca. |
| M2. Cambio en `build_planilla.py` sin aviso a Martín | Registrado como pendiente de Martín | Anotado en el registro, con su alcance de 79 planillas, y en `PREGUNTAS_ABIERTAS.md`. `fuente/` no volvió a cambiar: la fecha de modificación de `build_planilla.py` sigue siendo la del 25/10 a las 19:49. |
| M3. Verificación visual no reproducible | Corregido | `requirements-dev.txt` fija `pypdfium2==5.14.0`. La comparación píxel a píxel ahora es la prueba `test_blanca_identica_pixel_a_pixel_en_todas_las_paginas`, que falla si falta la dependencia. Las imágenes se regeneraron en `out/etapa1/revision_reproducible/`. |
| M4. Sin historial de versiones | Corregido | Hay dos commits locales en `master`: b922971 («Etapa 1: piloto SAA-1 aprobado») y 5cdd862 («Etapa 1: corrección de observaciones de auditoría»). No hay repositorio remoto. Se versionan 223 archivos, sin `.env`, `.venv`, cachés ni `out/`. Los entregables aprobados están versionados en `docs/aprobaciones/etapa1/`. |
| m1. Rastros de herramientas automáticas | Corregido | Ya no hay menciones a Codex ni al sandbox en `REGISTRO_DE_CAMBIOS.md`, `docs/`, `app/`, `tests/` ni `scripts/`. |
| m2. Pruebas imprecisas | Corregido | Cada campo se verifica en la columna J de la fila de su etiqueta, con valores distintos para cada campo, y las observaciones en A36 a A39. El encabezado y el pie del PDF se comparan como texto completo contra la referencia. Al invertir a propósito el orden de los campos en una copia, la prueba falla. |
| m3. Metadatos del PDF | Corregido en parte; resto pendiente de Jorge | El título se toma de la celda T1 y tiene prueba propia. Creador y productor siguen siendo «readyproof», en espera de la decisión de Jorge, que está registrada. |
| m4. Datos de ejemplo sin prefijo | Corregido | La excepción está documentada en `docs/PILOTO_SAA1.md`. |
| m5. Falta `fix_impresion.py` | Registrado como pendiente | Anotado en `PREGUNTAS_ABIERTAS.md`. |
| m6. Dos referencias de SAA-1 | Corregido | La documentación establece `tests/referencias/SAA-1_v5.xlsx` como única referencia oficial. |
| m7. `lxml` no declarado | Corregido | `lxml==6.1.3` está en `requirements.txt`. |

## Hallazgos nuevos

### Menores

**n1. La comparación del encabezado y el pie usa coordenadas fijas de SAA-1**
- Archivo: `tests/test_generacion.py`, función `_textos_fijos_encabezado_y_pie`, con límites de 126, 70 y 130 puntos y la posición de la fecha en V4.
- Qué pasa: los límites del encabezado y del pie están calculados para SAA-1. Si se reutiliza la prueba en la etapa 6 con otras planillas, puede comparar zonas equivocadas.
- Qué hacer: antes de la etapa 6, calcular esos límites a partir de cada planilla (filas del encabezado, observaciones y firmas) en lugar de dejarlos fijos.

**n2. El README no menciona las dependencias de verificación**
- Archivo: `README.md`, sección «Desarrollo local (etapa 0)».
- Qué pasa: indica instalar solo `requirements.txt`. Sin `requirements-dev.txt`, `pytest -q` falla al recolectar las pruebas porque `pypdfium2` es obligatorio.
- Qué hacer: indicar `pip install -r requirements-dev.txt` para correr las pruebas, o remitir a `docs/PILOTO_SAA1.md`.

## Decisiones pendientes que no son defectos

- Texto y ubicación de la leyenda «Planilla conforme a IRAM 3546:2011» (Martín). Bloquea la emisión a clientes reales.
- Aviso a Martín del ajuste de formato en `build_planilla.py`.
- Creador y productor de los metadatos del PDF (Jorge).
- Integridad de la copia del kit, por la falta de `fix_impresion.py`.
- Ediciones autorizadas de NFPA 17A y NFPA 10 (ya estaba pendiente desde antes).

---

## Controles ejecutados

| Control | Resultado |
|---|---|
| Historial git (`logs/HEAD`, `refs/heads/master`) | 2 commits locales, autor configurado solo en este repositorio, sin repositorio remoto. |
| Archivos versionados (`git ls-files` sobre el índice) | 223 archivos, sin `.env` real, `.venv`, `__pycache__`, `.pytest_cache` ni `out/`. |
| `pytest -q -rxXs` (copia aislada) | `22 passed, 1 xfailed in 7.06s`, código 0. La prueba marcada como xfail es la de la leyenda (M1). |
| `python -m compileall app` | Código 0. |
| Mutación: campos de un bloque en orden inverso | `1 failed`: la prueba de ubicación lo detecta. |
| Búsqueda de rastros de herramientas automáticas | Sin resultados en los archivos entregables. |
| Integridad de `fuente/` | `build_planilla.py` conserva la fecha de la etapa 1. El registro informa 173 archivos con SHA256 sin cambios. |
| Modelos de Martín en `fuente/modelos` (ahora versionados) | Sin datos de clientes: no hay CUIT, correos ni teléfonos. Los campos de cliente del modelo -IN están vacíos. |
| Secretos | Sin cambios respecto de la primera auditoría: ninguno. |

## Limitaciones

- Ejecuté las pruebas en una copia aislada con pytest 9.1.1, pypdf 6.17, Pillow 12.3 y LibreOffice 24.2. No usé el `.venv` de Windows, porque la terminal de la computadora es solo de lectura y clic. El resultado coincide con el registrado por el desarrollador: 22 aprobadas y 1 xfail.
- No pude leer el contenido de los commits porque los objetos de git no se copiaron al espacio de revisión. Los archivos versionados los verifiqué con el índice, y los commits con el registro de referencias.
- El SHA256 de `fuente/` contra el estado anterior a la tarea se toma del manifiesto del desarrollador (`out/auditoria_etapa1/`). Yo no lo recalculé.
