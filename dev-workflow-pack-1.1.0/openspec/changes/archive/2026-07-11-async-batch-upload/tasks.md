# Tasks: async-batch-upload

## 1. RAG 服务 — SQLite 数据库层

- [ ] 1.1 创建 `rag/core/database.py`：实现 SQLite 数据库管理（WAL 模式、连接管理、documents 表 DDL）
- [ ] 1.2 实现 `Database` 类：`init_db()`、`insert_document()`、`update_status()`、`get_documents()`、`get_document_by_id()`、`mark_stale_as_failed()`
- [ ] 1.3 在 `rag/server.py` 的启动逻辑中调用 `database.init_db()` 和 `database.mark_stale_as_failed()`
- [ ] 1.4 为 `Database` 类编写单元测试 `rag/tests/test_database.py`：覆盖 CRUD、并发写入、WAL 模式验证

## 2. RAG 服务 — 异步处理引擎

- [ ] 2.1 创建 `rag/core/async_engine.py`：实现 `AsyncEngine` 类（Semaphore(5) 并发控制、asyncio.Task 管理）
- [ ] 2.2 实现 `AsyncEngine.submit_tasks()`：接收文件列表，为每个文件创建 asyncio.Task
- [ ] 2.3 实现 `_process_single_file()`：异步处理流水线（CONVERTING → CHUNKING → EMBEDDING → READY/FAILED），每阶段更新 SQLite 状态
- [ ] 2.4 将 `rag/core/service.py` 的 `ingest_file()` 和 `ingest_content()` 重构为异步版本 `ingest_file_async()`：内部按阶段拆分，每个阶段更新状态
- [ ] 2.5 `EmbeddingService.encode()` 增加 `batch_size` 参数（默认从环境变量 `RAG_EMBEDDING_BATCH_SIZE` 读取，缺省 32）
- [ ] 2.6 为 `AsyncEngine` 编写单元测试 `rag/tests/test_async_engine.py`：覆盖并发限制（5 个同时 + 排队）、状态转换、错误处理

## 3. RAG 服务 — REST API 端点

- [ ] 3.1 在 `rag/api/app.py` 新增 `POST /api/collections/{name}/documents/batch`：接收 multipart 多文件，保存磁盘，写入 SQLite（status=UPLOADING），调用 `AsyncEngine.submit_tasks()`，返回 202 + 文档列表
- [ ] 3.2 新增 `GET /api/collections/{name}/documents/status`：查询该集合所有文档状态（从 SQLite 读取），按 `created_at DESC` 排序
- [ ] 3.3 新增 `GET /api/collections/{name}/documents/{doc_id}/status`：查询单个文档详细状态（含 error_message）
- [ ] 3.4 修改现有 `GET /api/collections/{name}/documents`：响应中增加 `status` 字段（从 SQLite 关联查询）
- [ ] 3.5 编写集成测试 `rag/tests/test_batch_upload.py`：测试批量上传端点（正常、超量、空文件列表）
- [ ] 3.6 编写集成测试 `rag/tests/test_status_query.py`：测试状态查询端点（集合查询、单文档查询、404 场景）

## 4. Java 后端 — RagApiClient 扩展

- [ ] 4.1 `RagApiClient.java`：新增 `getDocumentStatus(String collection)` 方法 — 调用 RAG `GET /api/collections/{name}/documents/status`
- [ ] 4.2 `RagApiClient.java`：新增 `getDocumentStatusById(String collection, int docId)` 方法 — 调用 RAG `GET /api/collections/{name}/documents/{id}/status`

## 5. Java 后端 — MCP 工具

- [ ] 5.1 `IaihubToolHandler.java`：修改 `handleKbUploadDocument()` — uploadUrl 改为批量端点 `/documents/batch`，instruction 说明支持多文件，curlExample 更新
- [ ] 5.2 `IaihubToolHandler.java`：新增 `handleKbDocumentStatus()` 方法 — 调用 `RagApiClient.getDocumentStatus()`，返回文档状态列表
- [ ] 5.3 `McpSdkServerConfig.java`：注册 `kb_document_status` 工具（参数：kbId 必填，docId 可选）
- [ ] 5.4 更新 `IaihubToolHandlerKbTest.java`：验证 `handleKbUploadDocument` 返回批量上传端点信息
- [ ] 5.5 新增 `IaihubToolHandlerKbStatusTest.java`：测试 `handleKbDocumentStatus`（正常查询、指定 docId、集合不存在）
- [ ] 5.6 运行 `cd backend && ./gradlew test` 确认全部通过

## 6. 前端 — 类型和服务层

- [ ] 6.1 `types/knowledge.ts`：新增 `DocumentStatus` 枚举（UPLOADING / CONVERTING / CHUNKING / EMBEDDING / READY / FAILED）
- [ ] 6.2 `types/knowledge.ts`：新增 `RagDocumentStatus` 接口（id, filename, status, chunk_count, error_message, created_at, updated_at）
- [ ] 6.3 `services/knowledge.ts`：新增 `batchUpload(documentsUrl: string, files: File[], onProgress?)` 方法 — POST multipart 多文件到 RAG
- [ ] 6.4 `services/knowledge.ts`：新增 `getDocumentStatus(documentsUrl: string)` 方法 — GET 文档状态列表
- [ ] 6.5 `services/knowledge.ts`：新增 `getSingleDocumentStatus(collectionUrl: string, docId: number)` 方法 — GET 单文档状态
- [ ] 6.6 `services/knowledge.ts`：修改现有 `uploadDocument` 为兼容单文件上传（内部调用 `batchUpload`）
- [ ] 6.7 前端 `npm run build` 验证编译通过

## 7. 前端 — StatusBadge 组件

- [ ] 7.1 创建 `components/knowledge/StatusBadge.vue`：接收 `status` prop，根据状态渲染不同颜色徽章（参考 design-system.md 色彩规范）
- [ ] 7.2 处理中状态（UPLOADING/CONVERTING/CHUNKING/EMBEDDING）显示脉冲动画 + 对应 Lucide 图标
- [ ] 7.3 READY 状态显示绿色勾，FAILED 状态显示红色感叹号
- [ ] 7.4 支持暗色/亮色双主题（使用 CSS 变量）

## 8. 前端 — InfoBanner 组件

- [ ] 8.1 创建 `components/knowledge/InfoBanner.vue`：接收 `message` prop，显示信息横幅
- [ ] 8.2 包含关闭按钮（X 图标），点击后 emit `close` 事件
- [ ] 8.3 关闭动画：`opacity: 0; transform: translateY(-10px)`，300ms 过渡
- [ ] 8.4 使用 `role="status"` 和 `aria-live="polite"`
- [ ] 8.5 支持暗色/亮色双主题（参考 design-system.md InfoBanner 规范）

## 9. 前端 — DocumentUpload 多文件上传

- [ ] 9.1 修改 `DocumentUpload.vue`：文件选择器添加 `multiple` 属性，支持多文件选择
- [ ] 9.2 上传区域展示多个文件卡片（文件名 + 大小 + StatusBadge），替换原有的单文件进度条
- [ ] 9.3 调用 `knowledgeService.batchUpload()` 上传多文件，接收返回的文档 ID 列表
- [ ] 9.4 上传后通过 `emit` 通知父组件刷新文档列表
- [ ] 9.5 错误处理：超过 20 个文件时显示提示，文件过大时显示提示

## 10. 前端 — DocumentList 状态展示与轮询

- [ ] 10.1 修改 `DocumentList.vue`：使用 `knowledgeService.getDocumentStatus()` 替代原有的 `getDocuments()` 获取文档列表
- [ ] 10.2 文档行增加 StatusBadge 组件展示处理状态
- [ ] 10.3 实现轮询逻辑：`onMounted` 启动 `setInterval(3000)` 调用状态查询 API
- [ ] 10.4 轮询停止条件：所有文档状态为 `READY` 或 `FAILED` 时 `clearInterval`
- [ ] 10.5 `onUnmounted` 清理定时器，避免内存泄漏
- [ ] 10.6 FAILED 状态的文档行显示警告图标，hover 展示 error_message

## 11. 前端 — KnowledgeSearch 搜索提示

- [ ] 11.1 修改 `KnowledgeSearch.vue`：页面顶部添加 `InfoBanner` 组件
- [ ] 11.2 提示内容："本页面仅基于向量距离检索相关文档片段，建议使用 AI 编程助手接入 MCP 获得更智能的检索体验。"
- [ ] 11.3 关闭按钮点击后隐藏横幅（使用 Vue ref 状态管理，不持久化到 localStorage）

## 12. 前端 — 页面集成

- [ ] 12.1 修改 `KnowledgeDetailPage.vue`：传递 `documentsUrl` 给 `DocumentUpload` 和 `DocumentList`
- [ ] 12.2 `DocumentUpload` 上传完成后触发 `refresh` 事件，`DocumentList` 接收后立即查询最新状态
- [ ] 12.3 前端 `npm run build` 验证编译通过

## 13. 基础设施 — Nginx 配置

- [ ] 13.1 更新 `nginx.conf` 的 `/rag/` location 块：`client_max_body_size 200M;`（支持大文件批量上传）
- [ ] 13.2 添加 `proxy_read_timeout 600s;`（批量上传 HTTP 传输可能较慢）
- [ ] 13.3 重载 Nginx：`nginx -s reload`

## 14. 集成验证

- [ ] 14.1 启动 RAG 服务 + Java 后端 + Nginx + 前端，创建新知识库
- [ ] 14.2 通过前端批量上传 5 个文件，确认浏览器网络面板显示 `POST /rag/api/collections/{name}/documents/batch`
- [ ] 14.3 确认文档列表显示 5 个文件的状态徽章，状态从 UPLOADING 逐步变为 READY
- [ ] 14.4 确认轮询在所有文档 READY 后停止（网络面板不再有新请求）
- [ ] 14.5 通过 MCP 客户端调用 `kb_upload_document`，确认返回批量上传端点信息
- [ ] 14.6 通过 MCP 客户端调用 `kb_document_status`，确认返回文档状态列表
- [ ] 14.7 搜索页面确认显示能力提示横幅，点击关闭后消失
- [ ] 14.8 上传一个不支持格式的文件（如 .exe），确认状态变为 FAILED 并显示错误信息
