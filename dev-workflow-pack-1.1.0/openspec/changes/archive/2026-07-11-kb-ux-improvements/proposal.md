## 为什么（Why）

知识库搜索页面当前以纯文本（`<p>{{ result.text }}</p>`）渲染检索结果，但 RAG 系统存储的 chunk 本身就是 Markdown 片段（所有文档上传时均经 markitdown 转换为 Markdown 后分块）。标题显示为 `# 第一章`、列表显示为 `- item` 原始符号、代码块无法高亮——严重浪费了已有的结构化信息。

同时，文档列表仅展示文件名、大小和状态，不支持下载源文件。用户上传后无法取回原始文件，当需要离线使用或备份时很不方便。此外，Vite 开发代理的 `/rag` target 指向了不可达的远程地址 `172.53.3.98:8000`，本地开发时所有 RAG 直连操作均失败。

## 变更内容（What Changes）

- **新增**：知识库搜索结果以 Markdown 格式渲染显示（复用项目已有的 markdown-it + highlight.js 技术栈）
- **新增**：知识库文档列表支持源文件下载，前端添加下载按钮，RAG 服务新增下载 API endpoint
- **修改**：RAG `ingest_content` 函数将文本文件原文件也保存到 `_uploads/` 目录，使所有类型文件均可下载（当前仅二进制文件 PDF/DOCX/PPTX/XLSX 保留了原文件）
- **修复**：Vite proxy `/rag` target 从不可达的 `172.53.3.98:8000` 改为 `localhost:8000`，支持环境变量配置
- **不涉及**：MCP 工具不需要支持文件下载功能

## 能力清单（Capabilities）

### 新增能力（New Capabilities）

- `kb-search-display`: 知识库检索结果 Markdown 渲染——将搜索结果从纯文本改为 markdown-it 渲染，支持标题、列表、代码块高亮等格式
- `kb-document-download`: 知识库文档源文件下载——RAG 服务新增下载 endpoint，前端文档列表添加下载按钮，支持所有文件类型

### 修改能力（Modified Capabilities）

（无现有规格级别的需求变更）

## 影响范围（Impact）

- **RAG 服务**（`rag-mcp/`）：`api/app.py` 新增下载路由，`core/service.py` 的 `ingest_content` 增加文件保存逻辑
- **前端**（`frontend/`）：`KnowledgeSearch.vue` 搜索结果改用 Markdown 渲染组件；`DocumentList.vue` 添加下载按钮；`vite.config.ts` 修复 proxy target；可能需要抽取通用 Markdown 渲染组件
- **后端**：`application.yml` 的 `app.rag.base-url` 需改为 `localhost:8000`（本地开发场景）
- **Nginx**：无需改动，已有 `/rag/` proxy_pass 配置
- **数据兼容**：已有的文本文件因未保存原文件而无法下载，需重新上传；二进制文件不受影响
