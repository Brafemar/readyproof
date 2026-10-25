import sys
fn = sys.argv[1] + '/content_SDI.py'
s = open(fn, encoding='utf8').read()
def r(o, n):
    global s
    assert s.count(o) == 1, (o[:80], s.count(o)); s = s.replace(o, n)

r("PL = {1: 'Información general', 2: 'Prueba mensual', 3: 'Prueba trimestral semestral anual', 4: 'Mantenimiento anual',\n      5: 'Inspección semanal (autocontrol)'}",
  "PL = {1: 'Información general', 2: 'Prueba mensual', 3: 'Prueba trimestral, semestral y anual', 4: 'Mantenimiento anual',\n      5: 'Información semanal (autocontrol)'}")
r("AVISO = ('Antes de realizar cualquier prueba, se debe notificar",
  "AVISO = ('Antes de realizar cualquier actividad de inspección o prueba que pueda generar alarmas o descargas, se deberá '\n"
  "         'notificar previamente al responsable del sistema o al servicio de monitoreo correspondiente. Además, antes de cualquier prueba se debe notificar")
r("'excesiva, pueden inspeccionarse durante las paradas programadas, con intervalos que no excedan los **18 meses**.'))",
  "'excesiva, pueden inspeccionarse durante las paradas programadas, con intervalos que no excedan los **18 meses**, si lo '\n"
  "            'aprueba la autoridad competente (NFPA 72, 14.3.2 y 14.4.4.1).'))")
r("('Dispositivos de iniciación de alarma', 'verificar el estado de los detectores de humo, de temperatura, de gas y de llama.'),",
  "('Dispositivos de iniciación de alarma', 'verificar el estado de los detectores de humo, de temperatura, de gas y de llama, de '\n"
  "                                              'las barreras infrarrojas y de los sistemas aspiradores.'),")
r("        ('Eventos repetidos', 'verificar los eventos repetidos del mes registrados en el panel.'),",
  "        ('Eventos repetidos', 'verificar los eventos repetidos del mes registrados en el panel.'),\n"
  "        ('Fuentes de energía', 'verificar que el sistema se halla alimentado con tensión primaria y secundaria.'),\n"
  "        ('Cableado', 'registrar las zonas con falla y las zonas conectadas.'),\n"
  "        ('Señales de otros sistemas', 'verificar la indicación de nivel del tanque de agua, de los detectores de flujo, de baja '\n"
  "                                      'presión en la red de cañerías y de arranque de bomba.'),\n"
  "        ('Componentes', 'verificar que todos los componentes se encuentran incrustados y ensamblados en alineación.'),\n"
  "        ('Registro de eventos', 'verificar las planillas de eventos ocurridos durante la semana.'),")
r("    a(('h4', 'Inspección semestral'))",
  "    a(('h4', 'Inspección trimestral'))\n"
  "    a(('p', 'Las inspecciones trimestrales tienen como finalidad verificar los dispositivos que requieren un control más frecuente '\n"
  "            'según la NFPA 72, Tabla 14.3.1.'))\n"
  "    a(('p', 'Durante esta inspección se debe verificar:'))\n"
  "    a(('items', [\n"
  "        ('Detectores de energía radiante (llama)', 'verificar que ningún punto que requiera detección esté obstruido o fuera del '\n"
  "                                                   'campo visual del detector.'),\n"
  "        ('Dispositivos de señales de supervisión', 'verificar su ubicación y condición.'),\n"
  "        ('Sensores de flujo de agua', 'verificar su ubicación y condición.'),\n"
  "    ]))\n"
  "    a(('p', compl(3)))\n\n"
  "    a(('h4', 'Inspección semestral'))")
r("        ('Equipos de comunicación de emergencia por voz', 'verificar su ubicación y condición.'),\n    ]))",
  "        ('Equipos de comunicación de emergencia por voz', 'verificar su ubicación y condición.'),\n"
  "        ('Dispositivos electromecánicos de descarga e interruptores de sistemas de extinción', 'verificar su ubicación y condición.'),\n"
  "        ('Interfaz de funciones de control de emergencia', 'verificar su ubicación y condición.'),\n"
  "        ('Aparatos de notificación audible textual', 'verificar su ubicación y condición.'),\n"
  "    ]))")
r("                                                                                  'estado operativo normal.'),\n    ]))",
  "                                                                                  'estado operativo normal.'),\n"
  "        ('Transmisores al servicio de monitoreo', 'verificar la ubicación, la condición física y la condición normal de los '\n"
  "                                                  'comunicadores.'),\n"
  "        ('Conexiones de fibra óptica', 'verificar su ubicación y condición.'),\n"
  "        ('Tubo de muestreo de detectores en ducto', 'verificar su orientación y que se extienda dentro del conducto según el diseño.'),\n"
  "    ]))")
r("    a(('p', cierre(2)))\n    a(('protocol', ('prueba de dispositivos iniciadores', [\n        ('Detectores de humo', [",
  "    a(('p', cierre(2)))\n"
  "    a(('p', 'En la prueba mensual, los detectores se prueban según la recomendación del fabricante; la prueba funcional de todos '\n"
  "            'los detectores con humo o producto listado se realiza en la prueba anual. El protocolo siguiente se aplica en ambos casos.'))\n"
  "    a(('protocol', ('prueba de dispositivos iniciadores', [\n"
  "        ('Aislamiento de salidas', [\n"
  "            ('Paso a paso', 'identificar en la secuencia de operación las funciones de control y los sistemas de extinción comandados '\n"
  "                            'por la central; desconectar los solenoides o actuadores de descarga, o aislar las salidas según el '\n"
  "                            'fabricante, y coordinar con el responsable las funciones de control que se van a deshabilitar.'),\n"
  "            ('Justificación técnica', 'evita descargas accidentales y la interrupción de equipos críticos (NFPA 72, 14.2.6.4).'),\n"
  "            ('Criterio de aceptación', 'todas las salidas críticas aisladas y registradas antes del primer accionamiento.')]),\n"
  "        ('Detectores de humo', [")
r("        ('Restablecimiento', [",
  "        ('Detectores especiales', [\n"
  "            ('Paso a paso', 'en sistemas de muestreo de aire, probar con humo desde el extremo de cada tramo de tubería y verificar el '\n"
  "                            'flujo en los demás puertos; en detectores de ducto con tubo de muestreo, verificar el muestreo de la '\n"
  "                            'corriente de aire; en detectores de haz proyectado, introducir humo o un filtro óptico en la trayectoria.'),\n"
  "            ('Justificación técnica', 'cada tecnología requiere el método de la NFPA 72, Tabla 14.4.3.2, ítem 17(g).'),\n"
  "            ('Criterio de aceptación', 'alarma recibida en la central para cada dispositivo probado.')]),\n"
  "        ('Restablecimiento', [")
r("        ('Tensión de carga de baterías', 'con el cargador desconectado y bajo carga, verificar que las baterías de plomo-ácido no '\n"
  "                                         'caen por debajo de **2,05 V por celda** y que las de níquel-cadmio mantienen una tensión '\n"
  "                                         'de flotación nominal de **1,42 V por celda**; en baterías de plomo-ácido abiertas, medir '\n"
  "                                         'la gravedad específica y verificar que está dentro del rango del fabricante.'),",
  "        ('Tensión de carga de baterías', 'plomo-ácido abiertas: con el cargador desconectado y bajo carga, la tensión no debe caer '\n"
  "                                         'por debajo de **2,05 V por celda**, y se debe medir la gravedad específica con hidrómetro '\n"
  "                                         'de lectura numérica, dentro del rango del fabricante; plomo-ácido selladas: desempeño '\n"
  "                                         'según el fabricante; níquel-cadmio: tensión de flotación nominal de **1,42 V por celda**, '\n"
  "                                         'medida durante la carga y, si es posible, celda por celda.'),\n"
  "        ('Detectores de llama', 'probar su funcionamiento y su sensibilidad con método o instrumento calibrado; no se deben usar '\n"
  "                                'fuentes de luz que apliquen radiación no medida.'),")
r("        ('Transmisión al servicio de monitoreo', 'accionar un dispositivo iniciador, crear una condición de falla y accionar un '",
  "        ('Baterías', 'reemplazarlas según el fabricante o cuando la batería recargada no alcance la tensión o la corriente '\n"
  "                     'especificada.'),\n"
  "        ('Alimentación primaria', 'probarla con carga máxima, con todos los aparatos de notificación en funcionamiento simultáneo.'),\n"
  "        ('Señales de falla de la central', 'verificar las señales audibles y visuales de falla, la rellamada del silenciamiento y '\n"
  "                                           'los interruptores de desconexión o aislamiento.'),\n"
  "        ('Transmisión al servicio de monitoreo', 'accionar un dispositivo iniciador, crear una condición de falla y accionar un '")
r("            ('Paso a paso', 'reconectar la alimentación primaria, restablecer la central y notificar la conclusión de la prueba.'),",
  "            ('Paso a paso', 'reconectar la alimentación primaria, restablecer la central y notificar la conclusión de la prueba; '\n"
  "                            'registrar la tensión de reposo y verificar la recarga completa en el tiempo indicado por el fabricante, '\n"
  "                            'informando al responsable que la autonomía queda reducida durante ese período.'),")
r("        ('Detectores de humo y temperatura', 'limpieza y calibración o verificación.'),\n"
  "        ('Detectores de gas', 'limpieza y calibración o verificación según el fabricante.'),",
  "        ('Detectores de humo y temperatura', 'limpieza y calibración o verificación (**8,3 %**, según la planilla IRAM 3546-6E).'),\n"
  "        ('Detectores de gas', 'limpieza y calibración o verificación según el fabricante (**8,3 %**, según la planilla IRAM 3546-6E).'),")
r("            'secuencia de operación.'))",
  "            'secuencia de operación. Todo dispositivo agregado se debe probar; después de cambios en el software del sitio se deben '\n"
  "            'probar el **100 %** de las funciones afectadas y el **10 %** de los dispositivos iniciadores no afectados, hasta un '\n"
  "            'máximo de **50** (NFPA 72, 14.4.2.1 y 14.4.2.4).'))")
r("        'Los registros se deben conservar, como mínimo, hasta la prueba siguiente y durante un año a partir de entonces; los de '\n"
  "        'detectores de temperatura restaurables probados en forma rotativa, durante cinco años y un año más, según la %s.' % N72,",
  "        'Estos registros aseguran la trazabilidad de las actividades, permiten verificar el estado operativo del sistema, facilitan '\n"
  "        'las auditorías técnicas y normativas e identifican tendencias de fallas o necesidades de mantenimiento.',\n"
  "        'Los registros se deben conservar como mínimo durante **tres años**, según la IRAM 3546:2011; los de los detectores de '\n"
  "        'temperatura restaurables probados en forma rotativa, durante el ciclo completo de cinco años más un año, según la %s, '\n"
  "        '14.6.2, por ser ese plazo mayor.' % N72,")
open(fn, 'w', encoding='utf8').write(s); print('SDI ok')
