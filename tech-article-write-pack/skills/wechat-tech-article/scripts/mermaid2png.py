#!/usr/bin/env python3
"""Render a mermaid (.mmd) source file to a house-style PNG figure.

The .mmd file carries optional metadata as leading comments:

    %%cap:   图 4
    %%title: 主标题，<span>蓝色后半句</span>
    %%lede:  一句副题（可省）
    %%foot:  底部收束句（可省）

Everything else is mermaid source (sequenceDiagram / flowchart / ...). The
output keeps the series figure frame (fig.css: cap / h1 / lede / foot on a
480 CSS px canvas) with the diagram drawn by the same engine mermaid-cli
uses (mermaid.js) running in local Chrome -- no Node needed at run time.

Usage:
    python3 mermaid2png.py [--dir DIR] name1 [name2 ...]   # -> name1.png + preview
    python3 mermaid2png.py [--dir DIR]                     # render every *.mmd in DIR

Env: CHROME overrides the Chrome binary path.
"""
import os
import re
import subprocess
import sys
import glob as _glob

from PIL import Image

CHROME = os.environ.get(
    "CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)
SCALE = 4
WINDOW = "480,2600"          # same canvas as render.py (fig.css is 480 CSS px)
PREVIEW_W = 686              # 343pt phone width x2
BUILD_DIR = "/tmp/mmd-build"  # self-contained temp pages, kept for debugging

# House theme: same palette as the hand-drawn figures (fig.css / fig-template).
MERMAID_INIT = """\
mermaid.initialize({
  startOnLoad: true,
  securityLevel: 'loose',
  theme: 'base',
  themeVariables: {
    fontFamily: '-apple-system, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif',
    fontSize: '15px',
    primaryColor: '#f7faff',
    primaryBorderColor: '#dbe4f0',
    primaryTextColor: '#1a1f2e',
    lineColor: '#9aa4b5',
    textColor: '#1a1f2e',
    actorBkg: '#eef4ff',
    actorBorder: '#bfd3f2',
    actorTextColor: '#1a5fb8',
    actorLineColor: '#d8e0ec',
    signalColor: '#5a6478',
    signalTextColor: '#1a1f2e',
    labelBoxBkgColor: '#fffaf3',
    labelBoxBorderColor: '#e0d3c0',
    labelTextColor: '#a35a12',
    loopTextColor: '#a35a12',
    activationBorderColor: '#1f6feb',
    activationBkgColor: '#dbe9ff',
    noteBkgColor: '#fffaf3',
    noteBorderColor: '#e0d3c0',
    noteTextColor: '#5a6478'
  },
  sequence: {
    useMaxWidth: true,
    mirrorActors: false,
    showSequenceNumbers: false,
    actorFontSize: 16,
    actorFontWeight: 700,
    noteFontSize: 15,
    messageFontSize: 15,
    messageAlign: 'center',
    noteMargin: 8,
    messageMargin: 26,
    actorMargin: 34,
    boxMargin: 6,
    boxTextMargin: 4,
    diagramMarginX: 8,
    diagramMarginY: 6,
    height: 40,
    width: 118
  }
});
"""

CSS_EXTRA = """
  .mmd { margin-top: 2px; }
  .mmd svg { display: block; margin: 0 auto; }
"""


def parse_mmd(path):
    meta, body = {}, []
    for line in open(path, encoding="utf-8"):
        m = re.match(r"%%(cap|title|lede|foot):\s*(.*?)\s*$", line)
        if m:
            meta[m.group(1)] = m.group(2)
        else:
            body.append(line)
    return meta, "".join(body).strip()


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_html(meta, source, fig_css, mermaid_js):
    frame = []
    if meta.get("cap"):
        frame.append('<div class="cap">%s</div>' % meta["cap"])
    if meta.get("title"):
        frame.append("<h1>%s</h1>" % meta["title"])
    if meta.get("lede"):
        frame.append('<div class="lede">%s</div>' % meta["lede"])
    frame.append('<pre class="mermaid mmd">%s</pre>' % esc(source))
    if meta.get("foot"):
        frame.append('<div class="foot">%s</div>' % meta["foot"])
    return (
        '<!DOCTYPE html>\n<html lang="zh-CN"><head><meta charset="utf-8">\n'
        "<style>" + fig_css + CSS_EXTRA + "</style></head><body>\n"
        + "\n".join(frame) + "\n"
        + "<script>" + mermaid_js + "</script>\n"
        + "<script>" + MERMAID_INIT + "</script>\n"
        + "</body></html>\n"
    )


def trim(path, prev_dir):
    """Crop bottom whitespace; write the 686px phone preview. Same as render.py."""
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
    os.makedirs(prev_dir, exist_ok=True)
    ph = round(PREVIEW_W * im.size[1] / im.size[0])
    im.resize((PREVIEW_W, ph), Image.LANCZOS).save(
        os.path.join(prev_dir, os.path.basename(path))
    )
    return im.size


def main(argv):
    args = argv[1:]
    d = "."
    if args[:1] == ["--dir"]:
        d, args = args[1], args[2:]
    if not args:
        args = sorted(
            os.path.basename(p)[:-4] for p in _glob.glob(os.path.join(d, "*.mmd"))
        )
    if not args:
        sys.exit("no .mmd files found in " + os.path.abspath(d))

    fig_css = open(os.path.join(d, "fig.css"), encoding="utf-8").read()
    mermaid_js = open(os.path.join(d, "mermaid.min.js"), encoding="utf-8").read()
    os.makedirs(BUILD_DIR, exist_ok=True)

    ok = 0
    for name in args:
        name = name[:-4] if name.endswith(".mmd") else name
        src = os.path.join(d, name + ".mmd")
        if not os.path.exists(src):
            print("FAIL  %s (.mmd not found)" % name, file=sys.stderr)
            continue
        meta, source = parse_mmd(src)
        html_path = os.path.join(BUILD_DIR, name + ".render.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(build_html(meta, source, fig_css, mermaid_js))
        out = os.path.join(d, name + ".png")
        subprocess.run(
            [
                CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                "--force-device-scale-factor=%d" % SCALE,
                "--window-size=%s" % WINDOW,
                "--virtual-time-budget=10000",
                "--screenshot=" + out,
                "file://" + html_path,
            ],
            capture_output=True,
        )
        if not os.path.exists(out):
            print(
                "FAIL  %s (no screenshot; page kept at %s)" % (name, html_path),
                file=sys.stderr,
            )
            continue
        w, h = trim(out, os.path.join(d, "preview"))
        kb = os.path.getsize(out) // 1024
        print("%s.png  %dx%d  %d KB" % (name, w, h, kb))
        ok += 1
    print("rendered %d, failed %d" % (ok, len(args) - ok))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
