# Rag Chunk Validator

## ADDED Requirements（新增需求）

### Requirement: 切片质量验证
系统 MUST 在每次切分完成后对结果执行 5 条验证规则，全部通过方可接受该切分结果：
1. 非空：chunks 数量 > 0
2. 大文档非单 chunk：若 totalChars > 2×chunkSize，则 chunks 数量 MUST > 1
3. 碎片率：排除最后一个 chunk 后，字符数 < 50 的 chunk 占比 MUST ≤ 25% 且碎片数 ≤ 2
4. 超大 chunk：任何 chunk 的字符数 MUST ≤ 2×chunkSize
5. 非全碎片：若 totalChars > chunkSize，则最大 chunk 的字符数 MUST ≥ chunkSize/4

#### Scenario: 切分结果正常通过验证
- **WHEN** 一个 3000 字符的 Markdown 文档以 chunkSize=800 切分，产出 5 个 chunk，最小 200 字符，最大 750 字符
- **THEN** 验证通过，返回该切分结果

#### Scenario: 大文档只产出单个 chunk
- **WHEN** 一个 5000 字符的文档以 chunkSize=800 切分，仅产出 1 个 chunk
- **THEN** 验证失败，触发降级

#### Scenario: 碎片率过高
- **WHEN** 切分产出 20 个 chunk，其中 8 个（排除最后一个后）字符数 < 50
- **THEN** 验证失败（碎片率 8/19 > 25%），触发降级

### Requirement: 自动降级链
当验证失败时，系统 MUST 按以下降级链尝试下一层切分策略：
- structural → recursive（最终兜底）
- semantic 模式不参与自动降级（用户显式选择的高成本模式）

降级后的结果不再二次验证（recursive 为最终兜底，始终返回结果）。

#### Scenario: structural 验证失败降级到 recursive
- **WHEN** structural 模式切分一个纯列表文档，产出大量碎片 chunk，验证失败
- **THEN** 系统自动使用 recursive 模式重新切分同一文档，返回 recursive 的结果

#### Scenario: semantic 模式不降级
- **WHEN** semantic 模式切分结果验证失败
- **THEN** 系统仍返回 semantic 的切分结果（不降级），但日志记录验证失败原因

#### Scenario: recursive 为最终兜底
- **WHEN** recursive 模式切分结果仍不满足验证规则
- **THEN** 系统仍返回该结果（不再降级），因为 recursive 是最终兜底

### Requirement: 验证结果可观测
系统 MUST 在切分日志中记录验证结果，包括：通过/失败、失败原因、是否触发降级、降级前后的策略名称。

#### Scenario: 降级事件被记录
- **WHEN** structural 切分验证失败并降级到 recursive
- **THEN** 日志输出包含：`chunker: tier structural rejected: too many tiny chunks; falling back to recursive`
