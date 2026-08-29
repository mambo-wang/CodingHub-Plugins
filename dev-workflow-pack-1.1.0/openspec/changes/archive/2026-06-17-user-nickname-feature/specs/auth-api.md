# Auth API - Nickname Registration

## ADDED Requirements

### Scenario 1: 注册成功 - 包含昵称

- GIVEN: 新用户注册信息，username="wangbao", nickname="王宝", password=***
- WHEN: 用户提交 POST /api/auth/register 请求
- THEN: 系统返回 201 状态码，用户信息包含 username 和 nickname，accessToken 和 refreshToken

### Scenario 2: 注册失败 - 昵称重复

- GIVEN: 数据库中已存在用户，username="user1", nickname="王宝"
- WHEN: 新用户提交注册请求，username="user2", nickname="王宝"
- THEN: 系统返回 400 状态码，错误信息"昵称已被使用"

### Scenario 3: 注册失败 - 昵称长度不足

- GIVEN: 新用户注册信息，username="newuser", nickname="A", password=***
- WHEN: 用户提交注册请求
- THEN: 系统返回 400 状态码，错误信息"昵称长度需在2-10字符之间"

### Scenario 4: 注册失败 - 用户名重复

- GIVEN: 数据库中已存在用户 username="existing"
- WHEN: 新用户提交注册请求，username="existing", nickname="新昵称"
- THEN: 系统返回 400 状态码，错误信息"用户名已被注册"

### Scenario 5: 登录返回用户昵称

- GIVEN: 数据库中用户 username="wangbao", nickname="王宝"
- WHEN: 用户提交登录请求，username="wangbao", password=***
- THEN: 系统返回用户信息包含 nickname="王宝"

### Scenario 6: 获取当前用户信息包含昵称

- GIVEN: 用户已登录，token 有效
- WHEN: 用户发送 GET /api/users/me 请求
- THEN: 系统返回用户信息包含 nickname 字段