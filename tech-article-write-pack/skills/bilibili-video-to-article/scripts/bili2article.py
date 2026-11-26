#!/usr/bin/env python3
"""B 站视频 -> 文字稿（可再交给 LLM 写文章）。

流程：
  1. 调 B 站公开 API 取标题/简介/分 P
  2. 有字幕（UP 上传的 CC 字幕）就直接下字幕，不跑 ASR
  3. 没字幕就下 DASH 音轨 -> afconvert 转 16k 单声道 wav -> faster-whisper 转写
  4. 输出 <标题>.md（带时间戳）和 <标题>.prompt.md（交给 LLM 写文章的提示词）

用法：
  python bili2article.py BV1xxxxxxxxx
  python bili2article.py "https://www.bilibili.com/video/BV1xxxxxxxxx?p=2"
  python bili2article.py BV1xxxxxxxxx --page all --model small
"""
import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36")
HOME = "https://www.bilibili.com/"


def api(url, referer=HOME):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": referer})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("code") != 0:
        raise RuntimeError(f"API 失败 {data.get('code')}: {data.get('message')} ({url})")
    return data["data"]


def download(url, path, referer=HOME, retries=3):
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": referer})
            with urllib.request.urlopen(req, timeout=120) as r, open(path + ".part", "wb") as f:
                while chunk := r.read(1 << 20):
                    f.write(chunk)
            os.replace(path + ".part", path)
            return path
        except Exception as e:
            if i == retries - 1:
                raise
            print(f"  下载失败({e})，重试 {i + 1}/{retries} ...")
            time.sleep(3)


def parse_target(arg):
    m = re.search(r"(BV[0-9A-Za-z]{10})", arg)
    if not m:
        sys.exit("没找到 BV 号，请贴完整链接或 BV 号")
    bvid = m.group(1)
    pm = re.search(r"[?&]p=(\d+)", arg)
    return bvid, int(pm.group(1)) if pm else None


def fmt_ts(sec):
    sec = int(sec)
    return f"{sec // 60:02d}:{sec % 60:02d}"


def srt_ts(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def get_subtitles(bvid, cid):
    """拿到 UP 主上传的字幕列表（无需登录）。AI 字幕需要 cookie，这里不处理。"""
    try:
        d = api(f"https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}")
    except Exception:
        return []
    subs = (d.get("subtitle") or {}).get("subtitles") or []
    # 中文优先
    subs.sort(key=lambda s: (not str(s.get("lan", "")).startswith("zh"), s.get("lan", "")))
    return subs


def fetch_subtitle(url):
    if url.startswith("//"):
        url = "https:" + url
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": HOME})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = json.load(r).get("body", [])
    return [(float(x["from"]), float(x["to"]), x["content"].strip()) for x in body]


def download_audio(bvid, cid, out_dir):
    path = os.path.join(out_dir, f"{bvid}_{cid}.m4a")
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path
    d = api(f"https://api.bilibili.com/x/player/playurl?bvid={bvid}&cid={cid}&fnval=16&fourk=1",
            f"https://www.bilibili.com/video/{bvid}")
    audio = (d.get("dash") or {}).get("audio") or []
    if not audio:
        raise RuntimeError("没拿到 DASH 音轨（可能是付费/番剧/地区限制）")
    best = max(audio, key=lambda x: x.get("bandwidth", 0))
    print(f"  音轨 {best.get('bandwidth', 0) // 1000} kbps, {best['baseUrl'].split('?')[0].rsplit('/', 1)[-1]}")
    return download(best["baseUrl"], path, f"https://www.bilibili.com/video/{bvid}")


def to_wav(m4a, out_dir):
    wav = os.path.splitext(m4a)[0] + "_16k.wav"
    if os.path.exists(wav):
        return wav
    # afconvert 是 macOS 自带，不需要装 ffmpeg
    subprocess.run(["afconvert", "-f", "WAVE", "-d", "LEI16@16000", "-c", "1", m4a, wav],
                   check=True)
    return wav


def read_wav(path):
    """直接读 16k 单声道 wav 成 float32，绕开 PyAV（新版 PyAV 与 faster-whisper 有兼容问题）。"""
    import wave as _wave
    import numpy as np
    with _wave.open(path) as w:
        assert w.getframerate() == 16000 and w.getnchannels() == 1, "wav 需要 16k 单声道"
        raw = w.readframes(w.getnframes())
    return np.frombuffer(raw, dtype="<i2").astype(np.float32) / 32768.0


def ensure_model(model_arg):
    """传 small/medium 这类名字时，从 ModelScope 拉模型（国内速度正常）。"""
    sizes = {"tiny", "base", "small", "medium", "large-v3"}
    if os.path.isdir(model_arg) or model_arg not in sizes:
        if not os.path.exists(model_arg):
            sys.exit(f"模型路径不存在：{model_arg}")
        return model_arg
    local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", model_arg)
    if os.path.exists(os.path.join(local, "model.bin")):
        return local
    os.makedirs(local, exist_ok=True)
    repo = f"Systran/faster-whisper-{model_arg}"
    print(f"首次使用，从 ModelScope 下载 {repo} ...")
    for f in ("config.json", "tokenizer.json", "vocabulary.txt", "model.bin"):
        url = (f"https://www.modelscope.cn/api/v1/models/{repo}/repo"
               f"?Revision=master&FilePath={f}")
        download(url, os.path.join(local, f), retries=2)
    return local


def transcribe(wav, model_path, language, hint=None):
    from faster_whisper import WhisperModel
    model = WhisperModel(model_path, device="cpu", compute_type="int8", cpu_threads=8)
    audio = read_wav(wav)
    for use_vad in (True, False):
        segs, info = model.transcribe(
            audio,
            language=None if language == "auto" else language,
            beam_size=5,
            vad_filter=use_vad,
            condition_on_previous_text=False,
            initial_prompt=hint or None,
        )
        out, last = [], 0.0
        for s in segs:
            text = s.text.strip()
            if text:
                out.append((s.start, s.end, text))
                if s.end - last > 60:
                    print(f"  ... {fmt_ts(s.end)} / {fmt_ts(info.duration)}", flush=True)
                    last = s.end
        if out:
            return out, info
        print("  VAD 切完没有内容，关掉 VAD 重试 ...")
    return [], info


def write_outputs(out_dir, meta, segs, source, elapsed):
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.join(out_dir, meta["file_stem"])
    lines = [
        f"# {meta['title']}",
        "",
        f"- 链接：{meta['url']}",
        f"- UP 主：{meta['owner']}",
        f"- 时长：{fmt_ts(meta['duration'])}",
        f"- 来源：{source}（耗时 {elapsed:.0f}s）",
        f"- 简介：{meta['desc'][:300].replace(chr(10), ' ')}",
        "",
        "## 逐句文字稿",
        "",
    ]
    lines += [f"[{fmt_ts(s)}] {t}" for s, _, t in segs]
    with open(base + ".md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    with open(base + ".srt", "w", encoding="utf-8") as f:
        for i, (s, e, t) in enumerate(segs, 1):
            f.write(f"{i}\n{srt_ts(s)} --> {srt_ts(e)}\n{t}\n\n")

    plain = "\n".join(t for _, _, t in segs)
    with open(base + ".txt", "w", encoding="utf-8") as f:
        f.write(plain + "\n")

    prompt = f"""下面是一期 B 站视频的完整文字稿（自动转写，可能有错别字和断句问题）。

请先在心里纠正明显的同音错字（例如技术术语、人名、产品名），不要逐句复述，然后写成一篇结构完整的中文文章：
1. 一句话概括视频讲了什么，再给 3-5 条核心结论；
2. 按视频的逻辑主线分节展开，补充必要的背景，让没看过视频的人也能看懂；
3. 保留具体数字、步骤、踩坑点和对比结论，不要写成空洞的摘要；
4. 结尾给一段"适合谁看/看完能做什么"；
5. 用 Markdown，小标题不超过三级，不要用"首先/其次/最后"这类套话。

视频标题：{meta['title']}
UP 主：{meta['owner']}

--- 文字稿开始 ---
{plain}
--- 文字稿结束 ---
"""
    with open(base + ".prompt.md", "w", encoding="utf-8") as f:
        f.write(prompt)
    return base


def main():
    ap = argparse.ArgumentParser(description="B 站视频转文字稿")
    ap.add_argument("target", help="视频链接、BV 号，或带 ?p=N 的链接")
    ap.add_argument("--page", default="1", help="分 P：1、2... 或 all（默认 1）")
    ap.add_argument("--out", default="output", help="输出目录")
    ap.add_argument("--model", default="small",
                    help="faster-whisper 模型名（tiny/base/small/medium/large-v3）或本地目录")
    ap.add_argument("--lang", default="zh", choices=["zh", "en", "auto"])
    ap.add_argument("--hint", default="",
                    help="术语提示，例如 'DeepSeek 扣子 Coze 智能体 插件 工作流'，能明显减少专有名词错字")
    ap.add_argument("--subs-only", action="store_true", help="只取字幕，没有就退出，不跑 ASR")
    args = ap.parse_args()
    args.model = ensure_model(args.model)

    bvid, p_in_url = parse_target(args.target)
    view = api(f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}")
    pages = view["pages"]
    url = f"https://www.bilibili.com/video/{bvid}"
    print(f"《{view['title']}》 {view['owner']['name']} · {len(pages)} P")

    if args.page == "all":
        todo = list(range(1, len(pages) + 1))
    else:
        todo = [int(args.page) if p_in_url is None else p_in_url]
    for pno in todo:
        if not 1 <= pno <= len(pages):
            sys.exit(f"没有第 {pno} P")
        page = pages[pno - 1]
        title = view["title"] if len(pages) == 1 else f"{view['title']}_P{pno}_{page['part']}"
        stem = re.sub(r'[\\/:*?"<>|\n\r]+', "_", title)[:80]
        meta = {
            "title": title,
            "url": f"{url}?p={pno}" if len(pages) > 1 else url,
            "owner": view["owner"]["name"],
            "duration": page["duration"],
            "desc": view.get("desc", ""),
            "file_stem": stem,
        }
        os.makedirs(args.out, exist_ok=True)
        t0 = time.time()

        segs, source = [], ""
        subs = get_subtitles(bvid, page["cid"])
        if subs:
            print(f"  P{pno} 发现字幕：{subs[0].get('lan_doc') or subs[0].get('lan')}")
            try:
                segs = fetch_subtitle(subs[0]["subtitle_url"])
                source = f"UP 字幕 {subs[0].get('lan_doc') or subs[0].get('lan')}"
            except Exception as e:
                print(f"  字幕下载失败：{e}")

        if not segs:
            if args.subs_only:
                print(f"  P{pno} 没有可下载的字幕")
                continue
            m4a = download_audio(bvid, page["cid"], os.path.join(args.out, "audio"))
            wav = to_wav(m4a, args.out)
            print(f"  转写中（{fmt_ts(meta['duration'])} 音频，CPU）...", flush=True)
            segs, info = transcribe(wav, args.model, args.lang, args.hint)
            source = f"whisper {os.path.basename(args.model)}（检测语言 {info.language} {info.language_probability:.2f}）"

        base = write_outputs(args.out, meta, segs, source, time.time() - t0)
        print(f"  -> {base}.md ({len(segs)} 段)")


if __name__ == "__main__":
    main()
