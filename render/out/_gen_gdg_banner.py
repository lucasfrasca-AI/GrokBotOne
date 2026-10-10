#!/usr/bin/env python3
"""GDG / Spark Festival event banner, in the dark glowing poster style of _gen_gdg.py.

Outputs (same dir): gdg-event-banner.{svg,png} 1200x627, gdg-event-banner-square.{svg,png} 1200x1200,
and 390-wide previews. Helpers (fonts, text measuring, glow, dot grid, guards) come from _gen_gdg.py.
Images (same-dir hrefs, rsvg rule): antigravity-a-mark.png (rainbow A knocked out of the RSVP screenshot),
logo-gdg-color-dark.png (GDG mark, original four colours), lf-mark.png.
Colours: tokens.css (+ the four sampled GDG colours, inside the logo PNG only). The Antigravity rainbow lives only inside
the A raster, never as SVG colour.
Run: python3 _gen_gdg_banner.py
"""
import re
import subprocess
import sys

from PIL import Image

import _gen_gdg as g

OUT = g.OUT
# GDG mark in its original four colours (sampled from gdg-logo-original.png); used in the logo PNG only
GDG_ORIGINAL = {"#D85140", "#5383EC", "#479B5F", "#F1BF42"}
ALLOWED = g.ALLOWED_HEX | GDG_ORIGINAL
A_IMG, GDG_IMG = "antigravity-a-mark.png", "logo-gdg-color-dark.png"
TITLE1, TITLE2 = "Google for Developers:", "Spark Festival"
LOCATION = "Google Sydney Headquarters, Pyrmont"
SESSIONS = ("AI Sovereignty panel", "Antigravity 2.0 Agent Skills workshop")
LOGOS = []


def img_size(fn):
    return Image.open(OUT / fn).size


def image(fn, x, y, w=None, h=None, tag=None):
    iw, ih = img_size(fn)
    if w is None:
        w = h * iw / ih
    if h is None:
        h = w * ih / iw
    if tag:
        LOGOS.append((tag, x, y, x + w, y + h))
    return (f'<image href="{fn}" xlink:href="{fn}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'preserveAspectRatio="xMidYMid meet"/>'), w, h


def gdg_corner(right=1164, top=36, width=132):
    s, w, h = image(GDG_IMG, right - width, top, w=width, tag="gdg")
    lab = g.T(right, top + h + 17.5, "Google Developer Group", 15, "mono", 500, g.MUTE, "end", ls=0.6, tag="gdg-label")
    return s + "\n" + lab


def pin(x, y, s=1.0, col=g.SUB):
    """Simple map pin: teardrop outline with a dot, top-left at (x, y), ~18x24 at s=1."""
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({s})" fill="none" stroke="{col}" stroke-width="2" '
            f'stroke-linejoin="round"><path d="M9 23 C9 23 1.5 14.5 1.5 9 A7.5 7.5 0 0 1 16.5 9 C16.5 14.5 9 23 9 23 Z"/>'
            f'<circle cx="9" cy="9" r="2.8" fill="{col}" stroke="none"/></g>')


def sessions_group(x, cy, fs, gap):
    """The two sessions as two quiet mono lines, each with a small violet 01 / 02 index,
    block vertically centred on cy (the centre of the L mark). Returns (svg, right_x)."""
    lh = fs * 1.35
    ix_w = g.tw("00", "mono", fs, 500, ls=0.6)
    tx = x + ix_w + gap
    out, right = [], x
    for i, ln in enumerate(SESSIONS):
        y = cy + (i - 0.5) * lh + fs * 0.36
        out.append(g.T(x, y, f"0{i + 1}", fs, "mono", 500, g.VIOLET, ls=0.6, tag=f"session-ix-{i}"))
        out.append(g.T(tx, y, ln, fs, "mono", 500, g.SUB, ls=0.6, tag=f"session-{i}"))
        right = max(right, tx + g.tw(ln, "mono", fs, 500, ls=0.6))
    return "\n".join(out), right


def wrap(inner, w, h):
    defs = "\n    ".join(g.DEFS)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    {defs}
  </defs>
  <rect width="{w}" height="{h}" fill="{g.PITCH}"/>
{inner}
</svg>
'''


def start():
    g.start_page()
    LOGOS.clear()


def check(name, w, h, extra_boxes=()):
    def hit(a, b, m=0):
        return not (a[3] + m <= b[1] or b[3] + m <= a[1] or a[4] + m <= b[2] or b[4] + m <= a[2])
    errs = []
    boxes = LOGOS + list(extra_boxes)
    for i, a in enumerate(g.TEXT_BOXES):
        if a[1] < 20 or a[3] > w - 20 or a[2] < 0 or a[4] > h - 10:
            errs.append(f"off-canvas {a}")
        for b in boxes:
            if hit(a, b, 6):
                errs.append(f"{a[0]!r} hits {b[0]}")
        for b in g.TEXT_BOXES[i + 1:]:
            if hit(a, b, 1):
                errs.append(f"text overlap {a[0]!r} / {b[0]!r}")
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            if hit(a, b, 8):
                errs.append(f"image overlap {a[0]} / {b[0]}")
    if errs:
        raise SystemExit(f"{name}: layout errors:\n  " + "\n  ".join(errs))


def guard(svg, name):
    for ch in ("\u2014", "\u2013"):
        if ch in svg:
            raise SystemExit(f"dash in {name}")
    for hx in re.findall(r"#[0-9A-Fa-f]{6}\b", svg):
        if hx.upper() not in ALLOWED:
            raise SystemExit(f"off-palette colour in {name}: {hx}")
    for m in re.findall(r"rgba\(([^)]*)\)", svg):
        if tuple(int(float(v)) for v in m.split(",")[:3]) not in {(243, 243, 241), (168, 85, 247), (5, 1, 14)}:
            raise SystemExit(f"off-palette rgba in {name}: {m}")
    for body in re.findall(r"<radialGradient.*?</radialGradient>", svg, re.S):
        for c in re.findall(r'stop-color="([^"]+)"', body):
            if c.upper() not in g.TOKEN_STOPS:
                raise SystemExit(f"non-token glow stop in {name}: {c}")
    if "<linearGradient" in svg or "<filter" in svg:
        raise SystemExit(f"linear gradient / filter in {name}")


# ---------------------------------------------------------------- 1200 x 627
def gen_banner():
    W, H = 1200, 627
    start()
    p = []
    # the A, right, with glow
    a_h = 372
    aw = a_h * img_size(A_IMG)[0] / img_size(A_IMG)[1]
    ax, ay = W - 60 - aw, 128
    acx, acy = ax + aw / 2, ay + a_h * 0.55
    p.append(g.dotgrid(acx, acy, 330))
    p.append(g.glow(acx, acy, 340, 0.55, sy=0.9))
    s, *_ = image(A_IMG, ax, ay, h=a_h, tag="A")
    p.append(s)
    # title block, left
    fs = 60
    b1 = 236
    p.append(g.T(g.MARGIN - 3, b1, TITLE1, fs, "head", 600, g.BONE, ls=-1.8, tag="t1"))
    p.append(g.T(g.MARGIN - 3, b1 + 70, TITLE2, fs, "head", 600, g.BONE, ls=-1.8, tag="t2"))
    ly = b1 + 70 + 66
    p.append(pin(g.MARGIN, ly - 20, 1.05))
    p.append(g.T(g.MARGIN + 32, ly, LOCATION, 26, "sans", 400, g.SUB, tag="loc"))
    # bottom row: LF mark | the two sessions
    lf_w = 52
    lf_h = lf_w * 144 / 154
    lf_y = H - 36 - lf_h
    p.append(f'<image href="lf-mark.png" xlink:href="lf-mark.png" x="{g.MARGIN}" y="{lf_y:.1f}" width="{lf_w}" '
             f'height="{lf_h:.1f}"/>')
    LOGOS.append(("lf", g.MARGIN, lf_y, g.MARGIN + lf_w, lf_y + lf_h))
    sg, right = sessions_group(g.MARGIN + lf_w + 28, lf_y + lf_h / 2, 20, 12)
    p.append(sg)
    p.append(gdg_corner())
    check("gdg-event-banner", W, H)
    return wrap("\n".join(p), W, H), (W, H)


# ---------------------------------------------------------------- 1200 x 1200
def gen_square():
    W, H = 1200, 1200
    start()
    p = []
    a_h = 566
    aw = a_h * img_size(A_IMG)[0] / img_size(A_IMG)[1]
    ax, ay = (W - aw) / 2 + 150, 138
    acx, acy = ax + aw / 2, ay + a_h * 0.55
    p.append(g.dotgrid(acx, acy, 470))
    p.append(g.glow(acx, acy, 470, 0.55, sy=0.9))
    s, *_ = image(A_IMG, ax, ay, h=a_h, tag="A")
    p.append(s)
    fs = 78
    b1 = 842
    p.append(g.T(g.MARGIN - 4, b1, TITLE1, fs, "head", 600, g.BONE, ls=-2.4, tag="t1"))
    p.append(g.T(g.MARGIN - 4, b1 + 88, TITLE2, fs, "head", 600, g.BONE, ls=-2.4, tag="t2"))
    ly = b1 + 88 + 76
    p.append(pin(g.MARGIN, ly - 25, 1.3))
    p.append(g.T(g.MARGIN + 38, ly, LOCATION, 30, "sans", 400, g.SUB, tag="loc"))
    # bottom row: LF mark (standard spot) | the two sessions
    p.append(g.lf_mark())
    LOGOS.append(("lf",) + g.LF_BOX)
    sg, right = sessions_group(g.MARGIN + 72 + 32, g.LOGO_BR_CY, 24, 14)
    p.append(sg)
    p.append(gdg_corner())
    check("gdg-event-banner-square", W, H)
    return wrap("\n".join(p), W, H), (W, H)


def render(name, svg, size):
    guard(svg, name)
    sp, pp = OUT / f"{name}.svg", OUT / f"{name}.png"
    sp.write_text(svg)
    # build.sh fits into 1200x1200 keeping aspect, so the 1200x627 viewBox renders at 1200x627
    subprocess.run([g.BUILD, str(sp), str(pp)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    im = Image.open(pp).convert("RGB")
    assert im.size == size, im.size
    im.resize((390, round(390 * size[1] / size[0])), Image.LANCZOS).save(OUT / f"preview-{name}-390.png")
    print(f"wrote {sp.name}, {pp.name} {im.size}, preview-{name}-390.png")


if __name__ == "__main__":
    for name, fn in (("gdg-event-banner", gen_banner), ("gdg-event-banner-square", gen_square)):
        if len(sys.argv) > 1 and name not in sys.argv[1:]:
            continue
        svg, size = fn()
        render(name, svg, size)
