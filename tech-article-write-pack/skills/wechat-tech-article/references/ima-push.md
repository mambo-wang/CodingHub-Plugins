# 推送 ima 笔记：流程与硬约束

ima 是本系列的发布留档通道。**铁律 4：本地留档随时做，推送必须先有用户明确同意**（「推送到ima」「出第 N 条笔记」这类话才算点头）。

## 0 · 两条不可逆的事实，决定了整个流程

- **没有覆盖接口。** `import_doc` / `append_doc` 是仅有的两个写接口，没有 update/replace/delete/rename。推错一次就在线上多一条旧笔记，只能由用户在 app 里手删。
- **接口返回 `code:0` 不等于内容对。** 解析退化是静默的（见 §3）。所以**推前 lint + 推后回读**两步都省不得。

由这两条推出「一次推准」的操作口径：稿子在推之前定稿（含脱敏、配图、代码块 lint），推完只做**结构核对**，不做「看着不太对再推一版」。真要修就是**再建一条新笔记**，并在汇报里明确哪条是 canonical。

## 1 · 推送流程（03 篇实测：17 批次 = 9 text + 8 image，全 ok）

```bash
SKILL=~/.agents/skills/ima-skill
OPTS=$(printf '{"clientId":"%s","apiKey":"%s"}' "$(cat ~/.config/ima/client_id)" "$(cat ~/.config/ima/api_key)")

# 1) 用 H1 那一行建笔记：只有 `# ` 行做标题，正文里不要再带 H1（否则标题重复）
node $SKILL/ima_api.cjs "openapi/note/v1/import_doc" \
  "$(node -e 'const fs=require("fs");const t=fs.readFileSync(process.argv[1],"utf8").split("\n")[0];
     process.stdout.write(JSON.stringify({content_format:1,content:t+"\n"}))' article/ai-gateway-NN.md)" "$OPTS"
# -> data.note_id

# 2) 正文（去掉首行 H1）里图片路径改绝对路径，写到临时稿；源稿一个字都不动
python3 - <<'PY'
import re
base='/…/article/'
t=open(base+'ai-gateway-NN.md').read()
body='\n'.join(t.split('\n')[1:]).lstrip('\n')
open('/tmp/push.md','w').write(re.sub(r'\]\(imgs/', ']('+base+'imgs/', body))
PY

# 3) 批次预演（--dry-run 也要求 --note-id，所以只能在建完笔记之后跑）
node $SKILL/notes/scripts/note-images.cjs --note-id <id> --file /tmp/push.md --dry-run

# 4) 正式追加
node $SKILL/notes/scripts/note-images.cjs --note-id <id> --file /tmp/push.md
```

写接口前按 ima-skill 的强制要求做 **UTF-8 校验**（`content`/`title` 全字段）。

## 2 · 批次切分规则：图片位置决定批次边界

`note-images.cjs` 按 `![alt](src)` 行切批：图片之间的**连续文本合成一批**，每张图单独一批。三条直接后果：

1. **本地图片必须绝对路径或 `file://`**，相对 `imgs/x.png` 直接 `Unsupported image source`。所以推临时稿，不改源稿；路径字符串不会进正文（回读 grep `/Users/` 应为 0）。
2. **一批出事就是「上一张图之后到这一张图之前」整段**，排查时按这个范围看，不用全文比对。
3. **批次不回滚。** 中途失败要接着推，得从失败那条开始切临时稿，别把已成功的再发一遍。

## 3 · 唯一的静默杀手：引用块里嵌围栏代码块

源稿出现 `> ```bash`（blockquote 里套 fenced code）时，ima 会**放弃整批的 markdown 解析**，把这一批 2000–4000 字塞进**一个 `p` 节点存原文**。线上看到的就是带 ` ``` `、`>`、`\*\*` 的纯文本，标题、代码块、callout 样式全丢，而接口照样返回 `ok`。

- 和篇幅无关：132 字的最小样本同样退化（03 篇用一条临时探针笔记验的，探针笔记用户手删）。
- 单层引用块（里面只有文字/行内 code）不受影响，03 篇另外三个 callout 就正常落成了 `blockquote`。

## 3b · `terminated` 不等于没收到：重试会造出重复图

05 篇实测（2026-10-07）：904 KB 的 image 批次报 `batch 4/13 failed: terminated`，脚本按批次边界停下，但**服务端其实已经把那张图落进了笔记**。照 §2 的说法从失败批次切片重推之后，回读 `cloud_image` 数 = 7（源稿 6 张），两条 图 2 的 caption 一模一样、一条 `data:image/png` 一条 `data:image/webp`。

- **任何一批失败后，先回读再决定重推范围**：`get_doc_content` `format:2` 数 `cloud_image` / `code_block`，和本地源稿对齐了才知道哪几批真没落。
- 已经落了一半又没法只补缺口时（没有 update/delete），代价就是**换一条新笔记整篇重推**，旧笔记交用户手删，汇报里写清哪条是 canonical。
- **预防**：单批 base64 控制在 ~750 KB 以内（03 篇 751 KB 平安、05 篇 904 KB 出事，中间没有实测点，别拿 1 MB 那条线当安全线）。>600 KB 的 PNG 先无损 WebP 再推（`p05-fig2` 678 KB → 249 KB，像素一致），微信 HTML 继续用 PNG。

**修**：把围栏提到引用块外面，callout 只留文字，中间加一句引入（03 篇是「补一个头就通，查询余额这条 `GET` 也一样：」）。

**防**（推前必跑，期望无输出）：

```bash
grep -nE '^[[:space:]]*>[[:space:]]*`{3}' article/ai-gateway-NN.md
```

**验**（推后必跑，只信 JSON 块树）：

```bash
node $SKILL/ima_api.cjs "openapi/note/v1/get_doc_content" \
  '{"note_id":"<id>","target_content_format":2}' "$OPTS"
```

判据三条：源稿 fence **对数** == 线上 `code_block` 节点数；`cloud_image` 节点数 == 源稿图片数；**没有任何节点的 text 里还留着 ` ``` `**。
⚠️ 不要用 `target_content_format:1` 自检——那个 Markdown 导出会把退化段落里的围栏转义成 ` \`\`\` `，肉眼和 grep 都像真代码块。`format:0` 是纯文本，图片不落进去，图缺不缺也别拿它判断。

**探针笔记**：怀疑某种写法会退化时，单独建一条一次性笔记验证（几行样本即可），别拿正式篇目试——正式篇目试错的成本是线上多一条废笔记。

## 4 · 图片体积：E2BIG 与 3 MiB 两条线

- 单张图原始字节 **< 3 MiB**（ima 侧限制）。
- `note-images.cjs` 把 base64 塞进一条 argv 发出，**超过约 1 MB 的图会 `spawnSync node E2BIG`**（macOS ARG_MAX）。02 篇 1.09 MB 的 PNG 就这么死过。
  修法：为推送临时换成**无损 WebP**（PIL `save(...,'WEBP',lossless=True,method=6)`，1.09 MB → 395 KB，像素一致，ima 收），临时稿里指到 `.webp`；微信 HTML 继续用 PNG。
  别想着缩放——LANCZOS 重采样会毁掉平色压缩，图反而更大。
- 推前 `--dry-run` 看每批 bytes，最大批控制在几百 KB 就安全（03 篇最大 751 KB，无风险）。

## 5 · 篇目一致性核对（推完顺手做，别只靠目测）

```bash
python3 - <<'PY'
import re
src=open('article/ai-gateway-NN.md').read()
alt=sum(len(re.findall(r'[一-鿿]',m)) for m in re.findall(r'^!\[([^\]]*)\]',src,re.M))
hz=len(re.findall(r'[一-鿿]',src))
print('file',hz,'alts',alt,'expect note',hz-alt)
PY
```

**汉字平衡式（两次实测精确）：`笔记汉字 = 源稿汉字 − 图片 alt 汉字`。** `get_doc_content` `format:0` 只渲染一次 H1、且丢掉所有 alt 文本，所以**不要**再 `+ 标题`（早期记的那条公式是错的）。

脱敏复扫（对线上正文）：`/Users/`、真实 key 形态、用户名、局域网 IP、`本机`、`反直觉`、`只能估` 全部应为 0 命中。

## 6 · 汇报口径

给用户：新 note id + 哪条是 canonical + 线上核对结果（code_block 数、图片数、汉字平衡）+ 需要他手删的旧笔记 id（接口删不了）。旧笔记是否保留**听用户的**，别自作主张说是错误。
