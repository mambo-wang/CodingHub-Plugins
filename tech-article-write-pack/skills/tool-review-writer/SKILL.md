---
name: tool-review-writer
description: 编排 doc-coauthoring、diagram-design、scientific-humanization、humanizer-zh 四个 skill，把开源工具评测从取材写到定稿。适用于两类对象：需要读源码并安装实操的 CLI、库、服务；以及 MCP 服务器、Agent Skill 这类拿来即用、不需要编译部署的工具。当用户说"评测/试用/分析这个开源项目""读源码并跑一遍再写文章""工作原理要配架构图、实操要配截图""核实一下 README 的说法准不准""把这篇评测写成公众号长文"时使用。产出 Markdown 长文 + 事实台账 + 图与截图，可选公众号导出。
---

# Tool Review Writer

评测长文的调度层。本 skill 不重复四个子 skill 的规则，只规定**什么时候加载谁、交接什么、什么不能先做**。

## 0. 前置检查

开工前确认，缺任何一项先告诉用户再继续：

1. 四个子 skill 是否可用：`doc-coauthoring`、`diagram-design`、`scientific-humanization`、`humanizer-zh`（`~/.qoder-cn/skills/`）。缺 `diagram-design` 时图退化为 Mermaid，其余三项缺了流程就断。
2. 出图依赖：`python` + Playwright chromium。验证 `python -c "import playwright"`。本机如果没有 `python`，就改用 `python3`。
3. 目标工具拿到了什么：仓库地址 / 包名 / 配置片段。只有 README 链接时先问要不要 clone。
4. 是否允许在本机安装、联网、往工作区写文件。装不上就写"装不上"，不要跳过第 5 节。

## 1. 判 track

看**结论从哪来**，不看语言或仓库大小：

- 要 clone / 装依赖 / 编译，或提供真实 CLI、库接口 → **A 类**（十节骨架）。
- 一行配置或一个目录拷贝就接进来，本体是提示词、工具清单或远端服务 → **B 类**（八节骨架）。

细则与每节写什么见 [references/article-structure.md](references/article-structure.md)。

## 2. 七个阶段

```bash
node scripts/scaffold.cjs <slug> --track a|b --out <父目录>   # 建骨架 + 台账 + shots/ diagrams/
```

| 阶段 | 动作 | 加载 |
| --- | --- | --- |
| P0 取材 | clone 或装包；跑 `--help`、版本行、一次真实任务、一次故意失败；把观察逐条写进 `facts.md` | [references/evidence-rules.md](references/evidence-rules.md) |
| P1 提问 | 走 `doc-coauthoring` Stage 1：5–10 个澄清问题，问到能命中边界情况和权衡点为止。**提问要基于 P0 的真实输出**，否则只会复述 README | `doc-coauthoring` |
| P2 填充 | Stage 2 逐节：每节 5–20 个候选 → 用户挑 → `str_replace` 定点落笔，不整篇重打 | `doc-coauthoring` |
| P2.5 校证据 | 每节写完立刻按降级表校判断强度：没跑过的性能数字、README 自称、单次观察外推，当场改 | `scientific-humanization` |
| P3 出图 | 结构稳定后画：§4 全景用 Architecture，主路径用 Swimlane/Sequence。过 `self_check.py`，用 `export_png.py` 出 `@2x` | `diagram-design` |
| P4 截图 | CLI 用 `capture_cli.cjs`；网页/面板用 browser-use MCP；Agent 轨迹按轨迹取法 | [references/screenshot-guide.md](references/screenshot-guide.md) |
| P5 读者测试 | 开无上下文子 Agent，只喂 `draft.md`，问 5–10 题（含"只看图能否回答数据从哪到哪"）。答偏处回 P2 补 | `doc-coauthoring` Stage 3 |
| P6 通稿 | 最后一步做表达层修改：空话、套话、公式化节奏。**不动事实、数字、术语、代码引用** | `humanizer-zh` |
| P7 收口 | `node scripts/lint_article.cjs draft.md --wechat`，要求 0 FAIL | — |

P3/P4 可并行，但都必须在 P6 之前。完整理由与跳步代价见 [references/orchestration.md](references/orchestration.md)。

## 3. 三条硬约束

1. **每个数字回台账。** 正文里的数字、耗时、行数、百分比必须挂在 `facts.md` 的 `[E##]` 上。`inferred` 只能写成推测。
2. **README 的自评只能以"声称"出现。** `strength: author-claim` 的条目被引用时，那句话必须带归因词。lint 会查。
3. **失败进正文。** 装不上、跑崩、超时的命令与原始输出留一张截图。只有成功路径的评测等于没测。

## 4. 脚本

| 脚本 | 用途 |
| --- | --- |
| `scripts/scaffold.cjs <slug> --track a\|b --out <dir> [--title X] [--force]` | 生成 `draft.md` + `facts.md` + `shots/` + `diagrams/` |
| `scripts/capture_cli.cjs "<标签>" --id NN --out <shots> [--png] [--max-lines 90] [--encoding auto\|gbk\|utf-8] -- <命令>` | 跑真实命令，留 transcript + 终端卡 HTML + PNG |
| `scripts/html2png.py <src.html> <out.png> [1–4] [--selector .shot-card\|svg] [--width N]` | Playwright 元素出图 |
| `scripts/lint_article.cjs <draft.md> [--track a\|b] [--facts f.md] [--wechat]` | 章节、图片落盘、台账对账、claim 强度、公众号排版 |

`capture_cli.cjs` 退出码非 0 是正常取证结果，脚本自身仍返回 0；只有启动失败或出图失败才非 0。

## 5. 交付

主交付是 `draft.md`（定稿后改名成文章名）+ `facts.md` + `diagrams/` + `shots/`。用户要发布时再选导出腿：

- 公众号：先 `--wechat` 过 lint（代码 ≤48 字符、表格 ≤4 列），再交给 `md2wechat` 或用户自己的主题 skill。
- IMA 笔记：走 `ima-skill` 的 notes 模块，图片以 data URL 内联，单图 <3 MiB。用户手工编辑过的笔记只追加、不覆盖。
- 内网 Markdown 直接分发：保持图片相对路径。

## 6. 边界

- 本 skill 与四个子 skill 都是内部使用。`doc-coauthoring` 上游无 LICENSE，**不要打包外发**。
- 不判断文章作者身份，也不承诺通过任何 AI 检测器。`humanizer-zh` 与 `scientific-humanization` 管的是表达与证据边界，不是检测规避。
- 事实责任在人。台账齐全不代表结论正确，P0 观察错了后面全错；写完仍要自己核一遍自己下的判断。
