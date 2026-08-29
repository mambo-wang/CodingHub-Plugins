## MODIFIED Requirements

### Requirement: 用户认证

#### Scenario 1: 用户使用用户名登录
- GIVEN: 用户已注册，用户名为 "testuser"，密码为 "password123"，status 为 ACTIVE
- WHEN: 用户提交登录请求，username="testuser", password="password123"
- THEN: 系统返回 JWT token 和用户信息（包含 role 和 status），登录成功

#### Scenario 2: 登录密码错误
- GIVEN: 用户已注册，用户名为 "testuser"，密码为 "password123"
- WHEN: 用户提交登录请求，username="testuser", password="wrongpassword"
- THEN: 系统返回 401 错误，提示"用户名或密码错误"

#### Scenario 3: 登录用户不存在
- GIVEN: 数据库中不存在用户名为 "nonexistent" 的用户
- WHEN: 用户提交登录请求，username="nonexistent", password="password123"
- THEN: 系统返回 401 错误，提示"用户名或密码错误"

#### Scenario 4: 注册密码长度不足
- GIVEN: 新用户注册信息，用户名为 "newuser"
- WHEN: 用户提交注册请求，密码为 "12345"（长度 5）
- THEN: 系统返回 400 错误，提示"密码长度至少6位"

#### Scenario 5: 普通用户注册成功
- GIVEN: 新用户注册信息，用户名为 "newuser"，role 为 USER
- WHEN: 用户提交注册请求，密码为 "password"（长度 >= 6），role="USER"
- THEN: 系统返回 201 状态码，创建用户成功（role=USER, status=ACTIVE），返回 accessToken 和 refreshToken

#### Scenario 6: 管理员注册成功进入待审批
- GIVEN: 新用户注册信息，用户名为 "newadmin"，role 为 ADMIN
- WHEN: 用户提交注册请求，role="ADMIN"
- THEN: 系统返回 201 状态码，创建用户成功（role=ADMIN, status=PENDING），不返回 token，提示"注册成功，等待超级管理员审批"

#### Scenario 7: 注册用户名已存在
- GIVEN: 数据库中已存在用户名为 "existinguser" 的用户
- WHEN: 新用户提交注册请求，用户名为 "existinguser"，密码为 "password123"
- THEN: 系统返回 400 错误，提示"用户名已被注册"

#### Scenario 8: PENDING 状态用户登录被拒绝
- GIVEN: 用户已注册，username="pendingadmin"，status=PENDING
- WHEN: 用户提交登录请求
- THEN: 系统返回 403 错误，提示"账号等待审批中"

#### Scenario 9: REJECTED 状态用户登录被拒绝
- GIVEN: 用户已注册，username="rejectedadmin"，status=REJECTED
- WHEN: 用户提交登录请求
- THEN: 系统返回 403 错误，提示"注册申请已被拒绝"

#### Scenario 10: DISABLED 状态用户登录被拒绝
- GIVEN: 用户已注册，username="banneduser"，status=DISABLED
- WHEN: 用户提交登录请求
- THEN: 系统返回 403 错误，提示"账号已被禁用"

## ADDED Requirements（新增需求）

### Requirement: 知识库 API 端点权限配置

SecurityConfig SHALL 配置知识库相关端点的访问权限：GET 请求公开访问，POST/PUT/DELETE 请求需要 JWT 认证。

#### Scenario: 公开访问知识库 GET 端点
- **WHEN** 未携带 JWT 的请求访问 GET `/api/v1/knowledge`、GET `/api/v1/knowledge/{id}`、GET `/api/v1/knowledge/{id}/documents`、GET `/api/v1/knowledge/{id}/config`、POST `/api/v1/knowledge/{id}/search`
- **THEN** 请求被允许通过 JwtAuthenticationFilter，无需认证

#### Scenario: 需认证的知识库写入端点
- **WHEN** 未携带 JWT 的请求访问 POST `/api/v1/knowledge`、PUT `/api/v1/knowledge/{id}`、DELETE `/api/v1/knowledge/{id}`、POST `/api/v1/knowledge/{id}/documents`、DELETE `/api/v1/knowledge/{id}/documents/{docId}`、PUT `/api/v1/knowledge/{id}/config`
- **THEN** 系统返回 401 Unauthorized

### Requirement: 知识库操作权限校验

Service 层 SHALL 对知识库的修改操作执行 owner/admin 权限校验。

#### Scenario: 所有者操作自己的知识库
- **WHEN** 知识库所有者调用更新/删除/上传/配置操作
- **THEN** 操作正常执行

#### Scenario: 管理员操作他人知识库
- **WHEN** role 为 ADMIN 或 SUPER_ADMIN 的用户操作任意知识库
- **THEN** 操作正常执行

#### Scenario: 普通用户操作他人知识库
- **WHEN** 非所有者且非管理员的用户操作他人知识库
- **THEN** 系统抛出 ForbiddenException（403）
