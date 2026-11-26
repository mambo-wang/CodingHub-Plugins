---
name: tool-review-writer
description: 编排 doc-coauthoring、diagram-design、scientific-humanization、humanizer-zh 四个 skill，把评测/长文从取材写到定稿。默认写法是「白皮书式长文」：导语口径 → 作用 → 是什么(含对比表) → 原理(结论前置) → 实操 → 边界 → 附录台账；原理图一律调用 diagram-design 技能（自包含 HTML + export_png 出 PNG），不用旧的 fig-template / render.py / mermaid2png 出图法。保留 A 读源码+安装实操、B 拿来即用 两套骨架。wechat-tool-review 的做法已放弃、不作合并。当用户说"评测/试用/分析这个开源项目""读源码并跑一遍再写文章""总结成一篇长文/白皮书""工作原理要配架构图、实操要配截图""核实 README 说法准不准""给文章配图/截图"时使用。产出 Markdown 长文 + 事实台账 + diagram-design 原理图 + 截图。《Higress AI 网关全解析》系列仍用 wechat-tech-article。
---

# Tool Review Writer

评测与长文的调度层。本 skill 不重复四个子 skill 的规则，只规定**什么时候加载谁、交接什么、什么不能先做**。

**两条总开关**：一是默认交付「白皮书式长文」（结构见 §1、写法见 [references/writing-style.md](references/writing-style.md)）；二是**原理图一律交给 `diagram-design` 技能生成**，不再使用 `wechat-tool-review` 那套 `fig-template.html` / `render.py` / `mermaid2png.py` 手画出图法。`wechat-tool-review` 不合并、不采用，旧的出图脚本与模板已删除（临时存 `/tmp/trw-removed-20261123/`）。

## 0. 前置检查

开工前确认，缺任何一项先告诉用户再继续：

1. 四个子 skill 是否可用：`doc-coauthoring`、`diagram-design`、`scientific-humanization`、`humanizer-zh`（`~/.qoder-cn/skills/` 或 `~/.agents/skills/`）。**缺 `diagram-design` 时不退回 mermaid，直接告知「配图暂缺」并停在该步**，其余三项缺了流程就断。
2. 出图依赖：`python` + Playwright chromium（`python -c "import playwright"`；本机没有 `python` 就用 `python3`），由 `diagram-design/scripts/export_png.py` 使用。**不再需要** markdown / pillow / 本机 Chrome / Node 这类旧出图依赖。
3. 目标工具拿到了什么：仓库地址 / 包名 / 配置片段。只有 README 链接时先问要不要 clone。
4. 是否允许在本机安装、联网、往工作区写文件。装不上就写"装不上"，不要跳过实操节。

## 1. 判 track（文章骨架）

看**结论从哪来**与**交付形态**，不看语言或仓库大小：

- 要 clone / 装依赖 / 编译，或提供真实 CLI、库接口 → **A 类**（十节骨架）。
- 一行配置或一个目录拷贝就接进来，本体是提示词、工具清单或远端服务 → **B 类**（八节骨架）。
- **默认：白皮书式长文**（多组件组合、机制介绍、想把一段实践总结成可直接发的长文）。固定为：导语口径 → `0` 这几样拼起来做什么 → `1` 各自是什么（含一张「定位 / 管什么 / 一句话差异」对比表）→ `2` 工作原理（`2.1` 全景…每小节结论前置）→ `3` 实操走查 → `4` 边界（适合谁 / 没验到什么）→ `附` 台账对照。章节名不套模板，lint 用 `--track skip`。
- 用户自带结构 → **自定义**，同样 `--track skip`。

判据看"结论从哪来"，不看语言或仓库大小。骨架与篇幅参考见 [references/article-structure.md](references/article-structure.md)。**旧的 C 类「公众号四段式」（是什么/怎么工作/实操/小结）已退役**，不再作为默认；要发公众号是在白皮书长文之上做导出（见 §5），不是另起一套骨架。

## 2. 铁律（先读，违了就是返工）

证据分级与台账格式见 [references/evidence-rules.md](references/evidence-rules.md)；文风、禁则、脱敏、可读性、白皮书式写法见 [references/writing-style.md](references/writing-style.md)。

1. **每个数字 / 断言回台账。** 正文的数字、耗时、行数、百分比挂在 `facts.md` 的 `[E##]` 上；`inferred` 只能写成推测。**内联 `[E##]` 可选**：发布稿常省（手机上读着噪声大），台账编号不变、附录给编号段对照，lint 加 `--plain`。
2. **README 的自评只能以「声称」出现。** `strength: author-claim` 被引用时必须带归因词（声称 / README 说 / 官方文档写）。lint 会查；plain 模式下须手工过。
3. **不写「本机验证」元叙事。** 数字以**产品事实**呈现（挂版本号或源码出处），不出现笔记本规格、「跑不跑得动」这类叙事。**性能数字例外于呈现、不例外于严谨**：吞吐 / 延迟必须一次性交代测试条件（模型、量化、硬件档次、并发 / 批大小），写脚注或表格头。**配图、截图里渲染成图的文字同样是发布内容，一并查。**
4. **正文不写源码行号。** 可核查性靠三样：**版本锚**（「v0.9.2 的源码里」）+ **标识符名**（函数 / 字段 / 常量名或原样引用的一行代码）+ **运行证据**（命令输出、落盘文件、日志读数）；文件级线索（`server.py`）可留。研究阶段照记 `path:line`，**行号只进台账**。
5. **每篇一个反直觉论点**（一句话立场，不是话题）。增量价值在「README 没说 / 说错了什么」，论点从核验差异里长出来；白皮书式长文落在「2 怎么工作」的反直觉小节。
6. **失败进正文。** 装不上、跑崩、超时的命令与原始输出如实贴、留一张截图。只有成功路径的评测等于没测。
7. **实操每个 Step 交出一份能看见效果的证据。** 只有命令、只有「配置已保存」的 Step 算返工：命令和期望输出成对贴，输出原样进代码块。证据通道按工具类型选（CLI 输出 / API 入参返回值 / 日志 / 产物回读 / 元素级截图），见 [references/research.md](references/research.md) 第 5 节；断言「中间层改了什么」搭回声 / 假服务取证；组件互相覆盖给单变量对照组，全开终态收在最后一步当验收。
8. **贴出来的每份配置逐键讲清「控制什么 / 不写取什么缺省 / 写错漏写什么后果」。** 配置文件、CLI flag、环境变量一视同仁；缺省值与执行条件回源码核（取值分支、构造器回填、执行条件判断），不抄文档。**最易写漏「配了但根本不执行」**：执行条件挂在别的键 / 模式上时，单看这份配置以为生效、其实一次都不跑。
9. **带 UI 面的 Step 逐步配截图，且只截重点元素。** 一个 Step 一张，`web-shot.mjs` 无头自截，**必须 `SHOT_CLIP=<选择器>` 只截文章要的那块**——侧栏、顶栏、页脚、版本号不进图，整屏帧算返工；默认态未必是要的那一态，先 `SHOT_EVAL` 点开。**纯命令行 Step 不截终端凑数**，证据走铁律 7 的输出打印。流程见 [references/screenshots.md](references/screenshots.md)。
10. **脱敏红线。** API key 一律 `sk-****`；演示凭据用显式占位符；不出现局域网 IP、主机名、`/Users/...` 路径。**每张截图插入前逐张扫描**：凭证格子、终端提示符、浏览器地址栏 / 书签、右上角账号标识、监控变量框。目标系统口令当次向用户索取（项目记忆有明确授权的除外），只用于本地实验，绝不写进正文、脚本常量、ima 或任何远端，也不进截图。脱敏改规则要重拍，别只在像素上抹。
11. **本地留档，同意才推。** 写文件、生成 HTML 随时做；**推 ima 必须先经用户明确同意**。ima 只有 `import_doc`/`append_doc`，没有覆盖也没有删除，一次推准（再推就是新笔记 + 旧的手删）。全流程与硬闸见 [references/ima-push.md](references/ima-push.md)。
12. **结构固定；原理图统一走 `diagram-design`。** 骨架按 §1；白皮书式长文段间用 `---`；「怎么工作」至少一张原理图，按 [semantic-patterns] 选型再用 Architecture / Sequence / Layer stack / Data flow 落地，**用 `diagram-design` 技能出图**（`template.html` 编辑态风格，`self_check.py` 过检，`export_png.py` 出 @2x PNG）；图源 `.html` 落 `diagrams/`，PNG 落 `imgs/`，图注统一 `图 N｜一句话`。**不再使用** `fig-template.html` / `render.py` / `mermaid2png.py` 这类旧手画出图法（wechat-tool-review 做法，已停用）。

**可读性（三类通用，面向 mixed 读者）**：分层不降级。开头给术语速查表、每小节结论前置、砍重复论点与写作元说明（挪附录）、收束段用白话；但**深度与证据标识符保留**，立场那句不为通俗稀释。白皮书式的具体手法（一句话差异、加粗原则领起、对比表、诚实边界）见 [references/writing-style.md](references/writing-style.md)「白皮书式长文」节。

## 3. 七个阶段

```bash
node scripts/scaffold.cjs <slug> --track a|b|skip --out <父目录>   # 建骨架 + 台账 + shots/ diagrams/
```

| 阶段 | 动作 | 加载 |
| --- | --- | --- |
| P0 取材 | clone 或装包；钉版本（优先 release tag）；跑 `--help`、版本行、一次真实任务、一次故意失败；README 断言逐条核（已核实 / 未核实 / 证伪）；观察逐条写进 `facts.md` | [references/evidence-rules.md](references/evidence-rules.md) · [references/research.md](references/research.md) |
| P1 提问 | 走 `doc-coauthoring` Stage 1：5–10 个澄清问题，问到能命中边界情况和权衡点为止。**提问要基于 P0 的真实输出**，否则只会复述 README | `doc-coauthoring` |
| P2 填充 | Stage 2 逐节：每节 5–20 个候选 → 用户挑 → `str_replace` 定点落笔，不整篇重打。起草实操先按铁律 7 规划证据链、按铁律 8 逐键记配置语义 | `doc-coauthoring` |
| P2.5 校证据 | 每节写完立刻按降级表校判断强度：没跑过的性能数字、README 自称、单次观察外推，当场改 | `scientific-humanization` |
| P3 出图 | 结构稳定后画：全景用 Architecture，主路径用 Sequence/Swimlane，缓存/分层用 Layer stack/Data flow。**一律走 `diagram-design`**：`self_check.py` 过检、`export_png.py` 出 @2x PNG 到 `imgs/`；图源 `.html` 落 `diagrams/`。**禁止** `render.py`/`mermaid2png`/`fig-template` 旧出图法 | `diagram-design` |
| P4 截图 | CLI 用 `capture_cli.cjs`；**网页/面板首选 `web-shot.mjs`**（browser-use 在 SPA 上常失效，退居探 DOM）；Agent 轨迹按轨迹取法 | [references/screenshot-guide.md](references/screenshot-guide.md) · [references/screenshots.md](references/screenshots.md) |
| P5 读者测试 | 开无上下文子 Agent，只喂 `draft.md`，问 5–10 题（含"只看图能否回答数据从哪到哪"）。答偏处回 P2 补 | `doc-coauthoring` Stage 3 |
| P6 通稿 | 最后一步做表达层修改：空话、套话、公式化节奏。**不动事实、数字、术语、代码引用** | `humanizer-zh` |
| P7 收口 | `node scripts/lint_article.cjs draft.md --track skip --facts notes/<tool>-facts.md --plain`（可选加 `--wechat`），要求 0 FAIL；再跑禁词 / 行号 / 脱敏 grep | — |

P3/P4 可并行，但都必须在 P6 之前。完整理由与跳步代价见 [references/orchestration.md](references/orchestration.md)。

## 4. 脚本

| 脚本 | 用途 |
| --- | --- |
| `scripts/scaffold.cjs <slug> --track a\|b\|skip --out <dir> [--title X] [--force]` | 生成 `draft.md` + `facts.md` + `shots/` + `diagrams/` |
| `scripts/capture_cli.cjs "<标签>" --id NN --out <shots> [--png] [--max-lines 90] [--encoding auto\|gbk\|utf-8] -- <命令>` | 跑真实命令，留 transcript + 终端卡 HTML + PNG |
| `scripts/html2png.py <src.html> <out.png> [1–4] [--selector .shot-card\|svg] [--width N]` | Playwright 元素出图（终端卡等） |
| `scripts/lint_article.cjs <draft.md> [--track a\|b\|skip] [--facts f.md] [--wechat] [--plain]` | 章节、图片落盘、台账对账、claim 强度、公众号排版；`--plain` 内联标记可选，`--track skip` 自定义结构 |
| `scripts/web-shot.mjs <url> <out.png> [等待ms]` | 无头 Chrome + CDP 截 Web UI（`SHOT_SESS`/`SHOT_EVAL`/`SHOT_CLIP`/`SHOT_H` 等环境变量） |
| `scripts/wechatify.py <article>.md` | Markdown → 微信内联样式 HTML（同目录 `.wechat.html`；只做排版转换，不出图） |
| ~~`render.py` / `mermaid2png.py` / `assets/fig-template.html` / `fig.css` / `fig-mermaid-template.mmd` / `mermaid.min.js`~~ | **已删除（2026-11-23）**：旧 `wechat-tool-review` 出图管线，配图改用 `diagram-design`；删除件临时存 `/tmp/trw-removed-20261123/` |

`capture_cli.cjs` 退出码非 0 是正常取证结果，脚本自身仍返回 0；只有启动失败或出图失败才非 0。**原理图的样式与模板用 `diagram-design` 自带的 `assets/template.html` + `references/style-guide.md`，不要再用 `assets/fig-template.html`/`fig.css`。** 截图（`web-shot.mjs`）与终端卡（`capture_cli.cjs`/`html2png.py`）不属「原理图」，照旧。

## 5. 交付

主交付是 `draft.md`（定稿后改名成文章名）+ `facts.md` + `diagrams/`（图源）+ `imgs/`（diagram-design 出的 PNG + 截图）+ `shots/`。用户要发布时再选导出腿：

- **公众号**：先 `--wechat` 过 lint（代码 ≤48 字符、表格 ≤4 列），再 `wechatify.py` 生成 `.wechat.html`（用户点名自己的主题 skill 如 `wechat-geek-dark-theme` 时以主题为准）。**配图用 `diagram-design` 出的 PNG（已在 `imgs/`），不再走 `render.py`/`mermaid2png.py`**；截图走 `web-shot.mjs`。生成后跑禁词 / 行号 / 脱敏 grep、逐 Step 证据链、逐键配置语义自检。
- **IMA 笔记**：**用户点头后才推**，按 [references/ima-push.md](references/ima-push.md) 全流程：批次切分（每图独立成批）、引用块嵌围栏会静默退化（推前 grep）、单批 base64 <~750KB（>600KB PNG 转无损 WebP 仅用于推送）、推后只信 JSON 块树（`format:2`，fence 对数 == `code_block` 数）、汉字平衡式。ima 无覆盖无删除，一次推准。
- **内网 Markdown 直接分发**：保持图片相对路径。

工作区约定：`article/<slug>.md` + `.wechat.html` + `imgs/`（原理图 PNG + 截图 `note/`）+ `diagrams/`（图源 `.html`）；台账 `notes/<tool>-facts.md`（`path:line` 只留这里）。

## 6. 边界

- 本 skill 与四个子 skill 都是内部使用。`doc-coauthoring` 上游无 LICENSE，**不要打包外发**。
- 不判断文章作者身份，也不承诺通过任何 AI 检测器。`humanizer-zh` 与 `scientific-humanization` 管的是表达与证据边界，不是检测规避。
- 事实责任在人。台账齐全不代表结论正确，P0 观察错了后面全错；写完仍要自己核一遍自己下的判断。
- **`wechat-tool-review` 不合并、不采用**；本 skill 走白皮书式长文 + `diagram-design` 配图。旧出图脚本/模板已删除。
- 《Higress AI 网关全解析》系列仍走 `wechat-tech-article`（含 `ai_log` 台账、回声上游取证等该系列专属配方），不用本 skill 顶替。

## Resources

- `references/article-structure.md` — A/B 骨架 + **白皮书式长文**结构、每节写什么、图与截图落位
- `references/writing-style.md` — 人称语气、**白皮书式长文手法**、可读性分层、数字呈现、AI 味黑名单、坑的写法、脱敏
- `references/evidence-rules.md` — 台账格式、四种 strength、降级表、内联标记可选（`--plain`）、交付前自查
- `references/research.md` — 钉版本、README 断言核验、事实台账、按工具类型选证据通道、性能数字呈现
- `references/screenshot-guide.md` — CLI 终端卡 / Web UI（web-shot 首选）/ Agent 轨迹三类视觉证据
- `references/screenshots.md` — Web UI 元素级自截（无头 Chrome + CDP + `SHOT_CLIP`）、脱敏与插入规范
- `references/toolchain.md` — 收口检查清单、推 ima 硬闸、常见故障（原「配图管线」章节已随旧出图法停用）
- `references/ima-push.md` — 推 ima 全流程：批次切分、静默退化、E2BIG 与无损 WebP、汉字平衡式、回读判据
- `references/orchestration.md` — P0–P7 顺序理由、跳步代价、与 oss-tool-eval 的关系
- `references/wechat-structure.md` — **遗留**：原 C 类四段式，已退役，仅存档
