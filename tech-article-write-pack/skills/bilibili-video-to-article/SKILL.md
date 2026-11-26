---
name: bilibili-video-to-article
description: 把 B 站（bilibili / b23.tv）的演讲、教程、评测视频转成有出处的中文技术长文：yt-dlp 取流、macOS Vision OCR 抽硬字幕、faster-whisper 转写无字幕视频、核对官方资料、配图、润色成稿。当用户给出 B 站链接并要求"写成文章 / 整理成文 / 转成公众号稿 / 总结这个视频"，或要把视频内容变成可发布的长文时使用。三类来源分流：有字幕轨走 yt-dlp 字幕，字幕烧进画面走 OCR，无字幕的演讲/直播走语音转写；用户提供配套 PPT 时合并为互补素材。
---

# B 站视频转技术文章

## 产出结构

```
articles/<slug>/
├── article.md
├── images/          # 截图与重绘图的 PNG/HTML
└── sources/         # 原始证据：元数据、视频、OCR、转写、官方文档
```

`<slug>` 用 `主题-来源`，例如 `lmcache-raysummit`。`sources/` 不是草稿箱，是文章里每个数字的出处，必须留档。

## 流程

### 0. 探测：先判断字幕在哪

OCR 路径依赖 `yt-dlp`、`swift`（Xcode Command Line Tools）、`python3`，不需要 ffmpeg；ASR 路径另需 faster-whisper 环境（见 `references/asr-transcription.md`）。下文 `$SKILL_DIR` 指本 skill 的绝对路径（加载时会给出）。先还原短链：

```bash
curl -L -s -o /dev/null -w '%{url_effective}\n' 'https://b23.tv/xxxx'
```

抓元数据，同时看字幕轨和可用格式：

```bash
mkdir -p articles/<slug>/sources && cd articles/<slug>/sources
yt-dlp --dump-single-json --no-playlist --no-warnings "<URL>" > bilibili-info.json 2>err.log
python3 -c "import json;d=json.load(open('bilibili-info.json'));print(d['title'],d['duration']);print('subtitles',d.get('subtitles'));[print(f['format_id'],f['ext'],f.get('vcodec'),f.get('resolution')) for f in d['formats']]"
```

分流：

- `subtitles` 非空 → `yt-dlp --write-subs --write-auto-subs --sub-langs 'zh.*,en.*' --sub-format json3`，跳到第 3 步整理时间轴。
- `subtitles` 为空（B 站常态）→ 先抽几帧看画面：字幕烧在画面里 → 走 OCR（第 1–3 步）；画面没有字幕（演讲、直播类常态）→ 走语音转写，见 `references/asr-transcription.md`（`scripts/bili2article.py` 一步完成取音轨 + 转写 + 时间戳稿）。
- 用户给了配套 PPT/讲义 → 先 `scripts/pptx_text.py` 提取文字留档，作为校对术语表与写作互补素材，流程见 `references/ppt-companion.md`。

OCR 分支下载后先抽几帧确认字幕在画面里的位置（见第 1 步末尾），再决定 OCR 区间。

### 1. 下载

视频选 480p AVC（`30032`），不要 HEVC（`30033`）：OCR 够用、解码稳、文件小。音频单独下一份，用于交叉验证和后续 ASR。

```bash
yt-dlp -f 30032 --no-warnings -o "video.%(ext)s" "<URL>"
yt-dlp -f bestaudio --no-warnings -o "audio.%(ext)s" "<URL>"
```

只有 360p 时用 `30016`。出现 403/412 是 B 站直链过期，重新 dump 元数据拿新链接再下；1080p 需要登录，通常没有必要。ASR 分支只需要音轨，`bili2article.py` 自己取，不用下视频。

下完先抽三帧，肉眼确认字幕位置、字号和是否中英双行：

```bash
swift $SKILL_DIR/scripts/extract_frames.swift video.mp4 check 60 300 600
```

### 2. 抽帧

```bash
DUR=$(python3 -c "import json;print(int(json.load(open('bilibili-info.json'))['duration']))")
TI=$(python3 -c "print(' '.join(str(x) for x in range(4,$DUR,2)))")
mkdir -p allframes
swift $SKILL_DIR/scripts/extract_frames.swift video.mp4 allframes ${=TI}
```

- 默认 2 秒一帧（34 分钟约 1000 帧）。语速快、字幕一闪而过时降到 1.5 秒。
- zsh 必须写 `${=TI}` 才会按空格拆成多个参数；bash 用 `$TI`。
- 幻灯片单独抽到 `slides/`，只抽内容切换的时间点，不要全量。
- OCR 用 480p 全帧即可，不要为了认字幕去下 1080p。

### 3. OCR 并生成转写

画面无字幕的视频不走本节，走 `references/asr-transcription.md`；产出同样是带时间戳的转写稿，第 4 步之后两条路径一致。

```bash
swift $SKILL_DIR/scripts/ocr_frames.swift allframes ocr-all.json
python3 $SKILL_DIR/scripts/ocr_to_transcript.py ocr-all.json \
  --out-zh transcript-zh.txt --out-bilingual transcript-bilingual.txt
```

- Vision 坐标系原点在左下角，`y` 越大越靠上。默认字幕带 `y<0.21`，中文 `0.055–0.21`，英文 `y<0.06`。
- 位置不对先用 `--probe` 看 y 分布，再调 `--band-max / --zh-min / --zh-max / --en-max`。
- 相邻帧重复行会自动折叠，输出是"一条字幕一行"，不是逐字时间轴。
- 1000 帧大约几分钟，放后台跑，定期看进度输出（每 50 帧一行 stderr）。

### 4. 校对转写（不可跳过）

OCR 结果不是逐字稿，错字和漏行都正常。至少做三件事：

1. **抽读**：按 2 分钟间隔分段读一遍，确认没有整段丢失（字幕切换、画面遮挡容易漏行）。
2. **关键数字回帧**：要写进文章的每个数字（吞吐、延迟、倍数、显存、版本号），用 `extract_frames.swift` 抽对应时间的原帧核对。OCR 常把 `1/l` 认成 `1/1`、`O.5` 认成 `0.5`。
3. **术语归一**：`VLLM`→vLLM、`Lmcache`→LMCache、`preflll`→prefill，统一改在 `transcript-zh.txt`，保留时间戳。

ASR 转写稿另有多轮归一流程（繁简顺序、词边界、复合词优先、raw 留档），见 `references/asr-transcription.md`。两条路径共同的一条：引用讲者原话前按时间戳回查转写稿，未解码的词保留原样并在台账注明。

### 5. 补齐外部资料

视频会省略口径，也会过期。逐项核对并落到 `sources/`：

- 官方文档，优先 `llms.txt` / `llms-full.txt` 这类给 LLM 的版本
- README、release notes、PyPI / npm 当前版本
- 论文、官方博客（有测试口径时优先于转写）
- 与视频说法冲突的第三方资料

网页存 HTML 和纯文本两份，`$SKILL_DIR/scripts/html2text.py` 可转。维护事实台账：

| 事实 | 值 | 来源 | 视频时间 | 状态 |
| --- | --- | --- | --- | --- |

规则：

- 每个数字都要有来源；没有来源的推算标"按公开配置估算"，并写明假设。
- 区分"演讲者说的"和"文档/实测写的"。视频基准如果用的是旧版本，必须在文中点明。
- 版本、star 数这类会变的事实，写查询日期，不写"目前最新"。

### 6. 写作

技术演讲常用结构：

1. 一个具体场景或数字开场
2. 没有它之前是什么样，它解决什么问题
3. 怎么工作（分层讲，配架构图）
4. 关键机制（时序、粒度、调度）
5. 效果与测试口径
6. 边界与坑：什么时候不该用
7. 结论

写作要求：

- 口语化解释技术，但比喻之后要落回真实机制，不靠比喻下结论。
- 保留演讲者的限定词（"在我们的测试里""大约"），不把"可能"写成"一定"。
- 来源分清：视频截图标注时间点；重绘的图注明"依据演讲/论文重绘，不是原始截图"。
- 不写"赋能、闭环、至关重要"这类词，留给润色阶段统一清理。

### 7. 配图

- 用 `diagram-design` skill 出 HTML + 内联 SVG，再导出 PNG；不要直接贴 Mermaid 渲染结果。
- 一张图只讲一个机制，超过 9 个节点就拆图。
- 图放在对应段落之后，图注写"这张图说明了什么"，而不是"架构图"三个字。
- 视频原截图用于基准数据、幻灯片结论、界面操作；示意图用于架构、时序、流程。

### 8. 润色与交付

- 用 `humanizer-zh` 对全文润色：保留全部事实、数字、来源和口语化解释，只去掉模板腔和过度拔高。
- 润色后逐条回查：数字、否定、限定、时间、归因有没有被改掉。
- 机械复查：`python3 $SKILL_DIR/scripts/check_article.py article.md --transcript <转写稿>`，时间戳全部可回查、图片引用存在、链接格式合法才算过。有配套 PPT 的，再做逐页覆盖核对（`references/ppt-companion.md`）。
- 交付 `article.md` + `images/` + `sources/`。
- 用户明确要求时才推 IMA：用 `ima-skill` 的 notes 模块，`import_doc` 新建，`note-images.cjs` 内嵌图片；推知识库要先确认。

## 常见故障

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `subtitles: {}` | B 站没有字幕轨 | 先抽帧确认字幕在画面里；没有则转 ASR 分支 |
| 画面无硬字幕可 OCR | 演讲/直播类视频 | 走 `references/asr-transcription.md` |
| 下载 403/412 | 直链过期 | 重新 dump 元数据再下 |
| OCR 结果全空 | 字幕不在画面或 y 区间不对 | 肉眼看帧，`--probe` 调区间 |
| OCR 很慢 | 1000+ 帧逐帧识别 | 后台跑，只 OCR 字幕带 |
| 转写漏段 | 采样间隔太大 | 缺失区间降到 1–1.5 秒重跑 |
| 数字被认错 | Vision 对细字体不敏感 | 回帧核对，以幻灯片和官方文档为准 |
| `${=TI}` 报错 | 用了 bash | bash 写 `$TI` |

## 平台差异

- OCR 依赖 macOS Vision（`swift` 直接调用），Linux / Windows 不可用。
- ASR 分支用 faster-whisper（CPU int8），跨平台可用；环境、模型下载通路与校对规则见 `references/asr-transcription.md`。
- 有字幕轨的视频跳过 OCR 与 ASR，直接 `yt-dlp --write-subs`。

## 资源

- `scripts/bili2article.py` — B 站取流 + faster-whisper 转写一步完成，输出时间戳稿（ASR 分支）
- `scripts/pptx_text.py` — PPTX 每页文字提取，stdlib 实现（配套 PPT 分支）
- `scripts/check_article.py` — 交付前复查：时间戳回查、图片引用、链接格式
- `scripts/extract_frames.swift` — AVFoundation 按时间点抽帧
- `scripts/ocr_frames.swift` — Vision 中英 OCR，输出带坐标的 JSON
- `scripts/ocr_to_transcript.py` — 按字幕带过滤、折叠重复、输出中英转写
- `scripts/html2text.py` — 网页存档转纯文本
- `references/asr-transcription.md` — 无字幕视频的转写与多轮校对流程
- `references/ppt-companion.md` — 配套 PPT 的提取、互补写作与覆盖核对
