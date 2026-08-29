# Video Interaction

## ADDED Requirements

### Requirement: 视频点赞

系统 SHALL 允许已登录用户对视频进行点赞和取消点赞操作。每个用户对同一视频只能点赞一次。点赞/取消点赞 SHALL 同步更新 Video 表的 likeCount 字段。

#### Scenario: 登录用户点赞视频
- **WHEN** 已登录用户提交 `POST /api/videos/{id}/like`
- **THEN** 创建 VideoLike 记录（userId + videoId），Video.likeCount 加 1，返回 200 OK 及当前点赞状态 `{liked: true, likeCount: N}`

#### Scenario: 用户取消点赞
- **WHEN** 已点赞的用户再次提交 `POST /api/videos/{id}/like`（toggle 模式）
- **THEN** 删除 VideoLike 记录，Video.likeCount 减 1，返回 200 OK 及 `{liked: false, likeCount: N}`

#### Scenario: 重复点赞防护
- **WHEN** 用户对同一视频的点赞记录已存在，再次提交点赞请求
- **THEN** 系统识别为取消点赞操作（toggle），而非创建重复记录

#### Scenario: 未登录用户点赞
- **WHEN** 未登录用户尝试 `POST /api/videos/{id}/like`
- **THEN** 返回 401 Unauthorized

#### Scenario: 对不存在的视频点赞
- **WHEN** 用户对不存在的 video id 提交点赞
- **THEN** 返回 404 Not Found

### Requirement: 视频评论

系统 SHALL 允许已登录用户对视频发表评论，评论内容经过 XSS 过滤后存储。评论 SHALL 同步更新 Video 表的 commentCount 字段。

#### Scenario: 登录用户发表评论
- **WHEN** 已登录用户提交 `POST /api/videos/{id}/comments`，携带 content 字段
- **THEN** 创建 VideoComment 记录，Video.commentCount 加 1，返回 201 Created 及评论详情

#### Scenario: 评论内容为空
- **WHEN** 用户提交评论时 content 为空或仅含空白字符
- **THEN** 返回 400 Bad Request，提示"评论内容不能为空"

#### Scenario: 评论内容 XSS 过滤
- **WHEN** 用户评论内容包含 HTML 脚本标签（如 `<script>alert(1)</script>`）
- **THEN** 内容经 XssSanitizer.sanitize() 过滤后存储，脚本标签被移除

#### Scenario: 未登录用户发评论
- **WHEN** 未登录用户尝试 `POST /api/videos/{id}/comments`
- **THEN** 返回 401 Unauthorized

### Requirement: 评论列表查询

系统 SHALL 提供视频评论列表接口，支持分页，按创建时间倒序排列，无需登录即可访问。

#### Scenario: 获取视频评论列表
- **WHEN** 用户请求 `GET /api/videos/{id}/comments?page=1&size=20`
- **THEN** 返回评论列表，每条评论包含 id、content、userId、userNickname、userAvatarUrl、createdAt，按 createdAt 倒序

#### Scenario: 视频无评论
- **WHEN** 请求的视频没有任何评论
- **THEN** 返回空列表，totalElements = 0

### Requirement: 视频收藏

系统 SHALL 允许已登录用户收藏和取消收藏视频。每个用户对同一视频只能收藏一次。

#### Scenario: 登录用户收藏视频
- **WHEN** 已登录用户提交 `POST /api/videos/{id}/favorite`
- **THEN** 创建 VideoFavorite 记录（userId + videoId），返回 200 OK 及当前收藏状态 `{favorited: true}`

#### Scenario: 用户取消收藏
- **WHEN** 已收藏的用户再次提交 `POST /api/videos/{id}/favorite`（toggle 模式）
- **THEN** 删除 VideoFavorite 记录，返回 200 OK 及 `{favorited: false}`

#### Scenario: 重复收藏防护
- **WHEN** 用户对同一视频的收藏记录已存在，再次提交收藏请求
- **THEN** 系统识别为取消收藏操作（toggle），而非创建重复记录

#### Scenario: 未登录用户收藏
- **WHEN** 未登录用户尝试 `POST /api/videos/{id}/favorite`
- **THEN** 返回 401 Unauthorized

### Requirement: 我的收藏列表

系统 SHALL 提供已登录用户查看自己收藏的视频列表，支持分页。

#### Scenario: 获取我的收藏列表
- **WHEN** 已登录用户请求 `GET /api/videos/my/favorites?page=1&size=20`
- **THEN** 返回当前用户收藏的视频列表（仅 NORMAL 状态视频），按收藏时间倒序，包含分页信息

#### Scenario: 收藏的视频被删除
- **WHEN** 用户收藏的视频被上传者删除（状态为 DELETED）
- **THEN** 该视频不出现在收藏列表中

#### Scenario: 未登录访问我的收藏
- **WHEN** 未登录用户请求 `GET /api/videos/my/favorites`
- **THEN** 返回 401 Unauthorized

### Requirement: 互动状态查询

系统 SHALL 在视频详情接口中返回当前登录用户对该视频的点赞和收藏状态。

#### Scenario: 登录用户查看视频详情时返回互动状态
- **WHEN** 已登录用户请求 `GET /api/videos/{id}`
- **THEN** 返回字段中包含 `userLiked: true/false` 和 `userFavorited: true/false`

#### Scenario: 未登录用户查看视频详情时互动状态默认 false
- **WHEN** 未登录用户请求 `GET /api/videos/{id}`
- **THEN** 返回字段中 `userLiked: false`，`userFavorited: false`
