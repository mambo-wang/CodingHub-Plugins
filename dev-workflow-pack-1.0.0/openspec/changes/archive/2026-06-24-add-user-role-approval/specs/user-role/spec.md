## ADDED Requirements

### Requirement: 用户角色枚举

系统 MUST 在 User 实体中定义三级单角色枚举：`USER`（普通用户）、`ADMIN`（管理员）、`SUPER_ADMIN`（超级管理员）。每个用户 MUST 有且仅有一个角色。

#### Scenario: 新用户注册为普通用户

- **WHEN** 用户提交注册请求，role 字段为 `USER`
- **THEN** 系统创建 User 记录，role 字段值为 `USER`

#### Scenario: 新用户注册为管理员

- **WHEN** 用户提交注册请求，role 字段为 `ADMIN`
- **THEN** 系统创建 User 记录，role 字段值为 `ADMIN`，status 字段值为 `PENDING`

#### Scenario: 注册请求携带 SUPER_ADMIN 角色被拒绝

- **WHEN** 用户提交注册请求，role 字段为 `SUPER_ADMIN`
- **THEN** 系统返回 400 错误，提示「不允许注册超级管理员」

#### Scenario: 超级管理员内置账号初始化

- **WHEN** 应用启动时，数据库中不存在 username 为 `admin` 的用户
- **THEN** 系统自动创建用户：username=admin，password=BCrypt(Cloud@1234)，role=SUPER_ADMIN，status=ACTIVE

#### Scenario: 超级管理员内置账号已存在时跳过

- **WHEN** 应用启动时，数据库中已存在 username 为 `admin` 的用户
- **THEN** 系统跳过创建，不修改已有记录

### Requirement: 账号状态枚举

系统 MUST 在 User 实体中定义账号状态枚举：`ACTIVE`（正常）、`PENDING`（待审批）、`REJECTED`（已拒绝）、`DISABLED`（已禁用）。

#### Scenario: 普通用户注册后状态为 ACTIVE

- **WHEN** 用户注册角色为 `USER`
- **THEN** User 记录 status 字段值为 `ACTIVE`，可直接登录

#### Scenario: 管理员注册后状态为 PENDING

- **WHEN** 用户注册角色为 `ADMIN`
- **THEN** User 记录 status 字段值为 `PENDING`，不可登录

#### Scenario: 审批通过后状态变为 ACTIVE

- **WHEN** 超级管理员对 PENDING 状态的用户执行「通过」操作
- **THEN** User 记录 status 字段值变为 `ACTIVE`

#### Scenario: 审批拒绝后状态变为 REJECTED

- **WHEN** 超级管理员对 PENDING 状态的用户执行「拒绝」操作
- **THEN** User 记录 status 字段值变为 `REJECTED`

#### Scenario: 老用户迁移默认角色和状态

- **WHEN** 数据库迁移执行，为现有 user 表新增 role 和 status 列
- **THEN** 所有现有用户记录 role 默认为 `USER`，status 默认为 `ACTIVE`

### Requirement: JWT 认证过滤器读取角色和状态

系统 MUST 在 JwtAuthenticationFilter 中从数据库查询 User 的 role 和 status，构建带 GrantedAuthority 的 Authentication。非 ACTIVE 状态的用户 MUST NOT 设置 Authentication。

#### Scenario: ACTIVE 状态用户请求受保护接口

- **WHEN** 携带有效 JWT token 的 ACTIVE 状态用户请求受保护接口
- **THEN** 系统设置 Authentication，authorities 包含 `ROLE_<角色名>`

#### Scenario: PENDING 状态用户请求受保护接口

- **WHEN** 携带有效 JWT token 的 PENDING 状态用户请求受保护接口
- **THEN** 系统不设置 Authentication，等同于未认证，返回 401

#### Scenario: DISABLED 状态用户请求受保护接口

- **WHEN** 携带有效 JWT token 的 DISABLED 状态用户请求受保护接口
- **THEN** 系统不设置 Authentication，返回 401
