# Impact Analysis

> 基于 `design.md` 中的文件/类清单执行 codegraph 扫描，确认技术设计的实际影响范围。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | 15+ | `backend/.../model/kb/KnowledgeBase.java`, `KbDocument.java`, `KbStatus.java` |
| 新增 | | `backend/.../repository/kb/KnowledgeBaseRepository.java`, `KbDocumentRepository.java` |
| 新增 | | `backend/.../service/kb/KnowledgeBaseService.java` |
| 新增 | | `backend/.../service/RagApiClient.java` |
| 新增 | | `backend/.../controller/kb/KnowledgeBaseController.java` |
| 新增 | | `backend/.../dto/kb/` (多个 DTO 文件) |
| 新增 | | `frontend/src/pages/knowledge/` (3 个页面) |
| 新增 | | `frontend/src/components/knowledge/` (5-6 个组件) |
| 新增 | | `frontend/src/services/knowledge.ts`, `frontend/src/types/knowledge.ts` |
| 修改 | 3 | `backend/.../config/SecurityConfig.java` |
| 修改 | | `frontend/src/router/index.ts` |
| 修改 | | `frontend/src/components/AppHeader.vue` |
| 修改 | | `backend/src/main/resources/application.yml` |

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `SecurityConfig.securityFilterChain` | `config/SecurityConfig.java` | L1 |
| `router.beforeEach` | `router/index.ts` | L1 |
| `AppHeader` nav template | `components/AppHeader.vue` | L0 |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

- `SecurityConfig` 被所有 Controller 的端点间接依赖（通过 filter chain）
- `router` 被所有页面的导航依赖
- `AppHeader` 被 `App.vue` 渲染

### 2.3 反向调用图（被谁调用）

```
[SecurityConfig]
  └── JwtAuthenticationFilter (已有)
      └── 所有 /api/v1/knowledge/** 端点 (新增)

[router/index.ts]
  └── App.vue RouterView (已有)
      └── KnowledgeListPage, KnowledgeDetailPage, KnowledgeEditorPage (新增)

[AppHeader.vue]
  └── App.vue (已有)
      └── 新增"知识库"导航链接 (新增)
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `JwtAuthenticationFilter` | 认证过滤器 | L0（复用，不修改） |
| `User` entity | 认证主体 | L0（复用，不修改） |
| `ApiResponse<T>` | 响应包装 | L0（复用，不修改） |
| `PageResponse<T>` | 分页响应 | L0（复用，不修改） |
| `ConfirmDialog.vue` | 删除确认弹窗 | L0（复用，不修改） |
| `GeneralizedSidebar.vue` | 侧栏导航 | L0（复用，不修改） |
| `SortTab.vue` | 排序切换 | L0（复用，不修改） |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| `SecurityConfig` 权限规则 | 新增知识库端点需加入 permitAll 或认证规则 |
| `router` 路由表 | 新增 4 条知识库路由 |
| `AppHeader` 导航 | 新增"知识库"链接 |
| `application.yml` | 新增 `app.rag.base-url` 配置 |

---

## 4. 受影响的测试 (Affected Tests)

当前项目后端无自动化测试套件（无 `src/test` 目录下的测试文件）。前端无单元测试。

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| N/A | — | — | 项目当前无自动化测试 |

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L0** | 纯新增模块（model/repository/service/controller/frontend） | 无 |
| **L1** | SecurityConfig 新增端点规则 | 人工验证 GET 公开、POST/PUT/DELETE 需认证 |
| **L1** | router 新增路由 | 人工验证导航跳转和权限守卫 |
| **L1** | AppHeader 新增导航链接 | 人工验证视觉和响应式 |

**本次改动风险等级**: **L1**（修改公共 API：SecurityConfig 权限规则、路由表、导航组件）

---

## 6. 层级依赖校验 (Layer Dependency Check)

> 校验后端是否仍满足 `controller → service → repository → model` 单向依赖。

新增的 kb 模块层级：
```
L4: KnowledgeBaseController (controller/kb/)
  ↓ 依赖
L3: KnowledgeBaseService (service/kb/)
  ↓ 依赖
L2: KnowledgeBaseRepository, KbDocumentRepository (repository/kb/)
  ↓ 依赖
L1: KnowledgeBase, KbDocument, KbStatus (model/kb/)
       KbCreateRequest, KbResponse, etc. (dto/kb/)
  ↓ 依赖
L0: SecurityConfig, RagClientConfig (config/)
       JwtAuthenticationFilter, exceptions (已有)
```

`RagApiClient` 位于 service 层（L3），依赖 config 层（L0）的 `app.rag.base-url` 配置。符合层级规则。

**结果**: PASS（新增模块不引入层级违规）

---

## 7. 回归测试建议 (Regression Suggestions)

由于项目无自动化测试，建议手动验证以下回归场景：

- [ ] 现有工具/论坛/微课 CRUD 不受影响（SecurityConfig 修改未破坏已有规则）
- [ ] 现有路由跳转正常（新路由未覆盖已有路径）
- [ ] AppHeader 导航链接在桌面/移动端显示正常
- [ ] 未登录状态下现有公开端点仍可访问

---

## 8. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方
- [x] 已列出上游/下游依赖
- [x] 已评估风险等级（L1）
- [x] 层级依赖校验通过（PASS）
- [x] 已列出回归测试清单（手动验证）

---

**生成时间**: 2026-06-26
**基础**: openspec/changes/add-knowledge-base/proposal.md + design.md
