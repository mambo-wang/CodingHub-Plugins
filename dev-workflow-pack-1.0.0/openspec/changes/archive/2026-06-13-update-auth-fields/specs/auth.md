# Auth Spec

## Scenarios

### Scenario 1: 用户使用用户名登录

- GIVEN: 用户已注册，用户名为 "testuser"，密码为 "password123"
- WHEN: 用户提交登录请求，username="testuser", password="password123"
- THEN: 系统返回 JWT token 和用户信息，登录成功

### Scenario 2: 登录密码错误

- GIVEN: 用户已注册，用户名为 "testuser"，密码为 "password123"
- WHEN: 用户提交登录请求，username="testuser", password="wrongpassword"
- THEN: 系统返回 401 错误，提示"用户名或密码错误"

### Scenario 3: 登录用户不存在

- GIVEN: 数据库中不存在用户名为 "nonexistent" 的用户
- WHEN: 用户提交登录请求，username="nonexistent", password="password123"
- THEN: 系统返回 401 错误，提示"用户名或密码错误"

### Scenario 4: 注册密码长度不足

- GIVEN: 新用户注册信息，用户名为 "newuser"
- WHEN: 用户提交注册请求，密码为 "12345"（长度 5）
- THEN: 系统返回 400 错误，提示"密码长度至少6位"

### Scenario 5: 注册成功

- GIVEN: 新用户注册信息，用户名为 "newuser"
- WHEN: 用户提交注册请求，密码为 "password"（长度 >= 6）
- THEN: 系统返回 201 状态码，创建用户成功

### Scenario 6: 注册用户名已存在

- GIVEN: 数据库中已存在用户名为 "existinguser" 的用户
- WHEN: 新用户提交注册请求，用户名为 "existinguser"，密码为 "password123"
- THEN: 系统返回 400 错误，提示"用户名已被注册"