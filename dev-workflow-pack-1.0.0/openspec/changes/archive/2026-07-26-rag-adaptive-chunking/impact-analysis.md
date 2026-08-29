# Impact Analysis

> 基于 `design.md` 中的文件/类清单执行影响范围分析。
>
> **触发条件**：design.md 涉及修改现有代码（chunker.py / vector_store.py / service.py / app.py / server.py / 前端知识库页面）。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | 3 | `rag/core/profiler.py`, `rag/core/validator.py`, `frontend/src/components/knowledge/ChunkingPreviewPanel.vue` |
| 修改 | 7 | `rag/core/chunker.py`, `rag/core/vector_store.py`, `rag/core/service.py`, `rag/api/app.py`, `rag/server.py`, `frontend/src/pages/knowledge/KnowledgeBaseDetailPage.vue`, `frontend/src/services/knowledge.ts` |
| 删除 | 0 | — |

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 被修改模块 | 调用方 | 位置 | 风险等级 |
|-----------|--------|------|----------|
| `chunker.chunk_text()` | `service.ingest_file()` | `rag/core/service.py` | L1 |
| `chunker.structural_chunk_text()` | `service.ingest_file()` | `rag/core/service.py` | L1 |
| `chunker.semantic_chunk_text()` | `service.ingest_file()` | `rag/core/service.py` | L1 |
| `vector_store.insert()` | `service.ingest_file()` | `rag/core/service.py` | L1 |
| `vector_store.query()` | `service.search()` | `rag/core/service.py` | L1 |
| `service.ingest_file()` | MCP `ingest_file` tool | `rag/server.py` | L1 |
| `service.ingest_directory()` | MCP `ingest_directory` tool | `rag/server.py` | L1 |
| `service.search()` | MCP `search` tool | `rag/server.py` | L1 |
| `service.search()` | REST `POST /search` | `rag/api/app.py` | L1 |
| REST API routes | 前端 `knowledge.ts` | `frontend/src/services/` | L0 |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

```
chunker.chunk_text() / structural_chunk_text()
  ├── service.ingest_file()
  │     ├── MCP ingest_file tool (server.py)
  │     ├── MCP ingest_directory tool (server.py) → 循环调用 ingest_file
  │     ├── REST POST /collections/{name}/documents (app.py)
  │     └── REST POST /collections/{name}/documents/batch (app.py) → async_engine
  └── service.ingest_directory()
        └── MCP ingest_directory tool (server.py)

vector_store.insert()
  └── service.ingest_file()
        └── (同上)

vector_store.query()
  └── service.search()
        ├── MCP search tool (server.py)
        └── REST POST /collections/{name}/search (app.py)
              └── 前端 KnowledgeSearchPage.vue
```

### 2.3 反向调用图（被谁调用）

```
[chunker.py 切分函数]
  ├── [service.ingest_file] (rag/core/service.py)
  │     ├── [MCP ingest_file] (rag/server.py)
  │     ├── [MCP ingest_directory] (rag/server.py)
  │     ├── [REST single upload] (rag/api/app.py)
  │     └── [REST batch upload] (rag/api/app.py → async_engine.py)
  └── [无其他调用方]

[vector_store.py schema]
  ├── [service.ingest_file] → insert
  ├── [service.search] → query
  ├── [service.delete_document] → delete
  └── [service.list_documents] → fetch metadata
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `zvec` Python 包 (≥0.5.0) | 向量存储引擎 + 原生 FTS | L1（schema 新增字段 + FtsIndexParam 需 v0.5.0+；旧版本无 MultiQuery API） |
| `core/embeddings.py` | Embedding 模型 | L0（接口不变，仅输入文本变长） |
| `core/reranker.py` | Reranker 模型 | L0（不受影响） |
| `core/database.py` | SQLite 状态追踪 | L0（不受影响） |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| MCP search tool 返回结构 | 新增 `context_header` 字段（向后兼容，旧客户端忽略） |
| REST search 响应 | 新增 `context_header` 字段 |
| 前端知识库搜索展示 | 可选展示 context_header 作为来源标注 |
| 前端知识库设置页 | 新增 strategy 选择器 + 分片预览面板 |
| Java 后端 KnowledgeController | 不受影响（Java 后端仅做 KB CRUD 代理，不直接调 RAG 切分） |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| RAG 服务无现有单元测试框架 | — | 需新建 | 新增 `rag/tests/test_chunker.py` 覆盖 protected patterns / validator / profiler |
| 前端无现有知识库组件测试 | — | 需新建 | 可选：ChunkingPreviewPanel 组件测试 |

> 注：CodingHub 既有测试失败 9 个（ToolFileControllerTest 等），均为 Java 后端，与本次 RAG Python 改动无关。

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L0** | 纯新增（profiler.py, validator.py, 前端组件） | 无 |
| **L1** | 修改 chunker.py 切分逻辑 / vector_store.py schema | 新增字段向后兼容；旧 collection 无 strategy 字段时保持 structural 默认行为 |
| **L2** | 无 | — |

**本次改动风险等级**: L1

关键风险点：
- zvec `coll.insert()` 新增 `context_header` 字段：需验证 zvec 是否支持动态 schema（已有 text/source/chunk_index 字段，新增 STRING 字段应兼容）
- 旧数据无 context_header 字段：`coll.fetch()` 返回时该字段为空/缺失，需在 service.py 中做 `.get("context_header", "")` 防御
- zvec FTS 版本门槛：`FtsIndexParam` 和 `MultiQuery` 为 v0.5.0+ 新增 API，当前环境需 `pip show zvec` 确认版本；若版本不足需升级
- 旧 collection 无 FTS 索引：已有 collection 的 text 字段未建 FTS 索引，`MultiQuery` 的 fts 分支可能报错 → 需 try/except 降级为纯 ANN 检索

---

## 6. 层级依赖校验 (Layer Dependency Check)

> 本次改动在 RAG Python 服务内部，不涉及 Java 后端分层。

RAG 服务内部层级：
```
server.py (MCP tools) / api/app.py (REST) → core/service.py → core/chunker.py + core/vector_store.py
```

新增 `profiler.py` 和 `validator.py` 被 `chunker.py` 或 `service.py` 调用，不引入循环依赖。

**结果**: PASS（单向依赖保持）

---

## 7. 回归测试建议 (Regression Suggestions)

- [ ] `test_chunker.py::test_protected_patterns` — 验证图片/链接/公式/表格/代码块不被切断
- [ ] `test_chunker.py::test_validator_fallback` — 验证碎片化文档自动降级到 recursive
- [ ] `test_chunker.py::test_context_header` — 验证 structural 模式生成正确面包屑
- [ ] `test_chunker.py::test_auto_profiler` — 验证不同文档类型选择正确策略
- [ ] `test_chunker.py::test_backward_compat` — 验证无 strategy 字段时默认 structural 行为不变
- [ ] `test_hybrid_search.py::test_multiquery_rrf` — 验证新 collection 的 MultiQuery RRF 融合排序正确
- [ ] `test_hybrid_search.py::test_fts_degradation` — 验证旧 collection（无 FTS 索引）降级为纯 ANN 不报错
- [ ] 手动验证：已有 collection 重新 search 结果不变（旧数据无 context_header 不影响 ANN）
- [ ] 手动验证：前端知识库设置页 strategy 选择器 + 预览面板正常工作

---

## 8. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方
- [x] 已列出上游/下游依赖
- [x] 已评估风险等级（L1）
- [x] 层级依赖校验通过（RAG 内部单向）
- [x] 已列出回归测试清单
- [ ] zvec 动态 schema 兼容性需实际验证（实施时确认）

---

**生成工具**: 手动代码追踪（CodeGraph MCP 仅索引 Java 后端，RAG Python 服务未被索引）
**生成时间**: 2026-07-22
**基础**: openspec/changes/rag-adaptive-chunking/proposal.md + design.md
