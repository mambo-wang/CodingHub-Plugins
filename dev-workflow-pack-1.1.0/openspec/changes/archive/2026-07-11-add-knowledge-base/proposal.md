## 为什么（Why）

CodingHub 目前缺少基于向量检索的知识库能力。用户无法将文档组织成可语义搜索的知识库，也无法基于知识库内容进行精准问答。RAG 服务（wandering-rag-mcp）已作为独立 Python 服务就绪，提供完整的 REST API（collection CRUD、文档管理、语义搜索、参数配置），但尚未与 CodingHub 集成。本次变更将 RAG 能力接入 CodingHub 平台，让用户可以在统一界面中创建、管理和使用知识库。

## 变更内容（What Changes）

- **新增**：知识库管理模块（后端 Java + 前端 Vue），采用混合模式——MySQL 存储元数据和所有权，Java 后端中转代理 RAG Python 服务 API
- **新增**：知识库 CRUD（创建/查看/编辑/删除），登录用户可创建，未登录用户可浏览
- **新增**：文档管理（上传/删除/列表），支持文本文件和二进制文档（PDF/DOCX/PPTX/XLSX）
- **新增**：知识库参数配置（chunk_mode/chunk_size/chunk_overlap/rerank），创建时可选高级配置，后续可修改
- **新增**：基于知识库的语义搜索问答（返回搜索片段，非对话式）
- **新增**：前端三个页面——知识库列表页、知识库详情页（含搜索+文档列表+配置）、知识库创建/编辑页
- **新增**：Java 后端引入 `java.net.http.HttpClient` 作为首个 HTTP 客户端，用于调用 RAG 服务
- **修改**：SecurityConfig 新增知识库端点的权限规则（GET 公开，POST/PUT/DELETE 需认证）
- **修改**：前端路由和导航新增知识库入口

## 能力清单（Capabilities）

### 新增能力（New Capabilities）

- `knowledge-base-crud`: 知识库的创建、查看、编辑、删除。MySQL 存储元数据（name/description/ownerId/rag_collection/status），RAG collection 名直接使用用户输入的知识库名称（Java 层查重返回 409）。
- `knowledge-document`: 文档上传、删除、列表管理。Java 接收 multipart 文件后转发至 RAG ingest API，MySQL 记录文档元数据。
- `knowledge-config`: 知识库参数配置（chunk_mode/chunk_size/chunk_overlap/rerank），创建时可设置默认值，后续可修改。前端高级配置区域可折叠。
- `knowledge-search`: 基于知识库的语义搜索问答。调用 RAG search API 返回文本片段（chunk 文本 + 来源文档 + 相关度分数），非对话式。
- `knowledge-frontend`: 前端页面与交互——知识库列表页（KnowledgeListPage）、知识库详情页（KnowledgeDetailPage，含搜索/文档列表/配置面板）、知识库编辑页（KnowledgeEditorPage）。

### 修改能力（Modified Capabilities）

- `frontend`: 路由配置新增知识库相关路由（/knowledge、/knowledge/:id、/knowledge/create、/knowledge/:id/manage），AppHeader 导航新增"知识库"入口。
- `auth`: SecurityConfig 新增知识库 API 端点的权限配置（GET /knowledge/** 公开，POST/PUT/DELETE 需认证 + owner 校验）。

## 影响范围（Impact）

- **后端代码**：新增 `model/kb/`（KnowledgeBase、KbDocument 实体）、`repository/kb/`、`service/kb/`（KnowledgeBaseService）、`controller/kb/`（KnowledgeBaseController）、`dto/kb/`、`config/RagClientConfig`（HTTP 客户端配置）、`service/RagApiClient`（RAG HTTP 代理层）
- **数据库**：新增 `knowledge_base` 表和 `kb_document` 表（JPA ddl-auto: update 自动建表）
- **前端代码**：新增 `pages/knowledge/`（3 个页面）、`components/knowledge/`（5-6 个组件）、`services/knowledge.ts`、`types/knowledge.ts`，修改 `router/index.ts` 和 `AppHeader.vue`
- **外部依赖**：Java 后端首次引入 HTTP 客户端（`java.net.http.HttpClient`，JDK 内置无额外依赖）；运行时依赖 RAG Python 服务（需独立启动在 localhost:8000）
- **配置**：`application.yml` 新增 `app.rag.base-url` 配置项
- **API**：新增 `/api/v1/knowledge/**` 系列端点（约 10 个）
