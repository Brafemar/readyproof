# -*- coding: utf-8 -*-
"""Planillas e informes de los cinco capítulos agregados: SRA (7), STM (11), SAA (13), SHC (14) y SDC (18).
Una planilla SG-PEM-IFI por cada planilla de la IRAM 3546:2011, en el orden de sus letras."""
SN = ['SI', 'NO']
B = '[______]'
SISTEMAS = {}

ABAST = ('ABASTECIMIENTO DE AGUA (CAPÍTULO 13)', ['Última prueba de abastecimiento de agua (fecha)',
                                                  'Condición de depósitos y depósitos de presión', ('Capacidad', 'm³')])
BOMBAS = ('BOMBAS CONTRA INCENDIO (CAPÍTULO 12)', [('Tipo de bomba', ['Diésel', 'Eléctrica', 'Naftera', 'Ninguna']),
                                                   'Registro de la última inspección (fecha)', 'Cantidad',
                                                   ('Funcionan', SN)])
TIB = ('TOMA DE IMPULSIÓN PARA BOMBEROS', ['Localización', ('Cantidad', 'u'), ('Diámetro', 'mm'), 'Identificación'])
INST = lambda extra=(): ('INSTALACIÓN', ['Designación del sistema', '¿Cuál es el riesgo protegido?',
                                         ('No hay modificaciones del sistema, entorno o uso del área protegida', SN)] + list(extra))

# ------------------------------------------------------------------ SRA (cap. 7)
SISTEMAS['SRA'] = dict(nom='Sistema de Rociadores Automáticos', cap='7', planillas=[
    dict(n=1, nombre='Información general', tipo='general', bloques=[
        INST([('Localización de la válvula de rociadores', ''), ('Tipo de sistema', ['Húmedo', 'Seco', 'Diluvio', 'Acción previa']),
              'Marca y modelo de los rociadores', ('Cantidad de rociadores', 'u'), ('Faltantes', SN), ('Sistema en servicio', SN)]),
        ('VÁLVULAS', [('Control de las válvulas', ['Precintadas', 'Enclavadas', 'Supervisadas']), ('Cantidad', 'u'), 'Tipo',
                      ('Diámetro', 'mm')]),
        ABAST, BOMBAS, TIB,
        ('SISTEMA HÚMEDO', ['Peligro de congelamiento', ('Memoria de cálculo del sistema hidráulico', SN),
                            ('Los datos hidráulicos figuran cerca de la válvula', SN), ('Anticongelante', SN)]),
        ('SISTEMA SECO', [('Válvula de alarma protegida', SN), ('Cantidad', 'u'), ('Diámetro', 'mm'),
                          ('Gas de presurización', ['Aire', 'Nitrógeno'])]),
        ('SISTEMA DE DILUVIO Y DE ACCIÓN PREVIA', [('Posee sistema de detección (ver SG-PEM-IFI-SDI)', SN),
                                                   'Si no posee detección, verificación directa']),
        ('ROCIADORES DE REPUESTO', [('Cantidad en el gabinete', 'u'), ('Llave por cada tipo', SN),
                                    ('Lista de rociadores en el gabinete (NFPA 25, 5.4.1.6.6)', SN)]),
    ]),
    dict(n=2, nombre='Inspección semanal (autocontrol)', tipo='periodico', modo='semanal', bloques=[
        ('INSPECCIÓN SEMANAL', ['Válvulas de control precintadas y abiertas', 'Válvulas del abastecimiento abiertas',
                                'Rociadores sin daños, sin pintura ni bloqueo', 'Distancia libre bajo rociadores 0,46 m',
                                ('Presión de agua', 'kPa'), ('Presión de aire', 'kPa'), ('Variación respecto de la normal', '%'),
                                'Válvula de tubería seca: dispositivos en posición, sin fugas']),
        ('INSPECCIÓN DIARIA EN HELADAS (TUBERÍA SECA)', ['Temperatura del local de la válvula > 5 °C (registrar)',
                                                          'Alarma de baja temperatura operativa (si existe)']),
    ]),
    dict(n=3, nombre='Inspección mensual', tipo='periodico', bloques=[
        ('INSPECCIÓN MENSUAL', ['Toma de impulsión para bomberos accesible, tapas y tapones', 'Válvulas enclavadas o supervisadas abiertas',
                                'Válvulas del abastecimiento abiertas', 'Válvulas de alarma sin fugas a cámara de retardo o drenaje',
                                'Repuestos: cantidad, tipo, 2 por tipo y llave', 'Tuberías sin daños físicos',
                                'Dispositivos de alarma y conexiones eléctricas', ('Presiones', 'kPa'),
                                'Cartel de cálculo hidráulico legible',
                                'Válvulas seca/acción previa/diluvio: exterior, trim, asiento (NFPA 25)']),
        ('MANTENIMIENTO MENSUAL', ['Áreas de pintura pulverizada: rociadores sin depósitos; bolsas ≤ 0,076 mm']),
    ]),
    dict(n=4, nombre='Inspección y pruebas trimestrales', tipo='checklist', bloques=[
        ('PRUEBA DE DRENAJE', [('Presión estática (manómetro inferior)', 'kPa'), ('Presión residual con drenaje abierto', 'kPa'),
                               ('Caída respecto de la prueba anterior (≤ 10 %)', '%'), 'Drenaje cerrado lentamente']),
        ('ALARMAS', ['Nivel de cebado de la válvula de tubería seca', ('Alarma de baja presión de aire (presión de actuación)', 'kPa'),
                     ('Alarma de flujo de tubería húmeda: interruptor ≤ 90 s', 's'), ('Campana hidráulica ≤ 5 min', 's'),
                     'Alarma de flujo de tubería seca (bypass)', 'Alarma de flujo de acción previa (bypass)',
                     'Alarma de flujo de diluvio (bypass)', 'Dispositivo de apertura rápida (NFPA 25, 13.4.5.2.4)',
                     'Acción previa: alarmas de presión de aire y solenoide (NFPA 25)']),
        ('VÁLVULAS Y CARTEL', ['Válvulas de corte: abiertas al tope y ¼ de vuelta atrás', 'Placa de datos hidráulicos']),
        ('MANTENIMIENTO TRIMESTRAL', ['Válvulas de poste indicador y OS&Y: recorrido completo y enclavamiento']),
    ]),
    dict(n=5, nombre='Inspección y pruebas semestrales', tipo='checklist', bloques=[
        ('PRUEBAS SEMESTRALES', ['Sistema de tubería seca: buen funcionamiento', 'Sistema de diluvio: detección (ver SG-PEM-IFI-SDI)',
                                 'Sistema de acción previa: detección (ver SG-PEM-IFI-SDI)',
                                 'Interruptores de supervisión: señal en 2 vueltas o 1/5 del recorrido',
                                 ('Concentración de nitrógeno ≥ 98 % (si se usa)', '%')]),
    ]),
    dict(n=6, nombre='Pruebas y mantenimiento anual', tipo='checklist', bloques=[
        ('CONDICIONES GENERALES', ['Rociadores, tuberías, soportes y sujeciones en buen estado',
                                   'Rociadores sin fuga, corrosión, daño, pérdida de líquido, carga ni pintura',
                                   'Antes de heladas: aberturas que no exponen tuberías', 'Condiciones de obstrucción de la red (lista)']),
        ('VÁLVULAS Y FILTROS', ['Válvulas operadas en su recorrido y lubricadas', 'Filtros verificados y limpios']),
        ('ANTICONGELANTE', [('Punto de solidificación', '°C'), 'Muestras arriba, abajo y punto remoto', 'Solución listada / permitida']),
        ('SISTEMA DE TUBERÍA SECA', ['Disparo de la válvula con corte parcialmente abierto', ('Tiempo hasta el disparo', 's'),
                                     ('Presión de aire de disparo', 'kPa'), 'Inspección y limpieza interna de la válvula',
                                     ('Abastecimiento de aire: restitución ≤ 30 min', 'min'), 'Alarmas de presión de aire y baja temperatura',
                                     'Tarjeta de disparo colocada']),
        ('SISTEMA DE ACCIÓN PREVIA', ['Disparo del sistema (automático y manual)', 'Inspección interna de la válvula']),
        ('SISTEMA DE DILUVIO', ['Disparo del sistema', ('Tiempo desde el iniciador hasta la descarga', 's'),
                                ('Presión en el rociador hidráulicamente más desfavorable', 'kPa'), 'Descarga y cobertura correctas',
                                ('Presión en la válvula de diluvio', 'kPa'), 'Inspección interna de la válvula']),
        ('MANTENIMIENTO ANUAL', ['Puntos bajos de drenaje (tubería seca)', 'Rociadores en cocinas: sustitución de eslabón fusible']),
    ]),
    dict(n=7, nombre='Pruebas de tres años', tipo='checklist', bloques=[
        ('DISPARO A CAUDAL TOTAL', ['Disparo de la válvula de tubería seca con corte totalmente abierto',
                                    ('Tiempo entre la apertura y la salida de agua', 's'), 'Agua limpia por la conexión de prueba',
                                    'Disparo a caudal total de la válvula de acción previa']),
        ('PÉRDIDA DE AIRE', [('Presión inicial (2,8 bar)', 'bar'), ('Pérdida en 2 h (≤ 0,2 bar)', 'bar')]),
    ]),
    dict(n=8, nombre='Mantenimiento quinquenal', tipo='checklist', bloques=[
        ('INSPECCIÓN INTERNA DE VÁLVULAS', ['Válvula de alarma: componentes operan, se mueven libremente, buen estado',
                                            'Válvula de retención: componentes operan, se mueven libremente, buen estado',
                                            'Filtros, orificios y cámaras de diafragma (seca, acción previa, diluvio)']),
        ('TOMA DE IMPULSIÓN', [('Prueba hidrostática a 10 bar, 2 h: pérdida < 0,3 bar', 'bar')]),
    ]),
    dict(n=9, nombre='Pruebas de cinco, veinte y cincuenta años', tipo='checklist', bloques=[
        ('CADA 5 AÑOS', ['Limpieza a caudal pleno de tuberías', 'Calibrado de manómetros (≤ 3 %)',
                         'Muestra de rociadores de temperatura extra alta (≥ 163 °C)', 'Evaluación interna de la red (NFPA 25, 14.2)',
                         'Rociadores en ambientes agresivos']),
        ('CADA 10 AÑOS DESDE LOS 20 AÑOS', ['Muestra de rociadores de respuesta rápida', 'Rociadores secos']),
        ('50 AÑOS Y CADA 10 AÑOS (CADA 5 DESDE LOS 75)', ['Muestra de rociadores de respuesta estándar',
                                                           ('Año de instalación de los rociadores', '')]),
    ]),
])

# ------------------------------------------------------------------ STM (cap. 11)
SISTEMAS['STM'] = dict(nom='Sistema de Tuberías y Mangueras', cap='11', planillas=[
    dict(n=1, nombre='Información general', tipo='general', bloques=[
        INST([('Cantidad de válvulas en servicio', 'u')]),
        ('MANGUERAS', [('Largo de manguera', ['Ninguna', '15 m', '20 m', '25 m']),
                       ('Tipo de manguera', ['Sintética', 'Profesional', 'Lino', 'Goma', 'Otras']), ('Diámetro', 'mm'),
                       ('Boquillas chorro niebla', SN)]),
        ('DISPOSITIVOS REGULADORES DE PRESIÓN', [('Se dispone de reguladores', SN),
                                                 ('Tipo', ['A resorte', 'Con piloto', 'Presión diferencial', 'Tanque ruptor'])]),
        ('VÁLVULAS INTERCEPTORAS', [('Control de las válvulas', ['Precintadas', 'Enclavadas', 'Supervisadas']), ('Cantidad', 'u'),
                                    'Tipo', ('Diámetro', 'mm')]),
        ('VÁLVULAS DE INCENDIO', [('Tipo teatro: cantidad', 'u'), ('Diámetro', 'mm'), ('Hidrantes', ['Húmedos', 'Secos']),
                                  ('Cantidad de hidrantes', 'u')]),
        ABAST, BOMBAS, TIB,
    ]),
    dict(n=2, nombre='Inspección semanal (autocontrol)', tipo='periodico', modo='semanal', bloques=[
        ('INSPECCIÓN SEMANAL', ['Válvulas interceptoras: modo preventivo (precintada, enclavada, supervisada)',
                                'Válvula para manga: volante, rosca sana, sin fugas, tapa', 'Válvula precintada',
                                'Reguladores: válvulas de servicio abiertas, manómetros legibles, piloto']),
    ]),
    dict(n=3, nombre='Inspección mensual', tipo='periodico', bloques=[
        ('INSPECCIÓN MENSUAL', ['Manguera sin daños, con unión y lanza colocadas', 'BIE señalizadas',
                                'Conexión para bomberos sin obstrucciones', 'Señalización', 'Modo preventivo de la válvula interceptora',
                                'Abastecimiento de agua según SG-PEM-IFI-SAA', 'Bomba contra incendio completa y en condiciones',
                                'Bocas sin equipamiento: tapas, volantes y armario con listado']),
    ]),
    dict(n=4, nombre='Inspección mensual de válvulas para mangas', tipo='checklist', bloques=[
        ('VÁLVULA', ['Tapa', 'Volante', 'Tuerca del volante', 'Llave de ajuste de uniones']),
        ('LANZA', ['Junta', 'Boquilla', 'Opera suavemente y sin obstrucciones']),
        ('GABINETE', ['Vidrio', 'Cerradura', 'Bisagras', 'Puerta (abre totalmente)', 'Pintura', 'Identificación',
                      'Devanadera o soporte (gira ≥ 90°)']),
        ('MANGUERA', ['Humedad / moho', 'Estado de las uniones', 'Junta', ('Tipo (sintética / lino)', ''), ('Diámetro', 'mm'),
                      ('Longitud', 'm'), 'Prueba hidrostática vigente (IRAM 3594)']),
        ('ESTADO', ['Boca completa (V° B°)', ('Número de boca', '')]),
    ]),
    dict(n=5, nombre='Prueba mensual y trimestral', tipo='checklist', bloques=[
        ('PRUEBA MENSUAL', [('Presión hidrostática en bocas tras descargar 15 L', 'kPa'), ('Bocas controladas en el mes', 'u'),
                            'Arranque de bombas con el 5 % de las bocas abiertas',
                            'Presión ≤ 6,9 bar residual (40 mm) y ≤ 12 bar en conexiones (NFPA 14)']),
        ('PRUEBA TRIMESTRAL', ['Válvulas interceptoras en el modo preestablecido', 'Válvulas profesionales: tapas y roscas',
                               ('Alarmas de flujo: tiempo de actuación', 's'), 'Toma de impulsión operada, tapas y anilla giratoria',
                               'Arranque de bombas con el 10 % de las bocas abiertas', 'Válvulas reductoras: abiertas, sin pérdidas']),
    ]),
    dict(n=6, nombre='Prueba hidrostática y de caudal de tuberías', tipo='checklist', bloques=[
        ('PRUEBA HIDROSTÁTICA A RED DE TUBERÍAS', [('Presión inicial de la prueba (≥ 13,8 bar o máx. + 3,4 bar)', 'bar'),
                                                   ('Hora de comienzo', 'h'), ('Presión al final de la prueba', 'bar'),
                                                   ('Hora final (≥ 2 h)', 'h'), ('Caída de presión (≤ 0,3 bar)', 'bar'),
                                                   'Sin pérdidas visibles', 'Sistema drenado (tuberías secas)']),
        ('PRUEBA DE CAUDAL (SALIDA MÁS DESFAVORABLE)', [('Presión estática', 'kPa'), ('Diámetro de boquilla', 'mm'),
                                                        ('Caudal bombeado', 'L/min'), ('Presión manométrica residual', 'kPa'),
                                                        ('Presión en piloto', 'kPa')]),
    ]),
    dict(n=7, nombre='Inspección anual y mantenimiento semestral, anual y bienal', tipo='checklist', bloques=[
        ('INSPECCIÓN ANUAL', ['Tuberías sin daños ni corrosión', 'Soportes y sujeciones', 'Cartel de cálculo hidráulico']),
        ('MANTENIMIENTO SEMESTRAL', ['Mangueras retiradas y reenrolladas (IRAM 3594)', 'Juntas de las uniones',
                                     'Racores y devanaderas engrasados con grafito']),
        ('MANTENIMIENTO ANUAL', ['Tuberías accesibles sin daños ni corrosión', 'Boquillas abren y cierran con facilidad',
                                 'Racores lubricados', 'Mangueras desconectadas y reenrolladas; juntas']),
        ('MANTENIMIENTO BIENAL', ['Recorrido de todas las válvulas tipo teatro (obturadores de goma)']),
    ]),
    dict(n=8, nombre='Prueba anual, bienal y quinquenal', tipo='checklist', bloques=[
        ('PRUEBA ANUAL', ['Bombas contra incendio (SG-PEM-IFI-SBC)', ('Ensayo de presión y alcance por boca', 'kPa'),
                          'Boquillas pasan de chorro a niebla', ('Prueba de pérdidas de tuberías secas a 1,7 MPa, 2 h', 'MPa'),
                          ('Caudal en la salida más desfavorable (≥ 500 L/min a 450 kPa)', 'L/min'),
                          'Reguladores de presión a caudal total (hoja adjunta)', 'Válvulas clase I y III abiertas y cerradas']),
        ('PRUEBA BIENAL', ['Prueba hidráulica de mangueras (IRAM 3594)']),
        ('PRUEBA QUINQUENAL', ['Prueba hidrostática de tuberías secas (SG-PEM-IFI-STM-6)', ('Prueba con aire de sistemas reparados', 'bar'),
                               ('Flujo en salida más desfavorable (500 / 300 L/min a 450 kPa o demanda NFPA 14)', 'L/min'),
                               'Válvula reguladora de presión con flujo', ('Lanzas probadas a 1,7 MPa', 'MPa')]),
    ]),
])

# ------------------------------------------------------------------ SAA (cap. 13)
SISTEMAS['SAA'] = dict(nom='Sistema de Abastecimiento de Agua', cap='13', planillas=[
    dict(n=1, nombre='Información general', tipo='general', bloques=[
        INST([('Cuenta con los instructivos de operación', SN)]),
        ('ABASTECIMIENTO DE AGUA', ['Última prueba de abastecimiento de agua (fecha)', 'Condición de depósitos y depósitos de presión',
                                    ('Capacidad', 'm³'), 'Material', 'Tipo', ('Elevado', 'm'),
                                    ('Ubicación', ['A superficie', 'Enterrado', 'Nivel']),
                                    ('Dispositivo de alarma de alto o bajo nivel', SN), 'Registro de alarmas',
                                    ('Control de nivel vinculado a la detección (SG-PEM-IFI-SDI)', SN)]),
        BOMBAS, TIB,
    ]),
    dict(n=2, nombre='Inspección semanal', tipo='periodico', modo='semanal', bloques=[
        ('INSPECCIÓN SEMANAL', [('Temperatura del agua (≥ 4 °C)', '°C'), 'Sistema de calentamiento',
                                'Válvulas de control precintadas y en posición']),
        ('INSPECCIÓN DIARIA EN ESTACIÓN FRÍA', ['Temperatura del agua registrada a diario', 'Calefacción en funcionamiento']),
    ]),
    dict(n=3, nombre='Inspección y prueba mensual', tipo='periodico', bloques=[
        ('INSPECCIÓN Y PRUEBA MENSUAL', ['Condición del agua', 'Nivel de agua (indicador)', 'Válvulas de control',
                                         ('Presión de aire en tanque hidroneumático', 'kPa'),
                                         'Prueba de alarmas de baja temperatura (*)',
                                         'Prueba de interruptores de límite de alta temperatura (*)',
                                         '(*) Tanques sujetos a congelamiento con calefacción']),
    ]),
    dict(n=4, nombre='Inspección trimestral y anual', tipo='checklist', bloques=[
        ('INSPECCIÓN TRIMESTRAL', ['Exterior del tanque', 'Estructura soporte', 'Pasarelas y escaleras de mano',
                                   'Áreas circundantes libres de combustibles y hielo', 'Endicados sin erosión (tela revestida)']),
        ('PRUEBA SEMESTRAL', ['Alarma de nivel alto', 'Alarma de nivel bajo']),
        ('INSPECCIÓN Y PRUEBA ANUAL', ['Superficies pintadas o protegidas', 'Juntas de expansión', 'Zunchos (tanques de madera)',
                                       ('Manómetros: error (≤ 3 % de la escala)', '%'), ('Válvula de llenado: caudal de llenado', 'L/min'),
                                       'Calefacción probada antes de la estación fría']),
    ]),
    dict(n=5, nombre='Mantenimiento', tipo='checklist', bloques=[
        ('MANTENIMIENTO', ['Nivel de agua de diseño', 'Termostato', 'Drenaje de sedimentos (semestral)', 'Válvulas de drenaje',
                           'Protección catódica (anual)', 'Mallas de venteos (anual)', 'Válvulas de control',
                           'Estructuras de acero / repintado', 'Válvulas de retención (inspección y mantenimiento cada 5 años)',
                           'Filtros de válvulas de llenado (trimestral)', 'Tanques de tela revestida en endicados (bienal)',
                           'Fosos y casetas ≥ 4 °C', 'Tapas del techo trabadas']),
    ]),
    dict(n=6, nombre='Pruebas quinquenales', tipo='checklist', bloques=[
        ('PRUEBAS QUINQUENALES', ['Interior del tanque en condiciones (*)', 'Válvulas de retención en condiciones',
                                  'Prueba del indicador de nivel (exactitud y movimiento)', 'Prueba de los manómetros',
                                  '(*) Tanques de acero sin protección y tanques a presión: cada 3 años']),
        ('ENSAYOS DE LA INSPECCIÓN INTERIOR (ACERO)', ['Adherencia ASTM D3359', ('Espesor de película seca', 'µm'),
                                                       ('Espesor de pared por ultrasonido', 'mm'), 'Esponja húmeda',
                                                       'Fondo por ultrasonido', 'Costuras del fondo con caja de vacío']),
    ]),
])

# ------------------------------------------------------------------ SHC (cap. 14)
SISTEMAS['SHC'] = dict(nom='Sistema de Hidrantes Contra Incendios', cap='14', planillas=[
    dict(n=1, nombre='Información general', tipo='general', bloques=[
        INST([('Cuenta con los instructivos de operación', SN)]),
        ('TIPO DE HIDRANTES', [('Tipo', ['Columna con agua', 'Columna seca']), ('Cantidad de hidrantes', 'u')]),
        ('BOCAS DE SALIDA POR HIDRANTE', [('Diámetro', 'mm'), ('Cantidad', 'u'), 'Rosca']),
        ('VÁLVULAS INTERCEPTORAS', [('Diámetro', 'mm'), ('Cantidad', 'u'), 'Tipo']),
        ('ACCESORIOS', [('Tapa', SN), ('Junta', SN), ('Cadena', SN), ('Tuercas de apertura en buen estado', SN)]),
        ('ARMARIOS', [('Cantidad', 'u'), ('Estado', ['Completos', 'Incompletos']), ('Señalización', SN),
                      ('Accesorios compatibles con la instalación', SN),
                      ('Distribución', ['Solo en ingreso', 'En planta', 'Intemperie'])]),
        BOMBAS,
    ]),
    dict(n=2, nombre='Inspección y pruebas de hidrantes', tipo='checklist', bloques=[
        ('IDENTIFICACIÓN DEL PUESTO', [('Puesto N°', ''), ('Numeración en armario', ''), 'Ubicación']),
        ('MENSUAL – ARMARIO', ['Libre', 'Señalización', 'Limpieza', 'Gabinete', 'Puerta', 'Vidrio']),
        ('MENSUAL – VÁLVULA Y MANGA', [('Diámetro', 'mm'), 'Tipo de salida', 'Volante / tuerca', ('Largo de manga', 'm'),
                                       'Última prueba hidrostática (IRAM 3594)', 'Lanza / boquilla', 'Llave de ajuste de unión',
                                       'Sin fugas ni ingreso de agua por el drenaje']),
        ('TRIMESTRAL', [('Presión estática', 'kPa'), 'Verificación de roscas (IRAM 3508)', 'Accionamiento de la válvula',
                        'Verificación de fugas (salidas y cuerpo)', 'Drenaje']),
        ('ANUAL', ['Apertura total y flujo ≥ 1 min', ('Drenaje de columna seca (≤ 60 min)', 'min'), 'Lubricación de empaquetaduras',
                   ('Caudal del hidrante más desfavorable', 'L/min'), ('Presión residual en hidrante próximo', 'kPa'),
                   'Lubricación de tuerca, vástagos, tapas y roscas', 'Junta de la tapa', 'Monitores: oscilación y lubricación']),
    ]),
    dict(n=3, nombre='Inspección semestral (columna seca) y anual (columna con agua)', tipo='checklist', bloques=[
        ('INSPECCIÓN', ['Hidrantes accesibles', 'Salidas y tapas ajustadas, con cadena', 'Estanqueidad del cuerpo',
                        'Sin grietas en el cuerpo', 'Drenaje correcto / sin agua ni hielo en la columna',
                        'Tuerca de apertura en buen estado y llave disponible', 'Roscas de las boquillas en buen estado',
                        'Armarios de mangueras con equipo completo']),
        ('RED (NFPA 25, CAPÍTULO 7)', ['Cañerías a la vista: pérdidas, daños, corrosión, anclajes', 'Filtros principales (anual)',
                                       'Monitores (semestral)', ('Prueba de flujo de la red (cada 5 años)', 'L/min')]),
    ]),
])

# ------------------------------------------------------------------ SDC (cap. 18)
SISTEMAS['SDC'] = dict(nom='Sistema de Extinción por Dióxido de Carbono', cap='18', planillas=[
    dict(n=1, nombre='Información general', tipo='general', bloques=[
        INST([('Fecha de instalación del sistema', '')]),
        ('VOLUMEN PROTEGIDO', [('Volumen', ['Ambiente', 'Falso techo', 'Falso piso', 'Otros']),
                               ('Concentración', ['34 %', '50 %', '66 %', 'Otra']), ('Tipo de sistema', ['Alta presión', 'Baja presión']),
                               ('Cantidad de cilindros (alta presión)', 'u'), ('Capacidad del cilindro', 'kg'),
                               ('Capacidad del sistema de baja presión', 'kg')]),
        ('ACTIVACIÓN DEL SISTEMA', [('Activación', ['Automático', 'Manual local', 'Manual remoto']),
                                    ('Válvula de bloqueo instalada y supervisada (NFPA 12)', SN)]),
        ('ALARMAS', [('Acústica neumática: cantidad', 'u'), ('Acústica eléctrica: cantidad', 'u'),
                     ('Visual estroboscópica: cantidad', 'u'), ('Visual rotativa: cantidad', 'u'), ('Retardo de predescarga', 's')]),
        ('SEÑALIZACIÓN', [('Carteles de advertencia en recinto, ingresos y accionadores (NFPA 12, 4.3.2)', SN)]),
    ]),
    dict(n=2, nombre='Inspección mensual', tipo='checklist', bloques=[
        ('INSPECCIÓN MENSUAL', ['Boquillas sin daños ni obstrucciones', 'Cierre automático de aberturas con la descarga',
                                'Sin cambios en el tamaño o tipo de riesgo', ('Peso en depósito de baja presión (pérdida ≤ 10 %)', '%'),
                                ('Presión en depósito de baja presión (2,1 MPa ± 3 %)', 'MPa'), 'Pérdidas o daños visibles',
                                'Energía presente en el equipo de refrigeración', ('Cilindros piloto de nitrógeno (≥ 90 %)', '%'),
                                'Válvula de bloqueo en posición normal', 'Carteles de advertencia']),
        ('NIVEL DE LÍQUIDO EN BAJA PRESIÓN (SEMANAL, NFPA 12, 4.8.3.6)', [('Semana 1', '%'), ('Semana 2', '%'), ('Semana 3', '%'),
                                                                          ('Semana 4', '%'), ('Semana 5', '%')]),
    ]),
    dict(n=3, nombre='Prueba y mantenimiento anual', tipo='checklist', bloques=[
        ('SEGURIDAD PREVIA', ['Recinto evacuado y válvula de bloqueo cerrada', 'Cabezales de control desconectados',
                              'Procedimientos de seguridad revisados (NFPA 12, 4.8.3.2.3)']),
        ('PRUEBA Y MANTENIMIENTO ANUAL', ['Indicios de fuga en los cilindros', 'Indicios de daños físicos en los componentes',
                                          ('Presión en cilindros piloto de nitrógeno (≥ 90 %)', '%'), 'Accionamiento de válvula direccional',
                                          'Peso de cilindros: pérdida > 10 % requiere recarga (SG-PEM-IFI-SDC-4)',
                                          'Etiqueta con el peso del cilindro completo', 'Funcionamiento del cabezal de disparo',
                                          'Prueba en blanco del sistema', 'Soplado de las líneas de descarga',
                                          'Actuación de alarma acústica y visual del espacio protegido',
                                          'Sistema de refrigeración según el fabricante']),
        ('VERIFICACIONES NFPA 12 (4.8.3.2 Y 4.5.6)', [('Retardo de predescarga', 's'), ('Nivel sonoro a 3 m (≥ 90 dBA)', 'dBA'),
                                                      'Alarmas distintas de la alarma del edificio', 'Alarmas exteriores en ingresos',
                                                      'Detectores probados según NFPA 72', 'Penetraciones del recinto selladas',
                                                      'Informe con recomendaciones entregado al propietario']),
    ]),
    dict(n=4, nombre='Control de peso de cilindros', tipo='checklist', bloques=[
        ('CILINDRO N° %d' % i, [('Capacidad', 'L'), ('Última prueba hidrostática (mes/año)', ''), ('Peso vacío grabado', 'kg'),
                                ('Peso leído', 'kg'), ('Carga neta (≥ 90 % de la nominal)', 'kg')]) for i in range(1, 13)
    ]),
    dict(n=5, nombre='Prueba quinquenal', tipo='checklist', bloques=[
        ('PRUEBA QUINQUENAL', ['Fecha de la última prueba general del sistema', 'Prueba en blanco previa del sistema',
                               ('Prueba hidrostática de flexibles (17,5 MPa alta / 6,3 MPa baja)', 'MPa'),
                               'Flexibles secados (≤ 66 °C) y marcados con la fecha',
                               'Prueba hidrostática de cilindros IRAM 2529 (parte I) – registrar en SG-PEM-IFI-SDC-4',
                               'Prueba neumática de la red de cañerías', 'Panel, cabezales y válvulas de descarga']),
    ]),
])

INFORMES = {
'SRA': dict(
    equipo=('Sistema:', 'Marca de rociadores:', 'Modelo:'),
    ident=[('Tipo de sistema:', '[HÚMEDO / SECO / ACCIÓN PREVIA / DILUVIO]'), ('Cantidad de rociadores:', '[______]'),
           ('Rociadores de repuesto:', '[______]'), ('Abastecimiento:', '[RED / TANQUE / BOMBA]'),
           ('Toma de impulsión para bomberos:', '[SI / NO]'), ('Riesgo protegido:', '')],
    alcance='válvulas de control, puesto de control, red de cañerías y soportes, rociadores y repuestos, dispositivos de alarma, '
            'abastecimiento de aire y toma de impulsión para bomberos',
    resultados=[
        ('RESULTADOS GENERALES', ['Se verificaron %s ítems de las planillas aplicables, de los cuales %s resultaron conformes, lo que '
                                  'representa un [______ %%] del total evaluado.' % (B, B)]),
        ('PRUEBA DE DRENAJE', ['La presión estática fue de [______ kPa] y la residual de [______ kPa], con una variación de '
                               '[______ %] respecto de la prueba anterior, valor [≤ / >] 10 %.']),
        ('ALARMAS', ['La alarma de flujo actuó en [______ s] y la campana hidráulica en [______ s], valores [CONFORMES / NO CONFORMES].']),
        ('DISPARO DE VÁLVULAS', ['La válvula de [TUBERÍA SECA / ACCIÓN PREVIA / DILUVIO] se disparó en [______ s] con una presión de '
                                 'aire de [______ kPa]; el agua llegó a la conexión de prueba en [______ s].']),
        ('ROCIADORES', ['Se detectaron [______] rociadores a reemplazar por corrosión, carga, pintura o daño.']),
    ],
    criterios=['Ítems conformes: [______ %]', 'Distancia libre bajo rociadores: [CONFORME / NO CONFORME]',
               'Fallas críticas: [______]']),
'STM': dict(
    equipo=('Sistema:', 'Marca de válvulas:', 'Modelo:'),
    ident=[('Bocas de incendio:', '[______] de DN 44,5 mm – [______] de DN 63,5 mm'), ('Tipo de red:', '[HÚMEDA / SECA]'),
           ('Reguladores de presión:', '[SI / NO]'), ('Abastecimiento:', '[RED / TANQUE / BOMBA]'),
           ('Toma de impulsión para bomberos:', '[SI / NO]'), ('Riesgo protegido:', '')],
    alcance='válvulas interceptoras, válvulas para mangas, bocas de incendio equipadas, mangueras y lanzas, reguladores de presión, '
            'red de tuberías y toma de impulsión para bomberos',
    resultados=[
        ('RESULTADOS GENERALES', ['Se verificaron %s ítems de las planillas aplicables, de los cuales %s resultaron conformes, lo que '
                                  'representa un [______ %%] del total evaluado.' % (B, B)]),
        ('BOCAS DE INCENDIO', ['Se inspeccionaron [______] bocas; [______] presentaron faltantes o deterioros.']),
        ('PRUEBAS DE PRESIÓN Y CAUDAL', ['En la boca más desfavorable se midió un caudal de [______ L/min] con una presión residual de '
                                         '[______ kPa], valor [CONFORME / NO CONFORME].']),
        ('PRUEBA HIDROSTÁTICA', ['La red seca se probó a [______ bar] durante [______ h] con una caída de [______ bar].']),
        ('MANGUERAS', ['[______] mangueras tienen la prueba hidrostática vigente según la IRAM 3594.']),
    ],
    criterios=['Ítems conformes: [______ %]', 'Presión y caudal en la boca más desfavorable: [CONFORME / NO CONFORME]',
               'Fallas críticas: [______]']),
'SAA': dict(
    equipo=('Tanque:', 'Material:', 'Tipo:'),
    ident=[('Capacidad:', '[______ m³]'), ('Ubicación:', '[ELEVADO / A NIVEL / ENTERRADO]'), ('Alarmas de nivel:', '[SI / NO]'),
           ('Calefacción:', '[SI / NO]'), ('Tanque a presión:', '[SI / NO]'), ('Sistemas abastecidos:', '')],
    alcance='tanque, estructura soporte, indicadores y alarmas de nivel, calefacción, válvulas de control, retención, drenaje y '
            'llenado, venteos y protección contra la corrosión',
    resultados=[
        ('RESULTADOS GENERALES', ['Se verificaron %s ítems de las planillas aplicables, de los cuales %s resultaron conformes, lo que '
                                  'representa un [______ %%] del total evaluado.' % (B, B)]),
        ('NIVEL Y TEMPERATURA', ['El tanque se encontró [LLENO / POR DEBAJO DEL NIVEL DE DISEÑO] y la temperatura mínima registrada '
                                 'del agua fue de [______ °C].']),
        ('ALARMAS', ['Las alarmas de nivel alto y bajo resultaron [OPERATIVAS / CON FALLAS].']),
        ('INSPECCIÓN INTERIOR', ['La última inspección interior se realizó el [______] con resultado [CONFORME / CON DEFICIENCIAS].']),
    ],
    criterios=['Ítems conformes: [______ %]', 'Volumen disponible: [CONFORME / NO CONFORME]', 'Fallas críticas: [______]']),
'SHC': dict(
    equipo=('Red de hidrantes:', 'Marca:', 'Modelo:'),
    ident=[('Tipo de hidrantes:', '[COLUMNA CON AGUA / COLUMNA SECA]'), ('Cantidad de hidrantes:', '[______]'),
           ('Armarios de mangueras:', '[______]'), ('Abastecimiento:', '[RED / TANQUE / BOMBA]'), ('Riesgo protegido:', '')],
    alcance='hidrantes, armarios de mangueras y su equipamiento, válvulas interceptoras, red exterior, filtros principales y monitores',
    resultados=[
        ('RESULTADOS GENERALES', ['Se verificaron %s ítems de las planillas aplicables, de los cuales %s resultaron conformes, lo que '
                                  'representa un [______ %%] del total evaluado.' % (B, B)]),
        ('PRUEBA DE FLUJO', ['El hidrante más desfavorable entregó [______ L/min] con una presión residual de [______ kPa].']),
        ('DRENAJE', ['[______] hidrantes de columna seca no drenaron dentro de los 60 min.']),
        ('ARMARIOS', ['[______] armarios se encontraron incompletos.']),
    ],
    criterios=['Ítems conformes: [______ %]', 'Caudal del hidrante más desfavorable: [CONFORME / NO CONFORME]',
               'Fallas críticas: [______]']),
'SDC': dict(
    equipo=('Sistema:', 'Marca:', 'Modelo:'),
    ident=[('Tipo de sistema:', '[ALTA PRESIÓN / BAJA PRESIÓN]'), ('Concentración de diseño:', '[______ %]'),
           ('Cantidad y capacidad de cilindros:', '[______] – [______ kg]'), ('Volumen protegido:', '[AMBIENTE / FALSO SUELO / FALSO TECHO]'),
           ('Válvula de bloqueo:', '[SI / NO]'), ('Fecha de instalación:', '')],
    alcance='cilindros o depósito de CO₂, cabezales de control, cilindros piloto, conexiones flexibles, válvulas direccionales y de '
            'bloqueo, red de cañerías y boquillas, detección, panel de control, alarmas, retardos, carteles y cierre del recinto',
    resultados=[
        ('RESULTADOS GENERALES', ['Se verificaron %s ítems de las planillas aplicables, de los cuales %s resultaron conformes, lo que '
                                  'representa un [______ %%] del total evaluado.' % (B, B)]),
        ('CARGA DE AGENTE', ['Se pesaron [______] cilindros; [______] presentaron una pérdida de carga neta mayor que el 10 %.']),
        ('PRUEBA EN BLANCO', ['La secuencia de detección, alarma, retardo de [______ s] y disparo resultó [CORRECTA / CON FALLAS].']),
        ('SEGURIDAD DEL PERSONAL', ['La válvula de bloqueo, los carteles de advertencia y las alarmas exteriores resultaron '
                                    '[CONFORMES / NO CONFORMES].']),
        ('PRUEBAS QUINQUENALES', ['Las pruebas hidrostáticas de flexibles y cilindros resultaron [APROBADAS / NO APROBADAS].']),
    ],
    criterios=['Ítems conformes: [______ %]', 'Carga de agente: [CONFORME / NO CONFORME]', 'Fallas críticas: [______]']),
}

# ------------------------------------------------------------------ SIM (NFPA 170) – sin informe
SISTEMAS['SIM'] = dict(nom='Simbología de Seguridad contra Incendios', cap='NFPA 170', planillas=[
    dict(n=1, nombre='Verificación de simbología en planos', tipo='checklist', bloques=[
        ('IDENTIFICACIÓN DEL PLANO', [('Número de plano / revisión', ''), ('Sistema representado (sigla SG-PEM-IFI)', ''),
                                      ('Motivo: relevamiento inicial / anual / cambio / emisión', '')]),
        ('CAJETÍN Y ORIENTACIÓN', ['Datos de la empresa, autor y fecha', 'Instalación identificada', 'Flecha de norte',
                                   'Escala o leyenda «sin escala»']),
        ('SÍMBOLOS', ['Símbolos de agua, rociadores y extinción según el procedimiento',
                      'Símbolos de detección, alarma y notificación según el procedimiento',
                      'Símbolos de egreso, clases de fuego y señales de uso general',
                      'Forma, relleno, escala relativa y orientación correctos']),
        ('INDICADORES Y LEYENDA', ['Diámetros y temperaturas de actuación indicados', 'Subíndices explicados en la leyenda',
                                   'Leyenda con todos los símbolos usados']),
        ('CORRESPONDENCIA CON LA INSTALACIÓN', ['Cantidad de componentes coincidente con lo relevado',
                                                'Tipo de componentes coincidente', 'Ubicación de componentes coincidente',
                                                'Cambios del edificio o del uso reflejados']),
    ]),
    dict(n=2, nombre='Verificación de diagramas de evacuación', tipo='checklist', bloques=[
        ('IDENTIFICACIÓN DEL DIAGRAMA', [('Ubicación del diagrama (piso / sector)', ''), ('Número de diagrama / revisión', '')]),
        ('COMPOSICIÓN Y UBICACIÓN (NFPA 170, 11.2)', ['Composición clara y simple, con gráficos y símbolos',
                                                      'Dos salidas como mínimo (o plano de ubicación)', 'Leyenda con los símbolos de la NFPA 170',
                                                      'Texto y símbolos visibles para todos los ocupantes',
                                                      'Altura y lugar de paso de empleados y visitantes']),
        ('ORIENTACIÓN (NFPA 170, 11.3)', ['Parte superior en la dirección de la vista', '«Usted está aquí» correcto y dominante']),
        ('CONTENIDO (NFPA 170, 11.4)', ['Salidas, accesos, escaleras, ascensores y vestíbulos',
                                        'Áreas de refugio, de asistencia para el rescate y puntos de reunión',
                                        'Avisadores manuales, teléfonos de emergencia, desfibriladores y extintores',
                                        'Números telefónicos de emergencia vigentes', 'Pautas de evacuación y señales de alerta',
                                        'Sin información adicional que confunda']),
        ('MATERIAL (NFPA 170, 11.5)', ['Sin decoloración ni desgaste', 'Fotoluminiscente o autoluminoso sin carga eléctrica (si aplica)']),
        ('RECORRIDO EN EL LUGAR', ['Salidas representadas existentes y libres', 'Recorrido coincidente con el dibujado',
                                   'Equipamiento en el lugar indicado']),
    ]),
])
