# AGENTS.md — Serie SG-PEM-IFI (readyproof)

Guía para cualquier agente de IA, o persona, que continúe, corrija o amplíe la serie de Procedimientos Específicos de Mantenimiento de Instalaciones Fijas contra Incendios (SG-PEM-IFI) de readyproof. Junta todo lo decidido hasta ahora: qué es el proyecto, qué normas mandan, cómo se escribe, cómo se generan los archivos, cómo se hacen las piezas comerciales y qué queda abierto.

**Versión vigente: v5 (octubre 2026).**

Para la redacción y el formato de un manual, la referencia de detalle es `PROMPT_Manuales_SG-PEM-IFI.md`. Este archivo no lo repite: lo enmarca y agrega lo que el prompt no cubre (herramientas, decisiones, estado, controles).

---

## 1. Contexto

- **Empresa:** readyproof, inspección, prueba y mantenimiento de instalaciones fijas contra incendios. Administración: Jorge Sánchez.
- **Autor de la serie y responsable técnico:** Martín Sánchez. Escribió los manuales originales SDI, SBC y SAL, las planillas y el informe SDI, y los borradores de los capítulos 7, 11, 13, 14 y 18 (SRA, STM, SAA, SHC y SDC), junto con la tabla que asigna las NFPA a cada capítulo. **Toda decisión de interpretación normativa la confirma Martín.**
- **Qué es un manual SG-PEM-IFI:** un documento Word que convierte un capítulo de la IRAM 3546:2011 en un procedimiento de inspección, prueba y mantenimiento, con la estructura, el tono y el formato de la serie. Cada manual tiene asociados:
  - planillas Excel de registro, una por planilla de la norma;
  - un informe general prediseñado en Word (`-IN`).
- **Rol esperado del agente:** redactor técnico con criterio de ingeniero en instalaciones contra incendios (IRAM y NFPA). Se basa **solo** en las normas de referencia y no inventa valores.

## 2. Estado de la serie (v5)

| Cap. IRAM 3546 | Sigla | Sistema | Origen | NFPA aplicadas | Planillas | Informe |
|---|---|---|---|---|---|---|
| 6 | SDI | Sistema de Detección de Incendios | Martín, mejorado | 72, 101, 70E | SDI-1 a 5 | SDI-2-IN (Martín, corregido) |
| 7 | SRA | Sistema de Rociadores Automáticos | Nuevo (v4), sobre borrador de Martín | 25 (cap. 4, 5, 13, 14, 15), 13 | SRA-1 a 9 (7A a 7H y 7I/J/K) | SRA-IN |
| 8 | SAP | Sistema de Agua Pulverizada | Nuevo | 15, 25 (cap. 10) | SAP-1 a 5 | SAP-IN |
| 9 | SRE | Sistema de Rociadores de Espuma | Nuevo | 25 (cap. 11) | SRE-1 a 7 | SRE-IN |
| 10 | SGE | Sistema Generador de Espuma | Nuevo | — | SGE-1 a 7 | SGE-IN |
| 11 | STM | Sistema de Tuberías y Mangueras | Nuevo (v4), sobre borrador de Martín | 14, 25 (cap. 6, 13, 15) | STM-1 a 8 (11A a 11H) | STM-IN |
| 12 | SBC | Sistema de Bombas Contraincendios | Martín, mejorado | 20, 25 (cap. 8), 70E | SBC-1 a 6 | SBC-IN |
| 13 | SAA | Sistema de Abastecimiento de Agua | Nuevo (v4), sobre borrador de Martín | 25 (cap. 9, 15); 22 solo como remisión | SAA-1 a 6 (13A a 13F) | SAA-IN |
| 14 | SHC | Sistema de Hidrantes Contra Incendios | Nuevo (v4), sobre borrador de Martín | 24, 25 (cap. 7, 13, 15), 14 | SHC-1 a 3 (14A a 14C) | SHC-IN |
| 15 | SEP | Sistema Fijo de Extinción por Polvo | Nuevo | — | SEP-1 a 3 | SEP-IN |
| 16 | SSA | Sistema Fijo de Extinción por Solución Acuosa | Nuevo | — | SSA-1 a 4 | SSA-IN |
| 16 | SCC | Sistema Fijo de Extinción para Cocinas Comerciales | Nuevo (v4.1; auditado; revisado en v5), con la UL 300 y la práctica readyproof | 96 (cap. 6, 8, 10, 12 y 13), UL 300 (2019), 72 (10.6.7.2.1, 17.13, 23.8.5.10) | SCC-1 a 4 (16A a 16D) y SCC-5 (aptitud UL 300 y NFPA 96) | SCC-IN |
| 17 | SAL | Sistema de Extinción por Agentes Limpios | Martín, mejorado | 2001 (cap. 10 y 11), 72, 101 | SAL-1 a 4 | SAL-1-IN |
| 18 | SDC | Sistema de Extinción por Dióxido de Carbono | Nuevo (v4), sobre borrador de Martín | 12 (4.3, 4.5.6, 4.8) | SDC-1 a 5 (18A a 18E) | SDC-IN |
| — | SIM | Simbología de Seguridad contra Incendios | Nuevo | 170 | SIM-1 y SIM-2 | sin informe |

La serie cubre los 13 capítulos de sistemas de la IRAM 3546:2011 (6 a 18), más el manual SIM y el manual SCC de cocinas comerciales, que desarrolla el capítulo 16 para ese riesgo (el SSA queda para los demás riesgos con solución acuosa). Los 15 manuales están generados, con índice, y validados; lo pendiente está en la sección 9. Páginas en v5: SAA 16, SAL 19, SAP 20, SBC 20, SCC 27, SDC 16, SDI 22, SEP 15, SGE 15, SHC 13, SIM 28, SRA 23, SRE 20, SSA 13 y STM 19.

**Qué cambió en v5 (revisión de Jorge):**
- **Alcance particular en cada manual.** Antes los 15 tenían el mismo alcance genérico. Ahora cada uno enumera los equipos que comprende y su relación con los demás procedimientos de la serie (sección 7, `alcances.py`).
- **Encabezado y pie centrados y equidistantes del recuadro** (plantilla maestra; geometría en la sección 7).
- **Planillas centradas en la hoja:** antes la tabla quedaba pegada al margen izquierdo y con un espacio muerto a la derecha; ahora ocupa el ancho útil y queda a igual distancia de los dos bordes (`fix_impresion.py`).
- **SCC y SEP:** presurización con nitrógeno seco como caso habitual (sección 3, criterios de cocinas).
- **SCC:** características del fusible de prueba y su uso en el protocolo semestral.

## 3. Jerarquía normativa (regla de oro)

1. **IRAM 3546:2011** es la base y fija **qué** se hace y **con qué frecuencia**. La numeración de capítulos (6 a 18) y de planillas (IRAM 3546-<cap><letra>) es la de esta norma.
2. **NFPA complementarias**, cuando están disponibles, aportan **métodos, valores de aceptación y tareas** que la IRAM no prevé:
   - NFPA 72, cap. 14: detección y alarma; Tablas 14.3.1 (inspección) y 14.4.3.2 (prueba).
   - NFPA 25: inspección, prueba y mantenimiento de sistemas a base de agua (cap. 5 rociadores, 6 columnas y mangueras, 7 redes e hidrantes, 8 bombas, 9 tanques, 10 agua pulverizada, 11 espuma, 13 válvulas y componentes, 14 obstrucciones, 15 puesta fuera de servicio).
   - NFPA 13, 14, 15, 20, 22 y 24: criterios de diseño e instalación que el sistema debe conservar.
   - NFPA 12 (CO₂) y NFPA 2001 (agentes limpios): seguridad, inspección y mantenimiento.
   - NFPA 70E: condición de trabajo eléctricamente segura.
   - NFPA 101: seguridad humana. Ver sección 5.
   - NFPA 170: simbología (manual SIM).
3. **Ante diferencias, se adopta la condición más exigente** y se declara la decisión en el cotejo.
4. **Cada valor tomado de una NFPA se cita** con la norma y el artículo o la tabla, **sin año de edición**. Por ejemplo: «(NFPA 72, 14.4.2.4)». El manual dice una sola vez que se aplica la edición vigente y que la numeración se confirma en ella. No se le pone el año de la edición vigente a un artículo verificado en otra edición, porque la numeración cambia entre ediciones. Ediciones:

| Norma | Edición con la que se verificaron las citas | Edición vigente según nfpa.org (octubre 2026) |
|---|---|---|
| NFPA 72 | 2016 (en español) | 2025 |
| NFPA 20 | 2007 (en español) | 2025 |
| NFPA 101 | 2024 (citas renumeradas en v4) | 2024 (la de 2027 está en elaboración) |
| NFPA 13 | 2019 | 2025 |
| NFPA 25 | 2026 | 2026 |
| NFPA 14 | 2024 | confirmar en nfpa.org |
| NFPA 24 | 2022 | confirmar en nfpa.org |
| NFPA 15 | 2022 | confirmar en nfpa.org |
| NFPA 12 | 2022 | confirmar en nfpa.org |
| NFPA 2001 | 2022 | confirmar en nfpa.org |
| NFPA 70E | 2021 (traducción al español) | confirmar en nfpa.org |
| NFPA 170 | 2018 | 2024 |

   Antes de cada revisión hay que consultar nfpa.org. Si readyproof consigue el texto de las ediciones vigentes, se vuelven a verificar las citas contra ellas.
5. **Nunca se escribe un número que no esté en una norma de referencia.** Si falta el valor, el criterio se expresa respecto del diseño, del fabricante o del registro anterior.
6. **Normas no disponibles:** NFPA 22 (tanques), NFPA 4, NFPA 1930 (mangueras), IRAM 3576, IRAM 3594 (mangueras), IRAM 3508 (acoples) e IRAM 2529 (cilindros). No se citan valores de ellas. Se mencionan solo como remisión, sin contenido. La NFPA 720 fue incorporada a la NFPA 72: el monóxido de carbono se cita «según la NFPA 72» (NFPA 101, 9.12).
7. **Copias de normas:** varias copias provistas tienen marcas de distribución no autorizada (capturas de sitios de terceros, canales de mensajería). Se usan solo para extraer criterios y citas breves; no se redistribuyen ni se incluyen en el paquete. Lo ideal es que readyproof adquiera las ediciones vigentes.

### Requisitos generales IRAM 3546 que van en todos los manuales
- **Autocontrol:** las tareas de frecuencia menor a un mes las puede hacer el usuario.
- **Cañería seca, gravedad o red directa** (salvo acción previa): las tareas de frecuencia menor a trimestral se hacen trimestralmente.
- **Sin motobomba:** las tareas de frecuencia menor a mensual se hacen mensualmente.
- **Planillas:** identificación del mantenedor certificado, leyenda NA y copia al usuario. El contenido de una planilla de la norma no se puede cambiar, salvo para agregar tareas: no se quita ninguna fila.
- **Codificación de tres símbolos:** ✓ cumple · **O no cumple** · X no apreciable · NA no aplicable. En la norma, la «O» es un símbolo, no la conjunción «o»; leerla como conjunción fue un error de la serie, ya corregido. Las listas de verificación tienen las columnas CUMPLE ✓, NO CUMPLE O, NO APREC. X y NA.
- **Conservación de registros: 3 años como mínimo.** Prevalece sobre el plazo de la NFPA 72 (prueba siguiente + 1 año), que es menor. La excepción son los detectores de temperatura restaurables probados por rotación: ciclo de 5 años + 1 (NFPA 72, 14.6.2), porque ese plazo es mayor. Todas las planillas llevan **«T.C. 3 AÑOS»**.

### Erratas y criterios fijados
- **NFPA 20 en español (ed. 2007), 6.2.2:** dice «40 %» de presión a caudal cero, por error de traducción. Se usa **140 %**, según el 7.1.2.2. El manual cita solo «NFPA 20, 6.2.2»; la errata queda documentada en `Cambios_manuales_Martin.md`.
- **SBC:** la tabla de caudales por boquilla del original no coincidía con la fórmula. Se usa **Q = 0,0666 · c · d² · √P**.
- **NFPA 20, 14.4:** remite la inspección, prueba y mantenimiento periódicos a la NFPA 25. Desde v4, la prueba anual de SBC usa los criterios de aceptación de la NFPA 25, 8.3.7.2 (95 % de la curva, 100 % del caudal nominal, demanda del sistema); los valores de la NFPA 20 quedan como características de diseño.
- **Cap. 11 (STM), presión de la prueba hidrostática:** el texto de la IRAM dice 340 kPa sobre la nominal y la planilla 11F, 1380 kPa sobre la normal si supera 1000 kPa. Se adopta la NFPA 25, 6.3.2.1: 13,8 bar durante 2 h, o 3,4 bar sobre la máxima si esta supera 10,3 bar. Prueba con aire de sistemas reparados: 1,7 bar (la IRAM dice 166 y 170 kPa).
- **«Más favorable» / «más desfavorable»:** la IRAM los usa en forma contradictoria (cap. 7 diluvio y planilla 11H). Se adopta siempre el punto hidráulicamente más desfavorable (NFPA 25, 6.3.1.1 y 13.4.4.2.7.1).
- **CO₂ (SDC):** el borrador de Martín copiaba de agentes limpios que el agente es apto para recintos ocupados. Es falso y peligroso; el manual se rehízo con la NFPA 12, 4.3. La «planilla F» citada en la IRAM 3546-18C y 18E se interpreta como la 18D (control de peso).
- **Rociadores de respuesta rápida:** IRAM, muestra a los 20 años; NFPA 25-2026, 25 años (20 en ESFR/CMSA). Se mantiene 20 años.
- **NFPA 101:** cada artículo se cita con su condición de aplicación. No se le atribuyen frecuencias de prueba que no tiene: la prueba anual de las funciones de control es de la NFPA 72, Tabla 14.4.3.2, ítem 24, no del 9.6.5.2. El manual «puede constituir» el programa aprobado del 9.6.1.4 solo una vez que lo acepte la autoridad competente.
- **SAL:** la pesada aplica solo a los agentes halogenados. En gases inertes se controla la presión. Pérdidas admisibles: 10 % de presión en halogenados, 5 % en inertes, 5 % de peso neto.

### Criterios de cocinas comerciales (SCC) y de polvo (SEP)
- **UL 300 no es una norma de mantenimiento.** Es la norma de ensayo con la que se lista el sistema. Se usa para los criterios de aptitud (SCC-5) y para saber qué debe conservar el sistema instalado; las frecuencias siguen siendo las de la IRAM, capítulo 16, y la NFPA 96, capítulo 12.
- **Presurización: nitrógeno seco.** En la Argentina el cilindro de agente húmedo, y también el de polvo químico, suele ser de presión contenida, presurizado con nitrógeno seco; el cartucho o el recipiente de gas expelente aparte es la alternativa, solo donde el diseño lo prevé. Base: UL 300, 5.8 (gas expelente: nitrógeno seco o aire seco) y 5.17 (presión a 21 °C). Nunca se presuriza con aire húmedo; en polvo, la humedad lo apelmaza. Manuales, planillas (SCC-1, SCC MAN y SEP-1) e informe ya distinguen las dos variantes.
- **Fusible de prueba.** En la prueba semestral se reemplaza el fusible más alejado de la línea por un fusible de prueba y se libera cortándolo o separándolo; nunca se funde un eslabón con llama. El fusible de prueba lo provee el fabricante del sistema o es equivalente en geometría y en carga de liberación, va identificado, no queda instalado y se repone el fusible de servicio. Sin valores de temperatura ni de carga propios: son los del listado del fabricante.
- **Eslabones fusibles cada 6 meses** (NFPA 96, 12.2.4), más exigente que el reemplazo anual de la IRAM 16D. Ver decisión 19 bis.
- **Restitución tras la prueba:** central en estado normal → explosor o actuador → cilindro, siempre último. En la prueba quinquenal, prueba hidrostática antes de la recarga.
- **Limpieza de la campana y del conducto:** no la hace el mantenedor; se verifica la constancia de la empresa especializada contra la Tabla 12.4 y el 12.6 de la NFPA 96.
- **Sin extintores de CO₂** en cocinas (NFPA 96, 10.9); los portátiles son clase K.
- **Baterías de la fuente secundaria (centrales):** ninguna norma de la serie fija un reemplazo en años. Se reemplazan según el fabricante o cuando, recargadas, no alcanzan su especificación (NFPA 72, Tabla 14.4.3.2, ítem 9; marcado de mes y año, 10.6.10.1). La IRAM, capítulo 6, pide controles trimestrales y la prueba anual de 24 h.

## 4. Tono, estructura y formato (resumen; el detalle está en el PROMPT)

- **Tono:** impersonal, en tercera persona, técnico y formal. **Prohibidos:**
  - la segunda y la primera persona;
  - el imperativo al lector;
  - los coloquialismos;
  - las marcas, los modelos y los datos de un equipo o cliente concreto (ni nombres de comercios, ni fabricantes, ni personas, salvo el autor);
  - cualquier rastro de redacción automática.
- **Estructura fija:**
  - 1 Objetivo, 2 Alcance y 3 Procedimientos: textos comunes, no se tocan;
  - 3.1 Sistema, con «(Basado en IRAM 3546:2011 – Capítulo N)», propósito, descripción y equipamiento;
  - 3.1.1 Inspección, 3.1.2 Prueba y 3.1.3 Mantenimiento, con un subtítulo por frecuencia;
  - secciones complementarias, cuando corresponden;
  - 3.1.x Registro (siempre último);
  - 4 Anexos o registros.
- **Bloque de frecuencia:** subtítulo, frase de finalidad, «Durante esta inspección se debe verificar:», ítems «**Elemento:** verbo en infinitivo + qué + criterio» y cierre con la planilla. Los valores van en negrita.
- **Protocolo de Ensayo:** para pruebas con mediciones o maniobras. Pasos 1), 2)… con «Paso a paso», «Justificación técnica» y «Criterio de aceptación».
- **Alcance:** el apartado 2 de la plantilla es común, pero su lista de equipos y el párrafo de relación con otros manuales son propios de cada sistema y salen de `alcances.py`. No se edita el alcance en el .docx.
- **Planillas:** IRAM 3546-<cap>A → SG-PEM-IFI-<SIGLA>-1, B → -2, y así sucesivamente, **siguiendo el orden de letras de la norma**. El nombre es el literal de la norma: en mayúsculas en el capítulo 4 y en tipo oración en el cuerpo. La única excepción es SDI-5 (ver sección 9).
- **Formato (plantilla v3):** se trabaja siempre sobre la plantilla maestra y nunca se reconstruyen la portada, el encabezado ni los estilos:
  - títulos escalonados cada 0,7 cm: nivel 1 a 1,32 cm con línea inferior, 3.1 a 2,0 cm, 3.1.1 a 2,7 cm y 3.1.1.1 a 3,4 cm;
  - pie del modelo matriz, «Autor: Lic. Martin Sanchez | Pág. X de Y», centrado y a igual distancia del recuadro que el encabezado;
  - página «Índice de Contenido» después de la portada, con los niveles 1 a 3;
  - Times New Roman 12;
  - un párrafo vacío entre bloques;
  - cada lista reinicia en a) o en 1);
  - negrita solo donde la indica el prompt.

## 5. NFPA 101 (seguridad humana): regla del proyecto

Cuando un sistema usa la NFPA 72 (detección, o un sistema con disparo por detección, como SAL), el manual lleva la sección **«SEGURIDAD HUMANA: RECOMENDACIONES DE LA NFPA 101»**. Sus artículos se **traducen** del texto disponible de la NFPA 101, la edición 2018, y se **citan** por número, sin año. Temas base:

- 4.6.12, mantenimiento continuo, pruebas periódicas (4.6.12.5), supervisión (4.6.12.6) y registros en formularios aprobados, también electrónicos (4.6.12.7);
- 4.7, simulacros;
- 9.6, detección, alarma y notificación a ocupantes (9.6.1.3, 9.6.1.5, 9.6.1.6, 9.6.2.7, 9.6.2.10.4 y 9.6.2.10.5, 9.6.3.7 a 9.6.3.9 y 9.6.3.11, 9.6.4.4, 9.6.6.2 y 9.6.8);
- 9.8, sistemas alternativos (en SAL: 9.8.1 y 9.8.2);
- 9.11.4.1 prueba integrada y 9.11.4.2 prueba según NFPA 4 (edificios existentes: cada 10 años como máximo);
- 9.12, monóxido de carbono, según la NFPA 72.

La numeración es la de la edición 2024. La correspondencia con la de 2018, usada hasta v3, está en `Cambios_manuales_Martin.md`.

En el apartado PRUEBA de SDI y SAL va además el procedimiento de **desactivación** (NFPA 72, 10.20): aviso, autoridad competente si dura más de 8 h, mitigación, aviso de finalización, registro por 3 años y deficiencias por escrito dentro de las 24 h (14.2.2.2.3).

Los requisitos de la NFPA 101 que son tareas verificables se incorporan **también** al bloque de su frecuencia. Por ejemplo, los avisadores manuales accesibles van en la inspección semanal y la señal de evacuación audible en todo el edificio, en la prueba anual.

En el código, la sección la genera la función `seguridad_humana(a, extra_items)` de `content_SDI.py` y `content_SAL.py`.

## 6. Archivos del paquete

```
SG-PEM-IFI_Serie_completa_v5/
├── AGENTS.md                         ← este archivo
├── PROMPT_Manuales_SG-PEM-IFI.md     ← reglas de redacción y formato para generar un manual
├── SG-PEM-IFI_Plantilla_Maestra.docx ← base obligatoria de todo manual
├── Cotejo_y_dudas.md                 ← cotejo norma ↔ manual (sistemas nuevos de v2 y de v4)
├── Cambios_manuales_Martin.md        ← qué se cambió en SDI, SBC y SAL y por qué
├── auditorias/                       ← auditoria.md, auditoria_martin.md, auditoria3.md y auditoria_SCC.md
├── PDF/                              ← los 15 manuales en PDF, para lectura en el celular
├── SG-PEM-IFI-<SIGLA> <Nombre>/
│   ├── SG-PEM-IFI-<SIGLA> <Nombre>.docx
│   └── Registros/                    ← planillas .xlsx + informe -IN .docx
└── fuente/                           ← para regenerar todo
    ├── herramientas/                 ← scripts Python (sección 7), incluidos alcances.py y fix_numpages.py
    ├── contenidos/                   ← content_<SIGLA>.py, el texto de cada manual (content_SCC.py desde v4.1)
    ├── simbolos_png/                 ← 123 símbolos de SIM a 600 dpi (los genera simbolos.py)
    ├── modelos/                      ← originales de Martín: manual SDI (modelo matriz), manual SBC (base de la plantilla), SDI-1..4.xlsx y SDI-2-IN.docx
    ├── catalogo/                     ← scripts del catálogo comercial (sección 8 bis) y foto retocada
    └── identidad/                    ← logotipos de readyproof, positivo y negativo
```

La entrega se reparte en dos zip: **Serie completa** (manuales, registros y PDF, para usar) y **Kit interno** (este archivo, prompt, cotejos, auditorías y `fuente/`, para regenerar). El PDF del catálogo comercial se entrega aparte; sus scripts están en `fuente/catalogo/` (sección 8 bis).

**Las normas no se incluyen en el paquete**, por licencia. Para regenerar o auditar hay que colocarlas en `fuente/normas/` (IRAM 3546 en .md o .docx; NFPA en .txt extraído del PDF).

**La fuente autoritativa de la IRAM 3546 es la versión .md completa.** Una linealización de texto plano anterior perdía párrafos y viñetas, y llevó a una «corrección» errónea del SAP que hubo que revertir. Para texto, siempre la versión completa; el texto plano sirve solo para leer tablas.

## 7. Cómo regenerar

Requisitos: Python 3 con `python-docx`, `lxml` y `openpyxl`; LibreOffice (`soffice`) para renderizar; `pdftoppm` y Pillow para las hojas de contacto. Ejecutar Python con `-I`.

**El texto se edita en `contenidos/content_<SIGLA>.py`, nunca en el .docx.** Después se regenera.

| Paso | Comando | Notas |
|---|---|---|
| Plantilla | `python -I build_template.py <SBC_Martin.docx> <v2.docx>` y luego `python -I upgrade_template.py <v2.docx> <modelos/SDI_original_Martin.docx> <Plantilla_Maestra.docx>` | Solo si cambia la plantilla. La v2 sale del SBC de Martín; la v3 suma la jerarquía de títulos y el pie del modelo matriz (SDI). **La geometría de v5 del recuadro y del pie se ajustó a mano sobre la plantilla** (ver abajo): si se regenera la plantilla con estos scripts, hay que volver a aplicarla. |
| Manual | `python -I build_manual.py <Plantilla_Maestra.docx> <content_SIG.py> "<SG-PEM-IFI-SIG Nombre.docx>"` | Clona los párrafos ejemplo de la plantilla. Inserta el alcance de `alcances.py`. Controla marcadores y segunda persona, y quita los paraId. |
| Planillas (5 nuevos) | `python -I run_planillas.py <herramientas> <salida> <modelos/SDI-1.xlsx>` | Datos en `planillas_data.py`. |
| Planillas (SDI, SBC, SAL) | `python -I run_planillas.py <herramientas> <salida> <modelos/SDI-1.xlsx> planillas_data2` | Genera las 15 planillas. La clave opcional `solo` de un sistema limita cuáles se generan. |
| Planillas (SRA, STM, SAA, SHC, SDC, SIM) | `python -I run_planillas.py <herramientas> <salida> <modelos/SDI-1.xlsx> planillas_data3` | Datos e informes en `planillas_data3.py`. SIM no lleva informe. |
| Planillas e informe (SCC) | `python -I run_planillas.py <herramientas> <salida> <modelos/SDI-1.xlsx> planillas_data4` y `python -I build_informe.py <modelos/SDI-2-IN.docx> <herramientas> <salida> planillas_data4` | Datos e informe en `planillas_data4.py` (SCC-1 a 5 y SCC-IN). Las listas de la prueba semestral (`SEM`) y del mantenimiento (`MAN`) se comparten entre planillas. |
| Todo | `bash build_all_v4.sh <carpeta_de_trabajo>` | Genera los 15 manuales (SDI SRA SAP SRE SGE STM SBC SAA SHC SEP SSA SCC SAL SDC SIM), inserta los símbolos de SIM, agrega el índice, fija el total de páginas del pie y valida. Espera `manuales/`, `tools/`, `sim_png/` y `out/SG-PEM-IFI_Plantilla_Maestra.docx` dentro de la carpeta; escribe en `out_v4/manuales/`. |
| Informes | `python -I build_informe.py <modelos/SDI-2-IN.docx> <herramientas> <salida> [planillas_data2 \| planillas_data3 \| planillas_data4]` | Clona el informe de Martín. Datos en `informes_data.py` o en el `INFORMES` del módulo indicado. Claves opcionales por sistema: `periodo` (reemplaza las opciones «TRIMESTRAL…» del encabezado, por ejemplo «[MENSUAL / SEMESTRAL / ANUAL / QUINQUENAL]» en SCC) y `nc` (modelo de no conformidad; `{cap}` se reemplaza por el capítulo). Con `planillas_data4` la salida queda en `<salida>/SCC/`. El SDI-2-IN no se genera: es el de Martín, corregido a mano, y está en la carpeta Registros del SDI. |
| Índice | `python -I add_toc.py <manual.docx>` | Después de `build_manual.py`. Inserta el índice, renderiza con LibreOffice, ubica cada título en el PDF y escribe los números de página. Si Word pagina distinto, alcanza con «Actualizar campo». |
| Total de páginas | `python -I fix_numpages.py <manual.docx> [manual.pdf]` | Después del índice. Escribe en el campo NUMPAGES del pie el total real (si no, el visor muestra el valor guardado en la plantilla). Sin PDF, renderiza con LibreOffice. |
| Impresión de planillas | `python -I fix_impresion.py <carpeta>` | Centra horizontalmente todas las planillas `SG-PEM-IFI-*.xlsx` de la carpeta y lleva sus 25 columnas de 5,3 a 6,2, para que al imprimir la tabla quede de margen a margen y a igual distancia de los dos bordes, alineada con los logos del encabezado. Trabaja sobre el XML y conserva el encabezado con logos. Las planillas nuevas ya salen así de `build_planilla.py` (`COLW_IMP` y `horizontalCentered`); `COLW` = 5,3 queda solo para estimar el alto de las filas. |
| Metadatos de planillas | `python -I limpiar_metadatos.py <carpeta>` | Deja autor y empresa de las planillas en readyproof, sin rastros de herramientas. |
| Validar | `python validate.py <archivo.docx>` | Validador XSD del skill docx. |
| Revisar | `bash render.sh <archivo.docx> <carpeta>` | PDF + hoja de contactos de todas las páginas. |

**Alcance** (`alcances.py`): `ALCANCES[SIG]` con `items` (4 a 6 equipos o componentes, en tipo oración y con punto final), `rel` (relación con otros procedimientos y qué queda fuera) e `intro` opcional (solo SIM). Si no hay `intro`, el primer párrafo sale de `BASE % (nombre del sistema, capítulo)`. `build_manual.py` reemplaza el primer párrafo y la lista del apartado ALCANCE de la plantilla y agrega `rel` después del párrafo «Incluye las inspecciones…», conservando el formato de cada párrafo. Un manual nuevo necesita su entrada; sin ella, queda la lista genérica.

**Geometría de la plantilla (v5):**
- Recuadro de página (`w:pgBorders`): `offsetFrom="page"`, 25 pt de separación en los cuatro lados, detrás del texto.
- Márgenes (`w:pgMar`): superior 2875, derecho 567, inferior 1330, izquierdo 561, encabezado 470, pie 700 (dxa).
- Tabla del encabezado: sangría 189. Tabla del pie: ancho 10406 dxa, sangría 189, márgenes de celda 70, columnas 8815 + 1591, número de página centrado.
- Resultado: encabezado y pie centrados entre los lados del recuadro y a igual distancia de sus bordes superior e inferior. El encabezado se sube (470) para compensar el párrafo vacío que hay sobre su tabla. Respaldo previo: `SG-PEM-IFI_Plantilla_Maestra.bak_pie.docx`.

**Módulo de contenido** (`content_<SIGLA>.py`):
- Define `SIG`, `NOM`, `NOMU`, `CAP`, `PL` (n → nombre literal de la planilla), `CONTENT(cierre)` y `REGISTRO_EXTRA(...)`.
- Opcionales: `INFORME` (código del informe, si no es `SG-PEM-IFI-<SIG>-IN`) y `RETENCION=True` (si el módulo ya redacta la retención y el generador no debe agregarla).
- Bloques: `h2`, `basado`, `p`, `h3`, `h4`, `items`, `protocol` y `table`. `**x**` marca negrita. Las tablas de 4 columnas o más salen centradas, sin sangría y en 9 pt. `('table', {'w': [anchos relativos], 'rows': [...]})` fija anchos de columna distintos, sin sangría y con filas que no se parten entre páginas.
- Opcional: `SIN_INFORME=True` (SIM).
- El generador mantiene unida la lista del capítulo 4 y quita los párrafos vacíos finales, para que no queden líneas sueltas ni una última página en blanco.

**Trampas técnicas conocidas:**
- Un `w:num` nuevo en numbering.xml se inserta **después del último `w:num`**; si no, Word rechaza el archivo. Usa `abstractNumId` 153 para a) y 155 para 1), con `startOverride` = 1.
- En tablas, `w:tblInd` va después de `w:tblCellSpacing` o `w:jc`.
- La portada tiene cuadros de texto anidados: no se parsea con regex ni se reconstruye.
- openpyxl pierde el encabezado de página con logos (legacyDrawingHF + VML + imágenes). `build_planilla.inject_header()` lo copia de `modelos/SDI-1.xlsx` después de guardar. Si se toca una planilla de Martín con openpyxl, hay que reinyectarlo.
- Las negritas `**x**` no se procesan dentro de las celdas de `table`: en tablas se escribe texto plano.
- Al reemplazar el texto de un párrafo clonado hay que conservar el `rPr` de la primera corrida; si no, hereda negrita (pasó con las viñetas del alcance).
- Los scripts `fix_audit*.py` son parches históricos ya aplicados: `fix_audit.py`, `fix_audit2_*.py`, `fix_audit3_manuales.py` (sobre los `content_*.py`) y `fix_audit3_planillas.py` (sobre `planillas_data2.py` y `build_planilla.py`). **No se vuelven a ejecutar**: fallan a propósito (`assert`) si el texto ya cambió. Lo mismo vale para `fix_v4_nfpa101.py` (renumeración de la NFPA 101 a 2024), ya aplicado.

## 8. Control de calidad antes de entregar

1. Hacer el cotejo norma ↔ manual completo: toda actividad, frecuencia, viñeta, valor, nota y campo de planilla del capítulo está en el manual.
2. Verificar que cada valor NFPA citado exista en la fuente, con el mismo número y la misma unidad.
3. Validar el .docx y renderizarlo; revisar todas las páginas, sin títulos huérfanos ni listas mal numeradas.
4. Comprobar la consistencia del manual con las planillas y el informe en códigos, títulos, «T.C. 3 AÑOS» y anexos.
5. Revisar el tono: sin segunda ni primera persona y sin marcas.
6. En trabajo de alto impacto, pedir una **auditoría independiente**: un agente que no redactó el manual, con las mismas fuentes, que clasifique los hallazgos en crítico, mayor o menor y entregue el texto de la corrección. Los informes previos son `auditoria.md`, `auditoria_martin.md`, `auditoria3.md` y `auditoria_SCC.md`.
7. Documentar en el cotejo lo agregado fuera de la norma («Valores y contenidos agregados») y las decisiones de interpretación («Dudas»).
8. Verificar en el PDF que el pie diga «Pág. X de Y» con el total real, que el alcance sea el del sistema y que no aparezcan nombres de clientes, comercios, fabricantes ni rastros de redacción automática (buscar en todo el texto, también en planillas e informes).

## 8 bis. Piezas comerciales (catálogo y hojas de servicio)

Son material de venta, no parte de la serie, pero se apoyan en ella. El primero es el catálogo de cocinas comerciales (`readyproof_Catalogo_Cocinas_Comerciales.pdf`, A4 apaisado, 7 páginas).

**Identidad (manual de identidad de readyproof):**
- Colores: rojo **#D41120** (C9 M100 Y93 K2), negro **#1D1D1B**, gris claro **#DDDEDB**.
- Tipografías: Impact (logotipo), Century Gothic (principal, regular, itálica, negrita y negrita itálica) y Myriad Pro (secundaria). Sin los archivos de fuente, el catálogo usa sustitutos: Inter Display Black condensada para Impact, TeX Gyre Adventor para Century Gothic e Inter para Myriad. Cuando readyproof entregue `impact.ttf`, `GOTHIC*.TTF` y Myriad Pro, se reemplazan.
- Logotipo: los PNG de `identidad/` (positivo y negativo). Sin sombras ni 3D, sin deformar ni recolorear, nunca sobre fondos blancos, complejos o con patrones; tamaño mínimo 2 cm o 100 px; respetar el área de seguridad. Sobre fondo oscuro, la versión con palabra blanca y barras rojas.
- Recursos de diagramación: barra lateral oscura con índice y marcador ▶, solapas rojas con extremo redondeado, franjas diagonales grises de seguridad y franjas rojas y negras en las tapas.

**Contenido:**
- Contacto: solo WhatsApp, correo, web y dirección (Colón 300 esq. Güemes, Godoy Cruz, Mendoza; atención en Mendoza y San Juan). **No se publica el teléfono fijo.**
- **Respaldo sin sobrecompromiso** (pedido de Martín): se habla de «normas de referencia» y de documentación del servicio (planillas e informe técnico), no de garantías ni de «todo según norma». No se promete un resultado ni una certificación que dependa de terceros. No se usa el sello IRAM de la web mientras no esté claro su alcance.
- Sin marcas de fabricantes ni nombres de clientes; en fotos propias se tapan teléfonos y etiquetas de terceros.
- Ilustraciones: renders isométricos propios, en `fuente/catalogo/iso/`: `iso.py` (motor SVG), `cocina.py` (escena de cocina, variantes fuego y descarga, claro y oscuro), `comps.py` (componentes), `gen2.py` (páginas del catálogo, HTML) y `pdf2.py` (PDF con Chromium y Playwright). `gen2.py` toma los logotipos de `fuente/identidad/` y la foto retocada de `fuente/catalogo/instalacion_cocina_cat.jpg` (teléfono tapado y etiqueta de terceros difuminada). Los renders se pueden reemplazar por fotos propias de readyproof cuando las haya.
- Metadatos del PDF: autor y productor readyproof.

## 9. Decisiones abiertas (las confirma Martín)

1. **SDI-5 «Información semanal (autocontrol)»:** por el orden de letras le correspondería el número 2. Se numeró 5 para no renumerar las planillas que ya se usan. El código del informe, «SDI-2-IN», se decide junto con esta numeración.
2. **«8,3 %» de la planilla IRAM 3546-6E** (calibración de detectores): se transcribió sin interpretar. Lo probable es que sea 1/12 de los detectores por intervención, pero hay que confirmarlo.
3. **Frecuencia «B» de la planilla 12E** (interruptores o fusibles del motor): se interpretó como bienal. Se adopta la mensual de la 12D, que es más exigente.
4. **Reemplazo de planillas:** las 3 originales de SBC pasan a 6, y las SDI-1 a 4 de Martín se regeneraron con el formato de la serie y los campos IRAM que les faltaban.
5. **Criterio de cañería seca** en los sistemas a base de agua (paso a trimestral): aplicación por sistema.
6. **SEP-4:** la norma trae solo 3 planillas. Las tareas anuales, bienales y quinquenales se registran en SEP-3 como complementarias. Falta decidir si se crea una SEP-4 propia.
7. **NFPA 2001:** desde v4 se aplica el capítulo 11 (inspección mensual, semestral, anual, recipientes y mangueras cada 5 años) y el 10.6 (aborto y disparo manual). Los criterios de concentración, retención y pureza siguen sin desarrollarse: requieren la memoria de diseño de cada sistema.
8. **IRAM 3576:** el informe SDI-2-IN ahora evalúa respecto de la IRAM 3546, capítulo 6. Si la 3576 aplica, se cita como complementaria.
9. **Párrafo común de «Concordancia»** de la plantilla: contradice que la IRAM fije las frecuencias. La auditoría 3 propone otra redacción (ver `Cambios_manuales_Martin.md`). Al ser texto común, lo decide Martín.
10. **Nombre del sistema SBC:** «Contra incendio», «Contraincendios» y «Contra incendios» conviven. Hay que unificarlo.
11. **Fórmula de boquillas y leyes de afinidad (SBC):** son relaciones físicas generales que no figuran en las normas disponibles.
12. **Ediciones vigentes de las NFPA:** conseguir NFPA 72 (2025) y NFPA 20 (2025) para confirmar la numeración de los artículos citados; la NFPA 101 ya está renumerada a 2024.
13. **Planillas únicas o por planilla IRAM:** los borradores de Martín usan una planilla por sistema (por ejemplo SRA-1). La serie mantiene una planilla por cada planilla de la norma (SRA-1 a 9, STM-1 a 8, SAA-1 a 6, SHC-1 a 3, SDC-1 a 5). Lo confirma Martín.
14. **Tabla de NFPA por capítulo:** en la imagen de Martín, el capítulo 6 dice «72 y 10…» (cortado). Se interpretó como NFPA 72 y NFPA 101.
15. **NFPA 22 no disponible:** el capítulo 13 (SAA) usa el capítulo 9 de la NFPA 25 y cita la NFPA 22 solo como norma de diseño y reparación.
16. **Planilla 11H:** prueba anual de pérdidas de tuberías secas a 1,7 MPa durante 2 h, que el texto del capítulo no menciona. Se mantiene en la planilla con la condición de no superar la presión nominal de los componentes.
17. **Prueba de mangueras de CO₂:** se adoptan 17,5 MPa y 6,3 MPa (IRAM), levemente mayores que 17,24 MPa y 6,2 MPa (NFPA 12, 4.8.2.1).
18. **Combinación de criterios en manómetros de tanques (SAA):** frecuencia anual de la IRAM con tolerancia del 3 % de la NFPA 25 (la IRAM dice 10 %).

19. **SCC: normas pendientes.** La NFPA 96 (2021) ya está incorporada. Falta la edición vigente de la NFPA 17A y la NFPA 10 (extintores clase K). La NFPA 17A 2017 se consultó en una copia **no autorizada** (ver «Criterios NFPA 17A» abajo): los criterios sirven de revisión, pero las citas van recién con la edición vigente comprada en nfpa.org.
19 bis. **SCC: fusibles semestrales.** La IRAM 3546 (16D) pide sustitución anual de eslabones fusibles; la NFPA 96, 12.2.4, semestral. Se adoptó la semestral, más exigente. Afecta cotizaciones y pliegos que piden reemplazo anual. Lo confirma Martín.
19 ter. **SCC: auditoría independiente** (`auditoria_SCC.md`): 2 críticos, 5 mayores y 19 menores, todos corregidos. La sección de criterios de aptitud se movió después del mantenimiento (estructura fija de la serie); Martín confirma la ubicación.
19 quater. **v5, alcances:** los 15 alcances particulares de `alcances.py` los redactó la serie a partir del capítulo de cada sistema. Martín confirma la lista de equipos y los límites con otros procedimientos (por ejemplo, que la limpieza de campanas y conductos quede fuera del SCC, o que el SSA excluya las cocinas).
19 quinquies. **v5, fusible de prueba y presurización:** el criterio del fusible de prueba (más alejado, provisto por el fabricante o equivalente, liberado sin llama) y la presión contenida con nitrógeno seco como caso habitual en SCC y SEP los confirma Martín.
19 sexies. **«Certificado de operatividad»:** el SCC y su informe usan esa expresión (NFPA 96, 12.2.8). Para no comprometer más de lo necesario, se propuso cambiarla por «informe técnico de estado», como en el catálogo. Lo decide Martín.
20. **SCC frente a SSA:** el SCC reemplaza al SSA en las cocinas; Martín confirma si el SSA se mantiene o se retira de la serie.
21. **Unidad de presión en SCC:** las planillas usan bar (lectura habitual de los manómetros de cocina); el SSA usa MPa. Se unifica según decida Martín.

22. **Fuentes y fotos de marca:** pendientes los archivos de Impact, Century Gothic y Myriad Pro, y fotos propias de instalaciones, para reemplazar sustitutos y renders del catálogo.
23. **NFPA 17A y NFPA 10:** si readyproof consigue sus textos, se incorporan al SCC (decisión 19).

Cuando Martín resuelva una, se actualizan el `content_*.py` o los datos de planillas, se regenera, y se mueve la decisión a `Cambios_manuales_Martin.md` como resuelta.

### Criterios NFPA 17A (2017, copia no autorizada: solo para revisión)

Fuente: NFPA 17A, *Wet Chemical Extinguishing Systems*, edición 2017, capítulo 7 (y 7.5). La copia tiene marcas de distribución de terceros: **no se cita textualmente ni se incluye en el paquete**. Las citas de un manual se hacen con la edición vigente comprada en nfpa.org. Estado: criterios para cotejo del SCC, pendientes de confirmación de Martín; no aplicados aún a los manuales salvo lo ya decidido (19 bis).

| Tema | Criterio extraído (NFPA 17A, 2017) | Relación con la serie |
|---|---|---|
| Inspección mensual del propietario (7.2.1, 7.2.2) | Ubicación del sistema, actuadores manuales libres, precintos de manipulación, etiqueta de mantenimiento y ausencia de daño físico. | Coincide con la IRAM, capítulo 16. Verificar que la planilla SCC-2 cubra los cinco puntos. |
| Registro de la inspección mensual (7.2.5, 7.2.6) | Fecha e iniciales en cada inspección. Registros conservados entre las inspecciones semestrales. | Compatible con «T.C. 3 AÑOS» (el plazo mayor prevalece). |
| Mantenimiento semestral (7.3.2, 7.3.3) | Intervalo máximo de 6 meses, por técnico capacitado y con certificado (7.3.1, 7.3.1.1). | Coincide con la semestral de la NFPA 96, 12.2. |
| Contenido del mantenimiento (7.3.3.1) | Verificar que el riesgo no cambió; revisar detectores, gas expelente, cañerías, boquillas, señales, dispositivos de disparo y nivel de líquido. Verificar que la distribución no esté obstruida. | Cotejar con SCC-4 (el gas expelente ya figura; falta el nivel de líquido y la verificación de la distribución, si no están). |
| Prueba del sistema (7.3.3.4) | Probar todo el sistema, incluidas las señales de detección, los dispositivos de disparo y las estaciones manuales. | Cotejar con la prueba semestral SCC-3. |
| Elementos fusibles (7.3.4, 7.3.4.1, 7.3.4.2) | Reemplazo **al menos semestral** desde la instalación, con la misma clasificación; marcar año de fabricación y fecha de instalación en la etiqueta. | **Respalda la decisión 19 bis** (fusibles semestrales), que la IRAM 16D no cumple. Agregar en SCC-4 la marca de año de fabricación y fecha de instalación. |
| Elementos no fusibles (7.3.5) | Pueden quedar en servicio con inspección y limpieza al menos cada 12 meses. | Verificar si el SCC lo contempla. |
| Detectores térmicos restaurables (7.3.5.1) | Inspección visual, prueba funcional y verificación de calibración según el fabricante. | Cotejar con la planilla de detección térmica, si aplica. |
| Recarga y purga (7.4.1 a 7.4.3) | Tras la descarga, purgar cañerías con aire seco o nitrógeno según el manual del fabricante. | **Respalda el nitrógeno seco** ya adoptado. |
| Gas expelente (7.3.6) | Método para verificar cantidad y presión del gas expelente. | Ya figura en SCC-4 («Gas expelente»). |
| Prueba hidrostática (7.5.1 a 7.5.2.3) | Contenedores, contenedores de presión auxiliar y mangueras: cada **12 años**. Excepción para contenedores de hasta 2 in de diámetro y menos de 2 ft (0,6 m) de largo, y los DOT 3E. Presión igual a la marcada de fábrica o la del manual, sin pérdidas. | Se mantiene la **prueba quinquenal de la IRAM** (la más exigente). No se adopta el plazo de 12 años. |
| Sello de servicio (7.6) | Sello en el cuello con mes, año y nombre de la agencia que hizo la recarga o el examen interno. | Cotejar con SCC-4 («Cilindro»). |

Pendientes de la revisión: el capítulo 6 (planos y ensayos de aceptación, 17A-9) y el Anexo C (cocinas, 17A-17), que no se leyeron todavía.

## 10. Límites

- No usar copias de normas encontradas en la web, porque pueden ser no autorizadas. Se usan solo las que provee readyproof, y solo para extraer criterios fácticos citados.
- No inventar valores, frecuencias ni artículos.
- No modificar los textos comunes de la plantilla (Objetivo, Alcance, encuadre de Procedimientos).
- No borrar archivos originales de Martín: se trabaja sobre copias y los respaldos quedan en `bak/`.
- No usar el informe ARPEX ni datos de clientes como fuente o ejemplo.
- No agregar repositorios externos al proyecto.
- Escribir en español rioplatense técnico, con tildes también en mayúsculas.
