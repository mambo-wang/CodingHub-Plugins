# Proposal: 帖子删除功能（前端补全）

## Problem

CodingHub 论坛的帖子删除链路目前**后端已实现但前端缺失入口**，导致用户登录后无法删除自己创建的帖子：

1. **后端**：`ForumPostController.deletePost` + `ForumPostService.deletePost` 已在 `add-forum-module` 中实现（软删除 + 作者权限校验，非作者抛 `ForbiddenException("无权删除此帖子")`，找不到抛 `ResourceNotFoundException`）。
2. **前端 Service**：`forumService.deletePost(id)` 已封装 `DELETE /api/forum/posts/{id}`。
3. **前端 UI 缺失**（本次要解决的问题）：
   - `PostDetailPage.vue` 没有任何删除按钮，无论是否作者都看不到
   - `MyPostsPage.vue` 列表项只有"点击进入详情"行为，没有"删除"快捷操作
4. **二次确认缺失**：删除是高破坏性操作，缺失确认对话框会导致误删
5. **错误反馈不友好**：401（未登录）、403（非作者）、404（不存在）三种异常目前都未在 UI 中被清晰提示

## Solution

在不修改后端 API 的前提下，纯前端补全：

| 改动点 | 描述 |
|--------|------|
| 新增 `ConfirmDialog` 通用组件 | 复用现有 `Glass Card` 风格，支持"标题 / 描述 / 确认 / 取消"四要素，支持 Esc 关闭与背景点击关闭，支持 `aria-modal` |
| `PostDetailPage.vue` | 当 `isLoggedIn && currentUserId === post.authorId` 时在 like-section 旁显示"删除"按钮（红色 destructive 配色），点击后弹出 `ConfirmDialog`；确认后调 `forumService.deletePost`，成功 toast 并 `router.push('/forum')`，失败按错误码分别提示 |
| `MyPostsPage.vue` | `PostCard` 渲染时追加"删除"小图标按钮（在卡片右上角），点击同样弹 `ConfirmDialog`；删除成功后从本地列表中移除该条 |
| `stores/forum.ts` | 新增 `deletePost(id)` action：调 service 后从 `posts` 数组移除对应项；返回 `{ success, errorCode }` 供 UI 决策 |
| 错误处理 | 401 → "请先登录"；403 → "您不是该帖子的作者，无权删除"；404 → "帖子不存在或已被删除"；其他 → "删除失败，请稍后重试" |

复用现有后端 `DELETE /api/forum/posts/{id}` 接口，**不需要后端改动**。

## Testable Behaviors

### 帖子详情页
- WHEN 已登录用户 A 访问 `post.authorId === currentUserId` 的帖子详情页 THEN 在"点赞 / 收藏"按钮组下方出现红色"删除"按钮
- WHEN 未登录用户访问帖子详情页 THEN 不显示"删除"按钮
- WHEN 已登录用户 B 访问 `post.authorId !== currentUserId` 的帖子详情页 THEN 不显示"删除"按钮
- WHEN 作者点击"删除"按钮 THEN 弹出确认对话框，标题"删除帖子"，描述"删除后无法恢复，确定要删除吗？"，含"取消"与"确认删除"两按钮
- WHEN 作者在确认对话框点击"取消" THEN 对话框关闭，不调 API，帖子仍在
- WHEN 作者在确认对话框点击"确认删除" THEN 调用 `DELETE /api/forum/posts/{id}`，按钮变为 loading 态，请求成功后跳转到 `/forum` 并 toast "帖子已删除"
- WHEN 作者点击"确认删除"但后端返回 401 THEN 提示"请先登录"，不跳转
- WHEN 作者点击"确认删除"但后端返回 403 THEN 提示"您不是该帖子的作者，无权删除"
- WHEN 作者点击"确认删除"但后端返回 404 THEN 提示"帖子不存在或已被删除"

### 我的帖子页
- WHEN 已登录用户访问 `/forum/my-posts` THEN 列表中每条 `PostCard` 右上角显示"删除"图标按钮（hover 态变红）
- WHEN 用户点击列表中的"删除"按钮 THEN 弹出与详情页一致的确认对话框（标题"删除帖子"）
- WHEN 用户在确认对话框点击"确认删除" THEN 调用 `DELETE /api/forum/posts/{id}`，成功后该条从列表中消失，toast "帖子已删除"
- WHEN 用户在确认对话框点击"取消" THEN 对话框关闭，列表不变

### 通用交互
- WHEN 确认对话框打开 THEN 焦点自动落在"确认删除"按钮上，按 Esc 关闭，按 Tab 在两按钮间循环
- WHEN 删除请求进行中 THEN "确认删除"按钮 disabled 并显示 spinner，"取消"按钮 disabled
- WHEN 删除请求失败（除 401/403/404 外的网络错误） THEN 提示"删除失败，请稍后重试"，对话框保持打开
- WHEN 确认对话框被打开 THEN 背景出现 50% 黑色遮罩，点击遮罩等同于"取消"

### 权限与数据一致性
- WHEN 非作者用户 A 访问 `/api/forum/posts/{id}` 删除接口（即使绕过 UI） THEN 后端返回 403，数据库 `status` 保持 `NORMAL`（已由现有后端逻辑保证）
- WHEN 帖子被删除（`status = DELETED`）THEN `/api/forum/posts/{id}` 仍返回该帖但状态为 DELETED（已由现有 `getPostById` 行为保证，不在本 change 范围）

## Acceptance Criteria

### 通用组件
- [ ] 新增 `frontend/src/components/common/ConfirmDialog.vue`，支持 `v-model:visible`、`title`、`description`、`confirmText`、`cancelText`、`danger` 五个 props
- [ ] `ConfirmDialog` 使用 glass-card 风格、ESC 关闭、点遮罩关闭、role="dialog" + aria-modal="true"
- [ ] `ConfirmDialog` 暴露 `confirm` 与 `cancel` 两个事件

### 帖子详情页
- [ ] `PostDetailPage.vue` 在作者身份下显示"删除"按钮，遵循 `design-system/CodingHub/MASTER.md` 中 `Button` + Destructive 配色
- [ ] 非作者 / 未登录身份不渲染"删除"按钮
- [ ] 删除成功 → 跳转到 `/forum` + toast 提示
- [ ] 错误码 401/403/404 各自有不同中文提示
- [ ] 删除请求进行中按钮显示 loading 三态

### 我的帖子页
- [ ] `MyPostsPage.vue` 中每条 `PostCard` 右上角显示"删除"小图标按钮
- [ ] 删除成功后该条从本地列表中立即消失
- [ ] 非作者/无权限场景不会出现在此页面（页面本身只显示当前用户帖子）

### Store
- [ ] `stores/forum.ts` 新增 `deletePost(id)` action，返回 `{ success: boolean, errorCode?: 'AUTH' | 'FORBIDDEN' | 'NOT_FOUND' | 'UNKNOWN' }`

### 视觉 / 可访问性
- [ ] 删除按钮颜色使用 `--color-destructive` (#EF4444)
- [ ] 确认对话框通过 `prefers-reduced-motion` 媒体查询关闭淡入动画
- [ ] 焦点环可见（`outline: 2px solid var(--color-primary)`）
- [ ] 响应式：375px / 768px / 1024px 下确认对话框不溢出屏幕
