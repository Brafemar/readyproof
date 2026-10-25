# -*- coding: utf-8 -*-
SIG, NOM, NOMU, CAP = 'SAL', 'Sistema de Extinción por Agentes Limpios', 'SISTEMA DE EXTINCIÓN POR AGENTES LIMPIOS', '17'
PL = {1: 'Información general', 2: 'Inspección mensual', 3: 'Inspección y pruebas semestral y anual',
      4: 'Inspección y prueba quinquenal'}
INFORME = 'SG-PEM-IFI-SAL-1-IN'
N72 = 'NFPA 72'
VIG = ' Se aplica la edición vigente de cada norma NFPA; la numeración de los artículos citados se debe confirmar en esa edición, porque puede variar entre ediciones.'
N101 = 'NFPA 101, Código de Seguridad Humana'
AVISO = ('Antes de realizar cualquier inspección o prueba se debe notificar al responsable del área, a los ocupantes del recinto '
         'y al servicio de monitoreo correspondiente, y asegurar el sistema contra la descarga inadvertida.')


def seguridad_humana(a, extra_items):
    a(('h3', 'SEGURIDAD HUMANA: RECOMENDACIONES DE LA NFPA 101'))
    a(('p', 'La NFPA 101, Código de Seguridad Humana, establece requisitos orientados a proteger la vida de las '
            'personas que dependen directamente del sistema. Se incorporan como recomendaciones de buena práctica, traducidas de la '
            'norma y citadas por artículo, y son obligatorias donde la autoridad competente adopte ese código.'))
    a(('p', 'Se recomienda asegurar:'))
    a(('items', [
        ('Mantenimiento continuo (4.6.12.1)', 'todo dispositivo, equipo o sistema requerido para la seguridad humana debe '
                                              'mantenerse en forma continua, conforme a las normas NFPA aplicables o a lo que '
                                              'indique la autoridad competente.'),
        ('Elementos existentes (4.6.12.2 y 4.6.12.3)', 'no se debe retirar ni reducir ningún elemento de seguridad humana que sea '
                                                       'requisito para construcción nueva; los elementos existentes visibles al '
                                                       'público que no sean requeridos se deben mantener o retirar, porque su '
                                                       'presencia genera una expectativa de protección; no se deben '
                                                       'dejar instalados en condición inoperativa (A.4.6.12.3).'),
        ('Pruebas periódicas (4.6.12.5)', 'todo dispositivo, equipo, sistema o elemento que requiera pruebas, inspecciones u '
                                          'operación periódicas para asegurar su mantenimiento se debe probar, inspeccionar u '
                                          'operar según el código o según lo indique la autoridad competente.'),
        ('Supervisión de las tareas (4.6.12.6)', 'las pruebas, inspecciones y mantenimiento se deben realizar a los intervalos '
                                                 'especificados por las normas NFPA aplicables, bajo la supervisión de una persona '
                                                 'responsable que asegure su cumplimiento.'),
        ('Registros (4.6.12.7)', 'los registros de mantenimiento, inspección y prueba se deben documentar en informes o '
                                 'formularios aprobados, y se admite presentarlos, conservarlos, consultarlos y compartirlos en '
                                 'formato electrónico aprobado.'),
    ] + extra_items + [
        ('Prueba integrada de sistemas (9.11.4.1)', 'donde lo exijan los capítulos 11 a 43 del código y dos o más sistemas de '
                                                    'protección contra incendio o de seguridad humana estén integrados, al probar '
                                                    'uno de ellos se debe verificar la respuesta de los sistemas integrados; '
                                                    'después de una reparación o reemplazo, la nueva prueba se limita a las funciones '
                                                    'iniciadas por el equipo reparado o reemplazado.'),
        ('Prueba según la NFPA 4 (9.11.4.2)', 'en edificios de gran altura y en sistemas integrados que incluyen control de humo, '
                                              'la prueba integrada se realiza según la NFPA 4; en edificios existentes, a intervalos '
                                              'no mayores que **10 años**, salvo que un plan de prueba integrada indique otra '
                                              'frecuencia (9.11.4.2.2).'),
        ('Simulacros de evacuación (4.7)', 'donde sean requeridos, los simulacros se deben realizar con frecuencia suficiente para '
                                           'familiarizar a los ocupantes, priorizando una evacuación ordenada antes que la '
                                           'velocidad, en horarios esperados e inesperados, con reubicación en un lugar '
                                           'predeterminado y registro escrito de cada simulacro.'),
    ]))


def CONTENT(cierre):
    C = []; a = C.append
    a(('h2', NOMU))
    a(('basado', '(Basado en IRAM 3546:2011 – Capítulo %s; criterios complementarios: NFPA 2001; detección y disparo: %s, '
                 'capítulo 14; seguridad humana: NFPA 101)' % (CAP, N72)))
    a(('p', 'Este apartado establece los requisitos mínimos para la inspección, prueba y mantenimiento del sistema de extinción por '
            'agentes limpios, con el objetivo de asegurar que el sistema detecte el incendio en forma temprana y descargue el agente '
            'en la cantidad y la concentración de diseño, manteniéndola en el recinto durante el tiempo requerido, en condiciones de '
            'emergencia.'))
    a(('p', 'La IRAM 3546:2011 es la base del presente procedimiento y fija sus frecuencias. La NFPA 2001, Norma sobre sistemas '
            'extintores de incendio por agentes limpios, se aplica como criterio complementario para los valores de aceptación y '
            'para las tareas que la IRAM no contempla (capítulo 11, Inspección, servicio, prueba, mantenimiento y capacitación). Ante '
            'diferencias, se adopta siempre la condición más exigente.'))
    a(('p', 'Un sistema de extinción por agentes limpios descarga un agente gaseoso que no deja residuos ni daña equipos sensibles. '
            'Los procedimientos son aplicables a agentes halogenados, como el HFC-227ea, y a gases inertes, considerando en cada '
            'caso las particularidades de presión, concentración y condiciones de descarga indicadas por el fabricante.'))
    a(('p', 'El equipamiento del sistema incluye:'))
    a(('items', [
        ('Cilindros de agente extintor', 'recipientes de alta o baja presión que almacenan el agente, con su manómetro y su etiqueta '
                                         'de peso y presión.'),
        ('Cabezales de control y válvulas de accionamiento', 'dispositivos que liberan el agente al recibir la orden de disparo.'),
        ('Conexiones flexibles y red de cañerías', 'conducen el agente hasta las boquillas de descarga.'),
        ('Boquillas de descarga', 'distribuyen el agente en el volumen protegido: ambiente, falso suelo, falso techo u otros.'),
        ('Sistema de detección', 'detectores iónicos u ópticos de humo, termovelocimétricos, de temperatura fija o por compensación, '
                                 'con comando de zona simple, zona cruzada o dos detectores por zona.'),
        ('Panel de control', 'ejecuta la lógica de operación, el retardo y el disparo.'),
        ('Equipos auxiliares, tales como', ''),
        ['alarmas audibles y visuales y señalización;', 'interruptores de aborto y de disparo manual;',
         'cierres automáticos de puertas, compuertas y ventilación.'],
    ]))
    a(('p', 'Ante la detección de un evento, que puede requerir la confirmación por detección cruzada, el sistema activa las alarmas y '
            'un tiempo de retardo que permite la evacuación del recinto; durante ese período se ejecutan las funciones auxiliares, '
            'como el cierre de compuertas o la detención de la ventilación, y al finalizar se produce la descarga del agente.'))
    a(('p', AVISO))

    # ---------------- INSPECCIÓN ----------------
    a(('h3', 'INSPECCIÓN'))
    a(('p', 'La inspección consiste en la verificación visual del sistema y de sus componentes, para comprobar que se encuentran en '
            'condiciones aparentemente óptimas de operación y libres de daños físicos. Se realiza generalmente en cada planta, '
            'recorriendo las zonas protegidas.'))
    a(('p', 'Las inspecciones de frecuencia menor a un mes pueden ser completadas por el usuario de la instalación como '
            'inspecciones de autocontrol, y se deben identificar como tales; el mantenedor debe verificar su correcto '
            'cumplimiento, dejando constancia de los hallazgos verificados. En el presente sistema la IRAM 3546:2011 no '
            'establece inspecciones de esa frecuencia.'))
    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica previa '
            'de la instalación según la IRAM 3619; esta evaluación no es obligatoria y puede ser solicitada por cualquiera de las '
            'partes interesadas.'))

    a(('h4', 'Inspección mensual'))
    a(('p', 'Las inspecciones mensuales tienen como finalidad verificar que el sistema y el recinto protegido se mantienen en las '
            'condiciones de diseño.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Boquillas', 'verificar que las tapas están en su lugar y que las boquillas no están dañadas.'),
        ('Daños físicos', 'comprobar que el sistema no presenta indicios de daños en sus componentes.'),
        ('Recinto protegido', 'comprobar que no se modificaron los espacios protegidos ni el tamaño o tipo de riesgo.'),
        ('Cierre de aberturas', 'comprobar que todas las puertas del recinto disponen de muelle de autocierre o se cierran '
                                'automáticamente cuando se dispara el sistema.'),
    ]))
    a(('p', 'La NFPA 2001 (11.2.2) exige verificar además en la inspección mensual que el panel de disparo esté energizado y sin '
            'condiciones de supervisión, falla o alarma, que los controles manuales estén libres de obstrucciones, que los manómetros '
            'estén en el rango operable y que las deficiencias anteriores se hayan corregido. El registro de cada inspección debe '
            'indicar la fecha, las iniciales de quien la realizó y las deficiencias encontradas, y se conserva como mínimo hasta el '
            'siguiente servicio semestral (11.2.5).'))
    a(('p', cierre(2)))

    a(('h4', 'Inspección semestral'))
    a(('p', 'Las inspecciones semestrales permiten asegurar la disponibilidad del agente extintor en la cantidad de diseño.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Recipientes de agente', 'comprobar que no tienen daños.'),
        ('Presión de los recipientes', 'comprobar que los manómetros marcan la presión adecuada y registrarla, en MPa.'),
        ('Etiqueta', 'verificar que la presión y el peso están anotados en la etiqueta sujeta al recipiente; si no, colocarla.'),
    ]))
    a(('p', 'Si la pérdida de presión es mayor que el **10 %** con agentes halogenados, o que el **5 %** con agentes inertes, '
            'ajustada por la temperatura, respecto de la indicada en la placa de datos, se debe rellenar o sustituir el cilindro. '
            'Con agentes halogenados, también se debe rellenar o sustituir el recipiente cuando la pérdida de cantidad de agente '
            'supera el **5 %** (NFPA 2001, 11.3.1 a 11.3.4).'))
    a(('p', 'Los manómetros usados para controlar la carga de los gases inertes se deben comparar como mínimo una vez al año con un '
            'instrumento calibrado independiente (NFPA 2001, 11.3.5). La etiqueta del recipiente debe indicar la fecha de la '
            'inspección, quién la realizó, el tipo de agente, el peso bruto del recipiente y el peso neto de agente en los '
            'halogenados, y la presión y la temperatura del recipiente (NFPA 2001, 11.3.7).'))
    a(('p', cierre(3)))

    a(('h4', 'Inspección anual'))
    a(('p', 'Las inspecciones anuales tienen como finalidad validar el estado integral del sistema y la capacidad del recinto para '
            'retener el agente.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Inspección profunda del sistema', 'revisar todos los componentes del sistema.'),
        ('Estanqueidad del local', 'verificar la estanqueidad del recinto; si el recinto es complejo y genera dudas, realizar una '
                                   'prueba de estanqueidad que defina el nivel de fugas mediante un ventilador de puerta.'),
    ]))
    a(('p', 'La prueba con ventilador de puerta se realiza conforme al método de la ASTM E 779, citada en la bibliografía de la '
            'IRAM 3546:2011. La NFPA 2001 (11.4.5) admite reemplazar la inspección anual del recinto por un programa administrativo '
            'documentado que controle los cambios en la integridad de sus cerramientos o en sus dimensiones; si los cambios pueden '
            'impedir mantener la concentración, se deben corregir. En la inspección anual se examinan además todas las mangueras '
            'del sistema; si presentan alguna deficiencia, se reemplazan o se prueban de inmediato según la prueba quinquenal '
            '(11.4.4). Después del servicio anual se entrega al propietario un informe con recomendaciones, que puede conservarse '
            'en papel o en formato electrónico (11.4.2 y 11.4.3). La prueba anual no requiere la descarga del agente (11.4.1).'))
    a(('p', cierre(3)))
    a(('protocol', ('estanqueidad del recinto', [
        ('Preparación', [
            ('Paso a paso', 'cerrar puertas, compuertas y ventilación en la condición de descarga, y sellar provisoriamente las '
                            'aberturas propias del ensayo según el método.'),
            ('Justificación técnica', 'el ensayo debe representar el recinto tal como queda al producirse la descarga.'),
            ('Criterio de aceptación', 'recinto en condición de descarga.')]),
        ('Ensayo con ventilador de puerta', [
            ('Paso a paso', 'presurizar y despresurizar el recinto con el ventilador de puerta, registrar el caudal de fuga a las '
                            'presiones de ensayo y calcular el área de fuga según la ASTM E 779.'),
            ('Justificación técnica', 'el nivel de fugas determina si el agente se mantiene en la concentración necesaria.'),
            ('Criterio de aceptación', 'nivel de fugas compatible con el tiempo de retención de diseño, según la memoria de '
                                       'cálculo del sistema.')]),
    ])))

    # ---------------- PRUEBA ----------------
    a(('h3', 'PRUEBA'))
    a(('p', 'Las pruebas tienen como objetivo comprobar el funcionamiento del sistema en condiciones controladas, evitando la '
            'descarga del agente. El personal que las efectúa debe estar calificado y conocer la disposición del sistema y los '
            'riesgos de una descarga inadvertida. Cuando se detecten fallas, se debe proceder inmediatamente a su reparación.'))
    a(('p', 'Cuando el sistema, o una parte de él, quede fuera de servicio por una desactivación programada o por una falla, se debe:'))
    a(('items', [
        ('Notificación', 'notificar al propietario o a su representante y al servicio de monitoreo (NFPA 72, 10.20.1).'),
        ('Autoridad competente', 'informar a la autoridad competente cuando la condición se prolongue más de **ocho horas** '
                                 '(NFPA 72, 10.20.4).'),
        ('Medidas de mitigación', 'aplicar las medidas que la autoridad competente requiera (NFPA 72, 10.20.5); durante '
                                  'reparaciones o modificaciones, las áreas afectadas se ocupan solo con las protecciones '
                                  'mantenidas o con medidas alternativas aceptadas por la autoridad competente (NFPA 101, 4.6.10.1).'),
        ('Finalización', 'notificar la finalización de la desactivación (NFPA 72, 10.20.6).'),
        ('Registro', 'registrar el inicio, el fin, la causa y las medidas adoptadas; el registro se conserva como mínimo **tres '
                     'años** (IRAM 3546:2011; NFPA 72, 10.20.2).'),
    ]))
    a(('p', 'Las deficiencias que no se corrijan al finalizar la inspección, la prueba o el mantenimiento se deben informar por '
            'escrito al propietario o a su representante dentro de las **24 h** (NFPA 72, 14.2.2.2.3).'))

    a(('h4', 'Prueba semestral'))
    a(('p', 'Las pruebas semestrales tienen como finalidad verificar la actuación de los cabezales de control ante la orden de '
            'disparo, sin descarga del agente.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Activación de los cabezales de control', 'realizar la prueba según el protocolo de ensayo, con los cabezales retirados de '
                                                   'los cilindros.'),
    ]))
    a(('p', cierre(3)))
    a(('protocol', ('activación de los cabezales de control', [
        ('Aseguramiento del sistema', [
            ('Paso a paso', 'notificar a los ocupantes y al servicio de monitoreo y retirar el cabezal de control de cada recipiente '
                            'de agente extintor, de modo que el disparo no produzca la descarga.'),
            ('Justificación técnica', 'una descarga inadvertida consume el agente y puede exponer a las personas a concentraciones no '
                                      'aptas para la permanencia.'),
            ('Criterio de aceptación', 'todos los cabezales retirados e identificados.')]),
        ('Disparo', [
            ('Paso a paso', 'activar el sistema de detectores o el disparo manual.'),
            ('Justificación técnica', 'comprueba la cadena de detección, lógica de control y disparo.'),
            ('Criterio de aceptación', 'el émbolo del cabezal de control queda totalmente extendido.')]),
        ('Rearme del panel', [
            ('Paso a paso', 'comprobar que el panel de control se rearma a su situación normal de funcionamiento.'),
            ('Justificación técnica', 'un panel que no se rearma deja el sistema sin capacidad de un nuevo disparo.'),
            ('Criterio de aceptación', 'panel en condición normal.')]),
        ('Reconexión', [
            ('Paso a paso', 'rearmar los cabezales según el fabricante y verificar que el émbolo está retraído; medir con voltímetro, '
                            'en los bornes del circuito de disparo, la ausencia de tensión; verificar que no haya alarmas, '
                            'prealarmas ni retardos activos y que todos los dispositivos de iniciación estén restablecidos; '
                            'reconectar los cabezales de a uno, empezando por el piloto si lo hay.'),
            ('Justificación técnica', 'reconectar un cabezal con el émbolo extendido provoca la descarga inmediata.'),
            ('Criterio de aceptación', 'circuito de disparo sin tensión antes de cada reconexión; cabezales rearmados y '
                                       'reconectados; sistema en servicio.')]),
    ])))

    a(('h4', 'Prueba anual'))
    a(('p', 'Las pruebas anuales permiten verificar la secuencia completa de operación del sistema y de sus funciones auxiliares, '
            'sin descarga del agente.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Prueba de funcionamiento del sistema', 'simular la secuencia completa sin descarga, con el sistema asegurado, según el '
                                                 'protocolo de ensayo.'),
        ('Detectores del recinto', 'realizar la prueba funcional anual en el lugar de todos los detectores, con humo o producto '
                                   'listado, con el sistema asegurado.'),
        ('Detección cruzada', 'accionar un detector en cada zona y verificar la secuencia correcta con la primera y con la segunda zona.'),
        ('Interruptores de aborto', 'accionarlos y verificar que la secuencia y el funcionamiento son correctos; deben ser del tipo '
                                    'hombre muerto, que requiere presión manual constante, y no se admiten interruptores que '
                                    'queden en la posición de aborto al soltarlos (NFPA 2001, 10.6.14.1 y 10.6.14.2).'),
        ('Estaciones de disparo manual', 'verificar que requieren dos acciones separadas y distintas para operar, y que están '
                                         'identificadas, visibles, libres de obstrucciones y accesibles (NFPA 2001, 10.6.12.3 a '
                                         '10.6.12.5).'),
        ('Circuito del solenoide de descarga', 'verificar su funcionamiento.'),
        ('Supervisión de circuitos', 'verificar la supervisión mediante la creación de un circuito abierto.'),
        ('Alarmas y funciones auxiliares', 'verificar las alarmas audibles y visuales, el retardo y el cierre de puertas, compuertas '
                                           'y ventilación.'),
        ('Indicación en la alarma del edificio', 'verificar que la actuación del sistema activa o se indica en el sistema de '
                                                 'alarma de incendio del edificio, donde exista (NFPA 101, 9.8.2).'),
    ]))
    a(('p', 'Las pruebas de detección, aborto y disparo se realizan según la %s, tabla 14.4.3.2, ítem 18, como criterio '
            'complementario. La central de detección y disparo, sus fuentes de energía, sus dispositivos iniciadores y sus '
            'aparatos de notificación se inspeccionan, prueban y mantienen según el procedimiento SG-PEM-IFI-SDI, con el sistema '
            'de extinción asegurado según el protocolo de los cabezales de control.%s' % (N72, VIG)))
    a(('p', cierre(3)))
    a(('protocol', ('prueba de funcionamiento del sistema', [
        ('Aseguramiento', [
            ('Paso a paso', 'notificar a los ocupantes y al servicio de monitoreo y retirar los cabezales de control según el '
                            'protocolo semestral.'),
            ('Justificación técnica', 'la prueba recorre toda la secuencia de disparo y no debe producir la descarga.'),
            ('Criterio de aceptación', 'todos los cabezales retirados e identificados.')]),
        ('Detección cruzada', [
            ('Paso a paso', 'accionar un detector de la primera zona y verificar la prealarma; accionar un detector de la segunda '
                            'zona y verificar la alarma de descarga.'),
            ('Justificación técnica', 'comprueba la lógica de confirmación que evita descargas por una sola señal.'),
            ('Criterio de aceptación', 'secuencia correcta con la primera y con la segunda zona (NFPA 72, Tabla 14.4.3.2, 18(d)).')]),
        ('Retardo y funciones auxiliares', [
            ('Paso a paso', 'medir con cronómetro el tiempo de retardo y verificar el cierre de puertas y compuertas y el corte de '
                            'la ventilación.'),
            ('Justificación técnica', 'el retardo permite la evacuación y el cierre del recinto asegura la concentración de diseño.'),
            ('Criterio de aceptación', 'retardo según el diseño registrado y funciones auxiliares operativas.')]),
        ('Aborto y disparo manual', [
            ('Paso a paso', 'accionar el interruptor de aborto y luego el disparo manual; en los de tipo hombre muerto y especial, '
                            'verificar la secuencia; en los de tipo reciclaje, verificar la matriz con cada sensor accionado.'),
            ('Justificación técnica', 'el aborto permite detener una descarga indebida con personas en el recinto.'),
            ('Criterio de aceptación', 'secuencia y funcionamiento correctos (NFPA 72, Tabla 14.4.3.2, 18(a) a 18(c)).')]),
        ('Circuito de disparo y supervisión', [
            ('Paso a paso', 'verificar el funcionamiento del solenoide de descarga con carga simulada según el fabricante; en '
                            'circuitos con dispositivo explosivo, con lámpara de flash (AGI) u otra luz de prueba aprobada; en '
                            'circuitos de tipo matriz, accionar todos los sensores y verificar la matriz; en circuitos de zona '
                            'verificada, accionar los sensores en un mínimo de **cuatro** lugares del circuito; y verificar la '
                            'supervisión mediante la creación de un circuito abierto.'),
            ('Justificación técnica', 'confirma que la orden llega al actuador y que la central detecta un circuito cortado.'),
            ('Criterio de aceptación', 'funcionamiento del solenoide verificado e indicación de falla ante circuito abierto '
                                       '(NFPA 72, Tabla 14.4.3.2, 18(e) a 18(i)).')]),
        ('Restitución', [
            ('Paso a paso', 'restablecer la central y reconectar los cabezales según el paso de reconexión del protocolo semestral.'),
            ('Justificación técnica', 'evita la descarga al reconectar.'),
            ('Criterio de aceptación', 'sistema en servicio sin alarmas activas.')]),
    ])))

    a(('h4', 'Prueba quinquenal'))
    a(('p', 'Las pruebas quinquenales están orientadas a verificar la resistencia mecánica de los recipientes y conexiones sometidos '
            'a presión.'))
    a(('p', 'Cada cinco años se debe realizar:'))
    a(('items', [
        ('Prueba hidrostática', 'realizar la prueba hidrostática de las conexiones flexibles y de los cilindros de agente extintor, '
                                'registrando la fecha de la última prueba.'),
        ('Elementos defectuosos', 'destruir los conectores flexibles o cilindros que no pasen las pruebas.'),
        ('Examen visual de recipientes', 'realizar un completo examen visual de los recipientes de acuerdo con la IRAM 2529-1. La '
                                         'NFPA 2001 (11.6.2) exige esta inspección visual externa cada **5 años** en los '
                                         'recipientes en servicio continuo, según la sección 3 de la CGA C-6, con el resultado '
                                         'registrado en una tarjeta fija a cada recipiente y en un informe que el propietario '
                                         'conserva durante toda la vida útil del sistema; si el recipiente presenta daños, se '
                                         'requieren ensayos de resistencia adicionales.'),
        ('Mangueras del sistema', 'probarlas o reemplazarlas cada **5 años**, a **1,5 veces** la presión máxima del recipiente a '
                                  '**54,4 °C**, alcanzada en **1 min** y mantenida durante **1 min**; la manguera aprueba si no hay '
                                  'pérdida de presión, ni movimiento de los acoples, ni deformación permanente (NFPA 2001, 11.7).'),
    ]))
    a(('p', 'Se debe confeccionar una planilla con el número de cada cilindro y el resultado de la prueba. Las pruebas hidrostáticas '
            'se deben ejecutar conforme a procedimientos documentados en función de las normas de aplicación, con las presiones '
            'de prueba de la IRAM 2529-1 y del fabricante de las conexiones flexibles. El vaciado del cilindro lo realiza personal '
            'competente, con recuperación del agente y no por venteo. El agente recuperado o de reposición debe corresponder al tipo y a la especificación indicados en la placa del sistema y '
            'en la planilla SG-PEM-IFI-SAL-1, y su calidad se debe verificar según un procedimiento documentado, en función de las '
            'normas de aplicación y de las instrucciones del fabricante, con certificado de análisis del proveedor o del '
            'recuperador (IRAM 3546:2011, Mantenimiento de las instalaciones). No se deben mezclar agentes distintos ni recargar '
            'con agente de origen no certificado.'))
    a(('p', cierre(4)))

    # ---------------- MANTENIMIENTO ----------------
    a(('h3', 'MANTENIMIENTO'))
    a(('p', 'El mantenimiento tiene como finalidad conservar el sistema en condiciones operativas mediante el control de la carga de '
            'agente y de las conexiones.'))

    a(('h4', 'Mantenimiento mensual'))
    a(('p', 'La IRAM 3546:2011 no establece tareas de mantenimiento mensual para este sistema.'))

    a(('h4', 'Mantenimiento semestral'))
    a(('p', 'Las tareas de mantenimiento semestral permiten verificar la cantidad de agente almacenado.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Pesada de los recipientes', 'en agentes halogenados, control de la cantidad de agente por pesada del recipiente según el '
                                      'protocolo de ensayo, registrando el peso en kg; en gases inertes, la carga se controla por '
                                      'presión.'),
        ('Registro por cilindro', 'volcado en planilla del número de cilindro, tara, peso cargado y carga neta.'),
        ('Etiqueta', 'verificación de que el peso y la presión están registrados en la etiqueta sujeta al recipiente.'),
    ]))
    a(('p', 'Si el recipiente muestra una pérdida de peso neto mayor que el **5 %**, se debe sustituir o rellenar.'))
    a(('p', cierre(3)))
    a(('protocol', ('pesada de recipientes', [
        ('Aseguramiento', [
            ('Paso a paso', 'retirar el cabezal de control y el actuador manual, desconectar la conexión flexible de descarga y '
                            'colocar la tapa de protección y el dispositivo antirretroceso de la válvula según el fabricante.'),
            ('Justificación técnica', 'un disparo o un golpe con el cabezal montado descarga el agente y convierte al cilindro en '
                                      'un proyectil.'),
            ('Criterio de aceptación', 'cilindro sin cabezal, con la válvula protegida.')]),
        ('Pesada', [
            ('Paso a paso', 'pesar el cilindro con una balanza calibrada y registrar el número de cilindro, la tara, el peso cargado '
                            'y la carga neta.'),
            ('Justificación técnica', 'la carga neta es la cantidad real de agente disponible para la descarga.'),
            ('Criterio de aceptación', 'pérdida de peso neto no mayor que el **5 %**; en caso contrario, rellenar o sustituir.')]),
        ('Reconexión', [
            ('Paso a paso', 'reconectar la conexión flexible, retirar la protección de la válvula, verificar el émbolo retraído y '
                            'reponer el cabezal en último lugar, según el paso de reconexión del protocolo de cabezales.'),
            ('Justificación técnica', 'reponer el cabezal antes de completar la conexión puede provocar una descarga sin control.'),
            ('Criterio de aceptación', 'cilindro conectado y sistema en servicio.')]),
    ])))

    a(('h4', 'Mantenimiento anual'))
    a(('p', 'Las tareas de mantenimiento anual están orientadas al estado de las conexiones flexibles.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Conexiones flexibles', 'examen del estado de todas las conexiones; las defectuosas se deben sustituir o probar '
                                 'hidrostáticamente.'),
    ]))
    a(('p', cierre(3)))

    # ---------------- COMPLEMENTARIAS ----------------
    a(('h3', 'PROCEDIMIENTO POSTERIOR A UNA DESCARGA O ACTUACIÓN'))
    a(('p', 'Luego de una descarga, el sistema se debe considerar fuera de servicio hasta su restablecimiento, que tiene como '
            'finalidad recuperar la protección del recinto.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Personas', 'verificación de que no existan personas dentro del recinto.'),
        ('Ventilación', 'ventilación del recinto antes del reingreso.'),
        ('Evaluación', 'evaluación de las condiciones del área y determinación de la causa de la activación.'),
        ('Comunicación', 'aviso inmediato de la actuación a la autoridad competente (NFPA 2001, 11.5.2).'),
        ('Recinto', 'sellado inmediato de toda penetración en el recinto, restituyendo su resistencia al fuego original '
                    '(NFPA 2001, 11.5.4).'),
        ('Reposición', 'reposición del agente extintor, con verificación de su calidad según lo indicado para la prueba '
                       'quinquenal, rearme de los cabezales y restitución del sistema a su estado operativo.'),
    ]))
    a(('p', cierre(3)))

    a(('h3', 'SEGURIDAD Y SALUD OCUPACIONAL'))
    a(('p', 'La seguridad del personal tiene como finalidad garantizar una evacuación segura antes de la descarga y el reingreso '
            'solo en condiciones ambientales seguras.'))
    a(('p', 'Se debe asegurar:'))
    a(('items', [
        ('Evacuación', 'alarmas audibles y visuales, señalización adecuada y dispositivos de aborto operativos.'),
        ('Activación', 'abandono inmediato del recinto por el personal ante una activación del sistema.'),
        ('Reingreso', 'reingreso solo después de ventilar el área y verificar que las condiciones ambientales son seguras, con '
                      'autorización del responsable del área o del personal técnico.'),
        ('Pruebas', 'notificación a los ocupantes durante las reparaciones o pruebas y aseguramiento del sistema contra la descarga '
                    'inadvertida.'),
        ('Productos de descomposición', 'después de una descarga sobre un fuego, los agentes halogenados generan productos de '
                                        'descomposición tóxicos y corrosivos; el reingreso se hace con ventilación forzada y con '
                                        'protección respiratoria cuando no se pueda verificar la atmósfera.'),
        ('Sala de cilindros', 'recipientes sujetos; ningún cilindro se traslada con el cabezal de control montado.'),
    ]))

    seguridad_humana(a, [
        ('Norma de instalación (9.8.1 y tabla 9.8.1)', 'los sistemas de extinción por agentes limpios instalados como sistema '
                                                       'alternativo deben cumplir la NFPA 2001.'),
        ('Activación de la alarma del edificio (9.8.2.1 y 9.8.2.2)', 'si el sistema reemplaza a un sistema de rociadores '
                                                                     'supervisado requerido, su actuación debe activar el sistema '
                                                                     'de alarma del edificio; en los demás casos, su actuación '
                                                                     'debe indicarse en ese sistema, donde exista.'),
        ('Funciones de control (9.6.6.2)', 'donde otra sección del código lo requiera, el sistema de alarma debe actuar la '
                                           'liberación de retenedores de puertas, el desbloqueo de puertas y la detención del aire '
                                           'acondicionado, entre otras funciones; su verificación anual se realiza según la NFPA 72, '
                                           'Tabla 14.4.3.2, ítem 24. En este sistema esas funciones son además necesarias para '
                                           'mantener la concentración de diseño del agente.'),
    ])

    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'Los cambios en el uso del área, en su volumen o en las condiciones de ventilación afectan la concentración de agente que '
            'se alcanza y se mantiene. Deben evaluarse técnicamente para verificar que el sistema continúa siendo efectivo.'))
    a(('p', 'La empresa mantenedora es responsable de ejecutar las tareas de inspección, prueba y mantenimiento. El usuario o '
            'propietario debe garantizar que las condiciones del recinto no se alteren sin evaluación técnica. El responsable '
            'técnico supervisa y valida las tareas realizadas. Los simulacros de evacuación, donde sean requeridos, son '
            'responsabilidad del propietario o usuario, y de cada uno se debe completar un registro escrito (NFPA 101, 4.7.6).'))
    return C


def REGISTRO_EXTRA(cierre):
    return [
        'Los datos de la instalación, del agente, del volumen protegido, de la concentración, de los cilindros, de la detección y de '
        'los comandos de extinción se registran en la planilla SG-PEM-IFI-SAL-1 %s – %s.' % (NOM, PL[1]),
        'La documentación de diseño del sistema y los procedimientos de inspección, prueba y mantenimiento se deben conservar en '
        'un lugar aprobado y seguro durante toda la vida útil del sistema (NFPA 101, 9.11.3.1).',
        'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '
        'codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables se indican con NA. Toda '
        'condición O o X se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y '
        'por el responsable de la instalación, con su aclaración.',
    ]
