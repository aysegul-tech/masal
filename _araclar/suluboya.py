"""Masal için suluboya görünümlü SVG sahneleri üretir.

Kullanım: python3 suluboya.py <çıktı klasörü>
"""
import math
import random
import sys
from pathlib import Path

W, H = 1200, 800


def defs(seed):
    """Suluboya filtreleri, kâğıt dokusu ve kenar maskesi."""
    return f"""
<defs>
  <filter id="wc1" x="-20%" y="-20%" width="140%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="4" seed="{seed}" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="26" xChannelSelector="R" yChannelSelector="G" result="d"/>
    <feGaussianBlur in="d" stdDeviation="1.6" result="b"/>
    <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="2" seed="{seed+7}" result="gr"/>
    <feColorMatrix in="gr" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -0.7 1.25" result="ga"/>
    <feComposite in="b" in2="ga" operator="in"/>
  </filter>
  <filter id="wc2" x="-20%" y="-20%" width="140%" height="140%">
    <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="3" seed="{seed+3}" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="16" xChannelSelector="G" yChannelSelector="R" result="d"/>
    <feGaussianBlur in="d" stdDeviation="1" result="b"/>
    <feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="2" seed="{seed+11}" result="gr"/>
    <feColorMatrix in="gr" type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 -0.6 1.2" result="ga"/>
    <feComposite in="b" in2="ga" operator="in"/>
  </filter>
  <filter id="wash" x="-50%" y="-50%" width="200%" height="200%">
    <feTurbulence type="fractalNoise" baseFrequency="0.008" numOctaves="3" seed="{seed+5}" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="60" xChannelSelector="R" yChannelSelector="G" result="d"/>
    <feGaussianBlur in="d" stdDeviation="22"/>
  </filter>
  <filter id="glow" x="-100%" y="-100%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="18"/>
  </filter>
  <filter id="paper" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="5" seed="{seed+13}" result="t"/>
    <feDiffuseLighting in="t" lighting-color="#fffaf0" surfaceScale="1.4" result="l">
      <feDistantLight azimuth="45" elevation="60"/>
    </feDiffuseLighting>
  </filter>
  <filter id="edge" x="-10%" y="-10%" width="120%" height="120%">
    <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="4" seed="{seed+17}" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="45" xChannelSelector="R" yChannelSelector="G" result="d"/>
    <feGaussianBlur in="d" stdDeviation="6"/>
  </filter>
  <mask id="kenar">
    <rect x="0" y="0" width="{W}" height="{H}" fill="black"/>
    <rect x="46" y="40" width="{W-92}" height="{H-80}" rx="30" fill="white" filter="url(#edge)"/>
  </mask>
</defs>"""


def frame(seed, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">
{defs(seed)}
<rect width="{W}" height="{H}" fill="#f7f1e5"/>
<rect width="{W}" height="{H}" filter="url(#paper)" opacity="0.35" style="mix-blend-mode:multiply"/>
<g mask="url(#kenar)">
<g style="isolation:isolate">
{body}
</g>
</g>
</svg>
"""


M = 'style="mix-blend-mode:multiply"'


def wash(cx, cy, rx, ry, color, op=0.7):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" opacity="{op}" filter="url(#wash)" {M}/>'


def sky(top, mid, bottom, horizon=520):
    """Katmanlı gökyüzü yıkaması."""
    out = [f'<rect x="0" y="0" width="{W}" height="{horizon+80}" fill="{bottom}" opacity="0.55" filter="url(#wash)" {M}/>']
    out.append(f'<rect x="-100" y="-100" width="{W+200}" height="{horizon*0.65}" fill="{mid}" opacity="0.6" filter="url(#wash)" {M}/>')
    out.append(f'<rect x="-100" y="-120" width="{W+200}" height="{horizon*0.4}" fill="{top}" opacity="0.7" filter="url(#wash)" {M}/>')
    return "\n".join(out)


def peribacasi(x, gy, h, bw, body, cap, rnd):
    """Peribacası: geniş gövde, daralan boyun, koyu şapka."""
    nw = bw * rnd.uniform(0.22, 0.32)
    top = gy - h
    l, r = x - bw / 2, x + bw / 2
    p = (f"M{l:.0f},{gy} C{l+bw*0.08:.0f},{gy-h*0.45:.0f} {x-nw*1.4:.0f},{top+h*0.35:.0f} {x-nw:.0f},{top+18:.0f} "
         f"L{x+nw:.0f},{top+18:.0f} C{x+nw*1.4:.0f},{top+h*0.35:.0f} {r-bw*0.08:.0f},{gy-h*0.45:.0f} {r:.0f},{gy} Z")
    cw = nw * 2.3
    c = (f"M{x-cw:.0f},{top+22:.0f} C{x-cw*0.9:.0f},{top-8:.0f} {x-cw*0.3:.0f},{top-26:.0f} {x:.0f},{top-28:.0f} "
         f"C{x+cw*0.3:.0f},{top-26:.0f} {x+cw*0.9:.0f},{top-8:.0f} {x+cw:.0f},{top+22:.0f} Z")
    shade = (f"M{x+nw*0.2:.0f},{top+24:.0f} C{x+nw:.0f},{top+h*0.4:.0f} {r-bw*0.2:.0f},{gy-h*0.3:.0f} {r-bw*0.12:.0f},{gy} L{r:.0f},{gy} "
             f"C{r-bw*0.08:.0f},{gy-h*0.45:.0f} {x+nw*1.4:.0f},{top+h*0.35:.0f} {x+nw:.0f},{top+18:.0f} Z")
    return (f'<path d="{p}" fill="{body}" opacity="0.97" filter="url(#wc1)"/>'
            f'<path d="{shade}" fill="{cap}" opacity="0.28" filter="url(#wc2)" {M}/>'
            f'<path d="{c}" fill="{cap}" opacity="0.95" filter="url(#wc2)"/>')


def tepe(points, gy, color, op=0.75, f="wc1"):
    """Yumuşak tepe silueti; points = [(x,y), ...] soldan sağa."""
    d = f"M-60,{H+40} L-60,{points[0][1]}"
    prev = (-60, points[0][1])
    for x, y in points:
        mx = (prev[0] + x) / 2
        d += f" C{mx:.0f},{prev[1]} {mx:.0f},{y} {x},{y}"
        prev = (x, y)
    d += f" L{W+60},{prev[1]} L{W+60},{H+40} Z"
    return f'<path d="{d}" fill="{color}" opacity="{op}" filter="url(#{f})" {M}/>'


def ev(x, gy, s, wall, roof, window=None):
    w, h = 70 * s, 50 * s
    out = [f'<rect x="{x-w/2:.0f}" y="{gy-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{wall}" opacity="0.8" filter="url(#wc2)" {M}/>',
           f'<path d="M{x-w/2-8*s:.0f},{gy-h+2:.0f} L{x+w/2+8*s:.0f},{gy-h+2:.0f} L{x+w/2:.0f},{gy-h-12*s:.0f} L{x-w/2:.0f},{gy-h-12*s:.0f} Z" fill="{roof}" opacity="0.8" filter="url(#wc2)" {M}/>']
    if window:
        out.append(f'<circle cx="{x+w*0.15:.0f}" cy="{gy-h*0.55:.0f}" r="{26*s:.0f}" fill="{window}" opacity="0.55" filter="url(#glow)"/>')
        out.append(f'<rect x="{x+w*0.05:.0f}" y="{gy-h*0.7:.0f}" width="{14*s:.0f}" height="{16*s:.0f}" fill="{window}" opacity="0.95" filter="url(#wc2)"/>')
    return "\n".join(out)


def testi(x, y, s, color, op=0.9):
    """Toprak testi; (x,y) tabanın ortası."""
    d = (f"M{x-9*s:.1f},{y} C{x-30*s:.1f},{y-12*s:.1f} {x-34*s:.1f},{y-48*s:.1f} {x-12*s:.1f},{y-62*s:.1f} "
         f"L{x-8*s:.1f},{y-74*s:.1f} L{x-12*s:.1f},{y-80*s:.1f} L{x+12*s:.1f},{y-80*s:.1f} L{x+8*s:.1f},{y-74*s:.1f} "
         f"L{x+12*s:.1f},{y-62*s:.1f} C{x+34*s:.1f},{y-48*s:.1f} {x+30*s:.1f},{y-12*s:.1f} {x+9*s:.1f},{y} Z")
    kulp = f"M{x+14*s:.1f},{y-70*s:.1f} C{x+34*s:.1f},{y-72*s:.1f} {x+36*s:.1f},{y-50*s:.1f} {x+24*s:.1f},{y-44*s:.1f}"
    return (f'<path d="{d}" fill="{color}" opacity="{op}" filter="url(#wc2)" {M}/>'
            f'<path d="{kulp}" fill="none" stroke="{color}" stroke-width="{5*s:.1f}" opacity="{op}" filter="url(#wc2)" {M}/>')


def kiz(x, gy, s, color, testi_renk, yon=1, op=0.85):
    """Başörtülü, uzun etekli kız silueti; yon=1 sağa bakar, testi kolunda."""
    hx, hy = x, gy - 150 * s
    out = []
    # etek ve gövde
    d = (f"M{x-8*s:.1f},{hy+16*s:.1f} C{x-22*s:.1f},{hy+30*s:.1f} {x-26*s:.1f},{gy-70*s:.1f} {x-40*s:.1f},{gy} "
         f"L{x+40*s:.1f},{gy} C{x+26*s:.1f},{gy-70*s:.1f} {x+22*s:.1f},{hy+30*s:.1f} {x+8*s:.1f},{hy+16*s:.1f} Z")
    out.append(f'<path d="{d}" fill="{color}" opacity="{op}" filter="url(#wc2)" {M}/>')
    # başörtüsü: baştan omuza uzanan damla
    bd = (f"M{hx:.1f},{hy-20*s:.1f} C{hx+18*s:.1f},{hy-20*s:.1f} {hx+20*s:.1f},{hy+4*s:.1f} {hx+16*s:.1f},{hy+14*s:.1f} "
          f"C{hx+22*s:.1f},{hy+40*s:.1f} {hx-24*s:.1f},{hy+44*s:.1f} {hx-18*s:.1f},{hy+14*s:.1f} "
          f"C{hx-22*s:.1f},{hy+2*s:.1f} {hx-16*s:.1f},{hy-20*s:.1f} {hx:.1f},{hy-20*s:.1f} Z")
    out.append(f'<path d="{bd}" fill="{color}" opacity="{op}" filter="url(#wc2)" {M}/>')
    # kol ve testi
    tx = x + yon * 34 * s
    out.append(f'<path d="M{x+yon*10*s:.1f},{hy+30*s:.1f} Q{x+yon*30*s:.1f},{hy+50*s:.1f} {tx:.1f},{hy+62*s:.1f}" fill="none" stroke="{color}" stroke-width="{8*s:.1f}" stroke-linecap="round" opacity="{op}" filter="url(#wc2)" {M}/>')
    out.append(testi(tx + yon * 6 * s, hy + 128 * s, 0.85 * s, testi_renk))
    return "\n".join(out)


def yildizlar(rnd, n, ymax, color="#fff8e0"):
    return "\n".join(
        f'<circle cx="{rnd.uniform(60, W-60):.0f}" cy="{rnd.uniform(50, ymax):.0f}" r="{rnd.uniform(1.2, 3):.1f}" fill="{color}" opacity="{rnd.uniform(0.5, 0.95):.2f}"/>'
        for _ in range(n))


def ay(cx, cy, r, color="#fdf3d3", halo="#fff6dc"):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r*2.6}" fill="{halo}" opacity="0.35" filter="url(#wash)"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" opacity="0.95" filter="url(#wc2)"/>'
            f'<circle cx="{cx-r*0.3}" cy="{cy-r*0.2}" r="{r*0.25}" fill="#e8d9b0" opacity="0.4" filter="url(#wc2)" {M}/>'
            f'<circle cx="{cx+r*0.35}" cy="{cy+r*0.3}" r="{r*0.18}" fill="#e8d9b0" opacity="0.35" filter="url(#wc2)" {M}/>')


def vadi(rnd, gy, body, cap, xs, scale=1.0):
    out = []
    for x in xs:
        h = rnd.uniform(160, 300) * scale
        bw = rnd.uniform(90, 140) * scale
        out.append(peribacasi(x + rnd.uniform(-20, 20), gy + rnd.uniform(-8, 8), h, bw, body, cap, rnd))
    return "\n".join(out)


def acik(hexrenk, oran):
    """Rengi kâğıt rengine doğru açar (uzaktaki sıralar için)."""
    r, g, b = (int(hexrenk[i:i+2], 16) for i in (1, 3, 5))
    k = (247, 241, 229)
    return "#" + "".join(f"{int(c + (kc - c) * oran):02x}" for c, kc in zip((r, g, b), k))


def kume(rnd, gy, body, cap, x0, x1, scale=1.0, sik=0.8):
    """x0–x1 arasında birbirine yaslanan, ortası daha yüksek bir peribacası kümesi."""
    xs, x = [], x0
    while x < x1:
        bw = rnd.uniform(80, 120) * scale
        xs.append((x, bw))
        x += bw * sik * rnd.uniform(0.8, 1.15)
    orta = (x0 + x1) / 2
    yari = max(1, (x1 - x0) / 2)
    out = []
    # önce kısalar, sonra uzunlar; kenardakiler daha kısa
    sirali = sorted(xs, key=lambda t: -abs(t[0] - orta))
    for x, bw in sirali:
        yakinlik = 1 - min(1, abs(x - orta) / yari) * 0.45
        h = rnd.uniform(180, 300) * scale * yakinlik
        out.append(peribacasi(x, gy + rnd.uniform(-6, 10), h, bw, body, cap, rnd))
    return "\n".join(out)


def vadi2(rnd, gy, body, cap, on_kumeler, scale=1.0, arka=True):
    """Arkada soluk, sık bir sıra; önde belirgin kümeler."""
    out = []
    if arka:
        out.append(kume(rnd, gy - 45, acik(body, 0.5), acik(cap, 0.5), -40, W + 40, scale * 0.55, sik=1.15))
    for x0, x1 in on_kumeler:
        out.append(kume(rnd, gy, body, cap, x0, x1, scale))
    return "\n".join(out)


# --- Sahneler ---------------------------------------------------------------

def sahne1():
    """Peribacalı vadi, akşam; nenenin evinde ışık."""
    rnd = random.Random(1)
    b = [sky("#3d4f86", "#9b7fa8", "#f0c9a4", 560),
         yildizlar(rnd, 26, 230),
         ay(930, 150, 46),
         tepe([(150, 520), (420, 470), (700, 510), (1000, 460), (1260, 500)], 0, "#c9a98c", 0.55),
         vadi2(rnd, 600, "#d9b48a", "#7a5640", [(20, 470), (760, 1180)], 1.05),
         tepe([(200, 610), (500, 590), (800, 620), (1100, 600)], 0, "#b68a64", 0.8),
         ev(640, 640, 1.4, "#e6cfae", "#8a6248", "#ffcf6b"),
         tepe([(300, 700), (700, 680), (1000, 710)], 0, "#8a6a52", 0.75, "wc2")]
    return frame(11, "\n".join(b))


def sahne2():
    """Dolunayda vadiye inen Nilüfer, elinde testi."""
    rnd = random.Random(2)
    b = [sky("#23315f", "#3f5591", "#8c8fb8", 560),
         yildizlar(rnd, 40, 330),
         ay(860, 190, 78),
         vadi2(rnd, 560, "#8f94b8", "#3f456e", [(10, 400), (780, 1190)], 1.1),
         tepe([(150, 548), (450, 535), (800, 552), (1150, 540)], 0, "#5d6595", 0.85),
         # taşların içinde saklı ışık
         "\n".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff2c4" opacity="0.5" filter="url(#glow)"/>'
                   for x, y, r in [(260, 690, 18), (420, 720, 12), (760, 700, 16), (980, 730, 14), (1100, 690, 10)]),
         tepe([(250, 700), (600, 680), (950, 705)], 0, "#3f4775", 0.85, "wc2"),
         kiz(560, 690, 1.35, "#2a2f55", "#b5603c")]
    return frame(22, "\n".join(b))


def sahne3():
    """Sisli kış gecesi; testiden yükselen gümüş yol köye uzanıyor."""
    rnd = random.Random(3)
    b = [sky("#4b4f62", "#7d7f93", "#a9a8b6", 600),
         "\n".join(ev(x, y, s, "#b9b5c2", "#5f5a70", "#ffd98a" if i % 2 else None)
                   for i, (x, y, s) in enumerate([(820, 400, 0.9), (930, 420, 1.0), (1050, 395, 0.85), (980, 360, 0.7)])),
         tepe([(200, 470), (600, 440), (1000, 460), (1250, 430)], 0, "#8a8798", 0.55),
         # sis katmanları
         wash(300, 380, 520, 120, "#c9c6d4", 0.7),
         wash(900, 300, 500, 110, "#bdbacb", 0.55),
         wash(600, 560, 700, 140, "#cfcbd8", 0.6),
         # gümüş yol
         '<path d="M260,690 C380,600 330,540 520,520 C700,500 640,450 800,430 C880,420 900,410 940,400" fill="none" stroke="#fffbe8" stroke-width="46" stroke-linecap="round" opacity="0.55" filter="url(#glow)"/>',
         '<path d="M260,690 C380,600 330,540 520,520 C700,500 640,450 800,430 C880,420 900,410 940,400" fill="none" stroke="#f3f0ff" stroke-width="14" stroke-linecap="round" opacity="0.85" filter="url(#wc2)"/>',
         tepe([(300, 720), (700, 700), (1100, 730)], 0, "#6c6880", 0.75, "wc2"),
         testi(240, 735, 1.4, "#a3583a"),
         '<circle cx="240" cy="620" r="60" fill="#fffbe8" opacity="0.6" filter="url(#glow)"/>']
    return frame(33, "\n".join(b))


def sahne4():
    """Sabah; Nilüfer testisiyle yeniden vadiye iniyor."""
    rnd = random.Random(4)
    b = [sky("#a9c4d9", "#f3d3b0", "#fbe6c2", 560),
         f'<circle cx="300" cy="300" r="90" fill="#fbd27a" opacity="0.55" filter="url(#wash)" {M}/>',
         '<circle cx="300" cy="300" r="46" fill="#f8c25c" opacity="0.85" filter="url(#wc2)"/>',
         tepe([(150, 510), (500, 480), (850, 500), (1200, 470)], 0, "#d8b897", 0.55),
         vadi2(rnd, 590, "#e2b98d", "#9a6a48", [(380, 760), (980, 1190)], 0.95),
         tepe([(200, 610), (550, 600), (900, 630), (1200, 610)], 0, "#c79a6e", 0.8),
         '<path d="M1180,800 C1000,740 900,720 820,690" fill="none" stroke="#f1dcc0" stroke-width="40" stroke-linecap="round" opacity="0.8" filter="url(#wc1)"/>',
         tepe([(300, 720), (650, 700), (1000, 730)], 0, "#a37b58", 0.7, "wc2"),
         kiz(860, 700, 0.85, "#6d4a3a", "#b5603c", yon=-1)]
    return frame(44, "\n".join(b))


def elma(x, y, s, rot):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">'
            f'<path d="M0,-30 C-30,-48 -60,-20 -52,14 C-46,44 -20,60 0,48 C20,60 46,44 52,14 C60,-20 30,-48 0,-30 Z" fill="#c8453a" opacity="0.88" filter="url(#wc2)" {M}/>'
            f'<path d="M-30,-14 C-38,0 -36,16 -28,26" fill="none" stroke="#f7d8b4" stroke-width="7" stroke-linecap="round" opacity="0.6" filter="url(#wc2)"/>'
            f'<path d="M0,-30 C2,-44 6,-52 10,-58" fill="none" stroke="#5a3a24" stroke-width="5" stroke-linecap="round" opacity="0.9" filter="url(#wc2)"/>'
            f'<path d="M8,-50 C26,-70 52,-62 56,-54 C40,-40 20,-40 8,-50 Z" fill="#6f9a52" opacity="0.85" filter="url(#wc2)" {M}/>'
            f'</g>')


def sahne5():
    """Gökten üç elma düşer."""
    rnd = random.Random(5)
    b = [sky("#a7c2dc", "#d7e3ea", "#f6e8cf", 600),
         wash(300, 200, 260, 70, "#ffffff", 0.6),
         wash(900, 150, 300, 60, "#ffffff", 0.55),
         vadi2(rnd, 680, "#e1c09c", "#9c7354", [(10, 260), (940, 1190)], 0.9),
         tepe([(200, 680), (600, 650), (1000, 690)], 0, "#b9a07f", 0.7),
         elma(390, 300, 1.4, -14),
         elma(610, 440, 1.6, 8),
         elma(830, 260, 1.3, 22),
         "\n".join(f'<path d="M{x},{y-90} L{x},{y-170}" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity="0.6" filter="url(#wc2)"/>'
                   for x, y in [(390, 300), (610, 440), (830, 260)])]
    return frame(55, "\n".join(b))


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    for i, fn in enumerate([sahne1, sahne2, sahne3, sahne4, sahne5], 1):
        (out / f"{i}.svg").write_text(fn(), encoding="utf-8")
        print("yazıldı", out / f"{i}.svg")
