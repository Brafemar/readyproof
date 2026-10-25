# Auditoría técnica independiente: SG-PEM-IFI-SDI, SG-PEM-IFI-SBC y SG-PEM-IFI-SAL

Alcance: cotejo contra la IRAM 3546:2011 (texto del capítulo y planillas), la NFPA 72 ed. 2016 cap. 14, la NFPA 20 ed. 2007, el prompt de redacción (PROMPT_Manuales_SG-PEM-IFI v2) y los manuales originales de Martín.
Severidad: **CRÍTICO** (incumple la IRAM, introduce un riesgo para las personas o el equipo, o usa un valor sin respaldo); **MAYOR** (omisión normativa o técnica relevante, o desvío del prompt con efecto en la trazabilidad); **MENOR** (forma, redacción o coherencia).

Resultado del control de números: en los tres manuales, todos los valores numéricos tienen respaldo en la IRAM 3546 o en el texto NFPA provisto. No se encontraron números inventados. Las únicas excepciones son la posición del tubo Pitot a «medio diámetro» y el coeficiente 0,0666 de la fórmula de boquillas; son relaciones físicas o prácticas generales, pero no figuran en el texto provisto (ver SBC-m4).
Control de estilo: no hay segunda ni primera persona, coloquialismos ni marcas. Los párrafos introductorios no están numerados y no hay cursivas, subrayados ni colores.

---

## 1. SG-PEM-IFI-SDI — Sistema de Detección de Incendios

### SDI-C1 · CRÍTICO · El plazo de conservación de los registros es menor que el que exige la IRAM
- **Texto actual (REGISTRO):** «Los registros se deben conservar, como mínimo, hasta la prueba siguiente y durante un año a partir de entonces; los de detectores de temperatura restaurables probados en forma rotativa, durante cinco años y un año más, según la NFPA 72, edición 2016.»
- **Problema:** la IRAM 3546, en el capítulo REQUISITOS (*Registros de mantenimiento* y *Otra documentación de la instalación*), exige conservar la documentación **como mínimo durante tres años**. El manual adopta el plazo de la NFPA 72 (14.6.2.1), que es menos exigente, y contradice el criterio de «condición más exigente» que el propio manual declara. En una auditoría de certificación es una no conformidad directa.
- **Corrección:** «Los registros se deben conservar como mínimo durante **tres años**, según la IRAM 3546:2011. Los registros de los detectores de temperatura restaurables probados en forma rotativa se deben conservar durante el ciclo completo de **cinco años** más **un año**, según la NFPA 72, edición 2016, 14.6.2, cuando ese plazo resulte mayor.»

### SDI-M1 · MAYOR · El protocolo de dispositivos iniciadores no deshabilita las funciones de descarga ni de control
- **Texto actual:** el «Protocolo de Ensayo: prueba de dispositivos iniciadores» empieza directamente con «1) Detectores de humo… aplicar humo…». El paso 4 dice «verificar que las funciones de control deshabilitadas durante la prueba quedaron restauradas», pero ningún paso anterior las deshabilita.
- **Problema:** probar los detectores con humo real activa las salidas de la central: disparo de sistemas de extinción, cierre de compuertas, corte de HVAC, liberación de puertas y llamada de ascensores. La NFPA 72, 14.2.6.4, exige asegurar los sistemas de supresión contra la activación inadvertida durante la prueba, desconectando solenoides o actuadores o cerrando válvulas. El ítem c) de SEGURIDAD lo menciona, pero no se traslada al protocolo, que es lo que se ejecuta en campo.
- **Corrección:** agregar como paso 1 «**1) Aislamiento de salidas.** Paso a paso: identificar en la secuencia de operación las funciones de control y los sistemas de extinción comandados por la central; desconectar los solenoides o actuadores de descarga, o aislar las salidas según el fabricante, y coordinar con el responsable las funciones de control que se van a deshabilitar. Justificación técnica: evita descargas accidentales y la interrupción de equipos críticos (NFPA 72, 14.2.6.4). Criterio de aceptación: todas las salidas críticas aisladas y registradas antes del primer accionamiento.» Renumerar los pasos siguientes.

### SDI-M2 · MAYOR · La planilla 6B no respeta el orden de letras y su nombre está alterado
- **Texto actual:** «SG-PEM-IFI-SDI-5 Sistema de Detección de Incendios – Inspección semanal (autocontrol)».
- **Problema:** el prompt (4.3) exige seguir el orden de letras de la norma, lo que da 6B → SDI-2, 6C → SDI-3, 6D → SDI-4 y 6E → SDI-5. También exige copiar el nombre literal sin corregirlo, y el nombre de la norma es «**Información** semanal (autocontrol)». La razón de usar el número 5 (no renumerar las planillas en uso) está en *Cambios_manuales_Martin.md*, pero no en un *Dudas* aprobado.
- **Corrección:** renumerar las planillas según el orden de letras, o dejar aprobada por escrito la excepción en el cotejo del SDI. Usar el nombre literal «Información semanal (autocontrol)» en el cuerpo y «INFORMACIÓN SEMANAL (AUTOCONTROL)» en el capítulo 4. Revisar además el informe «SDI-2-IN», cuyo número coincide con el de una planilla.

### SDI-M3 · MAYOR · Faltan en el cuerpo campos de la planilla 6B
- **Texto actual (Inspección semanal):** ítems a) a g) sin estos campos.
- **Campos de la 6B que no figuran en el texto:**
  - detectores de **barreras infrarrojas** y **sistema aspirador**;
  - alimentación **secundaria**: el ítem d) cita solo la primaria;
  - «Están todos los componentes incrustados»;
  - CABLEADO: «Zona con falla» y «Zonas conectadas»;
  - ALARMAS Y ANUNCIACIÓN: «Detección de nivel del tanque de agua», «Indicación detectores de flujo», «Indicación de baja presión en red de cañerías» e «Indicación arranque de bomba»;
  - «Verificar planillas de eventos ocurridos durante la semana».

  El prompt (4.1) obliga a incorporar al bloque de su frecuencia todo campo de planilla que no figure en el texto.
- **Corrección:** agregar los ítems h) a l) siguientes.
  - h) «**Fuentes de energía:** verificar que el sistema se halla alimentado con tensión primaria y secundaria.»
  - i) «**Cableado:** registrar las zonas con falla y las zonas conectadas.»
  - j) «**Señales de otros sistemas:** verificar la indicación de nivel del tanque de agua, de los detectores de flujo, de baja presión en la red de cañerías y de arranque de bomba.»
  - k) «**Componentes:** verificar que todos los componentes se encuentran incrustados y ensamblados en alineación.»
  - l) «**Registro de eventos:** verificar las planillas de eventos ocurridos durante la semana.»

  Agregar además «barreras infrarrojas y sistemas aspiradores» al ítem a).

### SDI-M4 · MAYOR · Falta el valor «(%8,3)» de la planilla 6E
- **Norma:** la planilla 6E dice «Calibración de detectores de humo y temperatura (%8,3)» y «Calibración de detectores de gas (%8,3)».
- **Problema:** el valor no se transcribe ni se declara en *Dudas*. Probablemente indica una proporción de calibración (8,3 % ≈ 1/12), pero el manual no puede omitirlo.
- **Corrección:** en Mantenimiento anual, ítems c) y d), agregar «(**8,3 %**, según la planilla IRAM 3546-6E)» y declarar en *Dudas* que la norma no define el alcance del porcentaje (por ejemplo, la proporción de detectores que se calibra por intervención).

### SDI-M5 · MAYOR · Faltan inspecciones de la NFPA 72 con frecuencia trimestral y semestral
- **Problema:** el manual adopta la NFPA 72 para las tareas que la IRAM no prevé, pero no tiene «Inspección trimestral». La Tabla 14.3.1 fija frecuencia **trimestral** para:
  - 17(g) detectores de energía radiante (llama): campo visual sin obstrucciones;
  - 17(k) dispositivos de señales de supervisión;
  - 17(l) sensores de flujo de agua.

  En la semestral faltan:
  - 17(c) dispositivos electromecánicos de descarga;
  - 17(d) interruptores de los sistemas de extinción;
  - 20 interfaz de las funciones de control de emergencia;
  - 22(b) aparatos textuales audibles.

  En la anual faltan:
  - 4 transmisores DACT y otros;
  - 16 conexiones de fibra óptica;
  - 17(b)(2) tubo de muestreo de los detectores en ducto.
- **Corrección:** crear el subtítulo «Inspección trimestral» con los ítems 17(g), (k) y (l), que se registra en la SDI-3 (Prueba trimestral, semestral y anual) como tarea complementaria. Completar las listas semestral y anual con los ítems indicados.

### SDI-M6 · MAYOR · Faltan pruebas de la NFPA 72 (Tabla 14.4.3.2)
- **Omisiones con efecto técnico:**
  - 9(a)(1), 9(b)(1) y 9(c)(1): **reemplazo anual de baterías** según el fabricante, o cuando la tensión o la corriente de la batería recargada caigan por debajo de lo especificado;
  - 2(e): prueba de la alimentación primaria **con carga máxima**, con todos los aparatos de alarma que funcionan en simultáneo; la prueba mensual c) solo dice «comprobar el suministro»;
  - 3(a) y 3(b): función de rellamada de la señal de falla e interruptores de desconexión o aislamiento;
  - 17(f): detectores de llama, con prueba **semestral** y determinación de sensibilidad con método o instrumento calibrado;
  - 17(g)(4), (5) y (6): muestreo de aire probado desde el extremo de cada tramo, detector de ducto con tubo de muestreo y detector de haz proyectado con filtro óptico o humo;
  - 9(a)(5): no usar hidrómetros de solo «aprobado / reprobado».
- **Corrección:**
  - incorporar en Prueba anual los ítems k) «**Baterías:** reemplazo según el fabricante o cuando la batería recargada no alcance la tensión o corriente especificada» y l) «**Alimentación primaria:** prueba con carga máxima, con todos los aparatos de notificación en funcionamiento simultáneo»;
  - incorporar en Prueba semestral el ítem h) «**Detectores de llama:** prueba de funcionamiento y de sensibilidad con método o instrumento calibrado; no usar fuentes de luz que apliquen radiación no medida»;
  - agregar los métodos de muestreo de aire, ducto y haz al protocolo de iniciadores.

### SDI-m1 · MENOR · La tensión de flotación del níquel-cadmio está mal definida
- **Texto actual:** «con el cargador desconectado y bajo carga, verificar … que las de níquel-cadmio mantienen una tensión de flotación nominal de 1,42 V por celda».
- **Problema:** la tensión de flotación se mide con el cargador conectado. La Tabla 14.4.3.2 9(b)(4) dice «Durante la carga, verificar que el voltaje de flotación … sea de 1.42 voltios por celda, nominal. Si fuera posible, medir las celdas individualmente.» Además, el criterio de 2,05 V corresponde al plomo-ácido abierto (9(a)(4)); para el plomo-ácido sellado el criterio es el del fabricante (9(c)(4)).
- **Corrección:** separar los criterios.
  - Plomo-ácido abierto: no menos de **2,05 V** por celda bajo carga.
  - Plomo-ácido sellado: según el fabricante.
  - Níquel-cadmio: tensión de flotación de **1,42 V** por celda nominal, medida durante la carga y, si es posible, celda por celda.

### SDI-m2 · MENOR · La prueba de 24 h no prevé la recarga posterior
- **Texto actual (protocolo de fuente secundaria, paso 4):** «reconectar la alimentación primaria, restablecer la central y notificar la conclusión de la prueba».
- **Problema:** después de 24 h en reserva más la alarma, las baterías quedan descargadas y el sistema queda con autonomía reducida hasta que se recargan.
- **Corrección:** agregar al paso 4: «registrar la tensión de reposo y verificar, en una visita posterior o con la tensión de carga, la recarga completa en el tiempo indicado por el fabricante; durante ese período se debe informar al responsable de la instalación que la autonomía está reducida.»

### SDI-m3 · MENOR · El intervalo de 18 meses omite la condición de la NFPA 72
- **Texto actual:** «…pueden inspeccionarse durante las paradas programadas, con intervalos que no excedan los 18 meses.»
- **Corrección:** agregar «, si lo aprueba la autoridad competente (NFPA 72, 14.3.2 y 14.4.4.1)».

### SDI-m4 · MENOR · Falta la prueba de reaceptación después de cambios
- **Texto actual (CONTROL DE CAMBIOS):** «Toda modificación del sistema o de su programación se debe evaluar técnicamente y documentar…».
- **Corrección:** agregar «Después de cambios en el software del sitio se deben probar el **100 %** de las funciones afectadas y el **10 %** de los dispositivos iniciadores no afectados, hasta un máximo de **50** (NFPA 72, 14.4.2.4). Todo dispositivo agregado se debe probar (14.4.2.1).»

### SDI-m5 · MENOR · Otros puntos de forma
- Nombre de la 6D: el literal es «Prueba trimestral, **semestral y** anual», y el manual dice «Prueba trimestral semestral anual».
- El aviso previo no usa la versión canónica del prompt (6.4). La versión del manual es más exigente y sirve, pero debe incluir la frase canónica.
- «CONTROL DE CAMBIOS Y RESPONSABILIDADES» va en una sola sección; el prompt prevé dos secciones con frase de finalidad e ítems cada una.
- Inspección mensual, ítem a): la frecuencia mensual de la Tabla 14.3.1 vale solo para el plomo-ácido abierto y la pila seca, y el ítem lo aplica a todas las baterías. Es más exigente, pero repite el ítem a) de la semestral; conviene acotarlo.
- El protocolo de iniciadores está bajo «Prueba mensual» y puede leerse como prueba con humo de todos los detectores cada mes. Conviene aclarar que la prueba de todos los detectores es anual (ítem e de la Prueba anual) y que la mensual sigue la recomendación del fabricante.
- Se perdió el párrafo de Martín «Estos registros permiten: trazabilidad, verificación del estado operativo, auditorías, identificación de tendencias de fallas». Conviene reponerlo en REGISTRO.
- El nombre del sistema difiere entre la portada y el título 3.1 («…CONVENCIONAL DE DOS HILOS») y el encabezado y las propiedades («Sistema de Detección de Incendios»). Unificarlo o declararlo.

---

## 2. SG-PEM-IFI-SBC — Sistema de Bombas Contraincendios

### SBC-C1 · CRÍTICO · No hay bloqueo del arranque automático durante el mantenimiento
- **Texto actual (SEGURIDAD b):** «Partes rotantes: protecciones de acoples y ejes colocadas durante la marcha y prohibición de intervenir con el equipo en funcionamiento.»
- **Problema:** el mantenimiento anual incluye «lubricación del acople», «control del juego en el extremo del eje y del alineamiento», «ajuste de conexiones» y «disparo del interruptor». Esas tareas se hacen con el equipo detenido pero en **automático**, y la bomba puede arrancar sola si la presión de la red cae. Prohibir intervenir con el equipo «en funcionamiento» no cubre un arranque imprevisto. Es un riesgo de atrapamiento y de choque eléctrico.
- **Corrección:** agregar el ítem e) «**Bloqueo de arranque:** antes de intervenir partes rotantes o eléctricas, se debe pasar el controlador a posición apagado, abrir, bloquear y etiquetar el seccionador; en motores diésel, colocar el selector en apagado y desconectar los dos bancos de baterías. La intervención se trata como puesta fuera de servicio, con aviso al responsable y al servicio de supervisión. Al finalizar se retiran los bloqueos y se verifica el selector en automático.»

### SBC-M1 · MAYOR · El criterio de corriente es incompleto y no coincide con lo informado
- **Texto actual:** «b) Corriente: producto de la tensión y la corriente de cada fase no mayor que el producto de los valores nominales de placa por el factor de servicio.»
- **Problema:** es el criterio de la IRAM y de la NFPA 20, 14.2.7.4.5, que se aplica con **tensión variable**. La NFPA 20, 14.2.7.4.4, fija para tensión y frecuencia nominales que «la demanda de amperios en cada fase no deberá superar … la carga total multiplicado por el factor de servicio». Ese límite es más exigente cuando la tensión está por debajo de la nominal. *Cambios_manuales_Martin.md* dice que este criterio se agregó, pero no figura en el manual.
- **Corrección:** «b) **Corriente:** la corriente de cada fase no debe superar la corriente de plena carga de placa multiplicada por el factor de servicio (NFPA 20, 14.2.7.4.4). Con tensión distinta de la nominal, el producto de la tensión real por la corriente de cada fase no debe superar el producto de los valores de placa por el factor de servicio (IRAM 3546:2011; NFPA 20, 14.2.7.4.5).»

### SBC-M2 · MAYOR · La prueba a caudal cero se hace con la válvula de descarga principal cerrada
- **Texto actual (protocolo anual, paso 3):** «con la válvula de descarga principal cerrada, arrancar la bomba y registrar la presión máxima…» durante 0,5 h.
- **Problema:** cerrar la válvula de descarga principal aísla la red. La protección del edificio queda fuera de servicio durante toda la prueba, y además durante 0,5 h. La condición sin flujo se obtiene con las válvulas de prueba y de los cabezales de prueba cerradas, sin consumo en la red. No hace falta aislar el sistema; la NFPA 20, 14.2.7.3.2, lo exige solo para el control de velocidad variable.
- **Corrección:** «Paso a paso: con las válvulas del cabezal de prueba y de drenaje cerradas, sin consumo en la red y con la válvula de descarga al sistema abierta, arrancar la bomba, registrar la presión de succión y de descarga y verificar la descarga de la válvula de alivio de circulación durante **0,5 h**. Si por razones operativas se debe aislar la red, se aplica el procedimiento de puesta fuera de servicio y se informa al responsable.»

### SBC-M3 · MAYOR · Falta un criterio de presión de succión en la prueba de caudal
- **Texto actual:** el paso 1 cita la cavitación, pero ningún paso fija un control de la presión de succión durante el flujo al 150 %.
- **Problema:** sin ese control, la prueba puede provocar presión negativa en la succión, con cavitación, y en un abastecimiento desde red pública, depresión en la red.
- **Corrección:** en los pasos 4 y 5, agregar «registrar la presión de succión en cada punto. Con dispositivo antirretorno, la presión de succión no debe ser menor que **0 bar** en el manómetro al **150 %** de la capacidad nominal (NFPA 20, 5.26.4.2). En los demás casos no debe ser menor que la mínima admitida por el diseño o por el prestador del abastecimiento. Ante fluctuaciones de lectura o ruido de cavitación, se interrumpe el aumento de caudal.»

### SBC-M4 · MAYOR · La prueba semanal se registra en la planilla mensual sin declararlo
- **Texto actual:** «Prueba semanal de funcionamiento … Los resultados deben registrarse en la planilla SG-PEM-IFI-SBC-3 … – Inspección mensual.»
- **Problema:** el texto de la IRAM fija la prueba como semanal y la planilla 12C se llama «Inspección mensual». El prompt (4.1) exige incluir la tarea en las dos frecuencias y declararlo en *Dudas*. Con motobomba, la prueba se hace cada semana y una planilla mensual no permite registrar las cuatro o cinco marchas del mes.
- **Corrección:** agregar después del cierre: «La planilla IRAM 3546-12C es de frecuencia mensual. En sistemas con motobomba, cada prueba semanal se registra en una planilla SBC-3 propia, o en una columna por semana; en sistemas sin motobomba, la prueba se hace y se registra cada mes.» Declarar el criterio en *Dudas*.

### SBC-M5 · MAYOR · Faltan en el cuerpo campos de la planilla 12C
- **Campos que no figuran en el texto:**
  - «Último cambio de aceite y filtro», «Último cambio de combustible» y «Próximo cambio de combustible»;
  - «Presión de agua de enfriamiento (MPa)»;
  - «Presión de aceite de motor», como valor que se registra;
  - «Tem. agua enfri. precalentado / en funcionamiento»;
  - «Nivel de aceite del cárter» y «Nivel de electrolito de baterías» antes de la puesta en marcha;
  - los datos de placa de la motobomba, la electrobomba y la bomba jockey (caudal nominal, altura manométrica, vueltas/min, presión máxima y potencia).
- **Corrección:** agregar al bloque de la prueba semanal estos ítems.
  - «**Motor diésel, antes de la marcha:** registrar el nivel de aceite del cárter, el nivel de electrolito, la temperatura del agua de enfriamiento con el precalentador y las fechas del último cambio de aceite y filtro, del último cambio de combustible y del próximo.»
  - «**Motor diésel, durante la marcha:** registrar la presión de agua de enfriamiento, la presión de aceite, la temperatura del agua en funcionamiento y las vueltas/min.»
  - Los datos de placa se registran en la planilla SBC-3.

### SBC-M6 · MAYOR · Se perdió contenido técnico del original de Martín que tiene valor y no necesita números
Contenido de Martín que se puede reponer sin valores inventados:
1. **Bomba jockey:** registrar la cantidad de arranques en el panel; un exceso respecto del registro anterior indica fugas en la red.
2. **Termografía bajo carga:** escaneo de bornes del contactor y guardamotor, cables de alimentación, rodamientos y carcasa del motor durante el punto de 150 %.
3. **Equilibrio de fases:** registrar la corriente de cada fase con pinza amperométrica y comparar cada una con el promedio y con el registro anterior.
4. **Manovacuómetro:** purgar la toma antes de leer; una presión de succión anormalmente baja indica un filtro de succión obstruido.
5. **Pérdidas de carga:** comparar la presión en la bomba con la del hidrante más desfavorable.
6. **Boquillas:** usar boquillas de diámetro conocido en los hidrantes más alejados; no descargar sin boquilla, porque la lectura resulta falsa.
7. **Caudalímetro:** las fluctuaciones rápidas de lectura indican entrada de aire en la succión.

- **Corrección:** agregar al protocolo anual el paso «**Termografía y equilibrio de fases** · Paso a paso: al **150 %** del caudal nominal, registrar con cámara termográfica la temperatura de los bornes del tablero, de los cables y de los rodamientos, y con pinza amperométrica la corriente de cada fase. Criterio de aceptación: sin puntos calientes respecto de componentes similares ni respecto del registro anterior; desbalance de corriente comparable con el registro anterior y dentro de lo que indica el fabricante del motor.» Incorporar los puntos 1, 4, 5, 6 y 7 como rótulos *Qué se determina con la lectura*.

### SBC-m1 · MENOR · La cita de la presión a caudal cero es incorrecta
- **Texto actual:** «Se consideran aceptables, según la IRAM 3546:2011 y la NFPA 20 …: c) 150 % / 65 %; d) 140 %».
- **Problema:** la IRAM no fija los valores c) y d). El 140 % se respalda en la NFPA 20, 7.1.2.2, porque el 6.2.2 en español dice «40 %».
- **Corrección:** citar por separado.
  - a) y b): IRAM 3546:2011 y NFPA 20, 14.2.7.4.
  - c): NFPA 20, 6.2.1 y 7.1.2.1.
  - d): NFPA 20, 7.1.2.2, con la nota de que el 6.2.2 en español contiene un error de traducción, declarada en *Dudas*.

  Aclarar también que el criterio principal de una prueba periódica es la comparación con la curva de aceptación en campo y con los ensayos anteriores (IRAM; NFPA 20, 14.2.4.2).

### SBC-m2 · MENOR · La nota de la frecuencia «B» no es coherente
- **Texto actual:** «La verificación de interruptores o fusibles … figura en la planilla de la norma con la frecuencia «B», que se interpreta como bienal.»
- **Problema:** la planilla 12D ya asigna «Interruptores o fusibles (M)» al sistema eléctrico del motor diésel. La condición más exigente es la mensual, que ya está en Mantenimiento mensual a).
- **Corrección:** «La planilla IRAM 3546-12D asigna frecuencia mensual a la verificación de interruptores o fusibles del motor diésel, y la 12E les asigna la frecuencia «B». Se adopta la verificación mensual; la «B» se interpreta como el cambio bienal, a confirmar.»

### SBC-m3 · MENOR · Omisiones del texto de la IRAM
- Procedimiento para el motor eléctrico, ítem c): falta la aclaración «(para controles de parada automática)».
- Pruebas anuales: falta «Lo mismo se aplica para las llaves de transferencia automática», es decir, que se ensayan según su norma.
- Planilla 12E: falta el ítem «Cañería» del sistema de combustible.
- La planilla 12D dice «cárter» de las baterías; el manual lo cambia por «carcasa» y no lo declara.

### SBC-m4 · MENOR · Valores de medición sin fuente declarada
- La fórmula Q = 0,0666 · c · d² · √P y la posición del Pitot a «medio diámetro» no figuran en el texto NFPA 20 provisto. Son correctas físicamente: verificación con boquilla de 28,6 mm a 345 kPa, 1 012 L/min ≈ 267 gpm.
- **Corrección:** declararlas en *Valores y contenidos agregados* como relación física general y práctica de medición con Pitot, citando la NFPA 291 o la NFPA 25 si se dispone de ellas.

### SBC-m5 · MENOR · Faltan párrafos tipo y hay inconsistencias de nombre y estructura
- PRUEBA no tiene la regla de fallas del prompt (6.4). MANTENIMIENTO no dice cuándo se realiza.
- La portada y el 3.1 dicen «SISTEMA DE BOMBAS CONTRA INCENDIO», y el encabezado, las propiedades y los anexos dicen «Sistema de Bombas Contraincendios». Unificar.
- La regla «sin motobombas, las tareas de frecuencia menor a mensual se hacen mensualmente» está solo en PRUEBA, pero también afecta a las inspecciones semanales de 3.1.1. Repetirla allí y declarar cómo convive con la regla de autocontrol.
- Las tres primeras inspecciones semanales no cierran con planilla; solo cierra la del motor diésel. Agregar el cierre o una frase que indique que las cuatro se registran en la SBC-2.
- La puesta fuera de servicio se resuelve en un párrafo. Conviene detallarla: aviso, identificación del equipo fuera de servicio, medidas compensatorias y restitución con prueba de arranque.
- Falta la conservación de registros por **tres años** (IRAM, REQUISITOS).
- Falta, según la NFPA 20, 14.5, repetir la prueba de campo cuando se reemplazan componentes críticos.

---

## 3. SG-PEM-IFI-SAL — Sistema de Extinción por Agentes Limpios

### SAL-C1 · CRÍTICO · La pesada de cilindros no tiene medidas de seguridad
- **Texto actual (Mantenimiento semestral a):** «Pesada de los recipientes: control de la cantidad de agente por pesada del recipiente, registrando el peso en kg.»
- **Problema:** para pesar un cilindro hay que desconectarlo y moverlo. Si el cabezal de control o el actuador manual siguen montados, o si la válvula queda sin protección, un disparo o un golpe puede descargar el agente: el cilindro se convierte en proyectil y se forma una atmósfera con agente en la sala de cilindros. El manual no indica retirar el cabezal antes de la pesada ni tiene protocolo. El prompt (6.3) exige un Protocolo de Ensayo para el pesaje.
- **Corrección:** agregar después del cierre «Protocolo de Ensayo: pesada de recipientes».
  - 1) **Aseguramiento.** Retirar el cabezal de control y el actuador manual y desconectar la conexión flexible de descarga; colocar la tapa de protección y el dispositivo antirretroceso de la válvula según el fabricante.
  - 2) **Pesada.** Usar una balanza calibrada; registrar el número de cilindro, la tara, el peso cargado y la carga neta.
  - 3) **Criterio.** Si la pérdida de peso neto es mayor que el **5 %**, se debe rellenar o sustituir el recipiente.
  - 4) **Reconexión.** Reconectar la conexión flexible, verificar el émbolo retraído y reponer el cabezal en último lugar.

  En el ítem a), aclarar que la pesada aplica a los agentes halogenados (planilla 17C, «Peso del recipiente con halogenados») y que en los gases inertes la carga se controla por presión.

### SAL-M1 · MAYOR · Falta la regla de autocontrol
- **Problema:** el prompt (4.2) exige transcribir siempre la regla de autocontrol, la identificación del mantenedor, la leyenda NA y la copia al usuario. La sección 3.1.1 del SAL no tiene la regla de autocontrol, que sí está en el SDI y en el SBC.
- **Corrección:** agregar en 3.1.1: «Las inspecciones de frecuencia menor a un mes pueden ser completadas por el usuario de la instalación como inspecciones de autocontrol, y se deben identificar como tales; el mantenedor debe verificar su correcto cumplimiento, dejando constancia de los hallazgos. En el presente sistema la IRAM 3546:2011 no establece inspecciones de esa frecuencia.»

### SAL-M2 · MAYOR · La reconexión de cabezales no comprueba la ausencia de tensión de disparo
- **Texto actual (protocolo de cabezales, paso 4):** «rearmar los cabezales según el fabricante, verificar que el émbolo está retraído y reconectarlos a los recipientes.»
- **Problema:** si el circuito de disparo sigue energizado (salida enclavada, retardo en curso o una segunda zona en alarma), reponer un actuador eléctrico produce la descarga aunque el panel parezca normalizado. El paso 3 solo pide el rearme del panel.
- **Corrección:** agregar al paso 4, antes de reconectar: «medir con voltímetro, en los bornes del circuito de disparo, la ausencia de tensión; verificar que no haya alarmas, prealarmas ni retardos activos y que todos los dispositivos de iniciación estén restablecidos. Reconectar los cabezales de a uno, empezando por el piloto si lo hay.» Agregar al criterio de aceptación «circuito de disparo sin tensión antes de cada reconexión».

### SAL-M3 · MAYOR · Faltan protocolos para la estanqueidad, la prueba anual de secuencia y la prueba hidrostática
- **Problema:** el prompt (6.3) exige un protocolo para estanqueidad, pesaje y descargas simuladas. Hoy:
  - la prueba de estanqueidad (Inspección anual b) solo remite a la ASTM E 779;
  - la prueba anual de secuencia (sin descarga) no tiene pasos;
  - la prueba hidrostática quinquenal no tiene pasos.
- **Corrección:**
  - (a) Agregar el «Protocolo de Ensayo: prueba de funcionamiento del sistema», con estos pasos: aseguramiento según el protocolo semestral; actuación de la primera zona y verificación de la prealarma; actuación de la segunda zona y verificación de la alarma de descarga; medición del retardo, con criterio «según el diseño registrado»; verificación del cierre de compuertas y puertas y del corte de ventilación; interruptor de aborto, según su tipo; disparo manual; circuito de disparo con lámpara de prueba o carga simulada según el fabricante (NFPA 72, Tabla 14.4.3.2, 18(f) y 18(g)); supervisión por circuito abierto (18(i)).
  - (b) Agregar el «Protocolo de Ensayo: estanqueidad del recinto», con la prueba con ventilador de puerta según la ASTM E 779 y el criterio de aceptación «nivel de fugas compatible con el tiempo de retención de diseño, según la memoria de cálculo del sistema».
  - (c) En la prueba quinquenal, indicar que el vaciado y la recuperación del agente los hace personal competente, con recuperación del agente y no por venteo, y que las presiones de prueba son las de la IRAM 2529-1 y las del fabricante de las conexiones flexibles.

### SAL-M4 · MAYOR · El subsistema de detección y disparo no tiene inspección, prueba ni mantenimiento propios
- **Problema:** el manual declara la NFPA 72 como criterio complementario para la detección y el disparo, pero no incluye:
  - la prueba funcional de los detectores del recinto (Tabla 14.4.3.2, 17(g)(1), anual);
  - las pruebas de las baterías del panel de disparo (ítems 7 y 9);
  - la inspección de dispositivos electromecánicos de descarga e interruptores (Tabla 14.3.1, 17(c) y 17(d), semestral);
  - las funciones de la central (ítem 2).

  Un panel de disparo con baterías degradadas no dispara ante un corte de energía.
- **Corrección:** agregar en PRUEBA el párrafo «La central de detección y disparo, sus fuentes de energía, sus dispositivos iniciadores y sus aparatos de notificación se inspeccionan, prueban y mantienen según el procedimiento SG-PEM-IFI-SDI, con la condición de que toda prueba de detectores se hace con el sistema de extinción asegurado según el protocolo de cabezales.» Incorporar la prueba anual de los detectores del recinto en la lista de la Prueba anual.

### SAL-m1 · MENOR · La interpretación del 10 % y el 5 % no está declarada
- **Texto actual:** «Si la pérdida de presión es mayor que el 10 % … o que el 5 % …».
- **Problema:** el texto de la IRAM dice «Si la lectura es menor que el 10 %… de la indicada», lo que leído en forma literal no tiene sentido técnico. El manual toma correctamente el criterio de la planilla 17C («pérdida de presión mayores del 10 %»), pero no lo declara.
- **Corrección:** declarar en *Dudas* que se adopta la redacción de la planilla 17C.

### SAL-m2 · MENOR · Estructura respecto del prompt
- La prueba quinquenal va en PRUEBA, pero el prompt la ubica en la sección complementaria «Ensayos de largo plazo». Moverla o declararlo.
- «Mantenimiento mensual»: la norma tiene el título sin tareas. El prompt pide escribir el subtítulo seguido del párrafo «La IRAM 3546:2011 no establece tareas de mantenimiento mensual para este sistema», en lugar de incluirlo en la definición.
- El PROCEDIMIENTO POSTERIOR A UNA DESCARGA cierra con la planilla SAL-3, pero sus tareas no figuran en ninguna planilla de la norma. Según el prompt, una práctica del rubro sin planilla no lleva cierre. Quitar el cierre o declarar las tareas como complementarias.
- «CONTROL DE CAMBIOS Y RESPONSABILIDADES» va en una sola sección. En el original de Martín eran dos secciones.

### SAL-m3 · MENOR · Seguridad y salud ocupacional
- Se perdió el párrafo de Martín «Los agentes limpios están diseñados para su uso en recintos ocupados; sin embargo, durante su descarga pueden alcanzarse concentraciones que no resultan adecuadas para la permanencia prolongada de personas». Reponerlo como frase de finalidad.
- Agregar: «Después de una descarga sobre un fuego, los agentes halogenados generan productos de descomposición tóxicos y corrosivos. El reingreso se hace con ventilación forzada y con protección respiratoria cuando no se pueda verificar la atmósfera.»
- Agregar también que en la sala de cilindros los recipientes deben estar sujetos y que ningún cilindro se mueve con el cabezal montado (ver SAL-C1).

### SAL-m4 · MENOR · Faltan pruebas de equipos de riesgos especiales
- No figuran los ítems de la NFPA 72, Tabla 14.4.3.2:
  - 18(a), (b) y (c): los tres tipos de interruptor de aborto, cada uno con su criterio;
  - 18(g): circuito de disparo por dispositivo explosivo, con lámpara AGI;
  - 18(h): circuito de zona verificado, secuencial o de conteo, con sensores accionados en un mínimo de **cuatro** lugares.
- **Corrección:** agregarlos a la Prueba anual, con la aclaración «cuando existan».
- También falta la conservación de registros por **tres años** (IRAM, REQUISITOS).

---

## 4. Observaciones comunes a los tres manuales
1. **Retención de registros:** fijar en los tres manuales el mínimo de **tres años** de la IRAM 3546, capítulo REQUISITOS (ver SDI-C1).
2. **Protocolos y seguridad:** todo protocolo que manipula cilindros, actuadores, partes rotantes o tableros debe tener un primer paso de aseguramiento o bloqueo y un último paso de restitución con verificación (ver SBC-C1, SAL-C1, SAL-M2 y SDI-M1).
3. **Cotejo:** los tres manuales necesitan su *cotejo.md* (Norma | Manual, Valores agregados, Dudas). Hoy las decisiones están solo en *Cambios_manuales_Martin.md*, y faltan las de SDI-M2, SDI-M4, SBC-M4, SBC-m1, SBC-m2 y SAL-m1.
