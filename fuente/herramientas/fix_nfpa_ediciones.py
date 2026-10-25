"""Quita los años de edición de las NFPA y agrega la regla de edición vigente. Uso: python -I fix_nfpa_ediciones.py <manuales>"""
import os, sys
D = sys.argv[1]
def patch(sig, pairs):
    p = os.path.join(D, 'content_%s.py' % sig); s = open(p, encoding='utf8').read()
    for o, n in pairs:
        assert s.count(o) >= 1, (sig, o[:70]); s = s.replace(o, n)
    open(p, 'w', encoding='utf8').write(s)
VIG = (" Se aplica la edición vigente de cada norma NFPA; la numeración de los artículos citados se debe confirmar en esa "
       "edición, porque puede variar entre ediciones.")
patch('SDI', [
    ("N72 = 'NFPA 72, edición 2016'", "N72 = 'NFPA 72'"),
    ("N101 = 'NFPA 101, Código de Seguridad Humana, edición 2018'", "N101 = 'NFPA 101, Código de Seguridad Humana'"),
    ("'La NFPA 101, Código de Seguridad Humana, edición 2018, establece", "'La NFPA 101, Código de Seguridad Humana, establece"),
    ("criterios complementarios: %s, capítulo 14, y NFPA 101, edición 2018)", "criterios complementarios: %s y NFPA 101)"),
    ("            'diferencias de frecuencia o de exigencia, se adopta siempre la condición más exigente.' % N72))",
     "            'diferencias de frecuencia o de exigencia, se adopta siempre la condición más exigente.%s' % (N72, VIG)))"),
    ("N72 = 'NFPA 72'", "N72 = 'NFPA 72'\nVIG = %r" % VIG),
])
patch('SAL', [
    ("N72 = 'NFPA 72, edición 2016'", "N72 = 'NFPA 72'\nVIG = %r" % VIG),
    ("N101 = 'NFPA 101, Código de Seguridad Humana, edición 2018'", "N101 = 'NFPA 101, Código de Seguridad Humana'"),
    ("'La NFPA 101, Código de Seguridad Humana, edición 2018, establece", "'La NFPA 101, Código de Seguridad Humana, establece"),
    ("'capítulo 14; seguridad humana: NFPA 101, edición 2018)'", "'capítulo 14; seguridad humana: NFPA 101)'"),
])
patch('SBC', [
    ("N20 = 'NFPA 20, edición 2007'", "N20 = 'NFPA 20'"),
    ("'del tubo Pitot sigue la NFPA 13, edición 2019, A.5.2.2.'", "'del tubo Pitot sigue la NFPA 13, A.5.2.2.'"),
    ("'en campo de la NFPA 20 (14.2) se aplican por analogía a la prueba anual.' % N20))",
     "'en campo de la NFPA 20 (14.2) se aplican por analogía a la prueba anual.%s' % (N20, %r)))" % VIG),
    ("'no mayor que el **140 %** de la presión total nominal (NFPA 20, 6.2.2, cuya versión en español '\n"
     "                                  'indica «40 %» por error de traducción; el valor de 140 % se confirma en el 7.1.2.2, para '\n"
     "                                  'bombas verticales).'",
     "'no mayor que el **140 %** de la presión total nominal (NFPA 20, 6.2.2).'"),
])
print('ok')
