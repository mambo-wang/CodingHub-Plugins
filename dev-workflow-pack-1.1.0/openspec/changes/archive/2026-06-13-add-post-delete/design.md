# Design: 帖子删除功能

## 1. File Structure

### 1.1 新增文件

| 路径 | 用途 | 关联测试 |
|------|------|----------|
| `frontend/src/components/common/ConfirmDialog.vue` | 通用确认对话框组件（毛玻璃 + ESC 关闭 + 遮罩） | `frontend/tests/unit/components/common/ConfirmDialog.spec.ts` |
| `frontend/tests/unit/components/common/ConfirmDialog.spec.ts` | ConfirmDialog 单元测试 | — |
| `frontend/tests/unit/stores/forum.spec.ts` | forum store 的 `deletePost` action 单测（含 AUTH/FORBIDDEN/NOT_FOUND 分支） | — |

### 1.2 修改文件

| 路径 | 改动摘要 | 关联测试 |
|------|----------|----------|
| `frontend/src/pages/forum/PostDetailPage.vue` | 在 like-section 旁追加"删除"按钮（仅作者），点击弹 `ConfirmDialog`；成功跳转 `/forum` | `frontend/tests/unit/pages/forum/PostDetailPage.spec.ts` |
| `frontend/src/pages/forum/MyPostsPage.vue` | `PostCard` 上叠加"删除"小图标按钮，弹同一 `ConfirmDialog`；成功后从本地列表移除 | `frontend/tests/unit/pages/forum/MyPostsPage.spec.ts` |
| `frontend/src/components/forum/PostCard.vue` | 新增可选 prop `deletable?: boolean` + `@delete` 事件（保持向后兼容） | `frontend/tests/unit/components/forum/PostCard.spec.ts` |
| `frontend/src/stores/forum.ts` | 新增 `deletePost(id)` action；返回 `{ success, errorCode }` | `frontend/tests/unit/stores/forum.spec.ts`（同 1.1） |
| `frontend/src/services/forum.ts` | 已存在 `deletePost(id)`，**无需修改** | — |

### 1.3 后端文件

**无后端改动**。`ForumPostController.deletePost` + `ForumPostService.deletePost` 已在 `add-forum-module` 中实现并通过测试（软删除 + 作者权限校验）。

## 2. Test Strategy

### 2.1 单元测试（Vitest + @vue/test-utils）

#### `ConfirmDialog.spec.ts`

| 用例 | 输入 | 期望 |
|------|------|------|
| 渲染默认状态 | props: `{ visible: true, title: 'T', description: 'D' }` | 标题、描述、确认/取消按钮可见 |
| 点击确认按钮 | 点击"确认" | 触发 `confirm` 事件 |
| 点击取消按钮 | 点击"取消" | 触发 `cancel` 事件 |
| 按 Esc 关闭 | visible=true, keydown 'Escape' | 触发 `cancel` 事件 |
| 点击遮罩关闭 | 触发遮罩 click | 触发 `cancel` 事件 |
| visible=false | — | 不渲染 DOM |
| danger 模式 | props: `{ danger: true }` | "确认"按钮使用 destructive 颜色 |
| aria 属性 | — | `role="dialog"`、`aria-modal="true"`、`aria-labelledby`、`aria-describedby` 正确 |
| 焦点进入 | visible 从 false 变 true | 焦点落在"确认"按钮上 |

#### `stores/forum.spec.ts`

| 用例 | 输入 | 期望 |
|------|------|------|
| 成功删除 | `service.deletePost(1)` resolve + 当前 posts 含 id=1 | 返回 `{ success: true }`，posts 中移除 id=1 |
| 401 未登录 | service reject (status 401) | 返回 `{ success: false, errorCode: 'AUTH' }` |
| 403 非作者 | service reject (status 403) | 返回 `{ success: false, errorCode: 'FORBIDDEN' }` |
| 404 帖子不存在 | service reject (status 404) | 返回 `{ success: false, errorCode: 'NOT_FOUND' }` |
| 网络错误 | service reject (其他) | 返回 `{ success: false, errorCode: 'UNKNOWN' }` |

> **测试约定**：mock `forumService.deletePost` 使用 `vi.mock('@/services/forum')`，axios 错误通过 `new AxiosError(...)` 构造。

#### `PostDetailPage.spec.ts`

| 用例 | 输入 | 期望 |
|------|------|------|
| 作者可见删除按钮 | `currentUser.id === post.authorId` | 模板中存在 `[data-testid="delete-post-btn"]` |
| 非作者不可见 | `currentUser.id !== post.authorId` | 模板中不存在该按钮 |
| 未登录不可见 | `isLoggedIn=false` | 模板中不存在该按钮 |
| 点击删除弹对话框 | 点击按钮 | `ConfirmDialog` visible 变 true |
| 确认删除成功 | 在对话框点击"确认删除"，service 成功 | `router.push('/forum')` 被调用 |
| 确认删除 403 | service 拒绝 403 | 提示"您不是该帖子的作者，无权删除"，不跳转 |
| 确认删除 404 | service 拒绝 404 | 提示"帖子不存在或已被删除"，关闭对话框并跳转 |

#### `MyPostsPage.spec.ts`

| 用例 | 输入 | 期望 |
|------|------|------|
| 列表显示删除按钮 | `forumStore.posts = [post1, post2]` | 每条 `PostCard` 有 `deletable=true` |
| 删除成功后列表移除 | 触发 `PostCard` 的 `delete` 事件且 service 成功 | 列表中 id 对应项被移除 |
| 取消删除 | 触发后 dialog cancel | 列表不变 |

#### `PostCard.spec.ts`

| 用例 | 输入 | 期望 |
|------|------|------|
| `deletable=false` | — | 不渲染"删除"图标 |
| `deletable=true` | — | 渲染"删除"图标按钮，`aria-label="删除此帖"` |
| hover 变红 | hover | class 变化（使用 `getComputedStyle` 检查） |
| 点击删除 | 点击图标 | 触发 `@delete` 事件，payload 为 `post.id` |

### 2.2 集成测试（Playwright，可选 — 由 tasks.md 中 C 段覆盖）

> 集成测试不是必选，因为是纯前端变更，主要价值在 E2E 路径覆盖，列在 tasks.md 的"Browser Test"块中。

### 2.3 后端测试

**无新增**。现有后端 deletePost 行为由 `add-forum-module` 覆盖。

### 2.4 测试运行命令

```bash
# 进入前端目录
cd frontend

# 运行所有单元测试
npm run test:unit

# 单文件运行
npm run test:unit -- ConfirmDialog.spec.ts
npm run test:unit -- stores/forum.spec.ts
npm run test:unit -- PostDetailPage.spec.ts
npm run test:unit -- MyPostsPage.spec.ts
npm run test:unit -- PostCard.spec.ts

# 覆盖率
npm run test:unit -- --coverage
```

> 仓库根目录 `Makefile` 未覆盖前端测试命令，需要在 `frontend/package.json` 中确认 `test:unit` 脚本已存在；如不存在，tasks.md 中加 RED 任务补足。

## 3. Source ↔ Test Mapping

| 源文件 | 测试文件 |
|--------|----------|
| `components/common/ConfirmDialog.vue` | `tests/unit/components/common/ConfirmDialog.spec.ts` |
| `stores/forum.ts`（`deletePost` action） | `tests/unit/stores/forum.spec.ts` |
| `pages/forum/PostDetailPage.vue` | `tests/unit/pages/forum/PostDetailPage.spec.ts` |
| `pages/forum/MyPostsPage.vue` | `tests/unit/pages/forum/MyPostsPage.spec.ts` |
| `components/forum/PostCard.vue`（`deletable` prop） | `tests/unit/components/forum/PostCard.spec.ts` |
| `services/forum.ts`（已存在） | 复用现有测试或仅 mock |

## 4. UI Component Inventory

| 组件 | 复用 / 新增 | 引用 |
|------|------------|------|
| `ConfirmDialog.vue` | **新增** | 本次 design-system.md § 4 |
| `Button`（destructive 变体） | 复用 Master § Buttons | 引用 `design-system/CodingHub/MASTER.md` |
| `Toast` | 复用现有 | 调用 `useToast()` 或事件总线（项目内） |
| `Trash2` 图标 | 复用 Lucide | `import { Trash2 } from '@lucide/vue'` |
| `Loader2` 图标 | 复用 Lucide | 同上 |

## 5. Page Layout

### 5.1 PostDetailPage（修改后结构）

```
┌──────────────────────────────────────────┐
│ [CategoryTag]                            │
│ Post Title                                │
│ [Author] · 2026-06-09                    │
│ ─────────────────────────────────────── │
│ 👁 1.2k 浏览  💬 5 评论  ❤️ 12 点赞    │
│ ─────────────────────────────────────── │
│ [👍 点赞] [🔖 收藏]            ← 现有     │
│ [🗑️ 删除]                       ← 本次新增 │
│                                          │
│ Post Content (Markdown)                  │
│ ─────────────────────────────────────── │
│ Comments                                 │
│ CommentEditor                            │
└──────────────────────────────────────────┘
```

> 删除按钮**仅**当 `isLoggedIn && currentUserId === post.authorId` 时渲染。

### 5.2 MyPostsPage（修改后结构）

```
┌──────────────────────────────────────────┐
│ 我的帖子                                  │
│ ┌──────────────────────────────────────┐ │
│ │ PostCard 1            [🗑️]           │ │ ← deletable=true
│ │ PostCard 2            [🗑️]           │ │
│ │ ...                                  │ │
│ └──────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

> `PostCard` 右上角追加"删除"小图标按钮；点击 `event.stopPropagation()` 防止触发卡片本身的点击进入详情。

### 5.3 ConfirmDialog（结构）

```vue
<Transition name="modal">
  <div v-if="visible" class="modal-overlay" @click.self="$emit('cancel')">
    <div class="modal-content glass-card" role="dialog" aria-modal="true"
         :aria-labelledby="titleId" :aria-describedby="descId">
      <h2 :id="titleId">{{ title }}</h2>
      <p :id="descId">{{ description }}</p>
      <div class="modal-actions">
        <button class="btn-secondary" @click="$emit('cancel')">{{ cancelText }}</button>
        <button :class="['btn-primary', { 'btn-danger': danger }]" :disabled="loading"
                @click="$emit('confirm')">
          <Loader2 v-if="loading" :size="16" class="spin" />
          {{ confirmText }}
        </button>
      </div>
    </div>
  </div>
</Transition>
```

## 6. Accessibility Validation Points

- [ ] 删除按钮键盘可达（Tab 顺序：点赞 → 收藏 → 删除）
- [ ] 删除按钮 `aria-label="删除帖子"`
- [ ] 图标删除按钮 `aria-label="删除此帖"`
- [ ] 打开对话框时 `focus()` 移入"确认"按钮
- [ ] 关闭对话框时 `focus()` 回到触发按钮（详情页是"删除"按钮，列表页是卡片上的"删除"图标）
- [ ] `role="dialog"` + `aria-modal="true"` + `aria-labelledby` + `aria-describedby`
- [ ] 错误提示 `role="alert"`
- [ ] 焦点环可见
- [ ] 颜色对比度 ≥ 4.5:1
- [ ] `prefers-reduced-motion` 关闭淡入/缩放动画

## 7. Risk Level

- **L0 纯新增**（主）：新增 `ConfirmDialog` 组件、新增 `deletePost` action、新增测试文件
- **L1 修改公共 API**（次）：`PostCard.vue` 新增 `deletable` prop + `@delete` 事件（向后兼容，默认 `deletable=false`）

总体风险：**L1**。需在 `PostCard` 现有调用点确认 `deletable` 默认为 `false` 不影响其他列表（如 `PostListPage`）。
