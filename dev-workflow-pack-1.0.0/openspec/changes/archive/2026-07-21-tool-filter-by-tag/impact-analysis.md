# Impact Analysis

> 基于 `design.md` 中的文件/类清单执行调用图扫描，确认技术设计的实际影响范围。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | 0 | — |
| 修改 | 11 | `ToolController.java`, `ToolService.java`, `ToolRepository.java`, `HomePage.vue`, `TagBadge.vue`, `McpSdkServerConfig.java`, `IaihubToolHandler.java`, `McpSearchService.java`, `McpResourceHandler.java`, `SKILL.md` + `references/tool-reference.md` + `scripts/chub.cjs` + `scripts/chub.py`（Skill） |
| 删除 | 0 | — |

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `ToolController.getTools` | `controller/ToolController.java:33` | L1 |
| `IaihubToolHandler.handleToolSearch` | `mcp/IaihubToolHandler.java:116` | L1 |
| `McpResourceHandler.readAllTools / readRecentTools` | `mcp/McpResourceHandler.java:54,69` | L1 |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

- 前端 `HomePage.vue` 通过 HTTP `GET /api/v1/tools` 调用 `ToolController.getTools`
- MCP 客户端通过 `h3_coding_hub_tool_search` 工具（`McpSdkServerConfig.java:196-202` 注册）调用 `IaihubToolHandler.handleToolSearch` → `McpSearchService.searchTools`
- MCP Resources（`tools://all`、`tools://recent`）通过 `McpResourceHandler` 调用 `McpSearchService.searchTools(null, null, N)`

### 2.3 反向调用图（被谁调用）

```
ToolRepository.findByFilters / findByFiltersOrderByName / findByFiltersOrderByHot
  └── ToolService.getTools (service/ToolService.java:42)
        └── ToolController.getTools (controller/ToolController.java:33)
              └── [HTTP] GET /api/v1/tools → 前端 HomePage.vue

ToolRepository.findApprovedToolsWithCategory
  └── McpSearchService.searchTools (service/McpSearchService.java:61)
        ├── IaihubToolHandler.handleToolSearch (mcp/IaihubToolHandler.java:116)
        │     └── McpSdkServerConfig h3_coding_hub_tool_search (mcp/McpSdkServerConfig.java:201)
        └── McpResourceHandler.readAllTools / readRecentTools (mcp/McpResourceHandler.java:54,69)
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `ToolRepository` (JPQL 查询) | 数据访问层 | L1 — 需新增/修改查询方法 |
| `ToolTagRepository` | 数据访问层 | L0 — 仅新增 `findToolIdsByTagId` 方法 |
| `TagRepository` | 数据访问层 | L0 — 不修改 |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| `HomePage.vue` | 新增 tagId 参数传递 |
| `TagBadge.vue` | 新增可选 clickable prop + emit |
| `tool.ts` (前端 service) | 请求参数扩展 |
| `McpSdkServerConfig` | tool_search schema 新增 tag 参数 + 参数提取 |
| `IaihubToolHandler` | handleToolSearch 签名新增 tag 参数 |
| `McpResourceHandler` | searchTools 调用处适配新签名（传 null） |
| CodingHub Skill（SKILL.md / tool-reference.md / chub 脚本） | 文档 + CLI 新增 --tag 选项 |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| 当前无 ToolService/ToolController 单元测试 | — | — | 建议新增 |

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L1** | 修改 `ToolService.getTools` 方法签名（新增 tagId 参数） | 唯一调用方 ToolController 同步修改；MCP 不受影响 |

**本次改动风险等级**: L1

理由：修改了 `ToolService.getTools()` 的公共方法签名（新增参数），但调用方唯一且同步修改。API 层面向后兼容（tagId 为可选参数）。无数据库 schema 变更。

---

## 6. 层级依赖校验 (Layer Dependency Check)

> 校验后端是否仍满足 `controller → service → repository → model` 单向依赖。

本次改动严格遵循分层：
- Controller 接收参数 → 传递给 Service
- Service 调用 Repository 查询
- Repository 使用 JPQL 查询 ToolTag 关联

**结果**: PASS（无跨层依赖引入）

---

## 7. 回归测试建议 (Regression Suggestions)

- [ ] 验证不带 tagId 的 `GET /api/v1/tools` 行为不变（向后兼容）
- [ ] 验证 tagId + categoryId + keyword 三参数叠加筛选正确
- [ ] 验证前端分类 Pills 和标签 Pills 交互不冲突
- [ ] 验证 TagBadge 在详情页仍为纯展示（不可点击）

---

## 8. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方
- [x] 已列出上游/下游依赖
- [x] 已评估风险等级
- [x] 层级依赖校验通过
- [x] 已列出回归测试清单
- [ ] （L2 风险）不适用

---

**生成工具**: grep 手动追踪（CodeGraph 未索引目标符号）
**生成时间**: 2026-07-20
**基础**: openspec/changes/tool-filter-by-tag/proposal.md
