# Manuales y planillas SG-PEM-IFI en readyproof

Resumen de orientación basado en el kit interno vigente. No reemplaza los manuales ni introduce frecuencias, valores de aceptación o interpretaciones normativas. Las decisiones técnicas corresponden al Lic. Martín Sánchez.

| Código | Nombre de la serie | Registros del kit | Estado en la aplicación |
|---|---|---|---|
| SAA | Sistema de Abastecimiento de Agua | SAA-1 a SAA-6; informe SAA-IN | SAA-1 es el piloto de carga, firma y emisión PDF con datos ficticios. |
| SDI | Sistema de Detección de Incendios | SDI-1 a SDI-5; informe SDI-2-IN | Catálogo declarativo y vínculo a manual; faltan formularios/adaptadores y cotejo individual para habilitar todas sus planillas. |
| SBC | Sistema de Bombas Contraincendios | SBC-1 a SBC-6; informe SBC-IN | Catálogo declarativo y vínculo a manual; no equivale a generación operativa de todas las planillas. |
| SAL | Sistema de Extinción por Agentes Limpios | SAL-1 a SAL-4; informe SAL-1-IN | Catálogo declarativo y vínculo a manual; habilitación operativa pendiente. |

Jorge confirmó el 27/10/2026 utilizar para SAL el nombre **Sistema de Extinción por Agentes Limpios**, tal como figura en el kit. Se conserva la denominación de SBC de la tabla de referencia sin resolver por esta guía las variantes de nombre que el proyecto mantiene abiertas.

## SAA-1 Información general

Identifica la instalación y reúne información general del abastecimiento de agua, bombas y toma de impulsión para bomberos. La pantalla toma sus campos y opciones de la definición del kit y conserva su orden. Incluye observaciones y espacios de firma.

El piloto permite borrador, vista previa, finalización, PDF y preparación de correo. Los ejemplos no acreditan el estado de una instalación real. La versión interna con identidad actual es `00-26-rp1`; la revisión formal impresa de la serie no fue renumerada por ese cambio de identidad.

## SDI Detección de incendios

El manual aborda inspección, prueba, mantenimiento y registro de los componentes de detección y alarma, con las referencias técnicas identificadas por la serie. La numeración SDI-5 y el código SDI-2-IN conservan la decisión histórica del kit; esta guía no los renumera.

## SBC Bombas contraincendios

El manual reúne los procedimientos de bombas, accionamientos y componentes asociados y sus registros. Los valores y criterios deben tomarse del documento fuente aprobado y del diseño del sistema. No se trasladan a una instalación concreta datos de placa o ejemplos que aparezcan en los modelos originales.

## SAL Agentes limpios

El manual corresponde a extinción por agentes limpios. Su aplicación debe distinguir las variantes del sistema previstas en la serie y utilizar los criterios del diseño y del fabricante donde corresponda. No se agregan a este resumen valores de presión, concentración o periodicidad.

## Fuentes y límites

- [Guía del kit](../fuente/KIT_AGENTS.md), tabla de sistemas y decisiones abiertas.
- `fuente/herramientas/planillas_data2.py`: SDI, SBC y SAL.
- `fuente/herramientas/planillas_data3.py`: SAA, incluido el piloto SAA-1.
- `fuente/herramientas/build_planilla.py`: fuente del formato de planillas.
- `fuente/herramientas/build_informe.py`: generador de informes de referencia.
- [Guía de acceso](GUIA_ACCESO_BRAFEMAR.md) y [checklist de entrega](CHECKLIST_ENTREGA_BRAFEMAR.md).

La existencia de datos de catálogo no significa que estén implementados todos los formularios o informes. Los informes -IN desde cargas de la aplicación y los controles anteriores de puesta en producción siguen pendientes. No se incluyen normas ni fragmentos extensos de ellas en esta guía.
