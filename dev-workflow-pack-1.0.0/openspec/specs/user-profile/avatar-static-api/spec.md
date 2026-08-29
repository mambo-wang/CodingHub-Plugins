# Avatar Static Resource API

## Purpose

TBD - 头像静态资源访问 API

## Requirements

### Requirement: 头像静态资源 API

#### Scenario 1: 公开访问头像资源 - 已上传
- GIVEN: 用户 `id=2` 已上传头像，文件存在 `~/aifiles/avatars/2.jpg`
- WHEN: 任意客户端（含未登录）请求 `GET /api/v1/static/avatars/2`
- THEN: 返回 `200 OK`，`Content-Type: image/jpeg`，body 为图片字节流，`Cache-Control: public, max-age=3600`

#### Scenario 2: 公开访问 - 未上传
- GIVEN: 用户 `id=5` 未上传头像，磁盘无 `5.*` 文件
- WHEN: 请求 `GET /api/v1/static/avatars/5`
- THEN: 返回 `404 Not Found`

#### Scenario 3: 公开访问 - 用户不存在
- GIVEN: 数据库中无 `id=99999` 的用户
- WHEN: 请求 `GET /api/v1/static/avatars/99999`
- THEN: 返回 404（不应区分"用户不存在"和"未上传"，避免枚举攻击）

#### Scenario 4: 不需要鉴权
- GIVEN: 未登录客户端
- WHEN: 请求 `GET /api/v1/static/avatars/2`
- THEN: 返回 200（头像属于公开信息，无需 token）

#### Scenario 5: 文件名后缀协商
- GIVEN: 用户 `id=2` 上传的是 `2.png`
- WHEN: 请求 `/api/v1/static/avatars/2`（不带后缀）
- THEN: 后端尝试 `2.jpg / 2.jpeg / 2.png / 2.webp / 2.gif` 顺序探测，返回第一个存在的文件

#### Scenario 6: 拒绝路径穿越
- GIVEN: 攻击者请求 `/api/v1/static/avatars/..%2F..%2Fetc%2Fpasswd`
- WHEN: 后端处理
- THEN: 返回 400 或 404，禁止跳出 `~/aifiles/avatars/` 目录
