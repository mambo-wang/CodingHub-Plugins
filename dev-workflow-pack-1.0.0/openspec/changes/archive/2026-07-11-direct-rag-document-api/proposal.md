## 为什么（Why）

当前知识库的文档操作（上传/列表/删除/搜索）全部经 Java 后端代理转发至 RAG Python 服务。RAG 处理文档涉及 markitdown 转换 + embedding 模型推理，单个 53KB docx 文件处理时间可达 5 分钟，导致 Java HTTP 客户端频繁超时（即使 300s/900s 也不够）。Java 在文档链路中纯粹充当代理，增加了不必要的延迟和故障点。前端和 MCP 客户端应直连 RAG 服务处理文档操作，Java 仅保留 KB 元数据管理。

## 变更内容（What Changes）

- **BREAKING** 删除 Java 后端的文档代理 API：`POST /{id}/documents`（上传）、`DELETE /{id}/documents/{docId}`（删除）、`GET /{id}/documents`（列表）。前端和 MCP 客户端改为直连 RAG Python 服务。
- KbResponse DTO 新增 `ragBaseUrl`、`documentsUrl` 字段，Java 在返回 KB 信息时告知客户端 RAG 服务地址。
- 前端 `knowledge.ts` service 层的文档/搜索/配置操作改为直连 RAG URL（从 KB detail 获取）。
- MCP 工具 `kb_upload_document` 返回 RAG 直传地址（`http://rag:8000/api/collections/{name}/documents`）和无需认证的说明，替代原有的 Java 后端地址。
- `kb_search` 保持经 Java 代理（搜索为秒级响应，无超时问题）。
- 删除 Java 的 `RagApiClient` 中 `uploadDocument`、`deleteDocument`、`search` 方法，仅保留 `configureCollection` 和 `getCollectionConfig`。
- MySQL `kb_document` 表保留但不再写入新记录；文档列表直接查 RAG。
- 文档操作不做权限校验（内部系统，接受风险）。

## 能力清单（Capabilities）

### 新增能力（New Capabilities）

- `rag-direct-document-api`: 前端和 MCP 客户端直连 RAG Python 服务进行文档上传、列表、删除操作；Java 后端在 KB 响应中返回 RAG 服务地址，不再代理文档请求。

### 修改能力（Modified Capabilities）

- `mcp-knowledge-base`: `kb_upload_document` 工具返回 RAG 直传地址而非 Java 后端地址；移除认证要求说明。

## 影响范围（Impact）

- **Java 后端**：`KnowledgeBaseController` 删除 3 个文档端点；`KnowledgeBaseService` 删除 `uploadDocument`/`deleteDocument`/`listDocuments`/`search` 方法；`RagApiClient` 删除 3 个方法；`KbResponse` DTO 新增字段；`SecurityConfig` 删除文档相关规则；MCP `IaihubToolHandler.handleKbUploadDocument` 改返回内容。
- **前端**：`knowledge.ts` service 的 6 个方法（uploadDocument/deleteDocument/getDocuments/search/getConfig/updateConfig）改请求目标为 RAG URL；`KnowledgeDetailPage.vue` 适配。
- **MCP 客户端**：`kb_upload_document` 返回结构变化（URL 指向 RAG，无认证要求）。
- **数据库**：`kb_document` 表不再写入，但不删表（向后兼容）。
- **RAG 服务**：无改动（已有完整的文档 REST API）。
