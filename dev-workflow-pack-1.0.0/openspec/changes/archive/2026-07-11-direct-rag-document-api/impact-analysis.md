# Impact Analysis: direct-rag-document-api

## 改动类型判定

design.md 中存在多个现有源码文件的修改/删除，属于 **L2 — 修改公共 API + 删除端点**。

## 受影响文件分析

### 后端（Java）

| 文件 | 改动类型 | 风险 | 说明 |
|------|---------|------|------|
| `KnowledgeBaseController.java` | 删除方法 | L2 | 删除 uploadDocument/deleteDocument/listDocuments 端点，影响前端和 MCP |
| `KnowledgeBaseService.java` | 删除方法 | L2 | 删除 uploadDocument/deleteDocument/listDocuments/search 方法 |
| `RagApiClient.java` | 删除方法 | L1 | 删除 uploadDocument/deleteDocument/search，保留 configureCollection/getCollectionConfig |
| `dto/kb/KbResponse.java` | 新增字段 | L1 | 新增 ragBaseUrl、documentsUrl |
| `mcp/IaihubToolHandler.java` | 修改方法 | L1 | handleKbUploadDocument 改返回 RAG 直传地址 |
| `mcp/McpSdkServerConfig.java` | 无改动 | - | 工具注册不变 |
| `config/SecurityConfig.java` | 删除规则 | L1 | 删除 `/api/v1/knowledge/{id}/documents` 相关安全规则 |

### 前端（Vue）

| 文件 | 改动类型 | 风险 | 说明 |
|------|---------|------|------|
| `services/knowledge.ts` | 修改方法 | L1 | 6 个方法改请求目标为 RAG URL |
| `types/knowledge.ts` | 新增类型 | L0 | KbResponse 新增 ragBaseUrl/documentsUrl 字段 |
| `pages/knowledge/KnowledgeDetailPage.vue` | 修改调用 | L1 | 适配新的 service 方法签名 |

### 测试

| 文件 | 改动类型 | 说明 |
|------|---------|------|
| `IaihubToolHandlerKbTest.java` | 修改 | handleKbUploadDocument 测试用例需更新 |
| `RagApiClient` 相关测试 | 删除 | 被删除方法的测试用例需移除 |

## 依赖链路追踪

```
KnowledgeBaseController.uploadDocument()
  └─ KnowledgeBaseService.uploadDocument()
       ├─ RagApiClient.uploadDocument()     ← 删除
       └─ KbDocumentRepository.save()       ← 不再调用

KnowledgeBaseController.listDocuments()
  └─ KnowledgeBaseService.listDocuments()
       └─ KbDocumentRepository.findByKbIdAndStatus()  ← 不再调用

IaihubToolHandler.handleKbUploadDocument()
  └─ KnowledgeBaseService.getKnowledgeBase()  ← 保留（获取 ragCollection）
       └─ 构造 KbUploadDocumentInfoResponse   ← 改返回内容
```

## 回归测试建议

| 测试项 | 优先级 | 验证方式 |
|--------|--------|---------|
| KB CRUD 全流程 | P0 | 前端 E2E 或手动测试 |
| MCP kb_list/kb_create/kb_update/kb_delete | P0 | MCP 客户端调用验证 |
| MCP kb_upload_document 返回 RAG URL | P0 | 检查返回 JSON 包含完整 RAG 地址 |
| MCP kb_search 仍正常工作 | P0 | MCP 客户端搜索验证 |
| 前端文档上传直连 RAG | P0 | 浏览器网络面板确认请求目标 |
| 前端文档列表直连 RAG | P1 | 浏览器网络面板确认请求目标 |
| 前端搜索直连 RAG | P1 | 浏览器网络面板确认请求目标 |
| 旧文档端点返回 404 | P2 | curl 验证 |

## 设计修正建议

- design.md 未提及 `dto/kb/KbDocumentResponse.java` — 此 DTO 在删除文档端点后不再被 Controller 使用，但可保留（不影响功能）
- `KbDocumentRepository.java` 和 `KbDocument.java` 可保留不删（向后兼容，不增加维护成本）
