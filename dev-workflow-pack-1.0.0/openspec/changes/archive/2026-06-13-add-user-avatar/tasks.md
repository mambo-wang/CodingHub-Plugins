# Tasks: User Avatar Feature

## Impact Analysis Status

- 状态：已生成（`impact-analysis.md`）
- 跳过原因：N/A
- 参考 `impact-analysis.md` 的调用图、受影响测试、回归建议和设计修正建议。

---

## A. Atomic TDD Task List

### 数据库迁移

#### Feature: user 表添加 avatar_url 列

- [ ] RED: 编写集成测试——断言 `User` 实体 `getAvatarUrl()` 默认返回 `null`
- [ ] GREEN: 创建迁移脚本 `V20260610__add_user_avatar.sql`，执行 `ALTER TABLE user ADD COLUMN avatar_url VARCHAR(255) NULL`
- [ ] GREEN: `User.java` 实体添加 `@Column(name = "avatar_url", length = 255) private String avatarUrl;` 字段
- [ ] REFACTOR: 清理测试代码

### 后端：头像工具与配置

#### Feature: UploadConfig 新增头像专属配置

- [ ] RED: 编写 `UploadConfigTest`——断言 `getAvatarSubdir()=="avatars"`, `getAvatarMaxFileSize()=="2MB"`, `getAvatarAllowedExtensions()` 包含 jpg/png/webp/gif
- [ ] GREEN: `UploadConfig.java` 新增 `avatarSubdir / avatarMaxFileSize / avatarAllowedExtensions` 三个属性 + `@PostConstruct` 创建子目录
- [ ] REFACTOR: 清理测试代码

#### Feature: AvatarUtil 文件名校验与 MIME 探测

- [ ] RED: 编写 `AvatarUtilTest`——覆盖：合法扩展名(jpg/png/webp/gif) → 返回 ext；非法 (pdf/exe) → 抛 `AvatarValidationException`；SVG → 抛"出于安全考虑"；空文件 / null → 抛"请选择头像文件"
- [ ] GREEN: 实现 `AvatarUtil.validateAndGetExtension(MultipartFile)` + `validatePathSafe(String userIdStr)`
- [ ] RED: 编写路径穿越测试——`validatePathSafe("..%2F..%2Fetc")` 抛异常
- [ ] GREEN: 实现正则 `^\\d+$` 校验
- [ ] REFACTOR: 清理测试代码

#### Feature: AvatarValidationException

- [ ] RED: 编写 `AvatarValidationExceptionTest`——构造时 message 正确传递
- [ ] GREEN: 创建 `AvatarValidationException` 类继承 `RuntimeException`
- [ ] REFACTOR: 清理

### 后端：Service 层

#### Feature: UserService.uploadAvatar

- [ ] RED: 编写 `UserServiceAvatarTest`——mock `UserRepository`、`UploadConfig`，断言：(1) 合法文件上传后 user.avatarUrl 被设置；(2) `updatedAt` 被更新；(3) 旧文件被删除；(4) 非法格式抛 `AvatarValidationException`；(5) 超大文件抛 `AvatarValidationException`
- [ ] GREEN: 实现 `UserService.uploadAvatar(Long userId, MultipartFile file)` —— 校验 → 找 user → 删旧 → 写新 → 更新 user → 返回 `AvatarUploadResponse`
- [ ] RED: 编写测试——avatarUrl 包含 `?v={timestamp}` 版本号
- [ ] GREEN: 在响应 builder 中拼上 `?v=updatedAt.getTime()`
- [ ] REFACTOR: 抽取 `deleteExistingAvatars(Path, Long)` 私有方法

#### Feature: UserService.deleteAvatar

- [ ] RED: 编写测试——mock user 有 avatarUrl，调用后 user.avatarUrl=null，磁盘文件被删
- [ ] GREEN: 实现 `UserService.deleteAvatar(Long userId)` —— 找 user → 删文件 → user.avatarUrl=null → save
- [ ] RED: 编写测试——user 无头像时调用不抛异常
- [ ] GREEN: 加 null 检查
- [ ] REFACTOR: 清理

#### Feature: UserService.getPublicProfile

- [ ] RED: 编写测试——返回 `PublicUserDTO` 含 id/username/nickname/avatarUrl/createdAt，**不含** password/email/lastLoginAt
- [ ] GREEN: 实现 `UserService.getPublicProfile(Long id)` —— findById → 构造 DTO
- [ ] RED: 编写测试——用户不存在抛 `UserNotFoundException`
- [ ] GREEN: 加 orElseThrow
- [ ] REFACTOR: 清理

#### Feature: UserService.getCurrentUser 返回 avatarUrl

- [ ] RED: 编写测试——断言返回的 `UserDTO` 含 `avatarUrl` 字段
- [ ] GREEN: `UserService.getCurrentUser` 的 builder 新增 `.avatarUrl(user.getAvatarUrl())`
- [ ] REFACTOR: 清理

### 后端：Controller 层

#### Feature: UserController POST /me/avatar

- [ ] RED: 编写 `UserControllerAvatarTest`（`@WebMvcTest` + `MockMvc`）——断言：(1) 合法 jpg 上传返回 200 + `data.avatarUrl`；(2) 格式非法返回 400；(3) 超大返回 413；(4) 未登录返回 401
- [ ] GREEN: 实现 `UserController.uploadAvatar(@RequestParam MultipartFile file, @AuthenticationPrincipal User)`
- [ ] REFACTOR: 清理

#### Feature: UserController DELETE /me/avatar

- [ ] RED: 编写测试——已登录用户删除返回 200，user.avatarUrl 置 null
- [ ] GREEN: 实现 `UserController.deleteAvatar(@AuthenticationPrincipal User)`
- [ ] REFACTOR: 清理

#### Feature: UserController GET /{id}

- [ ] RED: 编写测试——公开访问，断言返回 `PublicUserDTO` 不含 password 字段
- [ ] GREEN: 实现 `UserController.getPublicProfile(@PathVariable Long id)`
- [ ] RED: 编写测试——不存在的 id 返回 404
- [ ] GREEN: 加异常处理
- [ ] RED: 编写测试——非数字 id 返回 400
- [ ] GREEN: 加校验
- [ ] REFACTOR: 清理

#### Feature: AvatarStaticController GET /static/avatars/{userId}

- [ ] RED: 编写 `AvatarStaticControllerTest`——(1) 文件存在返回 200 + 正确 Content-Type + Cache-Control header；(2) 文件不存在返回 404；(3) 路径穿越请求返回 400
- [ ] GREEN: 实现 `AvatarStaticController.getAvatar(@PathVariable String userId)` —— 探测 jpg/jpeg/png/webp/gif → FileSystemResource
- [ ] REFACTOR: 清理

### 前端：类型与 store

#### Feature: User 类型扩展 avatarUrl

- [ ] RED: 编写 `UserTypeTest`——断言 `User` 类型 `avatarUrl?: string | null` 存在
- [ ] GREEN: `types/index.ts` 新增 `avatarUrl?: string | null`
- [ ] REFACTOR: 清理

#### Feature: auth store 持久化 avatarUrl

- [ ] RED: 编写 `auth.test.ts` 测试——`setUser({avatarUrl: "x"})` 后 initFromStorage 能读出 avatarUrl
- [ ] GREEN: `stores/auth.ts` `setUser` 持久化到 localStorage（已通过 JSON.stringify 自动包含）
- [ ] REFACTOR: 清理

### 前端：UserAvatar 组件

#### Feature: UserAvatar 基础渲染

- [ ] RED: 编写 `UserAvatar.test.ts`——断言：(1) `avatarUrl` 不为 null 渲染 `<img>`；(2) `avatarUrl` 为 null 渲染首字母 div；(3) `size="sm"|"md"|"lg"` 直径分别为 24/32/40px
- [ ] GREEN: 实现 `UserAvatar.vue` 基础结构
- [ ] REFACTOR: 清理

#### Feature: UserAvatar 哈希色

- [ ] RED: 编写测试——`user.id=42` 渲染时背景色 = `PALETTE[42 % 6]`
- [ ] GREEN: 实现 `paletteColor` computed
- [ ] RED: 编写测试——`user.id=42` 多次渲染颜色稳定
- [ ] GREEN: computed 已天然稳定
- [ ] REFACTOR: 清理

#### Feature: UserAvatar 加载失败降级

- [ ] RED: 编写测试——模拟 `<img onerror>` 触发后，组件切回首字母 div
- [ ] GREEN: 实现 `imgError` ref + `onError` handler
- [ ] REFACTOR: 清理

### 前端：AuthorBadge 改造

#### Feature: AuthorBadge avatarUrl prop

- [ ] RED: 编写 `AuthorBadge.test.ts`（改造）——(1) 传 `avatarUrl` 渲染头像；(2) 不传只渲染文字
- [ ] GREEN: `AuthorBadge.vue` 接收 `avatarUrl` 可选 prop，条件渲染 `<UserAvatar>`
- [ ] REFACTOR: 清理

### 前端：AppHeader 改造

#### Feature: AppHeader 改用 UserAvatar

- [ ] RED: 编写 `AppHeader.test.ts`（改造）——(1) `authStore.user.avatarUrl` 不为空时显示 `<UserAvatar>`；(2) 为 null 时显示首字母 div
- [ ] GREEN: `AppHeader.vue` 替换第 69-71 行的硬编码 div 为 `<UserAvatar :user="user" size="md" />`
- [ ] REFACTOR: 清理

#### Feature: AppHeader 用户菜单新增"个人资料"

- [ ] RED: 编写测试——点击"个人资料"跳转 `/me/profile`
- [ ] GREEN: `AppHeader.vue` 下拉菜单新增一项 + `goToProfile` 方法
- [ ] REFACTOR: 清理

### 前端：ProfilePage

#### Feature: ProfilePage 路由注册

- [ ] RED: 编写测试——访问 `/me/profile` 未登录时跳 `/login?redirect=/me/profile`
- [ ] GREEN: `router/index.ts` 注册 `{ path: '/me/profile', name: 'Profile', component: () => import(...), meta: { requiresAuth: true } }`
- [ ] REFACTOR: 清理

#### Feature: ProfilePage 基础结构 + 头像预览

- [ ] RED: 编写 `ProfilePage.test.ts`——(1) 加载完成时显示当前头像或首字母；(2) 头像容器 128px（桌面）/ 96px（移动）
- [ ] GREEN: 创建 `ProfilePage.vue` + 基础布局
- [ ] REFACTOR: 清理

#### Feature: ProfilePage 文件选择 + 客户端校验

- [ ] RED: 编写测试——选择 .svg 文件时弹错"仅支持 jpg / png / webp / gif"
- [ ] GREEN: 实现 `handleFileChange` —— 校验扩展名
- [ ] RED: 编写测试——选择 3MB 文件时弹错"头像不能超过 2MB"
- [ ] GREEN: 实现大小校验
- [ ] RED: 编写测试——合法文件 → 显示 base64 预览
- [ ] GREEN: 实现 `FileReader.readAsDataURL`
- [ ] REFACTOR: 清理

#### Feature: ProfilePage 上传 + Loading 态

- [ ] RED: 编写测试——点击"确认上传"后按钮显示 spinner，接口 200 后更新 `authStore.user.avatarUrl`
- [ ] GREEN: 实现 `handleUpload` —— `api.post('/users/me/avatar', formData)` + 更新 store
- [ ] RED: 编写测试——接口 500 时显示 `role="alert"` 错误提示，旧头像不变
- [ ] GREEN: 加 try/catch
- [ ] RED: 编写测试——上传成功后显示"上传成功"提示
- [ ] GREEN: 实现 success state
- [ ] REFACTOR: 清理

#### Feature: ProfilePage 移除头像

- [ ] RED: 编写测试——点击"移除头像"调用 `DELETE /users/me/avatar`，成功后 UI 切回首字母
- [ ] GREEN: 实现 `handleRemove` 方法
- [ ] REFACTOR: 清理

### 跨端集成

#### Feature: 缓存破坏 URL

- [ ] RED: 编写测试——上传后 `authStore.user.avatarUrl` 包含 `?v=` 参数
- [ ] GREEN: 已在后端 response 中加版本号；前端 store 直接透传
- [ ] REFACTOR: 清理

#### Feature: 双主题适配

- [ ] RED: 编写测试——切换主题后 `UserAvatar` 容器边框/阴影跟随 CSS 变量
- [ ] GREEN: 验证 CSS 全部用 `var(--xxx)`，无硬编码颜色
- [ ] REFACTOR: 清理

#### Feature: 移动端响应式

- [ ] RED: 编写测试——视口 < 640px 时 ProfilePage 上下堆叠，按钮 width:100%
- [ ] GREEN: 实现 CSS Grid 响应式断点
- [ ] REFACTOR: 清理

---

## B. UI Implementation Tasks

> 基于 `design-system.md` 和 `ui-preview.html` 实现 UI 任务。

### UI: UserAvatar 通用组件

- [ ] 实现 `UserAvatar.vue`——基于 `design-system.md` 第 4.1/4.2 节，使用 CSS 变量支持双主题
- [ ] 验证 `UserAvatar.vue`——视觉对照 `ui-preview.html` Section 1/2/6，状态（normal/loading/error）齐全
- [ ] 双主题验证——暗色/亮色下边框/阴影/焦点环随主题切换

### UI: AuthorBadge 增强

- [ ] 改造 `AuthorBadge.vue`——新增 `avatarUrl` prop，参考 `ui-preview.html` Section 3
- [ ] 验证 `AuthorBadge.vue`——有/无头像两态切换正确
- [ ] 双主题验证——背景色 `rgba(139,92,246,0.12)` 暗色和亮色对比度都满足 WCAG AA

### UI: AppHeader 集成

- [ ] 改造 `AppHeader.vue` 第 69-71 行——改用 `<UserAvatar :user="user" />`
- [ ] 验证 `AppHeader.vue`——对照 `ui-preview.html` Section 4，菜单展开后能看到"个人资料"项
- [ ] 双主题验证——user-menu 背景色随主题

### UI: ProfilePage

- [ ] 实现 `ProfilePage.vue`——参考 `ui-preview.html` Section 5，包含头像预览 + 上传/移除按钮 + 错误/成功提示
- [ ] 验证 `ProfilePage.vue`——上传/移除/Loading/错误/成功状态全对照
- [ ] 双主题验证——alert 颜色、按钮、卡片背景随主题

---

## C. Browser Test

> 开发任务完成后，手动加载 `/openspec-browser-test` skill 或使用 opencli browser 执行浏览器测试。
> **测试依据**: `specs/`、`design.md`、`ui-preview.html`

### Test: 头像上传流程

- [ ] TC-01: 登录用户访问 `/me/profile`，看到当前头像（或首字母兜底）
- [ ] TC-02: 点击"更换头像"选择合法 jpg → 预览显示 → 点击"确认上传" → 头像更新
- [ ] TC-03: 选择 svg 文件 → 立即弹错"仅支持 jpg / png / webp / gif"
- [ ] TC-04: 选择 3MB jpg → 立即弹错"头像不能超过 2MB"
- [ ] TC-05: 上传中按钮显示 spinner，禁止重复点击
- [ ] TC-06: 上传成功 2s 后 success 提示自动消失
- [ ] TC-07: 上传失败（接口 500）→ 错误提示显示，旧头像不变

### Test: 头像显示

- [ ] TC-08: AppHeader 右上角显示已上传的头像
- [ ] TC-09: 切换主题后头像容器边框跟随
- [ ] TC-10: 工具详情页 / 帖子列表 AuthorBadge 显示头像
- [ ] TC-11: 旧用户（无头像）AppHeader / AuthorBadge 降级到首字母 + 哈希色
- [ ] TC-12: 同一 id 多次访问，兜底色块颜色稳定

### Test: 头像移除

- [ ] TC-13: 点击"移除头像"调用 DELETE，UI 切回首字母

### Test: 兼容性

- [ ] TC-14: 移动端（视口 375px）ProfilePage 上下堆叠
- [ ] TC-15: 移动端按钮 width:100%
- [ ] TC-16: 键盘 Tab 焦点环在双主题下都可见
- [ ] TC-17: 屏幕阅读器读取头像 alt 文本

### Test: 缓存破坏

- [ ] TC-18: 上传新头像后，URL `?v=` 时间戳变化
- [ ] TC-19: 浏览器返回上一页时加载新头像（不命中旧缓存）

### Test: 异常路径

- [ ] TC-20: 后端头像文件被删后，前端 `<img onerror>` 切回首字母
- [ ] TC-21: 未登录访问 `/me/profile` → 重定向到 `/login?redirect=/me/profile`
- [ ] TC-22: 路径穿越请求 `/api/v1/static/avatars/..%2Fetc%2Fpasswd` → 400/404
