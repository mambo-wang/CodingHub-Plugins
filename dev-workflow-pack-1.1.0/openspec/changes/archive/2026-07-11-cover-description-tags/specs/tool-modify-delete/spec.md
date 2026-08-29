## ADDED Requirements（新增需求）

### Requirement: 工具短描述字段

系统 SHALL 在 `Tool` 实体上新增 `description` 字段（VARCHAR 200，纯文本），用于存储工具的简短描述。该字段独立于现有的 `content` 字段（Markdown 正文），两者互不影响。

#### Scenario: 创建工具时设置描述
- **WHEN** 已登录用户创建工具，请求体包含 `description: "一个快速的数据格式转换工具"`
- **THEN** 工具创建成功，`description` 字段保存该文本

#### Scenario: 创建工具时不传描述
- **WHEN** 用户创建工具，请求体不包含 `description`
- **THEN** 工具创建成功，`description` 字段为 null（向后兼容）

#### Scenario: 描述字段长度限制
- **WHEN** 用户创建或更新工具，传入的 `description` 超过 200 字符
- **THEN** 返回 400 Bad Request，提示"描述不能超过 200 字符"

### Requirement: 工具列表卡片展示描述

系统 SHALL 在工具列表接口的响应中包含 `description` 字段，前端工具卡片在名称下方展示描述文字。

#### Scenario: 工具列表返回描述
- **WHEN** 用户请求工具列表 `GET /api/v1/tools`
- **THEN** 每个工具的 `ToolSummaryDTO` 响应中 SHALL 包含 `description` 字段

#### Scenario: 工具详情返回描述
- **WHEN** 用户请求工具详情 `GET /api/v1/tools/{id}`
- **THEN** `ToolDetailDTO` 响应中 SHALL 包含 `description` 字段

#### Scenario: 前端卡片展示描述
- **GIVEN** 工具 toolId=1 的 description 为 "一个快速的数据格式转换工具"
- **WHEN** 前端渲染工具卡片
- **THEN** 卡片在工具名称下方以次文字色（`--text-secondary`）展示描述，单行 ellipsis 截断

#### Scenario: 描述为空时卡片不展示描述行
- **GIVEN** 工具 toolId=2 的 description 为 null
- **WHEN** 前端渲染工具卡片
- **THEN** 卡片名称下方不展示描述行（避免空白）
