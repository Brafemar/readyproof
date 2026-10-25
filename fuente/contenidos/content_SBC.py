# -*- coding: utf-8 -*-
SIG, NOM, NOMU, CAP = 'SBC', 'Sistema de Bombas Contraincendios', 'SISTEMA DE BOMBAS CONTRA INCENDIO', '12'
PL = {1: 'Información general', 2: 'Inspección semanal / autocontrol', 3: 'Inspección mensual',
      4: 'Mantenimiento mensual - trimestral', 5: 'Mantenimiento semestral - anual', 6: 'Pruebas'}
N20 = 'NFPA 20'
VIG = ' Se aplica la edición vigente de cada norma NFPA; la numeración de los artículos citados se debe confirmar en esa edición, porque puede variar entre ediciones.'


def CONTENT(cierre):
    C = []; a = C.append
    a(('h2', NOMU))
    a(('basado', '(Basado en IRAM 3546:2011 – Capítulo %s; criterios complementarios: NFPA 25 y %s)' % (CAP, N20)))
    a(('p', 'Este apartado establece los requisitos mínimos para la inspección, prueba y mantenimiento del equipo de bombeo contra '
            'incendio, con el objetivo de asegurar que el sistema suministre el caudal y la presión requeridos por la protección '
            'contra incendio a la que sirve, en condiciones de emergencia.'))
    a(('p', 'La IRAM 3546:2011 es la base del presente procedimiento y fija sus frecuencias. La NFPA 25 (capítulo 8, Bombas contra '
            'incendio), a la que la NFPA 20 (14.4) remite la inspección, prueba y mantenimiento periódicos, se aplica como criterio '
            'complementario para las tareas, los valores de aceptación de la prueba anual y los instrumentos de prueba; la %s, Norma '
            'para la instalación de bombas estacionarias de protección contra incendios, se aplica para las características de '
            'diseño de la bomba que se deben conservar. Ante diferencias, se adopta siempre la condición más exigente.%s' % (N20, VIG)))
    a(('p', 'El equipamiento del sistema incluye:'))
    a(('items', [
        ('Fuente de agua', 'depósito, cisterna o red que abastece a la bomba, cuyo mantenimiento se rige por el capítulo 13 de la '
                           'IRAM 3546:2011.'),
        ('Cañerías de succión y descarga', 'con sus válvulas de succión, de descarga y de derivación (bypass).'),
        ('Bomba contra incendio', 'equipo hidráulico que genera el caudal y la presión de diseño.'),
        ('Impulsor', 'motor eléctrico, motor diésel o turbina de vapor, con su equipo de control.'),
        ('Equipamiento auxiliar, tal como', ''),
        ['accesorios de la bomba: acople del eje, válvula automática de purga de aire, manómetros y válvula de alivio de circulación;',
         'dispositivo de prueba de la bomba;',
         'válvula de alivio y su cañería, donde la presión máxima de descarga excede la presión de diseño de los componentes;',
         'sensores de alarma e indicadores;',
         'caja de engranajes en ángulo recto, en bombas turbina verticales impulsadas por motor de combustión;',
         'bomba de mantenimiento de presión (jockey) y sus accesorios.'],
    ]))
    a(('p', 'La inspección, prueba y mantenimiento del equipo de bombeo puede dejarlo fuera de servicio. Para minimizar o anular '
            'ese inconveniente se debe acordar con el responsable de la instalación el momento de la intervención y las medidas '
            'compensatorias mientras el equipo no esté disponible.'))
    a(('p', 'Donde se cuente con un servicio de supervisión, para evitar falsas alarmas se debe notificar al personal de ese servicio '
            'antes de realizar cualquier prueba o acción que pueda generar una alarma y luego de concluir las tareas.'))

    # ---------------- INSPECCIÓN ----------------
    a(('h3', 'INSPECCIÓN'))
    a(('p', 'La inspección tiene como propósito verificar que el equipo de bombeo se encuentra en aparentes condiciones de '
            'operación y libre de daños físicos. Las inspecciones visuales se deben realizar semanalmente.'))
    a(('p', 'Las inspecciones de frecuencia menor a un mes pueden ser completadas por el usuario de la instalación como '
            'inspecciones de autocontrol, y se deben identificar como tales; el mantenedor debe verificar su correcto '
            'cumplimiento, dejando constancia de los hallazgos.'))
    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica previa '
            'de la instalación según la IRAM 3619; esta evaluación no es obligatoria y puede ser solicitada por cualquiera de las '
            'partes interesadas.'))

    a(('h4', 'Inspección semanal de la sala de bombas (autocontrol)'))
    a(('p', 'La inspección de la sala de bombas tiene como finalidad verificar las condiciones ambientales y de seguridad del recinto.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Temperatura ambiente', 'comprobar que es como mínimo de **4 °C**, o de **21 °C** en salas con bombas diésel sin '
                                 'calefactor del motor (NFPA 25, 8.2.2); la IRAM 3546:2011 indica 20 °C y se adopta el valor de '
                                 'la NFPA 25, más exigente.'),
        ('Aberturas de ventilación', 'verificar que están libres y operan sin inconvenientes.'),
        ('Iluminación de emergencia', 'verificar su funcionamiento.'),
    ]))

    a(('h4', 'Inspección semanal del sistema de bombeo (autocontrol)'))
    a(('p', 'Esta inspección permite verificar el estado y la posición de los componentes hidráulicos del sistema.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Válvulas de succión, descarga y bypass', 'verificar que se encuentran en la posición acorde a la maniobra, con las '
                                                   'válvulas de succión y descarga totalmente abiertas.'),
        ('Cañerías', 'verificar que están libres de pérdidas.'),
        ('Presión de succión', 'verificar que la lectura es normal.'),
        ('Presión del sistema', 'verificar que la lectura es normal.'),
        ('Válvula de alivio', 'verificar la circulación de agua en la válvula de alivio.'),
        ('Reservorio de agua', 'verificar que se encuentra totalmente lleno.'),
    ]))

    a(('h4', 'Inspección semanal del sistema eléctrico (autocontrol)'))
    a(('p', 'Esta inspección tiene como finalidad verificar el estado de la alimentación y del control eléctrico de la bomba.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Luz piloto del controlador', 'verificar que está encendida.'),
        ('Luz piloto de la llave de transferencia', 'verificar que está normal e iluminada.'),
        ('Llave seccionadora', 'verificar que está cerrada.'),
        ('Rotación de fases', 'verificar que la luz piloto de alarma de inversión de fase está apagada o que la luz de rotación '
                              'normal está encendida, y la presencia de las tres fases.'),
        ('Motor vertical', 'verificar que el nivel de aceite en el visor es normal.'),
        ('Bobinado del motor', 'controlar la temperatura del bobinado.'),
        ('Bombas jockey, principal y de achique', 'verificar su estado de funcionamiento.'),
    ]))

    a(('h4', 'Inspección semanal del motor diésel (autocontrol)'))
    a(('p', 'Esta inspección permite verificar los componentes que aseguran el arranque y el funcionamiento del motor de combustión.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Tanque de combustible', 'verificar que se encuentra con un nivel superior a **dos tercios** de su capacidad, sin agua en '
                                  'el sistema y con conexiones flexibles y conectores en buen estado.'),
        ('Selector del controlador', 'verificar que se encuentra en posición automático.'),
        ('Baterías', 'verificar que la tensión y la corriente de carga de los dos bancos son normales, que sus luces piloto están '
                     'encendidas o las de falla apagadas, que el nivel de electrolito es normal y que los terminales están libres '
                     'de corrosión.'),
        ('Luces de alarma', 'verificar que todas están apagadas.'),
        ('Medidor de horas de marcha', 'verificar que está operativo.'),
        ('Lubricación', 'verificar que el nivel de aceite del cárter y de la caja de engranajes en ángulo recto es normal, la '
                        'temperatura del aceite y la ausencia de pérdidas en el circuito.'),
        ('Sistema de enfriamiento', 'verificar el nivel de agua, la circulación de agua en el intercambiador de calor, la ausencia '
                                    'de pérdidas y el estado de mangueras, flexibles y conexiones.'),
        ('Calefactor de camisas de agua', 'verificar que está operativo y la temperatura del calentador.'),
        ('Sistema de escape', 'verificar las trampas de drenaje de condensado.'),
        ('Sistema eléctrico', 'realizar la inspección general.'),
    ]))
    a(('p', cierre(2)))

    # ---------------- PRUEBA ----------------
    a(('h3', 'PRUEBA'))
    a(('p', 'Las pruebas tienen como propósito asegurar la operación automática o manual del equipo de bombeo ante la demanda y la '
            'entrega continua del caudal requerido por el sistema, y detectar deficiencias no evidenciadas durante la inspección.'))
    a(('p', 'En los sistemas que no cuenten con bombas accionadas por motores de combustión interna, las tareas con periodicidad '
            'menor a mensual indicadas en el presente procedimiento se deben realizar mensualmente, según la IRAM 3546:2011. No '
            'obstante, la NFPA 25 (8.3.1.2.1) exige la prueba semanal sin flujo de las electrobombas que abastecen sistemas en '
            'edificios que superan la capacidad de bombeo del servicio de bomberos, de las que tienen controladores de servicio '
            'limitado, de las bombas turbina verticales y de las que toman agua de tanques a nivel del terreno o de fuentes que no '
            'aseguran presión de succión suficiente; en esos casos se mantiene la frecuencia semanal, más exigente.'))

    a(('h4', 'Prueba semanal de funcionamiento'))
    a(('p', 'La prueba semanal tiene como finalidad verificar el arranque automático y el funcionamiento sin flujo de la bomba y de '
            'su impulsor. Se realiza solamente por personal calificado, sin flujo de agua en la red.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Arranque automático', 'provocar el arranque automático de la bomba; se permite un temporizador para el arranque '
                                'automático semanal.'),
        ('Tiempo mínimo de funcionamiento', 'mantener la bomba en marcha como mínimo **10 min** con motor eléctrico o **30 min** '
                                            'con motor diésel.'),
        ('Bomba', 'registrar las presiones de arranque, de succión y de descarga; controlar que las empaquetaduras tengan una descarga '
                  'suave por goteo que asegure la refrigeración y ajustarlas si es necesario; controlar ruidos o vibraciones '
                  'inusuales y el sobrecalentamiento de empaquetaduras, cojinetes y carcasa.'),
        ('Motor eléctrico', 'registrar el tiempo que tarda en alcanzar la velocidad nominal, el tiempo en que el controlador '
                            'permanece en la primera etapa de tensión o corriente de arranque reducida, el tiempo de marcha desde '
                            'el arranque (para controles de parada automática) y la corriente de cada fase.'),
        ('Motor diésel', 'registrar el tiempo de arranque y el tiempo que tarda en alcanzar su velocidad; observar periódicamente la '
                         'presión de aceite, la velocidad y las temperaturas de aceite y agua; registrar cualquier anormalidad y '
                         'controlar el flujo de agua de enfriamiento en el intercambiador de calor.'),
        ('Motor diésel antes de la marcha', 'registrar el nivel de aceite del cárter, el nivel de electrolito, la temperatura '
                                            'del agua de enfriamiento con el precalentador y las fechas del último cambio de '
                                            'aceite y filtro, del último cambio de combustible y del próximo.'),
        ('Motor diésel durante la marcha', 'registrar la presión de agua de enfriamiento, la presión de aceite, la temperatura '
                                           'del agua en funcionamiento y la velocidad.'),
        ('Condiciones previas', 'registrar el nivel y la temperatura del agua de la reserva, la temperatura de la sala, la presión del '
                                'sistema y del tanque pulmón, el estado de la válvula de alivio, el estado automático o manual, las '
                                'tensiones y corrientes de carga de los bancos de baterías, la temperatura del agua de enfriamiento y '
                                'el nivel de combustible.'),
        ('Bomba jockey', 'registrar sus presiones de arranque y de parada, las horas acumuladas de uso y la cantidad de arranques '
                         'indicada en el panel; un aumento de arranques respecto del registro anterior indica fugas en la red.'),
        ('Condiciones posteriores', 'registrar la presión del sistema, el estado automático, el tiempo de funcionamiento y la '
                                    'temperatura de la sala después de la prueba, y realizar la limpieza del equipo.'),
    ]))
    a(('p', 'Durante toda la marcha de la bomba debe estar presente personal calificado (NFPA 25, 8.3.2.7). Si la diferencia entre '
            'las presiones de descarga y de succión a caudal cero supera el **95 %** de la presión nominal de la bomba, la causa se '
            'debe investigar y corregir (NFPA 25, 8.3.2.1.2.1). En los controladores con sensores electrónicos de presión se deben '
            'registrar la presión actual y las presiones máxima y mínima del registro de eventos del controlador, y en las bombas '
            'con válvula de alivio de circulación se debe verificar que descarga agua (NFPA 25, 8.3.2.8 y 8.3.2.9).'))
    a(('p', cierre(3)))
    a(('p', 'La planilla IRAM 3546-12C es de frecuencia mensual. En sistemas con motobomba, cada prueba semanal se registra en '
            'una planilla SG-PEM-IFI-SBC-3 propia; en sistemas sin motobomba, la prueba se realiza y se registra cada mes. Los '
            'datos de placa de la motobomba, la electrobomba y la bomba jockey se registran en la misma planilla.'))
    a(('protocol', ('prueba de funcionamiento sin flujo', [
        ('Preparación', [
            ('Paso a paso', 'notificar al servicio de supervisión, verificar el selector en automático y provocar el arranque por '
                            'caída de presión en la red, abriendo la válvula de prueba o de drenaje del presostato.'),
            ('Justificación técnica', 'el arranque por caída de presión comprueba la cadena real de arranque automático.'),
            ('Criterio de aceptación', 'arranque automático de la bomba ante la caída de presión.')]),
        ('Tiempos de arranque', [
            ('Paso a paso', 'medir con cronómetro el tiempo hasta la velocidad nominal y el tiempo en la etapa de arranque reducido, '
                            'desde el cierre del primer contactor hasta el cambio al contactor de marcha.'),
            ('Justificación técnica', 'un aumento del tiempo de arranque respecto de los registros anteriores anticipa fallas en el '
                                      'bobinado, en los rodamientos o en la alimentación.'),
            ('Criterio de aceptación', 'tiempos comparables con los registros anteriores y con los valores del fabricante del '
                                       'controlador.')]),
        ('Marcha y observación', [
            ('Paso a paso', 'mantener la marcha durante el tiempo mínimo, recorrer el perímetro de la bomba para detectar ruidos o '
                            'vibraciones, observar el goteo de las empaquetaduras y controlar con termómetro de contacto o cámara '
                            'termográfica la temperatura de cojinetes y carcasa.'),
            ('Justificación técnica', 'el funcionamiento a flujo cero sin recirculación calienta el agua de la carcasa y daña los '
                                      'sellos; los sellos mecánicos no deben gotear y las empaquetaduras sí, en forma leve.'),
            ('Criterio de aceptación', 'sin ruidos ni vibraciones inusuales, sin sobrecalentamiento, con recirculación por la válvula '
                                       'de alivio de circulación y tiempo de marcha no menor que el mínimo.')]),
        ('Normalización', [
            ('Paso a paso', 'detener la bomba según la configuración, verificar la presión del sistema y el selector en automático, y '
                            'notificar la conclusión al servicio de supervisión.'),
            ('Justificación técnica', 'un equipo que queda en manual no arranca ante una emergencia.'),
            ('Criterio de aceptación', 'equipo en automático y presión del sistema normal.')]),
    ])))

    a(('h4', 'Prueba anual de rendimiento'))
    a(('p', 'La prueba anual tiene como finalidad verificar que la bomba cumple su curva característica, controlando la cantidad de '
            'agua descargada a través de dispositivos de prueba en las condiciones de caudal mínimo, nominal y máximo.'))
    a(('p', 'En las bombas de velocidad constante la prueba se realiza a caudal cero, al **100 %** y al **150 %** del caudal nominal; '
            'en las de velocidad variable, a caudal cero y al **25 %**, **50 %**, **75 %**, **100 %**, **125 %** y **150 %** del caudal '
            'nominal (NFPA 25, 8.3.3.1 y 8.3.3.2). Si el abastecimiento no permite el 150 %, la bomba se prueba al 100 % y al máximo '
            'caudal admisible con la mínima presión de succión permitida (8.3.3.4). La descarga por mangueras o por el medidor de '
            'caudal hacia drenaje o reservorio se debe usar como mínimo **cada tres años**; la recirculación en circuito cerrado con '
            'medidor de caudal se admite dos de cada tres años, controlando la temperatura del agua recirculada (8.3.3.9).'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Método de descarga', 'realizar la descarga mediante mangueras, midiendo la presión de succión y de descarga y el caudal de '
                               'cada boquilla, o mediante medidor de caudal ajustado previamente según el fabricante; se debe tener '
                               'cuidado de no generar daños con los chorros de agua.'),
        ('Consistencia del medidor de caudal', 'si los resultados con medidor no son consistentes con los de años anteriores, '
                                               'verificarlos mediante mangueras y boquillas; si no es posible, calibrar el medidor y '
                                               'repetir la prueba.'),
        ('Boca cerrada (sin flujo)', 'controlar la descarga de la válvula de alivio de circulación y la operación de la válvula de '
                                     'alivio de presión, si está instalada, y continuar la prueba durante **0,5 h**. La NFPA 25 '
                                     '(8.3.3.10) establece no detener la electrobomba antes de **10 min** de marcha ni la motobomba '
                                     'antes de **30 min**.'),
        ('Cada condición de flujo', 'registrar la tensión y la corriente de cada motor, la velocidad de la bomba, simultáneamente la '
                                    'presión de succión, la de descarga y el caudal, y la operación de indicadores de alarma o '
                                    'cualquier anormalidad visible.'),
        ('Llave de transferencia automática', 'simular la falla de la energía normal con la bomba a potencia máxima, verificar la '
                                              'transferencia a la fuente de emergencia sin apertura de las protecciones de '
                                              'sobrecorriente, registrar tensión, corriente, velocidad y presiones, mantener la '
                                              'bomba a potencia máxima con la fuente alternativa como mínimo **2 min** y verificar '
                                              'la reconexión a la fuente normal al restablecerla (NFPA 25, 8.3.3.13).'),
        ('Alarmas', 'activar los circuitos de alarma desde la ubicación de los sensores y verificar todas las alarmas locales y remotas.'),
        ('Generadores de emergencia', 'ensayarlos y mantenerlos según la norma respectiva.'),
        ('Condiciones ambientales de la sala', 'verificar que la ventilación, la iluminación y la temperatura son adecuadas para la '
                                               'operación manual o automática.'),
        ('Filtros de succión', 'inspeccionarlos y limpiarlos después de las descargas de agua de la prueba (NFPA 25, 8.3.3.16).'),
        ('Módulo de control electrónico', 'en motores con gestión electrónica de combustible, probar el módulo de respaldo y los '
                                          'sensores principal y redundante (NFPA 25, 8.3.3.17).'),
        ('Alineación', 'inspeccionar durante la prueba la alineación paralela y angular de la bomba y el motor y corregir la '
                       'desalineación (NFPA 25, 8.3.6.4).'),
    ]))
    a(('p', 'Los resultados se deben comparar con la curva de aceptación en campo de la bomba y con los ensayos de años anteriores. '
            'Incrementar la velocidad de la bomba más allá del valor nominal del fabricante no es un método válido para obtener el '
            'desempeño especificado.'))
    a(('p', 'Según la NFPA 25 (8.3.7.2.3), los resultados de la prueba son aceptables cuando se cumplen todas las condiciones '
            'siguientes:'))
    a(('items', [
        ('Demanda del sistema', 'la bomba satisface el caudal y la presión del sistema más exigente que abastece, según los datos de '
                                'diseño que aporte el propietario.'),
        ('Caudal nominal', 'la bomba entrega el **100 %** de su caudal nominal.'),
        ('Presión neta', 'en cada punto de caudal la presión neta es como mínimo el **95 %** de la que indica la curva original del '
                         'fabricante, la curva original sin corregir de la prueba de aceptación en campo o la curva de la placa.'),
        ('Succión', 'se cumplen los requisitos del abastecimiento de agua de la succión (NFPA 25, 8.1.5).'),
    ]))
    a(('p', 'Se consideran además aceptables:'))
    a(('items', [
        ('Tensión', 'lecturas entre **−5 % y +10 %** del valor nominal de placa (IRAM 3546:2011; NFPA 25, 8.3.7.2.9).'),
        ('Corriente', 'en electrobombas de velocidad constante, la corriente de cada fase en cada punto de prueba no debe superar '
                      'la corriente de plena carga de placa multiplicada por el factor de servicio; en las de tensión variable, el '
                      'producto de la tensión por la corriente de cada fase no debe superar el producto de los valores de placa por el '
                      'factor de servicio; si se superan, se debe identificar y corregir la causa (IRAM 3546:2011; NFPA 25, '
                      '8.3.7.2.5 a 8.3.7.2.8).'),
        ('Caudal máximo', 'la bomba debe entregar no menos del **150 %** de su capacidad nominal a no menos del **65 %** de la presión '
                          'total nominal (NFPA 20, 6.2.1).'),
        ('Presión a caudal cero', 'no mayor que el **140 %** de la presión total nominal (NFPA 20, 6.2.2).'),
        ('Presión de succión', 'con dispositivo o montaje de prevención de contraflujo, no menor que **0 bar** en el manómetro al **150 %** de la capacidad '
                               'nominal (NFPA 20, 5.26.4.2); en los demás casos, no menor que la mínima admitida por el diseño o '
                               'por el prestador del abastecimiento.'),
        ('Curva', 'desempeño coincidente con la curva de aceptación, dentro de la precisión del equipamiento de prueba, sin '
                  'recalentamientos ni vibraciones inaceptables.'),
    ]))
    a(('p', 'Los valores de caudal máximo, presión a caudal cero y presión de succión son características de diseño de la NFPA 20 '
            'que la bomba debe conservar. Si la prueba no resulta aceptable, se debe notificar por escrito al propietario, investigar '
            'la causa y, si la bomba no satisface la demanda máxima del sistema, tratar la condición como puesta fuera de servicio; '
            'las vibraciones excesivas o los componentes desgastados o flojos son deficiencias, y un desempeño degradado que aún '
            'satisface la demanda máxima es una deficiencia no crítica (NFPA 25, 8.3.7.2.4).'))
    a(('p', 'Las precauciones de seguridad para la operación cerca de las partes eléctricas de los equipos se deben respetar durante '
            'toda la prueba.'))
    a(('p', cierre(6)))
    a(('protocol', ('prueba anual de rendimiento hidráulico', [
        ('Preparación y seguridad', [
            ('Paso a paso', 'notificar al servicio de supervisión, delimitar el área de descarga, verificar que el drenaje puede evacuar '
                            'el caudal de prueba y que las válvulas de succión y descarga están libres de obstrucciones.'),
            ('Justificación técnica', 'una obstrucción en la succión provoca cavitación, que daña el impulsor en poco tiempo.'),
            ('Criterio de aceptación', 'área delimitada, drenaje disponible y succión libre.')]),
        ('Instrumentos', [
            ('Paso a paso', 'instalar manómetros de prueba calibrados en la succión y en la descarga, con etiqueta de la fecha de '
                            'calibración y exactitud de **± 1 %** (NFPA 25, 8.3.3.5.1 y 8.3.3.5.2); los medidores de caudal se '
                            'calibran anualmente con una exactitud de **± 3 %** (8.3.3.5.3); contrastar los manómetros fijos de la sala.'),
            ('Justificación técnica', 'los datos deben ser trazables; los manómetros fijos se descalibran por vibración.'),
            ('Criterio de aceptación', 'manómetros de prueba calibrados como mínimo anualmente con una exactitud de **± 1 %**; los '
                                       'instrumentos fijos que difieran más del **5 %** se deben cambiar o recalibrar.')]),
        ('Caudal cero', [
            ('Paso a paso', 'con las válvulas del cabezal de prueba y de drenaje cerradas, sin consumo en la red y con la válvula de '
                            'descarga al sistema abierta, arrancar la bomba, registrar la presión de succión y de descarga y '
                            'verificar la descarga de la válvula de alivio de circulación durante **0,5 h**; si por razones '
                            'operativas se debe aislar la red, se aplica el procedimiento de puesta fuera de servicio.'),
            ('Justificación técnica', 'una presión alta puede dañar accesorios de la red; una presión baja indica desgaste interno.'),
            ('Criterio de aceptación', 'presión no mayor que el **140 %** de la nominal y recirculación verificada.')]),
        ('Caudal nominal', [
            ('Paso a paso', 'abrir los dispositivos de prueba hasta el caudal nominal de placa, estabilizar el flujo y registrar '
                            'presiones de succión y descarga, velocidad, tensión y corriente de cada fase; purgar la toma del '
                            'manovacuómetro antes de leer.'),
            ('Qué se determina con la lectura', 'una presión de succión anormalmente baja indica un filtro de succión obstruido; '
                                                'la comparación entre la presión en la bomba y en el hidrante más desfavorable '
                                                'indica las pérdidas de carga de la red; las fluctuaciones rápidas del caudalímetro '
                                                'indican entrada de aire en la succión.'),
            ('Justificación técnica', 'es el punto de diseño con el que se calculó la protección del edificio.'),
            ('Criterio de aceptación', 'presión neta coincidente con la curva de aceptación; tensión y corriente dentro de los límites.')]),
        ('Caudal máximo', [
            ('Paso a paso', 'llevar la descarga al **150 %** del caudal nominal y registrar los mismos parámetros, incluida la presión '
                            'de succión; si el abastecimiento no lo permite, operar al máximo disponible y verificar que se superan '
                            'los requisitos de diseño; ante fluctuaciones de lectura o ruido de cavitación, interrumpir el aumento '
                            'de caudal.'),
            ('Justificación técnica', 'es el margen de seguridad ante demandas mayores que las previstas.'),
            ('Criterio de aceptación', 'presión no menor que el **65 %** de la presión total nominal y presión de succión no menor '
                                       'que la mínima admitida.')]),
        ('Termografía y equilibrio de fases', [
            ('Paso a paso', 'al **150 %** del caudal nominal, registrar con cámara termográfica la temperatura de los bornes del '
                            'contactor y guardamotor, de los cables de alimentación, de los rodamientos y de la carcasa del motor, y '
                            'con pinza amperométrica la corriente de cada fase.'),
            ('Justificación técnica', 'el calor localizado anticipa fallas por bornes flojos o lubricación deficiente, y el '
                                      'desbalance de corriente reduce la vida útil del motor.'),
            ('Criterio de aceptación', 'sin puntos calientes respecto de componentes similares ni del registro anterior; desbalance '
                                       'de corriente comparable con el registro anterior y dentro de lo que indica el fabricante '
                                       'del motor.')]),
        ('Medición por boquillas', [
            ('Paso a paso', 'cuando se descarga por mangueras, medir con tubo Pitot la presión en el centro del chorro de cada boquilla, '
                            'a medio diámetro de la salida, con boquillas de diámetro conocido y abiertas a chorro pleno, y calcular el '
                            'caudal de cada una mediante **Q = 0,0666 · c · d² · √P** (Q en L/min, d en mm, P en kPa, c coeficiente de '
                            'la boquilla); el caudal total es la suma de los caudales parciales. Se deben usar las boquillas de los '
                            'gabinetes en los hidrantes más alejados y no descargar sin boquilla, porque la lectura resulta falsa. La posición '
                            'del tubo Pitot sigue la NFPA 13, A.5.2.2.'),
            ('Justificación técnica', 'permite determinar el caudal real sin caudalímetro y contrastar sus lecturas.'),
            ('Criterio de aceptación', 'caudal total obtenido con boquillas de coeficiente conocido y registrado en la planilla.')]),
        ('Corrección por velocidad', [
            ('Paso a paso', 'si la velocidad medida con tacómetro difiere de la nominal, corregir los valores con las leyes de afinidad: '
                            'caudal proporcional a la velocidad y presión proporcional al cuadrado de la velocidad.'),
            ('Justificación técnica', 'permite comparar los resultados con la curva nominal sin modificar la velocidad de la bomba.'),
            ('Criterio de aceptación', 'curva corregida coincidente con la de aceptación.')]),
        ('Normalización', [
            ('Paso a paso', 'cerrar las líneas de prueba, reponer las válvulas abiertas y precintadas, dejar el equipo en automático y '
                            'notificar al servicio de supervisión; comparar los datos con la curva del fabricante y con los años anteriores.'),
            ('Justificación técnica', 'un equipo que no queda en automático no está disponible para una emergencia.'),
            ('Criterio de aceptación', 'equipo en automático y planilla con todos los datos registrados.')]),
    ])))

    # ---------------- MANTENIMIENTO ----------------
    a(('h3', 'MANTENIMIENTO'))
    a(('p', 'El mantenimiento comprende las tareas destinadas a conservar el equipo de bombeo en condiciones adecuadas de '
            'funcionamiento y confiabilidad. En este sistema, la IRAM 3546:2011 establece las tareas de mantenimiento en sus planillas.'))

    a(('h4', 'Mantenimiento mensual'))
    a(('p', 'Las tareas de mantenimiento mensual tienen como finalidad conservar el sistema eléctrico y las baterías del motor diésel.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Sistema eléctrico', 'activación del interruptor y seccionamiento; verificación de interruptores o fusibles.'),
        ('Baterías', 'remoción de corrosión, limpieza y secado de la carcasa; verificación de la densidad específica o estado de '
                     'carga, del cargador y de la tasa de carga; ecualización de la carga.'),
    ]))
    a(('p', cierre(4)))

    a(('h4', 'Mantenimiento trimestral'))
    a(('p', 'Las tareas de mantenimiento trimestral están orientadas a los sistemas auxiliares del motor diésel.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Combustible', 'verificación de filtros o similares, y prueba de los interruptores de flotante y de la señal de supervisión '
                        'del espacio intersticial del tanque de combustible (NFPA 25, 8.1.1.2.7).'),
        ('Lubricación', 'verificación del venteo del cárter.'),
        ('Enfriamiento', 'limpieza de los filtros de agua.'),
        ('Escape', 'inspección de la aislación y del riesgo de incendio.'),
        ('Baterías', 'limpieza y ajuste de terminales.'),
        ('Sistema eléctrico', 'inspección del rozamiento de cables en los puntos donde se mueven.'),
    ]))
    a(('p', cierre(4)))

    a(('h4', 'Mantenimiento semestral'))
    a(('p', 'Las tareas de mantenimiento semestral permiten verificar los medios de arranque y las protecciones del motor diésel.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Arranque manual con energía eléctrica', 'operación del medio de arranque manual.'),
        ('Enfriamiento', 'verificación del nivel de protección del anticongelante.'),
        ('Escape', 'inspección de la sección flexible del escape.'),
        ('Sistema eléctrico del motor', 'prueba de la operación de seguridades y alarmas e inspección de cajas, paneles y gabinetes.'),
    ]))
    a(('p', cierre(5)))

    a(('h4', 'Mantenimiento anual'))
    a(('p', 'Las tareas de mantenimiento anual están orientadas a la lubricación, alineación y calibración del conjunto de bombeo y '
            'a la renovación de fluidos del motor diésel.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Bomba', 'lubricación de cojinetes, control del juego en el extremo del eje y del alineamiento del eje.'),
        ('Instrumentos', 'contraste de instrumentos; cambio o recalibración si difieren más del **5 %** (NFPA 25, 8.1.1.2.23).'),
        ('Transmisión mecánica', 'lubricación del acople y de la caja de engranajes en ángulo recto.'),
        ('Sistema eléctrico', 'disparo del interruptor, inspección y operación de los medios de arranque manual de emergencia sin '
                              'energía eléctrica, ajuste de conexiones, lubricación de partes mecánicas móviles excepto arrancadores '
                              'y rieles, calibración del reinicio de presostatos y engrase de cojinetes del motor.'),
        ('Combustible', 'control de agua o material extraño en el tanque, verificación de que el venteo del tanque y la cañería de '
                        'sobreflujo están desobstruidos y control de la cañería de combustible.'),
        ('Lubricación del motor', 'cambio de aceite y de filtros de aceite cada **50 h** de marcha o anualmente (NFPA 25, '
                                  '8.1.1.2.17 y 8.1.1.2.18).'),
        ('Combustible diésel', 'análisis anual de degradación del combustible según la ASTM D975 o la ASTM D6751; si es deficiente, '
                               'se reacondiciona o reemplaza, se limpia el tanque y se cambian los filtros (NFPA 25, 8.3.4); el '
                               'filtro de combustible se cambia anualmente (8.1.1.2.19).'),
        ('Baterías del motor', 'verificación de la densidad, del estado de carga y del cargador; limpieza de terminales; tensión de '
                               'arranque mayor que **9 V** en sistemas de 12 V o que **18 V** en sistemas de 24 V; uso exclusivo de '
                               'agua destilada (NFPA 25, 8.1.1.2.15).'),
        ('Otros componentes del motor', 'reemplazo anual del filtro de agua de circulación, inspección de los ánodos de sacrificio, '
                                        'de las mangueras y conexiones flexibles y del escape, y prueba de la señal de supervisión '
                                        'de alta temperatura del agua de enfriamiento (NFPA 25, 8.1.1.2.8 a 8.1.1.2.22).'),
        ('Acoples elastoméricos', 'reemplazo cada **5 años** o según el fabricante (NFPA 25, 8.1.1.2.24).'),
        ('Enfriamiento', 'cambio de anticongelante, limpieza interior del intercambiador de calor e inspección de conductos y '
                         'limpieza de lumbreras.'),
        ('Escape', 'control de contrapresión excesiva y de colgantes y soportes del sistema.'),
        ('Sistema eléctrico del motor', 'ajuste de las conexiones de cableado de control y de potencia.'),
    ]))
    a(('p', 'La planilla IRAM 3546-12D asigna frecuencia mensual a la verificación de interruptores o fusibles del sistema '
            'eléctrico, y la 12E les asigna la frecuencia «B». Se adopta la verificación mensual, más exigente; la «B» se interpreta '
            'como bienal.'))
    a(('p', cierre(5)))

    # ---------------- COMPLEMENTARIAS ----------------
    a(('h3', 'SEGURIDAD Y SALUD OCUPACIONAL'))
    a(('p', 'La seguridad del personal tiene como finalidad evitar riesgos eléctricos, mecánicos e hidráulicos durante las pruebas.'))
    a(('p', 'Durante las tareas se debe asegurar:'))
    a(('items', [
        ('Partes eléctricas', 'respeto de las medidas de seguridad para la operación cerca de partes energizadas del controlador y '
                              'del motor, con elementos de protección personal adecuados.'),
        ('Partes rotantes', 'protecciones de acoples y ejes colocadas durante la marcha y prohibición de intervenir con el equipo en '
                            'funcionamiento.'),
        ('Bloqueo de arranque', 'antes de intervenir partes rotantes o eléctricas, pasar el controlador a posición apagado y abrir, '
                                'bloquear y etiquetar el seccionador; en motores diésel, colocar el selector en apagado y '
                                'desconectar los dos bancos de baterías. La intervención se trata como puesta fuera de servicio, '
                                'con aviso al responsable y al servicio de supervisión; al finalizar se retiran los bloqueos y se '
                                'verifica el selector en automático.'),
        ('Condición de trabajo eléctricamente segura', 'según la NFPA 70E (120.5), antes de trabajar en el controlador o en el '
                                                       'motor se deben, en este orden: determinar todas las fuentes de alimentación '
                                                       'con planos y etiquetas actualizados; interrumpir la carga y abrir el '
                                                       'dispositivo de desconexión de cada fuente; verificar visualmente que está '
                                                       'abierto; liberar la energía almacenada; bloquear o aliviar la energía no '
                                                       'eléctrica; aplicar los dispositivos de bloqueo y etiquetado según un '
                                                       'procedimiento documentado; y verificar la ausencia de tensión en cada '
                                                       'conductor, entre fases y entre fase y tierra, con un instrumento cuyo '
                                                       'funcionamiento se comprueba antes y después en una fuente conocida.'),
        ('Trabajo con el controlador energizado', 'cuando se deban reemplazar o recalibrar instrumentos con el controlador '
                                                  'energizado, se deben usar los elementos de protección personal que indique la '
                                                  'NFPA 70E (NFPA 25, 8.1.1.2.23.2).'),
        ('Descarga de agua', 'delimitación del área de descarga y control de los chorros para no generar daños a personas ni bienes.'),
        ('Motor diésel', 'ventilación de la sala y control de pérdidas de combustible y del sistema de escape.'),
    ]))

    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'Los cambios en la demanda del sistema, en la fuente de agua o en el equipo de bombeo pueden modificar el punto de '
            'trabajo de la bomba. Toda modificación se debe evaluar técnicamente y registrar en la planilla de información general. '
            'Cuando se reemplace, cambie o modifique un componente fundamental de la bomba, del impulsor o del controlador, se debe '
            'realizar una nueva prueba de rendimiento en campo y registrarla en la planilla SG-PEM-IFI-SBC-6 (NFPA 20, 14.5.2.1).'))
    a(('p', 'La interpretación de los datos de las pruebas debe ser realizada por personal experimentado en el tema. La empresa '
            'mantenedora es responsable de ejecutar las tareas y de verificar las inspecciones de autocontrol. El usuario o '
            'propietario es responsable de completar las inspecciones de autocontrol, de notificar al servicio de supervisión y de '
            'coordinar las puestas fuera de servicio.'))
    return C


def REGISTRO_EXTRA(cierre):
    return [
        'Los datos de la instalación, del riesgo protegido, de la sala de bombas, del abastecimiento de agua, de las bombas y de la '
        'toma de impulsión para bomberos se registran en la planilla SG-PEM-IFI-SBC-1 %s – %s.' % (NOM, PL[1]),
        'La documentación de diseño del sistema y los procedimientos de inspección, prueba y mantenimiento se deben conservar en '
        'un lugar aprobado y seguro durante toda la vida útil del sistema (NFPA 101, 9.11.3.1).',
        'El informe escrito de la prueba anual, que conserva el propietario, debe contener como mínimo todos los datos medidos para '
        'evaluar el desempeño de la bomba (presiones de succión y descarga, tensión y corriente y velocidad en cada caudal), la '
        'demanda del sistema informada por el propietario, el resultado satisfactorio o no satisfactorio, las deficiencias con sus '
        'recomendaciones, los datos de desempeño del fabricante y las curvas reales, los tiempos de arranque, parada y transferencia '
        'y, cuando corresponda, la comparación con las pruebas anteriores (NFPA 25, 8.4).',
        'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '
        'codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables se indican con NA. Toda '
        'condición O o X se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y '
        'por el responsable de la instalación, con su aclaración.',
    ]
