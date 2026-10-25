import sys
D = sys.argv[1]
def edit(name, pairs):
    fn = '%s/content_%s.py' % (D, name); s = open(fn, encoding='utf8').read()
    for o, n in pairs:
        assert s.count(o) == 1, (name, o[:80], s.count(o)); s = s.replace(o, n)
    open(fn, 'w', encoding='utf8').write(s); print(name, 'ok')

edit('SBC', [
    ("                         'controlar el flujo de agua de enfriamiento en el intercambiador de calor.'),",
     "                         'controlar el flujo de agua de enfriamiento en el intercambiador de calor.'),\n"
     "        ('Motor diésel antes de la marcha', 'registrar el nivel de aceite del cárter, el nivel de electrolito, la temperatura '\n"
     "                                            'del agua de enfriamiento con el precalentador y las fechas del último cambio de '\n"
     "                                            'aceite y filtro, del último cambio de combustible y del próximo.'),\n"
     "        ('Motor diésel durante la marcha', 'registrar la presión de agua de enfriamiento, la presión de aceite, la temperatura '\n"
     "                                           'del agua en funcionamiento y la velocidad.'),"),
    ("        ('Bomba jockey', 'registrar sus presiones de arranque y de parada y las horas acumuladas de uso.'),",
     "        ('Bomba jockey', 'registrar sus presiones de arranque y de parada, las horas acumuladas de uso y la cantidad de arranques '\n"
     "                         'indicada en el panel; un aumento de arranques respecto del registro anterior indica fugas en la red.'),"),
    ("        ('Condiciones posteriores', 'registrar la presión del sistema, el estado automático, el tiempo de funcionamiento y la '\n"
     "                                    'temperatura de la sala después de la prueba, y realizar la limpieza del equipo.'),\n    ]))\n    a(('p', cierre(3)))",
     "        ('Condiciones posteriores', 'registrar la presión del sistema, el estado automático, el tiempo de funcionamiento y la '\n"
     "                                    'temperatura de la sala después de la prueba, y realizar la limpieza del equipo.'),\n    ]))\n    a(('p', cierre(3)))\n"
     "    a(('p', 'La planilla IRAM 3546-12C es de frecuencia mensual. En sistemas con motobomba, cada prueba semanal se registra en '\n"
     "            'una planilla SG-PEM-IFI-SBC-3 propia; en sistemas sin motobomba, la prueba se realiza y se registra cada mes. Los '\n"
     "            'datos de placa de la motobomba, la electrobomba y la bomba jockey se registran en la misma planilla.'))"),
    ("    a(('p', 'Se consideran aceptables, según la IRAM 3546:2011 y la %s:' % N20))",
     "    a(('p', 'Se consideran aceptables:'))"),
    ("        ('Tensión', 'lecturas entre **−5 % y +10 %** del valor nominal de placa.'),\n"
     "        ('Corriente', 'producto de la tensión y la corriente de cada fase no mayor que el producto de los valores nominales de placa '\n"
     "                      'por el factor de servicio.'),\n"
     "        ('Caudal máximo', 'la bomba debe entregar no menos del **150 %** de su capacidad nominal a no menos del **65 %** de la presión '\n"
     "                          'total nominal.'),\n"
     "        ('Presión a caudal cero', 'no mayor que el **140 %** de la presión total nominal.'),",
     "        ('Tensión', 'lecturas entre **−5 % y +10 %** del valor nominal de placa (IRAM 3546:2011; NFPA 20, 14.2.7.4.6).'),\n"
     "        ('Corriente', 'la corriente de cada fase no debe superar la corriente de plena carga de placa multiplicada por el factor '\n"
     "                      'de servicio (NFPA 20, 14.2.7.4.4); con tensión distinta de la nominal, el producto de la tensión real por la '\n"
     "                      'corriente de cada fase no debe superar el producto de los valores de placa por el factor de servicio '\n"
     "                      '(IRAM 3546:2011; NFPA 20, 14.2.7.4.5).'),\n"
     "        ('Caudal máximo', 'la bomba debe entregar no menos del **150 %** de su capacidad nominal a no menos del **65 %** de la presión '\n"
     "                          'total nominal (NFPA 20, 6.2.1 y 7.1.2.1).'),\n"
     "        ('Presión a caudal cero', 'no mayor que el **140 %** de la presión total nominal (NFPA 20, 7.1.2.2; el 6.2.2 de la versión '\n"
     "                                  'en español indica «40 %», un error de traducción).'),\n"
     "        ('Presión de succión', 'con dispositivo antirretorno, no menor que **0 bar** en el manómetro al **150 %** de la capacidad '\n"
     "                               'nominal (NFPA 20, 5.26.4.2); en los demás casos, no menor que la mínima admitida por el diseño o '\n"
     "                               'por el prestador del abastecimiento.'),"),
    ("            ('Paso a paso', 'con la válvula de descarga principal cerrada, arrancar la bomba y registrar la presión máxima, verificando '\n"
     "                            'la descarga de la válvula de alivio de circulación durante **0,5 h**.'),",
     "            ('Paso a paso', 'con las válvulas del cabezal de prueba y de drenaje cerradas, sin consumo en la red y con la válvula de '\n"
     "                            'descarga al sistema abierta, arrancar la bomba, registrar la presión de succión y de descarga y '\n"
     "                            'verificar la descarga de la válvula de alivio de circulación durante **0,5 h**; si por razones '\n"
     "                            'operativas se debe aislar la red, se aplica el procedimiento de puesta fuera de servicio.'),"),
    ("            ('Paso a paso', 'abrir los dispositivos de prueba hasta el caudal nominal de placa, estabilizar el flujo y registrar '\n"
     "                            'presiones, velocidad, tensión y corriente de cada fase.'),",
     "            ('Paso a paso', 'abrir los dispositivos de prueba hasta el caudal nominal de placa, estabilizar el flujo y registrar '\n"
     "                            'presiones de succión y descarga, velocidad, tensión y corriente de cada fase; purgar la toma del '\n"
     "                            'manovacuómetro antes de leer.'),\n"
     "            ('Qué se determina con la lectura', 'una presión de succión anormalmente baja indica un filtro de succión obstruido; '\n"
     "                                                'la comparación entre la presión en la bomba y en el hidrante más desfavorable '\n"
     "                                                'indica las pérdidas de carga de la red; las fluctuaciones rápidas del caudalímetro '\n"
     "                                                'indican entrada de aire en la succión.'),"),
    ("            ('Paso a paso', 'llevar la descarga al **150 %** del caudal nominal y registrar los mismos parámetros; si el abastecimiento '\n"
     "                            'no lo permite, operar al máximo disponible y verificar que se superan los requisitos de diseño.'),",
     "            ('Paso a paso', 'llevar la descarga al **150 %** del caudal nominal y registrar los mismos parámetros, incluida la presión '\n"
     "                            'de succión; si el abastecimiento no lo permite, operar al máximo disponible y verificar que se superan '\n"
     "                            'los requisitos de diseño; ante fluctuaciones de lectura o ruido de cavitación, interrumpir el aumento '\n"
     "                            'de caudal.'),"),
    ("            ('Criterio de aceptación', 'presión no menor que el **65 %** de la presión total nominal.')]),",
     "            ('Criterio de aceptación', 'presión no menor que el **65 %** de la presión total nominal y presión de succión no menor '\n"
     "                                       'que la mínima admitida.')]),\n"
     "        ('Termografía y equilibrio de fases', [\n"
     "            ('Paso a paso', 'al **150 %** del caudal nominal, registrar con cámara termográfica la temperatura de los bornes del '\n"
     "                            'contactor y guardamotor, de los cables de alimentación, de los rodamientos y de la carcasa del motor, y '\n"
     "                            'con pinza amperométrica la corriente de cada fase.'),\n"
     "            ('Justificación técnica', 'el calor localizado anticipa fallas por bornes flojos o lubricación deficiente, y el '\n"
     "                                      'desbalance de corriente reduce la vida útil del motor.'),\n"
     "            ('Criterio de aceptación', 'sin puntos calientes respecto de componentes similares ni del registro anterior; desbalance '\n"
     "                                       'de corriente comparable con el registro anterior y dentro de lo que indica el fabricante '\n"
     "                                       'del motor.')]),"),
    ("                            'la boquilla); el caudal total es la suma de los caudales parciales.'),",
     "                            'la boquilla); el caudal total es la suma de los caudales parciales. Se deben usar las boquillas de los '\n"
     "                            'gabinetes en los hidrantes más alejados y no descargar sin boquilla, porque la lectura resulta falsa.'),"),
    ("        ('Partes rotantes', 'protecciones de acoples y ejes colocadas durante la marcha y prohibición de intervenir con el equipo en '\n"
     "                            'funcionamiento.'),",
     "        ('Partes rotantes', 'protecciones de acoples y ejes colocadas durante la marcha y prohibición de intervenir con el equipo en '\n"
     "                            'funcionamiento.'),\n"
     "        ('Bloqueo de arranque', 'antes de intervenir partes rotantes o eléctricas, pasar el controlador a posición apagado y abrir, '\n"
     "                                'bloquear y etiquetar el seccionador; en motores diésel, colocar el selector en apagado y '\n"
     "                                'desconectar los dos bancos de baterías. La intervención se trata como puesta fuera de servicio, '\n"
     "                                'con aviso al responsable y al servicio de supervisión; al finalizar se retiran los bloqueos y se '\n"
     "                                'verifica el selector en automático.'),"),
])

edit('SAL', [
    ("    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica previa '",
     "    a(('p', 'Las inspecciones de frecuencia menor a un mes pueden ser completadas por el usuario de la instalación como '\n"
     "            'inspecciones de autocontrol, y se deben identificar como tales; el mantenedor debe verificar su correcto '\n"
     "            'cumplimiento. En el presente sistema la IRAM 3546:2011 no establece inspecciones de esa frecuencia.'))\n"
     "    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica previa '"),
    ("            ('Paso a paso', 'rearmar los cabezales según el fabricante, verificar que el émbolo está retraído y reconectarlos a los '\n"
     "                            'recipientes.'),",
     "            ('Paso a paso', 'rearmar los cabezales según el fabricante y verificar que el émbolo está retraído; medir con voltímetro, '\n"
     "                            'en los bornes del circuito de disparo, la ausencia de tensión; verificar que no haya alarmas, '\n"
     "                            'prealarmas ni retardos activos y que todos los dispositivos de iniciación estén restablecidos; '\n"
     "                            'reconectar los cabezales de a uno, empezando por el piloto si lo hay.'),"),
    ("            ('Criterio de aceptación', 'cabezales rearmados y reconectados; sistema en servicio.')]),",
     "            ('Criterio de aceptación', 'circuito de disparo sin tensión antes de cada reconexión; cabezales rearmados y '\n"
     "                                       'reconectados; sistema en servicio.')]),"),
    ("        ('Prueba de funcionamiento del sistema', 'simular la secuencia completa sin descarga, con el sistema asegurado.'),",
     "        ('Prueba de funcionamiento del sistema', 'simular la secuencia completa sin descarga, con el sistema asegurado, según el '\n"
     "                                                 'protocolo de ensayo.'),\n"
     "        ('Detectores del recinto', 'realizar la prueba funcional anual en el lugar de todos los detectores, con humo o producto '\n"
     "                                   'listado, con el sistema asegurado.'),"),
    ("    a(('p', 'Las pruebas de detección, aborto y disparo se realizan según la %s, tabla 14.4.3.2, ítem 18, como criterio '\n"
     "            'complementario.' % N72))\n    a(('p', cierre(3)))",
     "    a(('p', 'Las pruebas de detección, aborto y disparo se realizan según la %s, tabla 14.4.3.2, ítem 18, como criterio '\n"
     "            'complementario. La central de detección y disparo, sus fuentes de energía, sus dispositivos iniciadores y sus '\n"
     "            'aparatos de notificación se inspeccionan, prueban y mantienen según el procedimiento SG-PEM-IFI-SDI, con el sistema '\n"
     "            'de extinción asegurado según el protocolo de los cabezales de control.' % N72))\n    a(('p', cierre(3)))\n"
     "    a(('protocol', ('prueba de funcionamiento del sistema', [\n"
     "        ('Aseguramiento', [\n"
     "            ('Paso a paso', 'notificar a los ocupantes y al servicio de monitoreo y retirar los cabezales de control según el '\n"
     "                            'protocolo semestral.'),\n"
     "            ('Justificación técnica', 'la prueba recorre toda la secuencia de disparo y no debe producir la descarga.'),\n"
     "            ('Criterio de aceptación', 'todos los cabezales retirados e identificados.')]),\n"
     "        ('Detección cruzada', [\n"
     "            ('Paso a paso', 'accionar un detector de la primera zona y verificar la prealarma; accionar un detector de la segunda '\n"
     "                            'zona y verificar la alarma de descarga.'),\n"
     "            ('Justificación técnica', 'comprueba la lógica de confirmación que evita descargas por una sola señal.'),\n"
     "            ('Criterio de aceptación', 'secuencia correcta con la primera y con la segunda zona (NFPA 72, Tabla 14.4.3.2, 18(d)).')]),\n"
     "        ('Retardo y funciones auxiliares', [\n"
     "            ('Paso a paso', 'medir con cronómetro el tiempo de retardo y verificar el cierre de puertas y compuertas y el corte de '\n"
     "                            'la ventilación.'),\n"
     "            ('Justificación técnica', 'el retardo permite la evacuación y el cierre del recinto asegura la concentración de diseño.'),\n"
     "            ('Criterio de aceptación', 'retardo según el diseño registrado y funciones auxiliares operativas.')]),\n"
     "        ('Aborto y disparo manual', [\n"
     "            ('Paso a paso', 'accionar el interruptor de aborto según su tipo y luego el disparo manual.'),\n"
     "            ('Justificación técnica', 'el aborto permite detener una descarga indebida con personas en el recinto.'),\n"
     "            ('Criterio de aceptación', 'secuencia y funcionamiento correctos (NFPA 72, Tabla 14.4.3.2, 18(a) a 18(c)).')]),\n"
     "        ('Circuito de disparo y supervisión', [\n"
     "            ('Paso a paso', 'verificar el circuito del solenoide de descarga con lámpara de prueba o carga simulada según el '\n"
     "                            'fabricante y la supervisión mediante la creación de un circuito abierto.'),\n"
     "            ('Justificación técnica', 'confirma que la orden llega al actuador y que la central detecta un circuito cortado.'),\n"
     "            ('Criterio de aceptación', 'funcionamiento del solenoide verificado e indicación de falla ante circuito abierto '\n"
     "                                       '(NFPA 72, Tabla 14.4.3.2, 18(f) y 18(i)).')]),\n"
     "        ('Restitución', [\n"
     "            ('Paso a paso', 'restablecer la central y reconectar los cabezales según el paso de reconexión del protocolo semestral.'),\n"
     "            ('Justificación técnica', 'evita la descarga al reconectar.'),\n"
     "            ('Criterio de aceptación', 'sistema en servicio sin alarmas activas.')]),\n"
     "    ])))"),
    ("    a(('p', 'La prueba con ventilador de puerta se realiza conforme al método de la ASTM E 779, citada en la bibliografía de la '\n"
     "            'IRAM 3546:2011.'))\n    a(('p', cierre(3)))",
     "    a(('p', 'La prueba con ventilador de puerta se realiza conforme al método de la ASTM E 779, citada en la bibliografía de la '\n"
     "            'IRAM 3546:2011.'))\n    a(('p', cierre(3)))\n"
     "    a(('protocol', ('estanqueidad del recinto', [\n"
     "        ('Preparación', [\n"
     "            ('Paso a paso', 'cerrar puertas, compuertas y ventilación en la condición de descarga, y sellar provisoriamente las '\n"
     "                            'aberturas propias del ensayo según el método.'),\n"
     "            ('Justificación técnica', 'el ensayo debe representar el recinto tal como queda al producirse la descarga.'),\n"
     "            ('Criterio de aceptación', 'recinto en condición de descarga.')]),\n"
     "        ('Ensayo con ventilador de puerta', [\n"
     "            ('Paso a paso', 'presurizar y despresurizar el recinto con el ventilador de puerta, registrar el caudal de fuga a las '\n"
     "                            'presiones de ensayo y calcular el área de fuga según la ASTM E 779.'),\n"
     "            ('Justificación técnica', 'el nivel de fugas determina si el agente se mantiene en la concentración necesaria.'),\n"
     "            ('Criterio de aceptación', 'nivel de fugas compatible con el tiempo de retención de diseño, según la memoria de '\n"
     "                                       'cálculo del sistema.')]),\n"
     "    ])))"),
    ("    a(('p', 'Se debe confeccionar una planilla con el número de cada cilindro y el resultado de la prueba. Las pruebas hidrostáticas '\n"
     "            'se deben ejecutar conforme a procedimientos documentados en función de las normas de aplicación.'))",
     "    a(('p', 'Se debe confeccionar una planilla con el número de cada cilindro y el resultado de la prueba. Las pruebas hidrostáticas '\n"
     "            'se deben ejecutar conforme a procedimientos documentados en función de las normas de aplicación, con las presiones '\n"
     "            'de prueba de la IRAM 2529-1 y del fabricante de las conexiones flexibles. El vaciado del cilindro lo realiza personal '\n"
     "            'competente, con recuperación del agente y no por venteo.'))"),
    ("        ('Pesada de los recipientes', 'control de la cantidad de agente por pesada del recipiente, registrando el peso en kg.'),",
     "        ('Pesada de los recipientes', 'en agentes halogenados, control de la cantidad de agente por pesada del recipiente según el '\n"
     "                                      'protocolo de ensayo, registrando el peso en kg; en gases inertes, la carga se controla por '\n"
     "                                      'presión.'),"),
    ("    a(('p', 'Si el recipiente muestra una pérdida de peso neto mayor que el **5 %**, se debe sustituir o rellenar.'))\n    a(('p', cierre(3)))",
     "    a(('p', 'Si el recipiente muestra una pérdida de peso neto mayor que el **5 %**, se debe sustituir o rellenar.'))\n    a(('p', cierre(3)))\n"
     "    a(('protocol', ('pesada de recipientes', [\n"
     "        ('Aseguramiento', [\n"
     "            ('Paso a paso', 'retirar el cabezal de control y el actuador manual, desconectar la conexión flexible de descarga y '\n"
     "                            'colocar la tapa de protección y el dispositivo antirretroceso de la válvula según el fabricante.'),\n"
     "            ('Justificación técnica', 'un disparo o un golpe con el cabezal montado descarga el agente y convierte al cilindro en '\n"
     "                                      'un proyectil.'),\n"
     "            ('Criterio de aceptación', 'cilindro sin cabezal, con la válvula protegida.')]),\n"
     "        ('Pesada', [\n"
     "            ('Paso a paso', 'pesar el cilindro con una balanza calibrada y registrar el número de cilindro, la tara, el peso cargado '\n"
     "                            'y la carga neta.'),\n"
     "            ('Justificación técnica', 'la carga neta es la cantidad real de agente disponible para la descarga.'),\n"
     "            ('Criterio de aceptación', 'pérdida de peso neto no mayor que el **5 %**; en caso contrario, rellenar o sustituir.')]),\n"
     "        ('Reconexión', [\n"
     "            ('Paso a paso', 'reconectar la conexión flexible, retirar la protección de la válvula, verificar el émbolo retraído y '\n"
     "                            'reponer el cabezal en último lugar, según el paso de reconexión del protocolo de cabezales.'),\n"
     "            ('Justificación técnica', 'reponer el cabezal antes de completar la conexión puede provocar una descarga sin control.'),\n"
     "            ('Criterio de aceptación', 'cilindro conectado y sistema en servicio.')]),\n"
     "    ])))"),
])
