## ADDED Requirements（新增需求）

### Requirement: 批量文档上传
系统必须支持通过单次 HTTP 请求上传多个文档文件到指定知识库。

#### Scenario: 成功批量上传多个文件
- **WHEN** 用户发送 `POST /api/collections/{name}/documents/batch` 请求，包含 3 个 PDF 文件
- **THEN** 系统立即返回 `202 Accepted`，响应体包含每个文件的 `id`、`filename`、`status`（均为 `UPLOADING`）

#### Scenario: 超过文件数量限制
- **WHEN** 用户上传 25 个文件（超过限制）
- **THEN** 系统返回 `400 Bad Request`，错误信息说明"单次最多上传 20 个文件"

#### Scenario: 空文件列表
- **WHEN** 用户上传请求中不包含任何文件
- **THEN** 系统返回 `400 Bad Request`，错误信息说明"至少需要上传 1 个文件"

---

### Requirement: 异步文档处理
系统必须异步处理已上传的文档，通过状态机跟踪处理进度。

#### Scenario: 文档状态转换流程
- **WHEN** 系统接收到新上传的文档
- **THEN** 文档状态按顺序转换：`UPLOADING` → `CONVERTING` → `CHUNKING` → `EMBEDDING` → `READY`

#### Scenario: 格式转换失败
- **WHEN** 文档在 `CONVERTING` 阶段发生错误（如不支持的文件格式）
- **THEN** 文档状态变为 `FAILED`，`error_message` 字段记录"格式转换失败：{具体原因}"

#### Scenario: 向量化失败
- **WHEN** 文档在 `EMBEDDING` 阶段发生错误（如模型加载失败）
- **THEN** 文档状态变为 `FAILED`，`error_message` 字段记录"向量化失败：{具体原因}"

#### Scenario: 并发处理控制
- **WHEN** 用户同时上传 10 个文件
- **THEN** 系统使用 Semaphore(5) 控制并发，最多 5 个文件同时处理，其余 5 个排队等待

---

### Requirement: 文档元数据持久化
系统必须使用 SQLite 存储文档元数据，包含处理状态和分块信息。

#### Scenario: 创建文档记录
- **WHEN** 文件上传完成并保存到磁盘
- **THEN** 系统在 SQLite 中创建记录，包含 `collection`、`filename`、`filepath`、`file_size`、`uploader`、`status=UPLOADING`、`created_at`

#### Scenario: 更新处理状态
- **WHEN** 文档处理阶段发生变化
- **THEN** 系统更新 SQLite 中的 `status` 和 `updated_at` 字段

#### Scenario: 记录分块数量
- **WHEN** 文档成功完成向量化，状态变为 `READY`
- **THEN** 系统更新 `chunk_count` 为实际生成的向量数量

---

### Requirement: 文档状态查询 API
系统必须提供查询文档处理状态的 REST API。

#### Scenario: 查询集合所有文档状态
- **WHEN** 用户发送 `GET /api/collections/{name}/documents/status`
- **THEN** 系统返回该集合所有文档的 `id`、`filename`、`status`、`chunk_count`、`created_at`，按创建时间倒序排列

#### Scenario: 查询单个文档详细状态
- **WHEN** 用户发送 `GET /api/collections/{name}/documents/{doc_id}/status`
- **THEN** 系统返回该文档的完整信息，包含 `error_message`（如状态为 `FAILED`）

#### Scenario: 查询不存在的文档
- **WHEN** 用户查询不存在的 `doc_id`
- **THEN** 系统返回 `404 Not Found`

---

### Requirement: 前端多文件上传 UI
前端必须支持用户选择多个文件并显示每个文件的处理状态。

#### Scenario: 选择多个文件
- **WHEN** 用户点击上传区域
- **THEN** 系统打开文件选择器，允许选择多个文件（`multiple` 属性）

#### Scenario: 显示批量上传进度
- **WHEN** 用户提交了 5 个文件
- **THEN** 前端显示 5 个文件卡片，每个卡片显示文件名和状态徽章（上传中 / 转换中 / 分块中 / 向量化中 / 已解析 / 失败）

#### Scenario: 自动轮询更新状态
- **WHEN** 存在状态为 `UPLOADING`/`CONVERTING`/`CHUNKING`/`EMBEDDING` 的文档
- **THEN** 前端每 3 秒调用状态查询 API 并更新界面，直到所有文档状态变为 `READY` 或 `FAILED`

---

### Requirement: 文档列表状态展示
前端文档列表必须展示每个文档的当前处理状态。

#### Scenario: 显示状态徽章
- **WHEN** 文档列表加载完成
- **THEN** 每个文档行显示状态徽章：`UPLOADING`（灰色）、`CONVERTING`（黄色）、`CHUNKING`（蓝色）、`EMBEDDING`（紫色）、`READY`（绿色）、`FAILED`（红色）

#### Scenario: 显示错误信息
- **WHEN** 文档状态为 `FAILED`
- **THEN** 状态徽章旁显示警告图标，鼠标悬停显示 `error_message`

#### Scenario: 自动停止轮询
- **WHEN** 集合内所有文档状态均为 `READY` 或 `FAILED`
- **THEN** 前端停止状态轮询

---

### Requirement: MCP 批量上传工具
MCP Server 必须提供批量上传指引工具。

#### Scenario: 获取批量上传信息
- **WHEN** AI 助手调用 `kb_upload_document` 工具并指定多个文件
- **THEN** 工具返回批量上传端点 URL（`POST /api/collections/{name}/documents/batch`）、HTTP 方法、`requiresAuth` 说明（无需认证）、curl 示例

---

### Requirement: MCP 文档状态查询工具
MCP Server 必须提供查询文档处理状态的工具。

#### Scenario: 查询知识库文档状态
- **WHEN** AI 助手调用 `kb_document_status` 工具并传入知识库 ID
- **THEN** 工具返回该知识库所有文档的状态列表，包含文件名、处理状态、分块数量

#### Scenario: 查询特定文档状态
- **WHEN** AI 助手调用 `kb_document_status` 工具并传入知识库 ID 和文档 ID
- **THEN** 工具返回该文档的详细状态，包含错误信息（如处理失败）

---

### Requirement: 搜索页能力提示
前端知识库搜索页必须展示信息提示，说明搜索能力的局限性。

#### Scenario: 显示搜索能力提示
- **WHEN** 用户打开知识库语义搜索页面
- **THEN** 页面顶部显示信息提示横幅："本页面仅基于向量距离检索相关文档片段，建议使用 AI 编程助手接入 MCP 获得更智能的检索体验。"

#### Scenario: 提示可关闭
- **WHEN** 用户点击提示横幅的关闭按钮
- **THEN** 提示横幅消失，当前会话内不再显示（使用 Vue 状态管理，不持久化）

---

### Requirement: 服务重启恢复
系统必须在服务重启后处理中间状态的文档。

#### Scenario: 扫描中间状态文档
- **WHEN** RAG 服务启动时
- **THEN** 系统扫描 SQLite 中状态为 `UPLOADING`/`CONVERTING`/`CHUNKING`/`EMBEDDING` 的文档，将其标记为 `FAILED`，错误信息为"服务重启，处理中断"

---

### Requirement: 大文件上传支持
系统必须支持大文件的 multipart 上传。

#### Scenario: 上传 50MB 文件
- **WHEN** 用户通过前端上传 50MB 的 PDF 文件
- **THEN** Nginx 和 RAG 服务均接受该请求，文件成功保存并开始异步处理

#### Scenario: 上传超过 Nginx 限制的文件
- **WHEN** 用户上传 250MB 文件（超过 Nginx 200MB 限制）
- **THEN** Nginx 返回 `413 Request Entity Too Large`，前端显示"文件过大，请上传小于 200MB 的文件"
