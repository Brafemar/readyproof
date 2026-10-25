# -*- coding: utf-8 -*-
"""Alcance particular de cada manual SG-PEM-IFI. build_manual.py lo inserta en el apartado ALCANCE de la plantilla:
intro reemplaza el primer párrafo, items reemplaza la lista genérica y rel se agrega después del párrafo «Incluye…»."""
BASE = ('El presente procedimiento es aplicable a las actividades de inspección, prueba, mantenimiento y control periódico del '
        '%s y de sus componentes, ejecutadas por la organización conforme al capítulo %s de la IRAM 3546:2011 y a los requisitos '
        'de la IRAM 3501-1.')

ALCANCES = {
'SDI': dict(items=[
    'Unidades de control de alarma de incendio, con sus fuentes de energía primaria y secundaria.',
    'Dispositivos iniciadores: detectores de humo, de temperatura, de llama y de gas, avisadores manuales y dispositivos de supervisión y de flujo conectados a la central.',
    'Aparatos de notificación audibles y visibles y sistemas de evacuación por voz.',
    'Circuitos, canalizaciones y conexiones del sistema.',
    'Anunciadores remotos, transmisión al servicio de monitoreo y módulos de control de funciones de emergencia.'],
    rel='Los sistemas de extinción, rociadores y bombas vinculados a la central se mantienen según sus procedimientos específicos; '
        'este procedimiento comprende las señales que esos sistemas envían a la central o reciben de ella.'),
'SRA': dict(items=[
    'Sistemas de rociadores automáticos de tubería húmeda, de tubería seca, de acción previa y de diluvio.',
    'Válvulas de control, de alarma, de tubería seca, de acción previa y de diluvio, con sus accesorios de puesto de control.',
    'Red de cañerías, soportes y rociadores, incluidos los rociadores de repuesto y sus llaves.',
    'Dispositivos de alarma de flujo y de supervisión, compresores y abastecimiento de aire o nitrógeno.',
    'Toma de impulsión para bomberos y cartel de datos del cálculo hidráulico.'],
    rel='El abastecimiento de agua, las bombas y la detección que comanda los sistemas de acción previa y de diluvio se mantienen '
        'según los procedimientos SG-PEM-IFI-SAA, SG-PEM-IFI-SBC y SG-PEM-IFI-SDI.'),
'SAP': dict(items=[
    'Sistemas fijos de agua pulverizada para la protección de equipos, recipientes y estructuras.',
    'Válvulas de diluvio con su sistema de presurización, y válvulas de control y de corte.',
    'Red de cañerías, soportes, filtros, drenajes y boquillas pulverizadoras.',
    'Sistema de detección y accionamiento propio del sistema y alarmas de flujo.',
    'Toma de impulsión para bomberos.'],
    rel='El abastecimiento de agua, las bombas y la detección vinculada a la central de alarma se mantienen según los procedimientos '
        'SG-PEM-IFI-SAA, SG-PEM-IFI-SBC y SG-PEM-IFI-SDI.'),
'SRE': dict(items=[
    'Sistemas de rociadores de espuma-agua de tubería húmeda, seca, de acción previa y de diluvio.',
    'Reserva de espumígeno, bomba de espumígeno y sistema proporcionador.',
    'Válvulas de control y de rociadores, red de tuberías y rociadores de espuma.',
    'Dispositivos de alarma, filtros, detección y actuación manual propios del sistema.',
    'Toma de impulsión para bomberos.'],
    rel='El abastecimiento de agua, las bombas y la detección vinculada a la central de alarma se mantienen según los procedimientos '
        'SG-PEM-IFI-SAA, SG-PEM-IFI-SBC y SG-PEM-IFI-SDI. Los ensayos de laboratorio del espumígeno se realizan en laboratorios '
        'que cuenten con los medios para hacerlos.'),
'SGE': dict(items=[
    'Sistemas generadores de espuma para la protección de tanques, recintos y áreas de riesgo.',
    'Tanque de emulsor, bomba de espumígeno y proporcionador o dosificador.',
    'Válvulas de control, red de tuberías y dispositivos de descarga de espuma.',
    'Sistema de detección, cuando la actuación depende de él, y toma de impulsión para bomberos.'],
    rel='El abastecimiento de agua, las bombas y la detección vinculada a la central de alarma se mantienen según los procedimientos '
        'SG-PEM-IFI-SAA, SG-PEM-IFI-SBC y SG-PEM-IFI-SDI.'),
'STM': dict(items=[
    'Sistemas de columnas de agua y mangueras, húmedos y secos.',
    'Válvulas interceptoras, red de tuberías y válvulas para mangas.',
    'Bocas de incendio equipadas, con sus gabinetes, mangueras, lanzas y accesorios.',
    'Dispositivos reguladores de presión, manómetros y alarmas de flujo.',
    'Toma de impulsión para bomberos y cartel de datos del cálculo hidráulico.'],
    rel='El abastecimiento de agua y las bombas se mantienen según los procedimientos SG-PEM-IFI-SAA y SG-PEM-IFI-SBC. El cuidado '
        'y las pruebas de las mangueras siguen la IRAM 3594.'),
'SBC': dict(items=[
    'Bombas contra incendio principales, de accionamiento eléctrico o por motor diésel, y bombas de mantenimiento de presión.',
    'Controladores, tableros y sus fuentes de alimentación, incluidos el combustible y las baterías de los motores diésel.',
    'Cañerías de succión y descarga, válvulas de control, de retención y de alivio.',
    'Dispositivos de prueba de la bomba, manómetros, sensores e indicadores.',
    'Recinto o sala de bombas, con su ventilación y calefacción.'],
    rel='La fuente de agua se mantiene según el procedimiento SG-PEM-IFI-SAA, y los sistemas que la bomba abastece, según sus '
        'procedimientos específicos.'),
'SAA': dict(items=[
    'Tanques de reserva de agua contra incendio elevados, a nivel, enterrados y a presión.',
    'Estructura soporte, escaleras, plataformas y accesos.',
    'Indicadores y alarmas de nivel y de temperatura, y sistema de calefacción.',
    'Válvulas de control, retención, drenaje y llenado, venteos y protección contra la corrosión.'],
    rel='Las bombas que toman agua del tanque y los sistemas que este abastece se mantienen según sus procedimientos específicos. '
        'La red pública de abastecimiento queda fuera del alcance.'),
'SHC': dict(items=[
    'Red exterior de servicio privado contra incendio, enterrada y a la vista.',
    'Válvulas interceptoras y sus indicadores de posición.',
    'Hidrantes de columna seca y de columna con agua, con sus bocas, tapas y accesorios.',
    'Armarios o casetas de mangueras y su equipamiento.',
    'Monitores conectados a la red.'],
    rel='El abastecimiento de agua y las bombas se mantienen según los procedimientos SG-PEM-IFI-SAA y SG-PEM-IFI-SBC.'),
'SEP': dict(items=[
    'Sistemas fijos de extinción por polvo químico para equipos, recintos y equipos de cocina.',
    'Cilindros contenedores de polvo, de presión contenida y presurizados con nitrógeno seco, o asociados a un cartucho de gas propelente.',
    'Sistema de disparo, con eslabones fusibles, cable, poleas y panel, y activador manual.',
    'Red de descarga, latiguillos y boquillas atomizadoras.',
    'Conexión al sistema de alarma y corte automático del suministro de gas o de energía.'],
    rel='Los extintores portátiles del área se mantienen según la IRAM 3517-2. Las cocinas comerciales protegidas con agente húmedo '
        'se mantienen según el procedimiento SG-PEM-IFI-SCC.'),
'SSA': dict(items=[
    'Sistemas fijos de extinción por solución acuosa para riesgos distintos de las cocinas comerciales.',
    'Recipientes de solución extintora, recipiente de presión auxiliar y cilindros de gas propelente.',
    'Sistema de detección, comandos de extinción y dispositivos de disparo.',
    'Red de descarga, flexibles y boquillas.',
    'Alarmas, manómetros, indicadores antimanipulación y equipo auxiliar.'],
    rel='Los sistemas que protegen cocinas comerciales se mantienen según el procedimiento SG-PEM-IFI-SCC.'),
'SCC': dict(items=[
    'Sistemas fijos de extinción por agente húmedo que protegen artefactos de cocción comercial, campanas, plenos y conductos.',
    'Cilindros de agente de presión contenida, presurizados con nitrógeno seco, o con cartucho de gas expelente donde el diseño lo prevé.',
    'Línea de detección por fusibles o detección electrónica, mecanismo de disparo, central de comando y pulsador manual.',
    'Red de descarga y toberas de artefactos, de pleno y de conducto.',
    'Cortes de gas y de energía de los artefactos y vinculación con el sistema de alarma del edificio.',
    'Verificación de las condiciones de la cocina que afectan al sistema: artefactos, filtros, extintores clase K y certificados de limpieza.'],
    rel='La limpieza de la campana y del conducto, a cargo de una empresa especializada, y el servicio técnico de los artefactos de '
        'cocción no forman parte de este procedimiento; el mantenedor verifica su constancia. La central de alarma del edificio se '
        'mantiene según el procedimiento SG-PEM-IFI-SDI.'),
'SAL': dict(items=[
    'Sistemas de extinción por agentes limpios de inundación total.',
    'Cilindros de agente, cabezales de control, válvulas de accionamiento y conexiones flexibles.',
    'Red de cañerías y boquillas de descarga.',
    'Sistema de detección, panel de control, interruptores de aborto y de disparo manual.',
    'Alarmas audibles y visuales, señalización y cierres automáticos de puertas, compuertas y ventilación.'],
    rel='La central de alarma del edificio a la que se vincula el panel se mantiene según el procedimiento SG-PEM-IFI-SDI. Los '
        'cambios del recinto protegido que afecten la concentración de diseño se evalúan con la memoria de cálculo del sistema.'),
'SDC': dict(items=[
    'Sistemas de extinción por dióxido de carbono de alta y de baja presión.',
    'Cilindros o depósito de baja presión, con su refrigeración, y cilindros piloto.',
    'Cabezales de control, válvulas direccionales y válvula de bloqueo.',
    'Red de cañerías, conexiones flexibles y boquillas.',
    'Detección, panel de control, alarmas, retardos, carteles de advertencia y cierres del recinto.'],
    rel='La central de alarma del edificio a la que se vincula el panel se mantiene según el procedimiento SG-PEM-IFI-SDI. Las '
        'pruebas hidrostáticas de cilindros se realizan según la IRAM 2529-1.'),
'SIM': dict(intro='El presente procedimiento es aplicable a la verificación de la simbología de seguridad contra incendios en los '
                  'planos y diagramas de las instalaciones mantenidas por la organización, conforme a la NFPA 170.',
    items=[
    'Planos de instalación de los sistemas fijos contra incendio.',
    'Planos conforme a obra que acompañan a las planillas de información general.',
    'Diagramas para análisis de riesgo y para aseguradoras.',
    'Diagramas y planos de evacuación exhibidos en el edificio.'],
    rel='La simbología se aplica a los sistemas tratados en los procedimientos de la serie SG-PEM-IFI; la elaboración de proyectos '
        'nuevos queda fuera del alcance.'),
}
