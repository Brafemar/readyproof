# -*- coding: utf-8 -*-
"""Contenido de las planillas y de los informes de los sistemas SAP, SRE, SGE, SEP y SSA.
Fuente: planillas IRAM 3546:2011 de cada capítulo + manuales SG-PEM-IFI correspondientes."""
SN = ['SI', 'NO']

SISTEMAS = {}

# ============================================================== SAP
SISTEMAS['SAP'] = dict(nom='Sistema de Agua Pulverizada', cap='8', planillas=[
    dict(n=1, nombre='Información general', tipo='general', bloques=[
        ('INSTALACIÓN', [('No hay modificaciones del sistema, entorno o uso del área protegida', SN),
                         ('Existe documentación técnica de diseño y construcción', SN),
                         'Localización de la válvula tipo diluvio',
                         ('Tipo de accionamiento', ['Manual', 'Detección automática']),
                         ('Tipo de sistema de detección', ['Neumático', 'Eléctrico', 'Otro']),
                         ('Está todo el sistema en servicio', SN)]),
        ('VÁLVULAS, TOBERAS Y CAÑERÍAS', ['Marca, modelo y tipo de válvula de control', 'Marca, modelo y tipo de tobera',
                                          'Cantidad de toberas / faltantes', 'Tipo de cañerías y accesorios']),
        ('ABASTECIMIENTO DE AGUA', ['Última prueba de abastecimiento de agua',
                                    'Condiciones de depósitos y depósitos de presión', ('Capacidad', 'm³')]),
        ('BOMBAS CONTRA INCENDIO', [('Tipo de bomba', ['Diésel', 'Eléctrica', 'Naftera', 'Ninguna']),
                                    'Registro de la última inspección', ('Cantidad / funcionan', SN),
                                    'Marca y modelo de la bomba', ('Condiciones nominales: caudal', 'm³/h'),
                                    ('Condiciones nominales: altura manométrica', 'MPa'), 'Peligro de congelamiento']),
        ('TOMA DE IMPULSIÓN PARA BOMBEROS', ['Localización', ('Cantidad', 'm'), ('Diámetro', 'mm'), 'Identificación']),
    ]),
    dict(n=2, nombre='Inspección semanal', titulo='Inspección semanal (autocontrol)', tipo='periodico', modo='semanal', bloques=[
        ('INSPECCIÓN SEMANAL – MES: ________  AÑO: ______', [
            'Elemento protegido sin modificaciones', 'Elemento protegido no obstruye la descarga',
            'Orientación de las boquillas', 'Válvulas de control en posición correcta', 'Válvulas precintadas',
            'Boquillas y cañerías en buen estado y no bloqueadas', ('Local de válvula de control > 5 °C', '°C'),
            'Válvula de control y componentes sin daños', 'Válvula de diluvio sin daños ni fugas',
            'Componentes eléctricos en servicio', 'Temperatura de la sala de bombas',
            'Presión del sistema en valores normales', ('Presión del sistema de presurización', 'MPa')]),
    ]),
    dict(n=3, nombre='Inspección y pruebas mensual-trimestral', tipo='periodico', bloques=[
        ('INSPECCIÓN MENSUAL – SISTEMA DE VÁLVULAS Y CAÑERÍAS', [
            'Sin modificaciones de sistema, entorno o uso', 'Boquillas sin corrosión, materias extrañas ni daños',
            'Tuberías en buen estado, sin fugas, alineadas', 'Soportes sin daños ni corrosión',
            'Manómetros en buen estado', ('Presión del sistema al comienzo', 'MPa'), ('Presión del sistema al final', 'MPa'),
            'Válvulas precintadas e identificadas', 'Válvulas en posición correcta', 'Estado de la válvula de control',
            'Accionamientos manual y automático (sin descarga)', ('Temperatura lugar de montaje de válvula y reserva', '°C')]),
        ('INSPECCIÓN MENSUAL – RESERVA, PRESURIZACIÓN Y TOMA DE BOMBEROS', [
            'Reserva sin presión (cap. 13) o presurizada: nivel de agua', 'Reserva: válvulas y cañerías',
            'Válvula de llenado', ('Aire comprimido: presión de arranque del compresor', 'MPa'),
            ('Aire comprimido: presión de parada del compresor', 'MPa'), 'Arranque automático del compresor',
            'Funcionamiento de presostatos', ('Nitrógeno: presión de almacenamiento', 'MPa'),
            'Posición de la válvula reductora', 'Bomba centrífuga de presurización (cap. 12)',
            'Toma de impulsión operativa y señalizada', 'Instrucciones operativas en sala de bombas']),
        ('PRUEBAS MENSUALES Y MANTENIMIENTO MENSUAL', [
            'Válvulas de control abiertas (enclavadas o supervisadas)', 'Drenaje adecuado',
            'Conexiones de bomberos accesibles, visibles, tapas lubricadas', 'Maniobra de disparos manuales y válvulas a ¼ de vuelta',
            'Lubricación de vástagos (grafito / grafito con aceite)', 'Limpieza de cañerías enterradas (agua limpia)']),
        ('PRUEBAS TRIMESTRALES (MARCAR EN EL MES DE EJECUCIÓN)', [
            'Prueba de alarma de flujo de agua', 'Apertura de la válvula bypass de la alarma',
            'Válvulas de control a tope y a ¼ de vuelta']),
        ('TAREAS COMPLEMENTARIAS TRIMESTRALES (NFPA 25, CAPÍTULO 10)', [
            'Drenaje del área: sumideros y canaletas libres, muros de contención en buen estado']),
    ]),
    dict(n=4, nombre='Inspección y pruebas anuales', tipo='checklist', bloques=[
        ('INSPECCIÓN ANUAL', ['Boquillas sin daños físicos, sin corrosión y no obstruidas',
                              'Tuberías sin daños físicos, alineadas y sin cargas exteriores',
                              'Soportes de tuberías sin daños físicos ni corrosión', 'Calibración de manómetros']),
        ('PRUEBA ANUAL', [('Prueba de caudal total: funcionamiento correcto y tiempo de operación', 's'),
                          'Modelo de descarga', 'Funcionamiento del sistema y cobertura de agua pulverizada',
                          'Inspección interna de la válvula de diluvio: componentes libres y en buen estado',
                          'Válvulas de corte accionadas en su totalidad y precintadas o enclavadas',
                          'Filtros inspeccionados y limpios después de la prueba']),
        ('MANTENIMIENTO ANUAL', ['Lubricado de vástagos de válvulas de corte', 'Limpieza de cañerías y conexiones subterráneas con caudal pleno',
                                 'Limpieza de todos los filtros', 'Calibración de válvulas de seguridad en sistemas hidroneumáticos',
                                 'Mantenimiento del sistema de detección realizado (cap. 6)', 'Prueba de bombas realizada (cap. 12)']),
        ('TAREAS COMPLEMENTARIAS ANUALES (NFPA 25, CAPÍTULO 10)', [
            ('Tiempo de respuesta de la detección térmica (≤ 40 s)', 's'), ('Tiempo entre la detección y la llegada del agua', 's'),
            ('Presión en la boquilla hidráulicamente más remota', 'bar'), ('Presión en la válvula de diluvio', 'bar'),
            'Prueba simultánea de la máxima cantidad de sistemas esperada', 'Accionamiento manual operado',
            'Drenajes de puntos bajos abiertos, vaciados y cerrados', 'Filtro principal lavado; filtros de boquillas limpios',
            'Filtro principal retirado e inspeccionado (cada 5 años)',
            'Áreas inaccesibles inspeccionadas en la última parada (≤ 18 meses)']),
    ]),
    dict(n=5, nombre='Inspección y pruebas semestrales', tipo='checklist', bloques=[
        ('PRUEBA SEMESTRAL', ['Prueba en blanco del sistema: detección y actuación de la válvula (sin descarga)',
                              'Inspección interna de válvulas de diluvio: componentes libres, sin desgaste ni deformación',
                              'Reemplazo de partes dañadas de válvulas de diluvio',
                              'Prueba hidráulica o neumática de resistencia mecánica de cañerías', 'Flujo por todas las salidas',
                              'Recorrido de componentes de los picos atomizadores']),
        ('ENSAYO QUINQUENAL', [('Prueba hidráulica de tanques hidroneumáticos y cilindros de gases (fecha última prueba)', 'fecha')]),
    ]),
])

# ============================================================== SRE
SISTEMAS['SRE'] = dict(nom='Sistema de Rociadores de Espuma', cap='9', planillas=[
    dict(n=1, nombre='Información general', tipo='general', bloques=[
        ('INSTALACIÓN', [('No hay modificaciones del sistema, entorno o uso del área protegida', SN)]),
        ('VÁLVULAS', ['Localización de la válvula de control', 'Marca y modelo de la válvula',
                      ('Control de las válvulas', ['Precintadas', 'Enclavadas', 'Supervisadas']),
                      'Identificación: cantidad / tipo / diámetro']),
        ('ABASTECIMIENTO DE AGUA (CAPÍTULO 13)', ['Última prueba de abastecimiento de agua',
                                                  'Condiciones de depósitos y depósitos de presión', ('Capacidad', 'm³')]),
        ('BOMBAS (CAPÍTULO 12)', [('Tipo de bomba', ['Diésel', 'Eléctrica', 'Naftera', 'Ninguna']),
                                  'Registro de la última inspección', ('Cantidad / funcionan', SN)]),
        ('TOMA DE IMPULSIÓN PARA BOMBEROS', ['Localización', ('Cantidad', 'm'), ('Diámetro', 'mm'), 'Identificación']),
        ('INSTRUCCIONES DE OPERACIÓN', [('Están visibles las instrucciones de operación', SN)]),
    ]),
    dict(n=2, nombre='Inspección semanal', titulo='Inspección semanal (autocontrol)', tipo='periodico', modo='semanal', bloques=[
        ('INSPECCIÓN SEMANAL – MES: ________  AÑO: ______', [
            'Válvulas de control abiertas (incl. poste indicador y de calle)', 'Válvulas precintadas (si no, reprecintar)',
            'Rociadores sin daños ni bloqueos', 'Distancia libre de 46 cm por debajo de los rociadores',
            'Cubiertas o tapas en su lugar y listas']),
    ]),
    dict(n=3, nombre='Inspección mensual', tipo='periodico', bloques=[
        ('INSPECCIÓN MENSUAL', [
            'Toma de bomberos accesible, visible y no obstruida', 'Tapas sin daños, limpias y lubricadas con grafito',
            'Drenaje por válvula de goteo (riesgo de congelamiento)', 'Válvulas enclavadas o precintadas abiertas',
            'Dispositivos de alarma sin daños', 'Conexiones eléctricas de alarmas correctas',
            'Manómetros en valores normales', ('Presión del agua (diferencia > 10 %: investigar)', 'MPa'),
            'Instrucciones de operación visibles']),
    ]),
    dict(n=4, nombre='Inspección anual', tipo='checklist', bloques=[
        ('INSPECCIÓN ANUAL', ['Rociadores libres de corrosión, obstrucción, materiales extraños y daños físicos',
                              'Posición y ubicación de los rociadores',
                              'Tuberías en buen estado, sin daños, sin corrosión, alineadas y sin cargas externas',
                              'Soportes, anclajes y brazos sísmicos sin daños ni corrosión',
                              'Manómetros en buen estado y presión normal de abastecimiento']),
    ]),
    dict(n=5, nombre='Inspección quinquenal', tipo='checklist', bloques=[
        ('INSPECCIÓN QUINQUENAL', ['Válvulas de retención: inspección interna (enumerar cada válvula en observaciones)',
                                   'Válvulas de alarma: inspección interna', 'Válvulas de diluvio, preacción o similar: inspección interna',
                                   'Filtros: inspección interna de todos los existentes',
                                   'Bombas de espumígeno: revisión completa de bomba, impulsor y accesorios',
                                   'Sistemas proporcionadores: revisión completa según fabricante',
                                   'Tanque de espumígeno: vaciado, limpieza y control interno de corrosión',
                                   ('Tanque a presión: prueba hidrostática a 1,5 veces la presión (condición más exigente)', 'MPa')]),
        ('INSPECCIÓN INTERNA POR OBSTRUCCIÓN DE TUBERÍAS', ['Situación desfavorable detectada (A a G del manual)',
                                                            'Inspección interna realizada y resultado',
                                                            ('Próxima inspección periódica', 'fecha')]),
    ]),
    dict(n=6, nombre='Pruebas trimestral y semestral', tipo='checklist', bloques=[
        ('PRUEBA TRIMESTRAL – CAUDAL CON EL DRENAJE PRINCIPAL', [
            ('Presión estática del abastecimiento', 'MPa'), ('Presión residual del abastecimiento', 'MPa'),
            ('Variación respecto de la lectura anterior (> 10 %: investigar)', '%'), 'Cierre lento de la válvula de drenaje',
            'Presión de diseño grabada y etiqueta de criterios de diseño en la válvula']),
        ('PRUEBA TRIMESTRAL – ALARMAS, VÁLVULAS Y BOMBA', [
            'Alarma de flujo por apertura del bypass', 'Operación de válvulas y reposición de precintos',
            'Válvulas de corte a tope y a ¼ de vuelta', ('Bomba de espumígeno 20 s a 30 s sin pérdidas', 's'),
            'Válvulas, interruptores y controles repuestos; sistema en servicio']),
        ('PRUEBA SEMESTRAL', ['Disparo de la válvula de control sin descarga (agua y espumígeno cerrados)',
                              'Disparo por detección automática o actuación manual', 'Sistema de detección probado (cap. 6)',
                              ('Drenaje de espumígeno del fondo del depósito; reposo; incrustaciones', 'L'),
                              'Estado de la válvula del depósito de espumígeno',
                              'Válvulas, interruptores y controles repuestos; sistema en servicio']),
    ]),
    dict(n=7, nombre='Prueba y mantenimiento anual', tipo='checklist', bloques=[
        ('PRUEBA ANUAL', ['Calidad de espumígeno: muestra de medio litro al fabricante; informe adjunto',
                          ('Tiempo de respuesta del sistema proporcionador', 's'), ('Tiempo de descarga', 's'),
                          ('Presión del rociador hidráulicamente más alejado', 'bar'), ('Presión en la válvula de control principal', 'bar'),
                          'Descarga correcta de los rociadores (dirección y patrón)',
                          ('Dosificación (no menor que el 90 % de la mínima de diseño)', '%')]),
        ('TAREAS COMPLEMENTARIAS (NFPA 25, CAPÍTULO 11)', [
            'Mensual: posición de las válvulas del sistema proporcionador', 'Trimestral: drenaje del área y muros de contención',
            'Anual: prueba operativa del proporcionador', 'Anual: cantidad de espumígeno según el diseño original',
            'Anual: tanque de espumígeno sin corrosión externa ni daños', 'Anual: análisis de calidad del espumígeno (informe)',
            'Compatibilidad entre espumígeno y dispositivos de descarga verificada',
            'Filtros de dispositivos de descarga inspeccionados y limpios']),
        ('MANTENIMIENTO ANUAL', ['Operación de válvulas de poste indicador y husillo ascendente; ¼ de vuelta',
                                 'Válvulas de corte en todo su recorrido, precintadas o enclavadas',
                                 'Lubricado de válvulas con grafito o grafito con aceite liviano',
                                 'Válvulas de retención en aspiración de espumígeno: revisión interna']),
    ]),
])

# ============================================================== SGE
SISTEMAS['SGE'] = dict(nom='Sistema Generador de Espuma', cap='10', planillas=[
    dict(n=1, nombre='Información general', tipo='general', bloques=[
        ('INSTALACIÓN', [('Tipo de sistema', ['Húmedo', 'Seco', 'Diluvio', 'Acción previa']),
                         'Marca y modelo de la válvula y formadores de espuma', 'Cantidad de toberas / faltantes',
                         ('Sistema en servicio', SN), ('No hay modificaciones del sistema, entorno o uso del área protegida', SN)]),
        ('VÁLVULAS', ['Localización de la válvula de control', ('Control de las válvulas', ['Precintadas', 'Enclavadas', 'Supervisadas']),
                      'Identificación: cantidad / tipo / diámetro']),
        ('ABASTECIMIENTO DE AGUA', ['Última prueba de abastecimiento de agua', ('Depósitos a gravedad: capacidad', 'm³'),
                                    ('Bajo presión', 'MPa'), ('Bajo presión: capacidad', 'm³')]),
        ('BOMBAS CONTRA INCENDIO', [('Tipo de bomba', ['Diésel', 'Eléctrica', 'Naftera', 'Ninguna']),
                                    'Registro de la última inspección', ('Cantidad / funcionan', SN)]),
        ('TOMA DE IMPULSIÓN PARA BOMBEROS', ['Localización', ('Cantidad', 'm'), ('Diámetro', 'mm'), 'Identificación']),
        ('SISTEMA HÚMEDO / SECO / ACCIÓN PREVIA', ['Peligro de congelamiento', ('La válvula está protegida', SN),
                                                   ('Memoria de cálculo del sistema hidráulico', SN),
                                                   ('Los datos hidráulicos figuran cerca de la válvula', SN)]),
        ('ESPUMÍGENO Y DOSIFICACIÓN', [('Tanque para líquido espumígeno', ['PRFV', 'Metálico']), ('Capacidad del tanque', 'L'),
                                       ('Dosificador', ['Eductor', 'Sistema de pilotaje', 'Presión balanceada'])]),
    ]),
    dict(n=2, nombre='Inspección semanal', titulo='Inspección semanal (autocontrol)', tipo='periodico', modo='semanal', bloques=[
        ('INSPECCIÓN SEMANAL – MES: ________  AÑO: ______', [
            'Válvulas de control abiertas (incl. poste indicador y de calle)', 'Válvulas precintadas (si no, reprecintar)',
            'Abastecimiento: depósitos a gravedad y bajo presión', 'Nivel del tanque de líquido emulsor']),
    ]),
    dict(n=3, nombre='Inspección mensual', tipo='periodico', bloques=[
        ('INSPECCIÓN MENSUAL', [
            'Bombas: tipo y registro de la última inspección', 'Conexión de bomberos accesible, visible y no obstruida',
            'Tapas sin daños, limpias y lubricadas con grafito', 'Drenaje por válvula de goteo (riesgo de congelamiento)',
            'Válvulas enclavadas o precintadas abiertas', ('Presiones del sistema', 'MPa'),
            'Dispositivos de descarga sin daños ni obstrucción', 'Depósito de espumígeno lleno (mitad de la cúpula)',
            'Instrucciones de operación visibles']),
    ]),
    dict(n=4, nombre='Inspección anual', tipo='checklist', bloques=[
        ('INSPECCIÓN ANUAL', ['Cámaras de espuma sin daños, no obstruidas y con sellos intactos',
                              'Tuberías en buen estado, sin daños mecánicos, sin corrosión, alineadas y sin cargas externas',
                              'Soportes de tuberías sin daños ni corrosión',
                              'Manómetros en buen estado y presiones normales en el abastecimiento']),
    ]),
    dict(n=5, nombre='Pruebas trimestrales y semestral', tipo='checklist', bloques=[
        ('PRUEBA TRIMESTRAL', ['Bomba de espumígeno en funcionamiento, con recirculación, sin pérdidas',
                               'Prueba del sistema cuya actuación depende de la bomba',
                               'Válvulas, interruptores y controles repuestos; sistema en servicio']),
        ('PRUEBA DEL PRIMER SEMESTRE', ['Sistema de detección probado (cap. 6)',
                                        ('Drenaje de espumígeno del fondo del depósito; reposo; sedimentos', 'L'),
                                        'Estado de las válvulas instaladas en el depósito de espumígeno']),
        ('PRUEBA DEL SEGUNDO SEMESTRE', ['Sistema de detección probado (cap. 6)',
                                         ('Drenaje de espumígeno del fondo del depósito; reposo; sedimentos', 'L'),
                                         'Estado de las válvulas instaladas en el depósito de espumígeno']),
    ]),
    dict(n=6, nombre='Prueba anual', tipo='checklist', bloques=[
        ('PRUEBA ANUAL', ['Calidad de espumígeno: muestra enviada al fabricante o laboratorio; informe adjunto',
                          'Prueba de funcionamiento con descarga', ('Tiempo de respuesta', 's'), ('Tiempo de descarga', 's'),
                          ('Presión en el dispositivo de descarga hidráulicamente más alejado', 'bar'),
                          ('Presión en la válvula de control principal', 'bar'),
                          ('Dosificación (no menor que el 90 % de la mínima de diseño)', '%'),
                          'Verificación de calidad de espuma obtenida (expansión y drenaje según fabricante)',
                          'Mediciones resultantes adjuntas o registradas en observaciones']),
    ]),
    dict(n=7, nombre='Mantenimiento', tipo='checklist', bloques=[
        ('MANTENIMIENTO TRIMESTRAL', ['Operación de válvulas en todo su recorrido y retorno a posición normal; precintado']),
        ('MANTENIMIENTO SEMESTRAL', ['Estado de la válvula de presión-vacío del depósito de espumígeno']),
        ('MANTENIMIENTO ANUAL', ['Lubricación de válvulas']),
    ]),
])

# ============================================================== SEP
SISTEMAS['SEP'] = dict(nom='Sistema Fijo de Extinción por Polvo', cap='15', planillas=[
    dict(n=1, nombre='Información general', tipo='general', bloques=[
        ('INSTALACIÓN', ['¿Cuál es el riesgo protegido?', ('No hay modificaciones del sistema, entorno o uso del área protegida', SN),
                         ('Cuenta con los instructivos de operación', SN)]),
        ('TIPO DE AGENTE EXTINTOR', [('Agente', ['Bicarbonato potásico', 'Fosfato monoamónico', 'Cloruro potásico']),
                                     ('Agente (cont.)', ['Urea bicarbonato potásico', 'Bicarbonato sódico', 'Otros'])]),
        ('CILINDROS DE POLVO', [('Presión normal', 'kPa'), ('Presión normal según fabricante', 'kPa'), ('Peso normal', 'kg'),
                                ('Peso normal según fabricante', 'kg')]),
        ('EQUIPO PROTEGIDO', [('Equipos', ['Freidora', 'Plancha', 'Parrilla', 'Parrillas altas']),
                              ('Equipos (cont.)', ['Quemador', 'Conducto', 'Otros'])]),
        ('GAS PROPELENTE, ALARMA Y CORTE', [('Presurización', ['Presión contenida (nitrógeno seco)', 'Cartucho de gas propelente']),
                                            ('¿Se dispone de cartucho propelente de gas?', SN), ('Peso normal del cartucho', 'kg'),
                                            ('Presión normal (para nitrógeno)', 'kPa'), ('¿Está conectado el sistema de alarma?', SN),
                                            ('Corte automático del equipo de cocina', SN), ('Tipo de corte', ['Gas', 'Eléctrico'])]),
    ]),
    dict(n=2, nombre='Inspección mensual', tipo='periodico', bloques=[
        ('INSPECCIÓN MENSUAL', [
            'Tapas de boquillas colocadas', 'Sin grasa acumulada en boquillas y eslabones',
            'No se usan líquidos corrosivos en cables y eslabones', 'No se añadió ni modificó equipo de cocina',
            'Boquillas orientadas a las superficies que protegen', 'Disparadores manuales no obstruidos',
            'Indicadores antimanipulación y sellos intactos', 'Etiqueta o certificado de mantenimiento en su lugar',
            ('Presión indicada en el manómetro correcta', 'kPa')]),
    ]),
    dict(n=3, nombre='Inspección semestral', tipo='checklist', bloques=[
        ('INSPECCIÓN Y PRUEBA SEMESTRAL (CORRECTO SI ES ≥ AL MÍNIMO DE SEP-1)', [
            ('Presión del cilindro de polvo', 'kPa'), 'Unión del cartucho de gas propelente con el cilindro',
            ('Cartucho de gas propelente: presión (nitrógeno)', 'kPa'), ('Cartucho de gas propelente: peso (CO₂) y testigo del disco', 'kg'),
            'Estado del cilindro contenedor de polvo', 'Apelmazado del polvo (sistemas tipo cartucho de gas)',
            'Prueba del accionamiento automático (sin descarga)', 'Operaciones de mantenimiento recomendadas por el fabricante']),
        ('ANUAL', ['Sustitución de eslabones fusibles por otros del mismo rango de temperatura',
                   'Cable reinstalado y encajado en las poleas; sistema restituido desde el panel',
                   'Control de señales eléctricas o neumáticas de disparo (sistemas sin fusibles)',
                   'Tuberías de descarga desde la válvula del cilindro hasta las boquillas (tarea complementaria)']),
        ('CADA 2 AÑOS (TAREAS COMPLEMENTARIAS)', [('Estado y peso de carga del polvo', 'kg'),
                                                  'Vaciado y recarga de equipos BC o ABC, sin mezclar agentes',
                                                  'Recorrido de la válvula de descarga y de su señal de disparo']),
        ('CADA 5 AÑOS (TAREAS COMPLEMENTARIAS)', ['Prueba de descarga del sistema', 'Ensayo de extinción del agente',
                                                  ('Prueba hidrostática de cilindros de polvo, de gas y latiguillos (IRAM 3517-II)', 'fecha')]),
    ]),
])

# ============================================================== SSA
SISTEMAS['SSA'] = dict(nom='Sistema Fijo de Extinción por Solución Acuosa', cap='16', planillas=[
    dict(n=1, nombre='Información general', tipo='general', bloques=[
        ('INSTALACIÓN', ['Designación del local', 'Marca del sistema', 'Marca de los detectores', 'Marca del panel de control',
                         'Fecha de instalación del sistema', ('Tipo de sistema', ['Alta presión', 'Baja presión']),
                         'Cantidad de cilindros', ('Capacidad del cilindro', 'kg'), ('Capacidad del sistema', 'kg/m³'),
                         ('Presión normal a 20 °C', 'MPa'), 'Fusible: marca',
                         ('Disparo', ['Manual', 'Eléctrico', 'Neumático', 'Automático']),
                         ('No hay modificaciones del sistema, entorno o uso del área protegida', SN)]),
        ('SISTEMA DE DETECCIÓN', [('Detectores', ['Termovelocimétricos', 'Temperatura fija', 'Por compensación', 'Otros'])]),
        ('COMANDOS DE EXTINCIÓN', [('Comando', ['Zona simple', 'Dos zonas (zona cruzada)', 'Dos detectores por zona', 'Otros'])]),
        ('RESULTADOS', ['Resultado y comentarios de inspección / mantenimiento', 'Otros equipos probados o inspeccionados']),
    ]),
    dict(n=2, nombre='Inspección mensual', tipo='periodico', bloques=[
        ('INSPECCIÓN MENSUAL', [
            'Tapas de boquillas colocadas', 'Sin grasa acumulada en boquillas y eslabones',
            'No se usan líquidos corrosivos en cables y eslabones', 'No se añadió ni modificó equipo de cocina',
            'Boquillas orientadas a las superficies que protegen', 'Disparadores manuales no obstruidos',
            'Indicadores antimanipulación y sellos intactos', 'Etiqueta o certificado de mantenimiento en su lugar',
            ('Presión indicada en el manómetro correcta', 'MPa')]),
    ]),
    dict(n=3, nombre='Prueba semestral y quinquenal', tipo='checklist', bloques=[
        ('PRUEBA DEL PRIMER SEMESTRE', ['Funcionamiento del sistema sin descarga (detección, alarmas, disparo)',
                                        'Equipos asociados', 'Sistema de detección probado (cap. 6)']),
        ('PRUEBA DEL SEGUNDO SEMESTRE', ['Funcionamiento del sistema sin descarga (detección, alarmas, disparo)',
                                         'Equipos asociados', 'Sistema de detección probado (cap. 6)']),
        ('PRUEBA QUINQUENAL', ['Artefactos fríos, aceite retirado, gas y energía cortados',
                               'Prueba de descarga usando agua en lugar de solución acuosa',
                               'Sistema de tubería secado con aire o nitrógeno', 'Recarga con nueva solución extintora acuosa',
                               'Prueba hidrostática: recipiente de agente extintor', 'Prueba hidrostática: recipiente de presión auxiliar',
                               'Prueba hidrostática: flexibles de unión']),
    ]),
    dict(n=4, nombre='Mantenimiento', tipo='checklist', bloques=[
        ('MANTENIMIENTO DEL PRIMER SEMESTRE', ['Detectores y eslabones fusibles', 'Recipiente de solución extintora acuosa',
                                               'Cilindros de gas propelente', 'Dispositivos de disparo',
                                               'Tuberías y boquillas; tuberías no obstruidas', 'Alarmas', 'Equipo auxiliar',
                                               'Prueba hidrostática o reemplazo (según necesidad)']),
        ('MANTENIMIENTO DEL SEGUNDO SEMESTRE', ['Detectores y eslabones fusibles', 'Recipiente de solución extintora acuosa',
                                                'Cilindros de gas propelente', 'Dispositivos de disparo',
                                                'Tuberías y boquillas; tuberías no obstruidas', 'Alarmas', 'Equipo auxiliar',
                                                'Prueba hidrostática o reemplazo (según necesidad)']),
        ('MANTENIMIENTO ANUAL', ['Sustitución de los eslabones fusibles']),
    ]),
])
