## ADDED Requirements

### Requirement: 我的点赞查询
系统必须提供 `GET /api/v1/interactions/likes/mine?targetType=` 端点，返回当前登录用户在某类型下的点赞目标资源分页列表（此前点赞仅支持按目标查询）。

#### Scenario: 登录用户查询我的点赞
- **WHEN** 登录用户发送 `GET /api/v1/interactions/likes/mine?targetType=TOOL&page=0&size=10`
- **THEN** 系统在 `unified_like` 中按 userId + targetType 查询，返回该用户点赞的工具资源 DTO 分页列表（复用 `ToolSummaryDTO` / `ForumPostSummaryDTO` / `VideoListItem`），按创建时间倒序

#### Scenario: 过滤已删除目标
- **WHEN** 用户点赞的目标资源已被软删除（status != NORMAL）
- **THEN** 系统在返回列表中跳过该记录，避免死链

#### Scenario: 未登录查询
- **WHEN** 未登录用户发送该请求
- **THEN** 系统返回 401 未授权

### Requirement: 我的评论查询
系统必须提供 `GET /api/v1/interactions/comments/mine` 端点，返回当前登录用户的评论分页列表，并附带每条评论所属目标的类型、ID 与标题（此前评论仅支持按目标查询）。

#### Scenario: 登录用户查询我的评论
- **WHEN** 登录用户发送 `GET /api/v1/interactions/comments/mine?page=0&size=10`
- **THEN** 系统按 userId 查询 `unified_comment`，返回包含 `targetType`、`targetId`、`targetTitle`、`content`、`createdAt` 的分页列表，`targetTitle` 按类型解析为 tool.name / forumPost.title / video.title，按创建时间倒序

#### Scenario: 过滤已删除目标
- **WHEN** 评论所属目标已被软删除
- **THEN** 系统在返回列表中跳过该评论

#### Scenario: 未登录查询
- **WHEN** 未登录用户发送该请求
- **THEN** 系统返回 401 未授权
