# -*- coding: utf-8 -*-
SIG, NOM, NOMU, CAP = ('SCC', 'Sistema Fijo de Extinción para Cocinas Comerciales',
                       'SISTEMA FIJO DE EXTINCIÓN PARA COCINAS COMERCIALES', '16')
PL = {1: 'Información general', 2: 'Inspección mensual', 3: 'Prueba semestral y quinquenal', 4: 'Mantenimiento',
      5: 'Verificación de aptitud del sistema (UL 300 y NFPA 96)'}
VIG = (' Se aplica la edición vigente de cada norma UL y NFPA citada; la numeración de los artículos se debe confirmar en esa '
       'edición, porque puede variar entre ediciones.')
AVISO = ('Antes de realizar cualquier actividad de inspección o prueba que pueda generar alarmas, cortes de gas o de energía, o '
         'descargas, se debe notificar al responsable de la instalación, al personal de cocina y al servicio de monitoreo '
         'correspondiente, y acordar el horario de la intervención fuera de los períodos de cocción.')


def CONTENT(cierre):
    C = []; a = C.append
    a(('h2', NOMU))
    a(('basado', '(Basado en IRAM 3546:2011 – Capítulo %s; criterios complementarios: NFPA 96, UL 300 y NFPA 72)' % CAP))
    a(('p', 'Este apartado establece los requisitos mínimos para la inspección, prueba y mantenimiento de los sistemas fijos de '
            'extinción que protegen equipos de cocción comercial, campanas, plenos y conductos de extracción en restaurantes, '
            'locales gastronómicos, comedores y usos similares, con el objetivo de asegurar que el sistema detecte el incendio, '
            'corte el suministro de gas y de energía de los artefactos y descargue el agente extintor sobre todas las superficies '
            'protegidas, en las condiciones con las que fue ensayado y listado.'))
    a(('p', 'La IRAM 3546:2011, en su capítulo 16, es la base del presente procedimiento y fija sus frecuencias. La UL 300, Ensayo '
            'de fuego de sistemas de extinción para la protección de equipos de cocción comercial, es la norma con la que se '
            'ensayan y listan los sistemas preingenierizados para cocinas; no establece tareas de mantenimiento, sino las '
            'condiciones de desempeño que el sistema instalado debe conservar (UL 300, 1.1). Por eso sus criterios se aplican en '
            'la verificación de aptitud del sistema, en el relevamiento inicial y después de cada cambio en la línea de cocción. '
            'La NFPA 96, Norma para el control de la ventilación y la protección contra incendio de las operaciones de cocción '
            'comercial, exige que esos sistemas cumplan la UL 300 u otras normas equivalentes (NFPA 96, 10.2.3) y fija los requisitos de protección, de '
            'cortes de seguridad, de accionamiento, de operación y de inspección, mantenimiento y limpieza de la campana, los '
            'filtros, el conducto y el sistema de extinción. La NFPA 72 se aplica a la central '
            'electrónica de comando y a su vinculación con el sistema de alarma del edificio. Ante diferencias, se adopta siempre '
            'la condición más exigente.' + VIG))
    a(('p', 'Para las instalaciones de cocina se aplica este procedimiento; el procedimiento SG-PEM-IFI-SSA se mantiene para los '
            'demás riesgos protegidos con solución acuosa. La protección de la cocina comprende el sistema automático de extinción, '
            'como protección primaria, y los extintores portátiles, como respaldo secundario (NFPA 96, 10.2.1); el sistema debe '
            'proteger los artefactos que producen vapores con grasa, los dispositivos de remoción de grasa, el pleno de la campana y '
            'el conducto de extracción (NFPA 96, 10.1.1 y 10.1.2).'))

    # ---------------- DESCRIPCIÓN ----------------
    a(('p', 'El fuego de cocina se desarrolla sobre aceites y grasas vegetales o animales a alta temperatura y se clasifica como '
            'fuego de clase K. El agente extintor habitual es una solución acuosa de sales de potasio, como el acetato de potasio, '
            'que enfría el aceite y forma sobre su superficie una capa jabonosa que impide la reignición.'))
    a(('p', 'El equipamiento del sistema incluye:'))
    a(('items', [
        ('Cilindro de agente', 'recipiente que almacena la solución extintora con su válvula, manómetro y soporte a la pared. En '
                               'la mayoría de las instalaciones es de presión contenida: el agente y el gas expelente, nitrógeno '
                               'seco, se almacenan en el mismo cilindro. Algunos diseños usan, en cambio, un cartucho o un '
                               'recipiente de gas expelente independiente.'),
        ('Línea de detección', 'fusibles metálicos ubicados en arcos portadetectores sobre los artefactos y en la entrada del '
                               'conducto, unidos por un cable de acero que corre por una tubería de detección con poleas de '
                               'esquina hasta el mecanismo de disparo, con su tensor.'),
        ('Mecanismo de disparo', 'módulo mecánico o central electrónica de comando, con su interfaz mecánico-eléctrica, que '
                                 'acciona la válvula del cilindro en forma mecánica, neumática o mediante un explosor '
                                 'pirotécnico.'),
        ('Disparo manual', 'pulsador o estación de accionamiento manual, ubicado en la vía de salida de la cocina.'),
        ('Red de descarga', 'tubería que conduce el agente desde el cilindro hasta las toberas.'),
        ('Toberas', 'boquillas de descarga dirigidas a cada artefacto, al pleno y filtros de la campana y al conducto de '
                    'extracción, con sus capuchones de protección contra la grasa.'),
        ('Cortes de seguridad', 'válvula de corte de gas, mecánica o electroválvula, y corte de la energía eléctrica de los '
                                'artefactos protegidos.'),
        ('Señalización y vinculación', 'indicaciones sonoras y luminosas de la central y, donde exista, la vinculación con el '
                                       'sistema de alarma o de monitoreo del edificio.'),
        ('Fuentes de energía de la central', 'alimentación principal desde la red eléctrica y alimentación secundaria por batería, con su cargador.'),
    ]))
    a(('p', 'Cuando la temperatura en la campana alcanza la temperatura nominal de un fusible, este se funde, el cable de acero '
            'pierde tensión y el mecanismo de disparo acciona la válvula del cilindro; en los sistemas electrónicos, la central '
            'recibe la señal y activa el explosor. El agente se descarga en forma simultánea por todas las toberas sobre los '
            'artefactos, el pleno y el conducto, y la actuación corta el gas y la energía de los artefactos, condición necesaria '
            'para evitar la reignición del aceite. El pulsador manual permite la descarga inmediata ante un fuego advertido por el '
            'personal, antes de la actuación de los fusibles.'))
    a(('p', 'La central electrónica de comando presenta, en general, las siguientes indicaciones. La denominación, el color y el '
            'comportamiento de cada una se deben confirmar con el manual del fabricante de la central instalada.'))
    a(('table', [
        ['Indicación', 'Señal', 'Condición normal', 'Acción ante la señal'],
        ['Encendido (alimentación principal)', 'Luz verde fija', 'Encendida', 'Si se apaga, verificar la alimentación de red'],
        ['Alimentación secundaria', 'Luz ámbar fija', 'Apagada', 'Funciona con batería: restituir la red'],
        ['Batería baja o falla de alimentación', 'Luz roja destellante y sonido', 'Apagada', 'Verificar batería y cargador'],
        ['Extinción conectada', 'Luz verde fija', 'Encendida', 'Si se apaga, el disparo no está conectado: sistema fuera de servicio'],
        ['Disparo de extinción', 'Luz roja destellante y sonido', 'Apagada', 'Aplicar el procedimiento posterior a una descarga'],
        ['Falla de línea de detección', 'Luz roja destellante y sonido', 'Apagada', 'Revisar fusibles, cable y conexiones'],
        ['Falla de línea de disparo', 'Luz roja destellante y sonido', 'Apagada', 'Revisar explosor y su conexión'],
        ['Falla de comando de válvula de gas', 'Luz roja destellante y sonido', 'Apagada', 'Revisar electroválvula y su línea'],
    ]))
    a(('p', 'Los pulsadores de silenciar alarma y de reposición del sistema solo deben ser operados por el personal del mantenedor '
            'o por personal capacitado del usuario, después de identificar la causa de la señal.'))
    a(('p', AVISO))


    # ---------------- INSPECCIÓN ----------------
    a(('h3', 'INSPECCIÓN'))
    a(('p', 'La inspección consiste en la verificación visual del sistema y de sus componentes, con el fin de comprobar que se '
            'encuentran en condiciones aparentemente óptimas de operación y libres de daños físicos, y que el riesgo protegido no '
            'ha sido modificado.'))
    a(('p', 'Las planillas de inspección cuya frecuencia sea menor a un mes pueden ser completadas por el usuario de la instalación '
            'y se deben identificar como inspecciones de autocontrol; en este sistema la norma no establece inspecciones de '
            'frecuencia menor a un mes. La inspección mensual es exigencia de la IRAM 3546:2011 aunque el contrato solo prevea los '
            'servicios semestrales; si no está contratada, se debe dejar constancia en el informe.'))
    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica previa '
            'de la instalación según la IRAM 3619, junto con la verificación del apartado de criterios de aptitud del sistema; la '
            'evaluación no es obligatoria y puede ser solicitada por cualquiera de las partes interesadas.'))

    a(('h4', 'Inspección mensual'))
    a(('p', 'Las inspecciones mensuales tienen como finalidad verificar que las toberas, los elementos de detección y disparo y '
            'los cortes de seguridad se mantienen en las condiciones de diseño y que la línea de cocción no ha sido modificada.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Capuchones de las toberas', 'verificar que se encuentran colocados.'),
        ('Acumulación de grasa', 'verificar que no hay grasa acumulada en los fusibles, en el cable de detección ni en las toberas.'),
        ('Productos de limpieza', 'verificar que no se utiliza ningún tipo de solución corrosiva para la limpieza de fusibles, cables '
                                  'y toberas.'),
        ('Equipos de cocina', 'verificar que no se ha instalado, reemplazado, reubicado ni modificado ningún artefacto, lo que '
                              'implica instalar nuevas toberas o redistribuir las existentes.'),
        ('Orientación de las toberas', 'verificar que apuntan a las superficies que protegen, tal como se diseñaron.'),
        ('Filtros de la campana', 'verificar que están colocados y sin acumulación excesiva de grasa.'),
        ('Pulsador manual', 'verificar que no está obstruido y que está señalizado.'),
        ('Indicadores antimanipulación y sellos', 'verificar que están intactos.'),
        ('Etiqueta de mantenimiento', 'verificar que el certificado o la etiqueta de mantenimiento está en su lugar y vigente.'),
        ('Manómetro', 'verificar que, si existe, marca la presión adecuada de operación.'),
        ('Central de comando', 'verificar que están encendidas las indicaciones de alimentación principal y de extinción conectada '
                               'y que no hay indicaciones de falla.'),
        ('Línea de detección', 'verificar que no hay objetos colgados del cable ni de los arcos portadetectores.'),
        ('Extintores clase K', 'verificar que están en su lugar, con el cartel que indica accionar primero el sistema fijo (NFPA 96, '
                               '10.2.2).'),
        ('Operación de la extracción', 'verificar con el personal de cocina que el extractor funciona siempre que se cocina y que '
                                       'no se opera con los filtros retirados (NFPA 96, 12.1.1 y 12.1.2).'),
        ('Instrucciones de accionamiento', 'verificar que las instrucciones para accionar manualmente el sistema están exhibidas '
                                           'en la cocina (NFPA 96, 12.1.4.3).'),
    ]))
    a(('p', cierre(2)))

    # ---------------- PRUEBA ----------------
    a(('h3', 'PRUEBA'))
    a(('p', 'Las pruebas consisten en verificaciones funcionales destinadas a comprobar el correcto funcionamiento de los equipos y '
            'dispositivos del sistema, y permiten detectar fallas operativas que no pueden observarse únicamente mediante '
            'inspección visual. Cuando durante las pruebas se detecten fallas o anomalías, se debe proceder inmediatamente a su '
            'reparación o mantenimiento.'))

    a(('h4', 'Prueba semestral'))
    a(('p', 'Las pruebas semestrales tienen como finalidad verificar el funcionamiento de la detección, del disparo, de los cortes '
            'de seguridad y de las alarmas sin descargar el agente extintor. Se realizan en los dos servicios semestrales del año, '
            'por personal capacitado, calificado y certificado (NFPA 96, 12.2.1). En cada servicio se deben probar todos los '
            'componentes de actuación y control, incluidos los pulsadores remotos, los dispositivos mecánicos y eléctricos, los '
            'detectores y los actuadores, según los procedimientos del fabricante, y se deben seguir el manual de instalación y '
            'mantenimiento del sistema listado y sus boletines de servicio (NFPA 96, 12.2.2 y 12.2.3).'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Funcionamiento del sistema', 'hacer funcionar el sistema, incluyendo detección, alarmas, dispositivos de disparo y otros '
                                       'equipos asociados, sin descarga del agente extintor, según el protocolo de ensayo.'),
        ('Sistema de detección', 'en los sistemas cuya actuación depende de una detección electrónica, controlar que fue probado '
                                 'según el capítulo 6 de la IRAM 3546:2011 y el procedimiento SG-PEM-IFI-SDI.'),
        ('Línea de detección', 'disparar el mecanismo con un fusible de prueba o un elemento equivalente en cada línea de '
                               'detección y verificar que actúa.'),
        ('Disparo manual', 'accionar el pulsador manual y verificar el disparo del sistema.'),
        ('Disparo por la central', 'en sistemas electrónicos, disparar el sistema desde la central con una lámpara o un módulo de '
                                   'prueba conectado en lugar del explosor y verificar su activación.'),
        ('Supervisión de fallas', 'en sistemas electrónicos, simular la falla de la línea de detección, de la línea de disparo y '
                                  'de la línea de comando de la válvula de gas y verificar la indicación de cada una.'),
        ('Corte de gas y de energía', 'verificar que, al disparar el sistema, cierra la válvula de gas y se corta la energía de los '
                                      'artefactos protegidos y de los artefactos a gas no protegidos bajo la misma campana, y que '
                                      'el restablecimiento solo es posible mediante rearme manual (NFPA 96, 10.4.1, 10.4.3 y 10.4.4).'),
        ('Extractor', 'verificar que el extractor sigue funcionando después del disparo, salvo que el diseño exija detenerlo, y que '
                      'arranca con la actuación si el extractor y los artefactos estaban detenidos (NFPA 96, 8.2.3.1 y 8.2.3.2).'),
        ('Indicaciones', 'verificar el funcionamiento de todas las indicaciones luminosas y sonoras de la central y de las alarmas.'),
        ('Fuente secundaria', 'medir la tensión de la batería, verificar la conmutación de la red a la batería y regular el '
                              'cargador a su tensión de flote, según el fabricante de la central y de la batería.'),
        ('Modo batería', 'repetir todas las pruebas anteriores con la central alimentada solo por batería.'),
        ('Vinculación con el edificio', 'donde exista, verificar la recepción de las señales de disparo y de falla en el sistema '
                                        'de alarma o de monitoreo del edificio.'),
        ('Operación simultánea', 'donde varias campanas formen un único riesgo, verificar la actuación simultánea de todos sus '
                                 'sistemas (NFPA 96, 10.3.1).'),
    ]))
    a(('p', 'En sistemas con central electrónica, las baterías y su cargador se prueban además según el procedimiento '
            'SG-PEM-IFI-SDI. La fuente secundaria debe sostener el sistema en reposo como mínimo durante **24 h** y, al cabo de '
            'ese período, hacer funcionar las alarmas durante **5 min** (NFPA 72, 10.6.7.2.1). La capacidad se verifica con el '
            'cálculo o la prueba de capacidad del procedimiento SG-PEM-IFI-SDI y se registra en la planilla SG-PEM-IFI-SCC-3.'))
    a(('p', 'La prueba de la línea de detección se realiza con un fusible de prueba, que debe reunir las siguientes características:'))
    a(('items', [
        ('Provisión', 'fusible o dispositivo de prueba provisto o indicado por el fabricante del sistema para ese modelo de línea de '
                      'detección.'),
        ('Geometría', 'mismas dimensiones y misma forma de enganche al cable que el fusible de servicio, de modo que la línea '
                      'conserve su tensión normal durante la prueba.'),
        ('Liberación', 'permite liberar la línea a mano y en forma controlada, sin calor ni llama, por corte o separación del '
                       'elemento de prueba.'),
        ('Identificación', 'marcado o de color distinto del fusible de servicio, para que no pueda quedar instalado por error.'),
        ('Ubicación', 'se coloca en la posición del fusible más alejado del mecanismo de disparo, para comprobar el recorrido completo '
                      'del cable; en sistemas con varias líneas, en cada una de ellas.'),
        ('Restitución', 'al terminar, se retira el fusible de prueba y se coloca el fusible de servicio de la temperatura nominal '
                        'indicada en el manual del sistema, y se registra en la planilla.'),
    ]))
    a(('p', 'No se deben fundir fusibles de servicio con llama, soplete ni pistola de calor dentro de la campana para probar el '
            'sistema.'))
    a(('p', 'La planilla registra por separado, para el primer y el segundo semestre, la fecha, el inspector y el resultado de cada '
            'prueba.'))
    a(('p', cierre(3)))
    a(('protocol', ('prueba de funcionamiento sin descarga', [
        ('Preparación', [
            ('Paso a paso', 'notificar según el aviso de este procedimiento, con los artefactos apagados; aislar el cilindro según el '
                            'fabricante y, en sistemas electrónicos, desconectar el explosor y conectar en su lugar la lámpara o el '
                            'módulo de prueba; identificar el cilindro y el explosor desconectados con una tarjeta.'),
            ('Justificación técnica', 'la prueba verifica toda la cadena de detección y disparo sin descargar el agente; un explosor '
                                      'conectado durante la prueba produce la descarga.'),
            ('Criterio de aceptación', 'cilindro aislado, explosor desconectado y tarjetas colocadas.')]),
        ('Disparo por la línea de detección', [
            ('Paso a paso', 'reemplazar el fusible más alejado del mecanismo por el fusible de prueba, cortar o separar el elemento '
                            'de prueba y verificar que el cable libera el mecanismo de disparo; repetir en cada línea de detección y '
                            'comprobar el recorrido del cable por las poleas de esquina sin trabas.'),
            ('Justificación técnica', 'un cable trabado en una polea o con tensión incorrecta impide el disparo aunque el fusible '
                                      'se funda.'),
            ('Criterio de aceptación', 'disparo del mecanismo en cada línea, con indicación de disparo en la central y activación de '
                                       'la lámpara o módulo de prueba.')]),
        ('Disparo manual y cortes de seguridad', [
            ('Paso a paso', 'rearmar el mecanismo, accionar el pulsador manual y verificar el disparo, el cierre de la válvula de gas, '
                            'el corte de la energía de los artefactos protegidos, las alarmas y la señal en el sistema del edificio.'),
            ('Justificación técnica', 'sin corte de la fuente de calor el aceite puede volver a encenderse después de la descarga.'),
            ('Criterio de aceptación', 'disparo, corte de gas y de energía, alarmas y señales remotas según el diseño.')]),
        ('Supervisión de fallas', [
            ('Paso a paso', 'abrir sucesivamente la línea de detección, la línea de disparo y la línea de comando de la válvula de gas '
                            'y verificar en cada caso la indicación de falla correspondiente; restituir cada línea.'),
            ('Justificación técnica', 'una falla no indicada deja el sistema fuera de servicio sin que el usuario lo advierta.'),
            ('Criterio de aceptación', 'indicación luminosa y sonora de cada falla y retorno a la condición normal al restituirla.')]),
        ('Modo batería', [
            ('Paso a paso', 'cortar la alimentación de red, verificar la conmutación a batería y la indicación de alimentación '
                            'secundaria, medir la tensión de la batería y repetir los pasos de disparo y de supervisión de fallas; '
                            'restituir la red y medir la tensión de flote del cargador.'),
            ('Justificación técnica', 'el incendio puede coincidir con un corte de energía; la batería debe sostener el disparo.'),
            ('Criterio de aceptación', 'todas las funciones operan con batería y la tensión de flote coincide con la indicada por el '
                                       'fabricante.')]),
        ('Restitución', [
            ('Paso a paso', 'reponer los fusibles de servicio y rearmar el mecanismo con el cilindro todavía aislado; reponer la '
                            'central a su condición normal y comprobar, con la lámpara o el módulo de prueba aún conectado, que no '
                            'hay indicación de disparo y que la salida de disparo está inactiva; retirar la lámpara o el módulo de '
                            'prueba y conectar el explosor siguiendo las instrucciones del fabricante; comprobar la indicación de '
                            'extinción conectada y la ausencia de fallas; recién entonces reconectar el cilindro o su actuador; '
                            'colocar sellos; rearmar el corte de gas con los comandos de los artefactos cerrados, reencender los '
                            'pilotos por personal habilitado verificando la ausencia de fugas, y retirar las tarjetas.'),
            ('Justificación técnica', 'un explosor conectado con la salida de disparo activa se acciona en el momento de la conexión '
                                      'y, con el cilindro conectado, descarga el sistema; un explosor o un cilindro sin reconectar '
                                      'deja la cocina sin protección aunque la prueba haya resultado correcta.'),
            ('Criterio de aceptación', 'central en condición normal antes de conectar el explosor, cilindro conectado en último lugar, '
                                       'sistema en servicio, extinción conectada, sin indicaciones de falla y sellos intactos.')]),
    ])))

    a(('h4', 'Prueba quinquenal'))
    a(('p', 'Las pruebas quinquenales están orientadas a verificar el desempeño de la red de descarga y la resistencia mecánica de '
            'los recipientes y conexiones sometidos a presión.'))
    a(('p', 'Cada cinco años se debe realizar:'))
    a(('items', [
        ('Prueba de descarga con agua', 'realizar la prueba de descarga del sistema usando agua en lugar de solución extintora acuosa.'),
        ('Secado de la red', 'secar el sistema de tubería con aire o nitrógeno después de la prueba de descarga.'),
        ('Prueba hidrostática', 'probar hidrostáticamente los siguientes equipos:'),
        ['recipiente de agente extintor;', 'recipiente de presión auxiliar o cartucho de gas, donde exista;', 'flexibles de unión.'],
        ('Recarga', 'una vez aprobadas las pruebas hidrostáticas, rellenar el sistema con nueva solución extintora acuosa, del tipo '
                    'indicado por el fabricante del sistema, presurizar con nitrógeno seco o reponer el cartucho de gas expelente, según el diseño, y reemplazar el explosor según el fabricante.'),
    ]))
    a(('p', 'Las pruebas hidrostáticas se deben ejecutar conforme a procedimientos documentados en función de las normas de '
            'aplicación, según los requisitos generales de la IRAM 3546:2011.'))
    a(('p', cierre(3)))
    a(('protocol', ('prueba de descarga con agua', [
        ('Preparación', [
            ('Paso a paso', 'notificar según el aviso de este procedimiento; verificar que los artefactos están apagados y a '
                            'temperatura ambiente, que el aceite fue retirado o las cubas están tapadas y que el gas y la energía '
                            'están cortados; retirar la solución extintora con los elementos de protección personal de su hoja de '
                            'datos de seguridad, disponerla según la normativa ambiental aplicable y cargar el cilindro con agua según '
                            'el fabricante.'),
            ('Justificación técnica', 'el agua sobre aceite caliente provoca su proyección violenta; el agua permite verificar la '
                                      'red sin consumir agente.'),
            ('Criterio de aceptación', 'artefactos fríos y sin aceite expuesto, gas y energía cortados y cilindro cargado con agua.')]),
        ('Descarga', [
            ('Paso a paso', 'accionar el sistema y observar la descarga por cada tobera de artefacto, de pleno y de conducto, '
                            'verificando que el agua alcanza las superficies protegidas.'),
            ('Justificación técnica', 'una tobera obstruida o desorientada deja sin protección un artefacto o el conducto.'),
            ('Criterio de aceptación', 'todas las toberas descargan sin obstrucciones y con la orientación de diseño.')]),
        ('Secado y recarga', [
            ('Paso a paso', 'secar la red con aire o nitrógeno; vaciar y secar por completo las cubas de las freidoras, los woks y '
                            'todo recipiente o superficie de los artefactos que haya recibido agua, y verificar su secado antes de '
                            'cargar aceite o encender cualquier artefacto; limpiar y colocar los capuchones de las toberas; realizar '
                            'las pruebas hidrostáticas de este apartado; recargar con nueva solución extintora; presurizar el cilindro '
                            'con nitrógeno seco o reemplazar o recargar el cartucho de gas expelente, según el diseño, y reemplazar el '
                            'explosor accionado, según el fabricante, y '
                            'restituir el sistema con la secuencia de restitución de la prueba de funcionamiento sin descarga.'),
            ('Justificación técnica', 'el agua remanente en la red diluye el agente y favorece la corrosión; el agua que queda en una '
                                      'cuba se vaporiza en forma violenta al contacto con el aceite caliente y lo proyecta sobre las '
                                      'personas.'),
            ('Criterio de aceptación', 'red seca, cubas y artefactos secos, pruebas hidrostáticas aprobadas, cilindro cargado con '
                                       'nueva solución, gas expelente y explosor repuestos y sistema en servicio.')]),
    ])))

    # ---------------- MANTENIMIENTO ----------------
    a(('h3', 'MANTENIMIENTO'))
    a(('p', 'El mantenimiento comprende las tareas destinadas a conservar los equipos y componentes del sistema en condiciones '
            'adecuadas de funcionamiento y confiabilidad. Estas tareas deben realizarse inmediatamente después de detectar fallas '
            'durante las inspecciones o pruebas.'))

    a(('h4', 'Mantenimiento semestral'))
    a(('p', 'Las tareas de mantenimiento semestral tienen como finalidad comprobar el estado de los componentes de detección, '
            'almacenamiento, disparo y descarga y eliminar la grasa que compromete su funcionamiento. Se realizan junto con la '
            'prueba semestral.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Componentes del sistema', 'comprobar que se encuentran en buen estado y que no han sido removidos, reemplazados ni '
                                    'intervenidos por terceros.'),
        ('Cilindro y soporte', 'comprobar el estado del cilindro, su identificación y su soporte y sujeción a la pared.'),
        ('Manómetro', 'comprobar que, si existe, indica que el cilindro está presurizado dentro del rango de operación.'),
        ('Gas expelente', 'en cilindros de presión contenida, comprobar la presión en el manómetro y la ausencia de pérdidas; donde '
                          'existan cartuchos o recipientes de gas expelente independientes, comprobar su estado y su carga.'),
        ('Toberas y tubería', 'comprobar que los capuchones están en su lugar y que la tubería no ha sido dañada ni modificada.'),
        ('Limpieza de toberas', 'desarmar y limpiar las toberas y reponer sus capuchones.'),
        ('Limpieza de la red de descarga', 'limpiar la cañería de extinción y verificar que no está obstruida.'),
        ('Línea de detección', 'comprobar que los portafusibles y los arcos portadetectores están libres de grasa y sin daños.'),
        ('Fusibles', 'sustituir los fusibles de aleación metálica, y los rociadores de aleación metálica usados como detectores, por '
                     'otros del modelo y la temperatura nominal indicados en el manual del sistema listado (NFPA 96, 12.2.3 y '
                     '12.2.4); marcar el año de fabricación y la fecha de instalación en la tarjeta de inspección del sistema, '
                     'firmada o con las iniciales del técnico que los instala, y destruir los fusibles retirados (NFPA 96, 12.2.5 a '
                     '12.2.5.2).'),
        ('Compuertas cortafuego', 'donde la campana tenga compuertas accionadas por fusible, inspeccionar su accionamiento según el '
                                  'fabricante y sustituir sus fusibles, con su documentación en la tarjeta (NFPA 96, 12.3.2 a 12.3.4).'),
        ('Tubería de detección', 'comprobar la tubería de detección, las poleas de esquina y el cable tensor.'),
        ('Mecanismo de disparo', 'comprobar la interfaz o el módulo mecánico y, en sistemas electrónicos, el explosor, su conexión '
                                 'y su vigencia según el fabricante.'),
        ('Central de comando', 'comprobar el estado de la central y de la batería.'),
        ('Válvula de corte de gas', 'comprobar su estado y su rearme.'),
        ('Alarmas y equipo auxiliar', 'comprobar su estado.'),
    ]))
    a(('p', 'Cuando las revisiones anteriores revelen daños en los componentes, tales como corrosión que supere los límites '
            'indicados por el fabricante, daños estructurales, daños por fuego o daños por reparaciones con soldadura u oxicorte, '
            'se debe realizar la prueba hidrostática, conforme a procedimientos documentados, o reemplazar la zona afectada.'))
    a(('p', cierre(4)))

    a(('p', 'La IRAM 3546:2011 (planilla 16D) establece la sustitución anual de los eslabones fusibles; la NFPA 96 exige reemplazar '
            'los fusibles y los rociadores de aleación metálica como mínimo cada seis meses (12.2.4), porque la grasa de campanas y '
            'conductos afecta su funcionamiento (A.12.2.4). Se adopta la frecuencia semestral, que es la más exigente; la '
            'sustitución anual de la IRAM queda cumplida con la del segundo semestre y se registra en la fila anual de la planilla.'))

    a(('h4', 'Mantenimiento anual'))
    a(('p', 'Las tareas de mantenimiento anual están orientadas a revisar los elementos de detección que no son fusibles de aleación '
            'metálica.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Detectores de bulbo y fusibles no metálicos', 'examen y limpieza o reemplazo (NFPA 96, 12.2.6).'),
        ('Otros elementos sensores de temperatura fija', 'inspección y limpieza, o reemplazo si es necesario, según el fabricante, '
                                                         'cada **12 meses** o con mayor frecuencia (NFPA 96, 12.2.7).'),
        ('Artefactos de cocción', 'verificación de la constancia de inspección y servicio anual de los artefactos, a cargo del '
                                  'usuario (NFPA 96, 12.7.1).'),
    ]))
    a(('p', cierre(4)))

    # ---------------- APTITUD UL 300 ----------------
    a(('h3', 'CRITERIOS DE APTITUD DEL SISTEMA'))
    a(('p', 'Los criterios de aptitud tienen como finalidad verificar que el sistema instalado conserva las condiciones con las que '
            'fue ensayado y las que exige la NFPA 96 para la cocina. Se verifican en el relevamiento inicial, en cada servicio '
            'semestral y después de cualquier cambio en la cocina.'))
    a(('h4', 'Criterios de la UL 300'))
    a(('p', 'La UL 300 ensaya cada sistema preingenierizado con los límites que fija su fabricante: longitudes máximas y mínimas '
            'de tubería, accesorios, cantidad de codos y tes, cantidad, tipo y ubicación de las toberas, tipos de artefactos y sus '
            'áreas máximas de protección (UL 300, 5.19). El sistema instalado solo conserva el desempeño ensayado mientras se '
            'mantenga dentro de esos límites. La superficie protegida de cada artefacto se limita a sus superficies de cocción '
            '(UL 300, 5.2).'))
    a(('p', 'Los criterios de desempeño del ensayo explican la importancia de las verificaciones de campo: el fuego se debe '
            'extinguir con la descarga completa del agente, y en freidoras, woks y anafes no debe haber reignición durante '
            '**20 min** o hasta que el aceite se enfríe **34 °C** por debajo de su temperatura de autoignición, lo que sea más '
            'largo; en los demás artefactos, durante **5 min** (UL 300, 6.1.3). Esos resultados se obtienen con la fuente de calor '
            'cortada en el momento de la descarga (UL 300, 6.2.7 y 6.4.6), por lo que el corte de gas y de energía es una '
            'condición de eficacia del sistema y no un accesorio.'))
    a(('p', 'Se deben verificar los siguientes criterios:'))
    a(('table', {'w': [22, 62, 16], 'rows': [
        ['Criterio', 'Verificación en campo', 'Referencia UL 300'],
        ['Sistema ensayado', 'El sistema y sus componentes están listados según la UL 300 y se usan dentro de su rango de '
                             'aplicación y condiciones previstas.', '1.1, 2.3 y 2.4'],
        ['Tipos de artefacto', 'Cada artefacto protegido corresponde a un tipo previsto en el manual de instalación del '
                               'fabricante; la sartén basculante se protege con los límites de cobertura de la freidora.', '6.1.1'],
        ['Área de cobertura', 'El largo y el ancho de la superficie de cocción no superan la cobertura máxima de la tobera '
                              'asignada; con varias toberas, ninguna cubre más que su cobertura individual.', '6.1.8 y 6.1.10'],
        ['Freidoras grandes', 'Una freidora de más de 0,55 m² protegida con varias toberas tiene su modelo indicado en el '
                              'manual del fabricante del sistema.', '6.1.11'],
        ['Altura y orientación de toberas', 'Cada tobera está entre la altura mínima y la máxima del manual de instalación y '
                                            'apunta al punto indicado; una tobera más baja que la mínima puede proyectar aceite '
                                            'encendido.', '6.1.7'],
        ['Red de descarga', 'Longitudes, diámetros, codos, tes y cantidad de toberas por cilindro dentro de los límites del '
                            'fabricante; ninguna ampliación ni modificación fuera de ellos.', '5.19 y 6.1.4'],
        ['Obstrucciones', 'Las tapas, estantes u otras obstrucciones fijas o móviles sobre los artefactos están previstas en el '
                          'manual del fabricante para ese modelo de artefacto.', '6.1.14'],
        ['Artefactos especiales', 'Las parrillas radiantes a gas con recipiente integrado de combustible sólido para aromatizar, '
                                  'como leña, y las freidoras con velocidad de enfriamiento mayor que la del ensayo están '
                                  'indicadas por modelo en el manual.', '6.1.13 y 6.2.2'],
        ['Freidoras de cubas múltiples', 'La actuación del sistema corta la energía de todas las cubas.', '6.2.4'],
        ['Campana y filtros', 'Filtros de grasa colocados en su posición de diseño y toberas del pleno con cobertura del área de '
                              'filtros.', '7.3.1 y 7.12'],
        ['Cilindro', 'Ubicado dentro del rango de temperatura de almacenamiento del fabricante, con la presión dentro del rango '
                     'operable; la presión de operación se refiere a 21 °C.', '5.16, 5.17 y 6.1.5'],
    ]}))
    a(('h4', 'Criterios de la NFPA 96'))
    a(('p', 'La NFPA 96 fija los siguientes requisitos de la instalación, que se deben conservar y cuyo incumplimiento se registra '
            'como no conformidad:'))
    a(('table', {'w': [22, 62, 16], 'rows': [
        ['Requisito', 'Verificación en campo', 'Referencia NFPA 96'],
        ['Sistema según la UL 300', 'Sistema automático que cumple la UL 300 u otra norma de ensayo equivalente, instalado según '
                                    'su listado. Todo sistema existente debe cumplir este requisito: un sistema de polvo o de '
                                    'agente húmedo que no lo cumple se registra como no conformidad y se debe adecuar, en '
                                    'particular cuando se cambia el aceite animal por vegetal, se cambia la posición o se '
                                    'reemplaza un artefacto, o el fabricante deja de dar soporte al equipo.',
                                    '10.2.3, 10.2.3.1 y 10.2.3.2'],
        ['Modificaciones de la campana', 'Sin cañerías ni conductos abandonados dentro de la campana, el pleno o el conducto; '
                                         'perforaciones selladas con dispositivos estancos; sin deflectores, estantes ni otros '
                                         'agregados que obstruyan la descarga de las toberas.', '10.2.7.1 a 10.2.7.3'],
        ['Cambios del riesgo', 'Todo cambio del riesgo posterior a la instalación exige reevaluar el diseño del sistema por '
                               'personal capacitado, calificado y certificado.', '10.2.7.4'],
        ['Operación simultánea', 'Las campanas instaladas una a continuación de otra, espalda con espalda o con conducto común, '
                                 'hasta 22,9 m de la más alejada y con artefactos que producen vapores con grasa bajo una o más '
                                 'de ellas, forman un único riesgo y sus sistemas actúan en forma simultánea; no se exige la '
                                 'actuación simultánea de campanas sin conducto común separadas por muros u otros medios que '
                                 'impidan la propagación de los vapores.', '10.3.1 a 10.3.1.2'],
        ['Corte de combustible y energía', 'La actuación corta en forma automática el combustible y la energía que producen calor '
                                           'en todos los artefactos protegidos y en los artefactos a gas no protegidos ubicados '
                                           'bajo la misma campana; el restablecimiento requiere rearme manual y, con '
                                           'electroválvula, un relé de rearme manual. No se exige el corte automático del vapor '
                                           'suministrado desde una fuente externa ni de los artefactos de combustible sólido, que '
                                           'se registran con NA.', '10.4.1 a 10.4.5'],
        ['Accionamiento manual', 'Accionamiento automático y manual; al menos un pulsador en una vía de egreso, con '
                                 'identificación del riesgo protegido e instrucciones de uso, y con protección donde pueda '
                                 'accionarse por accidente.', '10.5.1 a 10.5.1.3'],
        ['Señalización', 'Alarma sonora o indicación visual de la actuación; donde exista sistema de alarma de incendio, la '
                         'actuación lo activa según la NFPA 72.', '10.6.1 y 10.6.2'],
        ['Extintores portátiles', 'Extintores clase K listados para la cocina, con un cartel visible junto a cada uno que indica '
                                  'accionar el sistema fijo antes de usar el extintor; no se admiten extintores de dióxido de '
                                  'carbono.', '10.2.2, 10.9.1, 10.9.2 y 10.9.4'],
        ['Filtros de grasa', 'Filtros listados, no combustibles y rígidos, inclinados no menos de 45° respecto de la horizontal y '
                             'dispuestos de modo que todo el aire pase a través de ellos. Distancia entre el filtro y la '
                             'superficie de cocción no menor que 457 mm, y no menor que 1,22 m sobre artefactos de combustible '
                             'sólido y parrillas a la brasa a gas o eléctricas; se admiten 152 mm en artefactos sin llama '
                             'expuesta cuyos gases de combustión no pasan por los filtros, o la distancia menor que fije el '
                             'listado del filtro.', '6.2.1.1 a 6.2.1.4, 6.2.3.1 a 6.2.3.4 y 6.2.3.6'],
        ['Extractor', 'El extractor de la campana sigue funcionando después de la actuación del sistema, salvo que un componente '
                      'listado o el diseño del sistema exijan detenerlo, y arranca con la actuación si el extractor y los '
                      'artefactos estaban detenidos.', '8.2.3.1 y 8.2.3.2'],
        ['Freidoras', 'Separación de al menos 406 mm entre la freidora y las llamas de los artefactos contiguos, o una pantalla de '
                      'acero o vidrio templado de al menos 203 mm de altura.', '13.1.2.4 y 13.1.2.5'],
        ['Artefactos', 'Ningún artefacto protegido se mueve, modifica o reordena sin la reevaluación previa del instalador o del '
                       'mantenedor del sistema; si se mueve para limpieza, se devuelve a su posición de diseño con un método '
                       'aprobado y se reconectan las toberas antes de cocinar.', '13.1.2.2, 13.1.2.3 y 13.1.2.3.1'],
    ]}))
    a(('p', 'Todo artefacto nuevo, reemplazado, reubicado o modificado, todo cambio de campana, filtros o conducto y toda '
            'modificación de la red de descarga exigen repetir esta verificación antes de poner en uso el artefacto. Un artefacto '
            'fuera de cobertura, una tobera fuera de sus límites o un sistema que no cumple la UL 300 ni una norma equivalente se registra como no '
            'conformidad y se informa al responsable de la instalación para su evaluación técnica.'))
    a(('p', cierre(5)))

    # ---------------- COMPLEMENTARIAS ----------------
    a(('h3', 'AGENTE EXTINTOR Y RECARGA'))
    a(('p', 'La recarga tiene como finalidad restituir el agente con el que el sistema fue ensayado y listado.'))
    a(('p', 'En toda recarga se debe asegurar:'))
    a(('items', [
        ('Agente', 'uso exclusivo de la solución extintora indicada por el fabricante del sistema, sin mezclarla con otros agentes '
                   'ni reemplazarla por otro agente, como dióxido de carbono o polvo químico.'),
        ('Identificación', 'coincidencia entre la etiqueta reglamentaria del cilindro y la tarjeta de identificación de la recarga '
                           'en el tipo de agente, la capacidad y la fecha.'),
        ('Presurización', 'presurización con nitrógeno seco, u otro gas expelente seco indicado por el fabricante (UL 300, 5.8), hasta la '
                          'presión de operación indicada por el fabricante a **21 °C** (UL 300, 5.17), y verificación de la ausencia de '
                          'pérdidas en la válvula y el manómetro; no se debe usar aire húmedo ni otro gas no indicado, porque la '
                          'humedad favorece la corrosión del cilindro y de la válvula.'),
        ('Calidad del agente', 'verificación de la calidad de la solución extintora y de su vigencia según el fabricante, conforme a '
                               'procedimientos documentados en función de las normas de aplicación, según los requisitos generales '
                               'de la IRAM 3546:2011.'),
    ]))
    a(('p', 'Un cilindro cargado con un agente distinto del indicado deja la cocina sin protección eficaz y puede haber sufrido '
            'daños estructurales. Se debe retirar de servicio, someter a prueba hidrostática conforme a procedimientos documentados '
            'y, solo si la aprueba, recargar con el agente correcto.'))

    a(('h3', 'SISTEMAS INTERVENIDOS POR TERCEROS'))
    a(('p', 'La recepción de un sistema intervenido por terceros tiene como finalidad no asumir como operativo un sistema cuyo '
            'estado se desconoce.'))
    a(('p', 'Cuando se detecten indicios de que el sistema fue intervenido por personal ajeno al mantenedor se debe:'))
    a(('items', [
        ('Registro', 'dejar constancia de lo observado, con fotografías, y consultar al responsable de la instalación.'),
        ('Condición del sistema', 'verificar si el cilindro está conectado, si el explosor o el mecanismo de disparo está conectado '
                                  'y armado, y si la central indica extinción conectada.'),
        ('Agente', 'verificar la identificación del agente según el apartado de agente extintor y recarga.'),
        ('Explosores', 'verificar su estado, porque pueden haber sido accionados al desconectarlos.'),
        ('Comunicación', 'si el sistema no está operativo, informar por escrito y de inmediato al responsable de la instalación que '
                         'la cocina se encuentra sin protección, y aplicar la puesta fuera de servicio.'),
        ('Restitución', 'realizar un control completo del sistema, con las pruebas y el mantenimiento semestrales, antes de '
                        'declararlo operativo.'),
    ]))
    a(('p', 'El mantenedor no garantiza un sistema modificado por terceros sin su autorización escrita, hasta completar su control.'))

    a(('h3', 'PROCEDIMIENTO POSTERIOR A UNA DESCARGA O ACTUACIÓN'))
    a(('p', 'El procedimiento posterior a una descarga tiene como finalidad restablecer la protección después de una actuación real '
            'o accidental. Hasta su restablecimiento, el sistema se debe considerar fuera de servicio.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Seguridad', 'mantener cortados el gas y la energía de los artefactos hasta que se enfríen y hasta completar la restitución.'),
        ('Limpieza', 'retirar el agente descargado y el aceite saponificado de los artefactos, la campana y el piso con elementos de '
                     'protección personal; la limpieza de los artefactos para volver a cocinar corresponde al usuario.'),
        ('Recarga del agente', 'rellenar el cilindro con nueva solución extintora indicada por el fabricante.'),
        ('Presurización', 'presurizar el cilindro con nitrógeno seco a la presión de operación, o reemplazar o recargar el cartucho o el '
                          'recipiente de gas expelente, según el diseño del sistema.'),
        ('Explosor', 'reemplazar el explosor pirotécnico accionado.'),
        ('Fusibles', 'reemplazar los fusibles actuados o expuestos al fuego.'),
        ('Toberas y tubería', 'verificar que no han quedado obstruidas, limpiarlas y colocar los capuchones.'),
        ('Central', 'verificar el funcionamiento de la central y reponerla a su condición normal.'),
        ('Restitución', 'rearmar el mecanismo de disparo y el corte de gas, verificar sellos, indicadores antimanipulación y etiqueta '
                        'de mantenimiento, y realizar la prueba de funcionamiento sin descarga.'),
    ]))
    a(('p', cierre(4)))

    a(('h3', 'PUESTA FUERA DE SERVICIO'))
    a(('p', 'La puesta fuera de servicio tiene como finalidad que la cocina no opere sin protección. Los artefactos no se deben '
            'operar mientras el sistema de extinción o el de extracción estén fuera de servicio o deteriorados; en ese caso el '
            'sistema se identifica con una tarjeta de no conforme, se notifica por escrito al propietario o a su representante y, '
            'donde se requiera, a la autoridad competente (NFPA 96, 12.1.6 y 12.1.6.1).'))
    a(('p', 'Cuando el sistema quede fuera de servicio por una prueba, una falla, una descarga o una intervención se debe:'))
    a(('items', [
        ('Aviso', 'informar por escrito al responsable de la instalación y al servicio de monitoreo, indicando la causa y la duración '
                  'prevista.'),
        ('Tarjetas', 'colocar una tarjeta de fuera de servicio en la central, en el cilindro y en el pulsador manual.'),
        ('Artefactos', 'dejar constancia de que los artefactos protegidos no se deben usar mientras dure la interrupción.'),
        ('Restitución', 'al restablecer el servicio, verificar la indicación de extinción conectada, retirar las tarjetas e informar '
                        'a todas las partes notificadas.'),
    ]))

    a(('h3', 'VINCULACIÓN CON EL SISTEMA DE ALARMA DEL EDIFICIO'))
    a(('p', 'La vinculación tiene como finalidad que la actuación y las fallas del sistema de la cocina se conozcan fuera del local.'))
    a(('p', 'Donde el edificio cuente con sistema de alarma o de monitoreo se debe verificar:'))
    a(('items', [
        ('Señal de actuación', 'el funcionamiento de un sistema de extinción debe iniciar una señal de alarma mediante dispositivos '
                               'iniciadores listados, por ejemplo por la presión o por la operación mecánica del mecanismo de '
                               'descarga (NFPA 72, 17.13 y A.17.13).'),
        ('Conexión de la central', 'la unidad de control del servicio de descarga se conecta al sistema de alarma de la instalación '
                                   'protegida, y sus señales de alarma y de supervisión se anuncian en esa unidad (NFPA 72, '
                                   '23.8.5.10.1 y 23.8.5.10.2).'),
        ('Activación de la alarma', 'donde el edificio cuente con sistema de alarma de incendio, la actuación del sistema de la cocina '
                                    'lo debe activar (NFPA 96, 10.6.2).'),
        ('Prueba', 'la recepción de las señales se verifica en cada prueba semestral, en coordinación con el servicio de monitoreo.'),
    ]))

    a(('h3', 'INSPECCIÓN Y LIMPIEZA DEL SISTEMA DE EXTRACCIÓN'))
    a(('p', 'La inspección y limpieza del sistema de extracción tiene como finalidad evitar que la grasa acumulada en la campana, los '
            'filtros, el conducto y el extractor propague un incendio fuera del alcance del sistema. La realiza una empresa de '
            'limpieza contratada por el usuario, con personal capacitado, calificado y certificado; el mantenedor del sistema de '
            'extinción verifica su cumplimiento en cada servicio y coordina con ella las tareas sobre los componentes del sistema.'))
    a(('p', 'Todo el sistema de extracción se debe inspeccionar para detectar acumulación de grasa con las frecuencias de la '
            'siguiente tabla (NFPA 96, 12.4 y Tabla 12.4):'))
    a(('table', {'w': [64, 36], 'rows': [
        ['Tipo o volumen de cocción', 'Frecuencia de inspección'],
        ['Cocción con combustible sólido (leña, carbón)', 'Mensual'],
        ['Alto volumen: cocción durante 24 h, parrillas a la brasa y woks', 'Trimestral'],
        ['Volumen moderado', 'Semestral'],
        ['Bajo volumen: iglesias, campamentos diurnos, actividades estacionales y centros de jubilados', 'Anual'],
    ]}))
    a(('p', 'Durante la verificación se debe comprobar:'))
    a(('items', [
        ('Criterio de limpieza', 'cuando la inspección detecta depósitos de grasa, se limpian las partes contaminadas; la limpieza '
                                 'se dispara con un espesor medido de **2000 µm** (**3175 µm** en la carcasa del extractor), medido con '
                                 'peine calibrador, y las superficies se limpian hasta **50 µm** como máximo (NFPA 96, 12.6.1 y '
                                 '12.6.1.1.1 a 12.6.1.1.4).'),
        ('Certificado', 'existencia en el local de un certificado con el nombre de la empresa, de la persona que realizó el trabajo y '
                        'la fecha, y de un informe escrito al propietario que indique las áreas inaccesibles o no limpiadas (NFPA '
                        '96, 12.6.13 y 12.6.14).'),
        ('Etiquetas de acceso', 'etiqueta de la empresa con la fecha junto a cada panel de acceso abierto (NFPA 96, 12.6.10).'),
        ('Recipientes de grasa', 'inspección o vaciado de los recipientes metálicos de recolección de grasa como mínimo una vez por '
                                 'semana, a cargo del usuario (NFPA 96, 12.6.16).'),
        ('Artefactos', 'limpieza de la grasa acumulada debajo, detrás o en la salida de gases de las planchas, freidoras y parrillas '
                       '(NFPA 96, 12.7.2).'),
    ]))
    a(('p', 'Durante la limpieza se debe asegurar:'))
    a(('items', [
        ('Sistema de extinción', 'sus componentes no se deben dejar inoperables, salvo que lo haga personal capacitado y calificado '
                                 'del mantenedor, que lo restituye al terminar (NFPA 96, 12.6.4 y 12.6.5).'),
        ('Bloqueo eléctrico', 'bloqueo de los interruptores que puedan accionarse por accidente al comenzar (NFPA 96, 12.6.3).'),
        ('Productos', 'prohibición de usar solventes inflamables y de aplicar productos de limpieza sobre los fusibles y demás '
                      'detectores, y de recubrir el sistema con polvo u otra sustancia después de limpiarlo (NFPA 96, 12.6.6 a '
                      '12.6.8).'),
        ('Restitución', 'paneles de acceso y tapas restituidos, compuertas y difusores en posición, e interruptores y componentes '
                        'devueltos a su estado operable (NFPA 96, 12.6.9, 12.6.11 y 12.6.12).'),
    ]))

    a(('h3', 'SEGURIDAD Y SALUD OCUPACIONAL'))
    a(('p', 'La seguridad del personal tiene como finalidad evitar que las pruebas, recargas y descargas expongan a las personas a '
            'quemaduras, irritaciones, fugas de gas o descargas accidentales.'))
    a(('p', 'Durante las tareas se debe asegurar:'))
    a(('items', [
        ('Equipos de cocina', 'artefactos apagados y fríos, y suministro de gas y de energía cortado antes de toda prueba con descarga '
                              'o recarga; la solución extintora es alcalina e irritante para la piel y los ojos.'),
        ('Explosores', 'manipulación y conexión solo con el cilindro aislado y la central en condición normal, sin indicación de '
                       'disparo, siguiendo las instrucciones del fabricante.'),
        ('Elementos de protección personal', 'guantes, protección ocular y respiratoria según la hoja de datos de seguridad del '
                                             'agente, y calzado antideslizante.'),
        ('Trabajo sobre la campana', 'escalera o plataforma estable, sin apoyarse en la campana ni en los artefactos, y con la '
                                     'extracción detenida al trabajar en el pleno o el conducto.'),
        ('Delimitación del área', 'señalización de la cocina y prohibición de permanecer frente a los artefactos durante la descarga.'),
        ('Rearme del corte de gas', 'rearme con los comandos de todos los artefactos cerrados y reencendido de los pilotos por '
                                    'personal habilitado, verificando la ausencia de fugas.'),
        ('Disposición de residuos', 'recolección y disposición del agente y del aceite según la normativa ambiental aplicable.'),
    ]))

    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'La instalación de nuevos artefactos, su reemplazo, reubicación o modificación, y los cambios de campana, filtros o '
            'conducto implican instalar nuevas toberas o redistribuir las existentes. Toda modificación se debe evaluar con los '
            'criterios de aptitud de este procedimiento antes de poner en uso el artefacto, y se debe registrar en la planilla de '
            'información general.'))
    a(('p', 'La empresa mantenedora es responsable de ejecutar las tareas de inspección, prueba y mantenimiento y de emitir el '
            'certificado de operatividad de cada servicio. El usuario o propietario es responsable de:'))
    a(('items', [
        ('Limpieza', 'limpiar los filtros de la campana con la frecuencia que exija el volumen de cocción y contratar la inspección '
                     'y limpieza del sistema de extracción con las frecuencias de la NFPA 96, sin usar soluciones corrosivas sobre '
                     'fusibles, cables y toberas.'),
        ('Operación', 'hacer funcionar el extractor siempre que se cocine, no operarlo sin filtros y no cocinar con el sistema de '
                      'extinción o de extracción fuera de servicio (NFPA 96, 12.1.1, 12.1.2 y 12.1.6).'),
        ('Capuchones', 'mantener colocados los capuchones de las toberas.'),
        ('Cambios', 'no instalar, reemplazar ni mover artefactos sin la evaluación previa del mantenedor.'),
        ('Accesos', 'mantener libres el pulsador manual y la central, y no colgar objetos de la línea de detección.'),
        ('Terceros', 'no permitir la intervención del sistema por personal ajeno al mantenedor sin autorización escrita.'),
        ('Capacitación', 'instruir a cada empleado nuevo al ingresar y a todo el personal una vez por año en el uso de los '
                         'extintores portátiles y en el accionamiento manual del sistema, conservar los registros de esa '
                         'capacitación y exhibir en la cocina las instrucciones de accionamiento manual (NFPA 96, 12.1.4 a '
                         '12.1.4.3).'),
        ('Extintores', 'mantener los extintores clase K con su cartel, según la NFPA 10 (NFPA 96, 10.9.5).'),
        ('Avisos', 'informar al mantenedor toda descarga, accionamiento accidental o indicación de falla de la central.'),
    ]))
    return C


def REGISTRO_EXTRA(cierre):
    return [
        'Los datos de la instalación, del sistema, del agente, de los cilindros, de la detección, del disparo, de los cortes de '
        'seguridad, de la central y de los artefactos protegidos se registran en la planilla SG-PEM-IFI-%s-1 %s – %s, en la '
        'primera intervención y cada vez que se modifiquen.' % (SIG, NOM, PL[1]),
        'La verificación de aptitud se registra en la planilla SG-PEM-IFI-%s-5 %s – %s, en el relevamiento inicial, en cada servicio '
        'semestral y después de cada cambio en la cocina.' % (SIG, NOM, PL[5]),
        'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '
        'codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables, como el corte de gas en una '
        'cocina sin gas, se indican con NA. Toda condición O o X se debe describir en observaciones. Cada planilla debe ser firmada '
        'por el supervisor del mantenedor y por el responsable de la instalación, con su aclaración.',
        'El informe general de cada servicio semestral constituye el certificado de operatividad del sistema: indica si el sistema '
        'queda operativo o, en caso contrario, las acciones que se deben tomar y su urgencia. Donde se requiera, los certificados '
        'de inspección y mantenimiento se remiten a la autoridad competente, en papel o en formato electrónico (NFPA 96, 12.2.8 y '
        '12.2.8.1).',
    ]
