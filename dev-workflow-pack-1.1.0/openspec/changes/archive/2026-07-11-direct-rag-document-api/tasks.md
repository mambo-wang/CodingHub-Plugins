# Tasks: direct-rag-document-api

## 1. Java 后端 — KbResponse 增加 RAG URL 字段

- [x] 1.1 修改 `KbResponse.java`：新增 `ragBaseUrl`（String）和 `documentsUrl`（String）字段
- [x] 1.2 修改 `KnowledgeBaseService.toKbResponse()`：从 `app.rag.public-url` 读取 RAG 公共地址，拼接 `ragCollection` 生成 `documentsUrl`，注入到 KbResponse
- [x] 1.3 为 toKbResponse 新增字段编写单元测试（在 IaihubToolHandlerKbTest 中通过 mock KbResponse 验证）

## 2. Java 后端 — 删除文档代理端点和相关代码

- [x] 2.1 `KnowledgeBaseController.java`：删除 `uploadDocument`、`deleteDocument`、`listDocuments`、`getConfig`、`updateConfig` 方法（保留 search）
- [x] 2.2 `KnowledgeBaseService.java`：删除 `uploadDocument`、`deleteDocument`、`listDocuments`、`getConfig`、`updateConfig` 方法（保留 search）
- [x] 2.3 `RagApiClient.java`：删除 `uploadDocument`、`deleteDocument` 方法，保留 `configureCollection`、`getCollectionConfig`、`deleteCollection`、`search`
- [x] 2.4 `SecurityConfig.java`：删除 `/api/v1/knowledge/{id}/documents`、`/api/v1/knowledge/{id}/config` 相关安全规则（保留 search permitAll）
- [x] 2.5 更新 `IaihubToolHandler.java`：移除 handleKbUpdate 中对 updateConfig 的调用和 KbConfigRequest import
- [x] 2.6 更新 `IaihubToolHandlerKbTest.java`：移除已删除方法的测试用例（configParams、bothNameAndConfig），更新 uploadDocument 测试检查 RAG URL
- [x] 2.7 运行 `cd backend && gradlew test` 确认全部通过

## 3. Java MCP — kb_upload_document 返回 RAG 直传地址

- [x] 3.1 修改 `IaihubToolHandler.handleKbUploadDocument()`：uploadUrl 改为 `kb.getDocumentsUrl()`（RAG 直传地址），requiresAuth 改为 "无需认证"
- [x] 3.2 `KbUploadDocumentInfoResponse` 内部类：更新 curlExample 不携带 JWT header，更新 explanation 和 instruction
- [x] 3.3 更新 `IaihubToolHandlerKbTest.java` 中 handleKbUploadDocument 测试用例：验证返回 RAG URL 和"无需认证"
- [x] 3.4 运行 `cd backend && gradlew test` 确认全部通过

## 4. 前端 — knowledge service 改直连 RAG

- [x] 4.1 `types/knowledge.ts`：KnowledgeBase 类型新增 `ragBaseUrl` 和 `documentsUrl` 字段；新增 `RagDocument` 类型
- [x] 4.2 `services/knowledge.ts`：修改 `uploadDocument` 方法 — 接收 documentsUrl，用 axios 直传 RAG（无 JWT header）
- [x] 4.3 `services/knowledge.ts`：修改 `getDocuments` 方法 — 直连 RAG `GET documentsUrl`
- [x] 4.4 `services/knowledge.ts`：修改 `deleteDocument` 方法 — 直连 RAG `DELETE documentsUrl` with body `{filepath}`
- [x] 4.5 `services/knowledge.ts`：`search` 方法保持不变（经 Java 代理）
- [x] 4.6 `services/knowledge.ts`：修改 `getConfig` 和 `updateConfig` 方法 — 直连 RAG `GET/PUT /api/collections/{name}/config`
- [x] 4.7 前端 `npm run build` 验证编译通过

## 5. 前端 — 组件适配

- [x] 5.1 `DocumentList.vue`：props 改为 `documentsUrl`，使用 `RagDocument` 类型，模板适配 source/chunk_count
- [x] 5.2 `DocumentUpload.vue`：props 改为 `documentsUrl`，直传 RAG
- [x] 5.3 `ConfigPanel.vue`：props 改为 `ragBaseUrl` + `ragCollection`，直连 RAG 配置 API
- [x] 5.4 `KnowledgeDetailPage.vue`：传递 documentsUrl/ragBaseUrl/ragCollection 给子组件
- [x] 5.5 `KnowledgeEditorPage.vue`：适配 getConfig/updateConfig 新签名

## 6. 基础设施

- [x] 6.1 `nginx.conf`：新增 `/rag/` location 块，代理到 RAG 服务 `http://localhost:8000`
- [x] 6.2 `application.yml`：新增 `app.rag.public-url: /rag`，用于 KbResponse 中的前端可访问 URL
- [x] 6.3 前端 `npm run build` 验证通过
- [x] 6.4 后端 `gradlew test` 验证通过

## 7. 集成验证（待执行）

- [ ] 7.1 启动后端 + RAG + Nginx + 前端，创建新知识库
- [ ] 7.2 通过前端上传文档到知识库，确认直连 RAG（浏览器网络面板检查请求目标为 /rag/）
- [ ] 7.3 通过 MCP 客户端调用 `kb_upload_document`，确认返回 RAG 直传地址
- [ ] 7.4 通过 MCP 客户端调用 `kb_search`，确认搜索仍经 Java 代理正常工作
