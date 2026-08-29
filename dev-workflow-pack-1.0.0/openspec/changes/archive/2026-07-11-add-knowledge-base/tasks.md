## 1. 后端基础设施

- [x] 1.1 创建 kb 模块目录结构：`model/kb/`、`repository/kb/`、`service/kb/`、`controller/kb/`、`dto/kb/`
- [x] 1.2 创建 `KbStatus` 枚举（NORMAL, DELETED）
- [x] 1.3 创建 `KnowledgeBase` 实体类（id, name, description, ownerId, ragCollection, status, createdAt, updatedAt），使用 Lombok + JPA 注解
- [x] 1.4 创建 `KbDocument` 实体类（id, kbId, uploaderId, originalName, fileSize, chunkCount, chunkMode, status, createdAt, updatedAt）
- [x] 1.5 创建 `KnowledgeBaseRepository`（findByStatus + Pageable, findByNameAndStatus, existsByNameAndStatus）
- [x] 1.6 创建 `KbDocumentRepository`（findByKbIdAndStatus + Pageable, findByIdAndKbIdAndStatus）
- [x] 1.7 在 `application.yml` 中添加 `app.rag.base-url: http://localhost:8000` 配置项
- [x] 1.8 创建 `RagClientConfig` 配置类，注册 `java.net.http.HttpClient` bean（10s 连接超时）

## 2. RAG API 客户端

- [x] 2.1 创建 `RagApiClient` service 类，注入 HttpClient 和 baseUrl
- [x] 2.2 实现 `configureCollection(name, config)` — PUT /api/collections/{name}/config
- [x] 2.3 实现 `getCollectionConfig(name)` — GET /api/collections/{name}/config
- [x] 2.4 实现 `deleteCollection(name)` — DELETE /api/collections/{name}
- [x] 2.5 实现 `uploadDocument(collection, file, chunkSize, chunkMode)` — POST /api/collections/{name}/documents（multipart 转发）
- [x] 2.6 实现 `deleteDocument(collection, filepath)` — DELETE /api/collections/{name}/documents
- [x] 2.7 实现 `search(collection, query, topK, rerank)` — POST /api/collections/{name}/search
- [ ] 2.8 为 RagApiClient 编写单元测试（Mock HttpClient，验证请求构造和响应解析）

## 3. DTO 定义

- [x] 3.1 创建 `KbCreateRequest`（name, description, chunkMode, chunkSize, chunkOverlap, rerank），含 Jakarta 校验注解
- [x] 3.2 创建 `KbUpdateRequest`（name, description）
- [x] 3.3 创建 `KbConfigRequest`（chunkMode, chunkSize, chunkOverlap, rerank, description）
- [x] 3.4 创建 `KbSearchRequest`（query, topK, rerank, expandContext）
- [x] 3.5 创建 `KbResponse`（id, name, description, ownerId, ownerNickname, documentCount, createdAt）
- [x] 3.6 创建 `KbDocumentResponse`（id, kbId, originalName, fileSize, chunkCount, chunkMode, uploaderNickname, createdAt）
- [x] 3.7 创建 `KbSearchResultResponse`（text, source, score, chunkIndex）

## 4. Service 层实现

- [x] 4.1 创建 `KnowledgeBaseService`，注入 KnowledgeBaseRepository, KbDocumentRepository, UserRepository, RagApiClient
- [x] 4.2 实现 `listKnowledgeBases(page, size, sortBy)` — 分页查询，hot 模式按 score 排序，latest 按 createdAt DESC
- [x] 4.3 实现 `getKnowledgeBase(id)` — 查询单个知识库详情，组装 ownerNickname 和 documentCount
- [x] 4.4 实现 `createKnowledgeBase(request, user)` — 查重(409) → MySQL INSERT → RAG PUT /config → 返回
- [x] 4.5 实现 `updateKnowledgeBase(id, request, user)` — owner/admin 校验 → MySQL UPDATE → 同步 RAG description
- [x] 4.6 实现 `deleteKnowledgeBase(id, user)` — owner/admin 校验 → MySQL 软删除 → RAG DELETE collection
- [x] 4.7 实现 `listDocuments(kbId)` — 查询知识库下所有 NORMAL 文档
- [x] 4.8 实现 `uploadDocument(kbId, file, user)` — owner 校验 → RAG 上传 → MySQL INSERT kb_document
- [x] 4.9 实现 `deleteDocument(kbId, docId, user)` — owner/admin 校验 → MySQL 软删除 → RAG DELETE document
- [x] 4.10 实现 `search(kbId, request)` — 查询知识库 → RAG search → 返回结果列表
- [x] 4.11 实现 `getConfig(kbId)` — 查询知识库 → RAG GET config
- [x] 4.12 实现 `updateConfig(kbId, request, user)` — owner/admin 校验 → RAG PUT config → 同步 MySQL description
- [ ] 4.13 为 KnowledgeBaseService 编写单元测试（Mock repositories 和 RagApiClient，覆盖所有 Scenario：正常创建、重名409、非owner 403、RAG不可用503）

## 5. Controller 层

- [x] 5.1 创建 `KnowledgeBaseController`，@RequestMapping("/api/v1/knowledge")
- [x] 5.2 实现 GET / — listKnowledgeBases（公开）
- [x] 5.3 实现 GET /{id} — getKnowledgeBase（公开）
- [x] 5.4 实现 POST / — createKnowledgeBase（@AuthenticationPrincipal，登录）
- [x] 5.5 实现 PUT /{id} — updateKnowledgeBase（owner/admin）
- [x] 5.6 实现 DELETE /{id} — deleteKnowledgeBase（owner/admin）
- [x] 5.7 实现 GET /{id}/documents — listDocuments（公开）
- [x] 5.8 实现 POST /{id}/documents — uploadDocument（owner，multipart）
- [x] 5.9 实现 DELETE /{id}/documents/{docId} — deleteDocument（owner/admin）
- [x] 5.10 实现 POST /{id}/search — search（公开）
- [x] 5.11 实现 GET /{id}/config — getConfig（公开）
- [x] 5.12 实现 PUT /{id}/config — updateConfig（owner/admin）
- [ ] 5.13 为 KnowledgeBaseController 编写单元测试（MockMvc，验证端点权限：公开/认证/owner）

## 6. 安全配置

- [x] 6.1 在 SecurityConfig 中添加知识库 GET 端点到 permitAll 列表（/api/v1/knowledge, /api/v1/knowledge/{id}, /api/v1/knowledge/{id}/documents, /api/v1/knowledge/{id}/config）
- [x] 6.2 在 SecurityConfig 中添加 POST /api/v1/knowledge/{id}/search 到 permitAll 列表
- [x] 6.3 验证 POST/PUT/DELETE 端点默认需要认证（不加入 permitAll 即受保护）

## 7. 后端集成验证

- [ ] 7.1 启动后端，验证 JPA 自动建表（knowledge_base, kb_document）
- [ ] 7.2 手动测试创建知识库流程（POST + RAG 配置初始化）
- [ ] 7.3 手动测试文档上传流程（multipart → RAG → MySQL 记录）
- [ ] 7.4 手动测试语义搜索流程（POST search → RAG search → 返回结果）
- [ ] 7.5 运行全部单元测试：`cd backend && ./gradlew test`，确认全部通过

## 8. 前端类型与服务

- [x] 8.1 创建 `frontend/src/types/knowledge.ts`：KnowledgeBase, KbDocument, KbConfig, KbSearchResult, KbCreateRequest, KbSearchRequest 等 TypeScript 类型
- [x] 8.2 创建 `frontend/src/services/knowledge.ts`：封装所有知识库 API 调用（使用共享 api 实例或独立 axios 实例）

## 9. 前端页面 — 知识库列表

- [x] 9.1 创建 `KnowledgeCard.vue` 组件（glass-card 样式，显示名称/描述/作者/文档数/日期）
- [x] 9.2 创建 `KnowledgeListPage.vue`：GeneralizedSidebar + SortTab + 卡片网格 + 分页加载 + 空状态
- [x] 9.3 侧栏导航项：全部知识库、我的知识库（requiresAuth）
- [x] 9.4 已登录时顶部显示"创建知识库"按钮

## 10. 前端页面 — 知识库详情

- [x] 10.1 创建 `KnowledgeDetailPage.vue`：返回按钮 + 标题卡片 + 作者/日期/统计信息
- [x] 10.2 创建 `KnowledgeSearch.vue` 组件：搜索输入框 + 搜索结果卡片列表（来源文档名 + chunk 文本 + 相关度）
- [x] 10.3 创建 `DocumentList.vue` 组件：文档列表 + 删除按钮（owner 可见）
- [x] 10.4 创建 `DocumentUpload.vue` 组件：拖拽/点击上传区域 + 上传进度 + 成功/错误状态
- [x] 10.5 创建 `ConfigPanel.vue` 组件：可折叠配置面板（chunkMode/chunkSize/chunkOverlap/rerank 表单）
- [x] 10.6 详情页整合：搜索区 + Tab 切换（文档管理 / 配置）+ 编辑/删除按钮（owner 可见）

## 11. 前端页面 — 创建/编辑

- [x] 11.1 创建 `KnowledgeEditorPage.vue`：名称输入 + 描述文本框 + 可折叠高级配置 + 创建/取消按钮
- [x] 11.2 高级配置区域：chunkMode 下拉选择、chunkSize/chunkOverlap 数字输入、rerank 开关
- [x] 11.3 编辑模式：回填已有数据，提交后跳转回详情页
- [x] 11.4 创建名称冲突时显示 409 错误提示

## 12. 路由与导航

- [x] 12.1 在 `router/index.ts` 中添加知识库路由：/knowledge (公开), /knowledge/create (requiresAuth), /knowledge/:id (公开), /knowledge/:id/edit (requiresAuth)
- [x] 12.2 在 `AppHeader.vue` 导航链接中添加"知识库"入口
- [x] 12.3 验证路由守卫：未登录访问 /knowledge/create 重定向到登录页

## 13. 前端集成验证

- [x] 13.1 启动前端开发服务器，验证所有知识库页面正常渲染
- [x] 13.2 验证暗色/亮色双主题下知识库页面样式正确
- [x] 13.3 验证响应式布局（768px/1024px 断点）
- [x] 13.4 端到端测试：创建知识库 → 上传文档 → 搜索 → 修改配置 → 删除
