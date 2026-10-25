# Auditoría técnica independiente N.º 3: SG-PEM-IFI-SDI, SG-PEM-IFI-SBC y SG-PEM-IFI-SAL

**Objeto:** los manuales finales (.docx, revisión 00-26), sus planillas (`planillas2/`) y sus informes (-IN).
**Fuentes usadas:** IRAM 3546:2011 (`normas/3546.md`; las planillas se leyeron en `3546_lin.txt` y la codificación de las celdas en `3546.docx`), NFPA 72 ed. 2016, cap. 14 y cap. 10 (`ch14.txt`, `nfpa72.txt`), NFPA 20 ed. 2007 (`nfpa20.txt`), NFPA 101 ed. 2018 (`nfpa101.txt`, `n101L.txt`) y NFPA 13 (`nfpa13.txt`, solo para el tubo Pitot).
**Criterio del proyecto:** la IRAM fija las frecuencias. La NFPA aporta los métodos y los valores. Si las dos normas difieren, se adopta lo más exigente. Los registros se conservan como mínimo 3 años.
**Severidad:**
- **CRÍTICO:** incumple en forma directa la IRAM, crea un riesgo para las personas o el equipo, o usa un valor sin respaldo.
- **MAYOR:** omite un requisito normativo relevante, atribuye a una norma algo que no dice o afecta la trazabilidad.
- **MENOR:** problemas de forma, coherencia o citas de detalle.
- **NO VERIFICABLE:** la norma o el dato no están en las fuentes provistas.

Para ubicar cada hallazgo se usa la numeración del PDF de cada manual (`manuales/r_*/`). Los ítems se identifican con la letra que muestra el documento.

---

## 1. Resumen ejecutivo

**Correcciones de la auditoría anterior.** De sus 19 hallazgos críticos y mayores, el .docx final corrige 17 y deja 2 en estado parcial (SDI-M2 y SBC-M5). No hay regresiones en el cuerpo de los manuales. En SDI, SBC y SAL ya no quedan riesgos de seguridad abiertos: están el aislamiento de salidas, el bloqueo de arranque, el protocolo de pesada y la verificación de ausencia de tensión en el circuito de disparo. La retención de 3 años figura en los tres apartados REGISTRO y en todas las planillas.

**Dónde están ahora los problemas.** El cuerpo de los manuales quedó, en general, bien alineado con la IRAM 3546 y con la NFPA 72 y la NFPA 20. Los problemas se trasladaron a las **planillas** y a la **coherencia documental**:

- Las **planillas SDI de Martín**, que se conservaron, eliminan contenido obligatorio de la IRAM:
  - la «Prueba de detectores en ductos» de la planilla 6D;
  - «Manual instructivo» y «Planos» de la planilla 6B;
  - la identificación del mantenedor certificado en SDI-1 a SDI-4.
- Las **planillas SBC-3 y SBC-6** omiten campos de las planillas 12C y 12F:
  - la presión del Pitot;
  - las presiones de succión y de descarga al 150 %;
  - los datos de placa, que el manual dice que se registran en la SBC-3.
- La **codificación** de las planillas está mal transcripta en los tres manuales y en las planillas. La IRAM usa tres símbolos: **✓ cumple, O no cumple y X no apreciable**. La serie los convirtió en «✓ cumple; X no cumple o no apreciable».
- El **informe SDI-2-IN** declara la conformidad respecto de la «IRAM 3576». Esa norma no está entre las fuentes y no es la norma del procedimiento.
- El apartado **NFPA 101** está bien traducido en lo esencial y no inventa valores. Sus defectos son de atribución y de alcance:
  - se atribuye al 9.6.1.5 un procedimiento de desactivación que el artículo no contiene; su contenido real está en la NFPA 72, 10.20;
  - se usa el 9.6.5.2 como fuente de una prueba anual que el artículo no exige; la fuente correcta es la NFPA 72, Tabla 14.4.3.2, ítem 24;
  - se omiten condiciones de aplicación en 9.6.3.6, 9.6.7 y 9.11.4;
  - falta el 9.11.3.1, sobre la documentación durante toda la vida del sistema, y el 4.6.10.1, sobre la ocupación con protecciones fuera de servicio.

**Conteo:** 2 CRÍTICOS · 6 MAYORES · 8 MENORES.

| Severidad | ID | Síntesis |
|---|---|---|
| CRÍTICO | A3-C1 | Las planillas SDI-1 a SDI-5 quitan contenido obligatorio de las planillas 6A, 6B y 6D y no identifican al mantenedor certificado |
| CRÍTICO | A3-C2 | Las planillas SBC-3 y SBC-6 omiten campos obligatorios de las 12C y 12F, entre ellos la presión del Pitot, la succión y la descarga al 150 % y los datos de placa |
| MAYOR | A3-M1 | La codificación ✓/O/X de la IRAM está mal transcripta en los 3 manuales y en las planillas |
| MAYOR | A3-M2 | El informe SDI-2-IN evalúa la conformidad respecto de la «IRAM 3576» (no verificable) y no cita la IRAM 3546 |
| MAYOR | A3-M3 | El manual declara que las tareas complementarias se registran en planillas que no tienen filas para ellas (SDI-2, SDI-3, SDI-4 y SAL-3) |
| MAYOR | A3-M4 | SDI y SAL no tienen procedimiento de desactivación; lo que se atribuye al 9.6.1.5 de la NFPA 101 no está en ese artículo |
| MAYOR | A3-M5 | Atribuciones a la NFPA 101 que el texto no respalda: 9.6.1.4 («constituye ese programa») y 9.6.5.2 como fuente de la prueba anual |
| MAYOR | A3-M6 | SAL: falta el procedimiento documentado de verificación de la calidad del agente que exige la IRAM |
| MENOR | A3-m1 a m8 | Ver el apartado 3.3 |

---

## 2. Auditoría del apartado NFPA 101, ed. 2018 (tarea 1)

Ubicación: SDI 3.1.6, ítems a) a m), y SAL 3.1.6, ítems a) a h). Además hay citas a la NFPA 101 en SDI 3.1.1.2 b), SDI 3.1.2.4 h) e i) y SAL 3.1.2.2 h).

Escala de fidelidad:
- **FIEL:** la cita es correcta y la traducción es fiel.
- **FIEL*:** fiel con matiz menor.
- **ALCANCE+:** omite condiciones de aplicación y amplía el alcance.
- **ATRIB:** el artículo no dice lo que se le atribuye.

Ningún ítem introduce valores numéricos inventados. Los únicos números del apartado son 3,0 m y 6,1 m, que corresponden a 10 ft y 20 ft del 9.6.2.10.4.

| # | Manual | Artículo citado | ¿Existe? | Qué dice la NFPA 101 (cita breve) | Fidelidad | Pertinencia para inspección, prueba y mantenimiento | Observación |
|---|---|---|---|---|---|---|---|
| 1 | SDI a) / SAL a) | 4.6.12.1 | Sí | «…required for compliance with the provisions of this Code… shall thereafter be continuously maintained… in accordance with applicable NFPA requirements… or as directed by the AHJ» | FIEL* | Alta | El manual dice «requerido para la seguridad humana»; el original dice «requerido para cumplir este Código». Omite la opción del diseño basado en desempeño. |
| 2 | SDI b) / SAL b) | 4.6.12.2 y 4.6.12.3 | Sí | «No existing life safety feature shall be removed or reduced where such feature is a requirement for new construction»; «Existing life safety features obvious to the public, if not required… shall be either maintained or removed» | FIEL* | Alta | «Nunca dejar inoperativos» no está en el artículo; sale del Anexo A.4.6.12.3, que no es obligatorio («…present a false sense of safety»). Hay que indicarlo. |
| 3 | SDI c) / SAL c) | 4.6.12.4 y 4.6.12.5 | Sí | «…tested, inspected, or operated as specified elsewhere in this Code or as directed by the AHJ»; «…under the supervision of a responsible person…» | FIEL | Alta | — |
| 4 | SDI d) | 9.6.1.3 y 9.6.1.4 | Sí | «…installed, tested, and maintained in accordance with… NFPA 70 and NFPA 72 unless it is an approved existing installation»; «…shall have an **approved** maintenance and testing program» | ATRIB (parcial) | Alta | «El presente procedimiento constituye ese programa» exagera el alcance: el programa debe estar *aprobado* por la autoridad competente. Se omite además la excepción de la instalación existente aprobada. Ver A3-M5. |
| 5 | SDI e) | 9.6.1.5 | Sí | «Fire alarm system impairment procedures shall comply with NFPA 72.» | **ATRIB** | Alta | El artículo solo remite a la NFPA 72. La notificación, las medidas compensatorias y el registro corresponden a la NFPA 72, 10.20.1 a 10.20.6. Allí las medidas de mitigación son obligatorias solo «donde sea requerido por la autoridad competente», y se agrega el aviso a la autoridad competente si el sistema queda fuera de servicio más de 8 h (10.20.4). Ver A3-M4. |
| 6 | SDI f); SDI 3.1.1.2 b) | 9.6.2.7 | Sí | «Manual fire alarm boxes shall be accessible, unobstructed, and visible.» | FIEL | Alta | — |
| 7 | SDI g) | 9.6.2.10.4 | Sí | «…smoke alarms and smoke detectors shall not be installed within an area of exclusion determined by a 10 ft (3.0 m) radial distance along a horizontal flow path from a stationary or fixed cooking appliance… between 10 ft (3.0 m) and 20 ft (6.1 m)… alarm-silencing means or… photoelectric» [72:29.8.3.4(4)] | FIEL* / ALCANCE+ | Baja | Es un requisito de instalación del apartado 9.6.2.10 *Smoke Alarms*, extraído del cap. 29 de la NFPA 72 (unidades de vivienda). Se pierde «a lo largo de un recorrido horizontal» y la excepción del 9.6.2.10.5. El manual dice «Se verifica en la inspección anual», pero la 3.1.1.6 a) no lo menciona. |
| 8 | SDI h); SDI 3.1.2.4 h) | 9.6.3.6, 9.6.3.7, 9.6.3.8 y 9.6.3.10.1 | Sí | 9.6.3.6: «…shall operate in accordance with **one of the methods** prescribed by 9.6.3.6.1 through 9.6.3.6.3»; 9.6.3.7: «…effectively heard above the average ambient sound level…»; 9.6.3.8: «…distinctive…»; 9.6.3.10.1: «…used only for fire alarm system or other emergency purposes» | ALCANCE+ | Media | Solo se presenta la evacuación total del 9.6.3.6.1, con las excepciones del 9.6.3.6.4 y del 9.6.3.6.5. Se omiten la notificación selectiva (9.6.3.6.2) y el modo privado (9.6.3.6.3), y también el 9.6.3.10.2, que permite usar el sistema de voz para otros fines. Las citas 9.6.3.7 y 9.6.3.8 de la prueba anual son FIEL. |
| 9 | SDI i) | 9.6.4.4 | Sí | «For other than existing installations, where fire alarm systems are required to provide emergency forces notification, supervisory signals and trouble signals shall sound and be visibly displayed… at an approved, remotely located receiving facility or at a location… constantly attended by qualified personnel.» | FIEL | Media | Conviene sumar el 9.7.2.1.2, que repite el mismo requisito para las señales de supervisión de rociadores, porque el SDI las recibe (ítem j de la semanal). |
| 10 | SDI j) | 9.6.7.2 y 9.6.7.3 | Sí | 9.6.7.1: «**Where alarm annunciation is required** by another section…»; 9.6.7.3: «…each floor… other than floors of existing buildings, shall be considered as not less than one zone, unless otherwise permitted by 9.6.7.4.4…» | ALCANCE+ | Baja (es de diseño) | Se omiten la condición del 9.6.7.1 y las excepciones del 9.6.7.4.x. Faltan el 9.6.7.5 y el 9.6.7.6, que exigen anunciar las señales de falla y de supervisión en forma audible y visible y que sí se pueden verificar en una prueba. |
| 11 | SDI k) | 9.12 | Sí | «Where required by another section of this Code, CO detection and warning equipment shall be provided in accordance with NFPA 720.» | FIEL | Baja | El contenido de la NFPA 720 es NO VERIFICABLE. |
| 12 | SDI l) / SAL g) | 9.11.4 | Sí | «**Where required by Chapters 11 through 43**, and where two or more… systems are integrated, the integrated system shall be tested… in accordance with NFPA 4.» | ALCANCE+ | Media | Se omite la condición «donde lo exijan los capítulos 11 a 43». El contenido de la NFPA 4 es NO VERIFICABLE. |
| 13 | SDI m) / SAL h) | 4.7 (4.7.1 a 4.7.6) | Sí | Frecuencia suficiente (4.7.2), evacuación ordenada (4.7.3), horarios esperados e inesperados (4.7.4), lugar de reubicación (4.7.5) y registro escrito (4.7.6) | FIEL | Baja para el mantenedor | Es una obligación del propietario o usuario. Hay que asignarla en CONTROL DE CAMBIOS Y RESPONSABILIDADES. El A.4.7.6 detalla el contenido del registro: fecha, hora, participantes, lugar y resultados. |
| 14 | SDI 3.1.2.4 i) / SAL f) | 9.6.5.2 | Sí | «**Where required by another section of this Code**, the following functions shall be actuated: (1) Release of hold-open devices… (6) HVAC shutdown» | **ATRIB** | Alta (la tarea), nula (la cita) | El artículo enumera funciones que deben *actuarse*, pero no exige verificarlas en una prueba anual. La prueba anual de las funciones de control de emergencia está en la NFPA 72, Tabla 14.4.3.2, ítem 24 («verificar la activación de los dispositivos interfaz… verificar que… haya sido restaurado»). Además, en SAL f) la justificación «retención del agente» es una inferencia del redactor que se presenta como si fuera del artículo. Ver A3-M5. |
| 15 | SAL d) | 9.8.1 y Tabla 9.8.1 | Sí | «…extinguishing system shall be installed in accordance with the applicable standard referenced in Table 9.8.1» (Clean agent → NFPA 2001) | FIEL | Baja (es de instalación) | La NFPA 2001 es NO VERIFICABLE. Es la norma que contiene la inspección, prueba y mantenimiento propios del agente limpio, de modo que su ausencia deja sin contrastar los criterios de concentración y retención. |
| 16 | SAL e); SAL 3.1.2.2 h) | 9.8.2.1 y 9.8.2.2 | Sí | «…in lieu of a required, supervised automatic sprinkler system… shall activate the building fire alarm system, where provided»; «…not installed in lieu… shall be indicated at the building fire alarm system, where provided» | FIEL | Alta | — |

**Lo que falta de la NFPA 101 y es pertinente:**
- **9.11.3.1:** «All required documentation regarding the design of the fire protection system and the procedures for maintenance, inspection, and testing… shall be maintained at an approved, secured location for the life of the fire protection system.» Corresponde a los tres manuales, en el apartado REGISTRO. Ver A3-m2.
- **4.6.10.1:** el edificio se puede ocupar durante reparaciones solo con las protecciones requeridas mantenidas o con medidas alternativas aceptadas por la autoridad competente. Es la base de seguridad humana para una puesta fuera de servicio (A.4.6.10.1: «…a required automatic sprinkler system has been shut off…»). Ver A3-M4.
- **A.9.6.1.4:** «Records of conducted maintenance and testing and a copy of the certificate of compliance should be maintained.» Es una recomendación que conviene incorporar en el apartado REGISTRO del SDI.
- **9.7:** en la edición 2018, el 9.7 (rociadores) **no** trae requisitos de mantenimiento. Estos pasaron al 9.11.1 (inspección, prueba y mantenimiento según la NFPA 25), al 9.11.2 (deterioros según la NFPA 25) y al 9.11.3.2 (registros). El 9.7.2.1.2 sí es pertinente para el SDI (ver fila 9). Para el **SBC**, el 9.11.1 y el 9.11.2 remiten a la NFPA 25, que no está entre las fuentes: NO VERIFICABLE. El SBC no tiene apartado NFPA 101. Se sugiere agregar, al menos, el 4.6.12, el 9.11.3.1 y el 4.6.10.1.
- El 9.6.1.1 dice que el 9.6 se aplica «only where specifically required by another section of this Code». El párrafo introductorio, que dice «obligatorias donde la autoridad competente adopte ese código», es aceptable, pero conviene agregar «y donde el capítulo de ocupación correspondiente lo requiera».

---

## 3. Hallazgos

### 3.1 CRÍTICOS

#### A3-C1 · CRÍTICO · Las planillas SDI eliminan contenido obligatorio de la IRAM y no identifican al mantenedor certificado
- **Ubicación:**
  - `planillas2/SDI/SG-PEM-IFI-SDI-3_PRUEBA_TRIMESTRAL_SEMESTRAL_ANUAL_SDI.xlsx`, bloque «PRUEBA SEMESTRAL»: tiene 4 filas («Accionamiento…», «Módulos de control…», «Módulos de verificación…» y «Accionamiento de detectores de flujo») y no tiene «Prueba de detectores en ductos».
  - `SG-PEM-IFI-SDI-5_…xlsx`: no tiene las filas «Manual instructivo en español» ni «Planos de la instalación».
  - `SDI-1`, `SDI-2`, `SDI-3` y `SDI-4`: no tienen el campo «EMPRESA MANTENEDORA / N.° MANTENEDOR CERTIFICADO» ni el campo «Inspector». SDI-1 tampoco tiene «Designación del sistema».
  - El manual, en 3.1.8, dice: «Las planillas deben incluir la identificación de la empresa como mantenedor certificado.»
- **Evidencia de la norma:**
  - IRAM 3546, REQUISITOS, *Empleo de las planillas…*: «b) el mantenedor debe incluir en cada una de las planillas… la identificación de la empresa como mantenedor certificado; c) el contenido de las planillas no puede ser cambiado por el mantenedor excepto por el agregado de tareas…».
  - Planilla 6D, bloque SEMESTRAL: «…Accionamiento de detectores de flujo / **Prueba de detectores en ductos**».
  - Planilla 6B: «Manual instructivo en español / Planos de la instalación».
  - Planilla 6A: «Fecha… Inspector… Designación del sistema».
  - El texto del capítulo 6 (Pruebas, Semestral) también exige «Prueba de detectores en ductos», y el manual la tiene en 3.1.2.3 f).
- **Por qué es crítico:** el manual ordena una prueba semestral, pero la planilla oficial no permite registrarla. Las planillas que se entregan al usuario no cumplen los requisitos b) y c) de la IRAM. En una auditoría de certificación son no conformidades directas, con el mismo criterio que la auditoría anterior aplicó al plazo de retención (SDI-C1).
- **Corrección propuesta:**
  - En **SDI-3**, bloque PRUEBA SEMESTRAL, agregar después de «Accionamiento de detectores de flujo»: `Prueba de detectores en ductos: comprobar el funcionamiento de los detectores instalados en conductos. | SI | NO`.
  - En **SDI-5**, agregar dos filas al final de la grilla semanal: `Manual instructivo en español disponible` y `Planos de la instalación disponibles`.
  - En **SDI-1 a SDI-4**, reemplazar el encabezado por el de las planillas SBC y SAL: `EMPRESA MANTENEDORA: BRAFEMAR | N.° MANTENEDOR CERTIFICADO: | INSPECTOR:` y `SISTEMA / DESIGNACIÓN:`.
  - En SDI-2 y SDI-3, agregar la leyenda de codificación y la columna NA (ver A3-M1).

#### A3-C2 · CRÍTICO · Las planillas SBC-3 y SBC-6 omiten campos obligatorios de las planillas 12C y 12F
- **Ubicación:**
  - `SG-PEM-IFI-SBC-6_PRUEBAS_SBC.xlsx`:
    - no tiene la fila «Presión del piloto (MPa)» en ningún punto de prueba;
    - el bloque «CAUDAL MÁXIMO (150 %)» no tiene «Presión de succión» ni «Presión de descarga»;
    - faltan los datos de cabecera de la 12F: tablero de control (marca y listado), fuente de abastecimiento, impulsor, características eléctricas y supervisión.
  - `SG-PEM-IFI-SBC-3_INSPECCION_MENSUAL_SBC.xlsx`:
    - no tiene los datos de placa de la motobomba, la electrobomba y la bomba jockey (marca, año, caudal nominal, altura manométrica, vueltas/min, presión máxima, marca y potencia del motor);
    - no tiene «Nivel de aceite del cárter», «Nivel de electrolito de baterías» ni «Presión de agua de enfriamiento»;
    - registra una sola «Temperatura del agua de enfriamiento», cuando la 12C distingue con precalentador y en funcionamiento;
    - no separa motobomba de electrobomba.
  - El manual, en 3.1.2.1, dice: «Los datos de placa de la motobomba, la electrobomba y la bomba jockey se registran en la misma planilla.» Sus ítems f) y g) piden registrar el aceite del cárter, el electrolito y la presión de agua de enfriamiento.
  - El manual, en 3.1.2.2, ítem e) de los criterios de aceptación, exige «Presión de succión… no menor que 0 bar… al 150 %».
- **Evidencia de la norma:**
  - IRAM 3546, planilla 12F: «Presión de succión (MPa) / Presión de descarga (MPa) / Presión neta de bomba (MPa) / … / **Presión del piloto (MPa)** / Diámetro boquilla… / Coeficiente de abertura C / Caudal real L/min».
  - Planilla 12C: «MOTOBOMBA | ELECTROBOMBA – Marca… Caudal nominal… Altura manométrica… Presión máxima… / Nivel de aceite del cárter / Nivel de electrolito de baterías / Presión de agua de enfriamiento (MPa)…».
  - IRAM, REQUISITOS, ítem c), citado en A3-C1.
  - NFPA 20, 5.26.4.2: «…presión de succión mínima de 0 psi (0 bar) en el manómetro al 150 por ciento de la capacidad nominal».
- **Por qué es crítico:** sin la presión del Pitot no se puede reconstruir el caudal medido con boquillas. Sin la succión al 150 % no queda evidencia del criterio que se agregó para corregir SBC-M3. La prueba anual de la bomba queda sin trazabilidad, y la planilla altera el contenido de la norma.
- **Corrección propuesta:**
  - En **SBC-6**, agregar en los bloques CAUDAL NOMINAL y CAUDAL MÁXIMO la fila `Presión del piloto (Pitot) por boquilla | _____ MPa`.
  - En el bloque CAUDAL MÁXIMO, agregar `Presión de succión (≥ 0 bar con dispositivo de prevención de contraflujo, o ≥ mínima de diseño) | _____ MPa` y `Presión de descarga | _____ MPa`.
  - En DATOS DE LA PRUEBA, agregar `Tablero de control: marca / listado`, `Fuente de abastecimiento`, `Impulsor` y `Supervisión`.
  - En **SBC-3**, agregar un bloque `DATOS DE PLACA` con columnas MOTOBOMBA / ELECTROBOMBA / JOCKEY y las filas `Marca y año`, `Caudal nominal (m³/h)`, `Altura manométrica (m H₂O)`, `Vueltas/min`, `Presión máxima (MPa)` y `Motor: marca y potencia`.
  - En el bloque ANTES DE LA PUESTA EN MARCHA, agregar `Nivel de aceite del cárter`, `Nivel de electrolito de baterías` y `Temperatura del agua de enfriamiento con precalentador | _____ °C`.
  - En el bloque DURANTE EL FUNCIONAMIENTO, agregar `Presión de agua de enfriamiento | _____ MPa`, `Presión de aceite del motor | _____ MPa`, `Vueltas/min | _____` y `Temperatura del agua de enfriamiento en funcionamiento | _____ °C`.
  - En el bloque BOMBA JOCKEY, agregar `Cantidad de arranques indicada en el panel | _____`, que el manual pide en 3.1.2.1 i).

### 3.2 MAYORES

#### A3-M1 · MAYOR · La codificación de las planillas está mal transcripta: la IRAM usa tres símbolos
- **Ubicación:**
  - Manuales SDI, SBC y SAL, 3.1.8 (REGISTRO): «En cada planilla se debe indicar con ✓ si el ítem cumple, o con X si no cumple o no es apreciable…».
  - Leyenda de las planillas SBC-1 a SBC-6, SAL-1 a SAL-4 y SDI-5: «CUMPLE ✓ · NO CUMPLE O NO APRECIABLE X · NA: NO APLICABLE».
  - SDI-3 usa columnas SI/NO, SDI-4 usa SI CUMPLE / NO CUMPLE / NO APLICA, y SDI-1 y SDI-2 no tienen leyenda.
- **Evidencia de la norma:** en `normas/3546.docx` las celdas de la leyenda son `CUMPLE | 🗸 | NO CUMPLE | O | NO APRECIABLE | X`, y lo mismo se ve en el formato de la 12D en `3546_lin.txt`. La «O» es el **símbolo** de NO CUMPLE, no la conjunción «o». El mismo error aparece en *Cotejo_y_dudas.md* («✓ cumple y X no cumple o no apreciable»), de modo que afecta a toda la serie de 8 manuales.
- **Efecto:** se pierde la distinción entre un ítem no conforme y un ítem que no se pudo apreciar. Las no conformidades del informe -IN, que cuenta «ítems conformes», quedan mezcladas con lo no inspeccionado.
- **Corrección propuesta:**
  - En REGISTRO, 3.1.8, de los tres manuales: «En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables se indican con NA. Toda condición O o X se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y por el responsable de la instalación, con su aclaración.»
  - En la leyenda de todas las planillas: `CUMPLE ✓ · NO CUMPLE O · NO APRECIABLE X · NA: NO APLICABLE`.
  - Corregir también *Cotejo_y_dudas.md* y los otros 5 manuales.

#### A3-M2 · MAYOR · El informe SDI-2-IN evalúa la conformidad respecto de la «IRAM 3576»
- **Ubicación:** `planillas2/SDI/SG-PEM-IFI-SDI-2-IN_INFORME_GENERAL_DEL_SDI.docx`:
  - punto 3: «…conforme a los lineamientos establecidos por la NFPA 72, y su nivel de cumplimiento respecto de la IRAM 3576»;
  - punto 7: «[CONFORME / …] respecto de los requisitos establecidos por la IRAM 3576»;
  - punto 8: «Incumplimiento IRAM» sin número;
  - punto 9: «…garantizar el cumplimiento de la IRAM 3576».
  - El informe no menciona la IRAM 3546 en ningún lugar. En 5.3 pide un «tiempo promedio de activación… [ADECUADO / ELEVADO]» sin criterio de aceptación.
- **Evidencia:** el manual SDI se basa en la «IRAM 3546:2011 – Capítulo 6». La IRAM 3576 no está entre las fuentes provistas y no figura en los Documentos normativos para consulta de la IRAM 3546: **NO VERIFICABLE**. *Cambios_manuales_Martin.md* ya lo había dejado como duda («Normas que cita el informe SDI-2-IN»), pero no se resolvió. Los informes SBC-IN y SAL-1-IN sí citan «IRAM 3546:2011, capítulo 12/17, ítem ___».
- **Corrección propuesta:** alinear el informe con los de SBC y SAL.
  - Subtítulo: «Procedimiento SG-PEM-IFI-SDI · IRAM 3546:2011, capítulo 6».
  - Punto 3: «Evaluar el estado de funcionamiento, confiabilidad y capacidad de respuesta del sistema de detección y alarma de incendio, conforme a los requisitos de inspección, prueba y mantenimiento establecidos en el capítulo 6 de la IRAM 3546:2011 y en el procedimiento SG-PEM-IFI-SDI, con los criterios complementarios de la NFPA 72, edición 2016, capítulo 14.»
  - Puntos 7 y 9: reemplazar «IRAM 3576» por «IRAM 3546:2011, capítulo 6».
  - Punto 8: «NC-0n: ______ → Incumplimiento IRAM 3546:2011, capítulo 6, ítem ______».
  - Punto 5.3: quitar «tiempo promedio de activación» o reemplazarlo por «respuesta de cada dispositivo verificada en la central (NFPA 72, Tabla 14.4.3.2, ítem 17)».
  - Si Martín confirma que la IRAM 3576 es aplicable, citarla como complementaria y no como base.

#### A3-M3 · MAYOR · El manual remite tareas complementarias a planillas que no tienen filas para ellas
- **Ubicación y evidencia:**
  - **SDI 3.1.1.3 (Inspección mensual):** «Se registra en la planilla SG-PEM-IFI-SDI-2… como tarea complementaria». La SDI-2 no tiene filas de baterías. Tampoco tiene filas para 3.1.2.1 e) «Indicadores sonoros del panel», n) «Dispositivos de aviso lumínicos y sonoros» ni o) «Altavoces». Las tres están en el texto IRAM de la prueba mensual del capítulo 6, aunque no en la planilla 6C.
  - **SDI 3.1.1.4, 3.1.1.5 y 3.1.1.6 (inspecciones trimestral, semestral y anual de la NFPA 72):** «Se registra en la planilla SG-PEM-IFI-SDI-3… como tarea complementaria». La SDI-3 solo tiene las filas IRAM. También faltan las pruebas NFPA de 3.1.2.3 e), g) y h) y de 3.1.2.4 c) a m).
  - **SDI 3.1.4 (Ensayos de largo plazo):** «Se registra en la planilla SG-PEM-IFI-SDI-4…». La SDI-4 no tiene esas filas.
  - **SAL 3.1.2.2 y 3.1.4:** se registran en la SAL-3, pero la planilla no tiene filas para b) «Detectores del recinto», f) «Supervisión de circuitos», g) «Alarmas y funciones auxiliares», h) «Indicación en la alarma del edificio (NFPA 101, 9.8.2)» ni para el procedimiento posterior a una descarga.
- **Norma:** IRAM, REQUISITOS, ítem c): el agregado está **permitido**, pero tiene que estar hecho para que la planilla sea evidencia. Si la tarea no tiene fila, no queda registro. En el caso de las de 5 años y 1 año del 14.6.2.2 de la NFPA 72, que el manual mismo exige conservar, se pierde además ese registro.
- **Corrección propuesta:** agregar al pie de cada planilla un bloque `TAREAS COMPLEMENTARIAS (NFPA)` con las filas siguientes.
  - **SDI-2:** `Baterías: corrosión, fugas, conexiones, fecha (mensual, NFPA 72 T.14.3.1-9)`, `Nivel de electrolito plomo-ácido`, `Indicadores sonoros del panel`, `Dispositivos de aviso lumínicos y sonoros` y `Altavoces del sistema de audio`.
  - **SDI-3:** subbloques `INSPECCIÓN TRIMESTRAL`, `INSPECCIÓN SEMESTRAL` e `INSPECCIÓN ANUAL`, con un renglón por ítem de 3.1.1.4 a 3.1.1.6, y `PRUEBAS NFPA`, con un renglón por cada ítem de 3.1.2.3 e) a h) y 3.1.2.4 c) a m).
  - **SDI-4:** `Sensibilidad de detectores de humo (fecha de la última prueba / próxima)`, `Detectores no restaurables a 15 años`, `Detectores de temperatura restaurables probados este año (identificación)`.
  - **SAL-3:** `Detectores del recinto (prueba funcional anual)`, `Supervisión por circuito abierto`, `Alarmas, retardo y cierres`, `Indicación en la alarma del edificio` y `Restablecimiento posterior a descarga`.

#### A3-M4 · MAYOR · SDI y SAL no tienen procedimiento de desactivación (puesta fuera de servicio), y lo atribuido al 9.6.1.5 no está en ese artículo
- **Ubicación:**
  - SDI 3.1.6 e): «Sistema fuera de servicio (9.6.1.5): los procedimientos ante la salida de servicio del sistema deben cumplir la NFPA 72: notificación al responsable de la instalación, medidas compensatorias mientras dure la condición y registro de su inicio y fin.»
  - SDI 3.1.2: «Si una deficiencia no se corrige al finalizar la prueba, se debe informar por escrito al responsable de la instalación.»
  - SAL: solo se trata la condición fuera de servicio luego de una descarga (3.1.4).
- **Evidencia:**
  - NFPA 101, 9.6.1.5: «Fire alarm system impairment procedures shall comply with NFPA 72», sin ningún otro contenido.
  - NFPA 72, 14.2.2.2.1: «Los requisitos de la Sección 10.20 deben ser aplicables cuando un sistema presente una desactivación».
  - NFPA 72, 10.20.1: notificar al propietario.
  - NFPA 72, 10.20.2: registro de desactivaciones «durante un período de un año a partir de la fecha en que se haya corregido».
  - NFPA 72, 10.20.4: «El proveedor del servicio debe informar a la autoridad competente sobre cualquier sistema que se encuentre fuera de servicio durante más de ocho horas».
  - NFPA 72, 10.20.5: medidas de mitigación «Donde sea requerido por la autoridad competente».
  - NFPA 72, 10.20.6: aviso de finalización.
  - NFPA 72, 14.2.2.2.3: si una deficiencia no se corrige, se informa «por escrito y dentro de las 24 horas».
  - NFPA 101, 4.6.10.1: el edificio se ocupa solo con las protecciones mantenidas o con medidas alternativas aceptadas por la autoridad competente.
  - La IRAM, cap. 12, exige seguir «un procedimiento adecuado» ante la puesta fuera de servicio. El SBC lo trata, pero el SDI y el SAL no.
- **Corrección propuesta:**
  - En SDI y SAL, agregar en 3.1.2 (PRUEBA), después del primer párrafo:
    «**Desactivación del sistema.** Cuando el sistema o una parte de él quede fuera de servicio, se debe: a) notificar al propietario o a su representante y al servicio de monitoreo; b) informar a la autoridad competente si la condición se prolonga más de ocho horas; c) aplicar las medidas de mitigación que la autoridad competente requiera, como ronda de vigilancia o restricción de uso del área, y no habilitar la ocupación de las áreas afectadas sin protección o medidas alternativas aceptadas (NFPA 101, 4.6.10.1); d) notificar la finalización de la desactivación; e) registrar inicio, fin, causa y medidas adoptadas, conservando el registro como mínimo tres años (IRAM 3546:2011; NFPA 72, edición 2016, 10.20). Las deficiencias no corregidas al finalizar la tarea se informan por escrito al propietario dentro de las 24 h (NFPA 72, 14.2.2.2.3).»
  - En SDI 3.1.6 e), reemplazar el ítem por: «Sistema fuera de servicio (9.6.1.5): los procedimientos ante la desactivación del sistema de alarma deben cumplir la NFPA 72; se aplican según el apartado *Desactivación del sistema* de este procedimiento (NFPA 72, edición 2016, 10.20).»

#### A3-M5 · MAYOR · Atribuciones a la NFPA 101 que el texto no respalda
- **Ubicación:**
  - (a) SDI 3.1.6 d): «…con un programa aprobado que asegure su integridad operativa; el presente procedimiento constituye ese programa.»
  - (b) SDI 3.1.2.4 i): «…y la detención del aire acondicionado (NFPA 101, 9.6.5.2).»
  - (c) SAL 3.1.6 f): «Funciones de control (9.6.5.2): la detención del aire acondicionado, la liberación de retenedores de puertas y el desbloqueo de puertas comandados por el sistema deben verificarse en la prueba anual, porque aseguran la retención del agente y la evacuación de las personas.»
- **Evidencia:**
  - NFPA 101, 9.6.1.4: «…shall have an **approved** maintenance and testing program…». En la NFPA, *approved* significa aceptable para la autoridad competente: el procedimiento no se convierte en ese programa por declararlo así.
  - NFPA 101, 9.6.5.2: «Where required by another section of this Code, the following functions shall be actuated: …». Es un requisito de funcionamiento, sin frecuencia de prueba.
  - La prueba anual está en la NFPA 72, Tabla 14.4.3.2, ítem 24 «Funciones de control de emergencias – Anualmente – …verificar la activación de los dispositivos interfaz… verificar que… haya sido restaurado apropiadamente».
- **Corrección propuesta:**
  - (a) «…con un programa aprobado que asegure su integridad operativa; el presente procedimiento puede constituir ese programa una vez aceptado por la autoridad competente.»
  - (b) Cambiar la cita por «(NFPA 72, edición 2016, Tabla 14.4.3.2, ítem 24; funciones enumeradas en la NFPA 101, 9.6.5.2)».
  - (c) «Funciones de control (9.6.5.2): donde otra sección del código lo requiera, el sistema de alarma debe actuar la liberación de retenedores de puertas, el desbloqueo de puertas y la detención del aire acondicionado, entre otras funciones. Su verificación anual se realiza según la NFPA 72, edición 2016, Tabla 14.4.3.2, ítem 24. En este sistema esas funciones son además necesarias para mantener la concentración de diseño del agente.»

#### A3-M6 · MAYOR · SAL: falta el procedimiento documentado de verificación de la calidad del agente
- **Ubicación:** SAL 3.1.2.3, último párrafo: «El vaciado del cilindro lo realiza personal competente, con recuperación del agente y no por venteo.» También 3.1.3.1, criterio «rellenar o sustituir», y 3.1.4 d), «reposición del agente extintor». Ninguno de los tres exige verificar el agente recuperado o el de reposición.
- **Evidencia:** IRAM 3546, REQUISITOS, *Mantenimiento de las Instalaciones*: «Para verificar la calidad del agente extintor se debe contar con procedimientos documentados en función de las normas de aplicación.» La norma específica (NFPA 2001) es NO VERIFICABLE.
- **Corrección propuesta:** agregar al final de 3.1.2.3 y de 3.1.4 d):
  «El agente recuperado o de reposición debe corresponder al tipo y a la especificación indicados en la placa del sistema y en la planilla SG-PEM-IFI-SAL-1. Su calidad se debe verificar según un procedimiento documentado, en función de las normas de aplicación y de las instrucciones del fabricante del sistema, con certificado de análisis del proveedor o del recuperador (IRAM 3546:2011, requisitos de mantenimiento de las instalaciones). No se debe mezclar agentes distintos ni recargar con agente de origen no certificado.»
  Declarar en *Dudas* que, sin la NFPA 2001, no se fijan valores de pureza ni de humedad.

### 3.3 MENORES

#### A3-m1 · MENOR · NFPA 101: condiciones de aplicación omitidas y requisitos de diseño mezclados con inspección, prueba y mantenimiento
- SDI 3.1.6 h), 9.6.3.6: agregar «…según el método aprobado: evacuación general en todo el edificio, salvo escaleras de salida y cabinas de ascensor (9.6.3.6.1), notificación selectiva por zonas aprobada por la autoridad competente (9.6.3.6.2) o modo privado (9.6.3.6.3)». Agregar también: «los sistemas de comunicación de emergencia por voz pueden usarse para otros fines según la NFPA 72 (9.6.3.10.2)».
- SDI 3.1.6 j), 9.6.7: anteponer «Donde se requiera anunciación (9.6.7.1)» y agregar «las señales de falla y de supervisión deben anunciarse en forma audible y visible (9.6.7.5 y 9.6.7.6)».
- SDI l) y SAL g), 9.11.4: anteponer «Donde lo exijan los capítulos 11 a 43 del código y…».
- SDI g), 9.6.2.10.4: «…medidos a lo largo de un recorrido horizontal desde el artefacto…», con mención de la excepción del 9.6.2.10.5. Hay que aclarar que es un requisito de ubicación tomado de la NFPA 72, cap. 29, o agregar en 3.1.1.6 a): «…incluida la distancia de los detectores de humo a artefactos de cocción fijos (NFPA 101, 9.6.2.10.4)».
- SDI b) y SAL b): «…se deben mantener o retirar; no se deben dejar instalados en condición inoperativa (NFPA 101, A.4.6.12.3, no obligatorio)».

#### A3-m2 · MENOR · NFPA 101: faltan la documentación y la asignación de los simulacros
- En el apartado REGISTRO (3.1.8 en SDI y SAL; 3.1.6 en SBC), agregar: «La documentación de diseño del sistema y los procedimientos de inspección, prueba y mantenimiento se deben conservar en un lugar aprobado y seguro durante toda la vida útil del sistema (NFPA 101, 9.11.3.1; NFPA 72, 14.6.1.3). Se recomienda conservar junto con los registros una copia del certificado de cumplimiento (NFPA 101, A.9.6.1.4).»
- En CONTROL DE CAMBIOS Y RESPONSABILIDADES de SDI y SAL: «Los simulacros de evacuación, donde sean requeridos, son responsabilidad del propietario o usuario; su registro escrito debe indicar fecha, hora, participantes, lugar y resultados (NFPA 101, 4.7.6 y A.4.7.6).»

#### A3-m3 · MENOR · SDI: pruebas de la NFPA 72 sin incorporar
Hay que agregar a 3.1.2.4 (Prueba anual), con la aclaración «cuando existan»:
- 17(a): dispositivos electromecánicos de descarga, verificados retirando el eslabón fusible;
- 17(b): interruptores de alarma de los sistemas de extinción;
- 17(c): detectores de gas, según el fabricante;
- 17(e): todos los avisadores manuales; hoy solo están en el protocolo;
- 5(a) a (f): equipos de comunicación de emergencia;
- 22(b): aparatos textuales audibles, con información distinguible y comprensible;
- 4(b): DACT, con recepción dentro de los 90 s y dos medios de transmisión.

Agregar a 3.1.4 a): «En zonas donde las falsas alarmas aumenten respecto del año anterior, se deben realizar pruebas de calibración (14.4.4.3.3.2).»

Agregar a 3.1.7: «Las reparaciones del hardware de la central se prueban según los ítems 2(a) y 2(d) de la Tabla 14.4.3.2 (14.4.2.3), y los cambios del software ejecutivo, con el 10 % del sistema (14.4.2.5).»

#### A3-m4 · MENOR · SAL: equipos para riesgos especiales de la NFPA 72 incompletos y una cita imprecisa
- En el protocolo de prueba de funcionamiento, el paso «Circuito de disparo y supervisión» atribuye la «lámpara de prueba» al ítem 18(f). En la Tabla 14.4.3.2, el 18(f) solo dice «Verificar el funcionamiento del solenoide»; la lámpara AGI corresponde al 18(g), que es el dispositivo explosivo.
- Redacción propuesta: «verificar el funcionamiento del solenoide de descarga con carga simulada según el fabricante (18(f)); en circuitos con dispositivo explosivo, con lámpara de flash AGI u otra luz de prueba aprobada (18(g)); en circuitos de tipo matriz, accionar todos los sensores y verificar la matriz (18(e)); en circuitos de zona verificada, secuencial o de conteo, accionar los sensores en un mínimo de cuatro lugares del circuito (18(h)); supervisión mediante circuito abierto (18(i)).»
- Interruptores de aborto: distinguir el tipo hombre muerto y el especial, en los que se verifica la secuencia, del tipo reciclaje, en el que se verifica la matriz con cada sensor (18(a) a (c)).

#### A3-m5 · MENOR · SBC: omisiones de detalle respecto de la IRAM y de la 12E
- 3.1.2.1 d): agregar «(para controles de parada automática)» después de «el tiempo de marcha desde el arranque».
- 3.1.2.2 g): agregar «Lo mismo se aplica a las llaves de transferencia automática.»
- 3.1.3.4 e) y SBC-5: agregar la tarea «Cañería de combustible (A)», que es una fila de la 12E.
- 3.1.3.1 b) y SBC-4 dicen «carcasa» donde la 12D dice «cárter». Declarar la interpretación en *Dudas*.
- Nota de la frecuencia «B» en 3.1.3.4: la 12D ya asigna frecuencia mensual a «Interruptores o fusibles» (sigue SBC-m2). Redacción propuesta: «La planilla IRAM 3546-12D asigna frecuencia mensual a la verificación de interruptores o fusibles del sistema eléctrico, y la 12E les asigna la frecuencia «B». Se adopta la verificación mensual, más exigente; la «B» se interpreta como bienal, a confirmar.»
- SBC-2: agregar las filas `Corriente de carga de baterías (bancos 1 y 2) (A)` y `Luces piloto de baterías encendidas o de falla apagadas`, del texto IRAM, motor diésel c), d) y e).

#### A3-m6 · MENOR · SBC: alcance de las citas NFPA 20 y valores sin fuente en los textos provistos
- **NFPA 20, 14.4:** «Las bombas contra incendio deberán inspeccionarse, probarse y mantenerse de acuerdo con la NFPA 25». Los valores del 14.2 son de la **prueba de aceptación**. Agregar a 3.1, segundo párrafo: «…los valores de la prueba de aceptación en campo de la NFPA 20 (14.2) se aplican por analogía a la prueba anual; la NFPA 25, a la que remite la NFPA 20, 14.4, no se encuentra disponible.»
- **7.1.2.1 y 7.1.2.2** corresponden a las bombas tipo turbina de eje vertical (cap. 7). Para las bombas centrífugas horizontales rige el 6.2. Redacción propuesta para d): «(NFPA 20, 6.2.2, cuya versión en español indica «40 %» por error de traducción; el valor de 140 % se confirma en el 7.1.2.2 para bombas verticales)».
- **5.26.4.2** se refiere a un «dispositivo de prevención de contraflujo», no a cualquier antirretorno. Cambiar «con dispositivo antirretorno» por «con dispositivo o montaje de prevención de contraflujo».
- **±1 %** de los manómetros de prueba: agregar la cita «(NFPA 20, 14.2.7.1.2)» en el criterio del paso «Instrumentos».
- **Tubo Pitot a medio diámetro:** es VERIFICABLE en la NFPA 13 (ed. 2019), A.5.2.2 («The pitot tube should be held approximately one-half the diameter of the hydrant or nozzle opening away from the opening… in the center of the stream»). Agregar la cita.
- **Q = 0,0666 · c · d² · √P y leyes de afinidad:** NO VERIFICABLE en los textos provistos. El coeficiente es dimensionalmente correcto (29,83 gpm/(in²·√psi) convertido a L/min, mm y kPa da 0,0666). Declararlos en *Valores y contenidos agregados* como relaciones físicas generales.
- Falta la **nueva prueba de campo después de reemplazar un componente fundamental** (NFPA 20, 14.5.2.1: «Cuando se reemplaza, cambia o modifica un componente fundamental… deberá efectuarse una nueva prueba en el lugar»). Agregar en 3.1.5: «Cuando se reemplace, cambie o modifique un componente fundamental de la bomba, del impulsor o del controlador, se debe realizar una nueva prueba de rendimiento en campo y registrarla en la planilla SG-PEM-IFI-SBC-6 (NFPA 20, 14.5.2.1).»

#### A3-m7 · MENOR · SAL: seguridad y textos tipo
- 3.1.1, regla de autocontrol: le falta «dejando constancia de los hallazgos verificados», que sí está en la IRAM, en el SDI y en el SBC. Redacción propuesta: «…el mantenedor debe verificar su correcto cumplimiento, dejando constancia de los hallazgos verificados. En el presente sistema la IRAM 3546:2011 no establece inspecciones de esa frecuencia.»
- 3.1.5: siguen sin incorporarse dos puntos de SAL-m3.
  - Agregar e): «Productos de descomposición: después de una descarga sobre un fuego, los agentes halogenados generan productos de descomposición tóxicos y corrosivos; el reingreso se hace con ventilación forzada y con protección respiratoria cuando no se pueda verificar la atmósfera.»
  - Agregar f): «Sala de cilindros: los recipientes deben estar sujetos y ningún cilindro se mueve con el cabezal de control montado.»
- 3.1.3: el «Mantenimiento mensual» sin tareas está dentro de la definición (sigue SAL-m2). Es aceptable, pero lo coherente con la serie es el subtítulo «Mantenimiento mensual» seguido de «La IRAM 3546:2011 no establece tareas de mantenimiento mensual para este sistema.»

#### A3-m8 · MENOR · Coherencia de títulos, códigos y forma (ver la tabla 6)
- **SDI-3:** el título del xlsx dice «PRUEBA - SISTEMA CONVENCIONAL DE DOS HILOS». Debe decir «PRUEBA TRIMESTRAL, SEMESTRAL Y ANUAL – SISTEMA CONVENCIONAL DE DOS HILOS», y el encabezado «SISTEMA DE DETECCIÓN DE INCENDIOS», en plural y con tilde.
- **SDI-2, SDI-3 y SDI-4** dicen «T.C. 3 años». Unificar a «T.C. 3 AÑOS».
- **Erratas** en SDI-2: «Panela de audio para evaluación» → «Panel de audio para evacuación»; «Indicaciòn» → «Indicación»; «RESPONSABLE DEL LA INSTLACION» → «RESPONSABLE DE LA INSTALACIÓN».
- **Erratas** en SDI-1: «Memoria técnica del conexión» → «Memoria técnica de la conexión»; «DETECCION» → «DETECCIÓN».
- **SDI-4:** «( según plan de registro)» → «(según planillas de registro)», según la 6E.
- **Anexos del informe SDI-2-IN:** «SDI-1 General SDI» → «SDI-1 Información general SDI»; «SDI-3 Prueba Trimestral Semestral Anual SDI» → «SDI-3 Prueba trimestral, semestral y anual SDI»; «SDI-4 Anual SDI» → «SDI-4 Mantenimiento anual SDI».
- **Encabezados:** los informes dicen «INSTALACIONES FIJAS CONTRAINCENDIOS» y los manuales «CONTRA INCENDIOS».
- **Nombre del sistema SBC:** la portada y el 3.1 dicen «SISTEMA DE BOMBAS CONTRA INCENDIO», el encabezado «Bombas Contraincendios» y las planillas IRAM «CONTRA INCENDIOS». Sigue SBC-m5.
- **Códigos de informe** «SDI-2-IN» y «SAL-1-IN»: el número coincide con el de una planilla. Sigue SDI-M2; se decide junto con la numeración de la SDI-5.
- **Cambios_manuales_Martin.md** está desactualizado. En la sección SDI dice «Registros: se conservan hasta la prueba siguiente y un año más» y en la seguridad humana dice «15 mayores», cuando fueron 16.
- **Párrafo común de «Concordancia»:** dice «no prescribe en todos los casos frecuencias rígidas» y enumera frecuencias «semanales… trimestrales» que no existen en SAL. Contradice el segundo párrafo de 3.1 («La IRAM 3546:2011… fija sus frecuencias»). Redacción propuesta: «La IRAM 3546:2011 fija las tareas y frecuencias mínimas de cada sistema en sus planillas; el presente procedimiento las adopta, las complementa con métodos y criterios de aceptación de las normas NFPA aplicables y define listas de verificación y protocolos de ensayo para su aplicación uniforme.»

---

## 4. Verificación de las correcciones de la auditoría anterior (tarea 2)

| ID anterior | Tema | Estado | Evidencia en el .docx final o en las planillas |
|---|---|---|---|
| SDI-C1 | Retención de registros | **CORREGIDO** | 3.1.8: «Los registros se deben conservar como mínimo durante tres años, según la IRAM 3546:2011; los de los detectores de temperatura restaurables probados en forma rotativa, durante el ciclo completo de cinco años más un año, según la NFPA 72, edición 2016, 14.6.2…». Las 5 planillas dicen «T.C. 3 AÑOS/años». |
| SBC-C1 | Bloqueo del arranque | **CORREGIDO** | 3.1.4 c): «Bloqueo de arranque: antes de intervenir partes rotantes o eléctricas, pasar el controlador a posición apagado y abrir, bloquear y etiquetar el seccionador; en motores diésel… desconectar los dos bancos de baterías…». |
| SAL-C1 | Seguridad en la pesada | **CORREGIDO** | 3.1.3.1, «Protocolo de Ensayo: pesada de recipientes», con los pasos Aseguramiento («retirar el cabezal de control y el actuador manual… tapa de protección y el dispositivo antirretroceso»), Pesada y Reconexión («reponer el cabezal en último lugar»). En a): «en agentes halogenados… en gases inertes, la carga se controla por presión». |
| SDI-M1 | Aislamiento de salidas antes de probar iniciadores | **CORREGIDO** | Protocolo de iniciadores, paso «Aislamiento de salidas… desconectar los solenoides o actuadores de descarga… (NFPA 72, 14.2.6.4)». |
| SDI-M2 | Orden de letras y nombre de la planilla 6B | **PARCIAL** | El nombre ya es literal («SG-PEM-IFI-SDI-5… Información semanal (autocontrol)», en 3.1.1.2, en el cap. 4 y en el xlsx). Se mantiene el número 5 y el informe «SDI-2-IN», y la excepción figura solo en *Cambios…* como «Decisiones que quedan para Martín». No existe un cotejo SDI que la apruebe. |
| SDI-M3 | Campos de la 6B en el cuerpo | **CORREGIDO** | 3.1.1.2, ítems a) («…barreras infrarrojas… sistemas aspiradores») y h) a l). La planilla SDI-5 tiene las filas. Lo que falta de la 6B en la planilla está en A3-C1. |
| SDI-M4 | «8,3 %» de la 6E | **CORREGIDO** | 3.1.3.1 c) y d): «(8,3 %, según la planilla IRAM 3546-6E)». La SDI-4 también lo tiene. La duda está declarada en *Cambios…*. |
| SDI-M5 | Inspecciones NFPA trimestral, semestral y anual | **CORREGIDO** (manual) | 3.1.1.4 a) a c) y 3.1.1.5 f) a h); 3.1.1.6 c) a e). Las filas de planilla que faltan están en A3-M3. |
| SDI-M6 | Pruebas NFPA faltantes | **CORREGIDO** | 3.1.2.4 j) («Baterías: reemplazarlas…»), k) («…con carga máxima…») y l) («…rellamada del silenciamiento y los interruptores de desconexión»); 3.1.2.3 h) (llama); protocolo, paso «Detectores especiales»; 3.1.2.3 g) («hidrómetro de lectura numérica»). |
| SBC-M1 | Criterio de corriente | **CORREGIDO** | 3.1.2.2, criterio b): «…no debe superar la corriente de plena carga de placa multiplicada por el factor de servicio (NFPA 20, 14.2.7.4.4); con tensión distinta… (IRAM 3546:2011; NFPA 20, 14.2.7.4.5)». |
| SBC-M2 | Caudal cero sin aislar la red | **CORREGIDO** | Protocolo anual, paso «Caudal cero»: «…con la válvula de descarga al sistema abierta… si por razones operativas se debe aislar la red, se aplica el procedimiento de puesta fuera de servicio». |
| SBC-M3 | Presión de succión al 150 % | **CORREGIDO** (manual) | Criterio e): «…no menor que 0 bar en el manómetro al 150 %… (NFPA 20, 5.26.4.2)». Paso «Caudal máximo»: «…incluida la presión de succión… ante fluctuaciones… interrumpir». La SBC-6 no tiene la fila (A3-C2) y la cita del dispositivo es imprecisa (A3-m6). |
| SBC-M4 | Prueba semanal en planilla mensual | **CORREGIDO** | 3.1.2.1: «La planilla IRAM 3546-12C es de frecuencia mensual. En sistemas con motobomba, cada prueba semanal se registra en una planilla SG-PEM-IFI-SBC-3 propia; en sistemas sin motobomba…». |
| SBC-M5 | Campos de la 12C | **PARCIAL** | El texto está corregido: 3.1.2.1 f) («Motor diésel antes de la marcha: … nivel de aceite del cárter, … electrolito… fechas del último cambio…») y g). Pero el manual dice que los datos de placa «se registran en la misma planilla», y la SBC-3 no tiene datos de placa ni varios campos de la 12C (A3-C2). |
| SBC-M6 | Contenido de Martín recuperable | **CORREGIDO** | Paso «Termografía y equilibrio de fases»; 3.1.2.1 i) (arranques de la jockey); paso «Caudal nominal», con «purgar la toma del manovacuómetro» y el rótulo «Qué se determina con la lectura» (filtro, pérdidas de carga, entrada de aire); paso «Medición por boquillas» («…no descargar sin boquilla…»). |
| SAL-M1 | Regla de autocontrol | **CORREGIDO** | 3.1.1: «Las inspecciones de frecuencia menor a un mes pueden ser completadas por el usuario… En el presente sistema la IRAM 3546:2011 no establece inspecciones de esa frecuencia.» Le falta «dejando constancia de los hallazgos» (A3-m7). |
| SAL-M2 | Ausencia de tensión antes de reconectar | **CORREGIDO** | Protocolo de cabezales, paso «Reconexión»: «…medir con voltímetro, en los bornes del circuito de disparo, la ausencia de tensión; verificar que no haya alarmas, prealarmas ni retardos activos… reconectar los cabezales de a uno, empezando por el piloto». |
| SAL-M3 | Protocolos de estanqueidad, secuencia y prueba hidrostática | **CORREGIDO** | «Protocolo de Ensayo: estanqueidad del recinto» (3.1.1.3); «Protocolo de Ensayo: prueba de funcionamiento del sistema» (3.1.2.2); 3.1.2.3: «…presiones de prueba de la IRAM 2529-1 y del fabricante… con recuperación del agente y no por venteo». |
| SAL-M4 | Detección y disparo según el SDI | **CORREGIDO** | 3.1.2.2: «La central de detección y disparo, sus fuentes de energía… se inspeccionan, prueban y mantienen según el procedimiento SG-PEM-IFI-SDI…», y b) «Detectores del recinto: … prueba funcional anual…». |

**Resultado:** 17 CORREGIDOS y 2 PARCIALES (SDI-M2 y SBC-M5), sin NO CORREGIDOS. Tres de los corregidos tienen una salvedad en la planilla, que se cuenta como hallazgo nuevo: SDI-M3 y SDI-M5 (A3-C1 y A3-M3) y SBC-M3 (A3-C2). **No hay regresiones** en el cuerpo de los manuales. Se observa una regresión documental: *Cambios_manuales_Martin.md* sigue diciendo que en el SDI los registros se conservan «hasta la prueba siguiente y un año más» (A3-m8).

---

## 5. Cotejo por manual (tarea 3)

Estados posibles: OK, FALTA, FRECUENCIA DISTINTA y VALOR DISTINTO. Cuando el texto del manual está bien pero la planilla no, se indica en la columna Estado.

### 5.1 SDI · IRAM 3546, cap. 6 (Sistema de detección de incendios convencional de dos hilos)

| # | Requisito IRAM (cap. 6 / planilla) | Frec. | Manual | Planilla | Estado |
|---|---|---|---|---|---|
| 1 | Inspección: ratificar existencia de planos | — (6B: semanal) | 3.1.1.1 a) | SDI-1 («¿Existe plano del cableado?») | OK texto · **FALTA** fila en SDI-5 (6B) |
| 2 | Manual instructivo en español | — (6B: semanal) | 3.1.1.1 b) | SDI-1 | OK texto · **FALTA** fila en SDI-5 (6B) |
| 3 | Planillas de eventos del mes | M | 3.1.1.1 c) | SDI-1 (sin fila) | OK texto · sin fila específica |
| 4 | Estado de dispositivos de iniciación (humo, temperatura, gas, llama; 6B: barreras, aspirador) | S | 3.1.1.2 a) | SDI-5 | OK |
| 5 | Pulsadores no obstruidos | S | 3.1.1.2 b) | SDI-5 | OK |
| 6 | Dispositivos de aviso (acústicos, sirenas, estroboscópicas) | S | 3.1.1.2 c) | SDI-5 | OK |
| 7 | Panel de alarma, LED y visor | S | 3.1.1.2 d) | SDI-5 | OK |
| 8 | Detectores no obstruidos, sin pintura, sin daños | S | 3.1.1.2 e) | SDI-5 | OK |
| 9 | Tuberías: estado, daños, corrosión, alineación, cargas | S | 3.1.1.2 f) | SDI-5 | OK |
| 10 | Eventos mensuales repetidos | S | 3.1.1.2 g) | SDI-5 | OK |
| 11 | Nota 10: tuberías ocultas | — | 3.1.1.2, párrafo final | — | OK |
| 12 | 6B: tensión primaria y secundaria | S | 3.1.1.2 h) | SDI-5 | OK |
| 13 | 6B: zonas con falla y zonas conectadas | S | 3.1.1.2 i) | SDI-5 | OK |
| 14 | 6B: nivel de tanque, flujo, baja presión, arranque de bomba | S | 3.1.1.2 j) | SDI-5 | OK |
| 15 | 6B: componentes incrustados y en alineación | S | 3.1.1.2 k) | SDI-5 | OK |
| 16 | 6B: planillas de eventos de la semana | S | 3.1.1.2 l) | SDI-5 | OK |
| 17 | Prueba mensual: fusibles | M | 3.1.2.1 a) | SDI-2 | OK |
| 18 | Equipos en interfase | M | 3.1.2.1 b) | SDI-2 | OK |
| 19 | Alimentación primaria | M | 3.1.2.1 c) | SDI-2 | OK |
| 20 | Indicadores lumínicos del panel | M | 3.1.2.1 d) | SDI-2 | OK |
| 21 | Indicadores sonoros del panel | M | 3.1.2.1 e) | — | OK texto · **FALTA** fila en SDI-2 (A3-M3) |
| 22 | Señales de falla, simulación | M | 3.1.2.1 f) | SDI-2 | OK |
| 23 | Conexiones de red | M | 3.1.2.1 g) | SDI-2 | OK |
| 24 | Panel de audio para evacuación | M | 3.1.2.1 h) | SDI-2 («Panela de audio para evaluación») | OK · errata (A3-m8) |
| 25 | Tensión de baterías | M | 3.1.2.1 i) | SDI-2 | OK |
| 26 | Conexiones central-zona | M | 3.1.2.1 j) | SDI-2 | OK |
| 27 | Anunciadores remotos y comando | M | 3.1.2.1 k) | SDI-2 | OK |
| 28 | Discador telefónico | M | 3.1.2.1 l) | SDI-2 | OK |
| 29 | Detectores según fabricante (humo, temperatura, gas, llama, aspiración) | M | 3.1.2.1 m) + protocolo | SDI-2 (elementos de iniciación) | OK |
| 30 | Dispositivos de aviso lumínicos y sonoros | M | 3.1.2.1 n) | — | OK texto · **FALTA** fila en SDI-2 |
| 31 | Altavoces de audio | M | 3.1.2.1 o) | — | OK texto · **FALTA** fila en SDI-2 |
| 32 | Ensayo del cargador | T | 3.1.2.2 a) + protocolo | SDI-3 | OK |
| 33 | Prueba de descarga de baterías | T | 3.1.2.2 b) + protocolo | SDI-3 | OK |
| 34 | Accionamiento de dispositivos y su correspondencia | Sem | 3.1.2.3 a) | SDI-3 | OK |
| 35 | Módulos de control | Sem | 3.1.2.3 b) | SDI-3 | OK |
| 36 | Módulos de verificación | Sem | 3.1.2.3 c) | SDI-3 | OK |
| 37 | Accionamiento de detectores de flujo | Sem | 3.1.2.3 d) | SDI-3 | OK |
| 38 | **Prueba de detectores en ductos** | Sem | 3.1.2.3 f) | — | OK texto · **FALTA** en SDI-3 (A3-C1) |
| 39 | Prueba de baterías (24 h) | A | 3.1.2.4 a) + protocolo | SDI-3 | OK |
| 40 | Planimetría | A | 3.1.2.4 b) | SDI-3 | OK |
| 41 | Mantenimiento: limpieza del panel de control | A | 3.1.3.1 a) | SDI-4 | OK |
| 42 | Limpieza del panel de audio | A | 3.1.3.1 b) | SDI-4 | OK |
| 43 | Limpieza y calibración de humo y temperatura (8,3 %) | A | 3.1.3.1 c) | SDI-4 | OK |
| 44 | Limpieza y calibración de gas (8,3 %) | A | 3.1.3.1 d) | SDI-4 | OK |
| 45 | Verificación de valores y reemplazo | A | 3.1.3.1 e) | SDI-4 | OK |
| 46 | 5 % de repuestos por tipo | — | 3.1.3.1, párrafo | — | OK |
| 47 | Reemplazo por vida útil | A | 3.1.3.1 f) | SDI-4 | OK |
| 48 | Modificación o reparación según eventos | A | 3.1.3.1 g) | SDI-4 | OK |
| 49 | Mantenimiento inmediato después de pruebas con fallas | — | 3.1.2 y 3.1.3 | — | OK |
| 50 | Requisitos: autocontrol < 1 mes; verificación del mantenedor | — | 3.1.1 | SDI-5 («USUARIO (AUTOCONTROL) / SUPERVISOR») | OK |
| 51 | Requisitos: evaluación según la IRAM 3619 | — | 3.1.1 | — | OK |
| 52 | Requisitos: registros ≥ 3 años | — | 3.1.8 | T.C. 3 AÑOS/años | OK |
| 53 | Requisitos: identificación del mantenedor en cada planilla | — | 3.1.8 | Solo SDI-5 | **FALTA** en SDI-1 a SDI-4 (A3-C1) |
| 54 | Requisitos: leyenda NA | — | 3.1.8 | SDI-4 y SDI-5 | **FALTA** en SDI-1 a SDI-3 |
| 55 | Codificación ✓ / O / X | — | 3.1.8 | Varias | **VALOR DISTINTO** (A3-M1) |

**Valores NFPA citados en el SDI** (NFPA 72, ed. 2016, salvo indicación):

| Valor del manual | Ubicación | Fuente | Resultado |
|---|---|---|---|
| Intervalos ≤ 18 meses para inaccesibles, con aprobación de la autoridad competente | 3.1.1 | 14.3.2 + 14.3.3 («no deben exceder los 18 meses») y 14.4.4.1 | OK. El 18 está en el 14.3.3 para la inspección; conviene citarlo |
| Notificación antes y después; coordinación | 3.1 | 14.2.4.1, 14.2.4.2 y 14.2.4.3 | OK |
| Aislamiento de supresión durante la prueba | Protocolo, paso 1 | 14.2.6.4 | OK |
| Humo por ventilaciones; no imán | Protocolo, paso 2 | T.14.4.3.2 17(g)(1); 17(l) («verificación electrónica (imanes…) no es suficiente») | OK |
| Calor: fuente listada; no restaurables sin calor | Protocolo, paso 3 | 17(d)(1) y (3) | OK |
| Muestreo desde el extremo de cada tramo; ducto; haz con filtro | Protocolo, paso 5 | 17(g)(4), (5) y (6) | OK |
| Proteger la memoria volátil antes de probar baterías | Protocolo trimestral, paso 1 | T.14.4.3.2, 7/9 («…software… protegido contra pérdidas») | OK |
| 2,30 V/celda ± 0,02 V a 25 °C (plomo-ácido y selladas) | Protocolo trimestral, paso 2 | 9(a)(2) y 9(c)(2) | OK |
| Níquel-cadmio: 1/30 a 1/25 de la capacidad | Protocolo trimestral, paso 2 | 9(b)(2) | OK |
| Descarga con carga artificial equivalente | Protocolo trimestral, paso 3 | 9(a)(3), (b)(3) y (c)(3) | OK. La NFPA es anual y la IRAM trimestral: rige la trimestral |
| ≥ 2,05 V/celda bajo carga (plomo-ácido abiertas) | 3.1.2.3 g) | 9(a)(4) | OK |
| Gravedad específica con hidrómetro numérico | 3.1.2.3 g) | 9(a)(5) | OK |
| Selladas: según el fabricante | 3.1.2.3 g) | 9(c)(4) | OK |
| Níquel-cadmio: 1,42 V/celda de flotación | 3.1.2.3 g) | 9(b)(4) | OK |
| Válvula: dentro de 2 vueltas o 1/5 del recorrido | 3.1.2.3 e) | 17(j)(1), semestral | OK |
| Llama: semestral y sensibilidad calibrada; sin luz no medida | 3.1.2.3 h) | 17(f) | OK |
| 70 kPa; 4,4 °C; 70 mm / 300 mm | 3.1.2.4 g) | 17(j)(2) a (5) | OK |
| ≥ 2 detectores de calor por circuito por año; todos en 5 años | 3.1.2.4 f) | 14.4.4.5.1 a 14.4.4.5.4 | OK |
| Visibles: iluminación intermitente | 3.1.2.4 h) | 22(c) | OK |
| Funciones de control de emergencia | 3.1.2.4 i) | T.14.4.3.2, 24 | OK la tarea · la cita está en A3-M5 |
| Reemplazo de baterías | 3.1.2.4 j) | 9(a)(1), (b)(1) y (c)(1) | OK |
| Primaria con carga máxima | 3.1.2.4 k) | 2(e) | OK |
| Rellamada del silenciamiento; interruptores de aislamiento | 3.1.2.4 l) | 3(a) y 3(b) | OK |
| Señales fuera de las instalaciones (alarma, falla, supervisión) | 3.1.2.4 m) | 3(d) | OK |
| Alarma general ≥ 5 min; voz ≥ 15 min | Protocolo fuente secundaria, paso 3 | 7 | OK |
| 24 h en reserva | Protocolo fuente secundaria, paso 2 | IRAM 6, Anual («Prueba de baterías (24 h)») | OK (IRAM) |
| Sensibilidad: 1.º año, luego cada 2 años, extensible a 5; registro de falsas alarmas | 3.1.4 a) | 14.4.4.3.1 a 14.4.4.3.3.1 | OK |
| Sin aerosol no medido | 3.1.4 a) | 14.4.4.3.6 | OK |
| Fuera de rango: limpiar, recalibrar o reemplazar | 3.1.4 b) | 14.4.4.3.4 y 14.4.4.3.5 | OK |
| 15 años; 2 de cada 100; repetir cada 5 años | 3.1.4 c) | 17(d)(3) | OK |
| 100 % de lo afectado; 10 % hasta 50 | 3.1.7 | 14.4.2.4 | OK |
| Dispositivo agregado: probarlo | 3.1.7 | 14.4.2.1 | OK |
| Registro: 5 años + 1 (rotativos) | 3.1.8 | 14.6.2.2 | OK |
| Constancia de funcionamiento simulado | 3.1.2 | 14.6.4 | OK |
| Rearme lo antes posible | 3.1.3 | 14.5.4 | OK |
| Mantenimiento según el fabricante y el ambiente | 3.1.3 | 14.5.1 a 14.5.3 | OK |
| Inspección mensual: plomo-ácido y pila seca | 3.1.1.3 | T.14.3.1, 9(a) y (c) | OK. El ítem a) se aplica a todas las baterías: es más exigente |
| Inspecciones trimestrales 17(g), (k) y (l) | 3.1.1.4 | T.14.3.1 | OK |
| Inspecciones semestrales 9(b)/(d), 11, 14, 5, 17(c)/(d), 20 y 22(b) | 3.1.1.5 | T.14.3.1 | OK |
| Inspecciones anuales 1, 12/13, 4, 16 y 17(b)(2) | 3.1.1.6 | T.14.3.1 | OK |
| NFPA 101: 3,0 m y 6,1 m | 3.1.6 g) | NFPA 101, 9.6.2.10.4 | OK el valor · el alcance está en A3-m1 |

### 5.2 SBC · IRAM 3546, cap. 12 (Sistema de bombas de incendio)

| # | Requisito IRAM (cap. 12 / planilla) | Frec. | Manual | Planilla | Estado |
|---|---|---|---|---|---|
| 1 | Equipamiento y auxiliares a) a f) | — | 3.1, ítems a) a e) | SBC-1 | OK |
| 2 | Puesta fuera de servicio con procedimiento adecuado | — | 3.1 (párrafo) + 3.1.4 c) | — | OK |
| 3 | Notificación al prestador antes y después | — | 3.1 (párrafo) | — | OK |
| 4 | Sala: 4 °C / 20 °C | S | 3.1.1.1 a) | SBC-2 | OK |
| 5 | Sala: aberturas de ventilación | S | 3.1.1.1 b) | SBC-2 | OK |
| 6 | 12B: iluminación de emergencia | S | 3.1.1.1 c) | SBC-2 | OK |
| 7 | Bombeo: válvulas acordes a la maniobra (12B: totalmente abiertas) | S | 3.1.1.2 a) | SBC-2 | OK |
| 8 | Cañerías sin pérdidas | S | 3.1.1.2 b) | SBC-2 | OK |
| 9 | Presión de succión normal | S | 3.1.1.2 c) | SBC-2 | OK |
| 10 | Presión del sistema normal | S | 3.1.1.2 d) | SBC-2 | OK |
| 11 | 12B: circulación en la válvula de alivio | S | 3.1.1.2 e) | SBC-2 | OK |
| 12 | Reservorio lleno | S | 3.1.1.2 f) | SBC-2 | OK |
| 13 | Eléctrico a) a e) (luces piloto, seccionador, fases, aceite del motor vertical) | S | 3.1.1.3 a) a e) | SBC-2 | OK |
| 14 | 12B: presencia de fases, bobinado, jockey, principal y achique | S | 3.1.1.3 d), f) y g) | SBC-2 | OK |
| 15 | Diésel: tanque > 2/3; selector en automático | S | 3.1.1.4 a) y b) | SBC-2 | OK |
| 16 | Diésel: tensión (2) y corriente de carga (2) | S | 3.1.1.4 c) | SBC-2 (solo tensión) | OK texto · **FALTA** la corriente en SBC-2 (A3-m5) |
| 17 | Diésel: luces piloto de baterías | S | 3.1.1.4 c) | — | OK texto · **FALTA** fila en SBC-2 |
| 18 | Diésel: luces de alarma apagadas; horómetro | S | 3.1.1.4 d) y e) | SBC-2 | OK |
| 19 | Diésel: aceite de la caja en ángulo recto y del cárter | S | 3.1.1.4 f) | SBC-2 | OK |
| 20 | Diésel: agua de enfriamiento; electrolito; terminales; calefactor | S | 3.1.1.4 c), g) y h) | SBC-2 | OK |
| 21 | 12B: trampas de condensado; inspección general eléctrica | S | 3.1.1.4 i) y j) | SBC-2 | OK |
| 22 | Sin motobomba: tareas < mensual se hacen cada mes | — | 3.1.2 | — | OK |
| 23 | Prueba semanal por personal calificado, sin flujo | S | 3.1.2.1 | — | OK |
| 24 | Arranque automático; temporizador | S | 3.1.2.1 a) | SBC-3 | OK |
| 25 | ≥ 10 min eléctrica; ≥ 30 min diésel | S | 3.1.2.1 b) | SBC-3 | OK |
| 26 | Bomba a) a f) | S | 3.1.2.1 c) | SBC-3 | OK |
| 27 | Motor eléctrico a) a c) «(para controles de parada automática)» | S | 3.1.2.1 d) | SBC-3 | **VALOR DISTINTO** (falta la aclaración; A3-m5) |
| 28 | Motor diésel a) a e) | S | 3.1.2.1 e) | SBC-3 | OK |
| 29 | 12C: datos de placa (motobomba, electrobomba, jockey) | M | 3.1.2.1, párrafo final | — (están en SBC-1, juego único) | **FALTA** en SBC-3 (A3-C2) |
| 30 | 12C: nivel de aceite del cárter, electrolito, presión de agua de enfriamiento, vueltas/min, temperatura con precalentador y en funcionamiento | M | 3.1.2.1 f) y g) | — | OK texto · **FALTA** en SBC-3 (A3-C2) |
| 31 | 12C: después (empaquetadura, presión, calentamiento, estado, tiempo, temperatura de sala, limpieza) | M | 3.1.2.1 j) | SBC-3 | OK |
| 32 | 12C: jockey (arranque/parada, horas, limpieza) | M | 3.1.2.1 i) | SBC-3 (sin fila de arranques) | OK |
| 33 | Anual: caudal mínimo, nominal y máximo | A | 3.1.2.2 + protocolo | SBC-6 | OK |
| 34 | a) mangueras y boquillas; cuidado con los chorros | A | 3.1.2.2 a) + paso «Medición por boquillas» | SBC-6 | OK |
| 35 | b) medidor ajustado; inconsistencia → mangueras o calibrar | A | 3.1.2.2 a) y b) | SBC-6 | OK |
| 36 | Boca cerrada: alivio de circulación; alivio de presión; 0,5 h | A | 3.1.2.2 c) + paso «Caudal cero» | SBC-6 | OK |
| 37 | Cada flujo: V e I; rpm; succión, descarga y caudal simultáneos; alarmas | A | 3.1.2.2 d) | SBC-6 (sin succión/descarga al 150 %) | OK texto · **FALTA** en SBC-6 (A3-C2) |
| 38 | 12F: presión del piloto | A | Paso «Medición por boquillas» | — | OK texto · **FALTA** en SBC-6 (A3-C2) |
| 39 | Transferencia automática a potencia máxima | A | 3.1.2.2 e) | SBC-6 | OK |
| 40 | Alarmas desde los sensores | A | 3.1.2.2 f) | SBC-6 | OK |
| 41 | Generadores según su norma | A | 3.1.2.2 g) | — | OK |
| 42 | «Lo mismo… llaves de transferencia automática» | A | — | — | **FALTA** (A3-m5) |
| 43 | Ventilación, iluminación y temperatura de la sala | A | 3.1.2.2 h) | SBC-6 | OK |
| 44 | Medidas de seguridad cerca de partes eléctricas | — | 3.1.2.2, párrafo; 3.1.4 a) | — | OK |
| 45 | Resultados: interpretación por personal experimentado | — | 3.1.5 | — | OK |
| 46 | Curva de aceptación y años anteriores; no aumentar la velocidad | A | 3.1.2.2, párrafo | SBC-6 | OK |
| 47 | V·I ≤ placa × factor de servicio; −5 % / +10 % | A | Criterios a) y b) | SBC-6 | OK |
| 48 | 12D (M): activar interruptor; interruptores o fusibles | M | 3.1.3.1 a) | SBC-4 | OK |
| 49 | 12D (M): baterías (corrosión, densidad, cargador, ecualización) | M | 3.1.3.1 b) | SBC-4 | OK («carcasa» por «cárter», A3-m5) |
| 50 | 12D (T): filtros, venteo del cárter, filtros de agua, aislación del escape, terminales, rozado de cables | T | 3.1.3.2 a) a f) | SBC-4 | OK |
| 51 | 12E (S): arranque manual con energía, anticongelante, flexible del escape, seguridades y alarmas, cajas | Sem | 3.1.3.3 a) a d) | SBC-5 | OK |
| 52 | 12E (A): bomba, instrumentos (5 %), transmisión, eléctrico | A | 3.1.3.4 a) a d) | SBC-5 | OK |
| 53 | 12E (A): combustible: agua, venteo y sobreflujo, **cañería** | A | 3.1.3.4 e) | SBC-5 | **FALTA** «Cañería» (A3-m5) |
| 54 | 12E: aceite y filtros a 50 h o anual | A | 3.1.3.4 f) | SBC-5 | OK |
| 55 | 12E: anticongelante, «rod out», conductos y lumbreras | A | 3.1.3.4 g) | SBC-5 | OK |
| 56 | 12E: contrapresión, colgantes, ajuste del cableado | A | 3.1.3.4 h) e i) | SBC-5 | OK |
| 57 | 12E: interruptores o fusibles (B) | B | 3.1.3.4, nota | SBC-5 («bienal») | **FRECUENCIA DISTINTA** entre 12D (M) y 12E (B). Conviene declarar que se adopta la mensual (A3-m5) |
| 58 | 12A: datos generales, abastecimiento, toma de bomberos | — | 3.1.6 | SBC-1 | OK |
| 59 | Requisitos: autocontrol, IRAM 3619, 3 años, identificación, NA, copia | — | 3.1.1 y 3.1.6 | SBC-1 a SBC-6 | OK |
| 60 | Codificación ✓ / O / X | — | 3.1.6 | SBC-1 a SBC-6 | **VALOR DISTINTO** (A3-M1) |

**Valores NFPA citados en el SBC** (NFPA 20, ed. 2007, salvo indicación):

| Valor del manual | Ubicación | Fuente | Resultado |
|---|---|---|---|
| −5 % / +10 % de la tensión de placa | Criterio a) | IRAM cap. 12 + NFPA 20, 14.2.7.4.6 | OK |
| I por fase ≤ I de plena carga × factor de servicio | Criterio b) | 14.2.7.4.4 | OK |
| V real × I ≤ V × I de placa × factor de servicio | Criterio b) | IRAM + 14.2.7.4.5 | OK |
| 150 % de caudal a ≥ 65 % de presión | Criterio c) y paso «Caudal máximo» | 6.2.1 (centrífugas) y 7.1.2.1 (turbina vertical) | OK el valor · el alcance de la cita está en A3-m6 |
| Caudal cero ≤ 140 % | Criterio d) y paso «Caudal cero» | 7.1.2.2 (turbina vertical); 6.2.2 en español dice «40 %» | OK (errata del proyecto). El 140 % para centrífugas en el 6.2.2 original es NO VERIFICABLE con las fuentes |
| Succión ≥ 0 bar al 150 % con dispositivo | Criterio e) | 5.26.4.2 (dispositivo de prevención de contraflujo) | OK el valor · la terminología está en A3-m6 |
| Manómetros de prueba calibrados anualmente, ±1 %, etiqueta con fecha | Paso «Instrumentos» | 14.2.7.1.2 | OK (sin cita en el manual) |
| Instrumentos fijos: cambiar o recalibrar si difieren > 5 % | Paso «Instrumentos»; 3.1.3.4 b) | IRAM, planilla 12E | OK (IRAM) |
| Prueba con suministro insuficiente: al máximo disponible, superando el diseño | Paso «Caudal máximo» | 14.2.7.2.2 | OK |
| Curva dentro de la precisión del equipo, sin recalentamiento ni vibración | Criterio f) | 14.2.4.2, 14.2.5 y 14.2.6 | OK |
| Pitot en el centro del chorro, a ½ diámetro | Paso «Medición por boquillas» | NFPA 13 (ed. 2019), A.5.2.2 | OK (fuente no citada en el manual) |
| Q = 0,0666 · c · d² · √P (L/min, mm, kPa) | Paso «Medición por boquillas» | — | **NO VERIFICABLE** en las fuentes. Es dimensionalmente correcta |
| Leyes de afinidad (Q ∝ n; P ∝ n²) | Paso «Corrección por velocidad» | — | **NO VERIFICABLE** en las fuentes. Es una relación física general |
| 4 °C / 20 °C; > 2/3; 10 / 30 min; 0,5 h; 50 h | Varios | IRAM cap. 12 y planillas 12B y 12E | OK (IRAM) |

### 5.3 SAL · IRAM 3546, cap. 17 (Sistema de extinción por agentes limpios)

| # | Requisito IRAM (cap. 17 / planilla) | Frec. | Manual | Planilla | Estado |
|---|---|---|---|---|---|
| 1 | Tapas de boquillas en su lugar (17B: boquillas no dañadas) | M | 3.1.1.1 a) | SAL-2 | OK |
| 2 | Sin daños físicos | M | 3.1.1.1 b) | SAL-2 | OK |
| 3 | Espacios y riesgo sin modificar | M | 3.1.1.1 c) | SAL-2 | OK |
| 4 | Puertas con autocierre o cierre al disparo | M | 3.1.1.1 d) | SAL-2 | OK |
| 5 | Recipientes sin daños | Sem | 3.1.1.2 a) | SAL-3 | OK |
| 6 | Manómetros: presión adecuada; criterio 10 % / 5 % ajustado por temperatura | Sem | 3.1.1.2 b) + párrafo | SAL-3 | OK. Se adopta la redacción de la 17C («pérdida… mayores del 10 %»); la interpretación está declarada en *Cambios…* |
| 7 | 17C: presión y peso en la etiqueta | Sem | 3.1.1.2 c) y 3.1.3.1 c) | SAL-3 | OK |
| 8 | Inspección profunda | A | 3.1.1.3 a) | SAL-3 | OK |
| 9 | Estanqueidad; ventilador de puerta si hay dudas | A | 3.1.1.3 b) + protocolo | SAL-3 | OK |
| 10 | Prueba semestral: retirar cabezal, disparar, émbolo extendido, rearme del panel, reconectar | Sem | 3.1.2.1 a) + protocolo | SAL-3 | OK |
| 11 | 17C: prueba de funcionamiento anual sin descarga | A | 3.1.2.2 a) + protocolo | SAL-3 | OK |
| 12 | Prueba hidrostática de flexibles y cilindros | 5 años | 3.1.2.3 a) | SAL-4 | OK |
| 13 | Destruir los defectuosos | 5 años | 3.1.2.3 b) | SAL-4 | OK |
| 14 | Examen visual según la IRAM 2529-1 | 5 años | 3.1.2.3 c) | SAL-4 | OK |
| 15 | 17D: fecha de la última prueba; planilla por cilindro | 5 años | 3.1.2.3 a) + párrafo | SAL-4 | OK |
| 16 | Mantenimiento mensual (título sin tareas) | M | 3.1.3, párrafo | — | OK (forma: A3-m7) |
| 17 | Pesada; pérdida > 5 % → sustituir o rellenar | Sem | 3.1.3.1 a) + protocolo | SAL-3 | OK |
| 18 | Peso y presión en la etiqueta | Sem | 3.1.3.1 c) | SAL-3 | OK |
| 19 | 17C*: número, tara, peso cargado y carga neta | Sem | 3.1.3.1 b) | SAL-3 | OK |
| 20 | Conexiones flexibles: sustituir o probar | A | 3.1.3.2 a) | SAL-3 | OK |
| 21 | 17A: datos de agente, volumen, concentración, cilindros, detección y comandos | — | 3.1.8 | SAL-1 | OK |
| 22 | Requisitos: procedimientos documentados para pruebas hidrostáticas | — | 3.1.2.3, párrafo | — | OK |
| 23 | Requisitos: **procedimiento documentado de calidad del agente** | — | — | — | **FALTA** (A3-M6) |
| 24 | Requisitos: autocontrol | — | 3.1.1 | — | OK (le falta «dejando constancia»: A3-m7) |
| 25 | Requisitos: IRAM 3619; 3 años; identificación; NA; copia | — | 3.1.1 y 3.1.8 | SAL-1 a SAL-4 | OK |
| 26 | Codificación ✓ / O / X | — | 3.1.8 | SAL-1 a SAL-4 | **VALOR DISTINTO** (A3-M1) |

**Valores citados en el SAL:**

| Valor del manual | Ubicación | Fuente | Resultado |
|---|---|---|---|
| Pérdida de presión 10 % halogenados / 5 % inertes, ajustada por temperatura | 3.1.1.2 | IRAM cap. 17 y planilla 17C | OK |
| Pérdida de peso neto > 5 % | 3.1.3.1 | IRAM cap. 17 y planilla 17C | OK |
| 5 años (hidrostática) | 3.1.2.3 | IRAM cap. 17 y planilla 17D | OK |
| IRAM 2529-1 | 3.1.2.3 | IRAM cap. 17 | OK (contenido NO VERIFICABLE) |
| ASTM E 779, citada en la bibliografía de la IRAM | 3.1.1.3 | IRAM, Anexo bibliográfico («ASTM E 779:2003…») | OK (contenido NO VERIFICABLE) |
| Detección cruzada: primera y segunda zona | Protocolo anual | NFPA 72, T.14.4.3.2, 18(d) | OK |
| Aborto: secuencia según el tipo | Protocolo anual | 18(a) a 18(c) | OK (detalle por tipo: A3-m4) |
| Solenoide «con lámpara de prueba» | Protocolo anual | 18(f) dice solo «Verificar el funcionamiento del solenoide»; la lámpara corresponde al 18(g) | **VALOR DISTINTO** en la cita (A3-m4) |
| Supervisión por circuito abierto | 3.1.2.2 f) | 18(i) | OK |
| Personal calificado; notificación a ocupantes; aseguramiento; restitución | 3.1.2 y 3.1 | NFPA 72, 14.2.6.1, 14.2.6.2, 14.2.6.4 y 14.2.6.6 | OK |
| NFPA 2001 (concentración, retención) | 3.1.6 d) | — | **NO VERIFICABLE** (norma no disponible) |

---

## 6. Consistencia entre manual, planillas e informe (tarea 4)

| Código | Título en el cuerpo del manual | Cap. 4 del manual | Título en el xlsx o docx | Archivo | Anexo del informe | T.C. | Identificación del mantenedor | Resultado |
|---|---|---|---|---|---|---|---|---|
| SDI-1 | Información general | INFORMACIÓN GENERAL | INFORMACION GENERAL - SISTEMA CONVENCIONAL DE DOS HILOS | `…SDI-1_GENERAL_SDI` | «General SDI» | T.C. 3 AÑOS | No | Título del anexo y del archivo distintos; falta la identificación (A3-C1, A3-m8) |
| SDI-2 | Prueba mensual | PRUEBA MENSUAL | PRUEBA MENSUAL - … | `…SDI-2_PRUEBA_MENSUAL_SDI` | «Prueba Mensual SDI» | T.C. 3 años | No | Formato del T.C.; erratas; falta la identificación |
| SDI-3 | Prueba trimestral, semestral y anual | PRUEBA TRIMESTRAL, SEMESTRAL Y ANUAL | **PRUEBA** - … | `…SDI-3_PRUEBA_TRIMESTRAL_SEMESTRAL_ANUAL_SDI` | «Prueba Trimestral Semestral Anual SDI» | T.C. 3 años | No | El título del xlsx no coincide; falta la fila de ductos (A3-C1) |
| SDI-4 | Mantenimiento anual | MANTENIMIENTO ANUAL | MANTENIMIENTO ANUAL - … | `…SDI-4_ANUAL_SDI` | «Anual SDI» | T.C. 3 años | No | Anexo y archivo abreviados |
| SDI-5 | Información semanal (autocontrol) | INFORMACIÓN SEMANAL (AUTOCONTROL) | INFORMACIÓN SEMANAL (AUTOCONTROL) | `…SDI-5_INFORMACION_SEMANAL_AUTOCONTROL_SDI` | «Información semanal (autocontrol) SDI» | T.C. 3 AÑOS | Sí | OK. El orden de letras de la norma sigue sin resolverse (SDI-M2) |
| SDI-2-IN | Informe general – Sistema de Detección de Incendios | INFORME GENERAL | INFORME GENERAL – SISTEMA CONVENCIONAL DE DOS HILOS | `…SDI-2-IN_INFORME_GENERAL_DEL_SDI` | — | — | — | Cita la «IRAM 3576» (A3-M2); el código coincide con el de SDI-2 |
| SBC-1 a SBC-6 | Coinciden con 12A a 12F | Coinciden | Coinciden | Coinciden | Coinciden | T.C. 3 AÑOS | Sí | OK. Campos faltantes en SBC-3 y SBC-6 (A3-C2) |
| SBC-IN | Informe general – Sistema de Bombas Contraincendios | INFORME GENERAL | Ídem | `…SBC-IN_…` | — | — | — | OK. Encabezado «CONTRAINCENDIOS» |
| SAL-1 a SAL-4 | Coinciden con 17A a 17D | Coinciden | Coinciden | Coinciden | Coinciden | T.C. 3 AÑOS | Sí | OK |
| SAL-1-IN | Informe general – Sistema de Extinción por Agentes Limpios | INFORME GENERAL | Ídem | `…SAL-1-IN_…` | — | — | — | OK. El código coincide con el de SAL-1 (A3-m8) |

**Retención.** El apartado REGISTRO de los tres manuales dice «como mínimo durante tres años». Todas las planillas de los tres sistemas llevan «T.C. 3 AÑOS» o «T.C. 3 años», y todas dicen «Revisión 00-26». **OK**, con la salvedad del formato en SDI-2, SDI-3 y SDI-4.

**Propiedades de los documentos.** Los tres manuales tienen como título «SG-PEM-IFI-<SIGLA> …» y como autor «martin». El informe SDI-2-IN no tiene título en sus propiedades. Las planillas xlsx tampoco tienen título.

---

## 7. Elementos NO VERIFICABLES con las fuentes provistas
- IRAM 3576, citada en el informe SDI-2-IN.
- Contenido de la NFPA 2001 (agentes limpios), la NFPA 4 (prueba integrada), la NFPA 720 (CO), la NFPA 70, la NFPA 25 (inspección, prueba y mantenimiento de bombas y rociadores, a la que remite la NFPA 20, 14.4) y la NFPA 291.
- Contenido de la ASTM E 779, la IRAM 2529-1 y la IRAM 3619. Solo se verificó que se las cite.
- Coeficiente 0,0666 de la fórmula de boquillas y leyes de afinidad. Son físicamente correctos, pero no figuran en las fuentes.
- Texto original en inglés del 6.2.2 de la NFPA 20 (140 %). Se usa la errata conocida del proyecto.
