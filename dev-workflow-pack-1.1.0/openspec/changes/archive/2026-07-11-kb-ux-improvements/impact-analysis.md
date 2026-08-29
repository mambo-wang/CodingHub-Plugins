# Impact Analysis

> 基于 `design.md` 中的文件/类/测试清单执行 codegraph 扫描，确认技术设计的实际影响范围。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | 0 | — |
| 修改 | 5 | `frontend/src/components/knowledge/KnowledgeSearch.vue` |
| 修改 | | `frontend/src/components/knowledge/DocumentList.vue` |
| 修改 | | `frontend/vite.config.ts` |
| 修改 | | `rag-mcp/api/app.py`（RAG 独立仓库） |
| 修改 | | `rag-mcp/core/service.py`（RAG 独立仓库） |
| 删除 | 0 | — |

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `KnowledgeDetailPage.vue` | `frontend/src/pages/knowledge/KnowledgeDetailPage.vue:180,184` | L0 |
| `knowledgeService.search()` | `frontend/src/services/knowledge.ts:161` | L0 |
| `knowledgeService.deleteDocument()` | `frontend/src/services/knowledge.ts:124` | L0 |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

- `KnowledgeDetailPage` 通过 `<KnowledgeSearch>` 和 `<DocumentList>` 组件引用被修改的组件
- `KnowledgeEditorPage` 仅引用 `knowledgeService.getDetail/update`，不受影响
- `ConfigPanel`、`DocumentUpload` 使用 `knowledgeService` 的其他方法，不受影响

### 2.3 反向调用图（被谁调用）

```
[KnowledgeSearch.vue]
  └── KnowledgeDetailPage.vue (line 180)
        └── Vue Router /knowledge/:id

[DocumentList.vue]
  └── KnowledgeDetailPage.vue (line 184)
        └── Vue Router /knowledge/:id

[vite.config.ts /rag proxy]
  └── Vite dev server (npm run dev)
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `markdown-it` (npm) | 前端库 | L0 — 已有依赖，无需新增 |
| `highlight.js` (npm) | 前端库 | L0 — 已有依赖，无需新增 |
| `knowledgeService` | 前端服务层 | L0 — 不修改 service 接口 |
| `RagApiClient.java` | 后端 HTTP 客户端 | L0 — 不修改 |
| `starlette.responses.FileResponse` | RAG 框架 | L0 — 已有依赖 |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| 无 | `knowledgeService` 接口不变，新增的下载功能仅前端直连 RAG |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| `IaihubToolHandlerKbTest.java` | 单元 | 仍有效 | 无需改动（MCP KB 工具不涉及下载） |
| 无前端测试 | — | — | 项目前端无单元测试配置 |

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L0** | 纯前端 UI 改动（KnowledgeSearch、DocumentList） | 无 |
| **L0** | Vite proxy 配置修改 | 仅影响开发环境，不影响生产 |
| **L0** | RAG 新增 endpoint | 新增 API，不影响现有 endpoint |
| **L1** | `ingest_content` 保存文件到磁盘 | 增加磁盘写入，需确保目录创建和路径安全 |

**本次改动风险等级**: L0（RAG `ingest_content` 改动为 L1 但影响可控）

---

## 6. 层级依赖校验 (Layer Dependency Check)

本次不涉及后端 Java 代码修改，无需执行 `scripts/lint-arch.sh`。

- 前端：`KnowledgeSearch.vue` 和 `DocumentList.vue` 仍在 L3 组件层，引用 L1 服务层 `knowledgeService`，层级合法
- RAG：新增 endpoint 在 `api/app.py`（路由层），调用 `service.py`（业务层），读取文件系统，层级合法

---

## 7. 回归测试建议 (Regression Suggestions)

- [ ] 手动验证：搜索结果页面 Markdown 渲染正常（标题、代码块、列表）
- [ ] 手动验证：文档列表下载按钮可正常下载二进制文件（PDF/DOCX）
- [ ] 手动验证：新上传的文本文件可下载
- [ ] 手动验证：历史文本文件下载时显示友好提示
- [ ] 手动验证：`npm run dev` 启动后文档列表、上传、删除、下载均可用
- [ ] 手动验证：Nginx 生产环境下下载功能正常
- [ ] 手动验证：暗色/亮色主题切换后搜索结果样式正确

---

## 8. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方
- [x] 已列出上游/下游依赖
- [x] 已评估风险等级
- [x] 后端层级依赖不适用（无 Java 代码改动）
- [x] 已列出回归测试清单
- [x] 无 L2 风险

---

**生成时间**: 2026-06-29
**基础**: openspec/changes/kb-ux-improvements/proposal.md + design.md
