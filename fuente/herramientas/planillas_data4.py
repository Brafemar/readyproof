# -*- coding: utf-8 -*-
"""Planillas e informe del sistema SCC (cocinas comerciales, IRAM 3546:2011 cap. 16 + NFPA 96 + UL 300).
Planillas 1 a 4 según las planillas 16A a 16D de la IRAM 3546:2011; planilla 5 de aptitud según la UL 300 y la NFPA 96."""
SN = ['SI', 'NO']
B = '[______]'
SISTEMAS = {}

SEM = [('Inspector', ''),
       'Cilindro aislado y explosor reemplazado por lámpara o módulo de prueba antes de la prueba',
       'Funcionamiento del sistema y de los equipos asociados (IRAM 3546-16C)',
       'Sistema de detección del que depende la actuación probado según SG-PEM-IFI-SDI (IRAM 3546-16C, ver capítulo 6)',
       'Fusible de prueba del fabricante, identificado, en la posición más alejada del mecanismo',
       'Línea de detección: disparo con fusible de prueba (cada línea)', 'Recorrido del cable por poleas sin trabas',
       'Disparo por pulsador manual', 'Disparo por la central con lámpara o módulo de prueba',
       'Falla de línea de detección indicada', 'Falla de línea de disparo indicada',
       'Falla de línea de comando de válvula de gas indicada', 'Corte de gas al disparar', 'Corte de energía de los artefactos',
       'Indicaciones luminosas y sonoras', ('Tensión de batería', 'V'), 'Conmutación de la red a batería',
       ('Tensión de flote del cargador', 'V'), 'Capacidad de batería: 24 h en reposo y 5 min de alarma (NFPA 72, 10.6.7.2.1)',
       'Todas las pruebas repetidas en modo batería',
       'Señales recibidas en el sistema del edificio / monitoreo',
       'Todos los componentes de actuación y control probados (NFPA 96, 12.2.2)',
       'Corte de artefactos a gas no protegidos bajo la misma campana (NFPA 96, 10.4.3)',
       'Rearme manual de gas y energía; relé de rearme manual (NFPA 96, 10.4.4)',
       'Extractor: sigue funcionando tras el disparo y arranca si estaba detenido (NFPA 96, 8.2.3.1 y 8.2.3.2)',
       'Actuación simultánea de campanas de un único riesgo (NFPA 96, 10.3.1)',
       'Fusible de prueba retirado y fusible de servicio de la temperatura nominal repuesto',
       'Central en condición normal y salida de disparo inactiva antes de conectar el explosor',
       'Cilindro reconectado en último lugar; extinción conectada al finalizar']

MAN = [('Inspector', ''), 'Componentes en buen estado, no removidos ni reemplazados', 'Cilindro, identificación, soporte y sujeción a la pared',
       ('Manómetro (si existe): cilindro presurizado', 'bar'), 'Presión del cilindro (nitrógeno seco) o cartuchos de gas expelente (si existen)',
       'Capuchones de toberas en su lugar; tubería sin daños ni modificaciones', 'Toberas desarmadas y limpias',
       'Cañería de extinción limpia y no obstruida', 'Portafusibles y arcos portadetectores',
       ('Fusibles y rociadores de aleación metálica sustituidos (NFPA 96, 12.2.4)', 'u'),
       'Tarjeta con año de fabricación y fecha de instalación de fusibles, firmada (12.2.5 y 12.2.5.1)',
       'Fusibles retirados destruidos (12.2.5.2)', 'Compuertas cortafuego: accionamiento y fusibles (12.3)',
       'Tubería de detección, poleas de esquina y cable tensor', 'Interfaz o módulo mecánico de disparo',
       'Explosor: estado, conexión y vigencia', 'Central de comando y batería', 'Válvula de corte de gas y su rearme',
       'Alarmas y equipo auxiliar', 'Prueba hidrostática o reemplazo (según necesidad)']

SISTEMAS['SCC'] = dict(nom='Sistema Fijo de Extinción para Cocinas Comerciales', cap='16', planillas=[
    dict(n=1, nombre='Información general', tipo='general', bloques=[
        ('INSTALACIÓN', ['Designación del local', 'Marca y modelo del sistema', ('Sistema ensayado según UL 300 o norma equivalente', SN),
                         'Fecha de instalación del sistema',
                         ('No hay modificaciones del sistema, entorno o uso del área protegida (artefactos, campana, filtros y conducto)', SN)]),
        ('DATOS DE LA PLANILLA IRAM 3546-16A', ['Marca de los detectores', 'Fusible marca', ('Tipo de sistema', ['Alta presión', 'Baja presión']),
                                               ('Capacidad del cilindro', 'kg'), ('Capacidad del sistema', 'kg/m³'),
                                               ('Presión normal a 20 °C', 'MPa'), ('Disparo manual', ['Eléctrico', 'Neumático', 'Automático'])]),
        ('SISTEMA DE DETECCIÓN', [('Detectores termovelocimétricos', SN), ('Detectores de temperatura fija', SN),
                                  ('Detectores por compensación', SN), 'Otros']),
        ('COMANDOS DE EXTINCIÓN', [('Zona simple', SN), ('Dos zonas (zona cruzada)', SN), ('Dos detectores por zona', SN), 'Otros']),
        ('AGENTE Y CILINDROS', ['Agente extintor', ('Cantidad de cilindros', 'u'), ('Capacidad del cilindro', 'L'),
                                ('Presión de operación a 21 °C', 'bar'),
                                ('Gas expelente', ['Nitrógeno seco (presión contenida)', 'Cartucho', 'Recipiente auxiliar']),
                                'Fecha de la última prueba hidrostática']),
        ('DETECCIÓN Y DISPARO', [('Detección', ['Mecánica por fusibles', 'Electrónica', 'Otra']), ('Cantidad de fusibles', 'u'),
                                 ('Temperatura nominal de los fusibles', '°C'), 'Fecha del último reemplazo de fusibles',
                                 'Año de fabricación de los fusibles instalados',
                                 ('Disparo', ['Mecánico', 'Neumático', 'Explosor pirotécnico']), ('Pulsador manual', SN)]),
        ('CENTRAL DE COMANDO', ['Marca y modelo de la central', ('Batería', 'V / Ah'), 'Fecha de la batería',
                                ('Vinculación con alarma o monitoreo del edificio', SN)]),
        ('CORTES DE SEGURIDAD', [('Corte de gas', ['Válvula mecánica', 'Electroválvula', 'No posee gas']),
                                 ('Corte de energía de los artefactos', SN)]),
        ('COCINA Y EXTRACCIÓN (NFPA 96)', [('Volumen de cocción (Tabla 12.4)', ['Combustible sólido', 'Alto', 'Moderado', 'Bajo']),
                                           ('Frecuencia de inspección de grasa requerida', ['Mensual', 'Trimestral', 'Semestral', 'Anual']),
                                           'Empresa de limpieza del sistema de extracción', 'Fecha del último certificado de limpieza',
                                           ('Compuertas cortafuego en la campana', SN), ('Campanas que forman un único riesgo', 'u'),
                                           ('Extintores clase K', 'u')]),
        ('ARTEFACTOS PROTEGIDOS', [('Freidoras', 'u'), ('Planchas', 'u'), ('Anafes / hornallas', 'u'), ('Parrillas', 'u'),
                                   ('Woks', 'u'), ('Sartenes basculantes', 'u'), 'Otros']),
        ('TOBERAS', [('De artefactos', 'u'), ('De pleno y filtros', 'u'), ('De conducto', 'u')]),
        ('RESULTADOS', ['Resultado y comentarios de inspección / mantenimiento', 'Otros equipos probados o inspeccionados']),
    ]),
    dict(n=2, nombre='Inspección mensual', tipo='periodico', bloques=[
        ('INSPECCIÓN MENSUAL', [
            'Capuchones de toberas colocados', 'Sin grasa en fusibles, cable y toberas',
            'No se usan líquidos corrosivos en fusibles, cables y toberas', 'No se añadió, modificó, reemplazó ni movió ningún artefacto',
            'Toberas orientadas a las superficies que protegen', 'Filtros de la campana colocados y sin acumulación excesiva de grasa',
            'Pulsador manual libre y señalizado', 'Indicadores antimanipulación y sellos intactos',
            'Etiqueta o certificado de mantenimiento vigente', ('Presión indicada en el manómetro (si existe)', 'bar'),
            'Central: alimentación y extinción conectada, sin fallas', 'Sin objetos colgados de la línea de detección',
            'Extintor clase K en su lugar, con cartel (NFPA 96, 10.2.2)', 'Extractor en uso al cocinar; filtros colocados (12.1.1 y 12.1.2)',
            'Instrucciones de accionamiento manual exhibidas (12.1.4.3)']),
    ]),
    dict(n=3, nombre='Prueba semestral y quinquenal', tipo='checklist', bloques=[
        ('PRUEBA DEL PRIMER SEMESTRE', SEM),
        ('PRUEBA DEL SEGUNDO SEMESTRE', SEM),
        ('PRUEBA QUINQUENAL', [('Inspector', ''), 'Artefactos fríos, aceite retirado, gas y energía cortados',
                               'Prueba de descarga usando agua en lugar de solución acuosa',
                               'Todas las toberas descargan (artefactos, pleno y conducto)',
                               'Sistema de tubería secado con aire o nitrógeno',
                               'Cubas y artefactos vaciados y secos antes de cargar aceite o encender',
                               'Prueba hidrostática: recipiente de agente extintor',
                               'Prueba hidrostática: recipiente de presión auxiliar o cartucho', 'Prueba hidrostática: flexibles de unión',
                               'Recarga con nueva solución extintora acuosa', 'Cilindro presurizado con nitrógeno seco o cartucho repuesto; explosor reemplazado']),
    ]),
    dict(n=4, nombre='Mantenimiento', tipo='checklist', bloques=[
        ('MANTENIMIENTO DEL PRIMER SEMESTRE', MAN),
        ('MANTENIMIENTO DEL SEGUNDO SEMESTRE', MAN),
        ('MANTENIMIENTO ANUAL', ['Sustituir los eslabones fusibles (IRAM 3546-16D): cumplido con la sustitución semestral',
                                 'Detectores de bulbo y fusibles no metálicos: examen y limpieza o reemplazo (NFPA 96, 12.2.6)',
                                 'Otros sensores de temperatura fija: inspección y limpieza (NFPA 96, 12.2.7)',
                                 'Constancia de servicio anual de los artefactos de cocción (NFPA 96, 12.7.1)']),
        ('AGENTE Y RECARGA', ['Agente indicado por el fabricante, sin mezclas', 'Calidad y vigencia del agente según procedimiento documentado',
                              'Presurizado con nitrógeno seco a la presión del fabricante; sin pérdidas', 'Etiqueta y tarjeta del cilindro coincidentes',
                              ('Presión de operación a 21 °C', 'bar')]),
        ('POSTERIOR A UNA DESCARGA O ACTUACIÓN', ['Gas y energía cortados hasta la restitución', 'Agente y aceite saponificado retirados',
                                                  'Cilindro recargado', 'Explosor reemplazado', 'Fusibles reemplazados',
                                                  'Cilindro presurizado con nitrógeno seco o cartucho de gas expelente reemplazado',
                                                  'Toberas limpias y con capuchones', 'Central repuesta',
                                                  'Mecanismo de disparo y corte de gas rearmados; sellos, indicadores y etiqueta verificados',
                                                  'Prueba de funcionamiento sin descarga']),
        ('PUESTA FUERA DE SERVICIO', ['Aviso escrito al responsable y al monitoreo (causa y duración)',
                                      'Tarjeta de no conforme en central, cilindro y pulsador (NFPA 96, 12.1.6.1)',
                                      'Constancia de no uso de los artefactos',
                                      'Restitución: extinción conectada, tarjetas retiradas y partes informadas']),
        ('SISTEMA INTERVENIDO POR TERCEROS', ['Constancia y fotografías', 'Cilindro y disparo conectados',
                                              'Identificación del agente coincidente', 'Estado de los explosores',
                                              'Aviso escrito al responsable (si no está operativo)', 'Control completo antes de declararlo operativo']),
    ]),
    dict(n=5, nombre='Verificación de aptitud del sistema (UL 300 y NFPA 96)', tipo='checklist', bloques=[
        ('SISTEMA', ['Sistema y componentes ensayados según UL 300 (1.1, 2.3 y 2.4)',
                     'Red de descarga dentro de los límites del fabricante (5.19 y 6.1.4)',
                     ('Toberas por cilindro (límite del fabricante)', 'u'),
                     'Cilindro dentro del rango de temperatura de almacenamiento (6.1.5)',
                     'Presión dentro del rango operable (5.16 y 5.17)']),
    ] + [
        ('ARTEFACTO N° %d' % i, [('Tipo de artefacto', ''), 'Tipo previsto en el manual del fabricante (6.1.1)',
                                 ('Superficie de cocción (largo × ancho)', 'm'), 'Dentro de la cobertura de la tobera (6.1.8 y 6.1.10)',
                                 ('Altura de la tobera (mín. / máx. del manual)', 'mm'), 'Orientación de la tobera (6.1.7)',
                                 'Obstrucciones previstas en el manual (6.1.14)',
                                 'Corte de gas o energía al actuar (NFPA 96, 10.4.1); en freidoras de cubas múltiples, de todas las cubas (UL 300, 6.2.4)'])
        for i in range(1, 7)
    ] + [
        ('CAMPANA Y CONDUCTO (UL 300)', ['Filtros colocados en su posición de diseño (7.3.1)', 'Toberas de pleno con cobertura de filtros (7.12)',
                                         'Tobera de conducto en su posición', 'Sin cambios de campana, filtros o conducto']),
        ('PROTECCIÓN (NFPA 96)', ['Sistema según UL 300 o norma equivalente; si no cumple, no conformidad (10.2.3 a 10.2.3.2)',
                                  'Sin cañerías abandonadas; perforaciones selladas (10.2.7.1 y 10.2.7.2)',
                                  'Sin obstrucciones a la descarga de las toberas (10.2.7.3)',
                                  'Cambios del riesgo reevaluados (10.2.7.4)', 'Operación simultánea de un único riesgo (10.3.1)',
                                  'Corte automático de combustible y energía; rearme manual (10.4)',
                                  'Pulsador en vía de egreso, identificado, con instrucciones y protección (10.5.1)',
                                  'Alarma o indicación de actuación; activación de la alarma del edificio (10.6)',
                                  'Extintores clase K listados, con cartel; sin extintores de CO₂ (10.2.2 y 10.9)']),
        ('CAMPANA, FILTROS Y ARTEFACTOS (NFPA 96)', [('Distancia filtro – superficie de cocción (≥ 457 mm; ≥ 1,22 m sobre parrillas a la brasa o de combustible sólido) (6.2.1)', 'mm'),
                                                     'Filtros listados, no combustibles, rígidos (6.2.3.1 a 6.2.3.3)',
                                                     'Todo el aire pasa por los filtros (6.2.3.4)', ('Inclinación de filtros (≥ 45°)', '°'),
                                                     'Extractor sigue funcionando tras la actuación y arranca si estaba detenido (8.2.3.1 y 8.2.3.2)',
                                                     ('Separación freidora – llamas contiguas (≥ 406 mm o pantalla ≥ 203 mm)', 'mm'),
                                                     'Artefactos en su posición de diseño (13.1.2.2 y 13.1.2.3)']),
        ('LIMPIEZA DEL SISTEMA DE EXTRACCIÓN (NFPA 96, 12.4 Y 12.6)', ['Frecuencia de inspección según Tabla 12.4 cumplida',
                                                                       ('Espesor de grasa medido (limpieza a 2000 µm; 3175 µm en la carcasa del extractor) (12.6.1.1.3 y 12.6.1.1.4)', 'µm'),
                                                                       'Superficies limpias hasta 50 µm como máximo (12.6.1.1.1)',
                                                                       'Certificado de limpieza en el local (12.6.13)',
                                                                       'Informe con áreas no limpiadas (12.6.14)',
                                                                       'Etiquetas junto a paneles de acceso (12.6.10)',
                                                                       'Recipientes de grasa inspeccionados o vaciados al menos una vez por semana (12.6.16)']),
    ]),
])

INFORMES = {
'SCC': dict(
    periodo='[MENSUAL / SEMESTRAL / ANUAL / QUINQUENAL]',
    nc='NC-%02d: ______ → Incumplimiento [IRAM 3546:2011, capítulo {cap} / NFPA 96 / UL 300], ítem ______',
    equipo=('Sistema:', 'Marca:', 'Modelo:'),
    ident=[('Agente extintor:', ''), ('Cantidad y capacidad de cilindros:', '[______] – [______ L]'),
           ('Detección:', '[MECÁNICA POR FUSIBLES / ELECTRÓNICA]'), ('Disparo:', '[MECÁNICO / NEUMÁTICO / EXPLOSOR]'),
           ('Corte de gas:', '[VÁLVULA MECÁNICA / ELECTROVÁLVULA / NO POSEE GAS]'), ('Artefactos protegidos:', '[______]'),
           ('Fecha de instalación:', '')],
    alcance='cilindro de agente y su soporte, línea y tubería de detección, fusibles, mecanismo de disparo, central de comando y '
            'batería, pulsador manual, red de descarga, toberas de artefactos, pleno y conducto, cortes de gas y de energía, '
            'alarmas, vinculación con el edificio, extintores clase K y verificación de la limpieza del sistema de extracción',
    resultados=[
        ('RESULTADOS GENERALES', ['Se verificaron %s ítems de las planillas aplicables, de los cuales %s resultaron conformes, lo que '
                                  'representa un [______ %%] del total evaluado.' % (B, B)]),
        ('APTITUD DEL SISTEMA', ['Se verificaron %s artefactos; %s se encuentran fuera de la cobertura listada o con toberas fuera de '
                                 'sus límites.' % (B, B),
                                 'Se detectaron [______] cambios en la cocina que requieren evaluación técnica.']),
        ('DETECCIÓN Y DISPARO', ['La prueba de funcionamiento sin descarga resultó [CORRECTA / CON FALLAS] en detección, disparo '
                                 'manual, disparo por la central y supervisión de fallas.',
                                 'Se sustituyeron [______] fusibles de [______ °C], con su tarjeta de año de fabricación y fecha de '
                                 'instalación.']),
        ('CORTES DE SEGURIDAD', ['El corte de gas y el corte de energía de los artefactos actuaron en forma [CORRECTA / DEFICIENTE / NA].']),
        ('CENTRAL Y BATERÍA', ['La batería presentó una tensión de [______ V] y el cargador una tensión de flote de [______ V]; las '
                               'pruebas en modo batería resultaron [CORRECTAS / CON FALLAS].']),
        ('CILINDRO Y AGENTE', ['El manómetro indicó [______ bar], presión [DENTRO / FUERA] del rango de operación; la identificación '
                               'del agente resultó [COINCIDENTE / NO COINCIDENTE].']),
        ('INSPECCIÓN MENSUAL', ['Las inspecciones mensuales del período [SE REALIZARON / NO ESTÁN CONTRATADAS]; meses registrados: '
                                '[______].']),
        ('PRUEBA QUINQUENAL', ['La prueba de descarga con agua y las pruebas hidrostáticas del recipiente de agente, del recipiente de '
                               'presión auxiliar o cartucho y de los flexibles resultaron [CORRECTAS / CON FALLAS / NO CORRESPONDEN EN '
                               'EL PERÍODO]; última prueba: [______].']),
        ('TOBERAS Y RED', ['Se limpiaron [______] toberas y la cañería de extinción; [______] capuchones fueron repuestos.']),
        ('SISTEMA DE EXTRACCIÓN', ['El último certificado de limpieza es del [______]; la frecuencia requerida por la NFPA 96, '
                                   'Tabla 12.4, es [MENSUAL / TRIMESTRAL / SEMESTRAL / ANUAL] y [SE CUMPLE / NO SE CUMPLE].']),
        ('CERTIFICADO DE OPERATIVIDAD', ['Al finalizar el servicio el sistema queda [OPERATIVO / FUERA DE SERVICIO]. Acciones '
                                         'requeridas: [______].']),
    ],
    criterios=['Ítems conformes: [______ %]', 'Aptitud del sistema (UL 300 y NFPA 96): [CONFORME / NO CONFORME]', 'Limpieza del sistema de extracción: [CONFORME / NO CONFORME]', 'Fallas críticas: [______]']),
}
