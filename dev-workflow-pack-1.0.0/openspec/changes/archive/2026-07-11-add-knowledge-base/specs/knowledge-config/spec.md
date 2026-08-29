## ADDED Requirements（新增需求）

### Requirement: 查看知识库配置

系统 SHALL 提供 GET `/api/v1/knowledge/{id}/config` 端点，返回知识库的当前配置。此端点 SHALL 无需认证。配置数据从 RAG 服务实时获取。

#### Scenario: 查看已有知识库的配置
- **WHEN** 用户请求 GET `/api/v1/knowledge/42/config`
- **THEN** 系统调用 RAG GET /api/collections/{name}/config，返回 200，包含 chunkMode、chunkSize、chunkOverlap、rerank、description

#### Scenario: RAG 服务不可用时查看配置
- **WHEN** 用户请求 GET `/api/v1/knowledge/42/config`，RAG 服务无响应
- **THEN** 系统返回 503 Service Unavailable

### Requirement: 更新知识库配置

系统 SHALL 提供 PUT `/api/v1/knowledge/{id}/config` 端点，允许知识库所有者或管理员更新配置。请求体中的字段为部分更新，仅包含需要修改的参数。

#### Scenario: 所有者更新分块模式
- **WHEN** 知识库所有者提交 PUT `/api/v1/knowledge/42/config`，body: `{"chunkMode": "semantic"}`
- **THEN** 系统调用 RAG PUT /api/collections/{name}/config，仅更新 chunk_mode 为 semantic，其他参数保持不变，返回 200

#### Scenario: 所有者更新多个配置参数
- **WHEN** 知识库所有者提交 PUT `/api/v1/knowledge/42/config`，body: `{"chunkSize": 500, "rerank": false}`
- **THEN** 系统调用 RAG PUT /config 更新 chunk_size 和 rerank，返回 200 包含完整更新后的配置

#### Scenario: 非所有者尝试更新配置
- **WHEN** 非所有者、非管理员的已登录用户提交 PUT `/api/v1/knowledge/42/config`
- **THEN** 系统返回 403 Forbidden

#### Scenario: 更新配置时描述变化同步到 MySQL
- **WHEN** 所有者提交 PUT `/api/v1/knowledge/42/config`，body 包含 description 字段
- **THEN** 系统同时更新 RAG 配置和 MySQL knowledge_base 表的 description 字段

### Requirement: 创建时初始化配置

系统 SHALL 在创建知识库时，使用请求中的配置参数（或默认值）调用 RAG PUT /config 初始化 collection 配置。默认值为 chunkMode=structural、chunkSize=800、chunkOverlap=50、rerank=true。

#### Scenario: 创建知识库时使用默认配置
- **WHEN** 用户创建知识库，未指定高级配置参数
- **THEN** 系统使用默认值（structural/800/50/true）调用 RAG PUT /config

#### Scenario: 创建知识库时使用自定义配置
- **WHEN** 用户创建知识库，指定 chunkMode=semantic、chunkSize=500
- **THEN** 系统使用用户指定值调用 RAG PUT /config，未指定的参数使用默认值
