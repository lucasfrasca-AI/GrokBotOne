#!/usr/bin/env python3
"""GDG / Google for Developers x Spark Festival graphics (1200x1200 dark brand).

CURRENT STYLE (4th): chart-led launch poster (Linear / Vercel): pitch background, one dominant
visual per graphic with a soft token-colour radial glow and faint rule2 dot grid, minimal text,
compact mono source footer. Earlier styles: .bak-expressive, .bak-apple, .bak-swiss.

House style copied (not imported) from _gen_fde.py: spectrum rule top-left, mono violet
eyebrow, big title, subtitle, LF mark bottom-left, corner logos, dash guard.
Swiss / International Typographic editorial style: bone paper, ink type, strict 12-column grid
(36px margins, 72px columns, 24px gutters), thick ink section rules with 01/02/03 markers,
hairline subdivisions, no boxes, no fills, no gradients. Violet only on the key items.
Earlier styles: _gen_gdg.py.bak-expressive, _gen_gdg.py.bak-apple.
Fonts: General Sans (Fontshare, installed in ~/.fonts) for headings and hero numbers,
Geist for body, Geist Mono for labels.

Graphics:
  gdg-stats         Sovereign AI in Australia, by the numbers
  gdg-sovereignty   AI sovereignty is leverage (panel framework)
  gdg-antigravity   Antigravity 2.0: one prompt, three agents (workshop)

Logos: real violet PNGs are picked up automatically from
  /workspace/projects/gdg-sovereignty/assets/{google-for-developers,spark-foundation}-violet.png
  -> cropped to alpha bbox and copied to OUT as logo-gfd-violet.png / logo-spark-violet.png.
If neither source nor copy exists, a dashed placeholder box with the same bounding box is drawn.

Run:  python3 _gen_gdg.py            (writes SVGs, renders PNGs + 390 previews)
"""
import math
import re
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageFont

OUT = Path("/workspace/render/out")
ASSETS = Path("/workspace/projects/gdg-sovereignty/assets")
BUILD = "/workspace/render/build.sh"
W = H = 1200

# ---------------------------------------------------------------- tokens (tokens.css only)
PITCH = "#05010E"
BONE = "#F3F3F1"
SUB = "#D4D2CE"
MUTE = "#A4A098"
VIOLET = "#A855F7"
INDIGO = "#6366F1"
AMBER = "#FCD34D"
ACCENT = "#895AF6"
SURFACE = "#160F24"
SURFACE2 = "#1C1528"
INPUT = "#1B122B"
RED = "#DC2828"
RULE = "rgba(243,243,241,.12)"
RULE2 = "rgba(243,243,241,.07)"
ALLOWED_HEX = {c.upper() for c in (PITCH, BONE, SUB, MUTE, VIOLET, INDIGO, AMBER, ACCENT,
                                    SURFACE, SURFACE2, INPUT, RED)}


INK = PITCH                        # type and rules on bone paper
INK2 = "rgba(5,1,14,.74)"          # secondary body (ink tint)
INK3 = "rgba(5,1,14,.56)"          # quiet labels (ink tint)


def violet_a(a):
    return f"rgba(168,85,247,{a})"


SANS = "Geist, ui-sans-serif, system-ui, sans-serif"
HEAD = "General Sans, Geist, ui-sans-serif, system-ui, sans-serif"
MONO = "Geist Mono, ui-monospace, SFMono-Regular, Menlo, monospace"

MARK = "lf-mark.png"          # same-dir href: rsvg will not load ../ paths
MARGIN = 36
BODY_TOP = 168
BODY_BOT = 1080
LF_BOX = (36, 1105, 108, 1105 + 72 * 144 / 154)

# ---------------------------------------------------------------- logos
LOGO_RIGHT = W - MARGIN       # 1164
LOGO_TR_CY = 64               # eyebrow line
LOGO_BR_CY = 1105 + 72 * 144 / 154 / 2   # LF mark centre (1138.7)
# (out filename, source filename, target width, max height, placeholder height)
# GFD lockup is a 10:1 wordmark: 150 wide (~15 tall) keeps it legible at 390 px.
# Spark Foundation lockup is 2.2:1 (stacked "spark > foundation"): sized by height (~43 tall, ~94 wide), level
# with the LF mark; a 20-26 px height cap would shrink it to ~55 px wide and unreadable.
LOGO_GFD = ("logo-gfd-violet.png", "google-for-developers-violet.png", 150, 48, 15)
LOGO_SPARK = ("logo-spark-violet.png", "spark-foundation-violet.png", 94, 43, 43)
# GDG mark (purple/yellow, redrawn from the original): replaces the Google for Developers lockup top-right
LOGO_GDG = ("logo-gdg-purple-yellow.png", "gdg-logo-purple-yellow.png", 132, 40, 28)
GDG_LABEL = "Google Developer Group"
LOGO_STATUS = {}
LOGO_BOXES = []


def sync_logo(spec):
    """Copy (alpha-cropped) source asset into OUT if present and newer. Returns (w, h) px or None."""
    fn, src_name, *_ = spec
    src, dst = ASSETS / src_name, OUT / fn
    if src.exists() and (not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime):
        im = Image.open(src).convert("RGBA")
        bb = im.getchannel("A").getbbox()
        if bb:
            im = im.crop(bb)
        im.save(dst)
    if dst.exists():
        LOGO_STATUS[fn] = "real" if src.exists() else "real (copy in out/, source missing)"
        return Image.open(dst).size
    LOGO_STATUS[fn] = "placeholder"
    return None


def logo(spec, right, cy):
    fn, _, tw_, max_h, ph_h = spec
    size = sync_logo(spec)
    if size:
        pw, ph = size
        w_, h_ = tw_, tw_ * ph / pw
        if h_ > max_h:
            h_, w_ = max_h, max_h * pw / ph
    else:
        w_, h_ = tw_, ph_h
    x, y = right - w_, cy - h_ / 2
    LOGO_BOXES.append((fn, x, y, x + w_, y + h_))
    if size:
        return (f'<image href="{fn}" xlink:href="{fn}" x="{x:.1f}" y="{y:.1f}" width="{w_:.1f}" '
                f'height="{h_:.1f}" preserveAspectRatio="xMaxYMid meet"/>')
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w_:.1f}" height="{h_:.1f}" rx="4" fill="none" '
            f'stroke="{violet_a(.6)}" stroke-width="1.5" stroke-dasharray="5 4"/>'
            f'<!-- placeholder for {fn} -->')


def corner_logos():
    """GDG mark top-right (top on the 36px margin, bottom on the eyebrow baseline) + label; Spark bottom-right."""
    size = sync_logo(LOGO_GDG)
    h = LOGO_GDG[2] * size[1] / size[0] if size else LOGO_GDG[4]
    top = MARGIN
    out = ["  " + logo(LOGO_GDG, LOGO_RIGHT, top + h / 2),
           "  " + T(LOGO_RIGHT, top + h + 17.5, GDG_LABEL, 15, "mono", 500, MUTE, "end", ls=0.6, tag="gdg-label"),
           "  " + logo(LOGO_SPARK, LOGO_RIGHT, LOGO_BR_CY)]
    return "\n".join(out)


# ---------------------------------------------------------------- fonts + text
FONT_DIR = "/usr/share/fonts/truetype/sand-box/google"
_FONT_FILES = {
    "sans": f"{FONT_DIR}/Geist/Geist-VariableFont_wght.ttf",
    "sans_i": f"{FONT_DIR}/Geist/Geist-Italic-VariableFont_wght.ttf",
    "mono": f"{FONT_DIR}/Geist Mono/GeistMono-VariableFont_wght.ttf",
}
GS_DIR = Path.home() / ".fonts"
_GS = {300: "Light", 400: "Regular", 500: "Medium", 600: "Semibold", 700: "Bold"}
_font_cache = {}
WARN = []
TEXT_BOXES = []      # (label, x0, y0, x1, y1) for every text run, for collision checks


def font(kind, size, weight=400):
    key = (kind, size, weight)
    if key not in _font_cache:
        if kind in ("head", "head_i"):
            nm = _GS[min(_GS, key=lambda k: abs(k - weight))]
            if kind == "head_i":
                nm = (nm if nm != "Regular" else "") + "Italic"
            path = GS_DIR / f"GeneralSans-{nm}.ttf"
            if not path.exists():
                raise SystemExit(f"General Sans missing: {path}")
            _font_cache[key] = ImageFont.truetype(str(path), size)
            return _font_cache[key]
        f = ImageFont.truetype(_FONT_FILES[kind], size)
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
        _font_cache[key] = f
    return _font_cache[key]


def tw(text, kind="sans", size=16, weight=400, ls=0):
    return font(kind, size, weight).getlength(text) + ls * len(text)


def esc(t):
    return escape(t, {"'": "&apos;", '"': "&quot;"})


def wrap_px(text, max_w, kind="sans", size=16, weight=400):
    words = text.split()
    lines, cur = [], []
    for w_ in words:
        trial = " ".join(cur + [w_])
        if tw(trial, kind, size, weight) <= max_w or not cur:
            cur.append(w_)
        else:
            lines.append(" ".join(cur))
            cur = [w_]
    if cur:
        lines.append(" ".join(cur))
    return lines


def T(x, y, s, fs=19, kind="sans", wt=400, fill=SUB, anchor="start", ls=0, italic=False,
      head=False, tag=None, opacity=None):
    """One text run. Records its bbox for collision checks."""
    if head:
        kind = "head"
    fam = MONO if kind == "mono" else (HEAD if kind == "head" else SANS)
    mk = (kind + "_i") if italic else kind
    w_ = tw(s, mk, fs, wt, ls)
    x0 = {"start": x, "middle": x - w_ / 2, "end": x - w_}[anchor]
    TEXT_BOXES.append((tag or s[:24], x0, y - 0.74 * fs, x0 + w_, y + 0.22 * fs))
    extra = ""
    if ls:
        extra += f' letter-spacing="{ls}"'
    if italic:
        extra += ' font-style="italic"'
    if anchor != "start":
        extra += f' text-anchor="{anchor}"'
    if opacity is not None:
        extra += f' fill-opacity="{opacity}"'
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{fs}" font-weight="{wt}" '
            f'fill="{fill}"{extra}>{esc(s)}</text>')


def para(x, y, text, max_w, fs=19, lh=None, **kw):
    """Wrapped paragraph; returns (svg, last_baseline)."""
    lh = lh or round(fs * 1.3)
    kind = "sans_i" if kw.get("italic") else kw.get("kind", "sans")
    lines = wrap_px(text, max_w, kind, fs, kw.get("wt", 400))
    out = [T(x, y + i * lh, ln, fs, **kw) for i, ln in enumerate(lines)]
    return "\n".join(out), y + (len(lines) - 1) * lh


def hero(x, y, num, fs=96, fill=BONE, unit=None, unit_fs=None, unit_fill=SUB, anchor="start", wt=700,
         tag=None):
    """Huge, tight General Sans number (negative tracking) with optional quiet unit after it."""
    ls = -round(fs * 0.04, 1)
    nw = tw(num, "head", fs, wt, ls)
    unit_fs = unit_fs or max(int(fs * 0.28), 20)
    gap = fs * 0.1
    uw = gap + tw(unit, "head", unit_fs, 500) if unit else 0
    total = nw + uw
    x0 = {"start": x, "middle": x - total / 2, "end": x - total}[anchor]
    TEXT_BOXES.append((tag or num, x0, y - 0.72 * fs, x0 + total, y + 0.03 * fs))
    s = (f'<text x="{x0:.1f}" y="{y:.1f}"><tspan font-family="{HEAD}" font-size="{fs}" font-weight="{wt}" '
         f'letter-spacing="{ls}" fill="{fill}">{esc(num)}</tspan>')
    if unit:
        s += (f'<tspan dx="{gap:.1f}" font-family="{HEAD}" font-size="{unit_fs}" font-weight="500" '
              f'letter-spacing="0" fill="{unit_fill}">{esc(unit)}</tspan>')
    return s + "</text>"


def hero_w(num, fs, wt=700):
    return tw(num, "head", fs, wt, -round(fs * 0.04, 1))


# ---------------------------------------------------------------- bento primitives (Apple)
RAD = 28            # the one corner radius
GUT = 20            # the one gutter
PAD = 32            # the one inner padding


def rrect(x, y, w, h, rx=RAD, fill=SURFACE, stroke=None, sw=0, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{st}{extra}/>'


def card(x, y, w, h, fill=SURFACE, stroke=RULE, sw=1):
    return rrect(x, y, w, h, RAD, fill=fill, stroke=stroke, sw=sw)


def label(x, y, s, fill=MUTE, anchor="start", tag=None):
    """Quiet mono uppercase label."""
    return T(x, y, s, 16, "mono", 500, fill, anchor, ls=1.4, tag=tag)


def hline(x0, x1, y, stroke=RULE, sw=1):
    return f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" stroke="{stroke}" stroke-width="{sw}"/>'


COLW, COLG = 72, 24                # 12-column grid


def GX(i):
    """Left edge of grid column i (0..11); GX(12) is the right margin + gutter."""
    return MARGIN + i * (COLW + COLG)


def SPAN(n):
    return n * COLW + (n - 1) * COLG


def rule(y, x0=None, x1=None, h=6, fill=None):
    x0 = GX(0) if x0 is None else x0
    x1 = W - MARGIN if x1 is None else x1
    return f'<rect x="{x0:.1f}" y="{y:.1f}" width="{x1 - x0:.1f}" height="{h}" fill="{fill or INK}"/>'


def hair(x0, x1, y, w=1, col=None):
    return (f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x1:.1f}" y2="{y:.1f}" stroke="{col or INK}" '
            f'stroke-width="{w}"/>')


def vhair(x, y0, y1, w=1, col=None):
    return (f'<line x1="{x:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y1:.1f}" stroke="{col or INK}" '
            f'stroke-width="{w}"/>')


def marker(x, y, num, text=None, tag=None):
    """Section marker: bold mono number, optional quiet label after it."""
    out = [T(x, y, num, 16, "mono", 700, INK, ls=1.0, tag=f"mk-{num}")]
    if text:
        out.append(T(x + 48, y, text, 16, "mono", 500, INK2, ls=1.4, tag=tag or f"mkl-{num}"))
    return "\n".join(out)


def slabel(x, y, s, fill=None, anchor="start", tag=None):
    return T(x, y, s, 16, "mono", 500, fill or INK2, anchor, ls=1.4, tag=tag)


def grid_x(x, w, n, gut=GUT):
    """n equal columns inside [x, x+w]: list of (x, w)."""
    cw = (w - gut * (n - 1)) / n
    return [(x + i * (cw + gut), cw) for i in range(n)]




# ---------------------------------------------------------------- page furniture (launch poster)
DEFS = []
_GID = [0]


def gid(prefix):
    _GID[0] += 1
    return f"id-{prefix}{_GID[0]}"


def glow(cx, cy, r, op=0.32, sy=1.0):
    """Soft violet light bloom: radial gradient of token colours fading to transparent."""
    g = gid("glow")
    DEFS.append(f'<radialGradient id="{g}" cx="0.5" cy="0.5" r="0.5">'
                f'<stop offset="0" stop-color="{VIOLET}" stop-opacity="{op:.3f}"/>'
                f'<stop offset="0.38" stop-color="{ACCENT}" stop-opacity="{op * 0.55:.3f}"/>'
                f'<stop offset="0.7" stop-color="{INDIGO}" stop-opacity="{op * 0.18:.3f}"/>'
                f'<stop offset="1" stop-color="{INDIGO}" stop-opacity="0"/></radialGradient>')
    return (f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{r:.1f}" ry="{r * sy:.1f}" fill="url(#{g})"/>')


def orb_fill(op=0.6):
    """Radial violet fill for the hero bubble / node (token colours only)."""
    g = gid("orb")
    DEFS.append(f'<radialGradient id="{g}" cx="0.38" cy="0.32" r="0.75">'
                f'<stop offset="0" stop-color="{VIOLET}" stop-opacity="{op:.3f}"/>'
                f'<stop offset="0.55" stop-color="{ACCENT}" stop-opacity="{op * 0.55:.3f}"/>'
                f'<stop offset="1" stop-color="{INDIGO}" stop-opacity="{op * 0.25:.3f}"/></radialGradient>')
    return f"url(#{g})"


def dotgrid(cx, cy, r, step=24):
    """Faint Vercel-style dot grid (rule2), faded out radially."""
    pid, mid, fid = gid("dots"), gid("dmask"), gid("dfade")
    DEFS.append(f'<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse" '
                f'x="{MARGIN % step}" y="{MARGIN % step}"><circle cx="1.5" cy="1.5" r="1.5" fill="{RULE2}"/></pattern>')
    DEFS.append(f'<radialGradient id="{fid}" cx="0.5" cy="0.5" r="0.5">'
                f'<stop offset="0" stop-color="{BONE}" stop-opacity="1"/>'
                f'<stop offset="0.6" stop-color="{BONE}" stop-opacity="0.6"/>'
                f'<stop offset="1" stop-color="{BONE}" stop-opacity="0"/></radialGradient>')
    DEFS.append(f'<mask id="{mid}"><rect x="{cx - r:.0f}" y="{cy - r:.0f}" width="{2 * r:.0f}" height="{2 * r:.0f}" '
                f'fill="url(#{fid})"/></mask>')
    return (f'<rect x="{cx - r:.0f}" y="{cy - r:.0f}" width="{2 * r:.0f}" height="{2 * r:.0f}" fill="url(#{pid})" '
            f'mask="url(#{mid})"/>')


def spectrum(x, y, w, h=4):
    g = gid("spec")
    DEFS.append(f'<linearGradient id="{g}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{INDIGO}"/>'
                f'<stop offset="0.5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{AMBER}"/></linearGradient>')
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="url(#{g})"/>'


def line(x1, y1, x2, y2, col=RULE, sw=1, extra=""):
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{sw}"{extra}/>')


def mlabel(x, y, s, fill=MUTE, anchor="start", fs=16, tag=None, wt=500):
    return T(x, y, s, fs, "mono", wt, fill, anchor, ls=1.2, tag=tag)


def header(eyebrow, title, subtitle=None):
    out = [mlabel(MARGIN, 64, eyebrow, MUTE, tag="eyebrow"),
           T(MARGIN - 3, 124, title, 52, "head", 600, BONE, ls=-1.8, tag="title")]
    if subtitle:
        out.append(T(MARGIN, 158, subtitle, 19, "sans", 400, MUTE, tag="subtitle"))
    return "\n".join(out)


def lf_mark(x=36, y=1105, width=72):
    height = width * 144 / 154
    return (f'<image href="{MARK}" xlink:href="{MARK}" x="{x}" y="{y}" width="{width}" '
            f'height="{height:.1f}" preserveAspectRatio="xMidYMid meet"/>')


SRC_X = 132                     # source text beside the LF mark
SRC_R = 1058                    # stop short of the Spark logo


def sources(text, fs=15, lh=21):
    """Compact mono source footer: up to 3 lines beside the LF mark, any earlier text above it at full width."""
    def wrap(words, width):
        lines, cur = [], []
        for w_ in words:
            trial = " ".join(cur + [w_])
            if tw(trial, "mono", fs, 400) <= width or not cur:
                cur.append(w_)
            else:
                lines.append(" ".join(cur))
                cur = [w_]
        if cur:
            lines.append(" ".join(cur))
        return lines
    text = text.replace(" \u00b7 ", "\u00a0\u00b7 ")     # keep each separator with the item before it
    words = text.split(" ")
    narrow = wrap(words, SRC_R - SRC_X)
    beside = narrow
    head_words = len(narrow) > 3
    # rebalance: fill full-width lines from the front, keep the remainder beside the mark
    above = []
    if head_words:
        # simple approach: take full-width lines until remaining text fits in 3 narrow lines
        all_words = words
        above = []
        i = 0
        while True:
            rem = wrap(all_words[i:], SRC_R - SRC_X)
            if len(rem) <= 3:
                beside = rem
                break
            nxt = wrap(all_words[i:], W - 2 * MARGIN)[0]
            above.append(nxt)
            i += len(nxt.split(" "))
    out = [lf_mark()]
    yb0 = 1162 - (len(beside) - 1) * lh
    for k, ln in enumerate(beside):
        out.append(T(SRC_X, yb0 + k * lh, ln, fs, "mono", 400, MUTE, tag=f"src-b{k}"))
    ya_last = min(yb0, 1120) - lh if beside else 1162
    ya_last = min(ya_last, 1094)
    for k, ln in enumerate(above):
        out.append(T(MARGIN, ya_last - (len(above) - 1 - k) * lh, ln, fs, "mono", 400, MUTE, tag=f"src-a{k}"))
    top = (ya_last - (len(above) - 1) * lh) if above else yb0
    return "\n".join(out), top - fs


def source_line(text, fs=12):
    """One quiet mono source line, centred on the LF mark row, clear of the mark and the Spark logo."""
    y = LOGO_BR_CY + fs * 0.35
    x_max = min(b[1] for b in LOGO_BOXES if b[0].startswith("logo-spark")) - 16 if LOGO_BOXES else SRC_R
    if SRC_X + tw(text, "mono", fs, 400) > x_max:
        WARN.append(f"source line too long ({tw(text, 'mono', fs, 400):.0f}px)")
    return lf_mark() + "\n" + T(SRC_X, y, text, fs, "mono", 400, MUTE, tag="src-line")


def wrap_svg(inner):
    defs = "\n    ".join(DEFS)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="1200" height="1200" viewBox="0 0 1200 1200">
  <defs>
    {defs}
  </defs>
  <rect width="1200" height="1200" fill="{PITCH}"/>
{inner}
</svg>
'''


def start_page():
    TEXT_BOXES.clear()
    LOGO_BOXES.clear()
    DEFS.clear()


def check_layout(name, allow_overlap=()):
    def hit(a, b, m=0):
        return not (a[3] + m <= b[1] or b[3] + m <= a[1] or a[4] + m <= b[2] or b[4] + m <= a[2])
    lf = ("lf-mark",) + LF_BOX
    errs = []
    for i, a in enumerate(TEXT_BOXES):
        if a[1] < 16 or a[3] > W - MARGIN + 4 or a[2] < 0 or a[4] > H:
            errs.append(f"off-canvas {a}")
        for f in [lf] + LOGO_BOXES:
            if hit(a, f, 6):
                errs.append(f"{a[0]!r} hits {f[0]}")
        for b in TEXT_BOXES[i + 1:]:
            if hit(a, b, 1) and (a[0], b[0]) not in allow_overlap:
                errs.append(f"text overlap {a[0]!r} / {b[0]!r}")
    if errs:
        raise SystemExit(f"{name}: layout errors:\n  " + "\n  ".join(errs))


TOKEN_STOPS = {c.upper() for c in (VIOLET, ACCENT, INDIGO, BONE)}


def check_bad(svg, name):
    for ch in ("\u2014", "\u2013"):
        if ch in svg:
            raise SystemExit(f"dash found in {name}: {ch!r}")
    for hx in re.findall(r"#[0-9A-Fa-f]{6}\b", svg):
        if hx.upper() not in ALLOWED_HEX:
            raise SystemExit(f"off-token colour in {name}: {hx}")
    for m in re.findall(r"rgba\(([^)]*)\)", svg):
        rgb = tuple(int(float(v)) for v in m.split(",")[:3])
        if rgb not in {(243, 243, 241), (168, 85, 247), (5, 1, 14)}:
            raise SystemExit(f"off-token rgba in {name}: {m}")
    # radial gradients: glow/orb/fade only, built from token colours
    for body in re.findall(r"<radialGradient.*?</radialGradient>", svg, re.S):
        for c in re.findall(r'stop-color="([^"]+)"', body):
            if c.upper() not in TOKEN_STOPS:
                raise SystemExit(f"radial gradient with non-token stop in {name}: {c}")
    # linear gradients: only --spectrum (indigo, violet, amber), at most one
    lins = re.findall(r"<linearGradient.*?</linearGradient>", svg, re.S)
    if len(lins) > 1:
        raise SystemExit(f"more than one linear gradient in {name}")
    for body in lins:
        if [c.upper() for c in re.findall(r'stop-color="([^"]+)"', body)] != [INDIGO, VIOLET, AMBER]:
            raise SystemExit(f"non-spectrum linear gradient in {name}")
    for bad in ("filter=", "<filter", "feGaussian", "drop-shadow"):
        if bad in svg:
            raise SystemExit(f"filter/shadow found in {name}: {bad}")


EYEBROW_PANEL = "SPARK FESTIVAL  \u00b7  SOVEREIGN AI PANEL  \u00b7  SYDNEY"


# ================================================================ graphic 1: gdg-stats

def gen_stats():
    start_page()
    p = []
    # ---- hero: bubble cluster, circle AREA proportional to A$
    R = 280.0
    r = lambda v: R * math.sqrt(v / 20000.0)
    rA, rO, rM, rS = R, r(7000), r(5000), r(29.9)
    ax, ay = MARGIN + 26 + rA, 492
    gap = 14
    t1 = math.radians(-17)
    ox, oy = ax + (rA + rO + gap) * math.cos(t1), ay + (rA + rO + gap) * math.sin(t1)
    # Microsoft: touches both, below the OpenAI bubble
    d1, d2 = rA + rM + gap, rO + rM + gap
    dx, dy = ox - ax, oy - ay
    d = math.hypot(dx, dy)
    a_ = (d1 ** 2 - d2 ** 2 + d ** 2) / (2 * d)
    h_ = math.sqrt(max(d1 ** 2 - a_ ** 2, 0))
    px_, py_ = ax + a_ * dx / d, ay + a_ * dy / d
    mx, my = px_ - h_ * dy / d, py_ + h_ * dx / d
    if my < oy:
        mx, my = px_ + h_ * dy / d, py_ - h_ * dx / d
    p.append(dotgrid(560, ay, 580))
    p.append(glow(ax, ay, rA * 1.9, 0.34))
    p.append(f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="{rA:.1f}" fill="{orb_fill(0.62)}" stroke="{VIOLET}" stroke-width="2"/>')
    for cx, cy, rr in ((ox, oy, rO), (mx, my, rM)):
        p.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rr:.1f}" fill="rgba(243,243,241,.045)" '
                 f'stroke="rgba(243,243,241,.42)" stroke-width="1.5"/>')
    # labels inside
    p.append(hero(ax, ay + 20, "A$20B", 132, BONE, anchor="middle", wt=600, tag="aws-n"))
    p.append(T(ax, ay + 76, "AWS, 2025 to 2029", 24, "sans", 500, BONE, "middle", tag="aws-w"))
    p.append(hero(ox, oy + 14, "A$7B", 68, BONE, anchor="middle", wt=600, tag="oai-n"))
    p.append(T(ox, oy + 50, "OpenAI + NEXTDC", 20, "sans", 500, SUB, "middle", tag="oai-w"))
    p.append(hero(mx, my + 12, "A$5B", 60, BONE, anchor="middle", wt=600, tag="ms-n"))
    p.append(T(mx, my + 46, "Microsoft", 20, "sans", 500, SUB, "middle", tag="ms-w"))
    # A$29.9M dot, true scale, with hairline callout
    sx = max(ox + rO, mx + rM) + 56
    sy = (oy + rO + my - rM) / 2 + 8
    p.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{rS:.2f}" fill="{BONE}"/>')
    cyl = sy + 110
    p.append(line(sx, sy + rS + 6, sx, cyl - 38, "rgba(243,243,241,.5)", 1))
    lx, anc = sx, "start"
    if sx + tw("AI Safety Institute", "sans", 19, 500) > W - MARGIN:
        lx, anc = W - MARGIN, "end"
    p.append(hero(lx - 2 if anc == "start" else lx, cyl, "A$29.9M", 38, BONE, wt=600, anchor=anc, tag="aisi-n"))
    p.append(T(lx, cyl + 28, "AI Safety Institute", 19, "sans", 500, SUB, anc, tag="aisi-w"))
    p.append(T(lx, cyl + 52, "same scale", 16, "mono", 400, MUTE, anc, tag="aisi-s"))
    p.append(mlabel(W - MARGIN, 186, "CIRCLE AREA TO SCALE", MUTE, "end", tag="scale"))
    hero_bot = max(ay + rA, my + rM, cyl + 52)
    # ---- supporting row: 79% / 70%
    y1 = hero_bot + 32
    p.append(line(MARGIN, y1, W - MARGIN, y1))
    nb = y1 + 28 + 0.72 * 76
    for i, (num, a, b) in enumerate((("79%", "of Australian businesses say keeping", "AI data in Australia matters"),
                                     ("70%", "would pay more for AI hosted", "entirely in Australia"))):
        x = MARGIN + i * 576
        p.append(hero(x - 3, nb, num, 76, VIOLET if i == 0 else BONE, wt=600, tag=f"pct-{num}"))
        tx = x + hero_w(num, 76, 600) + 22
        p.append(T(tx, nb - 30, a, 20, "sans", 500, BONE, tag=f"pa-{num}"))
        p.append(T(tx, nb - 3, b, 20, "sans", 500, BONE, tag=f"pb-{num}"))
    # ---- dated strip
    y2 = nb + 40
    p.append(line(MARGIN, y2, W - MARGIN, y2))
    cw = (W - 2 * MARGIN - 2 * 32) / 3
    items = [("19 days", "Claude Fable 5 offline worldwide under a US export directive"),
             ("84 days", "for OpenAI to tell government its agent accessed a Medicare portal"),
             ("10 Dec 2026", "Privacy Act automated-decision rules begin")]
    last = 0
    for i, (num, body) in enumerate(items):
        x = MARGIN + i * (cw + 32)
        if i:
            p.append(line(x - 16, y2 + 22, x - 16, y2 + 118))
        b = y2 + 24 + 0.72 * 34
        p.append(hero(x - 1, b, num, 34, BONE, wt=600, tag=f"d-{i}"))
        s_, l_ = para(x, b + 30, body, cw, 18, 23, fill=SUB, tag=f"db-{i}")
        p.append(s_)
        last = max(last, l_)
    corner = corner_logos()          # registers logo boxes for source_line
    p.append(source_line("Sources: Amazon, NEXTDC, Microsoft, National AI Plan, Decidr, Anthropic, ABC, OAIC"))
    STATS_BOTTOM[0] = last
    if last + 5 > 1105 - 24:
        WARN.append(f"strip {last:.0f} runs into the footer row")
    parts = [header(EYEBROW_PANEL, "Sovereign AI in Australia, by the numbers")] + p + [corner]
    check_layout("gdg-stats")
    return wrap_svg("\n".join(parts))


STATS_BOTTOM = [0]


# ================================================================ graphic 2: gdg-sovereignty

def gen_sovereignty():
    start_page()
    p = []
    # quote as headline-scale hero
    p.append(T(MARGIN - 4, 222, "\u201cSovereignty = leverage,", 58, "head", 600, BONE, ls=-1.8, tag="q1"))
    p.append(T(MARGIN + 20, 286, "not just choice\u201d", 58, "head", 600, BONE, ls=-1.8, tag="q2"))
    p.append(mlabel(MARGIN + 20 + tw("not just choice\u201d", "head", 58, 600, -1.8) + 24, 284,
                    "RAYMOND SUN, HSF KRAMER", MUTE, tag="q-attr"))
    # stool
    seat_y, seat_h = 350, 20
    cxs = [150, 375, 600, 825, 1050]
    legs = [("Model", None, 92), ("Data", "LOCALISATION", 92), ("Policy", "TRUE SOVEREIGNTY", 176),
            ("Inference", "LOCALISATION", 92), ("Intellectual", "ADDED 5TH LEG", 92)]
    bot_n, bot_p = 700, 752
    p.append(dotgrid(600, 560, 520))
    p.append(glow(600, 560, 420, 0.42, sy=0.95))
    p.append(f'<rect x="{MARGIN + 54}" y="{seat_y}" width="{W - 2 * MARGIN - 108}" height="{seat_h}" rx="10" '
             f'fill="{BONE}"/>')
    for (name, tag, w_), cx in zip(legs, cxs):
        core = name == "Policy"
        added = name == "Intellectual"
        top = seat_y + seat_h + 10
        bot = bot_p if core else bot_n
        if core:
            p.append(f'<rect x="{cx - w_ / 2:.1f}" y="{top}" width="{w_}" height="{bot - top}" rx="12" '
                     f'fill="{orb_fill(0.9)}" stroke="{VIOLET}" stroke-width="2"/>')
        else:
            dash = ' stroke-dasharray="7 6"' if added else ""
            p.append(f'<rect x="{cx - w_ / 2:.1f}" y="{top}" width="{w_}" height="{bot - top}" rx="12" '
                     f'fill="rgba(243,243,241,.05)" stroke="rgba(243,243,241,.42)" stroke-width="1.5"{dash}/>')
        nb = bot + 46
        p.append(T(cx, nb, name, 34 if core else 26, "head", 600, BONE, "middle", ls=-0.6, tag=f"leg-{name}"))
        if tag:
            p.append(mlabel(cx, nb + 30, tag, VIOLET if core else MUTE, "middle", fs=18, tag=f"legt-{name}",
                            wt=600 if core else 500))
    ay = bot_p + 46 + 30 + 52
    p.append(T(MARGIN, ay, "Four legs: David Brudenell, Decidr. Fifth: Raymond Sun.", 18, "sans", 400, SUB,
               tag="attr"))
    # spectrum
    sy = ay + 84
    p.append(line(MARGIN, ay + 26, W - MARGIN, ay + 26))
    x0, x1 = MARGIN + 6, W - MARGIN - 6
    au = (x0 + x1) / 2
    p.append(spectrum(x0, sy - 2, x1 - x0, 4))
    for x, col, rr in ((x0, INDIGO, 7), (x1, AMBER, 7)):
        p.append(f'<circle cx="{x:.1f}" cy="{sy}" r="{rr}" fill="{col}" stroke="{PITCH}" stroke-width="3"/>')
    p.append(glow(au, sy, 70, 0.6))
    p.append(f'<circle cx="{au:.1f}" cy="{sy}" r="12" fill="{VIOLET}" stroke="{BONE}" stroke-width="2.5"/>')
    p.append(T(x0 - 6, sy - 20, "EU", 20, "mono", 700, BONE, tag="eu"))
    p.append(mlabel(x0 - 6 + 38, sy - 20, "hygiene factor", MUTE, tag="eu-q"))
    p.append(T(x1 + 6, sy - 20, "US", 20, "mono", 700, BONE, "end", tag="us"))
    p.append(mlabel(x1 + 6 - 38, sy - 20, "Wild West", MUTE, "end", tag="us-q"))
    p.append(T(au - 18, sy - 22, "AU", 20, "mono", 700, BONE, "end", tag="au"))
    p.append(T(au + 18, sy - 22, "ethical middle ground", 20, "sans", 600, BONE, tag="au-q"))
    p.append(mlabel(au, sy + 36, "WHERE AUSTRALIA SITS  \u00b7  LAURA HEIDRICH, GOOGLE CLOUD", MUTE, "middle", fs=15,
                    tag="geo-attr"))
    # rule of three, one line
    ry = sy + 96
    p.append(line(MARGIN, ry - 34, W - MARGIN, ry - 34))
    r3 = "Know where your data goes  \u00b7  Know who can be compelled  \u00b7  Prove it"
    p.append(T(MARGIN, ry, r3, 21, "sans", 500, BONE, tag="r3"))
    p.append(mlabel(W - MARGIN, ry, "RAMESH HEIDARY, GOOGLE CLOUD", MUTE, "end", fs=15, tag="r3-attr"))
    s_, top = sources("Paraphrased from notes taken at the Sovereign AI panel, Spark Festival, 24 Sep 2026", 16)
    p.append(s_)
    if ry + 20 > top:
        WARN.append(f"rule of three {ry} runs into sources {top}")
    parts = [header(EYEBROW_PANEL, "AI sovereignty is leverage")] + p + [corner_logos()]
    check_layout("gdg-sovereignty")
    return wrap_svg("\n".join(parts))


# ================================================================ graphic 3: gdg-antigravity

def _icon_wrap(cx, cy, r=34):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="rgba(243,243,241,.05)" '
            f'stroke="rgba(243,243,241,.2)" stroke-width="1.2"/>')


def icon(kind, cx, cy):
    s0 = f'fill="none" stroke="{BONE}" stroke-linecap="round" stroke-linejoin="round"'
    s = s0 + ' stroke-width="2.2"'
    out = [_icon_wrap(cx, cy)]
    if kind == "grill":          # speech bubble with question mark
        out.append(f'<path d="M {cx - 17} {cy - 13} h 34 a 5 5 0 0 1 5 5 v 16 a 5 5 0 0 1 -5 5 h -16 l -9 8 v -8 '
                   f'h -9 a 5 5 0 0 1 -5 -5 v -16 a 5 5 0 0 1 5 -5 z" {s}/>')
        out.append(f'<path d="M {cx - 4.5} {cy - 4} a 4.5 4.5 0 1 1 6 4.2 c -1.4 .6 -1.5 1.4 -1.5 2.8" {s0} stroke-width="2"/>')
        out.append(f'<circle cx="{cx:.1f}" cy="{cy + 8.5:.1f}" r="1.4" fill="{BONE}"/>')
    elif kind == "goal":         # target
        out.append(f'<circle cx="{cx}" cy="{cy}" r="17" {s}/><circle cx="{cx}" cy="{cy}" r="9.5" {s}/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="3.2" fill="{BONE}"/>')
    elif kind == "sub":          # one agent fanning out to three
        out.append(f'<path d="M {cx} {cy - 10} V {cy - 2} M {cx} {cy - 2} C {cx} {cy + 4} {cx - 14} {cy + 2} {cx - 14} {cy + 10} '
                   f'M {cx} {cy - 2} V {cy + 10} M {cx} {cy - 2} C {cx} {cy + 4} {cx + 14} {cy + 2} {cx + 14} {cy + 10}" {s}/>')
        out.append(f'<circle cx="{cx}" cy="{cy - 14}" r="5" fill="{BONE}"/>')
        for dx in (-14, 0, 14):
            out.append(f'<circle cx="{cx + dx}" cy="{cy + 14}" r="4" {s0} stroke-width="2"/>')
    elif kind == "clock":
        out.append(f'<circle cx="{cx}" cy="{cy}" r="17" {s}/><path d="M {cx} {cy - 9} V {cy} L {cx + 7} {cy + 5}" {s}/>')
    return "\n".join(out)


def tile(x, y, w, h, fill="rgba(243,243,241,.035)", stroke="rgba(243,243,241,.14)"):
    return (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="24" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="1.2"/>')


def gen_antigravity():
    """v3: one big worktree fork, four plain chips, red security line, one source line."""
    start_page()
    p = []
    # ---- caption
    cap_y = 262
    p.append(mlabel(MARGIN, cap_y - 52, "NEW IN 2.0", VIOLET, tag="new", wt=600))
    p.append(T(MARGIN - 2, cap_y, "Native Git worktrees", 44, "head", 600, BONE, ls=-1.2, tag="cap"))
    # ---- hero: git graph. main branch, fork commit, three parallel worktree lanes, best lane merges back
    ym = 396
    lanes = [("a", "No skill", 516), ("b", "/grill-me", 626), ("c", "/interview-me", 736)]
    WIN = "b"                      # unsourced: notes don't say which approach was kept (see report)
    fx, mx_ = 236, 1080            # fork commit, merge commit
    x_end = 950                    # where discarded lanes stop
    commits = (668, 768, 868)
    MAINC, LANEC = "rgba(243,243,241,.5)", "rgba(243,243,241,.62)"
    p.append(dotgrid(620, 566, 560))
    p.append(glow(mx_, ym + 40, 360, 0.5, sy=0.9))
    p.append(glow(560, 626, 520, 0.1, sy=0.5))
    st = 'fill="none" stroke-linecap="round" stroke-linejoin="round"'
    # main branch
    p.append(f'<path d="M {MARGIN + 20} {ym} L {W - MARGIN - 16} {ym}" stroke="{MAINC}" stroke-width="3" {st}/>')
    for x in (96, 166):
        p.append(f'<circle cx="{x}" cy="{ym}" r="7" fill="{PITCH}" stroke="{BONE}" stroke-width="2.5"/>')
    p.append(T(MARGIN + 20, ym - 26, "main", 16, "mono", 500, MUTE, ls=1.0, tag="main"))
    p.append(T(fx - 14, ym - 26, "one repo, same prompt", 20, "mono", 600, BONE, tag="fork-l"))
    # lanes
    for k, name, ly in lanes:
        win = k == WIN
        col = VIOLET if win else LANEC
        p.append(f'<path d="M {fx} {ym} L {fx} {ly - 34} Q {fx} {ly} {fx + 34} {ly} L {x_end} {ly}" stroke="{col}" '
                 f'stroke-width="3" {st}/>')
        for x in commits:
            p.append(f'<circle cx="{x}" cy="{ly}" r="7" fill="{PITCH}" stroke="{VIOLET if win else BONE}" '
                     f'stroke-width="2.5"/>')
        lx = fx + 64
        wt_ = f"worktree {k}"
        p.append(T(lx, ly - 16, wt_, 20, "mono", 500, MUTE, tag=f"wt-{k}"))
        x2 = lx + tw(wt_, "mono", 20, 500) + 10
        p.append(T(x2, ly - 16, "\u00b7", 20, "mono", 500, MUTE, tag=f"wd-{k}"))
        x3 = x2 + tw("\u00b7", "mono", 20, 500) + 10
        kind = "mono" if name.startswith("/") else "sans"
        p.append(T(x3, ly - 16, name, 22, kind, 600, BONE, tag=f"wn-{k}"))
        if k == "a":
            xf = x3 + tw(name, kind, 22, 600) + 18
            if xf + tw("fastest", "mono", 16, 500, 1.0) < commits[0] - 14:
                p.append(T(xf, ly - 16, "fastest", 16, "mono", 500, MUTE, ls=1.0, tag="fast"))
            else:
                WARN.append("fastest dropped (no room)")
        if win:
            p.append(f'<path d="M {x_end} {ly} L {mx_ - 40} {ly} Q {mx_} {ly} {mx_} {ly - 40} L {mx_} {ym + 30}" '
                     f'stroke="{VIOLET}" stroke-width="3" {st}/>')
        else:
            p.append(f'<rect x="{x_end + 2}" y="{ly - 9}" width="18" height="18" rx="3" fill="{PITCH}" '
                     f'stroke="{MUTE}" stroke-width="2"/>')
            p.append(T(x_end + 34, ly + 6, "discarded", 16, "mono", 500, MUTE, ls=1.0, tag=f"disc-{k}"))
    # fork + merge commits
    p.append(f'<circle cx="{fx}" cy="{ym}" r="13" fill="{BONE}"/>')
    p.append(f'<circle cx="{mx_}" cy="{ym}" r="24" fill="{orb_fill(1.0)}" stroke="{VIOLET}" stroke-width="2.5"/>')
    p.append(f'<circle cx="{mx_}" cy="{ym}" r="8" fill="{BONE}"/>')
    p.append(T(W - MARGIN, ym - 40, "keep the best", 22, "mono", 600, BONE, "end", tag="keep"))
    p.append(T(fx + 64, lanes[-1][2] + 52, "running in parallel", 18, "mono", 500, MUTE, ls=1.0, tag="par"))
    # ---- chips
    chip_y = 896
    names = ["/grill-me", "/goal", "Subagents", "Scheduled tasks"]
    gap = 16
    cw = (W - 2 * MARGIN - 3 * gap) / 4
    for i, c in enumerate(names):
        x = MARGIN + i * (cw + gap)
        p.append(f'<rect x="{x:.1f}" y="{chip_y - 34}" width="{cw:.1f}" height="68" rx="34" '
                 f'fill="rgba(243,243,241,.04)" stroke="rgba(243,243,241,.24)" stroke-width="1.2"/>')
        kind = "mono" if c.startswith("/") else "sans"
        p.append(T(x + cw / 2, chip_y + 8, c, 24, kind, 500, BONE, "middle", tag=f"chip-{i}"))
    # ---- security
    sy2 = 1012
    p.append(f'<rect x="{MARGIN}" y="{sy2 - 15}" width="40" height="3" fill="{RED}"/>')
    p.append(mlabel(MARGIN + 54, sy2 - 6, "SECURITY", RED, tag="sec", wt=700))
    p.append(T(MARGIN + 54 + tw("SECURITY", "mono", 16, 700, 1.2) + 18, sy2 - 6, "Only install skills you trust.",
               22, "sans", 500, BONE, tag="sec-t"))
    corner = corner_logos()
    p.append(source_line("Sources: Brett Morgan workshop, Google Sydney, 24 Sep 2026 \u00b7 antigravity.google "
                         "\u00b7 Sundar Pichai"))
    parts = [header("SPARK FESTIVAL  \u00b7  AGENT SKILLS WORKSHOP  \u00b7  SYDNEY",
                    "What's new in Antigravity 2.0")] + p + [corner]
    check_layout("gdg-antigravity")
    return wrap_svg("\n".join(parts))


# ================================================================ graphic 4: gdg-sovereignty-detail
# Default content = wording supported by event-notes.md / research.md only.
# BRIEFED = the fuller wording from the brief (not all of it is in the project notes); rendered to /tmp only.

DETAIL_NOTES = dict(
    quote="\u201cSovereignty = leverage\u201d",
    legs=[("Model", "model bias and national values", None),
          ("Data", None, None),
          ("Policy", None, None),
          ("Inference", None, None),
          ("Intellectual", "intellectual sovereignty", "5TH LEG")],
    stool="A four-legged stool (policy, model, data, inference), plus a fifth leg: intellectual sovereignty",
    credit=None,
    r3_label="VISIBILITY RULE OF THREE",
    r3=["Where data goes", "Who can be compelled", "Prove it"],
    geo=[("EU", "Hygiene"), ("AU", "Ethical middle ground"), None],
    also=("Also discussed: feature vs market \u00b7 utility vs commodity \u00b7 market exit risk is a negotiating "
          "tactic \u00b7 export controls underrated"),
)
DETAIL_BRIEFED = dict(
    quote="\u201cSovereignty = leverage, not just choice\u201d",
    legs=[("Model", "who builds it, and whose values it carries", None),
          ("Data", "where it is stored and processed", "MOSTLY LOCALISATION"),
          ("Policy", "who sets and enforces the rules", "TRUE SOVEREIGNTY"),
          ("Inference", "where the model runs", "MOSTLY LOCALISATION"),
          ("Intellectual", "domain know-how that can't be scraped", "5TH LEG, ADDED BY RAYMOND SUN")],
    stool=None,
    credit=("Four legs: David Brudenell, Decidr. Raymond Sun: data, compute and inference are mostly localisation; "
            "true sovereignty is policy."),
    r3_label="RULE OF THREE",
    r3=["Know where your data goes, including prompts and metadata",
        "Know who can be legally compelled to hand it over", "Be able to prove it"],
    geo=[("EU", "A hygiene factor"), ("AU", "The ethical middle ground"), ("US", "The Wild West")],
    also=None,
)


def gen_sov_detail(C=None, pad=None):
    """Two-pass: first pass measures free space, second distributes it (legs + section gaps)."""
    C = C or DETAIL_NOTES
    if pad is None:
        _sov_detail(C, 0)
        return _sov_detail(C, max(FREE[0] - 34, 0))
    return _sov_detail(C, pad)


def _sov_detail(C, pad):
    leg_x = pad * 0.5
    gap_x = pad * 0.5 / (3 if C["also"] else 2)
    start_page()
    p = []
    BODY = 22
    # ---- quote
    qfs = 54 if len(C["quote"]) < 30 else 44
    qb = 214
    p.append(T(MARGIN - 3, qb, C["quote"], qfs, "head", 600, BONE, ls=-1.4, tag="q"))
    p.append(T(W - MARGIN, qb, "Raymond Sun, HSF Kramer", BODY, "sans", 500, SUB, "end", tag="q-attr"))
    if tw(C["quote"], "head", qfs, 600, -1.4) + tw("Raymond Sun, HSF Kramer", "sans", BODY, 500) + 40 > W - 2 * MARGIN:
        WARN.append("quote and attribution collide")
    # ---- stool: seat + five short legs + text columns
    seat = 262
    p.append(glow(600, 340 + leg_x / 2, 360 + leg_x, 0.42, sy=0.6))
    p.append(f'<rect x="{MARGIN}" y="{seat}" width="{W - 2 * MARGIN}" height="14" rx="7" fill="{BONE}"/>')
    gap = 24
    cw = (W - 2 * MARGIN - 4 * gap) / 5
    last = 0
    for i, (name, desc, tag) in enumerate(C["legs"]):
        x = MARGIN + i * (cw + gap)
        core, added = name == "Policy", name == "Intellectual"
        lt, lb = seat + 14 + 8, seat + 14 + 8 + (92 if core else 64) + leg_x
        lw = 84 if core else 40
        lx = x + 18
        if core:
            p.append(f'<rect x="{lx}" y="{lt}" width="{lw}" height="{lb - lt}" rx="10" fill="{orb_fill(0.95)}" '
                     f'stroke="{VIOLET}" stroke-width="2"/>')
        else:
            dash = ' stroke-dasharray="6 5"' if added else ""
            p.append(f'<rect x="{lx}" y="{lt}" width="{lw}" height="{lb - lt}" rx="10" fill="rgba(243,243,241,.05)" '
                     f'stroke="rgba(243,243,241,.45)" stroke-width="1.5"{dash}/>')
        nb = seat + 14 + 8 + 92 + leg_x + 50
        p.append(T(x, nb, name, 32 if core else 30, "head", 600, VIOLET if core else BONE, ls=-0.6, tag=f"leg-{name}"))
        yy = nb
        if desc:
            s_, yy = para(x, nb + 34, desc, cw, BODY, 28, fill=SUB, tag=f"legd-{name}")
            p.append(s_)
        if tag:
            for k, ln in enumerate(wrap_px(tag, cw, "mono", 16, 600)):
                yy += 30 if k == 0 else 21
                p.append(T(x, yy, ln, 16, "mono", 600, VIOLET if core else MUTE, ls=1.0, tag=f"legt-{name}{k}"))
        last = max(last, yy)
    yy = last + 44
    for key in ("stool", "credit"):
        if C[key]:
            s_, yy = para(MARGIN, yy, C[key], W - 2 * MARGIN, BODY, 29, fill=BONE if key == "stool" else SUB,
                          tag=f"s-{key}")
            p.append(s_)
            yy += 32
    # ---- rule of three
    y3 = yy + 6 + gap_x
    p.append(line(MARGIN, y3, W - MARGIN, y3))
    p.append(mlabel(MARGIN, y3 + 40, f"{C['r3_label']}  \u00b7  RAMESH HEIDARY, GOOGLE CLOUD", MUTE, tag="r3-l"))
    cw3 = (W - 2 * MARGIN - 2 * 32) / 3
    last = 0
    for i, t in enumerate(C["r3"]):
        x = MARGIN + i * (cw3 + 32)
        nb = y3 + 72 + 0.72 * 56
        p.append(hero(x - 2, nb, str(i + 1), 56, VIOLET, wt=600, tag=f"r3n-{i}"))
        tx = x + 52
        s_, l_ = para(tx, nb - 30 if len(wrap_px(t, cw3 - 52, "sans", 24, 500)) > 1 else nb - 8, t, cw3 - 52, 24, 30,
                      wt=500, fill=BONE, tag=f"r3t-{i}")
        p.append(s_)
        last = max(last, l_, nb)
    # ---- spectrum (Laura Heidrich)
    yg = last + 40 + gap_x
    p.append(line(MARGIN, yg, W - MARGIN, yg))
    p.append(mlabel(MARGIN, yg + 40, "WHERE AUSTRALIA SITS  \u00b7  LAURA HEIDRICH, GOOGLE CLOUD", MUTE, tag="geo-l"))
    by = yg + 92
    x0, x1 = MARGIN + 8, W - MARGIN - 8
    au = (x0 + x1) / 2
    has_us = C["geo"][2] is not None
    p.append(line(x0, by, x1, by, "rgba(243,243,241,.35)", 2))
    pts = [(x0, C["geo"][0], "start"), (au, C["geo"][1], "middle")] + ([(x1, C["geo"][2], "end")] if has_us else [])
    p.append(glow(au, by, 90, 0.6))
    for x, (code, q), anc in pts:
        is_au = code == "AU"
        p.append(f'<circle cx="{x:.1f}" cy="{by}" r="{12 if is_au else 8}" fill="{VIOLET if is_au else BONE}"'
                 f'{f" stroke={chr(34)}{BONE}{chr(34)} stroke-width={chr(34)}2.5{chr(34)}" if is_au else ""}/>')
        lx = x - 8 if anc == "start" else (x + 8 if anc == "end" else x)
        p.append(T(lx, by - 22, code, 22, "mono", 700, BONE, anc, tag=f"geo-{code}"))
        p.append(T(lx, by + 48, f"\u201c{q}\u201d", 26 if is_au else 24, "head", 600 if is_au else 500, BONE, anc,
                   italic=True, tag=f"geo-q-{code}"))
    yy = by + 48
    if C["also"]:
        ya = yy + 56 + gap_x
        p.append(line(MARGIN, ya - 34, W - MARGIN, ya - 34))
        s_, yy = para(MARGIN, ya, C["also"], W - 2 * MARGIN, BODY, 29, fill=SUB, tag="also")
        p.append(s_)
    if yy + 8 > 1105 - 10:
        WARN.append(f"detail content {yy:.0f} runs into footer")
    FREE[0] = 1105 - yy
    corner = corner_logos()
    p.append(lf_mark())
    p.append(T(SRC_X, LOGO_BR_CY + 6, "Paraphrased from notes taken at the Sovereign AI panel, Spark Festival, 24 Sep 2026",
               16, "mono", 400, MUTE, tag="foot"))
    parts = [header(EYEBROW_PANEL, "AI sovereignty, in detail")] + p + [corner]
    check_layout("gdg-sovereignty-detail")
    return wrap_svg("\n".join(parts))


FREE = [0]


def gen_sov_detail_v3():
    """v3: quote, five equal legs, rule of three, two-point spectrum. Notes wording only."""
    start_page()
    p = []
    # ---- quote
    p.append(glow(330, 262, 420, 0.22, sy=0.55))
    p.append(T(MARGIN - 4, 270, "\u201cSovereignty = leverage\u201d", 66, "head", 600, BONE, ls=-1.8, tag="q"))
    p.append(T(MARGIN, 316, "Raymond Sun, HSF Kramer", 22, "sans", 500, SUB, tag="q-attr"))
    # ---- section 1: five equal legs
    seat = 398
    p.append(f'<rect x="{MARGIN}" y="{seat}" width="{W - 2 * MARGIN}" height="10" rx="5" fill="{BONE}" '
             f'fill-opacity=".9"/>')
    names = ["Model", "Data", "Policy", "Inference", "Intellectual"]
    cw = (W - 2 * MARGIN) / 5
    top, bot = seat + 10 + 8, seat + 10 + 8 + 128
    for i, n in enumerate(names):
        cx = MARGIN + cw * (i + 0.5)
        dash = ' stroke-dasharray="7 6"' if n == "Intellectual" else ""
        p.append(f'<rect x="{cx - 26:.1f}" y="{top}" width="52" height="{bot - top}" rx="10" '
                 f'fill="rgba(243,243,241,.05)" stroke="rgba(243,243,241,.5)" stroke-width="1.6"{dash}/>')
        p.append(T(cx, bot + 44, n, 28, "head", 600, BONE, "middle", ls=-0.5, tag=f"leg-{n}"))
        if n == "Intellectual":
            p.append(T(cx, bot + 74, "fifth leg", 20, "mono", 500, MUTE, "middle", tag="leg-5"))
    # ---- section 2: rule of three
    s2 = bot + 168
    p.append(line(MARGIN, s2 - 44, W - MARGIN, s2 - 44))
    p.append(mlabel(MARGIN, s2, "RULE OF THREE  \u00b7  RAMESH HEIDARY, GOOGLE CLOUD", MUTE, tag="s2"))
    items = ["Where data goes", "Who can be compelled", "Prove it"]
    cw3 = (W - 2 * MARGIN) / 3
    nb = s2 + 36 + 0.72 * 80
    for i, t in enumerate(items):
        x = MARGIN + i * cw3
        p.append(hero(x - 3, nb, str(i + 1), 80, VIOLET, wt=600, tag=f"r3n-{i}"))
        p.append(T(x + hero_w(str(i + 1), 80, 600) + 18, nb - 4, t, 26, "sans", 500, BONE, tag=f"r3t-{i}"))
    # ---- section 3: three-point spectrum (AU at the exact midpoint)
    s3 = nb + 104
    p.append(line(MARGIN, s3 - 44, W - MARGIN, s3 - 44))
    p.append(mlabel(MARGIN, s3, "WHERE AUSTRALIA SITS  \u00b7  LAURA HEIDRICH, GOOGLE CLOUD", MUTE, tag="s3"))
    by = s3 + 70
    eu, us = 160, 1040
    au = (eu + us) / 2                     # exactly the midpoint of the line
    p.append(spectrum(eu, by - 2, us - eu, 4))
    p.append(glow(au, by, 110, 0.55))
    for x in (eu, us):
        p.append(f'<circle cx="{x}" cy="{by}" r="9" fill="{BONE}" stroke="{PITCH}" stroke-width="3"/>')
    p.append(f'<circle cx="{au}" cy="{by}" r="13" fill="{VIOLET}" stroke="{BONE}" stroke-width="2.5"/>')
    p.append(T(eu - 26, by + 8, "EU", 24, "mono", 700, BONE, "end", tag="eu"))
    p.append(T(us + 26, by + 8, "US", 24, "mono", 700, BONE, tag="us"))
    p.append(T(au, by - 28, "AU", 24, "mono", 700, BONE, "middle", tag="au"))
    p.append(T(eu, by - 26, "stricter rules", 16, "mono", 500, MUTE, ls=1.0, tag="cue-strict"))
    p.append(T(us, by - 26, "looser rules", 16, "mono", 500, MUTE, "end", ls=1.0, tag="cue-loose"))
    p.append(T(eu, by + 56, "hygiene", 26, "head", 500, SUB, "middle", tag="eu-q"))
    p.append(T(au, by + 56, "ethical middle ground", 26, "head", 600, BONE, "middle", tag="au-q"))
    BOTTOM[0] = by + 56
    corner = corner_logos()
    p.append(lf_mark())
    p.append(T(SRC_X, LOGO_BR_CY + 6, "Paraphrased from notes taken at the Sovereign AI panel, Spark Festival, 24 Sep 2026",
               16, "mono", 400, MUTE, tag="foot"))
    parts = [header(EYEBROW_PANEL, "AI sovereignty, in detail")] + p + [corner]
    check_layout("gdg-sovereignty-detail")
    return wrap_svg("\n".join(parts))


BOTTOM = [0]


# ================================================================ driver

GRAPHICS = [("gdg-stats", gen_stats), ("gdg-sovereignty", gen_sovereignty),
            ("gdg-antigravity", gen_antigravity), ("gdg-sovereignty-detail", gen_sov_detail_v3)]


def render(name, svg):
    check_bad(svg, name)
    svg_path, png_path = OUT / f"{name}.svg", OUT / f"{name}.png"
    svg_path.write_text(svg)
    subprocess.run([BUILD, str(svg_path), str(png_path)], check=True, stdout=subprocess.DEVNULL)
    im = Image.open(png_path).convert("RGB")
    im.resize((390, 390), Image.LANCZOS).save(OUT / f"preview-{name}-390.png")
    print(f"wrote {svg_path.name}, {png_path.name}, preview-{name}-390.png")


def render_alt(path_png, svg):
    """Preview-only render outside out/ (e.g. the as-briefed detail variant). Same guards."""
    check_bad(svg, path_png)
    sp = Path(path_png).with_suffix(".svg")
    for fn in (MARK, LOGO_GDG[0], LOGO_SPARK[0]):        # rsvg needs same-dir hrefs: copy the images alongside
        (sp.parent / fn).write_bytes((OUT / fn).read_bytes())
    sp.write_text(svg)
    subprocess.run([BUILD, str(sp), path_png], check=True, stdout=subprocess.DEVNULL)


def main(only=None):
    for name, fn in GRAPHICS:
        if only and name not in only:
            continue
        WARN.clear()
        svg = fn()
        render(name, svg)
        for w_ in WARN:
            print("WARN", name, w_)
    print("logos:", LOGO_STATUS)


if __name__ == "__main__":
    main(sys.argv[1:] or None)
