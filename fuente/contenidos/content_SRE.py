# -*- coding: utf-8 -*-
SIG, NOM, NOMU, CAP = 'SRE', 'Sistema de Rociadores de Espuma', 'SISTEMA DE ROCIADORES DE ESPUMA', '9'
PL = {1: 'Información general', 2: 'Inspección semanal', 3: 'Inspección mensual', 4: 'Inspección anual',
      5: 'Inspección quinquenal', 6: 'Pruebas trimestral y semestral', 7: 'Prueba y mantenimiento anual'}

AVISO = ('Antes de realizar cualquier actividad de inspección o prueba que pueda generar alarmas o descargas, '
         'se deberá notificar previamente al responsable del sistema o al servicio de monitoreo correspondiente.')
REPOSICION = ('Reposición del sistema', 'comprobar que todas las válvulas, interruptores y controles de funcionamiento se '
              'reponen a su posición normal y que el sistema queda en servicio.')


def CONTENT(cierre):
    C = []; a = C.append
    a(('h2', NOMU))
    a(('basado', '(Basado en IRAM 3546:2011 – Capítulo %s; criterios complementarios: NFPA 25)' % CAP))
    a(('p', 'Este apartado establece los requisitos mínimos para la inspección, prueba y mantenimiento del sistema de rociadores '
            'de espuma, con el objetivo de asegurar que el sistema descargue la solución de espuma con la dosificación, la presión '
            'y el patrón de descarga previstos en las condiciones de diseño, en condiciones de emergencia.'))
    a(('p', 'La IRAM 3546:2011 es la base del presente procedimiento y fija sus frecuencias. El capítulo 11 de la NFPA 25, '
            'Sistemas de espuma, se aplica como criterio complementario para las tareas que la IRAM no contempla. Ante diferencias, se '
            'adopta siempre la condición más exigente. Se aplica la edición vigente de cada norma NFPA; la numeración de los artículos citados se debe confirmar en esa '
            'edición, porque puede variar entre ediciones.'))
    a(('p', 'El sistema de rociadores de espuma es una red de rociadores alimentada con una solución de agua y espumígeno, que se '
            'forma mediante un sistema proporcionador a partir del abastecimiento de agua y de la reserva de espumígeno. Su '
            'eficacia depende tanto de la integridad de la red y de los rociadores como de la calidad del espumígeno y de la '
            'correcta dosificación de la solución.'))
    a(('p', 'El equipamiento del sistema incluye:'))
    a(('items', [
        ('Abastecimiento de agua y bombas', 'fuente de agua y bombas contra incendio que proveen el caudal y la presión requeridos, '
                                            'cuyo mantenimiento se rige por los capítulos 13 y 12 de la IRAM 3546:2011.'),
        ('Válvulas de control', 'válvulas de poste indicador, válvulas de calle, válvulas de husillo ascendente y puente fijo y '
                                'válvulas de mariposa, precintadas, enclavadas o supervisadas.'),
        ('Válvulas de rociadores', 'válvulas de retención, de alarma, de diluvio, de preacción o similares, según el tipo de sistema.'),
        ('Reserva de espumígeno', 'tanque de espumígeno atmosférico o tanque de espumígeno a presión.'),
        ('Bomba de espumígeno', 'equipo que impulsa el espumígeno hacia el sistema proporcionador, cuando la instalación lo prevé.'),
        ('Sistema proporcionador', 'conjunto que dosifica el espumígeno en el agua para formar la solución de espuma.'),
        ('Red de tuberías', 'tuberías, dispositivos de anclaje y brazos sísmicos que conducen la solución hasta los rociadores.'),
        ('Rociadores de espuma', 'dispositivos que descargan la solución de espuma sobre el área protegida.'),
        ('Equipos auxiliares, tales como', ''),
        ['manómetros del sistema;',
         'dispositivos de alarma de flujo de agua y presostato;',
         'filtros;',
         'sistema de detección y dispositivos de actuación manual;',
         'toma de impulsión para bomberos.'],
    ]))
    a(('p', 'En los sistemas de accionamiento automático, el sistema de detección provoca el disparo de la válvula de control; el '
            'agua ingresa al sistema proporcionador, que incorpora el espumígeno en la proporción de diseño, y la solución de '
            'espuma se descarga a través de los rociadores. El sistema también puede accionarse en forma manual.'))
    a(('p', AVISO))

    # ---------------- INSPECCIÓN ----------------
    a(('h3', 'INSPECCIÓN'))
    a(('p', 'La inspección consiste en la verificación visual del sistema y de sus componentes, con el fin de comprobar que se '
            'encuentran en condiciones aparentemente óptimas de operación y libres de daños físicos. Se realiza generalmente en '
            'cada planta, recorriendo las zonas protegidas.'))
    a(('p', 'Las inspecciones de frecuencia menor a un mes pueden ser completadas por el usuario de la instalación como '
            'inspecciones de autocontrol, y se deben identificar como tales; el mantenedor debe verificar su correcto cumplimiento, '
            'dejando constancia de los hallazgos.'))
    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica '
            'previa de la instalación según la IRAM 3619, para verificar su grado de cumplimiento con las normas y la legislación '
            'vigente; esta evaluación no es obligatoria y puede ser solicitada por cualquiera de las partes interesadas.'))
    a(('p', 'De acuerdo con los requisitos generales de la IRAM 3546:2011, cuando el sistema sea de cañería seca, a excepción de '
            'los sistemas de acción previa, o se abastezca de agua por gravedad o en forma directa desde la red pública o privada, '
            'las tareas con periodicidad menor a trimestral se deben realizar trimestralmente.'))

    a(('h4', 'Inspección semanal (autocontrol)'))
    a(('p', 'Las inspecciones semanales tienen como finalidad verificar que las válvulas de control se mantienen abiertas y '
            'precintadas y que los rociadores de espuma se encuentran en condiciones de descargar sin interferencias.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Válvulas de control', 'comprobar que las válvulas selladas o precintadas, incluidas las de poste indicador y las válvulas '
                                'de calle, se encuentran abiertas.'),
        ('Precintos', 'verificar que las válvulas están precintadas; si no lo están, se deben volver a precintar y dejar constancia '
                      'en observaciones.'),
        ('Rociadores de espuma', 'comprobar que no están dañados ni bloqueados y que no presentan ningún otro tipo de problema.'),
        ('Espacio libre bajo los rociadores', 'verificar que se mantiene una distancia libre de **46 cm** por debajo de los '
                                              'rociadores; en caso contrario, indicarlo en observaciones.'),
        ('Cubiertas o tapas', 'comprobar que, si existen, se encuentran en su lugar y listas para funcionar cuando sea necesario.'),
    ]))
    a(('p', cierre(2)))

    a(('h4', 'Inspección mensual'))
    a(('p', 'Las inspecciones mensuales permiten comprobar la disponibilidad de las conexiones para el servicio de bomberos, la '
            'posición de las válvulas enclavadas, el estado de los dispositivos de alarma y la presión del sistema.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Conexiones para el servicio de bomberos', 'comprobar que están siempre accesibles, visibles y no obstruidas, y que sus '
                                                    'cubiertas o tapas están en su lugar, sin daños aparentes, limpias y '
                                                    'ligeramente lubricadas con grafito.'),
        ('Drenaje de las conexiones', 'en los lugares con riesgo de congelamiento, verificar que las conexiones se drenan a través '
                                      'de su válvula de goteo, ubicada delante de la válvula de retención.'),
        ('Válvulas de control enclavadas', 'comprobar que las válvulas enclavadas, incluidas las de poste indicador y las válvulas '
                                           'de calle, se encuentran abiertas.'),
        ('Dispositivos de alarma', 'verificar que no presentan daños físicos y que sus conexiones eléctricas son correctas.'),
        ('Manómetros', 'comprobar que las presiones del sistema se encuentran en sus valores normales.'),
        ('Presiones del sistema', 'registrar la presión del agua en la planilla.'),
        ('Instrucciones de operación', 'comprobar que se encuentran visibles.'),
    ]))
    a(('p', 'Si la presión del agua registrada presenta una diferencia mayor que el **10 %**, se debe investigar la causa, evaluar '
            'su impacto en la operación del sistema y describirlo brevemente en observaciones. Toda condición que no cumpla se '
            'debe corregir y anotar en observaciones.'))
    a(('p', cierre(3)))

    a(('h4', 'Inspección anual'))
    a(('p', 'Las inspecciones anuales tienen como finalidad verificar el estado de conservación de los rociadores, de la red de '
            'tuberías, de sus anclajes y de los manómetros del sistema.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Rociadores de espuma', 'comprobar que están libres de:'),
        ['corrosión;', 'obstrucción de sus boquillas;', 'materiales extraños;', 'daños físicos.'],
        ('Posición de los rociadores', 'verificar la posición y la ubicación de los rociadores.'),
        ('Tuberías de rociadores', 'comprobar que se encuentran:'),
        ['en buen estado;', 'sin daños mecánicos;', 'sin corrosión;', 'bien alineadas;', 'no sometidas a cargas externas.'],
        ('Dispositivos de anclaje y brazos sísmicos', 'comprobar que no están dañados ni presentan corrosión.'),
        ('Manómetros', 'comprobar que están en buen estado y que se mantiene el valor normal de la presión de abastecimiento de agua.'),
    ]))
    a(('p', 'Las tuberías y los dispositivos de anclaje situados en espacios cerrados, tales como falsos techos, no requieren la '
            'inspección anual.'))
    a(('p', cierre(4)))

    a(('h4', 'Inspección quinquenal'))
    a(('p', 'Las inspecciones quinquenales están orientadas a verificar el estado interno de las válvulas, de los filtros y de '
            'los equipos de almacenamiento, impulsión y dosificación del espumígeno.'))
    a(('p', 'Cada cinco años se debe realizar:'))
    a(('items', [
        ('Válvulas de retención', 'inspeccionar internamente todas las válvulas y verificar que sus componentes funcionan '
                                  'adecuadamente, se mueven libremente y están en buen estado; cada válvula se debe enumerar en '
                                  'observaciones.'),
        ('Válvulas de alarma', 'inspeccionarlas internamente y verificar que todos sus componentes operan adecuadamente.'),
        ('Válvulas de diluvio, de preacción o similares', 'inspeccionarlas internamente y verificar que todos sus componentes '
                                                          'operan adecuadamente.'),
        ('Filtros', 'realizar la inspección interna de todos los filtros existentes.'),
        ('Bombas de espumígeno', 'realizar la revisión completa de la bomba, de su impulsor y de sus accesorios, según las '
                                 'instrucciones del fabricante.'),
        ('Sistemas proporcionadores', 'realizar la revisión completa según las instrucciones del fabricante.'),
        ('Tanque de espumígeno', 'realizar su vaciado y limpieza y verificar internamente la presencia de corrosión.'),
        ('Tanque de espumígeno a presión', 'realizar las mismas tareas que en el tanque atmosférico y, además, la prueba '
                                           'hidrostática a **1,5 veces** la presión de diseño; la planilla de la norma indica 1,5 veces la presión de trabajo, por lo '
                                           'que se debe adoptar la condición más exigente.'),
    ]))
    a(('p', 'La prueba hidrostática se debe ejecutar conforme a procedimientos documentados en función de las normas de aplicación, '
            'según los requisitos generales de la IRAM 3546:2011.'))
    a(('p', cierre(5)))

    a(('h4', 'Inspección interna por obstrucción de tuberías'))
    a(('p', 'La inspección interna de la red tiene como finalidad asegurar que el sistema de rociadores se mantenga libre de '
            'obstrucciones. Se debe realizar inmediatamente cuando se presente alguna de las situaciones desfavorables que se '
            'indican a continuación y, a partir de ese momento, periódicamente cada **cinco años**.'))
    a(('p', 'Son situaciones desfavorables que obligan a la inspección interna:'))
    a(('items', [
        ('Filtros de la toma de la bomba', 'funcionamiento defectuoso de los filtros cuando la bomba aspira de ríos, pozos o lagos, '
                                           'que puede permitir la entrada de residuos en la aspiración y en las tuberías.'),
        ('Materiales en la descarga', 'presencia de materiales que obstruyen la descarga durante las pruebas rutinarias de '
                                      'funcionamiento, tales como las pruebas de flujo de agua en los rociadores.'),
        ('Residuos en el mantenimiento', 'presencia de residuos durante el mantenimiento de válvulas y tubería seca, de válvulas de '
                                         'retención y de bombas contra incendio.'),
        ('Coloración del agua', 'fuerte coloración del agua durante la prueba de drenaje con la tubería de 50 mm o en la descarga '
                                'de la conexión de prueba de inspección.'),
        ('Atasco de tuberías', 'atascos producidos por modificaciones del sistema o como consecuencia de una falla del sistema '
                               'durante un incendio.'),
        ('Limpieza de tuberías enterradas', 'falla durante la limpieza de tuberías enterradas después de su instalación o '
                                            'reparación, por residuos que quedaron en su interior durante la manipulación.'),
        ('Rotura de tuberías principales', 'rotura de tuberías principales en el área, cuya reparación puede introducir residuos '
                                           'en el sistema.'),
    ]))
    a(('p', cierre(5)))

    # ---------------- PRUEBA ----------------
    a(('h3', 'PRUEBA'))
    a(('p', 'Las pruebas consisten en verificaciones funcionales destinadas a comprobar el correcto funcionamiento de los equipos '
            'y dispositivos del sistema, y permiten detectar fallas operativas que no pueden observarse únicamente mediante '
            'inspección visual. Cuando durante las pruebas se detecten fallas o anomalías, se debe proceder inmediatamente a su '
            'reparación o mantenimiento.'))

    a(('h4', 'Prueba trimestral'))
    a(('p', 'Las pruebas trimestrales tienen como finalidad verificar la disponibilidad del abastecimiento de agua, la actuación '
            'de las alarmas de flujo, la libre maniobra de las válvulas y el funcionamiento de la bomba de espumígeno.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Prueba de caudal con el drenaje principal', 'registrar la presión estática y la presión residual del abastecimiento de '
                                                      'agua según el protocolo de ensayo; en los sistemas con válvulas de '
                                                      'rociadores de diluvio, la prueba se realiza con la tubería de drenaje de '
                                                      '**50 mm**.'),
        ('Daños por la descarga', 'comprobar que el caudal de agua de la prueba no daña la instalación.'),
        ('Alarmas de flujo de agua', 'probar las alarmas abriendo el bypass de conexión, de modo que el agua fluya desde la parte '
                                     'baja de la válvula de diluvio hasta el presostato, simulando la circulación de agua a '
                                     'través de la válvula.'),
        ('Válvulas de corte', 'abrir las válvulas hasta que se note tensión en el vástago de accionamiento y girarlas **un cuarto '
                              'de vuelta** para prevenir agarrotamientos.'),
        ('Operación de válvulas', 'operar las válvulas abriéndolas y cerrándolas totalmente y reponer los precintos.'),
        ('Bomba de espumígeno', 'si existe, hacerla funcionar durante **20 s a 30 s**, con el circuito de retorno o recirculación al '
                                'depósito habilitado según el diseño, y verificar que no hay pérdidas de espumígeno.'),
        REPOSICION,
    ]))
    a(('p', 'En los sistemas de rociadores de espuma no es posible utilizar la conexión de prueba de inspección para probar las '
            'alarmas, ya que los rociadores están abiertos. No requieren la prueba trimestral de maniobra las válvulas de husillo '
            'ascendente y puente fijo ni las de mariposa accionadas mediante engranajes con indicador.'))
    a(('p', cierre(6)))
    a(('protocol', ('prueba de caudal con el drenaje principal', [
        ('Lectura de la presión estática', [
            ('Paso a paso', 'con el sistema en reposo, registrar la presión indicada por el manómetro situado en la parte baja de la '
                            'válvula de rociadores; esta lectura corresponde a la presión estática del abastecimiento de agua.'),
            ('Justificación técnica', 'la presión estática es la referencia para evaluar el estado del abastecimiento y debe '
                                      'compararse con las lecturas anteriores registradas.'),
            ('Criterio de aceptación', 'lectura registrada y comparable con las pruebas anteriores.')]),
        ('Apertura del drenaje y presión residual', [
            ('Paso a paso', 'abrir totalmente la válvula de drenaje principal, o la de **50 mm** en sistemas con válvulas de '
                            'diluvio, dejar que el flujo se estabilice y registrar nuevamente la presión en el mismo manómetro; '
                            'esta lectura corresponde a la presión residual del abastecimiento de agua.'),
            ('Justificación técnica', 'una variación significativa respecto de las lecturas anteriores indica un problema en el '
                                      'abastecimiento, tal como una válvula cerrada o una obstrucción de la tubería.'),
            ('Criterio de aceptación', 'las pérdidas de presión mayores que un **10 %** respecto de las lecturas anteriores se deben '
                                       'investigar inmediatamente, determinar su causa y corregir antes de dar por finalizada la prueba.')]),
        ('Cierre del drenaje', [
            ('Paso a paso', 'cerrar lentamente la válvula de drenaje y verificar que la presión del sistema retorna a su valor normal.'),
            ('Justificación técnica', 'el cierre lento evita golpes de ariete sobre la red y los accesorios.'),
            ('Criterio de aceptación', 'drenaje cerrado y presión del sistema en su valor normal.')]),
        ('Verificación de los datos de diseño', [
            ('Paso a paso', 'comprobar que la presión original de diseño del abastecimiento de agua está anotada y grabada en la '
                            'válvula de rociadores y que, en los sistemas calculados hidráulicamente, la válvula tiene sujeta una '
                            'etiqueta con los criterios de diseño.'),
            ('Justificación técnica', 'el dato de diseño permite determinar si la caída de presión observada afecta el '
                                      'funcionamiento de los rociadores.'),
            ('Criterio de aceptación', 'presión de diseño y etiqueta presentes y legibles.')]),
    ])))

    a(('h4', 'Prueba semestral'))
    a(('p', 'Las pruebas semestrales permiten comprobar el disparo de las válvulas de control y el funcionamiento del sistema de '
            'detección sin producir descarga de espuma, así como el estado del depósito de espumígeno.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Disparo de la válvula de control', 'probar el disparo de las válvulas de control sin producir la descarga de espuma, '
                                             'cerrando las válvulas de abastecimiento de agua y de espumígeno y siguiendo las '
                                             'instrucciones del fabricante instalador para cada sistema.'),
        ('Sistema de disparo', 'probar el disparo a través del sistema de detección automática o de la actuación manual; la prueba '
                               'no requiere flujo de agua a través del sistema.'),
        ('Sistema de detección', 'probar su correcto funcionamiento según el capítulo 6 de la IRAM 3546:2011.'),
        ('Espumígeno del depósito', 'drenar aproximadamente **20 L** de espumígeno desde el fondo del depósito y verificar la '
                                    'presencia de incrustaciones según el protocolo de ensayo.'),
        ('Válvula del depósito de espumígeno', 'comprobar el estado de la válvula instalada en el depósito.'),
        REPOSICION,
    ]))
    a(('p', 'Si se detectan fallas, se deben reparar y anotar en observaciones.'))
    a(('p', cierre(6)))
    a(('protocol', ('disparo de la válvula de control sin descarga de espuma', [
        ('Aislamiento de los circuitos', [
            ('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo, cerrar las válvulas de abastecimiento de '
                            'agua y de espumígeno según las instrucciones del fabricante instalador y registrar su posición.'),
            ('Justificación técnica', 'permite verificar la actuación de la válvula de control sin consumir espumígeno ni descargar '
                                      'espuma sobre el área protegida.'),
            ('Criterio de aceptación', 'ambos circuitos cerrados e identificados, sin posibilidad de descarga.')]),
        ('Disparo', [
            ('Paso a paso', 'provocar el disparo mediante el sistema de detección automática o la actuación manual y observar la '
                            'actuación de la válvula de control y de las alarmas asociadas.'),
            ('Justificación técnica', 'comprueba la cadena completa de disparo, desde la detección hasta la válvula de control.'),
            ('Criterio de aceptación', 'la válvula de control actúa ante la orden de disparo.')]),
        ('Rearme y reapertura', [
            ('Paso a paso', 'rearmar la válvula de control según el fabricante, drenar el agua remanente y reabrir lentamente las '
                            'válvulas de abastecimiento de agua y de espumígeno, volviendo a precintarlas.'),
            ('Justificación técnica', 'una válvula de abastecimiento cerrada anula la protección aunque el disparo funcione.'),
            ('Criterio de aceptación', 'válvula rearmada, circuitos de agua y espumígeno abiertos y precintados, y sistema en servicio.')]),
    ])))
    a(('protocol', ('control de sedimentos en el depósito de espumígeno', [
        ('Extracción de la muestra', [
            ('Paso a paso', 'drenar aproximadamente **20 L** de espumígeno desde el fondo del depósito a través de su válvula de '
                            'drenaje, recogiéndolo en un recipiente limpio.'),
            ('Justificación técnica', 'el fondo del depósito es el punto donde se acumulan los sedimentos e incrustaciones que '
                                      'pueden obstruir el sistema proporcionador.'),
            ('Criterio de aceptación', 'muestra extraída sin pérdidas de espumígeno.')]),
        ('Reposo y observación', [
            ('Paso a paso', 'dejar reposar el líquido durante varias horas y observar si se han depositado incrustaciones en el '
                            'fondo del recipiente.'),
            ('Justificación técnica', 'permite determinar si el depósito tiene incrustaciones y, por lo tanto, debe ser limpiado.'),
            ('Criterio de aceptación', 'ausencia de incrustaciones; si existen, se debe programar la limpieza del depósito y '
                                       'registrarlo en observaciones.')]),
        ('Devolución del espumígeno', [
            ('Paso a paso', 'devolver el líquido al depósito después de haberlo pasado por un filtro y comprobar el estado de la '
                            'válvula del depósito.'),
            ('Justificación técnica', 'se conserva la reserva de espumígeno de diseño sin introducir partículas en el depósito.'),
            ('Criterio de aceptación', 'depósito en su nivel normal y válvula en condiciones.')]),
    ])))

    a(('h4', 'Prueba anual'))
    a(('p', 'Las pruebas anuales tienen como finalidad verificar la calidad del espumígeno y el desempeño del sistema en una '
            'descarga real de espuma, comprobando la dosificación, los tiempos de respuesta y las presiones de funcionamiento.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Calidad del espumígeno', 'comprobar que no está deteriorado ni descompuesto, enviando una muestra al fabricante para que '
                                   'ensaye su calidad; el informe del fabricante se debe adjuntar a la planilla.'),
        ('Prueba funcional de descarga', 'realizar la descarga de espuma para verificar la dosificación, según el protocolo de ensayo.'),
        ('Patrón de descarga', 'verificar que la descarga de los rociadores es correcta en dirección y patrón.'),
        ('Dosificación de espumígeno', 'verificar que la dosificación es como mínimo el **90 %** del valor mínimo de diseño.'),
        REPOSICION,
    ]))
    a(('p', 'Para la verificación de la calidad del agente extintor se debe contar con procedimientos documentados en función de '
            'las normas de aplicación, según los requisitos generales de la IRAM 3546:2011.'))
    a(('p', cierre(7)))
    a(('protocol', ('prueba funcional de descarga del sistema', [
        ('Toma de la muestra de espumígeno', [
            ('Paso a paso', 'extraer una muestra de espumígeno en un frasco de medio litro, etiquetado con el nombre de la persona de '
                            'contacto, la localización del sistema, la dirección, el teléfono y la fecha de envío, y remitirla al '
                            'fabricante para su análisis.'),
            ('Justificación técnica', 'un espumígeno deteriorado o descompuesto no forma una espuma eficaz, aunque el sistema '
                                      'descargue correctamente.'),
            ('Criterio de aceptación', 'informe del fabricante que confirme la aptitud del espumígeno, adjunto a la planilla.')]),
        ('Preparación de la descarga', [
            ('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo, coordinar con el usuario la descarga '
                            'sobre el área protegida y verificar que el área puede recibir y evacuar la espuma descargada.'),
            ('Justificación técnica', 'la prueba implica una descarga real de espuma y debe realizarse sin afectar las actividades '
                                      'ni los equipos del entorno.'),
            ('Criterio de aceptación', 'notificación realizada y área preparada.')]),
        ('Accionamiento y tiempos', [
            ('Paso a paso', 'accionar el sistema y registrar con cronómetro el tiempo de respuesta del sistema proporcionador y el '
                            'tiempo de descarga, en segundos.'),
            ('Justificación técnica', 'el tiempo de respuesta refleja el estado del disparo, de la válvula de control y del sistema '
                                      'proporcionador.'),
            ('Criterio de aceptación', 'tiempos registrados y comparables con los de diseño o con los de la prueba anual anterior.')]),
        ('Presiones de funcionamiento', [
            ('Paso a paso', 'durante la descarga, registrar la presión en el rociador hidráulicamente más alejado y la presión en la '
                            'válvula de control principal, en bar.'),
            ('Justificación técnica', 'el rociador más alejado es el punto más desfavorable de la red; su presión demuestra que el '
                                      'sistema alcanza todo el área protegida.'),
            ('Criterio de aceptación', 'presiones registradas y acordes con los cálculos hidráulicos del sistema.')]),
        ('Dosificación y patrón de descarga', [
            ('Paso a paso', 'medir la concentración de la solución de espuma con refractómetro o conductímetro y curva patrón, según el '
                            'método indicado por el fabricante del espumígeno, y observar la dirección y el patrón de descarga de '
                            'los rociadores.'),
            ('Justificación técnica', 'una dosificación insuficiente reduce la capacidad de extinción y de sellado de la espuma.'),
            ('Criterio de aceptación', 'dosificación no menor que el **90 %** de la dosificación mínima de diseño y descarga correcta '
                                       'en dirección y patrón.')]),
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
            'durante las inspecciones o pruebas. En este sistema, la IRAM 3546:2011 integra las tareas de mantenimiento en el '
            'programa anual de pruebas.'))

    a(('h4', 'Mantenimiento anual'))
    a(('p', 'Las tareas de mantenimiento anual están orientadas a conservar la libre maniobra y la lubricación de las válvulas y el '
            'estado de las válvulas de retención del circuito de espumígeno.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Operación de válvulas de poste indicador y de husillo ascendente', 'cierre total de cada válvula y nueva apertura; al '
            'abrirla, giro del volante hasta notar resistencia en el vástago, para asegurar que no se ha separado de la compuerta, y '
            'retroceso de **un cuarto de vuelta** desde la apertura total para prevenir agarrotamientos.'),
        ('Válvulas de corte', 'operación de cada válvula en todo su recorrido, retorno a su posición normal y nuevo precintado o '
                              'enclavamiento.'),
        ('Lubricación de vástagos', 'aplicación de grafito o de grafito con aceite liviano en todos los vástagos, con cierre y '
                                    'apertura total de cada válvula para redistribuir el lubricante.'),
        ('Válvulas de retención en la aspiración de espumígeno', 'revisión interna para verificar que operan correctamente.'),
    ]))
    a(('p', cierre(7)))

    # ---------------- COMPLEMENTARIAS ----------------
    a(('h3', 'CRITERIOS COMPLEMENTARIOS DE LA NFPA 25'))
    a(('p', 'Los criterios complementarios tienen como finalidad incorporar las tareas del capítulo 11 de la NFPA 25 que la '
            'IRAM 3546:2011 no contempla.'))
    a(('p', 'Se debe asegurar:'))
    a(('items', [
        ('Sin descarga involuntaria', 'toda inspección y prueba se realiza sin descargar en forma involuntaria solución de espuma en '
                                      'las cañerías del sistema (11.1.1.3).'),
        ('Compatibilidad', 'si se detecta que el espumígeno o los componentes fueron cambiados y no son compatibles entre sí, el '
                           'sistema se considera fuera de servicio (11.1.7); se verifica además que no se hayan sustituido '
                           'combinaciones no listadas de dispositivos de descarga y espumígeno (11.2.4.1.4).'),
        ('Drenaje del área', 'inspección trimestral del área bajo el sistema y a su alrededor, para verificar que los drenajes no '
                             'están obstruidos y que los muros de contención están en buen estado (11.2.7 y Tabla 11.1.1.2).'),
        ('Sistema proporcionador', 'inspección mensual de la posición de las válvulas del sistema proporcionador según las '
                                   'condiciones de operación especificadas (11.2.8 y Tabla 11.1.1.2) y prueba operativa anual del '
                                   'proporcionador; con aprobación de la autoridad competente se admiten líquidos sustitutos del '
                                   'espumígeno (11.3.2).'),
        ('Reserva de espumígeno', 'verificación anual de que la cantidad de espumígeno satisface el diseño original e inspección del '
                                  'tanque de almacenamiento para detectar corrosión externa y daños (11.2.9).'),
        ('Análisis del espumígeno', 'envío anual de muestras al fabricante o a un laboratorio aprobado para verificar que cumple las '
                                    'especificaciones del fabricante (11.3.1).'),
        ('Filtros', 'inspección de los filtros de los dispositivos de descarga después de cada activación, de cada prueba operativa '
                    'y de cada lavado, y limpieza después de cada uso (11.2.6).'),
        ('Prueba operativa', 'prueba anual de los dispositivos de descarga, que debe demostrar que el sistema responde según el '
                             'diseño en forma automática y manual, tomando precauciones para no dañar bienes; donde la descarga sea '
                             'peligrosa, se admite un método alternativo aprobado (11.3.10).'),
        ('Recipientes del espumígeno', 'prueba hidrostática de los tanques de proporcionador de presión estándar y de vejiga según la '
                                       'Tabla 11.1.1.2, sin crear diferencia de presión a través de la vejiga (11.3.5); vaciado y '
                                       'lavado del tanque de almacenamiento metálico cuando haya sedimento excesivo (11.4.3.1).'),
    ]))
    a(('p', 'Estas tareas se registran como tareas complementarias en la planilla de la frecuencia correspondiente, conforme al '
            'requisito general de la IRAM 3546:2011 que admite el agregado de tareas a las planillas.'))

    a(('h3', 'PROCEDIMIENTO POSTERIOR A UNA DESCARGA O ACTUACIÓN'))
    a(('p', 'El procedimiento posterior a una descarga tiene como finalidad restablecer la disponibilidad operativa del sistema '
            'luego de la prueba funcional de descarga o de una actuación real.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Reposición de válvulas y controles', 'reposición de todas las válvulas, interruptores y controles de funcionamiento a su '
                                               'posición normal, con nuevo precintado o enclavamiento.'),
        ('Reserva de espumígeno', 'reposición del espumígeno consumido hasta el nivel de diseño del depósito.'),
        ('Lavado del circuito', 'lavado con agua del sistema proporcionador y de las tuberías que conducen solución de espuma, '
                                'según las instrucciones del fabricante.'),
        ('Filtros', 'inspección y limpieza de los filtros.'),
        ('Puesta en servicio', 'verificación de que la presión del sistema se encuentra en sus valores normales y de que el sistema '
                               'queda en servicio.'),
    ]))
    a(('p', cierre(7)))

    a(('h3', 'SEGURIDAD Y SALUD OCUPACIONAL'))
    a(('p', 'La seguridad del personal tiene como finalidad evitar que la manipulación del espumígeno y las descargas de espuma expongan a las personas a irritaciones, caídas o pérdida de visibilidad.'))
    a(('p', 'Durante las pruebas con descarga y las tareas posteriores se debe asegurar:'))
    a(('items', [('Elementos de protección personal', 'uso de guantes, protección ocular y ropa de trabajo según la hoja de datos de seguridad del espumígeno durante su manipulación, muestreo y reposición.'), ('Delimitación del área', 'señalización y delimitación de la zona de descarga y prohibición de permanecer dentro de ella durante la prueba.'), ('Superficies resbaladizas', 'circulación restringida sobre superficies cubiertas de espuma hasta su limpieza.'), ('Disposición del efluente', 'recolección y disposición de la espuma descargada y del espumígeno drenado según la normativa ambiental aplicable.')]))
    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'Las modificaciones del sistema, del entorno o del uso del área protegida pueden afectar la eficacia de la protección. '
            'Toda modificación se debe evaluar técnicamente antes de su ejecución y su existencia se debe registrar en la planilla '
            'de información general.'))
    a(('p', 'La empresa mantenedora es responsable de ejecutar las tareas de inspección, prueba y mantenimiento y de verificar las '
            'inspecciones de autocontrol. El usuario o propietario es responsable de completar las inspecciones de autocontrol, '
            'de mantener libres el espacio bajo los rociadores y el acceso a las conexiones, y de no alterar las condiciones del '
            'área protegida sin evaluación técnica.'))
    return C


def REGISTRO_EXTRA(cierre):
    return [
        'Los datos de la instalación, de las válvulas, del abastecimiento de agua, de las bombas, de la toma de impulsión para '
        'bomberos y de las instrucciones de operación deben registrarse en la planilla SG-PEM-IFI-%s-1 %s – %s, en la primera '
        'intervención y cada vez que se modifiquen.' % (SIG, NOM, PL[1]),
        'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '
        'codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables se indican con NA. Toda '
        'condición O o X se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y '
        'por el responsable de la instalación, con su aclaración.',
    ]
