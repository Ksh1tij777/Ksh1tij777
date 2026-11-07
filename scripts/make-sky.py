"""'Tonight over Jaipur' widget: moon phase + where Betelgeuse sits at 10 pm IST.
Pure astronomy maths, no API. Run daily: python scripts/make-sky.py -> assets/sky.svg"""
import datetime as dt
import math
import random
from pathlib import Path

from theme import ACCENT, FAINT, FG, MUTED, PANEL, RULE, svg, text

OUT = Path(__file__).resolve().parent.parent / "assets" / "sky.svg"
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
LAT, LON = 26.9124, 75.7873           # Jaipur
SYNODIC = 29.530588853
REF_NEW = dt.datetime(2000, 1, 6, 18, 14, tzinfo=dt.timezone.utc)
BET_RA, BET_DEC = 88.7929, 7.4071     # Betelgeuse, degrees (J2000)


def julian(t: dt.datetime) -> float:
    return t.timestamp() / 86400 + 2440587.5


def moon(t):
    age = ((t - REF_NEW).total_seconds() / 86400) % SYNODIC
    f = age / SYNODIC
    illum = (1 - math.cos(2 * math.pi * f)) / 2
    names = ["New moon", "Waxing crescent", "First quarter", "Waxing gibbous",
             "Full moon", "Waning gibbous", "Last quarter", "Waning crescent"]
    name = names[int((f * 8 + 0.5)) % 8]
    to_full = ((0.5 - f) % 1) * SYNODIC
    to_new = ((1 - f) % 1) * SYNODIC
    return f, illum, age, name, t + dt.timedelta(days=to_full), t + dt.timedelta(days=to_new)


def alt_az(t, ra, dec):
    d = julian(t) - 2451545.0
    lst = (280.46061837 + 360.98564736629 * d + LON) % 360
    h = math.radians((lst - ra) % 360)
    phi, delta = math.radians(LAT), math.radians(dec)
    alt = math.asin(math.sin(phi) * math.sin(delta) + math.cos(phi) * math.cos(delta) * math.cos(h))
    az = math.atan2(-math.sin(h) * math.cos(delta), math.cos(phi) * math.sin(delta) - math.sin(phi) * math.cos(delta) * math.cos(h))
    return math.degrees(alt), math.degrees(az) % 360


def compass(az):
    return ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"][int((az + 22.5) // 45) % 8]


def moon_path(cx, cy, r, f):
    """Lit part of the disc for phase fraction f (0 new, .5 full)."""
    k = math.cos(2 * math.pi * f)          # 1 new → -1 full
    rx = abs(k) * r
    waxing = f < 0.5
    limb_sweep = 1 if waxing else 0        # lit limb on the right while waxing
    term_sweep = (0 if k > 0 else 1) if waxing else (1 if k > 0 else 0)
    return (f"M{cx} {cy - r} A{r} {r} 0 0 {limb_sweep} {cx} {cy + r} "
            f"A{rx:.2f} {r} 0 0 {term_sweep} {cx} {cy - r}Z")


def main():
    now = dt.datetime.now(IST)
    tonight = now.replace(hour=22, minute=0, second=0, microsecond=0)
    f, illum, age, name, nfull, nnew = moon(tonight)
    alt, az = alt_az(tonight.astimezone(dt.timezone.utc), BET_RA, BET_DEC)

    W, H = 600, 290
    rnd = random.Random(now.toordinal())
    stars = "".join(f'<circle class="tw t{k % 3}" cx="{rnd.uniform(330, 580):.1f}" cy="{rnd.uniform(60, 250):.1f}" '
                    f'r="{rnd.choice([.6, .8, 1])}" fill="{FG}"/>' for k in range(40))
    MX, MY, MR = 455, 150, 62
    disc = (f'<circle cx="{MX}" cy="{MY}" r="{MR + 18}" fill="{FG}" fill-opacity=".03"/>'
            f'<circle cx="{MX}" cy="{MY}" r="{MR}" fill="{PANEL}" stroke="{RULE}"/>'
            f'<path class="glow" d="{moon_path(MX, MY, MR, f)}" fill="{FG}" fill-opacity=".92"/>')
    if alt > 0:
        bet = f"Betelgeuse {alt:.0f}° up in the {compass(az)}"
    else:
        bet = "Betelgeuse below the horizon"
    body = (
        text(28, 40, "TONIGHT OVER JAIPUR", "m", 10.5, MUTED, ls=1.8)
        + text(572, 40, tonight.strftime("%d %b %Y").upper(), "mm", 10.5, ACCENT, "end", ls=1.4)
        + text(26, 112, f"{illum * 100:.0f}%", "d", 64, FG, ls=-1)
        + text(28, 142, name.lower(), "di", 22, MUTED)
        + f'<line x1="28" x2="290" y1="166" y2="166" stroke="{RULE}"/>'
        + text(28, 190, f"Moon age {age:.1f} days", "s", 13, MUTED)
        + text(28, 211, f"Next full moon {nfull.strftime('%d %b')}", "s", 13, MUTED)
        + text(28, 232, f"Next new moon {nnew.strftime('%d %b')}", "s", 13, MUTED)
        + text(28, 262, bet + " at 10 pm", "mm" if alt > 0 else "m", 10, ACCENT if alt > 0 else FAINT, ls=.6)
        + stars + disc
    )
    css = """.tw{animation:tw 5s ease-in-out infinite}.t1{animation-delay:-1.7s;animation-duration:6.3s}.t2{animation-delay:-3.1s;animation-duration:4.1s}
@keyframes tw{0%,100%{opacity:.25}50%{opacity:.85}}
.glow{animation:glow 6s ease-in-out infinite}
@keyframes glow{0%,100%{fill-opacity:.85}50%{fill-opacity:1}}"""
    OUT.write_text(svg(W, H, body, f"Tonight over Jaipur: {name}, {illum * 100:.0f}% illuminated.", css))
    print("wrote", OUT, name, f"{illum:.2f}", f"bet alt {alt:.1f} az {az:.0f}")


if __name__ == "__main__":
    main()
