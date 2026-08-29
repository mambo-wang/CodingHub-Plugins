# Tasks: 帖子删除功能

## Impact Analysis Status

- [x] **已生成** `impact-analysis.md`
- 原因：本次 change 修改现有源码 `PostDetailPage.vue` / `MyPostsPage.vue` / `PostCard.vue` / `stores/forum.ts`，非纯新增
- 调用图：详情页与列表页都通过 `forumStore.deletePost` → `forumService.deletePost` → 后端 `DELETE /api/forum/posts/{id}`，复用现有链路
- 风险等级：**L1**（修改公共 API 兼容性）

---

## A. Atomic TDD Task List

### Feature: forum store 新增 deletePost action

- [x] RED: 编写失败测试——`stores/forum.spec.ts` 测试 `deletePost(1)` 在 service resolve 时返回 `{ success: true }` 并从 `posts` 数组移除 id=1
- [x] GREEN: 最小实现——在 `stores/forum.ts` 添加 `deletePost(id)` action：调 `forumService.deletePost(id)`，成功后 `this.posts = this.posts.filter(p => p.id !== id)`，返回 `{ success: true }`
- [x] RED: 编写失败测试——`deletePost(1)` 在 service reject (status 401) 时返回 `{ success: false, errorCode: 'AUTH' }`
- [x] GREEN: 最小实现——用 try/catch 捕获错误，按 `error.response.status` 区分错误码
- [x] RED: 编写失败测试——`deletePost(1)` 在 status 403 时返回 `{ success: false, errorCode: 'FORBIDDEN' }`
- [x] GREEN: 最小实现——扩展错误码映射表
- [x] RED: 编写失败测试——`deletePost(1)` 在 status 404 时返回 `{ success: false, errorCode: 'NOT_FOUND' }`
- [x] GREEN: 最小实现——扩展错误码映射表
- [x] RED: 编写失败测试——`deletePost(1)` 在网络错误（无 response）时返回 `{ success: false, errorCode: 'UNKNOWN' }`
- [x] GREEN: 最小实现——处理 `error.response` 为空的情况
- [x] REFACTOR: 重构——将错误码映射提取为内部函数 `_mapErrorToCode(error)`，单测覆盖

---

### Feature: ConfirmDialog 通用组件

- [x] RED: 编写失败测试——`ConfirmDialog.spec.ts` 测试 `props.visible=true` 时渲染标题、描述、确认/取消按钮
- [x] GREEN: 最小实现——创建 `components/common/ConfirmDialog.vue` 骨架，props: `visible, title, description, confirmText='确认', cancelText='取消', danger=false`；emit `confirm` / `cancel`
- [x] RED: 编写失败测试——点击"确认"按钮触发 `confirm` 事件
- [x] GREEN: 最小实现——绑定 `@click="$emit('confirm')"`
- [x] RED: 编写失败测试——点击"取消"按钮触发 `cancel` 事件
- [x] GREEN: 最小实现——绑定 `@click="$emit('cancel')"`
- [x] RED: 编写失败测试——`visible=false` 时不渲染 DOM
- [x] GREEN: 最小实现——`<div v-if="visible">` 包装
- [x] RED: 编写失败测试——按 Esc 触发 `cancel` 事件
- [x] GREEN: 最小实现——`onMounted` 注册 `keydown` 全局监听，`Escape` 触发 `cancel`
- [x] RED: 编写失败测试——点击遮罩触发 `cancel` 事件
- [x] GREEN: 最小实现——遮罩 `@click.self="$emit('cancel')"`
- [x] RED: 编写失败测试——`danger=true` 时"确认"按钮带 destructive class
- [x] GREEN: 最小实现——`[class.btn-danger]="danger"`
- [x] RED: 编写失败测试——`role="dialog"`、`aria-modal="true"`、`aria-labelledby`、`aria-describedby` 属性正确
- [x] GREEN: 最小实现——添加 a11y 属性
- [x] RED: 编写失败测试——`visible` 从 false 变 true 时"确认"按钮获得焦点
- [x] GREEN: 最小实现——`watch(visible, val => val && nextTick(() => confirmBtnRef.value?.focus()))`
- [x] REFACTOR: 重构——样式抽到 `<style scoped>`，与设计系统 tokens 一致（`--color-destructive`、`--color-border` 等）

---

### Feature: PostCard 新增 deletable prop + @delete 事件

- [x] RED: 编写失败测试——`PostCard.spec.ts` 测试 `deletable=false`（默认）时不渲染删除图标按钮
- [x] GREEN: 最小实现——`props: { post: ForumPost, deletable?: boolean }`，默认 `false`
- [x] RED: 编写失败测试——`deletable=true` 时渲染删除图标按钮，含 `aria-label="删除此帖"`
- [x] GREEN: 最小实现——`<button v-if="deletable" class="btn-icon-delete" aria-label="删除此帖">` 内含 Trash2 SVG
- [x] RED: 编写失败测试——点击删除按钮触发 `@delete` 事件，payload 为 `post.id`
- [x] GREEN: 最小实现——`@click.stop="$emit('delete', post.id)"`
- [x] REFACTOR: 重构——确保 `PostListPage.vue` / `MyFavoritesPage.vue` / `PostEditorPage.vue` 三处现有调用点不受影响（不传 `deletable` 默认为 `false`）

---

### Feature: PostDetailPage 接入删除流程

- [x] RED: 编写失败测试——`PostDetailPage.spec.ts` 测试作者身份（`currentUser.id === post.authorId`）时模板存在 `[data-testid="delete-post-btn"]`
- [x] GREEN: 最小实现——在 like-section 旁追加 `<button v-if="isLoggedIn && currentUserId === post.authorId" data-testid="delete-post-btn" class="btn-delete">`
- [x] RED: 编写失败测试——非作者 / 未登录身份不渲染该按钮
- [x] GREEN: 最小实现——v-if 条件已覆盖，确认测试通过
- [x] RED: 编写失败测试——点击"删除"按钮，`ConfirmDialog` 的 visible 变 true
- [x] GREEN: 最小实现——`@click="dialogVisible = true"`，模板中挂载 `<ConfirmDialog v-model:visible="dialogVisible" ...>`
- [x] RED: 编写失败测试——在对话框点击"确认删除"且 service 成功时，`router.push('/forum')` 被调用
- [x] GREEN: 最小实现——`@confirm="handleConfirmDelete"`，方法内调 `forumStore.deletePost(post.id)`，成功 `router.push('/forum')` + toast
- [x] RED: 编写失败测试——service 返回 403 时不跳转，提示"您不是该帖子的作者，无权删除"
- [x] GREEN: 最小实现——按 `errorCode` 分支显示不同 toast，403 保持对话框打开
- [x] RED: 编写失败测试——service 返回 404 时关闭对话框 + 跳转 `/forum` + toast"帖子不存在或已被删除"
- [x] GREEN: 最小实现——404 特殊路径处理
- [x] REFACTOR: 重构——抽 `handleConfirmDelete` 为 async，错误码→toast 文案映射表

---

### Feature: MyPostsPage 接入删除流程

- [x] RED: 编写失败测试——`MyPostsPage.spec.ts` 测试 `PostCard` 接收 `deletable=true`
- [x] GREEN: 最小实现——`<PostCard :deletable="true" :post="post" @delete="handlePostDelete" />`
- [x] RED: 编写失败测试——点击 PostCard 上的删除图标弹 `ConfirmDialog`
- [x] GREEN: 最小实现——`@delete="(id) => { deleteId = id; dialogVisible = true }"`
- [x] RED: 编写失败测试——在对话框点击"确认删除"且 service 成功后，列表中对应项被移除
- [x] GREEN: 最小实现——`@confirm="handleConfirmDelete"` 内调 `forumStore.deletePost`，store 已过滤数组
- [x] REFACTOR: 重构——与 `PostDetailPage` 共用 `ConfirmDialog` 复用，状态独立

---

## B. UI Implementation Tasks

> 引用 `design-system.md` §4 交互状态、§5 响应式、§6 可访问性规范；参考 `ui-preview.html` 作为视觉验收标准。

### UI: ConfirmDialog 视觉对齐设计系统

- [x] 实现 ConfirmDialog 视觉——毛玻璃背景、destructive 确认按钮样式、遮罩淡入；参考 `ui-preview.html` §3
- [x] 验证 ConfirmDialog——检查 normal / loading 两态、Esc 关闭、遮罩关闭、focus-visible 焦点环、role/aria 属性

### UI: 帖子详情页删除按钮

- [x] 实现 PostDetailPage 删除按钮——在 like-section 旁追加，仅作者可见；参考 `ui-preview.html` §1
- [x] 验证 PostDetailPage 删除按钮——normal/hover/focus/loading 四态、focus-visible 环、与点赞收藏按钮间距 12px

### UI: 我的帖子页列表项删除图标

- [x] 实现 MyPostsPage 列表项删除图标——PostCard 右上角，stopPropagation；参考 `ui-preview.html` §2
- [x] 验证 MyPostsPage 列表项删除图标——normal/hover/focus 三态、hover 变红、点击不触发卡片跳转

### UI: 响应式与可访问性

- [x] 实现 响应式布局——375px / 768px / 1024px 三档断点，参考 `ui-preview.html` §5
- [x] 验证 响应式——浏览器 DevTools 切换断点，按钮垂直堆叠 / 水平排列正确，对话框不溢出
- [x] 实现 焦点管理——打开对话框时焦点入"确认"按钮，关闭时回触发按钮
- [x] 验证 焦点管理——Tab 循环、Esc 关闭、Enter 触发全部正常
- [x] 实现 错误 toast——按 401/403/404/其他 区分提示，role="alert"
- [x] 验证 错误 toast——分别测试各错误码反馈

---

## C. Browser Test

> 使用 Playwright（项目内 `playwright-cli` skill）进行端到端验证。

### E2E: 作者删除帖子（详情页路径）

- [x] 场景1: 作者访问自己帖子详情 → 看到删除按钮 → 点击 → 弹确认对话框 → 确认 → 跳转到 `/forum` + toast 成功
- [x] 场景2: 作者在对话框按 Esc → 对话框关闭，帖子仍在
- [x] 场景3: 作者在对话框点遮罩 → 对话框关闭，帖子仍在

### E2E: 非作者不可见删除按钮

- [x] 场景4: 用户 B 登录后访问用户 A 的帖子详情 → 不显示删除按钮
- [x] 场景5: 游客访问任意帖子详情 → 不显示删除按钮

### E2E: 我的帖子页删除

- [x] 场景6: 用户在 `/forum/my-posts` 看到列表项右上角删除图标 → 点击 → 弹对话框 → 确认 → 该条消失 + toast
- [x] 场景7: 列表项删除图标点击不触发卡片跳转（stopPropagation）

### E2E: 错误码处理

- [x] 场景8: 模拟 service reject 401 → toast"请先登录"
- [x] 场景9: 模拟 service reject 403 → toast"您不是该帖子的作者，无权删除"
- [x] 场景10: 模拟 service reject 404 → 关闭对话框 + 跳转 + toast"帖子不存在或已被删除"
- [x] 场景11: 模拟 service reject 5xx → toast"删除失败，请稍后重试"，对话框保持打开

### E2E: 加载态

- [x] 场景12: 删除请求进行中 → 确认按钮 disabled + spinner，取消按钮 disabled

### E2E: 可访问性

- [x] 场景13: 键盘 Tab 循环在"取消"和"确认删除"之间
- [x] 场景14: 焦点环可见
- [x] 场景15: `prefers-reduced-motion: reduce` 下无淡入/缩放动画
