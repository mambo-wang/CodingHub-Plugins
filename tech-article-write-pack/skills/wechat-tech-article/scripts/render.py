#!/usr/bin/env python3
"""Render figure HTML -> PNG (+ phone preview) for WeChat articles.

Canvas is 480 CSS px (see fig.css). WeChat shows images at ~343pt on a phone,
so we render at 4x, trim bottom whitespace, and also emit a 686px-wide preview
under preview/ = what a retina phone actually renders. Check that preview.

Usage:
    python3 render.py [--dir DIR] [name ...]

    name   figure stem(s), e.g. p02-fig1-switch-tree (no .html suffix).
    --dir  directory holding the figure html+css (default: current directory).
    No names -> render every fig*.html / *-fig*.html in the directory.

Env:
    CHROME  override the Chrome binary path.
"""
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image

CHROME = os.environ.get(
    "CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
SCALE = 4
WINDOW = "480,2600"
PREVIEW_W = 686


def trim(path: Path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    last = 0
    for y in range(h - 1, -1, -1):
        row_has_ink = False
        for x in range(0, w, 6):
            r, g, b = px[x, y]
            if r < 248 or g < 248 or b < 248:
                row_has_ink = True
                break
        if row_has_ink:
            last = y
            break
    im = im.crop((0, 0, w, min(h, last + 1)))
    im.save(path, optimize=True)
    prev_dir = path.parent / "preview"
    prev_dir.mkdir(exist_ok=True)
    ph = round(PREVIEW_W * im.size[1] / im.size[0])
    im.resize((PREVIEW_W, ph), Image.LANCZOS).save(prev_dir / path.name)
    return im.size


def main(argv):
    base = Path.cwd()
    if argv and argv[0] == "--dir":
        if len(argv) < 2:
            sys.exit("--dir needs a value")
        base = Path(argv[1]).resolve()
        argv = argv[2:]
    if argv:
        names = argv
    else:
        names = sorted(p.stem for p in base.glob("*.html")
                       if p.stem.startswith("fig") or "-fig" in p.stem)
        # Skip preview renders naming collisions, keep order stable.
        names = [n for n in names if not n.endswith(".wechat")]
    if not names:
        sys.exit(f"no figures found in {base} (looked for fig*.html / *-fig*.html)")

    ok = fail = 0
    for name in names:
        html = base / f"{name}.html"
        if not html.exists():
            print(f"FAIL  {name}: {html} not found")
            fail += 1
            continue
        out = base / f"{name}.png"
        subprocess.run([
            CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            f"--force-device-scale-factor={SCALE}", f"--window-size={WINDOW}",
            f"--screenshot={out}", "file://" + str(html),
        ], capture_output=True)
        if not out.exists():
            print(f"FAIL  {name}")
            fail += 1
            continue
        w, h = trim(out)
        print(f"{name}.png  {w}x{h}  {out.stat().st_size // 1024} KB")
        ok += 1
    print(f"rendered {ok}, failed {fail}")
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
