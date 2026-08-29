## ADDED Requirements（新增需求）

### Requirement: 按标签筛选工具列表

系统必须（SHALL）支持通过标签 ID 筛选工具广场的工具列表。`GET /api/v1/tools` 接口必须（MUST）接受可选参数 `tagId`（Long 类型），当提供时仅返回关联了该标签的工具。该参数必须（MUST）与现有的 `categoryId`、`keyword`、`sortBy` 参数兼容叠加。

#### Scenario: 按标签筛选返回关联工具

- **WHEN** 用户请求 `GET /api/v1/tools?tagId=3&page=0&size=12`
- **THEN** 系统返回所有关联了 tagId=3 的工具分页列表，按默认排序（hot）返回

#### Scenario: 标签与分类叠加筛选

- **WHEN** 用户请求 `GET /api/v1/tools?tagId=3&categoryId=2&page=0&size=12`
- **THEN** 系统返回同时满足 tagId=3 且 categoryId=2 的工具分页列表

#### Scenario: 标签与关键词叠加筛选

- **WHEN** 用户请求 `GET /api/v1/tools?tagId=3&keyword=chat&page=0&size=12`
- **THEN** 系统返回关联 tagId=3 且名称/描述包含 "chat" 的工具分页列表

#### Scenario: 无 tagId 时行为不变

- **WHEN** 用户请求 `GET /api/v1/tools?categoryId=1&page=0&size=12`（不含 tagId）
- **THEN** 系统行为与变更前完全一致，返回分类 1 下的所有工具

#### Scenario: tagId 无关联工具

- **WHEN** 用户请求 `GET /api/v1/tools?tagId=999`，且无任何工具关联该标签
- **THEN** 系统返回空列表（`content: [], totalElements: 0`），HTTP 200

### Requirement: 前端标签筛选器

前端工具广场页面必须（MUST）在搜索栏旁提供标签下拉选择框，用户选择标签后触发按标签筛选。

#### Scenario: 展示标签下拉选择框

- **WHEN** 用户进入工具广场首页
- **THEN** 搜索栏右侧展示标签下拉选择框，默认显示"标签: 全部标签"，展开后列出所有 type=TOOL 的标签（数据来自 `GET /api/v1/tags?type=TOOL`），为 radio 样式单选列表

#### Scenario: 选择标签触发筛选

- **WHEN** 用户在下拉框中选择某个标签
- **THEN** 下拉框收起并显示"标签: {标签名}"（选中态高亮），工具列表刷新为仅包含该标签关联的工具，请求携带 `tagId` 参数

#### Scenario: 选择"全部标签"取消筛选

- **WHEN** 用户在下拉框中选择"全部标签"
- **THEN** 下拉框恢复显示"标签: 全部标签"，工具列表恢复为不带 tagId 的默认查询

#### Scenario: 标签筛选与分类筛选共存

- **WHEN** 用户先选择了分类，再在下拉框中选择了标签
- **THEN** 两个筛选条件同时生效，请求同时携带 `categoryId` 和 `tagId`

### Requirement: 工具卡片 TagBadge 可点击筛选

工具卡片上的 TagBadge 在工具广场上下文中必须（MUST）支持点击触发标签筛选。

#### Scenario: 点击卡片上的标签触发筛选

- **WHEN** 用户在工具广场列表中点击某个工具卡片上的 TagBadge
- **THEN** 筛选栏对应标签变为选中态，工具列表刷新为该标签的筛选结果

#### Scenario: 非工具广场页面 TagBadge 不可点击

- **WHEN** 用户在工具详情页查看 TagBadge
- **THEN** TagBadge 保持纯展示状态，无点击交互

### Requirement: MCP 工具搜索支持标签过滤

MCP 工具 `h3_coding_hub_tool_search` 必须（MUST）支持可选参数 `tag`（标签名称字符串），提供时仅返回关联了该标签的工具。标签名称匹配必须（MUST）忽略大小写。

#### Scenario: 按标签名称搜索工具

- **WHEN** MCP 客户端调用 `h3_coding_hub_tool_search`，参数 `{"tag": "开源"}`
- **THEN** 返回所有关联了"开源"标签的工具列表，结果中每个工具的 tags 数组包含"开源"

#### Scenario: 标签与关键词叠加搜索

- **WHEN** MCP 客户端调用 `h3_coding_hub_tool_search`，参数 `{"query": "chat", "tag": "API"}`
- **THEN** 返回名称/描述匹配 "chat" 且关联了 "API" 标签的工具

#### Scenario: 标签名称大小写不敏感

- **WHEN** MCP 客户端调用 `h3_coding_hub_tool_search`，参数 `{"tag": "gpt-4"}`，数据库中标签名为 "GPT-4"
- **THEN** 正常返回关联了 "GPT-4" 标签的工具

#### Scenario: 不传 tag 参数时行为不变

- **WHEN** MCP 客户端调用 `h3_coding_hub_tool_search`，参数 `{"query": "chat"}`（不含 tag）
- **THEN** 行为与变更前完全一致

#### Scenario: tag 无匹配工具

- **WHEN** MCP 客户端调用 `h3_coding_hub_tool_search`，参数 `{"tag": "不存在的标签"}`
- **THEN** 返回 `{"tools": [], "count": 0}`
