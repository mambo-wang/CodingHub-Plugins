# 工具链：配图 / HTML / 验证

## 依赖

```bash
python3 -m pip install markdown pillow
```

渲染依赖本机 Chrome（`/Applications/Google Chrome.app/...`，可用环境变量 `CHROME` 覆盖）。

脚本位置规则：**工作区 `article/` 里已有的脚本优先用**（历史文章用它生成，保持一致）；工作区没有时用本 skill 的 `scripts/` 副本（`render.py` / `mermaid2png.py` / `console-shot.mjs`），并把 `assets/fig.css`、`assets/fig-template.html` 拷到 `imgs/`；跑时序图还要拷 `assets/mermaid.min.js` 和起手模板 `assets/fig-mermaid-template.mmd`。

## 配图管线（原理图）

1. 起手：从 `assets/fig-template.html` 复制成 `imgs/p<NN>-fig<N>-<slug>.html`，`<link>` 指到同目录 `fig.css`。
2. 画图规则（手机可读性是硬约束）：
   - 画布固定 **480 CSS px** 宽——微信手机端按约 343pt 显示，缩放系数 0.71，所以正文字号**不低于 14.5px**（旧 1080px 宽版本在手机上就是死在这条）；
   - 结构惯例：`.cap`（图 N）→ `h1`（标题，后半句用 `<span>` 上蓝色）→ `.lede`（一句副题）→ 主体 → `.foot`（底部收束，自动带上虚线分隔）；
   - 配色 token：文字 `#1a1f2e`、次要 `#5a6478`、灰 `#8a93a6`/`#9aa4b5`、高亮蓝 `#1f6feb`（插件名 `#1f5fb8`）、绿 `#1f7a45`、橙 `#a35a12`、边框 `#d8e0ec`/`#e3e8f0`；
   - 多列用 flex，别用 grid；等宽内容用 `.mono` / `ui-monospace`。
3. 渲染：

```bash
# 在 imgs/ 目录下（或 --dir 指定）：
python3 render.py p02-fig1-switch-tree        # 指定图
python3 render.py                              # 不带参数 = 渲染目录里全部 fig 图
```

   - 每次渲染会写 `imgs/p02-fig1-switch-tree.png`（4x 缩放 + 底部留白自动裁掉）和 `imgs/preview/` 里 686px 的手机预览。
   - **必须看一遍 `preview/` 版本**——它就是手机上实际渲染的效果，字号太小、太密肉眼立刻能发现。
   - 改了图上的文字就重渲染一次；**图内文字同样是发布内容**，按铁律 1 自查（出现过「本机」「12 个容器」没随正文同步修正的漏网案例）。
4. 插入 md：`![图 N：标题](imgs/p02-fig1-switch-tree.png)`。
5. 命名：新图用 `p<NN>-fig<N>-<slug>` 约定；**第 01 篇的历史图（fig1–fig7）勿改名**，文章和 HTML 都引用着它们；01 篇后续追图接着 `fig8`、`fig9`… 排。
6. 序号两套，别混：文件名 `figN` 是**创建序号**（永不改名），图上 `.cap` 和 md caption 的「图 N」是**展示序号**（按正文出现位置）。往旧文章里插图会造成展示序号重排：改新图与后面各图的 `.cap` → 重渲染被改动过的图 → 改 md caption → 正文里提过「图 N」的地方一起搜一遍。01 篇实例：`fig8` 插成图 4 后，`fig2-credential-planes` 的图 4 → 图 5。
7. 图型分工：**架构图 / 流程图用上条的 HTML 骨架手画；时序图用 mermaid 画**（用户指定，2026-09-29）。时序图源文件 = `imgs/<name>.mmd`（命名跟 HTML 图一致：`p<NN>-fig<N>-<slug>`；起手复制 `assets/fig-mermaid-template.mmd`），用 `mermaid2png.py` 渲染成 PNG——同一 480px 画布、同一图框（fig.css）、同一 686px 预览门槛。选 mermaid 是因为泳道/时序/激活这类结构在 mermaid 里是声明式的，改文案成本低；架构/流程图的版式自由度更大，手画 HTML 更可控。
8. mermaid 管线用法：

```bash
# 在 imgs/ 目录下（或 --dir 指定）：
python3 mermaid2png.py fig8-request-sequence   # 指定图（.mmd 后缀可省）
python3 mermaid2png.py                          # 不带参数 = 渲染目录里全部 .mmd
```

   - 原理：`.mmd` 包进系列图框 + 本地 `mermaid.min.js`（v11.17.2，`assets/` 与 `imgs/` 各存一份；升级就换这两份文件），用本机 Chrome 无头渲染——和官方 `mermaid-cli`（mmdc）同一个引擎，但不需要 Node；预览照旧进 `imgs/preview/`。
   - `.mmd` 顶部元信息（其余行全是 mermaid 源）：`%%cap:` 图号、`%%title:`（可内嵌 `<span>` 标蓝）、`%%lede:`、`%%foot:`；缺哪项就不渲染哪块。
   - 写作约束（手机可读性硬约束）：参与者 **≤3 列**；消息文案用 `<br/>` 手动换行、单行 ~18 字以内；字号在脚本的 `MERMAID_INIT` 里统一调（当前 message/note 15px）。
   - 踩坑：同名 `.html` 若还留着，`render.py` 批量模式会用它覆盖 PNG——旧源改名 `*.html.bak` 归档（01 篇 fig8 即此例）。
   - 模板：起手复制 `assets/fig-mermaid-template.mmd`（带用法注释的泛化骨架，可直接渲染）；实样 01 篇 `fig8-request-sequence.mmd`——三泳道 + 自环步骤（①…⑥）+ `activate` 激活条表现「包住」关系 + `rect` 区间面板标「计量区间」；02、03 篇讲一次调用时序时改文案复用。

## 控制台截图管线（实操配图）

铁律 6：实操每个 Step 一张。驱动是 `scripts/console-shot.mjs`（无头 Chrome + CDP，Node ≥22 内置 `WebSocket`，不需要浏览器插件、不受窗口大小影响）。

```bash
# 1) 登录取 cookie（密码由用户当次提供，只进环境变量，不写文件/记忆）
curl -s -c /tmp/console-cookies.txt -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"'"$HI_PASS"'"}' http://localhost:8080/session/login
export SHOT_SESS=$(awk '$6=="_hi_sess" {print $7}' /tmp/console-cookies.txt)

# 2) 截一张（纯落地页，不用交互）
node imgs/console-shot.mjs http://localhost:8080/mcp-server \
     imgs/note/p08-s1-mcp-list.png

# 3) 需要交互的：SHOT_EVAL 里点页签/按钮/切模式，再截
export SHOT_EVAL='(async()=>{ const t=[...document.querySelectorAll(".ant-tabs-tab")].find(e=>e.innerText.trim()==="工具"); t.click(); await new Promise(r=>setTimeout(r,800)); })()'
node imgs/console-shot.mjs http://localhost:8080/mcp-server/detail imgs/note/p08-s2-tool.png 3000
```

要点：

- 环境变量：`SHOT_SESS`（必填，登录 cookie 值）、`SHOT_COOKIE_NAME`（默认 `_hi_sess`）、`SHOT_ORIGIN`（cookie domain，默认 `localhost`）、`SHOT_EVAL`（截图前执行的异步脚本）、`SHOT_EVAL_WAIT`（默认 2500ms）、`SHOT_PORT`（9333）、`SHOT_W`/`SHOT_H`（1440×900，出图 @2x = 2880×1800）、`CHROME`；第三个位置参数是页面加载等待（默认 4000ms）。
- antd 选择器经验：页签用 `.ant-tabs-tab` + `innerText.trim()` 精确匹配；按钮/链接用 `button,a` + 精确文本 + `offsetParent` 非空过滤；**别用宽泛的 `div,span`**，会命中 `.ant-card-extra` 之类外层容器。滚动容器是 `.ant-drawer-body` / `.ant-modal-body`，不是 window。
- `SHOT_EVAL` 的返回值会打印成 `EVAL>`——调试时把量到的 `scrollHeight`/`clientHeight`/元素数量返回出来看，比盲猜快。
- 截完**逐张目检**（账号标识、凭证格、抽屉默认态），按 `screenshots.md` §3 脱敏、§4 插入。

## 微信 HTML

```bash
python3 wechatify.py ai-gateway-NN.md
# -> ai-gateway-NN.wechat.html （同目录）
```

- 原理：Markdown → HTML，所有样式内联（微信编辑器会剥 `<style>` 和 `class`）；图片单独成段的自动转居中 `<section>`；`*斜体*` 渲染成灰色标注。
- 生成后必须验证（见下）；再在浏览器里 `file://` 打开目检一遍排版（表格、代码块、图片居中）。

## 发布前检查清单

对 `article/` 下的目标文章跑一遍：

```bash
MD=ai-gateway-NN.md
HT=ai-gateway-NN.wechat.html

# 1) 篇幅：汉字数（第 01 篇 ~4300 作参照）
python3 -c "import re,sys; t=open(sys.argv[1]).read(); print('汉字:', len(re.findall(r'[\u4e00-\u9fff]', t)))" $MD

# 2) 图片数三处一致：MD 引用 == HTML <img> == 磁盘文件都在
grep -c '!\[' $MD; grep -c '<img' $HT; grep -o '(imgs/[^)]*)' $MD | tr -d '()' | sort -u | xargs -I{} test -f {} && echo "files ok"

# 3) HTML 无残留样式/类名
grep -cE '<style|class=' $HT   # 期望 0

# 4) 铁律 1：无「本机」叙事 —— 正文 + 文章引用的配图源码（图内文字也是发布内容；.html 与 .mmd 都扫）
grep -nE '本机|跑得动|我这台|笔记本|Intel' $MD   # 期望无输出
grep -oE 'imgs/[^)]+\.png' $MD | sed 's/\.png$//' | sort -u | while read -r b; do
  for f in "$b.html" "$b.mmd"; do
    [ -f "$f" ] && grep -nE '本机|跑得动|我这台|笔记本|Intel|实测' "$f"; done; done   # 期望无输出

# 4b) 铁律 7：正文不写源码行号（`:153-200`、`main.go:50` 这类；`:80`/`:8080`/`:443` 是端口，不算）
grep -nE '\.go:[0-9]+|:[0-9]{2,4}-[0-9]{2,4}|行号可直接对' $MD   # 期望无输出

# 4c) 铁律 8：每个 Step 都带证据（截图或入参/返回值打印）——逐 Step 数代码块与图
awk '/^#{2,3} .*Step |^\*\*Step /{if(n){printf "%-44s 围栏行 %2d 图 %d\n", substr(n,1,44), f, i} n=$0; f=0; i=0}
     /^```/{f++} /!\[/{i++} END{printf "%-44s 围栏行 %2d 图 %d\n", substr(n,1,44), f, i}' $MD
# 期望：每行「围栏行/2 + 图」>= 1；再人工读一遍——围栏里那份得是**输出/读数**（回声 Body、ai_log、
# GET 结果、config_dump），不是只有配置片段。只讲「已保存」「应该能看到」的 Step 按返工处理。

# 4d) 铁律 9：贴出来的 YAML 每个顶层键都要在正文点过名（找漏写的配置项）
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
# 「未点名」不是都要补一段——整组键一起解释（`dashscope`/`dashvector` 这种块名）算已覆盖，
# 但像 `needReference` 那样全篇没提的必须补一句「关掉/打开分别改变什么」。

# 5) 脱敏：真实 key / LAN IP / 用户名 / 本机路径（正文、HTML、全部配图源码）
grep -nE 'sk-[0-9a-f]{8}|10\.[0-9]+\.|192\.168\.|kirito|/Users/' $MD $HT imgs/*.html imgs/*.mmd   # 期望无输出

# 6) 实操截图数 == 带 UI 面的 Step 数（铁律 6；逐张目检账号标识与凭证格）
grep -c 'imgs/note/' $MD

# 7) 推 ima 前：引用块里嵌围栏会让整批 markdown 退化成纯文本（期望无输出，细则见 ima-push.md）
grep -nE '^[[:space:]]*>[[:space:]]*`{3}' $MD
```

补充人工项：系列导读表本篇加粗对；脚注三要素在；截图逐张过目（见 `screenshots.md` 第 3 节）。

## 推 ima

流程、批次切分规则、引用块内嵌围栏这个静默退化、E2BIG/WebP、汉字平衡式、推后回读判据，全部在 **`ima-push.md`**。这里只留两条最容易被忘的硬闸：

```bash
# 推前 lint：期望无输出（有输出必须先改源稿，把围栏提到引用块外）
grep -nE '^[[:space:]]*>[[:space:]]*`{3}' $MD

# 推后只信 JSON 块树：源稿 fence 对数 == 线上 code_block 数，且无节点 text 含 ```
# ima_api "openapi/note/v1/get_doc_content" '{"note_id":"<id>","target_content_format":2}'
# 不要用 format:1 自检——它会把退化段落里的围栏转义成 \`\`\`，看着像真代码块
```

## 常见故障

- `ModuleNotFoundError: markdown` → `pip install markdown`。
- render.py 出 `FAIL`：Chrome 路径不对（设 `CHROME` 环境变量）或 html 里有 `grid`/超宽元素。
- mermaid 图渲染成空白 / 显示原始代码：打开 `/tmp/mmd-build/<name>.render.html` 在浏览器里复现（多为语法错误）；换引擎版本 = 替换 `imgs/mermaid.min.js` 与 skill 的 `assets/mermaid.min.js` 两份。
- HTML 里 `<img` 数对不上：MD 里图片被包进了非独立段落（加了行内文字），wechatify 的居中逻辑不生效——图片保持独立成段。
- console-shot 报 `chrome debug port never came up`：9333 端口被上一次的 Chrome 占了，换 `SHOT_PORT` 或 `pkill -f console-shot-profile`。
- console-shot 截出来是登录页：`SHOT_SESS` 空或过期（cookie 取法见上；awk 的字段是 `$6=="_hi_sess" {print $7}`，按 `$6=="/"` 取会得到空串）。
- console-shot 截出来状态不对（抽屉没开、还在默认页签）：`SHOT_EVAL` 没点中，看 `EVAL>` 返回值定位；一次调用只能截一屏，多屏就多次调用、每次把完整动作串写进 `SHOT_EVAL`。
