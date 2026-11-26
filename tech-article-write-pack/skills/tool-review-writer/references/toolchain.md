# 工具链：配图 / HTML / 验证

> **配图管线停用（2026-11-23）**：原 `render.py`（HTML 画图）/ `mermaid2png.py`（时序图）及 `assets/fig-template.html`、`fig.css` 属 `wechat-tool-review` 做法，已停用。**原理图一律用 `diagram-design` 技能**（`template.html` 风格 + `self_check.py` + `export_png.py`）。本文件里与配图相关的命令/依赖不再使用；推 ima 硬闸、发布前检查、常见故障等与配图无关的条目仍有效。

## 依赖

```bash
python3 -m pip install markdown pillow
```

渲染依赖本机 Chrome（`/Applications/Google Chrome.app/...`，可用环境变量 `CHROME` 覆盖）。

脚本位置规则：**工作区 `article/imgs/` 里已有的脚本优先用**；没有时从本 skill `scripts/` 拷（`render.py` / `mermaid2png.py` / `web-shot.mjs`），并把 `assets/fig.css`、`assets/fig-template.html` 拷到 `imgs/`；跑时序图还要拷 `assets/mermaid.min.js` 和起手模板 `assets/fig-mermaid-template.mmd`。

## 配图管线（原理图）

1. 起手：从 `assets/fig-template.html` 复制成 `imgs/<slug>-fig<N>-<name>.html`，`<link>` 指到同目录 `fig.css`。
2. 画图规则（手机可读性是硬约束）：
   - 画布固定 **480 CSS px** 宽——微信手机端按约 343pt 显示，缩放系数 0.71，所以正文字号**不低于 14.5px**（1080px 宽版本在手机上就是死在这条）；
   - 结构惯例：`.cap`（图 N）→ `h1`（标题，后半句用 `<span>` 上蓝色）→ `.lede`（一句副题）→ 主体 → `.foot`（底部收束，自动带虚线分隔）；
   - 配色 token：文字 `#1a1f2e`、次要 `#5a6478`、灰 `#8a93a6`/`#9aa4b5`、高亮蓝 `#1f6feb`（组件名 `#1f5fb8`）、绿 `#1f7a45`、橙 `#a35a12`、边框 `#d8e0ec`/`#e3e8f0`；
   - 多列用 flex，别用 grid；等宽内容用 `.mono` / `ui-monospace`。
3. 渲染：

```bash
# 在 imgs/ 目录下（或 --dir 指定）：
python3 render.py <slug>-fig1-<name>     # 指定图
python3 render.py                        # 不带参数 = 渲染目录里全部 fig 图
```

   - 每次渲染写 `<name>.png`（4x 缩放 + 底部留白自动裁掉）和 `preview/` 里 686px 手机预览。
   - **必须看一遍 `preview/` 版本**——它就是手机上实际渲染的效果，字号太小、太密肉眼立刻能发现。
   - 改了图上文字就重渲染；**图内文字同样是发布内容**，按铁律 1 自查（正文清干净了、图里没清，是踩过的坑）。
4. 插入 md：`![图 N：标题](imgs/<slug>-fig1-<name>.png)`。
5. 序号两套，别混：文件名 `figN` 是**创建序号**（永不改名，文章和 HTML 都引用着）；图上 `.cap` 和 md caption 的「图 N」是**展示序号**（按正文出现位置）。往旧文章插图会重排展示序号：改新图与后面各图的 `.cap` → 重渲染被改动的图 → 改 md caption → 正文提过「图 N」的地方一起搜一遍。
6. **【已停用，改用 `diagram-design`】** 图型分工（旧法）：架构图 / 流程图用 HTML 骨架手画；时序图用 mermaid 画。时序图源 = `imgs/<slug>-fig<N>-<name>.mmd`（起手复制 `assets/fig-mermaid-template.mmd`），用 `mermaid2png.py` 渲染——同一 480px 画布、同一图框（fig.css）、同一 686px 预览门槛。泳道/时序/激活在 mermaid 里是声明式的，改文案成本低；架构/流程图版式自由度大，手画 HTML 更可控。
7. mermaid 管线用法：

```bash
# 在 imgs/ 目录下（或 --dir 指定）：
python3 mermaid2png.py <slug>-fig2-<name>   # 指定图（.mmd 后缀可省）
python3 mermaid2png.py                      # 不带参数 = 渲染目录里全部 .mmd
```

   - 原理：`.mmd` 包进图框 + 本地 `mermaid.min.js`（v11.17.2，`assets/` 与 `imgs/` 各存一份；升级换这两份），本机 Chrome 无头渲染，不需要 Node；预览照旧进 `preview/`。
   - `.mmd` 顶部元信息（其余行全是 mermaid 源）：`%%cap:` 图号、`%%title:`（可内嵌 `<span>` 标蓝）、`%%lede:`、`%%foot:`；缺哪项就不渲染哪块。
   - 写作约束：参与者 **≤3 列**；消息文案 `<br/>` 手动换行、单行 ~18 字以内；字号在脚本 `MERMAID_INIT` 里统一调（当前 message/note 15px）。
   - 踩坑：同名 `.html` 若还留着，`render.py` 批量模式会用它覆盖 PNG——旧源改名 `*.html.bak` 归档。
   - 激活条（`activate`）表现「包住」关系，`rect` 区间面板标注阶段（如「计量区间」）。

## Web UI 截图管线（实操配图）

铁律 6：带 UI 面的 Step 一个一张。驱动 `scripts/web-shot.mjs`（无头 Chrome + CDP，Node ≥22）。登录取 cookie、`SHOT_EVAL` 交互、`SHOT_CLIP` 元素级截图、`SHOT_H` 量高、脱敏，全流程在 **`screenshots.md`**。环境变量速查：`SHOT_SESS`（可选）、`SHOT_COOKIE_NAME`（设了 SESS 必填）、`SHOT_ORIGIN`、`SHOT_EVAL`、`SHOT_EVAL_WAIT`（2500ms）、`SHOT_CLIP`、`SHOT_PORT`（9333）、`SHOT_W`/`SHOT_H`（1440×900 @2x）、`CHROME`；第三个位置参数是页面加载等待（默认 4000ms）。

## 微信 HTML

```bash
python3 wechatify.py <article>.md
# -> <article>.wechat.html （同目录）
```

- 原理：Markdown → HTML，所有样式内联（微信编辑器剥 `<style>` 和 `class`）；图片独立成段的自动转居中 `<section>`；`*斜体*` 渲染成灰色标注。
- 生成后必须验证（见下）；再在浏览器 `file://` 打开目检排版（表格、代码块、图片居中）。
- 用户有自己的排版主题（如 `wechat-geek-dark-theme`）且点名要用时，以主题 skill 为准，本脚本是缺省腿。

## 发布前检查清单

对目标文章跑一遍：

```bash
MD=<article>.md
HT=<article>.wechat.html

# 1) 篇幅：汉字数（~4000–4500 作参照）
python3 -c "import re,sys; t=open(sys.argv[1]).read(); print('汉字:', len(re.findall(r'[一-鿿]', t)))" $MD

# 2) 图片数三处一致：MD 引用 == HTML <img> == 磁盘文件都在
grep -c '!\[' $MD; grep -c '<img' $HT; grep -o '(imgs/[^)]*)' $MD | tr -d '()' | sort -u | xargs -I{} test -f {} && echo "files ok"

# 3) HTML 无残留样式/类名
grep -cE '<style|class=' $HT   # 期望 0

# 4) 铁律 1：无「本机」叙事 —— 正文 + 配图源码（图内文字也是发布内容；.html 与 .mmd 都扫）
grep -nE '本机|跑得动|我这台|笔记本|Intel' $MD   # 期望无输出
grep -oE 'imgs/[^)]+\.png' $MD | sed 's/\.png$//' | sort -u | while read -r b; do
  for f in "$b.html" "$b.mmd"; do
    [ -f "$f" ] && grep -nE '本机|跑得动|我这台|笔记本|Intel|实测' "$f"; done; done   # 期望无输出

# 4b) 铁律 7：正文不写源码行号（`:153-200`、`main.go:50` 这类；`:80`/`:8080`/`:443` 是端口，不算）
grep -nE '\.(go|py|ts|js|rs|java):[0-9]+|:[0-9]{2,4}-[0-9]{2,4}|行号可直接对' $MD   # 期望无输出

# 4c) 铁律 8：每个 Step 都带证据——逐 Step 数代码块与图
awk '/^#{2,3} .*Step |^\*\*Step /{if(n){printf "%-44s 围栏行 %2d 图 %d\n", substr(n,1,44), f, i} n=$0; f=0; i=0}
     /^```/{f++} /!\[/{i++} END{printf "%-44s 围栏行 %2d 图 %d\n", substr(n,1,44), f, i}' $MD
# 期望：每行「围栏行/2 + 图」>= 1；再人工读一遍——围栏里那份得是**输出/读数**，不是只有配置片段。
# 只讲「已保存」「应该能看到」的 Step 按返工处理。

# 4d) 铁律 9：贴出来的 YAML 每个顶层键都要在正文点过名
python3 - "$MD" <<'PY'
import re, sys
md = open(sys.argv[1]).read()
for s in re.split(r'(?m)^(?=#{2,3} (?:Step |\*\*Step ))', md)[1:]:
    rest = s.split('\n', 1)[1]
    keys = {m.group(1) for blk in re.findall(r'(?m)^```ya?ml\n(.*?)^```', rest, re.S)
            for line in blk.split('\n') if (m := re.match(r'^([A-Za-z_][\w-]*):', line))}
    prose = re.sub(r'(?m)^```.*?^```', '', rest, flags=re.S)
    missing = sorted(k for k in keys if k not in prose)
    print(f'{s.splitlines()[0][:44]:46s} 键{len(keys):2d} 未点名: {",".join(missing) or "—"}')
PY
# 「未点名」不是都要补一段——整组键一起解释算已覆盖，但全篇没提的键必须补一句「关掉/打开分别改变什么」。
# CLI flag / 环境变量配置同理人工过一遍。

# 5) 脱敏：真实 key / LAN IP / 用户名 / 本机路径（正文、HTML、全部配图源码）
grep -nE 'sk-[0-9a-f]{8}|10\.[0-9]+\.|192\.168\.|kirito|/Users/' $MD $HT imgs/*.html imgs/*.mmd   # 期望无输出

# 6) UI 截图数 == 带 UI 面的 Step 数（铁律 6；逐张目检账号标识与凭证格）
grep -c 'imgs/note/' $MD

# 7) 推 ima 前：引用块里嵌围栏会让整批 markdown 退化成纯文本（期望无输出，细则见 ima-push.md）
grep -nE '^[[:space:]]*>[[:space:]]*`{3}' $MD
```

补充人工项：导读表本篇加粗对（系列）；脚注三要素在；性能数字测试条件交代了；截图逐张过目（`screenshots.md` 第 3 节）。

## 推 ima

流程、批次切分、静默退化、E2BIG/WebP、汉字平衡式、回读判据，全部在 **`ima-push.md`**。两条最容易被忘的硬闸：

```bash
# 推前 lint：期望无输出（有输出先改源稿，把围栏提到引用块外）
grep -nE '^[[:space:]]*>[[:space:]]*`{3}' $MD

# 推后只信 JSON 块树：源稿 fence 对数 == 线上 code_block 数，且无节点 text 含 ```
# ima_api "openapi/note/v1/get_doc_content" '{"note_id":"<id>","target_content_format":2}'
# 不要用 format:1 自检——它会把退化段落里的围栏转义成 \`\`\`，看着像真代码块
```

## 常见故障

- `ModuleNotFoundError: markdown` → `pip install markdown`。
- render.py 出 `FAIL`：Chrome 路径不对（设 `CHROME`）或 html 里有 `grid`/超宽元素。
- mermaid 渲染空白/显示原始代码：打开 `/tmp/mmd-build/<name>.render.html` 浏览器复现（多为语法错误）；换引擎版本 = 替换 `imgs/mermaid.min.js` 与 skill `assets/mermaid.min.js` 两份。
- HTML 里 `<img` 数对不上：MD 里图片被包进了非独立段落（加了行内文字），居中逻辑不生效——图片保持独立成段。
- web-shot 报 `chrome debug port never came up`：9333 被上一次 Chrome 占了，换 `SHOT_PORT` 或按 `screenshots.md` §1.1 清理。
- web-shot 截出来是登录页：`SHOT_SESS` 空或过期，重新登录取 cookie。
- web-shot 截出来状态不对（抽屉没开、默认页签）：`SHOT_EVAL` 没点中，看 `EVAL>` 返回值定位；一次调用只截一屏，多屏多次调用、每次把完整动作串写进 `SHOT_EVAL`。