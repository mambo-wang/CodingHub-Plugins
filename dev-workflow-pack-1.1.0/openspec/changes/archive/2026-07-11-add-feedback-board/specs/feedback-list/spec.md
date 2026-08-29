## ADDED Requirements（新增需求）

### Requirement: 用户可分页查询留言列表
系统必须提供 REST API 端点返回留言列表，支持分页和按分类筛选。列表按创建时间倒序排列。仅展示 status=NORMAL 的留言。

#### Scenario: 查询留言列表默认分页
- **WHEN** 用户发送 GET /api/v1/feedback（无需认证）
- **THEN** 系统返回分页的留言列表，默认每页 20 条，按 created_at 倒序排列，包含留言内容、昵称、分类、创建时间和管理员回复（如有）

#### Scenario: 按分类筛选留言
- **WHEN** 用户发送 GET /api/v1/feedback?category=BUG_REPORT
- **THEN** 系统仅返回 category 为 BUG_REPORT 的留言

#### Scenario: 分页查询第二页
- **WHEN** 用户发送 GET /api/v1/feedback?page=1&size=10
- **THEN** 系统返回第 11-20 条留言，响应包含总记录数和总页数

#### Scenario: 已软删除的留言不展示
- **WHEN** 数据库中存在 status=DELETED 的留言
- **THEN** GET /api/v1/feedback 不返回这些记录

#### Scenario: 匿名留言不暴露 IP 信息
- **WHEN** 查询匿名提交的留言
- **THEN** 响应中不包含 ip_hash 和 user_id 字段，仅展示 nickname
