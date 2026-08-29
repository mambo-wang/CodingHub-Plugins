## ADDED Requirements（新增需求）

### Requirement: 管理员可回复留言
系统必须提供 REST API 端点允许管理员（ADMIN 或 SUPER_ADMIN 角色）回复留言。回复内容写入 feedback_message 的 admin_reply 字段，同时记录 replied_by 和 replied_at。

#### Scenario: 管理员成功回复留言
- **WHEN** ADMIN 角色用户发送 PUT /api/v1/feedback/{id}/reply，请求体包含 adminReply="感谢建议，已排期"
- **THEN** 系统更新该留言的 admin_reply、replied_by（当前管理员 ID）和 replied_at 字段，返回 200 OK

#### Scenario: 非管理员尝试回复被拒绝
- **WHEN** 普通 USER 角色用户发送 PUT /api/v1/feedback/{id}/reply
- **THEN** 系统返回 403 Forbidden，留言未被修改

#### Scenario: 未认证用户尝试回复被拒绝
- **WHEN** 未携带 JWT 的请求发送 PUT /api/v1/feedback/{id}/reply
- **THEN** 系统返回 401 Unauthorized

#### Scenario: 回复不存在的留言
- **WHEN** 管理员发送 PUT /api/v1/feedback/99999/reply，该 ID 不存在
- **THEN** 系统返回 404 Not Found

### Requirement: 管理员可软删除留言
系统必须提供 REST API 端点允许管理员软删除留言，将 status 设为 DELETED。

#### Scenario: 管理员成功删除留言
- **WHEN** SUPER_ADMIN 角色用户发送 DELETE /api/v1/feedback/{id}
- **THEN** 系统将该留言 status 更新为 DELETED，返回 200 OK，留言不再出现在公开列表中

#### Scenario: 非管理员尝试删除被拒绝
- **WHEN** 普通 USER 角色用户发送 DELETE /api/v1/feedback/{id}
- **THEN** 系统返回 403 Forbidden，留言未被修改

#### Scenario: 删除不存在的留言
- **WHEN** 管理员发送 DELETE /api/v1/feedback/99999
- **THEN** 系统返回 404 Not Found
