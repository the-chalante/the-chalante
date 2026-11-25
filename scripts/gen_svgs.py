import random, sys, os

random.seed(7)
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

OR, RED, AMB, BG, DIM = "#ff6a00", "#ff2a1a", "#ffb000", "#0a0605", "#a8501c"
FONT = "'JetBrains Mono','Fira Code',Consolas,'DejaVu Sans Mono','Courier New',monospace"
CW = 0.6  # monospace char width ratio


def typed(x, y, parts, size, begin, dur, uid, weight="normal"):
    """Typewriter text. parts = [(text, fill), ...]"""
    raw = "".join(t for t, _ in parts)
    n = len(raw)
    w = n * size * CW
    vals = ";".join(f"{w * i / n:.1f}" for i in range(n + 1))
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    spans = "".join(f'<tspan fill="{f}">{esc(t)}</tspan>' for t, f in parts)
    return (
        f'<clipPath id="{uid}"><rect x="{x}" y="{y - size}" width="0" height="{size * 1.5}">'
        f'<animate attributeName="width" values="{vals}" begin="{begin}s" dur="{dur}s" calcMode="discrete" fill="freeze"/>'
        f"</rect></clipPath>"
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" textLength="{w:.1f}" '
        f'lengthAdjust="spacingAndGlyphs" clip-path="url(#{uid})">{spans}</text>'
    ), w, vals


# ---------------------------------------------------------------- banner
W, H = 1200, 420
X = 40
s = []
s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{FONT}">')
s.append(f"""<style>
.blink{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.in{{opacity:0;animation:in .35s steps(3) forwards}}
@keyframes in{{0%{{opacity:0}}40%{{opacity:1}}60%{{opacity:.2}}100%{{opacity:1}}}}
.flick{{animation:flick 7s infinite}}
@keyframes flick{{0%,95%,100%{{opacity:1}}96%{{opacity:.78}}97%{{opacity:1}}98.5%{{opacity:.88}}}}
.gr{{animation:gr 4s infinite}} .gy{{animation:gy 4s infinite}}
@keyframes gr{{0%,86%,100%{{transform:translate(0,0)}}87%{{transform:translate(-6px,2px)}}89%{{transform:translate(5px,-2px)}}91%{{transform:translate(-3px,0)}}93%{{transform:translate(4px,1px)}}}}
@keyframes gy{{0%,86%,100%{{transform:translate(0,0)}}87%{{transform:translate(5px,-1px)}}89%{{transform:translate(-6px,2px)}}91%{{transform:translate(3px,-1px)}}93%{{transform:translate(-4px,0)}}}}
.main{{animation:jolt 4s infinite}}
@keyframes jolt{{0%,87%,100%{{transform:translate(0,0)}}88%{{transform:translate(2px,0) skewX(-6deg)}}90%{{transform:translate(-2px,0)}}}}
.sweep{{animation:sweep 6s linear infinite}}
@keyframes sweep{{from{{transform:translateY(-80px)}}to{{transform:translateY({H}px)}}}}
.ag{{animation:ag 2s infinite}}
@keyframes ag{{0%,100%{{opacity:.15}}50%{{opacity:1}}}}
.bar{{animation:bar 2.4s steps(1) infinite}}
@keyframes bar{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
</style>""")
s.append(f"""<defs>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="#000" opacity=".55"/></pattern>
<linearGradient id="sw" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{OR}" stop-opacity="0"/><stop offset=".5" stop-color="{OR}" stop-opacity=".09"/><stop offset="1" stop-color="{OR}" stop-opacity="0"/></linearGradient>
<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient>
<filter id="glow" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft" x="-5%" y="-50%" width="110%" height="200%"><feGaussianBlur stdDeviation="1.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="frame"><rect x="2" y="2" width="{W-4}" height="{H-4}" rx="10"/></clipPath>
</defs>""")
s.append(f'<rect width="{W}" height="{H}" rx="12" fill="{BG}"/>')
s.append('<g clip-path="url(#frame)"><g class="flick">')

# title bar
s.append(f'<rect width="{W}" height="36" fill="#1a0c04"/><rect y="36" width="{W}" height="1.5" fill="{OR}" opacity=".6"/>')
for i, c in enumerate([RED, OR, AMB]):
    s.append(f'<rect x="{16 + i * 20}" y="12" width="12" height="12" fill="{c}"/>')
s.append(f'<text x="90" y="23.5" font-size="14" fill="{OR}" opacity=".75">root@the-chalante: ~/swarm — tty1 — PID 1</text>')
s.append(f'<g class="blink"><rect x="{W - 112}" y="13" width="10" height="10" fill="{RED}"/><text x="{W - 96}" y="23.5" font-size="14" font-weight="bold" fill="{RED}">LIVE</text></g>')
s.append(f'<text x="{W - 60}" y="23.5" font-size="14" fill="{DIM}">[×]</text>')

# command line
prompt = "root@the-chalante:~$ "
t, pw, _ = typed(X, 78, [(prompt, AMB), ("./primarch --summon --swarm=all", OR)], 18, 0.4, 1.6, "c1")
s.append(t)

# boot log
logs = [
    [("[  OK  ] ", OR), ("operator authenticated ..... the-chalante", AMB)],
    [("[  OK  ] ", OR), ("spawning agents ............. 1024/1024", DIM)],
    [("[ WARN ] ", RED), ("chain of command: 1 human -> 1024 agents", DIM)],
]
for i, parts in enumerate(logs):
    t, _, _ = typed(X, 116 + i * 26, parts, 15, 2.2 + i * 0.45, 0.4, f"l{i}")
    s.append(t)

# swarm grid
gx, gy, cols, rows, cell = 880, 74, 14, 6, 20
s.append(f'<g class="in" style="animation-delay:2.6s">')
s.append(f'<text x="{gx}" y="{gy - 12}" font-size="12" fill="{DIM}" letter-spacing="2">SWARM MAP // 84 NODES SHOWN</text>')
s.append(f'<rect x="{gx - 6}" y="{gy - 6}" width="{cols * cell + 4}" height="{rows * cell + 4}" fill="none" stroke="{OR}" stroke-opacity=".35"/>')
for r in range(rows):
    for c in range(cols):
        col = RED if random.random() < 0.12 else (AMB if random.random() < 0.15 else OR)
        d = random.uniform(0, 3)
        dur = random.uniform(1.1, 3.2)
        s.append(f'<rect class="ag" style="animation-delay:{d:.2f}s;animation-duration:{dur:.2f}s" x="{gx + c * cell}" y="{gy + r * cell}" width="12" height="12" fill="{col}"/>')
s.append("</g>")

# title with glitch
title = "PRIMARCH OF THE AGENT SWARMS"
ts, ty = 60, 262
tw = len(title) * ts * CW
attrs = f'x="{X}" y="{ty}" font-size="{ts}" font-weight="800" textLength="{tw:.0f}" lengthAdjust="spacingAndGlyphs"'
s.append(f'<g class="in" style="animation-delay:3.5s">')
s.append(f'<g class="gr"><text {attrs} fill="{RED}" opacity=".85">{title}</text></g>')
s.append(f'<g class="gy"><text {attrs} fill="{AMB}" opacity=".6">{title}</text></g>')
s.append(f'<g class="main"><text {attrs} fill="{OR}" filter="url(#glow)">{title}</text></g>')
s.append("</g>")
s.append(f'<rect x="{X}" y="{ty + 16}" width="0" height="4" fill="{OR}"><animate attributeName="width" from="0" to="{tw:.0f}" begin="3.7s" dur=".6s" fill="freeze"/></rect>')
s.append(f'<rect x="{X}" y="{ty + 16}" width="0" height="4" fill="{RED}" opacity=".9"><animate attributeName="width" from="0" to="120" begin="3.7s" dur=".3s" fill="freeze"/></rect>')

# subtitle
sub = [("> ", RED), ("AI RESEARCHER ", OR), ("// ", RED), ("AI-POWERED DEV", OR)]
t, sw, _ = typed(X, 326, sub, 26, 4.3, 1.0, "s1", "bold")
s.append(f'<g filter="url(#soft)">{t}</g>')
s.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="5.3s" fill="freeze"/><rect class="blink" x="{X + sw + 8:.0f}" y="304" width="15" height="26" fill="{OR}"/></g>')

# operator ID tag
s.append(f'<g class="in" style="animation-delay:5.5s">')
s.append(f'<rect x="{W - 330}" y="300" width="290" height="36" fill="#1a0c04" stroke="{RED}" stroke-width="2"/>')
s.append(f'<rect x="{W - 330}" y="300" width="8" height="36" fill="{RED}"/>')
s.append(f'<text x="{W - 310}" y="324" font-size="14" fill="{DIM}" letter-spacing="1">ID:</text>')
s.append(f'<text x="{W - 276}" y="325" font-size="20" font-weight="800" fill="{AMB}" textLength="{12 * 20 * CW:.0f}" lengthAdjust="spacingAndGlyphs" filter="url(#soft)">THE-CHALANTE</text>')
s.append("</g>")

# status bar
s.append(f'<rect y="{H - 54}" width="{W}" height="54" fill="#140803"/><rect y="{H - 54}" width="{W}" height="1.5" fill="{OR}" opacity=".5"/>')
status = "SWARM: ONLINE  |  AGENTS: 1024  |  MODE: AGGRESSIVE  |  OVERSIGHT: HUMAN"
s.append(f'<text class="in" style="animation-delay:5s" x="{X}" y="{H - 21}" font-size="14" fill="{OR}" letter-spacing="1">{status}</text>')
bx = W - 250
s.append(f'<g class="in" style="animation-delay:5.2s"><text x="{bx}" y="{H - 21}" font-size="14" fill="{RED}" font-weight="bold">THREAT</text>')
for i in range(10):
    fill = RED if i >= 7 else OR
    cls = ' class="bar"' if i >= 7 else ""
    s.append(f'<rect{cls} x="{bx + 70 + i * 14}" y="{H - 34}" width="10" height="16" fill="{fill}" style="animation-delay:{i * 0.15:.2f}s"/>')
s.append("</g>")

s.append("</g>")  # flick
# CRT overlays
s.append(f'<rect class="sweep" width="{W}" height="80" fill="url(#sw)"/>')
s.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
s.append(f'<rect width="{W}" height="{H}" fill="url(#vig)"/>')
s.append("</g>")
s.append(f'<rect x="1.5" y="1.5" width="{W - 3}" height="{H - 3}" rx="11" fill="none" stroke="{OR}" stroke-width="3"/>')
s.append("</svg>")
open(os.path.join(OUT, "banner.svg"), "w").write("\n".join(s))

# ---------------------------------------------------------------- button
GRN = "#39ff7a"
SKILLS = ["PYTORCH", "SPARK", "AIRFLOW", "OPENCV", "SCIKIT-LEARN", "PYTHON", "C++"]
BW, BH = 720, 200
b = []
b.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BW} {BH}" width="{BW}" height="{BH}" font-family="{FONT}">')
tick = "".join(f"{k}  //  " for k in SKILLS)
tsz = 18
tlen = len(tick) * tsz * CW
b.append(f"""<style>
.pulse{{animation:pulse 1.6s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:.25}}50%{{opacity:1}}}}
.shine{{animation:shine 3.2s ease-in-out infinite}}
@keyframes shine{{0%{{transform:translateX(-200px)}}60%,100%{{transform:translateX({BW + 100}px)}}}}
.chev{{animation:chev 1.2s steps(3) infinite}}
@keyframes chev{{0%{{opacity:.2}}33%{{opacity:.6}}66%,100%{{opacity:1}}}}
.tick{{animation:tick {len(SKILLS) * 2.2:.1f}s linear infinite}}
@keyframes tick{{from{{transform:translateX(-{tlen:.1f}px)}}to{{transform:translateX(0)}}}}
.blink{{animation:blink 1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
</style>
<defs>
<filter id="g" x="-20%" y="-60%" width="140%" height="220%"><feGaussianBlur stdDeviation="7"/></filter>
<filter id="t" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="tg" x="-5%" y="-50%" width="110%" height="200%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="{OR}" stop-opacity="0"/><stop offset=".5" stop-color="{AMB}" stop-opacity=".22"/><stop offset="1" stop-color="{OR}" stop-opacity="0"/></linearGradient>
<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{BG}"/><stop offset=".08" stop-color="{BG}" stop-opacity="0"/><stop offset=".92" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}"/></linearGradient>
<clipPath id="in"><rect x="20" y="20" width="{BW - 40}" height="{BH - 40}"/></clipPath>
<clipPath id="band"><rect x="22" y="128" width="{BW - 44}" height="48"/></clipPath>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="#000" opacity=".5"/></pattern>
</defs>""")
b.append(f'<rect class="pulse" x="20" y="20" width="{BW - 40}" height="{BH - 40}" fill="none" stroke="{OR}" stroke-width="8" filter="url(#g)"/>')
b.append(f'<rect x="20" y="20" width="{BW - 40}" height="{BH - 40}" fill="{BG}" stroke="{OR}" stroke-width="3"/>')
b.append(f'<g clip-path="url(#in)"><rect class="shine" x="0" y="0" width="160" height="{BH}" fill="url(#sh)" transform="skewX(-20)"/></g>')
L = 26
for cx, cy, dx, dy in [(12, 12, 1, 1), (BW - 12, 12, -1, 1), (12, BH - 12, 1, -1), (BW - 12, BH - 12, -1, -1)]:
    b.append(f'<path d="M{cx} {cy + dy * L}V{cy}H{cx + dx * L}" fill="none" stroke="{RED}" stroke-width="4"/>')
label = "ENTER THE SWARM"
ls = 46
lw = len(label) * ls * CW
b.append(f'<text x="{BW / 2}" y="92" font-size="{ls}" font-weight="800" fill="{OR}" text-anchor="middle" textLength="{lw:.0f}" lengthAdjust="spacingAndGlyphs" filter="url(#t)">{label}</text>')
for i in range(3):
    b.append(f'<text class="chev" style="animation-delay:{i * 0.2:.1f}s" x="{BW / 2 - lw / 2 - 70 + i * 18}" y="90" font-size="34" font-weight="bold" fill="{RED}">&gt;</text>')
    b.append(f'<text class="chev" style="animation-delay:{(2 - i) * 0.2:.1f}s" x="{BW / 2 + lw / 2 + 22 + i * 18}" y="90" font-size="34" font-weight="bold" fill="{RED}">&lt;</text>')
# skills ticker band
b.append(f'<rect x="22" y="126" width="{BW - 44}" height="1.5" fill="{GRN}" opacity=".5"/>')
b.append(f'<rect x="22" y="128" width="{BW - 44}" height="50" fill="#03140a"/>')
b.append(f'<g clip-path="url(#band)"><g class="tick">')
for k in range(3):
    b.append(f'<text x="{k * tlen:.1f}" y="168" font-size="{tsz}" font-weight="bold" fill="{GRN}" letter-spacing="0" textLength="{tlen:.1f}" lengthAdjust="spacingAndGlyphs" filter="url(#tg)">{tick.replace("&", "&amp;")}</text>')
b.append(f'</g><rect x="22" y="128" width="{BW - 44}" height="50" fill="url(#fade)"/></g>')
b.append(f'<text x="30" y="143" font-size="11" fill="{GRN}" opacity=".8" letter-spacing="2" class="blink">● ARSENAL</text>')
b.append(f'<g clip-path="url(#in)"><rect width="{BW}" height="{BH}" fill="url(#scan)"/></g>')
b.append("</svg>")
open(os.path.join(OUT, "enter-button.svg"), "w").write("\n".join(b))
print("ok")
