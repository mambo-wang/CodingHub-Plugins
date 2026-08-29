# Avatar Upload API

## Purpose

TBD - 头像上传 API

## Requirements

### Requirement: 头像上传 API

#### Scenario 1: 上传头像成功 - JPG
- GIVEN: 已登录用户上传 `avatar.jpg`（1.5MB, image/jpeg）
- WHEN: 客户端 `POST /api/v1/users/me/avatar`（multipart/form-data, field=avatar）
- THEN: 返回 `200 OK`，body `{ code: 200, message: "头像上传成功", data: { avatarUrl: "/api/v1/static/avatars/{userId}.jpg?v={timestamp}" } }`；文件落地 `~/aifiles/avatars/{userId}.jpg`

#### Scenario 2: 上传头像成功 - PNG
- GIVEN: 已登录用户上传 `avatar.png`（500KB, image/png）
- WHEN: `POST /api/v1/users/me/avatar`
- THEN: 返回 200 + URL 指向 `.png`

#### Scenario 3: 上传头像成功 - WebP
- GIVEN: 上传 `avatar.webp`（300KB, image/webp）
- WHEN: 调用上传接口
- THEN: 返回 200 + URL 指向 `.webp`

#### Scenario 4: 上传头像成功 - GIF
- GIVEN: 上传 `avatar.gif`（800KB, image/gif）
- WHEN: 调用上传接口
- THEN: 返回 200 + URL 指向 `.gif`

#### Scenario 5: 上传失败 - 格式非法（PDF）
- GIVEN: 上传 `evil.pdf`（1MB, application/pdf）
- WHEN: 调用上传接口
- THEN: 返回 `400 Bad Request`，错误信息"仅支持 jpg / png / webp / gif 格式"

#### Scenario 6: 上传失败 - 格式非法（SVG 拒绝）
- GIVEN: 上传 `pic.svg`（10KB, image/svg+xml）
- WHEN: 调用上传接口
- THEN: 返回 400，错误信息"出于安全考虑，不支持 SVG 格式"（SVG 可携带脚本）

#### Scenario 7: 上传失败 - 文件超大（> 2MB）
- GIVEN: 上传 `big.jpg`（3MB, image/jpeg）
- WHEN: 调用上传接口
- THEN: 返回 `413 Payload Too Large`，错误信息"头像文件不能超过 2MB"

#### Scenario 8: 上传失败 - 未登录
- GIVEN: 客户端无有效 token
- WHEN: 调用 `POST /api/v1/users/me/avatar`
- THEN: 返回 `401 Unauthorized`

#### Scenario 9: 上传失败 - 缺文件
- GIVEN: multipart 请求但未携带 `avatar` 字段
- WHEN: 调用上传接口
- THEN: 返回 400，错误信息"请选择头像文件"

#### Scenario 10: 重复上传 - 覆盖旧文件
- GIVEN: 用户已上传 `old.png`
- WHEN: 再次上传 `new.jpg`
- THEN: 旧文件从磁盘删除（或被覆盖）；user 表 `avatar_url` 更新为 `.jpg` 后缀；`updated_at` 更新

#### Scenario 11: 上传后 updatedAt 变化
- GIVEN: 用户上传头像前 `updated_at=2026-06-01T00:00:00Z`
- WHEN: 上传成功
- THEN: 同一 user 记录的 `updated_at` 更新为当前时间（用于前端缓存破坏）

#### Scenario 12: 返回的 avatarUrl 带版本号
- GIVEN: 用户上传头像后 `updated_at=2026-06-10T10:00:00Z`
- WHEN: 客户端拿到响应
- THEN: `data.avatarUrl` 形如 `/api/v1/static/avatars/3.jpg?v=1718013600000`，毫秒时间戳作为 query param
