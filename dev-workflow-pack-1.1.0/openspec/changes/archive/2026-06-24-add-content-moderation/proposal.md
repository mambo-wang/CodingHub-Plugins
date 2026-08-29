## 为什么（Why）

当前工具、帖子、微课的删除和编辑权限仅限创建者本人，管理员（ADMIN/SUPER_ADMIN）无法对违规内容进行治理。需要引入内容审核权限，让管理员能够删除和编辑任何用户创建的工具、帖子、微课，以支撑社区内容治理场景。同时，现有前端在列表页（hover 态）和详情页缺少统一的删除/编辑操作入口，且帖子编辑页、微课编辑页尚未补齐，需要一并完善。

## 变更内容（What Changes）

- 后端：`ToolService`、`ForumPostService`、`VideoService` 的 `delete` 和 `update` 方法权限校验从「仅创建者」扩展为「创建者或管理员（ADMIN/SUPER_ADMIN）」
- 后端：三个 Service 方法签名从接收 `Long userId` 改为接收 `User user`，以便获取角色信息
- 前端：新增 `useContentPermissions` composable，统一计算 `canEdit` / `canDelete` 权限
- 前端：工具列表页（HomePage）、帖子列表页（PostListPage）、微课列表页（VideoListPage）的卡片在 hover 时显示半透明的编辑/删除按钮（hover 高亮）
- 前端：工具详情页（DetailPage）、帖子详情页（PostDetailPage）、微课详情页（VideoDetailPage）增加编辑/删除按钮，按权限显示
- 前端：补齐帖子编辑功能——`PostEditorPage` 接通编辑模式（带 id 时回填并调用 `updatePost`），新增路由 `/forum/posts/:id/edit`
- 前端：新增微课编辑页 `VideoEditPage`（仅编辑标题/简介，不替换视频文件），新增路由 `/videos/:id/edit`
- 前端：`PostCard`、`VideoCard` 组件增加 `editable` / `deletable` prop 控制按钮显示

## 能力清单（Capabilities）

### 新增能力（New Capabilities）
- `content-moderation`: 管理员（ADMIN/SUPER_ADMIN）对工具、帖子、微课的删除与编辑审核权限，以及前端按角色显示操作按钮的统一行为

### 修改能力（Modified Capabilities）
- `forum-post`: Scenario 4（作者更新）需扩展——管理员也可更新他人帖子；删除权限同步扩展
- `post-delete`: Scenario 2/3/8/10 需扩展——管理员可见删除按钮且后端放行；新增编辑按钮相关场景
- `tool-modify-delete`: 「修改他人工具返回错误」场景需补充管理员例外（仅 REST API 层面，MCP 工具规格不在本次范围）

## 影响范围（Impact）

- **后端 Service 层**：`ToolService`、`ForumPostService`、`VideoService` 的 `deleteXxx` / `updateXxx` 方法签名及权限逻辑
- **后端 Controller 层**：`ToolController`、`ForumPostController`、`VideoController` 传参从 `currentUser.getId()` 改为 `currentUser`
- **前端 composable**：新增 `useContentPermissions.ts`
- **前端组件**：`PostCard.vue`、`VideoCard.vue`（加操作按钮）、`HomePage.vue`、`DetailPage.vue`、`PostListPage.vue`、`PostDetailPage.vue`、`VideoListPage.vue`、`VideoDetailPage.vue`
- **前端编辑页**：`PostEditorPage.vue`（接通编辑）、新增 `VideoEditPage.vue`
- **前端路由**：`router/index.ts` 新增帖子编辑、微课编辑路由
- **现有规格**：`forum-post`、`post-delete`、`tool-modify-delete` 的 delta 规格
