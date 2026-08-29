# Impact Analysis

> 基于 `design.md` 中的文件/类/测试清单执行 codegraph 扫描，确认技术设计的实际影响范围。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | ~15 | `model/feedback/FeedbackMessage.java`, `model/feedback/FeedbackCategory.java`, `repository/feedback/FeedbackMessageRepository.java`, `service/feedback/FeedbackService.java`, `controller/feedback/FeedbackController.java`, `dto/feedback/FeedbackDTO.java`, `dto/feedback/FeedbackCreateRequest.java`, `dto/feedback/FeedbackReplyRequest.java`, `types/feedback.ts`, `services/feedback.ts`, `pages/feedback/FeedbackPage.vue`, `components/feedback/FeedbackForm.vue`, `components/feedback/FeedbackCard.vue`, `db/migration/V8__create_feedback_table.sql` |
| 修改 | 3 | `config/SecurityConfig.java`, `Makefile`, `frontend/src/router/index.ts` |
| 删除 | 0 | — |

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `SecurityConfig.filterChain` | `config/SecurityConfig.java` | L1 |
| `router/index.ts` (路由注册) | `frontend/src/router/index.ts` | L0 |
| `Makefile` db target | `Makefile` | L0 |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

- `JwtAuthenticationFilter` 通过 `SecurityConfig` 的 filter chain 影响所有端点的认证流程（本次新增 feedback 端点走 permitAll，不影响已有路径）
- Nginx 反向代理通过 `/api/` 前缀匹配自动转发 feedback API 请求（无需 Nginx 配置变更）

### 2.3 反向调用图（被谁调用）

```
[SecurityConfig.filterChain]
  ├── [所有 Controller] (通过 Spring Security filter chain)
  │     └── 新增 FeedbackController (permitAll + authenticated)
  └── [JwtAuthenticationFilter] (前置 filter)
        └── 对 /api/v1/feedback POST 不拦截（无 token 时放行）

[router/index.ts]
  └── [FeedbackPage.vue] (新增路由 /feedback)
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `XssSanitizer` | 工具类 | L0 — 仅调用，不修改 |
| `JwtAuthenticationFilter` | 安全 filter | L0 — 不修改，feedback POST 走 permitAll |
| `UserRepository` | 数据访问层 | L0 — 仅在 reply 时查询管理员信息 |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| Nginx 反向代理 | 无需变更，`/api/` 前缀已覆盖 |
| 前端导航 | 需在侧栏/导航中添加留言板入口链接 |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| （项目当前无自动化测试） | — | — | — |

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L0** | 新增 feedback 模块的所有新文件 | 标准 CRUD 模式，风险极低 |
| **L1** | SecurityConfig 新增 URL 权限规则 | 仅追加规则，不修改已有规则；catch-all `anyRequest().permitAll()` 兜底 |

**本次改动风险等级**: L1（因修改 SecurityConfig）

---

## 6. 层级依赖校验 (Layer Dependency Check)

> 校验后端是否仍满足 `controller → service → repository → model` 单向依赖。

新增文件严格遵循分层：
- `FeedbackController` → `FeedbackService` → `FeedbackMessageRepository` → `FeedbackMessage`
- DTO 层仅依赖 Model 层
- 无循环依赖风险

**结果**: PASS（新增模块，不破坏已有依赖关系）

---

## 7. 回归测试建议 (Regression Suggestions)

- [ ] SecurityConfig 权限回归 — 验证已有端点权限未被修改（工具/论坛/微课 API 仍可正常访问）
- [ ] 匿名 POST 测试 — 不携带 JWT 提交留言，验证不返回 401
- [ ] 管理员回复权限 — 非管理员尝试回复应返回 403
- [ ] 前端路由 — 访问 /feedback 正常加载，不影响其他路由

---

## 8. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方
- [x] 已列出上游/下游依赖
- [x] 已评估风险等级
- [x] 层级依赖校验通过
- [x] 已列出回归测试清单

---

**生成时间**: 2026-06-26
**基础**: openspec/changes/add-feedback-board/proposal.md + design.md
