#!/usr/bin/env python3
"""RAG post graphics (LinkedIn portrait 1200x1500), dark glowing chart-led poster style.

Sources: /workspace/projects/rag-3-types/sources/*.html and ../stats.md (sourcing: graphics-sourcing.md).
Helpers are self-contained here: _gen_gdg.py was no longer on the box when this set was made.
Run: python3 _gen_rag.py [name ...]
"""
import re
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageFont

OUT = Path(__file__).resolve().parent
BUILD = "/workspace/render/build.sh"
W, H = 1200, 1500
M = 72                       # content margin
LF_X, LF_Y, LF_W = 36, 1405, 72
LF_H = LF_W * 144 / 154
LF_BOX = ("lf", LF_X, LF_Y, LF_X + LF_W, LF_Y + LF_H)

# ---- tokens.css only
PITCH, BONE, SUB, MUTE = "#05010E", "#F3F3F1", "#D4D2CE", "#A4A098"
VIOLET, INDIGO, AMBER, ACCENT = "#A855F7", "#6366F1", "#FCD34D", "#895AF6"
SURFACE, SURFACE2, INPUT, RED = "#160F24", "#1C1528", "#1B122B", "#DC2828"
RULE, RULE2 = "rgba(243,243,241,.12)", "rgba(243,243,241,.07)"
ALLOWED_HEX = {PITCH, BONE, SUB, MUTE, VIOLET, INDIGO, AMBER, ACCENT, SURFACE, SURFACE2, INPUT, RED}
ALLOWED_RGB = {(243, 243, 241), (168, 85, 247), (5, 1, 14)}

# ---- fonts (PIL measuring mirrors what rsvg renders)
FONT_FILES = {
    "head": {500: "/home/box/.fonts/GeneralSans-Medium.ttf", 600: "/home/box/.fonts/GeneralSans-Semibold.ttf",
             400: "/home/box/.fonts/GeneralSans-Regular.ttf"},
    "sans": "/usr/share/fonts/truetype/sand-box/google/Geist/Geist-VariableFont_wght.ttf",
    "mono": "/usr/share/fonts/truetype/sand-box/google/Geist Mono/GeistMono-VariableFont_wght.ttf",
}
FAMILY = {"head": "General Sans, sans-serif", "sans": "Geist, ui-sans-serif, system-ui, sans-serif",
          "mono": "Geist Mono, ui-monospace, SFMono-Regular, Menlo, monospace"}
_fc = {}


def font(kind, size, wt):
    key = (kind, size, wt)
    if key not in _fc:
        if kind == "head":
            f = ImageFont.truetype(FONT_FILES["head"][wt], size)
        else:
            f = ImageFont.truetype(FONT_FILES[kind], size)
            f.set_variation_by_axes([wt])
        _fc[key] = f
    return _fc[key]


def tw(s, kind="sans", size=20, wt=400, ls=0.0):
    return font(kind, size, wt).getlength(s) + ls * max(len(s) - 1, 0)


def wrap_px(s, maxw, kind, size, wt=400, ls=0.0):
    lines, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if cur and tw(t, kind, size, wt, ls) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


TEXT_BOXES, BLOCKS = [], []


def T(x, y, s, fs=20, kind="sans", wt=400, fill=SUB, anchor="start", ls=0.0, tag=None, opacity=None, rot=None):
    w = tw(s, kind, fs, wt, ls)
    x0 = {"start": x, "middle": x - w / 2, "end": x - w}[anchor]
    if rot is None:
        TEXT_BOXES.append((tag or s, x0, y - fs * 0.76, x0 + w, y + fs * 0.24))
    attrs = f'font-family="{FAMILY[kind]}" font-size="{fs}" font-weight="{wt}" fill="{fill}"'
    if anchor != "start":
        attrs += f' text-anchor="{anchor}"'
    if ls:
        attrs += f' letter-spacing="{ls}"'
    if opacity is not None:
        attrs += f' opacity="{opacity}"'
    if rot is not None:
        attrs += f' transform="rotate({rot} {x:.1f} {y:.1f})"'
    return f'<text x="{x:.1f}" y="{y:.1f}" {attrs}>{escape(s)}</text>'


def block(tag, x0, y0, x1, y1):
    BLOCKS.append((tag, x0, y0, x1, y1))


DEFS = []
_gid = [0]


def gid(p):
    _gid[0] += 1
    return f"id-{p}-{_gid[0]}"


def glow(cx, cy, r, op=0.5, col=VIOLET, sy=1.0):
    i = gid("glow")
    DEFS.append(f'<radialGradient id="{i}" cx="50%" cy="50%" r="50%">'
                f'<stop offset="0" stop-color="{col}" stop-opacity="{op}"/>'
                f'<stop offset="0.45" stop-color="{ACCENT}" stop-opacity="{op * 0.35}"/>'
                f'<stop offset="1" stop-color="{INDIGO}" stop-opacity="0"/></radialGradient>')
    return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{r:.1f}" ry="{r * sy:.1f}" fill="url(#{i})"/>'


def dotgrid(cx, cy, r, step=24):
    p, m = gid("dots"), gid("mask")
    g = gid("mg")
    DEFS.append(f'<pattern id="{p}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
                f'<circle cx="{step / 2}" cy="{step / 2}" r="1.1" fill="{BONE}" fill-opacity="0.16"/></pattern>')
    DEFS.append(f'<radialGradient id="{g}" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{BONE}" '
                f'stop-opacity="1"/><stop offset="1" stop-color="{BONE}" stop-opacity="0"/></radialGradient>')
    DEFS.append(f'<mask id="{m}"><rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" fill="url(#{g})"/></mask>')
    return f'<rect x="{cx - r}" y="{cy - r}" width="{2 * r}" height="{2 * r}" fill="url(#{p})" mask="url(#{m})"/>'


def start():
    TEXT_BOXES.clear()
    BLOCKS.clear()
    DEFS.clear()
    BLOCKS.append(LF_BOX)


def header(eyebrow, title_lines, sub=None, y=112, tfs=58, sub_w=1000):
    """Eyebrow (mono, violet dot), General Sans title, optional Geist subtitle. Returns the y below it."""
    p = [f'<circle cx="{M + 5}" cy="{y - 7}" r="5" fill="{VIOLET}"/>',
         T(M + 22, y, eyebrow.upper(), 20, "mono", 500, MUTE, ls=2.4, tag="eyebrow")]
    ty = y + 30 + tfs
    for i, ln in enumerate(title_lines):
        p.append(T(M - 2, ty, ln, tfs, "head", 600, BONE, ls=-tfs * 0.025, tag=f"title-{i}"))
        ty += tfs * 1.1
    yb = ty - tfs * 1.1 + tfs * 0.3
    if sub:
        sy = yb + 44
        lines = [ln for part in sub.split("\n") for ln in wrap_px(part, sub_w, "sans", 26, 400)]
        for i, ln in enumerate(lines):
            p.append(T(M, sy, ln, 26, "sans", 400, SUB, tag=f"sub-{i}"))
            sy += 36
        yb = sy - 36 + 8
    return "\n".join(p), yb


def footer(source):
    cy = LF_Y + LF_H / 2
    return "\n".join([
        f'<image href="lf-mark.png" xlink:href="lf-mark.png" x="{LF_X}" y="{LF_Y}" width="{LF_W}" height="{LF_H:.1f}"/>',
        T(LF_X + LF_W + 28, cy + 7, source, 20, "mono", 400, MUTE, ls=0.2, tag="source")])


def wrap_svg(inner):
    defs = "\n    ".join(DEFS)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    {defs}
  </defs>
  <rect width="{W}" height="{H}" fill="{PITCH}"/>
{inner}
</svg>
'''


def check(name):
    def hit(a, b, m=0):
        return not (a[3] + m <= b[1] or b[3] + m <= a[1] or a[4] + m <= b[2] or b[4] + m <= a[2])
    errs = []
    for i, a in enumerate(TEXT_BOXES):
        if a[1] < 30 or a[3] > W - 30 or a[2] < 20 or a[4] > H - 20:
            errs.append(f"off-canvas {a}")
        for b in BLOCKS:
            if hit(a, b, 4):
                errs.append(f"text {a[0]!r} hits {b[0]}")
        for b in TEXT_BOXES[i + 1:]:
            if hit(a, b, 1):
                errs.append(f"text overlap {a[0]!r} / {b[0]!r}")
    if errs:
        raise SystemExit(f"{name}: layout errors:\n  " + "\n  ".join(errs))


def guard(svg, name):
    for ch in ("\u2014", "\u2013"):
        if ch in svg:
            raise SystemExit(f"dash in {name}")
    for hx in re.findall(r"#[0-9A-Fa-f]{6}\b", svg):
        if hx.upper() not in ALLOWED_HEX:
            raise SystemExit(f"off-palette colour in {name}: {hx}")
    for m in re.findall(r"rgba\(([^)]*)\)", svg):
        if tuple(int(float(v)) for v in m.split(",")[:3]) not in ALLOWED_RGB:
            raise SystemExit(f"off-palette rgba in {name}: {m}")
    if "<linearGradient" in svg or "<filter" in svg:
        raise SystemExit(f"linear gradient / filter in {name}")


def render(name, svg):
    guard(svg, name)
    sp, pp = OUT / f"{name}.svg", OUT / f"{name}.png"
    sp.write_text(svg)
    r = subprocess.run([BUILD, str(sp), str(pp)], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr)
    size = Image.open(pp).size
    if size != (W, H):
        # build.sh fits into a 1200x1200 box, so a 1200x1500 viewBox comes out 960x1200.
        # Re-render at the true portrait size with exactly build.sh's rsvg flags.
        subprocess.run(["rsvg-convert", f"--width={W}", f"--height={H}", "--keep-aspect-ratio",
                        "--background-color", PITCH, "-o", str(pp), str(sp)], check=True)
    im = Image.open(pp).convert("RGB")
    assert im.size == (W, H), im.size
    im.resize((390, round(390 * H / W)), Image.LANCZOS).save(OUT / f"preview-{name}-390.png")
    print(f"wrote {name}.svg/.png {im.size} (build.sh gave {size[0]}x{size[1]}), preview-{name}-390.png")


# ======================================================================= 1. failure map
def gen_failure_map():
    start()
    p = []
    hd, yb = header("RAG options · output character",
                    ["Which failure mode", "can you live with?"],
                    "Soft failures look identical to correct answers. Hard failures announce themselves.")
    X0, X1, Y0, Y1 = 168, 1128, yb + 64, 1222
    cx, cy = (X0 + X1) / 2, (Y0 + Y1) / 2
    p.append(dotgrid(cx, cy, 560))
    p.append(glow(cx + 120, cy + 120, 520, 0.42, sy=0.9))
    p.append(hd)
    # quadrant frame and cross
    p.append(f'<rect x="{X0}" y="{Y0:.1f}" width="{X1 - X0}" height="{Y1 - Y0:.1f}" rx="18" fill="none" stroke="{RULE}" stroke-width="1.5"/>')
    p.append(f'<line x1="{cx}" y1="{Y0:.1f}" x2="{cx}" y2="{Y1}" stroke="{RULE}" stroke-width="1.5"/>')
    p.append(f'<line x1="{X0}" y1="{cy:.1f}" x2="{X1}" y2="{cy:.1f}" stroke="{RULE}" stroke-width="1.5"/>')
    # axis labels
    p.append(T(124, (Y0 + cy) / 2, "DETERMINISTIC", 21, "mono", 500, SUB, "middle", ls=2.2, rot=-90))
    p.append(T(124, (cy + Y1) / 2, "PROBABILISTIC", 21, "mono", 500, SUB, "middle", ls=2.2, rot=-90))
    block("y-axis", 100, Y0, 130, Y1)
    ay = Y1 + 40
    p.append(T(X0, ay, "WORDS", 21, "mono", 500, SUB, ls=2.2, tag="x-words"))
    p.append(T(cx, ay, "WORDS AND MEANING", 21, "mono", 500, SUB, "middle", ls=2.2, tag="x-both"))
    p.append(T(X1, ay, "MEANING", 21, "mono", 500, SUB, "end", ls=2.2, tag="x-meaning"))
    p.append(f'<path d="M{cx - 7} {Y1 + 2} l7 9 l7 -9" fill="none" stroke="{MUTE}" stroke-width="1.5"/>')

    def mark(x, y, hard, name, desc, side, straddle=False):
        r = 15
        if hard:
            s = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{VIOLET}"/>'
        else:
            s = (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r - 1.5}" fill="{VIOLET}" fill-opacity="0.16" '
                 f'stroke="{VIOLET}" stroke-width="3"/>')
        block(name + "-mark", x - r, y - r, x + r, y + r)
        out = [s]
        if side == "r":
            tx, anc = x + r + 16, "start"
        else:
            tx, anc = x - r - 16, "end"
        w = max(tw(name, "sans", 26, 500), tw(desc, "sans", 21, 400))
        bx = tx if anc == "start" else tx - w
        if straddle:   # name above the line, detail below it, like the mark itself
            out.append(T(tx, y - 12, name, 26, "sans", 500, BONE, anc, tag=name))
            out.append(T(tx, y + 30, desc, 21, "sans", 400, MUTE, anc, tag=name + "-d"))
        else:
            out.append(T(tx, y + 6, name, 26, "sans", 500, BONE, anc, tag=name))
            out.append(T(tx, y + 34, desc, 21, "sans", 400, MUTE, anc, tag=name + "-d"))
        return "\n".join(out)

    q = (cy - Y0)
    # deterministic, words
    p.append(mark(X0 + 150, Y0 + q * 0.42, False, "Text-to-query", "deterministic on execution", "r"))
    # the two mixed cases sit on / just under the deterministic line, words-and-meaning column
    p.append(mark(cx, cy, True, "Hybrid + metadata filters", "deterministic scope, probabilistic ranking", "l", True))
    p.append(mark(cx, cy + q * 0.24, False, "Hybrid Graph RAG", "exact entry, probabilistic neighbourhood", "l"))
    p.append(mark(cx, cy + q * 0.50, False, "Hybrid + reranker", "words and meaning", "l"))
    p.append(mark(cx, cy + q * 0.76, False, "Agentic hybrid", "probabilistic and path-dependent", "l"))
    # probabilistic, meaning
    mx = cx + 200
    p.append(mark(mx, cy + q * 0.24, False, "Long context", "probabilistic, meaning", "r"))
    p.append(mark(mx, cy + q * 0.50, False, "Vector RAG", "meaning only", "r"))
    p.append(mark(mx, cy + q * 0.76, False, "GraphRAG", "meaning at corpus scale", "r"))
    # legend
    ly = ay + 66
    p.append(f'<circle cx="{X0 + 12}" cy="{ly - 8}" r="12" fill="{VIOLET}"/>')
    p.append(T(X0 + 36, ly, "Fails hard: returns nothing and tells you so", 22, "sans", 400, SUB, tag="lg-hard"))
    p.append(f'<circle cx="{X0 + 12}" cy="{ly + 34}" r="10.5" fill="{VIOLET}" fill-opacity="0.16" stroke="{VIOLET}" stroke-width="3"/>')
    p.append(T(X0 + 36, ly + 42, "Fails soft: returns a plausible wrong answer", 22, "sans", 400, SUB, tag="lg-soft"))
    p.append(T(X1, ly + 42, "Position inside a quadrant is not a score", 19, "mono", 400, MUTE, "end", tag="lg-note"))
    p.append(footer("Source: rag-options-at-a-glance"))
    check("rag-failure-map")
    return wrap_svg("\n".join(p))


# ======================================================================= 2. cost ladder
LADDER = [  # name, sub, index dots, query dots, verdict  (rag-options-at-a-glance, table order)
    ("Long context", "no retrieval", 0, 4, "Baseline to beat"),
    ("Vector RAG", "dense only", 1, 1, "Prototypes only"),
    ("Hybrid + reranker", "dense + lexical", 1, 2, "Production floor"),
    ("Hybrid + metadata filters", "+ structured fields", 2, 1, "Production floor"),
    ("Agentic hybrid", "iterative, decomposed", 1, 3, "Fastest-growing"),
    ("Text-to-query", "SQL or Cypher on your schema", 0, 1, "Under-used"),
    ("GraphRAG", "derived structural", 4, 3, "Rare, narrow"),
    ("Hybrid Graph RAG", "dense + lexical + structural", 4, 4, "Secondary index"),
]


def dots(x, cy, n, r=9, gap=27):
    out = []
    for i in range(4):
        cxx = x + r + i * gap
        if i < n:
            out.append(f'<circle cx="{cxx:.1f}" cy="{cy:.1f}" r="{r}" fill="{VIOLET}"/>')
        else:
            out.append(f'<circle cx="{cxx:.1f}" cy="{cy:.1f}" r="{r - 1}" fill="none" stroke="{MUTE}" stroke-width="2" stroke-opacity="0.75"/>')
    return "\n".join(out)


def gen_cost_ladder():
    start()
    p = []
    hd, yb = header("RAG options · cost", ["Eight steps, from", "baseline to secondary index"],
                    "Dots are the source's index and query cost ratings.\nFour filled marks is the most expensive option in the set.", sub_w=1060)
    p.append(dotgrid(820, 900, 560))
    p.append(glow(860, 760, 560, 0.40, sy=1.0))
    p.append(hd)
    DX = 1128 - 2 * 4 * 27 - 50          # dot columns
    IX, QX = DX - 4 * 27 - 44 + 50, DX + 50
    top = yb + 110
    p.append(T(IX + 4 * 27 / 2 - 4, top - 22, "INDEX", 19, "mono", 500, MUTE, "middle", ls=2, tag="h-index"))
    p.append(T(QX + 4 * 27 / 2 - 4, top - 22, "QUERY", 19, "mono", 500, MUTE, "middle", ls=2, tag="h-query"))
    bottom = 1352
    floor_gap = 64
    n = len(LADDER)
    gap = 12
    sh = (bottom - top - floor_gap - gap * (n - 2)) / n
    off = 52
    y = bottom
    rows = []
    for i, (name, sub, ix, qx, verdict) in enumerate(LADDER):
        y0 = y - sh
        x0 = M + i * off
        floor = name == "Hybrid + reranker"
        stroke = f'stroke="{VIOLET}" stroke-width="2"' if floor else f'stroke="{RULE}" stroke-width="1.5"'
        p.append(f'<rect x="{x0}" y="{y0:.1f}" width="{1128 - x0}" height="{sh:.1f}" rx="12" fill="{SURFACE}" {stroke}/>')
        p.append(f'<text x="{x0 + 24}" y="{y0 + sh / 2 - 4:.1f}" font-family="{FAMILY["mono"]}" font-size="18" '
                 f'font-weight="500" fill="{VIOLET}">{i + 1:02d}</text>')
        TEXT_BOXES.append((f"n{i}", x0 + 24, y0 + sh / 2 - 18, x0 + 48, y0 + sh / 2))
        p.append(T(x0 + 64, y0 + sh / 2 - 4, name, 26, "sans", 500, BONE, tag=name))
        p.append(T(x0 + 64, y0 + sh / 2 + 26, verdict, 20, "sans", 400, MUTE, tag=name + "-v"))
        p.append(dots(IX, y0 + sh / 2, ix))
        p.append(dots(QX, y0 + sh / 2, qx))
        rows.append((y0, y))
        y = y0 - gap
        if floor:
            # production floor: its own band directly under the hybrid + reranker step
            pass
        if i == 1:
            y = y0 - floor_gap
            fy = y0 - floor_gap / 2 + 2
            p.append(f'<line x1="{M}" y1="{fy:.1f}" x2="1128" y2="{fy:.1f}" stroke="{VIOLET}" stroke-width="2" stroke-dasharray="8 7"/>')
            lw = tw("PRODUCTION FLOOR", "mono", 20, 600, 2.4)
            p.append(f'<rect x="{M + 2 * off - 4}" y="{fy - 16:.1f}" width="{lw + 28:.1f}" height="32" rx="16" fill="{PITCH}" stroke="{VIOLET}" stroke-width="1.5"/>')
            p.append(T(M + 2 * off + 10, fy + 7, "PRODUCTION FLOOR", 20, "mono", 600, VIOLET, ls=2.4, tag="floor"))
    # dot legend
    p.append(footer("Source: rag-options-at-a-glance"))
    check("rag-cost-ladder")
    return wrap_svg("\n".join(p))


# ======================================================================= 3. selection matrix
COLS = ["Long context, no retrieval", "Vector only", "Hybrid + reranker", "Hybrid + metadata filters",
        "Agentic hybrid", "Text-to-query on existing schema", "GraphRAG"]
ROWS = [  # name, small, cells: S strong, W workable, X wrong tool (rag-selection-matrix.html)
    ("Exact identifier lookup", "Part numbers, SKUs, error codes, clause references", "WXSSSSW"),
    ("Conceptual or paraphrased", "\u201cWhat\u2019s our stance on contractor access?\u201d", "SSSSSXW"),
    ("Multi-hop synthesis", "Answer depends on chaining two or three retrievals", "WXXWSWW"),
    ("Global or aggregative", "\u201cWhat themes recur across 4,000 reports?\u201d", "XXXXWWS"),
    ("Relational traversal", "Blast radius, dependency chains, shared counterparties", "XXXXWSS"),
]


def cell_mark(cx, cy, state, s=34):
    x, y = cx - s / 2, cy - s / 2
    if state == "S":
        return f'<rect x="{x:.1f}" y="{y:.1f}" width="{s}" height="{s}" rx="5" fill="{VIOLET}"/>'
    if state == "W":
        return (f'<path d="M{x:.1f} {y + s:.1f} L{x + s:.1f} {y:.1f} L{x + s:.1f} {y + s:.1f} Z" fill="{VIOLET}"/>'
                f'<rect x="{x + 1.25:.1f}" y="{y + 1.25:.1f}" width="{s - 2.5}" height="{s - 2.5}" rx="5" fill="none" stroke="{VIOLET}" stroke-width="2.5"/>')
    return (f'<rect x="{x + 1.25:.1f}" y="{y + 1.25:.1f}" width="{s - 2.5}" height="{s - 2.5}" rx="5" fill="none" '
            f'stroke="{MUTE}" stroke-width="2.5" stroke-opacity="0.8"/>')


def gen_matrix():
    start()
    p = []
    hd, yb = header("RAG selection matrix", ["Choose by the query,", "not by the industry"],
                    "Selection is driven by corpus properties and query archetype, not by industry label.")
    p.append(dotgrid(800, 900, 520))
    p.append(glow(820, 900, 520, 0.36))
    p.append(hd)
    RX0, CX0, CX1 = M, 400, 1128
    cw = (CX1 - CX0) / len(COLS)
    head_top = yb + 40
    head_bot = head_top + 330
    for j, c in enumerate(COLS):
        x = CX0 + cw * (j + 0.5) + 8
        lines = wrap_px(c, 300, "sans", 23, 500)
        for k, ln in enumerate(lines):
            xx = x + (k - (len(lines) - 1) / 2) * 27
            p.append(T(xx, head_bot - 8, ln, 23, "sans", 500, BONE, rot=-90))
        block(f"col{j}", x - 14, head_bot - 300, x + 14, head_bot)
    gy0 = head_bot + 16
    p.append(T(RX0, head_bot - 8, "QUERY ARCHETYPE", 19, "mono", 500, MUTE, ls=2, tag="corner"))
    gy1 = 1240
    rh = (gy1 - gy0) / len(ROWS)
    p.append(f'<rect x="{CX0}" y="{gy0:.1f}" width="{CX1 - CX0}" height="{gy1 - gy0:.1f}" rx="14" fill="{SURFACE}" fill-opacity="0.7" stroke="{RULE}" stroke-width="1.5"/>')
    for j in range(1, len(COLS)):
        x = CX0 + cw * j
        p.append(f'<line x1="{x:.1f}" y1="{gy0:.1f}" x2="{x:.1f}" y2="{gy1}" stroke="{RULE2}" stroke-width="1.5"/>')
    for i, (name, small, cells) in enumerate(ROWS):
        y0 = gy0 + rh * i
        if i:
            p.append(f'<line x1="{RX0}" y1="{y0:.1f}" x2="{CX1}" y2="{y0:.1f}" stroke="{RULE}" stroke-width="1.5"/>')
        sl = wrap_px(small, CX0 - RX0 - 24, "sans", 19, 400)
        bh = 26 + 25 * len(sl)
        ty = y0 + rh / 2 - bh / 2 + 20
        p.append(T(RX0, ty, name, 24, "sans", 500, BONE, tag=name))
        for k, ln in enumerate(sl):
            p.append(T(RX0, ty + 30 + 25 * k, ln, 19, "sans", 400, MUTE, tag=f"{name}-{k}"))
        for j, st in enumerate(cells):
            p.append(cell_mark(CX0 + cw * (j + 0.5), y0 + rh / 2, st, 40))
    # legend
    ly = gy1 + 62
    items = [("S", "Strong fit"), ("W", "Workable with effort"), ("X", "Wrong tool")]
    x = RX0
    for st, lab in items:
        p.append(cell_mark(x + 13, ly - 8, st, 26))
        p.append(T(x + 38, ly, lab, 22, "sans", 400, SUB, tag="lg-" + st))
        x += 38 + tw(lab, "sans", 22) + 44
    p.append(T(RX0, ly + 44, "Hybrid Graph RAG has no column: the source treats \u201chybrid graph\u201d as an ensemble.",
               18, "mono", 400, MUTE, tag="note"))
    p.append(footer("Source: rag-selection-matrix"))
    check("rag-selection-matrix")
    return wrap_svg("\n".join(p))


# ======================================================================= 4 + 5. pipeline cards
def chips(x, y, maxx, labels, fs=20, h=40, gapx=12, gapy=12, hi=()):
    out, cx, cy = [], x, y
    for lab in labels:
        w = tw(lab, "mono", fs, 500) + 32
        if cx + w > maxx and cx > x:
            cx, cy = x, cy + h + gapy
        strong = lab in hi
        out.append(f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" '
                   f'fill="{INPUT}" stroke="{VIOLET if strong else RULE}" stroke-width="1.5"/>')
        out.append(T(cx + 16, cy + h / 2 + fs * 0.34, lab, fs, "mono", 500, BONE if strong else SUB, tag=lab))
        cx += w + gapx
    return "\n".join(out), cy + h


def chip_rows(x, maxx, labels, fs=20, gapx=12):
    """Rows the chips wrap to."""
    rows, cx = 1, x
    for lab in labels:
        w = tw(lab, "mono", fs, 500) + 32
        if cx + w > maxx and cx > x:
            rows, cx = rows + 1, x
        cx += w + gapx
    return rows


def flow_arrow(x, y0, y1, label):
    out = [f'<line x1="{x}" y1="{y0:.1f}" x2="{x}" y2="{y1 - 9:.1f}" stroke="{VIOLET}" stroke-width="2"/>',
           f'<path d="M{x - 7} {y1 - 11:.1f} L{x} {y1:.1f} L{x + 7} {y1 - 11:.1f}" fill="none" stroke="{VIOLET}" stroke-width="2"/>',
           T(x + 18, (y0 + y1) / 2 + 7, label, 19, "mono", 500, MUTE, ls=0.6, tag="flow-" + label)]
    return "\n".join(out)


def stage_card(x0, y0, x1, y1, num, name, line, labels, hi=(), accent=False):
    out = [f'<rect x="{x0}" y="{y0:.1f}" width="{x1 - x0}" height="{y1 - y0:.1f}" rx="16" fill="{SURFACE}" '
           f'stroke="{VIOLET if accent else RULE}" stroke-width="{2 if accent else 1.5}"/>',
           f'<rect x="{x0}" y="{y0 + 22:.1f}" width="4" height="{y1 - y0 - 44:.1f}" rx="2" fill="{VIOLET}"/>']
    pad = 36
    rows = chip_rows(x0 + pad, x1 - pad, labels)
    content = 40 + 12 + 28 + 22 + rows * 40 + (rows - 1) * 12
    ty = y0 + (y1 - y0 - content) / 2 + 36
    out.append(T(x0 + pad, ty, num, 20, "mono", 600, VIOLET, ls=1.5, tag=num + name))
    out.append(T(x0 + pad + 46, ty + 2, name, 36, "head", 600, BONE, ls=-0.6, tag=name))
    out.append(T(x0 + pad, ty + 40, line, 22, "sans", 400, SUB, tag=name + "-line"))
    c, _ = chips(x0 + pad, ty + 62, x1 - pad, labels, hi=hi)
    out.append(c)
    return "\n".join(out)


def endpoint(x, y, label):
    w = tw(label, "mono", 20, 500, 1.2) + 40
    return "\n".join([f'<rect x="{x - w / 2:.1f}" y="{y - 22:.1f}" width="{w:.1f}" height="44" rx="22" fill="none" '
                      f'stroke="{SUB}" stroke-width="1.5" stroke-dasharray="5 5"/>',
                      T(x, y + 7, label, 20, "mono", 500, SUB, "middle", ls=1.2, tag="ep-" + label)])


VECTOR_STAGES = [
    ("01", "Parse", "Files become structured text",
     ["Parser / layout handling", "Table preservation", "Heading preservation", "Parsed content delimited as data"], ()),
    ("02", "Clean", "Strip noise before it becomes a chunk",
     ["Cleaning", "Dedup", "Boilerplate removal"], ()),
    ("03", "Chunk", "The make-or-break component",
     ["Chunk size", "Overlap", "Structure-aware splitting", "Metadata attached", "Stable IDs",
      "Versioned by instrument and amendment date", "Field quality at ingest"], ()),
]
VECTOR_FLOWS = ["structured text", "clean text"]

GRAPH_STAGES = [
    ("01", "Ontology", "Rules for what goes into the graph",
     ["Which entities become nodes", "Which relationships become edges", "Nodes immutable", "Supersession is an edge",
      "Hand-curated graph over LLM extraction"], ()),
    ("02", "Entity extraction", "Find the nodes the ontology allows",
     ["Deterministic first: parsers over NER", "Full LLM pass over the corpus"], ()),
    ("03", "Entity resolution / dedup", "The make-or-break component",
     ["Merge duplicate entities", "Disambiguate identical entities", "Risk: fragments under real-world naming"],
     ("Risk: fragments under real-world naming",)),
    ("04", "Relationship extraction", "Find the edges the ontology allows",
     ["Edge types from the ontology", "Edges only between resolved entities"], ()),
    ("05", "Validation", "Check every node and edge against the schema",
     ["Checked against the ontology", "Schema-validated, never prose-parsed"], ()),
]
GRAPH_FLOWS = ["node and edge types", "entities", "resolved entities", "typed edges"]


def gen_pipeline(kind):
    start()
    p = []
    if kind == "vector":
        hd, yb = header("Vector DB prep", ["Chunking is the", "make-or-break component"],
                        "Three stages between raw documents and the vector index.")
        stages, flows, src_ep, dst_ep = VECTOR_STAGES, VECTOR_FLOWS, "RAW DOCUMENTS", "TO EMBEDDING + INDEX"
        src = "Sources: rag-selection-matrix, compliance-rag-fde-coverage-map"
        last_flow = "chunks + metadata"
    else:
        hd, yb = header("Knowledge graph prep", ["Entity resolution is the", "make-or-break component"],
                        "A changing corpus forces full re-extraction, so every stage has to be right the first time.")
        stages, flows, src_ep, dst_ep = GRAPH_STAGES, GRAPH_FLOWS, "RAW DOCUMENTS", "TO GRAPH STORE"
        src = "Sources: rag-options-at-a-glance, rag-selection-matrix, coverage map"
        last_flow = "validated graph"
    p.append(dotgrid(820, 860, 560))
    p.append(glow(850, 860, 600, 0.34, sy=1.1))
    p.append(hd)
    x0, x1 = M, 1128
    ep_h, arrow = 44, (64 if kind == "vector" else 46)
    top = yb + 46
    bottom = 1352
    n = len(stages)
    avail = bottom - top - 2 * ep_h - (n + 1) * arrow
    # card heights proportional to their chip rows
    need = [140 + chip_rows(x0 + 36, x1 - 36, s[3]) * 52 for s in stages]
    k = avail / sum(need)
    y = top
    acx = x0 + 60
    if kind == "graph":
        p.append(stage_card(x0, y, x1, y + need[0] * k, *stages[0][:4], accent=True))
        y += need[0] * k
        p.append(flow_arrow(acx, y, y + arrow, flows[0]))
        y += arrow
        p.append(endpoint(x1 - 160, y - arrow / 2 + 2, src_ep))
        rest, rflows = stages[1:], flows[1:] + [last_flow]
        need = need[1:]
        # rebalance the remaining space
        avail2 = bottom - y - ep_h - len(rest) * arrow
        k = avail2 / sum(need)
    else:
        p.append(endpoint(x0 + tw(src_ep, "mono", 20, 500, 1.2) / 2 + 20, y + ep_h / 2, src_ep))
        y += ep_h
        p.append(flow_arrow(acx, y, y + arrow, "source files"))
        y += arrow
        rest, rflows = stages, flows + [last_flow]
    for i, s in enumerate(rest):
        h = need[i] * k
        p.append(stage_card(x0, y, x1, y + h, s[0], s[1], s[2], s[3], hi=s[4],
                            accent=(s[2] == "The make-or-break component")))
        y += h
        p.append(flow_arrow(acx, y, y + arrow, rflows[i]))
        y += arrow
    if dst_ep:
        p.append(endpoint(x0 + tw(dst_ep, "mono", 20, 500, 1.2) / 2 + 20, y + ep_h / 2, dst_ep))
    p.append(footer(src))
    check(f"rag-{kind}-pipeline")
    return wrap_svg("\n".join(p))


# ======================================================================= 6. stats (stats.md graphic labels)
STATS = [  # before, figure, after, source   (stats.md "Graphic label", split around the figure)
    ("RAG used in", "51%", "of enterprise AI deployments", "Menlo Ventures, 2024"),
    ("Contextual retrieval + reranking:", "67%", "fewer retrieval failures", "Anthropic, 2024"),
    ("GraphRAG wins", "72 to 83%", "on comprehensiveness vs vector RAG",
     "Microsoft Research, 2024 · corpus-wide questions"),
    ("LinkedIn:", "28.6%", "faster ticket resolution with graph RAG", "Xu et al., SIGIR 2024"),
]
REALITY = ("Legal RAG tools still hallucinate", "17 to 33%", "of the time", "Stanford/Yale, 2024")


def stat_block(x, y, w, h, st, fs_num, fill=SURFACE, stroke=RULE, center=False):
    before, fig, after, source = st
    out = [f'<rect x="{x}" y="{y:.1f}" width="{w}" height="{h:.1f}" rx="18" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>']
    pad = 36
    bl = wrap_px(before, w - 2 * pad, "sans", 24, 400)
    al = wrap_px(after, w - 2 * pad, "sans", 24, 400)
    while tw(fig, "head", fs_num, 600, -fs_num * 0.03) > w - 2 * pad:
        fs_num -= 2
    content = 32 * len(bl) + fs_num * 0.98 + 32 + 32 * len(al)
    ty = y + (h - 40 - content) / 2 + 26
    for i, ln in enumerate(bl):
        out.append(T(x + pad, ty + i * 32, ln, 24, "sans", 400, SUB, tag=f"{fig}-b{i}"))
    ny = ty + 32 * (len(bl) - 1) + 14 + fs_num * 0.74
    out.append(T(x + pad - 3, ny, fig, fs_num, "head", 600, BONE, ls=-fs_num * 0.03, tag=fig))
    ay = ny + fs_num * 0.24 + 32
    for i, ln in enumerate(al):
        out.append(T(x + pad, ay + i * 32, ln, 24, "sans", 400, SUB, tag=f"{fig}-a{i}"))
    out.append(T(x + pad, y + h - 28, source, 12, "mono", 400, MUTE, ls=0.4, tag=f"{fig}-src"))
    return "\n".join(out)


def gen_stats():
    start()
    p = []
    hd, yb = header("RAG in production", ["What the numbers say"], None, tfs=62)
    p.append(dotgrid(600, 620, 560))
    p.append(glow(600, 600, 620, 0.36, sy=0.9))
    p.append(hd)
    gx, gap = M, 24
    cw = (1128 - M - gap) / 2
    top = yb + 56
    rc_h = 300
    sep = 1352 - rc_h - 66
    ch = (sep - 40 - top - gap) / 2
    for i, st in enumerate(STATS):
        r, c = divmod(i, 2)
        p.append(stat_block(gx + c * (cw + gap), top + r * (ch + gap), cw, ch, st, 110))
    # separator + reality check
    lw = tw("REALITY CHECK", "mono", 22, 600, 3)
    p.append(f'<line x1="{M}" y1="{sep:.1f}" x2="{1128 - lw - 28:.1f}" y2="{sep:.1f}" stroke="{SUB}" stroke-width="1.5" stroke-dasharray="6 6"/>')
    p.append(T(1128, sep + 8, "REALITY CHECK", 22, "mono", 600, BONE, "end", ls=3, tag="rc-label"))
    rcy = sep + 40
    before, fig, after, source = REALITY
    p.append(f'<rect x="{M}" y="{rcy:.1f}" width="{1128 - M}" height="{rc_h}" rx="18" fill="none" stroke="{SUB}" stroke-width="2"/>')
    fs = 140
    p.append(T(M + 40, rcy + 54, before, 28, "sans", 400, SUB, tag="rc-b"))
    p.append(T(M + 36, rcy + 54 + 24 + fs * 0.74, fig, fs, "head", 600, BONE, ls=-fs * 0.03, tag="rc-fig"))
    fx = M + 36 + tw(fig, "head", fs, 600, -fs * 0.03) + 26
    p.append(T(fx, rcy + 54 + 24 + fs * 0.74, after, 32, "sans", 400, SUB, tag="rc-a"))
    p.append(T(M + 40, rcy + rc_h - 30, source, 12, "mono", 400, MUTE, ls=0.4, tag="rc-src"))
    p.append(footer("Source: stats.md, compiled 23 Oct 2026"))
    check("rag-stats")
    return wrap_svg("\n".join(p))


def compact_card(x0, y0, x1, h, num, name, line, labels, hi=(), accent=False):
    """Name and one-line role on one row, chips below; content vertically centred in h."""
    out = [f'<rect x="{x0}" y="{y0:.1f}" width="{x1 - x0}" height="{h:.1f}" rx="16" fill="{SURFACE}" '
           f'stroke="{VIOLET if accent else RULE}" stroke-width="{2 if accent else 1.5}"/>',
           f'<rect x="{x0}" y="{y0 + 18:.1f}" width="4" height="{h - 36:.1f}" rx="2" fill="{VIOLET}"/>']
    pad = 34
    rows = chip_rows(x0 + pad, x1 - pad, labels, fs=19, gapx=10)
    content = 32 + 20 + rows * 38 + (rows - 1) * 10
    ty = y0 + (h - content) / 2 + 26
    out.append(T(x0 + pad, ty, num, 20, "mono", 600, VIOLET, ls=1.5, tag=num + name))
    out.append(T(x0 + pad + 44, ty + 2, name, 34, "head", 600, BONE, ls=-0.6, tag=name))
    lx = x0 + pad + 44 + tw(name, "head", 34, 600, -0.6) + 22
    out.append(T(lx, ty, line, 22, "sans", 400, MUTE, tag=name + "-line"))
    c, _ = chips(x0 + pad, ty + 22, x1 - pad, labels, fs=19, h=38, gapx=10, gapy=10, hi=hi)
    out.append(c)
    return "\n".join(out)


def compact_need(labels, x0=M, x1=1128):
    rows = chip_rows(x0 + 34, x1 - 34, labels, fs=19, gapx=10)
    return 32 + 20 + rows * 38 + (rows - 1) * 10 + 2 * 24


def gen_graph():
    start()
    p = []
    hd, yb = header("Knowledge graph prep", ["Entity resolution is the", "make-or-break component"],
                    "Extraction errors become permanent structure that later queries treat as fact.", tfs=52)
    p.append(dotgrid(820, 860, 560))
    p.append(glow(850, 860, 600, 0.34, sy=1.1))
    p.append(hd)
    x0, x1 = M, 1128
    acx = x0 + 60
    top, bottom = yb + 36, 1356
    need = [compact_need(st[3]) for st in GRAPH_STAGES]
    band0, arrow = 76, 40            # band under the ontology holds the raw-documents input
    free = bottom - top - band0 - arrow * 3 - sum(need)
    if free < 0:
        raise SystemExit(f"graph pipeline overflows by {-free:.0f}px")
    grow = free / len(need)
    y = top
    labels = ["node and edge types", "entities", "resolved entities", "typed edges"]
    for i, st in enumerate(GRAPH_STAGES):
        h = need[i] + grow
        p.append(compact_card(x0, y, x1, h, st[0], st[1], st[2], st[3], hi=st[4],
                              accent=st[2] == "The make-or-break component" or i == 0))
        y += h
        if i == len(GRAPH_STAGES) - 1:
            break
        a = band0 if i == 0 else arrow
        p.append(flow_arrow(acx, y, y + a, labels[i]))
        if i == 0:
            ex = 860
            p.append(endpoint(ex, y + 24, "RAW DOCUMENTS"))
            p.append(f'<line x1="{ex}" y1="{y + 46:.1f}" x2="{ex}" y2="{y + a - 9:.1f}" stroke="{VIOLET}" stroke-width="2"/>')
            p.append(f'<path d="M{ex - 7} {y + a - 11:.1f} L{ex} {y + a:.1f} L{ex + 7} {y + a - 11:.1f}" fill="none" stroke="{VIOLET}" stroke-width="2"/>')
        y += a
    p.append(footer("Sources: rag-options-at-a-glance, rag-selection-matrix, coverage map"))
    check("rag-graph-pipeline")
    return wrap_svg("\n".join(p))


GRAPHICS = [
    ("rag-failure-map", gen_failure_map),
    ("rag-cost-ladder", gen_cost_ladder),
    ("rag-selection-matrix", gen_matrix),
    ("rag-vector-pipeline", lambda: gen_pipeline("vector")),
    ("rag-graph-pipeline", gen_graph),
    ("rag-stats", gen_stats),
]


def contact_sheet():
    tw_, th_ = 360, 450
    pad, cap = 30, 44
    sheet = Image.new("RGB", (3 * tw_ + 4 * pad, 2 * (th_ + cap) + 3 * pad - 10), (5, 1, 14))
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    f = font("mono", 18, 500)
    for i, (name, _) in enumerate(GRAPHICS):
        r, c = divmod(i, 3)
        x, y = pad + c * (tw_ + pad), pad + r * (th_ + cap + pad)
        im = Image.open(OUT / f"{name}.png").convert("RGB").resize((tw_, th_), Image.LANCZOS)
        sheet.paste(im, (x, y))
        d.rectangle([x - 1, y - 1, x + tw_, y + th_], outline=(34, 30, 41))  # --rule (bone 12%) flattened on pitch
        d.text((x, y + th_ + 12), f"{name}.png", font=f, fill=(164, 160, 152))
    sheet.save(OUT / "rag-contact-sheet.png")
    print("wrote rag-contact-sheet.png", sheet.size)


if __name__ == "__main__":
    want = sys.argv[1:]
    for name, fn in GRAPHICS:
        if want and name not in want:
            continue
        render(name, fn())
    if not want or "sheet" in want:
        contact_sheet()
