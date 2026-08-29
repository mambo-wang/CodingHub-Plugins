# Proposal: User Avatar (用户头像) 功能

## Problem

平台当前 `User` 模型和前端展示都没有头像（avatar）能力。`AppHeader.vue` 用一个紫色圆形 + username 首字母充当占位头像（`L69-71`），但：

- `AuthorBadge.vue`（工具/帖子作者标识）完全没有头像位，只显示文字
- 用户在工具详情、帖子列表、评论里看到的"作者"是清一色文字，无法视觉区分不同作者
- 工具广场首页/概览页的统计卡片没有头像展示
- 用户没有"个人资料页"管理自己的展示信息

随着 user-nickname-feature 落地、论坛和工具广场活跃度上升，**视觉身份识别**已经变成可用性瓶颈。

## Context

**已有基础设施**（可直接复用，不重造）：

| 资产 | 位置 | 复用点 |
|---|---|---|
| 文件上传基座 | `UploadConfig.java` | `~/aifiles` 目录、最大 50MB / 200MB |
| 文件表 `tool_file` | 数据库 | 命名规则可参考（id/原名/路径/大小/MIME） |
| 静态服务 | `StaticController.java` | 已有 `/api/v1/readme` 模式，可加 `/api/v1/static/avatars/{id}` |
| 昵称 + 唯一索引 | `User.java` `L14` | 头像 URL 不需唯一（每用户一个） |
| 用户 store | `stores/auth.ts` | 新增 `avatarUrl` 字段持久化到 localStorage |
| 主题系统 | `main.css` + `useThemeStore` | 双主题适配免写 |

**已有的"未上传头像"兜底**：
- `AppHeader.vue:70` 当前用 `username?.charAt(0).toUpperCase()` + 紫蓝渐变背景
- 推荐升级为**首字母 + 基于 userId 哈希的 6 色配色**，让无头像用户也有视觉差异

**已有"用户管理容器"缺口**：
- 没有 `ProfilePage.vue`，`/me/*` 路由只挂了 `MyToolsPage`（管理工具）
- 头像上传 UI、昵称修改、密码修改都需要一个统一的"个人资料"容器
- 建议本次顺带补 `ProfilePage.vue` + 路由 `/me/profile`

**Out of Scope**（明确划在本次之外）：
- 第三方登录头像（GitHub OAuth 等）
- 头像历史版本（用户换头像后只保留最新一张）
- 头像审核 / NSFW 过滤（社区体量未到这一步）
- 群组头像、组织头像
- Gravatar 集成（user 表尚无 email 字段）

## Testable Behaviors

### 后端

1. **WHEN** `POST /api/v1/users/me/avatar` 接收 multipart/form-data 上传（jpg/png/webp/gif，≤2MB）
   **THEN** 服务端校验通过后，文件存到 `~/aifiles/avatars/{userId}.{ext}`，返回 `{ code: 200, data: { avatarUrl: "/api/v1/static/avatars/{userId}?v={updatedAt-millis}" } }`

2. **WHEN** `POST /api/v1/users/me/avatar` 上传非白名单格式（exe/pdf/svg 等）
   **THEN** 返回 400 错误，提示"仅支持 jpg / png / webp / gif 格式"

3. **WHEN** `POST /api/v1/users/me/avatar` 上传文件 > 2MB
   **THEN** 返回 413 错误，提示"头像文件不能超过 2MB"

4. **WHEN** 用户未登录访问 `POST /api/v1/users/me/avatar`
   **THEN** 返回 401 错误

5. **WHEN** `GET /api/v1/users/me` 获取当前用户信息
   **THEN** 返回体包含 `avatarUrl` 字段（已上传则为带版本号的 URL，未上传则为 `null`）

6. **WHEN** `GET /api/v1/users/{id}` 获取指定用户公开信息
   **THEN** 返回体包含 `avatarUrl` 字段

7. **WHEN** `GET /api/v1/static/avatars/{userId}` 请求头像资源
   **THEN** 找到文件返回 200 + `image/*` 资源；用户未上传时返回 404；用户不存在时返回 404

8. **WHEN** 用户再次上传头像覆盖旧文件
   **THEN** 旧文件被新文件替换，user 表 `updatedAt` 被更新（用于 URL 缓存破坏）

9. **WHEN** 数据库迁移执行
   **THEN** 老用户（`avatar_url IS NULL`）`GET /me` 返回 `avatarUrl: null`，前端走首字母兜底

10. **WHEN** 用户注册（`POST /api/v1/auth/register`）
    **THEN** 不强制要求头像；新用户 `avatarUrl` 默认为 `null`

11. **WHEN** 头像静态资源被请求
    **THEN** 不需要鉴权（头像属于公开可见信息）

### 前端

12. **WHEN** 用户访问 `/me/profile` 且未登录
    **THEN** 重定向到 `/login` 并保留 redirect 参数

13. **WHEN** 用户在个人资料页点击"上传头像"并选择合法图片
    **THEN** 调用 `POST /api/v1/users/me/avatar`，成功后将响应里的 `avatarUrl` 更新到 `authStore.user.avatarUrl`，UI 立即反映新头像

14. **WHEN** 用户上传头像时遇到 4xx/5xx 错误
    **THEN** 显示 `role="alert"` 错误提示（中文），且不清空旧头像

15. **WHEN** 任意页面渲染 `AppHeader` 的右上角用户信息
    **THEN** `authStore.user.avatarUrl` 不为空时显示 `<img>` 圆形头像；为空时显示首字母 + 哈希色块

16. **WHEN** `AuthorBadge` 接收 `avatarUrl` prop
    **THEN** 优先显示圆形头像缩略图（24px / 32px / 40px 三档），未传时退化到文字徽章

17. **WHEN** 用户在 `/me/profile` 看到自己的头像预览
    **THEN** 展示 128×128 圆形预览，下方有"上传 / 移除"两个按钮

18. **WHEN** 用户在移动端（< 640px）访问 `/me/profile`
    **THEN** 头像预览 + 表单上下堆叠，间距符合 `var(--space-md)`

19. **WHEN** 用户在浅色/深色主题下查看头像
    **THEN** 头像容器边框、阴影、焦点环都跟随主题切换；头像图片本身不随主题变化（用户上传什么就显示什么）

20. **WHEN** 头像加载失败（404、损坏图片）
    **THEN** `onerror` 降级到首字母 + 哈希色块，不显示破图占位

21. **WHEN** 任何带 `avatarUrl` 的组件首次挂载
    **THEN** 头像 URL 末尾带 `?v={updatedAt}` 查询参数（缓存破坏），切换头像后能即时刷新

## Acceptance Criteria

### 数据层

- [ ] `user` 表新增 `avatar_url VARCHAR(255) NULL` 字段
- [ ] 数据库迁移脚本：`V20260610__add_user_avatar.sql`
- [ ] 老用户迁移后 `avatar_url` 全部为 `NULL`，应用层零感知

### 后端

- [ ] `User.java` 实体新增 `avatarUrl` 字段
- [ ] `UserDTO.java` 新增 `avatarUrl` 字段
- [ ] `UploadConfig.java` 新增 `avatarSubdir` / `avatarMaxSize` 配置项（默认 `avatars` / `2MB`）
- [ ] `UserController` 新增 `POST /api/v1/users/me/avatar` 接口
- [ ] `UserController` 新增 `GET /api/v1/users/{id}` 公开信息接口
- [ ] `UserService` 新增 `uploadAvatar(userId, MultipartFile)` 方法
- [ ] `UserService` 新增 `getPublicProfile(userId)` 方法
- [ ] `StaticController` 或新 `AvatarController` 提供 `GET /api/v1/static/avatars/{userId}` 公开资源
- [ ] 头像格式白名单：jpg / jpeg / png / webp / gif
- [ ] 头像大小上限：2MB
- [ ] 头像存储路径：`~/aifiles/avatars/{userId}.{ext}`（不含随机后缀，userId 唯一即可）
- [ ] 上传后更新 user 的 `updatedAt`（用于缓存破坏）
- [ ] 完整测试覆盖：上传成功 / 格式非法 / 超大 / 未登录 / 不存在的 userId

### 前端

- [ ] `types/index.ts` 的 `User` 接口新增 `avatarUrl?: string | null`
- [ ] `UserAvatar.vue` 通用组件（封装 `<img>` + 错误降级 + 哈希色块兜底）
- [ ] `AuthorBadge.vue` 扩展 `avatarUrl` 和 `avatarSize` props
- [ ] `AppHeader.vue` 右上角改用 `UserAvatar` 组件
- [ ] `stores/auth.ts` 的 `User` 类型同步，`setUser` 持久化 `avatarUrl`
- [ ] 新增 `pages/ProfilePage.vue` + 路由 `/me/profile`
- [ ] `router/index.ts` 注册 `/me/profile` 路由（`requiresAuth: true`）
- [ ] `AppHeader` 用户菜单新增"个人资料"入口（跳转 `/me/profile`）
- [ ] 上传组件支持图片预览（FileReader 读 base64）、格式校验、大小校验
- [ ] 上传按钮 Loading 状态（防重复提交）
- [ ] 双主题适配：所有头像容器使用 CSS 变量，支持暗色/亮色切换
- [ ] `aria-label`、`alt` 文本完善

### 非功能性

- [ ] 静态服务带 `Cache-Control: public, max-age=3600`（CDN/浏览器友好）
- [ ] URL 缓存破坏：`?v={updatedAt.getTime()}` 防止换头像不刷新
- [ ] 错误降级：`onerror` 切回首字母兜底
- [ ] 移动端（< 640px）布局可用
- [ ] 焦点环、键盘可达、屏幕阅读器友好
- [ ] 旧用户零数据迁移成本（`avatar_url = NULL` 直接走兜底）

## Scope

### 后端

- [ ] `User` 实体加 `avatarUrl` 字段
- [ ] 数据库迁移脚本
- [ ] `UserDTO` 加 `avatarUrl` 字段
- [ ] `UserService.uploadAvatar(userId, file)` 实现
- [ ] `UserService.getPublicProfile(userId)` 实现
- [ ] `UserService.getCurrentUser(userId)` 返回 `avatarUrl`
- [ ] `UserController` 头像上传 + 公开信息接口
- [ ] 静态服务 `/api/v1/static/avatars/{userId}`
- [ ] 单元测试 + 集成测试

### 前端

- [ ] `User` 类型扩展
- [ ] `UserAvatar.vue` 通用头像组件（含哈希色块降级）
- [ ] `AuthorBadge.vue` 接入头像
- [ ] `AppHeader.vue` 改用 `UserAvatar`
- [ ] `ProfilePage.vue` 头像上传 UI
- [ ] 路由注册 + 导航入口
- [ ] 组件级测试

### 跨端

- [ ] 双主题视觉验收
- [ ] 移动端响应式验收
- [ ] 错误状态 / 加载状态验收

## Out of Scope

- 头像历史版本与回滚
- 头像 CDN 加速（先走本地静态服务，体量到再上 CDN）
- 头像裁剪 / 滤镜（让用户上传前自己用工具裁好）
- 头像审核 / NSFW 检测
- Gravatar 集成
- 群组 / 组织头像
- 第三方登录头像拉取
- 头像性能优化（WebP 自动转换等，后续专项）

---

**提议作者**: AI Agent（基于 explore-mode 探索推荐）
**目标版本**: CodingHub v0.x
**关联变更**: `user-nickname-feature`（提供昵称基础）、`update-auth-fields`
**预计影响面**: L1（修改 user 表 schema + 新增 2 个 API 端点；前端影响 4 个组件 / 新增 2 个文件）
