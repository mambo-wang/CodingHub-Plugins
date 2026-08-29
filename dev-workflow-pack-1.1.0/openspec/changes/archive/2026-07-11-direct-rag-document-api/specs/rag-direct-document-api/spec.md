## ADDED Requirements（新增需求）

### Requirement: KB 响应包含 RAG 服务地址
Java 后端 SHALL 在知识库详情响应（KbResponse）中包含 RAG 服务基础地址和文档 API 端点 URL，使客户端能自发现文档操作的目标地址。

#### Scenario: 获取 KB 详情包含 RAG URL
- **WHEN** 客户端调用 `GET /api/v1/knowledge/{id}`
- **THEN** 响应 SHALL 包含 `ragBaseUrl`（如 `http://localhost:8000`）和 `documentsUrl`（如 `http://localhost:8000/api/collections/vdi/documents`）字段

#### Scenario: KB 列表也包含 RAG URL
- **WHEN** 客户端调用 `GET /api/v1/knowledge` 获取知识库列表
- **THEN** 每个知识库条目 SHALL 包含 `ragBaseUrl` 和 `documentsUrl` 字段

### Requirement: 前端直连 RAG 进行文档上传
前端 SHALL 直接向 RAG Python 服务的 `POST /api/collections/{collection}/documents` 端点上传文件，不再经 Java 后端代理。

#### Scenario: 上传文档到 RAG
- **WHEN** 用户在前端选择文件上传到知识库
- **THEN** 前端 SHALL 从 KB 详情获取 `documentsUrl`，直接向该 URL 发送 multipart POST 请求
- **THEN** 上传成功时前端从 RAG 响应获取 `{status, filename, chunks}` 并更新文档列表

#### Scenario: 上传进度反馈
- **WHEN** 用户上传大文件
- **THEN** 前端 SHALL 显示上传进度条（基于 axios 的 onUploadProgress）

### Requirement: 前端直连 RAG 获取文档列表
前端 SHALL 直接调用 RAG 的 `GET /api/collections/{collection}/documents` 获取文档列表。

#### Scenario: 获取文档列表
- **WHEN** 用户进入知识库详情页
- **THEN** 前端 SHALL 直接请求 RAG 的文档列表端点，展示每个文档的 source（文件名）和 chunk_count

### Requirement: 前端直连 RAG 删除文档
前端 SHALL 直接调用 RAG 的 `DELETE /api/collections/{collection}/documents` 删除文档。

#### Scenario: 删除文档
- **WHEN** 用户点击删除文档按钮
- **THEN** 前端 SHALL 直接向 RAG 发送 DELETE 请求，body 为 `{"filepath": "..."}`
- **THEN** 删除成功后刷新文档列表

### Requirement: 前端直连 RAG 进行搜索和配置管理
前端 SHALL 直接调用 RAG 的搜索和配置 API，不再经 Java 后端代理。

#### Scenario: 语义搜索
- **WHEN** 用户在知识库详情页输入搜索关键词
- **THEN** 前端 SHALL 直接向 RAG 的 `POST /api/collections/{collection}/search` 发送搜索请求

#### Scenario: 获取和更新 RAG 配置
- **WHEN** 用户查看或修改知识库 RAG 配置（chunk_mode、chunk_size 等）
- **THEN** 前端 SHALL 直接调用 RAG 的 `GET/PUT /api/collections/{collection}/config`

### Requirement: Java 后端移除文档代理端点
Java 后端 SHALL 移除所有文档代理相关的 API 端点和内部代码。

#### Scenario: 文档上传端点不可用
- **WHEN** 客户端请求 `POST /api/v1/knowledge/{id}/documents`
- **THEN** 系统 SHALL 返回 404 Not Found

#### Scenario: 文档列表端点不可用
- **WHEN** 客户端请求 `GET /api/v1/knowledge/{id}/documents`
- **THEN** 系统 SHALL 返回 404 Not Found

#### Scenario: KB CRUD 和搜索仍正常
- **WHEN** 客户端请求 KB 的创建/更新/删除/列表/详情/搜索
- **THEN** 系统 SHALL 正常响应，不受文档端点移除的影响

### Requirement: RAG 地址动态配置
RAG 服务的基础地址 SHALL 从 Spring Boot 配置 `app.rag.base-url` 读取，不硬编码。

#### Scenario: 通过配置文件指定 RAG 地址
- **WHEN** `application.yml` 中 `app.rag.base-url` 设置为 `http://localhost:8000`
- **THEN** KbResponse 中的 `ragBaseUrl` SHALL 为该值，`documentsUrl` SHALL 为 `{ragBaseUrl}/api/collections/{ragCollection}/documents`
