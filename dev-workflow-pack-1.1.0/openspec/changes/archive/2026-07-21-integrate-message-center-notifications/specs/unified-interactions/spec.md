## ADDED Requirements

### Requirement: 评论生成所有者通知
系统在 `UnifiedCommentService.addComment` 成功保存评论后，若评论者为登录用户且非资源所有者，MUST 向资源所有者生成一条 `COMMENT_REPLY` 通知。

#### Scenario: 登录用户评论他人资源生成通知
- **WHEN** 登录用户对他人的 TOOL / FORUM_POST / VIDEO 发表评论并保存成功
- **THEN** 系统调用 `NotificationService.createCommentNotification` 向资源所有者写入 `COMMENT_REPLY` 通知

#### Scenario: 评论自己的资源不通知
- **WHEN** 登录用户评论自己所拥有的资源
- **THEN** 系统不调用通知生成方法

### Requirement: 点赞生成所有者通知
系统在 `UnifiedLikeService.toggleLike` 点赞成功（`liked=true`）后，若点赞者为登录用户且非资源所有者，MUST 向资源所有者生成一条 `LIKE` 通知；取消点赞 MUST NOT 生成通知。

#### Scenario: 登录用户点赞他人资源生成通知
- **WHEN** 登录用户对他人的 TOOL / FORUM_POST / VIDEO 点赞成功
- **THEN** 系统调用 `NotificationService.createLikeNotification` 向资源所有者写入 `LIKE` 通知

#### Scenario: 取消点赞不通知
- **WHEN** 已点赞用户取消点赞（`liked=false`）
- **THEN** 系统不调用通知生成方法
