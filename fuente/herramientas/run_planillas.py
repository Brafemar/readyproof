import sys, os, re, unicodedata
sys.path.insert(0, sys.argv[1])
from build_planilla import build
import importlib
SISTEMAS = importlib.import_module(sys.argv[4] if len(sys.argv) > 4 else 'planillas_data').SISTEMAS
out, modelo = sys.argv[2], sys.argv[3]
def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'[^A-Za-z0-9]+', '_', t).strip('_').upper()
for sig, S in SISTEMAS.items():
    d = os.path.join(out, sig); os.makedirs(d, exist_ok=True)
    for p in S['planillas']:
        if 'solo' in S and p['n'] not in S['solo']: continue
        sp = dict(p); sp['sistema'] = S['nom']; sp['codigo'] = 'SG-PEM-IFI-%s-%d' % (sig, p['n'])
        sp.setdefault('titulo', p['nombre'])
        fn = os.path.join(d, 'SG-PEM-IFI-%s-%d_%s_%s.xlsx' % (sig, p['n'], slug(p['nombre']), sig))
        build(sp, fn, modelo); print(fn)
