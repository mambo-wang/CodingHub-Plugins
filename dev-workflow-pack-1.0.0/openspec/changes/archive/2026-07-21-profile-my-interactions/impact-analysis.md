# Impact Analysis

> 基于 `design.md` 中的文件/类清单执行影响范围分析。
> **CodeGraph MCP 不可用**，回退为基于源码的手动追踪（grep 调用关系）。
> **结论先行**：本次改动全部为**增量新增**（新方法、新端点、新前端板块），不修改任何现有方法签名或公共 API 行为，调用方不受影响。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | 0 | （无全新文件，前端在 ProfilePage 内联扩展，后端在既有类中加方法） |
| 修改 | 6 | 后端：`UnifiedInteractionController.java`、`UnifiedLikeService.java`、`UnifiedLikeRepository.java`、`UnifiedCommentService.java`、`UnifiedCommentRepository.java`；前端：`services/interaction.ts`、`pages/ProfilePage.vue` |
| 删除 | 0 | — |

> 注：均为在既有类/文件中**追加**方法，不涉及删除或重写。

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `UnifiedInteractionController.getMyFavorites` | `controller/UnifiedInteractionController.java:118` | L0（已有，仅作参照） |
| 前端 `interactionApi.getMyFavorites` | `services/interaction.ts:79` | L0（已有，仅作参照） |
| 新增 `getMyLikes` / `getMyComments` 端点 | 本变更新增 | L0（无既有调用方） |

### 2.2 传递调用方 (Transitive Callers)

- 本次新增端点仅被前端 `ProfilePage.vue`（个人中心）在用户打开对应标签时调用，无其它上游调用链。
- 新增仓储方法 `findByUserIdAndTargetTypeOrderByCreatedAtDesc`（点赞）、`findByUserIdOrderByCreatedAtDesc`（评论）仅被对应新增 Service 方法调用。

### 2.3 反向调用图（被谁调用）

```text
[新增] UnifiedInteractionController.getMyLikes / getMyComments
  └── [调用方] ProfilePage.vue（个人中心，用户交互触发）

[修改] UnifiedLikeService.getMyLikes（新方法）
  └── [被调用] UnifiedLikeRepository.findByUserIdAndTargetTypeOrderByCreatedAtDesc（新增）

[修改] UnifiedCommentService.getMyComments（新方法）
  └── [被调用] UnifiedCommentRepository.findByUserIdOrderByCreatedAtDesc（新增）
  └── [被调用] ToolRepository / ForumPostRepository / VideoRepository（既有，只读查询）
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `ToolRepository` / `ForumPostRepository` / `VideoRepository` | 数据访问层（既有） | L0（只读，无改动） |
| `ToolSummaryDTO` / `ForumPostSummaryDTO` / `VideoListItem` | DTO（既有，复用） | L0 |
| `UserRepository` | 数据访问层（既有） | L0 |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| 前端 `ProfilePage.vue` | 新增三板块渲染、跳转逻辑 |
| 现有模块收藏页 `/forum/my-favorites`、`/videos/my-favorites` | 不受影响（复用既有 `getMyFavorites`） |
| 现有「按目标」互动接口 | 不受影响（本次仅新增「按用户」接口） |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| 现有 `UnifiedInteractionController` / Service 测试（如有） | 单元/集成 | 仍有效 | 无需改动（既有方法未动） |
| 前端 `ProfilePage` 交互 | 组件 | 建议新增 | 覆盖三板块加载/空/跳转 |

> 说明：项目当前测试覆盖度未知；本次新增接口建议补充端点测试与前端组件测试（见 tasks.md）。

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L0** | 纯新增，不影响现有代码 | 无 |
| **L1** | 修改函数签名/公共 API | 本次未改动既有签名，仅新增端点 |
| **L2** | 修改数据库 schema / 业务规则 | 无 schema 变更 |

**本次改动风险等级**: **L0**（增量新增，仅新增只读端点与前端展示）。

---

## 6. 层级依赖校验 (Layer Dependency Check)

> 校验后端是否仍满足 `controller → service → repository → model` 单向依赖。

新增方法链路：`Controller → Service → Repository → Model/DTO`，完全符合单向依赖；未引入反向依赖。

`scripts/lint-arch.sh` 若存在应运行；本次新增方法未打破既有分层。

**结果**: PASS（逻辑校验，无新反向依赖）。

---

## 7. 回归测试建议 (Regression Suggestions)

- [ ] `GET /interactions/likes/mine?targetType=TOOL` —— 返回当前用户点赞的工具 DTO 列表
- [ ] `GET /interactions/comments/mine` —— 返回当前用户评论（含 targetTitle），过滤已删除目标
- [ ] 未登录访问上述端点返回 401
- [ ] 前端三板块：加载 / 空 / 点击跳转 三种状态

---

## 8. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方（均为新增，无既有调用方受影响）
- [x] 已列出上游/下游依赖（既有 Repository/DTO 复用，只读）
- [x] 已评估风险等级（L0）
- [x] 分层依赖校验通过（无反向依赖）
- [x] 已列出回归测试清单
- [x] 非 L2 风险，无需通知模块负责人

---

**生成工具**: 手动代码追踪（CodeGraph MCP 不可用）
**生成时间**: 2026-07-11
**基础**: openspec/changes/profile-my-interactions/proposal.md
