"""Símbolos SG-PEM-IFI-SIM redibujados (vectorial con matplotlib -> PNG 600 dpi) siguiendo la geometría de la NFPA 170.
Dibujo propio de BRAFEMAR: no se copian imágenes de la norma. Uso: python -I simbolos.py <carpeta_salida>
Cada símbolo se define en un lienzo de 3 x 2 unidades (x de -1.5 a 1.5, y de -1 a 1)."""
import math, os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import patches as P

OUT = sys.argv[1] if len(sys.argv) > 1 else 'simbolos'
LW = 2.2
K = 'black'
FONT = 'DejaVu Sans'

class C:
    def __init__(self, w=3.0, h=2.0):
        self.w, self.h = w, h
        self.fig = plt.figure(figsize=(w * 0.5, h * 0.5), dpi=600)
        self.ax = self.fig.add_axes([0, 0, 1, 1]); self.ax.set_xlim(-w / 2, w / 2); self.ax.set_ylim(-h / 2, h / 2)
        self.ax.set_aspect('equal'); self.ax.axis('off')
    def add(self, p): self.ax.add_patch(p); return p
    def circle(self, x, y, r, fill=False, fc=K, lw=LW):
        return self.add(P.Circle((x, y), r, fill=fill, fc=fc if fill else 'none', ec=K, lw=lw))
    def poly(self, pts, fill=False, fc=K, lw=LW, ec=K):
        return self.add(P.Polygon(pts, closed=True, fill=fill, fc=fc if fill else 'none', ec=ec, lw=lw, joinstyle='miter'))
    def rect(self, x, y, w, h, fill=False, fc=K, lw=LW):
        return self.add(P.Rectangle((x - w / 2, y - h / 2), w, h, fill=fill, fc=fc if fill else 'none', ec=K, lw=lw))
    def rrect(self, x, y, w, h, r=0.25, lw=LW):
        return self.add(P.FancyBboxPatch((x - w / 2 + r, y - h / 2 + r), w - 2 * r, h - 2 * r,
                                         boxstyle='round,pad=%f' % r, fill=False, ec=K, lw=lw))
    def line(self, pts, lw=LW, ls='-', color=K):
        xs, ys = zip(*pts); self.ax.plot(xs, ys, color=color, lw=lw, ls=ls, solid_capstyle='butt')
    def text(self, x, y, s, size=9, weight='normal', ha='center', va='center', color=K):
        self.ax.text(x, y, s, fontsize=size, fontfamily=FONT, fontweight=weight, ha=ha, va=va, color=color)
    def arrow(self, x0, y0, x1, y1, lw=LW, hw=0.12):
        self.ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                         arrowprops=dict(arrowstyle='-|>,head_width=%f,head_length=%f' % (hw * 2, hw * 3), lw=lw, color=K))
    def save(self, name):
        os.makedirs(OUT, exist_ok=True)
        self.fig.savefig(os.path.join(OUT, name + '.png'), dpi=600, transparent=False, facecolor='white')
        plt.close(self.fig)

def hexagon(c, x=0, y=0, r=0.55, fill=False, lw=LW):
    pts = [(x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a))) for a in range(0, 360, 60)]
    return c.poly(pts, fill=fill, lw=lw)
def triangle(c, x=0, y=0, s=1.1, fill=False, lw=LW, up=True, fc=K):
    h = s * math.sqrt(3) / 2; k = 1 if up else -1
    return c.poly([(x - s / 2, y - k * h / 3), (x + s / 2, y - k * h / 3), (x, y + k * 2 * h / 3)], fill=fill, lw=lw, fc=fc)
def diamond(c, x=0, y=0, rx=0.55, ry=0.55, fill=False, lw=LW):
    return c.poly([(x, y + ry), (x + rx, y), (x, y - ry), (x - rx, y)], fill=fill, lw=lw)
def bowtie(c, x=0, y=0, s=0.4, lw=LW):
    c.poly([(x - s, y + s * 0.75), (x - s, y - s * 0.75), (x + s, y + s * 0.75), (x + s, y - s * 0.75)], lw=lw)
def pipe(c, y=0, x0=-1.45, x1=1.45, gap=None):
    if gap: c.line([(x0, y), (gap[0], y)], lw=1.2, ls=(0, (4, 3))); c.line([(gap[1], y), (x1, y)], lw=1.2, ls=(0, (4, 3)))
    else: c.line([(x0, y), (x1, y)], lw=1.2, ls=(0, (4, 3)))
def star(c, x=0, y=0, R=0.6, r=0.25, fill=False):
    pts = []
    for i in range(10):
        a = math.radians(90 + i * 36); rr = R if i % 2 == 0 else r
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    c.poly(pts, fill=fill)

S = {}   # clave -> función de dibujo
def sym(key):
    def deco(f): S[key] = f; return f
    return deco

# ---------------- 7.2 Abastecimiento y distribución de agua ----------------
@sym('riser')
def _(c): c.circle(0, 0, 0.55); c.line([(-0.39, 0.39), (0.39, -0.39)]); c.line([(-0.39, -0.39), (0.39, 0.39)])
@sym('riser_humedo')
def _(c):
    c.circle(0, 0, 0.55); c.poly([(0, 0), (-0.39, 0.39), (0.39, 0.39)], fill=True); c.poly([(0, 0), (-0.39, -0.39), (0.39, -0.39)], fill=True)
    c.line([(-0.39, 0.39), (0.39, -0.39)]); c.line([(-0.39, -0.39), (0.39, 0.39)])
@sym('riser_seco')
def _(c):
    triangle(c, 0, -0.05, 1.7, fill=True); c.circle(0, -0.15, 0.42, fill=True, fc='white')
    c.line([(-0.3, 0.15), (0.3, -0.45)]); c.line([(-0.3, -0.45), (0.3, 0.15)])
@sym('riser_accion_previa')
def _(c): diamond(c, 0, 0, 0.45, 0.8); c.circle(0, 0, 0.3); c.line([(-0.21, 0.21), (0.21, -0.21)]); c.line([(-0.21, -0.21), (0.21, 0.21)])
@sym('valvula')
def _(c): bowtie(c)
@sym('valvula_osy')
def _(c): pipe(c, gap=(-0.42, 0.42)); bowtie(c); c.line([(0, 0), (0, 0.65)]); c.line([(-0.2, 0.65), (0.2, 0.65)])
@sym('valvula_mariposa_ind')
def _(c): pipe(c, gap=(-0.42, 0.42)); bowtie(c); c.line([(0, 0), (0, 0.55)]); c.rect(0, 0.7, 0.28, 0.25, fill=True)
@sym('retencion')
def _(c): c.line([(-0.4, 0.45), (-0.4, -0.45), (0.4, 0.45), (0.4, -0.45)]); c.arrow(-0.4, -0.7, 0.4, -0.7, lw=1.5)
@sym('bomba')
def _(c): c.rrect(-0.35, 0, 1.4, 0.7, r=0.12); c.ax.add_patch(P.FancyBboxPatch((-0.93, -0.23), 1.16, 0.46, boxstyle='round,pad=0.12', fc=K, ec=K)); c.line([(0.35, 0), (0.75, 0)], lw=5); c.circle(1.0, 0, 0.3, fill=True)
@sym('bomberos_simple')
def _(c): pipe(c, y=-0.5); c.line([(0, -0.5), (0, 0.35)]); c.circle(0, 0.55, 0.2)
@sym('bomberos_siamesa')
def _(c): pipe(c, y=-0.55); c.line([(0, -0.55), (0, 0.05)]); c.line([(0, 0.05), (-0.4, 0.45)]); c.line([(0, 0.05), (0.4, 0.45)]); c.circle(-0.53, 0.58, 0.18); c.circle(0.53, 0.58, 0.18)
@sym('hidrante_privado')
def _(c): c.line([(0.3, 0.9), (0.3, -0.9)], lw=1.2, ls=(0, (4, 3))); c.line([(0.3, 0), (-0.05, 0)]); c.circle(-0.3, 0, 0.25)
@sym('hidrante_publico')
def _(c): c.line([(0.3, 0.9), (0.3, -0.9)], lw=1.2, ls=(0, (4, 3))); c.line([(0.3, 0), (0.05, 0)]); c.circle(-0.25, 0, 0.32, fill=True)
@sym('medidor')
def _(c): pipe(c, gap=(-0.45, 0.45)); c.circle(0, 0, 0.45); c.arrow(-0.2, -0.2, 0.25, 0.25, lw=1.5, hw=0.08)

# ---------------- 7.6.1 Tipos de sistemas de extinción ----------------
def sistema(c, auto, inner):
    if auto: c.circle(0, 0, 0.62)
    else: c.rect(0, 0, 1.15, 1.15)
    inner(c)
for auto in (True, False):
    sfx = 'auto' if auto else 'manual'
    S['sis_humedo_' + sfx] = (lambda a: lambda c: sistema(c, a, lambda c: c.circle(0, 0, 0.45, fill=True)))(auto)
    S['sis_seco_' + sfx] = (lambda a: lambda c: sistema(c, a, lambda c: c.circle(0, 0, 0.45)))(auto)
    S['sis_espuma_' + sfx] = (lambda a: lambda c: sistema(c, a, lambda c: (c.circle(0, 0, 0.45), c.line([(-0.32, 0.32), (0.32, -0.32)]), c.line([(-0.32, -0.32), (0.32, 0.32)]))))(auto)
    S['sis_niebla_' + sfx] = (lambda a: lambda c: sistema(c, a, lambda c: diamond(c, 0, 0, 0.22, 0.48, fill=True)))(auto)
    S['sis_polvo_' + sfx] = (lambda a: lambda c: sistema(c, a, lambda c: c.rect(0, 0, 0.55, 0.55, fill=True)))(auto)
    S['sis_co2_' + sfx] = (lambda a: lambda c: sistema(c, a, lambda c: triangle(c, 0, -0.03, 0.75, fill=True)))(auto)
    S['sis_agente_limpio_' + sfx] = (lambda a: lambda c: sistema(c, a, lambda c: triangle(c, 0, -0.03, 0.75)))(auto)
@sym('sis_accion_previa_auto')
def _(c): c.circle(0, 0, 0.62, lw=LW * 1.8)
@sym('sup_rociado_total')
def _(c): c.circle(0, 0, 0.6); c.text(0, 0, 'AS', 10)
@sym('sup_no_rociado')
def _(c): c.poly([(-1.0, 0), (-0.55, 0.5), (0.55, 0.5), (1.0, 0), (0.55, -0.5), (-0.55, -0.5)]); c.text(0, 0, 'NS', 10)
@sym('sup_agua_pulverizada')
def _(c): c.circle(0, 0, 0.6); c.text(0, 0, 'WS', 10)

# ---------------- 7.6.2 y 7.6.3 Rociadores, cañerías y válvulas ----------------
@sym('rociador_montante')
def _(c): pipe(c, gap=(-0.4, 0.4)); c.circle(0, 0, 0.4)
@sym('rociador_colgante')
def _(c): pipe(c, gap=(-0.4, 0.4)); c.circle(0, 0, 0.4, fill=True)
@sym('rociador_lateral')
def _(c): pipe(c, y=-0.45); triangle(c, 0, -0.05, 0.75, up=False)
@sym('rociador_abierto_montante')
def _(c): diamond(c, 0, 0, 0.55, 0.55)
@sym('rociador_abierto_colgante')
def _(c): diamond(c, 0, 0, 0.55, 0.55, fill=True)
@sym('boquilla_pulverizadora')
def _(c): c.line([(-1.2, -0.55), (1.0, -0.55)]); c.line([(0, -0.55), (0, -0.2)]); triangle(c, 0, 0.12, 0.7)
@sym('cano_rociadores')
def _(c): c.line([(-1.3, 0), (1.3, 0)])
@sym('valvula_alarma')
def _(c): c.line([(-0.4, 0.3), (-0.4, -0.6), (0.4, 0.3), (0.4, -0.6)]); c.arrow(-0.4, -0.8, 0.4, -0.8, lw=1.5); c.circle(-0.25, 0.6, 0.22, fill=True); c.text(0.3, 0.68, 'A', 9, 'bold')
@sym('valvula_tubo_seco')
def _(c): pipe(c, y=-0.25, gap=(-0.42, 0.42)); bowtie(c, 0, -0.25); c.line([(0, -0.25), (0, 0.4)]); c.circle(0, 0.6, 0.2)
@sym('valvula_diluvio')
def _(c): pipe(c, gap=(-0.6, 0.6)); diamond(c, 0, 0, 0.6, 0.35)
@sym('valvula_accion_previa')
def _(c): pipe(c, gap=(-0.6, 0.6)); diamond(c, 0, 0, 0.6, 0.35); c.line([(0, 0.35), (0, -0.35)])
@sym('valvula_control_piso')
def _(c): c.line([(-0.6, -0.3), (0.6, -0.3)]); c.line([(-0.6, -0.15), (-0.6, -0.45)]); c.line([(0.6, -0.15), (0.6, -0.45)]); c.circle(0, -0.3, 0.17, fill=True); c.text(0, 0.35, 'F/Z', 9, 'bold')
@sym('soporte_cano')
def _(c): pipe(c); c.line([(-0.3, 0.45), (0.3, -0.45)])

# ---------------- 7.7 y 7.8 Extintores y equipos de lucha ----------------
def ext(c, inner=None, fill=False):
    triangle(c, 0, -0.1, 1.45)
    if inner: inner(c)
@sym('extintor')
def _(c): ext(c)
@sym('extintor_agua')
def _(c): ext(c)
@sym('extintor_espuma')
def _(c): ext(c, lambda c: (c.circle(0, -0.1, 0.25), c.line([(-0.18, 0.08), (0.18, -0.28)]), c.line([(-0.18, -0.28), (0.18, 0.08)])))
@sym('extintor_polvo_bc')
def _(c): ext(c, lambda c: c.rect(0, -0.12, 0.38, 0.38))
@sym('extintor_polvo_abc')
def _(c): ext(c, lambda c: (c.rect(0, -0.12, 0.38, 0.38), c.rect(0, -0.12, 0.22, 0.22, fill=True)))
@sym('extintor_co2')
def _(c): ext(c, lambda c: triangle(c, 0, -0.12, 0.7, fill=True))
@sym('extintor_agente_limpio')
def _(c): ext(c, lambda c: triangle(c, 0, -0.12, 0.7))
@sym('extintor_metales')
def _(c): ext(c, lambda c: (triangle(c, 0, -0.12, 0.7, up=False), c.line([(-0.35, -0.12), (0.35, -0.12)])))
@sym('equipo_lucha')
def _(c): c.ax.add_patch(P.Wedge((0, -0.35), 0.75, 0, 180, fill=False, ec=K, lw=LW)); c.line([(-0.75, -0.35), (0.75, -0.35)])
@sym('boca_incendio')
def _(c): c.line([(-1.1, -0.1), (0.3, -0.1)]); c.line([(-0.3, -0.1), (-0.3, 0.15)]); c.line([(-0.45, 0.15), (-0.15, 0.15)]); c.rect(0.38, -0.1, 0.12, 0.38, fill=True)
@sym('gabinete_manguera_humedo')
def _(c):
    c.ax.add_patch(P.Wedge((0, -0.35), 0.75, 0, 180, fill=False, ec=K, lw=LW)); c.line([(-0.75, -0.35), (0.75, -0.35)])
    c.circle(0, -0.08, 0.27, fill=True); c.arrow(0.25, 0.25, 0.95, 0.7, lw=1.5, hw=0.08)
@sym('recipiente_agente')
def _(c): c.rect(-0.45, 0, 0.3, 0.6); c.circle(0.1, 0, 0.38)
@sym('fusible')
def _(c): c.rrect(0, 0, 1.6, 0.7, r=0.3); c.circle(-0.5, 0, 0.06, fill=True); c.circle(0.5, 0, 0.06, fill=True); c.line([(-0.12, 0.22), (0.08, 0.02), (-0.08, -0.02), (0.12, -0.22)], lw=1.6)

def recipiente(sub):
    def f(c): c.rect(-0.45, 0.1, 0.3, 0.6); c.circle(0.1, 0.1, 0.38); c.text(0.15, -0.6, sub, 8)
    return f
S['recipiente_quimico_humedo'] = recipiente('WC'); S['recipiente_agente_limpio'] = recipiente('CA'); S['recipiente_co2'] = recipiente('CO₂'); S['recipiente_polvo'] = recipiente('DC'); S['recipiente_espuma'] = recipiente('FO')

# ---------------- 8.2 a 8.5 Detección, alarma y notificación ----------------
def caja(txt, size=8):
    def f(c): c.rect(0, 0, max(0.9, 0.2 + 0.24 * len(txt)), 0.6); c.text(0, 0, txt, size)
    return f
for k, t in [('central_facu', 'FACU'), ('anunciador_faa', 'FAA'), ('central_descarga', 'RSFACU'), ('controlador_bomba', 'FPC'),
             ('interfaz_central', 'FACI'), ('panel_sirenas_aux', 'NAC'), ('caja_paso', 'JB'), ('retenedor_puerta', 'DH'),
             ('flujo_ws', 'WF'), ('supervisor_valvula', 'VS'), ('presostato', 'PS'), ('nivel', 'LS'), ('fuente_ups', 'UPS'),
             ('dact', 'DACT')]:
    S[k] = caja(t)
def hexs(main, sub=None, fill=False):
    def f(c):
        hexagon(c, 0, 0, 0.55, fill=fill)
        if main: c.text(0, 0, main, 11, color='white' if fill else K)
        if sub: c.text(0.62, -0.5, sub, 7.5, ha='left')
    return f
S['detector_base'] = hexs(None)
S['detector_humo'] = hexs('S'); S['detector_humo_fotoelectrico'] = hexs('S', 'P'); S['detector_humo_ionico'] = hexs('S', 'I')
S['detector_humo_aspiracion'] = hexs('S', 'AS'); S['detector_haz_receptor'] = hexs('S', 'BR'); S['detector_haz_emisor'] = hexs('S', 'BT')
S['detector_temp'] = hexs('H'); S['detector_temp_fija'] = hexs('H', 'F'); S['detector_temp_termovelocimetrico'] = hexs('H', 'R')
S['detector_temp_combinado'] = hexs('H', 'R/F')
@sym('detector_ducto')
def _(c): hexagon(c, 0, -0.25, 0.5); c.text(0, -0.25, 'S', 10); c.line([(-0.12, 0.3), (-0.12, 0.85)], lw=1.4); c.line([(0.12, 0.3), (0.12, 0.85)], lw=1.4)
@sym('detector_llama')
def _(c): hexagon(c); c.line([(-0.22, -0.2), (0, 0.22), (0.22, -0.2)], lw=1.8)
@sym('detector_llama_uvir')
def _(c): hexagon(c); c.line([(-0.22, -0.2), (0, 0.22), (0.22, -0.2)], lw=1.8); c.text(0.62, -0.5, 'UV/IR', 7.5, ha='left')
@sym('detector_gas')
def _(c): hexagon(c, fill=True); triangle(c, 0, -0.03, 0.5, fill=True, lw=0.1); c.poly([(-0.25, -0.17), (0.25, -0.17), (0, 0.27)], fill=True, fc='white', lw=0.1, ec='white'); c.text(0.62, -0.5, 'xx', 7.5, ha='left')
@sym('detector_co')
def _(c): hexagon(c, fill=True); c.poly([(-0.25, -0.17), (0.25, -0.17), (0, 0.27)], fill=True, fc='white', lw=0.1, ec='white'); c.text(0.62, -0.5, 'CO', 7.5, ha='left')
S['avisador_manual'] = (lambda c: (c.rect(0, 0, 0.6, 0.6), c.text(0, 0, 'F', 10)))
S['avisador_manual_descarga'] = (lambda c: (c.rect(0, 0, 0.6, 0.6), c.text(0, 0, 'CA', 8)))
def aborto(t):
    def f(c):
        c.rect(0, -0.15, 0.7, 0.6); c.text(0, -0.15, t, 8)
        c.ax.add_patch(P.Arc((0, 0.25), 0.6, 0.5, theta1=0, theta2=180, ec=K, lw=LW)); c.line([(0, 0.15), (0, 0.5)], lw=1.6)
    return f
S['aborto'] = aborto('A'); S['descarga_manual'] = aborto('M')
S['modulo_entrada'] = hexs(None);
@sym('modulo_entrada')
def _(c): c.poly([(-0.6, 0), (-0.35, 0.33), (0.35, 0.33), (0.6, 0), (0.35, -0.33), (-0.35, -0.33)]); c.text(0, 0, 'AIM', 8)
@sym('modulo_salida')
def _(c): c.poly([(-0.6, 0), (-0.35, 0.33), (0.35, 0.33), (0.6, 0), (0.35, -0.33), (-0.35, -0.33)]); c.text(0, 0, 'AOM', 8)
@sym('modulo_aislador')
def _(c): c.poly([(-0.6, 0), (-0.35, 0.33), (0.35, 0.33), (0.6, 0), (0.35, -0.33), (-0.35, -0.33)]); c.text(0, 0, 'IM', 8)
@sym('valvula_solenoide')
def _(c): bowtie(c, 0, -0.35, 0.35); c.line([(0, -0.35), (0, 0.15)]); c.add(P.Ellipse((0, 0.42), 0.8, 0.45, fill=False, ec=K, lw=LW)); c.text(0, 0.42, 'SOV', 7)
@sym('sirena')
def _(c): c.rect(0, -0.2, 0.65, 0.65); c.text(0, -0.2, 'F', 9); triangle(c, 0, 0.42, 0.4, up=False, lw=1.6); c.text(0.42, -0.55, 'H', 7.5, ha='left')
@sym('campana')
def _(c): c.rect(0, -0.2, 0.65, 0.65); c.text(0, -0.2, 'F', 9); c.line([(0, 0.13), (0, 0.33)], lw=1.4); c.circle(0, 0.45, 0.12, lw=1.4); c.text(0.42, -0.55, 'V', 7.5, ha='left')
@sym('sirena_luz')
def _(c):
    c.rect(0, -0.2, 0.65, 0.65); c.line([(-0.32, 0.12), (0.32, -0.52)], lw=1.3); c.line([(-0.32, -0.52), (0.32, 0.12)], lw=1.3)
    c.circle(0, -0.2, 0.13, fill=True, fc='white', lw=1.3); triangle(c, 0.25, 0.42, 0.38, up=False, lw=1.6); c.text(-0.25, 0.42, 'CD', 7)
@sym('luz_estroboscopica_pared')
def _(c):
    c.circle(0, 0, 0.22, lw=1.6); c.line([(0, -0.22), (0, -0.6)], lw=1.6); c.line([(-0.3, -0.6), (0.3, -0.6)], lw=1.6)
    for a in (35, 145): c.line([(0.24 * math.cos(math.radians(a)), 0.24 * math.sin(math.radians(a))), (0.55 * math.cos(math.radians(a)), 0.55 * math.sin(math.radians(a)))], lw=1.6)
    c.text(0.45, 0.55, 'CD', 7)
@sym('altavoz')
def _(c): c.rect(0, -0.2, 0.65, 0.65); c.text(0, -0.2, 'S', 9); c.poly([(-0.2, 0.55), (0.2, 0.55), (0, 0.2)], fill=True, lw=1); c.text(0.45, 0.5, 'W', 7, ha='left')
@sym('resistencia_fin_linea')
def _(c):
    pts = [(-1.0, 0), (-0.5, 0)] + [(-0.5 + 0.125 * i, 0.22 if i % 2 else -0.22) for i in range(1, 8)] + [(0.5, 0), (1.0, 0)]
    c.line(pts, lw=1.8)
@sym('telefono_bomberos')
def _(c): c.rect(0, 0, 0.55, 0.8); c.text(0, 0, '☎', 12)

# ---------------- Clase de fuego (Figura 4.3(b)) ----------------
@sym('clase_a')
def _(c): triangle(c, 0, -0.1, 1.5, fill=True, fc='#2e8b3a'); c.text(0, -0.2, 'A', 16, 'bold', color='white')
@sym('clase_b')
def _(c): c.rect(0, 0, 1.2, 1.2, fill=True, fc='#d0202a'); c.text(0, 0, 'B', 16, 'bold', color='white')
@sym('clase_c')
def _(c): c.circle(0, 0, 0.65, fill=True, fc='#1f5fbf'); c.text(0, 0, 'C', 16, 'bold', color='white')
@sym('clase_d')
def _(c): star(c, 0, -0.03, 0.85, 0.36, fill=True); c.ax.patches[-1].set_facecolor('#f2c200'); c.text(0, -0.08, 'D', 12, 'bold', color='black')

# ---------------- 6.3.4 y 7.4 Medios de egreso ----------------
@sym('salida')
def _(c): c.line([(-1.3, 0), (1.3, 0)], lw=7)
@sym('acceso_salida')
def _(c): c.line([(-1.3, 0), (1.3, 0)], lw=7, ls=(0, (2.2, 1.2)))
@sym('descarga_salida')
def _(c): c.line([(-1.3, 0), (1.3, 0)], lw=7, ls=(0, (1.1, 0.6)))
@sym('luz_emergencia')
def _(c):
    c.rect(0, 0.2, 1.4, 0.35)
    for x in (-0.45, 0.45): triangle(c, x, -0.18, 0.4, up=False, lw=1.6)
@sym('cartel_salida')
def _(c): c.circle(0, 0.15, 0.42); c.poly([(0, 0.15), (-0.3, 0.45), (0.3, 0.45)], fill=True); c.poly([(0, 0.15), (-0.3, -0.15), (0.3, -0.15)], fill=True); c.arrow(-0.35, -0.6, 0.45, -0.6, lw=1.6)
@sym('dea')
def _(c): c.line([(-1.2, -0.35), (1.2, -0.35)]); c.line([(-1.2, -0.25), (1.2, -0.25)], lw=1); c.text(0, 0.25, '♡', 18)
@sym('ascensor')
def _(c): c.rect(0, 0, 0.8, 0.8); c.text(0, 0, 'E', 11)
@sym('puerta_cortafuego')
def _(c):
    c.line([(-0.8, -0.6), (0.8, -0.6)], lw=1.4); c.line([(-0.8, -0.5), (0.8, -0.5)], lw=1.4)
    c.line([(-0.6, -0.5), (-0.6, 0.6)], lw=1.4, ls=(0, (3, 2))); c.ax.add_patch(P.Arc((-0.6, -0.5), 2.2, 2.2, theta1=0, theta2=90, ec=K, lw=1.4, ls=(0, (3, 2))))
    diamond(c, -0.1, -0.1, 0.17, 0.17, fill=True)

# ---------------- Diagramas de evacuación (capítulo 11, dibujo propio) ----------------
@sym('usted_esta_aqui')
def _(c):
    c.rect(0, 0.1, 2.4, 1.1, fill=True, fc='#d0202a'); c.text(0, 0.3, 'USTED', 8, 'bold', color='white'); c.text(0, -0.08, 'ESTÁ AQUÍ', 8, 'bold', color='white')
    c.poly([(-0.18, -0.45), (0.18, -0.45), (0, -0.85)], fill=True, fc='#d0202a', ec='#d0202a')
@sym('norte')
def _(c): c.circle(0, 0, 0.6, lw=1.6); c.poly([(0, 0.5), (0.18, -0.3), (0, -0.15), (-0.18, -0.3)], fill=True); c.text(0, 0.78, 'N', 9, 'bold')
@sym('punto_reunion')
def _(c):
    c.rect(0, 0, 1.2, 1.2, fill=True, fc='#2e8b3a')
    for (x, y) in [(-0.3, 0.25), (0.3, 0.25), (-0.3, -0.25), (0.3, -0.25)]: c.circle(x, y, 0.1, fill=True, fc='white', lw=0.5)
    c.arrow(0.05, 0.05, -0.15, 0.05, lw=1.2, hw=0.05)

if __name__ == '__main__':
    for k, f in sorted(S.items()):
        c = C(); f(c); c.save(k)
    print(len(S), 'símbolos en', OUT)
