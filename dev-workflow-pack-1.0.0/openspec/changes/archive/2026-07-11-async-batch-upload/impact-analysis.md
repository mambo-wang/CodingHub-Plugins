# Impact Analysis: async-batch-upload

> 基于 `design.md` 中的文件/类/测试清单执行 codegraph 扫描，确认技术设计的实际影响范围。
>
> **位置**：在 `design` 之后、`tasks` 之前生成。
>
> **触发条件**：仅当 `design.md` 涉及**修改现有代码**时必选；纯新增模块/页面时跳过此 artifact。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | 6 | `rag/core/database.py`, `rag/core/async_engine.py`, `frontend/src/components/knowledge/StatusBadge.vue`, `frontend/src/components/knowledge/InfoBanner.vue`, `frontend/src/types/knowledge-status.ts`, `backend/src/test/java/com/iaihub/toolbox/mcp/IaihubToolHandlerKbStatusTest.java` |
| 修改 | 11 | `rag/api/app.py`, `rag/core/service.py`, `rag/server.py`, `frontend/src/components/knowledge/DocumentUpload.vue`, `frontend/src/components/knowledge/DocumentList.vue`, `frontend/src/components/knowledge/KnowledgeSearch.vue`, `frontend/src/services/knowledge.ts`, `frontend/src/types/knowledge.ts`, `backend/src/main/java/com/iaihub/toolbox/mcp/IaihubToolHandler.java`, `backend/src/main/java/com/iaihub/toolbox/mcp/McpSdkServerConfig.java`, `backend/src/main/java/com/iaihub/toolbox/service/kb/RagApiClient.java` |
| 删除 | 0 | - |

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `DocumentUpload.vue` → `knowledge.ts.batchUpload()` | `frontend/src/components/knowledge/DocumentUpload.vue:87` | L1 |
| `DocumentList.vue` → `knowledge.ts.getDocumentStatus()` | `frontend/src/components/knowledge/DocumentList.vue:45` | L1 |
| `KnowledgeSearch.vue` → 渲染 `InfoBanner` | `frontend/src/components/knowledge/KnowledgeSearch.vue:12` | L0 |
| `IaihubToolHandler.handleKbUploadDocument()` → 返回批量上传信息 | `backend/src/main/java/com/iaihub/toolbox/mcp/IaihubToolHandler.java:342` | L1 |
| `IaihubToolHandler.handleKbDocumentStatus()` → `RagApiClient.getDocumentStatus()` | `backend/src/main/java/com/iaihub/toolbox/mcp/IaihubToolHandler.java:415` | L0 (新增方法) |
| `app.py.batch_upload_endpoint()` → `async_engine.submit_tasks()` | `rag/api/app.py:156` | L0 (新增端点) |
| `app.py.status_query_endpoint()` → `database.get_documents()` | `rag/api/app.py:189` | L0 (新增端点) |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

- `KnowledgeDetailPage.vue` 通过 `DocumentUpload.vue` 调用 `batchUpload()`
- `KnowledgeDetailPage.vue` 通过 `DocumentList.vue` 调用 `getDocumentStatus()`
- `McpSdkServerConfig` 注册 `handleKbDocumentStatus` 工具
- `async_engine.submit_tasks()` 通过 `service.ingest_file_async()` 调用 `database.update_status()`

### 2.3 反向调用图（被谁调用）

```
[batch_upload_endpoint] (rag/api/app.py:156)
  ├── [前端 DocumentUpload.vue] (frontend/src/components/knowledge/DocumentUpload.vue:87)
  │     └── [KnowledgeDetailPage.vue] (frontend/src/pages/knowledge/KnowledgeDetailPage.vue)
  └── [MCP kb_upload_document] (backend/src/main/java/com/iaihub/toolbox/mcp/IaihubToolHandler.java:342)
        └── [MCP Client] (外部)

[status_query_endpoint] (rag/api/app.py:189)
  ├── [前端 DocumentList.vue 轮询] (frontend/src/components/knowledge/DocumentList.vue:45)
  │     └── [KnowledgeDetailPage.vue] (frontend/src/pages/knowledge/KnowledgeDetailPage.vue)
  └── [MCP kb_document_status] (backend/src/main/java/com/iaihub/toolbox/mcp/IaihubToolHandler.java:415)
        └── [MCP Client] (外部)
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `aiosqlite` (Python 库) | 异步 SQLite 驱动 | L0 (新增依赖) |
| `asyncio.Semaphore` (Python 标准库) | 并发控制 | L0 |
| `zvec` (向量数据库) | 存储向量数据 | L0 (已存在) |
| `sentence-transformers` (Python 库) | Embedding 模型 | L0 (已存在) |
| `markitdown` (Python 库) | 文档格式转换 | L0 (已存在) |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| 前端知识库详情页 | 文档上传和列表展示变化 |
| MCP 客户端 | `kb_upload_document` 返回结构变化，新增 `kb_document_status` 工具 |
| Nginx 配置 | 需调整 `/rag/` location 的 `client_max_body_size` 和 `proxy_read_timeout` |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| `backend/src/test/java/com/iaihub/toolbox/mcp/IaihubToolHandlerKbTest.java` | 单元 | 需更新 | 更新 `handleKbUploadDocument` 测试用例，验证返回批量上传信息 |
| `backend/src/test/java/com/iaihub/toolbox/mcp/IaihubToolHandlerKbStatusTest.java` | 单元 | 需新增 | 新增 `handleKbDocumentStatus` 测试用例 |
| `rag/tests/test_async_engine.py` | 单元 | 需新增 | 测试异步任务提交和状态更新 |
| `rag/tests/test_database.py` | 单元 | 需新增 | 测试 SQLite CRUD 操作 |
| `rag/tests/test_batch_upload.py` | 集成 | 需新增 | 测试批量上传端点 |
| `rag/tests/test_status_query.py` | 集成 | 需新增 | 测试状态查询端点 |

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L0** | 纯新增模块（`database.py`, `async_engine.py`, `StatusBadge.vue`） | 无影响，独立测试 |
| **L1** | 修改 `DocumentUpload.vue` 和 `DocumentList.vue` 的 props 和事件 | 前端组件测试 + 手动验证双主题 |
| **L1** | 修改 `knowledge.ts` service 层，新增 `batchUpload` 和 `getDocumentStatus` 方法 | TypeScript 类型检查 + API 调用测试 |
| **L1** | 修改 `IaihubToolHandler.handleKbUploadDocument()` 返回结构 | 单元测试验证返回格式 |
| **L1** | 修改 `rag/core/service.py` 的 `ingest_file` 为异步版本 | 集成测试验证异步处理流程 |

**本次改动风险等级**: **L1**（修改现有组件的公共 API 和返回结构，但不涉及数据库 schema 变更）

---

## 6. 层级依赖校验 (Layer Dependency Check)

> 校验后端是否仍满足 `controller → service → repository → model` 单向依赖。

```bash
bash scripts/lint-arch.sh
```

**结果**: PASS（本次改动不涉及后端层级结构变更，仅在 MCP 层新增工具方法）

---

## 7. 回归测试建议 (Regression Suggestions)

- [ ] `test_single_file_upload` —— 验证单文件上传仍正常工作（向后兼容），位于 `rag/tests/test_api.py`
- [ ] `test_document_delete` —— 验证删除文档后状态正确更新，位于 `rag/tests/test_api.py`
- [ ] `test_mcp_kb_upload_document` —— 验证 MCP 工具返回正确的批量上传信息，位于 `backend/src/test/java/com/iaihub/toolbox/mcp/IaihubToolHandlerKbTest.java`
- [ ] `test_frontend_polling_stop` —— 验证所有文档处理完成后前端停止轮询，位于 `frontend/src/components/knowledge/DocumentList.vue` (手动测试)
- [ ] `test_concurrent_file_processing` —— 验证 Semaphore(5) 正确限制并发数，位于 `rag/tests/test_async_engine.py`
- [ ] `test_service_restart_recovery` —— 验证服务重启后中间状态文档被标记为 FAILED，位于 `rag/tests/test_database.py`
- [ ] `test_large_file_upload` —— 验证 50MB 文件上传成功，位于 `rag/tests/test_batch_upload.py`
- [ ] `test_search_hint_dismissible` —— 验证搜索页提示可关闭且会话内保持隐藏，位于 `frontend/src/components/knowledge/KnowledgeSearch.vue` (手动测试)

---

## 8. 设计修正建议 (Design Amendment Suggestions)

基于代码影响分析，发现以下设计文档中可能遗漏的点：

1. **前端轮询管理**：`DocumentList.vue` 需要管理轮询定时器，建议使用 Vue 的 `onMounted` / `onUnmounted` 生命周期钩子，避免内存泄漏。设计文档未明确提及定时器的清理逻辑。

2. **SQLite 连接池**：`async_engine.py` 中的多个 asyncio.Task 可能同时访问 SQLite，建议使用 `aiosqlite` 的连接池模式（或单连接 + 事务队列），避免 SQLite 锁冲突。设计文档提到了 WAL 模式，但未详细说明连接管理策略。

3. **错误信息国际化**：`error_message` 字段当前存储英文错误信息，若需支持多语言，应在前端根据错误码映射显示文本，而非直接展示后端返回的错误字符串。

4. **文件去重策略**：设计文档的"待定问题"中提到文件去重，建议在实施时明确：同一文件名重复上传时，是覆盖（更新现有记录）还是跳过（返回已存在的记录）。推荐：默认跳过，提供 `force=true` 参数强制覆盖。

---

## 9. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方
- [x] 已列出上游/下游依赖
- [x] 已评估风险等级（L1）
- [x] `scripts/lint-arch.sh` 校验通过（PASS）
- [x] 已列出回归测试清单（8 项）
- [x] 已提出设计修正建议（4 项）
- [ ] （L2 风险）已通知相关模块负责人 —— 不适用（本次为 L1 风险）

---

**生成工具**: Task(code-explorer) 子代理 + scripts/lint-arch.sh 静态分析  
**生成时间**: 2026-06-27  
**基础**: openspec/changes/async-batch-upload/proposal.md, design.md
