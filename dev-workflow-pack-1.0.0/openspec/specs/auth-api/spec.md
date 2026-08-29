## MODIFIED Requirements

### Requirement: 昵称注册

#### Scenario 1: 注册成功 - 普通用户包含昵称
- GIVEN: 新用户注册信息，username="wangbao", nickname="王宝", password=***, role="USER"
- WHEN: 用户提交 POST /api/v1/auth/register 请求
- THEN: 系统返回 201 状态码，用户信息包含 username、nickname、role="USER"、status="ACTIVE"，accessToken 和 refreshToken

#### Scenario 2: 注册成功 - 管理员进入待审批
- GIVEN: 新用户注册信息，username="admin1", nickname="管理员1", password=***, role="ADMIN"
- WHEN: 用户提交 POST /api/v1/auth/register 请求
- THEN: 系统返回 201 状态码，用户信息包含 username、nickname、role="ADMIN"、status="PENDING"，不返回 token，消息提示"等待审批"

#### Scenario 3: 注册失败 - 昵称重复
- GIVEN: 数据库中已存在用户，username="user1", nickname="王宝"
- WHEN: 新用户提交注册请求，username="user2", nickname="王宝"
- THEN: 系统返回 400 状态码，错误信息"昵称已被使用"

#### Scenario 4: 注册失败 - 昵称长度不足
- GIVEN: 新用户注册信息，username="newuser", nickname="A", password=***
- WHEN: 用户提交注册请求
- THEN: 系统返回 400 状态码，错误信息"昵称长度需在2-10字符之间"

#### Scenario 5: 注册失败 - 用户名重复
- GIVEN: 数据库中已存在用户 username="existing"
- WHEN: 新用户提交注册请求，username="existing", nickname="新昵称"
- THEN: 系统返回 400 状态码，错误信息"用户名已被注册"

#### Scenario 6: 注册失败 - 角色字段为 SUPER_ADMIN
- GIVEN: 新用户注册信息，username="super", role="SUPER_ADMIN"
- WHEN: 用户提交注册请求
- THEN: 系统返回 400 状态码，错误信息"不允许注册超级管理员"

#### Scenario 7: 登录返回用户昵称和角色
- GIVEN: 数据库中用户 username="wangbao", nickname="王宝", role="USER", status="ACTIVE"
- WHEN: 用户提交登录请求，username="wangbao", password=***
- THEN: 系统返回用户信息包含 nickname="王宝", role="USER", status="ACTIVE"

#### Scenario 8: 获取当前用户信息包含昵称和角色
- GIVEN: 用户已登录，token 有效
- WHEN: 用户发送 GET /api/v1/users/me 请求
- THEN: 系统返回用户信息包含 nickname、role、status 字段

## ADDED Requirements

### Requirement: 管理端 API 鉴权

系统 MUST 对 `/api/v1/admin/**` 路径下的接口按角色鉴权。审批相关接口仅 SUPER_ADMIN 可访问，用户管理接口 ADMIN 和 SUPER_ADMIN 可访问。

#### Scenario: 超级管理员访问审批接口

- **WHEN** 超级管理员发送 GET /api/v1/admin/pending-users 请求
- **THEN** 系统返回 200，包含待审批用户列表

#### Scenario: 未认证用户访问管理接口

- **WHEN** 未携带 token 的请求访问 /api/v1/admin/users
- **THEN** 系统返回 401 错误

#### Scenario: 普通用户访问用户管理接口

- **WHEN** role=USER 的用户发送 GET /api/v1/admin/users 请求
- **THEN** 系统返回 403 错误
