# Impact Analysis: 帖子删除功能

## 1. 改动范围 (Change Surface)

| 类别 | 文件 | 类型 | 备注 |
|------|------|------|------|
| 新增 | `frontend/src/components/common/ConfirmDialog.vue` | 新增组件 | 通用确认对话框，零外部依赖 |
| 新增 | `frontend/tests/unit/components/common/ConfirmDialog.spec.ts` | 新增测试 | 覆盖 9 个用例 |
| 新增 | `frontend/tests/unit/stores/forum.spec.ts` | 新增测试 | 覆盖 `deletePost` action 5 个错误分支 |
| 新增 | `frontend/tests/unit/pages/forum/PostDetailPage.spec.ts` | 新增测试 | 覆盖 7 个用例 |
| 新增 | `frontend/tests/unit/pages/forum/MyPostsPage.spec.ts` | 新增测试 | 覆盖 3 个用例 |
| 新增 | `frontend/tests/unit/components/forum/PostCard.spec.ts` | 新增测试 | 覆盖 4 个用例 |
| 修改 | `frontend/src/pages/forum/PostDetailPage.vue` | 修改现有 | 新增删除按钮 + ConfirmDialog 引入 |
| 修改 | `frontend/src/pages/forum/MyPostsPage.vue` | 修改现有 | 给 PostCard 传 `deletable=true` |
| 修改 | `frontend/src/components/forum/PostCard.vue` | 修改现有（向后兼容） | 新增 `deletable?: boolean` prop + `@delete` 事件 |
| 修改 | `frontend/src/stores/forum.ts` | 修改现有 | 新增 `deletePost(id)` action |

> **后端无改动**：`ForumPostController.deletePost` + `ForumPostService.deletePost` 已存在并实现软删除 + 作者权限校验。

## 2. 调用图 (Call Graph)

### 2.1 直接调用方

#### `stores/forum.ts` 的 `deletePost` action

- 被 `pages/forum/PostDetailPage.vue::handleConfirmDelete` 调用
- 被 `pages/forum/MyPostsPage.vue::handlePostDelete` 调用

#### `components/forum/PostCard.vue` 的 `@delete` 事件

- 被 `pages/forum/MyPostsPage.vue` 监听（`@delete="handlePostDelete"`）
- **不被**以下页面监听，但因 `deletable` 默认 `false` 不渲染删除按钮，因此无副作用：
  - `pages/forum/PostListPage.vue`
  - `pages/forum/MyFavoritesPage.vue`（**潜在增强点**：未来可考虑 `deletable=true`，本 change 不做）
  - `pages/forum/PostEditorPage.vue`

#### `components/common/ConfirmDialog.vue` 的 `confirm` / `cancel` 事件

- 被 `pages/forum/PostDetailPage.vue` 监听
- 被 `pages/forum/MyPostsPage.vue` 监听

### 2.2 传递调用方

```
PostDetailPage.handleConfirmDelete
  └─ forumStore.deletePost(id)
        └─ forumService.deletePost(id)
              └─ axios DELETE /api/forum/posts/{id}
                    └─ ForumPostController.deletePost() (后端，跨语言边界)
                          └─ ForumPostService.deletePost() (后端，跨语言边界)
                                └─ forumPostRepository.save(post.setStatus(DELETED))
```

```
MyPostsPage.handlePostDelete
  └─ forumStore.deletePost(id)  (同上)
```

### 2.3 反向调用图（树状）

```
forumService.deletePost
└─ forumStore.deletePost
   ├─ PostDetailPage.handleConfirmDelete
   └─ MyPostsPage.handlePostDelete
```

## 3. 依赖链 (Dependency Chain)

### 3.1 上游（本 change 依赖）

| 依赖 | 现状 | 风险 |
|------|------|------|
| `forumService.deletePost` | 已存在 | 无 |
| `ForumPostController.deletePost` | 已存在 | 无 |
| `ForumPostService.deletePost` | 已存在，含作者校验 + 软删除 | 无 |
| `@lucide/vue-next` 图标 | 已在项目内（`Trash2` 可直接 import） | 无 |
| `useToast` 或全局 toast 事件 | 项目内已有使用先例（如 `PostDetailPage` 中错误处理） | 需在 implementation 时确认具体 API |
| Vitest + @vue/test-utils | 项目内已有 | 无 |

### 3.2 下游（本 change 影响的）

| 影响对象 | 风险 |
|----------|------|
| `PostListPage.vue`（用 PostCard） | 低 — `deletable` 默认 `false`，视觉无变化 |
| `MyFavoritesPage.vue`（用 PostCard） | 低 — 同上 |
| `PostEditorPage.vue`（用 PostCard） | 低 — 同上 |
| `PostDetailPage.vue` 既有功能 | 中 — 需保证作者判定逻辑不影响点赞/收藏路径 |
| `MyPostsPage.vue` 既有功能 | 中 — 列表移除逻辑需与刷新逻辑兼容 |
| 任何已 mock `forumService` 的测试 | 低 — `deletePost` 是新方法不影响其他 mock |

## 4. 受影响的测试 (Affected Tests)

> 现有测试是否需要同步更新？

| 文件 | 是否需要更新 | 原因 |
|------|-------------|------|
| `frontend/tests/unit/components/forum/PostCard.spec.ts` | **新增** | 现有仓库若无此文件则新增 |
| `frontend/tests/unit/stores/forum.spec.ts` | **新增** | 现有仓库若无此文件则新增 |
| `frontend/tests/unit/pages/forum/PostDetailPage.spec.ts` | **新增** | 现有仓库若无此文件则新增 |
| `frontend/tests/unit/pages/forum/MyPostsPage.spec.ts` | **新增** | 现有仓库若无此文件则新增 |
| `frontend/tests/unit/components/common/ConfirmDialog.spec.ts` | **新增** | 新组件，强制新增 |
| `frontend/tests/integration/**` | 不需要 | 纯前端组件级变更 |
| 后端 `**/ForumPostServiceTest.java` | **不需要** | 后端无改动 |

## 5. 风险评估 (Risk Assessment)

### 5.1 风险等级：**L1**

| 维度 | 评级 | 说明 |
|------|------|------|
| API 稳定性 | L0 | 复用现有 `deletePost` API，无破坏性变更 |
| 数据迁移 | L0 | 无 DB 迁移 |
| UI 兼容性 | L1 | `PostCard` 新增可选 prop 需保持向后兼容（默认 `deletable=false`） |
| 测试覆盖 | L0 | 全部为新增测试文件 |
| 后端 | L0 | 零改动 |
| 错误处理 | L1 | 401/403/404 三种错误码需分别处理（需在实现时检查 axios 错误结构） |

### 5.2 关键风险点

1. **PostCard 兼容性**：`PostCard.vue` 被 5 个页面使用，引入 `deletable` prop 时必须默认 `false`，**不能**在所有页面统一开启
2. **axios 错误识别**：store 中需正确识别 `error.response.status`，避免误把 5xx 归为 `UNKNOWN`
3. **焦点管理**：确认对话框打开/关闭时焦点进出，需在实现时使用 `nextTick` + template ref
4. **MyPostsPage 列表状态**：store 中 `deletePost` 成功时需同时从 `posts` 数组移除对应项，否则列表不刷新
5. **防止重复删除**：用户在确认对话框"确认删除"后，按钮必须立刻 disabled 防止双击

## 6. 层级依赖校验 (Layer Dependency Check)

### 6.1 后端（无变化，跳过 lint）

> 后端无文件变更，不需要 `scripts/lint-arch.sh` 校验。

### 6.2 前端依赖图

```
pages/ → components/ → services/ → types/
   ↓           ↓
  stores/ ←────┘
```

- `PostDetailPage.vue` (L4) → `ConfirmDialog` (L3) ✅
- `PostDetailPage.vue` (L4) → `PostContent`, `CommentList`, `CommentEditor` (L3) ✅
- `MyPostsPage.vue` (L4) → `PostCard.vue` (L3) ✅
- `PostCard.vue` (L3) → `services/api.ts` (L1) ✅
- `stores/forum.ts` (L2) → `services/forum.ts` (L1) ✅

**结论**：本次变更**未破坏**前端分层依赖。

## 7. 回归测试建议 (Regression Suggestions)

### 7.1 必跑回归

```bash
cd frontend
npm run test:unit            # 所有 unit 测试
npm run build                # 类型检查 + 构建
```

### 7.2 推荐补跑

| 场景 | 用例 | 期望 |
|------|------|------|
| 浏览帖子详情（未登录） | `PostListPage` → 详情 | 不显示删除按钮 |
| 浏览帖子详情（非作者） | 登录 B 看 A 的帖 | 不显示删除按钮 |
| 作者删除自己帖子 | 登录 A 删除自己的帖 | 跳回列表，toast 成功 |
| 我的帖子页删除 | 登录 A 在 `/forum/my-posts` | 列表项消失，toast 成功 |
| 焦点管理 | 打开对话框 | 焦点在"确认删除"按钮 |
| Esc 关闭 | 打开对话框按 Esc | 关闭，不调 API |
| 遮罩点击关闭 | 打开对话框点遮罩 | 关闭，不调 API |
| 列表中其他卡片不受影响 | `PostListPage` 中卡片 | 无删除按钮显示 |

## 8. 检查清单 (Checklist)

- [x] 后端 API 复用：复用现有 `DELETE /api/forum/posts/{id}`
- [x] 前端 service 复用：复用现有 `forumService.deletePost`
- [x] 现有源码兼容：`PostCard.deletable` 默认 `false`，5 个调用点均无需修改
- [x] 测试文件全部新增
- [x] 分层依赖未破坏
- [x] 无 DB 迁移
- [x] 无新 npm 依赖（复用 `@lucide/vue-next`）
- [x] 错误码处理覆盖 401/403/404
- [x] 焦点管理有实现路径
- [x] 响应式 375/768/1024 三档已规划
- [x] 配色仅使用 `--color-destructive` + `--color-primary` 焦点环
- [x] 无 emoji，使用 Lucide `Trash2` / `Loader2`
- [x] `prefers-reduced-motion` 已考虑

## 9. 设计修正建议

无。`design.md` 已完整覆盖改动面、测试策略、源码↔测试对应。
