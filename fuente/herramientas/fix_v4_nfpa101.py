# -*- coding: utf-8 -*-
"""v4: renumera las citas de la NFPA 101 a la edición 2024 en SDI y SAL (y SBC si corresponde).
Uso: python -I fix_v4_nfpa101.py <carpeta_manuales>"""
import sys, os
D = sys.argv[1]

COMUN = [
    ("""        ('Supervisión de las tareas (4.6.12.4 y 4.6.12.5)', 'las pruebas, inspecciones y mantenimiento se deben realizar a los '
                                                            'intervalos especificados, bajo la supervisión de una persona '
                                                            'responsable que asegure su cumplimiento.'),""",
     """        ('Pruebas periódicas (4.6.12.5)', 'todo dispositivo, equipo, sistema o elemento que requiera pruebas, inspecciones u '
                                          'operación periódicas para asegurar su mantenimiento se debe probar, inspeccionar u '
                                          'operar según el código o según lo indique la autoridad competente.'),
        ('Supervisión de las tareas (4.6.12.6)', 'las pruebas, inspecciones y mantenimiento se deben realizar a los intervalos '
                                                 'especificados por las normas NFPA aplicables, bajo la supervisión de una persona '
                                                 'responsable que asegure su cumplimiento.'),
        ('Registros (4.6.12.7)', 'los registros de mantenimiento, inspección y prueba se deben documentar en informes o '
                                 'formularios aprobados, y se admite presentarlos, conservarlos, consultarlos y compartirlos en '
                                 'formato electrónico aprobado.'),"""),
    ("""        ('Prueba integrada de sistemas (9.11.4)', 'donde lo exijan los capítulos 11 a 43 del código y dos o más sistemas de '
                                                  'protección contra incendio o de seguridad humana '
                                                  'estén integrados, se debe probar el sistema integrado para verificar su '
                                                  'operación y función conjunta, según la NFPA 4.'),""",
     """        ('Prueba integrada de sistemas (9.11.4.1)', 'donde lo exijan los capítulos 11 a 43 del código y dos o más sistemas de '
                                                    'protección contra incendio o de seguridad humana estén integrados, al probar '
                                                    'uno de ellos se debe verificar la respuesta de los sistemas integrados; '
                                                    'después de una reparación o reemplazo, la nueva prueba se limita a las funciones '
                                                    'iniciadas por el equipo reparado o reemplazado.'),
        ('Prueba según la NFPA 4 (9.11.4.2)', 'en edificios de gran altura y en sistemas integrados que incluyen control de humo, '
                                              'la prueba integrada se realiza según la NFPA 4; en edificios existentes, a intervalos '
                                              'no mayores que **10 años**, salvo que un plan de prueba integrada indique otra '
                                              'frecuencia (9.11.4.2.2).'),"""),
    ("('Funciones de control (9.6.5.2)'", "('Funciones de control (9.6.6.2)'"),
    ("funciones enumeradas en la NFPA 101, 9.6.5.2)", "funciones enumeradas en la NFPA 101, 9.6.6.2)"),
]

SDI = [
    ("('Programa de prueba y mantenimiento (9.6.1.3 y 9.6.1.4)'", "('Programa de prueba y mantenimiento (9.6.1.3 y 9.6.1.5)'"),
    ("('Sistema fuera de servicio (9.6.1.5)'", "('Sistema fuera de servicio (9.6.1.6)'"),
    ("""        ('Detectores cerca de cocinas (9.6.2.10.4)', 'requisito de ubicación: no deben ubicarse a menos de **3,0 m**, medidos en '
                                                    'recorrido horizontal, de un artefacto de cocción fijo, salvo '
                                                    'que estén listados para esa proximidad; entre **3,0 m y 6,1 m** deben contar con '
                                                    'silenciamiento de alarma o ser fotoeléctricos, con las excepciones del 9.6.2.10.5. '
                                                    'Se verifica en la inspección anual de cambios del edificio.'),""",
     """        ('Detectores cerca de cocinas y baños (9.6.2.10.4 y 9.6.2.10.5)', 'la instalación de alarmas y detectores de humo cerca '
                                                                           'de artefactos de cocción fijos y cerca de la puerta de '
                                                                           'un baño con ducha o bañera debe cumplir la NFPA 72. '
                                                                           'Se verifica en la inspección anual de cambios del '
                                                                           'edificio.'),"""),
    ("('Señal de evacuación (9.6.3.6, 9.6.3.7, 9.6.3.8 y 9.6.3.10)'", "('Señal de evacuación (9.6.3.7, 9.6.3.8, 9.6.3.9 y 9.6.3.11)'"),
    ("exceptuados (9.6.3.6.1)", "exceptuados (9.6.3.7.1)"),
    ("autoridad competente (9.6.3.6.2)", "autoridad competente (9.6.3.7.2)"),
    ("evacuar por sí mismos (9.6.3.6.3)", "evacuar por sí mismos (9.6.3.7.3)"),
    ("(NFPA 101, 9.6.3.7 y 9.6.3.8)", "(NFPA 101, 9.6.3.8 y 9.6.3.9)"),
    ("('Anunciación (9.6.7.1 a 9.6.7.6)'", "('Anunciación (9.6.8)'"),
    ("('Monóxido de carbono (9.12)', 'donde sea requerida la detección de monóxido de carbono, debe cumplir la NFPA 720.'),",
     "('Monóxido de carbono (9.12)', 'donde sea requerida la detección de monóxido de carbono, debe cumplir la NFPA 72; los '\n"
     "                                       'detectores instalados en conductos de aire no reemplazan la protección de las áreas '\n"
     "                                       'abiertas (9.12.1).'),"),
]

for fn, reps in (('content_SDI.py', COMUN + SDI), ('content_SAL.py', COMUN)):
    p = os.path.join(D, fn); s = open(p, encoding='utf-8').read()
    for old, new in reps:
        n = s.count(old)
        if n == 0:
            if 'Funciones de control' in old and fn == 'content_SDI.py': continue
            if 'funciones enumeradas' in old and fn == 'content_SAL.py': continue
            raise SystemExit('no encontrado en %s: %s' % (fn, old[:80]))
        s = s.replace(old, new)
    open(p, 'w', encoding='utf-8').write(s)
    print('ok', fn)
