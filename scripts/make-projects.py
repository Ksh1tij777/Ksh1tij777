"""Animated project cards for Ksh1tij777's profile README.
Writes assets/projects/{01-route-resilience,02-cassandra,03-driver-score}.svg
Palette matches assets/header.svg (deep navy + lavender/cyan/amber)."""
import math, random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "projects"; OUT.mkdir(parents=True, exist_ok=True)
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from theme import ACCENT, BG, FAINT, FG, MUTED, OCHRE, RULE, SAGE, svg as theme_svg, text as ttext

W, H = 600, 330
PANEL = "#1c1a17"
# role colours: lines/ink = FG, highlight = ACCENT, caution = OCHRE, ok = SAGE
LAV, CYAN, AMBER, RED, GREEN = FG, FG, OCHRE, ACCENT, SAGE
MONO, SANS = "m", "s"

CARD_CSS = """
.draw{stroke-dasharray:var(--len,800);stroke-dashoffset:var(--len,800);animation:draw 6s ease-in-out infinite}
@keyframes draw{0%{stroke-dashoffset:var(--len,800)}35%,85%{stroke-dashoffset:0}100%{stroke-dashoffset:0;opacity:0}}
.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.2s ease-out infinite}
@keyframes pulse{0%{transform:scale(.6);opacity:.8}100%{transform:scale(2.6);opacity:0}}
.blink{animation:blink 6s ease-in-out infinite}
@keyframes blink{0%,30%{opacity:0}40%,85%{opacity:1}100%{opacity:0}}
"""

def t(x, y, s, size=10.5, fill=MUTED, font=MONO, anchor="start", weight=None, ls=1.2, extra=""):
    cls = font if font in ("d", "di", "m", "mm", "s") else "m"
    if weight and cls == "m":
        cls = "mm"
    return ttext(x, y, s, cls, size, fill, anchor, ls, extra)

def frame(kicker, title, badge, desc_lines, body, css="", label=""):
    desc = "".join(t(28, 284 + i * 21, l, 14, MUTED, "s", ls=0) for i, l in enumerate(desc_lines))
    head = (t(28, 40, kicker, 10.5, MUTED, ls=1.8)
            + t(26, 74, title, 38, FG, "d", ls=-.6)
            + t(572, 40, badge, 10.5, ACCENT, anchor="end", weight=500, ls=1.4))
    return theme_svg(W, H, head + body + f'<line x1="28" x2="572" y1="258" y2="258" stroke="{RULE}"/>' + desc,
                     label, CARD_CSS + css)

# ---------------------------------------------------------------- 1. Route Resilience
def route_resilience():
    rnd = random.Random(3)
    X0, Y0, CELL, N, M = 28, 102, 14, 13, 10  # satellite tile 182 x 140
    tiles = []
    for i in range(N):
        for j in range(M):
            g = rnd.choice(["#1d1b18", "#211f1b", "#24221e", "#1a1916", "#262420"])
            tiles.append(f'<rect x="{X0+i*CELL}" y="{Y0+j*CELL}" width="{CELL-1.5}" height="{CELL-1.5}" rx="2" fill="{g}"/>')
    # a few "cloud / tree occlusion" blobs
    occl = "".join(f'<rect x="{X0+i*CELL}" y="{Y0+j*CELL}" width="{CELL*w-1.5}" height="{CELL*h-1.5}" rx="4" fill="#3a362f" opacity=".7"/>'
                   for i, j, w, h in [(3, 2, 2, 2), (8, 6, 3, 2)])
    roads = [
        ("M28 159 C80 155 120 165 210 158", 190),
        ("M98 96 C100 140 92 190 102 236", 150),
        ("M150 96 C152 130 160 160 156 236", 150),
        ("M28 208 C70 205 130 214 210 204", 190),
    ]
    road_svg = "".join(
        f'<path class="draw" style="--len:{L};animation-delay:{0.35*k:.2f}s" d="{d}" stroke="{CYAN}" stroke-width="3" fill="none" stroke-linecap="round"/>'
        for k, (d, L) in enumerate(roads))
    scan = f'<rect class="scan" x="{X0}" y="{Y0}" width="182" height="2" fill="{LAV}" opacity=".9"/>'
    tile = f'<g><clipPath id="tc"><rect x="{X0}" y="{Y0}" width="182" height="140" rx="6"/></clipPath><g clip-path="url(#tc)">{"".join(tiles)}{occl}<g transform="translate(0,6)">{road_svg}</g>{scan}</g></g>'

    # arrow
    arrow = (f'<path class="flow" d="M222 166 H262" stroke="{LAV}" fill="none"/>'
             f'<path d="M262 161 L270 166 L262 171Z" fill="{LAV}"/>'
             + t(246, 152, "SegFormer", 9.5, MUTED, anchor="middle", ls=.6)
             + t(246, 190, "+ clDice", 9.5, MUTED, anchor="middle", ls=.6))

    # road graph
    nodes = {"a": (300, 118), "b": (360, 108), "c": (420, 126), "d": (300, 168), "e": (365, 162),
             "f": (430, 176), "g": (310, 222), "h": (372, 214), "i": (440, 226), "j": (500, 150),
             "k": (540, 110), "l": (548, 200)}
    edges = ["ab", "bc", "ad", "be", "cf", "de", "ef", "dg", "eh", "fi", "gh", "hi", "cj", "fj", "jk", "jl", "il"]
    crit = {"fj", "cj"}
    es = []
    for k, (u, v) in enumerate(edges):
        (x1, y1), (x2, y2) = nodes[u], nodes[v]
        if u + v in crit:
            es.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{AMBER}" stroke-width="3" class="critical"/>')
        else:
            es.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#4a463f" stroke-width="1.6"/>')
    ns = []
    for k, (x, y) in nodes.items():
        c = AMBER if k in "cfj" else LAV
        ns.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="{BG}" stroke="{c}" stroke-width="2"/>')
    jx, jy = nodes["j"]
    pulse = f'<circle class="pulse" cx="{jx}" cy="{jy}" r="6" fill="none" stroke="{AMBER}" stroke-width="1.5"/>'
    # traffic dots flowing over the network, forced through the bottleneck
    dots = "".join(
        f'<circle r="3" fill="{CYAN}"><animateMotion dur="{d}s" begin="{b}s" repeatCount="indefinite" path="{p}"/></circle>'
        for p, d, b in [("M300 118 L360 108 L420 126 L500 150 L540 110", 4, 0),
                        ("M310 222 L372 214 L440 226 L548 200", 4.5, .8),
                        ("M300 168 L365 162 L430 176 L500 150 L548 200", 4.2, 1.6)])
    labels = (t(300, 95, "ROAD GRAPH", 10, MUTED, ls=1.4)
              + t(572, 250, "high betweenness = critical link", 10, AMBER, anchor="end", ls=.4, extra='class="blink"')
              + t(28, 95, "SENTINEL-2 TILE", 10, MUTED, ls=1.4))
    css = """.scan{animation:scan 3.2s ease-in-out infinite alternate}
@keyframes scan{from{transform:translateY(0)}to{transform:translateY(138px)}}
.critical{animation:crit 1.6s ease-in-out infinite}
@keyframes crit{0%,100%{stroke-opacity:.45}50%{stroke-opacity:1}}"""
    body = tile + arrow + "".join(es) + dots + "".join(ns) + pulse + labels
    return frame("SATELLITE ROADS → CITY RESILIENCE", "Route Resilience", "ISRO / NNRMS · JAIPUR",
                 ["SegFormer + clDice pull roads out of occluded Sentinel-2 imagery; graph",
                  "centrality flags the links a city can't afford to lose.  IoU 0.47 · Dice 0.64"],
                 body, css, "Route Resilience project card")

# ---------------------------------------------------------------- 2. Cassandra
def cassandra():
    # trace waterfall on the left
    spans = [(0, 150, "agent.run", LAV), (14, 60, "llm.plan", "#6f685d"), (30, 46, "tool.lookup", RED),
             (80, 56, "llm.answer", "#6f685d"), (96, 40, "respond", "#6f685d")]
    X0, Y0 = 28, 108
    rows = []
    for k, (off, w, name, c) in enumerate(spans):
        y = Y0 + k * 24
        cls = 'class="bad"' if c == RED else ""
        rows.append(f'<rect x="{X0+70+off}" y="{y}" width="{w}" height="12" rx="3" fill="{c}" opacity=".85" {cls}>'
                    f'<animate attributeName="width" from="0" to="{w}" dur="0.6s" begin="{0.25*k:.2f}s" fill="freeze"/></rect>')
        rows.append(t(X0, y + 10, name, 9.5, MUTED, ls=.4))
    bad_y = Y0 + 2 * 24 + 6
    flag = (f'<circle class="pulse" cx="{X0+70+30+46+10}" cy="{bad_y}" r="5" fill="none" stroke="{RED}" stroke-width="1.5"/>'
            + t(X0 + 70 + 30 + 46 + 28, bad_y + 4, "empty → fabricated", 9.5, RED, ls=.3))
    eye_scan = f'<rect class="eyescan" x="{X0+66}" y="{Y0-6}" width="2" height="122" fill="{CYAN}" opacity=".8"/>'
    waterfall = t(X0, 95, "PHOENIX TRACE", 10, MUTED, ls=1.4) + "".join(rows) + eye_scan + flag

    # healing loop on the right
    cx, cy, R = 470, 166, 62
    stages = ["DIAGNOSE", "EVALS", "PATCH", "RED-TEAM"]
    ring = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{RULE}" stroke-width="1.5"/>'
    ring += f'<circle class="flow" cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{LAV}" stroke-opacity=".6"/>'
    st = []
    for k, s in enumerate(stages):
        a = -math.pi / 2 + k * math.pi / 2
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        st.append(f'<path d="M{x:.1f} {y-6:.1f}L{x+6:.1f} {y:.1f}L{x:.1f} {y+6:.1f}L{x-6:.1f} {y:.1f}Z" fill="{CYAN if k == 0 else FG}"/>')
        lx = x + (14 if k == 1 else 0)
        ly = y + {0: -12, 1: 4, 2: 22, 3: -14}[k]
        st.append(t(f"{lx:.1f}", f"{ly:.1f}", s, 9.5, MUTED, anchor="start" if k == 1 else "middle", ls=1))
    orbit = (f'<circle r="4.5" fill="{CYAN}"><animateMotion dur="4s" repeatCount="indefinite" '
             f'path="M{cx} {cy-R} A{R} {R} 0 1 1 {cx-0.01} {cy-R}"/></circle>')
    eye = (f'<circle cx="{cx}" cy="{cy}" r="20" fill="{PANEL}" stroke="{LAV}" stroke-width="1.5"/>'
           f'<circle class="iris" cx="{cx}" cy="{cy}" r="8" fill="{LAV}"/><circle cx="{cx}" cy="{cy}" r="3.5" fill="{BG}"/>')
    link = (f'<path class="flow" d="M{X0+250} 164 C340 164 360 188 {cx-R-14} 188" stroke="{RED}" stroke-opacity=".8" fill="none"/>'
            f'<path d="M{cx-R-14} 183 L{cx-R-6} 188 L{cx-R-14} 193Z" fill="{RED}"/>')
    fixed = t(98, 246, "✓ fix replayed on the original failure", 10, GREEN, anchor="start", ls=.3, extra='class="blink"')
    css = """.eyescan{animation:es 3s ease-in-out infinite}
@keyframes es{0%{transform:translateX(0)}60%,100%{transform:translateX(200px);opacity:0}}
.bad{animation:bad 1.4s ease-in-out infinite}
@keyframes bad{0%,100%{opacity:.45}50%{opacity:1}}
.iris{transform-box:fill-box;transform-origin:center;animation:look 4s ease-in-out infinite}
@keyframes look{0%,100%{transform:translate(-5px,0)}50%{transform:translate(5px,0)}}"""
    body = waterfall + link + ring + "".join(st) + orbit + eye + fixed
    return frame("THE AGENT THAT WATCHES AGENTS", "Cassandra", "1ST OF 14,000+ · GOOGLE CLOUD",
                 ["Reads live Phoenix traces, catches the failing span, writes evals, patches the",
                  "prompt and red-teams its own fix. No human in the loop."],
                 body, css, "Cassandra project card")

# ---------------------------------------------------------------- 3. Driver safety score
def driver_score():
    # accelerometer trace, two copies side by side for a seamless scroll
    rnd = random.Random(11)
    pts, events = [], []
    X0, Y0, WID = 28, 165, 300
    for i in range(0, WID + 1, 4):
        y = 10 * math.sin(i / 17) + rnd.uniform(-3, 3)
        if 70 <= i <= 82:   y = -42 + (i - 70) * 2      # hard brake spike
        if 190 <= i <= 202: y = 38 - (i - 190) * 2      # sharp turn
        pts.append((i, y))
    events = [(76, -44, "HARD BRAKE", RED), (196, 40, "SHARP TURN", AMBER)]
    def path(dx):
        return "M" + " L".join(f"{X0+dx+x:.1f} {Y0+y:.1f}" for x, y in pts)
    sig = f'<path d="{path(0)}" stroke="{CYAN}" stroke-width="1.8" fill="none"/><path d="{path(WID)}" stroke="{CYAN}" stroke-width="1.8" fill="none"/>'
    marks = ""
    for dx in (0, WID):
        for x, y, name, c in events:
            ty = Y0 + y + (-10 if y < 0 else 18)
            marks += (f'<circle cx="{X0+dx+x}" cy="{Y0+y}" r="4" fill="{c}"/>'
                      + t(X0 + dx + x, ty, name, 9, c, anchor="middle", ls=.8))
    scroller = f'<g class="scroll">{sig}{marks}</g>'
    clip = f'<clipPath id="sc"><rect x="{X0}" y="100" width="{WID}" height="150"/></clipPath>'
    axis = (f'<line x1="{X0}" x2="{X0+WID}" y1="{Y0}" y2="{Y0}" stroke="{RULE}" stroke-dasharray="2 4"/>'
            + t(X0, 95, "ACCEL · GYRO · SPEED", 10, MUTED, ls=1.4))
    fade_edges = (f'<linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
                  f'<linearGradient id="fr" x1="0" x2="1"><stop offset="0" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}"/></linearGradient>'
                  f'<rect x="{X0}" y="96" width="30" height="146" fill="url(#fl)"/><rect x="{X0+WID-30}" y="96" width="30" height="146" fill="url(#fr)"/>')
    signal = clip + axis + f'<g clip-path="url(#sc)">{scroller}</g>' + fade_edges

    arrow = (f'<path class="flow" d="M340 166 H372" stroke="{LAV}" fill="none"/><path d="M372 161 L380 166 L372 171Z" fill="{LAV}"/>')

    # score gauge 300..900
    cx, cy, R = 478, 186, 74
    def pt(frac, r=R):
        a = math.pi + frac * math.pi
        return cx + r * math.cos(a), cy + r * math.sin(a)
    segs = [(0, .33, RED), (.33, .66, AMBER), (.66, 1, GREEN)]
    arcs = ""
    for a0, a1, c in segs:
        (x0, y0), (x1, y1) = pt(a0 + .006), pt(a1 - .006)
        arcs += f'<path d="M{x0:.1f} {y0:.1f} A{R} {R} 0 0 1 {x1:.1f} {y1:.1f}" stroke="{c}" stroke-width="10" fill="none" stroke-opacity=".85"/>'
    ticks = "".join(t(f"{pt(f, R+16)[0]:.1f}", f"{pt(f, R+16)[1]+4:.1f}", v, 9, MUTED, anchor="middle", ls=0)
                    for f, v in [(0, "300"), (.5, "600"), (1, "900")])
    needle = (f'<g class="needle"><line x1="{cx}" y1="{cy}" x2="{cx-R+24}" y2="{cy}" stroke="{FG}" stroke-width="2.5" stroke-linecap="round"/></g>'
              f'<circle cx="{cx}" cy="{cy}" r="6" fill="{FG}"/>')
    score = (t(cx - 26, cy - 10, "742", 34, FG, "d", anchor="middle", ls=0, extra='class="blink"')
             + t(cx, cy + 22, "SAFETY SCORE", 9.5, MUTED, anchor="middle", ls=1.4)
             + t(cx, cy + 38, "→ lower premium", 9.5, GREEN, anchor="middle", ls=.4, extra='class="blink"'))
    # needle sweeps 300 → ~742 (frac .737 → 132.7deg), holds, returns
    css = f""".scroll{{animation:scroll 7s linear infinite}}
@keyframes scroll{{from{{transform:translateX(0)}}to{{transform:translateX(-{WID}px)}}}}
.needle{{transform-origin:{cx}px {cy}px;animation:needle 6s cubic-bezier(.3,1.4,.5,1) infinite}}
@keyframes needle{{0%{{transform:rotate(0deg)}}35%,85%{{transform:rotate(132.7deg)}}100%{{transform:rotate(0deg)}}}}"""
    body = signal + arrow + arcs + ticks + needle + score
    return frame("TELEMATICS → INSURANCE RISK", "Driver Safety Score", "UAH-DRIVESET · UBI",
                 ["Turns raw driving signals into a portable, CIBIL-style 300–900 score:",
                  "safer drivers pay less, insurers price risk and spot fraud at claim time."],
                 body, css, "Driver Safety Score project card")

for name, fn in [("01-route-resilience", route_resilience), ("02-cassandra", cassandra), ("03-driver-score", driver_score)]:
    (OUT / f"{name}.svg").write_text(fn())
    print("wrote", name)
