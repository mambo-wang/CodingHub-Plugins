# 实操截图：取用与脱敏流程

带 UI 面的实操 Step 才配图（铁律 6）；纯命令行 Step 用输出打印当证据，不截终端凑数。截图两条来源：**A 无头 Chrome 自截是首选**；**B ima 笔记来源**只在用户主动给笔记（或目标 UI 不可达）时用。共用第 3 节脱敏与第 4 节插入规范。

## 1 · A 来源：headless Chrome 自截（首选）

工具：`scripts/web-shot.mjs`（Node ≥22 内置 WebSocket + CDP，无需 puppeteer）。工作区 `article/imgs/web-shot.mjs` 若存在优先用工作区那份。

为什么不用应用内浏览器（browser-use MCP）：它在 SPA 上常报 `NATIVE_BROWSER_VIEWPORT_UNAVAILABLE`，合成点击也常常落空。直接走本管线。

### 1.1 会话 cookie（目标 UI 需要登录时才做）

```bash
# 登录接口按目标产品而定；口令当次向用户索取（项目记忆有明确授权的除外）
curl -s -c /tmp/shot-cookies.txt -o /dev/null -w '%{http_code}\n' \
  -X POST http://localhost:<port>/<login-path> \
  -H 'Content-Type: application/json' -d '{"username":"...","password":"..."}'
export SHOT_SESS=$(awk '$6=="<cookie名>" {print $7}' /tmp/shot-cookies.txt | head -1)
export SHOT_COOKIE_NAME=<cookie名>
```

- 口令只进环境变量与 `/tmp`，不落正文、配图、脚本常量、ima、任何远端。
- cookie 域用 `SHOT_ORIGIN` 覆盖（默认 `localhost`）。过期就重新登录取一次。
- 无需登录的 UI 不设 `SHOT_SESS`，脚本直接导航。
- 报 `chrome debug port never came up` 基本都是上一次的无头 Chrome 还占着 9333：`pgrep -f console-shot-profile-9333` 找到 PID，确认 `--user-data-dir` 是本管线建的，`kill -TERM` 后重跑；或换 `SHOT_PORT=9444`。

### 1.2 逐 Step 截图

```bash
node scripts/web-shot.mjs "http://localhost:<port>/<page>" imgs/note/<slug>-s1-<name>.png 5000
```

- 每次调用是**全新导航**，状态不跨调用保留。「点页签再点按钮」整串写进一个 async 的 `SHOT_EVAL`（脚本打印 `EVAL>` 返回值确认点没点中）：

  ```bash
  export SHOT_EVAL="(async()=>{const s=ms=>new Promise(r=>setTimeout(r,ms));
    const tab=t=>[...document.querySelectorAll('.ant-tabs-tab')].find(e=>e.textContent.trim()===t);
    const btn=t=>[...document.querySelectorAll('button,a')].find(e=>e.textContent.trim()===t&&e.offsetParent);
    tab('目标页签')?.click(); await s(2000); btn('目标按钮')?.click(); await s(2500);
    return document.querySelector('.ant-modal-body,.ant-drawer-body')?'ok':'NODIALOG';})()"
  ```

- 选择器经验（antd 系 UI；其他框架先 take_snapshot/DOM 探查再定选择器）：页签 `.ant-tabs-tab`、按钮/链接 `button,a`，都按**精确文本**匹配并要求 `offsetParent` 非空；宽泛的 `div,span` 会命中外层容器而点不动。滚动容器一般是 `.ant-drawer-body` / `.ant-modal-body`，先比 `scrollHeight` 与 `clientHeight` 再滚。
- 对话框/抽屉**默认态未必是文章要的那一态**。截前先用 `EVAL>` 回读正文文本确认状态。
- 视口默认 1440×900 @2x，但**发布用的图一律 `SHOT_CLIP` 只截文章要的那块**：侧栏、顶栏、页脚、版本号不进图——版本归属由正文承担。抽屉用 `.ant-drawer-body`，列表/表单截承载它的卡片容器。
  ```bash
  SHOT_CLIP='.ant-drawer-body' node scripts/web-shot.mjs <url> imgs/note/<name>.png 5000
  ```
  元素比视口高时脚本滚到顶部并开 `captureBeyondViewport`；`SHOT_CLIP` 选不中直接报错退出，不会静默出整页图。
- **`SHOT_H` 才是决定截全与否的旋钮**：抽屉 body 自己就是滚动容器，bounding rect 只有视口高，**长表单会被静默裁掉下半部分**，`captureBeyondViewport` 救不了。先量再截：`SHOT_EVAL` 回读表单 `scrollHeight`，再 `export SHOT_H=$((sh+200))`。
- 要截**页面级的一块**（卡片网格、表格区域）时，`SHOT_CLIP` 按类名常选不中或命中多个。正确做法：`SHOT_EVAL` 里给目标元素打临时 id（`t.id='shot-target'`），再 `SHOT_CLIP='#shot-target'`。网格可读性：1440 视口下 4 列卡片压到 686px 手机宽就糊了——`SHOT_W=820` 让 antd 回落 2 列，必要时 PIL 按行裁掉用不到的行。
- 事后补裁是退路不是正路：已截成整页时按「白色面板边界 + 最后一行有内容的行」定位补裁，整页原片留 `imgs/note/_full/*.full.png` 溯源。

### 1.3 一个 Step 一张，贴在该 Step 的配置/命令片段之后

实操有几个带 UI 面的 Step 就截几张。

## 2 · B 来源：ima 笔记（用户给笔记时）

ima OpenAPI 读不了分享页、导不出图片，但**分享页在浏览器里不用登录就能完整渲染**，图片是签名的临时 COS 直链。

1. 分享链接形如 `https://ima.qq.com/note/share/<token>?channel=4`，浏览器打开等 DOM 稳定。
2. `evaluate_script` 跑 TreeWalker，把正文按 DOM 顺序抽成 `{text, img}` 序列存 `imgs/_note_manifest.json`。合并文本**累积全文**别截断；每张图往前留约 260 字上下文判断归属；JSON 可能双重编码，`json.loads(json.loads(raw))` 兜底。
3. 图片下载**必须带** `User-Agent` + `Referer: https://ima.qq.com/`；**签名约 24 小时过期**，别缓存 URL。存 `imgs/note/<slug>.webp` 并转 PNG。
4. 对照 manifest 归位：对不上的先存着不硬插；缺图问用户要，别用相似的凑。

## 3 · 脱敏（强制，不做完不插入）

逐张扫描五类目标：

1. **凭证/表单格子**（API key、令牌、密码框）；
2. **终端提示符**（用户名@主机名）；
3. **浏览器地址栏/书签栏**（LAN IP、内网域名、个人书签）；
4. **监控/控制台变量框**（数据源地址、变量值）；
5. **右上角账号标识**（头像 + 用户名）——整页截图必中，涂白即可；元素级截图通常在框外，确认过就不用动。

命中就涂：PIL 打开 → 2x 探针裁片量坐标 → 画白矩形 → 需要写字用 Arial（`/System/Library/Fonts/Supplemental/Arial.ttf`）画掩码文本（如 `sk-****`）。涂完**重新打开目检**确认无残余。

演示用的别名、端口、`<占位符>`**不算敏感**，正文里本来就有，保留。

## 4 · 裁边、插入与溯源

- 底部大片留白可裁，但别裁掉有信息的行；一律先 `SHOT_CLIP` 截元素，再裁元素内部的空白尾巴。
- 插入位置：对应 Step 的配置/命令片段之后，单独成段，配一句桥接说明这屏看什么。
- alt 写法：`![界面：工具列表，demo-server 一行，类型 OpenAPI](imgs/note/<name>.png)`——描述自足。
- **来源凭据不删**：B 来源 webp 原件 + manifest 留在 `imgs/note/`；A 来源把截图时的 `SHOT_EVAL` 关键动作记进事实台账，方便重截。