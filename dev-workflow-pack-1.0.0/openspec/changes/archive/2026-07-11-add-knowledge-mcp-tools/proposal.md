## 为什么（Why）

CodingHub 已通过 REST API 和前端页面实现了完整的知识库管理功能（CRUD、文档上传、语义搜索、配置管理），底层对接 RAG 向量检索服务。但目前 AI 助手（如 QoderWork、CodeBuddy 等 MCP 客户端）无法通过 MCP 协议操作知识库——只能浏览工具和帖子，无法管理知识库内容。增加知识库 MCP 工具后，AI 助手可以直接帮用户创建知识库、上传文档、执行语义检索，将知识库能力开放给所有 MCP 生态客户端。

## 变更内容（What Changes）

- 在 `McpSdkServerConfig` 中新增 6 个知识库相关 MCP 工具注册
- 在 `IaihubToolHandler` 中新增对应的 handler 方法，注入 `KnowledgeBaseService` 依赖
- 新增 MCP 专用响应 DTO（内部类），序列化知识库操作结果
- 写操作（创建/编辑/删除知识库、上传/删除文档、修改配置）沿用现有 MCP 认证模式：客户端传入 username/password，handler 内联调用 `userService.login()` 获取用户身份
- 读操作（列表/详情/搜索/文档列表/配置查看）无需认证，与 REST API 保持一致的公开策略

## 能力清单（Capabilities）

### 新增能力（New Capabilities）

- `mcp-knowledge-base`: MCP 协议下的知识库全生命周期管理，包含 6 个工具：
  - `h3_coding_hub_kb_list` — 列出知识库（分页，支持热度/最新排序）
  - `h3_coding_hub_kb_search` — 语义搜索知识库内容（公开，无需认证）
  - `h3_coding_hub_kb_create` — 创建知识库（需认证）
  - `h3_coding_hub_kb_update` — 更新知识库名称/描述/RAG配置参数（需认证）
  - `h3_coding_hub_kb_delete` — 删除知识库（需认证）
  - `h3_coding_hub_kb_upload_document` — 上传文档到知识库（需认证，返回 REST API 上传信息供客户端直传）

### 修改能力（Modified Capabilities）

（无现有规格需要修改，知识库 MCP 能力为全新引入）

## 影响范围（Impact）

- **后端代码**：`McpSdkServerConfig.java`（+6 工具注册）、`IaihubToolHandler.java`（+6 handler 方法 + 注入 KnowledgeBaseService + 新增内部 DTO 类）
- **依赖**：无新增外部依赖，复用现有 `KnowledgeBaseService`、`RagApiClient`、`UserService`
- **MCP 协议**：工具总数从 11 增至 17，serverInfo 版本号可从 2.0.0 升至 2.1.0
- **安全**：写操作沿用现有 username/password 内联认证模式，与 tool_create/post_create 等工具一致
- **前端**：无影响，MCP 工具变更不涉及前端代码
