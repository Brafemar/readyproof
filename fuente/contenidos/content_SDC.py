# -*- coding: utf-8 -*-
SIG, NOM, NOMU, CAP = 'SDC', 'Sistema de Extinción por Dióxido de Carbono', 'SISTEMA DE EXTINCIÓN POR DIÓXIDO DE CARBONO (CO₂)', '18'
PL = {1: 'Información general', 2: 'Inspección mensual', 3: 'Prueba y mantenimiento anual',
      4: 'Control de peso de cilindros', 5: 'Prueba quinquenal'}
VIG = (' Se aplica la edición vigente de cada norma NFPA; la numeración de los artículos citados se debe confirmar en esa '
       'edición, porque puede variar entre ediciones.')


def CONTENT(cierre):
    C = []; a = C.append
    a(('h2', NOMU))
    a(('basado', '(Basado en IRAM 3546:2011 – Capítulo %s; criterios complementarios: NFPA 12)' % CAP))
    a(('p', 'Este apartado establece los requisitos mínimos para la inspección, prueba y mantenimiento del sistema fijo de extinción '
            'por dióxido de carbono, con el objetivo de asegurar que el sistema descargue la cantidad de agente prevista y alcance la '
            'concentración de diseño en el riesgo protegido, y de proteger la vida de las personas que puedan quedar expuestas al agente.'))
    a(('p', 'La IRAM 3546:2011 es la base del presente procedimiento y fija sus frecuencias. La NFPA 12, Norma sobre sistemas '
            'extintores de dióxido de carbono, se aplica como criterio complementario para la seguridad del personal, los valores de '
            'aceptación y las tareas que la IRAM no contempla. Ante diferencias, se adopta siempre la condición más exigente.' + VIG))
    a(('p', 'El dióxido de carbono extingue el fuego principalmente por reducción de la concentración de oxígeno, con un efecto '
            'complementario de enfriamiento. Las concentraciones de diseño de inundación total (34 % o más) son letales para las '
            'personas: el CO₂ no es un agente apto para recintos ocupados durante la descarga, y la seguridad del personal es la '
            'primera condición de toda intervención sobre el sistema (NFPA 12, 4.3).'))
    a(('p', 'El sistema puede ser de alta presión, con cilindros a temperatura ambiente, o de baja presión, con un depósito '
            'refrigerado a **2,1 MPa**, y de inundación total o de aplicación local. El equipamiento del sistema incluye:'))
    a(('items', [
        ('Almacenamiento del agente', 'cilindros de alta presión con sus válvulas de descarga, o depósito de baja presión con su '
                                      'equipo de refrigeración e indicadores de nivel y de presión.'),
        ('Accionamiento', 'cabezales de control eléctricos, neumáticos o mecánicos, cilindros piloto de nitrógeno y disparadores '
                          'manuales locales y remotos.'),
        ('Distribución', 'conexiones flexibles, colector, válvulas direccionales, red de cañerías y boquillas.'),
        ('Válvula de bloqueo', 'válvula manual supervisada que impide el paso del agente al recinto durante el mantenimiento o cuando '
                               'hay personas en él.'),
        ('Detección y control', 'detectores, panel de control y extinción, interruptor de servicio, retardos y presostato de descarga.'),
        ('Alarmas y señalización', 'alarmas de predescarga acústicas neumáticas y eléctricas, alarmas visuales, carteles de '
                                   'advertencia y dispositivos de cierre automático de puertas, trampas y ventilación.'),
    ]))
    a(('p', 'Donde se cuente con un servicio de supervisión, para evitar falsas alarmas se debe notificar al personal de ese servicio '
            'antes de realizar cualquier prueba o acción que pueda generar una alarma y luego de concluir las tareas.'))

    # ---------------- SEGURIDAD (primero) ----------------
    a(('h3', 'SEGURIDAD DEL PERSONAL'))
    a(('p', 'Las medidas de seguridad tienen como finalidad evitar que una descarga, prevista o accidental, alcance a personas dentro '
            'del recinto protegido o en espacios adyacentes. Se deben aplicar antes de cualquier inspección, prueba o mantenimiento.'))
    a(('p', 'Según la NFPA 12, se debe asegurar:'))
    a(('items', [
        ('Bloqueo del sistema', 'durante el mantenimiento o las pruebas, el sistema se debe bloquear mediante la válvula de bloqueo, '
                                'o el recinto protegido y los espacios a los que el agente pueda migrar se deben evacuar '
                                '(4.3.3.4.5). El interruptor de servicio del panel no reemplaza a la válvula de bloqueo (4.3.3.4.4).'),
        ('Guardia de incendio', 'cuando la protección se deba mantener durante el bloqueo, se debe asignar una guardia de incendio con '
                                'equipos portátiles o semiportátiles o con medios para restituir la protección, comunicada con un '
                                'lugar atendido en forma permanente; las autoridades responsables de la protección se deben notificar '
                                'del bloqueo y del restablecimiento (4.3.3.4.6).'),
        ('Migración del agente', 'el CO₂ es más pesado que el aire y puede derivar y acumularse en sótanos, fosos y espacios adyacentes, '
                                 'y también a partir de la descarga de un dispositivo de alivio del depósito (4.3.1.1 y 4.3.1.2).'),
        ('Ingreso al recinto', 'después de una descarga no debe ingresar personal sin protección hasta que el recinto se haya '
                               'ventilado y una medición de la atmósfera haya verificado que es segura; las personas que no estén '
                               'entrenadas y equipadas con equipo de respiración autónomo no deben permanecer donde la concentración '
                               'supere el **4 %** (4.3.3.1.1).'),
        ('Evacuación y rescate', 'medios para la evacuación inmediata, para impedir el ingreso a atmósferas peligrosas y para el '
                                 'rescate de personas atrapadas, y capacitación del personal (4.3.1.3.1 y 4.3.1.3.2).'),
        ('Información', 'todas las personas que puedan ingresar en el recinto deben conocer los riesgos y los procedimientos de '
                        'evacuación; la descarga directa contra una persona puede causar lesiones en ojos y oídos o caídas por la '
                        'pérdida del equilibrio (4.3.3.1 y 4.3.3.3).'),
        ('Cilindros', 'transporte de cilindros según procedimientos de manipulación segura (4.3.3.5), con el capuchón de '
                      'protección de la válvula colocado.'),
    ]))
    a(('p', 'En cada recinto protegido, en cada ingreso y en cada estación de accionamiento manual deben estar colocados los carteles '
            'de advertencia de la NFPA 12 (4.3.2). El cartel del ingreso indica, en traducción técnica: «ADVERTENCIA. El gas dióxido de '
            'carbono puede causar lesiones o la muerte. Cuando opere la alarma, no ingresar hasta que el recinto esté ventilado».'))
    a(('p', 'Antes de cada prueba se deben revisar los procedimientos de seguridad (NFPA 12, 4.8.3.2.3). Las personas que inspeccionan, '
            'prueban, mantienen u operan el sistema deben estar capacitadas en las funciones que realizan (NFPA 12, 4.8.4).'))

    # ---------------- INSPECCIÓN ----------------
    a(('h3', 'INSPECCIÓN'))
    a(('p', 'La inspección consiste en un examen visual del sistema y de sus componentes, para verificar que está en condiciones '
            'aparentes de operación y libre de daños físicos. Se realiza generalmente en cada planta, recorriendo las zonas protegidas.'))
    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica previa '
            'de la instalación según la IRAM 3619; esta evaluación no es obligatoria y puede ser solicitada por cualquiera de las '
            'partes interesadas.'))

    a(('h4', 'Inspección semanal de depósitos de baja presión (autocontrol)'))
    a(('p', 'Esta inspección tiene como finalidad detectar a tiempo la pérdida de agente en los depósitos de baja presión.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Nivel de líquido', 'observar los indicadores de nivel de los depósitos de baja presión como mínimo una vez por semana; si '
                             'la pérdida supera el **10 %**, el depósito se debe rellenar, salvo que se sigan cubriendo las cantidades '
                             'mínimas de agente requeridas (NFPA 12, 4.8.3.6).'),
    ]))
    a(('p', 'La NFPA 12 exige esta observación semanal, más exigente que la mensual de la IRAM 3546:2011, y se adopta. Se registra en '
            'la planilla de inspección mensual del período.'))
    a(('p', cierre(2)))

    a(('h4', 'Inspección mensual'))
    a(('p', 'La inspección mensual tiene como finalidad verificar el estado de los componentes, la cantidad de agente y la '
            'integridad del recinto protegido. La NFPA 12 (4.8.1) exige una inspección del estado operativo como mínimo cada '
            '**30 días**.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Boquillas y aberturas', 'comprobar que las boquillas no están dañadas ni obstruidas.'),
        ('Cierre de aberturas', 'comprobar que todas las puertas del local protegido tienen muelles de autocierre o se cierran '
                                'automáticamente al activarse el sistema de inundación total.'),
        ('Riesgo protegido', 'comprobar que no hubo cambios en el volumen ni en el tipo de riesgo del local.'),
        ('Peso de agente en baja presión', 'observar el indicador de peso de cada depósito de baja presión y rellenar si la pérdida '
                                           'supera el **10 %** de su capacidad.'),
        ('Presión en baja presión', 'comprobar que la presión del depósito es de **2,1 MPa** con una tolerancia de **± 3 %**.'),
        ('Refrigeración', 'comprobar que el equipo compresor de refrigeración tiene alimentación eléctrica.'),
        ('Cilindros piloto de nitrógeno', 'comprobar que la presión es correcta y recargarlos si es menor que el **90 %** de la nominal.'),
        ('Componentes', 'inspeccionar todos los componentes del sistema para detectar pérdidas o daños visibles.'),
        ('Seguridad', 'comprobar que la válvula de bloqueo está en su posición normal y supervisada, y que los carteles de advertencia '
                      'están colocados y legibles.'),
    ]))
    a(('p', cierre(2)))

    # ---------------- PRUEBA ----------------
    a(('h3', 'PRUEBA'))
    a(('p', 'Las pruebas tienen como propósito verificar la cantidad de agente, la secuencia completa de detección, alarma, retardo y '
            'disparo, y la integridad de los componentes sometidos a presión, sin producir la descarga de CO₂. Todas las pruebas se '
            'realizan con el sistema bloqueado o con los cabezales de control desconectados, y con el recinto evacuado.'))

    a(('h4', 'Prueba semestral de peso de cilindros de alta presión'))
    a(('p', 'Esta prueba tiene como finalidad verificar la carga neta de cada cilindro de alta presión.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Peso de los cilindros', 'pesar todos los cilindros de alta presión, por los indicadores de control de peso o desmontándolos, '
                                  'y anotar la fecha de la última prueba hidrostática (NFPA 12, 4.8.3.5.1).'),
        ('Pérdida admisible', 'si la carga neta es menor que el **90 %** de la nominal, es decir, si la pérdida supera el **10 %**, '
                              'completar la carga o reemplazar el cilindro y rearmar el sistema (NFPA 12, 4.8.3.5.2).'),
        ('Etiqueta', 'colocar en cada cilindro una etiqueta con el peso del cilindro completo y la fecha.'),
    ]))
    a(('p', 'La IRAM 3546:2011 establece el pesaje en la prueba anual; la NFPA 12 lo exige como mínimo cada seis meses, y se adopta la '
            'frecuencia semestral, más exigente. Para pesar un cilindro se desconecta su válvula de descarga del sistema de tuberías, '
            'se retira el cilindro cuidando la válvula, se pesa y se resta el peso del cilindro vacío grabado en su cuerpo; el peso '
            'resultante debe ser igual al peso nominal de CO₂ según la relación de llenado.'))
    a(('p', cierre(4)))

    a(('h4', 'Prueba anual'))
    a(('p', 'La prueba anual tiene como finalidad verificar la secuencia completa de operación del sistema mediante la prueba en blanco, '
            'el estado de los componentes y la carga de agente.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Indicios de fuga y daños', 'comprobar la ausencia de indicios de fuga en los cilindros y de daños físicos en los componentes.'),
        ('Cilindros piloto de nitrógeno', 'comprobar que la presión es como mínimo el **90 %** de la nominal.'),
        ('Válvulas direccionales', 'comprobar su accionamiento.'),
        ('Actuadores de las válvulas de descarga', 'retirar los cabezales de control, activar los detectores o los pulsadores manuales '
                                                   'y comprobar la secuencia completa y que el émbolo del cabezal se desplace '
                                                   'totalmente; en sistemas neumáticos o mecánicos, probar la estanqueidad de las '
                                                   'líneas o la correcta transmisión de fuerza.'),
        ('Conexiones flexibles', 'comprobar que no están dañadas ni corroídas.'),
        ('Prueba en blanco', 'con el cabezal de control desconectado, verificar todas las funciones del panel de control, la '
                             'alimentación eléctrica normal y de emergencia, los detectores, los retardos, las alarmas, los '
                             'dispositivos de cierre de puertas y trampas, el equipo de disparo y los accionadores manuales, y '
                             'controlar las tuberías, las boquillas y el almacenamiento de agente.'),
        ('Soplado de las líneas de descarga', 'verificar que las cañerías están libres de obstrucciones.'),
        ('Alarmas del espacio protegido', 'comprobar la actuación de las alarmas acústicas y visuales.'),
        ('Refrigeración (baja presión)', 'verificar el sistema de refrigeración según las indicaciones del fabricante.'),
    ]))
    a(('p', 'La NFPA 12 (4.8.3.2) exige verificar además, como mínimo una vez al año, con la documentación del sistema:'))
    a(('items', [
        ['la operación del sistema de CO₂;', 'que no hubo cambios en el tamaño, el tipo y la configuración del riesgo y del sistema;',
         'la operación de todos los retardos;', 'la operación de todas las alarmas audibles;', 'la operación de todas las señales visibles;',
         'que todos los carteles de advertencia están colocados según 4.3.2;',
         'que los procedimientos y dispositivos de alarma y retardo de 4.5.6 son adecuados y operables;',
         'cada detector, con los métodos de la NFPA 72.'],
    ]))
    a(('p', 'Las alarmas de predescarga y los retardos se consideran aceptables cuando cumplen la NFPA 12 (4.5.6):'))
    a(('items', [
        ('Alarmas distintivas', 'alarmas acústicas y visuales del sistema de CO₂ distintas de todas las demás, incluida la alarma de '
                                'incendio del edificio (4.5.6.1).'),
        ('Retardo', 'tiempo de retardo suficiente para que las personas de los lugares más alejados de las salidas evacúen el recinto, '
                    'determinado mediante simulacros (4.5.6.2.2 y 4.5.6.2.5).'),
        ('Nivel sonoro', 'alarma de predescarga como mínimo **15 dB** sobre el ruido ambiente o **5 dB** sobre el nivel máximo, lo '
                         'que sea mayor, medido a 1,5 m del piso, con un mínimo de **90 dBA** a 3 m y no más de 120 dB a la distancia '
                         'mínima de audición (4.5.6.2.6).'),
        ('Alarmas exteriores', 'alarmas visuales y acústicas fuera de cada ingreso, que comienzan antes o al inicio de la descarga y se '
                               'mantienen hasta que el recinto se ventila y se verifica que la atmósfera es segura (4.5.6.3).'),
    ]))
    a(('p', 'La prueba con descarga real se realiza cuando el mantenimiento indique que es conveniente (NFPA 12, 4.8.3.2.2). Toda '
            'penetración realizada en un recinto protegido por inundación total se debe sellar de inmediato, restituyendo la '
            'resistencia al fuego original (NFPA 12, 4.8.3.4).'))
    a(('p', 'La planilla IRAM 3546-18C remite el registro del pesaje a una «planilla F» que el capítulo no incluye. Se interpreta '
            'que se refiere a la planilla de control de peso de cilindros (IRAM 3546-18D), en la que se registran el peso y la fecha '
            'de la última prueba hidrostática de cada cilindro.'))
    a(('p', cierre(3)))
    a(('protocol', ('prueba anual en blanco', [
        ('Bloqueo y evacuación', [
            ('Paso a paso', 'notificar al responsable de la instalación y al servicio de supervisión, evacuar el recinto, cerrar y '
                            'bloquear la válvula de bloqueo, desconectar los cabezales de control de las válvulas de los cilindros y '
                            'dejarlos libres para observar su carrera.'),
            ('Justificación técnica', 'el bloqueo mecánico del paso del agente es la única barrera que impide una descarga accidental '
                                      'sobre el personal; el interruptor de servicio no la reemplaza.'),
            ('Criterio de aceptación', 'válvula de bloqueo cerrada y señalizada, cabezales desconectados y recinto vacío.')]),
        ('Detección y alarmas', [
            ('Paso a paso', 'activar un detector de cada zona y luego los de la zona cruzada, si existe, y verificar la alarma de '
                            'primera etapa, la alarma de predescarga, la indicación en el panel y la transmisión al servicio de '
                            'supervisión.'),
            ('Justificación técnica', 'la alarma de predescarga es la que permite evacuar antes de la descarga.'),
            ('Criterio de aceptación', 'secuencia de alarmas según el diseño y niveles sonoros conformes a la NFPA 12.')]),
        ('Retardo y disparo', [
            ('Paso a paso', 'medir con cronómetro el tiempo de retardo, verificar la actuación de los cierres de puertas, trampas y '
                            'ventilación, y comprobar que los cabezales de control se disparan con el desplazamiento total del émbolo.'),
            ('Justificación técnica', 'el retardo debe alcanzar para la evacuación medida en los simulacros; los cierres son '
                                      'necesarios para mantener la concentración.'),
            ('Criterio de aceptación', 'retardo igual al de diseño, cierres operados y cabezales disparados.')]),
        ('Disparo manual', [
            ('Paso a paso', 'restablecer el panel y repetir el disparo desde cada accionador manual local y remoto.'),
            ('Justificación técnica', 'el disparo manual es el respaldo ante una falla de la detección.'),
            ('Criterio de aceptación', 'disparo de los cabezales desde cada accionador.')]),
        ('Rearme', [
            ('Paso a paso', 'restablecer el panel sin alarmas ni fallas, rearmar los cabezales de control, volver a conectarlos a las '
                            'válvulas, abrir la válvula de bloqueo, retirar los carteles de bloqueo y notificar la conclusión.'),
            ('Justificación técnica', 'un cabezal conectado antes de restablecer el panel puede producir una descarga.'),
            ('Criterio de aceptación', 'panel normal, cabezales conectados, válvula de bloqueo abierta y supervisada.')]),
    ])))

    a(('h4', 'Prueba quinquenal'))
    a(('p', 'La prueba quinquenal tiene como finalidad verificar la integridad de los componentes sometidos a presión y la '
            'operación del sistema antes de las pruebas hidrostáticas.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Prueba en blanco previa', 'realizarla antes de comenzar la prueba hidrostática de los cilindros o del depósito de baja '
                                    'presión, solo con personal entrenado y comprobando que nadie permanece en el local protegido.'),
        ('Panel, cabezales y válvulas de descarga', 'comprobar su funcionamiento como complemento de la prueba en blanco.'),
        ('Conexiones flexibles', 'probarlas hidrostáticamente a **17,5 MPa** en los sistemas de alta presión y a **6,3 MPa** en los '
                                 'de baja presión, y con mayor frecuencia si las inspecciones detectan daños o corrosión.'),
        ('Cilindros de alta presión', 'realizar las pruebas hidráulicas y revisiones periódicas según la IRAM 2529 (parte I), con '
                                      'procedimientos documentados, y registrarlas en la planilla de control de peso de cilindros.'),
        ('Red de cañerías', 'realizar la prueba neumática de la red de cañerías.'),
        ('Fecha de la última prueba general', 'registrarla.'),
    ]))
    a(('p', 'Las presiones de prueba de las conexiones flexibles de la IRAM 3546:2011 son levemente mayores que las de la NFPA 12 '
            '(4.8.2.1), que fija **17 239 kPa** (2500 psi) y **6205 kPa** (900 psi); se adoptan las de la IRAM. El procedimiento de la '
            'prueba sigue la NFPA 12 (4.8.2.2).'))
    a(('p', cierre(5)))
    a(('protocol', ('prueba hidrostática de conexiones flexibles', [
        ('Desmontaje', [
            ('Paso a paso', 'con el sistema bloqueado, desmontar la manguera de toda conexión; en mangueras de líneas manuales, '
                            'verificar la continuidad eléctrica entre los acoples.'),
            ('Justificación técnica', 'la prueba se realiza fuera del sistema para no presurizar componentes ajenos.'),
            ('Criterio de aceptación', 'manguera desmontada e identificada.')]),
        ('Presurización', [
            ('Paso a paso', 'colocar la manguera dentro de un recinto de protección que permita observarla, llenarla completamente '
                            'con agua, elevar la presión hasta la de prueba en **1 min** y mantenerla durante **1 min**.'),
            ('Justificación técnica', 'el llenado con agua evita la energía almacenada del gas comprimido en caso de rotura.'),
            ('Criterio de aceptación', 'sin caída de presión, sin movimiento de los acoples y sin pérdidas.')]),
        ('Evaluación', [
            ('Paso a paso', 'liberar la presión y observar la manguera; si no hay deformación permanente, se considera aprobada.'),
            ('Justificación técnica', 'una deformación permanente indica que el refuerzo de la manguera cedió.'),
            ('Criterio de aceptación', 'sin deformación permanente.')]),
        ('Secado y marcado', [
            ('Paso a paso', 'secar completamente el interior, con calor a no más de **66 °C** si se usa, y marcar en la manguera la '
                            'fecha de la prueba; las mangueras que fallan se marcan, se destruyen y se reemplazan por nuevas.'),
            ('Justificación técnica', 'la humedad interior produce corrosión y puede congelarse durante la descarga.'),
            ('Criterio de aceptación', 'manguera seca y marcada, o destruida y reemplazada.')]),
    ])))

    # ---------------- MANTENIMIENTO ----------------
    a(('h3', 'MANTENIMIENTO'))
    a(('p', 'El mantenimiento debe asegurar que todos los componentes del sistema estén operativos y confiables. El fabricante debe '
            'entregar al propietario un procedimiento de prueba y mantenimiento del sistema (NFPA 12, 4.8.3.1), que se aplica junto '
            'con este manual.'))
    a(('p', 'Durante las tareas de mantenimiento se debe realizar:'))
    a(('items', [
        ('Recarga', 'recarga o reemplazo de los cilindros con pérdida mayor que el 10 % y de los cilindros piloto con presión menor '
                    'que el 90 % de la nominal.'),
        ('Componentes', 'reparación o reemplazo de los componentes dañados o corroídos detectados en las inspecciones y pruebas.'),
        ('Recinto', 'sellado inmediato de toda penetración en el recinto protegido y verificación del cierre automático de aberturas.'),
        ('Informe', 'entrega al propietario de un informe de mantenimiento con recomendaciones (NFPA 12, 4.8.3.3).'),
    ]))
    a(('p', cierre(3)))

    # ---------------- COMPLEMENTARIAS ----------------
    a(('h3', 'PROCEDIMIENTO POSTERIOR A UNA DESCARGA O ACTUACIÓN'))
    a(('p', 'Después de una descarga, el sistema se debe considerar fuera de servicio hasta que se restablezca por completo.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Ingreso al recinto', 'ingreso solo después de ventilar y de verificar con una medición que la atmósfera es segura, o con '
                               'equipo de respiración autónomo y personal entrenado; búsqueda de personas en el recinto y en los '
                               'espacios bajos adyacentes.'),
        ('Causa', 'determinación de la causa de la actuación.'),
        ('Comunicación', 'aviso de la actuación y del restablecimiento a la autoridad competente (NFPA 12, 4.8.3.1).'),
        ('Reposición', 'recarga o reemplazo de los cilindros o del depósito y verificación de su fecha de prueba hidrostática.'),
        ('Rearme', 'rearme de los cabezales de control, de los cierres y del panel, y prueba en blanco antes de abrir la válvula de bloqueo.'),
    ]))
    a(('p', cierre(3)))

    a(('h3', 'SEGURIDAD Y SALUD OCUPACIONAL'))
    a(('p', 'Además de las medidas de seguridad del personal de este manual, durante las tareas se debe asegurar:'))
    a(('items', [
        ('Recipientes a presión', 'manipulación de cilindros con el capuchón colocado, sujeción durante el transporte y prohibición de '
                                  'desconectar una válvula de descarga sin el dispositivo antirretroceso o la tapa de seguridad que '
                                  'indique el fabricante.'),
        ('Partes eléctricas', 'intervención en el panel de control y en los circuitos de disparo con el sistema bloqueado y según el '
                              'procedimiento de trabajo eléctrico seguro de la instalación.'),
        ('Baja temperatura', 'uso de guantes y protección ocular ante el contacto con CO₂ líquido o con superficies frías del depósito '
                             'de baja presión.'),
    ]))

    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'Los cambios en el volumen, en el tipo de riesgo, en las aberturas o en la ventilación del recinto modifican la cantidad de '
            'agente necesaria y el riesgo para las personas. Toda modificación se debe evaluar técnicamente antes de su ejecución y '
            'registrar en la planilla de información general.'))
    a(('p', 'La empresa mantenedora es responsable de ejecutar las tareas de inspección, prueba y mantenimiento y de bloquear el sistema '
            'durante las intervenciones. El usuario o propietario es responsable de capacitar e informar a las personas que ingresan en '
            'el recinto, de conservar los carteles de advertencia, de mantener cerradas las aberturas y de comunicar cualquier '
            'modificación del recinto.'))
    return C


def REGISTRO_EXTRA(cierre):
    return [
        'Los datos de la instalación, del volumen protegido, de la concentración de diseño, del tipo de sistema, de los cilindros o '
        'del depósito, de la activación y de las alarmas se registran en la planilla SG-PEM-IFI-%s-1 %s – %s.' % (SIG, NOM, PL[1]),
        'El peso de cada cilindro, su capacidad, la fecha de su última prueba hidrostática, el peso vacío grabado, el peso leído y la '
        'carga neta se registran en la planilla SG-PEM-IFI-%s-4 %s – %s.' % (SIG, NOM, PL[4]),
        'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '
        'codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables se indican con NA. Toda '
        'condición O o X se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y '
        'por el responsable de la instalación, con su aclaración.',
    ]
