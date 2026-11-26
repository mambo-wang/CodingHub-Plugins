# 实操截图：取用与脱敏流程

实操章节的截图有两条来源。**A 控制台自截是首选**——逐 Step 自己截，构图可控、能覆盖文章真正要讲的那一屏；**B ima 笔记来源**只在用户主动给笔记（或控制台不可达）时用。两条来源共用第 3 节的脱敏与第 4 节的插入规范。

## 1 · A 来源：headless Chrome 自截（首选）

工具：`scripts/console-shot.mjs`（Node ≥22 内置 WebSocket + CDP，无需 puppeteer/mmdc 一类依赖）。工作区 `article/imgs/console-shot.mjs` 若存在优先用工作区那份，与本脚本保持一致。

为什么不用应用内浏览器（browser-use MCP）：它在控制台这类 SPA 上报 `NATIVE_BROWSER_VIEWPORT_UNAVAILABLE`，合成点击也常常落空。**别再试它**，直接走本管线。

### 1.1 拿会话 cookie

```bash
curl -s -c /tmp/console-cookies.txt -o /dev/null -w '%{http_code}\n' \
  -X POST http://localhost:8080/session/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"<用户当次提供>","password":"<用户当次提供>"}'   # 201 = 成功
export SHOT_SESS=$(awk '$6=="_hi_sess" {print $7}' /tmp/console-cookies.txt | head -1)
```

- 口令按项目记忆走：用户 2026-10-10 已授权把本机 trial 控制台的 `admin` 口令存进项目记忆（见 `[[higress-console-credentials]]` 一类的条目），**别再每次问**。授权范围只有这台机器的这套栈：口令不进正文、配图、脚本常量、ima、任何远端；截图里出现账号标识或凭据格子一律涂白。控制台凭据在 nacos 里是 `enc|…` 加密存的，别想着还原，也别试默认密码。
- cookie 名/域可用 `SHOT_COOKIE_NAME` / `SHOT_ORIGIN` 覆盖（Higress 控制台是 `_hi_sess` @ localhost）。会话过期就重新 `POST /session/login` 取一次，`SHOT_SESS` 只存 `/tmp` 下。
- 驱动报 `chrome debug port never came up` 基本都是**上一次会话遗留的无头 Chrome 还占着 9333**（不是 Chrome 装坏了）：`pgrep -f console-shot-profile-9333` 找到 PID，确认 `--user-data-dir` 是本管线建的，`kill -TERM` 后重跑；或换 `SHOT_PORT=9444`。

### 1.2 逐 Step 截图

```bash
node scripts/console-shot.mjs "http://localhost:8080/mcp/list" /tmp/shot-step1.png 5000
```

- 每次调用是**全新导航**，页面状态不跨调用保留。需要「点页签再点按钮」时，把整串动作写进一个 async 的 `SHOT_EVAL`（`awaitPromise:true`，脚本会打印 `EVAL>` 返回值用来确认点没点中）：

  ```bash
  export SHOT_EVAL="(async()=>{const s=ms=>new Promise(r=>setTimeout(r,ms));
    const tab=t=>[...document.querySelectorAll('.ant-tabs-tab')].find(e=>e.textContent.trim()===t);
    const btn=t=>[...document.querySelectorAll('button,a')].find(e=>e.textContent.trim()===t&&e.offsetParent);
    tab('工具')?.click(); await s(2000); btn('编辑工具')?.click(); await s(2500);
    return document.querySelector('.ant-modal-body,.ant-drawer-body')?'ok':'NODIALOG';})()"
  ```

- 选择器经验（antd 系通用）：页签 `.ant-tabs-tab`、按钮/链接 `button,a`，都按**精确文本**匹配并要求 `offsetParent` 非空；用宽泛的 `div,span` 会命中外层容器（如 `.ant-card-extra`）而点不动。滚动容器一般是 `.ant-drawer-body` / `.ant-modal-body`，先比 `scrollHeight` 与 `clientHeight` 再滚。
- 对话框/抽屉**默认态未必是文章要的那一态**（例：MCP 编辑工具对话框默认 Swagger 模式，要点「YAML模式」卡片才是要截的编辑器）。截前先用 `EVAL>` 回读正文文本确认状态。
- 视口默认 1440×900 @2x，但**发布用的图一律用 `SHOT_CLIP` 只截文章要的那块**（用户明确要求，2026-10-02：「截的图是整个屏幕的，能不能改成截取我们需要的那部分」）。侧栏、顶栏、页脚、页脚版本号都不进图——版本归属由正文和文末引文承担。抽屉用 `.ant-drawer-body`（或 `.ant-drawer-content-wrapper` 连标题栏一起要），列表/表单页截承载它的那张卡片容器（`.ant-card`、`.ant-table-wrapper`）。
  ```bash
  SHOT_CLIP='.ant-drawer-body' node scripts/console-shot.mjs <url> imgs/note/p03-s1-x.png 5000
  ```
  元素比视口高时脚本会滚到顶部并开 `captureBeyondViewport`，能截全；`SHOT_CLIP` 选不中元素直接报错退出，不会静默出整页图。
- **`SHOT_H` 才是决定截全与否的旋钮**（06 篇踩的坑）：`.ant-drawer-body` 自己就是滚动容器，它的 bounding rect 只有视口高，所以**长表单会被静默裁掉下半部分**，`captureBeyondViewport` 救不了——它超出的是元素自己的滚动高度，不是页面高度。先量再截：跑一段 `SHOT_EVAL` 回读 `document.querySelector('.ant-drawer-body form').scrollHeight`，再 `export SHOT_H=$((sh+200))`（06 篇实测：RAG 表单 1364→1560、历史 1057→1260、配额 971→1180；YAML 编辑器一律 600）。
- 要截的是**页面级的一块**（策略配置页的插件卡片网格、表格区域）而不是抽屉时：`SHOT_CLIP` 按类名常常选不中（`.ant-collapse-item-active` 能匹配到 7 个面板）。正确做法在 `SHOT_EVAL` 里给目标元素打一个临时 id（`t.id='shot-target'`），再 `SHOT_CLIP='#shot-target'`。网格还有一层可读性问题：1440 视口下卡片是 4 列，压到 686px 手机宽就糊了——`SHOT_W=820` 让 antd 回落到 2 列（卡片 322 宽、行距 221px），必要时再用 PIL 按行裁掉文章用不到的行。
- 事后补裁是退路不是正路：已经截成整页时，按「白色面板左边界 + 最后一行有内容的行」自动定位（03 篇五张就这么救回来的，脚本口径：从 x=1100 起第一个全白列即抽屉左边，行内像素 <245 的最后一行 +46px 为底）。整页原片留 `imgs/note/_full/*.full.png` 作溯源。

### 1.3 一个 Step 一张，贴在该 Step 的落库 YAML 之后

实操有几个带 UI 面的 Step 就截几张（08 篇是 4 张：列表、编辑抽屉、工具 YAML、请求认证）。纯命令行 Step 不配图，别为凑数截终端。

## 2 · B 来源：ima 笔记（用户给笔记时）

ima 的 OpenAPI 读不了分享页、导不出图片，但**分享页在浏览器里不用登录就能完整渲染**，图片是签名的临时 COS 直链。

1. 分享链接形如 `https://ima.qq.com/note/share/<token>?channel=4`，用应用内浏览器打开（读笔记正文可以，截图不行），等 DOM 稳定。
2. `evaluate_script` 跑 TreeWalker，把正文按 DOM 顺序抽成 `{text, img}` 序列，存 `article/imgs/_note_manifest.json`。合并文本要**累积全文**别截断（第一版截到 100 字，把「添加消费者：」这类关键标签截没了，图片就对不上步骤）；每张图往前留约 260 字上下文判断归属；JSON 可能被双重编码，读时 `json.loads(json.loads(raw))` 兜底。
3. 图片 URL 形如 `https://ima-notebook-prod.image.myqcloud.com/.../<hash>.webp?q-sign-algorithm=sha1&...`，普通 urllib 可下但**必须带** `User-Agent` + `Referer: https://ima.qq.com/`；**签名约 24 小时过期**，别缓存 URL。存 `imgs/note/<slug>.webp` 并转 PNG。
4. 对照 manifest 归位：对不上的先存着不硬插；一图多处选最贴近的 Step；缺图问用户要，别用相似的凑。

## 3 · 脱敏（强制，不做完不插入）

逐张扫描五类目标：

1. **凭证/表单格子**（API key、令牌、密码框）；
2. **终端提示符**（用户名@主机名）；
3. **浏览器地址栏/书签栏**（LAN IP、内网域名、个人书签）；
4. **Grafana/控制台变量框**（数据源地址、变量值）；
5. **控制台右上角账号标识**（头像 + 用户名）——整页截图必中，涂白矩形即可；抽屉/弹窗截图通常被遮，确认过就不用动。

命中就涂：PIL 打开 → 2x 探针裁片量坐标 → 画白矩形 → 需要写字用 Arial（`/System/Library/Fonts/Supplemental/Arial.ttf`）画掩码文本（如 `sk-****`）。涂完**重新打开图片目检**，确认无残余。

本案记录：01 篇 `ai-service.png` 凭证格暴露真实 key 前缀 `sk-6**********（已略）` → 涂白改写 `sk-****`；08 篇两张整页截图右上角 `admin` 标识 → 涂白。

演示用的容器别名（如 `weather.internal`）、端口、`<higress-gateway-ip>` 占位符**不算敏感**，正文里本来就有，保留。

## 4 · 裁边、插入与溯源

- 底部大片留白可裁（01 篇 `ai-service.png`、`consumer.png` 处理过），但别裁掉有信息的行；自截一律先按上一条的 `SHOT_CLIP` 截元素，截完再裁掉元素内部的空白尾巴。
- 插入位置：对应 Step 的落库 YAML 片段之后（或之前），单独成段，配一句桥接说明这屏看什么。
- alt 写法：`![控制台：MCP 管理列表，weather-mcp 一行，服务类型 OpenAPI](imgs/note/p08-mcp-list.png)`——微信不渲染 alt 成图注，描述要自足。
- **来源凭据不删**：B 来源的 webp 原件 + manifest 留在 `imgs/note/`；A 来源保留 `/tmp` 原片无意义，落盘即终稿，但把截图时的 `SHOT_EVAL` 关键动作记进项目记忆，方便重截。
