## ADDED Requirements

### Requirement: 统一点赞服务
系统必须通过 `/api/v1/interactions/likes` 端点为所有模块（TOOL / FORUM_POST / VIDEO）提供统一的点赞切换功能。

#### Scenario: 登录用户点赞
- **WHEN** 登录用户发送 POST `/api/v1/interactions/likes`，body 包含 `{"targetType": "TOOL", "targetId": 123}`
- **THEN** 系统在 `unified_like` 表中创建记录（user_id 为用户 ID，ip_hash 为 NULL），目标资源的 likeCount 加 1，返回 `{"liked": true, "likeCount": N+1}`

#### Scenario: 登录用户取消点赞
- **WHEN** 已点赞的登录用户再次发送相同的 POST 请求
- **THEN** 系统删除 `unified_like` 记录，目标资源的 likeCount 减 1，返回 `{"liked": false, "likeCount": N}`

#### Scenario: 匿名用户点赞
- **WHEN** 未登录用户发送 POST `/api/v1/interactions/likes`
- **THEN** 系统将请求 IP 进行 SHA-256 哈希后存入 `ip_hash` 字段（user_id 为 NULL），目标资源 likeCount 加 1

#### Scenario: 匿名用户取消点赞
- **WHEN** 已点赞的匿名用户（相同 IP）再次发送相同请求
- **THEN** 系统根据 ip_hash 匹配并删除记录，likeCount 减 1

#### Scenario: 点赞不存在的资源
- **WHEN** 用户发送点赞请求但 targetId 对应的资源不存在
- **THEN** 系统返回 404 错误

#### Scenario: 查询点赞状态
- **WHEN** 用户发送 GET `/api/v1/interactions/likes/status?targetType=TOOL&targetId=123`
- **THEN** 登录用户按 user_id 查询，匿名用户按 ip_hash 查询，返回 `{"liked": true/false, "likeCount": N}`

### Requirement: 统一评论服务
系统必须通过 `/api/v1/interactions/comments` 端点为所有模块提供统一的评论功能，支持嵌套回复。

#### Scenario: 创建顶层评论
- **WHEN** 用户发送 POST `/api/v1/interactions/comments`，body 包含 `{"targetType": "FORUM_POST", "targetId": 456, "content": "评论内容"}` 且无 parentId
- **THEN** 系统在 `unified_comment` 表中创建记录（parent_id 和 root_id 均为 NULL），目标资源的 commentCount 加 1

#### Scenario: 创建嵌套回复
- **WHEN** 用户发送评论请求且 body 包含 `parentId: 789`
- **THEN** 系统查找 parentId 对应的评论，设置 root_id 为 `parent.rootId ?? parent.id`，创建回复记录

#### Scenario: 匿名评论
- **WHEN** 未登录用户发送评论请求且 body 包含 `userName: "匿名"`
- **THEN** 系统创建评论记录（user_id 为 NULL，user_name 为 "匿名"）

#### Scenario: 评论内容 XSS 过滤
- **WHEN** 评论内容包含 HTML/Script 标签
- **THEN** 系统必须通过 XssSanitizer.sanitize() 过滤后再存储

#### Scenario: 获取评论列表（分页）
- **WHEN** 用户发送 GET `/api/v1/interactions/comments?targetType=TOOL&targetId=123&page=0&size=20`
- **THEN** 系统返回按 created_at 排序的分页评论列表，每条记录包含 parentId 和 rootId 字段供前端组装树形结构

#### Scenario: 删除评论（权限校验）
- **WHEN** 用户发送 DELETE `/api/v1/interactions/comments/{id}`
- **THEN** 系统校验 isOwner（user_id 匹配）或 isAdmin（ADMIN/SUPER_ADMIN 角色），通过后删除评论并更新目标资源的 commentCount

#### Scenario: 评论不存在时删除
- **WHEN** 用户尝试删除不存在的评论 ID
- **THEN** 系统返回 404 错误

### Requirement: 统一收藏服务
系统必须通过 `/api/v1/interactions/favorites` 端点为所有模块提供统一的收藏功能，收藏必须登录。

#### Scenario: 登录用户收藏
- **WHEN** 登录用户发送 POST `/api/v1/interactions/favorites`，body 包含 `{"targetType": "TOOL", "targetId": 123}`
- **THEN** 系统在 `unified_favorite` 表中创建记录，返回 `{"favorited": true}`

#### Scenario: 登录用户取消收藏
- **WHEN** 已收藏的用户再次发送相同的 POST 请求
- **THEN** 系统删除收藏记录，返回 `{"favorited": false}`

#### Scenario: 未登录用户尝试收藏
- **WHEN** 未登录用户发送收藏请求
- **THEN** 系统返回 401 未授权

#### Scenario: 获取我的收藏列表
- **WHEN** 登录用户发送 GET `/api/v1/interactions/favorites?targetType=TOOL&page=0&size=10`
- **THEN** 系统返回该用户指定类型的收藏资源分页列表，包含资源的完整 DTO（ToolSummaryDTO / ForumPostDTO / VideoListItem）

#### Scenario: 查询收藏状态
- **WHEN** 登录用户发送 GET `/api/v1/interactions/favorites/status?targetType=TOOL&targetId=123`
- **THEN** 系统返回 `{"favorited": true/false}`

#### Scenario: 收藏已删除的资源
- **WHEN** 用户尝试收藏 status=DELETED 的资源
- **THEN** 系统返回 404 错误

### Requirement: targetType 枚举校验
系统必须对 targetType 参数进行应用层枚举校验，仅接受 TOOL、FORUM_POST、VIDEO。

#### Scenario: 无效的 targetType
- **WHEN** 请求中 targetType 值不在枚举范围内
- **THEN** 系统返回 400 参数错误

### Requirement: 数据迁移
系统必须提供 SQL 脚本将旧表数据迁移到新表。

#### Scenario: 迁移 tool_like 到 unified_like
- **WHEN** 执行迁移脚本
- **THEN** tool_like 的所有记录以 target_type=TOOL 写入 unified_like，旧表改名为 tool_like_deprecated

#### Scenario: 迁移 forum_like（仅帖子点赞）到 unified_like
- **WHEN** 执行迁移脚本
- **THEN** forum_like 中 comment_id 为 NULL 的记录以 target_type=FORUM_POST 写入 unified_like，comment_id 非空的记录（评论点赞）不迁移

#### Scenario: 迁移 forum_comment 到 unified_comment
- **WHEN** 执行迁移脚本
- **THEN** forum_comment 的所有记录以 target_type=FORUM_POST 写入 unified_comment，保留 parent_id 和 root_id
