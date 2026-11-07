"""Shared look for every SVG on the profile: ink-on-paper palette + embedded fonts.

Fonts (Instrument Serif, IBM Plex Mono/Sans; SIL OFL) are subset to the glyphs each
SVG actually uses and inlined as base64 @font-face, so GitHub renders them exactly.
Text elements pick a face with class="d" (serif), "di" (serif italic), "m" (mono),
"mm" (mono medium) or "s" (sans).
"""
from __future__ import annotations

import base64
import html
import io
import re
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

FONTS = Path(__file__).resolve().parent / "fonts"

# palette (matches GitHub dark) ------------------------------------------
PANEL = "#161b22"   # GitHub raised surface
BG = "#0d1117"      # GitHub dark canvas
RULE = "#30363d"    # GitHub border
FAINT = "#484f58"   # inactive marks
MUTED = "#8b949e"   # secondary text
FG = "#e6edf3"      # GitHub foreground
ACCENT = "#ff5b35"  # vermilion — the one loud colour
OCHRE = "#d8a34a"
SAGE = "#9db38f"

FACES = {
    "d":  ("KVSerif", "serif.woff2", "normal", 400),
    "di": ("KVSerif", "serif-italic.woff2", "italic", 400),
    "m":  ("KVMono", "mono.woff2", "normal", 400),
    "mm": ("KVMono", "mono-medium.woff2", "normal", 500),
    "s":  ("KVSans", "sans.woff2", "normal", 400),
}
FALLBACK = {"KVSerif": "Georgia,'Times New Roman',serif",
            "KVMono": "'SFMono-Regular',Consolas,Menlo,monospace",
            "KVSans": "'Segoe UI',Helvetica,Arial,sans-serif"}


def text(x, y, s, cls="m", size=11, fill=MUTED, anchor="start", ls=0, extra=""):
    """A <text> element in one of the theme faces."""
    m = __import__("re").search(r'class="([^"]*)"', extra)
    if m:
        cls = f"{cls} {m.group(1)}"
        extra = extra.replace(m.group(0), "")
    return (f'<text class="{cls}" x="{x}" y="{y}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}" letter-spacing="{ls}" {extra}>{html.escape(str(s), quote=False)}</text>')


def _subset_b64(file: str, chars: str) -> str:
    font = TTFont(FONTS / file)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga"]
    opts.name_IDs = []
    opts.notdef_outline = True
    sub = subset.Subsetter(opts)
    sub.populate(text=chars + " ")
    sub.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def font_css(svg_body: str) -> str:
    used: dict[str, set] = {}
    for cls, content in re.findall(r'<text class="(\w+)[^"]*"[^>]*>(.*?)</text>', svg_body, re.S):
        used.setdefault(cls, set()).update(html.unescape(re.sub(r"<[^>]+>", "", content)))
    css = []
    for cls, chars in used.items():
        fam, file, style, weight = FACES[cls]
        b64 = _subset_b64(file, "".join(sorted(chars)))
        css.append(f"@font-face{{font-family:'{fam}-{cls}';src:url(data:font/woff2;base64,{b64}) format('woff2');"
                   f"font-style:{style};font-weight:{weight}}}")
        css.append(f".{cls}{{font-family:'{fam}-{cls}',{FALLBACK[fam]};font-style:{style};font-weight:{weight}}}")
    return "".join(css)


MOTION_CSS = """
.fade{opacity:0;animation:fade .8s ease-out forwards}
@keyframes fade{to{opacity:1}}
.flow{stroke-dasharray:3 6;animation:flow 1.4s linear infinite}
@keyframes flow{to{stroke-dashoffset:-18}}
.ping{transform-box:fill-box;transform-origin:center;animation:ping 2.4s ease-out infinite}
@keyframes ping{0%{transform:scale(.6);opacity:.8}100%{transform:scale(2.8);opacity:0}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;opacity:1!important;stroke-dashoffset:0!important;transform:none!important}}
"""


def svg(w, h, body, label, css="", frame=True):
    border = (f'<rect width="{w}" height="{h}" rx="6" fill="{BG}"/>'
              f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="6" fill="none" stroke="{RULE}"/>') if frame else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{html.escape(label)}"><style>{font_css(body)}{MOTION_CSS}{css}</style>'
            f'{border}{body}</svg>')
