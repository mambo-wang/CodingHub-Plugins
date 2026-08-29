## 背景（Context）

CodingHub RAG 服务（`rag/core/chunker.py`）当前提供三种切片模式：recursive（递归字符切分）、semantic（embedding 相似度断点）、structural（Markdown 标题/代码块/表格边界）。用户通过 collection config 的 `chunk_mode` 手动选择。

通过对 WeKnora（腾讯开源，Go 实现，`internal/infrastructure/chunker/`）源码的深度分析，识别出四个可移植的核心机制：Protected Patterns（保护区域不切断）、Validator + Tier 降级（质量兜底）、ContextHeader 分离（embedding 上下文与原文位置解耦）、Auto Profiler（文档特征驱动策略选择）。

约束条件：
- RAG 服务为纯 Python 单进程，CPU-only 运行（i7-6700 VDI 环境）
- 不引入 LLM 依赖，保持"纯检索、零配置"设计哲学
- zvec 嵌入式向量库，schema 变更需考虑向后兼容
- 前端 Vue 3.4 + TypeScript，知识库页面已有基础 CRUD 和搜索展示

## 目标 / 非目标（Goals / Non-Goals）

**目标：**
- 切分质量：消除原子内容被切断的问题（图片/链接/公式/表格行/代码块）
- 质量兜底：任何模式下切出碎片时自动降级到 recursive，避免垃圾 chunk 进入向量库
- 上下文增强：embedding 时携带标题面包屑，提升跨 section 检索召回率
- 零配置体验：新文档 ingest 时自动选择最优策略，无需用户手动指定 chunk_mode
- 可观测性：前端提供分片预览调试面板，用户可直观看到切分效果

**非目标：**
- 不实现 Parent-Child 双层切片（现有 expand_context 邻居扩展已覆盖）
- 不实现 Heuristic Tier（form-feed/多语言章节标记——CodingHub 文档以 MD/代码为主）
- 不引入 GraphRAG / 知识图谱
- 不改变 MCP/REST 接口签名（仅扩展返回字段）
- 不改变 semantic 模式的 embedding 调用逻辑（CPU 上慢，保持为可选模式）

## 决策（Decisions）

### D1: Protected Patterns 实现方式

**选择**：正则预扫描 + span 标记，切分时跳过保护区

**备选方案**：
- A) 预扫描标记 span（WeKnora 方案）：先用 6 组正则找出所有保护区 byte offset，切分只在非保护区进行 ✓
- B)  tokenizer 级别保护：用 embedding model 的 tokenizer 做 token-aware 切分——过重，CPU 上不可接受
- C) 后处理修复：先切再检查是否切断了保护内容，切断了就回退——逻辑复杂且不可靠

**理由**：方案 A 是 WeKnora 验证过的方案，正则预扫描 O(N) 且纯 CPU，保护模式固定（6 种正则），不需要模型推理。

### D2: Validator 规则集

**选择**：5 条规则，不合格则降级

| 规则 | 阈值 | 来源 |
|------|------|------|
| 空输出 | chunks == 0 | WeKnora validator |
| 大文档单 chunk | chunks == 1 且 totalChars > 2×chunkSize | WeKnora validator |
| 碎片率过高 | >25% 的 chunk < 50 字符（排除最后一个） | WeKnora validator |
| 超大 chunk | 任何 chunk > 2×chunkSize | WeKnora validator |
| 全 chunk 远低于目标 | maxLen < chunkSize/4 且 totalChars > chunkSize | WeKnora validator |

**降级链**：structural → recursive（semantic 不参与自动降级，因为它是用户显式选择的高成本模式）

### D3: ContextHeader 存储方案

**选择**：zvec schema 新增 `context_header` STRING 字段

**备选方案**：
- A) zvec 新增字段（独立存储）✓
- B) 拼入 text 字段用特殊分隔符（如 `[CTX]...[/CTX]`）——污染原文，解析脆弱
- C) 存 SQLite 元数据表，zvec 只存 content——检索时需额外 join，增加延迟

**理由**：zvec 支持动态 schema（`coll.insert` 时传新字段即可），旧数据该字段为空字符串，不影响 ANN 检索。embedding 输入改为 `context_header + "\n\n" + content`，存储和检索解耦。

### D4: Auto Profiler 策略选择逻辑

**选择**：简化版 profiler（对比 WeKnora 的 15+ 指标，CodingHub 只需 4 个）

```python
def select_strategy(text: str) -> str:
    """单遍扫描，返回最优 chunk_mode"""
    heading_count = count_md_headings(text)  # #{1,6} 标题数
    code_ratio = compute_code_ratio(text)     # 围栏代码占比
    has_tables = detect_tables(text)          # 是否有 | 表格
    total_chars = len(text)

    if heading_count >= 3 and heading_count / max(lines, 1) > 0.005:
        return "structural"
    if code_ratio > 0.5:
        return "structural"  # 代码文档用结构切分保护代码块
    if total_chars < 200:
        return "recursive"   # 极短文本无需结构分析
    return "structural"      # 默认 structural（对 MD 最友好）
```

**理由**：CodingHub 知识库主要是 MD/TXT/代码文件，structural 是绝大多数场景的最优解。Profiler 的价值在于：1) 识别纯文本无结构文档降级到 recursive；2) 为未来扩展留接口。semantic 模式因 CPU 成本不参与 auto 选择。

### D5: 前端分片预览 API 设计

**选择**：RAG REST API 新增 `POST /api/collections/{name}/chunking/preview`

```json
// Request
{ "text": "样本文本...", "strategy": "auto", "chunk_size": 800, "chunk_overlap": 50 }

// Response
{
  "strategy_used": "structural",
  "chunks": [
    { "index": 0, "text": "...", "context_header": "# 标题", "char_count": 342, "token_est": 85 }
  ],
  "stats": { "total_chunks": 12, "avg_chars": 410, "min_chars": 120, "max_chars": 780, "stddev": 156 }
}
```

**理由**：参考 WeKnora 的 `POST /api/v1/chunker/preview` 设计，只读操作，不写 DB，不调 embedding API，5s 超时保护。前端直接调 RAG :8000 端口（已有 CORS）。

### D6: BM25 混合检索实现方式

**选择**：zvec v0.5.0+ 原生 FTS（FtsIndexParam + MultiQuery + RRF 融合）

**备选方案**：
- A) SQLite FTS5 独立索引：在 `rag/core/bm25_index.py` 中维护一套关键词倒排索引，检索时分别查 ANN 和 FTS5 再手动 RRF 融合——需额外维护索引同步、增加 ingest 复杂度
- B) rank_bm25 Python 库：内存中构建 BM25 索引——大集合时内存占用高，且进程重启需全量重建
- C) zvec 原生 FTS ✓：在 text 字段上建 FtsIndexParam，查询时用 MultiQuery 同时走 ANN + FTS，引擎内部 RRF/Weighted 融合排序——零额外依赖，索引自动同步

**理由**：zvec v0.5.0 已原生支持全文检索（BM25 评分 + WAND/Block-Max WAND 剪枝 + Roaring Bitmap 倒排），与向量索引共享同一 collection，insert/delete 时 FTS 索引自动维护，无需额外同步逻辑。MultiQuery 支持 `rrf` 和 `weighted` 两种融合策略，开箱即用。

**实现要点**：
```python
# vector_store.py — 建表时
from zvec import FtsIndexParam
fts_param = FtsIndexParam(field_name="text")
coll.create_index(..., fts_index_params=[fts_param])

# vector_store.py — 检索时
from zvec import MultiQuery
multi_query = MultiQuery(
    vector_query=embedding,       # ANN 向量检索
    fts_query=query_text,         # BM25 全文检索
    fusion="rrf",                 # RRF 融合排序
    limit=top_k,
)
results = coll.search(multi_query)
```

**约束**：
- 需确认当前 zvec 版本 ≥ 0.5.0（`pip show zvec` 验证）
- FTS 索引仅对 STRING 类型字段生效，text 字段已满足
- 旧 collection 需重建索引才能启用 FTS（通过 re-ingest 或 `coll.create_index` 补建）

## 流程图

```mermaid
flowchart TD
    A[文档输入] --> B[Auto Profiler<br/>单遍扫描文档特征]
    B --> C{选择策略}
    C -->|heading≥3 或 code>50%| D[structural 切分]
    C -->|无结构/极短文本| E[recursive 切分]
    C -->|用户显式指定 semantic| F[semantic 切分]

    D --> G[Protected Patterns<br/>标记保护区域]
    E --> G
    F --> H[直接切分<br/>semantic 不走保护]

    G --> I[执行切分<br/>跳过保护区]
    I --> J[Validator<br/>5条规则检查]
    H --> J

    J -->|通过| K[ContextHeader 生成<br/>提取标题面包屑]
    J -->|不合格| L{当前模式?}
    L -->|structural| E
    L -->|recursive| M[强制字符切分<br/>最终兜底]

    K --> N[Embedding<br/>header + content 拼接向量化]
    M --> N
    N --> O[zvec 存储<br/>text + context_header 分离]
```

## 时序图

```mermaid
sequenceDiagram
    participant FE as 前端知识库页
    participant RAG as RAG REST :8000
    participant Chunker as chunker.py
    participant ZVec as zvec 向量库

    Note over FE,ZVec: 文档 Ingest 流程
    FE->>RAG: POST /collections/{name}/documents (上传文件)
    RAG->>Chunker: select_strategy(text)
    Chunker-->>RAG: "structural"
    RAG->>Chunker: structural_chunk_text(text, strategy="structural")
    Chunker->>Chunker: protected_spans(text)
    Chunker->>Chunker: split (跳过保护区)
    Chunker->>Chunker: validate_chunks()
    alt 验证通过
        Chunker-->>RAG: chunks[] with context_header
    else 验证失败
        Chunker->>Chunker: fallback recursive
        Chunker-->>RAG: chunks[]
    end
    RAG->>ZVec: insert(text, context_header, embedding)

    Note over FE,ZVec: 混合检索流程（ANN + BM25 + RRF）
    FE->>RAG: POST /collections/{name}/search {query, top_k}
    RAG->>RAG: embedding = encode(query)
    RAG->>ZVec: MultiQuery(vector=embedding, fts=query, fusion="rrf")
    ZVec->>ZVec: ANN 向量检索 + FTS BM25 检索 → RRF 融合排序
    ZVec-->>RAG: results[] (text, context_header, score)
    RAG->>RAG: rerank(query, results) [可选]
    RAG-->>FE: JSON 检索结果（含 context_header）

    Note over FE,ZVec: 分片预览流程
    FE->>RAG: POST /collections/{name}/chunking/preview {text, strategy}
    RAG->>Chunker: preview_chunk(text, strategy, chunk_size)
    Chunker-->>RAG: {chunks, stats, strategy_used}
    RAG-->>FE: JSON 预览结果（不写DB，不embedding）
```

## 数据模型

```mermaid
erDiagram
    ZVEC_COLLECTION {
        string id PK "doc_id_chunk_index"
        string embedding "VECTOR_FP32 向量"
        string text "原文内容（不含header）+ FTS索引"
        string source "源文件路径"
        int chunk_index "序号"
        string context_header "标题面包屑（新增）"
    }
    COLLECTION_CONFIG {
        string name PK "集合名"
        string chunk_mode "structural/semantic/recursive"
        string strategy "auto/structural/semantic/recursive（新增）"
        int chunk_size "默认800"
        int chunk_overlap "默认50"
        boolean rerank "默认true"
        string description "集合描述"
    }
```

## 风险 / 权衡（Risks / Trade-offs）

- [Protected Patterns 正则性能] 6 组正则在超大文档（>1MB）上可能耗时 → 缓解：对 >500KB 文档跳过保护扫描，直接 recursive 切分
- [zvec schema 兼容性] 新增 context_header 字段后旧数据该字段为空 → 缓解：检索时空字符串不影响 ANN，EmbeddingContent() 对空 header 直接返回 content
- [Validator 误杀] 某些文档天然碎片化（如 FAQ 列表），structural 切出短 chunk 被误判为碎片 → 缓解：排除最后一个 chunk；阈值 25% 足够宽松；用户可手动指定 chunk_mode 绕过 auto
- [前端直连 RAG 端口] 预览 API 在 :8000，前端需 CORS → 缓解：RAG 已默认开启 CORS（RAG_CORS_ORIGINS）
- [embedding 维度变化] context_header 拼入后 embedding 输入变长，向量语义偏移 → 缓解：header 通常 <50 字符，对 512-800 字符的 chunk 影响 <10%；且所有 chunk 统一加 header，相对排序不变
- [zvec FTS 版本要求] 原生 FTS 需 zvec ≥ 0.5.0 → 缓解：实施前 `pip show zvec` 验证版本；若版本不足则 `pip install --upgrade zvec`，FTS 为增量功能不影响已有 ANN 索引
- [旧 collection FTS 索引缺失] 已有 collection 的 text 字段无 FTS 索引 → 缓解：search 时检测 FTS 可用性，不可用则降级为纯 ANN 检索（行为与变更前一致）；提供 re-ingest 命令补建索引

## 迁移计划（Migration Plan）

1. **Phase 1（RAG 后端 - 切分增强）**：修改 `chunker.py` + `vector_store.py` + `service.py`，新增 protected patterns / validator / profiler / context_header。已有 collection 无 strategy 字段时默认 "structural"（保持现有行为）。
2. **Phase 1.5（RAG 后端 - 混合检索）**：修改 `vector_store.py`，collection 创建时 text 字段附加 FtsIndexParam；search 改用 MultiQuery（ANN + FTS + RRF）。旧 collection 降级为纯 ANN（向后兼容）。
3. **Phase 2（REST API）**：新增 `/chunking/preview` 端点。
4. **Phase 3（前端）**：知识库设置页增加分片预览面板；文档列表增加 chunk 统计列。
5. **回滚策略**：strategy 字段为纯新增，删除即回退；zvec 新字段为空不影响旧逻辑；FTS 索引为增量，删除后 search 自动降级为纯 ANN；前端组件独立，移除不影响现有页面。

## 待定问题（Open Questions）

- 是否需要对已有文档提供"重新切片"按钮（re-ingest with new strategy）？当前设计是仅新文档走 auto，旧文档保持不变。
- semantic 模式是否也应加 Protected Patterns？当前设计不加（semantic 按句子粒度切，本身不会切断行内元素），但如果句子提取逻辑有 bug 仍可能切断。
- zvec FTS 分词器配置：中文文本需要合适的 tokenizer（jieba / character n-gram），需确认 zvec FtsIndexParam 是否支持自定义 tokenizer 或默认按空格/标点分词。若默认分词对中文效果不佳，可能需要 `analyzer` 参数或退化为 character trigram。
