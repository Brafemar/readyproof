# -*- coding: utf-8 -*-
SIG, NOM, NOMU, CAP = 'SEP', 'Sistema Fijo de Extinción por Polvo', 'SISTEMA FIJO DE EXTINCIÓN POR POLVO', '15'
PL = {1: 'Información general', 2: 'Inspección mensual', 3: 'Inspección semestral'}

AVISO = ('Antes de realizar cualquier actividad de inspección o prueba que pueda generar alarmas o descargas, '
         'se deberá notificar previamente al responsable del sistema o al servicio de monitoreo correspondiente.')
COMPLEMENTARIA = ('La IRAM 3546:2011 no asigna una planilla propia a esta tarea. Se registra en la planilla SG-PEM-IFI-%s-3 %s – %s '
                  'como tarea complementaria, conforme al requisito general que admite el agregado de tareas, pruebas o '
                  'inspecciones complementarias a las planillas de la norma.' % (SIG, NOM, PL[3]))


def CONTENT(cierre):
    C = []; a = C.append
    a(('h2', NOMU))
    a(('basado', '(Basado en IRAM 3546:2011 – Capítulo %s)' % CAP))
    a(('p', 'Este apartado establece los requisitos mínimos para la inspección, prueba y mantenimiento del sistema fijo de '
            'extinción por polvo, con el objetivo de asegurar que el sistema detecte el incendio y descargue el polvo extintor '
            'sobre las superficies y equipos protegidos, con la carga y la presión previstas en las condiciones de diseño, en '
            'condiciones de emergencia.'))
    a(('p', 'El sistema fijo de extinción por polvo protege equipos y superficies de riesgo, en particular los equipos de cocina '
            'tales como freidoras, planchas, parrillas, parrillas altas, quemadores y conductos. En la mayoría de las instalaciones el '
            'polvo se almacena en un cilindro de presión contenida, presurizado con nitrógeno seco; en otros diseños se impulsa '
            'mediante un cartucho independiente de gas propelente. El polvo se descarga a través de boquillas atomizadoras '
            'orientadas hacia las superficies protegidas.'))
    a(('p', 'El equipamiento del sistema incluye:'))
    a(('items', [
        ('Cilindro contenedor de polvo', 'recipiente que almacena el agente extintor, en general de presión contenida y presurizado '
                                         'con nitrógeno seco, o asociado a un cartucho de gas propelente.'),
        ('Agente extintor', 'polvo químico del tipo bicarbonato potásico, bicarbonato sódico, fosfato monoamónico, cloruro potásico, '
                            'urea bicarbonato potásico u otro indicado por el fabricante.'),
        ('Cartucho de gas propelente', 'cartucho independiente de nitrógeno o de dióxido de carbono, cuando el sistema lo prevé.'),
        ('Sistema de disparo', 'eslabones fusibles eutécticos, ampollas rociadoras o señales eléctricas o neumáticas, con cable de '
                               'accionamiento, poleas y panel de disparo.'),
        ('Activador manual', 'dispositivo que permite el disparo manual del sistema.'),
        ('Red de descarga', 'tuberías de descarga desde la válvula del cilindro y latiguillos de unión.'),
        ('Boquillas atomizadoras', 'dispositivos que descargan el polvo sobre las superficies protegidas, con sus tapas cuando el '
                                   'diseño las prevé.'),
        ('Equipos auxiliares, tales como', ''),
        ['manómetro del cilindro, si existe;',
         'indicadores antimanipulación y sellos;',
         'conexión al sistema de alarma;',
         'corte automático del suministro de gas o de energía eléctrica del equipo de cocina.'],
    ]))
    a(('p', 'Ante un incendio, el elemento de disparo actúa sobre el panel de disparo y libera el agente, que se descarga a través '
            'de las boquillas sobre las superficies protegidas. Cuando la instalación lo prevé, la actuación del sistema activa la '
            'alarma y corta el suministro de gas o de energía eléctrica del equipo protegido.'))
    a(('p', AVISO))

    # ---------------- INSPECCIÓN ----------------
    a(('h3', 'INSPECCIÓN'))
    a(('p', 'La inspección consiste en la verificación visual del sistema y de sus componentes, con el fin de comprobar que se '
            'encuentran en condiciones aparentemente óptimas de operación y libres de daños físicos. Se realiza generalmente en '
            'cada planta, recorriendo las zonas protegidas.'))
    a(('p', 'Las planillas de inspección cuya frecuencia sea menor a un mes pueden ser completadas por el usuario de la '
            'instalación y se deben identificar como inspecciones de autocontrol; el mantenedor debe verificar su correcto '
            'cumplimiento. En este sistema la norma no establece inspecciones de frecuencia menor a un mes.'))
    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica '
            'previa de la instalación según la IRAM 3619, para verificar su grado de cumplimiento con las normas y la legislación '
            'vigente; esta evaluación no es obligatoria y puede ser solicitada por cualquiera de las partes interesadas.'))

    a(('h4', 'Inspección mensual'))
    a(('p', 'Las inspecciones mensuales tienen como finalidad verificar que las boquillas, los elementos de disparo y los '
            'dispositivos de accionamiento se mantienen en las condiciones de diseño y que el riesgo protegido no ha sido modificado.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Tapas de las boquillas', 'si el sistema está diseñado para tenerlas, verificar que se encuentran en su lugar.'),
        ('Acumulación de grasa', 'verificar que no se acumula grasa en el eslabón fusible ni en las boquillas.'),
        ('Productos de limpieza', 'verificar que no se utilizan productos de limpieza corrosivos en los fusibles, cables o boquillas.'),
        ('Equipos de cocina', 'verificar si algún equipo de cocina ha sido añadido al existente o modificado.'),
        ('Orientación de las boquillas', 'verificar que todas las boquillas continúan dirigidas hacia las superficies que deben '
                                         'proteger, tal como se diseñaron.'),
        ('Manómetro', 'si existe, verificar que indica la presión adecuada de operación.'),
        ('Cilindro presurizado', 'si el polvo se almacena en un cilindro presurizado, verificar la presión en su manómetro.'),
        ('Activador manual', 'verificar que no se encuentra obstruido.'),
        ('Indicadores antimanipulación y sellos', 'verificar que se encuentran intactos.'),
        ('Etiqueta de mantenimiento', 'verificar que la etiqueta o el certificado de mantenimiento se encuentra en su lugar.'),
    ]))
    a(('p', cierre(2)))

    a(('h4', 'Inspección semestral'))
    a(('p', 'Las inspecciones semestrales permiten comprobar la carga del sistema, el estado del cilindro contenedor de polvo y la '
            'condición del gas propelente.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Presión del cilindro de polvo', 'registrar la presión, en kPa.'),
        ('Unión del cartucho de gas propelente', 'si el sistema tiene un cartucho independiente, verificar su unión con el cilindro '
                                                 'contenedor de polvo.'),
        ('Cartuchos de nitrógeno', 'comprobar y registrar la presión del cartucho, en kPa.'),
        ('Cartuchos de dióxido de carbono', 'observar que el testigo del disco de seguridad se encuentra en su lugar y registrar '
                                            'el peso del cartucho, en kg.'),
        ('Cilindro contenedor de polvo', 'verificar su estado.'),
        ('Apelmazado del polvo', 'en los sistemas del tipo cartucho de gas, comprobar que el polvo no se encuentra apelmazado.'),
    ]))
    a(('p', 'Las presiones y los pesos son correctos cuando son **iguales o mayores** que los valores mínimos anotados en la '
            'planilla SG-PEM-IFI-%s-1 %s – %s.' % (SIG, NOM, PL[1])))
    a(('p', cierre(3)))

    a(('h4', 'Inspección anual'))
    a(('p', 'Las inspecciones anuales tienen como finalidad verificar la integridad de la red de descarga del agente.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Tuberías de descarga', 'verificar el estado de las tuberías de descarga, desde la válvula del cilindro contenedor de '
                                 'polvo hasta las boquillas atomizadoras.'),
    ]))
    a(('p', COMPLEMENTARIA))

    # ---------------- PRUEBA ----------------
    a(('h3', 'PRUEBA'))
    a(('p', 'Las pruebas consisten en verificaciones funcionales destinadas a comprobar el correcto funcionamiento de los equipos '
            'y dispositivos del sistema, y permiten detectar fallas operativas que no pueden observarse únicamente mediante '
            'inspección visual. Cuando durante las pruebas se detecten fallas o anomalías, se debe proceder inmediatamente a su '
            'reparación o mantenimiento.'))

    a(('h4', 'Prueba semestral'))
    a(('p', 'Las pruebas semestrales tienen como finalidad verificar que el sistema responde ante la condición de incendio '
            'mediante su accionamiento automático.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Accionamiento automático', 'realizar la prueba del accionamiento automático del equipo, según el protocolo de ensayo.'),
    ]))
    a(('p', COMPLEMENTARIA))
    a(('protocol', ('prueba del accionamiento automático sin descarga', [
        ('Preparación', [
            ('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo, con los artefactos de cocina apagados, y '
                            'aislar el cilindro de agente según '
                            'las instrucciones del fabricante, de modo que el accionamiento no produzca la descarga.'),
            ('Justificación técnica', 'la prueba verifica la cadena de disparo sin consumir el agente ni contaminar el equipo de cocina.'),
            ('Criterio de aceptación', 'cilindro aislado e identificado, sin posibilidad de descarga.')]),
        ('Simulación del disparo', [
            ('Paso a paso', 'provocar el accionamiento del elemento de disparo, eslabón fusible o señal eléctrica o neumática, '
                            'mediante el método indicado por el fabricante.'),
            ('Justificación técnica', 'comprueba que el elemento sensible transmite la orden al panel de disparo a través del cable '
                                      'y de las poleas.'),
            ('Criterio de aceptación', 'el panel de disparo actúa y, cuando existen, se activan la alarma y el corte automático del '
                                       'equipo de cocina.')]),
        ('Restitución', [
            ('Paso a paso', 'verificar que el panel de disparo quedó rearmado, restituir el sistema a su estado normal, reconectar el '
                            'cilindro, verificar los sellos y los indicadores antimanipulación y rearmar el corte automático con los '
                            'comandos de los artefactos cerrados, reencendiendo los pilotos por personal habilitado.'),
            ('Justificación técnica', 'un cilindro sin reconectar deja el riesgo sin protección aunque el disparo funcione.'),
            ('Criterio de aceptación', 'sistema en servicio, cilindro conectado y sellos intactos.')]),
    ])))

    a(('h4', 'Prueba bienal'))
    a(('p', 'Las pruebas bienales permiten comprobar que el agente extintor conserva su estado y su carga de diseño.'))
    a(('p', 'Cada dos años se debe realizar:'))
    a(('items', [
        ('Carga de polvo', 'comprobar el estado y el peso de carga del polvo.'),
    ]))
    a(('p', COMPLEMENTARIA))
    a(('protocol', ('pesaje y control de la carga de polvo', [
        ('Preparación', [
            ('Paso a paso', 'con los artefactos de cocina apagados y fríos, notificar al responsable del sistema, aislar el disparo y '
                            'desmontar el cilindro según las instrucciones del fabricante.'),
            ('Justificación técnica', 'evita una descarga accidental durante la manipulación del cilindro.'),
            ('Criterio de aceptación', 'disparo aislado y cilindro desmontado sin pérdida de agente.')]),
        ('Pesaje', [
            ('Paso a paso', 'pesar el cilindro con una balanza calibrada y registrar el peso en la planilla.'),
            ('Justificación técnica', 'una pérdida de peso indica fuga de agente o de gas y reduce la capacidad de extinción.'),
            ('Criterio de aceptación', 'peso **igual o mayor** que el mínimo anotado en la planilla SG-PEM-IFI-SEP-1.')]),
        ('Estado del polvo', [
            ('Paso a paso', 'en los sistemas que lo permitan, comprobar que el polvo fluye libremente y no está apelmazado ni húmedo.'),
            ('Justificación técnica', 'un polvo apelmazado no se descarga aunque el cilindro conserve su peso.'),
            ('Criterio de aceptación', 'polvo suelto y seco; en caso contrario, recarga del cilindro.')]),
        ('Reinstalación', [
            ('Paso a paso', 'reinstalar el cilindro, restituir el disparo, verificar sellos e indicadores antimanipulación y '
                            'actualizar la etiqueta de mantenimiento.'),
            ('Justificación técnica', 'el sistema queda fuera de servicio mientras el cilindro está desmontado.'),
            ('Criterio de aceptación', 'sistema en servicio y etiqueta actualizada.')]),
    ])))

    a(('h4', 'Prueba quinquenal'))
    a(('p', 'Las pruebas quinquenales están orientadas a verificar el desempeño del sistema en una descarga y la resistencia '
            'mecánica de los recipientes y conexiones sometidos a presión.'))
    a(('p', 'Cada cinco años se debe realizar:'))
    a(('items', [
        ('Prueba de descarga', 'realizar la prueba de descarga del sistema, cuando se exija.'),
        ('Prueba hidrostática', 'probar hidrostáticamente los siguientes equipos:'),
        ['los cilindros de polvo;', 'los cilindros de gas;', 'los latiguillos de unión.'],
    ]))
    a(('p', 'La prueba hidrostática de los cilindros y de todo el equipo que estará sometido a presión de trabajo cuando el sistema '
            'se descargue debe ser realizada por una empresa habilitada, aplicando la IRAM 3517-II, y conforme a procedimientos '
            'documentados en función de las normas de aplicación, según los requisitos generales de la IRAM 3546:2011.'))
    a(('p', COMPLEMENTARIA))

    # ---------------- MANTENIMIENTO ----------------
    a(('h3', 'MANTENIMIENTO'))
    a(('p', 'El mantenimiento comprende las tareas destinadas a conservar los equipos y componentes del sistema en condiciones '
            'adecuadas de funcionamiento y confiabilidad. Estas tareas deben realizarse inmediatamente después de detectar fallas '
            'durante las inspecciones o pruebas.'))

    a(('h4', 'Mantenimiento semestral'))
    a(('p', 'Las tareas de mantenimiento semestral tienen como finalidad conservar el equipo según las condiciones establecidas por '
            'su fabricante.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Operaciones del fabricante', 'ejecución de las operaciones de mantenimiento recomendadas por el fabricante del sistema.'),
    ]))
    a(('p', cierre(3)))

    a(('h4', 'Mantenimiento anual'))
    a(('p', 'Las tareas de mantenimiento anual están orientadas a renovar los elementos sensibles del sistema de disparo.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Eslabones fusibles', 'retiro de todos los eslabones fusibles del sistema y reemplazo por eslabones nuevos del **mismo '
                               'rango de temperatura**.'),
        ('Cable de disparo', 'reinstalación del cable desde los nuevos fusibles, asegurando que quede encajado en las poleas.'),
        ('Restitución', 'restitución del sistema a su estado normal desde el panel de disparo.'),
        ('Sistemas sin fusibles', 'control de las señales eléctricas o neumáticas de disparo en los sistemas que no utilizan '
                                  'fusibles eutécticos ni ampollas rociadoras.'),
    ]))
    a(('p', cierre(3)))

    a(('h4', 'Mantenimiento bienal'))
    a(('p', 'Las tareas de mantenimiento bienal permiten renovar la carga de polvo y verificar el recorrido de la válvula de descarga.'))
    a(('p', 'Cada dos años se debe realizar:'))
    a(('items', [
        ('Recarga de polvo BC o ABC', 'vaciado y nueva carga de los equipos, controlando el estado y la cantidad del polvo; la '
                                       'recarga se realiza con el mismo agente indicado por el fabricante, sin mezclar agentes '
                                       'de distinto tipo.'),
        ('Válvula de descarga', 'recorrido de la válvula de descarga y de su señal de disparo.'),
    ]))
    a(('p', COMPLEMENTARIA))

    a(('h4', 'Mantenimiento quinquenal'))
    a(('p', 'Las tareas de mantenimiento quinquenal tienen como finalidad verificar la capacidad de extinción del agente y el '
            'funcionamiento del sistema en descarga.'))
    a(('p', 'Cada cinco años se debe realizar:'))
    a(('items', [
        ('Prueba de descarga', 'ejecución de la prueba de descarga del sistema.'),
        ('Ensayo de extinción', 'realización de un ensayo de extinción del agente.'),
    ]))
    a(('p', COMPLEMENTARIA))

    # ---------------- COMPLEMENTARIAS ----------------
    a(('h3', 'PROCEDIMIENTO POSTERIOR A UNA DESCARGA O ACTUACIÓN'))
    a(('p', 'El procedimiento posterior a una descarga tiene como finalidad restablecer la protección del equipo luego de una '
            'prueba de descarga o de una actuación real. Hasta su restablecimiento, el sistema se debe considerar fuera de servicio.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Recarga del agente', 'nueva carga del cilindro con el agente indicado por el fabricante, controlando su peso de carga.'),
        ('Presurización', 'presurización del cilindro con nitrógeno seco a la presión indicada por el fabricante, o reemplazo o '
                          'recarga del cartucho de gas propelente, según el diseño; no se debe usar aire húmedo, porque la humedad '
                          'apelmaza el polvo.'),
        ('Elementos de disparo', 'reemplazo de los eslabones fusibles actuados por eslabones del mismo rango de temperatura y '
                                 'reinstalación del cable en las poleas.'),
        ('Boquillas y tuberías', 'verificación de que las boquillas y la red de descarga no han quedado obstruidas y de que las '
                                 'tapas están colocadas.'),
        ('Restitución', 'restitución del sistema desde el panel de disparo, verificación de sellos, indicadores antimanipulación y '
                        'etiqueta de mantenimiento, y rearme del corte automático y de la alarma.'),
    ]))
    a(('p', cierre(3)))

    a(('h3', 'SEGURIDAD Y SALUD OCUPACIONAL'))
    a(('p', 'La seguridad del personal tiene como finalidad evitar que las pruebas, recargas y descargas en equipos de cocina expongan a las personas a quemaduras, irritaciones o fugas de gas.'))
    a(('p', 'Durante las pruebas con descarga y las tareas posteriores se debe asegurar:'))
    a(('items', [('Equipos de cocina', 'artefactos apagados y a temperatura ambiente, y suministro de gas y de energía eléctrica cortado, antes de toda prueba con descarga o recarga. Luego de una descarga, el área se debe ventilar antes de retomar las tareas.'), ('Elementos de protección personal', 'uso de guantes, protección ocular y respiratoria según la hoja de datos de seguridad del polvo extintor durante su manipulación, recarga y limpieza.'), ('Delimitación del área', 'señalización del área de cocina y prohibición de permanecer frente a los artefactos durante la descarga.'), ('Rearme del corte de gas', 'rearme del corte automático con los comandos de todos los artefactos cerrados, y reencendido de los pilotos por personal habilitado, verificando la ausencia de fugas de gas.'), ('Disposición de residuos', 'recolección y disposición del agente descargado o retirado según la normativa ambiental aplicable.')]))
    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'La instalación de nuevos equipos de cocina o la modificación de los existentes implica la instalación de nuevas '
            'boquillas o la redistribución de las existentes. Toda modificación se debe evaluar técnicamente antes de poner el '
            'equipo en servicio y su existencia se debe registrar en la planilla de información general.'))
    a(('p', 'La empresa mantenedora es responsable de ejecutar las tareas de inspección, prueba y mantenimiento. El usuario o '
            'propietario es responsable de no utilizar productos de limpieza corrosivos sobre fusibles, cables y boquillas, de '
            'evitar la acumulación de grasa, de mantener libre el activador manual y de no modificar los equipos de cocina sin '
            'evaluación técnica.'))
    return C


def REGISTRO_EXTRA(cierre):
    return [
        'Los datos de la instalación, del riesgo protegido, del tipo de agente extintor, de las presiones y pesos normales de los '
        'cilindros y del cartucho propelente, del equipo protegido, de la conexión al sistema de alarma y del corte automático '
        'deben registrarse en la planilla SG-PEM-IFI-%s-1 %s – %s, en la primera intervención y cada vez que se modifiquen.'
        % (SIG, NOM, PL[1]),
        'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '
        'codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables se indican con NA. Toda '
        'condición O o X se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y '
        'por el responsable de la instalación, con su aclaración.',
    ]
