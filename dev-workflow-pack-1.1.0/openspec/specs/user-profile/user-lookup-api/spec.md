# User Public Lookup API

## Purpose

TBD - 用户公开查询 API

## Requirements

### Requirement: 用户公开查询 API

#### Scenario 1: 公开查询其他用户
- GIVEN: 已登录用户 `currentUser.id=1` 想查看 `id=2` 的公开信息
- WHEN: 客户端请求 `GET /api/v1/users/2`
- THEN: 返回 `200 OK`，body `{ code: 200, data: { id: 2, username: "wangbao", nickname: "王宝", avatarUrl: "/api/v1/static/avatars/2.jpg?v=...", createdAt: "..." } }`

#### Scenario 2: 公开查询不返回敏感字段
- GIVEN: 请求 `GET /api/v1/users/2`
- WHEN: 服务端处理
- THEN: 响应中**不包含** `password`、`email`（如有）、`lastLoginAt`（属于隐私）

#### Scenario 3: 用户不存在
- GIVEN: 数据库中无 `id=99999`
- WHEN: 请求 `GET /api/v1/users/99999`
- THEN: 返回 404，错误信息"用户不存在"

#### Scenario 4: 不需要鉴权
- GIVEN: 未登录客户端
- WHEN: 请求 `GET /api/v1/users/2`
- THEN: 返回 200 + 公开信息（公开信息不需鉴权）

#### Scenario 5: 路径参数非法
- GIVEN: 请求 `GET /api/v1/users/abc`（非数字）
- WHEN: 服务端处理
- THEN: 返回 400，错误信息"无效的用户 ID"
