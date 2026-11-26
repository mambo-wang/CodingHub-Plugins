#!/usr/bin/env python3
"""Turn Vision OCR frame results into timestamped transcripts.

Input is the JSON written by ocr_frames.swift: [{"t": seconds, "lines": [...]}].
Vision boxes use a bottom-left origin, so larger y means higher on screen.
Hard subtitles usually sit in the lower band, Chinese above English.
"""

import argparse
import json
import re
import sys

CJK = re.compile(r"[\u4e00-\u9fff]")


def is_zh(text):
    return bool(CJK.search(text))


def fmt_ts(seconds):
    s = int(seconds)
    return f"[{s // 60:02d}:{s % 60:02d}]"


def probe(frames, limit):
    ys = []
    for frame in frames[:limit]:
        ys.extend(round(line["y"], 2) for line in frame["lines"])
    if not ys:
        print("no OCR lines found")
        return
    buckets = {}
    for y in ys:
        buckets[y // 0.02 * 0.02] = buckets.get(y // 0.02 * 0.02, 0) + 1
    print(f"lines={len(ys)} frames={min(limit, len(frames))}")
    for bucket in sorted(buckets):
        print(f"  y {bucket:.2f}-{bucket + 0.02:.2f}: {buckets[bucket]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ocr_json")
    ap.add_argument("--out-zh", default="transcript-zh.txt")
    ap.add_argument("--out-bilingual", default="transcript-bilingual.txt")
    ap.add_argument("--band-max", type=float, default=0.21,
                    help="ignore lines above this y (slide body)")
    ap.add_argument("--zh-min", type=float, default=0.055)
    ap.add_argument("--zh-max", type=float, default=0.21)
    ap.add_argument("--en-max", type=float, default=0.06)
    ap.add_argument("--min-conf", type=float, default=0.0,
                    help="drop noisy lines; 0.3 helps on bad video, but can eat valid subtitles")
    ap.add_argument("--probe", action="store_true",
                    help="print y distribution of the first 5 frames and exit")
    args = ap.parse_args()

    frames = json.load(open(args.ocr_json, encoding="utf-8"))
    if args.probe:
        probe(frames, 5)
        return

    rows = []
    for frame in frames:
        t = frame["t"]
        lines = [l for l in frame["lines"]
                 if l["y"] < args.band_max and l.get("conf", 1) >= args.min_conf]
        lines.sort(key=lambda l: -l["y"])  # Vision y grows upward: top line first
        zh = [l["text"].strip() for l in lines
              if args.zh_min <= l["y"] < args.zh_max and is_zh(l["text"])]
        en = [l["text"].strip() for l in lines
              if l["y"] < args.en_max and not is_zh(l["text"])]
        rows.append((t, " ".join(zh), " ".join(en)))

    out, last = [], None
    for t, zh, en in rows:
        if zh != last:
            out.append((t, zh, en))
            last = zh

    with open(args.out_zh, "w", encoding="utf-8") as f:
        for t, zh, _ in out:
            if zh:
                f.write(f"{fmt_ts(t)} {zh}\n")

    with open(args.out_bilingual, "w", encoding="utf-8") as f:
        for t, zh, en in out:
            if zh or en:
                f.write(f"{fmt_ts(t)} {zh}\n")
                if en:
                    f.write(f"            {en}\n")

    utterances = sum(1 for _, zh, _ in out if zh)
    print(f"frames={len(frames)} utterances={utterances} collapses={len(out)}")
    if not utterances:
        sys.exit("no Chinese subtitle lines matched; rerun with --probe to tune the band")


if __name__ == "__main__":
    main()
