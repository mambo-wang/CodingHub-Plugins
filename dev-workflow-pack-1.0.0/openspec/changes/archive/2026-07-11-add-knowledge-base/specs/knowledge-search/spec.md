## ADDED Requirements（新增需求）

### Requirement: 基于知识库的语义搜索

系统 SHALL 提供 POST `/api/v1/knowledge/{id}/search` 端点，允许用户基于知识库内容进行语义搜索。此端点 SHALL 无需认证。返回结果为文本片段（chunk），包含来源文档、相关度分数。

#### Scenario: 未登录用户搜索知识库
- **WHEN** 未登录用户提交 POST `/api/v1/knowledge/42/search`，body: `{"query": "如何配置VLAN", "topK": 5}`
- **THEN** 系统调用 RAG POST /api/collections/{name}/search，返回 200，包含搜索结果列表，每条含 text（chunk 文本）、source（来源文件名）、score（相关度分数）、chunkIndex

#### Scenario: 搜索结果为空
- **WHEN** 用户搜索一个与知识库内容无关的查询
- **THEN** 系统返回 200，results 为空数组

#### Scenario: 搜索空知识库
- **WHEN** 用户搜索一个尚未上传任何文档的知识库
- **THEN** 系统返回 200，results 为空数组

#### Scenario: 搜索时指定 rerank
- **WHEN** 用户提交 POST `/api/v1/knowledge/42/search`，body: `{"query": "...", "rerank": true}`
- **THEN** 系统将 rerank=true 传递给 RAG，RAG 使用 reranker 模型对结果精排后返回

#### Scenario: 搜索时 RAG 服务不可用
- **WHEN** 用户提交搜索请求，但 RAG 服务无响应
- **THEN** 系统返回 503 Service Unavailable

#### Scenario: 搜索查询为空
- **WHEN** 用户提交 POST `/api/v1/knowledge/42/search`，query 为空字符串
- **THEN** 系统返回 400 Bad Request，提示"搜索查询不能为空"

### Requirement: 搜索结果包含上下文扩展

系统 SHALL 支持搜索请求中的 expandContext 参数（整数，默认 0），用于返回每个匹配 chunk 前后的相邻 chunk，提供更完整的上下文。

#### Scenario: 搜索带上下文扩展
- **WHEN** 用户提交 POST `/api/v1/knowledge/42/search`，body: `{"query": "...", "expandContext": 2}`
- **THEN** 系统将 expand_context=2 传递给 RAG，RAG 返回每个结果前后各 2 个相邻 chunk 的合并文本
