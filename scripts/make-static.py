"""Static pieces: section divider and toolkit card.
Run: python scripts/make-static.py  ->  assets/divider.svg, assets/toolkit.svg"""
from pathlib import Path

from theme import ACCENT, FG, MUTED, RULE, svg, text

A = Path(__file__).resolve().parent.parent / "assets"

# divider: hairline with a small vermilion mark that drifts across
div = (f'<line x1="0" x2="1200" y1="10" y2="10" stroke="{RULE}"/>'
       f'<rect class="drift" x="0" y="9" width="36" height="2" fill="{ACCENT}"/>')
(A / "divider.svg").write_text(svg(1200, 20, div, "", """
.drift{animation:drift 12s linear infinite}
@keyframes drift{from{transform:translateX(-40px)}to{transform:translateX(1240px)}}""", frame=False))

COLS = [
    ("LANGUAGES", ["Python", "C++", "C", "JavaScript", "SQL"]),
    ("MACHINE LEARNING", ["PyTorch", "Hugging Face", "scikit-learn", "OpenCV", "SegFormer", "EfficientNet"]),
    ("AGENTS & CLOUD", ["Gemini", "Vertex AI", "Arize Phoenix", "Cloud Run", "Firestore"]),
    ("SHIPPING", ["FastAPI", "Flask", "Docker", "Git & Linux", "MongoDB", "Three.js"]),
]
body = text(28, 40, "TOOLKIT", "m", 10.5, MUTED, ls=1.8)
body += text(1172, 40, "WHAT I REACH FOR", "mm", 10.5, ACCENT, "end", ls=1.4)
for i, (head, items) in enumerate(COLS):
    x = 28 + i * 290
    body += f'<line x1="{x}" x2="{x + 260}" y1="66" y2="66" stroke="{RULE}"/>'
    body += text(x, 88, head, "m", 9.5, MUTED, ls=1.6)
    for j, it in enumerate(items):
        body += (f'<g class="fade" style="animation-delay:{.05 * (i * 6 + j):.2f}s">'
                 + text(x, 122 + j * 28, it, "d", 22, FG) + "</g>")
(A / "toolkit.svg").write_text(svg(1200, 300, body, "Toolkit: Python, C++, PyTorch, Hugging Face, OpenCV, Gemini, Vertex AI, FastAPI, Docker and more"))
print("wrote divider + toolkit")

# record card: every hackathon result, wins first
REC = [("1st / 14,000+", "Google Cloud Rapid Agent Hackathon", True),
       ("Winner", "HackCrux · 36-hour national", True),
       ("1st", "Space IDEATHON", False),
       ("2nd", "Space Hackathon", False),
       ("4th", "Control+Space", False),
       ("R1", "Smart India Hackathon · qualified", False)]
body = text(28, 40, "RECORD", "m", 10.5, MUTED, ls=1.8) + text(572, 40, "HACKATHONS", "mm", 10.5, ACCENT, "end", ls=1.4)
for k, (place, event, win) in enumerate(REC):
    y = 82 + k * 34
    body += (f'<g class="fade" style="animation-delay:{.1 + k * .12:.2f}s">'
             + (f'<rect x="28" y="{y - 16}" width="3" height="22" fill="{ACCENT}"/>' if win else "")
             + text(42, y, place, "d", 22, ACCENT if win else FG)
             + text(572, y, event, "s", 13, FG if win else MUTED, "end")
             + f'<line x1="42" x2="572" y1="{y + 12}" y2="{y + 12}" stroke="{RULE}" stroke-opacity=".6"/>' + "</g>")
(A / "record.svg").write_text(svg(600, 290, body, "Hackathon record: 1st of 14,000+ Google Cloud Rapid Agent Hackathon; winner HackCrux; 1st Space IDEATHON; 2nd Space Hackathon; 4th Control+Space; SIH round 1."))
print("wrote record")
