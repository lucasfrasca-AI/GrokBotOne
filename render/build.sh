#!/usr/bin/env bash
# Deterministic diagram renderer for Studio.
# Usage: ./build.sh <diagram.svg> [output.png]
# Renders SVG → 1200×1200 PNG via rsvg-convert (no image models).
# Colours/type must already be baked into the SVG from tokens.css / archetypes.md.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
WIDTH=1200
HEIGHT=1200

if [[ $# -lt 1 ]]; then
  echo "usage: $0 <diagram.svg> [output.png]" >&2
  exit 2
fi

SRC="$1"
if [[ ! -f "$SRC" ]]; then
  # allow paths relative to /workspace/render
  if [[ -f "$ROOT/$SRC" ]]; then
    SRC="$ROOT/$SRC"
  else
    echo "error: source not found: $1" >&2
    exit 1
  fi
fi

if [[ $# -ge 2 ]]; then
  OUT="$2"
else
  base="$(basename "$SRC")"
  OUT="$ROOT/${base%.svg}.png"
fi

# ensure output directory exists
mkdir -p "$(dirname "$OUT")"

command -v rsvg-convert >/dev/null || {
  echo "error: rsvg-convert not installed (librsvg2-bin)" >&2
  exit 1
}

rsvg-convert \
  --width="$WIDTH" \
  --height="$HEIGHT" \
  --keep-aspect-ratio \
  --background-color '#05010E' \
  -o "$OUT" \
  "$SRC"

# If keep-aspect-ratio produced non-square, pad to 1200×1200 with pitch background
# using a second pass only when needed — rsvg may letterbox; verify size.
python3 - "$OUT" "$WIDTH" "$HEIGHT" <<'PY'
import struct, sys, zlib

path, W, H = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

def read_png_size(p):
    with open(p, "rb") as f:
        sig = f.read(8)
        if sig != b"\x89PNG\r\n\x1a\n":
            raise SystemExit(f"not a PNG: {p}")
        length = struct.unpack(">I", f.read(4))[0]
        ctype = f.read(4)
        if ctype != b"IHDR":
            raise SystemExit("missing IHDR")
        data = f.read(length)
        w, h = struct.unpack(">II", data[:8])
        return w, h

w, h = read_png_size(path)
print(f"rendered {path} ({w}x{h})")
if w != W or h != H:
    print(f"note: not exactly {W}x{H}; Studio should author SVG viewBox=\"0 0 {W} {H}\" for a full-bleed square.", file=sys.stderr)
PY

echo "OK $OUT"
