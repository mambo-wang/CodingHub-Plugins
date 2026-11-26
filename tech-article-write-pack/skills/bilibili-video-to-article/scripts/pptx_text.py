#!/usr/bin/env python3
"""提取 PPTX 每页文字（stdlib，无需 python-pptx）。

用法：
  python3 pptx_text.py deck.pptx [deck2.pptx ...] [--out-dir DIR]

每个输入产出 <文件名>-slides.md：按页列出文本框/表格文字，段落一行。
只读 ppt/slides/slideN.xml 的 <a:t>；图片、图表里的数字提不出来，
需要时回原幻灯片截图核对。
"""
import argparse
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"


def slide_text(xml_bytes):
    root = ET.fromstring(xml_bytes)
    paras = []
    for p in root.iter(A + "p"):
        runs = [t.text or "" for t in p.iter(A + "t")]
        line = "".join(runs).strip()
        if line:
            paras.append(line)
    return paras


def extract(path, out_dir):
    with zipfile.ZipFile(path) as z:
        slides = [n for n in z.namelist()
                  if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)]
        slides.sort(key=lambda n: int(re.search(r"\d+", n).group()))
        stem = os.path.splitext(os.path.basename(path))[0]
        out = os.path.join(out_dir, stem + "-slides.md")
        lines = [f"# {stem}（共 {len(slides)} 页）", ""]
        for i, name in enumerate(slides, 1):
            lines.append(f"## Slide {i}")
            lines.append("")
            lines.extend(slide_text(z.read(name)))
            lines.append("")
        with open(out, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    print(f"{path} -> {out}（{len(slides)} 页）")
    return out


def main():
    ap = argparse.ArgumentParser(description="PPTX 每页文字提取")
    ap.add_argument("pptx", nargs="+")
    ap.add_argument("--out-dir", default=".", help="输出目录，默认当前目录")
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    for p in args.pptx:
        if not os.path.exists(p):
            sys.exit(f"文件不存在：{p}")
        extract(p, args.out_dir)


if __name__ == "__main__":
    main()