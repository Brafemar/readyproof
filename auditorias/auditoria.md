# Auditoría técnica independiente: manuales SG-PEM-IFI (SAP, SRE, SGE, SEP, SSA)

**Referencia:** IRAM 3546:2011, capítulos 8, 9, 10, 15 y 16 (texto y planillas), capítulo REQUISITOS («Mantenimiento de las Instalaciones», «Evaluación previa», «Empleo de las planillas») y PROMPT_Manuales_SG-PEM-IFI v2.
**Fecha:** 2026-10-23
**Método:** lectura completa de cada .docx (pandoc y render con LibreOffice para verificar la numeración real) y cotejo, ítem por ítem, con 3546.md. Para los campos de planilla se usó también 3546_lin.txt, y el texto se tomó siempre de 3546.md.

**Escala:**
- **CRÍTICO:** riesgo para las personas, o valor o requisito inventado o contrario a la norma.
- **MAYOR:** omisión de un requisito o campo de la norma, requisito debilitado o cambiado, sección obligatoria del spec ausente, o protocolo técnicamente defectuoso.
- **MENOR:** redacción, trazabilidad o forma.

## Verificaciones sin hallazgos (las cinco series)

- **Numeración real** (render LibreOffice): 3.1 / 3.1.1 / 3.1.1.n correcta en los cinco manuales, y REGISTRO siempre último.
- **Planillas:** el mapeo IRAM 3546-<cap>A… → SG-PEM-IFI-<SIGLA>-1… sigue el orden de las letras en los cinco manuales. Los nombres son literales y coinciden entre el cuerpo y el capítulo 4.
- **Cierres:** cada frecuencia cierra con una planilla.
- **Valores numéricos:** no se detectaron valores inventados. Todos los valores (5 °C, 18 meses, 46 cm, 10 %, 50 mm, 20 s a 30 s, 20 L, 90 %, 1,5 veces, medio litro, 20 °C, 2 y 5 años) están en la norma.
- **Estilo:** sin segunda ni primera persona, sin marcas y sin coloquialismos.

---

## Hallazgos comunes a varios manuales

| # | Sev. | Manuales | Hallazgo | Corrección propuesta |
|---|---|---|---|---|
| G1 | MAYOR | SAP, SRE, SGE, SEP, SSA | Ningún manual incluye la sección **SEGURIDAD Y SALUD OCUPACIONAL**. El spec (5, secciones complementarias) la exige cuando «el agente o la descarga es un riesgo para las personas». Se cumple en todos: descarga de agua sobre transformadores o equipos energizados y áreas con líquidos inflamables (SAP); espumígeno irritante, superficies resbaladizas y efluente contaminante (SRE, SGE); polvo que reduce la visibilidad y es irritante respiratorio (SEP); solución alcalina irritante para piel y ojos (SSA). | Agregar 3.1.x SEGURIDAD Y SALUD OCUPACIONAL, antes de Control de cambios, con frase de finalidad e ítems sin valores numéricos: elementos de protección personal según la hoja de seguridad del agente; delimitación y señalización del área de prueba; coordinación con el responsable de la instalación (energía eléctrica, gas, proceso); prohibición de permanecer en la zona de descarga; contención y disposición del efluente según la normativa ambiental. Sin cierre de planilla (práctica del rubro). Declararla en «Valores y contenidos agregados». |
| G2 | MENOR | SRE, SGE, SEP, SSA | «CONTROL DE CAMBIOS Y RESPONSABILIDADES» está en una sola sección y en prosa. El spec las prevé separadas, en ese orden, con frase de finalidad e ítems. | Dividir en 3.1.x CONTROL DE CAMBIOS y 3.1.x RESPONSABILIDADES, cada una con frase de finalidad e ítems a), b)… |
| G3 | MENOR | SRE, SEP, SSA | Hay frecuencias de 5 años (y de 2 años en SEP) pero no existe la sección **ENSAYOS DE LARGO PLAZO** que exige el spec. | Agregar la sección después de MANTENIMIENTO, con remisión a los subtítulos quinquenales y bienales, o mover allí las tareas y dejar la remisión en el subtítulo de la frecuencia. |
| G4 | MENOR | SEP, SSA | Falta el párrafo de autocontrol. El spec 4.2 lo considera de transcripción obligatoria («siempre se transcriben»). | En 3.1.1 agregar: «Las planillas de inspección cuya frecuencia sea menor a un mes pueden ser completadas por el usuario de la instalación y se deben identificar como inspecciones de autocontrol; el mantenedor debe verificar su correcto cumplimiento, dejando constancia de los hallazgos verificados. En este sistema la norma no establece inspecciones de frecuencia menor a un mes.» |
| G5 | MENOR | SAP, SRE, SGE | El párrafo de autocontrol omite «y se deben identificar como inspecciones de autocontrol» (norma, Empleo de las planillas). | Texto actual: «…pueden ser completadas por el usuario de la instalación como inspecciones de autocontrol;». Reemplazar por: «…pueden ser completadas por el usuario de la instalación y se deben identificar como inspecciones de autocontrol;». |
| G6 | MENOR | Todos | En REGISTRO se lee «si cada ítem cumple, no cumple o no es apreciable». La planilla tiene dos categorías: «CUMPLE ✓» y «NO CUMPLE O NO APRECIABLE X». | «…indicar con ✓ si el ítem cumple, o con X si no cumple o no es apreciable, describiendo el desvío en observaciones…». |
| G7 | MENOR | Todos | La planilla de Información general se resume por categorías. Quedan sin mencionar campos que son tareas o datos de control: «Revisar condiciones de depósitos y depósitos de presión», «Anotar la última prueba de abastecimiento de agua», «Registro de la última inspección / Funcionan» (bombas), «Existe documentación técnica de diseño y construcción» (SAP), «Memoria de cálculo», «Los datos hidráulicos figuran cerca de la válvula», «La válvula está protegida», «Peligro de congelamiento» (SGE), «Cuenta con los instructivos de operación» (SEP), «Designación del local», «Capacidad del sistema kg/m³», «Otros equipos probados o inspeccionados», «Resultado y comentarios de inspección / mantenimiento» (SSA). | En REGISTRO enumerar como viñetas los campos de verificación de la planilla -1, o incorporarlos al bloque de la primera intervención. |
| G8 | MENOR | Todos | Falta la recomendación de la evaluación técnica previa según la IRAM 3619 (REQUISITOS, «Evaluación previa», NOTA 9), que el spec manda aplicar en el paso 4.2. | En 3.1.1, o como párrafo previo, agregar: «Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica previa de la instalación según la IRAM 3619.» |
| G9 | MENOR | Todos (texto común) | El tercer párrafo común de «Concordancia…» afirma que la IRAM 3546 «no prescribe en todos los casos frecuencias rígidas». Es inexacto: los capítulos auditados fijan frecuencias concretas. No se modifica en el manual porque es texto común. | Elevarlo al responsable de la plantilla maestra para su revisión. |
| G10 | MENOR | SRE, SGE, SEP, SSA | El PROCEDIMIENTO POSTERIOR A UNA DESCARGA cierra con una planilla de la norma, pero sus ítems son en su mayoría práctica agregada. El spec indica que una sección de práctica sin planilla no lleva cierre. | Quitar el cierre o limitarlo a «Las tareas de la norma incluidas en esta sección se registran en…». Declararlo en Dudas. |
| G11 | MAYOR | SEP, SSA | Los protocolos de prueba de disparo prueban el corte automático de gas o energía, pero no prevén el rearme seguro. Tras actuar la válvula de corte de gas, la reapertura sin verificar los pilotos y quemadores puede dejar escapes de gas sin quemar. | Agregar al paso de Restitución: «Rearmar la válvula de corte de gas o el corte eléctrico solo con los comandos de los artefactos en posición cerrada; la reapertura del gas y el reencendido de pilotos se realizan por el usuario o por personal habilitado en gas, verificando la ausencia de fugas.» Criterio: «corte rearmado, artefactos operativos y sin fugas». |

---

## 1. SG-PEM-IFI-SAP Sistema de Agua Pulverizada (cap. 8)

### Completitud y exactitud

**SAP-1 · MAYOR · Prueba anual: falta el campo «Modelo de descarga» (planilla 8D).**
- Dónde: 3.1.2.4.
- Agregar después de d): «e) Modelo de descarga: verificar y registrar el modelo de descarga observado en cada boquilla, comparándolo con el previsto en el diseño.»

**SAP-2 · MAYOR · Las tareas «Lubricado de válvulas de corte» y «Limpieza de cañerías» faltan en Mantenimiento anual.**
- La planilla 8D asigna frecuencia anual a «Lubricado de válvulas de corte» y a «Limpieza de cañerías… con caudal pleno de agua para asegurar que la suciedad arrastrada por el abastecimiento de agua no obstruye las boquillas. El agua debe fluir limpia».
- El manual solo las incluye en Mantenimiento mensual (texto). El spec 4.1 exige incluirlas en las dos frecuencias y declararlo en Dudas.
- Agregar en 3.1.3.2:
  - «Lubricado de válvulas de corte: aplicación de grafito o de grafito en aceite liviano en todos los vástagos.»
  - «Limpieza de cañerías: lavado con caudal pleno de todas las cañerías y conexiones subterráneas, para asegurar que la suciedad arrastrada por el abastecimiento no obstruye las boquillas; el agua debe fluir limpia.»
- En 3.1.3.1 d) agregar la finalidad que da la planilla («…para asegurar que la suciedad arrastrada… no obstruye las boquillas»).

**SAP-3 · MAYOR · Falta la sección RESPONSABILIDADES, pese a que el sistema tiene autocontrol (Semanal – Autocontrol). Falta también CONTROL DE CAMBIOS.**
- La eficacia depende del elemento protegido: la norma exige inspeccionar semanalmente que «no se ha modificado el elemento a proteger».
- Agregar 3.1.x CONTROL DE CAMBIOS y 3.1.x RESPONSABILIDADES antes de REGISTRO:
  - Usuario: completar la inspección semanal de autocontrol en SAP-2; no modificar el elemento protegido ni interponer objetos en la descarga; mantener calefaccionado el local de válvulas.
  - Mantenedor: verificar el autocontrol y dejar constancia.

**SAP-4 · MENOR · Inspección semanal: el ítem 6 de la planilla 8B («Inspeccionar que la válvula de control y sus componentes no tengan daños») no figura como tal.**
- El ítem h) habla solo de la «válvula de diluvio».
- Texto actual: «h) Válvula de diluvio: verificar que está libre de daños…». Reemplazar por: «h) Válvula de diluvio (válvula de control) y sus componentes: verificar que están libres de daños…».

**SAP-5 · MENOR · Inspección semanal g): la condición de temperatura queda restringida a «durante el tiempo frío».**
- La planilla 8B exige, sin condición, que el local «se mantiene por encima de 5 °C».
- Separar el ítem:
  - «g) Temperatura del local de la válvula de control: verificar que se mantiene por encima de **5 °C**.»
  - «h) Calefacción del local: durante el tiempo frío, comprobar que se encuentra suficientemente calefaccionado.»

**SAP-6 · MENOR · Inspección mensual i): falta la reserva presurizada (tanque hidroneumático) de la planilla 8C.**
- Texto actual: «i) Reserva de agua: verificar el nivel de agua…». Reemplazar por: «i) Reserva de agua sin presión o presurizada (tanque hidroneumático): verificar…».

**SAP-7 · MENOR · Prueba semestral d): la prueba hidráulica o neumática de cañerías no remite a procedimientos documentados.**
- La remisión solo aparece en Ensayos de largo plazo.
- Agregar tras d): «La prueba hidráulica o neumática se debe ejecutar conforme a procedimientos documentados en función de las normas de aplicación.» Para la prueba neumática conviene una advertencia de energía almacenada (agregado).

**SAP-8 · MENOR · Subtítulo «Inspección semanal».**
- La norma titula «Semanal - Autocontrol» y el spec (5, reglas) exige «Inspección semanal (autocontrol)».
- Cambiar el subtítulo 3.1.1.1.

**SAP-9 · MENOR · La regla de cañería seca se transcribe en forma genérica sin decir que aplica a este sistema.**
- La norma describe el SAP como «normalmente… sistemas tipo diluvio por cañerías secas».
- Agregar: «En los sistemas de agua pulverizada tipo diluvio con cañerías secas, que son el caso habitual, las tareas semanales y mensuales de este procedimiento se realizan trimestralmente, manteniendo sus subtítulos y planillas.»

**SAP-10 · MENOR · Mantenimiento mensual cierra en SAP-4 «Inspección y pruebas anuales».**
- Es admisible porque 8D contiene esos campos, pero debe declararse en Dudas.
- La maniobra de dispositivos de disparo (a) no tiene campo en 8D.

**SAP-11 · MENOR · REGISTRO no dice que SAP-1 se completa «en la primera intervención y cada vez que cambian los datos de la instalación».**
- El spec 4.3 lo exige, y los otros cuatro manuales sí lo dicen.
- Agregar la frase al final del párrafo de SAP-1.

### Solidez de los protocolos

**SAP-12 · CRÍTICO · Protocolo «prueba a caudal total», paso 3: «recorrer el área protegida durante la descarga».**
- Instruye al personal a ingresar en la zona de descarga de un sistema que protege transformadores eléctricos y depósitos de líquidos o gases inflamables. Hay riesgo de electrocución por equipos energizados y de exposición al proceso.
- En el paso 1 falta además la coordinación eléctrica y operativa.
- Paso 1, agregar: «coordinar con el responsable eléctrico y de proceso las condiciones del equipo protegido durante la descarga y obtener su autorización escrita».
- Paso 3, reemplazar «recorrer el área protegida durante la descarga» por: «observar la descarga desde posiciones fuera de la zona de descarga y fuera de las distancias de seguridad a partes energizadas definidas por el responsable eléctrico; verificar…».

**SAP-13 · MAYOR · Protocolo «prueba en blanco»: con la válvula de control aguas arriba cerrada (paso 1) no circula agua.**
- Por eso no puede verificarse «la actuación de la alarma de flujo de agua» (paso 3), y el criterio «se producen las señales de alarma previstas en el diseño» es inalcanzable.
- Tampoco se prevé la señal de supervisión de la válvula cerrada ni la reapertura lenta.
- Paso 3, cambiar a: «verificar el disparo de la válvula de diluvio (apertura del mecanismo o del clapeta, actuación del solenoide o del actuador) y las señales eléctricas de disparo en el panel; la alarma de flujo se verifica en la prueba trimestral».
- Paso 1, agregar: «registrar la señal de supervisión de válvula cerrada, cuando exista».
- Paso 4, agregar: «abrir lentamente la válvula de control para evitar golpe de ariete».

**SAP-14 · MAYOR · Faltan protocolo y precauciones para el disparo del sistema.**
- Prueba mensual e) «comprobar el funcionamiento de los accionamientos manuales y automáticos» y Mantenimiento mensual a) «operación de los dispositivos manuales de disparo» disparan la válvula de diluvio. Con la válvula de control abierta, eso produce la descarga total sobre el riesgo.
- El manual no indica cómo hacerlo sin descarga. El spec 6.3 exige protocolo para maniobras.
- Agregar después del cierre de 3.1.2.1: «Los accionamientos manuales y automáticos se comprueban con la válvula de control aguas arriba cerrada o con el dispositivo de prueba del fabricante, siguiendo los pasos 1, 3 y 4 del Protocolo de Ensayo de la prueba en blanco.» Agregar la misma remisión en 3.1.3.1 a).

**SAP-15 · MENOR · Protocolo trimestral, paso 3: el criterio «presión del sistema igual a la lectura inicial» es impracticable** (hay fluctuaciones normales del abastecimiento).
- Reemplazar por «presión del sistema dentro de sus valores normales y comparable con la lectura inicial».
- Paso 4: agregar «de a una válvula por vez, verificando su posición normal antes de maniobrar la siguiente».

---

## 2. SG-PEM-IFI-SRE Sistema de Rociadores de Espuma (cap. 9)

### Completitud y exactitud

**SRE-1 · MAYOR · Inspección quinquenal h): la norma da dos valores de presión de prueba hidrostática y el manual solo transcribe uno, sin declarar la discrepancia.**
- El texto (Cada 5 años) dice «prueba hidrostática a 1,5 veces la **presión de diseño**».
- La planilla 9E dice «Prueba hidrostática a 1,5 veces la **presión de trabajo**».
- Son valores distintos y el spec 4.1 exige incluir ambos y declararlo.
- Texto actual: «…la prueba hidrostática a 1,5 veces la presión de diseño.». Reemplazar por: «…la prueba hidrostática a **1,5 veces** la presión de diseño (texto de la norma); la planilla IRAM 3546-9E indica **1,5 veces** la presión de trabajo. El valor que se aplique debe definirlo el responsable técnico con el procedimiento documentado de prueba hidrostática y los datos del fabricante del tanque.» Declararlo en Dudas.

**SRE-2 · MAYOR · Prueba anual b) y protocolo, paso 5: la dosificación se verifica sin método ni instrumento.**
- El texto actual es «verificar la concentración de la solución de espuma». El spec 6.3 exige «con qué instrumento y dónde se mide».
- Es el criterio de aceptación central (≥ 90 % de la dosificación mínima de diseño).
- Reemplazar por: «tomar muestras de la solución en la conexión de prueba o en la descarga, y determinar la concentración con refractómetro o conductímetro, por comparación con una curva patrón preparada con el mismo espumígeno y agua del sistema, según las instrucciones del fabricante del espumígeno».

**SRE-3 · MAYOR · La prueba semestral de disparo de la válvula de control no tiene protocolo.**
- Es la maniobra más crítica: se cierran las válvulas de abastecimiento de agua y de espumígeno, el sistema queda fuera de servicio y requiere rearme y reapertura de ambos circuitos.
- Agregar «Protocolo de Ensayo: prueba de disparo sin descarga» con estos pasos:
  1. notificación y cierre e identificación de las válvulas de agua y de espumígeno;
  2. disparo por detección automática y por actuación manual;
  3. verificación de la apertura de la válvula de control sin flujo;
  4. rearme según el fabricante instalador, reapertura lenta de agua y espumígeno, precintado y verificación de presión normal.
- Criterio de aceptación: «disparo en ambos modos, válvulas de agua y espumígeno abiertas y precintadas, sistema en servicio».

**SRE-4 · MENOR · Prueba trimestral: la prueba de la bomba de espumígeno (20 s a 30 s) no tiene protocolo ni precaución de circuito.**
- Ejecutada sin recirculación, puede operar la bomba contra válvula cerrada o inyectar espumígeno en la red de agua.
- Agregar un protocolo breve: alineación a la línea de retorno o recirculación al tanque según el fabricante; marcha de **20 s a 30 s**; verificación de ausencia de pérdidas; realineación a la posición normal.

**SRE-5 · MENOR · Prueba trimestral a): faltan como ítems requisitos que solo aparecen en el protocolo.**
- El criterio «Las pérdidas de presión mayores que un **10 %** se deben investigar inmediatamente» y el requisito de que «la presión original de diseño… debe anotarse y grabarse en la válvula de rociadores» (más la etiqueta de criterios de diseño) solo están en el protocolo, después del cierre.
- Agregar como ítems h) e i) del bloque.

**SRE-6 · MENOR · Protocolo trimestral, paso 2: el criterio agrega una condición temporal que la norma no impone.**
- El texto «corregir antes de dar por finalizada la prueba» puede ser inejecutable, por ejemplo con una válvula cerrada en la red pública.
- La norma dice «debe corregirse el problema para que éstos funcionen adecuadamente».
- Reemplazar por «…determinar su causa y corregir el problema, registrando la acción correctiva».

**SRE-7 · MENOR · Prueba anual: los registros obligatorios figuran solo en el protocolo.**
- Los registros «tiempos de respuesta y descarga», «presión en el rociador hidráulicamente más alejado» y «presión en válvula de control principal» (en bar, planilla 9G) no están en la lista de ítems.
- Agregar como ítems.

**SRE-8 · MENOR · Las tareas de prueba anual se reclasificaron como Mantenimiento anual.**
- La norma no tiene un apartado Mantenimiento en el cap. 9: la operación de válvulas, la lubricación y la revisión de retenciones están en «Pruebas – Anual».
- Es aceptable porque la planilla 9G es «Prueba y mantenimiento anual», pero debe declararse en Dudas, y 3.1.3 debe decir que la norma no establece un apartado de mantenimiento propio.

**SRE-9 · MENOR · «Inspección interna por obstrucción de tuberías» cierra en SRE-5, que no tiene campos para esa tarea.**
- Declararlo en Dudas (spec 4.3).
- El título de la norma es «Bloqueo de tuberías»: conviene citarlo entre paréntesis para la trazabilidad.

**SRE-10 · MENOR · Protocolo de sedimentos, paso 1: falta la salvedad para tanques a presión.**
- En tanques de espumígeno a presión (de vejiga), el drenaje de fondo puede dañar la vejiga o no ser aplicable.
- Agregar: «en tanques a presión, según las instrucciones del fabricante».

---

## 3. SG-PEM-IFI-SGE Sistema Generador de Espuma (cap. 10)

### Completitud y exactitud

**SGE-1 · MAYOR · Prueba semestral a): requisito debilitado.**
- El texto de la norma exige probar: «Prueba del sistema de detección. Se prueba el sistema de detección para verificar su correcto funcionamiento.»
- El manual solo pide «controlar que fue probado» (redacción de la planilla 10E). Así se convierte una prueba en una verificación documental.
- Reemplazar por: «a) Sistema de detección: probar el sistema de detección para verificar su correcto funcionamiento, según el capítulo 6 de la IRAM 3546:2011, y, en los sistemas cuya actuación depende de él, controlar que la prueba quedó registrada.»

**SGE-2 · MAYOR · Prueba anual c) y protocolo, paso 5: la calidad de la espuma no tiene método ni criterio de aceptación.**
- Es un campo de la planilla 10F («Verificación de calidad de espuma obtenida»), pero el criterio del paso 5 solo trata la dosificación.
- La dosificación también carece de instrumento (igual que SRE-2).
- Agregar en el paso de ensayo: «tomar muestras de espuma en el dispositivo de descarga o en la conexión de prueba y determinar la relación de expansión y el tiempo de drenaje, y la concentración de la solución con refractómetro o conductímetro».
- Criterio: «relación de expansión y tiempo de drenaje según los valores del fabricante del espumígeno y del dispositivo generador; dosificación no menor que el **90 %** del valor mínimo de diseño».

**SGE-3 · MAYOR · Protocolo de descarga, paso 2: no prevé el caso de cámaras de espuma montadas en tanques de almacenamiento de inflamables.**
- La descarga real dentro del tanque contamina el producto y opera en atmósfera inflamable.
- Agregar: «En cámaras de espuma de tanques de almacenamiento, la descarga se realiza a través de la conexión de prueba o desviando la descarga fuera del tanque, según el diseño, sin introducir espuma en el producto almacenado; la descarga dentro del tanque solo se realiza con autorización del responsable de la instalación.»

**SGE-4 · MENOR · Protocolo, paso 4: se reemplazó la referencia de la norma sin dejar constancia.**
- El texto «dispositivo de descarga hidráulicamente más alejado» sustituye a la norma, que dice «rociador hidráulicamente más alejado».
- La adaptación es técnicamente razonable, pero debe declararse en Dudas o citarse así: «(la norma indica rociador)».

**SGE-5 · MENOR · Prueba trimestral a): falta protocolo y precaución de recirculación para la marcha de la bomba de espumígeno** (igual que SRE-4).
- La norma no fija la duración: no importar los «20 s a 30 s» del cap. 9.

**SGE-6 · MENOR · Mantenimiento semestral: la frase de finalidad es técnicamente imprecisa.**
- Texto actual: «conserve su condición de presión y vacío de diseño».
- Reemplazar por: «…verificar que la válvula de presión-vacío protege al depósito contra sobrepresión y depresión y limita la evaporación y la contaminación del espumígeno».

**SGE-7 · MENOR · Mantenimiento anual a): ítem tautológico.**
- Texto actual: «Lubricación de válvulas: lubricación de las válvulas del sistema».
- Reemplazar por: «Lubricación de válvulas: lubricación de vástagos y mecanismos de las válvulas del sistema según las instrucciones del fabricante.» No importar grafito ni aceite del cap. 9.

**SGE-8 · MENOR · Inspección mensual a): remisión que la norma no hace.**
- El manual agrega «según el capítulo 12 de la IRAM 3546:2011», pero el texto del cap. 10 no la contiene.
- Es aceptable como agregado, pero debe declararse.

---

## 4. SG-PEM-IFI-SEP Sistema Fijo de Extinción por Polvo (cap. 15)

### Completitud y exactitud

**SEP-1 · MAYOR · No hay protocolo para las tareas de mayor riesgo y medición.**
- Faltan protocolos para:
  - el pesaje y control de carga bienal («Comprobar el estado y peso de carga del polvo»);
  - el vaciado y la recarga bienal de BC y ABC;
  - la prueba de descarga quinquenal.
- El spec 6.3 lo exige para pesaje y descargas.
- Agregar «Protocolo de Ensayo: control de peso de carga» (balanza calibrada; criterio: peso igual o mayor que el mínimo anotado en SEP-1, según 15C).
- Agregar «Protocolo de Ensayo: prueba de descarga». Pasos:
  1. artefactos de cocina apagados y fríos, alimentos y aceites retirados o cubiertos;
  2. coordinación con el usuario y área delimitada;
  3. descarga y verificación de cobertura de todas las boquillas;
  4. limpieza, recarga y restitución.

**SEP-2 · MENOR · Mantenimiento bienal a): falta la precaución contra mezcla de agentes (agregado necesario).**
- Agregar: «con el mismo tipo de agente registrado en SEP-1 y sin mezclar agentes de distinta base (por ejemplo, fosfato monoamónico con bicarbonatos), según las instrucciones del fabricante».

**SEP-3 · MENOR · Inspección mensual d) y e): se importó texto del capítulo 16.**
- d) agrega «lo que implica la instalación de nuevas boquillas o la redistribución de las existentes», que es texto del cap. 16 y no del cap. 15.
- e) usa la redacción del cap. 16.
- El cap. 15 dice: «Verificar si algún equipo de cocina ha sido añadido al existente o modificado» y «Verificar que todas las boquillas están todavía cubriendo las superficies para las que han sido diseñadas».
- Usar la redacción del cap. 15, o declarar el agregado.

**SEP-4 · MENOR · Inspección semestral: corrección no declarada de una errata de la norma.**
- La planilla 15C remite a «el mínimo anotado en la planilla **10-A**» (errata: 10A es Información general del cap. 10). El manual la corrige a SEP-1 sin declararlo.
- Declarar en Dudas.

**SEP-5 · MENOR · La prueba de descarga quinquenal figura dos veces con condiciones distintas.**
- En «Prueba – Cada 5 años» es condicional («cuando se exija»); en «Mantenimiento – Cada 5 años» es incondicional.
- Declarar la inconsistencia de la norma en Dudas y unificar el criterio en el manual. Propuesta: obligatoria cada 5 años salvo exención documentada.

**SEP-6 · MENOR · El protocolo de prueba semestral, paso 3, no exige verificar el rearme antes de reconectar.**
- Debe constatarse que el mecanismo de disparo quedó armado antes de reconectar el cilindro o cartucho: un mecanismo disparado produce la descarga al reconectar.
- Agregar al paso: «verificar que el mecanismo de disparo y el actuador del cilindro se encuentran en posición armada antes de reconectar el cilindro o el cartucho».

**SEP-7 · MENOR · Registros bienales y quinquenales en SEP-3, con trato desigual.**
- Concentrar en SEP-3 (semestral) los registros bienales y quinquenales es defendible por el apartado c) de Empleo de las planillas.
- Sin embargo, Mantenimiento semestral, anual y posterior a descarga cierran en SEP-3 sin la misma aclaración.
- Unificar el criterio y declararlo en Dudas.

---

## 5. SG-PEM-IFI-SSA Sistema Fijo de Extinción por Solución Acuosa (cap. 16)

### Solidez de los protocolos

**SSA-1 · CRÍTICO · Protocolo «prueba de descarga con agua», pasos 1 y 2: no exige que los artefactos estén fríos y sin aceite.**
- Descargar agua sobre freidoras o planchas con aceite caliente provoca proyección violenta del aceite y riesgo de quemaduras graves o incendio.
- El criterio actual («área protegida preparada para recibir la descarga») no lo cubre.
- Paso 1, agregar: «verificar que todos los artefactos protegidos están apagados y a temperatura ambiente, con el aceite retirado o las cubas tapadas, y que el gas y la energía están cortados».
- Criterio paso 1: «artefactos apagados y fríos, sin aceite expuesto, área delimitada».

**SSA-2 · MAYOR · Protocolo quinquenal, paso 1: no hay precauciones de manipulación ni de disposición.**
- La solución extintora se retira del recipiente sin medidas de manipulación. Es alcalina e irritante para piel y ojos.
- Tampoco se indica la disposición de la solución retirada, que la norma manda reemplazar por «nueva solución».
- Agregar: «con elementos de protección ocular y de manos según la hoja de seguridad del agente; la solución retirada se dispone conforme a la normativa ambiental aplicable». Vincularlo con G1.

### Completitud y exactitud

**SSA-3 · MENOR · Mantenimiento semestral: los ítems a) a h) son sustantivos sueltos («a) Detectores y eslabones fusibles.»).**
- Incumple el spec 6.2.4 («Elemento: verbo + qué se controla + criterio»). La introducción tampoco usa la fórmula canónica.
- Reescribir con la fórmula, por ejemplo: «a) Detectores y eslabones fusibles: comprobación de su estado, limpieza y ausencia de grasa o daños.» Introducción: «Durante estas tareas se debe realizar:».

**SSA-4 · MENOR · La prueba hidrostática de Mantenimiento semestral no remite a procedimientos documentados.**
- La prueba hidrostática «según necesidad» (párrafo de daños por corrosión, fuego o soldadura) carece de la remisión que el spec 4.2 exige.
- Agregar la frase.

**SSA-5 · MENOR · Equipamiento y protocolo semestral no nombran el corte de gas o energía.**
- Si la instalación tiene corte automático de gas o energía como «equipo asociado», debe nombrarse en el equipamiento y verificarse en el paso 2 del protocolo semestral, con el rearme seguro (G11).

**SSA-6 · MENOR · Faltan campos de SSA-1 en REGISTRO** (ver G7): «Designación del local», «Capacidad del sistema kg/m³», «No hay modificaciones…», «Resultado y comentarios de inspección / mantenimiento», «Otros equipos probados o inspeccionados».
