## ADDED Requirements（新增需求）

### Requirement: 文档特征自动分析
系统 MUST 在文档 ingest 时（当 collection config 的 strategy 为 "auto" 或未设置时）对文档文本执行单遍扫描，统计以下特征：
1. Markdown 标题数量（`#{1,6}` 开头的行数）
2. 标题密度（标题数 / 总行数）
3. 围栏代码占比（代码块内字符数 / 总字符数）
4. 表格存在性（是否有 `| ... |` 格式行）
5. 总字符数

#### Scenario: Markdown 文档被识别为结构化
- **WHEN** 文档包含 8 个 Markdown 标题，总行数 200 行（标题密度 4% > 0.5%）
- **THEN** profiler 输出 heading_count=8, heading_density=0.04, 推荐策略为 "structural"

#### Scenario: 纯代码文件被识别
- **WHEN** 文档围栏代码占比 > 50%
- **THEN** profiler 输出 code_ratio > 0.5, 推荐策略为 "structural"（保护代码块完整性）

#### Scenario: 纯文本无结构
- **WHEN** 文档无 Markdown 标题（heading_count=0），无代码块，无表格
- **THEN** profiler 推荐策略为 "recursive"

### Requirement: 策略自动选择
系统 MUST 根据 profiler 输出按以下优先级选择切分策略：
1. heading_count >= 3 且 heading_density > 0.005 → "structural"
2. code_ratio > 0.5 → "structural"
3. total_chars < 200 → "recursive"
4. 默认 → "structural"

semantic 模式 MUST NOT 被 auto profiler 自动选择（CPU 成本过高）。

#### Scenario: 标准 Markdown 文档
- **WHEN** 一个包含 5 个二级标题、2 个代码块的技术文档被 ingest，collection strategy 为 "auto"
- **THEN** 系统自动选择 "structural" 模式切分

#### Scenario: 极短文本
- **WHEN** 一个 150 字符的 README 片段被 ingest
- **THEN** 系统自动选择 "recursive" 模式（无需结构分析开销）

#### Scenario: 用户显式指定策略覆盖 auto
- **WHEN** collection config 的 strategy 为 "semantic"（非 "auto"）
- **THEN** 系统跳过 profiler，直接使用 semantic 模式

### Requirement: Profiler 性能约束
Profiler 单遍扫描 MUST 在 O(N) 时间内完成（N 为文档字符数），不引入额外模型推理或网络调用。

#### Scenario: 大文档 profiler 性能
- **WHEN** 一个 500KB 的 Markdown 文档被 ingest
- **THEN** profiler 扫描耗时 < 100ms（纯字符串操作，无正则回溯）
