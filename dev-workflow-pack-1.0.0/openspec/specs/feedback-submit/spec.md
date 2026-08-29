## ADDED Requirements（新增需求）

### Requirement: 用户可提交留言
系统必须提供 REST API 端点接受用户提交的留言。留言内容（content）为必填字段，昵称（nickname）、联系方式（contact）和分类（category）为可选字段。

#### Scenario: 匿名用户成功提交留言
- **WHEN** 未登录用户发送 POST /api/v1/feedback，请求体包含 content="建议增加暗色模式" 和 nickname="路人"
- **THEN** 系统创建一条 feedback_message 记录，user_id 为 null，ip_hash 为请求 IP 的 SHA-256 值，返回 201 Created 和留言数据

#### Scenario: 已登录用户提交留言
- **WHEN** 已登录用户发送 POST /api/v1/feedback，携带有效 Bearer token，请求体包含 content="文件上传偶尔失败"
- **THEN** 系统创建一条 feedback_message 记录，user_id 关联当前用户，nickname 自动取自用户 nickname 字段，ip_hash 为 null，返回 201 Created

#### Scenario: 留言内容为空时拒绝提交
- **WHEN** 用户发送 POST /api/v1/feedback，请求体 content 为空字符串或缺失
- **THEN** 系统返回 400 Bad Request，不创建记录

#### Scenario: 用户输入包含 XSS 内容
- **WHEN** 用户发送 POST /api/v1/feedback，content 包含 `<script>alert(1)</script>`
- **THEN** 系统通过 XssSanitizer 清洗内容后存储，返回 201 Created，存储内容不含 script 标签

#### Scenario: 分类字段使用预定义枚举值
- **WHEN** 用户提交留言，category 为 "SUGGESTION"、"BUG_REPORT"、"PRAISE" 或 "OTHER" 之一
- **THEN** 系统接受并存储该分类值

#### Scenario: 未提供分类时使用默认值
- **WHEN** 用户提交留言，未提供 category 字段
- **THEN** 系统使用默认分类 "SUGGESTION"
