# -*- coding: utf-8 -*-
SIG, NOM, NOMU, CAP = 'SGE', 'Sistema Generador de Espuma', 'SISTEMA GENERADOR DE ESPUMA', '10'
PL = {1: 'Información general', 2: 'Inspección semanal', 3: 'Inspección mensual', 4: 'Inspección anual',
      5: 'Pruebas trimestrales y semestral', 6: 'Prueba anual', 7: 'Mantenimiento'}

AVISO = ('Antes de realizar cualquier actividad de inspección o prueba que pueda generar alarmas o descargas, '
         'se deberá notificar previamente al responsable del sistema o al servicio de monitoreo correspondiente.')
REPOSICION = ('Reposición del sistema', 'comprobar que todas las válvulas, interruptores y controles de funcionamiento se '
              'reponen a su posición normal y que el sistema queda en servicio.')


def CONTENT(cierre):
    C = []; a = C.append
    a(('h2', NOMU))
    a(('basado', '(Basado en IRAM 3546:2011 – Capítulo %s)' % CAP))
    a(('p', 'Este apartado establece los requisitos mínimos para la inspección, prueba y mantenimiento del sistema generador de '
            'espuma, con el objetivo de asegurar que el sistema produzca y descargue espuma con la dosificación y la calidad '
            'previstas en las condiciones de diseño, en condiciones de emergencia.'))
    a(('p', 'Un sistema de espuma está constituido por una fuente de agua, válvulas de control, proporcionadores, un tanque de '
            'emulsor y dispositivos de descarga. La espuma se forma al dosificar el espumígeno en el agua y al incorporar aire en '
            'los dispositivos de descarga, por lo que la eficacia del sistema depende tanto del estado de sus componentes como de '
            'la calidad del espumígeno almacenado.'))
    a(('p', 'El equipamiento del sistema incluye:'))
    a(('items', [
        ('Abastecimiento de agua', 'depósitos a gravedad o bajo presión y bombas contra incendio, cuyo mantenimiento se rige por los '
                                   'capítulos 13 y 12 de la IRAM 3546:2011.'),
        ('Válvulas de control', 'válvulas de poste indicador, válvulas de calle y demás válvulas de seccionamiento, precintadas, '
                                'enclavadas o supervisadas, según el tipo de sistema: húmedo, seco, diluvio o acción previa.'),
        ('Tanque de emulsor', 'depósito de espumígeno, de plástico reforzado con fibra de vidrio o metálico, con cúpula de expansión '
                              'y válvula de presión-vacío.'),
        ('Bomba de espumígeno', 'equipo que impulsa el espumígeno hacia el dosificador, cuando la instalación lo prevé.'),
        ('Proporcionador o dosificador', 'equipo que incorpora el espumígeno en el agua en la proporción de diseño, del tipo eductor, '
                                         'sistema de pilotaje o presión balanceada.'),
        ('Dispositivos de descarga', 'cámaras de espuma, formadores de espuma y toberas que generan y aplican la espuma sobre el riesgo.'),
        ('Red de tuberías', 'tuberías y soportes que conducen el agua y la solución de espuma.'),
        ('Equipos auxiliares, tales como', ''),
        ['manómetros del sistema;',
         'sistema de detección, cuando la actuación depende de él;',
         'toma de impulsión para bomberos.'],
    ]))
    a(('p', 'Ante la actuación del sistema, manual o mediante el sistema de detección, se abre la válvula de control, el '
            'proporcionador incorpora el espumígeno en el caudal de agua y la solución llega a los dispositivos de descarga, donde '
            'se genera la espuma que se aplica sobre el riesgo protegido.'))
    a(('p', AVISO))

    # ---------------- INSPECCIÓN ----------------
    a(('h3', 'INSPECCIÓN'))
    a(('p', 'La inspección consiste en la verificación visual del sistema y de sus componentes, con el fin de comprobar que se '
            'encuentran en condiciones aparentemente óptimas de operación y libres de daños físicos. Se realiza generalmente en '
            'cada planta, recorriendo las zonas protegidas.'))
    a(('p', 'Si durante las inspecciones o pruebas se comprueba que el sistema ha sido alterado o cambiado, por cambio o reubicación '
            'de partes, se debe determinar si se alteró el diseño original y si el sistema opera normalmente. La prueba verifica que '
            'todos los dispositivos cumplan con lo requerido por el diseño original.'))
    a(('p', 'Las inspecciones de frecuencia menor a un mes pueden ser completadas por el usuario de la instalación como '
            'inspecciones de autocontrol, y se deben identificar como tales; el mantenedor debe verificar su correcto cumplimiento, '
            'dejando constancia de los hallazgos.'))
    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica '
            'previa de la instalación según la IRAM 3619, para verificar su grado de cumplimiento con las normas y la legislación '
            'vigente; esta evaluación no es obligatoria y puede ser solicitada por cualquiera de las partes interesadas.'))
    a(('p', 'De acuerdo con los requisitos generales de la IRAM 3546:2011, cuando el sistema sea de cañería seca, a excepción de '
            'los sistemas de acción previa, o se abastezca de agua por gravedad o en forma directa desde la red pública o privada, '
            'las tareas con periodicidad menor a trimestral se deben realizar trimestralmente.'))

    a(('h4', 'Inspección semanal'))
    a(('p', 'Las inspecciones semanales tienen como finalidad verificar que las válvulas de control se mantienen abiertas y que el '
            'abastecimiento de agua y la reserva de emulsor se encuentran disponibles.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Válvulas de control', 'comprobar que las válvulas selladas o precintadas, incluidas las de poste indicador y las válvulas '
                                'de calle, se encuentran abiertas.'),
        ('Precintos', 'verificar que las válvulas están precintadas; si no lo están, se deben volver a precintar y dejar constancia '
                      'en observaciones.'),
        ('Abastecimiento de agua', 'revisar los depósitos a gravedad y bajo presión.'),
        ('Tanque de líquido emulsor', 'inspeccionar su nivel.'),
    ]))
    a(('p', cierre(2)))

    a(('h4', 'Inspección mensual'))
    a(('p', 'Las inspecciones mensuales permiten comprobar la disponibilidad de las bombas y de las conexiones para el servicio de '
            'bomberos, la posición de las válvulas enclavadas, la presión del sistema, el estado de los dispositivos de descarga y '
            'el nivel del depósito de espumígeno.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Bombas contra incendio', 'inspeccionar el tipo de bomba y el registro de su última inspección, según el capítulo 12 de la '
                                   'IRAM 3546:2011.'),
        ('Conexiones para el servicio de bomberos', 'comprobar que están siempre accesibles, visibles y no obstruidas, y que sus '
                                                    'cubiertas o tapas están en su lugar, sin daños aparentes, limpias y '
                                                    'ligeramente lubricadas con grafito.'),
        ('Drenaje de las conexiones', 'en los lugares con riesgo de congelamiento, verificar que las conexiones se drenan a través '
                                      'de su válvula de goteo, ubicada delante de la válvula de retención.'),
        ('Válvulas de control enclavadas', 'comprobar que las válvulas enclavadas, incluidas las de poste indicador y las válvulas '
                                           'de calle, se encuentran abiertas.'),
        ('Manómetros', 'comprobar que las presiones se encuentran en sus valores normales y registrar las presiones del sistema.'),
        ('Dispositivos de descarga de espuma', 'verificar que no están dañados ni obstruidos y que no presentan ningún otro tipo de daño.'),
        ('Depósito de espumígeno', 'verificar que está lleno: el líquido debe llegar hasta **la mitad de la cúpula de expansión**.'),
        ('Instrucciones de operación', 'comprobar que se encuentran visibles.'),
    ]))
    a(('p', 'Toda condición que no cumpla se debe corregir y anotar en observaciones.'))
    a(('p', cierre(3)))

    a(('h4', 'Inspección anual'))
    a(('p', 'Las inspecciones anuales tienen como finalidad verificar el estado de conservación de las cámaras de espuma, de la red '
            'de tuberías, de sus soportes y de los manómetros del sistema.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Cámaras de espuma', 'comprobar que están libres de daños, que no se encuentran obstruidas y que sus sellos están intactos.'),
        ('Tuberías', 'comprobar que se encuentran en buen estado, sin daños mecánicos, sin corrosión, bien alineadas y no sometidas '
                     'a cargas externas.'),
        ('Soportes de tuberías', 'comprobar que no se encuentran dañados ni corroídos.'),
        ('Manómetros', 'comprobar que están en buen estado y que se mantiene el valor normal de la presión en el abastecimiento de agua.'),
    ]))
    a(('p', 'Las tuberías situadas en espacios cerrados, tales como falsos techos, no requieren la inspección anual.'))
    a(('p', cierre(4)))

    # ---------------- PRUEBA ----------------
    a(('h3', 'PRUEBA'))
    a(('p', 'Las pruebas consisten en verificaciones funcionales destinadas a comprobar el correcto funcionamiento de los equipos '
            'y dispositivos del sistema, y permiten detectar fallas operativas que no pueden observarse únicamente mediante '
            'inspección visual. Cuando durante las pruebas se detecten fallas o anomalías, se debe proceder inmediatamente a su '
            'reparación o mantenimiento.'))

    a(('h4', 'Prueba trimestral'))
    a(('p', 'Las pruebas trimestrales tienen como finalidad verificar el funcionamiento de la bomba de espumígeno y la correcta '
            'reposición del sistema a su condición de servicio.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Bomba de espumígeno', 'hacer funcionar la bomba, con el circuito de retorno o recirculación al depósito habilitado según el '
                                'diseño, y verificar que no hay pérdidas de espumígeno; en los sistemas cuya '
                                'actuación depende de ella, probar el sistema para verificar su correcto funcionamiento.'),
        REPOSICION,
    ]))
    a(('p', cierre(5)))

    a(('h4', 'Prueba semestral'))
    a(('p', 'Las pruebas semestrales permiten comprobar el funcionamiento del sistema de detección asociado y el estado del '
            'espumígeno almacenado y de las válvulas del depósito.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Sistema de detección', 'probar el sistema de detección para verificar su correcto funcionamiento, según el capítulo 6 de '
                                 'la IRAM 3546:2011, en los sistemas cuya actuación depende de él.'),
        ('Espumígeno del depósito', 'drenar aproximadamente **20 L** de espumígeno desde el fondo del depósito y verificar la '
                                    'presencia de sedimentos según el protocolo de ensayo.'),
        ('Válvulas del depósito de espumígeno', 'comprobar el estado de las válvulas instaladas en el depósito.'),
        REPOSICION,
    ]))
    a(('p', 'La planilla registra por separado, para el primer y el segundo semestre, la fecha y el inspector de las pruebas de '
            'detección, de emulsor espumígeno y de válvulas.'))
    a(('p', cierre(5)))
    a(('protocol', ('control de sedimentos en el depósito de espumígeno', [
        ('Extracción de la muestra', [
            ('Paso a paso', 'drenar aproximadamente **20 L** de espumígeno desde el fondo del depósito a través de su válvula de '
                            'drenaje, recogiéndolo en un recipiente limpio.'),
            ('Justificación técnica', 'el fondo del depósito es el punto donde se acumulan los sedimentos que pueden obstruir el '
                                      'proporcionador y alterar la dosificación.'),
            ('Criterio de aceptación', 'muestra extraída sin pérdidas de espumígeno.')]),
        ('Reposo y observación', [
            ('Paso a paso', 'dejar reposar el líquido durante varias horas y observar si se ha depositado algún sedimento en el '
                            'fondo del recipiente.'),
            ('Justificación técnica', 'permite determinar si el depósito tiene incrustaciones y, por lo tanto, debe ser limpiado.'),
            ('Criterio de aceptación', 'ausencia de sedimentos; si existen, se debe programar la limpieza del depósito y '
                                       'registrarlo en observaciones.')]),
        ('Devolución del espumígeno', [
            ('Paso a paso', 'devolver el líquido al depósito después de haberlo pasado por un filtro.'),
            ('Justificación técnica', 'se conserva la reserva de diseño sin introducir partículas en el depósito.'),
            ('Criterio de aceptación', 'depósito lleno hasta la mitad de la cúpula de expansión.')]),
    ])))

    a(('h4', 'Prueba anual'))
    a(('p', 'Las pruebas anuales tienen como finalidad verificar la calidad del espumígeno y de la espuma obtenida y el desempeño '
            'del sistema en una descarga real, comprobando la dosificación, los tiempos de respuesta y las presiones de funcionamiento.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Calidad del espumígeno', 'comprobar que no está deteriorado ni descompuesto, enviando una muestra al fabricante o al '
                                   'laboratorio de ensayo para que ensaye su calidad.'),
        ('Prueba funcional con descarga', 'realizar la descarga de espuma para verificar la dosificación, según el protocolo de ensayo.'),
        ('Calidad de la espuma obtenida', 'verificar la calidad de la espuma producida durante la descarga, mediante la relación de '
                                          'expansión y el tiempo de drenaje según el método y los valores del fabricante del espumígeno.'),
        ('Dosificación de espumígeno', 'verificar que la dosificación es como mínimo el **90 %** del valor mínimo de diseño.'),
        ('Mediciones resultantes', 'adjuntar las mediciones a la planilla o registrarlas en observaciones.'),
        REPOSICION,
    ]))
    a(('p', 'Para la verificación de la calidad del agente extintor se debe contar con procedimientos documentados en función de '
            'las normas de aplicación, según los requisitos generales de la IRAM 3546:2011.'))
    a(('p', cierre(6)))
    a(('protocol', ('prueba funcional de descarga del sistema', [
        ('Toma de la muestra de espumígeno', [
            ('Paso a paso', 'extraer una muestra de espumígeno en un frasco de medio litro, etiquetado con el nombre de la persona de '
                            'contacto, la localización del sistema, la dirección, el teléfono y la fecha de envío, y remitirla al '
                            'fabricante o al laboratorio de ensayo.'),
            ('Justificación técnica', 'un espumígeno deteriorado o descompuesto no genera una espuma eficaz, aunque el sistema '
                                      'descargue correctamente.'),
            ('Criterio de aceptación', 'informe del ensayo que confirme la aptitud del espumígeno, adjunto a la planilla.')]),
        ('Preparación de la descarga', [
            ('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo, coordinar con el usuario la descarga '
                            'y verificar que el área puede recibir y evacuar la espuma descargada; en los sistemas con cámaras de '
                            'espuma de tanques de almacenamiento de inflamables, la descarga se realiza por la conexión de prueba o '
                            'desviando la descarga fuera del tanque, según el diseño, para no contaminar el producto almacenado.'),
            ('Justificación técnica', 'la prueba implica una descarga real de espuma y debe realizarse sin afectar las actividades '
                                      'ni los equipos del entorno.'),
            ('Criterio de aceptación', 'notificación realizada y área preparada.')]),
        ('Accionamiento y tiempos', [
            ('Paso a paso', 'accionar el sistema y registrar con cronómetro los tiempos de respuesta y de descarga, en segundos.'),
            ('Justificación técnica', 'el tiempo de respuesta refleja el estado del accionamiento, de la válvula de control y del '
                                      'proporcionador.'),
            ('Criterio de aceptación', 'tiempos registrados y comparables con los de diseño o con los de la prueba anual anterior.')]),
        ('Presiones de funcionamiento', [
            ('Paso a paso', 'durante la descarga, registrar la presión en el dispositivo de descarga hidráulicamente más alejado y la '
                            'presión en la válvula de control principal.'),
            ('Justificación técnica', 'el dispositivo más alejado es el punto más desfavorable de la red; su presión demuestra que '
                                      'el sistema alcanza todo el riesgo protegido.'),
            ('Criterio de aceptación', 'presiones registradas y acordes con los cálculos hidráulicos del sistema.')]),
        ('Dosificación y calidad de la espuma', [
            ('Paso a paso', 'medir la concentración de la solución con refractómetro o conductímetro y curva patrón, determinar la relación '
                            'de expansión y el tiempo de drenaje de la espuma según el método del fabricante y registrar las mediciones.'),
            ('Justificación técnica', 'una dosificación insuficiente o una espuma de baja calidad reducen la capacidad de extinción '
                                      'y de sellado sobre el riesgo.'),
            ('Criterio de aceptación', 'dosificación no menor que el **90 %** del valor mínimo de diseño y calidad de espuma dentro de los valores '
                                       'del fabricante del espumígeno.')]),
        ('Restablecimiento', [
            ('Paso a paso', 'reponer todas las válvulas, interruptores y controles de funcionamiento a su posición normal y verificar '
                            'que el sistema queda en servicio.'),
            ('Justificación técnica', 'el sistema permanece fuera de servicio hasta su restablecimiento completo.'),
            ('Criterio de aceptación', 'sistema en servicio con todas las válvulas en su posición normal.')]),
    ])))

    # ---------------- MANTENIMIENTO ----------------
    a(('h3', 'MANTENIMIENTO'))
    a(('p', 'El mantenimiento comprende las tareas destinadas a conservar los equipos y componentes del sistema en condiciones '
            'adecuadas de funcionamiento y confiabilidad. Estas tareas deben realizarse inmediatamente después de detectar fallas '
            'durante las inspecciones o pruebas, y deben asegurar que todos los componentes y equipos que forman el sistema estén '
            'operativos y confiables.'))

    a(('h4', 'Mantenimiento trimestral'))
    a(('p', 'Las tareas de mantenimiento trimestral están orientadas a conservar la libre maniobra de las válvulas del sistema.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Operación de válvulas', 'operación de las válvulas en todo su recorrido y retorno a su posición normal, con nuevo precintado '
                                  'o enclavamiento cuando sea necesario.'),
    ]))
    a(('p', cierre(7)))

    a(('h4', 'Mantenimiento semestral'))
    a(('p', 'Las tareas de mantenimiento semestral permiten asegurar que el depósito de espumígeno conserve su condición de '
            'presión y vacío de diseño.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Válvula de presión-vacío', 'comprobación del estado de la válvula instalada en el depósito de espumígeno.'),
    ]))
    a(('p', cierre(7)))

    a(('h4', 'Mantenimiento anual'))
    a(('p', 'Las tareas de mantenimiento anual están orientadas a conservar la lubricación de las válvulas del sistema.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Lubricación de válvulas', 'lubricación de las válvulas del sistema.'),
    ]))
    a(('p', cierre(7)))

    # ---------------- COMPLEMENTARIAS ----------------
    a(('h3', 'PROCEDIMIENTO POSTERIOR A UNA DESCARGA O ACTUACIÓN'))
    a(('p', 'El procedimiento posterior a una descarga tiene como finalidad restablecer la disponibilidad operativa del sistema '
            'luego de la prueba funcional o de una actuación real.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Reposición de válvulas y controles', 'reposición de todas las válvulas, interruptores y controles de funcionamiento a su '
                                               'posición normal, con nuevo precintado o enclavamiento.'),
        ('Reserva de espumígeno', 'reposición del espumígeno consumido hasta la mitad de la cúpula de expansión del depósito.'),
        ('Lavado del circuito', 'lavado con agua del proporcionador y de las tuberías que conducen solución de espuma, según las '
                                'instrucciones del fabricante.'),
        ('Dispositivos de descarga', 'verificación de que las cámaras y los formadores de espuma no han quedado obstruidos y '
                                     'conservan sus sellos.'),
        ('Puesta en servicio', 'verificación de que la presión del sistema se encuentra en sus valores normales y de que el sistema '
                               'queda en servicio.'),
    ]))
    a(('p', cierre(6)))

    a(('h3', 'SEGURIDAD Y SALUD OCUPACIONAL'))
    a(('p', 'La seguridad del personal tiene como finalidad evitar que la manipulación del espumígeno y las descargas de espuma expongan a las personas a irritaciones, caídas o pérdida de visibilidad.'))
    a(('p', 'Durante las pruebas con descarga y las tareas posteriores se debe asegurar:'))
    a(('items', [('Elementos de protección personal', 'uso de guantes, protección ocular y ropa de trabajo según la hoja de datos de seguridad del espumígeno durante su manipulación, muestreo y reposición.'), ('Delimitación del área', 'señalización y delimitación de la zona de descarga y prohibición de permanecer dentro de ella durante la prueba, en especial cuando la espuma reduce la visibilidad o llena el recinto.'), ('Superficies resbaladizas', 'circulación restringida sobre superficies cubiertas de espuma hasta su limpieza.'), ('Disposición del efluente', 'recolección y disposición de la espuma descargada y del espumígeno drenado según la normativa ambiental aplicable.')]))
    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'Las modificaciones del sistema, del entorno o del uso del área protegida pueden afectar la eficacia de la protección. '
            'Toda modificación se debe evaluar técnicamente para determinar si se alteró el diseño original, y su existencia se '
            'debe registrar en la planilla de información general.'))
    a(('p', 'La empresa mantenedora es responsable de ejecutar las tareas de inspección, prueba y mantenimiento y de verificar las '
            'inspecciones de autocontrol. El usuario o propietario es responsable de completar las inspecciones de autocontrol, '
            'de mantener libre el acceso a las conexiones y a los dispositivos de descarga, y de no alterar las condiciones del '
            'área protegida sin evaluación técnica.'))
    return C


def REGISTRO_EXTRA(cierre):
    return [
        'Los datos de la instalación, del tipo de sistema, de las válvulas, del abastecimiento de agua, de las bombas, de la toma de '
        'impulsión para bomberos, del tanque de espumígeno y del dosificador deben registrarse en la planilla SG-PEM-IFI-%s-1 %s – '
        '%s, en la primera intervención y cada vez que se modifiquen.' % (SIG, NOM, PL[1]),
        'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '
        'codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables se indican con NA. Toda '
        'condición O o X se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y '
        'por el responsable de la instalación, con su aclaración.',
    ]
