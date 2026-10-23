# 截图取证

三类视觉证据，分工不同：`shots/` 是真跑出来的东西，`diagrams/` 是解释结构的东西，两者不能互相替代。

## 1. CLI 输出：`scripts/capture_cli.cjs`

跑真实命令，同时留下原始 transcript 和一张终端卡片图。

```bash
node scripts/capture_cli.cjs "首次索引" --id 05 --out <文章目录>/shots --png -- \
  codewiki index --repo D:/repos/X
```

产物：`shots/05-首次索引.txt`（完整原文，进台账当 `observed`）、`.html`（终端卡）、`.png`（进正文）。

要点：

- `--` 之后整段是命令，原样进 transcript，别手写改写。
- 文件名只用 ASCII；中文标签会退化成命令派生的名字，所以给 `--id`。
- 输出超过 `--max-lines`（默认 90）时图内截断并标"省略 N 行"，`.txt` 保全文。
- 退出码非 0 是正常结果，脚本仍返回 0 并把 `exit N` 画进卡片页脚。**失败的那张图往往比成功的那张更有说服力，不要只留成功的。**
- Windows 下子进程输出常是 GBK，脚本按 UTF-8 严格解码失败后自动退回 GBK，摘要里会打 `codec=gbk`。需要强制时加 `--encoding gbk|utf-8`。
- 命令里含密钥时，先确认这条命令要不要进正文；要进就把参数换成占位符另存一张，别把真密钥画进图。

## 2. 网页 / 桌面 UI：browser-use MCP

MCP 服务器面板、Web 控制台、带界面的工具用这个：`navigate_page` → `take_snapshot`（拿到元素引用）→ 需要时 `click`/`fill` → `take_screenshot`。

- 截图前先 `take_snapshot` 确认页面已经到位，别截加载中的骨架屏。
- 全页截图用 `fullPage`；只想留关键区时截视口。
- 落到 `shots/` 后按同一命名法改名（`NN-ASCII名.png`），并另存一份当时的 URL 和步骤到 `.txt`，否则三个月后没人知道这张图对应哪次操作。
- 隐私：截图前确认页面上没有 token、cookie、内部仓库名。有就先滚动或遮挡，必要时改用 CLI。

## 3. Agent 会话轨迹（B 类）

Skill / MCP 的核心证据是"它到底做了什么"。两种取法：

- 会话面板截图（browser-use）。
- 把工具调用序列整理成文本卡：用 `capture_cli.cjs` 的卡片样式手写一份 `.html`，再用 `html2png.py` 出图。保留调用名与参数，去掉无关的推理长文。

轨迹必须包含它**没**按规则做的那一次，否则第 5 节的拷问没有依据。

## 4. 通用规则

| 规则 | 原因 |
| --- | --- |
| 图里必须能看到版本 / 命令 / 退出码之一 | 否则等于没取证 |
| 不裁掉报错行，不加马赛克式涂抹 | 读者要判断的是真实行为 |
| 正文引用一律 `![](shots/NN-name.png)`，带 alt | alt 给读者测试和导出用；引 HTML 会被 lint 拦 |
| alt 写"看到什么"，不写"如下图所示" | 导出到公众号后 alt 是唯一兜底 |
| 一张图只讲一件事 | 讲两件事的图读者会漏掉第二件 |

## 5. 出图脚本

`scripts/html2png.py` 是 Playwright 元素截图，和 `diagram-design` 的 `export_png.py` 同源，区别是它截任意选择器：

```bash
python scripts/html2png.py shots/05-x.html shots/05-x.png 2 --selector .shot-card
python scripts/html2png.py diagrams/arch.html diagrams/arch@2x.png 2 --selector svg
```

`scale` 取 1–4，正文用 2。宽度不对时加 `--width 1200`。

## 6. 导出到公众号时另查

代码行 >48 字符、表格 >4 列会在手机上散架。`lint_article.cjs --wechat` 会把这两项列出来。改的是排版，不是事实。
