## ADDED Requirements（新增需求）

### Requirement: 知识库列表查询

系统 SHALL 提供 GET `/api/v1/knowledge` 端点，返回知识库列表（分页），支持 hot/latest 排序。此端点 SHALL 无需认证即可访问。

#### Scenario: 未登录用户查看知识库列表
- **WHEN** 未登录用户请求 GET `/api/v1/knowledge?page=0&size=20&sortBy=latest`
- **THEN** 系统返回 200，包含分页的知识库列表（PageResponse），每条记录含 id、name、description、ownerNickname、documentCount、createdAt

#### Scenario: 按热度排序知识库列表
- **WHEN** 用户请求 GET `/api/v1/knowledge?sortBy=hot`
- **THEN** 系统返回按 pinned DESC、score DESC 排序的知识库列表

#### Scenario: 知识库列表排除已删除项
- **WHEN** 用户请求知识库列表
- **THEN** 系统仅返回 status=NORMAL 的知识库，已软删除的不出现

### Requirement: 知识库详情查询

系统 SHALL 提供 GET `/api/v1/knowledge/{id}` 端点，返回单个知识库的完整信息。此端点 SHALL 无需认证。

#### Scenario: 查看存在的知识库详情
- **WHEN** 用户请求 GET `/api/v1/knowledge/42`，且该知识库存在且 status=NORMAL
- **THEN** 系统返回 200，包含 id、name、description、ownerId、ownerNickname、documentCount、ragCollection、createdAt

#### Scenario: 查看不存在的知识库
- **WHEN** 用户请求 GET `/api/v1/knowledge/999`，且该知识库不存在或 status=DELETED
- **THEN** 系统返回 404 ResourceNotFoundException

### Requirement: 创建知识库

系统 SHALL 提供 POST `/api/v1/knowledge` 端点，允许已认证用户创建知识库。请求体 SHALL 包含 name（必填，1-100 字符）、description（可选，最长 500 字符），以及可选的高级配置参数（chunkMode、chunkSize、chunkOverlap、rerank）。

#### Scenario: 登录用户成功创建知识库
- **WHEN** 已登录用户提交 POST `/api/v1/knowledge`，name="H3C技术文档"，description="技术文档合集"
- **THEN** 系统创建 MySQL 记录（ownerId=当前用户），调用 RAG PUT /config 初始化配置，返回 201 Created

#### Scenario: 创建知识库名称重复
- **WHEN** 已登录用户提交 POST `/api/v1/knowledge`，name 与已有 status=NORMAL 的知识库相同
- **THEN** 系统返回 409 Conflict，提示"知识库名称已存在"

#### Scenario: 未登录用户尝试创建知识库
- **WHEN** 未携带 JWT 的请求提交 POST `/api/v1/knowledge`
- **THEN** 系统返回 401 Unauthorized

#### Scenario: 创建知识库名称为空
- **WHEN** 已登录用户提交 POST `/api/v1/knowledge`，name 为空字符串
- **THEN** 系统返回 400 Bad Request，提示"知识库名称不能为空"

### Requirement: 更新知识库信息

系统 SHALL 提供 PUT `/api/v1/knowledge/{id}` 端点，允许知识库所有者或管理员更新知识库的 name 和 description。

#### Scenario: 所有者更新知识库描述
- **WHEN** 知识库所有者提交 PUT `/api/v1/knowledge/42`，description="更新后的描述"
- **THEN** 系统更新 MySQL 记录，若 description 变化则同步调用 RAG PUT /config 更新 description，返回 200

#### Scenario: 非所有者尝试更新知识库
- **WHEN** 非所有者、非管理员的已登录用户提交 PUT `/api/v1/knowledge/42`
- **THEN** 系统返回 403 Forbidden

#### Scenario: 更新名称与已有知识库冲突
- **WHEN** 所有者提交 PUT `/api/v1/knowledge/42`，name 与另一个 status=NORMAL 的知识库相同
- **THEN** 系统返回 409 Conflict

### Requirement: 删除知识库

系统 SHALL 提供 DELETE `/api/v1/knowledge/{id}` 端点，允许知识库所有者或管理员删除知识库。删除 SHALL 为软删除（status=DELETED），并同步调用 RAG 删除 collection。

#### Scenario: 所有者删除知识库
- **WHEN** 知识库所有者提交 DELETE `/api/v1/knowledge/42`
- **THEN** 系统将 MySQL 记录 status 设为 DELETED，调用 RAG DELETE /api/collections/{name}，返回 200

#### Scenario: 非所有者尝试删除知识库
- **WHEN** 非所有者、非管理员的已登录用户提交 DELETE `/api/v1/knowledge/42`
- **THEN** 系统返回 403 Forbidden

#### Scenario: 删除知识库时 RAG 服务不可用
- **WHEN** 所有者提交 DELETE `/api/v1/knowledge/42`，但 RAG 服务无响应
- **THEN** 系统仍将 MySQL 记录标记为 DELETED，返回 200（RAG 清理可异步重试或容忍）
