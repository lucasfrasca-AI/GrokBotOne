#!/usr/bin/env python3
"""Generate six CCAR-F reference-card SVGs (1200x1200 dark brand)."""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path("/workspace/render/out")
W = H = 1200

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
RULE = "rgba(243,243,241,.12)"

SANS = "Geist, ui-sans-serif, system-ui, sans-serif"
MONO = "Geist Mono, ui-monospace, SFMono-Regular, Menlo, monospace"

# same-dir href: rsvg on this box will not load ../ relative images
MARK = "lf-mark.png"



def esc(t: str) -> str:
    t = t.replace("\u2014", "-").replace("\u2013", "-").replace("—", "-").replace("–", "-")
    t = t.replace("\u2192", "->").replace("→", "->")
    return escape(t, {"'": "&apos;", '"': "&quot;"})



def spectrum_bar(x, y, w, h=4, gid=None):
    if gid is None:
        gid = f"spec{abs(hash((x, y, w))) % 10**8}"
    return f'''
  <defs>
    <linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{INDIGO}"/>
      <stop offset="50%" stop-color="{VIOLET}"/>
      <stop offset="100%" stop-color="{AMBER}"/>
    </linearGradient>
  </defs>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="url(#{gid})"/>'''



def chip(x, y, text, kind="mute"):
    colors = {
        "mute": (INPUT, MUTE),
        "violet": ("rgba(168,85,247,.18)", VIOLET),
        "indigo": ("rgba(99,102,241,.18)", INDIGO),
        "amber": ("rgba(252,211,77,.15)", AMBER),
        "accent": ("rgba(137,90,246,.18)", ACCENT),
    }
    bg, fg = colors.get(kind, colors["mute"])
    tw = max(54, int(len(text) * 9.6 + 24))
    th = 30
    return (
        f'<rect x="{x}" y="{y}" width="{tw}" height="{th}" rx="7" fill="{bg}"/>'
        f'<text x="{x + 12}" y="{y + 20}" font-family="{MONO}" font-size="14" '
        f'fill="{fg}" font-weight="500">{esc(text)}</text>',
        tw + 8,
    )



def chips_row(x, y, items, max_w=520):
    parts = []
    cx, cy = x, y
    row_h = 36
    for text, kind in items:
        frag, step = chip(cx, cy, text, kind)
        if cx + step - 8 > x + max_w and cx > x:
            cx = x
            cy += row_h
            frag, step = chip(cx, cy, text, kind)
        parts.append(frag)
        cx += step
    return "\n".join(parts), (cy - y) + 28



def card_box(x, y, w, h, rx=14):
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{SURFACE}" stroke="{RULE}" stroke-width="1"/>'
    )



def lf_mark(x=36, y=1108, width=72):
    height = width * 144 / 154
    return (
        f'<image href="{MARK}" xlink:href="{MARK}" x="{x}" y="{y}" width="{width}" '
        f'height="{height:.1f}" preserveAspectRatio="xMidYMid meet"/>'
    )



def footer(cite, mark_y=1105):
    return f'''
  {lf_mark(36, mark_y, 72)}
  <text x="1164" y="{mark_y + 44}" text-anchor="end" font-family="{SANS}"
        font-size="14" fill="{MUTE}">{esc(cite)}</text>
'''



def wrap_text(text, max_chars):
    words = text.split()
    lines, cur = [], []
    for w in words:
        trial = " ".join(cur + [w])
        if len(trial) <= max_chars:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines



def render_std_card(x, y, w, h, c):
    parts = [card_box(x, y, w, h)]
    pad = 18
    parts.append(
        f'<text x="{x + pad}" y="{y + 30}" font-family="{MONO}" font-size="16" '
        f'fill="{VIOLET}" font-weight="600">{esc(c["n"])}</text>'
    )
    parts.append(
        f'<text x="{x + pad}" y="{y + 60}" font-family="{SANS}" font-size="25" '
        f'fill="{BONE}" font-weight="650">{esc(c["title"])}</text>'
    )
    def_lines = wrap_text(c["def"], 38 if w < 520 else 44)
    dy = y + 90
    for line in def_lines[:2]:
        parts.append(
            f'<text x="{x + pad}" y="{dy}" font-family="{SANS}" font-size="17" '
            f'fill="{SUB}">{esc(line)}</text>'
        )
        dy += 23
    chip_y = dy + 8
    chip_svg, chip_h = chips_row(x + pad, chip_y, c["chips"], max_w=w - 2 * pad - 4)
    parts.append(chip_svg)
    cons_lines = wrap_text(c["cons"], 42 if w < 520 else 48)
    cons_y = y + h - 18 - (len(cons_lines[:2]) - 1) * 18
    min_cons = chip_y + chip_h + 14
    if cons_y < min_cons:
        cons_y = min(min_cons, y + h - 18)
    for i, line in enumerate(cons_lines[:2]):
        parts.append(
            f'<text x="{x + pad}" y="{cons_y + i * 18}" font-family="{SANS}" font-size="15" '
            f'fill="{AMBER}">{esc(line)}</text>'
        )
    return "\n".join(parts)



def wrap_svg(inner: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="1200" height="1200" viewBox="0 0 1200 1200">
  <rect width="1200" height="1200" fill="{PITCH}"/>
{inner}
</svg>
'''



def gen_g1():
    """Exam Overview: banded hierarchy (title -> FORMAT hero -> scenarios -> domains)."""
    cite = "Exam Guide v1.0 / Anthropic (facts)"
    parts = []
    parts.append(spectrum_bar(48, 36, 260, 4, "specOverview"))
    parts.append(
        f'<text x="48" y="68" font-family="{MONO}" font-size="14" fill="{VIOLET}"'
        f' letter-spacing="1.6" font-weight="600">CCAR-F  ·  REFERENCE</text>'
    )
    parts.append(
        f'<text x="48" y="104" font-family="{SANS}" font-size="36" fill="{BONE}"'
        f' font-weight="700">CCAR-F Exam Overview</text>'
    )
    parts.append(
        f'<text x="48" y="132" font-family="{SANS}" font-size="15" fill="{SUB}">'
        f'Claude Certified Architect - Foundations · Exam Guide v1.0</text>'
    )

    # FORMAT hero - taller, big numbers
    fx, fy, fw, fh = 36, 152, 1128, 248
    parts.append(card_box(fx, fy, fw, fh, rx=16))
    parts.append(f'<rect x="{fx}" y="{fy}" width="6" height="{fh}" rx="3" fill="{VIOLET}"/>')
    parts.append(
        f'<text x="{fx + 28}" y="{fy + 34}" font-family="{MONO}" font-size="16" '
        f'fill="{VIOLET}" font-weight="700" letter-spacing="2">EXAM FORMAT</text>'
    )
    top = [
        ("60", "Q", VIOLET, "rgba(168,85,247,.18)"),
        ("120", "min", INDIGO, "rgba(99,102,241,.18)"),
        ("720", "pass", VIOLET, "rgba(168,85,247,.18)"),
        ("$125", "USD", AMBER, "rgba(252,211,77,.15)"),
    ]
    cell_w = 250
    gap = 14
    for i, (num, unit, fg, bg) in enumerate(top):
        cx = 58 + i * (cell_w + gap)
        parts.append(
            f'<rect x="{cx}" y="{fy + 52}" width="{cell_w}" height="100" rx="14" fill="{bg}"/>'
        )
        parts.append(
            f'<text x="{cx + cell_w/2:.1f}" y="{fy + 108}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="42" fill="{fg}" font-weight="700">{esc(num)}</text>'
        )
        parts.append(
            f'<text x="{cx + cell_w/2:.1f}" y="{fy + 136}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="15" fill="{MUTE}" font-weight="600">{esc(unit)}</text>'
        )
    bottoms = [
        (58, 250, "closed book", INPUT, MUTE, 16),
        (322, 520, "partner-only Pearson", "rgba(99,102,241,.28)", INDIGO, 18),
        (856, 250, "12 months", INPUT, MUTE, 16),
    ]
    for bx, bw, label, bg, fg, fs in bottoms:
        parts.append(
            f'<rect x="{bx}" y="{fy + 168}" width="{bw}" height="60" rx="12" fill="{bg}"/>'
        )
        parts.append(
            f'<text x="{bx + bw/2:.1f}" y="{fy + 198}" text-anchor="middle" '
            f'dominant-baseline="central" font-family="{MONO}" font-size="{fs}" '
            f'fill="{fg}" font-weight="700">{esc(label)}</text>'
        )

    # Scenario structure
    sx, sy, sw, sh = 36, 416, 1128, 118
    parts.append(card_box(sx, sy, sw, sh, rx=14))
    parts.append(f'<rect x="{sx}" y="{sy}" width="6" height="{sh}" rx="3" fill="{AMBER}"/>')
    parts.append(
        f'<text x="{sx + 28}" y="{sy + 30}" font-family="{MONO}" font-size="14" '
        f'fill="{AMBER}" font-weight="700" letter-spacing="1.2">SCENARIO STRUCTURE</text>'
    )
    parts.append(
        f'<text x="{sx + 28}" y="{sy + 64}" font-family="{SANS}" font-size="24" '
        f'fill="{BONE}" font-weight="650">4 of 6 themes on a form · ~15 items each</text>'
    )
    chip_svg, _ = chips_row(
        sx + 28,
        sy + 78,
        [
            ("community note", "amber"),
            ("scenarios = dressing", "violet"),
            ("mechanisms recur", "mute"),
            ("learn toolkit not plot", "indigo"),
        ],
        max_w=1060,
    )
    parts.append(chip_svg)

    domains = [
        ("D1", "27%", "Agentic Architecture & Orchestration", VIOLET),
        ("D2", "18%", "Tool Design & MCP Integration", INDIGO),
        ("D3", "20%", "Claude Code Configuration & Workflows", VIOLET),
        ("D4", "20%", "Prompt Engineering & Structured Output", INDIGO),
        ("D5", "15%", "Context Management & Reliability", AMBER),
    ]
    dx, dy = 36, 550
    dw = 1128
    footer_top = 1105
    avail = footer_top - dy - 8
    hdr_h = 36
    gap_d = 8
    row_h = (avail - hdr_h - 4 * gap_d) // 5
    group_h = hdr_h + 5 * row_h + 4 * gap_d
    parts.append(card_box(dx, dy, dw, group_h, rx=16))
    parts.append(
        f'<text x="{dx + 22}" y="{dy + 26}" font-family="{MONO}" font-size="14" '
        f'fill="{VIOLET}" font-weight="700" letter-spacing="1.2">FIVE DOMAINS  ·  WEIGHTS</text>'
    )
    parts.append(
        f'<text x="{dx + dw - 22}" y="{dy + 26}" text-anchor="end" font-family="{MONO}" '
        f'font-size="13" fill="{MUTE}">100%</text>'
    )
    max_pct = 27
    for i, (dn, pct, name, accent) in enumerate(domains):
        ry = dy + hdr_h + i * (row_h + gap_d)
        parts.append(
            f'<rect x="{dx + 14}" y="{ry}" width="{dw - 28}" height="{row_h}" '
            f'rx="12" fill="{INPUT}"/>'
        )
        parts.append(
            f'<rect x="{dx + 14}" y="{ry}" width="5" height="{row_h}" rx="2" fill="{accent}"/>'
        )
        mid_y = ry + row_h / 2
        parts.append(
            f'<text x="{dx + 36}" y="{mid_y:.1f}" dominant-baseline="central" '
            f'font-family="{MONO}" font-size="17" fill="{accent}" font-weight="700">{dn}</text>'
        )
        parts.append(
            f'<text x="{dx + 84}" y="{mid_y:.1f}" dominant-baseline="central" '
            f'font-family="{MONO}" font-size="26" fill="{BONE}" font-weight="700">{pct}</text>'
        )
        parts.append(
            f'<text x="{dx + 180}" y="{mid_y:.1f}" dominant-baseline="central" '
            f'font-family="{SANS}" font-size="18" fill="{BONE}" font-weight="600">{esc(name)}</text>'
        )
        bar_max_w = 200
        pct_n = int(pct.rstrip("%"))
        bar_w = int(bar_max_w * pct_n / max_pct)
        bar_x = dx + dw - 28 - 18 - bar_max_w
        bar_y = mid_y - 6
        parts.append(
            f'<rect x="{bar_x}" y="{bar_y:.1f}" width="{bar_max_w}" height="12" '
            f'rx="6" fill="rgba(243,243,241,.08)"/>'
        )
        parts.append(
            f'<rect x="{bar_x}" y="{bar_y:.1f}" width="{bar_w}" height="12" '
            f'rx="6" fill="{accent}"/>'
        )

    parts.append(footer(cite, 1105))
    return wrap_svg("\n".join(parts))



def gen_g2():
    """Five Domains cheat: weight rail + bullets + right cue panel (no dead zone)."""
    cite = "Exam Guide v1.0 §4 / Anthropic"
    domains = [
        {
            "n": "D1",
            "pct": "27%",
            "pct_n": 27,
            "title": "Agentic Architecture & Orchestration",
            "accent": VIOLET,
            "keyword": "stop_reason",
            "cue": "loop · hub-spoke · gates",
            "bullets": [
                "stop_reason loop (tool_use / end_turn); append tool results",
                "Hub-spoke; parallel Task; allowedTools includes Task",
                "Hooks / prerequisite gates for irreversible or money-moving steps",
            ],
        },
        {
            "n": "D2",
            "pct": "18%",
            "pct_n": 18,
            "title": "Tool Design & MCP",
            "accent": INDIGO,
            "keyword": "tool scope",
            "cue": "desc first · 4-5 tools",
            "bullets": [
                "Differentiating tool descriptions; split generic tools",
                ".mcp.json (team + ${ENV}) vs ~/.claude.json (personal)",
                "Grep=contents; Glob=paths; ~4-5 tools per role",
            ],
        },
        {
            "n": "D3",
            "pct": "20%",
            "pct_n": 20,
            "title": "Claude Code Config & Workflows",
            "accent": VIOLET,
            "keyword": "project paths",
            "cue": "CLAUDE.md · rules · CI",
            "bullets": [
                "Team standards in project CLAUDE.md (not user-level)",
                ".claude/rules/ + paths: globs; skills context:fork",
                "CI: -p/--print, --output-format json, --json-schema",
            ],
        },
        {
            "n": "D4",
            "pct": "20%",
            "pct_n": 20,
            "title": "Prompt Engineering & Structured Output",
            "accent": INDIGO,
            "keyword": "tool_choice",
            "cue": "schema · nullable · batches",
            "bullets": [
                "Explicit categorical criteria; few-shot 2-4 with reasoning",
                "tool_use + schema; tool_choice auto/any/forced; nullable/enum",
                "Message Batches only if latency-tolerant; custom_id for failures",
            ],
        },
        {
            "n": "D5",
            "pct": "15%",
            "pct_n": 15,
            "title": "Context Management & Reliability",
            "accent": AMBER,
            "keyword": "escalate",
            "cue": "case-facts · trim · recover",
            "bullets": [
                "Case-facts block; trim tool output; lost-in-middle mitigation",
                "Escalate: human ask, policy gap, no progress - not sentiment",
                "Scratchpads / subagent isolation / crash-recovery manifests",
            ],
        },
    ]
    parts = []
    parts.append(spectrum_bar(48, 36, 260, 4, "specDomains"))
    parts.append(
        f'<text x="48" y="70" font-family="{MONO}" font-size="14" fill="{VIOLET}"'
        f' letter-spacing="1.6" font-weight="600">CCAR-F  ·  CHEAT</text>'
    )
    parts.append(
        f'<text x="48" y="110" font-family="{SANS}" font-size="38" fill="{BONE}"'
        f' font-weight="700">Five Domains</text>'
    )
    parts.append(
        f'<text x="48" y="140" font-family="{SANS}" font-size="16" fill="{SUB}">'
        f'Weights and pass reflexes from Exam Guide §4</text>'
    )
    body_top = 158
    margin_x = 36
    gap = 10
    footer_top = 1105
    avail = footer_top - body_top - 4
    total_w = sum(d["pct_n"] for d in domains)
    min_h = 148
    remaining = avail - 4 * gap - 5 * min_h
    if remaining < 0:
        min_h = (avail - 4 * gap) // 5
        remaining = 0
    y = body_top
    rail_w = 168
    cue_w = 210
    for i, d in enumerate(domains):
        extra = int(remaining * d["pct_n"] / total_w) if remaining else 0
        if i == 0 and remaining:
            extra += remaining - sum(
                int(remaining * dd["pct_n"] / total_w) for dd in domains
            )
        card_h = min_h + extra
        accent = d["accent"]
        parts.append(card_box(margin_x, y, rail_w, card_h, rx=14))
        parts.append(
            f'<rect x="{margin_x}" y="{y}" width="6" height="{card_h}" rx="3" fill="{accent}"/>'
        )
        pct_size = 34 + int(8 * d["pct_n"] / 27)
        mid = y + card_h / 2
        parts.append(
            f'<text x="{margin_x + rail_w/2:.0f}" y="{mid - 10:.0f}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="{pct_size}" fill="{BONE}" font-weight="700">'
            f'{d["pct"]}</text>'
        )
        parts.append(
            f'<text x="{margin_x + rail_w/2:.0f}" y="{mid + 26:.0f}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="15" fill="{accent}" font-weight="700">'
            f'{d["n"]}</text>'
        )
        bar_max = rail_w - 32
        bar_w = int(bar_max * d["pct_n"] / 27)
        bar_y = y + card_h - 20
        parts.append(
            f'<rect x="{margin_x + 16}" y="{bar_y}" width="{bar_max}" height="6" '
            f'rx="3" fill="rgba(243,243,241,.08)"/>'
        )
        parts.append(
            f'<rect x="{margin_x + 16}" y="{bar_y}" width="{bar_w}" height="6" '
            f'rx="3" fill="{accent}"/>'
        )
        rx = margin_x + rail_w + 12
        rw = W - margin_x - rx - cue_w - 12
        parts.append(card_box(rx, y, rw, card_h, rx=14))
        parts.append(
            f'<text x="{rx + 20}" y="{y + 32}" font-family="{SANS}" font-size="19" '
            f'fill="{BONE}" font-weight="650">{esc(d["title"])}</text>'
        )
        by = y + 60
        for b in d["bullets"]:
            lines = wrap_text(b, 48)
            for li, line in enumerate(lines[:2]):
                prefix = "· " if li == 0 else "  "
                parts.append(
                    f'<text x="{rx + 20}" y="{by}" font-family="{SANS}" font-size="14" '
                    f'fill="{SUB}">{esc(prefix + line)}</text>'
                )
                by += 20
            if len(lines) == 1:
                by += 2
        cx = rx + rw + 12
        parts.append(card_box(cx, y, cue_w, card_h, rx=14))
        parts.append(
            f'<rect x="{cx}" y="{y}" width="6" height="{card_h}" rx="3" fill="{accent}"/>'
        )
        parts.append(
            f'<text x="{cx + cue_w/2:.0f}" y="{y + card_h/2 - 22:.0f}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="22" fill="{accent}" font-weight="700">'
            f'{esc(d["pct"])}</text>'
        )
        parts.append(
            f'<text x="{cx + cue_w/2:.0f}" y="{y + card_h/2 + 8:.0f}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="14" fill="{BONE}" font-weight="650">'
            f'{esc(d["keyword"])}</text>'
        )
        parts.append(
            f'<text x="{cx + cue_w/2:.0f}" y="{y + card_h/2 + 32:.0f}" text-anchor="middle" '
            f'font-family="{SANS}" font-size="12" fill="{MUTE}">{esc(d["cue"])}</text>'
        )
        y += card_h + gap

    parts.append(footer(cite, 1105))
    return wrap_svg("\n".join(parts))



def gen_g3():
    cite = "Exam Guide / Anthropic docs (hit-list)"
    terms = [
        {
            "n": "01",
            "title": "stop_reason",
            "def": "Continue on tool_use; stop on end_turn.",
            "chips": [("max_tokens", "mute"), ("pause_turn", "mute"), ("refusal", "mute")],
            "cons": "Never end the loop by parsing assistant prose.",
        },
        {
            "n": "02",
            "title": "tool_choice",
            "def": "auto / any / tool+name / none.",
            "chips": [("auto", "indigo"), ("any", "violet"), ("forced", "amber")],
            "cons": "Force named tool for mandatory first step, then auto.",
        },
        {
            "n": "03",
            "title": "Hooks",
            "def": "PreToolUse can block; PostToolUse after; PreCompact before compact.",
            "chips": [("PreToolUse", "violet"), ("PostToolUse", "mute"), ("PreCompact", "mute")],
            "cons": "Money / irreversible -> PreToolUse gate, not a stronger prompt.",
        },
        {
            "n": "04",
            "title": "MCP paths",
            "def": "Team .mcp.json + ${ENV}; personal ~/.claude.json.",
            "chips": [(".mcp.json", "indigo"), ("~/.claude.json", "mute")],
            "cons": "Shared on clone -> project file; secrets via ${ENV_VAR}.",
        },
        {
            "n": "05",
            "title": "CLAUDE.md",
            "def": "~/.claude/ personal; project .claude/CLAUDE.md or root shared.",
            "chips": [("team=project", "violet"), ("personal", "mute")],
            "cons": "Team standards live in project CLAUDE.md, not user-level.",
        },
        {
            "n": "06",
            "title": "CLI CI",
            "def": "-p / --print non-interactive; --output-format json.",
            "chips": [("-p/--print", "amber"), ("json schema", "mute")],
            "cons": "Reject invented flags like CLAUDE_HEADLESS or --batch.",
        },
        {
            "n": "07",
            "title": "Grep vs Glob",
            "def": "Grep searches contents; Glob matches path patterns.",
            "chips": [("Grep=contents", "indigo"), ("Glob=paths", "violet")],
            "cons": "Incremental explore: Grep -> Read matches. Never Read-all.",
        },
        {
            "n": "08",
            "title": "Batches vs sync",
            "def": "Batches ~50% cheaper, up to 24h; no multi-turn tools.",
            "chips": [("~50% cheaper", "amber"), ("sync if blocking", "violet")],
            "cons": "Blocking / pre-merge -> sync Messages API.",
        },
    ]
    head = f'''
  {spectrum_bar(48, 36, 240, 4, "specTerms")}
  <text x="48" y="72" font-family="{MONO}" font-size="14" fill="{VIOLET}"
        letter-spacing="1.6" font-weight="600">CCAR-F  ·  MEMORISE</text>
  <text x="48" y="116" font-family="{SANS}" font-size="40" fill="{BONE}"
        font-weight="700">Terms Hit-List</text>
  <text x="48" y="148" font-family="{SANS}" font-size="17" fill="{SUB}">Paths, flags, and API params until reflexive</text>
'''
    body_top = 168
    margin_x = 36
    gap = 12
    col_w = (W - 2 * margin_x - gap) // 2
    avail = 1090 - body_top
    row_h = (avail - 3 * gap) // 4
    parts = [head]
    for i, c in enumerate(terms):
        col = i % 2
        row = i // 2
        x = margin_x + col * (col_w + gap)
        y = body_top + row * (row_h + gap)
        parts.append(render_std_card(x, y, col_w, row_h, c))
    parts.append(footer(cite, 1105))
    return wrap_svg("\n".join(parts))



def gen_g4():
    """Scenario Mechanics: core rule + constraints + six themes + dense triggers."""
    cite = "Exam Guide v1.0 / Anthropic (facts)"
    parts = []
    parts.append(spectrum_bar(48, 36, 260, 4, "specScenario"))
    parts.append(
        f'<text x="48" y="64" font-family="{MONO}" font-size="13" fill="{VIOLET}"'
        f' letter-spacing="1.6" font-weight="600">CCAR-F  ·  SCENARIOS</text>'
    )
    parts.append(
        f'<text x="48" y="98" font-family="{SANS}" font-size="34" fill="{BONE}"'
        f' font-weight="700">Scenario Mechanics</text>'
    )
    parts.append(
        f'<text x="48" y="124" font-family="{SANS}" font-size="14" fill="{SUB}">'
        f'4 of 6 appear · stories change, mechanisms repeat</text>'
    )

    x, y, w, h = 36, 140, 1128, 78
    parts.append(card_box(x, y, w, h, rx=12))
    parts.append(f'<rect x="{x}" y="{y}" width="6" height="{h}" fill="{AMBER}"/>')
    parts.append(
        f'<text x="{x + 24}" y="{y + 26}" font-family="{MONO}" font-size="12" '
        f'fill="{AMBER}" font-weight="700">CORE RULE</text>'
    )
    parts.append(
        f'<text x="{x + 24}" y="{y + 54}" font-family="{SANS}" font-size="18" '
        f'fill="{BONE}" font-weight="650">Money / safety / must -> hooks, gates, schemas, forced tool_choice. Not stronger prompts.</text>'
    )

    x2, y2, w2, h2 = 36, 230, 1128, 72
    parts.append(card_box(x2, y2, w2, h2, rx=12))
    parts.append(
        f'<text x="{x2 + 20}" y="{y2 + 22}" font-family="{MONO}" font-size="12" '
        f'fill="{VIOLET}" font-weight="700">FIND THE CONSTRAINT WORD FIRST</text>'
    )
    constraints = [
        ("latency", "indigo"),
        ("shared vs personal", "violet"),
        ("blocking", "amber"),
        ("guaranteed", "violet"),
        ("must / always", "amber"),
    ]
    chip_svg, _ = chips_row(x2 + 20, y2 + 34, constraints, max_w=1080)
    parts.append(chip_svg)

    themes = [
        ("01", "Customer Support Resolution Agent", "verify / refund gates", VIOLET),
        ("02", "Code Generation with Claude Code", "project CLAUDE.md / commands / plan", INDIGO),
        ("03", "Multi-Agent Research System", "Task parallel, explicit context", VIOLET),
        ("04", "Developer Productivity with Claude", "skills / rules / workflows", INDIGO),
        ("05", "Claude Code for CI", "-p/--print, json schema", AMBER),
        ("06", "Structured Data Extraction", "schemas, tool_choice, batches vs sync", AMBER),
    ]
    tx0, ty0 = 36, 316
    parts.append(
        f'<text x="{tx0 + 4}" y="{ty0}" font-family="{MONO}" font-size="12" '
        f'fill="{MUTE}" font-weight="700">SIX OFFICIAL THEMES  ·  4 appear</text>'
    )
    theme_top = ty0 + 10
    gap = 7
    left_w = 640
    right_w = 1128 - left_w - gap
    theme_h = 52
    for i, (n, title, cue, accent) in enumerate(themes):
        col = i % 2
        row = i // 2
        tw = left_w if col == 0 else right_w
        tx = tx0 if col == 0 else tx0 + left_w + gap
        ty = theme_top + row * (theme_h + gap)
        parts.append(card_box(tx, ty, tw, theme_h, rx=9))
        parts.append(
            f'<rect x="{tx}" y="{ty}" width="4" height="{theme_h}" rx="2" fill="{accent}"/>'
        )
        parts.append(
            f'<text x="{tx + 14}" y="{ty + 22}" font-family="{MONO}" font-size="13" '
            f'fill="{accent}" font-weight="700">{n}</text>'
        )
        parts.append(
            f'<text x="{tx + 42}" y="{ty + 22}" font-family="{SANS}" font-size="14" '
            f'fill="{BONE}" font-weight="600">{esc(title)}</text>'
        )
        parts.append(
            f'<text x="{tx + 42}" y="{ty + 42}" font-family="{SANS}" font-size="12" '
            f'fill="{MUTE}">{esc(cue)}</text>'
        )

    mech_label_y = theme_top + 3 * (theme_h + gap) + 12
    parts.append(
        f'<text x="{tx0 + 4}" y="{mech_label_y}" font-family="{MONO}" font-size="12" '
        f'fill="{MUTE}" font-weight="700">MECHANISM TRIGGERS</text>'
    )
    mechs = [
        {
            "n": "01",
            "title": "Hooks",
            "lines": [
                "PreToolUse blocks refunds / rm -rf",
                "PostToolUse cannot un-delete",
                "PreCompact before /compact (archive)",
                "No Compact tool for PreToolUse",
            ],
            "chips": [("Pre=block", "violet"), ("Post=after", "mute")],
        },
        {
            "n": "02",
            "title": "tool_choice",
            "lines": [
                "auto: text or tool (default)",
                "any: must call some tool",
                "forced name for mandatory first step",
                "none: no tools this turn",
            ],
            "chips": [("auto", "indigo"), ("any", "violet"), ("forced", "amber")],
        },
        {
            "n": "03",
            "title": "stop_reason",
            "lines": [
                "Continue on tool_use",
                "Stop on end_turn",
                "Also: max_tokens / pause_turn / refusal",
                "Never parse prose to exit loop",
            ],
            "chips": [("tool_use", "violet"), ("end_turn", "indigo")],
        },
        {
            "n": "04",
            "title": "Batches vs sync",
            "lines": [
                "No multi-turn tools in a batch",
                "custom_id to resubmit failures",
                "Blocking / pre-merge -> sync API",
                "~50% cheaper, up to 24h, no SLA",
            ],
            "chips": [("batches", "amber"), ("sync if blocking", "violet")],
        },
        {
            "n": "05",
            "title": "Grep / Glob + CI",
            "lines": [
                "Grep = file contents",
                "Glob = path patterns",
                "CI hang -> -p / --print",
                "Reject CLAUDE_HEADLESS / --batch",
            ],
            "chips": [("Grep=contents", "indigo"), ("Glob=paths", "violet"), ("-p", "amber")],
        },
        {
            "n": "06",
            "title": "Team MCP vs personal",
            "lines": [
                ".mcp.json + ${ENV} shared on clone",
                "~/.claude.json personal / experimental",
                "Secrets via ${ENV_VAR}",
                "stdio / SSE / HTTP transports",
            ],
            "chips": [(".mcp.json", "indigo"), ("~/.claude.json", "mute")],
        },
    ]
    mx0 = 36
    my0 = mech_label_y + 8
    footer_top = 1105
    avail = footer_top - my0 - 4
    gap_m = 8
    col_w = (1128 - 2 * gap_m) // 3
    row_h = (avail - gap_m) // 2

    def mech_card(mx, my, mw, mh, m):
        out = [card_box(mx, my, mw, mh, rx=11)]
        out.append(
            f'<rect x="{mx}" y="{my}" width="4" height="{mh}" rx="2" fill="{VIOLET}"/>'
        )
        out.append(
            f'<text x="{mx + 14}" y="{my + 22}" font-family="{MONO}" font-size="12" '
            f'fill="{VIOLET}" font-weight="700">{m["n"]}</text>'
        )
        out.append(
            f'<text x="{mx + 42}" y="{my + 22}" font-family="{SANS}" font-size="15" '
            f'fill="{BONE}" font-weight="650">{esc(m["title"])}</text>'
        )
        by = my + 42
        for line in m["lines"][:4]:
            out.append(
                f'<text x="{mx + 14}" y="{by}" font-family="{SANS}" font-size="14" '
                f'fill="{SUB}">{esc("· " + line)}</text>'
            )
            by += 20
        chip_s, _ = chips_row(mx + 12, my + mh - 38, m["chips"], max_w=mw - 24)
        out.append(chip_s)
        return "\n".join(out)

    for i, m in enumerate(mechs):
        col = i % 3
        row = i // 3
        mx = mx0 + col * (col_w + gap_m)
        my = my0 + row * (row_h + gap_m)
        parts.append(mech_card(mx, my, col_w, row_h, m))

    parts.append(footer(cite, 1105))
    return wrap_svg("\n".join(parts))



def gen_g5():
    """Prep Sequence: ordered ladder + UNOFFICIAL resources panel."""
    cite = "Pass directives §5 / Exam Guide §8 · Anthropic"
    steps = [
        ("01", "Guide end-to-end", "Exam Guide v1.0; self-score tasks red/amber/green", VIOLET, True),
        ("02", "Drill hit-list", "Paths, flags, stop_reason, tool_choice, hooks", AMBER, False),
        ("03", "Ex1: multi-tool + gate", "Structured errors + PreToolUse gate + escalate", INDIGO, False),
        ("04", "Ex2: CLAUDE.md + rules", "Project CLAUDE.md, rules globs, skill fork, .mcp.json", VIOLET, False),
        ("05", "Ex3: schema + batches", "Schema + validation-retry + Message Batches trial", INDIGO, False),
        ("06", "Ex4: coordinator + Task", "Hub-spoke, parallel Task, explicit context pass", VIOLET, False),
        ("07", "Weight-order deep-dive", "D1 then D3/D4 then D2 then D5 + Academy tracks", AMBER, True),
        ("08", "Timed mock 60/120", "Closed-book mock; night-before hit-list only", AMBER, True),
    ]
    parts = []
    parts.append(spectrum_bar(48, 36, 240, 4, "specPrep"))
    parts.append(
        f'<text x="48" y="68" font-family="{MONO}" font-size="14" fill="{VIOLET}"'
        f' letter-spacing="1.6" font-weight="600">CCAR-F  ·  PREP</text>'
    )
    parts.append(
        f'<text x="48" y="108" font-family="{SANS}" font-size="36" fill="{BONE}"'
        f' font-weight="700">Prep Sequence</text>'
    )
    parts.append(
        f'<text x="48" y="136" font-family="{SANS}" font-size="16" fill="{SUB}">'
        f'Eight ordered steps + resource shortlist</text>'
    )

    # Layout: ladder left (~720), resources right (~372)
    ladder_x = 36
    ladder_w = 720
    panel_x = 772
    panel_w = 392
    body_top = 152
    footer_top = 1105
    avail = footer_top - body_top - 4

    # Ladder
    gap_s = 6
    step_h = (avail - 7 * gap_s) // 8
    rail_x = ladder_x + 28
    parts.append(
        f'<rect x="{rail_x}" y="{body_top + 14}" width="3" height="{avail - 28}" '
        f'rx="1.5" fill="rgba(168,85,247,.35)"/>'
    )
    for i, (n, title, detail, accent, hi) in enumerate(steps):
        sy = body_top + i * (step_h + gap_s)
        cy = sy + step_h / 2
        parts.append(
            f'<circle cx="{rail_x + 1.5:.1f}" cy="{cy:.1f}" r="13" fill="{PITCH}" '
            f'stroke="{accent}" stroke-width="2.5"/>'
        )
        parts.append(
            f'<text x="{rail_x + 1.5:.1f}" y="{cy + 4:.1f}" text-anchor="middle" '
            f'font-family="{MONO}" font-size="11" fill="{accent}" font-weight="700">{n}</text>'
        )
        bx = ladder_x + 56
        bw = ladder_w - 56
        if hi:
            parts.append(
                f'<rect x="{bx}" y="{sy}" width="{bw}" height="{step_h}" rx="10" '
                f'fill="{SURFACE2}" stroke="{accent}" stroke-width="1.5"/>'
            )
            parts.append(
                f'<rect x="{bx}" y="{sy}" width="4" height="{step_h}" rx="2" fill="{accent}"/>'
            )
            tx = bx + 16
        else:
            parts.append(
                f'<rect x="{bx}" y="{sy}" width="{bw}" height="{step_h}" rx="10" '
                f'fill="{SURFACE}" stroke="{RULE}" stroke-width="1"/>'
            )
            tx = bx + 14
        parts.append(
            f'<text x="{tx}" y="{sy + step_h/2 - 6:.0f}" font-family="{SANS}" '
            f'font-size="16" fill="{BONE}" font-weight="650">{esc(title)}</text>'
        )
        dlines = wrap_text(detail, 56)
        parts.append(
            f'<text x="{tx}" y="{sy + step_h/2 + 16:.0f}" font-family="{SANS}" '
            f'font-size="13" fill="{SUB}">{esc(dlines[0])}</text>'
        )

    # Right resources panel
    parts.append(card_box(panel_x, body_top, panel_w, avail, rx=14))
    # OFFICIAL band at top of panel
    parts.append(
        f'<rect x="{panel_x}" y="{body_top}" width="{panel_w}" height="92" rx="14" '
        f'fill="{SURFACE2}"/>'
    )
    # clip bottom of official to square corners into body - redraw stroke
    parts.append(
        f'<rect x="{panel_x}" y="{body_top}" width="{panel_w}" height="92" '
        f'fill="{SURFACE2}"/>'
    )
    parts.append(
        f'<text x="{panel_x + 18}" y="{body_top + 28}" font-family="{MONO}" font-size="12" '
        f'fill="{AMBER}" font-weight="600">OFFICIAL</text>'
    )
    parts.append(
        f'<text x="{panel_x + 18}" y="{body_top + 54}" font-family="{SANS}" font-size="14" '
        f'fill="{BONE}" font-weight="600">Exam Guide v1.0 PDF</text>'
    )
    parts.append(
        f'<text x="{panel_x + 18}" y="{body_top + 76}" font-family="{SANS}" font-size="12" '
        f'fill="{MUTE}">Anthropic Partner / everpath</text>'
    )

    parts.append(
        f'<text x="{panel_x + 18}" y="{body_top + 118}" font-family="{MONO}" font-size="12" '
        f'fill="{VIOLET}" font-weight="600">UNOFFICIAL</text>'
    )
    parts.append(
        f'<text x="{panel_x + 18}" y="{body_top + 138}" font-family="{SANS}" font-size="12" '
        f'fill="{MUTE}">Verify against Guide + docs</text>'
    )

    resources = [
        ("hong-chu foundations wiki", "github.com/hong-chu/claude-certified-", "architect-foundations-llm-wiki"),
        ("paullarionov practical test", "github.com/paullarionov/claude-", "certified-architect (practical_test_en.html)"),
        ("sarveshtalele foundations", "github.com/sarveshtalele/claude-", "architect-exam-guide/.../foundations"),
        ("Certification Guide learn", "claudecertificationguide.com/learn", ""),
    ]
    ry = body_top + 158
    for name, url1, url2 in resources:
        parts.append(
            f'<rect x="{panel_x + 14}" y="{ry}" width="{panel_w - 28}" height="88" '
            f'rx="10" fill="{INPUT}"/>'
        )
        parts.append(
            f'<text x="{panel_x + 28}" y="{ry + 28}" font-family="{SANS}" font-size="14" '
            f'fill="{BONE}" font-weight="600">{esc(name)}</text>'
        )
        parts.append(
            f'<text x="{panel_x + 28}" y="{ry + 52}" font-family="{MONO}" font-size="11" '
            f'fill="{INDIGO}">{esc(url1)}</text>'
        )
        if url2:
            parts.append(
                f'<text x="{panel_x + 28}" y="{ry + 72}" font-family="{MONO}" font-size="11" '
                f'fill="{INDIGO}">{esc(url2)}</text>'
            )
        ry += 96

    parts.append(footer(cite, 1105))
    return wrap_svg("\n".join(parts))



def gen_g6():
    """PRACTICE QUESTION: large stem + proportional A-D. No answer / no WHY."""
    cite = "Exam Guide v1.0 sample questions (Anthropic)"
    parts = []
    parts.append(spectrum_bar(48, 36, 260, 4, "specQuiz"))
    parts.append(
        f'<text x="48" y="64" font-family="{MONO}" font-size="13" fill="{AMBER}"'
        f' letter-spacing="1.6" font-weight="600">PRACTICE / SAMPLE  ·  EXAM GUIDE</text>'
    )
    parts.append(
        f'<text x="48" y="100" font-family="{SANS}" font-size="32" fill="{BONE}"'
        f' font-weight="700">PRACTICE QUESTION</text>'
    )
    parts.append(
        f'<text x="48" y="126" font-family="{SANS}" font-size="14" fill="{SUB}">'
        f'Code Generation / review · Official sample - not live exam</text>'
    )

    # Stem - MUCH larger text, fills width
    # Stem sized to content; options get remaining height with matching type scale
    x, y = 36, 144
    stem = (
        "You want to create a custom /review slash command that runs your team's "
        "standard code review checklist. This command should be available to every "
        "developer when they clone or pull the repository. Where should you create "
        "this command file?"
    )
    lines = wrap_text(stem, 44)
    stem_fs = 34
    stem_lh = 44
    stem_top_pad = 62
    stem_bot_pad = 24
    # height hugs last baseline + descent + bottom pad (not an extra blank line)
    h = stem_top_pad + (len(lines) - 1) * stem_lh + int(stem_fs * 0.9) + stem_bot_pad
    w = 1128
    parts.append(card_box(x, y, w, h, rx=16))
    parts.append(
        f'<rect x="{x}" y="{y}" width="6" height="{h}" rx="3" fill="{VIOLET}"/>'
    )
    parts.append(
        f'<text x="{x + 28}" y="{y + 32}" font-family="{MONO}" font-size="14" '
        f'fill="{VIOLET}" font-weight="700">STEM</text>'
    )
    sy = y + stem_top_pad
    for line in lines:
        parts.append(
            f'<text x="{x + 28}" y="{sy}" font-family="{SANS}" font-size="{stem_fs}" '
            f'fill="{BONE}" font-weight="600">{esc(line)}</text>'
        )
        sy += stem_lh

    options = [
        ("A", "In the .claude/commands/ directory in the project repository"),
        ("B", "In ~/.claude/commands/ in each developer's home directory"),
        ("C", "In the CLAUDE.md file at the project root"),
        ("D", "In a .claude/config.json file with a commands array"),
    ]
    body_top = y + h + 16
    margin_x = 36
    gap = 10
    mark_zone = 92
    avail = 1200 - body_top - mark_zone - 4
    opt_h = (avail - 3 * gap) // 4
    for i, (letter, text_opt) in enumerate(options):
        oy = body_top + i * (opt_h + gap)
        parts.append(
            f'<rect x="{margin_x}" y="{oy}" width="{W - 2*margin_x}" height="{opt_h}" '
            f'rx="12" fill="{SURFACE}" stroke="{RULE}" stroke-width="1"/>'
        )
        parts.append(
            f'<text x="{margin_x + 28}" y="{oy + opt_h/2 + 12:.0f}" font-family="{MONO}" '
            f'font-size="36" fill="{VIOLET}" font-weight="700">{letter}</text>'
        )
        olines = wrap_text(text_opt, 42)
        nlines = min(2, len(olines))
        line_h = 34
        total_h = nlines * line_h
        start_y = oy + (opt_h - total_h) / 2 + 26
        for j, line in enumerate(olines[:2]):
            parts.append(
                f'<text x="{margin_x + 88}" y="{start_y + j * line_h:.0f}" font-family="{SANS}" '
                f'font-size="26" fill="{BONE}" font-weight="600">{esc(line)}</text>'
            )

    parts.append(footer(cite, 1108))
    return wrap_svg("\n".join(parts))


def check_bad(s: str, name: str):
    for ch in ("\u2014", "\u2013", "—", "–"):
        if ch in s:
            raise SystemExit(f"dash found in {name}: {ch!r}")



def main():
    gens = [
        ("ccarf-exam-overview", gen_g1),
        ("ccarf-domains-cheat", gen_g2),
        ("ccarf-terms-cheat", gen_g3),
        ("ccarf-scenario-cheat", gen_g4),
        ("ccarf-prep-sequence", gen_g5),
        ("ccarf-good-quiz", gen_g6),
    ]
    for name, fn in gens:
        svg = fn()
        check_bad(svg, name)
        path = OUT / f"{name}.svg"
        path.write_text(svg)
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
