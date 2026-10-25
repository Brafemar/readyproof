# -*- coding: utf-8 -*-
SIG, NOM, NOMU, CAP = 'SHC', 'Sistema de Hidrantes Contra Incendios', 'SISTEMA DE HIDRANTES CONTRA INCENDIOS', '14'
PL = {1: 'Información general', 2: 'Inspección y pruebas de hidrantes',
      3: 'Inspección semestral (columna seca) y anual (columna con agua)'}
VIG = (' Se aplica la edición vigente de cada norma NFPA; la numeración de los artículos citados se debe confirmar en esa '
       'edición, porque puede variar entre ediciones.')


def CONTENT(cierre):
    C = []; a = C.append
    a(('h2', NOMU))
    a(('basado', '(Basado en IRAM 3546:2011 – Capítulo %s; criterios complementarios: NFPA 24, NFPA 25 y NFPA 14)' % CAP))
    a(('p', 'Este apartado establece los requisitos mínimos para la inspección, prueba y mantenimiento del sistema de hidrantes '
            'contra incendios y de la red exterior que los abastece, con el objetivo de asegurar que cada hidrante entregue el caudal '
            'previsto y que su equipamiento esté completo y disponible para el servicio de bomberos y las brigadas.'))
    a(('p', 'La IRAM 3546:2011 es la base del presente procedimiento y fija sus frecuencias. La NFPA 24, Norma para la instalación '
            'de redes de servicio privado contra incendio y sus accesorios, fija los criterios de instalación que se deben conservar, '
            'y remite el mantenimiento a la NFPA 25 (NFPA 24, 14.1), cuyo capítulo 7 se aplica como criterio complementario. La '
            'NFPA 14 se aplica a las conexiones para mangueras alimentadas desde la red. Los acoples deben cumplir la IRAM 3508 y '
            'las mangueras, la IRAM 3594. Ante diferencias, se adopta siempre la condición más exigente.' + VIG))
    a(('p', 'El equipamiento del sistema incluye:'))
    a(('items', [
        ('Red exterior', 'cañerías enterradas y a la vista, con sus anclajes y filtros principales, desde el abastecimiento hasta los '
                         'hidrantes; el abastecimiento y las bombas se rigen por los capítulos 12 y 13 de la IRAM 3546:2011.'),
        ('Válvulas interceptoras', 'válvulas de corte de la red, con sus indicadores de posición.'),
        ('Hidrantes', 'de columna seca, con la válvula por debajo del nivel de congelamiento y drenaje de la columna, o de columna con '
                      'agua; con sus bocas de salida, tapas, cadenas y tuerca de apertura.'),
        ('Armarios o casetas de mangueras', 'gabinetes que contienen mangueras, lanzas, llaves y accesorios junto a los hidrantes.'),
        ('Monitores', 'lanzas fijas de gran caudal conectadas a la red, donde existan.'),
    ]))
    a(('p', 'La NFPA 24 fija los siguientes criterios de instalación, que se deben conservar y cuyo incumplimiento se registra como '
            'observación:'))
    a(('items', [
        ('Ubicación', 'hidrantes a no menos de **12 m** de los edificios o estructuras que protegen, salvo aprobación de la autoridad '
                      'competente (7.2.3 y 7.2.4).'),
        ('Altura de las salidas', 'centro de las bocas de salida entre **450 mm** y **900 mm** sobre el nivel del terreno terminado, '
                                  'y no menos de **300 mm** sobre el piso dentro de una caseta (7.3.3).'),
        ('Hidrantes con drenaje taponado', 'marcados para indicar que se deben bombear después de su uso (7.3.2.1.1).'),
        ('Casetas de mangueras', 'identificadas, ventiladas, protegidas contra la intemperie y equipadas, además de las mangueras, '
                                 'con dos lanzas regulables de chorro y niebla con cierre por cada diámetro de manguera, una llave '
                                 'de hidrante adicional a la del hidrante, cuatro llaves de acople y dos juntas por cada diámetro, '
                                 'y reducciones o bifurcaciones con válvula cuando hay dos diámetros (8.5 y 8.6).'),
        ('Uso exclusivo', 'prohibición de usar los hidrantes y las mangueras para fines ajenos al servicio contra incendio (8.7).'),
    ]))
    a(('p', 'La inspección, prueba y mantenimiento de los hidrantes puede dejar sectores de la red fuera de servicio. Para minimizar '
            'o anular ese inconveniente se debe acordar con el responsable de la instalación el momento de la intervención y aplicar '
            'el procedimiento de puesta fuera de servicio de este manual.'))

    # ---------------- INSPECCIÓN ----------------
    a(('h3', 'INSPECCIÓN'))
    a(('p', 'La inspección consiste en un examen visual para verificar que todos los hidrantes se encuentran en buenas condiciones de '
            'funcionamiento y libres de daños físicos. Cada hidrante se debe inspeccionar además después de cada uso (NFPA 25, '
            '7.2.2.4 y 7.2.2.5).'))
    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica previa '
            'de la instalación según la IRAM 3619; esta evaluación no es obligatoria y puede ser solicitada por cualquiera de las '
            'partes interesadas.'))

    a(('h4', 'Inspección mensual'))
    a(('p', 'La inspección mensual tiene como finalidad verificar que los hidrantes y los armarios de mangueras están completos y sin '
            'pérdidas.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Armarios de mangueras', 'comprobar que no están dañados y que el equipo de su interior está completo y en buen estado: '
                                  'ubicación libre, señalización, limpieza, gabinete, puerta y vidrio.'),
        ('Hidrantes', 'comprobar que están completos y en buen estado de uso.'),
        ('Pérdidas', 'comprobar que no existen fugas.'),
        ('Drenaje', 'comprobar que no ingresa agua por los orificios de drenaje.'),
    ]))
    a(('p', 'La NFPA 25 asigna frecuencia trimestral a la inspección de las casetas de mangueras (7.2.2.8) y anual a la de los '
            'hidrantes; la frecuencia mensual de la IRAM 3546:2011 es más exigente y se mantiene.'))
    a(('p', cierre(2)))

    a(('h4', 'Inspección semestral de hidrantes de columna seca'))
    a(('p', 'La inspección semestral tiene como finalidad verificar los hidrantes de columna seca, más expuestos a fallas del drenaje '
            'y a heladas.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Accesibilidad', 'comprobar que los hidrantes están accesibles y libres de nieve, hielo u otros materiales (NFPA 25, '
                          '7.4.2.2).'),
        ('Tapas y cadenas', 'comprobar que las tapas están colocadas, ajustadas y con su cadena de soporte.'),
        ('Cuerpo', 'comprobar la ausencia de grietas y de corrosión que afecte su integridad.'),
        ('Tuerca de apertura', 'comprobar que no está desgastada y que la llave de operación está disponible.'),
        ('Agua o hielo en la columna', 'comprobar que no hay agua ni hielo en la columna, lo que indicaría un drenaje defectuoso, una '
                                       'válvula con pérdida o un nivel freático alto (NFPA 25, 7.2.2.4).'),
        ('Roscas de las salidas', 'comprobar que no están desgastadas.'),
    ]))
    a(('p', cierre(3)))

    a(('h4', 'Inspección anual de hidrantes de columna con agua'))
    a(('p', 'La inspección anual tiene como finalidad verificar los hidrantes de columna con agua y la red a la vista.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Hidrantes de columna con agua', 'comprobar los mismos aspectos que en los de columna seca, excepto el drenaje de la columna '
                                          '(NFPA 25, 7.2.2.5).'),
        ('Cañerías a la vista', 'comprobar la ausencia de pérdidas, daños físicos y corrosión, y el estado de los anclajes '
                                '(NFPA 25, 7.2.2.1.2).'),
        ('Filtros principales', 'retirarlos e inspeccionarlos para detectar obstrucciones, incrustaciones y partes dañadas o '
                                'corroídas; también se deben inspeccionar y limpiar después de cada flujo mayor que el de un orificio '
                                'de 50 mm (NFPA 25, 7.2.2.3).'),
        ('Monitores', 'comprobar semestralmente la ausencia de pérdidas, daños físicos y corrosión (NFPA 25, 7.2.2.7).'),
    ]))
    a(('p', cierre(3)))

    # ---------------- PRUEBA ----------------
    a(('h3', 'PRUEBA'))
    a(('p', 'Las pruebas tienen como propósito verificar el caudal y el abastecimiento de todos los hidrantes, la estanqueidad de sus '
            'salidas y de su cuerpo y el funcionamiento del drenaje. El mantenimiento se debe realizar inmediatamente después de las '
            'pruebas que detectan fallas.'))

    a(('h4', 'Prueba trimestral'))
    a(('p', 'La prueba trimestral tiene como finalidad verificar la compatibilidad del equipamiento, la estanqueidad y la operación '
            'de las válvulas de cada hidrante.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Armarios de mangueras', 'comprobar que no están dañados y que el equipo está completo y en buen estado.'),
        ('Compatibilidad de roscas', 'comprobar que las mangueras, lanzas y accesorios tienen roscas compatibles entre sí y con las '
                                     'del hidrante, y que los acoples cumplen la IRAM 3508.'),
        ('Roscas de las salidas', 'comprobar que no están dañadas.'),
        ('Estanqueidad', 'comprobar la estanqueidad de las salidas del hidrante y la ausencia de fugas en el cuerpo.'),
        ('Drenaje', 'comprobar el funcionamiento del drenaje.'),
        ('Válvulas', 'comprobar el accionamiento de las válvulas.'),
        ('Presión estática', 'medir y registrar la presión estática.'),
    ]))
    a(('p', cierre(2)))

    a(('h4', 'Prueba anual'))
    a(('p', 'La prueba anual tiene como finalidad verificar que cada hidrante abre totalmente, descarga sin materiales extraños y '
            'drena después de su uso.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Apertura y flujo', 'abrir totalmente cada hidrante y dejar fluir el agua como mínimo durante **1 min**, hasta que se haya '
                             'eliminado todo material extraño (NFPA 25, 7.3.2.1 y 7.3.2.2).'),
        ('Drenaje de los hidrantes de columna seca', 'después de cerrar el hidrante, comprobar el drenaje; la prueba se da por '
                                                    'finalizada cuando la columna ha drenado totalmente, lo que no debe demorar más '
                                                    'de **60 min** (NFPA 25, 7.3.2.4). Los hidrantes que no drenen adecuadamente se '
                                                    'deben reparar de inmediato.'),
        ('Empaquetaduras', 'lubricarlas.'),
        ('Caudal', 'verificar el caudal del hidrante hidráulicamente más desfavorable.'),
        ('Monitores', 'hacerlos oscilar y moverlos en todo su rango para asegurar su operación completa (NFPA 25, 7.3.3).'),
    ]))
    a(('p', 'Donde las condiciones del suelo impidan el drenaje en 60 min, o el nivel freático esté por encima del drenaje, el '
            'drenaje se debe taponar y el agua de la columna se debe extraer por bombeo después de cada uso; esos hidrantes se deben '
            'identificar claramente en zonas sujetas a heladas (NFPA 25, 7.3.2.5 y 7.3.2.6).'))
    a(('p', 'El caudal de cada hidrante se calcula con la presión medida con tubo Pitot en el centro del chorro mediante '
            '**Q = 0,0666 · c · d² · √P** (Q en L/min, d en mm, P en kPa, c coeficiente de la salida o de la boquilla), registrando '
            'además la presión residual en un hidrante próximo.'))
    a(('p', cierre(2)))
    a(('protocol', ('prueba anual de flujo y drenaje de hidrantes', [
        ('Preparación', [
            ('Paso a paso', 'notificar al responsable de la instalación y al servicio de supervisión, verificar que el agua descargada '
                            'no afecta tránsito, instalaciones ni terrenos, y colocar un manómetro en un hidrante próximo para medir '
                            'la presión estática y la residual.'),
            ('Justificación técnica', 'la presión residual en otro punto de la red indica la capacidad del abastecimiento mientras el '
                                      'hidrante fluye.'),
            ('Criterio de aceptación', 'zona de descarga segura y presión estática registrada.')]),
        ('Apertura', [
            ('Paso a paso', 'retirar la tapa de la salida, abrir el hidrante lentamente hasta su apertura total con la llave de '
                            'hidrante y dejar fluir hasta que el agua salga limpia, como mínimo **1 min**.'),
            ('Justificación técnica', 'la apertura total evita que el agua escape por el drenaje de la columna y erosione el terreno; '
                                      'el flujo elimina los sedimentos de la red.'),
            ('Criterio de aceptación', 'apertura sin esfuerzo excesivo y agua limpia.')]),
        ('Medición', [
            ('Paso a paso', 'medir con tubo Pitot la presión en el centro del chorro y registrar simultáneamente la presión residual '
                            'en el hidrante próximo; calcular el caudal.'),
            ('Qué se determina con la lectura', 'una caída de caudal o de presión residual respecto de la prueba anterior indica una '
                                                'válvula parcialmente cerrada, una obstrucción o un deterioro del abastecimiento, que '
                                                'se debe investigar.'),
            ('Criterio de aceptación', 'caudal y presión residual no menores que los de diseño ni que los de la prueba anterior.')]),
        ('Cierre y drenaje', [
            ('Paso a paso', 'cerrar el hidrante lentamente, colocar la tapa y, en los de columna seca, comprobar con la mano sobre la '
                            'salida o con un medidor que la columna drena; registrar el tiempo de drenaje.'),
            ('Justificación técnica', 'el cierre brusco produce golpe de ariete; una columna que no drena se congela y rompe el '
                                      'cuerpo del hidrante.'),
            ('Criterio de aceptación', 'drenaje total en **60 min** como máximo y sin pérdidas por las salidas.')]),
    ])))

    a(('h4', 'Prueba quinquenal de la red'))
    a(('p', 'La prueba quinquenal tiene como finalidad verificar que la red exterior conserva su capacidad de transporte de agua.'))
    a(('p', 'Durante esta prueba se debe verificar:'))
    a(('items', [
        ('Prueba de flujo de la red', 'realizar una prueba de flujo de las cañerías enterradas y a la vista como mínimo cada '
                                      '**5 años**; todo resultado que indique un deterioro del caudal o de la presión disponibles se '
                                      'debe investigar hasta asegurar que se dispone del caudal y la presión requeridos (NFPA 25, '
                                      '7.3.1 y 7.3.1.1).'),
        ('Cañería de la toma de impulsión para bomberos', 'donde la red cuente con toma de impulsión, prueba hidrostática de la '
                                                          'cañería entre la toma y su válvula de retención a **10 bar** (150 psi) '
                                                          'durante **2 h**, con una pérdida menor que **0,3 bar** (NFPA 25, 13.8.5).'),
    ]))
    a(('p', 'Donde la red abastezca sistemas que no permitan una prueba a caudal total, se admite una prueba con el máximo caudal '
            'disponible (NFPA 25, 7.3.1.2).'))
    a(('p', cierre(3)))

    # ---------------- MANTENIMIENTO ----------------
    a(('h3', 'MANTENIMIENTO'))
    a(('p', 'El mantenimiento debe asegurar que todos los componentes del sistema estén operativos y confiables. Se debe realizar el '
            'mantenimiento inmediato de cualquier componente que falle.'))

    a(('h4', 'Mantenimiento anual'))
    a(('p', 'El mantenimiento anual tiene como finalidad asegurar que los hidrantes y monitores se puedan abrir rápidamente.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Tuerca de apertura y partes móviles', 'lubricación de la tuerca de apertura, vástagos, tapas, tapones y roscas para que el '
                                                'hidrante pueda abrirse rápidamente (NFPA 25, 7.4.2.1).'),
        ('Junta de la tapa', 'verificación y reemplazo si está deteriorada.'),
        ('Monitores', 'lubricación para asegurar su operación (NFPA 25, 7.4.3).'),
        ('Protección', 'protección de los hidrantes contra daños mecánicos y mantenimiento de un acceso libre.'),
    ]))
    a(('p', cierre(2)))

    # ---------------- COMPLEMENTARIAS ----------------
    a(('h3', 'PUESTA FUERA DE SERVICIO'))
    a(('p', 'La puesta fuera de servicio tiene como finalidad limitar el riesgo y la duración de cualquier interrupción de la red de '
            'hidrantes, programada o de emergencia, según el capítulo 15 de la NFPA 25.'))
    a(('p', 'Antes de cerrar una válvula interceptora o dejar un hidrante fuera de servicio se debe asegurar:'))
    a(('items', [
        ('Coordinador', 'designación de un coordinador por el propietario o su representante.'),
        ('Alcance', 'identificación de los hidrantes y sistemas que quedan sin abastecimiento y de la duración prevista.'),
        ('Medidas compensatorias', 'cuando la protección quede fuera de servicio más de **10 h** en un período de **24 h**, guardia '
                                   'de incendio aprobada, abastecimiento de agua provisorio o un programa aprobado para eliminar '
                                   'fuentes de ignición.'),
        ('Avisos y tarjetas', 'notificación al servicio de bomberos, a la aseguradora y a la autoridad competente, y colocación de una '
                              'tarjeta en la válvula cerrada y en los hidrantes afectados.'),
    ]))
    a(('p', 'Al restablecer el servicio se debe verificar la apertura total de las válvulas, informar a todas las partes notificadas '
            'y retirar las tarjetas.'))

    a(('h3', 'SEGURIDAD Y SALUD OCUPACIONAL'))
    a(('p', 'La seguridad del personal tiene como finalidad evitar los riesgos de las descargas de gran caudal y del tránsito durante '
            'las pruebas.'))
    a(('p', 'Durante las tareas se debe asegurar:'))
    a(('items', [
        ('Descarga', 'delimitación de la zona de descarga, ausencia de personas frente a la salida y control de que el agua no '
                     'afecte el tránsito, instalaciones eléctricas ni terrenos inestables.'),
        ('Tránsito', 'señalización de la zona de trabajo cuando el hidrante está en una vía de circulación.'),
        ('Operación del hidrante', 'uso de la llave de hidrante adecuada, apertura y cierre lentos y prohibición de usar '
                                   'prolongaciones improvisadas.'),
        ('Elementos de protección personal', 'uso de calzado de seguridad, guantes, protección ocular y ropa de alta visibilidad.'),
    ]))

    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'Los cambios en la red de distribución, en el abastecimiento, en la ubicación de los hidrantes, en los sectores protegidos '
            'o en los accesos pueden alterar el desempeño del sistema. Toda modificación se debe evaluar técnicamente y registrar en '
            'la planilla de información general.'))
    a(('p', 'La empresa mantenedora es responsable de ejecutar las tareas de inspección, prueba y mantenimiento. El usuario o '
            'propietario es responsable de mantener los hidrantes accesibles, de no usarlos para fines ajenos al servicio contra '
            'incendio y de coordinar las puestas fuera de servicio.'))
    return C


def REGISTRO_EXTRA(cierre):
    return [
        'Los datos de la instalación, del riesgo protegido, del tipo y la cantidad de hidrantes, de sus bocas de salida, de las '
        'válvulas interceptoras, de los accesorios, de los armarios y de las bombas se registran en la planilla SG-PEM-IFI-%s-1 '
        '%s – %s.' % (SIG, NOM, PL[1]),
        'Los resultados de las pruebas de flujo de cada hidrante y de la red se deben conservar para compararlos con las pruebas '
        'siguientes.',
        'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '
        'codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables se indican con NA. Toda '
        'condición O o X se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y '
        'por el responsable de la instalación, con su aclaración.',
    ]
