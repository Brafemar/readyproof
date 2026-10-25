# -*- coding: utf-8 -*-
"""SG-PEM-IFI-SIM · Simbología de Seguridad contra Incendios (NFPA 170, capítulos 4, 6, 7, 8 y 11).
En las tablas, '§sym:clave§' se reemplaza por el símbolo redibujado (tools/simbolos.py) con tools/insert_symbols.py."""
SIG, NOM, NOMU, CAP = 'SIM', 'Simbología de Seguridad contra Incendios', 'SIMBOLOGÍA DE SEGURIDAD CONTRA INCENDIOS Y EMERGENCIAS', '-'
PL = {1: 'Verificación de simbología en planos', 2: 'Verificación de diagramas de evacuación'}
SIN_INFORME = True
RETENCION = True
N170 = 'NFPA 170'
VIG = (' Se aplica la edición vigente de la NFPA 170; la numeración de los artículos y tablas citados se debe confirmar en esa '
       'edición, porque puede variar entre ediciones.')
H = ['Símbolo', 'Descripción', 'Uso en la serie SG-PEM-IFI / observaciones']
def T(*rows): return ('table', [H] + [['§sym:%s§' % k, d, o] for k, d, o in rows])


def CONTENT(cierre):
    C = []; a = C.append
    a(('h2', NOMU))
    a(('basado', '(Basado en NFPA 170 – Capítulos 4, 6, 7, 8 y 11 y Anexo A)'))
    a(('p', 'Este apartado establece los criterios para representar las instalaciones fijas contra incendio, los medios de egreso y '
            'los equipos de emergencia en planos, diagramas y planos de evacuación, con el objetivo de que toda la documentación '
            'gráfica emitida o verificada por la empresa utilice una simbología uniforme, comprensible para el personal técnico, '
            'los usuarios, los servicios de emergencia y las aseguradoras.'))
    a(('p', 'La NFPA 170 tiene por finalidad normalizar los símbolos utilizados para representar la seguridad contra incendio, '
            'las emergencias y los riesgos asociados (NFPA 170, 1.1 y 1.2). El presente procedimiento adopta esos símbolos y los '
            'complementa con las reglas de presentación de la norma y con los criterios de verificación de la serie SG-PEM-IFI.' + VIG))
    a(('p', 'Los símbolos de las tablas de este procedimiento fueron redibujados por la empresa siguiendo la geometría definida en '
            'la NFPA 170, para asegurar una presentación uniforme en todos los documentos. Los pictogramas de señalización del '
            'capítulo 4 de la norma, como la salida de emergencia o el pulsador de alarma, no se reproducen: se describen con su '
            'campo, sus colores y su aplicación, y en las señales se deben utilizar los pictogramas de la edición vigente de la '
            'norma o de señales que la cumplan.'))
    a(('p', 'La documentación alcanzada incluye:'))
    a(('items', [
        ('Planos de instalación', 'planos de los sistemas de abastecimiento de agua, rociadores, extinción, detección y alarma, '
                                  'emitidos para la instalación, la modificación o el relevamiento.'),
        ('Planos conforme a obra', 'planos que representan la instalación existente y que se verifican en las inspecciones '
                                   'anuales de planimetría de los procedimientos de la serie.'),
        ('Diagramas para análisis de riesgo y seguros', 'diagramas de sitio y de edificio utilizados para evaluar el riesgo '
                                                        'y la protección de una instalación.'),
        ('Diagramas y planos de evacuación', 'planos colocados dentro del edificio que muestran las vías de evacuación y la '
                                             'ubicación del equipamiento de emergencia.'),
    ]))

    # ---------------- 3.1.1 ----------------
    a(('h3', 'CRITERIOS GENERALES DE REPRESENTACIÓN'))
    a(('p', 'Los criterios generales de representación tienen como finalidad que cada símbolo conserve el mismo significado en '
            'cualquier plano o diagrama, sin importar quién lo confeccione.'))
    a(('p', 'En todo plano o diagrama se debe asegurar:'))
    a(('items', [
        ('Forma del símbolo', 'la forma de cada símbolo debe ser la indicada en las tablas de este procedimiento, sin modificar '
                              'su contorno ni su relleno (NFPA 170, 6.1.2.1, 7.1.2.1 y 8.1.2.1).'),
        ('Líneas tramadas', 'las líneas tramadas que acompañan a un símbolo no forman parte de él: representan la cañería, el '
                            'cableado o la superficie de montaje asociados (NFPA 170, 7.1.2.2 y 8.1.2.2).'),
        ('Escala', 'todos los símbolos de un mismo plano deben tener el mismo tamaño relativo (NFPA 170, 7.1.2.3 y 8.1.2.3).'),
        ('Orientación', 'los símbolos se deben orientar según el muro, la cañería o la línea eléctrica a la que están fijados '
                        '(NFPA 170, 7.1.2.4 y 8.1.2.4). La orientación de los símbolos de prohibición no se debe alterar '
                        '(NFPA 170, 4.1.3.1).'),
        ('Indicadores complementarios', 'la eficacia de un símbolo se puede completar con cifras, números, subíndices o '
                                        'abreviaturas, colocados dentro del símbolo o junto a él (NFPA 170, 3.3.5).'),
        ('Leyenda', 'se recomienda que cada conjunto de documentos en el que se utilicen indicadores complementarios vaya '
                    'acompañado de una leyenda con su significado (NFPA 170, A.3.3.5); en el presente procedimiento la leyenda '
                    'es obligatoria.'),
        ('Cajetín', 'el plano debe identificar la empresa, la persona que lo confeccionó y su fecha, y el nombre y la ubicación '
                    'de la instalación, e incluir la flecha de norte orientada según los edificios representados y la escala o la '
                    'leyenda «sin escala»; si se van a hacer copias reducidas, la escala se indica con una barra gráfica '
                    '(NFPA 170, A.6.1.2).'),
        ('Edificios', 'los muros exteriores se dibujan con línea simple, o con línea doble si tienen resistencia al fuego; el '
                      'perímetro de aleros, muelles de carga y otras estructuras abiertas se dibuja con línea de trazos '
                      '(NFPA 170, 6.2.1.1 y 6.2.1.2).'),
        ('Rociadores', 'la temperatura de actuación y las demás características de los rociadores se indican en la leyenda o '
                       'mediante notas en el plano, por ejemplo «todos los rociadores son de la misma temperatura salvo '
                       'indicación» (NFPA 170, 7.6.2.1 y A.7.6.2.1).'),
        ('Subíndices adicionales', 'se pueden agregar subíndices con una barra después del subíndice principal, por ejemplo WP '
                                   'para equipos a la intemperie o EP para equipos a prueba de explosión (NFPA 170, A.8.3).'),
    ]))
    a(('p', 'La escala de dibujo, los espesores de línea y los demás aspectos de presentación que la NFPA 170 no define se rigen '
            'por las normas de dibujo técnico aplicables (NFPA 170, A.6.1.2.1).'))

    # ---------------- 3.1.2 ----------------
    a(('h3', 'SÍMBOLOS PARA AGUA, ROCIADORES Y SISTEMAS DE EXTINCIÓN'))
    a(('p', 'Estos símbolos se utilizan en los planos de abastecimiento de agua, de los sistemas de extinción y de los rociadores, '
            'y en los diagramas para seguros (NFPA 170, capítulo 7).'))
    a(('h4', 'Abastecimiento y distribución de agua'))
    a(('p', 'Los símbolos de abastecimiento y distribución de agua son los de la Tabla 7.2 de la NFPA 170. Los elementos de los '
            'símbolos de hidrantes se pueden combinar según el tipo de hidrante (NFPA 170, A.7.2).'))
    a(T(('riser', 'Montante (riser).', 'Rociadores y redes de agua.'),
        ('riser_humedo', 'Montante húmedo.', 'Red húmeda.'),
        ('riser_seco', 'Montante seco.', 'Cañería seca: SRA, STM, SAP y SRE.'),
        ('riser_accion_previa', 'Montante de acción previa.', 'Sistemas de acción previa.'),
        ('valvula', 'Válvula, forma básica.', 'Indicar el diámetro de la válvula.'),
        ('valvula_osy', 'Válvula de vástago ascendente (OS&Y).', 'Indicar el diámetro.'),
        ('valvula_mariposa_ind', 'Válvula mariposa con indicador.', 'Indicar el diámetro.'),
        ('retencion', 'Válvula de retención.', 'Indicar diámetro y sentido de flujo.'),
        ('bomba', 'Bomba contra incendio con su impulsor.', 'SBC. Indicar el tipo de impulsor y la capacidad nominal.'),
        ('bomberos_simple', 'Conexión simple para bomberos.', 'Indicar tipo, diámetro, rosca y ángulo.'),
        ('bomberos_siamesa', 'Conexión siamesa para bomberos.', 'Indicar tipo, diámetro y ángulo.'),
        ('hidrante_privado', 'Hidrante privado, una salida.', 'SHC. Indicar diámetro, tipo de rosca o conexión.'),
        ('hidrante_publico', 'Hidrante público, dos salidas.', 'SHC. Indicar diámetro, tipo de rosca o conexión.'),
        ('medidor', 'Medidor.', 'Indicar el tipo.')))
    a(('h4', 'Tipos de sistemas de extinción'))
    a(('p', 'Estos símbolos identifican el tipo de sistema instalado para proteger un área (NFPA 170, A.7.6). En la NFPA 170, el '
            'contorno circular corresponde al sistema de actuación automática y el contorno cuadrado, al de actuación manual '
            '(Tablas 7.6.1.1 a 7.6.1.3).'))
    a(T(('sis_humedo_auto', 'Sistema húmedo, actuación automática.', 'SRA. Rociadores de cañería húmeda.'),
        ('sis_humedo_manual', 'Sistema húmedo, actuación manual.', ''),
        ('sis_seco_auto', 'Sistema seco, actuación automática, con aire.', 'SRA de tubería seca y SAP con cañería seca.'),
        ('sis_accion_previa_auto', 'Sistema seco de acción previa, actuación automática, con aire.', ''),
        ('sis_espuma_auto', 'Sistema de espuma, actuación automática.', 'SRE y SGE.'),
        ('sis_espuma_manual', 'Sistema de espuma, actuación manual.', 'SRE y SGE.'),
        ('sis_niebla_auto', 'Sistema de agua nebulizada, actuación automática.', ''),
        ('sis_polvo_auto', 'Sistema de polvo para fuegos de todo tipo (excepto metales), automático.', 'SEP.'),
        ('sis_polvo_manual', 'Sistema de polvo para fuegos de todo tipo (excepto metales), manual.', 'SEP.'),
        ('sis_co2_auto', 'Sistema de dióxido de carbono, actuación automática.', 'SDC.'),
        ('sis_agente_limpio_auto', 'Sistema de halón o de agente limpio, actuación automática.', 'SAL.'),
        ('sis_agente_limpio_manual', 'Sistema de halón o de agente limpio, actuación manual.', 'SAL.'),
        ('sup_rociado_total', 'Espacio totalmente protegido por rociadores.', 'Símbolo complementario.'),
        ('sup_no_rociado', 'Espacio sin rociadores.', 'Símbolo complementario.'),
        ('sup_agua_pulverizada', 'Sistema de agua pulverizada.', 'SAP. Símbolo complementario.')))
    a(('h4', 'Rociadores, cañerías y válvulas'))
    a(('p', 'Los símbolos de rociadores son los de la Tabla 7.6.2 y los de cañerías, válvulas y dispositivos de control, los de '
            'la Tabla 7.6.3 de la NFPA 170.'))
    a(T(('rociador_montante', 'Rociador montante (upright).', 'SRA. Indicar la temperatura en la leyenda.'),
        ('rociador_colgante', 'Rociador colgante (pendent).', 'SRA. Anotar «DP» si es colgante seco.'),
        ('rociador_lateral', 'Rociador de pared (sidewall).', 'SRA.'),
        ('rociador_abierto_montante', 'Rociador abierto montante.', 'SRA de diluvio.'),
        ('rociador_abierto_colgante', 'Rociador abierto colgante.', 'SRA de diluvio.'),
        ('boquilla_pulverizadora', 'Boquilla de agua pulverizada.', 'SAP.'),
        ('cano_rociadores', 'Cañería de rociadores y ramal.', 'Indicar el diámetro.'),
        ('soporte_cano', 'Soporte de cañería.', 'Trazo diagonal sobre la cañería soportada.'),
        ('valvula_alarma', 'Válvula de retención y alarma.', 'Indicar el diámetro.'),
        ('valvula_tubo_seco', 'Válvula de cañería seca.', 'Indicar el diámetro.'),
        ('valvula_diluvio', 'Válvula de diluvio.', 'SRA y SAP. Indicar diámetro y tipo.'),
        ('valvula_accion_previa', 'Válvula de acción previa.', 'Indicar diámetro y tipo.'),
        ('valvula_control_piso', 'Conjunto de válvula de control de piso o de zona.', 'Indicar el diámetro.')))
    a(('h4', 'Extintores y equipos de lucha contra incendio'))
    a(('p', 'Los símbolos de extintores portátiles son los de la Tabla 7.7, los de equipos de lucha contra incendio los de la '
            'Tabla 7.8 y los recipientes de agente los de la Tabla 7.9 de la NFPA 170.'))
    a(T(('extintor', 'Extintor portátil, forma básica.', 'Agua: misma forma básica.'),
        ('extintor_espuma', 'Extintor de espuma.', ''),
        ('extintor_polvo_bc', 'Extintor de polvo para fuegos de líquidos, gases y eléctricos (BC).', ''),
        ('extintor_polvo_abc', 'Extintor de polvo para fuegos de todo tipo excepto metales (ABC).', ''),
        ('extintor_co2', 'Extintor de dióxido de carbono.', ''),
        ('extintor_agente_limpio', 'Extintor de halón o de agente limpio.', ''),
        ('extintor_metales', 'Extintor para fuegos de metales.', ''),
        ('equipo_lucha', 'Equipo de lucha contra incendio, forma básica.', ''),
        ('gabinete_manguera_humedo', 'Estación de manguera, columna húmeda.', 'STM. Bocas de incendio equipadas.'),
        ('boca_incendio', 'Conexión de válvula de manguera.', 'STM. Indicar la rosca.'),
        ('recipiente_agente_limpio', 'Recipiente de agente limpio.', 'SAL. Indicar tipo de agente y montaje.'),
        ('recipiente_co2', 'Recipiente de dióxido de carbono.', 'SDC. Indicar alta o baja presión.'),
        ('recipiente_polvo', 'Recipiente de polvo químico.', 'SEP.'),
        ('recipiente_quimico_humedo', 'Recipiente de agente químico húmedo.', 'SSA.'),
        ('recipiente_espuma', 'Recipiente de espuma.', 'SRE y SGE.'),
        ('fusible', 'Eslabón fusible.', 'Indicar la temperatura en grados. SSA.')))

    # ---------------- 3.1.3 ----------------
    a(('h3', 'SÍMBOLOS PARA DETECCIÓN, ALARMA Y NOTIFICACIÓN'))
    a(('p', 'Estos símbolos se utilizan en los planos de los sistemas de detección y alarma, de notificación y de control de humo, '
            'y en el disparo de los sistemas de extinción (NFPA 170, capítulo 8).'))
    a(('h4', 'Centrales y equipos de control'))
    a(('p', 'La forma básica de las centrales y los equipos de control es un rectángulo con la abreviatura del equipo '
            '(NFPA 170, Tabla 8.2). En las centrales de descarga, el subíndice indica el tipo de agente, por ejemplo CA para '
            'agente limpio, DC para polvo químico, FO para espuma o WC para agente químico húmedo.'))
    a(T(('central_facu', 'Unidad de control de alarma de incendio (FACU).', 'SDI. Agregar el subíndice D si es dedicada.'),
        ('anunciador_faa', 'Anunciador de alarma de incendio (FAA).', 'SDI.'),
        ('central_descarga', 'Unidad de control de servicio de descarga (RSFACU).', 'SAL, SDC, SEP, SSA, SRE y SGE con subíndice.'),
        ('controlador_bomba', 'Controlador de bomba contra incendio (FPC).', 'SBC.'),
        ('interfaz_central', 'Interfaz de la central de alarma (FACI).', ''),
        ('panel_sirenas_aux', 'Fuente o panel extensor de circuitos de notificación (NAC).', 'Agregar el número de unidad.'),
        ('dact', 'Transmisor comunicador digital de alarma (DACT).', 'Transmisión al servicio de monitoreo.'),
        ('fuente_ups', 'Fuente de alimentación ininterrumpida (UPS).', '')))
    a(('h4', 'Dispositivos iniciadores y de supervisión'))
    a(('p', 'La forma básica de los dispositivos de detección automática y de supervisión es un hexágono; la orientación del '
            'símbolo del detector de humo no se debe modificar (NFPA 170, Tabla 8.3). La letra interior indica el principio de '
            'detección, S para humo y H para temperatura, y el subíndice, el tipo. En los detectores de temperatura se puede '
            'indicar la temperatura de actuación, y en los detectores de gas se debe indicar el gas monitoreado y, cuando '
            'corresponda, los límites inferior o superior de explosividad (NFPA 170, A.8.3).'))
    a(T(('detector_humo', 'Detector o sensor de humo, forma básica.', 'SDI.'),
        ('detector_humo_fotoelectrico', 'Detector de humo fotoeléctrico.', ''),
        ('detector_humo_ionico', 'Detector de humo iónico.', ''),
        ('detector_humo_aspiracion', 'Detector de humo por aspiración (muestreo de aire).', ''),
        ('detector_haz_emisor', 'Detector de humo de haz proyectado, emisor.', ''),
        ('detector_haz_receptor', 'Detector de humo de haz proyectado, receptor.', ''),
        ('detector_ducto', 'Detector de humo para conducto.', 'Se puede indicar la velocidad del aire.'),
        ('detector_temp', 'Detector o sensor de temperatura.', 'Se puede indicar la temperatura de actuación.'),
        ('detector_temp_fija', 'Detector de temperatura fija.', ''),
        ('detector_temp_termovelocimetrico', 'Detector termovelocimétrico (solo velocidad de aumento).', ''),
        ('detector_temp_combinado', 'Detector combinado termovelocimétrico y de temperatura fija.', ''),
        ('detector_llama', 'Detector de llama, forma básica.', 'Subíndice: tipo de detección.'),
        ('detector_llama_uvir', 'Detector de llama ultravioleta e infrarrojo.', ''),
        ('detector_gas', 'Detector de gas, forma básica.', 'Subíndice: tipo de gas.'),
        ('detector_co', 'Detector de monóxido de carbono.', ''),
        ('avisador_manual', 'Avisador manual de alarma de incendio.', 'SDI.'),
        ('avisador_manual_descarga', 'Avisador manual de sistema de extinción (ejemplo: agente limpio).', 'SAL. Letras según el agente.'),
        ('aborto', 'Interruptor de aborto.', 'SAL y SDC.'),
        ('descarga_manual', 'Estación de descarga manual.', 'SAL, SDC, SEP y SSA.'),
        ('flujo_ws', 'Detector o interruptor de flujo.', 'Redes de rociadores.'),
        ('supervisor_valvula', 'Interruptor de supervisión de válvula.', ''),
        ('presostato', 'Detector o interruptor de presión.', 'SBC y sistemas presurizados.'),
        ('nivel', 'Detector o interruptor de nivel.', 'SAA. Tanques de reserva.'),
        ('valvula_solenoide', 'Válvula solenoide.', 'Disparo de sistemas de extinción.'),
        ('modulo_entrada', 'Módulo direccionable de monitoreo de entrada.', ''),
        ('modulo_salida', 'Módulo direccionable de control de salida.', ''),
        ('modulo_aislador', 'Módulo aislador.', '')))
    a(('h4', 'Aparatos de notificación y equipos relacionados'))
    a(('p', 'Los símbolos de los aparatos de notificación son los de la Tabla 8.4.2, y los de los equipos relacionados, los de la '
            'Tabla 8.5 de la NFPA 170. A los aparatos de notificación se les aplican, cuando sea necesario para aclarar el plano, '
            'los subíndices de la Tabla 8.4.1.'))
    a(T(('sirena', 'Bocina (solo sonido).', ''),
        ('campana', 'Campana vibratoria.', ''),
        ('sirena_luz', 'Combinación bocina y señal visible.', 'CD: intensidad o ajuste en candelas.'),
        ('luz_estroboscopica_pared', 'Señal visible (estroboscópica), montaje en pared.', 'CD: intensidad o ajuste en candelas.'),
        ('altavoz', 'Altavoz, montaje en pared.', 'Indicar la derivación de potencia.'),
        ('telefono_bomberos', 'Estación telefónica de bomberos o de emergencia.', ''),
        ('retenedor_puerta', 'Retenedor de puerta.', 'Función de control del SDI.'),
        ('caja_paso', 'Caja de paso.', ''),
        ('resistencia_fin_linea', 'Resistencia de fin de línea.', 'SDI.')))
    a(('table', [['Subíndice', 'Significado', 'Subíndice / significado'],
                 ['C', 'Montaje en cielorraso', 'P: colgante'],
                 ['H', 'Ajuste sonoro alto', 'RI: indicador remoto'],
                 ['L', 'Ajuste sonoro bajo', 'SL: luz de señal'],
                 ['MNS', 'Sistema de notificación masiva', 'nW: ajuste de potencia (n = derivación del altavoz)'],
                 ['WP', 'Apto para intemperie', 'WG: con protector de alambre']]))

    # ---------------- 3.1.4 ----------------
    a(('h3', 'SÍMBOLOS DE MEDIOS DE EGRESO, CLASES DE FUEGO Y SEÑALIZACIÓN'))
    a(('p', 'Estos símbolos permiten representar las vías de evacuación y el equipamiento de emergencia, e identificar la clase de '
            'fuego para la que es apto cada extintor.'))
    a(('h4', 'Medios de egreso y equipos de emergencia'))
    a(('p', 'Los símbolos de los medios de egreso son los de las Tablas 6.3.4 y 7.4 de la NFPA 170, y el del desfibrilador, el '
            'de la Tabla 6.3.6.'))
    a(T(('salida', 'Salida.', 'Línea negra, ancha y continua.'),
        ('acceso_salida', 'Acceso a la salida.', 'Línea negra, ancha y de trazos.'),
        ('descarga_salida', 'Descarga de la salida.', 'Línea negra, ancha y de trazos cortos.'),
        ('puerta_cortafuego', 'Puerta cortafuego (ejemplo: resistencia de 1 h).', 'La cantidad de rombos indica la resistencia.'),
        ('ascensor', 'Ascensor en hueco no combustible.', ''),
        ('luz_emergencia', 'Luz de emergencia con batería.', 'Indicar la cantidad de lámparas.'),
        ('cartel_salida', 'Cartel de salida iluminado, una cara.', 'Indicar el sentido de circulación.'),
        ('dea', 'Ubicación de desfibrilador externo automático (DEA).', '')))
    a(('h4', 'Clases de fuego'))
    a(('p', 'Los extintores aptos para cada clase de fuego se identifican con la letra de la clase dentro de una figura. Si se '
            'utiliza color, el triángulo es verde, el cuadrado rojo, el círculo azul y la estrella amarilla (NFPA 170, Figura '
            '4.3(b)). La NFPA 170 presenta además un sistema de pictogramas para las clases A, B, C, D y K (Figura 4.3(a)), que '
            'se aplica según la edición vigente de la norma.'))
    a(T(('clase_a', 'Clase A: combustibles comunes.', 'Triángulo, verde si se colorea.'),
        ('clase_b', 'Clase B: líquidos inflamables.', 'Cuadrado, rojo si se colorea.'),
        ('clase_c', 'Clase C: equipos eléctricos.', 'Círculo, azul si se colorea.'),
        ('clase_d', 'Clase D: metales combustibles.', 'Estrella de cinco puntas, amarilla si se colorea.')))
    a(('h4', 'Señales de uso general'))
    a(('p', 'Las señales de uso general se diseñan para ayudar a localizar las salidas, el equipamiento de alerta y las áreas '
            'seguras. Su imagen, su color y la forma de su fondo son los que define la NFPA 170, y su color debe cumplir la ANSI '
            'Z535.1 (NFPA 170, 4.1.2.2, 4.1.2.3 y 4.1.3.3). Para los símbolos de prohibición se usa un círculo con una barra '
            'diagonal a 45°, desde arriba a la izquierda hacia abajo a la derecha (NFPA 170, 4.1.3.2.1). Los símbolos se pueden '
            'combinar, en forma vertical u horizontal, en la misma señal o en señales contiguas (NFPA 170, 4.1.3.4).'))
    a(('table', [['Señal', 'Campo y colores', 'Aplicación'],
                 ['Salida de emergencia', 'Campo cuadrado, fondo verde, vano de puerta blanco, figura en verde.', 'Identificar y ubicar una salida de emergencia.'],
                 ['Salida de emergencia con flecha', 'Campo rectangular. Pintada: fondo blanco, flechas rojas o negras. Retroiluminada: vano, flechas y letras verdes o rojas.', 'Indicar el recorrido hacia una salida.'],
                 ['No es salida', 'Campo circular, símbolo de prohibición rojo, fondo blanco.', 'Puertas que no conducen a una salida.'],
                 ['Use la escalera en caso de incendio', 'Campo cuadrado, llama roja, figura negra, fondo blanco.', 'Indicar el uso de la escalera.'],
                 ['No use el ascensor en caso de incendio', 'Campo rectangular, llama roja, figuras negras, círculo y barra rojos.', 'Junto al botón de llamada del ascensor.'],
                 ['Avisador manual de alarma', 'Campo rectangular, fondo rojo, llama, mano, caja y bocina blancas.', 'Sobre los avisadores manuales.'],
                 ['Extintor', 'Campo cuadrado, fondo rojo, símbolo blanco.', 'Ubicación de extintores.'],
                 ['Manguera o boca de incendio', 'Campo cuadrado, fondo rojo, símbolo blanco.', 'Ubicación de bocas de incendio.'],
                 ['Área de refugio', 'Campo cuadrado, fondo blanco, llama roja.', 'Área de refugio designada.'],
                 ['Desfibrilador (DEA)', 'Campo cuadrado, fondo blanco, corazón rojo con rayo blanco, letras negras.', 'Ubicación de desfibriladores.'],
                 ['Prohibido el uso de llama abierta / fumar', 'Campo circular, círculo y barra rojos, imagen negra, fondo blanco.', 'Áreas con prohibición.']]))

    # ---------------- 3.1.5 ----------------
    a(('h3', 'DIAGRAMAS Y PLANOS DE EVACUACIÓN'))
    a(('p', 'Los diagramas y planos de evacuación colocados dentro del edificio muestran las vías de evacuación y la ubicación del '
            'equipamiento de emergencia, e informan a los ocupantes cómo reportar una emergencia y cuándo evacuar hacia el '
            'punto de reunión exterior, un área de refugio o de asistencia para el rescate o un refugio designado, cuándo '
            'permanecer en el lugar o qué combinación de esas opciones aplicar (NFPA 170, 11.1).'))
    a(('p', 'Todo diagrama o plano de evacuación debe cumplir:'))
    a(('items', [
        ('Composición', 'clara y simple, que los ocupantes puedan comprender rápidamente; para evitar barreras de idioma se '
                        'deben usar representaciones gráficas y símbolos (NFPA 170, 11.2.1).'),
        ('Salidas', 'mostrar como mínimo dos salidas desde el lugar donde está colocado y, según la NFPA 101, la planta completa; '
                    'si no es posible, incluir un plano de ubicación que destaque el área representada (NFPA 170, 11.2.2 y '
                    'A.11.2.2).'),
        ('Leyenda', 'usar los símbolos de la NFPA 170 e incluir una leyenda que explique su significado (NFPA 170, 11.2.3).'),
        ('Tamaño', 'el texto, los símbolos y la información deben ser visibles para todos los ocupantes (NFPA 170, 11.2.4).'),
        ('Ubicación', 'a una altura que permita verlo a todos los ocupantes, en lugares por los que pasen todos los empleados y '
                      'visitantes durante su permanencia en el edificio (NFPA 170, 11.2.5).'),
        ('Orientación', 'orientado con la parte superior en la dirección hacia la que mira el observador (NFPA 170, 11.3.1).'),
        ('Usted está aquí', 'indicar la ubicación y la orientación del observador con la notación «usted está aquí», apuntando '
                            'hacia arriba, hacia el lugar del cartel; debe ser el gráfico dominante del diagrama (NFPA 170, '
                            '11.3.2).'),
        ('Medios de egreso', 'mostrar todas las salidas, accesos a salidas, escaleras, ascensores y sus vestíbulos, áreas de '
                             'refugio y de asistencia para el rescate, refugios y puntos de reunión exteriores (NFPA 170, '
                             '11.4.1.1).'),
        ('Equipamiento de emergencia', 'mostrar en la leyenda los avisadores manuales, los teléfonos de emergencia, los '
                                       'desfibriladores, los extintores, si los ocupantes están capacitados para usarlos, y '
                                       'el resto del equipamiento de emergencia propio del edificio (NFPA 170, 11.4.1.2).'),
        ('Información adicional', 'solo si no confunde al observador durante una emergencia (NFPA 170, 11.4.1).'),
        ('Teléfonos', 'los números telefónicos de emergencia (NFPA 170, 11.4.2).'),
        ('Instrucciones', 'las pautas de evacuación, con las distintas señales de alerta y qué hacer cuando suenan; si no hay '
                          'señales, cómo se instruirá a los ocupantes (NFPA 170, 11.4.3).'),
        ('Materiales', 'resistentes a la decoloración y al desgaste; pueden ser fotoluminiscentes o autoluminosos siempre que '
                       'no requieran carga eléctrica para mantener la luminiscencia, y deben cumplir la ASTM E2072 y la ASTM '
                       'E2073, o la ANSI/UL 1994 (NFPA 170, 11.5 y 11.5.1).'),
    ]))
    a(('p', 'Para las notaciones que la NFPA 170 exige sin fijarles un gráfico se utilizan los símbolos de diseño propio de la '
            'empresa de la tabla siguiente.'))
    a(T(('usted_esta_aqui', 'Usted está aquí.', 'Diseño propio para la notación del 11.3.2. Gráfico dominante del diagrama.'),
        ('norte', 'Flecha de norte.', 'Diseño propio (NFPA 170, A.6.1.2).'),
        ('punto_reunion', 'Punto de reunión exterior.', 'Diseño propio; la NFPA 170 lo exige sin fijar su gráfico (11.4.1.1).')))
    a(('p', cierre(2)))
    a(('protocol', ('verificación del diagrama de evacuación en el lugar', [
        ('Ubicación y altura', [
            ('Paso a paso', 'recorrer los accesos y las circulaciones principales y verificar que el diagrama se ve desde los lugares '
                            'por los que pasan todos los empleados y visitantes, a una altura visible para todos los ocupantes.'),
            ('Justificación técnica', 'un diagrama fuera del recorrido habitual no informa a los ocupantes antes de la emergencia.'),
            ('Criterio de aceptación', 'diagrama visible en el recorrido de todos los ocupantes (NFPA 170, 11.2.5).')]),
        ('Orientación', [
            ('Paso a paso', 'pararse frente al diagrama y comparar la dirección «hacia arriba» del plano con la dirección hacia la '
                            'que mira el observador; verificar que la notación «usted está aquí» coincide con la ubicación real del '
                            'cartel.'),
            ('Justificación técnica', 'un plano rotado obliga al ocupante a reinterpretarlo y puede llevarlo en la dirección '
                                      'equivocada.'),
            ('Criterio de aceptación', 'parte superior en la dirección de la vista y «usted está aquí» como gráfico dominante '
                                       '(NFPA 170, 11.3.1 y 11.3.2).')]),
        ('Vías de evacuación', [
            ('Paso a paso', 'recorrer desde el diagrama las dos salidas representadas, como mínimo, y verificar que existen, que '
                            'están libres y que el recorrido coincide con el dibujado.'),
            ('Justificación técnica', 'el diagrama solo es útil si representa la condición real del edificio.'),
            ('Criterio de aceptación', 'dos salidas como mínimo, coincidentes con el edificio (NFPA 170, 11.2.2 y 11.4.1.1).')]),
        ('Equipamiento y leyenda', [
            ('Paso a paso', 'comprobar que cada avisador manual, teléfono de emergencia, desfibrilador y extintor representado está '
                            'en el lugar indicado y que todos los símbolos usados figuran en la leyenda.'),
            ('Justificación técnica', 'un equipo mal ubicado en el plano demora su uso durante la emergencia.'),
            ('Criterio de aceptación', 'equipamiento coincidente y leyenda completa (NFPA 170, 11.2.3 y 11.4.1.2).')]),
        ('Información y material', [
            ('Paso a paso', 'verificar los teléfonos de emergencia, las pautas de evacuación y el estado del material: legibilidad, '
                            'decoloración, desgaste y, si es fotoluminiscente, la carga por luz ambiente.'),
            ('Justificación técnica', 'un número telefónico desactualizado o un diagrama ilegible anulan su función.'),
            ('Criterio de aceptación', 'información vigente y material sin decoloración ni desgaste (NFPA 170, 11.4.2, 11.4.3 y '
                                       '11.5).')]),
    ])))

    # ---------------- 3.1.6 ----------------
    a(('h3', 'VERIFICACIÓN DE PLANOS Y DIAGRAMAS'))
    a(('p', 'La verificación de los planos y diagramas tiene como finalidad asegurar que la documentación gráfica represente la '
            'instalación existente con la simbología de este procedimiento.'))
    a(('p', 'La verificación se debe realizar:'))
    a(('items', [
        ('Primera intervención', 'en el relevamiento inicial de la instalación, junto con la planilla de información general del '
                                 'procedimiento SG-PEM-IFI del sistema.'),
        ('Inspección anual', 'en la verificación anual de planimetría de los procedimientos de la serie, para detectar cambios '
                             'estructurales, de distribución o de uso que afecten el diseño del sistema.'),
        ('Después de un cambio', 'cada vez que se modifique la instalación, el edificio, su ocupación o sus vías de evacuación.'),
        ('Emisión de documentos', 'antes de entregar al cliente cualquier plano o diagrama confeccionado por la empresa.'),
    ]))
    a(('p', 'En la verificación de un plano se debe controlar:'))
    a(('items', [
        ('Cajetín y orientación', 'datos de la empresa, autor, fecha, instalación, flecha de norte y escala o leyenda «sin escala».'),
        ('Símbolos', 'que cada componente esté representado con el símbolo de este procedimiento, con forma, relleno, escala '
                     'relativa y orientación correctos.'),
        ('Indicadores y leyenda', 'diámetros, temperaturas de actuación, subíndices y leyenda con el significado de cada uno.'),
        ('Correspondencia con la instalación', 'que la cantidad, el tipo y la ubicación de los componentes coincidan con lo '
                                               'relevado.'),
    ]))
    a(('p', cierre(1)))

    a(('h3', 'CONTROL DE CAMBIOS Y RESPONSABILIDADES'))
    a(('p', 'Toda modificación de la instalación, del edificio o de sus vías de evacuación se debe reflejar en los planos y en los '
            'diagramas de evacuación antes de dar por concluida la intervención. Los planos reemplazados se identifican como '
            'anulados y se conservan junto con los registros.'))
    a(('p', 'La empresa mantenedora es responsable de confeccionar y verificar la documentación gráfica con la simbología de este '
            'procedimiento y de informar al usuario las diferencias detectadas. El usuario o propietario es responsable de '
            'comunicar las modificaciones del edificio y de su ocupación, y de mantener colocados y legibles los diagramas de '
            'evacuación.'))
    return C


def REGISTRO_EXTRA(cierre):
    return [
        'La verificación de cada plano se registra en la planilla SG-PEM-IFI-SIM-1 %s – %s, y la de cada diagrama de evacuación, '
        'en la planilla SG-PEM-IFI-SIM-2 %s – %s.' % (NOM, PL[1], NOM, PL[2]),
        'En cada planilla se debe indicar con ✓ si el ítem cumple, con O si no cumple y con X si no es apreciable, según la '
        'codificación de las planillas de la serie; los ítems que no resulten aplicables se indican con NA. Toda condición O o X '
        'se debe describir en observaciones. Cada planilla debe ser firmada por el supervisor del mantenedor y por el responsable '
        'de la instalación, con su aclaración.',
        'Las planillas se deben conservar como mínimo durante tres años, con el mismo criterio que los registros de mantenimiento '
        'de la IRAM 3546:2011. Los planos y diagramas vigentes se conservan durante toda la vida útil de la instalación.',
    ]
