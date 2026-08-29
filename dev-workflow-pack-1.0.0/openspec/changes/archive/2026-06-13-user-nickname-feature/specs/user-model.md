# User Model - Nickname Field

## ADDED Requirements

### Scenario 1: 用户注册时设置昵称

- GIVEN: 新用户注册信息，username="wangbao", nickname="王宝", password=***
- WHEN: 系统创建用户记录
- THEN: User 模型包含 nickname="王宝" 字段

### Scenario 2: 用户未设置昵称时显示账号

- GIVEN: 数据库中存在老用户，只有 username="olduser"，nickname 为 NULL
- WHEN: 前端展示用户信息
- THEN: 显示 "olduser"（降级显示账号）

### Scenario 3: 昵称唯一性约束

- GIVEN: 数据库中已存在 nickname="王宝" 的用户
- WHEN: 新用户注册时尝试使用 nickname="王宝"
- THEN: 系统返回 400 错误，提示"昵称已被使用"

### Scenario 4: 昵称长度验证

- GIVEN: 新用户注册信息，username="newuser", nickname="A"（长度1）
- WHEN: 用户提交注册请求
- THEN: 系统返回 400 错误，提示"昵称长度需在2-10字符之间"

### Scenario 5: 昵称格式验证

- GIVEN: 新用户注册信息，username="newuser", nickname="test<Script>"（包含特殊字符）
- WHEN: 用户提交注册请求
- THEN: 系统对 nickname 进行 XSS 过滤或返回 400 错误