# Rag Hybrid Search

## ADDED Requirements（新增需求）

### Requirement: zvec 原生 FTS 索引
系统 MUST 在创建新 collection 时，对 text 字段附加 FtsIndexParam，启用 BM25 全文索引：
1. collection 创建时调用 `FtsIndexParam(field_name="text")` 建立 FTS 索引
2. insert/delete 操作时 FTS 索引自动同步维护，无需额外逻辑
3. 已有 collection（无 FTS 索引）提供 `rebuild_fts_index()` 补建能力

#### Scenario: 新建 collection 自动启用 FTS
- **WHEN** 用户通过 REST API 或 MCP 工具创建一个新 collection
- **THEN** 该 collection 的 text 字段同时拥有向量索引和 FTS 索引

#### Scenario: 旧 collection 补建 FTS 索引
- **WHEN** 管理员对已有 collection 调用 `rebuild_fts_index(collection_name)`
- **THEN** 系统对该 collection 的 text 字段补建 FTS 索引，无需重新 embedding

### Requirement: MultiQuery 混合检索
系统 MUST 在 search 时同时执行 ANN 向量检索和 FTS BM25 全文检索，通过 RRF 融合排序返回结果：
1. 查询时构造 `MultiQuery(vector_query=embedding, fts_query=query_text, fusion="rrf", limit=top_k)`
2. zvec 引擎内部并行执行 ANN + FTS，RRF 公式融合两路分数
3. 融合结果再经 reranker（若启用）精排后返回

#### Scenario: 关键词精确匹配召回
- **WHEN** 用户查询 "FastAPI 中间件" 且文档中确实包含该精确词组
- **THEN** FTS 分支通过 BM25 精确匹配命中该文档，即使语义向量距离较远也能被召回

#### Scenario: 语义相似但无关键词重叠
- **WHEN** 用户查询 "如何部署服务" 而文档标题为 "Production Release Guide"
- **THEN** ANN 分支通过语义相似度命中该文档，FTS 分支不命中，RRF 融合后仍返回

#### Scenario: 两路同时命中排名提升
- **WHEN** 某文档同时被 ANN 和 FTS 命中
- **THEN** RRF 融合后该文档排名高于仅被单路命中的文档

### Requirement: 旧 collection 降级兼容
当 collection 未建 FTS 索引时，系统 MUST 自动降级为纯 ANN 向量检索，行为与变更前一致：
1. search 时检测 FTS 可用性（try/except 或 schema 检查）
2. FTS 不可用时退化为纯向量检索，不抛异常
3. 日志记录降级事件（INFO 级别）

#### Scenario: 旧 collection 无 FTS 索引
- **WHEN** 对一个变更前创建的 collection 执行 search
- **THEN** 系统检测到 FTS 不可用，自动降级为纯 ANN 检索，返回结果与变更前一致

#### Scenario: 空 query_text 退化
- **WHEN** search 请求的 query_text 为空字符串（仅有 embedding）
- **THEN** 系统跳过 FTS 分支，仅执行 ANN 向量检索

### Requirement: 版本前置检查
系统 SHOULD 在启动时检查 zvec 版本是否 ≥ 0.5.0：
1. 版本满足：启用 FTS + MultiQuery 混合检索
2. 版本不足：日志 WARNING 提示升级，运行时降级为纯 ANN（不阻塞服务启动）

#### Scenario: zvec 版本不足
- **WHEN** 当前 zvec 版本为 0.4.x，不支持 FtsIndexParam
- **THEN** 服务正常启动，日志输出 WARNING，所有 search 退化为纯 ANN
