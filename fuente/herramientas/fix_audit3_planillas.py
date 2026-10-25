"""Auditoría 3: A3-C1, A3-C2, A3-M3 sobre planillas_data2.py y A3-M1 (leyenda/columnas) sobre build_planilla.py."""
import sys, os
T = sys.argv[1]
def patch(fn, pairs):
    p = os.path.join(T, fn); s = open(p, encoding='utf8').read()
    for o, n in pairs:
        assert s.count(o) == 1, (fn, o[:80], s.count(o)); s = s.replace(o, n)
    open(p, 'w', encoding='utf8').write(s)

# ---------- build_planilla: tres símbolos ----------
patch('build_planilla.py', [
 ("for c1, c2, t in [(1, 16, 'VERIFICACIÓN'), (17, 19, 'VALOR'), (20, 21, 'CUMPLE'), (22, 23, 'NO CUMPLE'), (24, 25, 'NA')]:\n"
  "            s.cell(c1, c2, r0, r0, t, F(9 if c1 > 16 else 11, True), h='center')",
  "for c1, c2, t in [(1, 14, 'VERIFICACIÓN'), (15, 17, 'VALOR'), (18, 19, 'CUMPLE ✓'), (20, 21, 'NO CUMPLE O'),\n"
  "                          (22, 23, 'NO APREC. X'), (24, 25, 'NA')]:\n"
  "            s.cell(c1, c2, r0, r0, t, F(8 if c1 > 14 else 11, True), h='center')"),
 ("            s.cell(1, 16, r, r, txt, F(10))\n            s.cell(17, 19, r, r, ('_____ ' + unit) if unit else '', F(9), h='right')\n"
  "            for c1, c2 in [(20, 21), (22, 23), (24, 25)]:",
  "            s.cell(1, 14, r, r, txt, F(10))\n            s.cell(15, 17, r, r, ('_____ ' + unit) if unit else '', F(9), h='right')\n"
  "            for c1, c2 in [(18, 19), (20, 21), (22, 23), (24, 25)]:"),
 ("            s.height(r, txt, 16)\n        s.r = r0 + 1 + len(items)", "            s.height(r, txt, 14)\n        s.r = r0 + 1 + len(items)"),
 ("'CUMPLE ✓     ·     NO CUMPLE O NO APRECIABLE X     ·     NA: NO APLICABLE     ·     '\n"
  "                               'Toda condición que no cumpla se debe describir en observaciones.'",
  "'CUMPLE: ✓     ·     NO CUMPLE: O     ·     NO APRECIABLE: X     ·     NA: NO APLICABLE     ·     '\n"
  "                               'Toda condición O o X se debe describir en observaciones.'"),
])

SDI = '''SISTEMAS['SDI'] = dict(nom='Sistema de Detección de Incendios', cap='6', planillas=[
    dict(n=1, nombre='Información general', titulo='Información general – Sistema convencional de dos hilos', tipo='general', bloques=[
        ('INSTALACIÓN', ['Designación del sistema',
                         ('No hay modificación en el sistema, entorno o uso del área protegida', SN)]),
        ('PANEL DE CONTROL', ['Ubicación de la central', 'Marca y modelo',
                              ('Tipo de sistema', ['Convencional', 'Direccionable', 'Inteligente', 'Otros']),
                              'Cantidad de zonas: en servicio / de reserva', ('Sistema en servicio', SN),
                              ('Manual instructivo de operación en español', SN)]),
        ('ELEMENTOS DE INICIACIÓN', ['Control e identificación', 'Detectores de humo: cantidad / tipo / marca',
                                     'Detectores de temperatura: cantidad / tipo / marca', 'Detectores de llama: cantidad / tipo / marca',
                                     'Avisadores manuales: cantidad / tipo / marca']),
        ('FUENTES DE ENERGÍA', [('Primaria', ['Red eléctrica urbana', 'Grupo generador', 'Alimentado']),
                                ('Secundaria: tensión / corriente', 'V / A'), ('Secundaria alimentada', SN)]),
        ('CONDUCTOS', ['Tipo de instalación', ('Largo total', 'm'), ('Diámetro', 'mm'), 'Material del conducto']),
        ('CABLEADO', [('Aprobación del cable', SN), ('Memoria técnica de la conexión', SN), ('Existe plano de cableado', SN)]),
        ('ALARMAS', [('Señal visual / acústica', ['Estroboscópica', 'Rotativa acústica', 'Señal acústica', 'Sirena'])]),
        ('ANUNCIACIÓN', [('Posee sistema de aviso con parlantes', SN), ('Tipo', ['Estándar', 'Intrínsecos'])]),
    ]),
    dict(n=2, nombre='Prueba mensual', titulo='Prueba mensual – Sistema convencional de dos hilos', tipo='periodico', bloques=[
        ('PANEL DE CONTROL', ['Fusibles', 'Equipos de interfase', 'Alimentación de energía primaria', 'Indicadores lumínicos del panel',
                              'Señales de falla propias del panel de simulación', 'Conexiones de red', 'Panel de audio para evacuación',
                              'Medición de tensión de baterías (alimentación secundaria)', 'Conexiones entre la central y cada zona',
                              'Anunciadores remotos y su comando (en caso de existir)', 'Discador telefónico']),
        ('ELEMENTOS DE INICIACIÓN', ['Detectores de humo', 'Detectores de temperatura', 'Detectores de llama',
                                     'Detectores de gas/monóxido', 'Avisadores manuales', 'Barreras infrarrojas', 'Sistema aspirador',
                                     'Detección del nivel del tanque de agua', 'Indicación detectores de flujo',
                                     'Indicación de baja presión en red de cañerías', 'Indicación arranque de bomba']),
        ('TAREAS COMPLEMENTARIAS (TEXTO IRAM Y NFPA 72)', [
            'Indicadores sonoros del panel', 'Dispositivos de aviso lumínicos y sonoros', 'Altavoces del sistema de audio para evacuación',
            'Baterías: corrosión, fugas, conexiones y fecha (NFPA 72, T. 14.3.1)', 'Baterías de plomo-ácido: nivel de electrolito',
            'Baterías primarias (pila seca)', 'Desactivaciones del mes registradas (inicio, fin, causa, medidas)']),
    ]),
    dict(n=3, nombre='Prueba trimestral, semestral y anual', titulo='Prueba trimestral, semestral y anual – Sistema convencional de dos hilos',
         tipo='checklist', bloques=[
        ('PRUEBA TRIMESTRAL', ['Ensayo del cargador de baterías del panel', 'Prueba de descarga de baterías',
                               ('Tensión de flotación del cargador (2,30 V/celda ± 0,02 V a 25 °C)', 'V')]),
        ('PRUEBA SEMESTRAL', ['Accionamiento de dispositivos para asegurar su correspondencia con su funcionamiento',
                              'Módulos de control y sus accionamientos', 'Módulos de verificación', 'Accionamiento de detectores de flujo',
                              'Prueba de detectores en ductos',
                              'Interruptores de válvulas de control (señal en 2 vueltas o 1/5 del recorrido)',
                              ('Tensión de baterías bajo carga (≥ 2,05 V/celda plomo-ácido)', 'V'), 'Detectores de llama']),
        ('PRUEBA ANUAL', ['Prueba de baterías (24 h)', 'Planimetría',
                          'Funciones de la central (alarma, supervisión, falla, evacuación, auxiliares)', 'Integridad de circuitos',
                          'Detectores de humo: prueba funcional con humo o producto listado (todos)',
                          'Detectores de temperatura restaurables probados (2 por circuito; identificación)',
                          'Interruptores de supervisión (70 kPa / 4,4 °C / 70 o 300 mm)', 'Aparatos de notificación audibles y visibles',
                          'Funciones de control de emergencia (NFPA 72, T. 14.4.3.2, ítem 24)', 'Baterías: reemplazo según fabricante',
                          'Alimentación primaria con carga máxima', 'Señales de falla de la central',
                          'Transmisión al servicio de monitoreo (DACT ≤ 90 s)', 'Avisadores manuales (todos)',
                          'Dispositivos electromecánicos de descarga (donde existan)', 'Interruptores de alarma de sistemas de extinción',
                          'Detectores de gas (según fabricante)', 'Aparatos de notificación audible textual']),
        ('INSPECCIONES COMPLEMENTARIAS (NFPA 72, TABLA 14.3.1)', [
                          'Trimestral: detectores de llama sin obstrucción del campo visual',
                          'Trimestral: dispositivos de señales de supervisión', 'Trimestral: sensores de flujo de agua',
                          'Semestral: baterías de níquel-cadmio y plomo-ácido selladas', 'Semestral: dispositivos iniciadores',
                          'Semestral: aparatos de notificación', 'Semestral: anunciadores remotos y supresores de transientes',
                          'Semestral: equipos de comunicación de emergencia por voz',
                          'Semestral: dispositivos electromecánicos de descarga e interruptores de extinción',
                          'Semestral: interfaz de funciones de control de emergencia', 'Semestral: aparatos de notificación audible textual',
                          'Anual: todos los equipos', 'Anual: fuentes remotas y extensiones de circuitos de notificación',
                          'Anual: transmisores al servicio de monitoreo', 'Anual: conexiones de fibra óptica',
                          'Anual: tubo de muestreo de detectores en ducto']),
    ]),
    dict(n=4, nombre='Mantenimiento anual', titulo='Mantenimiento anual – Sistema convencional de dos hilos', tipo='checklist', bloques=[
        ('MANTENIMIENTO ANUAL', ['Limpieza del panel de control de alarma de incendio', 'Limpieza de panel de audio para evacuación',
                                 'Calibración de detectores de humo y temperatura (8,3 %)', 'Calibración de detectores de gas (8,3 %)',
                                 'Verificación de valores indicados y reemplazo de detectores fuera de valores',
                                 'Limpieza y/o calibración de detectores (humo y/o temperatura y/o gas)',
                                 'Reemplazo de elementos de iniciación (según vida útil de fabricante)',
                                 'Modificación y/o reparación de la instalación (según planillas de registro)']),
        ('ENSAYOS DE LARGO PLAZO (NFPA 72)', [
                                 'Sensibilidad de detectores de humo: fecha de la última prueba / próxima',
                                 'Detectores fuera de rango: limpieza, recalibración o reemplazo',
                                 'Detectores de temperatura no restaurables a 15 años: reemplazo o ensayo de 2 de cada 100',
                                 'Zonas con aumento de falsas alarmas: prueba de calibración']),
    ]),
    dict(n=5, nombre='Información semanal (autocontrol)', titulo='Información semanal (autocontrol) – Sistema convencional de dos hilos',
         tipo='periodico', modo='semanal', bloques=[
        ('INSPECCIÓN SEMANAL – MES: ________  AÑO: ______', [
            'Detectores de humo, temperatura, gas y llama en buen estado', 'Pulsadores manuales sin obstrucciones',
            'Sirenas, alarmas acústicas y luces estroboscópicas en buen estado', 'Panel: LED / visor en condición normal',
            'Panel: fusibles, equipos interconectados y energía primaria', 'Panel: sin señales de falla',
            'Detectores sin obstrucción, sin pintura ni daños', 'Canalizaciones en buen estado, alineadas, sin cargas',
            'Eventos repetidos del mes en el panel', 'Barreras infrarrojas y sistema aspirador',
            'Alimentación primaria y secundaria presentes', 'Zonas con falla / zonas conectadas',
            'Indicación de nivel de tanque, flujo, baja presión y arranque de bomba',
            'Componentes incrustados y alineados', 'Planillas de eventos de la semana verificadas',
            'Manual instructivo en español disponible', 'Planos de la instalación disponibles']),
    ]),
])
'''
p = os.path.join(T, 'planillas_data2.py'); s = open(p, encoding='utf8').read()
a = s.index("SISTEMAS['SDI'] = "); b = s.index("SISTEMAS['SBC'] = ")
s = s[:a] + SDI + '\n' + s[b:]
open(p, 'w', encoding='utf8').write(s)

patch('planillas_data2.py', [
 # SBC-2
 ("            ('Tensión de baterías (bancos 1 y 2)', 'V'), 'Electrolito y terminales sin corrosión',",
  "            ('Tensión de baterías (bancos 1 y 2)', 'V'), ('Corriente de carga de baterías (bancos 1 y 2)', 'A'),\n"
  "            'Luces piloto de baterías encendidas o de falla apagadas', 'Electrolito y terminales sin corrosión',"),
 # SBC-3
 ("    dict(n=3, nombre='Inspección mensual', tipo='checklist', bloques=[\n        ('ANTES DE LA PUESTA EN MARCHA', [",
  "    dict(n=3, nombre='Inspección mensual', tipo='checklist', bloques=[\n"
  "        ('DATOS DE PLACA (MOTOBOMBA / ELECTROBOMBA / JOCKEY)', [\n"
  "            'Marca y año de fabricación', ('Caudal nominal', 'm³/h'), ('Altura manométrica', 'm H₂O'), ('Velocidad', 'vueltas/min'),\n"
  "            ('Presión máxima', 'MPa'), 'Motor: marca y potencia nominal']),\n"
  "        ('ANTES DE LA PUESTA EN MARCHA', ["),
 ("            ('Temperatura del agua de enfriamiento', '°C'), 'Nivel de combustible']),",
  "            ('Temperatura del agua de enfriamiento con precalentador', '°C'), 'Nivel de combustible',\n"
  "            'Nivel de aceite del cárter', 'Nivel de electrolito de baterías']),"),
 ("            'Diésel: presión de aceite, velocidad, temperaturas de aceite y agua', 'Ruidos o vibraciones inusuales',",
  "            ('Diésel: presión de agua de enfriamiento', 'MPa'), ('Diésel: presión de aceite del motor', 'MPa'),\n"
  "            ('Diésel: velocidad', 'vueltas/min'), ('Diésel: temperatura del agua de enfriamiento en funcionamiento', '°C'),\n"
  "            ('Diésel: temperatura del aceite', '°C'), 'Ruidos o vibraciones inusuales',"),
 ("        ('BOMBA JOCKEY', [('Presión de arranque', 'MPa'), ('Presión de parada', 'MPa'), ('Horas acumuladas de uso', 'h'),",
  "        ('BOMBA JOCKEY', [('Presión de arranque', 'MPa'), ('Presión de parada', 'MPa'), ('Horas acumuladas de uso', 'h'),\n"
  "                          ('Cantidad de arranques indicada en el panel', 'arranques'),"),
 # SBC-5
 ("        ('ANUAL – MOTOR DIÉSEL', ['Agua o material extraño en el tanque de combustible', 'Venteo de tanque y cañería de sobreflujo',",
  "        ('ANUAL – MOTOR DIÉSEL', ['Agua o material extraño en el tanque de combustible', 'Venteo de tanque y cañería de sobreflujo',\n"
  "                                  'Cañería de combustible',"),
 ("'Interruptores o fusibles (bienal)']),", "'Interruptores o fusibles (frecuencia «B», interpretada como bienal)']),"),
 # SBC-6
 ("        ('DATOS DE LA PRUEBA', ['Tipo de prueba: mangueras y boquillas / medidor de caudal', 'Manómetros de prueba calibrados (± 1 %)',",
  "        ('DATOS DE LA PRUEBA', ['Motivo: prueba anual / reemplazo de componente fundamental (NFPA 20, 14.5.2.1)',\n"
  "                                'Tablero de control: marca / listado', 'Fuente de abastecimiento', 'Impulsor', 'Supervisión',\n"
  "                                'Tipo de prueba: mangueras y boquillas / medidor de caudal', 'Manómetros de prueba calibrados (± 1 %)',"),
 ("                                    ('Diámetro y número de boquillas; coeficiente C', 'mm')]),",
  "                                    ('Diámetro y número de boquillas; coeficiente C', 'mm'), ('Presión del Pitot por boquilla', 'MPa')]),"),
 ("        ('CAUDAL MÁXIMO (150 %)', [('Caudal real', 'L/min'), ('Presión neta (≥ 65 % de la nominal)', 'MPa'), ('Tensión', 'V'),",
  "        ('CAUDAL MÁXIMO (150 %)', [('Caudal real', 'L/min'),\n"
  "                                   ('Presión de succión (≥ 0 bar con prevención de contraflujo, o mínima de diseño)', 'MPa'),\n"
  "                                   ('Presión de descarga', 'MPa'), ('Presión neta (≥ 65 % de la nominal)', 'MPa'),\n"
  "                                   ('Diámetro y número de boquillas; coeficiente C', 'mm'), ('Presión del Pitot por boquilla', 'MPa'),\n"
  "                                   ('Tensión', 'V'),"),
 # SAL-2 y SAL-3
 ("'Sin indicios de daños físicos en componentes', 'Cierre automático de aberturas con la descarga']),",
  "'Sin indicios de daños físicos en componentes', 'Cierre automático de aberturas con la descarga',\n"
  "                                'Desactivaciones del mes registradas (inicio, fin, causa, medidas)']),"),
 ("                   'Conexiones flexibles: estado; sustituir o probar las defectuosas']),\n    ]),",
  "                   'Conexiones flexibles: estado; sustituir o probar las defectuosas',\n"
  "                   'Detectores del recinto: prueba funcional anual', 'Supervisión de circuitos (circuito abierto)',\n"
  "                   'Alarmas, retardo y cierre de puertas, compuertas y ventilación',\n"
  "                   'Indicación en la alarma del edificio (NFPA 101, 9.8.2)',\n"
  "                   'Funciones de control (NFPA 72, T. 14.4.3.2, ítem 24)']),\n"
  "        ('POSTERIOR A UNA DESCARGA O ACTUACIÓN', ['Ausencia de personas en el recinto', 'Ventilación antes del reingreso',\n"
  "                   'Causa de la activación determinada', 'Reposición del agente con verificación de calidad (certificado)',\n"
  "                   'Rearme de cabezales y restitución del sistema']),\n    ]),"),
])
print('ok')
