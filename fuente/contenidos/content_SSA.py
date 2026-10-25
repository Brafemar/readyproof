# -*- coding: utf-8 -*-
SIG, NOM, NOMU, CAP = ('SSA', 'Sistema Fijo de Extinción por Solución Acuosa',
                       'SISTEMA FIJO DE EXTINCIÓN POR SOLUCIÓN ACUOSA', '16')
PL = {1: 'Información general', 2: 'Inspección mensual', 3: 'Prueba semestral y quinquenal', 4: 'Mantenimiento'}

AVISO = ('Antes de realizar cualquier actividad de inspección o prueba que pueda generar alarmas o descargas, '
         'se deberá notificar previamente al responsable del sistema o al servicio de monitoreo correspondiente.')


def CONTENT(cierre):
    C = []; a = C.append
    a(('h2', NOMU))
    a(('basado', '(Basado en IRAM 3546:2011 – Capítulo %s)' % CAP))
    a(('p', 'Este apartado establece los requisitos mínimos para la inspección, prueba y mantenimiento del sistema fijo de '
            'extinción por solución acuosa, con el objetivo de asegurar que el sistema detecte el incendio y descargue la solución '
            'extintora sobre las superficies y equipos protegidos, con la carga y la presión previstas en las condiciones de '
            'diseño, en condiciones de emergencia.'))
    a(('p', 'El sistema fijo de extinción por solución acuosa protege equipos y superficies de riesgo, en particular los equipos de '
            'cocina y sus conductos. La solución extintora se almacena en recipientes de agente, de alta o de baja presión, y se '
            'impulsa mediante un recipiente de presión auxiliar o cilindros de gas propelente hacia boquillas orientadas a las '
            'superficies protegidas.'))
    a(('p', 'El equipamiento del sistema incluye:'))
    a(('items', [
        ('Recipientes de solución extintora acuosa', 'cilindros que almacenan el agente, con su capacidad y presión normal a 20 °C '
                                                     'indicadas por el fabricante.'),
        ('Recipiente de presión auxiliar y cilindros de gas propelente', 'equipos que impulsan la solución hacia la red de descarga.'),
        ('Sistema de detección', 'detectores termovelocimétricos, de temperatura fija, por compensación u otros, y eslabones fusibles.'),
        ('Comandos de extinción', 'configuraciones de zona simple, dos zonas en zona cruzada o dos detectores por zona.'),
        ('Dispositivos de disparo', 'disparo manual, eléctrico, neumático o automático, y panel de control.'),
        ('Red de descarga', 'tuberías y flexibles de unión.'),
        ('Boquillas', 'dispositivos que descargan la solución sobre las superficies protegidas, con sus tapas.'),
        ('Equipos auxiliares, tales como', ''),
        ['manómetros, si existen;', 'indicadores antimanipulación y sellos;', 'alarmas;', 'equipo auxiliar asociado.'],
    ]))
    a(('p', 'Ante un incendio, el sistema de detección o el disparo manual accionan los dispositivos de disparo, que liberan la '
            'presión del recipiente auxiliar o del gas propelente y producen la descarga de la solución extintora a través de las '
            'boquillas sobre las superficies protegidas.'))
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
        ('Tapas de las boquillas', 'verificar que se encuentran en su lugar.'),
        ('Acumulación de grasa', 'verificar que no hay grasa acumulada en el eslabón fusible ni en las boquillas.'),
        ('Productos de limpieza', 'verificar que no se utiliza ningún tipo de solución corrosiva para la limpieza de fusibles, '
                                  'cables y boquillas.'),
        ('Equipos de cocina', 'verificar si se ha instalado algún equipo de cocina nuevo o se ha modificado el existente, lo que '
                              'implica la instalación de nuevas boquillas o la redistribución de las existentes.'),
        ('Orientación de las boquillas', 'verificar que las boquillas están dirigidas hacia las superficies que deben proteger, tal '
                                         'como se diseñaron.'),
        ('Activadores manuales', 'verificar que no se encuentran obstruidos.'),
        ('Indicadores antimanipulación y sellos', 'verificar que se encuentran intactos.'),
        ('Etiqueta de mantenimiento', 'verificar que el certificado o la etiqueta de mantenimiento se encuentra en su lugar.'),
        ('Manómetros', 'si existen, verificar que marcan la presión adecuada de operación.'),
    ]))
    a(('p', cierre(2)))

    # ---------------- PRUEBA ----------------
    a(('h3', 'PRUEBA'))
    a(('p', 'Las pruebas consisten en verificaciones funcionales destinadas a comprobar el correcto funcionamiento de los equipos '
            'y dispositivos del sistema, y permiten detectar fallas operativas que no pueden observarse únicamente mediante '
            'inspección visual. Cuando durante las pruebas se detecten fallas o anomalías, se debe proceder inmediatamente a su '
            'reparación o mantenimiento.'))

    a(('h4', 'Prueba semestral'))
    a(('p', 'Las pruebas semestrales tienen como finalidad verificar el funcionamiento del sistema y de sus equipos asociados sin '
            'necesidad de descargar el agente extintor.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Funcionamiento del sistema', 'hacer funcionar el sistema, incluyendo detección, alarmas, dispositivos de disparo y otros '
                                       'equipos asociados, sin descarga del agente extintor, según el protocolo de ensayo.'),
        ('Sistema de detección', 'en los sistemas cuya actuación depende de él, controlar que fue probado para verificar su correcto '
                                 'funcionamiento, según el capítulo 6 de la IRAM 3546:2011.'),
    ]))
    a(('p', 'La planilla registra por separado, para el primer y el segundo semestre, la fecha y el inspector de la prueba de los '
            'equipos asociados y de la prueba de funcionamiento.'))
    a(('p', cierre(3)))
    a(('protocol', ('prueba de funcionamiento sin descarga', [
        ('Preparación', [
            ('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo y aislar el recipiente de agente según '
                            'las instrucciones del fabricante, de modo que el accionamiento no produzca la descarga.'),
            ('Justificación técnica', 'la prueba verifica la cadena de detección y disparo sin consumir el agente ni afectar el '
                                      'equipo protegido.'),
            ('Criterio de aceptación', 'recipiente aislado e identificado, sin posibilidad de descarga.')]),
        ('Actuación de detección y disparo', [
            ('Paso a paso', 'activar la detección o el disparo manual y verificar la actuación de los dispositivos de disparo, de las '
                            'alarmas y de los equipos asociados, según la configuración de comando del sistema.'),
            ('Justificación técnica', 'comprueba que la señal de incendio llega a los dispositivos de disparo y activa las funciones '
                                      'asociadas previstas en el diseño.'),
            ('Criterio de aceptación', 'actuación de todos los dispositivos de disparo, alarmas y equipos asociados según el diseño.')]),
        ('Restitución', [
            ('Paso a paso', 'restituir el panel y los dispositivos de disparo a su condición normal, reconectar el recipiente, '
                            'verificar sellos e indicadores antimanipulación y rearmar el corte automático de gas o de energía con los '
                            'comandos de los artefactos cerrados, reencendiendo los pilotos por personal habilitado.'),
            ('Justificación técnica', 'un recipiente sin reconectar deja el riesgo sin protección aunque el disparo funcione.'),
            ('Criterio de aceptación', 'sistema en servicio, recipiente conectado y sellos intactos.')]),
    ])))

    a(('h4', 'Prueba quinquenal'))
    a(('p', 'Las pruebas quinquenales están orientadas a verificar el desempeño de la red de descarga y la resistencia mecánica de '
            'los recipientes y conexiones sometidos a presión.'))
    a(('p', 'Cada cinco años se debe realizar:'))
    a(('items', [
        ('Prueba de descarga con agua', 'realizar la prueba de descarga del sistema usando agua en lugar de solución extintora acuosa.'),
        ('Secado de la red', 'secar el sistema de tubería con aire o nitrógeno después de la prueba de descarga.'),
        ('Recarga', 'rellenar el sistema con nueva solución extintora acuosa.'),
        ('Prueba hidrostática', 'probar hidrostáticamente los siguientes equipos:'),
        ['recipiente de agente extintor;', 'recipiente de presión auxiliar;', 'flexibles de unión.'],
    ]))
    a(('p', 'Las pruebas hidrostáticas se deben ejecutar conforme a procedimientos documentados en función de las normas de '
            'aplicación, según los requisitos generales de la IRAM 3546:2011.'))
    a(('p', cierre(3)))
    a(('protocol', ('prueba de descarga con agua', [
        ('Preparación', [
            ('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo; verificar que los artefactos de cocina '
                            'están apagados y a temperatura ambiente, que el aceite fue retirado o las cubas están tapadas y que el '
                            'gas y la energía eléctrica están cortados; retirar la solución extintora del recipiente con los elementos '
                            'de protección personal indicados en su hoja de datos de seguridad, disponerla según la normativa ambiental '
                            'aplicable y cargar el recipiente con agua según las instrucciones del fabricante.'),
            ('Justificación técnica', 'el uso de agua permite verificar la red de descarga sin consumir agente; el agua descargada sobre '
                                      'aceite caliente provoca su proyección violenta.'),
            ('Criterio de aceptación', 'artefactos fríos y sin aceite expuesto, gas y energía cortados, recipiente cargado con agua y área preparada.')]),
        ('Descarga', [
            ('Paso a paso', 'accionar el sistema y observar la descarga por cada boquilla, verificando que el agua alcanza las '
                            'superficies protegidas.'),
            ('Justificación técnica', 'una boquilla obstruida o desorientada deja sin protección una superficie del equipo de cocina.'),
            ('Criterio de aceptación', 'todas las boquillas descargan sin obstrucciones y con la orientación de diseño.')]),
        ('Secado y recarga', [
            ('Paso a paso', 'secar el sistema de tubería con aire o nitrógeno, rellenar con nueva solución extintora acuosa y '
                            'restituir el sistema.'),
            ('Justificación técnica', 'el agua remanente en la red diluye el agente y favorece la corrosión.'),
            ('Criterio de aceptación', 'red seca, recipiente cargado con nueva solución y sistema en servicio.')]),
    ])))

    # ---------------- MANTENIMIENTO ----------------
    a(('h3', 'MANTENIMIENTO'))
    a(('p', 'El mantenimiento comprende las tareas destinadas a conservar los equipos y componentes del sistema en condiciones '
            'adecuadas de funcionamiento y confiabilidad. Estas tareas deben realizarse inmediatamente después de detectar fallas '
            'durante las inspecciones o pruebas.'))

    a(('h4', 'Mantenimiento semestral'))
    a(('p', 'Las tareas de mantenimiento semestral tienen como finalidad comprobar el estado de los componentes de detección, '
            'almacenamiento, disparo y descarga del sistema.'))
    a(('p', 'Durante estas tareas se debe verificar:'))
    a(('items', [
        ('Detectores y eslabones fusibles', 'comprobar su estado.'),
        ('Recipientes de solución extintora acuosa', 'comprobar su estado.'),
        ('Cilindros de gas propelente', 'comprobar su estado.'),
        ('Dispositivos de disparo', 'comprobar su estado.'),
        ('Tuberías', 'comprobar su estado y verificar que no se encuentran obstruidas.'),
        ('Boquillas', 'comprobar su estado.'),
        ('Alarmas', 'comprobar su estado.'),
        ('Equipo auxiliar', 'comprobar su estado.'),
    ]))
    a(('p', 'Cuando las revisiones anteriores revelen daños en los componentes, tales como corrosión que supere los límites '
            'indicados por el fabricante, daños estructurales, daños por fuego o daños por reparaciones con soldadura u oxicorte, '
            'se debe realizar la prueba hidrostática, conforme a procedimientos documentados, o reemplazar la zona afectada.'))
    a(('p', cierre(4)))

    a(('h4', 'Mantenimiento anual'))
    a(('p', 'Las tareas de mantenimiento anual están orientadas a renovar los elementos sensibles del sistema de disparo.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Eslabones fusibles', 'sustitución de los eslabones fusibles.'),
    ]))
    a(('p', cierre(4)))

    # ---------------- COMPLEMENTARIAS ----------------
    a(('h3', 'PROCEDIMIENTO POSTERIOR A UNA DESCARGA O ACTUACIÓN'))
    a(('p', 'El procedimiento posterior a una descarga tiene como finalidad restablecer la protección del equipo luego de una '
            'actuación real. Hasta su restablecimiento, el sistema se debe considerar fuera de servicio.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Recarga del agente', 'rellenado del recipiente con nueva solución extintora acuosa indicada por el fabricante.'),
        ('Gas propelente', 'reemplazo o recarga del recipiente de presión auxiliar o de los cilindros de gas propelente.'),
        ('Eslabones fusibles', 'reemplazo de los eslabones fusibles actuados.'),
        ('Boquillas y tuberías', 'verificación de que no han quedado obstruidas y de que las tapas están colocadas.'),
        ('Restitución', 'restitución de los dispositivos de disparo y verificación de sellos, indicadores antimanipulación y etiqueta '
                        'de mantenimiento.'),
    ]))
    a(('p', cierre(4)))

    a(('h3', 'SEGURIDAD Y SALUD OCUPACIONAL'))
    a(('p', 'La seguridad del personal tiene como finalidad evitar que las pruebas, recargas y descargas en equipos de cocina expongan a las personas a quemaduras, irritaciones o fugas de gas.'))
    a(('p', 'Durante las pruebas con descarga y las tareas posteriores se debe asegurar:'))
    a(('items', [('Equipos de cocina', 'artefactos apagados y a temperatura ambiente, y suministro de gas y de energía eléctrica cortado, antes de toda prueba con descarga o recarga. La solución extintora acuosa es alcalina e irritante para la piel y los ojos.'), ('Elementos de protección personal', 'uso de guantes, protección ocular y respiratoria según la hoja de datos de seguridad del agente extintor durante su manipulación, recarga y limpieza.'), ('Delimitación del área', 'señalización del área de cocina y prohibición de permanecer frente a los artefactos durante la descarga.'), ('Rearme del corte de gas', 'rearme del corte automático con los comandos de todos los artefactos cerrados, y reencendido de los pilotos por personal habilitado, verificando la ausencia de fugas de gas.'), ('Disposición de residuos', 'recolección y disposición del agente descargado o retirado según la normativa ambiental aplicable.')]))
    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'La instalación de nuevos equipos de cocina o la modificación de los existentes implica la instalación de nuevas '
            'boquillas o la redistribución de las existentes. Toda modificación se debe evaluar técnicamente antes de poner el '
            'equipo en servicio y su existencia se debe registrar en la planilla de información general.'))
    a(('p', 'La empresa mantenedora es responsable de ejecutar las tareas de inspección, prueba y mantenimiento. El usuario o '
            'propietario es responsable de no utilizar soluciones corrosivas para la limpieza de fusibles, cables y boquillas, de '
            'evitar la acumulación de grasa, de mantener libres los activadores manuales y de no modificar los equipos de cocina '
            'sin evaluación técnica.'))
    return C


def REGISTRO_EXTRA(cierre):
    return [
        'Los datos de la instalación, de las marcas del sistema, de los detectores y del panel de control, de la fecha de '
        'instalación, del tipo de sistema, de la cantidad y capacidad de los cilindros, de la presión normal a 20 °C, del fusible, '
        'del tipo de disparo, del sistema de detección y de los comandos de extinción deben registrarse en la planilla '
        'SG-PEM-IFI-%s-1 %s – %s, en la primera intervención y cada vez que se modifiquen.' % (SIG, NOM, PL[1]),
        'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '
        'codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables se indican con NA. Toda '
        'condición O o X se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y '
        'por el responsable de la instalación, con su aclaración.',
    ]
