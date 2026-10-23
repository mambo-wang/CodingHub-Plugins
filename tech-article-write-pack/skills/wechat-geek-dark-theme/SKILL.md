---
name: wechat-geek-dark-theme
description: 用户自定义的微信公众号"极客暗色"排版主题（基于 md2wechat AI 模式）。当用户说"按我的主题排版""公众号排版"且要暗色/代码友好风格时使用。
---

# WeChat 极客暗色主题（geek-dark）

把 Markdown 文章排版成微信公众号兼容的暗色极客风 HTML。纯内联样式，适配优先、滑动兜底。

## 工具链

- 排版入口：`md2wechat convert <article.md> --mode ai --theme autumn-warm --custom-prompt "<下方风格提示词>" --json`，取 `data.prompt` 后由 Agent 按提示词内的兼容规则亲自渲染 HTML（AI 模式免费；`github-readme`/`cyber` 等 API 主题需 md2wechat.cn key，不走）。
- 发布：`convert --draft` 需 `WECHAT_APPID/WECHAT_SECRET`；无凭据时输出 HTML 让用户手动粘贴公众号编辑器。
- npm 装带 postinstall 二进制的包遇 `UNABLE_TO_GET_ISSUER_CERT_LOCALLY`（VDI TLS 拦截）：先跑 `D:\tmp_build\certs\export-roots.ps1` 重建 PEM，再 `NODE_EXTRA_CA_CERTS='D:\tmp_build\certs\allroots.pem' npm install -g <pkg>`。

## 配色（GitHub Dark Dimmed）

| 用途 | 色值 |
|---|---|
| 页面底 | `#0d1117` |
| 卡片/代码底 | `#161b22`（行内代码底 `#1f242c`） |
| 边框 | `#30363d` |
| 正文 | `#c9d1d9` |
| 标题 | `#e6edf3` |
| 强调青 | `#58a6ff` · 强调紫 `#bc8cff` |
| 关键字 | `#ff7b72` · 函数名 `#d2a8ff` |
| 字符串 | `#a5d6ff` · 绿色行内代码 `#7ee787` |
| 数字 | `#79c0ff` · 注释/行号 `#8b949e` |

## 结构规范

- 最外 `<section>`：`background-color:#0d1117;padding:40px 10px;display:flex;flex-direction:column;align-items:center;`，内层卡片 `max-width:680px;background:#161b22;border:1px solid #30363d;border-radius:12px;padding:32px 28px;`
- 每个 `<p>` 显式写 `color:#c9d1d9;font-size:16px;line-height:1.8;`（防微信重置为黑）。
- 代码块：终端卡片 = 标题栏（三圆点 `#ff5f56/#ffbd2e/#27c93f` + 文件名，12px `#8b949e`）+ 代码区（`Consolas` 12px、`line-height:1.7`、`white-space:pre`、两位行号 `#8b949e` 右对齐补 `&#160;`）。
- 引用：`border-left:3px solid #bc8cff;background:#131820;border-radius:0 8px 8px 0;`
- 禁 `<style>` 标签、class、外部 CSS；只用安全标签集（section/p/span/strong/em/h1-h6/ul/ol/li/blockquote/table/img/br/hr）。

## 超宽降级规则（核心约定）

公众号会剥掉 `overflow-x` 且正文禁横向滚动，**不得依赖左右滑动**：

- 代码：预算 12px 等宽 ≈ **48 字符/行**（含 4 字符行号前缀）。超预算的行在语法边界（逗号、运算符、`{` 前）折行，续行缩进对齐参数起点；行号按视觉行重排。
- 表格：≤4 列；单元格短语化并加 `word-break:break-all`；超 4 列或含长文本时改为"每条一个卡片"的列表呈现。
- `overflow-x:auto` 可保留作浏览器预览兜底，但排版完成前必须确认无行超出 48 字符预算。

## 风格提示词（喂给 --custom-prompt）

```
极客暗色代码风：GitHub Dark Dimmed 配色（页面底 #0d1117，卡片 #161b22，正文 #c9d1d9，强调青 #58a6ff 与紫 #bc8cff）。代码块是主角：#161b22 圆角卡片、顶部三圆点终端标题栏带语言名、等宽字体 12px、语法着色（关键字 #ff7b72、函数 #d2a8ff、字符串 #a5d6ff、数字 #79c0ff、注释行号 #8b949e）、两位行号。每行代码不超过 48 字符，超长在语法边界折行，不依赖横向滚动；表格不超过 4 列，超宽改为卡片列表。全内联样式，禁 style 标签，主容器 section 包裹，每个 p 显式 color，微信编辑器兼容。
```

## 验证

渲染后跑一次行宽检查：代码区内每个视觉行（去掉行号 span 后）≤44 可见字符；再用 headless Edge 出图核对：
`msedge --headless --disable-gpu --no-sandbox --user-data-dir=<新目录> --window-size=430,1500 --screenshot=<png> file:///<html>`
（截图没生成且 exit=0 → user-data-dir 被锁，换新目录重试。）
