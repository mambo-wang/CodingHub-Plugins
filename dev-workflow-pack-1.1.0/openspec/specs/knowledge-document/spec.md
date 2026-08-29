## ADDED Requirements（新增需求）

### Requirement: 知识库文档列表查询

系统 SHALL 提供 GET `/api/v1/knowledge/{id}/documents` 端点，返回指定知识库的文档列表。此端点 SHALL 无需认证。

#### Scenario: 查看知识库的文档列表
- **WHEN** 用户请求 GET `/api/v1/knowledge/42/documents`
- **THEN** 系统返回 200，包含该知识库下所有 status=NORMAL 的文档列表，每条含 id、originalName、fileSize、chunkCount、chunkMode、uploaderNickname、createdAt

#### Scenario: 查看不存在知识库的文档列表
- **WHEN** 用户请求 GET `/api/v1/knowledge/999/documents`，知识库不存在
- **THEN** 系统返回 404 ResourceNotFoundException

### Requirement: 上传文档到知识库

系统 SHALL 提供 POST `/api/v1/knowledge/{id}/documents` 端点，允许知识库所有者上传文档。接收 multipart/form-data 格式的文件，转发至 RAG 服务处理。

#### Scenario: 所有者上传文本文件
- **WHEN** 知识库所有者提交 POST `/api/v1/knowledge/42/documents`，包含一个 .md 文件
- **THEN** 系统将文件转发至 RAG POST /api/collections/{name}/documents，RAG 返回 chunk 数，系统在 MySQL 创建 kb_document 记录，返回 201 Created

#### Scenario: 所有者上传二进制文档
- **WHEN** 知识库所有者提交 POST `/api/v1/knowledge/42/documents`，包含一个 .pdf 文件
- **THEN** 系统将文件转发至 RAG，RAG 使用 markitdown 转换后进行向量化，返回 chunk 数，系统记录文档元数据，返回 201 Created

#### Scenario: 非所有者尝试上传文档
- **WHEN** 非所有者的已登录用户提交 POST `/api/v1/knowledge/42/documents`
- **THEN** 系统返回 403 Forbidden

#### Scenario: 上传文档时 RAG 服务不可用
- **WHEN** 所有者上传文档，但 RAG 服务无响应
- **THEN** 系统返回 503 Service Unavailable，提示"RAG 服务暂时不可用"

#### Scenario: 未登录用户尝试上传文档
- **WHEN** 未携带 JWT 的请求提交 POST `/api/v1/knowledge/42/documents`
- **THEN** 系统返回 401 Unauthorized

### Requirement: 删除知识库文档

系统 SHALL 提供 DELETE `/api/v1/knowledge/{id}/documents/{docId}` 端点，允许知识库所有者或管理员删除文档。

#### Scenario: 所有者删除文档
- **WHEN** 知识库所有者提交 DELETE `/api/v1/knowledge/42/documents/7`
- **THEN** 系统将 MySQL kb_document 记录标记为 DELETED，调用 RAG DELETE /api/collections/{name}/documents 删除向量数据，返回 200

#### Scenario: 非所有者尝试删除文档
- **WHEN** 非所有者、非管理员的已登录用户提交 DELETE `/api/v1/knowledge/42/documents/7`
- **THEN** 系统返回 403 Forbidden

#### Scenario: 删除不存在的文档
- **WHEN** 所有者提交 DELETE `/api/v1/knowledge/42/documents/999`，文档不存在
- **THEN** 系统返回 404 ResourceNotFoundException
