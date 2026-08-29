# Hot Ranking

## ADDED Requirements

### Requirement: Video 实体补全 score 字段

Video 实体 SHALL 新增 `score` 字段（DECIMAL(10,2)，默认值 0），并使用与 Tool/ForumPost 相同的计算公式：`score = viewCount × 1 + likeCount × 3 + commentCount × 5`。

#### Scenario: Video 数据库表新增 score 列

- WHEN: V3 迁移脚本执行
- THEN: video 表新增 `score` DECIMAL(10,2) NOT NULL DEFAULT 0 列

#### Scenario: Video score 计算公式

- WHEN: 调用 Video 的 updateScore() 方法
- THEN: score = viewCount × 1 + likeCount × 3 + commentCount × 5

#### Scenario: Video 浏览量增加时自动更新 score

- WHEN: 微课详情页被访问，viewCount + 1
- THEN: 自动调用 updateScore()，score 值随之更新

#### Scenario: Video 点赞量增加时自动更新 score

- WHEN: 用户点赞微课，likeCount + 1
- THEN: 自动调用 updateScore()，score 值随之更新

#### Scenario: Video 评论数增加时自动更新 score

- WHEN: 用户评论微课，commentCount + 1
- THEN: 自动调用 updateScore()，score 值随之更新

### Requirement: 每个模块提供 hot-top5 接口

Tool、ForumPost、Video 三个模块 SHALL 各提供一个 `GET /hot-top5` 端点，返回全局热度前 5 的内容 ID 列表（`List<Long>`）。

#### Scenario: Tool 热度 Top5 接口

- WHEN: 客户端请求 `GET /api/v1/tools/hot-top5`
- THEN: 返回 score 最高的前 5 个 Tool ID 列表，按 score 降序

#### Scenario: ForumPost 热度 Top5 接口

- WHEN: 客户端请求 `GET /api/forum/posts/hot-top5`
- THEN: 返回 score 最高的前 5 个 ForumPost ID 列表，按 score 降序

#### Scenario: Video 热度 Top5 接口

- WHEN: 客户端请求 `GET /api/v1/videos/hot-top5`
- THEN: 返回 score 最高的前 5 个 Video ID 列表，按 score 降序

#### Scenario: 内容不足 5 条时返回全部

- WHEN: 某模块内容总数少于 5 条
- THEN: hot-top5 接口返回全部内容的 ID 列表，不补全至 5 条

### Requirement: hot-top5 接口无需认证

hot-top5 端点 SHALL 对所有人公开访问，不需要 JWT 认证。

#### Scenario: 未登录用户访问 Tool hot-top5

- WHEN: 未携带 JWT Token 请求 `GET /api/v1/tools/hot-top5`
- THEN: 接口正常返回 Top5 ID 列表，不返回 401

#### Scenario: 未登录用户访问 ForumPost hot-top5

- WHEN: 未携带 JWT Token 请求 `GET /api/forum/posts/hot-top5`
- THEN: 接口正常返回 Top5 ID 列表，不返回 401

#### Scenario: 未登录用户访问 Video hot-top5

- WHEN: 未携带 JWT Token 请求 `GET /api/v1/videos/hot-top5`
- THEN: 接口正常返回 Top5 ID 列表，不返回 401

### Requirement: 全局 Top5 内容显示 Flame 图标

前端列表中，ID 存在于全局 hot-top5 列表中的内容项 SHALL 在卡片上显示 Flame 图标（火苗图标），标识其为热门内容。

#### Scenario: Top5 工具卡片显示 Flame 图标

- WHEN: 工具列表中某工具的 ID 存在于 hot-top5 返回列表中
- THEN: 该工具卡片上显示 Flame 图标

#### Scenario: 非 Top5 项不显示 Flame 图标

- WHEN: 列表中某内容项的 ID 不在 hot-top5 返回列表中
- THEN: 该卡片上不显示 Flame 图标

#### Scenario: Top5 帖子卡片显示 Flame 图标

- WHEN: 帖子列表中某帖子的 ID 存在于 hot-top5 返回列表中
- THEN: 该帖子卡片上显示 Flame 图标

#### Scenario: Top5 微课卡片显示 Flame 图标

- WHEN: 微课列表中某微课的 ID 存在于 hot-top5 返回列表中
- THEN: 该微课卡片上显示 Flame 图标

### Requirement: 前端页面加载时请求 hot-top5 并缓存

三个列表页 SHALL 在页面加载时调用 hot-top5 接口，将返回的 ID 列表缓存为 Set，供卡片渲染时判断是否显示 Flame 图标。

#### Scenario: 列表页加载时请求 hot-top5

- WHEN: 用户进入列表页
- THEN: 前端同时发起列表请求和 hot-top5 请求，将 top5 ID 存入 Set

#### Scenario: 卡片渲染时判断 Flame 图标

- WHEN: 前端渲染列表中的每个卡片
- THEN: 检查该卡片的 ID 是否在 top5Ids Set 中，存在则显示 Flame 图标

### Requirement: Video score 字段建立数据库索引

为优化热度排序查询性能，video 表的 score 列 SHALL 建立数据库索引，与 Tool/ForumPost 保持一致。

#### Scenario: video 表 score 列有索引

- WHEN: V3 迁移脚本执行
- THEN: video 表 score 列上创建索引（与 tool、forum_post 表一致）
