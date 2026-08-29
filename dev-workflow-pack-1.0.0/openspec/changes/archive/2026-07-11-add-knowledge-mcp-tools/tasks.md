# Tasks: 为 MCP Server 添加知识库工具

## 1. IaihubToolHandler — 新增 handler 方法与 DTO

- [x] 1.1 注入 `KnowledgeBaseService` 依赖
  - 构造函数新增 `KnowledgeBaseService knowledgeBaseService` 参数
  - 添加对应字段赋值

- [x] 1.2 实现 `handleKbList(int page, int size, String sortBy)` 方法
  - 调用 `knowledgeBaseService.listKnowledgeBases(page, size, sortBy)`
  - 返回分页结果（content、totalElements、totalPages、page、size）
  - 无需认证

- [x] 1.3 实现 `handleKbSearch(long kbId, String query, int topK, Boolean rerank, int expandContext)` 方法
  - 构建 `KbSearchRequest`，调用 `knowledgeBaseService.search(kbId, request)`
  - 返回搜索结果列表（text、source、score、chunkIndex）
  - 无需认证

- [x] 1.4 实现 `handleKbCreate(String name, String description, String chunkMode, Integer chunkSize, Integer chunkOverlap, Boolean rerank, String username, String password)` 方法
  - 使用 `userService.login()` 内联认证
  - 构建 `KbCreateRequest`，调用 `knowledgeBaseService.createKnowledgeBase(request, user)`
  - 返回 KbResponse

- [x] 1.5 实现 `handleKbUpdate(long kbId, String name, String description, String chunkMode, Integer chunkSize, Integer chunkOverlap, Boolean rerank, String username, String password)` 方法
  - 使用 `userService.login()` 内联认证
  - 构建 `User` 对象（含 role）
  - 如有 name 或 description 传入：构建 `KbUpdateRequest`，调用 `knowledgeBaseService.updateKnowledgeBase(kbId, request, user)`
  - 如有 chunkMode/chunkSize/chunkOverlap/rerank 传入：构建 `KbConfigRequest`，调用 `knowledgeBaseService.updateConfig(kbId, request, user)`
  - 返回更新后的 KbResponse

- [x] 1.6 实现 `handleKbDelete(long kbId, String username, String password)` 方法
  - 使用 `userService.login()` 内联认证
  - 构建 `User` 对象，调用 `knowledgeBaseService.deleteKnowledgeBase(kbId, user)`
  - 返回成功响应

- [x] 1.7 实现 `handleKbUploadDocument(long kbId)` 方法
  - 调用 `knowledgeBaseService.getKnowledgeBase(kbId)` 验证知识库存在
  - 返回 REST API 上传接口信息（URL、HTTP 方法、Content-Type、表单字段、限制）
  - 与 `handleToolFileUploadInfo` 模式一致
  - 注意：文档上传 REST API 路径为 `POST /api/v1/knowledge/{kbId}/documents`，需要 JWT 认证

- [x] 1.8 新增内部 DTO 类
  - `KbListResponse`：包含 knowledgeBases 列表、totalElements、totalPages、page、size
  - `KbSearchResponse`：包含 results 列表和 count
  - `KbUploadDocumentResponse`：包含 kbId、uploadUrl、method、contentType、fields、limits、requiresAuth

## 2. McpSdkServerConfig — 注册 6 个新工具

- [x] 2.1 注册 `h3_coding_hub_kb_list`
  - description: "获取知识库列表，支持分页和排序"
  - input schema: page(integer, 默认0), size(integer, 默认20), sortBy(string, 可选 "hot")
  - handler → `toolHandler.handleKbList(page, size, sortBy)`

- [x] 2.2 注册 `h3_coding_hub_kb_search`
  - description: "对指定知识库执行语义搜索，返回相关片段"
  - input schema: kbId(integer, 必填), query(string, 必填), topK(integer, 默认5), rerank(boolean, 可选), expandContext(integer, 默认0)
  - required: ["kbId", "query"]
  - handler → `toolHandler.handleKbSearch(kbId, query, topK, rerank, expandContext)`

- [x] 2.3 注册 `h3_coding_hub_kb_create`
  - description: "创建新知识库。需要传入账号密码进行认证"
  - input schema: name(string, 必填), description(string, 可选), chunkMode(string, 可选, 默认"structural"), chunkSize(integer, 可选, 默认800), chunkOverlap(integer, 可选, 默认50), rerank(boolean, 可选, 默认true), username(string, 必填), password(string, 必填, 默认123456)
  - required: ["name", "username", "password"]
  - handler → `toolHandler.handleKbCreate(...)`

- [x] 2.4 注册 `h3_coding_hub_kb_update`
  - description: "更新知识库，支持修改名称、描述和 RAG 配置参数。需要传入账号密码进行认证"
  - input schema: kbId(integer, 必填), name(string, 可选), description(string, 可选), chunkMode(string, 可选), chunkSize(integer, 可选), chunkOverlap(integer, 可选), rerank(boolean, 可选), username(string, 必填), password(string, 必填, 默认123456)
  - required: ["kbId", "username", "password"]
  - handler → `toolHandler.handleKbUpdate(...)`

- [x] 2.5 注册 `h3_coding_hub_kb_delete`
  - description: "删除知识库。需要传入账号密码进行认证"
  - input schema: kbId(integer, 必填), username(string, 必填), password(string, 必填, 默认123456)
  - required: ["kbId", "username", "password"]
  - handler → `toolHandler.handleKbDelete(...)`

- [x] 2.6 注册 `h3_coding_hub_kb_upload_document`
  - description: "获取知识库文档上传的 REST API 信息。客户端通过 HTTP multipart POST 直传文件"
  - input schema: kbId(integer, 必填)
  - required: ["kbId"]
  - handler → `toolHandler.handleKbUploadDocument(kbId)`

- [x] 2.7 更新日志信息
  - 将两处 `logger.info("...initialized with 11 tools")` 改为 `17 tools`

## 3. 单元测试

- [x] 3.1 编写 `IaihubToolHandlerKbTest` 测试类
  - 使用 `@ExtendWith(MockitoExtension.class)` mock `KnowledgeBaseService`、`UserService` 等依赖
  - 测试 `handleKbList`：验证默认参数调用、验证 sortBy="hot" 调用
  - 测试 `handleKbSearch`：验证成功搜索、验证知识库不存在时返回 isError=true
  - 测试 `handleKbCreate`：验证成功创建、验证认证失败时返回 isError=true
  - 测试 `handleKbUpdate`：验证成功更新名称/描述、验证成功更新 RAG 配置参数（chunkSize等）、验证非所有者返回 isError=true
  - 测试 `handleKbDelete`：验证成功删除、验证非所有者返回 isError=true
  - 测试 `handleKbUploadDocument`：验证返回上传信息、验证知识库不存在时返回 isError=true

## 4. 验证

- [x] 4.1 编译验证
  - 先停止 Spring Boot 进程
  - 执行 `gradlew build -x test`，确认编译通过无错误

- [x] 4.2 运行单元测试
  - 执行 `gradlew test --tests "*IaihubToolHandlerKbTest*"`，确认所有测试通过

- [x] 4.3 集成验证（手动）
  - 启动后端服务
  - 通过 MCP 客户端或 curl 调用 `tools/list`，确认 17 个工具全部注册
  - 调用 `h3_coding_hub_kb_list` 确认返回知识库列表
  - 调用 `h3_coding_hub_kb_create` 确认创建成功
  - 调用 `h3_coding_hub_kb_search` 确认搜索返回结果
