## 1. RAG 服务端：文件下载 API

- [x] 1.1 在 `rag-mcp/core/service.py` 中新增 `download_document(filepath, collection)` 方法，校验 filepath 在 `_uploads/{collection}/` 下（防路径遍历），返回文件绝对路径或抛出异常
- [x] 1.2 在 `rag-mcp/api/app.py` 中新增路由 `GET /api/collections/{name}/documents/download`，接收 query param `filepath`，调用 `service.download_document()`，返回 `FileResponse`（Content-Type: application/octet-stream, Content-Disposition: attachment）
- [x] 1.3 处理异常：filepath 缺失返回 400、路径遍历返回 403、文件不存在返回 404

## 2. RAG 服务端：文本文件上传时保存原文件

- [x] 2.1 修改 `rag-mcp/core/service.py` 的 `ingest_content()` 函数，在分块前将原始文本内容写入 `data/_uploads/{collection}/{filename}`
- [x] 2.2 确保重复上传同名文件时覆盖旧文件（与现有幂等逻辑一致）

## 3. RAG 服务端单元测试

- [x] 3.1 为 `download_document` 编写测试：正常下载、路径遍历攻击、文件不存在、filepath 缺失
- [x] 3.2 为修改后的 `ingest_content` 编写测试：验证文本文件被写入 `_uploads/` 目录
- [x] 3.3 运行 `cd rag-mcp && python -m pytest tests/ -v` 确认全部通过

## 4. 前端：搜索结果 Markdown 渲染

- [x] 4.1 在 `KnowledgeSearch.vue` 中引入 `markdown-it` 和 `highlight.js`，创建局部 md 实例（`html: false`，启用 highlight）
- [x] 4.2 将 `<p class="result-text">{{ result.text }}</p>` 改为 `<div class="result-text markdown-body" v-html="renderMarkdown(result.text)"></div>`
- [x] 4.3 添加 `renderMarkdown` 方法，调用 `md.render(text)` 并处理可能的渲染异常
- [x] 4.4 在 `<style scoped>` 中添加 `.result-text` 内 Markdown 元素的样式（h1-h6、code、pre、table、blockquote、ul/ol），确保双主题（暗色/亮色）样式正确

## 5. 前端：文档列表下载按钮

- [x] 5.1 在 `DocumentList.vue` 的每个文档项中，在删除按钮前添加下载按钮（使用 Lucide `Download` 图标）
- [x] 5.2 实现 `handleDownload(filepath, filename)` 方法：构造下载 URL `${props.ragBaseUrl}/api/collections/${props.ragCollection}/documents/download?filepath=${encodeURIComponent(filepath)}`，通过创建 `<a>` 标签触发下载
- [x] 5.3 下载按钮状态控制：仅当 `doc.status === 'READY'` 时启用，其他状态（UPLOADING/CONVERTING/CHUNKING/EMBEDDING/FAILED）设为 disabled
- [x] 5.4 处理下载失败（文件不存在 404）：显示友好提示

## 6. 前端：Vite 代理修复

- [x] 6.1 修改 `vite.config.ts` 中 `/rag` proxy 的 target 从 `http://172.53.3.98:8000` 改为 `http://localhost:8000`
- [x] 6.2 支持通过环境变量 `RAG_PORT` 覆盖 RAG 服务端口（默认 8000）

## 7. 集成验证

- [x] 7.1 手动验证：启动 RAG 服务，上传文本文件后通过下载接口下载成功
- [x] 7.2 手动验证：上传二进制文件（PDF/DOCX）后下载成功
- [x] 7.3 手动验证：搜索知识库，结果以 Markdown 格式正确渲染（标题、代码块、列表、表格）
- [x] 7.4 手动验证：暗色/亮色主题切换后搜索结果和文档列表样式正确
- [x] 7.5 手动验证：`npm run dev` 下文档列表、上传、删除、下载均正常工作
