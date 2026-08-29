## ADDED Requirements

### Requirement: 待审批用户列表查询

系统 MUST 提供接口供超级管理员查看所有 status 为 PENDING 的用户列表。普通用户和管理员 MUST NOT 有权访问此接口。

#### Scenario: 超级管理员查看待审批列表

- **WHEN** 超级管理员发送 GET /api/v1/admin/pending-users 请求
- **THEN** 系统返回所有 status=PENDING 的用户列表，包含 id、username、nickname、role、createdAt

#### Scenario: 普通用户访问待审批列表被拒绝

- **WHEN** 普通用户发送 GET /api/v1/admin/pending-users 请求
- **THEN** 系统返回 403 错误

#### Scenario: 管理员访问待审批列表被拒绝

- **WHEN** 管理员发送 GET /api/v1/admin/pending-users 请求
- **THEN** 系统返回 403 错误

#### Scenario: 待审批列表为空

- **WHEN** 超级管理员查看待审批列表，数据库中无 PENDING 状态用户
- **THEN** 系统返回空列表

### Requirement: 审批通过操作

系统 MUST 提供接口供超级管理员通过管理员注册审批。通过后用户 status 从 PENDING 变为 ACTIVE。

#### Scenario: 超级管理员通过审批

- **WHEN** 超级管理员发送 POST /api/v1/admin/approve/{id} 请求，目标用户 status=PENDING
- **THEN** 系统将目标用户 status 更新为 ACTIVE，返回成功消息

#### Scenario: 审批通过后用户可登录

- **WHEN** 审批通过后，用户使用原用户名和密码登录
- **THEN** 系统返回 accessToken 和 refreshToken，登录成功

#### Scenario: 对非 PENDING 状态用户执行通过操作

- **WHEN** 超级管理员对 status=ACTIVE 的用户执行通过操作
- **THEN** 系统返回 400 错误，提示「该用户不在待审批状态」

#### Scenario: 对不存在的用户执行通过操作

- **WHEN** 超级管理员对不存在的 userId 执行通过操作
- **THEN** 系统返回 404 错误

#### Scenario: 非超级管理员执行通过操作被拒绝

- **WHEN** 管理员发送 POST /api/v1/admin/approve/{id} 请求
- **THEN** 系统返回 403 错误

### Requirement: 审批拒绝操作

系统 MUST 提供接口供超级管理员拒绝管理员注册审批。拒绝后用户 status 从 PENDING 变为 REJECTED。

#### Scenario: 超级管理员拒绝审批

- **WHEN** 超级管理员发送 POST /api/v1/admin/reject/{id} 请求，目标用户 status=PENDING
- **THEN** 系统将目标用户 status 更新为 REJECTED，返回成功消息

#### Scenario: 拒绝后用户不可登录

- **WHEN** 审批被拒绝后，用户尝试登录
- **THEN** 系统返回错误，提示「注册申请已被拒绝」

#### Scenario: 对非 PENDING 状态用户执行拒绝操作

- **WHEN** 超级管理员对 status=ACTIVE 的用户执行拒绝操作
- **THEN** 系统返回 400 错误，提示「该用户不在待审批状态」

#### Scenario: 非超级管理员执行拒绝操作被拒绝

- **WHEN** 管理员发送 POST /api/v1/admin/reject/{id} 请求
- **THEN** 系统返回 403 错误
