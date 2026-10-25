# -*- coding: utf-8 -*-
SIG, NOM, NOMU, CAP = 'SAA', 'Sistema de Abastecimiento de Agua', 'SISTEMA DE ABASTECIMIENTO DE AGUA', '13'
PL = {1: 'Información general', 2: 'Inspección semanal', 3: 'Inspección y prueba mensual', 4: 'Inspección trimestral y anual',
      5: 'Mantenimiento', 6: 'Pruebas quinquenales'}
VIG = (' Se aplica la edición vigente de cada norma NFPA; la numeración de los artículos citados se debe confirmar en esa '
       'edición, porque puede variar entre ediciones.')


def CONTENT(cierre):
    C = []; a = C.append
    a(('h2', NOMU))
    a(('basado', '(Basado en IRAM 3546:2011 – Capítulo %s; criterios complementarios: NFPA 25 y NFPA 22)' % CAP))
    a(('p', 'Este apartado establece los requisitos mínimos para la inspección, prueba y mantenimiento de los tanques de '
            'almacenamiento de agua de los sistemas contra incendio, con el objetivo de asegurar que la reserva conserve el volumen, '
            'la calidad y la temperatura del agua previstos en el diseño y que su estructura no se deteriore.'))
    a(('p', 'La IRAM 3546:2011 es la base del presente procedimiento y fija sus frecuencias. La NFPA 25 (capítulo 9, '
            'Tanques de almacenamiento de agua) se aplica como criterio complementario para la inspección, prueba y mantenimiento, '
            'y la NFPA 22, Norma para tanques de agua de protección contra incendios privada, es la norma de diseño e instalación a '
            'la que deben ajustarse las reparaciones y los reemplazos. Ante diferencias, se adopta siempre la condición más '
            'exigente.' + VIG))
    a(('p', 'El procedimiento comprende los tanques elevados, a nivel y enterrados, de acero, hormigón, fibra de vidrio o tela '
            'revestida, los tanques a presión (hidroneumáticos) y sus accesorios. El equipamiento del sistema incluye:'))
    a(('items', [
        ('Tanque', 'cuerpo del tanque con su techo, tapas de acceso, venteos con mallas, rebosadero y placa antivórtice en la salida.'),
        ('Estructura soporte', 'fundaciones, columnas, pasarelas, escaleras y barandas, donde existan.'),
        ('Instrumentos y señales', 'indicador de nivel, alarmas de alto y bajo nivel, manómetros y alarmas de baja temperatura del agua.'),
        ('Sistema de calefacción', 'equipo de calefacción del agua, termostatos e interruptores de límite de alta temperatura, '
                                   'donde el tanque está sujeto a congelamiento.'),
        ('Válvulas y accesorios', 'válvulas de control, de retención, de drenaje y de llenado automático, cañerías y soportes.'),
        ('Protección contra la corrosión', 'pinturas, recubrimientos, aislaciones y protección catódica, donde exista.'),
    ]))
    a(('p', 'La inspección, prueba y mantenimiento de los tanques puede dejar al sistema fuera de servicio. Se deben seguir los '
            'procedimientos correspondientes para que esto no ocurra y aplicar el procedimiento de puesta fuera de servicio de este '
            'manual cuando la reserva deba vaciarse o aislarse.'))

    # ---------------- INSPECCIÓN ----------------
    a(('h3', 'INSPECCIÓN'))
    a(('p', 'La inspección consiste en un examen visual del tanque, de su estructura y de sus accesorios, para verificar que están en '
            'condiciones aparentes de operación y libres de daños, debilitamiento o condiciones que aceleren su deterioro.'))
    a(('p', 'Las inspecciones de frecuencia menor a un mes pueden ser completadas por el usuario de la instalación como '
            'inspecciones de autocontrol, y se deben identificar como tales; el mantenedor debe verificar su correcto cumplimiento, '
            'dejando constancia de los hallazgos.'))
    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica previa '
            'de la instalación según la IRAM 3619; esta evaluación no es obligatoria y puede ser solicitada por cualquiera de las '
            'partes interesadas.'))

    a(('h4', 'Inspección diaria en la estación fría (autocontrol)'))
    a(('p', 'Esta inspección tiene como finalidad evitar el congelamiento del agua en los tanques sujetos a bajas temperaturas.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Temperatura del agua', 'donde el tanque está sujeto a congelamiento, comprobar que la temperatura del agua es como mínimo '
                                 'de **4 °C** (NFPA 25, 9.2.3.1).'),
        ('Sistema de calefacción', 'comprobar que funciona durante la estación fría.'),
    ]))
    a(('p', 'Los tanques con alarma de baja temperatura supervisada desde un lugar atendido en forma permanente pueden controlarse '
            'semanalmente, registrando el resultado. La inspección diaria se registra en la planilla de inspección semanal del período.'))
    a(('p', cierre(2)))

    a(('h4', 'Inspección semanal'))
    a(('p', 'La inspección semanal tiene como finalidad verificar la temperatura del agua, la calefacción y la posición de las '
            'válvulas de control.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Temperatura del agua', 'en tanques con alarma de baja temperatura supervisada, comprobar y registrar que es como mínimo de '
                                 '**4 °C**.'),
        ('Sistema de calentamiento', 'en tanques con alarma de baja temperatura supervisada, comprobar que funciona.'),
        ('Válvulas de control', 'comprobar que están precintadas y en la posición indicada.'),
    ]))
    a(('p', cierre(2)))

    a(('h4', 'Inspección mensual'))
    a(('p', 'La inspección mensual tiene como finalidad verificar que el tanque conserva el nivel de diseño y que el agua y los '
            'tanques a presión están en condiciones.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Nivel de agua', 'comprobar mediante el indicador de nivel, donde exista, que el tanque está lleno o en el nivel de diseño '
                          '(NFPA 25, 9.2.1.3). En los tanques con alarma de nivel supervisada, la IRAM 3546:2011 admite la inspección '
                          'mensual o trimestral; se adopta la mensual.'),
        ('Condición del agua', 'comprobar la ausencia de contaminación, materiales extraños, crecimiento biológico o sedimentos '
                               'visibles.'),
        ('Válvulas de control', 'comprobar su posición y su estado.'),
        ('Tanques a presión', 'comprobar la presión de aire y el nivel de agua.'),
    ]))
    a(('p', cierre(3)))

    a(('h4', 'Inspección trimestral'))
    a(('p', 'La inspección trimestral tiene como finalidad detectar daños o debilitamiento del tanque y de su estructura, y '
            'condiciones del entorno que representen un riesgo.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Exterior del tanque', 'comprobar la ausencia de signos de daño o debilitamiento en paredes, techo, venteos, tapas y '
                                'fundaciones.'),
        ('Estructura soporte', 'comprobar su estado, donde exista.'),
        ('Pasarelas y escaleras', 'comprobar que están firmes y sin corrosión.'),
        ('Área circundante', 'comprobar que está libre de acumulación de materiales combustibles, basura o escombros que puedan '
                             'representar un riesgo de exposición a un incendio, libre de materiales sobre o cerca de partes que '
                             'puedan acelerar la corrosión o la putrefacción, y que el tanque está libre de hielo. En los tanques de '
                             'tela revestida soportados por endicados, comprobar además que los taludes no presentan erosión '
                             '(NFPA 25, 9.2.4.2).'),
    ]))
    a(('p', cierre(4)))

    a(('h4', 'Inspección anual'))
    a(('p', 'La inspección anual tiene como finalidad detectar la degradación de las protecciones exteriores y de las juntas.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Superficies pintadas, protegidas o aisladas', 'comprobar que las caras exteriores del tanque y de la estructura soporte '
                                                        'no se han degradado.'),
        ('Juntas de expansión', 'comprobar la ausencia de fugas o roturas.'),
        ('Tanques de madera', 'inspeccionar los zunchos y el emparrillado (NFPA 25, 9.2.4.4).'),
    ]))
    a(('p', cierre(4)))

    a(('h4', 'Inspección interior'))
    a(('p', 'La inspección interior tiene como finalidad detectar la corrosión, el deterioro del recubrimiento y los defectos '
            'estructurales que no son visibles desde el exterior.'))
    a(('p', 'El interior del tanque se debe inspeccionar cada **5 años**, salvo los tanques de acero a gravedad sin protección '
            'anticorrosiva y los tanques a presión, que se inspeccionan cada **3 años**. Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Recubrimiento interior', 'signos de falla local o generalizada, picaduras, corrosión, desprendimientos, putrefacción, '
                                   'residuos y crecimiento acuático (NFPA 25, 9.2.5.3).'),
        ('Columnas centrales', 'en los diseños tubulares, que no retienen agua y que no están permanentemente adosadas al piso.'),
        ('Fundaciones tipo anillo con arena', 'ausencia de huecos debajo del piso; los huecos se eliminan mediante rellenado.'),
        ('Sistema de calefacción', 'estado de sus componentes y cañerías; los dañados se deben reemplazar.'),
        ('Placa antivórtice', 'ausencia de deterioro o bloqueo.'),
    ]))
    a(('p', 'Cuando la inspección se realiza mediante una evaluación subacuática, primero se debe retirar el sedimento del fondo del '
            'tanque (NFPA 25, 9.2.5.2).'))
    a(('p', cierre(6)))

    # ---------------- PRUEBA ----------------
    a(('h3', 'PRUEBA'))
    a(('p', 'Las pruebas tienen como propósito verificar el funcionamiento de las señales, de la calefacción y de los instrumentos '
            'del tanque. El mantenimiento se debe realizar inmediatamente después de las pruebas que detectan fallas.'))

    a(('h4', 'Prueba mensual'))
    a(('p', 'La prueba mensual tiene como finalidad verificar las protecciones de temperatura en los tanques sujetos a congelamiento '
            'que requieren calentamiento en invierno.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Alarmas de baja temperatura', 'probarlas mensualmente durante la estación fría.'),
        ('Interruptores de límite de alta temperatura', 'probarlos mensualmente mientras el sistema de calefacción está en servicio.'),
    ]))
    a(('p', 'La NFPA 25 (9.3.3 y 9.3.4) exige probar estos dispositivos al comienzo de la temporada de calefacción; la frecuencia '
            'mensual de la IRAM 3546:2011 es más exigente y se mantiene.'))
    a(('p', cierre(3)))

    a(('h4', 'Prueba antes de la estación fría'))
    a(('p', 'Esta prueba tiene como finalidad asegurar que la calefacción del tanque funcionará antes de que se presenten condiciones '
            'de congelamiento.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Sistema de calefacción', 'probarlo antes de la llegada de la estación fría para asegurar su correcto funcionamiento '
                                   '(NFPA 25, 9.3.2).'),
    ]))
    a(('p', cierre(3)))

    a(('h4', 'Prueba semestral'))
    a(('p', 'La prueba semestral tiene como finalidad verificar las alarmas de nivel de agua.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Alarmas de alto y bajo nivel', 'probarlas como mínimo cada seis meses, verificando la recepción de la señal en el sistema de '
                                         'detección o de supervisión cuando el control de nivel está vinculado a él. La NFPA 25 '
                                         '(9.3.5) exige esta prueba con frecuencia anual; la semestral de la IRAM es más exigente.'),
    ]))
    a(('p', cierre(4)))

    a(('h4', 'Prueba anual'))
    a(('p', 'La prueba anual tiene como finalidad verificar la exactitud de los manómetros y el funcionamiento de las válvulas de '
            'llenado automático.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Manómetros', 'compararlos con manómetros calibrados según las instrucciones del fabricante. La IRAM 3546:2011 exige '
                       'recalibrar o reemplazar los que tengan un error mayor que el **10 %**, mientras que la NFPA 25 (13.2.4.3) '
                       'admite un error de hasta el **3 %** de la escala completa; se adopta la frecuencia anual de la IRAM con la '
                       'tolerancia del 3 % de la NFPA 25.'),
        ('Válvulas de llenado automático', 'bajar el nivel del tanque para que la válvula actúe automáticamente y medir y registrar '
                                           'el caudal de llenado (NFPA 25, 9.5.3).'),
    ]))
    a(('p', cierre(4)))

    a(('h4', 'Prueba quinquenal'))
    a(('p', 'La prueba quinquenal tiene como finalidad verificar los indicadores de nivel y el interior del tanque.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Indicadores de nivel', 'ensayarlos para verificar su exactitud y su libertad de movimiento (NFPA 25, 9.3.1).'),
        ('Interior del tanque', 'verificar sus condiciones según la inspección interior; en tanques de acero sin protección '
                                'anticorrosiva, cada tres años.'),
        ('Válvulas de retención', 'verificar sus condiciones mediante inspección interna.'),
        ('Manómetros', 'registrar el resultado de la última comparación con un manómetro calibrado.'),
    ]))
    a(('p', 'Durante la inspección interior de un tanque de acero que presente picaduras, corrosión o fallas del recubrimiento, se '
            'deben realizar las siguientes pruebas (IRAM 3546:2011; NFPA 25, 9.2.6):'))
    a(('items', [
        ('Adherencia del recubrimiento', 'ensayo de adherencia por cinta según la ASTM D3359, conocido como ensayo de cuadrícula.'),
        ('Espesor de película', 'mediciones del espesor de película seca en lugares elegidos al azar.'),
        ('Espesor de pared', 'medición por ultrasonido en los lugares con picaduras o corrosión.'),
        ('Continuidad del recubrimiento', 'ensayo con esponja húmeda para detectar poros, fisuras u otros defectos, con especial '
                                          'atención a los bordes agudos, como peldaños, tuercas y bulones.'),
        ('Fondo del tanque', 'detección de pérdida de material o herrumbre en la cara inferior por ultrasonido; como alternativa, '
                             'extracción, inspección visual y reposición de muestras del piso.'),
        ('Costuras del fondo', 'en tanques de fondo plano, ensayo de las costuras con caja de vacío según la NFPA 22.'),
    ]))
    a(('p', cierre(6)))

    # ---------------- MANTENIMIENTO ----------------
    a(('h3', 'MANTENIMIENTO'))
    a(('p', 'El mantenimiento debe asegurar que el tanque y sus accesorios estén operativos y confiables, y se debe realizar '
            'inmediatamente después de las pruebas que detectan fallas.'))

    a(('h4', 'Mantenimiento permanente'))
    a(('p', 'Estas condiciones se deben mantener en forma permanente y verificar en cada intervención.'))
    a(('p', 'Durante cada intervención se debe asegurar:'))
    a(('items', [
        ('Nivel de agua', 'tanque lleno al nivel de diseño (NFPA 25, 9.4.2).'),
        ('Tapas y accesos del techo', 'cubiertas de las trampas de techo y puertas de acceso firmemente aseguradas con trabas '
                                      'adecuadas, como protección contra el congelamiento y los vientos.'),
        ('Limpieza', 'interior y exterior del tanque y su estructura correctamente pintados y libres de crecimiento acuático, '
                     'sedimentos, materiales extraños, herramientas, equipos de pintura y cualquier objeto que interfiera con su '
                     'operación; sin acumulación de hielo en lugares que afecten el funcionamiento.'),
        ('Fundaciones', 'partes superiores de las pilas de fundación como mínimo **0,15 m** sobre el nivel del piso y sin material '
                        'combustible cerca de las columnas.'),
        ('Fosos de válvulas y casetas', 'temperatura mínima de **4 °C**, protección contra la intemperie y ausencia de acumulación '
                                        'de agua.'),
        ('Calefacción', 'mantenimiento del sistema según las instrucciones del fabricante, con una temperatura mínima del agua de '
                        '**4 °C**.'),
    ]))
    a(('p', cierre(5)))

    a(('h4', 'Mantenimiento semestral'))
    a(('p', 'El mantenimiento semestral tiene como finalidad evitar que los sedimentos alcancen el nivel de la salida del tanque.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Drenaje de sedimentos', 'eliminación de sedimentos por drenaje o extracción de fondo, abriendo y cerrando totalmente las '
                                  'válvulas de drenaje. La NFPA 25 (9.4.5) exige además retirar el sedimento en cada inspección '
                                  'interior o con mayor frecuencia, si es necesario.'),
    ]))
    a(('p', cierre(5)))

    a(('h4', 'Mantenimiento trimestral'))
    a(('p', 'El mantenimiento trimestral tiene como finalidad conservar la capacidad de llenado automático del tanque.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Filtros de las válvulas de llenado automático', 'limpieza de los filtros (NFPA 25, 9.5.2.3).'),
    ]))
    a(('p', cierre(5)))

    a(('h4', 'Mantenimiento anual'))
    a(('p', 'El mantenimiento anual tiene como finalidad conservar la protección contra la corrosión y la ventilación del tanque.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Protección catódica', 'mantenimiento según las instrucciones del fabricante.'),
        ('Venteos', 'limpieza como mínimo anual, o con mayor frecuencia si es necesario, y reemplazo de las mallas corroídas o rotas.'),
        ('Termostato', 'verificación del funcionamiento del termostato del sistema de calefacción.'),
        ('Válvulas de control y de drenaje', 'operación y mantenimiento según el capítulo 13 de la NFPA 25.'),
        ('Cañerías y soportes', 'mantenimiento según los criterios de cañerías y soportes de los capítulos 7 y 9 de la IRAM 3546:2011.'),
    ]))
    a(('p', cierre(5)))

    a(('h4', 'Mantenimiento bienal de tanques de tela revestida en endicados'))
    a(('p', 'Este mantenimiento tiene como finalidad conservar la membrana de los tanques de tela revestida soportados por endicados.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Superficies expuestas', 'inspección de la pintura cada **2 años** y limpieza y pintura según las instrucciones del '
                                  'fabricante (NFPA 25, 9.4.6.2), con la pintura y el procedimiento que el fabricante recomiende.'),
        ('Techo del tanque', 'ausencia de tablas, latas de pintura, accesorios o material suelto; accesorios de acceso firmemente '
                             'fijados; ausencia de grandes acumulaciones de hielo, lo que se evita manteniendo el agua sobre el punto '
                             'de congelamiento y el tanque lleno al tope.'),
        ('Entorno', 'ausencia de material combustible, hierbas, matorrales y follaje muerto cerca del tanque.'),
        ('Endicado', 'inspección de la superficie del endicado y de los aterrazados para detectar erosión del suelo.'),
        ('Interior', 'limpieza e inspección según se requiera para eliminar la acumulación de sedimentos.'),
    ]))
    a(('p', cierre(5)))

    a(('h4', 'Mantenimiento quinquenal'))
    a(('p', 'El mantenimiento quinquenal tiene como finalidad verificar internamente las válvulas de retención del abastecimiento.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Válvulas de retención', 'inspección interna y mantenimiento cada **5 años** (NFPA 25, 13.4.2.1).'),
        ('Válvulas de llenado automático', 'inspección interna y de filtros, orificios y piezas de goma según las instrucciones del '
                                           'fabricante (NFPA 25, Tabla 9.5.1.1).'),
    ]))
    a(('p', cierre(5)))

    a(('h4', 'Reparaciones y repintado'))
    a(('p', 'Las reparaciones tienen como finalidad restituir el tanque a su condición de diseño sin introducir riesgos de obstrucción.'))
    a(('p', 'En toda reparación se debe asegurar:'))
    a(('items', [
        ('Criterio de diseño', 'reparaciones y reemplazos según el criterio de diseño original y los criterios de instalación de la '
                               'NFPA 22.'),
        ('Materiales', 'uso exclusivo de materiales que no se aflojen ni se desprendan obstruyendo la salida.'),
        ('Soldaduras', 'ejecución y prueba de las soldaduras según la norma de tanques.'),
        ('Protección de la salida', 'cobertura de las aberturas de salida durante el mantenimiento interior y la pintura con una '
                                    'cubierta de no más de unas pocas hojas de papel, que se retira antes de devolver el tanque al '
                                    'servicio.'),
        ('Repintado de tanques de acero', 'repintado solo sobre superficies secas, totalmente limpias de pintura base suelta, '
                                          'escamas, incrustaciones u otros contaminantes.'),
        ('Huecos bajo el piso', 'relleno con inyección de mortero o reposición de la arena (NFPA 25, 9.4.1).'),
    ]))
    a(('p', cierre(5)))

    # ---------------- COMPLEMENTARIAS ----------------
    a(('h3', 'PUESTA FUERA DE SERVICIO'))
    a(('p', 'La puesta fuera de servicio tiene como finalidad limitar el riesgo y la duración de cualquier interrupción del '
            'abastecimiento, programada o de emergencia, según el capítulo 15 de la NFPA 25.'))
    a(('p', 'Antes de vaciar o aislar un tanque se debe asegurar:'))
    a(('items', [
        ('Coordinador', 'designación de un coordinador por el propietario o su representante.'),
        ('Alcance', 'determinación de los sistemas que dependen del tanque y de la duración prevista de la interrupción.'),
        ('Medidas compensatorias', 'cuando la protección quede fuera de servicio más de **10 h** en un período de **24 h**, '
                                   'abastecimiento de agua provisorio, guardia de incendio aprobada, evacuación del sector afectado '
                                   'o un programa aprobado para eliminar fuentes de ignición.'),
        ('Avisos y tarjetas', 'notificación al servicio de bomberos, a la aseguradora, a la empresa de monitoreo y a la autoridad '
                              'competente, y colocación de tarjetas en las tomas de impulsión y en las válvulas de control de los '
                              'sistemas afectados.'),
    ]))
    a(('p', 'Al restablecer el servicio se debe verificar el nivel de agua, la posición de las válvulas y el funcionamiento de los '
            'dispositivos de supervisión, informar a todas las partes notificadas y retirar las tarjetas.'))

    a(('h3', 'SEGURIDAD Y SALUD OCUPACIONAL'))
    a(('p', 'La seguridad del personal tiene como finalidad evitar los riesgos de trabajo en altura y en espacios confinados propios '
            'de los tanques.'))
    a(('p', 'Durante las tareas se debe asegurar:'))
    a(('items', [
        ('Espacio confinado', 'ingreso al interior del tanque solo con permiso de trabajo, medición previa de la atmósfera, '
                              'ventilación, vigía exterior y medios de rescate disponibles.'),
        ('Trabajo en altura', 'uso de arnés con línea de vida en escaleras, pasarelas y techos de tanques elevados, y verificación '
                              'previa de su estado.'),
        ('Inspección subacuática', 'ejecución solo por personal calificado para buceo, con el tanque aislado de las bombas.'),
        ('Recubrimientos y pinturas', 'uso de protección respiratoria y control de la ventilación durante la limpieza y el repintado.'),
        ('Tanques a presión', 'despresurización antes de abrir tapas o desmontar accesorios.'),
    ]))

    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'Los cambios en la demanda de los sistemas abastecidos, en el volumen útil del tanque o en sus accesorios pueden dejar la '
            'reserva por debajo de lo requerido. Toda modificación se debe evaluar técnicamente y registrar en la planilla de '
            'información general.'))
    a(('p', 'La empresa mantenedora es responsable de ejecutar las tareas de inspección, prueba y mantenimiento y de verificar las '
            'inspecciones de autocontrol. El usuario o propietario es responsable de completar las inspecciones de autocontrol, de '
            'mantener el tanque lleno y su entorno libre, y de coordinar las puestas fuera de servicio.'))
    return C


def REGISTRO_EXTRA(cierre):
    return [
        'Los datos de la instalación, del riesgo protegido, del abastecimiento de agua, de las características constructivas del '
        'tanque, de sus alarmas de nivel, de las bombas y de la toma de impulsión para bomberos se registran en la planilla '
        'SG-PEM-IFI-%s-1 %s – %s.' % (SIG, NOM, PL[1]),
        'Los registros de las inspecciones interiores, con las mediciones de espesores y los resultados de los ensayos, se deben '
        'conservar durante toda la vida útil del tanque para comparar su evolución.',
        'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '
        'codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables se indican con NA. Toda '
        'condición O o X se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y '
        'por el responsable de la instalación, con su aclaración.',
    ]
