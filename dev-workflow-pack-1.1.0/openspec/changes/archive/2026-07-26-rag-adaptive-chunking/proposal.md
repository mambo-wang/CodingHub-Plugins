## 为什么（Why）

CodingHub RAG 服务（wandering-rag-mcp）当前的切片策略存在三个系统性缺陷：1) 递归切分会切断 Markdown 图片/链接/LaTeX 公式/表格行等原子内容，导致检索到残缺片段；2) structural/semantic 模式对不适合的文档（如纯列表、短 FAQ）会产出大量碎片 chunk，无质量兜底；3) 标题上下文直接拼入 text 字段，破坏了原文位置信息，无法支持前端高亮回溯。

WeKnora（腾讯开源）的自适应三层切片架构（Profiler → Tier 链 → Validator 降级）和 Protected Patterns 机制已在生产环境验证了这些问题的解法。本次变更将其核心思路移植到 CodingHub 的 Python RAG 服务中，同时参考 RAGFlow/WeKnora 的文档管理 UI 为前端知识库页面增加分片预览与调试能力。

## 变更内容（What Changes）

- **新增 Protected Patterns 机制**：在递归切分前标记 LaTeX 公式块、Markdown 图片/链接、表格行、围栏代码块为不可切断区域，切分只在非保护区进行
- **新增 Chunk Validator + 自动降级**：切分结果经 5 条规则验证（空输出、大文档单 chunk、碎片率>25%、超大 chunk、全 chunk 远低于目标），不合格自动 fallback 到 recursive 模式
- **ContextHeader 与 Content 分离**：Chunk 数据结构新增 `context_header` 字段，embedding 时拼接（header + "\n\n" + content），zvec 存储时分开，支持原文位置回溯
- **新增 Auto Profiler**：ingest 时单遍扫描文档特征（MD 标题密度、代码占比、表格存在性、form-feed），自动选择最优 chunk_mode，替代纯手动配置
- **前端知识库分片调试 UI**：参考 WeKnora 的 Chunking Debug 面板和 RAGFlow 的文档解析预览，在知识库设置页增加"分片预览"功能——粘贴样本文本 → 实时展示切片结果（策略标签、chunk 卡片、大小统计）
- **前端文档管理增强**：参考 RAGFlow 的文档列表，展示每个文档的 chunk 数量、切片策略、处理状态

## 能力清单（Capabilities）

### 新增能力（New Capabilities）

- `rag-protected-patterns`: 切片保护区域机制——识别并保护 LaTeX/图片/链接/表格/代码块不被切断
- `rag-chunk-validator`: 切片质量验证与自动降级——5 条规则验证 + tier 降级链
- `rag-auto-profiler`: 文档特征自动分析与切片策略选择——替代手动 chunk_mode 配置
- `rag-hybrid-search`: 混合检索——zvec 原生 FTS（BM25）+ ANN 向量检索 + RRF 融合排序，替代纯向量检索，提升关键词精确匹配召回率
- `rag-chunking-preview`: 前端分片调试预览——样本文本实时切片展示（参考 WeKnora Chunking Debug）

### 修改能力（Modified Capabilities）

- `knowledge-config`: collection config 新增 `strategy: "auto" | "structural" | "semantic" | "recursive"` 字段，auto 为默认值；新增 `context_header` 开关
- `knowledge-frontend`: 知识库设置页增加分片预览面板；文档列表增加 chunk 数量/策略/状态列

## 影响范围（Impact）

- **RAG Python 服务**（`rag/core/chunker.py`）：核心改动，新增 protected patterns、validator、profiler、context_header 逻辑
- **RAG Python 服务**（`rag/core/vector_store.py`）：zvec schema 新增 `context_header` 字段（STRING）；text 字段附加 FtsIndexParam 启用 BM25 全文索引；`query()` 改用 MultiQuery（ANN + FTS + RRF 融合），旧 collection 降级纯 ANN
- **RAG Python 服务**（`rag/core/service.py`）：ingest 流程集成 auto profiler；search 返回结果携带 context_header
- **RAG REST API**（`rag/api/app.py`）：新增 `POST /api/collections/{name}/chunking/preview` 端点
- **前端**（`frontend/src/pages/knowledge/`）：知识库设置页新增分片预览组件；文档列表增强
- **前端**（`frontend/src/services/`）：新增 chunking preview API 调用
- **MCP 工具**（`rag/server.py`）：`configure_collection` 工具支持 strategy 参数；search 结果包含 context_header
- **向后兼容**：已有 collection 无 strategy 字段时默认 "structural"（保持现有行为）；zvec 新字段对旧数据为空字符串，不影响检索
