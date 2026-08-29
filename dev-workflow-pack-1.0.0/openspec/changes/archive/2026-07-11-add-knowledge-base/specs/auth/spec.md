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
