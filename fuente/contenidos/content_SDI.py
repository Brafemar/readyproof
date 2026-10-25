# -*- coding: utf-8 -*-
SIG, NOM, NOMU, CAP = 'SDI', 'Sistema de Detección de Incendios', 'SISTEMA DE DETECCIÓN DE INCENDIOS CONVENCIONAL DE DOS HILOS', '6'
PL = {1: 'Información general', 2: 'Prueba mensual', 3: 'Prueba trimestral, semestral y anual', 4: 'Mantenimiento anual',
      5: 'Información semanal (autocontrol)'}
N72 = 'NFPA 72'
VIG = ' Se aplica la edición vigente de cada norma NFPA; la numeración de los artículos citados se debe confirmar en esa edición, porque puede variar entre ediciones.'
INFORME = 'SG-PEM-IFI-SDI-2-IN'
RETENCION = True
N101 = 'NFPA 101, Código de Seguridad Humana'
AVISO = ('Antes de realizar cualquier actividad de inspección o prueba que pueda generar alarmas o descargas, se deberá '
         'notificar previamente al responsable del sistema o al servicio de monitoreo correspondiente. Además, antes de cualquier prueba se debe notificar a todas las personas e instalaciones que reciben señales de '
         'alarma, de supervisión o de falla, incluido el servicio de monitoreo, y a los ocupantes del edificio, para evitar una '
         'respuesta innecesaria. Al finalizar la prueba se debe notificar su conclusión. La prueba se debe coordinar con el '
         'responsable de la instalación para no interrumpir sistemas o equipos críticos del edificio.')
COMPL = ('La IRAM 3546:2011 no asigna planilla a esta tarea, que proviene de la %s. Se registra en la planilla SG-PEM-IFI-SDI-%d '
         '%s – %s como tarea complementaria, conforme al requisito general que admite el agregado de tareas a las planillas.')


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


def compl(n): return COMPL % (N72, n, NOM, PL[n])


def CONTENT(cierre):
    C = []; a = C.append
    a(('h2', NOMU))
    a(('basado', '(Basado en IRAM 3546:2011 – Capítulo %s; criterios complementarios: %s y NFPA 101)' % (CAP, N72)))
    a(('p', 'Este apartado establece los requisitos mínimos para la inspección, prueba y mantenimiento del sistema de detección de '
            'incendios convencional de dos hilos, con el objetivo de asegurar que el sistema detecte el incendio en su etapa '
            'inicial, transmita las señales de alarma, supervisión y falla y active los aparatos de notificación y las funciones '
            'de control previstas, en condiciones de emergencia.'))
    a(('p', 'La IRAM 3546:2011 es la base del presente procedimiento y fija sus frecuencias. La %s se aplica como criterio '
            'complementario para los métodos de prueba, los valores de aceptación y las tareas que la IRAM 3546 no prevé; ante '
            'diferencias de frecuencia o de exigencia, se adopta siempre la condición más exigente.%s' % (N72, VIG)))
    a(('p', 'El equipamiento del sistema incluye:'))
    a(('items', [
        ('Unidad de control de alarma de incendio', 'central o panel que recibe las señales de los dispositivos iniciadores, '
                                                    'supervisa los circuitos y comanda los aparatos de notificación y las '
                                                    'funciones de control.'),
        ('Fuentes de energía', 'alimentación primaria de red y alimentación secundaria por baterías, con su cargador.'),
        ('Dispositivos iniciadores', 'detectores de humo, de temperatura, de llama y de gas, avisadores manuales, sensores de '
                                     'flujo de agua y dispositivos de supervisión.'),
        ('Aparatos de notificación', 'sirenas, alarmas acústicas, luces estroboscópicas y altavoces del sistema de audio para '
                                     'evacuación.'),
        ('Circuitos y canalizaciones', 'cableado de zonas y de notificación, tuberías y conductos.'),
        ('Equipos auxiliares, tales como', ''),
        ['anunciadores remotos y sus comandos;', 'discador telefónico o transmisor hacia el servicio de monitoreo;',
         'módulos de control y de verificación;', 'equipos en interfaz con otros sistemas.'],
    ]))
    a(('p', 'Ante la actuación de un dispositivo iniciador, la central identifica la zona en alarma, activa los aparatos de '
            'notificación, transmite la señal al servicio de monitoreo cuando existe y ejecuta las funciones de control asociadas, '
            'tales como el accionamiento de otros sistemas de protección.'))
    a(('p', AVISO))

    # ---------------- INSPECCIÓN ----------------
    a(('h3', 'INSPECCIÓN'))
    a(('p', 'La inspección consiste en la verificación visual del sistema y de sus componentes, para comprobar que se encuentran en '
            'condiciones aparentemente óptimas de operación y libres de daños físicos. Se realiza generalmente en cada planta, '
            'recorriendo las zonas protegidas.'))
    a(('p', 'Las inspecciones de frecuencia menor a un mes pueden ser completadas por el usuario de la instalación como '
            'inspecciones de autocontrol, y se deben identificar como tales; el mantenedor debe verificar su correcto '
            'cumplimiento, dejando constancia de los hallazgos.'))
    a(('p', 'Antes de comenzar por primera vez con las tareas de mantenimiento se recomienda realizar una evaluación técnica previa '
            'de la instalación según la IRAM 3619; esta evaluación no es obligatoria y puede ser solicitada por cualquiera de las '
            'partes interesadas.'))
    a(('p', 'Los dispositivos inaccesibles por razones de seguridad, tales como procesos continuos, equipos energizados o altura '
            'excesiva, pueden inspeccionarse durante las paradas programadas, con intervalos que no excedan los **18 meses**, si lo '
            'aprueba la autoridad competente (NFPA 72, 14.3.2 y 14.4.4.1).'))

    a(('h4', 'Verificación documental'))
    a(('p', 'La verificación documental tiene como finalidad asegurar que se dispone de la información necesaria para operar y '
            'mantener el sistema.'))
    a(('p', 'Antes de las inspecciones operativas se debe verificar:'))
    a(('items', [
        ('Planos de la instalación', 'ratificar la existencia de los planos actualizados del sistema, conforme a obra.'),
        ('Manual del panel de control', 'corroborar que exista el manual instructivo, en idioma español, del funcionamiento del '
                                        'panel de control.'),
        ('Registro de eventos', 'verificar las planillas de registro de eventos ocurridos durante el mes e identificar fallas '
                                'repetitivas.'),
        ('Secuencia de operación', 'verificar que exista la secuencia de operación por escrito y, en sistemas programables, la '
                                   'versión vigente del software del sitio.'),
    ]))
    a(('p', cierre(1)))

    a(('h4', 'Inspección semanal (autocontrol)'))
    a(('p', 'Las inspecciones semanales tienen como finalidad verificar el estado general de los dispositivos de detección, aviso y '
            'control y de las canalizaciones de la instalación.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Dispositivos de iniciación de alarma', 'verificar el estado de los detectores de humo, de temperatura, de gas y de llama, de '
                                              'las barreras infrarrojas y de los sistemas aspiradores.'),
        ('Pulsadores manuales de alarma', 'verificar su estado y que se encuentren accesibles, sin obstrucciones y visibles, según la '
                                         'NFPA 101, 9.6.2.7.'),
        ('Dispositivos de aviso de incendio', 'verificar el estado de las alarmas acústicas, sirenas y señalización visual, '
                                              'tales como luces estroboscópicas.'),
        ('Panel de alarma', 'verificar su estado, sus indicadores lumínicos (LED) o visor de información, la condición normal del '
                            'sistema, los fusibles, los equipos interconectados, la alimentación primaria y la ausencia de '
                            'señales de falla.'),
        ('Condición de los detectores', 'asegurarse de que no se encuentran obstruidos, no poseen materiales extraños, por ejemplo '
                                        'pintura, y están libres de daños físicos.'),
        ('Canalizaciones', 'asegurarse de que las tuberías se encuentran en buenas condiciones, libres de daños físicos, sin '
                           'corrosión, alineadas y no sujetas a cargas externas.'),
        ('Eventos repetidos', 'verificar los eventos repetidos del mes registrados en el panel.'),
        ('Fuentes de energía', 'verificar que el sistema se halla alimentado con tensión primaria y secundaria.'),
        ('Cableado', 'registrar las zonas con falla y las zonas conectadas.'),
        ('Señales de otros sistemas', 'verificar la indicación de nivel del tanque de agua, de los detectores de flujo, de baja '
                                      'presión en la red de cañerías y de arranque de bomba.'),
        ('Componentes', 'verificar que todos los componentes se encuentran incrustados y ensamblados en alineación.'),
        ('Registro de eventos', 'verificar las planillas de eventos ocurridos durante la semana.'),
    ]))
    a(('p', 'Las tuberías en espacios ocultos, como sobre falsos techos, no requieren inspección.'))
    a(('p', cierre(5)))

    a(('h4', 'Inspección mensual'))
    a(('p', 'Las inspecciones mensuales permiten comprobar el estado de las baterías de la fuente secundaria.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Baterías', 'verificar la ausencia de corrosión o fugas, la condición de las conexiones y la marca de mes y año de '
                     'fabricación.'),
        ('Baterías de plomo-ácido', 'inspeccionar visualmente el nivel de electrolito.'),
        ('Baterías primarias (pila seca)', 'verificar su estado y fecha.'),
    ]))
    a(('p', compl(2)))

    a(('h4', 'Inspección trimestral'))
    a(('p', 'Las inspecciones trimestrales tienen como finalidad verificar los dispositivos que requieren un control más frecuente '
            'según la NFPA 72, Tabla 14.3.1.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Detectores de energía radiante (llama)', 'verificar que ningún punto que requiera detección esté obstruido o fuera del '
                                                   'campo visual del detector.'),
        ('Dispositivos de señales de supervisión', 'verificar su ubicación y condición.'),
        ('Sensores de flujo de agua', 'verificar su ubicación y condición.'),
    ]))
    a(('p', compl(3)))

    a(('h4', 'Inspección semestral'))
    a(('p', 'Las inspecciones semestrales tienen como finalidad verificar la ubicación y la condición de los dispositivos y equipos '
            'del sistema.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Baterías de níquel-cadmio y de plomo-ácido selladas', 'verificar corrosión, fugas, conexiones y fecha de fabricación.'),
        ('Dispositivos iniciadores', 'verificar la ubicación y condición de detectores de humo, de calor, avisadores manuales y '
                                     'detectores de ducto; en detectores de haz proyectado, que la trayectoria no esté obstruida; '
                                     'en sistemas de muestreo de aire, que los filtros en línea estén limpios.'),
        ('Aparatos de notificación', 'verificar la ubicación y condición de los aparatos audibles y visibles.'),
        ('Anunciadores remotos y supresores de transientes', 'verificar su ubicación y condición.'),
        ('Equipos de comunicación de emergencia por voz', 'verificar su ubicación y condición.'),
        ('Dispositivos electromecánicos de descarga e interruptores de sistemas de extinción', 'verificar su ubicación y condición.'),
        ('Interfaz de funciones de control de emergencia', 'verificar su ubicación y condición.'),
        ('Aparatos de notificación audible textual', 'verificar su ubicación y condición.'),
    ]))
    a(('p', compl(3)))

    a(('h4', 'Inspección anual'))
    a(('p', 'Las inspecciones anuales permiten detectar cambios en el edificio o en su uso que afecten el desempeño del sistema.'))
    a(('p', 'Durante esta inspección se debe verificar:'))
    a(('items', [
        ('Todos los equipos', 'verificar que no existan modificaciones del edificio, cambios de ocupación o de condiciones '
                              'ambientales, cambios en la ubicación u orientación de los dispositivos, obstrucciones físicas, '
                              'daños o falta de limpieza que afecten el desempeño.'),
        ('Fuentes de energía remotas y extensiones de circuitos de notificación', 'verificar los valores nominales de los '
                                                                                  'fusibles y que los indicadores señalen el '
                                                                                  'estado operativo normal.'),
        ('Transmisores al servicio de monitoreo', 'verificar la ubicación, la condición física y la condición normal de los '
                                                  'comunicadores.'),
        ('Conexiones de fibra óptica', 'verificar su ubicación y condición.'),
        ('Tubo de muestreo de detectores en ducto', 'verificar su orientación y que se extienda dentro del conducto según el diseño.'),
    ]))
    a(('p', compl(3)))

    # ---------------- PRUEBA ----------------
    a(('h3', 'PRUEBA'))
    a(('p', 'Las pruebas consisten en verificaciones funcionales destinadas a comprobar el correcto funcionamiento de los equipos '
            'y dispositivos del sistema. El mantenimiento debe realizarse inmediatamente después de las pruebas que detectan las '
            'fallas.'))
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
    a(('p', 'Cuando el funcionamiento de un dispositivo, circuito o función de la central se simule en lugar de accionarse, se '
            'debe dejar constancia en la planilla de que el funcionamiento fue simulado.'))

    a(('h4', 'Prueba mensual'))
    a(('p', 'Las pruebas mensuales tienen como finalidad verificar el funcionamiento de los componentes principales del sistema y '
            'de sus fuentes de alimentación.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Fusibles', 'comprobar su integridad y sus valores nominales.'),
        ('Equipos en interfase', 'verificar la comunicación con los sistemas asociados.'),
        ('Alimentación de energía primaria', 'comprobar el suministro eléctrico del sistema.'),
        ('Indicadores lumínicos del panel', 'iluminar y verificar todas las lámparas y LED.'),
        ('Indicadores sonoros del panel', 'comprobar el funcionamiento de las señales acústicas del panel.'),
        ('Señales de falla propias del panel', 'simular condiciones de falla y verificar la respuesta del sistema.'),
        ('Conexiones de red', 'verificar el estado de las conexiones.'),
        ('Panel de audio para evacuación', 'comprobar su funcionamiento.'),
        ('Tensión de baterías', 'medir la tensión de la alimentación secundaria.'),
        ('Conexiones entre la central y cada zona', 'comprobar continuidad y correcta conexión.'),
        ('Anunciadores remotos', 'verificar su funcionamiento y su comando, en caso de existir.'),
        ('Discador telefónico', 'comprobar la transmisión de señales al servicio de monitoreo.'),
        ('Detectores', 'probar los detectores de humo, temperatura, gas, llama y humo por aspiración forzada según la '
                       'recomendación del fabricante.'),
        ('Dispositivos de aviso lumínicos y sonoros', 'verificar su funcionamiento.'),
        ('Altavoces del sistema de audio para evacuación', 'comprobar su funcionamiento.'),
    ]))
    a(('p', cierre(2)))
    a(('p', 'En la prueba mensual, los detectores se prueban según la recomendación del fabricante; la prueba funcional de todos '
            'los detectores con humo o producto listado se realiza en la prueba anual. El protocolo siguiente se aplica en ambos casos.'))
    a(('protocol', ('prueba de dispositivos iniciadores', [
        ('Aislamiento de salidas', [
            ('Paso a paso', 'identificar en la secuencia de operación las funciones de control y los sistemas de extinción comandados '
                            'por la central; desconectar los solenoides o actuadores de descarga, o aislar las salidas según el '
                            'fabricante, y coordinar con el responsable las funciones de control que se van a deshabilitar.'),
            ('Justificación técnica', 'evita descargas accidentales y la interrupción de equipos críticos (NFPA 72, 14.2.6.4).'),
            ('Criterio de aceptación', 'todas las salidas críticas aisladas y registradas antes del primer accionamiento.')]),
        ('Detectores de humo', [
            ('Paso a paso', 'aplicar humo o un producto listado y aceptado por el fabricante, de modo que ingrese en la cámara '
                            'sensora a través de las ventilaciones, y verificar la alarma en la central.'),
            ('Justificación técnica', 'la verificación electrónica o con imán no comprueba el ingreso de humo a la cámara, que es la '
                                      'condición real de detección.'),
            ('Criterio de aceptación', 'alarma recibida en la central e identificación correcta de la zona.')]),
        ('Detectores de temperatura', [
            ('Paso a paso', 'en detectores restaurables, aplicar una fuente de calor listada o la indicada por el fabricante; en '
                            'detectores no restaurables, no aplicar calor y probar su funcionalidad en forma mecánica o eléctrica.'),
            ('Justificación técnica', 'el calor destruye el elemento de temperatura fija de los detectores no restaurables o '
                                      'combinados.'),
            ('Criterio de aceptación', 'alarma recibida en la central sin daño del detector.')]),
        ('Avisadores manuales y detectores de gas', [
            ('Paso a paso', 'operar los avisadores y probar los detectores de gas según las instrucciones del fabricante.'),
            ('Justificación técnica', 'cada tecnología requiere el método indicado por su fabricante para no dañar el sensor.'),
            ('Criterio de aceptación', 'señal recibida en la central para cada dispositivo probado.')]),
        ('Detectores especiales', [
            ('Paso a paso', 'en sistemas de muestreo de aire, probar con humo desde el extremo de cada tramo de tubería y verificar el '
                            'flujo en los demás puertos; en detectores de ducto con tubo de muestreo, verificar el muestreo de la '
                            'corriente de aire; en detectores de haz proyectado, introducir humo o un filtro óptico en la trayectoria.'),
            ('Justificación técnica', 'cada tecnología requiere el método de la NFPA 72, Tabla 14.4.3.2, ítem 17(g).'),
            ('Criterio de aceptación', 'alarma recibida en la central para cada dispositivo probado.')]),
        ('Restablecimiento', [
            ('Paso a paso', 'restablecer la central, reiniciar los aparatos que lo requieran y verificar que las funciones de '
                            'control deshabilitadas durante la prueba quedaron restauradas.'),
            ('Justificación técnica', 'una función de control que permanece deshabilitada anula la respuesta automática del sistema.'),
            ('Criterio de aceptación', 'sistema en condición normal, sin señales de falla.')]),
    ])))

    a(('h4', 'Prueba trimestral'))
    a(('p', 'Las pruebas trimestrales están orientadas a verificar el funcionamiento del sistema de respaldo energético.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Cargador de baterías del panel', 'ensayar el cargador según el protocolo de ensayo.'),
        ('Descarga de baterías', 'realizar la prueba de descarga según el protocolo de ensayo.'),
    ]))
    a(('p', cierre(3)))
    a(('protocol', ('cargador y descarga de baterías', [
        ('Protección de la programación', [
            ('Paso a paso', 'antes de cualquier prueba de baterías, verificar que la programación almacenada en memoria volátil está '
                            'protegida contra pérdidas.'),
            ('Justificación técnica', 'la desconexión de la alimentación puede borrar la configuración del panel.'),
            ('Criterio de aceptación', 'programación respaldada.')]),
        ('Prueba del cargador', [
            ('Paso a paso', 'con las baterías totalmente cargadas y conectadas al cargador, medir con voltímetro la tensión de las '
                            'baterías; en baterías de níquel-cadmio, medir la corriente de carga con amperímetro en serie.'),
            ('Justificación técnica', 'un cargador desajustado sobrecarga o deja descargadas las baterías.'),
            ('Criterio de aceptación', 'plomo-ácido y plomo-ácido selladas: **2,30 V por celda ± 0,02 V a 25 °C**, o el valor del '
                                       'fabricante; níquel-cadmio: corriente según el fabricante o, en su ausencia, de **1/30 a '
                                       '1/25** de la capacidad nominal.')]),
        ('Prueba de descarga', [
            ('Paso a paso', 'con el cargador desconectado, aplicar a las baterías la carga del sistema o una carga artificial '
                            'equivalente, según el fabricante, y medir la tensión.'),
            ('Justificación técnica', 'verifica la capacidad real de las baterías para sostener el sistema ante un corte de energía.'),
            ('Criterio de aceptación', 'la tensión no cae por debajo de los valores especificados por el fabricante.')]),
    ])))

    a(('h4', 'Prueba semestral'))
    a(('p', 'Las pruebas semestrales permiten comprobar la correspondencia entre los dispositivos y las acciones que generan, y el '
            'estado de carga de las baterías.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Accionamiento de dispositivos', 'comprobar que cada dispositivo activa la función que le corresponde.'),
        ('Módulos de control y sus acciones', 'verificar su funcionamiento.'),
        ('Módulos de verificación', 'comprobar su funcionamiento.'),
        ('Detectores de flujo', 'accionarlos haciendo fluir agua por la conexión de prueba o por la derivación de prueba de alarma, '
                                'según el tipo de sistema hidráulico.'),
        ('Interruptores de válvulas de control', 'accionar la válvula y verificar que la señal se recibe dentro de las primeras '
                                                 '**dos revoluciones** del volante o de **un quinto** del recorrido.'),
        ('Detectores en ductos', 'probar su funcionamiento.'),
        ('Tensión de carga de baterías', 'plomo-ácido abiertas: con el cargador desconectado y bajo carga, la tensión no debe caer '
                                         'por debajo de **2,05 V por celda**, y se debe medir la gravedad específica con hidrómetro '
                                         'de lectura numérica, dentro del rango del fabricante; plomo-ácido selladas: desempeño '
                                         'según el fabricante; níquel-cadmio: tensión de flotación nominal de **1,42 V por celda**, '
                                         'medida durante la carga y, si es posible, celda por celda.'),
        ('Detectores de llama', 'probar su funcionamiento y su sensibilidad con método o instrumento calibrado; no se deben usar '
                                'fuentes de luz que apliquen radiación no medida.'),
    ]))
    a(('p', cierre(3)))

    a(('h4', 'Prueba anual'))
    a(('p', 'Las pruebas anuales permiten verificar la capacidad operativa del sistema completo y su autonomía en condiciones '
            'prolongadas de funcionamiento.'))
    a(('p', 'Durante estas pruebas se debe verificar:'))
    a(('items', [
        ('Prueba de baterías de 24 horas', 'comprobar la autonomía del sistema ante un corte de la alimentación primaria.'),
        ('Planimetría', 'verificar con la planimetría de respaldo los posibles cambios estructurales o de distribución de la planta '
                        'que puedan modificar el diseño del sistema.'),
        ('Funciones de la central', 'verificar la recepción de señales de alarma, de supervisión y de falla, el funcionamiento de '
                                    'las señales de evacuación y de las funciones auxiliares, la supervisión de circuitos abiertos '
                                    'y de fallas a tierra y la indicación de pérdida de energía y de desconexión de baterías.'),
        ('Integridad de circuitos', 'probar cada circuito de dispositivos iniciadores y de aparatos de notificación para obtener la '
                                    'indicación correcta en la central.'),
        ('Detectores de humo', 'realizar la prueba funcional en el lugar de todos los detectores, con humo o producto listado.'),
        ('Detectores de temperatura fija restaurables', 'probar al menos **dos detectores por circuito** por año, distintos cada '
                                                        'año, de modo que en **cinco años** se hayan probado todos.'),
        ('Interruptores de supervisión', 'verificar la señal de los interruptores de presión de aire con una variación máxima de '
                                         '**70 kPa**, de temperatura ambiente y de agua a **4,4 °C**, y de nivel de agua con una '
                                         'variación máxima de **70 mm** en tanques a presión o **300 mm** en tanques sin presión.'),
        ('Aparatos de notificación', 'verificar el funcionamiento de los aparatos audibles, que se escuchen con claridad por encima '
                                     'del nivel sonoro ambiente promedio de ocupación normal y que su señal se distinga de otras '
                                     'señales del edificio (NFPA 101, 9.6.3.8 y 9.6.3.9), y que cada aparato visible presente '
                                     'iluminación intermitente.'),
        ('Funciones de control de emergencia', 'verificar la activación de los dispositivos de interfaz y su restauración luego de '
                                               'la prueba, incluidas, donde existan, la liberación de retenedores de puertas, la '
                                               'presurización de escaleras, el control de humo, el desbloqueo de puertas, la '
                                               'llamada y detención de ascensores y la detención del aire acondicionado (NFPA 72, '
                                               'Tabla 14.4.3.2, ítem 24; funciones enumeradas en la NFPA 101, 9.6.6.2).'),
        ('Baterías', 'reemplazarlas según el fabricante o cuando la batería recargada no alcance la tensión o la corriente '
                     'especificada.'),
        ('Alimentación primaria', 'probarla con carga máxima, con todos los aparatos de notificación en funcionamiento simultáneo.'),
        ('Señales de falla de la central', 'verificar las señales audibles y visuales de falla, la rellamada del silenciamiento y '
                                           'los interruptores de desconexión o aislamiento.'),
        ('Transmisión al servicio de monitoreo', 'accionar un dispositivo iniciador, crear una condición de falla y accionar un '
                                                 'dispositivo de supervisión, y verificar la recepción de cada señal fuera de las '
                                                 'instalaciones; con comunicador digital (DACT), verificar que cada intento de '
                                                 'transmisión se complete dentro de los **90 s** (NFPA 72, Tabla 14.4.3.2, ítem 4).'),
        ('Avisadores manuales', 'operar la totalidad de los avisadores manuales y verificar la señal en la central.'),
        ('Dispositivos electromecánicos de descarga', 'donde existan, verificar su funcionamiento mediante la remoción del '
                                                      'eslabón fusible (NFPA 72, Tabla 14.4.3.2, ítem 17).'),
        ('Interruptores de alarma de sistemas de extinción', 'donde existan, verificar la recepción de su señal en la central.'),
        ('Detectores de gas', 'probarlos según las instrucciones del fabricante.'),
        ('Aparatos de notificación audible textual', 'donde existan, verificar que la información emitida es distinguible y '
                                                     'comprensible (NFPA 72, Tabla 14.4.3.2, ítem 22).'),
    ]))
    a(('p', cierre(3)))
    a(('protocol', ('prueba de la fuente secundaria', [
        ('Corte de la alimentación primaria', [
            ('Paso a paso', 'notificar a los ocupantes y al servicio de monitoreo, desconectar todos los suministros de energía '
                            'primaria y verificar la indicación de falla correspondiente.'),
            ('Justificación técnica', 'la central debe advertir la pérdida de la alimentación principal.'),
            ('Criterio de aceptación', 'indicación de falla de energía primaria presente.')]),
        ('Capacidad de las baterías', [
            ('Paso a paso', 'medir la demanda de corriente de reserva y de alarma y verificar, con los datos del fabricante, que las '
                            'baterías cumplen los requisitos de autonomía; mantener el sistema en reserva durante **24 h**.'),
            ('Justificación técnica', 'confirma que el sistema funciona durante un corte prolongado de energía.'),
            ('Criterio de aceptación', 'sistema operativo al final del período de reserva.')]),
        ('Alarma con baterías', [
            ('Paso a paso', 'poner en funcionamiento la alarma general durante un mínimo de **5 minutos**, o el sistema de '
                            'comunicación de emergencia por voz durante un mínimo de **15 minutos**.'),
            ('Justificación técnica', 'la carga de alarma es la condición de mayor consumo y la más exigente para las baterías.'),
            ('Criterio de aceptación', 'aparatos de notificación en funcionamiento durante todo el período.')]),
        ('Reconexión', [
            ('Paso a paso', 'reconectar la alimentación primaria, restablecer la central y notificar la conclusión de la prueba; '
                            'registrar la tensión de reposo y verificar la recarga completa en el tiempo indicado por el fabricante, '
                            'informando al responsable que la autonomía queda reducida durante ese período.'),
            ('Justificación técnica', 'el sistema queda sin recarga de baterías hasta que se restituye la alimentación.'),
            ('Criterio de aceptación', 'sistema en condición normal y cargador en funcionamiento.')]),
    ])))

    # ---------------- MANTENIMIENTO ----------------
    a(('h3', 'MANTENIMIENTO'))
    a(('p', 'El mantenimiento comprende las tareas destinadas a conservar los equipos y componentes del sistema en condiciones '
            'adecuadas de funcionamiento y confiabilidad. Debe realizarse inmediatamente después de las pruebas que detectan '
            'fallas, según las instrucciones del fabricante y con una frecuencia que depende del tipo de equipo y de las '
            'condiciones ambientales del lugar. Los aparatos que deban rearmarse o reiniciarse se deben restablecer tan pronto '
            'como sea posible luego de cada prueba o alarma.'))

    a(('h4', 'Mantenimiento anual'))
    a(('p', 'El mantenimiento anual incluye tareas de limpieza, calibración y verificación técnica de los dispositivos del sistema.'))
    a(('p', 'Durante estas tareas se debe realizar:'))
    a(('items', [
        ('Limpieza del panel de control de alarma', 'eliminación de polvo o suciedad que pueda afectar el funcionamiento.'),
        ('Limpieza del panel de audio para evacuación', 'mantenimiento del sistema de comunicación de emergencia.'),
        ('Detectores de humo y temperatura', 'limpieza y calibración o verificación (**8,3 %**, según la planilla IRAM 3546-6E).'),
        ('Detectores de gas', 'limpieza y calibración o verificación según el fabricante (**8,3 %**, según la planilla IRAM 3546-6E).'),
        ('Valores indicados', 'verificación de los valores de los detectores y reemplazo de los que se encuentren fuera de los '
                              'valores determinados.'),
        ('Vida útil', 'reemplazo de los dispositivos de iniciación según la vida útil especificada por el fabricante.'),
        ('Modificación o reparación', 'modificación o reparación de la instalación según los eventos registrados en las planillas '
                                      'de inspecciones mensuales y anuales, acorde a la ingeniería básica.'),
    ]))
    a(('p', 'Para el reemplazo eventual de detectores se debe tener un **5 %** de cada tipo de elemento de iniciación.'))
    a(('p', cierre(4)))

    # ---------------- COMPLEMENTARIAS ----------------
    a(('h3', 'ENSAYOS DE LARGO PLAZO'))
    a(('p', 'Los ensayos de largo plazo tienen como finalidad verificar que los detectores conservan su sensibilidad de diseño a lo '
            'largo de su vida útil.'))
    a(('p', 'Se deben realizar:'))
    a(('items', [
        ('Sensibilidad de detectores de humo', 'control dentro del **primer año** posterior a la instalación y luego **cada dos '
                                               'años**; si después de la segunda prueba los detectores permanecen dentro de su '
                                               'rango, el intervalo puede extenderse hasta **cinco años**, conservando el registro '
                                               'de falsas alarmas. Se debe usar un método o instrumento calibrado; no se debe usar '
                                               'ningún dispositivo que aplique una concentración no medida de humo o aerosol.'),
        ('Detectores fuera de rango', 'limpieza y recalibración, ajuste dentro del rango listado o reemplazo.'),
        ('Detectores de temperatura fija no restaurables', 'a los **15 años** de la instalación, reemplazo de todos o ensayo de '
                                                           'laboratorio de **2 de cada 100**, repitiendo el ensayo cada **5 años** '
                                                           'si no se reemplazan.'),
    ]))
    a(('p', 'En zonas donde las falsas alarmas aumenten respecto del año anterior, se deben realizar pruebas de calibración '
            '(NFPA 72, 14.4.4.3.3.2).'))
    a(('p', compl(4)))

    a(('h3', 'SEGURIDAD Y SALUD OCUPACIONAL'))
    a(('p', 'La seguridad del personal tiene como finalidad evitar riesgos durante las tareas en altura y la manipulación de '
            'equipos energizados.'))
    a(('p', 'Durante las tareas se debe asegurar:'))
    a(('items', [
        ('Trabajo en altura', 'uso de escaleras o plataformas adecuadas y de los elementos de protección personal correspondientes.'),
        ('Equipos energizados', 'desconexión de la alimentación antes de intervenir el interior de la central o de las fuentes, y '
                                'manipulación de baterías con protección ocular y guantes.'),
        ('Condición de trabajo eléctricamente segura', 'para trabajar en la alimentación de la central o en tableros asociados se '
                                                       'debe establecer y verificar una condición de trabajo eléctricamente segura '
                                                       'según la NFPA 70E (120.5): identificar todas las fuentes, abrir los '
                                                       'dispositivos de desconexión y verificar su apertura, liberar la energía '
                                                       'almacenada, aplicar bloqueo y etiquetado según un procedimiento documentado y '
                                                       'verificar la ausencia de tensión con un instrumento cuyo funcionamiento se '
                                                       'comprueba antes y después en una fuente conocida.'),
        ('Sistemas de descarga asociados', 'aislamiento de los sistemas de extinción comandados por la central antes de probar los '
                                           'dispositivos iniciadores, para evitar descargas accidentales.'),
    ]))

    seguridad_humana(a, [
        ('Programa de prueba y mantenimiento (9.6.1.3 y 9.6.1.5)', 'el sistema de alarma debe instalarse, probarse y mantenerse '
                                                                   'según la NFPA 70 y la NFPA 72, con un programa aprobado que '
                                                                   'asegure su integridad operativa; el presente procedimiento '
                                                                   'puede constituir ese programa una vez aceptado por la '
                                                                   'autoridad competente.'),
        ('Sistema fuera de servicio (9.6.1.6)', 'los procedimientos ante la desactivación del sistema de alarma deben cumplir la '
                                                'NFPA 72; se aplican según lo indicado para la desactivación del sistema en el '
                                                'apartado PRUEBA de este procedimiento (NFPA 72, 10.20).'),
        ('Avisadores manuales (9.6.2.7)', 'deben permanecer accesibles, sin obstrucciones y visibles.'),
        ('Detectores cerca de cocinas y baños (9.6.2.10.4 y 9.6.2.10.5)', 'la instalación de alarmas y detectores de humo cerca '
                                                                           'de artefactos de cocción fijos y cerca de la puerta de '
                                                                           'un baño con ducha o bañera debe cumplir la NFPA 72. '
                                                                           'Se verifica en la inspección anual de cambios del '
                                                                           'edificio.'),
        ('Señal de evacuación (9.6.3.7, 9.6.3.8, 9.6.3.9 y 9.6.3.11)', 'la señal general de evacuación debe operar según el '
                                                                       'método aprobado: en todo el edificio, salvo los lugares '
                                                                       'exceptuados (9.6.3.7.1); por zonas, con notificación '
                                                                       'selectiva aprobada por la autoridad competente (9.6.3.7.2); '
                                                                       'o con los requisitos especiales para ocupantes que no pueden '
                                                                       'evacuar por sí mismos (9.6.3.7.3); '
                                                                         'debe oírse sobre el ruido ambiente, distinguirse de otras '
                                                                         'señales y los aparatos de notificación deben usarse solo '
                                                                         'para alarma o emergencia; los sistemas de comunicación de '
                                                                         'emergencia por voz pueden usarse para otros fines según la '
                                                                         'NFPA 72.'),
        ('Señales de supervisión y falla (9.6.4.4)', 'en instalaciones nuevas con aviso a bomberos, deben sonar y mostrarse en una '
                                                     'central receptora remota aprobada o en un lugar del edificio atendido en '
                                                     'forma permanente por personal calificado.'),
        ('Anunciación (9.6.8)', 'donde otra sección del código requiera anunciación, en el centro de control debe ser '
                                            'audible y visible, con al menos una zona por piso en edificios nuevos; las señales '
                                            'de falla y de supervisión también se deben anunciar.'),
        ('Monóxido de carbono (9.12)', 'donde sea requerida la detección de monóxido de carbono, debe cumplir la NFPA 72; los '
                                       'detectores instalados en conductos de aire no reemplazan la protección de las áreas '
                                       'abiertas (9.12.1).'),
    ])

    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'Las modificaciones del edificio, de su ocupación o de la distribución de la planta pueden alterar el diseño del sistema. '
            'Toda modificación del sistema o de su programación se debe evaluar técnicamente y documentar en los planos y en la '
            'secuencia de operación. Todo dispositivo agregado se debe probar; después de cambios en el software del sitio se deben '
            'probar el **100 %** de las funciones afectadas y el **10 %** de los dispositivos iniciadores no afectados, hasta un '
            'máximo de **50** (NFPA 72, 14.4.2.1 y 14.4.2.4). Las reparaciones o modificaciones del hardware de la central se '
            'prueban según los ítems 2(a) y 2(d) de la Tabla 14.4.3.2 (14.4.2.3), y los cambios del software ejecutivo requieren '
            'una prueba funcional del **10 %** del sistema, con al menos un dispositivo en cada circuito de entrada y de salida '
            '(14.4.2.5).'))
    a(('p', 'La empresa mantenedora es responsable de ejecutar las tareas de inspección, prueba y mantenimiento y de informar por '
            'escrito las deficiencias no corregidas. El usuario o propietario es responsable de completar las inspecciones de '
            'autocontrol, de conservar la documentación del sistema durante su vida útil y de coordinar las pruebas para no '
            'interrumpir equipos críticos del edificio. Los simulacros de evacuación, donde sean requeridos, son responsabilidad '
            'del propietario o usuario, y de cada uno se debe completar un registro escrito (NFPA 101, 4.7.6).'))
    return C


def REGISTRO_EXTRA(cierre):
    return [
        'La verificación documental y los datos de la instalación se registran en la planilla SG-PEM-IFI-SDI-1 %s – %s.' % (NOM, PL[1]),
        'Estos registros aseguran la trazabilidad de las actividades, permiten verificar el estado operativo del sistema, facilitan '
        'las auditorías técnicas y normativas e identifican tendencias de fallas o necesidades de mantenimiento.',
        'Los registros se deben conservar como mínimo durante **tres años**, según la IRAM 3546:2011; los de los detectores de '
        'temperatura restaurables probados en forma rotativa, durante el ciclo completo de cinco años más un año, según la %s, '
        '14.6.2, por ser ese plazo mayor.' % N72,
        'La documentación de diseño del sistema y los procedimientos de inspección, prueba y mantenimiento se deben conservar en '
        'un lugar aprobado y seguro durante toda la vida útil del sistema (NFPA 101, 9.11.3.1).',
        'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '
        'codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables se indican con NA. Toda '
        'condición O o X se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y '
        'por el responsable de la instalación, con su aclaración.',
    ]
