# -*- coding: utf-8 -*-
SIG, NOM, NOMU, CAP = 'SAP', 'Sistema de Agua Pulverizada', 'SISTEMA DE AGUA PULVERIZADA', '8'
PL = {1: 'Información general', 2: 'Inspección semanal', 3: 'Inspección y pruebas mensual-trimestral',
      4: 'Inspección y pruebas anuales', 5: 'Inspección y pruebas semestrales'}
AVISO = ('Antes de realizar cualquier actividad de inspección o prueba que pueda generar alarmas o descargas, '
         'se deberá notificar previamente al responsable del sistema o al servicio de monitoreo correspondiente.')


def CONTENT(cierre):
    C = []
    a = C.append
    a(('h2', NOMU))
    a(('basado', '(Basado en IRAM 3546:2011 – Capítulo %s; criterios complementarios: NFPA 25 y NFPA 15)' % CAP))
    a(('p', 'Este apartado establece los requisitos mínimos para la inspección, prueba y mantenimiento del sistema de agua '
            'pulverizada, con el objetivo de asegurar que el sistema aplique agua finamente dividida sobre los elementos '
            'protegidos, con el caudal y la cobertura previstos en las condiciones de diseño, en condiciones de emergencia.'))
    a(('p', 'La IRAM 3546:2011 es la base del presente procedimiento y fija sus frecuencias. La NFPA 15, Norma para sistemas fijos '
            'de agua pulverizada para protección contra incendios, remite la inspección, prueba y mantenimiento a la NFPA 25 y, para '
            'la detección, a la NFPA 72 (NFPA 15, 11.1.1); el capítulo 10 de la NFPA 25 se aplica como criterio complementario. Ante '
            'diferencias, se adopta siempre la condición más exigente. Se aplica la edición vigente de cada norma NFPA; la numeración de los artículos citados se debe confirmar en esa '
            'edición, porque puede variar entre ediciones.'))
    a(('p', 'El sistema de agua pulverizada aplica el agua sobre los elementos a proteger finamente dividida en gotas de tamaño '
            'muy pequeño. Su utilización está orientada a la protección de riesgos que necesitan grandes cantidades de agua para '
            'su refrigeración, tales como líquidos y gases inflamables, sus depósitos y sus elementos estructurales, y también '
            'se emplea en la protección de transformadores eléctricos.'))
    a(('p', 'Su aplicación se realiza normalmente mediante sistemas tipo diluvio con cañerías secas, y la instalación puede '
            'accionarse en forma automática o manual. Dado que la descarga se produce en forma simultánea por todas las boquillas '
            'del sector protegido, la disponibilidad operativa de la válvula de diluvio, del abastecimiento de agua y de la red de '
            'cañerías resulta determinante para la confiabilidad del sistema.'))
    a(('p', 'El equipamiento del sistema incluye:'))
    a(('items', [
        ('Abastecimiento de agua', 'reserva de agua sin presión o reserva presurizada (tanque hidroneumático) y, cuando corresponde, '
                                   'bombas contra incendio que proveen el caudal y la presión requeridos.'),
        ('Sistema de presurización', 'equipo de aire comprimido, de nitrógeno o bomba centrífuga que mantiene la presión del sistema '
                                     'en sus valores normales.'),
        ('Válvula de diluvio', 'válvula de control que, al actuar, habilita el paso de agua hacia la red de cañerías secas y las boquillas.'),
        ('Válvulas de control y de corte', 'válvulas de husillo ascendente y puente fijo, de poste indicador y demás válvulas de '
                                           'seccionamiento, precintadas, enclavadas o supervisadas.'),
        ('Red de cañerías y soportes', 'tuberías, accesorios y elementos de sujeción que conducen el agua hasta las boquillas.'),
        ('Boquillas pulverizadoras', 'dispositivos que fraccionan el agua en gotas y la distribuyen sobre el elemento protegido.'),
        ('Sistema de detección y accionamiento', 'detección neumática, eléctrica u otra, y dispositivos manuales de disparo que provocan '
                                                 'la apertura de la válvula de diluvio.'),
        ('Equipos auxiliares, tales como', ''),
        ['manómetros del sistema y del sistema de presurización;',
         'alarma de flujo de agua y válvula de derivación (bypass) de la alarma;',
         'filtros y drenajes del sistema;',
         'válvula de llenado, válvula reductora y válvulas de seguridad de sistemas hidroneumáticos;',
         'toma de impulsión para bomberos.'],
    ]))
    a(('p', 'En los sistemas de accionamiento automático, el sistema de detección asociado identifica la condición de incendio y '
            'provoca la apertura de la válvula de diluvio por medios neumáticos, eléctricos u otros. Al abrirse la válvula, el agua '
            'ingresa en la red de cañerías secas, se activa la alarma de flujo de agua y se produce la descarga simultánea por todas '
            'las boquillas del área protegida.'))
    a(('p', 'El sistema también puede accionarse en forma manual mediante los dispositivos de disparo previstos. Una vez finalizada '
            'la descarga, el sistema debe ser restablecido por personal competente según lo indicado en el apartado correspondiente '
            'al procedimiento posterior a una descarga o actuación.'))
    a(('p', AVISO))

    # ---------------- INSPECCIÓN ----------------
    a(('h3', 'INSPECCIÓN'))
    a(('p', 'La inspección consiste en la verificación visual del sistema y de sus componentes, con el fin de comprobar que se '
            'encuentran en condiciones aparentes de funcionamiento, sin daños físicos, obstrucciones o alteraciones que puedan '
            'afectar su operatividad. Se realiza generalmente en cada planta, recorriendo las zonas protegidas.'))
    a(('p', 'Las inspecciones de frecuencia menor a un mes pueden ser completadas por el usuario de la instalación como '
            'inspecciones de autocontrol, y se deben identificar como tales; el mantenedor debe verificar su correcto cumplimiento, '
            'dejando constancia de los hallazgos.'))
    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica '
            'previa de la instalación según la IRAM 3619, para verificar su grado de cumplimiento con las normas y la legislación '
            'vigente; esta evaluación no es obligatoria y puede ser solicitada por cualquiera de las partes interesadas.'))
    a(('p', 'De acuerdo con los requisitos generales de la IRAM 3546:2011, en las instalaciones a base de agua con cañería seca, a '
            'excepción de los sistemas de acción previa, en las abastecidas de agua por gravedad y en las abastecidas en forma '
            'directa desde la red pública o privada, las tareas con periodicidad menor a trimestral se deben realizar trimestralmente.'))

    a(('h4', 'Inspección semanal (autocontrol)'))
    a(('p', 'Las inspecciones semanales tienen como finalidad verificar que el elemento protegido, las boquillas, las válvulas y los '
            'componentes eléctricos del sistema se mantienen en las condiciones de diseño, sin modificaciones ni obstrucciones '
            'que comprometan la descarga.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Elemento protegido', 'verificar que no ha sido modificado respecto de las condiciones de diseño del sistema.'),
        ('Interferencia con la descarga', 'verificar que el elemento protegido no obstruye la descarga de las boquillas.'),
        ('Orientación de las boquillas', 'verificar que se mantiene la orientación prevista hacia el elemento protegido.'),
        ('Posición de las válvulas de control', 'comprobar que todas se encuentran en su correcta posición.'),
        ('Precintado de las válvulas', 'verificar que las válvulas se encuentran precintadas; si no lo están, se deben volver a '
                                       'precintar y dejar constancia en observaciones.'),
        ('Estado de boquillas y cañerías', 'verificar que se encuentran en buen estado y no bloqueadas; en caso contrario, indicar '
                                           'las correcciones y registrarlas en observaciones.'),
        ('Válvula de control', 'inspeccionar que la válvula de control y sus componentes no tengan daños.'),
        ('Local de la válvula de control', 'comprobar que se mantiene por encima de **5 °C** y, durante el tiempo frío, que está '
                                           'suficientemente calefaccionado; '
                                           'se debe registrar la temperatura.'),
        ('Válvula de diluvio', 'verificar que está libre de daños y que sus componentes se encuentran en condición correcta, sin '
                               'fugas de agua.'),
        ('Componentes eléctricos', 'comprobar que se encuentran en servicio.'),
        ('Sala de bombas', 'controlar la temperatura, especialmente en lugares con riesgo de congelamiento.'),
        ('Presión del sistema', 'verificar que se encuentra en los valores normales y registrar la presión leída en el manómetro '
                                'del sistema de presurización.'),
    ]))
    a(('p', 'Las áreas que resulten inaccesibles para la inspección se deben revisar durante cada cierre programado de la '
            'instalación y, como máximo, cada **dieciocho meses**.'))
    a(('p', cierre(2)))

    a(('h4', 'Inspección mensual'))
    a(('p', 'Las inspecciones mensuales permiten comprobar el estado de conservación de las boquillas, las tuberías, sus soportes '
            'y los manómetros, así como el estado de las válvulas, de la reserva de agua y del sistema de presurización.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Modificaciones', 'verificar que no hay modificaciones del sistema, del entorno ni del uso del área protegida.'),
        ('Boquillas pulverizadoras', 'verificar que están libres de corrosión, de materias extrañas y de daños físicos.'),
        ('Tuberías', 'verificar que se encuentran:'),
        ['en buen estado;', 'sin daños mecánicos;', 'sin fugas;', 'sin corrosión;', 'bien alineadas;', 'no sujetas a cargas externas.'],
        ('Soportes de tuberías', 'verificar que están libres de daños y de corrosión.'),
        ('Manómetros', 'verificar que se encuentran en buen estado y que indican una presión normal y constante de abastecimiento de agua.'),
        ('Presión de agua', 'registrar la presión del sistema, en MPa, al comienzo y al final de la inspección.'),
        ('Válvulas y cañerías del circuito de agua', 'verificar que las válvulas se encuentran precintadas, identificadas y en '
                                                     'posición correcta, y controlar el estado de la válvula de control.'),
        ('Temperatura del lugar de montaje', 'registrar la temperatura, en °C, del lugar de montaje de la válvula de control y de la reserva.'),
        ('Reserva de agua', 'en la reserva sin presión o presurizada (tanque hidroneumático), verificar el nivel de agua, el estado de las válvulas y cañerías y el funcionamiento de la válvula de '
                            'llenado; para la reserva de agua sin presión se aplica el capítulo 13 de la IRAM 3546:2011.'),
        ('Presurización por aire comprimido', 'verificar las válvulas y cañerías, el precintado, la identificación y la posición de '
                                              'las válvulas, y registrar la presión del sistema de aire comprimido, en MPa, al '
                                              'comienzo y al final de la inspección.'),
        ('Compresor', 'registrar las presiones de arranque y de parada, en MPa, y comprobar su arranque automático.'),
        ('Presostatos', 'comprobar su correcto funcionamiento.'),
        ('Presurización por nitrógeno', 'verificar las válvulas y cañerías, el precintado y la identificación de las válvulas, '
                                        'registrar la presión de almacenamiento, en MPa, y controlar la posición de la válvula reductora.'),
        ('Presurización por bomba centrífuga', 'verificar el equipo según el capítulo 12 de la IRAM 3546:2011.'),
        ('Instrucciones operativas en sala de bombas', 'verificar que la identificación de componentes y cañerías se encuentra en '
                                                       'condiciones operativas y señalizada.'),
    ]))
    a(('p', cierre(3)))

    # ---------------- PRUEBA ----------------
    a(('h3', 'PRUEBA'))
    a(('p', 'Las pruebas consisten en verificaciones funcionales destinadas a comprobar el correcto funcionamiento de los equipos '
            'y dispositivos del sistema, y permiten detectar fallas operativas que no pueden observarse únicamente mediante '
            'inspección visual. Cuando durante las pruebas se detecten fallas o anomalías, se debe proceder inmediatamente a su '
            'reparación o mantenimiento, de modo que los equipos funcionen adecuadamente cuando vuelvan a probarse.'))

    a(('h4', 'Prueba mensual'))
    a(('p', 'Las pruebas mensuales tienen como finalidad comprobar que las válvulas de control permanecen abiertas, que el drenaje '
            'es adecuado, que la conexión para el servicio de bomberos está disponible y que los accionamientos del sistema '
            'responden correctamente.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Válvulas de control', 'comprobar que se encuentran abiertas y enclavadas o supervisadas.'),
        ('Drenaje', 'comprobar que el drenaje del sistema es adecuado.'),
        ('Conexiones para el servicio de bomberos', 'verificar que se encuentran permanentemente accesibles y visibles en el exterior, '
                                                    'en condiciones operativas y señalizadas.'),
        ('Tapas de las conexiones', 'verificar que se encuentran en su lugar, limpias, sin daños y ligeramente lubricadas para su '
                                    'fácil apertura.'),
        ('Accionamientos del sistema', 'con la válvula de control aguas arriba cerrada o con el dispositivo de prueba del fabricante, '
                                       'según los pasos 1, 3 y 4 del protocolo de la prueba en blanco, comprobar el funcionamiento de los accionamientos manuales y automáticos del sistema y de '
                                       'la válvula de control.'),
    ]))
    a(('p', cierre(3)))

    a(('h4', 'Prueba trimestral'))
    a(('p', 'Las pruebas trimestrales están orientadas a verificar la respuesta de la alarma de flujo de agua y la libre maniobra '
            'de las válvulas de control en todo su recorrido.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Alarma de flujo de agua', 'comprobar su actuación.'),
        ('Válvula de derivación de la alarma', 'abrir la válvula de derivación (bypass) de la alarma para provocar el paso de agua '
                                               'hacia el dispositivo de alarma.'),
        ('Válvulas de control', 'abrir o cerrar cada válvula hasta su tope, volverla a su correcta posición y dejarla a **un cuarto '
                                'de vuelta** del tope.'),
    ]))
    a(('p', cierre(3)))
    a(('protocol', ('prueba de la alarma de flujo de agua y maniobra de válvulas de control', [
        ('Notificación y lectura inicial', [
            ('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo, registrar la presión indicada por el '
                            'manómetro del sistema e identificar la válvula de derivación de la alarma y su punto de drenaje.'),
            ('Justificación técnica', 'evita que la señal de prueba sea interpretada como un incendio real y permite comparar la '
                                      'presión del sistema antes y después del ensayo.'),
            ('Criterio de aceptación', 'notificación realizada y presión inicial dentro de los valores normales del sistema.')]),
        ('Apertura de la válvula de derivación', [
            ('Paso a paso', 'abrir la válvula de derivación de la alarma, de modo que circule agua hacia el dispositivo de alarma sin '
                            'abrir la válvula de diluvio, y observar la señal local y la señal transmitida al panel o al servicio de monitoreo.'),
            ('Justificación técnica', 'comprueba que el dispositivo de alarma de flujo y su circuito de transmisión responden ante el '
                                      'paso de agua; una alarma inoperante retrasa la respuesta ante una descarga real.'),
            ('Criterio de aceptación', 'la alarma de flujo actúa y la señal se recibe en el panel o en el servicio de monitoreo, '
                                       'según el diseño de la instalación.')]),
        ('Restablecimiento de la alarma', [
            ('Paso a paso', 'cerrar la válvula de derivación, drenar el agua remanente, restablecer la alarma y verificar que la '
                            'presión del sistema retorna a su valor inicial.'),
            ('Justificación técnica', 'una válvula de derivación abierta o una alarma sin restablecer deja al sistema en condición '
                                      'anormal y enmascara futuras señales.'),
            ('Criterio de aceptación', 'válvula de derivación cerrada, alarma restablecida y presión del sistema en su valor normal.')]),
        ('Maniobra de las válvulas de control', [
            ('Paso a paso', 'operar cada válvula de control hasta su tope, volverla a su correcta posición, dejarla a un cuarto de '
                            'vuelta del tope y volver a precintarla.'),
            ('Justificación técnica', 'detecta agarrotamientos o daños en el mecanismo y evita que la válvula quede trabada contra el tope.'),
            ('Criterio de aceptación', 'recorrido completo y libre, válvula en su posición normal a **un cuarto de vuelta** del tope y precinto colocado.')]),
    ])))

    a(('h4', 'Prueba semestral'))
    a(('p', 'Las pruebas semestrales permiten comprobar el buen funcionamiento del sistema en conjunto, desde la actuación del sistema '
            'de detección de incendios hasta la actuación posterior de la válvula, así como el estado interno de las válvulas de '
            'diluvio y la resistencia mecánica de las cañerías.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Prueba en blanco del sistema', 'comprobar el buen funcionamiento del sistema en conjunto: el sistema de detección de '
                                         'incendios y la actuación posterior de la válvula.'),
        ('Válvulas de diluvio', 'inspeccionar internamente todas las válvulas y comprobar que todos sus componentes actúan '
                                'correctamente y se mueven libremente.'),
        ('Partes de las válvulas de diluvio', 'reemplazar las partes dañadas cuando existan desgastes o deformaciones visibles.'),
        ('Cañerías', 'realizar la prueba hidráulica o neumática de resistencia mecánica.'),
        ('Salidas del sistema', 'verificar el flujo por todas las salidas.'),
        ('Picos atomizadores', 'realizar el recorrido de todos los componentes relacionados con los picos atomizadores.'),
    ]))
    a(('p', 'La prueba hidráulica de los tanques hidroneumáticos y de los cilindros de gases permanentes, incluida en la planilla '
            'semestral de la norma, se realiza con la frecuencia indicada en el apartado de ensayos de largo plazo.'))
    a(('p', cierre(5)))
    a(('protocol', ('prueba en blanco del sistema', [
        ('Aislamiento de la descarga', [
            ('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo, cerrar la válvula de control ubicada '
                            'aguas arriba de la válvula de diluvio o habilitar el dispositivo de prueba previsto por el fabricante, y '
                            'registrar la presión del sistema y la señal de supervisión de válvula cerrada, cuando exista.'),
            ('Justificación técnica', 'permite verificar la secuencia completa de actuación sin descarga de agua sobre el riesgo '
                                      'protegido ni consumo de la reserva.'),
            ('Criterio de aceptación', 'válvula de control en posición de prueba e identificada, sin posibilidad de descarga hacia las boquillas.')]),
        ('Activación del sistema de detección', [
            ('Paso a paso', 'activar un detector o el dispositivo de detección mediante el método de prueba que corresponda a su tipo '
                            '(neumático, eléctrico u otro) y observar la señal recibida en el panel o en el dispositivo de disparo.'),
            ('Justificación técnica', 'comprueba que la detección reconoce la condición de incendio y transmite la orden de disparo '
                                      'a la válvula de diluvio.'),
            ('Criterio de aceptación', 'la detección registra la alarma y emite la orden de apertura de la válvula de diluvio.')]),
        ('Actuación de la válvula de diluvio', [
            ('Paso a paso', 'verificar el disparo de la válvula de diluvio (apertura del mecanismo o de la clapeta, actuación del solenoide '
                            'o del actuador) y las señales eléctricas de disparo en el panel; la alarma de flujo de agua se verifica en '
                            'la prueba trimestral.'),
            ('Justificación técnica', 'una válvula que no actúa ante la orden de la detección deja sin protección al riesgo, aun con '
                                      'detección y abastecimiento operativos.'),
            ('Criterio de aceptación', 'la válvula actúa ante la orden de la detección y el panel registra las señales de disparo previstas en el diseño.')]),
        ('Rearme y restablecimiento', [
            ('Paso a paso', 'rearmar la válvula de diluvio según las instrucciones del fabricante, drenar el agua remanente, abrir lentamente la '
                            'válvula de control, volver a precintarla y restablecer el sistema de detección.'),
            ('Justificación técnica', 'el sistema debe quedar en servicio inmediatamente después del ensayo; una válvula de control '
                                      'cerrada anula la protección.'),
            ('Criterio de aceptación', 'válvula de diluvio rearmada, válvula de control abierta y precintada, presión del sistema en '
                                       'valores normales y detección en reposo.')]),
    ])))

    a(('h4', 'Prueba anual'))
    a(('p', 'Las pruebas anuales tienen como finalidad verificar el desempeño hidráulico del sistema mediante la descarga real de '
            'agua, comprobando el funcionamiento, la cobertura de las boquillas y el estado interno de las válvulas.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Prueba a caudal total', 'realizar una prueba a caudal total de cada sistema, comprobar su funcionamiento correcto y '
                                  'registrar el tiempo de operación.'),
        ('Filtros', 'inspeccionar y limpiar los filtros después de cada prueba.'),
        ('Descarga de agua', 'observar la descarga y comprobar que las boquillas no están obstruidas.'),
        ('Cobertura de agua pulverizada', 'hacer funcionar el sistema y comprobar que la cobertura sobre el elemento protegido es adecuada.'),
        ('Modelo de descarga', 'verificar y registrar el modelo de descarga de las boquillas sobre el elemento protegido.'),
        ('Válvula de diluvio o de acción previa', 'inspeccionar internamente la válvula y verificar que todos sus componentes '
                                                  'funcionan correctamente, se mueven libremente y están en buen estado.'),
        ('Válvulas de cierre', 'operar cada válvula hasta su recorrido total y volverla a su posición normal, volviendo a sellarla '
                               'o enclavarla cuando sea necesario.'),
        ('Válvulas del sistema', 'comprobar internamente las válvulas y verificar que todos sus componentes funcionan correctamente, '
                                 'se mueven libremente y están en buen estado.'),
        ('Boquillas', 'comprobar el estado de todas las boquillas, verificando que no tienen daños físicos ni corrosión y que no están obstruidas.'),
        ('Tuberías', 'comprobar el estado de todas las tuberías, verificando que no tienen daños físicos, no están desalineadas y '
                     'no están sometidas a cargas exteriores.'),
        ('Soportes de tuberías', 'comprobar todos los soportes, verificando que no tienen daños físicos ni corrosión.'),
        ('Manómetros', 'verificar su calibración.'),
        ('Válvulas de seguridad', 'calibrar las válvulas de seguridad de los sistemas hidroneumáticos.'),
        ('Bombas contra incendio', 'realizar la prueba de las bombas según el capítulo 12 de la IRAM 3546:2011.'),
    ]))
    a(('p', 'Las pruebas a caudal total se deben realizar con mayor frecuencia cuando las condiciones de la instalación lo justifiquen.'))
    a(('p', 'En la planilla se debe indicar, para cada componente, si se encuentra en buen estado; en caso contrario, se debe '
            'describir brevemente la condición observada en el espacio de observaciones.'))
    a(('p', cierre(4)))
    a(('protocol', ('prueba a caudal total', [
        ('Preparación del entorno', [
            ('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo, coordinar con el usuario la descarga '
                            'sobre el elemento protegido, verificar que el drenaje del área puede evacuar el caudal de prueba, '
                            'controlar el nivel de la reserva de agua y registrar la presión estática del sistema.'),
            ('Justificación técnica', 'la prueba implica una descarga real por todas las boquillas; un drenaje insuficiente o una '
                                      'reserva incompleta invalidan el resultado y pueden generar daños en el entorno.'),
            ('Criterio de aceptación', 'notificación realizada, área preparada, reserva en su nivel normal y presión estática registrada.')]),
        ('Accionamiento y tiempo de operación', [
            ('Paso a paso', 'accionar el sistema mediante la detección o el dispositivo manual de disparo y medir con cronómetro el '
                            'tiempo transcurrido desde el accionamiento hasta la descarga de agua por las boquillas.'),
            ('Qué mide', 'el tiempo de respuesta del conjunto formado por el accionamiento, la válvula de diluvio y el llenado de la '
                         'red de cañerías secas.'),
            ('Justificación técnica', 'un tiempo de operación mayor que el de las pruebas anteriores indica obstrucciones, fallas en '
                                      'la válvula o deficiencias en el abastecimiento.'),
            ('Criterio de aceptación', 'funcionamiento correcto del sistema y tiempo de operación registrado en la planilla, '
                                       'comparable con el de diseño o con el de las pruebas anteriores.')]),
        ('Observación de la descarga', [
            ('Paso a paso', 'desde fuera de la zona de descarga y respetando las distancias de seguridad a partes energizadas, con '
                            'autorización escrita del responsable eléctrico y de proceso, verificar que todas las boquillas descargan y que el '
                            'agua pulverizada cubre el elemento protegido, y registrar la presión residual en el punto de prueba.'),
            ('Justificación técnica', 'una boquilla obstruida o desorientada deja zonas del riesgo sin refrigeración, lo que '
                                      'compromete la protección de depósitos, estructuras o transformadores.'),
            ('Criterio de aceptación', 'todas las boquillas descargan sin obstrucciones, la cobertura es adecuada y la presión '
                                       'residual corresponde a la de los cálculos hidráulicos del sistema.')]),
        ('Cierre y restablecimiento', [
            ('Paso a paso', 'cerrar el abastecimiento, drenar el sistema, inspeccionar y limpiar los filtros, rearmar la válvula de '
                            'diluvio, abrir y precintar las válvulas de control y verificar que la presión del sistema retorna a sus '
                            'valores normales.'),
            ('Justificación técnica', 'la prueba arrastra suciedad hacia los filtros y deja la válvula de diluvio disparada; el '
                                      'sistema queda fuera de servicio hasta su restablecimiento.'),
            ('Criterio de aceptación', 'filtros limpios, válvula de diluvio rearmada, válvulas de control abiertas y precintadas, y '
                                       'sistema en servicio.')]),
    ])))

    # ---------------- MANTENIMIENTO ----------------
    a(('h3', 'MANTENIMIENTO'))
    a(('p', 'El mantenimiento comprende las tareas destinadas a conservar los equipos y componentes del sistema en condiciones '
            'adecuadas de funcionamiento y confiabilidad. Estas tareas deben realizarse inmediatamente después de detectar fallas '
            'durante las inspecciones o pruebas, y deben asegurar que todos los componentes y equipos que forman el sistema estén '
            'operativos y confiables.'))

    a(('h4', 'Mantenimiento mensual'))
    a(('p', 'Las tareas de mantenimiento mensual están orientadas a conservar la libre maniobra de las válvulas y de los dispositivos '
            'de disparo, su correcta lubricación y la limpieza interior de la red de cañerías enterradas.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Maniobra de dispositivos de disparo y válvulas', 'operación, con la válvula de control aguas arriba cerrada o con el '
            'dispositivo de prueba del fabricante para evitar la descarga, de los dispositivos manuales de disparo y de las válvulas, '
            'incluidas las de husillo ascendente y puente fijo y las de poste indicador, con apertura y cierre total; el volante debe '
            'quedar a **un cuarto de vuelta** de su posición de apertura o cierre.'),
        ('Lubricación de vástagos', 'aplicación de grafito o de grafito con aceite liviano en todos los vástagos de las válvulas.'),
        ('Distribución del lubricante', 'apertura y cierre de todas las válvulas para distribuir el lubricante.'),
        ('Limpieza de cañerías enterradas', 'lavado con chorro de agua de todas las tuberías y conexiones enterradas que conectan con '
            'las ascendentes del sistema, durante el tiempo necesario para asegurar que todo queda limpio y que el agua fluye limpia.'),
    ]))
    a(('p', 'El caudal de limpieza debe ser, como mínimo, el demandado por el sistema según los cálculos hidráulicos, o el caudal '
            'necesario para obtener una velocidad mayor que la de cálculo. Esta tarea puede implicar también la prueba a caudal total '
            'de las conexiones del sistema; después de la prueba, los filtros deben inspeccionarse y limpiarse.'))
    a(('p', cierre(3)))

    a(('h4', 'Mantenimiento anual'))
    a(('p', 'Las tareas de mantenimiento anual permiten restablecer la capacidad de filtrado del sistema y asegurar que el sistema '
            'de detección asociado cuente con su propio mantenimiento.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Limpieza de filtros', 'cierre del abastecimiento de agua y retiro de los filtros para su limpieza.'),
        ('Filtros autolimpiantes', 'rotación de su volante de accionamiento.'),
        ('Lubricado de válvulas de corte', 'lubricación de todos los vástagos de las válvulas con grafito o grafito en aceite liviano.'),
        ('Limpieza de cañerías', 'limpieza de todas las cañerías y conexiones subterráneas con caudal pleno de agua, para asegurar '
                                 'que la suciedad arrastrada por el abastecimiento no obstruye las boquillas; el agua debe fluir limpia.'),
        ('Mantenimiento del sistema de detección', 'verificación de que se haya realizado el mantenimiento del sistema de detección '
                                                   'según el capítulo 6 de la IRAM 3546:2011.'),
    ]))
    a(('p', cierre(4)))

    # ---------------- COMPLEMENTARIAS ----------------
    a(('h3', 'CRITERIOS COMPLEMENTARIOS DE LA NFPA 25'))
    a(('p', 'Los criterios complementarios tienen como finalidad incorporar las tareas y los valores de aceptación del capítulo 10 '
            'de la NFPA 25 que la IRAM 3546:2011 no contempla.'))
    a(('p', 'Se debe asegurar:'))
    a(('items', [
        ('Áreas inaccesibles', 'los componentes en áreas inaccesibles por razones de seguridad, como procesos continuos o equipos '
                               'energizados, se inspeccionan en cada parada programada, con un intervalo no mayor que **18 meses** '
                               '(10.2.1.1).'),
        ('Drenaje del área', 'inspección visual trimestral del área bajo el sistema y a su alrededor, para verificar que sumideros y '
                             'canaletas no están obstruidos y que los muros de contención están en buen estado (10.2.7).'),
        ('Filtros', 'lavado del filtro principal hasta que salga limpio y limpieza de los filtros de cada boquilla después de cada '
                    'operación o prueba de flujo; retiro e inspección del filtro principal cada **5 años** (10.2.1.7 y 10.2.6).'),
        ('Tiempo de respuesta', 'en la prueba con fuente de calor, la detección térmica debe operar dentro de los **40 s**; la '
                                'detección de gases inflamables, dentro del tiempo de diseño; ambos tiempos se registran '
                                '(10.3.3.1).'),
        ('Tiempo de descarga', 'registro del tiempo entre la operación de la detección y la llegada del agua al área protegida '
                               '(10.3.3.2).'),
        ('Patrón de descarga', 'observación de la descarga de todas las boquillas abiertas; si el agua no se puede descargar, se '
                               'verifica la orientación y se prueba el sistema con aire para comprobar que las boquillas no están '
                               'obstruidas (10.3.3.3).'),
        ('Presiones', 'registro de la presión en la boquilla hidráulicamente más remota y en la válvula de diluvio, y comparación '
                      'con las presiones del cálculo hidráulico (10.3.3.4).'),
        ('Sistemas múltiples', 'prueba simultánea de la máxima cantidad de sistemas que se espera que operen en caso de incendio, '
                               'para verificar la suficiencia del abastecimiento (10.3.4).'),
        ('Accionamiento manual', 'operación anual de los dispositivos de accionamiento manual (10.3.5).'),
        ('Puntos bajos', 'después de la prueba con caudal total, apertura de los drenajes de puntos bajos, vaciado, cierre y '
                         'reposición de los tapones, o verificación de que los orificios de drenaje están libres (10.3.6.1).'),
        ('Boquillas automáticas y rociadores piloto', 'inspección como rociadores, prueba según la vida útil del elemento sensible y '
                                                      'acopio de repuestos de cada tipo, conservados a no más de **38 °C** '
                                                      '(10.2.4.2, 10.2.4.3 y 10.3.7).'),
        ('Sistemas de ultra alta velocidad', 'prueba operativa completa con medición del tiempo de respuesta como mínimo una vez al '
                                             'año, con un tiempo no mayor que **100 ms**; prueba e inspección mensual de los '
                                             'detectores, e inspección de los controladores y de las válvulas del abastecimiento '
                                             'al comienzo de cada turno de trabajo (10.4).'),
        ('Fuera de servicio', 'aviso a la dirección de la instalación, al servicio de bomberos, a la brigada y a la autoridad '
                              'competente, y colocación de un cartel en cada toma de impulsión o válvula de control que indique qué '
                              'parte del sistema está fuera de servicio (10.1.6).'),
    ]))
    a(('p', 'Las tareas trimestrales se registran en la planilla SG-PEM-IFI-SAP-3 y las anuales en la SG-PEM-IFI-SAP-4, como tareas '
            'complementarias, conforme al requisito general de la IRAM 3546:2011 que admite el agregado de tareas a las planillas.'))

    a(('h3', 'ENSAYOS DE LARGO PLAZO'))
    a(('p', 'Los ensayos de largo plazo tienen como finalidad verificar la resistencia mecánica de los recipientes a presión '
            'asociados al abastecimiento y a la presurización del sistema.'))
    a(('p', 'Durante estos ensayos se debe realizar:'))
    a(('items', [
        ('Prueba hidráulica de recipientes', 'prueba hidráulica de los tanques hidroneumáticos y de los cilindros de gases permanentes '
            'cada **cinco años**, contados desde su fecha de fabricación o desde su última prueba hidráulica.'),
    ]))
    a(('p', 'Las pruebas hidrostáticas se deben ejecutar conforme a procedimientos documentados en función de las normas de '
            'aplicación, según los requisitos generales de la IRAM 3546:2011.'))
    a(('p', cierre(5)))

    a(('h3', 'PROCEDIMIENTO POSTERIOR A UNA DESCARGA O ACTUACIÓN'))
    a(('p', 'Luego de cada prueba con descarga de agua o de una actuación real del sistema, se deben restablecer las condiciones '
            'normales de servicio antes de dar por finalizada la intervención, de modo de asegurar la disponibilidad operativa del sistema.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Filtros', 'inspección y limpieza de los filtros.'),
        ('Válvula de diluvio', 'rearme de la válvula según las instrucciones del fabricante.'),
        ('Válvulas de control y de cierre', 'reposición de cada válvula a su posición normal y nuevo precintado o enclavamiento.'),
        ('Detección y alarmas', 'restablecimiento del sistema de detección y de la alarma de flujo de agua.'),
        ('Presión del sistema', 'verificación de que la presión retorna a sus valores normales.'),
        ('Boquillas', 'control de que no han quedado obstruidas y mantienen su orientación.'),
    ]))
    a(('p', cierre(4)))
    a(('h3', 'SEGURIDAD Y SALUD OCUPACIONAL'))
    a(('p', 'La seguridad del personal tiene como finalidad evitar que las pruebas con descarga de agua expongan a las personas a riesgos eléctricos, de proceso o de inflamables propios del elemento protegido.'))
    a(('p', 'Durante las pruebas con descarga y las tareas posteriores se debe asegurar:'))
    a(('items', [('Coordinación previa', 'autorización escrita del responsable eléctrico y de proceso de la instalación antes de toda descarga sobre transformadores, equipos energizados o depósitos de inflamables.'), ('Delimitación del área', 'señalización y delimitación de la zona de descarga y prohibición de permanecer dentro de ella durante la prueba.'), ('Distancias a partes energizadas', 'observación de la descarga desde fuera de la zona de descarga, respetando las distancias de seguridad a partes energizadas que establezca el responsable eléctrico.'), ('Elementos de protección personal', 'uso de los elementos de protección personal adecuados al riesgo protegido.'), ('Disposición del agua de prueba', 'evacuación del agua de prueba sin afectar instalaciones ni el ambiente, en particular cuando pueda arrastrar productos del área protegida.')]))
    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'Las modificaciones del elemento protegido, del entorno o del uso del área pueden afectar la orientación y la cobertura '
            'de las boquillas. Toda modificación se debe evaluar técnicamente antes de su ejecución y su existencia se debe registrar '
            'en la planilla de información general.'))
    a(('p', 'La empresa mantenedora es responsable de ejecutar las tareas de inspección, prueba y mantenimiento y de verificar las '
            'inspecciones de autocontrol. El usuario o propietario es responsable de completar las inspecciones de autocontrol, de '
            'mantener libre de obstrucciones la descarga de las boquillas y de no modificar el elemento protegido sin evaluación técnica.'))
    return C


def REGISTRO_EXTRA(cierre):
    return [
        'Los datos de la instalación, de las válvulas, toberas y cañerías, del abastecimiento de agua, de las bombas contra incendio '
        'y de la toma de impulsión para bomberos deben registrarse en la planilla SG-PEM-IFI-%s-1 %s – %s.' % (SIG, NOM, PL[1]),
        'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '
        'codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables se indican con NA. Toda '
        'condición O o X se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y '
        'por el responsable de la instalación, con su aclaración.',
    ]
