"""Correcciones de la auditoría independiente N.º 3 (auditoria3.md) sobre los content_*.py.
Uso: python -I fix_audit3_manuales.py <carpeta manuales>"""
import sys, os
D = sys.argv[1]
S = {}
def load(sig):
    S[sig] = open(os.path.join(D, 'content_%s.py' % sig), encoding='utf8').read()
def r(sig, o, n):
    assert S[sig].count(o) == 1, (sig, o[:90], S[sig].count(o)); S[sig] = S[sig].replace(o, n)

ALL = ['SAP', 'SRE', 'SGE', 'SEP', 'SSA', 'SDI', 'SBC', 'SAL']
for s in ALL: load(s)

# ---- A3-M1: codificación de tres símbolos (los 8 manuales) ----
OLD = ("'En cada planilla se debe indicar con ✓ si el ítem cumple, o con X si no cumple o no es apreciable, y cada planilla debe '\n"
       "        'ser firmada por el supervisor del mantenedor y por el responsable de la instalación, con su aclaración.',")
NEW = ("'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '\n"
       "        'codificación de las planillas de la IRAM 3546:2011; las tareas que no resulten aplicables se indican con NA. Toda '\n"
       "        'condición O o X se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y '\n"
       "        'por el responsable de la instalación, con su aclaración.',")
for s in ALL: r(s, OLD, NEW)

# ---- Desactivación (A3-M4), común a SDI y SAL ----
DESACT = '''    a(('p', 'Cuando el sistema, o una parte de él, quede fuera de servicio por una desactivación programada o por una falla, se debe:'))
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
'''

# ================= SDI =================
r('SDI', "            'fallas. Si una deficiencia no se corrige al finalizar la prueba, se debe informar por escrito al responsable de la '\n"
         "            'instalación.'))\n",
  "            'fallas.'))\n" + DESACT)
r('SDI', "'llamada y detención de ascensores y la detención del aire acondicionado (NFPA 101, '\n"
         "                                               '9.6.5.2).'),",
  "'llamada y detención de ascensores y la detención del aire acondicionado (NFPA 72, '\n"
  "                                               'Tabla 14.4.3.2, ítem 24; funciones enumeradas en la NFPA 101, 9.6.5.2).'),")
# A3-m3: pruebas anuales NFPA 72 adicionales
r('SDI', "        ('Transmisión al servicio de monitoreo', 'accionar un dispositivo iniciador, crear una condición de falla y accionar un '\n"
         "                                                 'dispositivo de supervisión, y verificar la recepción de cada señal fuera de las '\n"
         "                                                 'instalaciones.'),\n",
  "        ('Transmisión al servicio de monitoreo', 'accionar un dispositivo iniciador, crear una condición de falla y accionar un '\n"
  "                                                 'dispositivo de supervisión, y verificar la recepción de cada señal fuera de las '\n"
  "                                                 'instalaciones; con comunicador digital (DACT), verificar que cada intento de '\n"
  "                                                 'transmisión se complete dentro de los **90 s** (NFPA 72, Tabla 14.4.3.2, ítem 4).'),\n"
  "        ('Avisadores manuales', 'operar la totalidad de los avisadores manuales y verificar la señal en la central.'),\n"
  "        ('Dispositivos electromecánicos de descarga', 'donde existan, verificar su funcionamiento mediante la remoción del '\n"
  "                                                      'eslabón fusible (NFPA 72, Tabla 14.4.3.2, ítem 17).'),\n"
  "        ('Interruptores de alarma de sistemas de extinción', 'donde existan, verificar la recepción de su señal en la central.'),\n"
  "        ('Detectores de gas', 'probarlos según las instrucciones del fabricante.'),\n"
  "        ('Aparatos de notificación audible textual', 'donde existan, verificar que la información emitida es distinguible y '\n"
  "                                                     'comprensible (NFPA 72, Tabla 14.4.3.2, ítem 22).'),\n")
r('SDI', "'si no se reemplazan.'),\n    ]))\n    a(('p', compl(4)))",
  "'si no se reemplazan.'),\n    ]))\n"
  "    a(('p', 'En zonas donde las falsas alarmas aumenten respecto del año anterior, se deben realizar pruebas de calibración '\n"
  "            '(NFPA 72, 14.4.4.3.3.2).'))\n    a(('p', compl(4)))")
# A3-M5(a) y A3-M4: NFPA 101
r('SDI', "'asegure su integridad operativa; el presente procedimiento '\n"
         "                                                                   'constituye ese programa.'),",
  "'asegure su integridad operativa; el presente procedimiento '\n"
  "                                                                   'puede constituir ese programa una vez aceptado por la '\n"
  "                                                                   'autoridad competente.'),")
r('SDI', "        ('Sistema fuera de servicio (9.6.1.5)', 'los procedimientos ante la salida de servicio del sistema deben cumplir la NFPA 72: '\n"
         "                                                'notificación al responsable de la instalación, medidas compensatorias mientras dure '\n"
         "                                                'la condición y registro de su inicio y fin.'),",
  "        ('Sistema fuera de servicio (9.6.1.5)', 'los procedimientos ante la desactivación del sistema de alarma deben cumplir la '\n"
  "                                                'NFPA 72; se aplican según lo indicado para la desactivación del sistema en el '\n"
  "                                                'apartado PRUEBA de este procedimiento (NFPA 72, 10.20).'),")
# A3-m1
r('SDI', "('Detectores cerca de cocinas (9.6.2.10.4)', 'no deben ubicarse a menos de **3,0 m** de un artefacto de cocción fijo, salvo '",
  "('Detectores cerca de cocinas (9.6.2.10.4)', 'requisito de ubicación: no deben ubicarse a menos de **3,0 m**, medidos en '\n"
  "                                                    'recorrido horizontal, de un artefacto de cocción fijo, salvo '")
r('SDI', "'silenciamiento de alarma o ser fotoeléctricos. Se verifica en la inspección '\n"
         "                                                    'anual de cambios del edificio.'),",
  "'silenciamiento de alarma o ser fotoeléctricos, con las excepciones del 9.6.2.10.5. '\n"
  "                                                    'Se verifica en la inspección anual de cambios del edificio.'),")
r('SDI', "        ('Señal de evacuación (9.6.3.6, 9.6.3.7, 9.6.3.8 y 9.6.3.10.1)', 'la señal general de evacuación debe operar en todo el '\n"
         "                                                                         'edificio, salvo escaleras de salida y cabinas de ascensor; '",
  "        ('Señal de evacuación (9.6.3.6, 9.6.3.7, 9.6.3.8 y 9.6.3.10)', 'la señal general de evacuación debe operar según el '\n"
  "                                                                       'método aprobado: en todo el edificio, salvo los lugares '\n"
  "                                                                       'exceptuados (9.6.3.6.1); por zonas, con notificación '\n"
  "                                                                       'selectiva aprobada por la autoridad competente (9.6.3.6.2); '\n"
  "                                                                       'o con los requisitos especiales para ocupantes que no pueden '\n"
  "                                                                       'evacuar por sí mismos (9.6.3.6.3); '")
r('SDI', "'señales y los aparatos de notificación deben usarse solo '\n"
         "                                                                         'para alarma o emergencia.'),",
  "'señales y los aparatos de notificación deben usarse solo '\n"
  "                                                                         'para alarma o emergencia; los sistemas de comunicación de '\n"
  "                                                                         'emergencia por voz pueden usarse para otros fines según la '\n"
  "                                                                         'NFPA 72.'),")
r('SDI', "        ('Anunciación (9.6.7.2 y 9.6.7.3)', 'la anunciación en el centro de control debe ser audible y visible, con al menos una '\n"
         "                                            'zona por piso en edificios nuevos.'),",
  "        ('Anunciación (9.6.7.1 a 9.6.7.6)', 'donde otra sección del código requiera anunciación, en el centro de control debe ser '\n"
  "                                            'audible y visible, con al menos una zona por piso en edificios nuevos; las señales '\n"
  "                                            'de falla y de supervisión también se deben anunciar.'),")
# A3-m2 + A3-m3 (control de cambios)
r('SDI', "            'máximo de **50** (NFPA 72, 14.4.2.1 y 14.4.2.4).'))",
  "            'máximo de **50** (NFPA 72, 14.4.2.1 y 14.4.2.4). Las reparaciones o modificaciones del hardware de la central se '\n"
  "            'prueban según los ítems 2(a) y 2(d) de la Tabla 14.4.3.2 (14.4.2.3), y los cambios del software ejecutivo requieren '\n"
  "            'una prueba funcional del **10 %** del sistema, con al menos un dispositivo en cada circuito de entrada y de salida '\n"
  "            '(14.4.2.5).'))")
r('SDI', "            'interrumpir equipos críticos del edificio.'))\n    return C",
  "            'interrumpir equipos críticos del edificio. Los simulacros de evacuación, donde sean requeridos, son responsabilidad '\n"
  "            'del propietario o usuario, y de cada uno se debe completar un registro escrito (NFPA 101, 4.7.6).'))\n    return C")
DOC = ("        'La documentación de diseño del sistema y los procedimientos de inspección, prueba y mantenimiento se deben conservar en '\n"
       "        'un lugar aprobado y seguro durante toda la vida útil del sistema (NFPA 101, 9.11.3.1).',\n")
r('SDI', "        '14.6.2, por ser ese plazo mayor.' % N72,\n", "        '14.6.2, por ser ese plazo mayor.' % N72,\n" + DOC)

# función seguridad_humana (SDI y SAL): 4.6.12.3 y 9.11.4
for s in ('SDI', 'SAL'):
    r(s, "'público que no sean requeridos se deben mantener o retirar, nunca dejar '\n"
         "                                                       'inoperativos.'),",
      "'público que no sean requeridos se deben mantener o retirar, porque su '\n"
      "                                                       'presencia genera una expectativa de protección; no se deben '\n"
      "                                                       'dejar instalados en condición inoperativa (A.4.6.12.3).'),")
    r(s, "('Prueba integrada de sistemas (9.11.4)', 'cuando dos o más sistemas de protección contra incendio o de seguridad humana '",
      "('Prueba integrada de sistemas (9.11.4)', 'donde lo exijan los capítulos 11 a 43 del código y dos o más sistemas de '\n"
      "                                                  'protección contra incendio o de seguridad humana '")

# ================= SAL =================
r('SAL', "            'riesgos de una descarga inadvertida. Cuando se detecten fallas, se debe proceder inmediatamente a su reparación.'))\n",
  "            'riesgos de una descarga inadvertida. Cuando se detecten fallas, se debe proceder inmediatamente a su reparación.'))\n" + DESACT)
r('SAL', "            'cumplimiento. En el presente sistema la IRAM 3546:2011 no establece inspecciones de esa frecuencia.'))",
  "            'cumplimiento, dejando constancia de los hallazgos verificados. En el presente sistema la IRAM 3546:2011 no '\n"
  "            'establece inspecciones de esa frecuencia.'))")
# A3-m4
r('SAL', "            ('Paso a paso', 'verificar el circuito del solenoide de descarga con lámpara de prueba o carga simulada según el '\n"
         "                            'fabricante y la supervisión mediante la creación de un circuito abierto.'),",
  "            ('Paso a paso', 'verificar el funcionamiento del solenoide de descarga con carga simulada según el fabricante; en '\n"
  "                            'circuitos con dispositivo explosivo, con lámpara de flash (AGI) u otra luz de prueba aprobada; en '\n"
  "                            'circuitos de tipo matriz, accionar todos los sensores y verificar la matriz; en circuitos de zona '\n"
  "                            'verificada, accionar los sensores en un mínimo de **cuatro** lugares del circuito; y verificar la '\n"
  "                            'supervisión mediante la creación de un circuito abierto.'),")
r('SAL', "'(NFPA 72, Tabla 14.4.3.2, 18(f) y 18(i)).')]),",
  "'(NFPA 72, Tabla 14.4.3.2, 18(e) a 18(i)).')]),")
r('SAL', "            ('Paso a paso', 'accionar el interruptor de aborto según su tipo y luego el disparo manual.'),",
  "            ('Paso a paso', 'accionar el interruptor de aborto y luego el disparo manual; en los de tipo hombre muerto y especial, '\n"
  "                            'verificar la secuencia; en los de tipo reciclaje, verificar la matriz con cada sensor accionado.'),")
# A3-M6
CAL = ("El agente recuperado o de reposición debe corresponder al tipo y a la especificación indicados en la placa del sistema y '\n"
       "            'en la planilla SG-PEM-IFI-SAL-1, y su calidad se debe verificar según un procedimiento documentado, en función de las '\n"
       "            'normas de aplicación y de las instrucciones del fabricante, con certificado de análisis del proveedor o del '\n"
       "            'recuperador (IRAM 3546:2011, Mantenimiento de las instalaciones). No se deben mezclar agentes distintos ni recargar '\n"
       "            'con agente de origen no certificado.")
r('SAL', "            'competente, con recuperación del agente y no por venteo.'))",
  "            'competente, con recuperación del agente y no por venteo. " + CAL + "'))")
r('SAL', "        ('Reposición', 'reposición del agente extintor, rearme de los cabezales y restitución del sistema a su estado operativo.'),\n    ]))\n",
  "        ('Reposición', 'reposición del agente extintor, con verificación de su calidad según lo indicado para la prueba '\n"
  "                       'quinquenal, rearme de los cabezales y restitución del sistema a su estado operativo.'),\n    ]))\n")
# A3-m7 seguridad
r('SAL', "        ('Pruebas', 'notificación a los ocupantes durante las reparaciones o pruebas y aseguramiento del sistema contra la descarga '\n"
         "                    'inadvertida.'),\n",
  "        ('Pruebas', 'notificación a los ocupantes durante las reparaciones o pruebas y aseguramiento del sistema contra la descarga '\n"
  "                    'inadvertida.'),\n"
  "        ('Productos de descomposición', 'después de una descarga sobre un fuego, los agentes halogenados generan productos de '\n"
  "                                        'descomposición tóxicos y corrosivos; el reingreso se hace con ventilación forzada y con '\n"
  "                                        'protección respiratoria cuando no se pueda verificar la atmósfera.'),\n"
  "        ('Sala de cilindros', 'recipientes sujetos; ningún cilindro se traslada con el cabezal de control montado.'),\n")
# A3-m7 mantenimiento mensual con subtítulo
r('SAL', "            'agente y de las conexiones. La IRAM 3546:2011 no establece tareas de mantenimiento mensual para este sistema.'))\n",
  "            'agente y de las conexiones.'))\n\n"
  "    a(('h4', 'Mantenimiento mensual'))\n"
  "    a(('p', 'La IRAM 3546:2011 no establece tareas de mantenimiento mensual para este sistema.'))\n")
# A3-M5(c)
r('SAL', "        ('Funciones de control (9.6.5.2)', 'la detención del aire acondicionado, la liberación de retenedores de puertas y el '\n"
         "                                           'desbloqueo de puertas comandados por el sistema deben verificarse en la prueba anual, '\n"
         "                                           'porque aseguran la retención del agente y la evacuación de las personas.'),",
  "        ('Funciones de control (9.6.5.2)', 'donde otra sección del código lo requiera, el sistema de alarma debe actuar la '\n"
  "                                           'liberación de retenedores de puertas, el desbloqueo de puertas y la detención del aire '\n"
  "                                           'acondicionado, entre otras funciones; su verificación anual se realiza según la NFPA 72, '\n"
  "                                           'Tabla 14.4.3.2, ítem 24. En este sistema esas funciones son además necesarias para '\n"
  "                                           'mantener la concentración de diseño del agente.'),")
r('SAL', "            'técnico supervisa y valida las tareas realizadas.'))\n    return C",
  "            'técnico supervisa y valida las tareas realizadas. Los simulacros de evacuación, donde sean requeridos, son '\n"
  "            'responsabilidad del propietario o usuario, y de cada uno se debe completar un registro escrito (NFPA 101, 4.7.6).'))\n"
  "    return C")
r('SAL', "'los comandos de extinción se registran en la planilla SG-PEM-IFI-SAL-1 %s – %s.' % (NOM, PL[1]),\n",
  "'los comandos de extinción se registran en la planilla SG-PEM-IFI-SAL-1 %s – %s.' % (NOM, PL[1]),\n" + DOC)

# ================= SBC (menores A3-m5, A3-m6) =================
r('SBC', "'permanece en la primera etapa de tensión o corriente de arranque reducida, el tiempo de marcha desde '\n"
         "                            'el arranque y la corriente de cada fase.'),",
  "'permanece en la primera etapa de tensión o corriente de arranque reducida, el tiempo de marcha desde '\n"
  "                            'el arranque (para controles de parada automática) y la corriente de cada fase.'),")
r('SBC', "            'ante diferencias, se adopta siempre la condición más exigente.' % N20))",
  "            'ante diferencias, se adopta siempre la condición más exigente. La NFPA 20 (14.4) remite la inspección, prueba y '\n"
  "            'mantenimiento periódicos a la NFPA 25, que no se encuentra disponible; por eso, los valores de la prueba de aceptación '\n"
  "            'en campo de la NFPA 20 (14.2) se aplican por analogía a la prueba anual.' % N20))")
r('SBC', "'total nominal (NFPA 20, 6.2.1 y 7.1.2.1).'),",
  "'total nominal (NFPA 20, 6.2.1).'),")
r('SBC', "        ('Presión a caudal cero', 'no mayor que el **140 %** de la presión total nominal (NFPA 20, 7.1.2.2; el 6.2.2 de la versión '\n"
         "                                  'en español indica «40 %», un error de traducción).'),",
  "        ('Presión a caudal cero', 'no mayor que el **140 %** de la presión total nominal (NFPA 20, 6.2.2, cuya versión en español '\n"
  "                                  'indica «40 %» por error de traducción; el valor de 140 % se confirma en el 7.1.2.2, para '\n"
  "                                  'bombas verticales).'),")
r('SBC', "('Presión de succión', 'con dispositivo antirretorno, no menor que",
  "('Presión de succión', 'con dispositivo o montaje de prevención de contraflujo, no menor que")
r('SBC', "                            'calibración; contrastar los manómetros fijos de la sala.'),",
  "                            'calibración y exactitud de **± 1 %** (NFPA 20, 14.2.7.1.2); contrastar los manómetros fijos de la sala.'),")
r('SBC', "'gabinetes en los hidrantes más alejados y no descargar sin boquilla, porque la lectura resulta falsa.'),",
  "'gabinetes en los hidrantes más alejados y no descargar sin boquilla, porque la lectura resulta falsa. La posición '\n"
  "                            'del tubo Pitot sigue la NFPA 13, edición 2019, A.5.2.2.'),")
r('SBC', "        ('Combustible', 'control de agua o material extraño en el tanque y verificación de que el venteo del tanque y la cañería de '\n"
         "                        'sobreflujo están desobstruidos.'),",
  "        ('Combustible', 'control de agua o material extraño en el tanque, verificación de que el venteo del tanque y la cañería de '\n"
  "                        'sobreflujo están desobstruidos y control de la cañería de combustible.'),")
r('SBC', "    a(('p', 'La verificación de interruptores o fusibles del sistema eléctrico del motor figura en la planilla de la norma con la '\n"
         "            'frecuencia «B», que se interpreta como bienal.'))",
  "    a(('p', 'La planilla IRAM 3546-12D asigna frecuencia mensual a la verificación de interruptores o fusibles del sistema '\n"
  "            'eléctrico, y la 12E les asigna la frecuencia «B». Se adopta la verificación mensual, más exigente; la «B» se interpreta '\n"
  "            'como bienal.'))")
r('SBC', "            'trabajo de la bomba. Toda modificación se debe evaluar técnicamente y registrar en la planilla de información general.'))",
  "            'trabajo de la bomba. Toda modificación se debe evaluar técnicamente y registrar en la planilla de información general. '\n"
  "            'Cuando se reemplace, cambie o modifique un componente fundamental de la bomba, del impulsor o del controlador, se debe '\n"
  "            'realizar una nueva prueba de rendimiento en campo y registrarla en la planilla SG-PEM-IFI-SBC-6 (NFPA 20, 14.5.2.1).'))")
r('SBC', "'toma de impulsión para bomberos se registran en la planilla SG-PEM-IFI-SBC-1 %s – %s.' % (NOM, PL[1]),\n",
  "'toma de impulsión para bomberos se registran en la planilla SG-PEM-IFI-SBC-1 %s – %s.' % (NOM, PL[1]),\n" + DOC)

for s in ALL:
    open(os.path.join(D, 'content_%s.py' % s), 'w', encoding='utf8').write(S[s])
print('ok', ALL)
