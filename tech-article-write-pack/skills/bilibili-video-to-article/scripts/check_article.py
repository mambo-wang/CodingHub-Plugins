#!/usr/bin/env python3
"""交付前机械复查：时间戳可回查、图片引用存在、链接格式合法。

用法：
  python3 check_article.py article.md [--transcript 转写稿.md]

时间戳形如 [12:34] 或 [1:02:03]；给了 --transcript 就逐个回查，
查不到即失败（引用讲者原话前必须能在转写稿中定位）。
"""
import argparse
import os
import re
import sys


def main():
    ap = argparse.ArgumentParser(description="文章交付前复查")
    ap.add_argument("article")
    ap.add_argument("--transcript", help="带时间戳的转写稿，用于回查引用时间点")
    args = ap.parse_args()

    art = open(args.article, encoding="utf-8").read()
    base = os.path.dirname(os.path.abspath(args.article))
    fails = []

    ts = sorted(set(re.findall(r"\[(\d{1,3}:\d{2}(?::\d{2})?)\]", art)))
    if args.transcript:
        trans = open(args.transcript, encoding="utf-8").read()
        missing = [t for t in ts if f"[{t}]" not in trans]
        if missing:
            fails.append(f"时间戳在转写稿中找不到：{missing}")
    print(f"时间戳 {len(ts)} 个" + ("，全部可回查" if args.transcript and not fails else ""))

    imgs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", art)
    local = [p for p in imgs if not p.startswith(("http://", "https://"))]
    gone = [p for p in local if not os.path.exists(os.path.join(base, p))]
    if gone:
        fails.append(f"图片文件缺失：{gone}")
    print(f"图片引用 {len(imgs)} 个，本地文件齐全" if not gone else f"图片引用 {len(imgs)} 个")

    links = re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", art)
    bad = [u for u in links if not re.match(r"^(https?://|file://|#|/|\./)", u)]
    if bad:
        fails.append(f"链接格式可疑：{bad}")
    print(f"链接 {len(links)} 个")

    if fails:
        print("\n失败：")
        for f in fails:
            print(" -", f)
        sys.exit(1)
    print("复查通过")


if __name__ == "__main__":
    main()