## ADDED Requirements

### Requirement: 评论触发消息中心通知
系统 MUST 在登录用户对他人的 TOOL / FORUM_POST / VIDEO 资源发表评论（含嵌套回复）成功保存后，自动向该资源所有者生成一条 `COMMENT_REPLY` 类型通知。匿名评论、用户评论自己的资源 MUST NOT 生成通知。

#### Scenario: 登录用户评论他人资源
- **WHEN** 登录用户（userId=A）对 userId=B 拥有的 TOOL 发表评论且保存成功
- **THEN** 系统在 `notification` 表插入一条 `type=COMMENT_REPLY`、`user_id=B`、`targetType=TOOL`、`targetId=<资源ID>`、`actorId=A`、`message="{A 的昵称} 评论了: {内容预览}"` 的记录

#### Scenario: 用户评论自己的资源不通知
- **WHEN** 登录用户对属于自己的资源发表评论
- **THEN** 系统不生成任何通知

#### Scenario: 匿名评论不通知
- **WHEN** 未登录用户（userId 为 null）发表评论
- **THEN** 系统不生成任何通知

### Requirement: 点赞触发消息中心通知
系统 MUST 在登录用户对他人的 TOOL / FORUM_POST / VIDEO 资源点赞成功（`liked=true`）后，自动向该资源所有者生成一条 `LIKE` 类型通知。取消点赞、匿名点赞、点赞自己的资源 MUST NOT 生成通知。

#### Scenario: 登录用户点赞他人资源
- **WHEN** 登录用户（userId=A）对 userId=B 拥有的 FORUM_POST 点赞成功
- **THEN** 系统插入一条 `type=LIKE`、`user_id=B`、`targetType=FORUM_POST`、`targetId=<资源ID>`、`actorId=A`、`message="{A 的昵称} 赞了你的内容"` 的记录

#### Scenario: 取消点赞不通知
- **WHEN** 已点赞用户再次请求点赞（触发取消，`liked=false`）
- **THEN** 系统不生成任何通知

### Requirement: 注册审批触发管理员通知
系统 MUST 在超级管理员通过或拒绝某用户的注册审批后，向该申请人生成 `ADMIN_APPROVED` 或 `ADMIN_REJECTED` 类型通知。

#### Scenario: 审批通过
- **WHEN** 超级管理员审批通过 userId=U 的注册申请
- **THEN** 系统插入一条 `type=ADMIN_APPROVED`、`user_id=U`、`targetType=USER`、`targetId=U`、`message="你的注册申请已通过"` 的记录

#### Scenario: 审批拒绝
- **WHEN** 超级管理员拒绝 userId=U 的注册申请
- **THEN** 系统插入一条 `type=ADMIN_REJECTED`、`user_id=U`、`targetType=USER`、`targetId=U`、`message="你的注册申请已被拒绝"` 的记录

### Requirement: 通知写入为最佳努力副作用
通知生成 MUST 作为主业务事件的副作用执行；通知写入失败 MUST NOT 导致评论 / 点赞 / 审批主流程失败或回滚其已完成的业务结果。

#### Scenario: 通知写入异常不中断主流程
- **WHEN** 评论保存成功但通知写入抛出异常
- **THEN** 系统仍向调用方返回成功的评论响应，且不抛出的异常向上传播中断请求
