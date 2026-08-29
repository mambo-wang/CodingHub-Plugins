## MODIFIED Requirements

### Requirement: 用户昵称字段

#### Scenario 1: 用户注册时设置昵称
- GIVEN: 新用户注册信息，username="wangbao", nickname="王宝", password=***, role="USER"
- WHEN: 系统创建用户记录
- THEN: User 模型包含 nickname="王宝" 字段，role="USER", status="ACTIVE"

#### Scenario 2: 用户未设置昵称时显示账号
- GIVEN: 数据库中存在老用户，只有 username="olduser"，nickname 为 NULL
- WHEN: 前端展示用户信息
- THEN: 显示 "olduser"（降级显示账号）

#### Scenario 3: 昵称唯一性约束
- GIVEN: 数据库中已存在 nickname="王宝" 的用户
- WHEN: 新用户注册时尝试使用 nickname="王宝"
- THEN: 系统返回 400 错误，提示"昵称已被使用"

#### Scenario 4: 昵称长度验证
- GIVEN: 新用户注册信息，username="newuser", nickname="A"（长度1）
- WHEN: 用户提交注册请求
- THEN: 系统返回 400 错误，提示"昵称长度需在2-10字符之间"

#### Scenario 5: 昵称格式验证
- GIVEN: 新用户注册信息，username="newuser", nickname="test<Script>"（包含特殊字符）
- WHEN: 用户提交注册请求
- THEN: 系统对 nickname 进行 XSS 过滤或返回 400 错误

## ADDED Requirements

### Requirement: 用户角色字段

User 实体 MUST 包含 role 字段，类型为枚举（USER / ADMIN / SUPER_ADMIN），存储为字符串，不可为空。

#### Scenario: User 实体包含 role 字段

- **WHEN** 系统创建 User 实体
- **THEN** User 包含 role 字段，类型为枚举，使用 @Enumerated(EnumType.STRING) 映射

#### Scenario: role 字段不可为空

- **WHEN** 尝试创建 role 为 null 的 User 记录
- **THEN** 系统抛出约束违例异常

### Requirement: 用户账号状态字段

User 实体 MUST 包含 status 字段，类型为枚举（ACTIVE / PENDING / REJECTED / DISABLED），存储为字符串，不可为空。

#### Scenario: User 实体包含 status 字段

- **WHEN** 系统创建 User 实体
- **THEN** User 包含 status 字段，类型为枚举，使用 @Enumerated(EnumType.STRING) 映射

#### Scenario: status 字段不可为空

- **WHEN** 尝试创建 status 为 null 的 User 记录
- **THEN** 系统抛出约束违例异常

#### Scenario: 数据库迁移添加 role 和 status 列

- **WHEN** 执行数据库迁移脚本
- **THEN** user 表新增 role VARCHAR(20) NOT NULL DEFAULT 'USER' 和 status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' 列
