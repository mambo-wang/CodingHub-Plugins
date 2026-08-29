## 为什么（Why）

个人中心（ProfilePage）当前只有头像管理、编辑资料、修改密码，用户无法集中查看自己在平台上的互动痕迹（评论、收藏、点赞）。系统底层已有一套统一互动模型（unified_like / unified_comment / unified_favorite），收藏甚至已提供「按用户查询」接口，但点赞与评论仅支持「按目标查询」。本次在个人中心补齐这三类互动的聚合展示，并支持点击跳转到对应详情页，提升用户对自己内容的掌控感与回访效率。

## 变更内容（What Changes）

- 在 `ProfilePage.vue` 个人中心新增三个互动板块：**我的评论 / 我的收藏 / 我的点赞**，采用标签页形式内嵌展示。
- 每个板块分别按 `TOOL / FORUM_POST / VIDEO` 三种类型各拉取最近 N 条（默认 10），并支持「查看全部」展开。
- 每条互动项可点击，跳转到对应详情页：`/tools/:id`、`/forum/posts/:id`、`/videos/:id`。
- 后端新增两个「按用户查询」接口（镜像现有收藏实现）：
  - `GET /api/v1/interactions/likes/mine?targetType=` —— 返回当前用户点赞的目标资源 DTO。
  - `GET /api/v1/interactions/comments/mine` —— 返回当前用户的评论列表，并附带每条评论所属目标的类型、ID 与标题。
- 收藏板块复用已有的 `GET /api/v1/interactions/favorites?targetType=`，分三次（三种类型）调用。
- 所有「我的」查询仅统计登录用户（userId）的数据，过滤已软删除的目标，避免产生死链。

## 能力清单（Capabilities）

### 新增能力（New Capabilities）
- `profile-interactions`: 个人中心聚合展示当前用户的评论、收藏、点赞，并支持点击跳转至工具/帖子/微课详情页。

### 修改能力（Modified Capabilities）
- `unified-interactions`: 在统一互动服务中新增「我的点赞」与「我的评论」两个按用户查询的接口（此前仅支持按目标查询）。

## 影响范围（Impact）

- **后端**
  - `UnifiedInteractionController`：新增 `likes/mine`、`comments/mine` 两个 GET 端点。
  - `UnifiedLikeService` / `UnifiedLikeRepository`：新增按 userId + targetType 分页查询并解析目标 DTO 的逻辑。
  - `UnifiedCommentService` / `UnifiedCommentRepository`：新增按 userId 分页查询，并解析目标标题（tool 名称 / 帖子标题 / 视频标题）。
  - 复用现有 `ToolSummaryDTO` / `ForumPostSummaryDTO` / `VideoListItem` 作为点赞/收藏的返回结构；评论需新增轻量 DTO（含 targetType、targetId、targetTitle、content、createdAt）。
- **前端**
  - `services/interaction.ts`：新增 `getMyLikes(targetType)`、`getMyComments()`。
  - `pages/ProfilePage.vue`：新增三个互动板块（标签页 + 列表 + 跳转）。
  - 复用现有详情页路由（`ToolDetail` / `ForumPostDetail` / `VideoDetail`），无需新增路由。
- **依赖与约束**
  - 继承现有统一互动的 `TargetType` 枚举（TOOL / FORUM_POST / VIDEO）、JWT 鉴权、软删除过滤与 XSS 防护规则。
  - 不改变现有「按目标」接口行为，属纯增量，无破坏性变更。
