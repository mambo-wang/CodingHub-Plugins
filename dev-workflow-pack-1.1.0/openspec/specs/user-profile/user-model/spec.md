# User Model - Avatar Field

## Purpose

TBD - 用户模型头像字段

## Requirements

### Requirement: 用户头像字段

#### Scenario 1: User 实体新增 avatarUrl 字段
- GIVEN: 数据库中 `user` 表当前只有 `id / username / nickname / password / created_at / updated_at / last_login_at` 字段
- WHEN: 执行数据库迁移 `V20260610__add_user_avatar.sql`
- THEN: `user` 表新增 `avatar_url VARCHAR(255) NULL` 列；老用户的 `avatar_url` 全部为 `NULL`

#### Scenario 2: User 实体可读写 avatarUrl
- GIVEN: 已迁移的数据库 + `User` 实体
- WHEN: `User` 实体 `setAvatarUrl("https://example.com/x.jpg")` 后再 `getAvatarUrl()`
- THEN: 返回 `"https://example.com/x.jpg"`

#### Scenario 3: 未上传头像用户
- GIVEN: 数据库中老用户 `id=1, username="olduser", avatar_url=NULL`
- WHEN: 前端通过 `GET /api/v1/users/1` 获取用户信息
- THEN: 返回 JSON 中 `avatarUrl: null`

#### Scenario 4: 已上传头像用户
- GIVEN: 用户 `id=2` 上传过头像，user 表 `avatar_url="/api/v1/static/avatars/2"`，`updated_at=2026-06-10T10:00:00Z`
- WHEN: 前端调用 `GET /api/v1/users/2`
- THEN: 返回 JSON 中 `avatarUrl: "/api/v1/static/avatars/2?v=1718013600000"`

#### Scenario 5: 头像 URL 不唯一
- GIVEN: 数据库中两个用户都上传了头像
- WHEN: 检查 user 表索引
- THEN: `avatar_url` 字段没有 `UNIQUE` 约束（每用户一份，无重复需求）

#### Scenario 6: 重新上传覆盖
- GIVEN: 用户 `id=3` 已上传头像 `old.jpg`
- WHEN: 用户上传新文件 `new.png`
- THEN: 旧文件 `old.jpg` 被覆盖或删除；user 表 `avatar_url` 更新为 `/api/v1/static/avatars/3.png`；`updated_at` 更新为当前时间

#### Scenario 7: 注册时不强制头像
- GIVEN: 新用户提交注册 `username="newuser"`, `nickname="新人"`, `password=***`
- WHEN: `POST /api/v1/auth/register` 调用成功
- THEN: user 表中新增记录的 `avatar_url` 为 `NULL`
