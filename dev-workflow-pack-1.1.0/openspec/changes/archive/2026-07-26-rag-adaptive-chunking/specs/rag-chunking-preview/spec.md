## ADDED Requirements（新增需求）

### Requirement: 分片预览 API
RAG REST API MUST 提供 `POST /api/collections/{name}/chunking/preview` 端点，接受样本文本和切分参数，返回切分预览结果。该端点为只读操作，MUST NOT 写入数据库、MUST NOT 调用 embedding 模型。

请求体：
```json
{
  "text": "样本文本（最大 64KB）",
  "strategy": "auto | structural | semantic | recursive",
  "chunk_size": 800,
  "chunk_overlap": 50
}
```

响应体：
```json
{
  "strategy_used": "structural",
  "chunks": [
    {
      "index": 0,
      "text": "chunk 内容预览",
      "context_header": "# 标题 > ## 小节",
      "char_count": 342,
      "token_est": 85
    }
  ],
  "stats": {
    "total_chunks": 12,
    "avg_chars": 410,
    "min_chars": 120,
    "max_chars": 780,
    "stddev": 156
  },
  "profile": {
    "heading_count": 5,
    "code_ratio": 0.12,
    "has_tables": true,
    "total_chars": 4920
  }
}
```

#### Scenario: 成功预览切分结果
- **WHEN** 用户提交一段 2000 字符的 Markdown 文本，strategy 为 "auto"，chunk_size 为 512
- **THEN** 系统返回切分后的 chunk 列表（含 context_header）、统计信息和文档 profile，不写入任何持久化存储

#### Scenario: 文本超过 64KB 限制
- **WHEN** 用户提交超过 64KB 的文本
- **THEN** 系统返回 400 错误，消息为 "Text exceeds 64KB preview limit"

#### Scenario: 空文本
- **WHEN** 用户提交空字符串或纯空白文本
- **THEN** 系统返回 400 错误，消息为 "Text must not be empty"

#### Scenario: semantic 策略预览
- **WHEN** 用户指定 strategy 为 "semantic"
- **THEN** 系统返回 400 错误，消息为 "Semantic strategy is not supported in preview mode (requires embedding model)"

### Requirement: 前端分片预览面板
知识库设置页 MUST 提供可折叠的"分片预览"面板，包含：
1. 文本输入区（monospace 字体，最大 64KB）
2. 策略选择器（auto / structural / recursive 三个选项）
3. chunk_size 和 chunk_overlap 数值输入
4. 「运行预览」按钮
5. 结果展示区：策略标签 + 统计条 + chunk 卡片列表

#### Scenario: 用户运行预览
- **WHEN** 用户在文本输入区粘贴一段 Markdown 文本，选择 strategy="auto"，点击「运行预览」
- **THEN** 面板显示加载状态，完成后展示：使用的策略标签（彩色徽章）、统计条（total/avg/min/max）、chunk 卡片列表（每张卡片显示序号、字符数、context_header 标签、内容预览截断 3 行）

#### Scenario: chunk 卡片展开
- **WHEN** 用户点击某个 chunk 卡片
- **THEN** 卡片展开显示完整文本内容（monospace 字体，支持横向滚动）

#### Scenario: 预览面板折叠
- **WHEN** 用户点击面板标题栏的折叠按钮
- **THEN** 面板内容区收起，仅保留标题栏「分片预览」+ 展开图标

### Requirement: 文档列表增强
知识库文档列表 MUST 为每个文档展示以下额外信息：
1. chunk 数量（从 RAG API 获取）
2. 使用的切分策略（structural / recursive / semantic）
3. 处理状态（ready / processing / failed）

#### Scenario: 文档列表展示 chunk 统计
- **WHEN** 用户打开知识库详情页的文档列表
- **THEN** 每个文档行显示：文件名、大小、chunk 数量（如 "12 chunks"）、策略徽章、状态图标

#### Scenario: 文档处理中状态
- **WHEN** 文档正在被异步处理（batch upload）
- **THEN** 状态列显示旋转加载图标 + "处理中"文字，chunk 数量显示 "—"
