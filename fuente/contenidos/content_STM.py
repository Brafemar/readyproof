# -*- coding: utf-8 -*-
SIG, NOM, NOMU, CAP = 'STM', 'Sistema de Tuberías y Mangueras', 'SISTEMA DE TUBERÍAS Y MANGUERAS (RED DE AGUA)', '11'
PL = {1: 'Información general', 2: 'Inspección semanal (autocontrol)', 3: 'Inspección mensual',
      4: 'Inspección mensual de válvulas para mangas', 5: 'Prueba mensual y trimestral',
      6: 'Prueba hidrostática y de caudal de tuberías', 7: 'Inspección anual y mantenimiento semestral, anual y bienal',
      8: 'Prueba anual, bienal y quinquenal'}
VIG = (' Se aplica la edición vigente de cada norma NFPA; la numeración de los artículos citados se debe confirmar en esa '
       'edición, porque puede variar entre ediciones.')


def CONTENT(cierre):
    C = []; a = C.append
    a(('h2', NOMU))
    a(('basado', '(Basado en IRAM 3546:2011 – Capítulo %s; criterios complementarios: NFPA 14 y NFPA 25)' % CAP))
    a(('p', 'Este apartado establece los requisitos mínimos para la inspección, prueba y mantenimiento del sistema de tuberías y '
            'mangueras (red de agua), con el objetivo de asegurar que las bocas de incendio entreguen el caudal y la presión '
            'necesarios para el combate manual del fuego por los ocupantes, las brigadas o el servicio de bomberos.'))
    a(('p', 'La IRAM 3546:2011 es la base del presente procedimiento y fija sus frecuencias. La NFPA 25 (capítulos 6 y 13) se aplica '
            'como criterio complementario para la inspección, prueba y mantenimiento, y la NFPA 14, Norma para la instalación de '
            'sistemas de tubería vertical y de mangueras, para los valores de diseño que se deben conservar. Las mangueras y sus '
            'accesorios se rigen por la IRAM 3594. Ante diferencias, se adopta siempre la condición más exigente.' + VIG))
    a(('p', 'Las bocas de incendio de DN 63,5 mm son usualmente de uso profesional (bomberos, brigadas o personal calificado) y '
            'pueden estar equipadas, conocidas como bocas de incendio equipadas (BIE), o sin equipamiento; las de DN 44,5 mm están '
            'destinadas al uso por los ocupantes entrenados. Si una planta posee ambos sistemas, las bocas deben estar señalizadas e '
            'identificadas. El equipamiento del sistema incluye:'))
    a(('items', [
        ('Abastecimiento de agua', 'tanques o reservas y, cuando corresponde, bombas contra incendio, cuyo mantenimiento se rige por '
                                   'los capítulos 12 y 13 de la IRAM 3546:2011.'),
        ('Válvulas interceptoras', 'válvulas de corte de la red, precintadas, enclavadas o supervisadas.'),
        ('Red de tuberías', 'montantes, cañerías de distribución, soportes y sujeciones, húmedas o secas.'),
        ('Válvulas para mangas', 'válvulas de incendio tipo teatro y válvulas de uso profesional, con sus tapas y roscas.'),
        ('Bocas de incendio equipadas', 'gabinete, manguera, devanadera o soporte, lanza con boquilla de chorro y niebla, y llaves de '
                                        'ajuste de uniones.'),
        ('Equipos auxiliares, tales como', ''),
        ['dispositivos reguladores de presión (a resorte, con piloto, de presión diferencial o tanque ruptor);',
         'manómetros y dispositivos de alarma de flujo;',
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

    a(('h4', 'Inspección semanal (autocontrol)'))
    a(('p', 'La inspección semanal tiene como finalidad verificar que la red mantiene abiertas sus válvulas y que las válvulas para '
            'mangas y los reguladores de presión están en condiciones de uso.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Válvulas interceptoras', 'en redes con abastecimiento permanente, comprobar el modo preventivo en que se encuentran '
                                   '(precintadas, enclavadas o supervisadas) y que están en su posición normal.'),
        ('Válvulas para mangas', 'comprobar que el volante existe y no está deteriorado, que la salida roscada está sana y operable, '
                                 'que la tapa está en su lugar y que no hay fugas en la válvula ni en su conexión a la cañería.'),
        ('Dispositivos reguladores de presión', 'comprobar que las válvulas habilitantes o de servicio están abiertas, que los '
                                                'manómetros se pueden leer y que la válvula piloto, si existe, está en condiciones '
                                                'de uso.'),
    ]))
    a(('p', 'La NFPA 25 (13.5.4.1) establece también la inspección semanal de las válvulas reductoras de presión principales, para '
            'verificar que mantienen las presiones normales aguas arriba y aguas abajo y que no presentan daños ni pérdidas.'))
    a(('p', cierre(2)))

    a(('h4', 'Inspección mensual'))
    a(('p', 'La inspección mensual tiene como finalidad verificar que las bocas de incendio y su equipamiento están completos, '
            'señalizados y disponibles para su uso inmediato.'))
    a(('p', 'En las bocas de incendio equipadas se debe verificar:'))
    a(('items', [
        ('Manguera', 'comprobar visualmente que no está dañada y que está correctamente enrollada o plegada sobre su soporte, con '
                     'sus uniones y la lanza con su boquilla colocadas. Todas las mangueras y sus accesorios deben cumplir la '
                     'IRAM 3594.'),
        ('Válvula, lanza, gabinete y manguera', 'completar la revisión de cada boca según la planilla de inspección mensual de '
                                                'válvulas para mangas: tapa, volante, tuerca del volante y llave de ajuste de '
                                                'uniones; junta y boquilla de la lanza; vidrio, cerradura, bisagras, puerta y '
                                                'pintura del gabinete; humedad, estado de las uniones, junta, tipo, diámetro, '
                                                'longitud y vigencia de la prueba hidrostática de la manguera.'),
        ('Señalización', 'comprobar que las bocas están señalizadas.'),
    ]))
    a(('p', 'En las bocas de incendio sin equipamiento se debe verificar:'))
    a(('items', [
        ('Tapas y volantes', 'comprobar que las tapas están colocadas y son fácilmente operables, y que los volantes o elementos de '
                             'apertura están sanos y utilizables.'),
        ('Gabinetes o armarios de material', 'comprobar que existe el listado de materiales, que el material está disponible y que '
                                             'las uniones son compatibles en diámetro y tipo con las existentes en la planta.'),
    ]))
    a(('p', 'Para todo el sistema se debe verificar además:'))
    a(('items', [
        ('Toma de impulsión para bomberos', 'comprobar que está accesible y sin obstrucciones.'),
        ('Válvula interceptora', 'comprobar el modo preventivo en que se encuentra.'),
        ('Abastecimiento de agua', 'comprobar el nivel de todos los depósitos que abastecen a la bomba contra incendio, según el '
                                   'capítulo 13 de la IRAM 3546:2011.'),
        ('Bomba contra incendio', 'comprobar que está completa y en condiciones de uso.'),
    ]))
    a(('p', 'La NFPA 25 asigna frecuencia anual a la inspección de mangueras, lanzas, devanaderas y gabinetes (6.2.6 a 6.2.9); la '
            'frecuencia mensual de la IRAM 3546:2011 es más exigente y se mantiene. De la NFPA 25 se toman los siguientes criterios '
            'de rechazo, que se incorporan a la inspección mensual:'))
    a(('items', [
        ('Manguera', 'moho, cortes, abrasión o deterioro; roscas de las uniones dañadas o incompatibles; juntas faltantes o '
                     'deterioradas; manguera no conectada a la válvula o al soporte (6.2.6.1).'),
        ('Lanza', 'faltante, sin junta o con junta deteriorada, obstruida o que no opera suavemente (6.2.7.1).'),
        ('Devanadera o soporte', 'difícil de operar, dañado u obstruido; manguera mal enrollada o plegada; lanza fuera de su '
                                 'sujeción; soporte dentro del gabinete que no gira como mínimo **90°** (6.2.8.1).'),
        ('Gabinete', 'partes corroídas o dañadas; difícil de abrir; puerta que no abre totalmente; vidrio rajado o roto; cerradura '
                     'del gabinete de rotura de vidrio que no funciona; dispositivo de rotura faltante; falta de identificación como '
                     'gabinete de equipo contra incendio; obstrucciones visibles o físicas; equipamiento faltante (6.2.9.1).'),
    ]))
    a(('p', 'Las verificaciones de las bocas de incendio equipadas se registran en dos planillas: la de inspección mensual del '
            'sistema y la de inspección mensual de válvulas para mangas, que admite el registro individual de cada boca.'))
    a(('p', cierre(3)))
    a(('p', cierre(4)))

    a(('h4', 'Inspección anual'))
    a(('p', 'La inspección anual tiene como finalidad detectar el deterioro de la red de tuberías y de sus soportes.'))
    a(('p', 'Durante esta inspección se debe verificar que las tuberías y sus soportes estén libres de:'))
    a(('items', [
        ['daños;', 'corrosión;', 'materiales extraños;', 'manipulación indebida;', 'cambios edilicios que los afecten;',
         'obstrucciones;', 'crecimiento de follaje.'],
    ]))
    a(('p', 'Se debe verificar además que las tuberías no se usan como soporte de elementos ajenos al sistema, que los soportes, '
            'abrazaderas y sujeciones no están dañados, sueltos ni desprendidos, y que el cartel de datos del cálculo hidráulico está '
            'presente, bien sujeto y legible; un sistema que no fue dimensionado por cálculo hidráulico debe tener un cartel que lo '
            'indique (NFPA 25, 6.2.2, 6.2.4 y 6.2.5). Las tuberías y soportes situados en espacios ocultos no requieren inspección, '
            'y los situados en áreas inaccesibles por razones de seguridad del proceso se inspeccionan en cada parada programada.'))
    a(('p', cierre(7)))

    # ---------------- PRUEBA ----------------
    a(('h3', 'PRUEBA'))
    a(('p', 'Las pruebas tienen como propósito verificar la presión y el caudal disponibles en las bocas de incendio, la operación de '
            'las alarmas y de las válvulas, y la estanqueidad de la red. El mantenimiento se debe realizar inmediatamente después de '
            'las pruebas que detectan fallas.'))
    a(('p', 'Donde el agua pueda causar daños, antes de introducir agua en el sistema se debe realizar una prueba con aire a '
            '**1,7 bar** (25 psi) (NFPA 25, 6.3).'))

    a(('h4', 'Prueba mensual'))
    a(('p', 'La prueba mensual tiene como finalidad verificar que todas las bocas de la red tienen presión y, en sistemas con bombas, '
            'que estas arrancan ante la demanda.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Presión hidrostática en las bocas', 'controlar la presión en todas las bocas de la red después de descargar unos **15 L** '
                                              'de agua de cada una. En instalaciones con montantes verticales, el control se '
                                              'realiza como mínimo en bocas separadas **20 m** como máximo en dirección vertical, '
                                              'de modo que anualmente se haya controlado la totalidad de las bocas.'),
        ('Arranque de las bombas', 'en sistemas con bombas, abrir el **5 %** de las bocas, como mínimo una, para poner en marcha '
                                   'las bombas principales.'),
    ]))
    a(('p', 'Como referencia de diseño, la NFPA 14 (10.2.4) limita la presión en las conexiones para mangueras: donde la presión '
            'residual en una conexión de 40 mm para uso de personal entrenado supera los **6,9 bar** (100 psi), o la presión estática '
            'o residual en cualquier conexión supera los **12 bar** (175 psi), se debe contar con un dispositivo regulador de presión '
            'listado. Una lectura superior a esos valores se registra como no conformidad.'))
    a(('p', cierre(5)))

    a(('h4', 'Prueba trimestral'))
    a(('p', 'La prueba trimestral tiene como finalidad verificar las válvulas, las alarmas de flujo y la toma de impulsión para '
            'bomberos.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Válvulas interceptoras', 'en redes con abastecimiento permanente, comprobar que están en el modo preestablecido.'),
        ('Válvulas para mangas de uso profesional', 'comprobar que no están dañadas y que las tapas protectoras están en su lugar y '
                                                    'son fácilmente removibles; la NFPA 25 (13.6.1.1) agrega que las roscas y los '
                                                    'volantes no estén dañados, que las juntas no estén deterioradas, que no haya '
                                                    'pérdidas ni obstrucciones y que las tapas no aptas para presión tengan un '
                                                    'orificio de alivio.'),
        ('Alarmas de flujo', 'dejar fluir el agua a través del sistema hasta que se activen las alarmas de flujo; las alarmas '
                             'mecánicas deben sonar dentro de los **5 min** y los interruptores de paleta o presostatos deben dar '
                             'la señal dentro de los **90 s** (NFPA 25, 13.2.3).'),
        ('Toma de impulsión para bomberos', 'operarla para constatar su funcionamiento y que no está obstruida, que las tapas o '
                                            'tapones están en su lugar y se pueden extraer fácilmente y, si tiene anilla '
                                            'giratoria, que gira. La NFPA 25 (13.8.1) agrega que la señalización, las juntas, la '
                                            'válvula de retención sin pérdidas, el drenaje automático, las clapetas y la cañería '
                                            'visible estén en buen estado.'),
        ('Arranque de las bombas', 'en sistemas con bombas, realizar la puesta en marcha con el **10 %** de las bocas abiertas, '
                                   'como mínimo una.'),
        ('Válvulas reductoras de presión', 'comprobar que están abiertas, sin pérdidas, con su volante y manteniendo la presión de '
                                           'diseño aguas abajo (NFPA 25, 13.5.1.1).'),
    ]))
    a(('p', cierre(5)))

    a(('h4', 'Prueba anual'))
    a(('p', 'La prueba anual tiene como finalidad verificar en cada boca de incendio la presión y el alcance del chorro, el '
            'funcionamiento de las lanzas, de las válvulas y de los reguladores de presión, y el estado de las mangueras.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Bombas contra incendio', 'probarlas si forman parte del abastecimiento de agua, según el capítulo 12 de la IRAM 3546:2011.'),
        ('Ensayo hidrodinámico de presión y alcance', 'realizarlo en cada boca de incendio con tubo Pitot o con boquillas calibradas, '
                                                      'y el ensayo de alcance con los elementos de la planta. Si por razones '
                                                      'técnicas de espacio o de situación no es posible, se reemplaza por una '
                                                      'medición volumétrica de caudal y de presión hidrostática en bocas separadas '
                                                      '**40 m** como máximo en dirección vertical.'),
        ('Lanzas', 'comprobar que las boquillas pasan fácilmente de chorro a niebla.'),
        ('Mangueras', 'realizar las inspecciones, pruebas, ensayos y mantenimiento establecidos en la IRAM 3594.'),
        ('Prueba de pérdidas de tuberías secas', 'la planilla IRAM 3546-11H pide probar las tuberías secas a **1,7 MPa** durante '
                                                 '**2 h**; antes de ejecutarla se debe verificar que esa presión no supera la '
                                                 'presión nominal de los componentes instalados.'),
        ('Prueba de caudal', 'dejar fluir el agua por la salida hidráulicamente más desfavorable; el caudal mínimo sugerido en '
                             'instalaciones industriales es de **500 L/min** con una presión residual de **450 kPa**.'),
        ('Dispositivos reguladores de presión', 'probar a caudal total las salidas equipadas con reguladores, para comprobar que '
                                                'suministran el caudal adecuado, y anotar la presión de cada salida en una hoja '
                                                'adjunta a la planilla; cada válvula reductora para manguera se debe operar '
                                                'además en todo su recorrido (NFPA 25, 13.5.2.2).'),
        ('Válvulas para mangas de sistemas clase I y clase III', 'abrirlas y cerrarlas totalmente, y reparar o reemplazar las que '
                                                                 'sean difíciles de operar o pierdan (NFPA 25, 13.6.2.1).'),
    ]))
    a(('p', 'La planilla IRAM 3546-11H indica la prueba anual de caudal en la salida «más favorable», mientras que el texto del '
            'capítulo y la planilla 3546-11F la indican en la «más desfavorable». Se adopta la salida hidráulicamente más '
            'desfavorable, coincidente con la NFPA 25 (6.3.1.1). La prueba anual a caudal total de los reguladores de presión de la '
            'IRAM es más exigente que la de la NFPA 25, que pide prueba de caudal cada **5 años** (13.5.2.3) y prueba de flujo '
            'parcial anual para las válvulas reductoras de la red (13.5.1.3), y se mantiene.'))
    a(('p', 'Cuando se descarga por boquillas, el caudal de cada una se calcula con la presión medida con tubo Pitot en el centro '
            'del chorro mediante **Q = 0,0666 · c · d² · √P** (Q en L/min, d en mm, P en kPa, c coeficiente de la boquilla).'))
    a(('p', cierre(8)))
    a(('protocol', ('ensayo hidrodinámico de presión y alcance', [
        ('Preparación', [
            ('Paso a paso', 'notificar al servicio de supervisión, delimitar la zona de descarga, verificar que el drenaje puede '
                            'evacuar el agua y preparar el tubo Pitot o las boquillas calibradas y un manómetro calibrado.'),
            ('Justificación técnica', 'la descarga de una boca de 63,5 mm genera una fuerza de reacción y un volumen de agua que '
                                      'pueden causar daños.'),
            ('Criterio de aceptación', 'zona delimitada, drenaje disponible e instrumentos calibrados.')]),
        ('Presión estática', [
            ('Paso a paso', 'con la boca cerrada y la manguera conectada, registrar la presión estática en la boca.'),
            ('Justificación técnica', 'la diferencia entre la presión estática y la residual indica las pérdidas de la red y la '
                                      'capacidad del abastecimiento.'),
            ('Criterio de aceptación', 'lectura registrada y comparable con la de la prueba anterior.')]),
        ('Descarga', [
            ('Paso a paso', 'abrir totalmente la válvula de la boca con la manguera tendida sin dobleces, con la boquilla a chorro '
                            'pleno; medir con tubo Pitot la presión en el centro del chorro, a medio diámetro de la salida, y '
                            'registrar la presión residual en la boca y el alcance del chorro.'),
            ('Qué se determina con la lectura', 'la presión del Pitot permite calcular el caudal; un alcance menor que el de la '
                                                'prueba anterior indica una pérdida de presión o una obstrucción.'),
            ('Criterio de aceptación', 'caudal y presión residual no menores que los de diseño; en la boca más desfavorable, '
                                       'como mínimo **500 L/min** en DN 63,5 mm o **300 L/min** en DN 44,5 mm, con **450 kPa** '
                                       'de presión residual.')]),
        ('Chorro y niebla', [
            ('Paso a paso', 'pasar la boquilla de chorro a niebla y viceversa durante la descarga.'),
            ('Justificación técnica', 'una boquilla trabada impide al operador protegerse con la cortina de niebla.'),
            ('Criterio de aceptación', 'cambio de chorro a niebla sin dificultad.')]),
        ('Normalización', [
            ('Paso a paso', 'cerrar lentamente la válvula, drenar y secar la manguera según la IRAM 3594 antes de volver a '
                            'colocarla, y notificar la conclusión al servicio de supervisión.'),
            ('Justificación técnica', 'el cierre brusco produce golpe de ariete; la manguera guardada húmeda se deteriora.'),
            ('Criterio de aceptación', 'boca cerrada, sin pérdidas y con la manguera seca y colocada.')]),
    ])))

    a(('h4', 'Prueba bienal'))
    a(('p', 'La prueba bienal tiene como finalidad verificar la resistencia de las mangueras.'))
    a(('p', 'Durante esta prueba se debe realizar:'))
    a(('items', [
        ('Prueba hidráulica de mangueras', 'prueba de cada manguera según la IRAM 3594, con la frecuencia que esa norma establezca '
                                           'para su tipo, de uno o dos años, y registro de la fecha de la prueba vigente.'),
    ]))
    a(('p', cierre(8)))

    a(('h4', 'Prueba quinquenal'))
    a(('p', 'La prueba quinquenal tiene como finalidad verificar la estanqueidad de las tuberías secas y la capacidad de la red en '
            'su salida más desfavorable.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Prueba hidrostática de tuberías secas', 'mantener la presión de prueba durante **2 h**, registrando la presión inicial, la '
                                                  'hora de comienzo, la hora final y la presión al final de la prueba.'),
        ('Sistemas reparados', 'probar con aire a **1,7 bar** (170 kPa) los sistemas que estuvieron fuera de servicio para su '
                               'reparación, para asegurar su estanqueidad.'),
        ('Sistemas modificados', 'probar hidrostáticamente todo sistema que haya sido modificado.'),
        ('Prueba de flujo', 'realizarla desde la salida hidráulicamente más desfavorable, registrando la presión estática, el '
                            'diámetro de la boquilla, el caudal, la presión manométrica y la presión en el piloto. El caudal mínimo '
                            'sugerido es de **500 L/min** para bocas de DN 63,5 mm y de **300 L/min** para bocas de DN 44,5 mm, con '
                            'una presión residual de **450 kPa**, que se debe mantener en la boca inmediata a la o las que se estén '
                            'utilizando, según la simultaneidad requerida por el riesgo.'),
        ('Válvula reguladora de presión', 'probarla con flujo de agua para asegurar que reduce la presión y suministra el caudal '
                                          'adecuado a la salida equipada con ella.'),
        ('Lanzas', 'probarlas hidráulicamente a **1,7 MPa**.'),
    ]))
    a(('p', 'La presión de la prueba hidrostática presenta valores distintos en la IRAM 3546:2011: el texto indica **340 kPa** sobre '
            'la presión nominal de trabajo y la planilla 3546-11F indica **1380 kPa** por encima de la presión normal si esta excede '
            'de 1000 kPa. Se adopta el criterio de la NFPA 25 (6.3.2.1), que concilia ambos valores: la prueba se realiza a no menos '
            'de **13,8 bar** (200 psi) durante **2 h** o, cuando la presión máxima del sistema supera los **10,3 bar** (150 psi), a '
            '**3,4 bar** (50 psi) por encima de esa presión máxima, incluida la cañería de la toma de impulsión para bomberos. La '
            'presión se mide en el punto más bajo del sistema o zona probada; la tubería no debe mostrar pérdidas visibles y una '
            'caída de **0,3 bar** (5 psi) o menos no se considera falla (NFPA 25, 6.3.2.2). Después de cada prueba hidrostática de '
            'una tubería seca se debe drenar completamente el sistema, para que no quede expuesto a congelamiento.'))
    a(('p', 'En los sistemas automáticos, la NFPA 25 (6.3.1) exige que la prueba de flujo verifique la demanda del sistema según el '
            'criterio de diseño vigente a la fecha de la instalación. En los sistemas diseñados por la NFPA 14, esa demanda es de '
            '**1892 L/min** (500 gpm) en la columna más remota más **946 L/min** (250 gpm) por cada columna adicional en las clases I y '
            'III, y de **379 L/min** (100 gpm) en la clase II, con una presión residual mínima de **6,9 bar** (100 psi) en la '
            'conexión de 65 mm más remota y de **4,5 bar** (65 psi) en la de 40 mm (NFPA 14, 10.2.6.1). En esos sistemas se adoptan '
            'esos valores, más exigentes que los sugeridos por la IRAM 3546:2011. Si no se puede determinar la demanda de diseño, la '
            'define la autoridad competente.'))
    a(('p', cierre(6)))
    a(('p', cierre(8)))
    a(('protocol', ('prueba hidrostática de tuberías secas', [
        ('Preparación', [
            ('Paso a paso', 'aislar el sistema o zona a probar, cerrar las válvulas para mangas, instalar un manómetro calibrado en '
                            'el punto más bajo y conectar la bomba de prueba en la toma de impulsión o en una conexión de prueba.'),
            ('Justificación técnica', 'la presión se debe medir en el punto más bajo, donde es máxima.'),
            ('Criterio de aceptación', 'sistema aislado y manómetro calibrado instalado.')]),
        ('Purga de aire', [
            ('Paso a paso', 'llenar el sistema con agua desde el punto más bajo, purgando el aire por las válvulas más altas.'),
            ('Justificación técnica', 'el aire atrapado se comprime y falsea la lectura de la prueba.'),
            ('Criterio de aceptación', 'salida de agua sin aire por los puntos de purga.')]),
        ('Presurización y espera', [
            ('Paso a paso', 'elevar la presión hasta la presión de prueba, registrar la presión inicial y la hora, y mantenerla '
                            'durante **2 h** sin bombeo, recorriendo la red para detectar pérdidas.'),
            ('Justificación técnica', 'el tiempo de espera permite detectar pérdidas pequeñas en uniones y accesorios.'),
            ('Criterio de aceptación', 'sin pérdidas visibles y con una caída de presión no mayor que **0,3 bar**.')]),
        ('Drenaje', [
            ('Paso a paso', 'despresurizar lentamente, drenar completamente el sistema por sus puntos bajos y restituir las válvulas '
                            'a su posición normal.'),
            ('Justificación técnica', 'el agua remanente en una tubería seca se congela o corroe la cañería.'),
            ('Criterio de aceptación', 'sistema drenado y en su condición normal.')]),
    ])))

    # ---------------- MANTENIMIENTO ----------------
    a(('h3', 'MANTENIMIENTO'))
    a(('p', 'El mantenimiento debe asegurar que todos los componentes y equipos que forman el sistema estén operativos y confiables, '
            'y se debe realizar inmediatamente después de las pruebas que detectan fallas.'))

    a(('h4', 'Mantenimiento semestral'))
    a(('p', 'El mantenimiento semestral tiene como finalidad evitar que las mangueras se deterioren en los puntos de plegado.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Mangueras', 'retiro de las mangueras de sus soportes y nuevo enrollado o plegado según la IRAM 3594, de modo que partes '
                      'diferentes de la manguera queden en las curvas o dobleces.'),
        ('Juntas de las uniones', 'verificación del estado de las juntas y reemplazo de las deterioradas.'),
        ('Racores y devanaderas', 'engrase con grafito o grafito con aceite liviano de los racores y de los puntos giratorios de las '
                                  'devanaderas.'),
    ]))
    a(('p', cierre(7)))

    a(('h4', 'Mantenimiento anual'))
    a(('p', 'El mantenimiento anual tiene como finalidad conservar operables las boquillas y los racores, y verificar el estado de '
            'la tubería.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Tuberías', 'inspección de todas las partes accesibles para comprobar que no están dañadas ni corroídas.'),
        ('Boquillas', 'apertura y cierre de todas las boquillas para comprobar que operan con facilidad, y lubricación con grafito '
                      'si es necesario.'),
        ('Racores', 'lubricación de todos los racores con grafito.'),
        ('Enrollado de mangueras', 'desconexión y nuevo enrollado de la manguera según la IRAM 3594, con comprobación y sustitución '
                                   'de las juntas deterioradas.'),
        ('Válvulas para mangas', 'lubricación, reparación o reemplazo de las que no operan suavemente o no abren totalmente '
                                 '(NFPA 25, 13.6.3).'),
    ]))
    a(('p', cierre(7)))

    a(('h4', 'Mantenimiento bienal'))
    a(('p', 'El mantenimiento bienal tiene como finalidad conservar la operabilidad de las válvulas para mangas.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Válvulas para mangas', 'recorrido completo de todas las válvulas tipo teatro, con cambio de los obturadores si son de goma. '
                                 'En los sistemas clase II y en las bocas conectadas a sistemas de rociadores, la NFPA 25 '
                                 '(13.6.2.2) pide esta operación cada **3 años**; la frecuencia bienal de la IRAM es más exigente '
                                 'y se mantiene.'),
    ]))
    a(('p', cierre(7)))

    # ---------------- COMPLEMENTARIAS ----------------
    a(('h3', 'PUESTA FUERA DE SERVICIO'))
    a(('p', 'La puesta fuera de servicio tiene como finalidad limitar el riesgo y la duración de cualquier interrupción de la red, '
            'programada o de emergencia, según el capítulo 15 de la NFPA 25.'))
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
        ('Tarjeta de fuera de servicio', 'colocación de una tarjeta en cada toma de impulsión para bomberos y en la válvula de '
                                         'control del sistema.'),
    ]))
    a(('p', 'Al restablecer el sistema se deben realizar las inspecciones y pruebas que verifiquen su funcionamiento, informar a '
            'todas las partes notificadas y retirar la tarjeta.'))

    a(('h3', 'SEGURIDAD Y SALUD OCUPACIONAL'))
    a(('p', 'La seguridad del personal tiene como finalidad evitar los riesgos de las descargas de agua a presión y de las pruebas '
            'hidrostáticas.'))
    a(('p', 'Durante las tareas se debe asegurar:'))
    a(('items', [
        ('Reacción de la lanza', 'operación de las lanzas de 63,5 mm por dos personas como mínimo y apertura y cierre lentos de las '
                                 'válvulas para evitar el latigazo de la manguera y el golpe de ariete.'),
        ('Zona de descarga', 'delimitación de la zona alcanzada por el chorro y control de que el agua no alcance equipos '
                             'energizados ni bienes sensibles.'),
        ('Prueba hidrostática', 'permanencia fuera de la proximidad de uniones y tapas mientras la red está presurizada y '
                                'despresurización antes de ajustar cualquier unión.'),
        ('Elementos de protección personal', 'uso de calzado de seguridad, guantes y protección ocular durante las descargas.'),
    ]))

    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'Las modificaciones de la red, del abastecimiento o de la distribución de los ambientes pueden alterar la presión '
            'disponible en las bocas. Toda modificación se debe evaluar técnicamente y registrar en la planilla de información '
            'general, y todo sistema modificado se debe probar hidrostáticamente.'))
    a(('p', 'La empresa mantenedora es responsable de ejecutar las tareas de inspección, prueba y mantenimiento y de verificar las '
            'inspecciones de autocontrol. El usuario o propietario es responsable de completar las inspecciones de autocontrol, de '
            'mantener las bocas accesibles y señalizadas y de coordinar las puestas fuera de servicio.'))
    return C


def REGISTRO_EXTRA(cierre):
    return [
        'Los datos de la instalación, de las mangueras, de los reguladores de presión, de las válvulas interceptoras y de incendio, '
        'del abastecimiento de agua, de las bombas y de la toma de impulsión para bomberos se registran en la planilla '
        'SG-PEM-IFI-%s-1 %s – %s.' % (SIG, NOM, PL[1]),
        'Después de cada prueba de caudal de una válvula reductora para manguera se debe colocar en la válvula una tarjeta con la '
        'fecha, el caudal, las presiones estática y residual de entrada y la presión residual de salida (NFPA 25, 13.5.2.4).',
        'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '
        'codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables se indican con NA. Toda '
        'condición O o X se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y '
        'por el responsable de la instalación, con su aclaración.',
    ]
