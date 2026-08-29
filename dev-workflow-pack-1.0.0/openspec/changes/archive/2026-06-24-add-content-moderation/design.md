## 背景（Context）

CodingHub 当前对工具（Tool）、帖子（ForumPost）、微课（Video）三类内容的删除和编辑权限采用统一的「仅创建者」模式：三个 Service（`ToolService`、`ForumPostService`、`VideoService`）的 `deleteXxx` / `updateXxx` 方法只接收 `Long userId`，校验 `ownerId == userId`，否则抛 `ForbiddenException`。

系统已有完整的三级角色体系（`USER` / `ADMIN` / `SUPER_ADMIN`），`User` 实体含 `role` 字段，JWT 中携带角色，前端 `authStore` 已暴露 `isAdmin` / `isSuperAdmin` 计算属性。`SecurityConfig` 已用 `hasAnyRole("ADMIN","SUPER_ADMIN")` 保护 `/api/v1/admin/**` 路径。但内容 CRUD 接口（`/api/v1/tools/**`、`/api/forum/posts/**`、`/api/v1/videos/**`）的权限校验完全在 Service 层手工实现，未利用角色信息。

前端现状：工具编辑页（`EditToolPage`）完整且带创建者守卫；帖子编辑页（`PostEditorPage`）有 `isEdit` 判断但 `publish()` 只调 `createPost`，未接通更新；微课无编辑页。列表页中 `PostCard` 已有 `deletable` prop 但 `PostListPage` 未传值；`VideoCard` 和 `HomePage` 内联卡片无任何操作按钮。详情页中仅 `PostDetailPage` 有创建者删除按钮，`DetailPage`（工具）和 `VideoDetailPage` 无操作按钮。

## 目标 / 非目标（Goals / Non-Goals）

**目标：**
- 管理员（ADMIN/SUPER_ADMIN）能够删除和编辑任何用户的工具、帖子、微课
- 创建者保持对自己内容的删除和编辑能力
- 三类内容的列表页卡片在 hover 时显示半透明的编辑/删除操作按钮（hover 高亮），无权限时不显示
- 三类内容的详情页显示编辑/删除按钮，按权限控制可见性
- 补齐帖子编辑功能（`PostEditorPage` 接通更新模式 + 路由）
- 新增微课编辑页（仅编辑标题/简介，不替换视频文件）
- 后端权限校验统一、可测试

**非目标：**
- 不修改 MCP 工具（`h3_coding_hub_tool_modify` 等）的权限逻辑——本次仅涉及 REST API 层
- 不引入新的角色或权限模型（复用现有 `Role` 枚举）
- 不实现批量删除/编辑
- 不实现操作审计日志（可作为后续独立 change）
- 不修改 `SecurityConfig` 的 URL 级别权限规则——权限校验仍在 Service 层

## 决策（Decisions）

### 决策 1：Service 方法签名从 `Long userId` 改为 `User user`

**选择：** 三个 Service 的 `deleteXxx` / `updateXxx` 方法签名统一改为接收 `User user`（完整实体），而非仅 `Long userId`。

**理由：** Controller 已通过 `@AuthenticationPrincipal User currentUser` 拿到完整 User 对象（含 `role`），当前却只传 `currentUser.getId()`。改为传 `User` 后，Service 内可直接读取 `user.getRole()`，无需额外查询数据库，也无需引入 `SecurityContextHolder` 隐式依赖。

**备选方案：**
- *方案 B：Service 内部通过 `SecurityContextHolder.getContext().getAuthentication()` 获取角色* —— 被否决。会让 Service 隐式耦合 Spring Security 上下文，单元测试需 mock SecurityContext，违反分层清晰性。
- *方案 C：新增 `@AdminOrOwner` 自定义注解 + AOP* —— 被否决。当前仅 6 个方法需要改，引入 AOP 基础设施成本过高，且校验逻辑需访问实体字段（ownerId），注解难以表达。

### 决策 2：权限校验逻辑统一为 `canModify = isOwner || isAdmin`

**选择：** 删除和编辑使用相同的权限判断——创建者或管理员（ADMIN/SUPER_ADMIN）均可操作。

```java
boolean isOwner = entity.getOwnerId().equals(user.getId());
boolean isAdmin = user.getRole() == Role.ADMIN || user.getRole() == Role.SUPER_ADMIN;
if (!isOwner && !isAdmin) {
    throw new ForbiddenException("无权操作此内容");
}
```

**理由：** 用户在探索阶段确认「能删就能改」，权限对称简化了前端按钮显示逻辑（`canEdit === canDelete`），也减少了后端两套校验路径的维护成本。管理员编辑他人内容属于内容治理（修正标题/简介），与删除同属审核动作。

### 决策 3：前端抽取 `useContentPermissions` composable

**选择：** 新增 `frontend/src/composables/useContentPermissions.ts`，统一计算权限：

```typescript
export function useContentPermissions(ownerId: MaybeRef<number | null | undefined>) {
  const authStore = useAuthStore()
  const canEdit = computed(() => {
    const uid = authStore.user?.id
    const oid = unref(ownerId)
    return !!uid && !!oid && (uid === oid || authStore.isAdmin)
  })
  const canDelete = canEdit // 权限对称
  return { canEdit, canDelete }
}
```

**理由：** 权限判断将在 3 实体 × 2 位置（列表+详情）= 6 处复用。三个实体的 ownerId 字段名不同（`uploaderId` / `authorId`），通过参数传入 ownerId 而非整个 item，保持 composable 与实体类型解耦。

**备选方案：**
- *在每个组件内重复写判断* —— 被否决。6 处重复，且 `isAdmin` 逻辑变更时需改 6 处。
- *在 authStore 增加 `canModify(ownerId)` 方法* —— 被否决。store 不应感知具体业务实体的 ownerId 概念，composable 更合适。

### 决策 4：列表页卡片操作按钮采用「半透明 → hover 高亮」

**选择：** 卡片操作按钮默认 `opacity: 0.35`，卡片 hover 时 `opacity: 1`，按钮自身 hover 时变红（删除）/变紫（编辑）。

**理由：** 用户在探索阶段明确选择此方案。相比「完全隐藏 → hover 显示」，半透明方案在移动端（无 hover）也能看到按钮，可访问性更好。按钮使用 `position: absolute` 定位在卡片右上角，不占据布局空间，避免 hover 时布局位移。

### 决策 5：微课编辑页只改元数据，不替换视频文件

**选择：** 新增 `VideoEditPage.vue`，仅包含标题和简介的表单，调用 `PUT /api/v1/videos/{id}`（`VideoUpdateRequest` 已支持 title/description）。不提供视频文件替换。

**理由：** 视频文件替换等同于重新上传（涉及转码、存储清理），成本高且场景少。`VideoService.updateVideo` 已存在且只更新 title/description，前端补齐编辑页即可复用。

### 决策 6：帖子编辑复用现有 `PostEditorPage`，通过路由参数区分模式

**选择：** `/forum/editor`（无 id）为新建模式，`/forum/posts/:id/edit`（带 id）为编辑模式。`PostEditorPage` 内部已用 `isEdit = !!route.params.id` 判断，需补齐 `onMounted` 回填逻辑和 `publish()` 分支调用 `updatePost`。

**理由：** 组件已有 `isEdit` 判断骨架，补齐比新建成本低。复用同一表单 UI 保证新建/编辑体验一致。

## 风险 / 权衡（Risks / Trade-offs）

- **[风险] 管理员误删他人内容** → 删除操作统一走 `ConfirmDialog` 二次确认（帖子已有，工具/微课需新增）；删除为软删除（`status = DELETED`），可恢复。
- **[风险] 前端按钮显示与后端权限不一致** → 前端 `canEdit`/`canDelete` 仅控制按钮可见性，后端 Service 层独立校验，即使前端被绕过（直接调 API）后端仍拦截。前端捕获 403 时提示「无权操作」。
- **[风险] Service 签名变更影响现有调用方** → 三个 Service 的 `deleteXxx`/`updateXxx` 仅被各自 Controller 调用（已确认无其他调用方），签名变更影响面可控。Controller 同步修改传参。
- **[权衡] `canEdit === canDelete` 的对称性** → 若未来需要「管理员能删不能改」，需拆分 composable 返回值和后端校验。当前对称设计是最简方案，符合用户确认的需求。
- **[权衡] 列表页按钮半透明而非隐藏** → 视觉上略增噪音，但换取移动端可用性。可接受。
