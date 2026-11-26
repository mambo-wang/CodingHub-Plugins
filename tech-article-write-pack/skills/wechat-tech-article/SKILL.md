---
name: wechat-tech-article
description: 生成、续写或润色《Higress AI 网关全解析》类公众号技术长文。固定「是什么 → 怎么工作 → 分步骤实操 → 小结与系列导读」四段结构；含配图管线（HTML 画图 + Chrome 渲染 PNG、mermaid 时序图转 PNG）、实操阶段无头 Chrome 自截控制台截图（逐 Step 一张、`SHOT_CLIP` 只截重点元素）与脱敏流程、实操逐 Step 证据链（入参/返回值打印、`ai_log` 台账、回声上游取证配方）与逐键配置语义核对、微信内联样式 HTML 转换、发布前验证清单、推送 ima 笔记的批次切分与回读校验规则、本地留档规则。当用户要求写/生成/更新系列第 NN 篇、公众号技术长文、给文章配图、给实操章节截图、给实操补效果证据、解释或核对某一步的配置项、转微信 HTML、推送 ima 时使用。
---

# 公众号技术长文生成（AI 网关系列）

产出「可直接发公众号」的技术长文：中文源稿 Markdown + 微信内联样式 HTML + 配图 PNG。结构与文风按本 skill 固化，素材来自官方文档、源码核验和本地实验。

## 触发场景

- 写《Higress AI 网关全解析》下一篇（第 02–11 篇）
- 对既有篇目润色、改结构、换配图、重新生成 HTML
- 给文章配原理图 / 给实操章节逐步截控制台图 / 从 ima 笔记取截图
- 定稿后推送 ima

## 铁律（先读，违了就是返工）

1. **不写「本机验证」框架。** 用户原话：「你不用提本机能不能验证之类的，你就介绍功能和工作原理」。数字在写作时于本机核实，但以**产品事实**呈现——挂版本号或源码出处（如「v2.2.4 与 main 分支一致」「网关镜像 2.2.4 配套插件全是 2.0.1」），出处的写法见铁律 7（**有版本、有标识符名，没有行号**）；不出现笔记本规格、Docker 资源分配、容器内存合计、「跑不跑得动」这类元叙事。**配图、截图里会渲染成图的文字同样是发布内容，一并检查**（正文清干净了、图里没清，是踩过的坑）。
2. **每篇一个反直觉论点**（一句话立场，不是话题）。`references/series-map.md` 里备有 02–06 的草案。
3. **脱敏红线。** 上游 key 一律 `sk-****`；消费者 key 用 `sk-higress-local`；不出现局域网 IP、主机名、`/Users/...` 路径。**每张截图插入前逐张扫描**：凭证格子、终端提示符、浏览器地址栏/书签、Grafana 变量、**控制台右上角账号标识（头像 + 用户名）**——按铁律 6 截元素帧时它天然在框外，但只要有整页帧（含事后没裁干净的）就必中，涂白后再插。控制台密码：用户已在 2026-10-10 授权把本机 trial 控制台的口令存进项目记忆（`higress-console-credentials.md`），**别再每次问**；但口令只用于本机栈，绝不写进正文、脚本常量、ima 笔记或任何远端，也不进截图。换环境/远端控制台时仍需当次索取。
4. **本地留档，同意才推。** 写文件、生成 HTML 随时做；**推 ima 必须先经用户明确同意**。ima 只有 `import_doc`/`append_doc` 两个写接口，**没有覆盖也没有删除**，所以一次推准：推错/改稿的代价是线上多一条旧笔记（由用户手删），别用正式篇目试接口行为。**推送流程与硬约束全部在 `references/ima-push.md`**（批次按图片位置切分、引用块内嵌围栏会让整批静默退化成纯文本、E2BIG 与无损 WebP、推后 `target_content_format:2` 回读判据、汉字平衡式）。
5. **结构固定。** 标题 `# AI 网关系列 NN｜…`；四段式 `一、是什么 / 二、怎么工作 / 三、实操 / 四、小结与系列导读`；段间用 `---`。**「二、怎么工作」必须至少配一张原理图**——架构图 / 流程图 / 时序图，三选一起步；图贴着对应机制小节放（01 篇该节是三张齐备的样板）。**画法分工：架构图 / 流程图用 HTML 骨架手画；时序图用 mermaid 源（`.mmd`）+ `mermaid2png.py` 渲染**（见 §3 与 `toolchain.md` 第 7–8 条）。
6. **「三、实操」逐 Step 配控制台截图，而且只截重点元素。** 一个 Step 一张，贴在该 Step 的落库 YAML 之后；纯命令行 Step 不配图，别为凑数截终端。截图用无头 Chrome 自己截（`scripts/console-shot.mjs` + CDP），**必须带 `SHOT_CLIP=<选择器>` 只截文章要的那块**（抽屉 `.ant-drawer-body`、列表/表单截承载它的 `.ant-card` / `.ant-table-wrapper`）——侧栏、顶栏、页脚一律不进图，用户原话：「你截的图是整个屏幕的，能不能改成截取我们需要的那部分」；整屏帧算返工，版本归属由正文承担。图还得是**文章要的那一态**（对话框/抽屉默认态常常不是，得先用 `SHOT_EVAL` 点开对应页签或模式）。流程见 `references/screenshots.md`。
7. **正文不写源码行号。** 用户明确要求（2026-10-14：「把内容中写的代码行号去掉」）。`main.go:50-56`、`` `:153-200` ``、「源码路径相对 …，行号可直接对」这类定位一律不进发布稿——读者在手机上读，行号既对不上也用不上。断言的可核查性靠这三样撑：**版本锚**（「v2.2.4 的源码里」「同一个 tag 的响应侧」）、**标识符名**（`checkList`、`DontReadRequestBody()`，或原样引用的一行代码）、**运行证据**（`config_dump`、Nacos 落库文件、`ai_log` 读数）；文件级线索（`http_wrapper.go`）可以留，行号不要跟。研究阶段仍然照记 `path:line`，那份定位写进 `[[higress-*-facts]]` 一类的记忆/工作笔记里备查。发布前用 `toolchain.md` 清单第 4b 条 grep 复查（端口 `:80`/`:8080` 不算）。
8. **「三、实操」每个 Step 都要交出一份能看见效果的证据——截图或入参/返回值的打印都可以。** 用户原话（2026-10-14：「感觉实操步骤没有把可以看到效果的各个命令完整的输入输出展示出来……如何确认确实传了历史记录」「可以把相关证据或者接口输入输出也展示出来吗」；2026-10-14 复核后追加：「更新的 skill 里，实操阶段每个步骤要有这种证据链，截图或者入参返回值的打印都可以」）。只有命令、只有「配置已保存」的 Step 算返工：命令和期望输出成对贴，输出原样进代码块。断言「这个插件到底改了什么字节」时，日志与回答都反推不出来，要搭**回声上游**（provider `openaiCustomUrl` 临时指向只回吐自身收到的 Body 的 OpenAI 兼容服务，跑完切回），并在正文开头约定记号（`<absent>`、`N chars`、`host=` 用来分辨网关最终调用与插件自己发起的调用）。组件互相覆盖时给**单变量对照组**、把全开终态收在最后一步当验收。四种证据形状与完整写法见 `references/article-structure.md`「三、实操」；配方已实测于 `[[higress-prompt-rag-plugin-facts]]`。
9. **贴出来的每一份配置，逐键讲清「它控制什么 / 不写取什么缺省 / 写错或漏写是什么后果」。** 用户 2026-10-15 对着 Step 4 的表单说的：「解释一下实操第四步这个插件表单配置的作用」——他要的是**键级语义**，不是「这段 YAML 配了检索」。三类必须落到源码（`parseConfig` 的取值分支、引擎构造器里的 `if x == 0 { x = 默认 }`、`NeedExectue` 这类执行条件）而不是文档：缺省值、校验失败会不会让整份配置加载不起来、哪些键只在另一个键打开时才被读（如 `referenceFormat`/`referenceLocation` 只在 `needReference: true` 时读）。**最容易写漏的是「配了但根本不执行」**：执行条件挂在别的键上时，单看这段 YAML 以为生效、其实一次调用都不发（`ai-search` 的 `type: arxiv` 只在 `EngineType == "arxiv"` 时跑，而这个值只可能由 `searchRewrite` 的返回值解析出来——不配 `searchRewrite`，arxiv 引擎一次都不会被查询）。这类事实用铁律 7 的写法表达：标识符名 + 缺省值 + 后果，不写行号。逐键说明优先做进该 Step 的正文或 callout；读者要抄的那份配置，不能只靠抄完就完事。

## 工作流

### 0 · 定位
- 读 `references/series-map.md`：取本篇主题、核心论点、与相邻篇的衔接、第 01 篇已埋的跨篇预告。
- 读工作区 `article/ai-gateway-series-outline.md`（若有）当素材库；它是旧编号写的，编号以系列地图为准。
- 读前一篇成稿：新文章要兑现旧文预告、回扣旧文结论。

### 1 · 研究核验
- 官方文档：概括 + 链接，不整段搬运。
- 机制类断言必须落到源码（研究阶段记 `path:line`，**行号只留在笔记里，正文不写**，见 `references/writing-style.md`）或运行配置（`config_dump`、Nacos 落库文件）。
- 实验照跑照测，写作按铁律 1 呈现。他人博客的未验证说法先核再写（例：`ai-proxy` 的 `keepOriginalToken` 并不存在）。

### 2 · 起草
- 结构与首尾范式见 `references/article-structure.md`；文风与禁则见 `references/writing-style.md`。
- 篇幅参照第 01 篇 ~4300 汉字；坑写进对应步骤，不单开章节；结尾放系列导读表并加粗本篇。
- 起草「三、实操」时就按铁律 8 规划证据链：先想清楚这一步的「效果」在哪个通道可见（接口返回值 / `ai_log` 台账 / `config_dump` / 旁证存储），需不需要为它搭回声上游或假服务，别写完命令再回头补输出。
- 同一轮起草按铁律 9 过一遍每一份贴出来的配置：逐键记「控制什么 / 缺省值 / 写错漏写的后果」，缺省值和执行条件去源码的 `parseConfig` 与构造器里核实；尤其查一遍「这段配置里有没有哪个键挂空——配了但运行时不读、或要另一个键打开才执行」。
- 初稿就按目标文风写，别留「之后再去 AI 味」的债。

### 3 · 配图与截图
- 原理图两条管线：**架构 / 流程图**——从 `assets/fig-template.html` 起手 + `assets/fig.css`，命名 `p<NN>-fig<N>-<slug>.html`，用 `render.py` 渲染；**时序图**——写 `p<NN>-fig<N>-<slug>.mmd`（顶部 `%%cap/%%title/%%lede/%%foot` 元信息 + mermaid 源），用 `mermaid2png.py` 渲染（起手模板 `assets/fig-mermaid-template.mmd`，实样：01 篇 `fig8-request-sequence.mmd`）。两条管线都出 `imgs/preview/` 686px 手机预览，**必须过目**。更多见 `references/toolchain.md`。
- **「二、怎么工作」至少一张原理图**（铁律 5）。图型按内容选：分层 / 组件关系 → 架构图；一条数据路径 → 流程图；跨方向或跨时间的协作（请求下行 / 响应上行）→ 时序图（走 mermaid 管线）。
- 截图（铁律 6）：**实操每个 Step 一张控制台截图，且只截重点元素**，用 `scripts/console-shot.mjs` 无头自截（登录取 cookie → `SHOT_EVAL` 点开目标页签/模式 → **`SHOT_CLIP=<选择器>` 只截那块** → 存 `imgs/note/p<NN>-s<N>-<slug>.png`）；截图后**先脱敏再插**（账号标识、凭证格），流程与事后补裁的坐标口径见 `references/screenshots.md`。ima 笔记来源是备选路径（同一文件 §2）。
- 插入格式：原理图 `![图 N：标题](imgs/p02-fig1-x.png)`；截图 `![控制台：动作](imgs/note/x.png)`。alt 在微信不渲染成图注，只当描述——图注信息写进 alt 和正文。

### 4 · 生成微信 HTML
- `python3 scripts/wechatify.py ai-gateway-NN.md`（工作区 `article/wechatify.py` 存在就优先用它）→ 同目录 `.wechat.html`。
- 验证：HTML 里 `<img` 数 == MD 里 `![` 数；无 `<style>`、无 `class=`；浏览器打开目检。

### 5 · 验证与交付
- 跑 `references/toolchain.md` 末尾的检查清单（汉字数、图片数、脱敏 grep、「本机」grep、行号 grep 期望 0、逐 Step 证据链清点、逐键配置语义清点）。
- 汇报：两个文件链接 + 一句话改了什么；如实说明没验到的部分。
- 推送 ima：用户点头后才做，按 `references/ima-push.md` 全流程走（临时稿绝对路径、`--dry-run` 看批次、`import_doc` 只用 H1 那行、推完 `target_content_format:2` 回读）。**推前必跑 `grep -nE '^[[:space:]]*>[[:space:]]*\`{3}'`：引用块内嵌围栏会让 ima 把整批内容当纯文本存入、代码块样式全丢，而接口照样返回 ok**；推后判据是源稿 fence 对数 == 线上 `code_block` 节点数、`cloud_image` 数 == 图片数、无节点 text 残留 ` ``` `，并用汉字平衡式（笔记 = 源稿 − 图注）核对完整性。

## 工作区约定

```
article/
├── ai-gateway-NN.md            # 本篇源稿
├── ai-gateway-NN.wechat.html   # 微信 HTML（生成物）
├── ai-gateway-series-outline.md
├── wechatify.py                # 优先用工作区这份
└── imgs/
    ├── p02-fig1-….html/.png    # 架构/流程图（新约定，旧 figN-* 勿改名）
    ├── p02-fig2-….mmd/.png     # 时序图（mermaid 源）
    ├── fig.css  render.py  mermaid2png.py  mermaid.min.js
    ├── console-shot.mjs        # 无头 Chrome 控制台截图驱动
    ├── note/                   # 截图（自截 PNG / ima webp 原件 + _note_manifest.json）
    └── preview/                # 686px 手机预览
```

历史工作区：`/Users/kirito/Documents/Qoder/2026-09-28/c6250ae3/article/`（若已迁移，向用户确认新位置；新工作区按上面布局初始化，脚本和样式从本 skill 拷）。当前工作区：`/Users/kirito/Documents/Qoder/higress-ai-gateway-series/article/`。

依赖：`python3 -m pip install markdown pillow`；渲染需要 Chrome；控制台截图需要 Node ≥22（用内置 `WebSocket` 跑 CDP）。

## Resources

- `references/article-structure.md` — 四段结构逐节写法、首尾范式、图注规范
- `references/writing-style.md` — 文风、禁则、数字呈现、脱敏细则
- `references/series-map.md` — 11 篇地图、各篇论点、01 已埋预告、旧提纲对照
- `references/screenshots.md` — 实操逐 Step 控制台自截（无头 Chrome + CDP + `SHOT_CLIP` 元素级截图）、ima 笔记备选来源、脱敏与插入规范
- `references/ima-push.md` — 推送 ima 笔记全流程：批次按图片位置切分、引用块内嵌围栏的静默退化与 lint/回读判据、E2BIG 与无损 WebP、汉字平衡式、探针笔记验写法
- `references/toolchain.md` — 配图/HTML/验证命令与脚本用法
- `scripts/wechatify.py` — Markdown → 微信内联样式 HTML
- `scripts/render.py` — 配图 HTML → PNG + 手机预览
- `scripts/mermaid2png.py` — mermaid（`.mmd`）→ 图框 PNG + 手机预览（本机 Chrome 跑 mermaid.js，无需 Node）
- `scripts/console-shot.mjs` — 无头 Chrome + CDP 截控制台图（注入登录 cookie、按脚本点开页签/抽屉再截）
- `assets/fig.css`、`assets/fig-template.html` — 配图样式与骨架
- `assets/fig-mermaid-template.mmd` — 时序图起手模板（元信息 + 三泳道骨架，可直接渲染）
- `assets/mermaid.min.js` — 本地 mermaid 引擎（v11.17.2，配 mermaid2png.py 使用）
