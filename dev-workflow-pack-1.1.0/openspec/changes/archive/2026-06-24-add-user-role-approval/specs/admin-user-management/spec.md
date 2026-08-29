## ADDED Requirements

### Requirement: 用户列表查询

系统 MUST 提供接口供管理员和超级管理员查看用户列表（分页）。列表 MUST 包含用户 id、username、nickname、role、status、createdAt、lastLoginAt。普通用户 MUST NOT 有权访问此接口。

#### Scenario: 管理员查看用户列表

- **WHEN** 管理员发送 GET /api/v1/admin/users?page=0&size=10 请求
- **THEN** 系统返回分页用户列表，包含用户基本信息和角色、状态

#### Scenario: 超级管理员查看用户列表

- **WHEN** 超级管理员发送 GET /api/v1/admin/users?page=0&size=10 请求
- **THEN** 系统返回分页用户列表，包含用户基本信息和角色、状态

#### Scenario: 普通用户访问用户列表被拒绝

- **WHEN** 普通用户发送 GET /api/v1/admin/users 请求
- **THEN** 系统返回 403 错误

#### Scenario: 按角色筛选用户

- **WHEN** 管理员发送 GET /api/v1/admin/users?role=ADMIN 请求
- **THEN** 系统返回仅包含 role=ADMIN 的用户列表

#### Scenario: 按状态筛选用户

- **WHEN** 管理员发送 GET /api/v1/admin/users?status=PENDING 请求
- **THEN** 系统返回仅包含 status=PENDING 的用户列表

#### Scenario: 按用户名搜索

- **WHEN** 管理员发送 GET /api/v1/admin/users?keyword=admin 请求
- **THEN** 系统返回 username 或 nickname 包含 "admin" 的用户列表

### Requirement: 封禁用户

系统 MUST 提供接口供超级管理员封禁用户。封禁后用户 status 变为 DISABLED，不可登录。超级管理员不可被封禁。

#### Scenario: 超级管理员封禁普通用户

- **WHEN** 超级管理员发送 PUT /api/v1/admin/users/{id}/status 请求，body 为 {status: "DISABLED"}
- **THEN** 系统将目标用户 status 更新为 DISABLED，返回成功消息

#### Scenario: 封禁后用户不可登录

- **WHEN** 被封禁的用户尝试登录
- **THEN** 系统返回错误，提示「账号已被禁用」

#### Scenario: 管理员封禁用户被拒绝

- **WHEN** 管理员发送封禁用户请求
- **THEN** 系统返回 403 错误

#### Scenario: 封禁超级管理员被拒绝

- **WHEN** 超级管理员尝试封禁另一个 role=SUPER_ADMIN 的用户
- **THEN** 系统返回 400 错误，提示「不可封禁超级管理员」

#### Scenario: 封禁不存在的用户

- **WHEN** 超级管理员对不存在的 userId 发送封禁请求
- **THEN** 系统返回 404 错误

### Requirement: 解禁用户

系统 MUST 提供接口供超级管理员解禁用户。解禁后用户 status 变为 ACTIVE，可正常登录。

#### Scenario: 超级管理员解禁用户

- **WHEN** 超级管理员发送 PUT /api/v1/admin/users/{id}/status 请求，body 为 {status: "ACTIVE"}，目标用户 status=DISABLED
- **THEN** 系统将目标用户 status 更新为 ACTIVE，返回成功消息

#### Scenario: 解禁后用户可登录

- **WHEN** 被解禁的用户尝试登录
- **THEN** 系统返回 accessToken 和 refreshToken，登录成功

### Requirement: 删除用户

系统 MUST 提供接口供超级管理员删除用户。删除后用户记录从数据库移除，username 被释放可重新注册。超级管理员不可被删除。

#### Scenario: 超级管理员删除普通用户

- **WHEN** 超级管理员发送 DELETE /api/v1/admin/users/{id} 请求
- **THEN** 系统删除目标用户记录，返回成功消息

#### Scenario: 删除 REJECTED 用户后 username 可重新注册

- **WHEN** 超级管理员删除一个 status=REJECTED 的用户后，新用户用相同 username 注册
- **THEN** 系统允许注册，创建新用户记录

#### Scenario: 管理员删除用户被拒绝

- **WHEN** 管理员发送删除用户请求
- **THEN** 系统返回 403 错误

#### Scenario: 删除超级管理员被拒绝

- **WHEN** 超级管理员尝试删除另一个 role=SUPER_ADMIN 的用户
- **THEN** 系统返回 400 错误，提示「不可删除超级管理员」

#### Scenario: 删除不存在的用户

- **WHEN** 超级管理员对不存在的 userId 发送删除请求
- **THEN** 系统返回 404 错误
