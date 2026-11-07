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
from theme import PANEL
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

def win_badge(label):
    w = len(label) * 7.4 + 26
    return (f'<rect x="{572 - w:.1f}" y="24" width="{w:.1f}" height="24" rx="12" fill="{ACCENT}"/>'
            + t(572 - w / 2, 40, label, 10.5, BG, anchor="middle", weight=500, ls=1.4)
            + f'<rect class="shine" x="{572 - w:.1f}" y="24" width="18" height="24" fill="#fff" opacity=".25"/>')

CARD_CSS += """
.shine{animation:shine 4s ease-in-out infinite}
@keyframes shine{0%,60%{transform:translateX(0);opacity:0}70%{opacity:.35}100%{transform:translateX(220px);opacity:0}}
"""

def frame(kicker, title, badge, desc_lines, body, css="", label="", win=False):
    desc = "".join(t(28, 284 + i * 21, l, 14, MUTED, "s", ls=0) for i, l in enumerate(desc_lines))
    head = (t(28, 40, kicker, 10.5, MUTED, ls=1.8)
            + t(26, 74, title, 38, FG, "d", ls=-.6)
            + (win_badge(badge) if win else t(572, 40, badge, 10.5, ACCENT, anchor="end", weight=500, ls=1.4)))
    return theme_svg(W, H, head + body + f'<line x1="28" x2="572" y1="258" y2="258" stroke="{RULE}"/>' + desc,
                     label, CARD_CSS + css)

# ---------------------------------------------------------------- 1. Route Resilience
def route_resilience():
    rnd = random.Random(3)
    X0, Y0, CELL, N, M = 28, 102, 14, 13, 10  # satellite tile 182 x 140
    tiles = []
    for i in range(N):
        for j in range(M):
            g = rnd.choice(["#161b22", "#1c2128", "#21262d", "#151a21", "#1f242c"])
            tiles.append(f'<rect x="{X0+i*CELL}" y="{Y0+j*CELL}" width="{CELL-1.5}" height="{CELL-1.5}" rx="2" fill="{g}"/>')
    # a few "cloud / tree occlusion" blobs
    occl = "".join(f'<rect x="{X0+i*CELL}" y="{Y0+j*CELL}" width="{CELL*w-1.5}" height="{CELL*h-1.5}" rx="4" fill="#30363d" opacity=".9"/>'
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
            es.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#3d444d" stroke-width="1.6"/>')
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
    spans = [(0, 150, "agent.run", LAV), (14, 60, "llm.plan", "#484f58"), (30, 46, "tool.lookup", RED),
             (80, 56, "llm.answer", "#484f58"), (96, 40, "respond", "#484f58")]
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
    return frame("THE AGENT THAT WATCHES AGENTS", "Cassandra", "1ST / 14,000+ · GOOGLE CLOUD",
                 ["Reads live Phoenix traces, catches the failing span, writes evals, patches the",
                  "prompt and red-teams its own fix. No human in the loop."],
                 body, css, "Cassandra project card", win=True)

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
    return frame("TELEMATICS → INSURANCE RISK", "Driver Safety Score", "WINNER · HACKCRUX",
                 ["Won HackCrux, a 36-hour national hackathon. Raw trip data becomes a",
                  "CIBIL-style 300–900 score: safer drivers pay less, insurers price risk."],
                 body, css, "Driver Safety Score project card", win=True)


# ---------------------------------------------------------------- 4. Two-wheeler damage AI
def damage_ai():
    # stylised claim photo: a bike panel with damage regions revealed by a scan
    X0, Y0, PW, PH = 28, 100, 230, 140
    photo = (f'<rect x="{X0}" y="{Y0}" width="{PW}" height="{PH}" rx="4" fill="{PANEL}" stroke="{RULE}"/>'
             f'<circle cx="78" cy="212" r="22" fill="none" stroke="{MUTED}" stroke-width="1.4"/>'
             f'<circle cx="212" cy="212" r="22" fill="none" stroke="{MUTED}" stroke-width="1.4"/>'
             f'<path d="M78 212 L118 178 L178 178 L212 212 M150 178 L132 212 L78 212" fill="none" stroke="{FAINT}" stroke-width="1.4"/>'
             f'<path d="M112 176 C118 152 150 146 172 156 L176 176Z" fill="none" stroke="{MUTED}" stroke-width="1.4"/>'
             f'<path d="M168 158 L214 160 L210 170 L172 170" fill="none" stroke="{MUTED}" stroke-width="1.4"/>'
             f'<path d="M212 212 L196 150 L186 140 M196 150 L206 144" fill="none" stroke="{MUTED}" stroke-width="1.4"/>')
    masks = [("SCRATCH", "M124 160 L160 152 L162 157 L126 166Z", OCHRE, 0.6),
             ("DENT", "M140 166 C148 160 162 162 164 170 C162 178 148 179 142 174Z", ACCENT, 1.3),
             ("DAMAGE", "M196 196 L214 192 L222 214 L204 220Z", "#d2a8ff", 2.0)]
    m = ""
    for name, d, c, delay in masks:
        m += (f'<path class="mask" style="animation-delay:{delay}s" d="{d}" fill="{c}" fill-opacity=".45" stroke="{c}" stroke-width="1.2"/>')
    scan = f'<rect class="dscan" x="{X0}" y="{Y0}" width="2" height="{PH}" fill="{ACCENT}" opacity=".7"/>'
    clip = f'<clipPath id="ph"><rect x="{X0}" y="{Y0}" width="{PW}" height="{PH}" rx="4"/></clipPath>'
    left = clip + photo + f'<g clip-path="url(#ph)">{m}{scan}</g>' + t(X0, 95, "CLAIM PHOTO", 10, MUTED, ls=1.4)

    # pipeline stages on the right
    stages = [("SEGMENT", "SegFormer", 0.4), ("DEPTH", "MiDaS", 1.1), ("DIRECTION", "Hough", 1.8), ("FRAUD?", "EffNet-B4", 2.5)]
    right = ""
    for k, (a, b, d) in enumerate(stages):
        y = 112 + k * 32
        right += (f'<g class="stage" style="animation-delay:{d}s">'
                  f'<rect x="300" y="{y - 14}" width="160" height="24" rx="4" fill="{PANEL}" stroke="{RULE}"/>'
                  + t(312, y + 2, a, 10, FG, ls=1.2) + t(452, y + 2, b, 9.5, MUTED, anchor="end", ls=.3) + "</g>")
        if k < 3:
            right += f'<line x1="380" x2="380" y1="{y + 10}" y2="{y + 18}" stroke="{FAINT}"/>'
    right += f'<path class="flow" d="M262 170 H296" stroke="{FG}" fill="none"/>'
    verdict = (f'<g class="verdict"><rect x="480" y="150" width="92" height="40" rx="4" fill="none" stroke="{SAGE}"/>'
               + t(526, 166, "GENUINE", 10, SAGE, anchor="middle", weight=500, ls=1.4)
               + t(526, 181, "p = 0.94", 10, MUTED, anchor="middle", ls=.3) + "</g>"
               + f'<path class="flow" d="M462 170 H478" stroke="{SAGE}" fill="none"/>')
    legend = "".join(f'<rect x="{300 + k * 80}" y="236" width="8" height="8" fill="{c}" fill-opacity=".7"/>'
                     + t(312 + k * 80, 244, n, 9, MUTED, ls=1) for k, (n, _, c, _d) in enumerate(masks))
    css = """.mask{opacity:0;animation:mask 6s ease-in-out infinite}
@keyframes mask{0%,8%{opacity:0}15%,85%{opacity:1}100%{opacity:0}}
.dscan{animation:dscan 6s linear infinite}
@keyframes dscan{0%{transform:translateX(0)}50%,100%{transform:translateX(228px);opacity:0}}
.stage{opacity:.25;animation:stage 6s ease-in-out infinite}
@keyframes stage{0%{opacity:.25}10%,85%{opacity:1}100%{opacity:.25}}
.verdict{opacity:0;animation:verdict 6s ease-in-out infinite;animation-delay:3.1s}
@keyframes verdict{0%{opacity:0}8%,60%{opacity:1}75%,100%{opacity:0}}"""
    return frame("COMPUTER VISION FOR INSURANCE", "Two-wheeler Damage AI", "SURVEYORS AI · PRODUCTION",
                 ["Finds scratches, dents and damage in claim photos, estimates severity from",
                  "depth, and flags inconsistent damage as possible fraud. 7,149 images, 22,487 labels."],
                 left + right + verdict + legend, css, "Two-wheeler damage AI project card")

# ---------------------------------------------------------------- 5. Music source separation
def music_sep():
    rnd = random.Random(5)
    X0, Y0 = 28, 104
    cols, rows, cw, ch = 30, 12, 7, 10
    spec = ""
    for i in range(cols):
        for j in range(rows):
            v = max(0.05, min(1, rnd.random() * (1.2 - j / rows) * (0.6 + 0.4 * math.sin(i / 3))))
            spec += f'<rect x="{X0 + i * cw}" y="{Y0 + j * ch}" width="{cw - 1}" height="{ch - 1}" fill="{FG}" fill-opacity="{v * .55:.2f}"/>'
    spec += t(X0, 98, "MIXTURE SPECTROGRAM", 10, MUTED, ls=1.4)
    play = f'<rect class="playhead" x="{X0}" y="{Y0 - 2}" width="1.5" height="{rows * ch + 4}" fill="{ACCENT}"/>'
    unet = (f'<path d="M258 120 L278 138 L278 196 L258 214Z" fill="none" stroke="{MUTED}"/>'
            f'<path d="M298 138 L318 120 L318 214 L298 196Z" fill="none" stroke="{MUTED}"/>'
            f'<path class="flow" d="M278 167 H298" stroke="{FG}" fill="none"/>'
            + t(288, 232, "U-Net", 11, FG, "di", anchor="middle", ls=0)
            + f'<path class="flow" d="M244 167 H256" stroke="{FG}" fill="none"/>')
    stems = [("VOCALS", ACCENT, 1.0, 9), ("DRUMS", OCHRE, 2.2, 5), ("BASS", SAGE, .7, 14), ("OTHER", "#d2a8ff", 1.4, 7)]
    out = ""
    for k, (name, c, amp, per) in enumerate(stems):
        y = 118 + k * 30
        pts = " ".join(f"{350 + x * 1.55:.1f},{y + amp * 5 * math.sin(x / per * 2) * (0.6 + 0.4 * math.sin(x / 13)):.1f}" for x in range(0, 101))
        out += (f'<g class="stem" style="animation-delay:{.3 + k * .35:.2f}s">'
                + t(572, y + 4, name, 9.5, c, anchor="end", ls=1.2)
                + f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="1.4"/></g>'
                + f'<path class="flow" d="M322 167 L344 {y}" stroke="{FAINT}" fill="none"/>')
    css = """.playhead{animation:play 5s linear infinite}
@keyframes play{from{transform:translateX(0)}to{transform:translateX(210px)}}
.stem{opacity:0;animation:stem 5s ease-in-out infinite}
@keyframes stem{0%,10%{opacity:0}25%,85%{opacity:1}100%{opacity:0}}"""
    return frame("ONE TRACK IN, FOUR STEMS OUT", "Music Source Separation", "MUSDB18 · PYTORCH",
                 ["A spectrogram U-Net learns ratio masks that pull vocals, drums, bass and",
                  "everything else out of a single mixed recording."],
                 spec + play + unet + out, css, "Music source separation project card")

# ---------------------------------------------------------------- 6. Atmospheric turbulence corrector
def turbulence():
    rnd = random.Random(9)
    # left: twinkling, smeared stars; right: restored sharp ones
    starsL, starsR = "", ""
    pts = [(rnd.uniform(40, 220), rnd.uniform(108, 236), rnd.choice([1, 1, 1.5, 2.2])) for _ in range(26)]
    for k, (x, y, r) in enumerate(pts):
        starsL += (f'<g class="wob w{k % 3}"><circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 3.2:.1f}" fill="{FG}" fill-opacity=".10"/>'
                   f'<circle cx="{x + 1.5:.1f}" cy="{y - 1:.1f}" r="{r * 1.8:.1f}" fill="{FG}" fill-opacity=".22"/></g>')
        starsR += f'<circle cx="{x + 312:.1f}" cy="{y:.1f}" r="{r * .9:.1f}" fill="{FG}"/>'
    # one bright target with PSF readout
    starsL += (f'<g class="wob w1"><circle cx="130" cy="170" r="16" fill="{ACCENT}" fill-opacity=".12"/>'
               f'<circle cx="133" cy="168" r="8" fill="{ACCENT}" fill-opacity=".35"/></g>')
    starsR += (f'<circle cx="442" cy="170" r="3.2" fill="{ACCENT}"/>'
               f'<circle class="pulse" cx="442" cy="170" r="5" fill="none" stroke="{ACCENT}"/>')
    frameL = f'<rect x="28" y="100" width="210" height="146" rx="4" fill="none" stroke="{RULE}"/>' + t(28, 95, "OBSERVED · SEEING-LIMITED", 10, MUTED, ls=1.2)
    frameR = f'<rect x="340" y="100" width="210" height="146" rx="4" fill="none" stroke="{RULE}"/>' + t(340, 95, "RESTORED", 10, MUTED, ls=1.2)
    # PSF kernel in the middle
    psf = ""
    for i in range(5):
        for j in range(5):
            v = math.exp(-((i - 2) ** 2 + (j - 2.3) ** 2) / 2.2)
            psf += f'<rect x="{262 + i * 11}" y="{140 + j * 11}" width="10" height="10" fill="{ACCENT}" fill-opacity="{v:.2f}"/>'
    psf += t(289, 132, "PSF", 10, MUTED, anchor="middle", ls=1.4) + t(289, 214, "NAFNet", 11, FG, "di", anchor="middle", ls=0)
    psf += (f'<path class="flow" d="M240 173 H258" stroke="{FG}" fill="none"/>'
            f'<path class="flow" d="M320 173 H336" stroke="{FG}" fill="none"/>')
    reveal = f'<rect class="wipe" x="340" y="101" width="210" height="144" fill="{BG}"/>'
    css = """.wob{transform-box:fill-box;transform-origin:center;animation:wob 1.6s ease-in-out infinite}
.w1{animation-duration:1.1s;animation-delay:-.4s}.w2{animation-duration:2.1s;animation-delay:-.9s}
@keyframes wob{0%,100%{transform:translate(0,0) scale(1)}25%{transform:translate(1.5px,-1px) scale(1.08)}50%{transform:translate(-1px,1.5px) scale(.95)}75%{transform:translate(1px,1px) scale(1.04)}}
.wipe{transform-box:fill-box;transform-origin:right;animation:wipe 6s ease-in-out infinite}
@keyframes wipe{0%,10%{transform:scaleX(1)}45%,85%{transform:scaleX(0)}100%{transform:scaleX(1)}}"""
    return frame("ASTRONOMY × COMPUTER VISION", "Turbulence Corrector", "MAJOR PROJECT · LNMIIT",
                 ["The atmosphere smears every star. Estimate the blur kernel (PSF), then a",
                  "NAFNet restorer takes the twinkle out of ground-based telescope images."],
                 frameL + starsL + psf + frameR + starsR + reveal, css, "Atmospheric turbulence corrector project card")

for name, fn in [("01-route-resilience", route_resilience), ("02-cassandra", cassandra), ("03-driver-score", driver_score),
                 ("04-damage-ai", damage_ai), ("05-music-separation", music_sep), ("06-turbulence", turbulence)]:
    (OUT / f"{name}.svg").write_text(fn())
    print("wrote", name)
