## MODIFIED Requirements（修改需求）

### Requirement: Collection 配置字段
系统 MUST 支持以下 collection 配置字段（在原有 chunk_mode / chunk_size / chunk_overlap / rerank / description 基础上新增）：

- `strategy`: 字符串，可选值 "auto" | "structural" | "semantic" | "recursive"，默认 "auto"。控制切分策略选择方式。"auto" 表示由 profiler 自动决定；其他值为显式指定。
- `context_header`: 布尔值，默认 true。控制是否在 embedding 时拼接标题面包屑上下文。

向后兼容：已有 collection 无 strategy 字段时，系统 MUST 将其视为 "structural"（保持现有行为不变）。

#### Scenario: 新 collection 默认 strategy 为 auto
- **WHEN** 用户创建新 collection 且未指定 strategy 参数
- **THEN** collection config 中 strategy 默认为 "auto"，ingest 时由 profiler 自动选择切分模式

#### Scenario: 旧 collection 无 strategy 字段
- **WHEN** 系统读取一个在 strategy 字段引入之前创建的 collection config（无 strategy 键）
- **THEN** 系统将其视为 strategy="structural"，ingest 行为与变更前完全一致

#### Scenario: 用户显式指定 strategy 覆盖 auto
- **WHEN** 用户通过 configure_collection MCP 工具或 REST PUT /config 设置 strategy="semantic"
- **THEN** 后续 ingest 跳过 profiler，直接使用 semantic 模式切分

#### Scenario: context_header 关闭
- **WHEN** collection config 中 context_header=false
- **THEN** 切分时不生成标题面包屑，embedding 输入为纯 content（与变更前行为一致）

### Requirement: configure_collection MCP 工具扩展
`configure_collection` MCP 工具 MUST 接受新增的 `strategy` 和 `context_header` 参数，并将其持久化到 collection 的 `_config.json` 中。

#### Scenario: 通过 MCP 设置 strategy
- **WHEN** MCP 客户端调用 configure_collection(collection="my-kb", strategy="auto", context_header=true)
- **THEN** _config.json 更新为包含 "strategy": "auto", "context_header": true，后续 ingest 使用新配置
