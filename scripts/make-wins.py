"""Wins banner: the two hackathon wins, side by side.
Run: python scripts/make-wins.py  ->  assets/wins.svg"""
import math
import random
from pathlib import Path

from theme import ACCENT, BG, FAINT, FG, MUTED, PANEL, RULE, svg, text

OUT = Path(__file__).resolve().parent.parent / "assets" / "wins.svg"
W, H = 1200, 360

# ---- left: 1st of 14,000+ — a field of entries narrowing to one ----------
rnd = random.Random(2)
FX, FY, COLS, ROWS, GAP = 360, 92, 26, 14, 9
field = []
win_i, win_j = 19, 6
for i in range(COLS):
    for j in range(ROWS):
        if (i, j) == (win_i, win_j):
            continue
        d = rnd.uniform(0, 3.2)
        field.append(f'<circle class="out" style="animation-delay:{d:.2f}s" cx="{FX + i * GAP}" cy="{FY + j * GAP}" r="1.6" fill="{MUTED}"/>')
wx, wy = FX + win_i * GAP, FY + win_j * GAP
winner = (f'<circle cx="{wx}" cy="{wy}" r="3.2" fill="{ACCENT}"/>'
          f'<circle class="ping" cx="{wx}" cy="{wy}" r="5" fill="none" stroke="{ACCENT}"/>'
          f'<line class="lead" x1="{wx}" y1="{wy}" x2="{wx}" y2="{FY + ROWS * GAP + 14}" stroke="{ACCENT}" stroke-dasharray="2 3"/>'
          + text(wx, FY + ROWS * GAP + 30, "Cassandra", "di", 16, ACCENT, "middle"))
left = (
    text(40, 52, "GOOGLE CLOUD RAPID AGENT HACKATHON · 2026", "m", 10.5, MUTED, ls=1.8)
    + text(36, 168, "1st", "d", 120, FG, ls=-3)
    + text(40, 206, "of 14,000+ participants", "di", 26, MUTED)
    + f'<line x1="40" x2="330" y1="236" y2="236" stroke="{RULE}"/>'
    + text(40, 262, "ARIZE TRACK · $5,000 PRIZE", "mm", 11, ACCENT, ls=1.4)
    + text(40, 284, "An agent that watches other agents and heals them.", "s", 13, MUTED)
    + text(40, 304, "Built with Sirjan Singh.", "s", 13, MUTED)
    + "".join(field) + winner
)

# ---- right: HackCrux — the 36-hour clock --------------------------------
CX, CY, R = 1078, 196, 74
ticks = []
for h in range(36):
    a = -math.pi / 2 + h / 36 * 2 * math.pi
    r1 = R - (10 if h % 6 == 0 else 5)
    ticks.append(f'<line x1="{CX + r1 * math.cos(a):.1f}" y1="{CY + r1 * math.sin(a):.1f}" '
                 f'x2="{CX + R * math.cos(a):.1f}" y2="{CY + R * math.sin(a):.1f}" stroke="{FAINT if h % 6 else MUTED}"/>')
for h in (0, 12, 24):
    a = -math.pi / 2 + h / 36 * 2 * math.pi
    ticks.append(text(f"{CX + (R + 16) * math.cos(a):.1f}", f"{CY + (R + 16) * math.sin(a) + 4:.1f}", f"{h}h", "m", 9, MUTED, "middle"))
circ = 2 * math.pi * (R - 18)
ring = (f'<circle cx="{CX}" cy="{CY}" r="{R - 18}" fill="none" stroke="{PANEL}" stroke-width="6"/>'
        f'<circle class="clock" cx="{CX}" cy="{CY}" r="{R - 18}" fill="none" stroke="{ACCENT}" stroke-width="6" '
        f'stroke-linecap="round" pathLength="100" stroke-dasharray="100" transform="rotate(-90 {CX} {CY})"/>')
# a tiny driving trace inside the clock
trace = "M" + " L".join(f"{CX - 36 + x * 1.44:.1f} {CY + 6 + (-16 if 18 <= x <= 21 else 0) + 4 * math.sin(x / 3.2):.1f}" for x in range(51))
inner = (f'<path class="drive" d="{trace}" fill="none" stroke="{FG}" stroke-width="1.4" style="--len:200"/>'
         + text(CX, CY + 34, "36h", "di", 15, MUTED, "middle"))
right = (
    f'<line x1="790" x2="790" y1="40" y2="320" stroke="{RULE}"/>'
    + text(820, 52, "HACKCRUX · NATIONAL HACKATHON", "m", 10.5, MUTED, ls=1.8)
    + text(818, 112, "Winner", "d", 52, FG, ls=-1)
    + text(820, 140, "telematics", "di", 20, MUTED)
    + f'<line x1="820" x2="980" y1="236" y2="236" stroke="{RULE}"/>'
    + text(820, 262, "36-HOUR BUILD", "mm", 11, ACCENT, ls=1.4)
    + text(820, 284, "Driver behaviour scoring", "s", 13, MUTED)
    + text(820, 304, "from raw trip data.", "s", 13, MUTED)
    + "".join(ticks) + ring + inner
)

css = """
.out{animation:out 7s ease-in-out infinite}
@keyframes out{0%,8%{opacity:.9}40%,80%{opacity:.12}100%{opacity:.9}}
.lead{stroke-dashoffset:40;animation:lead 7s ease-in-out infinite}
@keyframes lead{0%,40%{opacity:0}55%,90%{opacity:1}100%{opacity:0}}
.clock{animation:arc36 7s cubic-bezier(.4,0,.2,1) infinite}
@keyframes arc36{0%{stroke-dashoffset:100;opacity:1}55%,90%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}
.drive{stroke-dasharray:var(--len);stroke-dashoffset:var(--len);animation:drive 7s ease-in-out infinite}
@keyframes drive{0%,20%{stroke-dashoffset:var(--len)}60%,90%{stroke-dashoffset:0}100%{stroke-dashoffset:0;opacity:0}}
"""
OUT.write_text(svg(W, H, left + right,
                   "Wins: 1st of 14,000+ at the Google Cloud Rapid Agent Hackathon 2026 with Cassandra; winner of HackCrux with a telematics project.",
                   css))
print("wrote", OUT)
