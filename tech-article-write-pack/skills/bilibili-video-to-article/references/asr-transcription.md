# 无字幕视频：faster-whisper 语音转写分支

适用：没有字幕轨、画面里也没有烧录字幕的视频（演讲、直播、配音教程）。
产出与 OCR 分支相同——带 `[mm:ss]` 时间戳的转写稿，主流程第 4 步之后完全一致。

## 环境

```bash
python3 -m venv .venv
.venv/bin/pip install faster-whisper zhconv
```

系统 python 有 PEP668 限制，必须用 venv。验证过的组合：Python 3.13 +
faster-whisper 1.2.1（ctranslate2 4.8.3）+ zhconv 1.4.3，CPU int8 推理，无需 GPU。
音频转码用 macOS 自带 `afconvert`，不需要 ffmpeg。

## 一步转写：scripts/bili2article.py

```bash
.venv/bin/python $SKILL_DIR/scripts/bili2article.py BV1xxxxxxxxx \
  --model small --lang zh --hint "vLLM LMCache Mooncake KV cache connector prefill"
```

脚本自动完成：B 站 API 取元数据/分 P → 检查 UP 主 CC 字幕（有就直接下，不跑 ASR）
→ DASH 音轨下载 → afconvert 转 16k 单声道 wav → faster-whisper 转写
→ 输出 `<标题>.md`（逐句带时间戳）、`.srt`、`.txt`、`.prompt.md`。
支持 `--page all` 一次转全部 P。

- **模型**：首次使用自动从 ModelScope 下载 `Systran/faster-whisper-<size>`
  到脚本同级的 `models/`（HF 直连被墙时的可用通路）。已有模型用
  `--model /path/to/models/small` 复用，例如 `~/WORK_bili2article/models/small`。
- **--hint 术语提示**：把视频主题的产品名、组件名、API 名喂进去，
  能明显减少专有名词同音错字。有配套 PPT 时从 PPT 提取稿抄术语表。
- **耗时预期**：125 分钟音频，small + int8 + 8 线程 CPU 约 29 分钟
  （约 0.23× 实时）。放后台跑，脚本每 60 秒音频打一行进度。
- 关键参数已内置，改之前先懂为什么：`condition_on_previous_text=False`
  防重复循环与幻觉扩散；VAD 过滤后若整段为空自动关 VAD 重试；
  直接读 wav 绕开 PyAV 与 faster-whisper 的兼容问题。

## 留档

转写原件（未校对）整体拷进 `sources/raw-asr-<BV号>/`，校对只改副本。
文章里每个数字、每句引文的最终出处是校对后的转写稿，raw 是对照依据。

## 多轮术语校对（不可跳过）

whisper small 的中文技术内容错字率高，一遍替换不够。本次实例：
四轮、约 300 条规则，脚本见 `~/WORK_bili2article/normalize_final.py`
（pass1/2 脚本同目录），每条规则依据 PPT 术语表 + 逐处上下文人工判读。

规则脚本的写法要点：

1. **繁简转换先行**（zhconv），否则繁体段漏网。
2. **复合短语先于单词**：`mukicstoreconnector → MooncakeStoreConnector`
   必须排在 `mukic → Mooncake` 之前，否则被截胡。
3. **中文替换不能用 ASCII `\b` 词边界**：中文与英文粘连时 `\b` 失效。
   用环视：`(?<![A-Za-z0-9])词(?![A-Za-z0-9])`，中文字符算边界。
4. **逐处判读，不盲改**：同音词在不同上下文可能对应不同术语；
   拿不准的保留原样，在事实台账标"未解码，引用须回听原视频"。
5. **时间戳一律不动**：只改文字，不合并、不重排段落。

校对后按 2 分钟间隔抽读一遍，确认没有整段丢失。whisper 在静音/音乐处
会重复或幻觉出整句：raw 里的重复段保留原样并做标记，文章不得引用这些段。

## 引文与数字核对

- 文章引用讲者原话前，按时间戳回查校对稿确认原文；时间点写错是常见事故
  （凭印象写"[62:00 附近]"，实际在 [61:09]）。交付前跑
  `scripts/check_article.py article.md --transcript <校对稿>` 机械回查全部时间戳。
- 要写进文章的数字（吞吐、延迟、显存、版本号、PR 号）不信任 ASR：
  对照幻灯片、官方文档核实；讲者自己说不准的（"好像是 45 开头"）保留不确定语气。

## 故障表

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| VAD 切完没有内容 | 音量低/背景音乐 | 脚本自动关 VAD 重试；仍为空则检查音轨 |
| 整句重复循环 | 上下文条件解码 | 已内置 `condition_on_previous_text=False`；raw 重复段标记不引用 |
| 专有名词全错 | 无术语提示 | `--hint` + PPT 术语表多轮归一 |
| 繁体段替换漏网 | 替换先于繁简转换 | zhconv 放第一步 |
| 中文规则不生效 | 用了 `\b` 边界 | 改环视边界 |
| 模型下载失败 | HF 直连被墙 | 脚本走 ModelScope；或 `--model` 指本地目录 |
| PyAV 报错 | 版本兼容 | 脚本直接读 16k wav，不经 PyAV |