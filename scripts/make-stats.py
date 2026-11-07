#!/usr/bin/env python3
"""Render profile stats SVGs (overview, languages, activity) from the GitHub GraphQL API.

Runs in GitHub Actions with the built-in GITHUB_TOKEN; no personal token needed.
Usage:  GITHUB_TOKEN=... python scripts/make-stats.py [username]
        python scripts/make-stats.py --demo          (fake data, for previews)
Writes assets/stats/{overview,languages,activity}.svg
"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import random
import sys
import urllib.request
from pathlib import Path

USER = next((a for a in sys.argv[1:] if not a.startswith("--")), os.environ.get("GITHUB_USER", "Ksh1tij777"))
EXCLUDE = {"HTML", "Batchfile"}  # generated/boilerplate files skew byte counts
OUT = Path(__file__).resolve().parent.parent / "assets" / "stats"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from theme import ACCENT, BG, FAINT, FG, MUTED, OCHRE, RULE, SAGE, svg as theme_svg, text as ttext

LANG_INK = [ACCENT, FG, OCHRE, SAGE, MUTED, FAINT]
CSS = """
.grow{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation:grow 1.2s cubic-bezier(.2,.8,.2,1) forwards}
@keyframes grow{to{transform:scaleX(1)}}
.draw{stroke-dasharray:var(--len);stroke-dashoffset:var(--len);animation:draw 2.6s ease-out .2s forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.2s ease-out infinite}
@keyframes pulse{0%{transform:scale(.6);opacity:.8}100%{transform:scale(2.6);opacity:0}}
"""

QUERY = """
query($login:String!){
  user(login:$login){
    name login
    followers{totalCount}
    pullRequests{totalCount}
    merged: pullRequests(states:MERGED){totalCount}
    issues{totalCount}
    repositories(first:100, ownerAffiliations:OWNER, isFork:false, privacy:PUBLIC){
      totalCount
      nodes{ stargazerCount languages(first:10, orderBy:{field:SIZE,direction:DESC}){ edges{ size node{ name color } } } }
    }
    contributionsCollection{
      totalCommitContributions restrictedContributionsCount
      contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } }
    }
  }
}"""


def t(x, y, s, size=11, fill=MUTED, font="m", anchor="start", weight=None, ls=1.2, extra=""):
    cls = font if font in ("d", "di", "m", "mm", "s") else "m"
    if weight and cls == "m":
        cls = "mm"
    return ttext(x, y, s, cls, size, fill, anchor, ls, extra)


def svg(w, h, body, label):
    return theme_svg(w, h, body, label, CSS)


# ------------------------------------------------------------------ data
def fetch() -> dict:
    token = os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-stats"})
    data = json.load(urllib.request.urlopen(req, timeout=60))
    if data.get("errors"):
        raise SystemExit(f"GraphQL error: {data['errors']}")
    return data["data"]["user"]


def demo() -> dict:
    rnd = random.Random(1)
    start = dt.date.today() - dt.timedelta(days=370)
    weeks, d = [], start
    while d <= dt.date.today():
        week = []
        for _ in range(7):
            if d > dt.date.today():
                break
            week.append({"date": d.isoformat(), "contributionCount": max(0, int(rnd.gauss(3, 4)))})
            d += dt.timedelta(days=1)
        weeks.append({"contributionDays": week})
    langs = [("Python", "#3572A5", 900), ("Jupyter Notebook", "#DA5B0B", 600), ("JavaScript", "#f1e05a", 200),
             ("HTML", "#e34c26", 120), ("C++", "#f34b7d", 60), ("CSS", "#563d7c", 30)]
    return {"name": "Kshitij Verma", "login": USER, "followers": {"totalCount": 42},
            "pullRequests": {"totalCount": 31}, "merged": {"totalCount": 24}, "issues": {"totalCount": 9},
            "repositories": {"totalCount": 11, "nodes": [{"stargazerCount": 2, "languages": {"edges": [
                {"size": s, "node": {"name": n, "color": c}} for n, c, s in langs]}}]},
            "contributionsCollection": {"totalCommitContributions": 512, "restrictedContributionsCount": 140,
                                        "contributionCalendar": {"totalContributions": 812, "weeks": weeks}}}


def streaks(days):
    counts = [(dt.date.fromisoformat(d["date"]), d["contributionCount"]) for d in days]
    longest = cur = 0
    for _, c in counts:
        cur = cur + 1 if c > 0 else 0
        longest = max(longest, cur)
    current = 0
    for i, (day, c) in enumerate(reversed(counts)):
        if c > 0:
            current += 1
        elif i == 0:          # today may still be empty; don't break the streak yet
            continue
        else:
            break
    return current, longest


# ------------------------------------------------------------------ cards
def overview(u):
    cc = u["contributionsCollection"]
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    current, longest = streaks(days)
    stars = sum(r["stargazerCount"] for r in u["repositories"]["nodes"])
    stats = [
        ("CONTRIBUTIONS · 1Y", cc["contributionCalendar"]["totalContributions"], FG),
        ("COMMITS · 1Y", cc["totalCommitContributions"] + cc["restrictedContributionsCount"], FG),
        ("PRS MERGED", u["merged"]["totalCount"], ACCENT),
        ("PUBLIC REPOS", u["repositories"]["totalCount"], FG),
        ("STARS EARNED", stars, FG),
        ("ISSUES OPENED", u["issues"]["totalCount"], FG),
    ]
    body = t(28, 40, "BY THE NUMBERS", 10.5, MUTED, ls=1.8) + t(572, 40, f"@{u['login']}", 10.5, ACCENT, anchor="end", weight=500, ls=1.2)
    for i, (label, val, col) in enumerate(stats):
        x, y = 28 + (i % 3) * 186, 92 + (i // 3) * 74
        body += (f'<g class="fade" style="animation-delay:{.1 + i * .12:.2f}s">'
                 + t(x, y + 4, f"{val:,}", 44, col, "d", ls=-.5)
                 + t(x, y + 24, label, 9.5, MUTED, ls=1.4) + "</g>")
    # streak strip
    body += f'<line x1="28" x2="572" y1="226" y2="226" stroke="{RULE}"/>'
    flame = f'<circle class="pulse" cx="40" cy="256" r="5" fill="none" stroke="{ACCENT}" stroke-width="1.2"/><circle cx="40" cy="256" r="3.5" fill="{ACCENT}"/>'
    body += flame + t(56, 261, f"{current}-day current streak" if current else "No active streak — today's a good day to start", 15, FG, "di", ls=0)
    body += t(572, 261, f"longest streak · {longest} days", 11, MUTED, anchor="end", ls=.8)
    return svg(600, 290, body, f"GitHub stats for {u['login']}")


def languages(u):
    totals: dict[str, list] = {}
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            if n in EXCLUDE:
                continue
            totals.setdefault(n, [0, None])[0] += e["size"]
    top = sorted(totals.items(), key=lambda kv: -kv[1][0])[:6]
    top = [(n, (v[0], LANG_INK[i])) for i, (n, v) in enumerate(top)]
    total = sum(v[0] for _, v in top) or 1
    body = t(28, 40, "WRITTEN IN", 10.5, MUTED, ls=1.8) + t(572, 40, "BY CODE SIZE · PUBLIC REPOS", 10.5, ACCENT, anchor="end", weight=500, ls=1.2)
    # stacked bar
    x = 28
    for i, (name, (size, color)) in enumerate(top):
        w = 544 * size / total
        body += f'<rect class="grow" style="animation-delay:{i * .08:.2f}s" x="{x:.1f}" y="62" width="{max(w - 2, 1):.1f}" height="12" rx="3" fill="{color}"/>'
        x += w
    for i, (name, (size, color)) in enumerate(top):
        cx, cy = 28 + (i % 2) * 280, 112 + (i // 2) * 52
        pct = 100 * size / total
        body += (f'<g class="fade" style="animation-delay:{.3 + i * .1:.2f}s">'
                 f'<rect x="{cx + 1}" y="{cy - 10}" width="10" height="10" fill="{color}"/>'
                 + t(cx + 22, cy, name, 20, FG, "d", ls=0)
                 + t(cx + 250, cy, f"{pct:.1f}%", 12, MUTED, anchor="end", ls=.4)
                 + f'<rect x="{cx + 22}" y="{cy + 10}" width="228" height="3" rx="1.5" fill="{RULE}"/>'
                 + f'<rect class="grow" style="animation-delay:{.4 + i * .1:.2f}s" x="{cx + 22}" y="{cy + 10}" width="{228 * pct / 100:.1f}" height="3" rx="1.5" fill="{color}"/>'
                 + "</g>")
    return svg(600, 290, body, "Most used languages")


def activity(u):
    days = [d for w in u["contributionsCollection"]["contributionCalendar"]["weeks"] for d in w["contributionDays"]][-90:]
    W, H, L, R, T, B = 1200, 280, 60, 30, 80, 44
    vals = [d["contributionCount"] for d in days]
    vmax = max(max(vals), 4)
    n = len(vals)
    xs = [L + i * (W - L - R) / (n - 1) for i in range(n)]
    ys = [H - B - v / vmax * (H - T - B) for v in vals]
    # smooth path (Catmull-Rom → Bézier)
    d = f"M{xs[0]:.1f} {ys[0]:.1f}"
    for i in range(n - 1):
        p0 = (xs[max(i - 1, 0)], ys[max(i - 1, 0)]); p1 = (xs[i], ys[i])
        p2 = (xs[i + 1], ys[i + 1]); p3 = (xs[min(i + 2, n - 1)], ys[min(i + 2, n - 1)])
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f" C{c1[0]:.1f} {min(c1[1], H - B):.1f} {c2[0]:.1f} {min(c2[1], H - B):.1f} {p2[0]:.1f} {p2[1]:.1f}"
    area = d + f" L{xs[-1]:.1f} {H - B} L{xs[0]:.1f} {H - B}Z"
    body = (f'<defs><linearGradient id="ag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{FG}" stop-opacity=".14"/>'
            f'<stop offset="1" stop-color="{FG}" stop-opacity="0"/></linearGradient></defs>')
    body += t(28, 40, "ACTIVITY · LAST 90 DAYS", 10.5, MUTED, ls=1.8)
    body += t(W - 28, 40, f"{sum(vals)} CONTRIBUTIONS", 10.5, ACCENT, anchor="end", weight=500, ls=1.2)
    for k in range(5):
        gy = T + k * (H - T - B) / 4
        body += f'<line x1="{L}" x2="{W - R}" y1="{gy:.1f}" y2="{gy:.1f}" stroke="{RULE}" stroke-dasharray="2 5"/>'
        body += t(L - 12, gy + 4, round(vmax * (4 - k) / 4), 10, MUTED, anchor="end", ls=0)
    for i in range(0, n, 14):
        day = dt.date.fromisoformat(days[i]["date"])
        body += t(xs[i], H - 18, day.strftime("%d %b"), 10, MUTED, anchor="middle", ls=.4)
    body += f'<path class="fade" style="animation-delay:1.2s" d="{area}" fill="url(#ag)"/>'
    plen = int(sum(math.hypot(xs[k+1]-xs[k], ys[k+1]-ys[k]) for k in range(n-1)) * 1.15) + 50
    body += f'<path class="draw" style="--len:{plen}" d="{d}" stroke="{FG}" stroke-width="1.6" fill="none" stroke-linejoin="round"/>'
    i = max(range(n), key=lambda k: vals[k])
    body += (f'<g class="fade" style="animation-delay:2.2s"><circle class="pulse" cx="{xs[i]:.1f}" cy="{ys[i]:.1f}" r="5" fill="none" stroke="{ACCENT}" stroke-width="1.2"/>'
             f'<circle cx="{xs[i]:.1f}" cy="{ys[i]:.1f}" r="3.5" fill="{ACCENT}"/>'
             + t(xs[i], ys[i] - 14, f"peak · {vals[i]}", 13, ACCENT, "di", anchor="middle", ls=.4) + "</g>")
    return svg(W, H, body, "Contribution activity over the last 90 days")


def main():
    u = demo() if "--demo" in sys.argv else fetch()
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [("overview", overview), ("languages", languages), ("activity", activity)]:
        (OUT / f"{name}.svg").write_text(fn(u))
        print("wrote", OUT / f"{name}.svg")


if __name__ == "__main__":
    main()
