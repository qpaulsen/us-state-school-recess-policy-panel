"""Figure 1: a, construction workflow (stages 1 to 7, codebook version adopted at each stage, audit log);
b, research applications of the released data and linkage to outcome data. No panel.json needed.
Run: python f1_overview.py <panel workbook>
"""
import sys
sys.path.insert(0, '.')
from style import *
import numpy as np
import openpyxl

_wb = openpyxl.load_workbook(sys.argv[1], read_only=True, data_only=True)
NLOG = sum(1 for r in _wb['AUDIT_LOG'].iter_rows(min_row=2, values_only=True) if r[0])
NROW = sum(1 for r in _wb['Panel'].iter_rows(min_row=2, values_only=True) if r[0])

W, H = 180, 84
fig = plt.figure(figsize=(W / 25.4, H / 25.4))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')

# stage fill / number colour: grey construction, blue quality assurance, green release
B = (GREY[0], GREY[4]); Q = (BLUE[0], BLUE[4]); R = (GREEN[0], GREEN[4])
st = [('Source identification', 'NASBE inventory, operative statute and rule text, LegiScan', B, ''),
      ('Coding', 'One row per instrument version, verbatim excerpt, deposited source', B, 'Codebook v1.0'),
      ('Reliability round 1', 'Masked double coding of AL, AK, AZ, AR (\u03ba on AK, AZ, AR)', Q, 'v1.1, rules 1\u201317'),
      ('Reliability round 2', 'Masked double coding of 6 random states: ID, IN, IA, RI, TN, VA', Q, 'v1.2, rules 18\u201325; amends 8, 11'),
      ('Completeness audit', '41 states and DC; 382 candidate instruments', Q, 'v1.3\u2013v1.4, rules 26\u201328'),
      ('District of Columbia', 'Coded with the expanded search perimeter and audit checks', B, 'v1.4'),
      ('Release', f'{NROW} rows, 51 jurisdictions, 1,256 source documents', R, '')]

TOP = H - 3.5
ax.text(2, TOP, 'a', fontsize=8, fontweight='bold', va='center')
ax.text(122, TOP, 'b', fontsize=8, fontweight='bold', va='center')

# ---- a: workflow
X, Wn, Hn, G = 10, 104, 9.0, 2.0
y = TOP - 4.5; cen = []
for i, (t, d, c, v) in enumerate(st):
    y0 = y - Hn
    node(ax, X, y0, Wn, Hn, c[0], c[0], r=0.8, lw=0)
    ax.text(X + 2.5, y0 + Hn - 1.6, str(i + 1), fontsize=7, fontweight='bold', color=c[1], va='top')
    ax.text(X + 6.0, y0 + Hn - 1.6, t, fontsize=7, fontweight='bold', va='top')
    ax.text(X + 6.0, y0 + 1.5, d, fontsize=6.5, va='bottom')
    if v: ax.text(X + Wn - 2.5, y0 + Hn - 1.6, v, fontsize=6.5, color=GREY[4], va='top', ha='right')
    cen.append((y0, y)); y = y0 - G
for (a, _), (_, b) in zip(cen, cen[1:]): arrow(ax, (X + 6.0 - 3.5 + 0.9, a), (X + 6.0 - 3.5 + 0.9, b), c=GREY[3], lw=0.6)
top, bot = cen[0][1], cen[-1][0]
# audit log: a thin bracket rather than a box
ax.plot([X - 3.5, X - 3.5], [bot + 0.4, top - 0.4], color=TONE[3], lw=0.8, solid_capstyle='butt')
for yy in (bot + 0.4, top - 0.4): ax.plot([X - 3.5, X - 2.3], [yy, yy], color=TONE[3], lw=0.8, solid_capstyle='butt')
ax.text(X - 5.6, (top + bot) / 2, f'Audit log: every source, search and decision ({NLOG:,} entries)', rotation=90, ha='center', va='center', fontsize=6.5)

# ---- b: uses
UX = 124
rel_y = (cen[-1][0] + cen[-1][1]) / 2
arrow(ax, (X + Wn, rel_y), (UX - 0.6, rel_y), c=GREEN[4], lw=0.8)
ax.plot([UX, UX], [bot + 0.4, top - 0.4], color=GREEN[4], lw=0.8, solid_capstyle='butt')
from matplotlib.patches import Circle, Polygon, PathPatch
from matplotlib.path import Path
IC, IF, LW = BLUE[4], BLUE[0], 1.0
def ic_eye(cx, cy, s):
    w, h = s * 0.95, s * 0.52
    verts = [(cx - w / 2, cy), (cx - w / 4, cy + h * 0.95), (cx + w / 4, cy + h * 0.95), (cx + w / 2, cy),
             (cx + w / 4, cy - h * 0.95), (cx - w / 4, cy - h * 0.95), (cx - w / 2, cy)]
    ax.add_patch(PathPatch(Path(verts, [Path.MOVETO] + [Path.CURVE4] * 6), fc='white', ec=IC, lw=LW, zorder=5))
    ax.add_patch(Circle((cx, cy), s * 0.21, fc=IF, ec=IC, lw=LW, zorder=6))
    ax.add_patch(Circle((cx, cy), s * 0.09, fc=IC, ec='none', zorder=7))
def ic_runner(cx, cy, s):
    k = s / 6.0; P = lambda x, y: (cx + x * k, cy + y * k)
    ax.add_patch(Circle(P(0.6, 2.35), 0.62 * k, fc=IC, ec='none', zorder=6))
    for seg in ([(0.3, 1.5), (-0.3, -0.4)], [(0.3, 1.2), (1.4, 0.6), (2.1, 1.1)], [(0.3, 1.2), (-0.8, 1.0), (-1.4, 0.2)],
                [(-0.3, -0.4), (0.9, -1.3), (0.8, -2.5)], [(-0.3, -0.4), (-1.0, -1.5), (-2.2, -1.6)]):
        ax.plot(*zip(*[P(*q) for q in seg]), color=IC, lw=1.7, solid_capstyle='round', solid_joinstyle='round', zorder=6)
def ic_cap(cx, cy, s):
    w, h = s * 0.5, s * 0.22; cy += h * 0.25
    ax.add_patch(Polygon([(cx - w * 0.55, cy - h * 0.2), (cx - w * 0.55, cy - h * 1.35), (cx, cy - h * 1.75),
                          (cx + w * 0.55, cy - h * 1.35), (cx + w * 0.55, cy - h * 0.2)], closed=True, fc=IF, ec=IC, lw=LW, zorder=5, joinstyle='round'))
    ax.add_patch(Polygon([(cx - w, cy + h * 0.3), (cx, cy + h * 1.3), (cx + w, cy + h * 0.3), (cx, cy - h * 0.7)],
                         closed=True, fc=IC, ec=IC, lw=LW, zorder=6, joinstyle='round'))
    ax.plot([cx + w * 0.82, cx + w * 0.82], [cy + h * 0.3, cy - h * 1.6], color=IC, lw=0.8, zorder=6)
    ax.add_patch(Circle((cx + w * 0.82, cy - h * 1.75), s * 0.05, fc=IC, ec='none', zorder=7))
def ic_scales(cx, cy, s):
    k = s / 6.0; P = lambda x, y: (cx + x * k, cy + y * k)
    ln = lambda pts, lw=LW: ax.plot(*zip(*[P(*q) for q in pts]), color=IC, lw=lw, solid_capstyle='round', zorder=6)
    ln([(0, -2.4), (0, 2.2)]); ln([(-1.2, -2.6), (1.2, -2.6)], lw=1.4); ln([(-2.5, 1.6), (2.5, 1.6)])
    ax.add_patch(Circle(P(0, 2.4), 0.35 * k, fc=IC, ec='none', zorder=7))
    for sx in (-2.3, 2.3):
        ln([(sx, 1.6), (sx - 1.0, -0.5)], lw=0.7); ln([(sx, 1.6), (sx + 1.0, -0.5)], lw=0.7)
        th = np.linspace(np.pi, 2 * np.pi, 30)
        ax.add_patch(Polygon([P(sx + 1.15 * np.cos(t), -0.5 + 0.75 * np.sin(t)) for t in th], closed=True, fc=IF, ec=IC, lw=LW, zorder=6))

apps = [(ic_eye, 'Myopia onset'), (ic_runner, 'Physical activity'), (ic_cap, 'Education policy'), (ic_scales, 'Legal epidemiology')]
y_hi, y_lo = top - 6.0, rel_y + 16.0
step = (y_hi - y_lo) / (len(apps) - 1)
for j, (fn, lab) in enumerate(apps):
    cy = y_hi - j * step; cx = UX + 8.5
    fn(cx, cy, 8.0)
    ax.text(cx + 7.0, cy, lab, fontsize=6.5, va='center')
ax.plot([UX + 3, W - 3], [rel_y + 6.5] * 2, color=GREY[1], lw=0.5, solid_capstyle='butt')
ax.text(UX + 3, rel_y, 'Links to outcome data by\nstate FIPS code and school year', fontsize=6.5, va='center', linespacing=1.3)
save(fig, 'QAP_Fig1_overview')
print('ok')
