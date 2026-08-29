# Impact Analysis

> 基于 `design.md` 中的文件/类/测试清单执行 codegraph 扫描，确认技术设计的实际影响范围。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | 8 | `model/Role.java`, `model/AccountStatus.java`, `config/DataInitializer.java`, `controller/AdminController.java`, `dto/AdminUserDTO.java`, `dto/ApprovalRequest.java`, `dto/PendingUserDTO.java`, `scripts/migrations/add-user-role-status.sql` |
| 修改 | 15 | `model/User.java`, `dto/RegisterRequest.java`, `dto/LoginResponse.java`, `dto/UserDTO.java`, `service/UserService.java`, `controller/AuthController.java`, `config/SecurityConfig.java`, `config/JwtAuthenticationFilter.java`, `repository/UserRepository.java`, `frontend/src/types/index.ts`, `frontend/src/stores/auth.ts`, `frontend/src/pages/RegisterPage.vue`, `frontend/src/pages/LoginPage.vue`, `frontend/src/router/index.ts`, `frontend/src/components/AppHeader.vue` |
| 删除 | 0 | — |

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `AuthController.register()` → `UserService.register()` | `controller/AuthController.java:20` | L1 |
| `AuthController.login()` → `UserService.login()` | `controller/AuthController.java:28` | L1 |
| `JwtAuthenticationFilter.doFilterInternal()` → `userRepository.findById()` | `config/JwtAuthenticationFilter.java:50` | L1 |
| `SecurityConfig.securityFilterChain()` → 权限规则 | `config/SecurityConfig.java:30` | L2 |
| `UserService.getCurrentUser()` → `UserDTO.builder()` | `service/UserService.java:115` | L1 |
| `UserService.getPublicProfile()` → `PublicUserDTO.builder()` | `service/UserService.java:193` | L0 |
| `IaihubToolHandler` → `userService.login()` | `mcp/IaihubToolHandler.java:215,247,301,344` | L1 |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

- `AuthController` 通过 `UserService.register()` 间接依赖 `User.role` / `User.status`
- `JwtAuthenticationFilter` 通过 `userRepository.findById()` 间接读取 `User.role` / `User.status` 构建 `GrantedAuthority`
- `SecurityConfig` 的 `hasRole()` 规则依赖 `JwtAuthenticationFilter` 注入的 `GrantedAuthority`
- MCP 端点 `IaihubToolHandler` 通过 `userService.login()` 间接受 status 检查影响

### 2.3 反向调用图（被谁调用）

```
[User.java] (新增 role, status 字段)
  ├── UserRepository.findById() (config/JwtAuthenticationFilter.java:50)
  │     └── JwtAuthenticationFilter → SecurityConfig 权限判断
  ├── UserService.register() (service/UserService.java:48)
  │     └── AuthController.register() (controller/AuthController.java:20)
  ├── UserService.login() (service/UserService.java:72)
  │     ├── AuthController.login() (controller/AuthController.java:28)
  │     └── IaihubToolHandler.login() (mcp/IaihubToolHandler.java:215,247,301,344)
  ├── UserService.getCurrentUser() → UserDTO (service/UserService.java:115)
  └── UserService.getPublicProfile() → PublicUserDTO (service/UserService.java:193)

[JwtAuthenticationFilter.java] (修改 authorities 构建)
  └── SecurityConfig.securityFilterChain() (config/SecurityConfig.java:64)
        └── 所有受保护的 HTTP 请求

[SecurityConfig.java] (新增 hasRole 规则)
  └── 所有 /api/v1/admin/** 请求
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `UserRepository` | 数据访问层 | L1 — 需新增 `findByStatus`, `findByRole` 查询 |
| `PasswordEncoder` (BCrypt) | 配置/工具 | L0 — 不变 |
| `JwtUtil` | 配置/工具 | L0 — 不变（token 不放 role） |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| `AuthController.register()` | 请求体新增 role 字段，响应结构变化 |
| `AuthController.login()` | 响应新增 status 检查，PENDING/REJECTED/DISABLED 拒绝登录 |
| `JwtAuthenticationFilter` | authorities 从空列表变为含 ROLE_* |
| `SecurityConfig` | 新增 /api/v1/admin/** hasRole 规则 |
| `IaihubToolHandler` (MCP) | login() 新增 status 检查，MCP 账号需为 ACTIVE |
| 前端 `api.ts` | 403 处理需区分「未认证」和「无权限」 |
| 前端 `auth.ts` store | user 对象新增 role/status |
| 前端 `AppHeader.vue` | 按角色显示管理入口 |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| `backend/src/test/java/.../service/ToolServiceTest.java` | 单元 | 需更新 | User.builder() 需补 role/status |
| `backend/src/test/java/.../service/ToolFileServiceTest.java` | 单元 | 需更新 | User.builder() 需补 role/status |
| `backend/src/test/java/.../service/video/VideoServiceTest.java` | 单元 | 需更新 | User.builder() 需补 role/status |
| `backend/src/test/java/.../service/video/VideoInteractionServiceTest.java` | 单元 | 需更新 | User.builder() 需补 role/status |
| `backend/src/test/java/.../service/video/VideoStreamTest.java` | 单元 | 需更新 | User.builder() 需补 role/status |

> **说明**：现有测试中使用 `User.builder()` 创建测试数据时，新增的 `role`/`status` 字段如果设了默认值（`@Builder.Default`）则测试可能不需改动；但建议显式设置以确保清晰。

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L1** | 修改 `JwtAuthenticationFilter` authorities 构建 | 全量回归测试受保护端点 |
| **L1** | 修改 `UserService.register()` / `login()` 签名行为 | 覆盖注册和登录的全场景测试 |
| **L2** | 修改数据库 schema（user 表新增列） | migration SQL 使用 DEFAULT 值，确保老数据兼容 |
| **L1** | 前端 `api.ts` 403 处理逻辑需更新 | 区分 401（未认证）和 403（无权限） |
| **L1** | MCP `IaihubToolHandler` 间接受 status 检查影响 | 确保 MCP 使用账号为 ACTIVE 状态 |

**本次改动风险等级**: L2（涉及数据库 schema 变更 + 认证核心逻辑变更）

---

## 6. 层级依赖校验 (Layer Dependency Check)

```bash
bash scripts/lint-arch.sh
```

**结果**: PASS（本次变更不引入新的跨层依赖，`AdminController` → `UserService` → `UserRepository` → `User` 符合 controller → service → repository → model 单向依赖）

---

## 7. 设计修正建议

基于代码扫描发现以下 design.md 未覆盖的影响点：

### 7.1 前端 `api.ts` 403 处理（必须修正）

`frontend/src/services/api.ts` 第 77-81 行当前将 403 统一视为"登录过期"并跳转登录页。新增 hasRole 鉴权后，普通用户访问 admin 端点会返回 403，会被误导向登录页。

**建议**：在 `api.ts` 中区分 401（未认证 → 跳转登录）和 403（无权限 → 显示提示不跳转）。

### 7.2 MCP `IaihubToolHandler` 适配（需确认）

`IaihubToolHandler` 通过 `userService.login()` 认证 MCP 客户端。login() 新增 status 检查后，如果 MCP 账号非 ACTIVE 状态将无法使用。

**建议**：确保 MCP 使用的账号始终为 ACTIVE 状态（超管账号默认 ACTIVE，无此问题）。无需额外代码改动。

### 7.3 `PublicUserDTO` 是否需要 role（可选）

`UserService.getPublicProfile()` 返回 `PublicUserDTO`，当前不含 role。如需在公开资料中展示管理员标识，需同步修改。

**建议**：本次不修改 `PublicUserDTO`，保持公开资料最小信息。如未来需要可在用户列表页单独展示。

### 7.4 前端 `AppHeader.vue`（修正文件名）

design.md 中写的是 `NavBar.vue`，实际项目中的导航栏组件为 `frontend/src/components/AppHeader.vue`。

---

## 8. 回归测试建议 (Regression Suggestions)

- [ ] `UserServiceTest` — 覆盖 USER 注册直接 ACTIVE、ADMIN 注册 PENDING、PENDING 登录拒绝、REJECTED 登录拒绝、DISABLED 登录拒绝
- [ ] `AdminControllerTest` — 覆盖待审批列表查询、通过审批、拒绝审批、用户列表分页、封禁/解禁/删除、权限校验（403）
- [ ] `JwtAuthenticationFilterTest` — 覆盖 ACTIVE 用户设置 authorities、PENDING 用户不设置 authentication
- [ ] `DataInitializerTest` — 覆盖首次启动创建超管、二次启动跳过
- [ ] `SecurityConfigTest` — 覆盖 /api/v1/admin/** 端点的角色鉴权
- [ ] 现有 `ToolServiceTest` / `VideoServiceTest` 等 — 更新 User.builder() 补充 role/status 字段

---

## 9. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方
- [x] 已列出上游/下游依赖
- [x] 已评估风险等级（L2）
- [x] `scripts/lint-arch.sh` 校验通过
- [x] 已列出回归测试清单
- [x] 已列出设计修正建议（api.ts 403 处理、AppHeader.vue 文件名修正）

---

**生成工具**: Task(code-explorer) 子代理 + scripts/lint-arch.sh 静态分析
**生成时间**: 2026-06-19 18:20
**基础**: openspec/changes/add-user-role-approval/proposal.md + design.md
