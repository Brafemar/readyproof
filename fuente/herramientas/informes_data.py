# -*- coding: utf-8 -*-
"""Contenido de los informes generales prediseñados (-IN), con la estructura del SG-PEM-IFI-SDI-2-IN."""
B = '[______]'

INFORMES = {
'SAP': dict(
    equipo=('Válvula de diluvio:', 'Marca:', 'Modelo:'),
    ident=[('Tipo de accionamiento:', '[MANUAL / DETECCIÓN AUTOMÁTICA]'), ('Tipo de detección:', '[NEUMÁTICO / ELÉCTRICO / OTRO]'),
           ('Cantidad de toberas / faltantes:', ''), ('Abastecimiento de agua:', '[SIN PRESIÓN / HIDRONEUMÁTICO]'),
           ('Sistema de presurización:', '[AIRE COMPRIMIDO / NITRÓGENO / BOMBA]'), ('Bombas contra incendio:', '[DIÉSEL / ELÉCTRICA / NINGUNA]'),
           ('Elemento protegido:', '')],
    alcance='válvulas de diluvio y de control, red de cañerías y soportes, boquillas pulverizadoras, abastecimiento de agua, '
            'sistema de presurización, sistema de detección y accionamiento, y toma de impulsión para bomberos',
    resultados=[
        ('RESULTADOS GENERALES', ['Se verificaron %s ítems de las planillas aplicables, de los cuales %s resultaron conformes, lo que '
                                  'representa un [______ %%] del total evaluado.' % (B, B),
                                  'El sistema se encuentra [EN SERVICIO / FUERA DE SERVICIO], con [______] ítems registrados como '
                                  'NO APLICABLE.']),
        ('VÁLVULAS Y CONTROL', ['Las válvulas de control se encontraron [ABIERTAS Y PRECINTADAS / CON DESVÍOS], con %s válvulas '
                                'que requirieron reprecintado o corrección de posición.' % B,
                                'La válvula de diluvio presenta una condición [CORRECTA / CON DAÑOS O FUGAS] en la inspección interna.']),
        ('ABASTECIMIENTO Y PRESURIZACIÓN', ['Se registró una presión del sistema de [______ MPa] al comienzo y de [______ MPa] al final '
                                            'de la inspección, considerada [NORMAL / FUERA DE VALORES].',
                                            'El sistema de presurización presenta una condición [OPERATIVA / CON FALLAS], con presiones de '
                                            'arranque y parada del compresor de [______ MPa] y [______ MPa].']),
        ('BOQUILLAS Y RED DE CAÑERÍAS', ['Se inspeccionaron %s boquillas, de las cuales %s presentan corrosión, obstrucción o '
                                         'desorientación.' % (B, B),
                                         'La red de cañerías y sus soportes presentan una condición [ADECUADA / CON DESVÍOS].']),
        ('PRUEBAS DE FUNCIONAMIENTO', ['La prueba en blanco resultó [CORRECTA / CON FALLAS] en la secuencia detección – disparo de la válvula.',
                                       'La prueba a caudal total registró un tiempo de operación de [______ s] y una cobertura '
                                       '[ADECUADA / INSUFICIENTE] sobre el elemento protegido.']),
    ],
    criterios=['Ítems conformes: [______ %]', 'Fallas críticas: [______]', 'Condición del abastecimiento y la presurización: [______]']),

'SRE': dict(
    equipo=('Válvula de control:', 'Marca:', 'Modelo:'),
    ident=[('Control de las válvulas:', '[PRECINTADAS / ENCLAVADAS / SUPERVISADAS]'), ('Tipo de válvula de rociadores:', '[ALARMA / DILUVIO / PREACCIÓN]'),
           ('Reserva de espumígeno:', '[TANQUE ATMOSFÉRICO / TANQUE A PRESIÓN]'), ('Sistema proporcionador:', ''),
           ('Bomba de espumígeno:', '[SI / NO]'), ('Bombas contra incendio:', '[DIÉSEL / ELÉCTRICA / NINGUNA]'),
           ('Área protegida:', '')],
    alcance='válvulas de control y de rociadores, abastecimiento de agua, reserva y bomba de espumígeno, sistema proporcionador, red de '
            'tuberías, rociadores de espuma, dispositivos de alarma y sistema de detección',
    resultados=[
        ('RESULTADOS GENERALES', ['Se verificaron %s ítems de las planillas aplicables, de los cuales %s resultaron conformes, lo que '
                                  'representa un [______ %%] del total evaluado.' % (B, B)]),
        ('ABASTECIMIENTO DE AGUA', ['La prueba de caudal con el drenaje principal registró una presión estática de [______ MPa] y una '
                                    'presión residual de [______ MPa], con una variación de [______ %] respecto de la lectura anterior, '
                                    'considerada [ACEPTABLE / A INVESTIGAR (> 10 %)].']),
        ('VÁLVULAS Y ALARMAS', ['Las válvulas de control se encontraron [ABIERTAS Y PRECINTADAS / CON DESVÍOS].',
                                'La alarma de flujo actuó en forma [CORRECTA / DEFICIENTE] durante la prueba por bypass.']),
        ('ESPUMÍGENO Y DOSIFICACIÓN', ['El control de sedimentos del depósito resultó [SIN INCRUSTACIONES / CON INCRUSTACIONES].',
                                       'El informe de calidad del espumígeno resultó [APTO / NO APTO].',
                                       'La dosificación medida fue de [______ %] de la mínima de diseño, valor [CONFORME / NO CONFORME] '
                                       'respecto del mínimo del 90 % establecido por la norma.']),
        ('PRUEBA FUNCIONAL DE DESCARGA', ['Se registró un tiempo de respuesta de [______ s], un tiempo de descarga de [______ s], una presión '
                                          'en el rociador más alejado de [______ bar] y en la válvula de control principal de [______ bar].',
                                          'La descarga de los rociadores resultó [CORRECTA / DEFICIENTE] en dirección y patrón.']),
    ],
    criterios=['Ítems conformes: [______ %]', 'Dosificación: [______ %] (mínimo 90 %)', 'Fallas críticas: [______]']),

'SGE': dict(
    equipo=('Válvula y formadores de espuma:', 'Marca:', 'Modelo:'),
    ident=[('Tipo de sistema:', '[HÚMEDO / SECO / DILUVIO / ACCIÓN PREVIA]'), ('Tanque de espumígeno:', '[PRFV / METÁLICO] – Capacidad: [______ L]'),
           ('Dosificador:', '[EDUCTOR / PILOTAJE / PRESIÓN BALANCEADA]'), ('Cantidad de toberas / faltantes:', ''),
           ('Abastecimiento de agua:', '[GRAVEDAD / BAJO PRESIÓN]'), ('Bombas contra incendio:', '[DIÉSEL / ELÉCTRICA / NINGUNA]'),
           ('Riesgo protegido:', '')],
    alcance='abastecimiento de agua, válvulas de control, proporcionador, tanque de emulsor, bomba de espumígeno, red de tuberías, '
            'cámaras y formadores de espuma y sistema de detección asociado',
    resultados=[
        ('RESULTADOS GENERALES', ['Se verificaron %s ítems de las planillas aplicables, de los cuales %s resultaron conformes, lo que '
                                  'representa un [______ %%] del total evaluado.' % (B, B),
                                  'Se detectaron [______] alteraciones respecto del diseño original del sistema.']),
        ('VÁLVULAS Y ABASTECIMIENTO', ['Las válvulas de control se encontraron [ABIERTAS Y PRECINTADAS / CON DESVÍOS] y el abastecimiento '
                                       'de agua presenta una condición [DISPONIBLE / CON DESVÍOS].']),
        ('ESPUMÍGENO Y DEPÓSITO', ['El depósito de espumígeno se encontró [LLENO HASTA LA MITAD DE LA CÚPULA / CON NIVEL INSUFICIENTE].',
                                   'El control de sedimentos resultó [SIN SEDIMENTOS / CON SEDIMENTOS] y la válvula de presión-vacío se '
                                   'encontró [CORRECTA / CON DESVÍOS].',
                                   'El informe de calidad del espumígeno resultó [APTO / NO APTO].']),
        ('DISPOSITIVOS DE DESCARGA', ['Se inspeccionaron %s cámaras o formadores de espuma, de los cuales %s presentan daños, '
                                      'obstrucciones o sellos deteriorados.' % (B, B)]),
        ('PRUEBA FUNCIONAL DE DESCARGA', ['Se registró un tiempo de respuesta de [______ s], un tiempo de descarga de [______ s] y una '
                                          'dosificación de [______ %] de la mínima de diseño, valor [CONFORME / NO CONFORME] respecto del '
                                          'mínimo del 90 % establecido por la norma.',
                                          'La calidad de la espuma obtenida resultó [ADECUADA / DEFICIENTE] según los valores del fabricante.']),
    ],
    criterios=['Ítems conformes: [______ %]', 'Dosificación: [______ %] (mínimo 90 %)', 'Fallas críticas: [______]']),

'SEP': dict(
    equipo=('Cilindro de polvo:', 'Marca:', 'Modelo:'),
    ident=[('Riesgo protegido:', ''), ('Equipos protegidos:', '[FREIDORA / PLANCHA / PARRILLA / QUEMADOR / CONDUCTO / OTROS]'),
           ('Agente extintor:', ''), ('Peso y presión normales:', '[______ kg] – [______ kPa]'),
           ('Cartucho de gas propelente:', '[NITRÓGENO / CO₂ / NO POSEE]'), ('Conexión a alarma:', '[SI / NO]'),
           ('Corte automático:', '[GAS / ELÉCTRICO / NO POSEE]')],
    alcance='cilindro contenedor de polvo, cartucho de gas propelente, sistema de disparo por eslabones fusibles o señales, '
            'activador manual, red de descarga, boquillas atomizadoras, alarma y corte automático del equipo protegido',
    resultados=[
        ('RESULTADOS GENERALES', ['Se verificaron %s ítems de las planillas aplicables, de los cuales %s resultaron conformes, lo que '
                                  'representa un [______ %%] del total evaluado.' % (B, B)]),
        ('CARGA DEL SISTEMA', ['El cilindro de polvo registró una presión de [______ kPa] y un peso de [______ kg], valores '
                               '[IGUALES O MAYORES / MENORES] que los mínimos anotados en la planilla de información general.',
                               'El polvo se encontró [SUELTO / APELMAZADO].']),
        ('SISTEMA DE DISPARO', ['La prueba del accionamiento automático resultó [CORRECTA / CON FALLAS].',
                                'Se sustituyeron [______] eslabones fusibles por otros del mismo rango de temperatura.']),
        ('BOQUILLAS Y EQUIPO PROTEGIDO', ['Se verificaron %s boquillas, de las cuales %s presentan grasa acumulada, tapas faltantes o '
                                          'desorientación.' % (B, B),
                                          'Se detectaron [______] modificaciones de los equipos de cocina que requieren evaluación técnica.']),
        ('ALARMA Y CORTE AUTOMÁTICO', ['El corte automático de [GAS / ENERGÍA] y la alarma actuaron en forma [CORRECTA / DEFICIENTE], y '
                                       'su rearme se realizó en condiciones seguras.']),
    ],
    criterios=['Ítems conformes: [______ %]', 'Carga y presión: [CONFORME / NO CONFORME]', 'Fallas críticas: [______]']),

'SSA': dict(
    equipo=('Sistema:', 'Marca:', 'Modelo:'),
    ident=[('Tipo de sistema:', '[ALTA PRESIÓN / BAJA PRESIÓN]'), ('Cantidad y capacidad de cilindros:', '[______] – [______ kg]'),
           ('Presión normal a 20 °C:', '[______ MPa]'), ('Disparo:', '[MANUAL / ELÉCTRICO / NEUMÁTICO / AUTOMÁTICO]'),
           ('Detección:', '[TERMOVELOCIMÉTRICOS / TEMPERATURA FIJA / COMPENSACIÓN]'), ('Comando de extinción:', '[ZONA SIMPLE / ZONA CRUZADA / DOS DETECTORES POR ZONA]'),
           ('Fecha de instalación:', '')],
    alcance='recipientes de solución extintora acuosa, recipiente de presión auxiliar y cilindros de gas propelente, sistema de '
            'detección y eslabones fusibles, dispositivos de disparo, red de descarga, boquillas y alarmas',
    resultados=[
        ('RESULTADOS GENERALES', ['Se verificaron %s ítems de las planillas aplicables, de los cuales %s resultaron conformes, lo que '
                                  'representa un [______ %%] del total evaluado.' % (B, B)]),
        ('RECIPIENTES Y PRESIÓN', ['Los manómetros indicaron una presión de [______ MPa], considerada [ADECUADA / NO ADECUADA].',
                                   'Los recipientes y cilindros de gas propelente presentan una condición [CORRECTA / CON DAÑOS O CORROSIÓN].']),
        ('DETECCIÓN Y DISPARO', ['La prueba de funcionamiento sin descarga resultó [CORRECTA / CON FALLAS] en detección, alarmas y '
                                 'dispositivos de disparo.',
                                 'Se sustituyeron [______] eslabones fusibles.']),
        ('BOQUILLAS Y EQUIPO PROTEGIDO', ['Se verificaron %s boquillas, de las cuales %s presentan grasa acumulada, tapas faltantes, '
                                          'obstrucción o desorientación.' % (B, B),
                                          'Se detectaron [______] modificaciones de los equipos de cocina que requieren evaluación técnica.']),
        ('PRUEBA QUINQUENAL', ['La prueba de descarga con agua resultó [CORRECTA / CON BOQUILLAS OBSTRUIDAS]; la red se secó y el '
                               'sistema se recargó con nueva solución extintora acuosa.',
                               'Las pruebas hidrostáticas resultaron [APROBADAS / NO APROBADAS].']),
    ],
    criterios=['Ítems conformes: [______ %]', 'Condición de recipientes y presión: [______]', 'Fallas críticas: [______]']),
}
