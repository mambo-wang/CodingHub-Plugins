## ADDED Requirements（新增需求）

### Requirement: MCP 创建工具支持简短描述

`h3_coding_hub_tool_create` MCP 工具 SHALL 接受可选的 `description` 参数（字符串，最大 200 字符），作为工具的简短描述写入 `Tool.description` 字段。

#### Scenario: 创建工具时传入简短描述
- **WHEN** AI 客户端调用 `h3_coding_hub_tool_create`，传入 description="一个强大的代码格式化工具"
- **THEN** 工具创建成功，`Tool.description` 存储为"一个强大的代码格式化工具"，`ToolSummaryDTO.description` 返回该值

#### Scenario: 创建工具时不传简短描述
- **WHEN** AI 客户端调用 `h3_coding_hub_tool_create`，不传 description 参数
- **THEN** 工具创建成功，`Tool.description` 为 null，行为与当前一致

### Requirement: MCP 创建工具支持标签名列表

`h3_coding_hub_tool_create` MCP 工具 SHALL 接受可选的 `tags` 参数（字符串数组，每个元素为标签名）。系统按标签名自动查找匹配的 TOOL 类型标签，不存在的标签自动创建。解析后的标签 ID 列表传入 `CreateToolRequest.tagIds`。

#### Scenario: 创建工具时传入已有标签名
- **GIVEN** 数据库中已存在 TOOL 类型标签 "CLI"（id=5）和 "Python"（id=8）
- **WHEN** AI 客户端调用 `h3_coding_hub_tool_create`，传入 tags=["CLI", "Python"]
- **THEN** 系统解析出 tagIds=[5, 8]，工具创建后关联这两个标签，各标签 usage_count 递增

#### Scenario: 创建工具时传入不存在的标签名
- **GIVEN** 数据库中不存在 TOOL 类型标签 "Rust"
- **WHEN** AI 客户端调用 `h3_coding_hub_tool_create`，传入 tags=["Rust"]
- **THEN** 系统自动创建新标签 "Rust"（type=TOOL, usage_count=0），解析其 ID 后关联到工具，该标签 usage_count 递增为 1

#### Scenario: 混合已有和不存在的标签名
- **GIVEN** 已存在标签 "CLI"，不存在标签 "Go"
- **WHEN** AI 客户端调用 `h3_coding_hub_tool_create`，传入 tags=["CLI", "Go"]
- **THEN** "CLI" 匹配已有标签，"Go" 自动创建，工具关联两个标签

#### Scenario: 创建工具时不传标签
- **WHEN** AI 客户端调用 `h3_coding_hub_tool_create`，不传 tags 参数
- **THEN** 工具创建成功，无标签关联，行为与当前一致

#### Scenario: 标签名重复（大小写不同）
- **GIVEN** 已存在标签 "python"
- **WHEN** AI 客户端调用 `h3_coding_hub_tool_create`，传入 tags=["Python"]
- **THEN** 按名称精确匹配（区分大小写），若 "Python" 不存在则创建新标签 "Python"

### Requirement: MCP 修改工具支持简短描述

`h3_coding_hub_tool_modify` MCP 工具 SHALL 接受可选的 `description` 参数。传入时更新 `Tool.description`，不传则保持不变。

#### Scenario: 修改工具时传入新的简短描述
- **GIVEN** 工具 toolId=42 当前 description="旧描述"
- **WHEN** 调用 `h3_coding_hub_tool_modify`，传入 description="新描述"
- **THEN** 工具 description 更新为"新描述"

#### Scenario: 修改工具时不传简短描述
- **GIVEN** 工具 toolId=42 当前 description="旧描述"
- **WHEN** 调用 `h3_coding_hub_tool_modify`，不传 description
- **THEN** 工具 description 保持"旧描述"不变

### Requirement: MCP 修改工具支持标签名列表

`h3_coding_hub_tool_modify` MCP 工具 SHALL 接受可选的 `tags` 参数（字符串数组）。传入时替换工具的标签关联（与 REST API `PUT /api/v1/tools/{id}` 行为一致：先删除旧关联，再添加新关联，调整 usage_count）。

#### Scenario: 修改工具时传入标签名列表
- **GIVEN** 工具 toolId=42 当前关联标签 ["旧标签"]
- **WHEN** 调用 `h3_coding_hub_tool_modify`，传入 tags=["新标签A", "新标签B"]
- **THEN** 移除旧标签关联（"旧标签" usage_count 递减），解析并关联新标签（"新标签A"、"新标签B" usage_count 递增）

#### Scenario: 修改工具时传入空标签列表
- **GIVEN** 工具 toolId=42 当前关联标签 ["标签A"]
- **WHEN** 调用 `h3_coding_hub_tool_modify`，传入 tags=[]
- **THEN** 移除所有标签关联

#### Scenario: 修改工具时不传标签
- **GIVEN** 工具 toolId=42 当前关联标签 ["标签A"]
- **WHEN** 调用 `h3_coding_hub_tool_modify`，不传 tags
- **THEN** 标签关联保持不变

### Requirement: 标签自动解析幂等性

`TagService.resolveOrCreateTags` SHALL 保证同一标签名不会被重复创建。在并发场景下，若 `UNIQUE(name, type)` 约束触发异常，系统回退到查询已有记录。

#### Scenario: 并发创建同名标签
- **GIVEN** 两个请求同时调用 resolveOrCreateTags 并传入相同的不存在标签名 "NewLang"
- **WHEN** 第一个请求成功创建标签，第二个请求触发唯一约束异常
- **THEN** 第二个请求捕获 `DataIntegrityViolationException`，回退查询已有记录，返回相同的标签 ID
