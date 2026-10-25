"""Aplica las correcciones de la auditoría técnica a los módulos de contenido."""
import sys
D = sys.argv[1]

def edit(fn, pairs):
    p = D + '/content_%s.py' % fn
    s = open(p, encoding='utf8').read()
    for old, new in pairs:
        assert s.count(old) == 1, (fn, old[:70], s.count(old))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf8').write(s)

AUTOC_OLD = ("'inspecciones de autocontrol; el mantenedor debe verificar su correcto cumplimiento, dejando constancia de los hallazgos.'))")
AUTOC_NEW = ("'inspecciones de autocontrol, y se deben identificar como tales; el mantenedor debe verificar su correcto cumplimiento, '\n"
             "            'dejando constancia de los hallazgos.'))\n"
             "    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica '\n"
             "            'previa de la instalación según la IRAM 3619, para verificar su grado de cumplimiento con las normas y la legislación '\n"
             "            'vigente; esta evaluación no es obligatoria y puede ser solicitada por cualquiera de las partes interesadas.'))")
REG_OLD_A = ("'En cada planilla se debe indicar si cada ítem cumple, no cumple o no es apreciable, y cada planilla debe ser firmada por '\n"
             "        'el supervisor del mantenedor y por el responsable de la instalación, con su aclaración.',")
REG_OLD_SAP = ("'En cada planilla se debe indicar si cada ítem cumple o no cumple, o si no es apreciable, y cada planilla debe ser firmada '")
REG_NEW = ("'En cada planilla se debe indicar con ✓ si el ítem cumple, o con X si no cumple o no es apreciable, y cada planilla debe '\n"
           "        'ser firmada por el supervisor del mantenedor y por el responsable de la instalación, con su aclaración.',")
SEG_ANCHOR = "    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))"

def seg(items, intro):
    s = "    a(('h3', 'SEGURIDAD Y SALUD OCUPACIONAL'))\n"
    s += "    a(('p', %r))\n" % intro
    s += "    a(('p', 'Durante las pruebas con descarga y las tareas posteriores se debe asegurar:'))\n"
    s += "    a(('items', %r))\n" % items
    return s

# ------------------------------------------------------------------ SAP
SAP_SEG = seg([
    ('Coordinación previa', 'autorización escrita del responsable eléctrico y de proceso de la instalación antes de toda descarga '
                            'sobre transformadores, equipos energizados o depósitos de inflamables.'),
    ('Delimitación del área', 'señalización y delimitación de la zona de descarga y prohibición de permanecer dentro de ella durante la prueba.'),
    ('Distancias a partes energizadas', 'observación de la descarga desde fuera de la zona de descarga, respetando las distancias de '
                                        'seguridad a partes energizadas que establezca el responsable eléctrico.'),
    ('Elementos de protección personal', 'uso de los elementos de protección personal adecuados al riesgo protegido.'),
    ('Disposición del agua de prueba', 'evacuación del agua de prueba sin afectar instalaciones ni el ambiente, en particular cuando '
                                       'pueda arrastrar productos del área protegida.'),
], 'La seguridad del personal tiene como finalidad evitar que las pruebas con descarga de agua expongan a las personas a riesgos '
   'eléctricos, de proceso o de inflamables propios del elemento protegido.')
SAP_CC = """    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'Las modificaciones del elemento protegido, del entorno o del uso del área pueden afectar la orientación y la cobertura '
            'de las boquillas. Toda modificación se debe evaluar técnicamente antes de su ejecución y su existencia se debe registrar '
            'en la planilla de información general.'))
    a(('p', 'La empresa mantenedora es responsable de ejecutar las tareas de inspección, prueba y mantenimiento y de verificar las '
            'inspecciones de autocontrol. El usuario o propietario es responsable de completar las inspecciones de autocontrol, de '
            'mantener libre de obstrucciones la descarga de las boquillas y de no modificar el elemento protegido sin evaluación técnica.'))
    return C
"""
edit('SAP', [
    (AUTOC_OLD, AUTOC_NEW),
    ("    a(('h4', 'Inspección semanal'))", "    a(('h4', 'Inspección semanal (autocontrol)'))"),
    ("        ('Local de la válvula de control', 'durante el tiempo frío, comprobar que se encuentra suficientemente calefaccionado y que '",
     "        ('Válvula de control', 'inspeccionar que la válvula de control y sus componentes no tengan daños.'),\n"
     "        ('Local de la válvula de control', 'comprobar que se mantiene por encima de **5 °C** y, durante el tiempo frío, que está '\n"
     "                                           'suficientemente calefaccionado; '"),
    ("'su temperatura se mantiene por encima de **5 °C**.'),", "'se debe registrar la temperatura.'),"),
    ("        ('Reserva de agua', 'verificar el nivel de agua,", "        ('Reserva de agua', 'en la reserva sin presión o presurizada (tanque hidroneumático), verificar el nivel de agua,"),
    ("        ('Accionamientos del sistema', 'comprobar el funcionamiento de los accionamientos manuales y automáticos del sistema y de '",
     "        ('Accionamientos del sistema', 'con la válvula de control aguas arriba cerrada o con el dispositivo de prueba del fabricante, '\n"
     "                                       'según los pasos 1, 3 y 4 del protocolo de la prueba en blanco, comprobar el funcionamiento de los accionamientos manuales y automáticos del sistema y de '"),
    ("alarma restablecida y presión del sistema igual a la lectura inicial.", "alarma restablecida y presión del sistema en su valor normal."),
    ("'registrar la presión del sistema.'),", "'registrar la presión del sistema y la señal de supervisión de válvula cerrada, cuando exista.'),"),
    ("('Paso a paso', 'verificar el disparo de la válvula de diluvio y la actuación de la alarma de flujo de agua o del dispositivo '\n"
     "                            'de señalización asociado.'),",
     "('Paso a paso', 'verificar el disparo de la válvula de diluvio (apertura del mecanismo o de la clapeta, actuación del solenoide '\n"
     "                            'o del actuador) y las señales eléctricas de disparo en el panel; la alarma de flujo de agua se verifica en '\n"
     "                            'la prueba trimestral.'),"),
    ("'la válvula actúa ante la orden de la detección y se producen las señales de alarma previstas en el diseño.'",
     "'la válvula actúa ante la orden de la detección y el panel registra las señales de disparo previstas en el diseño.'"),
    ("'rearmar la válvula de diluvio según las instrucciones del fabricante, drenar el agua remanente, abrir la '",
     "'rearmar la válvula de diluvio según las instrucciones del fabricante, drenar el agua remanente, abrir lentamente la '"),
    ("('Paso a paso', 'recorrer el área protegida durante la descarga, verificar que todas las boquillas descargan y que el '",
     "('Paso a paso', 'desde fuera de la zona de descarga y respetando las distancias de seguridad a partes energizadas, con '\n"
     "                            'autorización escrita del responsable eléctrico y de proceso, verificar que todas las boquillas descargan y que el '"),
    ("        ('Cobertura de agua pulverizada', 'comprobar que la cobertura sobre el elemento protegido es adecuada.'),",
     "        ('Cobertura de agua pulverizada', 'hacer funcionar el sistema y comprobar que la cobertura sobre el elemento protegido es adecuada.'),\n"
     "        ('Modelo de descarga', 'verificar y registrar el modelo de descarga de las boquillas sobre el elemento protegido.'),"),
    ("('Maniobra de dispositivos de disparo y válvulas', 'operación de los dispositivos manuales de disparo y de las válvulas, '",
     "('Maniobra de dispositivos de disparo y válvulas', 'operación, con la válvula de control aguas arriba cerrada o con el '\n"
     "            'dispositivo de prueba del fabricante para evitar la descarga, de los dispositivos manuales de disparo y de las válvulas, '"),
    ("        ('Filtros autolimpiantes', 'rotación de su volante de accionamiento.'),",
     "        ('Filtros autolimpiantes', 'rotación de su volante de accionamiento.'),\n"
     "        ('Lubricado de válvulas de corte', 'lubricación de todos los vástagos de las válvulas con grafito o grafito en aceite liviano.'),\n"
     "        ('Limpieza de cañerías', 'limpieza de todas las cañerías y conexiones subterráneas con caudal pleno de agua, para asegurar '\n"
     "                                 'que la suciedad arrastrada por el abastecimiento no obstruye las boquillas; el agua debe fluir limpia.'),"),
    ("    a(('p', cierre(4)))\n    return C\n", "    a(('p', cierre(4)))\n" + SAP_SEG + SAP_CC),
    (REG_OLD_SAP + "\n        'por el supervisor del mantenedor y por el responsable de la instalación, con su aclaración.',", REG_NEW),
    ("'Los datos de la instalación, de las válvulas, toberas y cañerías,", "'Los datos de la instalación, de las válvulas, toberas y cañerías,"),
])

# ------------------------------------------------------------------ SRE / SGE (espuma)
def espuma_seg(alta=False):
    return seg([
        ('Elementos de protección personal', 'uso de guantes, protección ocular y ropa de trabajo según la hoja de datos de seguridad '
                                             'del espumígeno durante su manipulación, muestreo y reposición.'),
        ('Delimitación del área', 'señalización y delimitación de la zona de descarga y prohibición de permanecer dentro de ella durante '
                                  'la prueba' + (', en especial cuando la espuma reduce la visibilidad o llena el recinto.' if alta else '.')),
        ('Superficies resbaladizas', 'circulación restringida sobre superficies cubiertas de espuma hasta su limpieza.'),
        ('Disposición del efluente', 'recolección y disposición de la espuma descargada y del espumígeno drenado según la normativa '
                                     'ambiental aplicable.'),
    ], 'La seguridad del personal tiene como finalidad evitar que la manipulación del espumígeno y las descargas de espuma expongan a '
       'las personas a irritaciones, caídas o pérdida de visibilidad.')

PROTO_DOSIF = ("'verificar la concentración de la solución de espuma y observar la dirección y el patrón de descarga de '\n"
               "                            'los rociadores.'),")
edit('SRE', [
    (AUTOC_OLD, AUTOC_NEW),
    ("    a(('h4', 'Inspección semanal'))", "    a(('h4', 'Inspección semanal (autocontrol)'))"),
    ("'hidrostática a **1,5 veces** la presión de diseño.'),",
     "'hidrostática a **1,5 veces** la presión de diseño; la planilla de la norma indica 1,5 veces la presión de trabajo, por lo '\n"
     "                                           'que se debe adoptar la condición más exigente.'),"),
    ("('Bomba de espumígeno', 'si existe, hacerla funcionar durante **20 s a 30 s** y verificar que no hay pérdidas de espumígeno.'),",
     "('Bomba de espumígeno', 'si existe, hacerla funcionar durante **20 s a 30 s**, con el circuito de retorno o recirculación al '\n"
     "                                'depósito habilitado según el diseño, y verificar que no hay pérdidas de espumígeno.'),"),
    (PROTO_DOSIF,
     "'medir la concentración de la solución de espuma con refractómetro o conductímetro y curva patrón, según el '\n"
     "                            'método indicado por el fabricante del espumígeno, y observar la dirección y el patrón de descarga de '\n"
     "                            'los rociadores.'),"),
    ("    a(('p', 'Si se detectan fallas, se deben reparar y anotar en observaciones.'))\n    a(('p', cierre(6)))",
     "    a(('p', 'Si se detectan fallas, se deben reparar y anotar en observaciones.'))\n    a(('p', cierre(6)))\n"
     "    a(('protocol', ('disparo de la válvula de control sin descarga de espuma', [\n"
     "        ('Aislamiento de los circuitos', [\n"
     "            ('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo, cerrar las válvulas de abastecimiento de '\n"
     "                            'agua y de espumígeno según las instrucciones del fabricante instalador y registrar su posición.'),\n"
     "            ('Justificación técnica', 'permite verificar la actuación de la válvula de control sin consumir espumígeno ni descargar '\n"
     "                                      'espuma sobre el área protegida.'),\n"
     "            ('Criterio de aceptación', 'ambos circuitos cerrados e identificados, sin posibilidad de descarga.')]),\n"
     "        ('Disparo', [\n"
     "            ('Paso a paso', 'provocar el disparo mediante el sistema de detección automática o la actuación manual y observar la '\n"
     "                            'actuación de la válvula de control y de las alarmas asociadas.'),\n"
     "            ('Justificación técnica', 'comprueba la cadena completa de disparo, desde la detección hasta la válvula de control.'),\n"
     "            ('Criterio de aceptación', 'la válvula de control actúa ante la orden de disparo.')]),\n"
     "        ('Rearme y reapertura', [\n"
     "            ('Paso a paso', 'rearmar la válvula de control según el fabricante, drenar el agua remanente y reabrir lentamente las '\n"
     "                            'válvulas de abastecimiento de agua y de espumígeno, volviendo a precintarlas.'),\n"
     "            ('Justificación técnica', 'una válvula de abastecimiento cerrada anula la protección aunque el disparo funcione.'),\n"
     "            ('Criterio de aceptación', 'válvula rearmada, circuitos de agua y espumígeno abiertos y precintados, y sistema en servicio.')]),\n"
     "    ])))"),
    ("    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))", espuma_seg() + SEG_ANCHOR),
    (REG_OLD_A, REG_NEW),
])
edit('SGE', [
    (AUTOC_OLD, AUTOC_NEW),
    ("        ('Sistema de detección', 'en los sistemas cuya actuación depende de él, controlar que fue probado para verificar su correcto '\n"
     "                                 'funcionamiento, según el capítulo 6 de la IRAM 3546:2011.'),",
     "        ('Sistema de detección', 'probar el sistema de detección para verificar su correcto funcionamiento, según el capítulo 6 de '\n"
     "                                 'la IRAM 3546:2011, en los sistemas cuya actuación depende de él.'),"),
    ("('Bomba de espumígeno', 'hacer funcionar la bomba y verificar que no hay pérdidas de espumígeno;",
     "('Bomba de espumígeno', 'hacer funcionar la bomba, con el circuito de retorno o recirculación al depósito habilitado según el '\n"
     "                                'diseño, y verificar que no hay pérdidas de espumígeno;"),
    ("        ('Calidad de la espuma obtenida', 'verificar la calidad de la espuma producida durante la descarga.'),",
     "        ('Calidad de la espuma obtenida', 'verificar la calidad de la espuma producida durante la descarga, mediante la relación de '\n"
     "                                          'expansión y el tiempo de drenaje según el método y los valores del fabricante del espumígeno.'),"),
    ("            ('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo, coordinar con el usuario la descarga '\n"
     "                            'y verificar que el área puede recibir y evacuar la espuma descargada.'),",
     "            ('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo, coordinar con el usuario la descarga '\n"
     "                            'y verificar que el área puede recibir y evacuar la espuma descargada; en los sistemas con cámaras de '\n"
     "                            'espuma de tanques de almacenamiento de inflamables, la descarga se realiza por la conexión de prueba o '\n"
     "                            'desviando la descarga fuera del tanque, según el diseño, para no contaminar el producto almacenado.'),"),
    ("'verificar la concentración de la solución y la calidad de la espuma obtenida, y registrar las mediciones.'),",
     "'medir la concentración de la solución con refractómetro o conductímetro y curva patrón, determinar la relación '\n"
     "                            'de expansión y el tiempo de drenaje de la espuma según el método del fabricante y registrar las mediciones.'),"),
    ("'dosificación no menor que el **90 %** del valor mínimo de diseño.')]),",
     "'dosificación no menor que el **90 %** del valor mínimo de diseño y calidad de espuma dentro de los valores '\n"
     "                                       'del fabricante del espumígeno.')]),"),
    ("    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))", espuma_seg(True) + SEG_ANCHOR),
    (REG_OLD_A, REG_NEW),
])

# ------------------------------------------------------------------ SEP / SSA (cocinas)
def cocina_seg(agente, extra):
    return seg([
        ('Equipos de cocina', 'artefactos apagados y a temperatura ambiente, y suministro de gas y de energía eléctrica cortado, antes '
                              'de toda prueba con descarga o recarga.' + extra),
        ('Elementos de protección personal', 'uso de guantes, protección ocular y respiratoria según la hoja de datos de seguridad del '
                                             '%s durante su manipulación, recarga y limpieza.' % agente),
        ('Delimitación del área', 'señalización del área de cocina y prohibición de permanecer frente a los artefactos durante la descarga.'),
        ('Rearme del corte de gas', 'rearme del corte automático con los comandos de todos los artefactos cerrados, y reencendido de los '
                                    'pilotos por personal habilitado, verificando la ausencia de fugas de gas.'),
        ('Disposición de residuos', 'recolección y disposición del agente descargado o retirado según la normativa ambiental aplicable.'),
    ], 'La seguridad del personal tiene como finalidad evitar que las pruebas, recargas y descargas en equipos de cocina expongan a las '
       'personas a quemaduras, irritaciones o fugas de gas.')

AUTOC_SIMPLE_OLD = ("            'cada planta, recorriendo las zonas protegidas.'))\n\n    a(('h4', 'Inspección mensual'))")
AUTOC_SIMPLE_NEW = ("            'cada planta, recorriendo las zonas protegidas.'))\n"
                    "    a(('p', 'Las planillas de inspección cuya frecuencia sea menor a un mes pueden ser completadas por el usuario de la '\n"
                    "            'instalación y se deben identificar como inspecciones de autocontrol; el mantenedor debe verificar su correcto '\n"
                    "            'cumplimiento. En este sistema la norma no establece inspecciones de frecuencia menor a un mes.'))\n"
                    "    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica '\n"
                    "            'previa de la instalación según la IRAM 3619, para verificar su grado de cumplimiento con las normas y la legislación '\n"
                    "            'vigente; esta evaluación no es obligatoria y puede ser solicitada por cualquiera de las partes interesadas.'))\n\n"
                    "    a(('h4', 'Inspección mensual'))")
REARME = ("            ('Paso a paso', 'restituir el sistema a su estado normal desde el panel de disparo, reconectar el cilindro y verificar '\n"
          "                            'los sellos y los indicadores antimanipulación.'),")
edit('SEP', [
    (AUTOC_SIMPLE_OLD, AUTOC_SIMPLE_NEW),
    ("('Equipos de cocina', 'verificar si se ha instalado algún equipo de cocina nuevo o se ha modificado el existente, lo que '\n"
     "                              'implica la instalación de nuevas boquillas o la redistribución de las existentes.'),",
     "('Equipos de cocina', 'verificar si algún equipo de cocina ha sido añadido al existente o modificado.'),"),
    ("('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo y aislar el cilindro de agente según '",
     "('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo, con los artefactos de cocina apagados, y '\n"
     "                            'aislar el cilindro de agente según '"),
    (REARME,
     "            ('Paso a paso', 'verificar que el panel de disparo quedó rearmado, restituir el sistema a su estado normal, reconectar el '\n"
     "                            'cilindro, verificar los sellos y los indicadores antimanipulación y rearmar el corte automático con los '\n"
     "                            'comandos de los artefactos cerrados, reencendiendo los pilotos por personal habilitado.'),"),
    ("        ('Carga de polvo', 'comprobar el estado y el peso de carga del polvo.'),\n    ]))\n    a(('p', COMPLEMENTARIA))",
     "        ('Carga de polvo', 'comprobar el estado y el peso de carga del polvo.'),\n    ]))\n    a(('p', COMPLEMENTARIA))\n"
     "    a(('protocol', ('pesaje y control de la carga de polvo', [\n"
     "        ('Preparación', [\n"
     "            ('Paso a paso', 'con los artefactos de cocina apagados y fríos, notificar al responsable del sistema, aislar el disparo y '\n"
     "                            'desmontar el cilindro según las instrucciones del fabricante.'),\n"
     "            ('Justificación técnica', 'evita una descarga accidental durante la manipulación del cilindro.'),\n"
     "            ('Criterio de aceptación', 'disparo aislado y cilindro desmontado sin pérdida de agente.')]),\n"
     "        ('Pesaje', [\n"
     "            ('Paso a paso', 'pesar el cilindro con una balanza calibrada y registrar el peso en la planilla.'),\n"
     "            ('Justificación técnica', 'una pérdida de peso indica fuga de agente o de gas y reduce la capacidad de extinción.'),\n"
     "            ('Criterio de aceptación', 'peso **igual o mayor** que el mínimo anotado en la planilla SG-PEM-IFI-SEP-1.')]),\n"
     "        ('Estado del polvo', [\n"
     "            ('Paso a paso', 'en los sistemas que lo permitan, comprobar que el polvo fluye libremente y no está apelmazado ni húmedo.'),\n"
     "            ('Justificación técnica', 'un polvo apelmazado no se descarga aunque el cilindro conserve su peso.'),\n"
     "            ('Criterio de aceptación', 'polvo suelto y seco; en caso contrario, recarga del cilindro.')]),\n"
     "        ('Reinstalación', [\n"
     "            ('Paso a paso', 'reinstalar el cilindro, restituir el disparo, verificar sellos e indicadores antimanipulación y '\n"
     "                            'actualizar la etiqueta de mantenimiento.'),\n"
     "            ('Justificación técnica', 'el sistema queda fuera de servicio mientras el cilindro está desmontado.'),\n"
     "            ('Criterio de aceptación', 'sistema en servicio y etiqueta actualizada.')]),\n"
     "    ])))"),
    ("('Recarga de polvo BC o ABC', 'vaciado y nueva carga de los equipos, controlando el estado y la cantidad del polvo.'),",
     "('Recarga de polvo BC o ABC', 'vaciado y nueva carga de los equipos, controlando el estado y la cantidad del polvo; la '\n"
     "                                       'recarga se realiza con el mismo agente indicado por el fabricante, sin mezclar agentes '\n"
     "                                       'de distinto tipo.'),"),
    ("    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))",
     cocina_seg('polvo extintor', ' Luego de una descarga, el área se debe ventilar antes de retomar las tareas.') + SEG_ANCHOR),
    (REG_OLD_A, REG_NEW),
])
edit('SSA', [
    (AUTOC_SIMPLE_OLD, AUTOC_SIMPLE_NEW),
    ("            ('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo, retirar la solución extintora del '\n"
     "                            'recipiente según las instrucciones del fabricante y cargarlo con agua.'),",
     "            ('Paso a paso', 'notificar al responsable del sistema o al servicio de monitoreo; verificar que los artefactos de cocina '\n"
     "                            'están apagados y a temperatura ambiente, que el aceite fue retirado o las cubas están tapadas y que el '\n"
     "                            'gas y la energía eléctrica están cortados; retirar la solución extintora del recipiente con los elementos '\n"
     "                            'de protección personal indicados en su hoja de datos de seguridad, disponerla según la normativa ambiental '\n"
     "                            'aplicable y cargar el recipiente con agua según las instrucciones del fabricante.'),"),
    ("'el uso de agua permite verificar la red de descarga sin consumir agente ni contaminar el '\n"
     "                                      'equipo de cocina.'),",
     "'el uso de agua permite verificar la red de descarga sin consumir agente; el agua descargada sobre '\n"
     "                                      'aceite caliente provoca su proyección violenta.'),"),
    ("'recipiente cargado con agua y área protegida preparada para recibir la descarga.'",
     "'artefactos fríos y sin aceite expuesto, gas y energía cortados, recipiente cargado con agua y área preparada.'"),
    ("            ('Paso a paso', 'restituir el panel y los dispositivos de disparo a su condición normal, reconectar el recipiente y '\n"
     "                            'verificar sellos e indicadores antimanipulación.'),",
     "            ('Paso a paso', 'restituir el panel y los dispositivos de disparo a su condición normal, reconectar el recipiente, '\n"
     "                            'verificar sellos e indicadores antimanipulación y rearmar el corte automático de gas o de energía con los '\n"
     "                            'comandos de los artefactos cerrados, reencendiendo los pilotos por personal habilitado.'),"),
    ("        ('Detectores y eslabones fusibles.', ''),\n        ('Recipientes de solución extintora acuosa.', ''),\n"
     "        ('Cilindros de gas propelente.', ''),\n        ('Dispositivos de disparo.', ''),\n"
     "        ('Tuberías', 'además, verificar que no se encuentran obstruidas.'),\n        ('Boquillas.', ''),\n"
     "        ('Alarmas.', ''),\n        ('Equipo auxiliar.', ''),",
     "        ('Detectores y eslabones fusibles', 'comprobar su estado.'),\n"
     "        ('Recipientes de solución extintora acuosa', 'comprobar su estado.'),\n"
     "        ('Cilindros de gas propelente', 'comprobar su estado.'),\n"
     "        ('Dispositivos de disparo', 'comprobar su estado.'),\n"
     "        ('Tuberías', 'comprobar su estado y verificar que no se encuentran obstruidas.'),\n"
     "        ('Boquillas', 'comprobar su estado.'),\n"
     "        ('Alarmas', 'comprobar su estado.'),\n"
     "        ('Equipo auxiliar', 'comprobar su estado.'),"),
    ("    a(('p', 'Durante estas tareas se debe comprobar el estado de:'))", "    a(('p', 'Durante estas tareas se debe verificar:'))"),
    ("'se debe realizar la prueba hidrostática o reemplazar la zona afectada.'))",
     "'se debe realizar la prueba hidrostática, conforme a procedimientos documentados, o reemplazar la zona afectada.'))"),
    ("    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))",
     cocina_seg('agente extintor', ' La solución extintora acuosa es alcalina e irritante para la piel y los ojos.') + SEG_ANCHOR),
    (REG_OLD_A, REG_NEW),
])
print('correcciones aplicadas')
