# Proposal

## Problem

1. 当前登录使用邮箱 + 密码，但用户记忆时账号比邮箱更方便
2. 注册时密码规则过于复杂（要求大小写字母和数字），导致用户体验差
3. 工具分类中存在 `API` 类型需要移除

## Testable Behaviors

### 认证相关

- WHEN `LoginRequest(username, password)` 被调用 THEN 验证通过后返回登录凭证
- WHEN `RegisterRequest(username, password)` 被调用且密码长度 >= 6 THEN 注册成功返回用户信息
- WHEN `RegisterRequest(username, password)` 被调用且密码长度 < 6 THEN 返回校验错误信息

### 工具分类相关

- WHEN 查询分类列表 THEN 返回不包含 `API` 类型的分类列表
- WHEN 查询工具列表 THEN 只返回 Skill、MCP、Prompt、其他 类型工具

## Acceptance Criteria

1. 用户可以使用用户名（而非邮箱）登录系统
2. 注册时密码长度 >= 6 位即可，无其他复杂度要求
3. 工具分类中移除 `API` 类型，保留 Skill、MCP、Prompt、其他
4. 数据库 user 表需添加 username 字段并设为唯一索引
5. 前端登录/注册表单相应调整