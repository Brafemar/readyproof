# Cambios autorizados en fuente/

Fecha: 28/10/2026. Decisión final de Jorge Sánchez: **conservar las cinco diferencias preexistentes, sin revertirlas**.

La comparación completa con el commit base se encuentra en `RECORD_CAMBIOS_FUENTE.md` y en `out/auditoria_punto6/cambios_fuente.json`. Son cambios anteriores, solicitados el 27/10/2026; no son modificaciones accidentales de la etapa 5 ni cambios introducidos por esta auditoría.

| Archivo | Cambio conservado | Motivo |
|---|---|---|
| `fuente/herramientas/build_planilla.py` | SAA-1 ajustada a una página A4 horizontal; los demás códigos mantienen altura libre | Requerimiento de Jorge; revertirlo cambiaría la generación actual |
| `fuente/planillas/SAA-1.json` | Versión v2 → v3 y huella del generador | Mantener correspondencia con el generador vigente |
| `fuente/planillas/SAL.json` | Versión v2 → v3 y huella del generador | Mantener correspondencia con el generador vigente |
| `fuente/planillas/SBC.json` | Versión v2 → v3 y huella del generador | Mantener correspondencia con el generador vigente |
| `fuente/planillas/SDI.json` | Versión v2 → v3 y huella del generador | Mantener correspondencia con el generador vigente |

Se verificó que el resto del contenido de los cuatro JSON coincide con la base Git. El único cambio del generador respecto de esa base es la condición de altura para SAA-1. Revertir aisladamente versiones o huellas puede bloquear emisiones y desalinear el catálogo.

La auditoría conserva los archivos y verifica sus SHA256 antes y después. No modifica filas, valores, unidades, PDF históricos ni base de datos. El ajuste de impresión debe permanecer registrado para el responsable técnico de la serie.

La autorización resuelve la pausa administrativa del hallazgo 3. No elimina los pendientes normativos: SCC-1 mantiene MPa del Excel oficial hasta la confirmación de Martín; SDI mantiene los cuatro estados del kit hasta la decisión correspondiente antes de uso real.
