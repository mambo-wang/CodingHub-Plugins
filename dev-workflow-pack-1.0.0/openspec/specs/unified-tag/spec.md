## ADDED Requirements（新增需求）

### Requirement: 统一标签实体

系统 SHALL 提供统一的 `Tag` 实体，通过 `tag_type` 字段（枚举值：TOOL / FORUM / VIDEO）区分标签所属模块。标签名称在同一 `tag_type` 内 MUST 唯一。每个标签 SHALL 维护 `usage_count` 计数（关联内容数量）。

#### Scenario: 创建工具标签
- **WHEN** 已登录用户提交 `POST /api/v1/tags`，请求体为 `{ "name": "Python", "type": "TOOL" }`
- **THEN** 系统创建标签记录，返回标签 id 和完整信息

#### Scenario: 创建重复标签名（同类型）
- **GIVEN** 已存在 name="Python"、type=TOOL 的标签
- **WHEN** 用户再次提交 `POST /api/v1/tags`，请求体为 `{ "name": "Python", "type": "TOOL" }`
- **THEN** 返回已有标签信息（幂等），不创建重复记录

#### Scenario: 同名不同类标签
- **GIVEN** 已存在 name="Java"、type=TOOL 的标签
- **WHEN** 用户提交 `POST /api/v1/tags`，请求体为 `{ "name": "Java", "type": "FORUM" }`
- **THEN** 系统创建新标签（同名不同 type 视为不同标签）

#### Scenario: 未登录用户创建标签
- **WHEN** 未登录用户尝试 `POST /api/v1/tags`
- **THEN** 返回 401 Unauthorized

### Requirement: 标签查询

系统 SHALL 提供按类型查询标签的接口，支持获取全部标签和热门标签。

#### Scenario: 查询指定类型的所有标签
- **WHEN** 用户请求 `GET /api/v1/tags?type=TOOL`
- **THEN** 返回 type=TOOL 的所有标签列表，按 usage_count 降序排列

#### Scenario: 查询热门标签
- **WHEN** 用户请求 `GET /api/v1/tags/hot?type=FORUM&limit=10`
- **THEN** 返回 type=FORUM 中 usage_count 最高的前 10 个标签

#### Scenario: 不传 type 参数
- **WHEN** 用户请求 `GET /api/v1/tags`（不带 type）
- **THEN** 返回所有类型的标签列表

### Requirement: 工具标签关联

系统 SHALL 支持工具与标签的多对多关联。创建和更新工具时可指定标签 ID 列表，工具列表和详情接口返回关联标签。

#### Scenario: 创建工具时设置标签
- **GIVEN** 已存在 tagId=1 (Python) 和 tagId=3 (AI) 的 TOOL 类型标签
- **WHEN** 用户创建工具，请求体包含 `tagIds: [1, 3]`
- **THEN** 工具创建成功，`tool_tag` 表写入两条关联记录，对应标签的 usage_count 各加 1

#### Scenario: 更新工具标签
- **GIVEN** 工具 toolId=5 当前关联标签 [1, 3]
- **WHEN** 用户更新工具，传入 `tagIds: [1, 5]`
- **THEN** 移除标签 3 的关联（usage_count -1），新增标签 5 的关联（usage_count +1），保留标签 1

#### Scenario: 工具列表返回标签
- **WHEN** 用户请求工具列表 `GET /api/v1/tools`
- **THEN** 每个工具的响应中包含 `tags` 数组，每项包含 `id` 和 `name`

#### Scenario: 工具详情返回标签
- **WHEN** 用户请求工具详情 `GET /api/v1/tools/{id}`
- **THEN** 响应中包含 `tags` 数组

### Requirement: 微课标签关联

系统 SHALL 支持微课视频与标签的多对多关联。上传和更新视频时可指定标签 ID 列表，视频列表和详情接口返回关联标签。

#### Scenario: 上传视频时设置标签
- **WHEN** 用户上传视频，请求参数包含 `tagIds=1,2`
- **THEN** 视频创建成功，`video_tag` 表写入关联记录，对应标签的 usage_count 各加 1

#### Scenario: 更新视频标签
- **WHEN** 用户更新视频，传入新的 `tagIds` 列表
- **THEN** 替换原有标签关联，usage_count 相应增减

#### Scenario: 视频列表返回标签
- **WHEN** 用户请求视频列表 `GET /api/v1/videos`
- **THEN** 每条视频的响应中包含 `tags` 数组

### Requirement: 论坛标签关联补全

系统 SHALL 补全论坛帖子与标签的关联功能。帖子列表和详情接口 MUST 返回关联标签信息。更新帖子时 MUST 支持修改标签。

#### Scenario: 帖子列表返回标签
- **WHEN** 用户请求帖子列表 `GET /api/forum/posts`
- **THEN** 每条帖子的响应中包含 `tags` 数组，每项包含 `id` 和 `name`

#### Scenario: 帖子详情返回标签
- **WHEN** 用户请求帖子详情 `GET /api/forum/posts/{id}`
- **THEN** 响应中包含 `tags` 数组

#### Scenario: 更新帖子标签
- **GIVEN** 帖子 postId=1 当前关联标签 [2, 5]
- **WHEN** 用户更新帖子，传入 `tagIds: [2, 8]`
- **THEN** 替换原有标签关联为 [2, 8]，usage_count 相应增减

#### Scenario: 创建帖子时不传标签
- **WHEN** 用户创建帖子，不传 `tagIds`
- **THEN** 帖子创建成功，无标签关联（向后兼容）
