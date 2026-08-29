# Impact Analysis

> 基于 `design.md` 中的文件/类清单执行代码影响分析。本变更为**修改现有代码**，故生成此报告。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | 0 | （复用既有 `NotificationService` 内部方法，无新文件） |
| 修改 | 4 | `backend/.../service/UnifiedCommentService.java`、`backend/.../service/UnifiedLikeService.java`、`backend/.../service/UserService.java`、`frontend/src/components/common/NotificationBell.vue` |
| 删除 | 0 | — |

> 注：路径前缀 `backend/src/main/java/com/iaihub/toolbox`、`frontend/src`。

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

被修改方法均为服务内部方法，其调用方为 Controller 层（通过方法调用，不依赖构造参数）：

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `UnifiedInteractionController.addComment` | `controller/UnifiedInteractionController.java` | L0（方法签名不变） |
| `UnifiedInteractionController.toggleLike` | `controller/UnifiedInteractionController.java` | L0（方法签名不变） |
| `AdminController.approveUser` / `rejectUser` | `controller/AdminController.java` | L0（方法签名不变） |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

- `UnifiedInteractionController` ← 由 Spring 路由 `/api/v1/interactions/*` 触发
- `AdminController` ← 由 Spring 路由 `/api/v1/admin/*` 触发
- 上述 Controller 不感知服务内部新增的通知调用，行为契约不变。

### 2.3 反向调用图（被谁调用）

```
[UnifiedCommentService.addComment]  ── 注入 NotificationService
[UnifiedLikeService.toggleLike]     ── 注入 NotificationService
[UserService.approveUser/rejectUser]── 注入 NotificationService
  └── 三者均通过既有 Controller 暴露，签名未变 → 调用方无感
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `NotificationService` | 通知写入 | L0（既存，仅新增调用方） |
| `ToolRepository` / `ForumPostRepository` / `VideoRepository` | 数据访问层（解析所有者） | L0（既存，已注入） |
| `UserRepository` | 数据访问层 | L0（既存，已注入） |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| `NotificationController` / 前端消息中心 | 产生实际通知数据，面板不再恒空 |
| `notification` 表 | 新增数据写入（无 schema 变更） |

---

## 4. 受影响的测试 (Affected Tests)

> ⚠️ 关键风险：三个服务当前使用 `new XService(repo1, repo2, ...)` 显式构造，新增 `NotificationService` 构造参数将**导致编译失败**，必须同步更新。

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| `src/test/java/com/iaihub/toolbox/service/UnifiedCommentServiceTest.java` | 单元 | 需更新 | 新增 `@Mock NotificationService` 字段并加入 `new UnifiedCommentService(...)` 构造参数 |
| `src/test/java/com/iaihub/toolbox/service/UnifiedLikeServiceTest.java` | 单元 | 需更新 | 新增 `@Mock NotificationService` 字段并加入 `new UnifiedLikeService(...)` 构造参数 |
| `src/test/java/com/iaihub/toolbox/service/UserServiceTest.java` | 单元 | 需更新 | 新增 `@Mock NotificationService` 字段并加入 `new UserService(...)` 构造参数 |

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L0** | 纯新增，不影响现有代码 | 无 |
| **L1** | 修改函数签名/公共 API | 全量回归受影响模块单元测试 |
| **L2** | 修改数据库 schema / 业务规则 / 跨模块契约 | 完整测试套件 + 灰度发布 |

**本次改动风险等级**: **L1**（共享服务行为变更 + 三处单元测试需适配构造参数变更，但方法签名与对外 API 契约不变）。

---

## 6. 层级依赖校验 (Layer Dependency Check)

> 校验后端是否仍满足 `controller → service → repository → model` 单向依赖。

新增依赖方向：`service → notification/NotificationService`（同层 service 间调用），`NotificationService` 本身仅依赖 `repository` 与 `model`，不破坏单向依赖链。

**结果**: PASS（预期，需实现后运行 `bash scripts/lint-arch.sh` 复核）

---

## 7. 回归测试建议 (Regression Suggestions)

- [ ] `UnifiedCommentServiceTest` —— 覆盖「评论他人资源触发通知」「评论自己不触发」，位于 `src/test/java/com/iaihub/toolbox/service/UnifiedCommentServiceTest.java`
- [ ] `UnifiedLikeServiceTest` —— 覆盖「点赞他人资源触发通知」「取消点赞不触发」，位于 `src/test/java/com/iaihub/toolbox/service/UnifiedLikeServiceTest.java`
- [ ] `UserServiceTest` —— 覆盖「审批通过/拒绝触发对应管理员通知」，位于 `src/test/java/com/iaihub/toolbox/service/UserServiceTest.java`

---

## 8. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方（Controller 层，签名不变）
- [x] 已列出上游/下游依赖（复用既有仓库与 NotificationService）
- [x] 已评估风险等级（L1）
- [x] 已识别三处单元测试需同步构造参数（编译阻断）
- [x] 已列出回归测试清单
- [ ] （L2 风险）已通知相关模块负责人 —— 非 L2，不适用

---

**生成工具**: 代码检索（grep / 文件读取）+ 人工分析（CodeGraph MCP 不可用时的回退方案）
**生成时间**: 2026-07-12
**基础**: openspec/changes/integrate-message-center-notifications/proposal.md
