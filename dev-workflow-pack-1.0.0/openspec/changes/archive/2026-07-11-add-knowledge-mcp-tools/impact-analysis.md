# Impact Analysis

> 基于 `design.md` 中的文件/类/测试清单执行 codegraph 扫描，确认技术设计的实际影响范围。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 修改 | 2 | `backend/src/main/java/com/iaihub/toolbox/mcp/McpSdkServerConfig.java` |
| 修改 | 1 | `backend/src/main/java/com/iaihub/toolbox/mcp/IaihubToolHandler.java` |
| 新增 | 0 | — |
| 删除 | 0 | — |

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `McpSdkServerConfig.registerAllTools()` | `McpSdkServerConfig.java:131` | L0 — 仅新增 registerTool() 调用，不修改现有注册 |
| `IaihubToolHandler` 构造函数 | `IaihubToolHandler.java:62` | L0 — 新增 KnowledgeBaseService 参数注入 |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

- `McpSdkServerConfig` 被 Spring 容器管理，通过 `@Bean` 注入到 Servlet 容器，无其他 Java 调用方
- `IaihubToolHandler` 被 `McpSdkServerConfig` 的两个 `@Bean` 方法注入，无其他 Java 调用方

### 2.3 反向调用图（被谁调用）

```
McpSdkServerConfig.registerAllTools()
  ├── streamableMcpServer() (Spring @Bean)
  └── sseMcpServer() (Spring @Bean)

IaihubToolHandler
  ├── handleKbList() ← 新增
  ├── handleKbSearch() ← 新增
  ├── handleKbCreate() ← 新增
  ├── handleKbUpdate() ← 新增
  ├── handleKbDelete() ← 新增
  └── handleKbUploadDocument() ← 新增
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `KnowledgeBaseService` | 业务逻辑层 | L0 — 仅新增注入，不修改现有方法 |
| `RagApiClient` | 外部 HTTP 客户端 | L0 — 通过 KnowledgeBaseService 间接调用 |
| `UserService` | 认证服务 | L0 — 已注入，复用现有 login() 方法 |
| `ObjectMapper` | JSON 序列化 | L0 — 已注入 |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| MCP 客户端 | 工具列表从 11 增至 17，客户端可发现新工具 |
| 无前端影响 | 纯后端变更 |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| 无现有 MCP 测试 | 单元 | — | 本次不新增测试文件（MCP handler 测试覆盖可在后续补充） |

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L0** | 纯新增工具注册 + handler 方法，不修改现有工具逻辑 | 无 |

**本次改动风险等级**: L0

---

## 6. 层级依赖校验 (Layer Dependency Check)

> 校验后端是否仍满足 `controller → service → repository → model` 单向依赖。

MCP 层 (`mcp/`) 依赖 `service/` 层，符合 L4 → L3 的依赖规则。`IaihubToolHandler` 注入 `KnowledgeBaseService` 与注入 `ToolService`/`ForumPostService` 模式完全一致。

**结果**: PASS（无需运行 lint-arch.sh，变更模式与现有代码完全一致）

---

## 7. 回归测试建议 (Regression Suggestions)

- [ ] `McpSdkServerConfig` 启动验证 — 确认 17 个工具全部注册成功，无 Bean 创建异常
- [ ] `IaihubToolHandler.handleKbList()` — 验证返回知识库列表 JSON 格式正确
- [ ] `IaihubToolHandler.handleKbSearch()` — 验证搜索返回结果格式正确
- [ ] `IaihubToolHandler.handleKbCreate()` — 验证认证失败时返回错误
- [ ] `IaihubToolHandler.handleKbCreate()` — 验证认证成功时创建成功

---

## 8. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方
- [x] 已列出上游/下游依赖
- [x] 已评估风险等级 (L0)
- [x] 层级依赖校验通过
- [x] 已列出回归测试清单

---

**生成时间**: 2026-06-27
**基础**: openspec/changes/add-knowledge-mcp-tools/proposal.md + design.md
