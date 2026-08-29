# Proposal

## Problem

当前平台用户注册和登录只使用 username（账号），缺少昵称（nickname）功能。用户无法自定义展示名称，工具和帖子的作者信息只能显示账号，显示体验不够友好。用户需要一个可自定义的昵称来提升个人展示形象。

## Context

平台现有用户体系：
- 注册时只填写 username（账号）和 password
- 用户信息存储在 User 模型中，仅有 id、username 字段
- 工具和帖子的作者字段为 uploaderUsername / authorUsername

用户期望：
- 注册时可以设置一个好记的昵称
- 登录后右上角显示昵称而非账号
- 作者信息展示"昵称(账号)"格式，如"王宝(wangbao)"

## Testable Behaviors

- WHEN 用户注册 THEN 需同时输入 username 和 nickname（昵称）
- WHEN username 或 nickname 重复 THEN 注册表单提示错误信息
- WHEN 注册成功 THEN 用户可使用 username 或 nickname 登录
- WHEN 用户登录后 THEN 右上角显示用户昵称（未设置则显示账号）
- WHEN 工具详情页展示作者 THEN 显示格式为"昵称(账号)"，如"王宝(wangbao)"
- WHEN 帖子详情页展示作者 THEN 显示格式为"昵称(账号)"，如"王宝(wangbao)"
- WHEN 用户未设置昵称 THEN 降级显示账号
- WHEN Hover 作者信息 THEN Tooltip 提示完整信息

## Design

### 注册页面

表单字段：
- Username（账号）：必填，4-20字符，字母数字下划线
- Nickname（昵称）：必填，2-10字符，中文/字母/数字/中文标点
- Password（密码）：必填，最少6字符

### 右上角用户信息

显示优先级：
1. 已设置昵称 → 显示"昵称"
2. 未设置昵称 → 显示"账号"

### 作者信息展示

格式：`昵称(账号)` 或 `账号（未设置昵称时）`

示例：
- 已设置昵称：王宝(wangbao)
- 未设置昵称：wangbao

### API 变更

**User 模型新增字段：**
```json
{
  "id": 1,
  "username": "wangbao",
  "nickname": "王宝",
  "createdAt": "2026-01-01T00:00:00Z",
  "lastLoginAt": "2026-06-01T00:00:00Z"
}
```

**注册接口变更：**
- POST /api/auth/register
- Request: `{ username, nickname, password }`
- Response: `{ code: 200, data: { user, accessToken, refreshToken } }`

**获取当前用户信息：**
- GET /api/users/me
- Response: 包含 nickname 字段

**修改昵称（可选，后续功能）：**
- PUT /api/users/me
- Request: `{ nickname: "新昵称" }`

## Acceptance Criteria

1. **注册流程**：注册表单新增 nickname 字段，必填
2. **登录流程**：登录后返回用户信息包含 nickname
3. **前端存储**：User 类型扩展包含 nickname 字段
4. **右上角展示**：登录后头部显示用户昵称，未设置显示账号
5. **工具详情页**：作者信息展示"昵称(账号)"格式
6. **帖子详情页**：作者信息展示"昵称(账号)"格式
7. **向后兼容**：未设置昵称的老用户正常显示账号
8. **昵称唯一性**：昵称不可重复，后端做唯一性校验

## Scope

**后端：**
- [ ] User 模型新增 nickname 字段
- [ ] 注册接口添加 nickname 参数校验
- [ ] 登录接口返回 nickname
- [ ] /me 接口返回 nickname
- [ ] 昵称唯一性校验

**前端：**
- [ ] User 类型扩展 nickname 字段
- [ ] 注册页面表单新增 nickname 输入框
- [ ] 右上角用户信息显示昵称
- [ ] 工具详情页作者信息格式化显示
- [ ] 帖子详情页作者信息格式化显示

## Out of Scope

- 昵称修改功能（后续迭代）
- 昵称敏感词过滤（后续迭代）
- 头像功能（独立迭代）
