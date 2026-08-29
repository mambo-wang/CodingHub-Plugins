## 1. Protected Patterns 保护区域机制

- [x] 1.1 在 `rag/core/chunker.py` 中新增 `protected_spans(text)` 函数：6 组正则预扫描（LaTeX 块公式、MD 图片、MD 链接、表格头+分隔行、表格数据行、围栏代码块），返回排序后的 byte offset span 列表，重叠取最长
- [x] 1.2 新增 `build_units_with_protection(text, protected, separators, chunk_size)` 函数：将文本拆为 splitUnit 列表，保护区域作为原子单元，非保护区域按分隔符优先级递归切分
- [x] 1.3 修改 `_recursive_split()` 和 `_merge_and_split_blocks()`：在切分前调用 protected_spans，切分时跳过保护区；超大保护区域（>7500 字符）在换行/空格处强制切分
- [x] 1.4 确保 semantic 模式（`semantic_chunk_text`）不调用保护扫描（保持现有逻辑不变）
- [x] 1.5 单元测试：新建 `rag/tests/test_protected_patterns.py`，覆盖 spec 中 4 个场景（图片不切断、公式不切断、代码块不切断、表格行不切断）+ 超大保护区域强制切分 + semantic 跳过

## 2. Chunk Validator 质量验证与降级

- [x] 2.1 新建 `rag/core/validator.py`：实现 `validate_chunks(chunks, total_chars, chunk_size)` 函数，5 条规则（非空、大文档非单 chunk、碎片率≤25%、超大 chunk≤2x、非全碎片），返回 `ValidationResult(ok, reason)`
- [x] 2.2 在 `rag/core/chunker.py` 中新增 `chunk_with_validation(text, filepath, mode, chunk_size, chunk_overlap)` 入口函数：执行切分 → 验证 → 不合格且 mode=="structural" 时降级到 recursive → 日志记录降级事件
- [x] 2.3 semantic 模式验证失败时不降级，仅日志记录，仍返回原结果
- [x] 2.4 单元测试：新建 `rag/tests/test_validator.py`，覆盖 5 条规则的通过/失败场景 + structural→recursive 降级 + semantic 不降级

## 3. ContextHeader 分离

- [x] 3.1 修改 `rag/core/chunker.py` 的 `Chunk` dataclass：新增 `context_header: str = ""` 字段
- [x] 3.2 修改 `structural_chunk_text()`：标题面包屑存入 `context_header` 字段而非拼入 `text`；新增 `embedding_content(chunk)` 辅助函数返回 `header + "\n\n" + content`（header 为空时直接返回 content）
- [x] 3.3 修改 `rag/core/vector_store.py`：zvec schema 新增 `context_header` STRING 字段；`insert()` 时写入；`query()` 返回时携带
- [x] 3.4 修改 `rag/core/service.py`：`ingest_file()` 中 embedding 输入改为 `embedding_content(chunk)`；`search()` 返回结果携带 `context_header`；对旧数据 `.get("context_header", "")` 防御
- [x] 3.5 修改 `rag/core/service.py`：collection config 新增 `context_header: bool = True` 开关，关闭时不生成面包屑
- [x] 3.6 单元测试：新建 `rag/tests/test_context_header.py`，覆盖 structural 模式生成正确面包屑 + 空 header 时 embedding_content 返回纯 content + context_header=false 时不生成

## 4. zvec FTS 混合检索（BM25 + ANN + RRF）

- [x] 4.1 验证 zvec 版本 ≥ 0.5.0：`pip show zvec`，不足则 `pip install --upgrade zvec`；确认 `FtsIndexParam` 和 `MultiQuery` 可导入
- [x] 4.2 修改 `rag/core/vector_store.py` 的 collection 创建逻辑：text 字段附加 `FtsIndexParam(field_name="text")`，新建 collection 自动启用 FTS 索引
- [x] 4.3 修改 `rag/core/vector_store.py` 的 `query()` 方法：接受 `query_text` 参数，构造 `MultiQuery(vector_query=embedding, fts_query=query_text, fusion="rrf", limit=top_k)` 替代纯 ANN 检索；FTS 不可用时（旧 collection）降级为纯向量检索
- [x] 4.4 修改 `rag/core/service.py` 的 `search()` 方法：将用户原始 query 文本传递给 `vector_store.query(query_text=...)`，使 FTS 分支可用
- [x] 4.5 新增 FTS 索引补建工具函数 `rebuild_fts_index(collection_name)`：对已有 collection 调用 `coll.create_index` 补建 FTS 索引（无需重新 embedding）
- [x] 4.6 单元测试：新建 `rag/tests/test_hybrid_search.py`，覆盖：新 collection 同时走 ANN+FTS、旧 collection 降级纯 ANN、MultiQuery RRF 融合结果排序正确、空 query_text 时退化为纯 ANN

## 5. Auto Profiler 自动策略选择

- [x] 5.1 新建 `rag/core/profiler.py`：实现 `profile_document(text)` 单遍扫描（heading_count、heading_density、code_ratio、has_tables、total_chars）+ `select_strategy(profile)` 按优先级返回策略名
- [x] 5.2 修改 `rag/core/service.py` 的 `ingest_file()`：当 collection config 的 strategy 为 "auto" 或缺失时，调用 profiler 选择策略；旧 collection 无 strategy 字段视为 "structural"（向后兼容）
- [x] 5.3 修改 `rag/core/service.py`：collection config 新增 `strategy: str = "auto"` 字段，持久化到 `_config.json`
- [x] 5.4 单元测试：新建 `rag/tests/test_profiler.py`，覆盖 MD 文档→structural、纯代码→structural、纯文本无结构→recursive、极短文本→recursive、用户显式指定覆盖 auto

## 6. REST API 分片预览端点

- [x] 6.1 在 `rag/api/app.py` 新增 `POST /api/collections/{name}/chunking/preview` 路由：接收 text/strategy/chunk_size/chunk_overlap，调用 chunker 切分（不写 DB、不调 embedding），返回 chunks + stats + profile
- [x] 6.2 输入校验：text 非空且 ≤64KB；strategy 为 "semantic" 时返回 400（preview 不支持 semantic）
- [x] 6.3 修改 `rag/api/app.py` 的 `GET /collections/{name}/documents` 响应：新增 chunk_count / strategy / status 字段（从 _registry.json 和 database.py 读取）
- [x] 6.4 修改 `rag/api/app.py` 的 `PUT /collections/{name}/config`：支持 strategy 和 context_header 字段更新

## 7. MCP 工具扩展

- [x] 7.1 修改 `rag/server.py` 的 `configure_collection` 工具：接受 strategy 和 context_header 参数
- [x] 7.2 修改 `rag/server.py` 的 `search` 工具返回结构：结果中携带 context_header 字段（向后兼容，旧客户端忽略）
- [x] 7.3 修改 `rag/server.py` 的 `get_collection_config` 工具：返回 strategy 和 context_header 字段

## 8. 前端分片预览面板

- [x] 8.1 新建 `frontend/src/components/knowledge/ChunkingPreviewPanel.vue`：文本输入区 + 策略选择器 + chunk_size/overlap 输入 + 运行按钮 + 结果展示（策略徽章 + 统计条 + chunk 卡片列表），遵循 design-system.md 双主题规范
- [x] 8.2 新建 `frontend/src/components/knowledge/ChunkCard.vue`：单 chunk 卡片（序号、字符数、context_header 标签、内容 3 行截断、点击展开）
- [x] 8.3 新建 `frontend/src/components/knowledge/StrategyBadge.vue`：策略颜色编码徽章（auto=紫、structural=青、recursive=灰）
- [x] 8.4 在 `frontend/src/services/knowledge.ts` 新增 `previewChunking(collection, text, strategy, chunkSize, overlap)` API 调用函数（直连 RAG :8000）

## 9. 前端知识库页面增强

- [x] 9.1 修改知识库设置页（`KnowledgeBaseDetailPage.vue` 或对应设置组件）：新增策略选择器（auto/structural/recursive）+ 集成 ChunkingPreviewPanel 折叠面板
- [x] 9.2 修改文档列表组件：新增 Chunks 列（chunk_count）、策略列（StrategyBadge）、状态列（ready/processing/failed 图标）
- [x] 9.3 策略变更保存调用 `PUT /api/collections/{name}/config`，提示"新上传文档将使用新策略"

## 10. 集成验证

- [x] 10.1 端到端测试：上传一个包含图片/链接/代码块/表格的 Markdown 文件，验证切分结果中保护区域完整、context_header 正确、strategy 自动选择为 structural
- [x] 10.2 向后兼容测试：对已有 collection（无 strategy 字段）执行 ingest 和 search，验证行为与变更前一致
- [x] 10.3 前端验证：分片预览面板正常运行、文档列表正确展示 chunk 统计、双主题切换正常
- [x] 10.4 运行全部 RAG 测试：`cd rag && python -m pytest tests/ -v`，确认全部通过
- [x] 10.5 混合检索验证：新建 collection 后 ingest 文档，分别用关键词查询和语义查询验证 FTS+ANN 融合生效；对旧 collection 验证降级为纯 ANN 不报错

## 11. 受影响模块回归测试（基于 impact-analysis.md）

- [x] 11.1 验证 MCP search 工具返回结构向后兼容（新增 context_header 字段不影响旧客户端解析）— L1 风险
- [x] 11.2 验证 REST POST /search 响应向后兼容 — L1 风险
- [x] 11.3 验证 zvec 新增 context_header 字段后，旧 collection 的 query/fetch 不报错（字段缺失时返回空字符串）— L1 风险
- [x] 11.4 验证 batch upload 异步流程（async_engine.py）在新 chunker 逻辑下正常工作 — L1 风险
- [x] 11.5 验证 Java 后端 KnowledgeController 代理调用不受影响（不直接调 RAG 切分）— L0 风险，无需改动
- [x] 11.6 验证 zvec FTS 索引对旧 collection 的兼容性：无 FTS 索引时 MultiQuery 降级为纯 ANN，不抛异常 — L1 风险
