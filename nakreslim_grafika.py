#!/usr/bin/env python3
"""Grafika pro FB příspěvky Nakreslím CZ (1080x1080, styl „blueprint“).

Použití:
  python3 nakreslim_grafika.py --motiv pudorys --nadpis "Nemáte výkresy domu?" \
      --podnadpis "Zaměříme a nakreslíme současný stav" \
      --body "Pasport stavby" "Zaměření nemovitosti" "Podklady pro dotace" \
      --out post.png
Motivy: pudorys | dum | dotace | navrh
"""
import argparse, html, subprocess, tempfile, os

W = H = 1080
BG = "#0f2a4a"      # tmavá modrá (blueprint)
GRID = "#1d3f66"
LINE = "#e8f1fb"
ACC = "#f5b942"     # žlutá – zvýraznění

def grid():
    g = []
    for i in range(0, W + 1, 27):
        w = 1.2 if i % 135 == 0 else 0.5
        g.append(f'<line x1="{i}" y1="0" x2="{i}" y2="{H}" stroke="{GRID}" stroke-width="{w}"/>')
        g.append(f'<line x1="0" y1="{i}" x2="{W}" y2="{i}" stroke="{GRID}" stroke-width="{w}"/>')
    return "\n".join(g)

def dim(x1, y1, x2, y2, label, vertical=False):
    s = f'<g stroke="{ACC}" stroke-width="2" fill="none">'
    s += f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'
    if vertical:
        s += f'<line x1="{x1-8}" y1="{y1}" x2="{x1+8}" y2="{y1}"/><line x1="{x2-8}" y1="{y2}" x2="{x2+8}" y2="{y2}"/></g>'
        s += f'<text x="{x1-14}" y="{(y1+y2)/2}" fill="{ACC}" font-size="20" font-family="DejaVu Sans Mono" text-anchor="middle" transform="rotate(-90 {x1-14} {(y1+y2)/2})">{label}</text>'
    else:
        s += f'<line x1="{x1}" y1="{y1-8}" x2="{x1}" y2="{y1+8}"/><line x1="{x2}" y1="{y2-8}" x2="{x2}" y2="{y2+8}"/></g>'
        s += f'<text x="{(x1+x2)/2}" y="{y1-12}" fill="{ACC}" font-size="20" font-family="DejaVu Sans Mono" text-anchor="middle">{label}</text>'
    return s

def motiv_pudorys(ox, oy):
    st = f'stroke="{LINE}" fill="none" stroke-linecap="square"'
    return f'''<g transform="translate({ox},{oy})">
<rect x="0" y="0" width="420" height="300" {st} stroke-width="9"/>
<line x1="200" y1="0" x2="200" y2="170" {st} stroke-width="5"/>
<line x1="0" y1="170" x2="140" y2="170" {st} stroke-width="5"/>
<line x1="200" y1="170" x2="420" y2="170" {st} stroke-width="5"/>
<line x1="300" y1="170" x2="300" y2="300" {st} stroke-width="5"/>
<line x1="200" y1="230" x2="200" y2="300" {st} stroke-width="5"/>
<path d="M140 170 A60 60 0 0 1 200 110" {st} stroke-width="2" stroke-dasharray="6 5"/>
<line x1="60" y1="-4" x2="140" y2="-4" stroke="{BG}" stroke-width="10"/><line x1="60" y1="0" x2="140" y2="0" {st} stroke-width="2"/>
<line x1="260" y1="-4" x2="360" y2="-4" stroke="{BG}" stroke-width="10"/><line x1="260" y1="0" x2="360" y2="0" {st} stroke-width="2"/>
<line x1="420" y1="210" x2="420" y2="270" stroke="{BG}" stroke-width="10"/><line x1="420" y1="210" x2="420" y2="270" {st} stroke-width="2"/>
<g fill="{LINE}" font-family="Inter" font-size="19" opacity="0.85">
<text x="100" y="95" text-anchor="middle">obývací pokoj</text><text x="100" y="118" text-anchor="middle" font-size="16">24,6 m²</text>
<text x="310" y="95" text-anchor="middle">ložnice</text><text x="310" y="118" text-anchor="middle" font-size="16">15,2 m²</text>
<text x="100" y="245" text-anchor="middle">kuchyň</text><text x="250" y="245" text-anchor="middle">koupelna</text><text x="360" y="245" text-anchor="middle">pokoj</text>
</g>
{dim(0,-40,420,-40,"12 450")}
{dim(-40,0,-40,300,"8 900",vertical=True)}
</g>'''

def motiv_dum(ox, oy):
    st = f'stroke="{LINE}" fill="none" stroke-linejoin="round"'
    return f'''<g transform="translate({ox},{oy})">
<path d="M0 140 L210 0 L420 140" {st} stroke-width="8"/>
<rect x="30" y="140" width="360" height="190" {st} stroke-width="8"/>
<rect x="70" y="190" width="80" height="70" {st} stroke-width="4"/><line x1="110" y1="190" x2="110" y2="260" {st} stroke-width="2"/>
<rect x="270" y="190" width="80" height="70" {st} stroke-width="4"/><line x1="310" y1="190" x2="310" y2="260" {st} stroke-width="2"/>
<rect x="180" y="220" width="60" height="110" {st} stroke-width="4"/>
<rect x="180" y="70" width="60" height="45" {st} stroke-width="3"/>
<line x1="-30" y1="330" x2="450" y2="330" stroke="{LINE}" stroke-width="3"/>
<g stroke="{LINE}" stroke-width="1.5">{"".join(f'<line x1="{x}" y1="330" x2="{x-14}" y2="346"/>' for x in range(-20, 450, 22))}</g>
{dim(30,375,390,375,"10 800")}
{dim(460,0,460,330,"7 600",vertical=True).replace(f'x="{446}"', f'x="{486}"')}
</g>'''

def motiv_dotace(ox, oy):
    st = f'stroke="{LINE}" fill="none" stroke-linejoin="round"'
    return f'''<g transform="translate({ox},{oy})">
<path d="M0 130 L170 0 L340 130" {st} stroke-width="8"/>
<rect x="25" y="130" width="290" height="190" {st} stroke-width="8"/>
<rect x="5" y="118" width="330" height="214" stroke="{ACC}" fill="none" stroke-width="3" stroke-dasharray="14 8" rx="4"/>
<rect x="125" y="210" width="90" height="110" {st} stroke-width="4"/>
<g transform="translate(400,170)">
<circle cx="0" cy="0" r="78" stroke="{ACC}" fill="none" stroke-width="7"/>
<text x="0" y="22" fill="{ACC}" font-family="Inter" font-weight="bold" font-size="64" text-anchor="middle">Kč</text>
</g>
<path d="M330 290 Q 380 330 410 255" stroke="{ACC}" fill="none" stroke-width="4" marker-end="url(#arr)"/>
<text x="170" y="370" fill="{ACC}" font-family="DejaVu Sans Mono" font-size="20" text-anchor="middle">zateplení · okna · zdroj tepla</text>
</g>'''

def motiv_navrh(ox, oy):
    st = f'stroke="{LINE}" fill="none" stroke-linejoin="round"'
    return f'''<g transform="translate({ox},{oy})">
<path d="M0 150 L180 30 L360 150" {st} stroke-width="8"/>
<rect x="25" y="150" width="310" height="180" {st} stroke-width="8"/>
<path d="M335 330 L335 210 L470 210 L470 330" stroke="{ACC}" fill="none" stroke-width="6" stroke-dasharray="16 9"/>
<path d="M335 210 L470 170" stroke="{ACC}" fill="none" stroke-width="6" stroke-dasharray="16 9"/>
<rect x="70" y="200" width="70" height="60" {st} stroke-width="4"/><rect x="220" y="200" width="70" height="60" {st} stroke-width="4"/>
<line x1="-20" y1="330" x2="500" y2="330" stroke="{LINE}" stroke-width="3"/>
<text x="402" y="290" fill="{ACC}" font-family="Inter" font-size="22" text-anchor="middle">přístavba</text>
</g>'''

MOTIVY = {"pudorys": motiv_pudorys, "dum": motiv_dum, "dotace": motiv_dotace, "navrh": motiv_navrh}

def wrap(text, max_chars):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 > max_chars and cur:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur: lines.append(cur)
    return lines

def build(motiv, nadpis, podnadpis, body, telefon):
    e = html.escape
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<defs><marker id="arr" markerWidth="10" markerHeight="10" refX="5" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="{ACC}"/></marker></defs>',
           f'<rect width="{W}" height="{H}" fill="{BG}"/>', grid()]
    # rám výkresu
    out.append(f'<rect x="40" y="40" width="{W-80}" height="{H-80}" fill="none" stroke="{LINE}" stroke-width="3"/>')
    # nadpis
    y = 135
    lines = wrap(nadpis, 22)
    fs = 72 if len(lines) <= 2 else 60
    for ln in lines:
        out.append(f'<text x="90" y="{y}" fill="#ffffff" font-family="Inter Display" font-weight="bold" font-size="{fs}">{e(ln)}</text>')
        y += fs + 8
    if podnadpis:
        y += 4
        for ln in wrap(podnadpis, 40):
            out.append(f'<text x="90" y="{y}" fill="{ACC}" font-family="Inter" font-weight="600" font-size="36">{e(ln)}</text>')
            y += 46
    # motiv
    out.append(MOTIVY[motiv](300 if motiv != "dotace" else 260, max(y + 70, 420)))
    # odrážky vlevo dole
    by = 830 - 0
    if body:
        by = H - 150 - 48 * (len(body) - 1)
        for b in body:
            out.append(f'<text x="90" y="{by}" fill="{LINE}" font-family="Inter" font-size="32"><tspan fill="{ACC}">✓</tspan> {e(b)}</text>')
            by += 48
    # razítko (rohové pole výkresu)
    sx, sy, sw, sh = W - 40 - 360, H - 40 - 130, 360, 130
    out.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="{BG}" stroke="{LINE}" stroke-width="3"/>')
    out.append(f'<line x1="{sx}" y1="{sy+70}" x2="{sx+sw}" y2="{sy+70}" stroke="{LINE}" stroke-width="2"/>')
    out.append(f'<text x="{sx+20}" y="{sy+50}" fill="#ffffff" font-family="Inter Display" font-weight="bold" font-size="38">Nakreslím CZ</text>')
    out.append(f'<text x="{sx+20}" y="{sy+108}" fill="{ACC}" font-family="DejaVu Sans Mono" font-weight="bold" font-size="30">☎ {e(telefon)}</text>')
    out.append('</svg>')
    return "\n".join(out)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--motiv", choices=MOTIVY, default="pudorys")
    p.add_argument("--nadpis", required=True)
    p.add_argument("--podnadpis", default="")
    p.add_argument("--body", nargs="*", default=[])
    p.add_argument("--telefon", default="725 368 006")
    p.add_argument("--out", required=True)
    a = p.parse_args()
    svg = build(a.motiv, a.nadpis, a.podnadpis, a.body, a.telefon)
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False, encoding="utf-8") as f:
        f.write(svg); tmp = f.name
    subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-o", a.out, tmp], check=True)
    os.unlink(tmp)
    print(a.out)
