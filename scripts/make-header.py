import random
random.seed(7)
W,H=1200,320
stars=[]
for i in range(140):
    x,y=random.uniform(0,W),random.uniform(0,H)
    r=random.choice([0.6,0.8,1,1.2,1.6])
    d=random.uniform(1.5,5); delay=random.uniform(0,5)
    stars.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#fff" class="tw" style="animation-duration:{d:.1f}s;animation-delay:-{delay:.1f}s"/>')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
 <linearGradient id="sky" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#05060f"/><stop offset=".55" stop-color="#0b1330"/><stop offset="1" stop-color="#1a0f3a"/>
 </linearGradient>
 <radialGradient id="neb1" cx=".78" cy=".35" r=".45"><stop offset="0" stop-color="#7c3aed" stop-opacity=".45"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>
 <radialGradient id="neb2" cx=".15" cy=".85" r=".4"><stop offset="0" stop-color="#0ea5e9" stop-opacity=".35"/><stop offset="1" stop-color="#0ea5e9" stop-opacity="0"/></radialGradient>
 <radialGradient id="planet" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#93c5fd"/><stop offset=".5" stop-color="#4f46e5"/><stop offset="1" stop-color="#1e1b4b"/></radialGradient>
 <linearGradient id="txt" x1="0" x2="1"><stop offset="0" stop-color="#e0f2fe"/><stop offset=".5" stop-color="#a5b4fc"/><stop offset="1" stop-color="#c4b5fd"/></linearGradient>
 <clipPath id="clip"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<style>
 .tw{{animation-name:tw;animation-iteration-count:infinite;animation-timing-function:ease-in-out}}
 @keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:1}}}}
 .orbit{{transform-origin:960px 150px;animation:spin 14s linear infinite}}
 @keyframes spin{{to{{transform:rotate(360deg)}}}}
 .shoot{{animation:shoot 7s ease-in infinite}}
 @keyframes shoot{{0%{{transform:translate(0,0);opacity:0}}3%{{opacity:1}}12%{{transform:translate(-420px,210px);opacity:0}}100%{{opacity:0;transform:translate(-420px,210px)}}}}
 .fade{{animation:fade 1.6s ease-out both}}
 .fade2{{animation:fade 1.6s .5s ease-out both}}
 .fade3{{animation:fade 1.6s 1s ease-out both}}
 @keyframes fade{{from{{opacity:0;transform:translateY(12px)}}to{{opacity:1;transform:none}}}}
 text{{font-family:'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif}}
</style>
<g clip-path="url(#clip)">
 <rect width="{W}" height="{H}" fill="url(#sky)"/>
 <rect width="{W}" height="{H}" fill="url(#neb1)"/>
 <rect width="{W}" height="{H}" fill="url(#neb2)"/>
 {''.join(stars)}
 <g class="shoot"><line x1="1150" y1="20" x2="1230" y2="-20" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".9"/></g>
 <!-- planet + orbit -->
 <ellipse cx="960" cy="150" rx="118" ry="118" fill="none" stroke="#a5b4fc" stroke-opacity=".18" stroke-dasharray="3 7"/>
 <circle cx="960" cy="150" r="58" fill="url(#planet)"/>
 <ellipse cx="960" cy="150" rx="96" ry="20" fill="none" stroke="#c4b5fd" stroke-opacity=".7" stroke-width="3" transform="rotate(-18 960 150)"/>
 <path d="M 868 165 A 96 20 -18 0 0 1052 135" fill="none" stroke="url(#planet)" stroke-width="0"/>
 <g class="orbit"><circle cx="1078" cy="150" r="7" fill="#fcd34d"/><circle cx="1078" cy="150" r="14" fill="#fcd34d" opacity=".2"/></g>
 <!-- text -->
 <g class="fade"><text x="70" y="128" font-size="64" font-weight="800" fill="url(#txt)" letter-spacing="1">Kshitij Verma</text></g>
 <g class="fade2"><text x="72" y="172" font-size="22" fill="#cbd5e1" letter-spacing=".5">ML Engineer  ·  Computer Vision  ·  AI Agents  ·  LNMIIT Jaipur</text></g>
 <g class="fade3">
  <rect x="72" y="204" width="510" height="44" rx="22" fill="#fcd34d" fill-opacity=".12" stroke="#fcd34d" stroke-opacity=".7"/>
  <text x="96" y="233" font-size="18" font-weight="700" fill="#fde68a">🥇 1st / 14,000+ · Google Cloud Rapid Agent Hackathon</text>
 </g>
</g>
</svg>'''
open(__import__("pathlib").Path(__file__).resolve().parent.parent / "assets" / "header.svg","w").write(svg)
