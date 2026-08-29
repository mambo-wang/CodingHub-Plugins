# Impact Analysis: add-user-avatar

> 基于 `design.md` 中的文件/类清单执行静态分析 + codegraph 扫描，确认技术设计的实际影响范围。
>
> **位置**：在 `design` 之后、`tasks` 之前生成。
>
> **触发条件**：本变更涉及**修改现有代码**（`User.java` / `UserController` / `UserService` / `UploadConfig` / `UserDTO` / `AppHeader.vue` / `AuthorBadge.vue` / `types/index.ts` / `stores/auth.ts` / `router/index.ts`），必选。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | 13 | `AvatarStaticController.java`, `UserService` 内部方法, `PublicUserDTO.java`, `AvatarUploadResponse.java`, `AvatarValidationException.java`, `UserNotFoundException.java`, `AvatarUtil.java`, `V20260610__add_user_avatar.sql`, `UserAvatar.vue`, `ProfilePage.vue`, 7 个后端测试文件, 4 个前端测试文件 |
| 修改 | 9 | `User.java`, `UploadConfig.java`, `UserController.java`, `UserService.java`, `UserDTO.java`, `AppHeader.vue`, `AuthorBadge.vue`, `types/index.ts`, `stores/auth.ts`, `router/index.ts` |
| 删除 | 0 | — |

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `UserController.getCurrentUser` | `controller/UserController.java:23-27` | L0 — 已有，需在 DTO 加字段后透传 |
| `UserService.getCurrentUser` | `service/UserService.java:98-109` | L0 — 需在 builder 加 avatarUrl |
| `UserService.register` | `service/UserService.java:24-53` | L0 — 不强制要求头像，零影响 |
| `UserService.login` | `service/UserService.java:55-80` | L0 — 透传 DTO 即可 |
| `AppHeader.vue` 头像 div | `components/AppHeader.vue:69-71` | L0 — 仅替换为 UserAvatar 组件 |
| `AuthorBadge.vue` 调用方 | `pages/DetailPage.vue`, `pages/forum/PostListPage.vue`, `pages/forum/PostDetailPage.vue`, `components/PostRankList.vue` 等 | L1 — 新 prop 可选，默认 undefined 不影响 |
| `auth.ts` `setUser` 调用 | `services/api.ts` 登录/注册响应处理 | L0 — 透传 user 对象 |
| `router/index.ts` 路由注册 | 前端路由初始化 | L0 — 新增一条路由 |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

- `HomePage.vue` → `ToolRankList.vue` → `AuthorBadge.vue` （工具列表作者展示）
- `PostListPage.vue` → `PostCard.vue` → `AuthorBadge.vue` （帖子列表作者）
- `MyToolsPage.vue` → `ToolSummary` 数据（DTO 字段透传）
- `DetailPage.vue` → `ToolDetail.uploaderUsername` （展示作者）

### 2.3 反向调用图（被谁调用）

```
User (entity)
  ├── UserService.getCurrentUser (file:98)
  │     └── UserController.getCurrentUser (file:23)
  │           └── frontend AppHeader / ProfilePage
  ├── UserService.register (file:24)
  │     └── AuthController.register
  ├── UserService.login (file:55)
  │     └── AuthController.login
  └── UserService.refreshToken (file:82)
        └── AuthController.refreshToken

UploadConfig
  ├── ToolFileService (现有上传工具文件)
  ├── ToolFileController (现有)
  └── [NEW] UserService.uploadAvatar (本次)
        └── [NEW] UserController.uploadAvatar

AppHeader.vue
  ├── useAuthStore.user
  └── [MODIFIED] 改用 UserAvatar
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `UserRepository` | 数据访问层 | L0 — 无需修改 |
| `UploadConfig` | 配置 | L0 — 仅新增 3 个属性 |
| `JwtUtil` | 工具 | L0 — 无需修改 |
| `PasswordEncoder` | Spring Security | L0 — 无需修改 |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| `AuthController` 登录/注册响应 | 响应体 `LoginResponse.UserDTO` 需同步加 `avatarUrl`（向后兼容：前端类型扩展为可选） |
| `UserController.getCurrentUser` | `/me` 响应含 `avatarUrl` |
| `LoginResponse.UserDTO` | 登录后前端 `authStore.setUser` 拿到新字段 |
| 前端 `User` 类型 | 所有使用 `user.username` / `user.nickname` 的组件仍能工作（向后兼容） |
| 前端 `ToolSummary` / `ToolDetail` | 列表/详情显示作者；新 prop `avatarUrl` 可选 |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| `UserTest` | 单元 | 需扩展 | 加 `avatarUrl` 字段测试 |
| `UserRepositoryTest` | 单元 | 仍有效 | 无需改动 |
| `AuthServiceTest` | 单元 | 需扩展 | 注册/登录返回包含 `avatarUrl=null` |
| `LoginResponseTest` | 单元 | 需扩展 | 序列化测试 |
| `UserDTOTest` | 单元 | 需扩展 | avatarUrl 字段 |
| `UserControllerAvatarTest`（新） | 集成 | 新增 | 4 个端点 |
| `AvatarStaticControllerTest`（新） | 集成 | 新增 | 静态资源 + 路径穿越 |
| `AvatarUtilTest`（新） | 单元 | 新增 | 校验逻辑 |
| `UserAvatar.test.ts`（新） | 组件 | 新增 | 渲染 / 降级 / 哈希色 |
| `AuthorBadge.test.ts` | 组件 | 需扩展 | avatarUrl prop |
| `AppHeader.test.ts` | 组件 | 需扩展 | UserAvatar 集成 |
| `ProfilePage.test.ts`（新） | 页面 | 新增 | 上传 / 移除 / 错误 |
| `auth.test.ts` | Store | 需扩展 | avatarUrl 持久化 |

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L0** | 纯新增字段（avatarUrl nullable） | 无破坏，老用户无感 |
| **L1** | 修改公共 API 响应体（加 avatarUrl 字段） | 前端类型扩展为可选；字段缺失时降级到首字母兜底 |
| **L1** | 新增静态资源端点 `/api/v1/static/avatars/{userId}` | 路径穿越防护（正则校验 userId 必须为数字）；不带敏感信息 |
| **L2** | 数据库 schema 变更（`ALTER TABLE user ADD COLUMN`） | 迁移脚本 nullable 默认值；上线前在测试环境验证 Flyway 行为 |

**本次改动风险等级**: **L1**（含一处 L2 schema 变更）

---

## 6. 层级依赖校验 (Layer Dependency Check)

> 校验后端是否仍满足 `controller → service → repository → model` 单向依赖。

**手动校验**（无 `scripts/lint-arch.sh` 在本仓库根）：

| 改动 | 依赖方向 | 校验结果 |
|------|---------|---------|
| `UserController` 新增端点 | L4 → L3 (UserService) | ✅ PASS |
| `AvatarStaticController` | L4 → L0 (UploadConfig) | ✅ PASS |
| `UserService` 新增方法 | L3 → L1 (User) + L0 (UploadConfig, AvatarUtil) | ✅ PASS |
| `AvatarUtil` | L0 → 无 | ✅ PASS |
| 新增 DTOs | L1 → 无 | ✅ PASS |
| 新增 Exceptions | exception/ → L0 | ✅ PASS |

**结果**: **PASS** — 无循环依赖，未破坏分层。

---

## 7. 回归测试建议 (Regression Suggestions)

- [ ] 现有用户登录 → 拿到 `avatarUrl=null` → AppHeader 降级首字母
- [ ] 现有作者展示（工具/帖子）→ `AuthorBadge` 无 `avatarUrl` prop → 走文字徽章
- [ ] 上传新头像 → `updated_at` 变化 → URL `?v=新时间戳` 触发新请求
- [ ] 删除头像 → `avatarUrl=null` → UI 切回首字母
- [ ] 路径穿越请求 `/api/v1/static/avatars/..%2F..%2Fetc%2Fpasswd` → 400/404
- [ ] 不存在的 userId 请求头像 → 404
- [ ] 老 user（avatarUrl=null）走 `getCurrentUser` 不抛 NPE
- [ ] 头像 404 时 `<img onerror>` 降级到首字母
- [ ] 大文件（3MB）上传 → 413
- [ ] SVG 上传 → 400
- [ ] 主题切换 → 头像容器边框/阴影跟随
- [ ] 移动端（< 640px） → ProfilePage 上下堆叠

---

## 8. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方
- [x] 已列出上游/下游依赖
- [x] 已评估风险等级
- [x] 层级依赖校验通过
- [x] 已列出回归测试清单
- [ ] （L2 风险）已通知相关模块负责人 — 待 apply 阶段确认
- [ ] 移动端响应式 — 待 UI 任务验证

---

**生成工具**: 静态分析（基于 design.md 文件清单 + codegraph 索引）
**生成时间**: 2026-06-10 20:30
**基础**: openspec/changes/add-user-avatar/design.md
