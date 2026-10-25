# -*- coding: utf-8 -*-
SIG, NOM, NOMU, CAP = 'SRA', 'Sistema de Rociadores Automáticos', 'SISTEMA DE ROCIADORES AUTOMÁTICOS', '7'
PL = {1: 'Información general', 2: 'Inspección semanal (autocontrol)', 3: 'Inspección mensual',
      4: 'Inspección y pruebas trimestrales', 5: 'Inspección y pruebas semestrales', 6: 'Pruebas y mantenimiento anual',
      7: 'Pruebas de tres años', 8: 'Mantenimiento quinquenal', 9: 'Pruebas de cinco, veinte y cincuenta años'}
VIG = (' Se aplica la edición vigente de cada norma NFPA; la numeración de los artículos citados se debe confirmar en esa '
       'edición, porque puede variar entre ediciones.')
N25 = 'NFPA 25'


def CONTENT(cierre):
    C = []; a = C.append
    a(('h2', NOMU))
    a(('basado', '(Basado en IRAM 3546:2011 – Capítulo %s; criterios complementarios: NFPA 25 y NFPA 13)' % CAP))
    a(('p', 'Este apartado establece los requisitos mínimos para la inspección, prueba y mantenimiento del sistema de rociadores '
            'automáticos, con el objetivo de asegurar que el sistema detecte y controle un incendio mediante la descarga automática '
            'de agua sobre el área afectada, con el caudal y la presión previstos en su diseño.'))
    a(('p', 'La IRAM 3546:2011 es la base del presente procedimiento y fija sus frecuencias. La NFPA 25, Norma para la inspección, '
            'prueba y mantenimiento de sistemas de protección contra incendios a base de agua, se aplica como criterio complementario '
            'para los valores de aceptación y para las tareas que la IRAM no contempla; la NFPA 13, Norma para la instalación de '
            'sistemas de rociadores, se aplica para los criterios de diseño que se deben conservar. Ante diferencias, se adopta '
            'siempre la condición más exigente.' + VIG))
    a(('p', 'El procedimiento comprende los sistemas de tubería húmeda, de tubería seca, de acción previa y de diluvio. El '
            'equipamiento del sistema incluye:'))
    a(('items', [
        ('Abastecimiento de agua', 'red pública, tanque o reserva de agua y, cuando corresponde, bombas contra incendio; su '
                                   'mantenimiento se rige por los capítulos 12 y 13 de la IRAM 3546:2011.'),
        ('Válvulas de control', 'válvulas de corte de husillo ascendente y puente fijo, de poste indicador y demás válvulas de '
                                'seccionamiento, precintadas, enclavadas o supervisadas eléctricamente.'),
        ('Puesto de control', 'válvula de alarma (tubería húmeda), válvula de tubería seca con su dispositivo de apertura rápida, '
                              'válvula de acción previa o válvula de diluvio, con sus manómetros, drenaje principal y trim.'),
        ('Red de cañerías', 'tubería ascendente, cañerías principales, ramales, soportes, abrazaderas y sujeciones sísmicas.'),
        ('Rociadores', 'rociadores automáticos instalados y acopio de rociadores de repuesto con sus llaves.'),
        ('Dispositivos de alarma y supervisión', 'campana hidráulica, interruptores de flujo, presostatos, interruptores de '
                                                 'supervisión de válvulas y alarmas de baja presión de aire.'),
        ('Equipos auxiliares, tales como', ''),
        ['conexión de prueba de inspección y válvula de derivación (bypass) de la alarma;',
         'compresor o abastecimiento de aire o nitrógeno de los sistemas de tubería seca y de acción previa;',
         'sistema de detección asociado a los sistemas de acción previa y de diluvio;',
         'toma de impulsión para bomberos;',
         'cartel de datos del cálculo hidráulico.'],
    ]))
    a(('p', 'La inspección, prueba y mantenimiento del sistema puede dejarlo total o parcialmente fuera de servicio. Para minimizar '
            'o anular ese inconveniente se debe acordar con el responsable de la instalación el momento de la intervención y aplicar '
            'el procedimiento de puesta fuera de servicio de este manual.'))
    a(('p', 'Donde se cuente con un servicio de supervisión, para evitar falsas alarmas se debe notificar al personal de ese servicio '
            'antes de realizar cualquier prueba o acción que pueda generar una alarma y luego de concluir las tareas.'))

    # ---------------- INSPECCIÓN ----------------
    a(('h3', 'INSPECCIÓN'))
    a(('p', 'La inspección consiste en un examen visual del sistema y de sus componentes, para verificar que está en condiciones '
            'aparentes de operación y libre de daños físicos. Se realiza generalmente en cada planta, recorriendo las zonas protegidas.'))
    a(('p', 'Las inspecciones de frecuencia menor a un mes pueden ser completadas por el usuario de la instalación como '
            'inspecciones de autocontrol, y se deben identificar como tales; el mantenedor debe verificar su correcto cumplimiento, '
            'dejando constancia de los hallazgos.'))
    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica previa '
            'de la instalación según la IRAM 3619; esta evaluación no es obligatoria y puede ser solicitada por cualquiera de las '
            'partes interesadas.'))

    a(('h4', 'Inspección diaria en tiempo de heladas (autocontrol)'))
    a(('p', 'Esta inspección tiene como finalidad evitar el congelamiento del agua en el puesto de control de los sistemas de '
            'tubería seca.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Local de la válvula de tubería seca', 'comprobar que el local calefaccionado que contiene la válvula de control mantiene '
                                                'una temperatura superior a **5 °C**. Si el local dispone de alarma de baja '
                                                'temperatura, la inspección se realiza semanalmente.'),
    ]))
    a(('p', 'La NFPA 25 (Tabla 9.1.1.2 y 13.4.5.2.7) exige además probar las alarmas de baja temperatura del recinto de la válvula '
            'una vez al año, al comienzo de la temporada de calefacción. La inspección diaria se registra en la planilla de '
            'inspección semanal del período.'))
    a(('p', cierre(2)))

    a(('h4', 'Inspección semanal (autocontrol)'))
    a(('p', 'La inspección semanal tiene como finalidad verificar que el sistema mantiene abiertas sus válvulas, libres sus rociadores '
            'y estables las presiones de los puestos de control.'))
    a(('p', 'Para todos los sistemas de rociadores se debe verificar:'))
    a(('items', [
        ('Válvulas de control precintadas', 'comprobar que se encuentran en su posición normal, abiertas, con el precinto colocado y '
                                            'sin pérdidas; si no lo están, volver a precintar e indicarlo en observaciones.'),
        ('Válvulas del abastecimiento de agua', 'comprobar que están abiertas, incluidas las que se encuentran en la vía pública.'),
        ('Rociadores', 'comprobar que no están dañados, bloqueados por materiales almacenados, pintados ni anulados.'),
        ('Distancia libre', 'comprobar que se mantiene una distancia libre de **0,46 m** por debajo de los deflectores; la NFPA 25 '
                            '(5.2.1.2.1) fija **457 mm** y eleva la distancia a **914 mm** en rociadores de supresión temprana y '
                            'respuesta rápida (ESFR) y de aplicación específica para almacenamiento (CMSA).'),
    ]))
    a(('p', 'Fijar a las cañerías una tira de papel o de plástico de 0,46 m de largo permite recordar a los usuarios la altura máxima '
            'de almacenamiento.'))
    a(('p', 'En los sistemas de tubería seca, de acción previa y de diluvio se debe verificar además:'))
    a(('items', [
        ('Manómetros de agua y de aire', 'comprobar que las presiones se mantienen dentro del rango adecuado para cada sistema y '
                                         'registrar las lecturas en **kPa**. Se recomienda anotar la presión normal en una etiqueta '
                                         'atada al manómetro. Toda pérdida de presión mayor que el **10 %** respecto de la indicada '
                                         'por el instalador se debe investigar. Si la presión de aire se supervisa desde un local '
                                         'permanentemente ocupado, los manómetros se inspeccionan mensualmente.'),
        ('Válvula de tubería seca', 'comprobar que todos sus dispositivos están en la posición correcta y que la válvula está en '
                                    'buen estado y sin fugas.'),
    ]))
    a(('p', 'La frecuencia semanal de la IRAM 3546:2011 es más exigente que la de la NFPA 25, que establece la inspección semanal '
            'solo para las válvulas precintadas (13.3.2.1) y mensual para los manómetros de los sistemas de tubería seca, de acción '
            'previa y de diluvio (13.2.4); por eso se mantiene la IRAM.'))
    a(('p', cierre(2)))

    a(('h4', 'Inspección mensual'))
    a(('p', 'La inspección mensual tiene como finalidad verificar la disponibilidad de la toma de impulsión para bomberos, de las '
            'válvulas, de los repuestos y de los dispositivos de alarma.'))
    a(('p', 'Para todos los sistemas de rociadores se debe verificar:'))
    a(('items', [
        ('Toma de impulsión para bomberos', 'comprobar que está permanentemente accesible y visible, con las tapas y los tapones en '
                                            'su sitio, limpios, sin daños y lubricados con una fina capa de grafito, y que se drena '
                                            'mediante la válvula de goteo de la válvula de retención para evitar heladas.'),
        ('Válvulas de control enclavadas o supervisadas', 'comprobar que están en su posición normal y abiertas.'),
        ('Válvulas del abastecimiento de agua', 'comprobar que están abiertas, incluidas las situadas en la vía pública.'),
        ('Acopio de rociadores de repuesto', 'comprobar que el tipo y la cantidad son correctos según la tabla siguiente, que hay '
                                             'como mínimo **dos** rociadores por cada tipo y rango de temperatura instalados y una '
                                             'llave por cada tipo de rociador.'),
        ('Tuberías', 'comprobar que están en buenas condiciones y libres de daños físicos.'),
        ('Dispositivos de alarma', 'comprobar que están libres de daños físicos y que las conexiones eléctricas son correctas.'),
        ('Manómetros', 'comprobar que la presión está en el rango correcto, que el manómetro mide la presión del sistema y que está '
                       'en buenas condiciones.'),
        ('Válvulas de alarma', 'comprobar que no tienen fugas hacia la cámara de retardo ni hacia el drenaje de alarma.'),
        ('Cartel de cálculo hidráulico', 'comprobar que la etiqueta con los datos del cálculo hidráulico, si existe, está legible y '
                                         'bien sujeta a la tubería ascendente.'),
    ]))
    a(('table', [['Rociadores instalados', 'Rociadores de repuesto (mínimo)'],
                 ['Hasta 300', '6'], ['De 301 a 1000', '12'], ['Más de 1000', '24']]))
    a(('p', 'La cantidad mínima de repuestos coincide con la NFPA 25 (5.4.1.6.4). Esa norma exige además que los repuestos '
            'correspondan a los tipos y temperaturas de los rociadores instalados, que el gabinete se ubique donde la temperatura '
            'nunca supere la temperatura máxima de techo admitida para los rociadores que contiene (5.4.1.6.2), que haya una llave '
            'por cada tipo de rociador (5.4.1.6.5) y que en el gabinete se exhiba la lista de los rociadores instalados, con '
            'fabricante, modelo, factor K, tipo de deflector, sensibilidad térmica, temperatura nominal, modelo de llave, cantidad '
            'instalada, cantidad en el gabinete y fecha de revisión de la lista (5.4.1.6.6).'))
    a(('p', 'En los sistemas de tubería seca, de acción previa y de diluvio, la NFPA 25 exige inspeccionar mensualmente el exterior '
            'de la válvula (13.4.3.1.1, 13.4.4.1.1 y 13.4.5.1.2) para verificar que está libre de daños, que las válvulas del trim '
            'están en la posición correcta, que no hay pérdidas por el asiento o por la cámara intermedia y que los componentes '
            'eléctricos están en servicio. Esa verificación se incorpora a la inspección mensual.'))
    a(('p', cierre(3)))

    a(('h4', 'Inspección anual'))
    a(('p', 'La inspección anual tiene como finalidad detectar el deterioro de los rociadores, de la red de cañerías y de sus '
            'soportes, y preparar el edificio para el tiempo frío.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Rociadores', 'comprobar desde el nivel del piso que están libres de corrosión, de obstrucciones del deflector, de materiales '
                       'extraños como pintura y de daños físicos.'),
        ('Tuberías', 'comprobar que no gotean, no presentan corrosión, no están desalineadas ni sujetas a cargas externas, y que no '
                     'se utilizan como soporte de elementos ajenos al sistema (NFPA 25, 5.2.2.2).'),
        ('Soportes y sujeciones sísmicas', 'comprobar que no están dañados, sueltos ni corroídos; los que lo estén se deben reemplazar '
                                           'o volver a fijar (NFPA 25, 5.2.3.2).'),
        ('Aberturas del edificio', 'antes del tiempo frío, comprobar que ventanas, puertas, claraboyas y otras aberturas no exponen '
                                   'las tuberías a heladas.'),
    ]))
    a(('p', 'Las tuberías, abrazaderas y varillas de sujeción situadas en espacios ocultos, como sobre falsos techos, no requieren '
            'inspección; las situadas en áreas inaccesibles por razones de seguridad del proceso se inspeccionan en cada parada '
            'programada (NFPA 25, 5.2.2.3, 5.2.2.4 y 5.2.3.4).'))
    a(('p', 'Según la NFPA 25 (5.2.1.1.1), se debe reemplazar todo rociador que presente alguna de las siguientes condiciones:'))
    a(('items', [
        ['pérdida de agua;', 'corrosión;', 'daño físico;', 'pérdida del líquido del bulbo;',
         'carga de polvo, grasa u otros depósitos;', 'pintura, salvo la aplicada por el fabricante.'],
    ]))
    a(('p', 'Como criterio de diseño que se debe conservar, la NFPA 13 fija una presión mínima de funcionamiento de **0,5 bar** '
            '(7 psi) en cualquier rociador, salvo que el listado del rociador exija un valor mayor. Ese valor no se verifica en la '
            'inspección visual; se controla con el cálculo hidráulico y con las pruebas de caudal del abastecimiento.'))
    a(('p', 'La temperatura nominal de los rociadores se identifica por el color del bulbo o de los brazos. Los rociadores de '
            'reemplazo deben tener las mismas características que los instalados y no se deben pintar ni recubrir después de '
            'fabricados (NFPA 25, 5.4.1.4, 5.4.1.7 y Tabla 5.4.1.6.2):'))
    a(('table', [['Clasificación', 'Temperatura nominal', 'Temperatura máxima de techo', 'Color de los brazos', 'Color del bulbo'],
                 ['Ordinaria', '57 °C a 77 °C', '38 °C', 'Sin color o negro', 'Naranja o rojo'],
                 ['Intermedia', '79 °C a 107 °C', '66 °C', 'Blanco', 'Amarillo o verde'],
                 ['Alta', '121 °C a 149 °C', '107 °C', 'Azul', 'Azul'],
                 ['Extra alta', '163 °C a 191 °C', '149 °C', 'Rojo', 'Violeta'],
                 ['Muy extra alta', '204 °C a 246 °C', '191 °C', 'Verde', 'Negro'],
                 ['Ultra alta', '260 °C a 302 °C y 343 °C', '246 °C y 329 °C', 'Naranja', 'Negro']]))
    a(('p', cierre(6)))

    # ---------------- PRUEBA ----------------
    a(('h3', 'PRUEBA'))
    a(('p', 'Las pruebas tienen como propósito verificar el funcionamiento hidráulico, de alarma y de disparo del sistema, y detectar '
            'deficiencias no evidenciadas durante la inspección. El mantenimiento se debe realizar inmediatamente después de las '
            'pruebas que detectan fallas.'))
    a(('p', 'Durante las pruebas se debe asegurar que el flujo de agua no daña la instalación ni los bienes protegidos, y que el '
            'drenaje puede evacuar el caudal de prueba.'))

    a(('h4', 'Prueba trimestral'))
    a(('p', 'La prueba trimestral tiene como finalidad verificar el estado del abastecimiento de agua y la operación de las alarmas '
            'de flujo y de baja presión de aire.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Prueba de drenaje (todos los sistemas)', 'anotar la presión estática que indica el manómetro inferior de la válvula de '
                                                   'control, abrir completamente el drenaje principal de **50,8 mm** y, con el '
                                                   'caudal estabilizado, anotar la presión residual. Las caídas mayores que el '
                                                   '**10 %** respecto de las lecturas anteriores se deben investigar de inmediato, '
                                                   'porque indican una válvula cerrada o una tubería obstruida (NFPA 25, 13.2.2.3).'),
        ('Nivel de cebado de la válvula de tubería seca', 'abrir lentamente la válvula de prueba del nivel de cebado; si sale solo '
                                                          'aire, cerrarla y cebar con agua.'),
        ('Alarma de flujo de tubería húmeda', 'abrir la conexión de prueba de inspección, que simula la descarga de un rociador, y '
                                              'verificar la actuación de la campana hidráulica y del interruptor de flujo o del '
                                              'presostato. En tiempo de heladas se usa la derivación (bypass) de la alarma, que no '
                                              'comprueba la clapeta de la válvula.'),
        ('Alarma de baja presión de aire (tubería seca)', 'con la válvula del abastecimiento de agua cerrada, liberar lentamente el '
                                                          'aire por la válvula de prueba de inspección, anotar la presión a la que '
                                                          'suena la alarma, sin permitir que la válvula de tubería seca se dispare, '
                                                          'y restablecer luego el aire y el agua.'),
        ('Alarma de flujo de tubería seca, de acción previa y de diluvio', 'abrir la válvula de derivación (bypass) de la alarma; '
                                                                          'en tubería seca no se usa la conexión de prueba de '
                                                                          'inspección, porque puede disparar la válvula.'),
        ('Dispositivo de apertura rápida (tubería seca)', 'probarlo según las instrucciones del fabricante; la NFPA 25 '
                                                          '(13.4.5.2.4) exige esta prueba con frecuencia trimestral, más exigente '
                                                          'que la semestral de la IRAM 3546:2011, y se adopta la trimestral.'),
        ('Válvulas de corte', 'abrir cada válvula hasta el tope y cerrarla luego un cuarto de vuelta para prevenir bloqueos.'),
        ('Cartel de cálculo hidráulico', 'verificar que está presente y legible.'),
    ]))
    a(('p', 'La alarma se considera aceptable cuando se cumplen los tiempos de la NFPA 25 (13.2.3):'))
    a(('items', [
        ('Alarmas mecánicas (campana hidráulica)', 'señal audible dentro de los **5 min** de iniciado el flujo, que se mantiene '
                                                   'hasta que el flujo se detiene.'),
        ('Interruptores de flujo de paleta y presostatos', 'señal dentro de los **90 s** con un caudal igual al de un rociador '
                                                          'del menor orificio instalado.'),
    ]))
    a(('p', 'La NFPA 25 asigna frecuencia anual al drenaje principal (13.2.2), salvo que el único abastecimiento pase por un '
            'dispositivo antirretorno o una válvula reductora, en cuyo caso es trimestral, y frecuencia semestral a la prueba de los '
            'interruptores de flujo de paleta (13.2.3.2.2). La IRAM 3546:2011 exige ambas pruebas cada trimestre, por lo que se '
            'mantiene la frecuencia trimestral. En los sistemas de acción previa, la NFPA 25 (13.4.3.2.11 y 13.4.3.2.12) exige '
            'además probar cada trimestre las alarmas de alta y baja presión de aire y el dispositivo de supervisión de la posición '
            'del solenoide.'))
    a(('p', cierre(4)))
    a(('protocol', ('prueba de drenaje principal', [
        ('Preparación', [
            ('Paso a paso', 'notificar al servicio de supervisión, verificar que la salida del drenaje principal descarga a un lugar '
                            'seguro y tener a mano la planilla con las lecturas anteriores.'),
            ('Justificación técnica', 'la comparación con las lecturas anteriores es lo que permite detectar el deterioro del '
                                      'abastecimiento.'),
            ('Criterio de aceptación', 'descarga segura y registros anteriores disponibles.')]),
        ('Presión estática', [
            ('Paso a paso', 'leer y anotar en kPa la presión del manómetro inferior de la válvula de control, sin flujo en el sistema.'),
            ('Justificación técnica', 'es la presión disponible del abastecimiento en reposo.'),
            ('Criterio de aceptación', 'lectura comparable con la de la prueba anterior.')]),
        ('Presión residual', [
            ('Paso a paso', 'abrir completamente la válvula de drenaje principal, esperar a que el caudal se estabilice y anotar la '
                            'presión del mismo manómetro.'),
            ('Qué se determina con la lectura', 'una caída de la presión residual mayor que la habitual indica una válvula '
                                                'parcialmente cerrada, una obstrucción en el abastecimiento o una disminución de '
                                                'la capacidad de la fuente.'),
            ('Criterio de aceptación', 'reducción no mayor que el **10 %** respecto de la prueba anterior; si es mayor, se investiga '
                                       'la causa y se evalúa su efecto sobre el funcionamiento del sistema.')]),
        ('Normalización', [
            ('Paso a paso', 'cerrar lentamente el drenaje para evitar golpes de ariete, verificar que la presión vuelve al valor '
                            'estático y notificar la conclusión al servicio de supervisión.'),
            ('Justificación técnica', 'el cierre brusco puede dañar la red o disparar la válvula de alarma.'),
            ('Criterio de aceptación', 'presión estática restablecida y drenaje cerrado.')]),
    ])))
    a(('protocol', ('prueba de alarma de flujo de tubería húmeda', [
        ('Apertura de la conexión de prueba', [
            ('Paso a paso', 'notificar al servicio de supervisión, abrir totalmente la conexión de prueba de inspección y medir con '
                            'cronómetro el tiempo hasta la actuación de cada alarma.'),
            ('Justificación técnica', 'la conexión de prueba simula la descarga de un rociador del menor orificio instalado.'),
            ('Criterio de aceptación', 'interruptor de flujo o presostato en **90 s** como máximo y campana hidráulica en **5 min** '
                                       'como máximo.')]),
        ('Verificación de las señales', [
            ('Paso a paso', 'verificar la indicación en la central de alarma y la transmisión al servicio de supervisión, cuando exista.'),
            ('Justificación técnica', 'la alarma de flujo es la que avisa a los ocupantes y al servicio de bomberos.'),
            ('Criterio de aceptación', 'señal local y remota recibida e identificada con la zona correcta.')]),
        ('Normalización', [
            ('Paso a paso', 'cerrar la conexión de prueba, verificar que las alarmas se restablecen y que la válvula de alarma no '
                            'queda perdiendo agua por el drenaje.'),
            ('Justificación técnica', 'una clapeta que no asienta produce alarmas falsas y pérdida de agua.'),
            ('Criterio de aceptación', 'alarmas restablecidas y sin pérdidas.')]),
    ])))

    a(('h4', 'Prueba semestral'))
    a(('p', 'La prueba semestral tiene como finalidad verificar los sistemas de detección que comandan los sistemas de acción previa '
            'y de diluvio, y los interruptores de supervisión de las válvulas.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Sistemas de diluvio y de acción previa', 'probar el correcto funcionamiento del sistema de detección de incendio, según '
                                                   'el capítulo 6 de la IRAM 3546:2011.'),
        ('Sistema de tubería seca', 'probar el buen funcionamiento del sistema y de sus dispositivos de apertura rápida.'),
        ('Interruptores de supervisión de válvulas', 'operar cada válvula supervisada y verificar que la señal se produce dentro de '
                                                     'las **dos** vueltas del volante o de **1/5** del recorrido, y que se '
                                                     'restablece solo al volver la válvula a su posición normal (NFPA 25, 13.3.3.5.1 y 13.3.3.5.2).'),
    ]))
    a(('p', 'En los sistemas de tubería seca y de acción previa que usan nitrógeno para conservar el coeficiente de rugosidad de '
            'diseño, la NFPA 25 (13.4.3.2.15 y 13.4.5.2.10) exige verificar cada semestre que la concentración de nitrógeno es del '
            '**98 %** o mayor.'))
    a(('p', cierre(5)))

    a(('h4', 'Prueba anual'))
    a(('p', 'La prueba anual tiene como finalidad verificar el disparo de las válvulas de los sistemas de tubería seca, de acción '
            'previa y de diluvio, la protección contra heladas y la ausencia de obstrucciones en la red.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Bloqueo de tuberías', 'controlar si se presentan condiciones que indican obstrucción; si se detecta alguna, examinar la red '
                                'de inmediato y repetir el examen cada **5 años** (NFPA 25, 14.3.2.1).'),
        ('Anticongelante (tubería húmeda)', 'antes de la temporada de heladas, medir el peso específico con un hidrómetro o un '
                                            'refractómetro y ajustar la solución para mantener su punto de congelamiento por debajo '
                                            'de la temperatura mínima estimada; anotar el punto de solidificación.'),
        ('Disparo de la válvula de tubería seca', 'en primavera, después del tiempo de heladas, con la válvula de corte ligeramente '
                                                  'abierta; anotar el tiempo entre la apertura de la válvula de prueba de inspección '
                                                  'y el disparo de la válvula.'),
        ('Inspección interna de la válvula de tubería seca', 'verificar que todos los componentes actúan adecuadamente, se mueven '
                                                             'libremente y están en buenas condiciones, y limpiar su interior '
                                                             '(NFPA 25, 13.4.5.3.1).'),
        ('Abastecimiento de aire comprimido', 'probarlo según las instrucciones del fabricante; al recargar el sistema, el '
                                              'abastecimiento debe restablecer la presión normal en **30 min** como máximo, o en '
                                              '**60 min** en espacios refrigerados por debajo de −15 °C (NFPA 25, 13.4.5.2.2.4).'),
        ('Alarmas de presión de aire y de baja temperatura', 'probar las alarmas de alta y baja presión de aire y de baja temperatura '
                                                             'del recinto de la válvula (NFPA 25, 13.4.5.2.6 y 13.4.5.2.7).'),
        ('Sistema de acción previa', 'probar el disparo del sistema según las instrucciones del fabricante, incluidos el accionamiento '
                                     'automático y el manual, e inspeccionar internamente la válvula.'),
        ('Sistema de diluvio', 'probar el disparo, anotar el tiempo de operación y el tiempo desde la activación del detector hasta '
                               'la descarga, observar la descarga, verificar que los rociadores no están obstruidos y que la '
                               'cobertura es correcta, registrar las presiones en la válvula de diluvio y en el rociador '
                               'hidráulicamente más desfavorable e inspeccionar internamente la válvula.'),
        ('Válvulas de control', 'operar cada válvula hasta su máximo recorrido, volverla a su posición normal y precintarla o '
                                'enclavarla (NFPA 25, 13.3.3.1).'),
    ]))
    a(('p', 'Las condiciones que indican obstrucción de la red, según la IRAM 3546:2011 y la NFPA 25 (14.3.1), son las siguientes:'))
    a(('items', [
        ['aspiración defectuosa de la bomba cuando se alimenta de un canal, pozo o lago;',
         'descarga de residuos durante las pruebas de agua, como la prueba de drenaje;',
         'residuos encontrados en válvulas de tubería seca, válvulas de retención o bombas;',
         'fuerte coloración del agua en las pruebas de drenaje o en la conexión de prueba de inspección;',
         'residuos encontrados al desconectar un rociador, o rociadores obstruidos;',
         'tuberías atascadas después de una modificación o de una actuación durante un incendio;',
         'falta de lavado de los colectores después de una instalación o reparación, o roturas de la red pública cercana;',
         'disparos falsos y frecuentes de las válvulas de tubería seca;',
         'puesta en servicio de un sistema parado durante más de un año;',
         'sospecha de silicato de sodio o sus derivados en las tuberías;',
         'abastecimiento con agua no tratada a través de la toma de impulsión para bomberos;',
         'pérdidas por picaduras causadas por corrosión interna;',
         'aumento del **25 %** del tiempo de llegada del agua a la conexión de prueba en sistemas de tubería seca, respecto de la '
         'prueba de aceptación.'],
    ]))
    a(('p', 'Si la solución anticongelante es de un tipo que ya no está permitido o no se puede identificar, el sistema se debe '
            'drenar y llenar con una solución listada; las muestras se toman en la parte superior y en la inferior del sistema, y en '
            'el punto más remoto y en la conexión con la red de agua cuando no coinciden con aquellas (NFPA 25, 5.3.4). Los glicoles '
            'dietilénico, etilénico y propilénico están prohibidos en cañerías de CPVC (NFPA 25, 5.3.4.3.1.1). El uso de soluciones '
            'anticongelantes debe cumplir las reglamentaciones sanitarias locales.'))
    a(('p', 'La IRAM 3546:2011 indica en el texto que el manómetro de la prueba del sistema de diluvio se instala en el rociador '
            'hidráulicamente «más favorable», mientras que la planilla 3546-7F pide la presión en el «más desfavorable». Se adopta el '
            'más desfavorable, coincidente con la NFPA 25 (13.4.4.2.7.1), que exige registrar la presión en la boquilla o rociador '
            'hidráulicamente más remoto y una segunda lectura en la válvula de diluvio, y compararlas con las presiones de diseño. '
            'Cuando el agua no se puede descargar, la prueba se realiza sin descarga, por ejemplo cerrando la válvula del '
            'abastecimiento, y la prueba con caudal total se realiza en la siguiente parada programada, con un intervalo no mayor '
            'que **3 años** (NFPA 25, 13.4.4.2.3).'))
    a(('p', cierre(6)))
    a(('protocol', ('prueba anual de disparo de la válvula de tubería seca', [
        ('Lavado previo', [
            ('Paso a paso', 'notificar al servicio de supervisión, abrir totalmente el drenaje principal y dejar fluir el agua hasta '
                            'que salga limpia; si hay hidrantes conectados al abastecimiento, hacerlos fluir antes.'),
            ('Justificación técnica', 'reduce la cantidad de residuos que pueden ingresar en las tuberías secas.'),
            ('Criterio de aceptación', 'agua limpia en el drenaje.')]),
        ('Disparo', [
            ('Paso a paso', 'con la válvula de corte del abastecimiento ligeramente abierta, abrir la válvula de prueba de inspección '
                            'y medir con cronómetro el tiempo hasta el disparo; anotar la presión de aire de disparo y la presión de '
                            'agua inicial. En cuanto la válvula se dispara, cerrar la válvula de corte.'),
            ('Justificación técnica', 'la apertura parcial evita inundar el sistema; algunas válvulas necesitan caudal suficiente '
                                      'para levantar completamente la clapeta.'),
            ('Criterio de aceptación', 'disparo con una presión de aire y en un tiempo comparables con los de la prueba de '
                                       'aceptación y los de pruebas anteriores.')]),
        ('Limpieza y rearme', [
            ('Paso a paso', 'abrir el drenaje de 50,8 mm y vaciar el sistema, quitar la tapa de la válvula, limpiar su interior, '
                            'reponer las partes dañadas, rearmar la válvula sin aplicar grasa ni selladores en los asientos '
                            '(NFPA 25, 13.4.5.2.3), colocar la tapa y agregar el agua de cebado.'),
            ('Justificación técnica', 'la limpieza anual del interior evita el pegado de la clapeta.'),
            ('Criterio de aceptación', 'componentes que se mueven libremente y en buenas condiciones.')]),
        ('Puesta en servicio', [
            ('Paso a paso', 'abrir el abastecimiento de aire y presurizar el sistema; alcanzada la presión normal, abrir el drenaje '
                            'de 50,8 mm, abrir totalmente la válvula de corte y cerrar lentamente el drenaje. Colocar en la válvula '
                            'la tarjeta con la fecha del disparo y el nombre de la persona y de la organización que realizó la '
                            'prueba (NFPA 25, 13.4.5.2.5).'),
            ('Justificación técnica', 'el drenaje abierto durante la apertura del agua reduce el golpe de ariete que puede hacer '
                                      'saltar la válvula.'),
            ('Criterio de aceptación', 'presión de aire normal restablecida en **30 min** como máximo y válvula de corte abierta y '
                                       'precintada.')]),
    ])))

    a(('h4', 'Prueba de tres años'))
    a(('p', 'La prueba de tres años tiene como finalidad verificar el disparo con caudal total de la válvula de tubería seca y la '
            'estanqueidad de las redes presurizadas con aire.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Disparo a caudal total de la válvula de tubería seca', 'realizar la prueba con la válvula del abastecimiento totalmente '
                                                                 'abierta y el dispositivo de apertura rápida en servicio, abriendo '
                                                                 'la válvula de prueba de inspección; anotar el tiempo entre la '
                                                                 'apertura y el comienzo de la salida de agua, y dar la prueba por '
                                                                 'terminada cuando fluya agua limpia por la conexión de prueba.'),
        ('Sistemas modificados o ampliados', 'realizar la prueba completa de disparo cada vez que el sistema se modifique o se amplíe.'),
        ('Disparo a caudal total de la válvula de acción previa', 'realizar la prueba con la válvula de control totalmente abierta '
                                                                  '(NFPA 25, 13.4.3.2.2).'),
        ('Pérdida de aire (tubería seca y acción previa)', 'presurizar con aire o nitrógeno a **2,8 bar** (40 psi) durante **2 h**; '
                                                           'la pérdida admisible es de **0,2 bar** (3 psi) y, si es mayor, se '
                                                           'deben reparar las fugas. Como alternativa, con el sistema a su presión '
                                                           'normal se corta el abastecimiento de gas durante **4 h**: si actúa la '
                                                           'alarma de baja presión, se deben reparar las fugas (NFPA 25, 13.4.3.2.6 '
                                                           'y 13.4.5.2.9).'),
    ]))
    a(('p', 'Los registros del tiempo de disparo y del tiempo de llegada del agua a la conexión de prueba se deben conservar para '
            'compararlos con la prueba de aceptación (NFPA 25, 13.4.5.2.5.2); un aumento del 25 % de ese tiempo obliga a investigar '
            'obstrucciones.'))
    a(('p', cierre(7)))

    a(('h4', 'Pruebas de cinco, veinte y cincuenta años'))
    a(('p', 'Estas pruebas tienen como finalidad verificar que los rociadores conservan su respuesta térmica a lo largo de su vida '
            'útil y que los instrumentos del sistema mantienen su exactitud.'))
    a(('p', 'Cada **5 años** se debe realizar:'))
    a(('items', [
        ('Rociadores de temperatura extra alta', 'retirar una muestra representativa de los rociadores de **163 °C** o más situados '
                                                 'en áreas sometidas en forma continua o periódica a la máxima temperatura ambiente '
                                                 'esperada, reponerlos con rociadores nuevos del mismo rango y enviar los retirados '
                                                 'a un laboratorio; si alguno falla, se sustituyen todos los rociadores de esa '
                                                 'clasificación.'),
        ('Manómetros', 'comparar cada manómetro con uno calibrado; los que se desvíen más del **3 %** de la escala completa se deben '
                       'recalibrar o sustituir (NFPA 25, 13.2.4.2 y 13.2.4.3).'),
        ('Limpieza de tuberías', 'si es necesario, limpiar las tuberías con flujo pleno de agua.'),
        ('Evaluación interna de la red', 'evaluar el estado interno de las cañerías para detectar material orgánico o inorgánico '
                                         'extraño (NFPA 25, 14.2.1.1); si se encuentran tubérculos o limo, se deben analizar para '
                                         'detectar corrosión inducida por microorganismos.'),
        ('Ambientes agresivos', 'ensayar una muestra de los rociadores expuestos a ambientes corrosivos, o reemplazarlos '
                                '(NFPA 25, 5.3.1.1.2).'),
    ]))
    a(('p', 'Cada **10 años**, desde los **20 años** de instalados, se debe realizar:'))
    a(('items', [
        ('Rociadores de respuesta rápida', 'probar una muestra representativa a los **20 años** de instalados y repetir la prueba '
                                           'cada **10 años**. La NFPA 25 (5.3.1.1.1.1) fija **25 años** para los de respuesta rápida '
                                           'y **20 años** para los ESFR y CMSA; se adopta el plazo de 20 años de la IRAM 3546:2011, '
                                           'más exigente.'),
        ('Rociadores secos', 'reemplazarlos o ensayar una muestra a los **20 años** de instalados y repetir el ensayo cada '
                             '**10 años** (NFPA 25, 5.3.1.1.1.5).'),
    ]))
    a(('p', 'A los **50 años** de instalados se debe retirar una muestra representativa de los rociadores, sustituirla por rociadores '
            'nuevos y enviar los retirados a un laboratorio; si fallan, se cambian todos los rociadores por otros nuevos de las '
            'mismas características. Después de esta prueba, el ensayo se repite cada **10 años**; a los **75 años**, cada **5 años** '
            '(NFPA 25, 5.3.1.1.1.4). Los rociadores fabricados antes de 1920 se deben sustituir.'))
    a(('p', 'Una muestra representativa consiste en la mayor de las opciones siguientes: dos rociadores por planta o sistema '
            'individual, o como mínimo cuatro rociadores o el **1 %** del número de rociadores de cada sistema individual, lo que '
            'resulte mayor. Si un rociador de la muestra falla, se reemplazan todos los rociadores del área representada por esa '
            'muestra (NFPA 25, 5.3.1.2 y 5.3.1.3).'))
    a(('p', cierre(9)))

    # ---------------- MANTENIMIENTO ----------------
    a(('h3', 'MANTENIMIENTO'))
    a(('p', 'El mantenimiento debe asegurar que todos los componentes y equipos que forman el sistema estén operativos y confiables, '
            'y se debe realizar inmediatamente después de las pruebas que detectan fallas.'))

    a(('h4', 'Mantenimiento mensual'))
    a(('p', 'El mantenimiento mensual tiene como finalidad evitar que los depósitos alteren la respuesta de los rociadores en áreas '
            'de pintura por pulverización.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Áreas de pintura pulverizada', 'inspección de los rociadores para prevenir depósitos sobre ellos. Los rociadores pueden '
                                         'protegerse con bolsas de celofán de **0,076 mm** de espesor como máximo o con bolsas de '
                                         'papel, que se retiran y sustituyen cuando acumulan residuos (NFPA 25, 5.4.1.10.2).'),
    ]))
    a(('p', cierre(3)))

    a(('h4', 'Mantenimiento trimestral'))
    a(('p', 'El mantenimiento trimestral tiene como finalidad conservar la operabilidad de las válvulas de poste indicador y de '
            'husillo ascendente y puente fijo.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Recorrido de las válvulas', 'operación de las válvulas en todo su recorrido y retorno a la posición normal. Al abrirlas, el '
                                      'volante se gira hasta que no se note resistencia en el husillo, lo que asegura que el husillo '
                                      'no se ha desprendido de la compuerta; luego se retrocede un cuarto de vuelta desde la '
                                      'apertura total para prevenir obstrucciones y se enclava la válvula.'),
    ]))
    a(('p', cierre(4)))

    a(('h4', 'Mantenimiento anual'))
    a(('p', 'El mantenimiento anual tiene como finalidad lubricar las válvulas, limpiar los filtros y eliminar la condensación de '
            'los sistemas de tubería seca.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Vástagos de las válvulas', 'lubricación con grafito o suspensión de grafito con aceite liviano, abriendo y cerrando la '
                                     'válvula para distribuir el lubricante (NFPA 25, 13.3.4.1 y 13.3.4.2).'),
        ('Filtros', 'limpieza de los filtros, con cierre del abastecimiento y retiro del filtro; algunos filtros son autolimpiantes y '
                    'solo requieren la rotación de un volante.'),
        ('Puntos bajos de drenaje (tubería seca)', 'drenaje de todos los puntos bajos, repetido diariamente hasta que desaparezca la '
                                                    'condensación; la NFPA 25 (13.4.5.3.3) exige además drenarlos después de cada '
                                                    'operación del sistema y al comienzo de la temporada de calefacción.'),
        ('Rociadores de cocinas', 'sustitución de los rociadores de eslabón fusible y de las boquillas pulverizadoras que protegen las '
                                  'cocinas y sus conductos de extracción; los de tipo bulbo que en el examen anual no muestren acumulación '
                                  'de grasa u otros materiales no requieren sustitución (NFPA 25, 5.4.1.8 y 5.4.1.8.1).'),
    ]))
    a(('p', cierre(6)))

    a(('h4', 'Mantenimiento quinquenal'))
    a(('p', 'El mantenimiento quinquenal tiene como finalidad verificar internamente las válvulas que permanecen cerradas sobre su '
            'asiento durante largos períodos.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Válvulas de alarma de tubería húmeda', 'inspección interna, verificando que todos sus componentes operan adecuadamente, se '
                                                 'mueven libremente y están en buenas condiciones (NFPA 25, 13.4.1.2).'),
        ('Válvulas de retención', 'inspección interna con el mismo criterio (NFPA 25, 13.4.2.1).'),
        ('Filtros y orificios restringidos', 'inspección interna de los filtros, orificios restringidos y cámaras de diafragma de '
                                             'las válvulas de tubería seca, de acción previa y de diluvio (NFPA 25, 13.4.3.1.3, '
                                             '13.4.4.1.3 y 13.4.5.1.4).'),
        ('Toma de impulsión para bomberos', 'prueba hidrostática de la cañería entre la toma y su válvula de retención a **10 bar** '
                                            '(150 psi) durante **2 h**, con una pérdida menor que **0,3 bar** (5 psi) y sin '
                                            'pérdidas visibles (NFPA 25, 13.8.5).'),
    ]))
    a(('p', cierre(8)))

    # ---------------- COMPLEMENTARIAS ----------------
    a(('h3', 'PUESTA FUERA DE SERVICIO'))
    a(('p', 'La puesta fuera de servicio tiene como finalidad limitar el riesgo y la duración de cualquier interrupción de la '
            'protección, programada o de emergencia, según el capítulo 15 de la NFPA 25.'))
    a(('p', 'Antes de autorizar una puesta fuera de servicio programada se debe asegurar:'))
    a(('items', [
        ('Coordinador', 'designación de un coordinador por el propietario o su representante; en su ausencia, el coordinador es el '
                        'propietario.'),
        ('Alcance', 'determinación de la extensión y la duración prevista, inspección de las áreas afectadas y evaluación del '
                    'aumento del riesgo.'),
        ('Medidas compensatorias', 'cuando el sistema quede fuera de servicio más de **10 h** en un período de **24 h**, evacuación '
                                   'del sector afectado, guardia de incendio aprobada, abastecimiento de agua provisorio o un '
                                   'programa aprobado para eliminar fuentes de ignición y limitar la carga combustible.'),
        ('Avisos', 'notificación al servicio de bomberos, a la aseguradora, a la empresa de monitoreo, a la autoridad competente y a '
                   'los responsables de las áreas afectadas.'),
        ('Tarjeta de fuera de servicio', 'colocación de una tarjeta en cada toma de impulsión para bomberos y en la válvula de control '
                                         'del sistema, indicando qué sistema o parte está fuera de servicio.'),
        ('Recursos', 'disponibilidad en el lugar de las herramientas y los materiales necesarios.'),
    ]))
    a(('p', 'Las interrupciones de emergencia, como un corte del abastecimiento, una cañería congelada o rota o una falla de un '
            'equipo, incluidas las detectadas durante la inspección, prueba o mantenimiento, siguen los mismos pasos. Al restablecer '
            'el sistema se deben realizar las inspecciones y pruebas que verifiquen su funcionamiento, informar a todas las partes '
            'notificadas y retirar la tarjeta.'))

    a(('h3', 'SEGURIDAD Y SALUD OCUPACIONAL'))
    a(('p', 'La seguridad del personal tiene como finalidad evitar riesgos de caída, hidráulicos y eléctricos durante la inspección y '
            'las pruebas.'))
    a(('p', 'Durante las tareas se debe asegurar:'))
    a(('items', [
        ('Trabajo en altura', 'uso de escaleras o plataformas adecuadas y de los elementos de protección contra caídas para acceder a '
                              'rociadores, cañerías y soportes.'),
        ('Descarga de agua', 'delimitación del área de descarga del drenaje y de la conexión de prueba, y control de que el agua no '
                             'alcance equipos energizados ni bienes sensibles.'),
        ('Presión almacenada', 'despresurización del sistema antes de abrir tapas de válvulas, desmontar rociadores o intervenir '
                               'compresores y recipientes de aire.'),
        ('Partes eléctricas', 'intervención en interruptores de flujo, presostatos y centrales solo con los circuitos desenergizados '
                              'o con los elementos de protección personal adecuados, según el procedimiento de trabajo eléctrico '
                              'seguro de la instalación.'),
        ('Rociadores retirados', 'embalaje e identificación de los rociadores enviados a laboratorio, indicando su ubicación, sin '
                                 'manipular el elemento sensible.'),
    ]))

    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'Los cambios en el uso del área, en la altura y el tipo de almacenamiento, en los cielorrasos o en la distribución de '
            'los ambientes pueden dejar al sistema fuera de su base de diseño. Toda modificación se debe evaluar técnicamente antes '
            'de su ejecución y registrar en la planilla de información general; después de cada modificación o ampliación se realiza '
            'una prueba completa de disparo.'))
    a(('p', 'La empresa mantenedora es responsable de ejecutar las tareas de inspección, prueba y mantenimiento y de verificar las '
            'inspecciones de autocontrol. El usuario o propietario es responsable de completar las inspecciones de autocontrol, de '
            'mantener la distancia libre bajo los rociadores, de conservar los registros y de coordinar las puestas fuera de servicio.'))
    return C


def REGISTRO_EXTRA(cierre):
    return [
        'Los datos de la instalación, de las válvulas, del abastecimiento de agua, de las bombas contra incendio, de la toma de '
        'impulsión para bomberos y de cada tipo de sistema se registran en la planilla SG-PEM-IFI-%s-1 %s – %s.' % (SIG, NOM, PL[1]),
        'Se recomienda que cada válvula de control tenga una tarjeta con la fecha de sellado o enclavamiento, y que cada válvula de '
        'alarma, de tubería seca, de acción previa o de diluvio tenga una tarjeta con la fecha y la información del último '
        'mantenimiento o disparo.',
        'Los planos conforme a obra, el cálculo hidráulico, los registros de la prueba de aceptación y las hojas de datos de los '
        'dispositivos se deben conservar durante toda la vida útil del sistema (NFPA 25, 4.3.4). Los registros pueden conservarse '
        'en formato electrónico (NFPA 25, 4.3.1.2).',
        'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '
        'codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables se indican con NA. Toda '
        'condición O o X se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y '
        'por el responsable de la instalación, con su aclaración.',
    ]
