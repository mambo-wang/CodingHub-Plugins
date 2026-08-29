## 为什么（Why）

当前知识库文档上传存在三个核心痛点：

1. **单文件上传效率低**：用户每次只能上传一个文件，多文件需反复操作，体验差。
2. **同步阻塞与状态不可见**：上传请求在文档完成格式转换、分块、向量化后才返回响应。大文件处理耗时数分钟，期间前端仅显示"处理中..."，用户无法得知具体进展（是正在转换格式？还是正在分块？还是卡住了？）。
3. **搜索能力认知偏差**：用户在知识库详情页使用语义搜索时，不清楚该搜索仅基于向量距离召回，误以为具备完整 AI 理解能力。应引导用户通过 MCP 接入 AI 编程助手获得更智能的检索体验。

此外，MCP 工具目前仅支持单文件上传指引和基础搜索，缺乏批量操作和状态查询能力，限制了 AI 助手在知识库管理场景的自动化能力。

## 变更内容（What Changes）

- **新增批量上传 API**：RAG 服务新增 `POST /api/collections/{name}/documents/batch` 端点，支持单次 multipart 请求上传多个文件，每个文件独立异步处理。
- **新增文档状态追踪**：RAG 服务引入 SQLite 数据库存储文档元数据（文件名、大小、上传者、状态、分块数、创建/更新时间），替代现有的 `_registry.json` 文件。文档状态包含 `UPLOADING`、`CONVERTING`、`CHUNKING`、`EMBEDDING`、`READY`、`FAILED` 六种状态。
- **新增文档状态查询 API**：RAG 服务新增 `GET /api/collections/{name}/documents/status` 端点，返回所有文档的当前处理状态。
- **前端批量上传 UI**：`DocumentUpload.vue` 支持多文件选择和拖拽，显示每个文件的独立上传进度和处理状态。
- **前端文档列表状态展示**：`DocumentList.vue` 展示文档处理状态徽章，自动轮询更新直到所有文档处理完成。
- **搜索页提示**：`KnowledgeSearch.vue` 新增信息提示，说明当前搜索基于向量距离，建议使用 AI 编程助手接入 MCP 获得更好效果。
- **MCP 工具增强**：`kb_upload_document` 工具返回批量上传端点信息；新增 `kb_document_status` 工具查询文档处理状态。
- **RAG 异步处理引擎**：RAG 服务内部引入 asyncio 任务队列 + Semaphore(5) 并发控制，文档上传后立即返回，后台异步执行转换→分块→向量化流水线。

## 能力清单（Capabilities）

### 新增能力（New Capabilities）

- `batch-document-upload`: RAG 服务批量文档上传 API、异步处理引擎、状态追踪（SQLite 存储）、状态查询 API；前端多文件上传 UI 与状态展示；MCP 批量上传与状态查询工具。

### 修改能力（Modified Capabilities）

（无现有规格级别的行为变更，所有改动均为新增能力。）

## 影响范围（Impact）

- **RAG Python 服务**：新增 SQLite 数据库层（`core/database.py`）；重构 `core/service.py` 的 `ingest_file`/`ingest_content` 为异步流水线；`api/app.py` 新增 batch upload 和 status 端点；`server.py` 新增 MCP 工具。
- **Java 后端**：`RagApiClient` 新增 `batchUpload`、`getDocumentStatus` 方法；`IaihubToolHandler` 新增 `handleKbDocumentStatus` 方法；`McpSdkServerConfig` 注册新工具。
- **前端**：`DocumentUpload.vue` 支持多文件；`DocumentList.vue` 增加状态列和轮询；`KnowledgeSearch.vue` 增加提示横幅；`services/knowledge.ts` 新增批量上传和状态查询方法；`types/knowledge.ts` 新增状态类型。
- **数据库**：RAG 服务本地新增 SQLite 数据库文件（`data/documents.db`），不影响 MySQL。
- **基础设施**：Nginx 的 `/rag/` 代理需确保支持大文件 multipart 上传（`client_max_body_size` 配置）。
