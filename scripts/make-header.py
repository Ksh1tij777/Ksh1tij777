"""Profile header: editorial title on the left, a hand-plotted star chart on the right.
Run: python scripts/make-header.py  ->  assets/header.svg"""
import random
from pathlib import Path

from theme import ACCENT, FAINT, FG, MUTED, RULE, svg, text

OUT = Path(__file__).resolve().parent.parent / "assets" / "header.svg"
W, H = 1200, 340

# --- star chart (right side) -----------------------------------------------
CX0, CY0, CW, CH = 760, 40, 400, 240
rnd = random.Random(4)
grid = []
for i in range(5):
    x = CX0 + i * CW / 4
    grid.append(f'<line x1="{x:.0f}" y1="{CY0}" x2="{x:.0f}" y2="{CY0+CH}" stroke="{RULE}"/>')
    grid.append(text(x, CY0 + CH + 16, f"{5 + i}h", "m", 9, FAINT, "middle"))
for j in range(4):
    y = CY0 + j * CH / 3
    grid.append(f'<line x1="{CX0}" y1="{y:.0f}" x2="{CX0+CW}" y2="{y:.0f}" stroke="{RULE}"/>')
    grid.append(text(CX0 + CW + 8, y + 3, f"{20 - j * 10:+d}°", "m", 9, FAINT))

# background field stars
field = []
for k in range(70):
    x, y = rnd.uniform(CX0 + 4, CX0 + CW - 4), rnd.uniform(CY0 + 4, CY0 + CH - 4)
    r = rnd.choice([.6, .7, .9, 1.1])
    field.append(f'<circle class="tw t{k % 4}" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{FG}"/>')

# an Orion-like figure (shoulders, belt, feet, sword)
S = {"bet": (845, 100), "bel": (985, 92), "min": (930, 168), "aln": (905, 174), "mtk": (880, 180),
     "sai": (1005, 238), "rig": (835, 246), "hd": (912, 64), "sw": (905, 205)}
lines = [("hd", "bet"), ("hd", "bel"), ("bet", "mtk"), ("bel", "min"), ("mtk", "aln"), ("aln", "min"),
         ("mtk", "rig"), ("min", "sai")]
fig = []
for k, (a, b) in enumerate(lines):
    (x1, y1), (x2, y2) = S[a], S[b]
    fig.append(f'<line class="trace" style="animation-delay:{.25 * k:.2f}s" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
               f'stroke="{FG}" stroke-opacity=".55" stroke-width="1"/>')
for name, (x, y) in S.items():
    r = {"bet": 4.2, "rig": 4, "bel": 3.2, "sai": 3, "aln": 2.8, "mtk": 2.6, "min": 2.6, "hd": 2, "sw": 1.6}[name]
    col = ACCENT if name == "bet" else FG
    fig.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{col}"/>')
bx, by = S["bet"]
fig.append(f'<circle class="ping" cx="{bx}" cy="{by}" r="6" fill="none" stroke="{ACCENT}"/>')
fig.append(text(bx - 12, by - 12, "α Ori", "di", 15, ACCENT, "end"))
fig.append(text(CX0 + 2, CY0 - 10, "PLATE I — ORION, AS SEEN FROM JAIPUR", "m", 9, MUTED, ls=1.4))
# slow survey sweep
sweep = f'<rect class="sweep" x="{CX0}" y="{CY0}" width="1" height="{CH}" fill="{ACCENT}" opacity=".5"/>'
chart = (f'<g>{"".join(grid)}</g><clipPath id="cc"><rect x="{CX0}" y="{CY0}" width="{CW}" height="{CH}"/></clipPath>'
         f'<g clip-path="url(#cc)">{"".join(field)}{sweep}</g>{"".join(fig)}')

# --- type (left side) -----------------------------------------------------
left = (
    text(48, 64, "N° 001 · PROFILE · JAIPUR, IN", "m", 11, MUTED, ls=2)
    + text(44, 160, "Kshitij Verma", "d", 92, FG, ls=-1.5)
    + text(48, 206, "builds models that look closely.", "di", 32, MUTED)
    + f'<line x1="48" x2="700" y1="250" y2="250" stroke="{RULE}"/>'
    + text(48, 278, "ML ENGINEER, SURVEYORS AI", "m", 11, FG, ls=1.4)
    + text(48, 298, "B.TECH CCE, LNMIIT JAIPUR · '28", "m", 11, MUTED, ls=1.4)
    + text(372, 278, "1ST OF 14,000+", "mm", 11, ACCENT, ls=1.4)
    + text(372, 298, "GOOGLE CLOUD RAPID AGENT HACKATHON", "m", 11, MUTED, ls=1.4)
)

css = """
.tw{animation:tw 5s ease-in-out infinite}
.t1{animation-delay:-1.3s;animation-duration:6.5s}.t2{animation-delay:-2.6s;animation-duration:4.2s}.t3{animation-delay:-3.9s;animation-duration:7.4s}
@keyframes tw{0%,100%{opacity:.25}50%{opacity:.9}}
.trace{stroke-dasharray:200;stroke-dashoffset:200;animation:trace 1.4s ease-out forwards}
@keyframes trace{to{stroke-dashoffset:0}}
.sweep{animation:sweep 9s linear infinite}
@keyframes sweep{from{transform:translateX(0)}to{transform:translateX(400px)}}
"""
OUT.write_text(svg(W, H, left + chart, "Kshitij Verma — builds models that look closely. ML engineer, Surveyors AI.", css))
print("wrote", OUT)
