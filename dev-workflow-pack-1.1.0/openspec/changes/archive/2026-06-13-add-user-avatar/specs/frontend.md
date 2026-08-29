# Frontend - User Avatar UI

## ADDED Requirements

### Scenario 1: UserAvatar 组件渲染 - 有 URL

- **GIVEN**: `authStore.user.avatarUrl = "/api/v1/static/avatars/2.jpg?v=123"`
- **WHEN**: `<UserAvatar :user="user" size="md" />` 渲染
- **THEN**: 显示 32px 圆形 `<img src="...">`, 加载成功后正常显示

### Scenario 2: UserAvatar 组件渲染 - 无 URL

- **GIVEN**: `authStore.user.avatarUrl = null`，`username = "wangbao"`
- **WHEN**: `<UserAvatar :user="user" size="md" />` 渲染
- **THEN**: 显示 32px 圆形 div 容器，背景 = 哈希色（根据 `user.id` 计算），文字 = 首字母 "W"

### Scenario 3: UserAvatar 组件 - 图片加载失败降级

- **GIVEN**: `avatarUrl = "/api/v1/static/avatars/2.jpg?v=123"`，但服务端 404
- **WHEN**: `<img>` 触发 `onerror`
- **THEN**: 自动切换为首字母 + 哈希色块兜底，不显示破图占位

### Scenario 4: UserAvatar 组件 - 三档尺寸

- **GIVEN**: 组件 `size` prop 传入 `'sm' | 'md' | 'lg'`
- **WHEN**: 渲染
- **THEN**: 直径分别 = 24px / 32px / 40px

### Scenario 5: UserAvatar 组件 - 哈希色确定性

- **GIVEN**: 同一 `user.id=42`
- **WHEN**: 多次渲染
- **THEN**: 兜底色块颜色一致（基于 id 哈希取模 6）

### Scenario 6: 哈希色不随用户名变化

- **GIVEN**: 用户 `id=42` 改名 username → nickname
- **WHEN**: 渲染兜底色块
- **THEN**: 颜色不变（基于 id 而非名字）

### Scenario 7: AuthorBadge 显示头像

- **GIVEN**: `<AuthorBadge username="wb" nickname="王宝" :avatar-url="url" />`
- **WHEN**: 渲染
- **THEN**: 显示 24px 圆形头像 + "王宝(wb)" 文字

### Scenario 8: AuthorBadge 无头像

- **GIVEN**: `<AuthorBadge username="wb" nickname="王宝" />`（无 avatarUrl）
- **WHEN**: 渲染
- **THEN**: 退化到纯文字徽章（现状行为不变）

### Scenario 9: AppHeader 右上角显示头像

- **GIVEN**: `authStore.user.avatarUrl` 不为空
- **WHEN**: 渲染 AppHeader
- **THEN**: 圆形头像 + 用户名/昵称；点击展开下拉

### Scenario 10: AppHeader 右上角 - 无头像

- **GIVEN**: `authStore.user.avatarUrl` 为 null
- **WHEN**: 渲染 AppHeader
- **THEN**: 首字母 + 哈希色圆形占位

### Scenario 11: ProfilePage - 加载现有头像

- **GIVEN**: 用户 `id=2` 已上传头像
- **WHEN**: 访问 `/me/profile`
- **THEN**: 页面加载完成时显示 128px 圆形头像预览 + "更换头像 / 移除" 按钮

### Scenario 12: ProfilePage - 选择文件

- **GIVEN**: 用户点击"更换头像"，在文件选择器中选 `new.jpg`
- **WHEN**: 确认选择
- **THEN**: 显示本地预览（FileReader → base64），不立即上传

### Scenario 13: ProfilePage - 客户端校验

- **GIVEN**: 用户选择 `bad.svg` 或 `huge.exe`
- **WHEN**: 选择完成
- **THEN**: 立即弹错"仅支持 jpg / png / webp / gif"，不进入预览

### Scenario 14: ProfilePage - 大小校验

- **GIVEN**: 用户选择 3MB 的 `big.jpg`
- **WHEN**: 选择完成
- **THEN**: 弹错"头像不能超过 2MB"

### Scenario 15: ProfilePage - 上传成功

- **GIVEN**: 用户点击"确认上传"
- **WHEN**: `POST /api/v1/users/me/avatar` 返回 200 + 新 avatarUrl
- **THEN**: 更新 `authStore.user.avatarUrl`，UI 立即换新头像；显示"上传成功"提示 2s 后自动消失

### Scenario 16: ProfilePage - 上传失败

- **GIVEN**: 接口返回 500
- **WHEN**: 上传失败
- **THEN**: 弹 `role="alert"` 错误信息，旧头像不变

### Scenario 17: ProfilePage - 移除头像

- **GIVEN**: 用户已上传头像
- **WHEN**: 点击"移除头像" + 确认
- **THEN**: 调用 `DELETE /api/v1/users/me/avatar`，user 表 `avatar_url` 置 NULL，UI 切回首字母兜底

### Scenario 18: ProfilePage - 移动端布局

- **GIVEN**: 视口宽度 < 640px
- **WHEN**: 渲染 ProfilePage
- **THEN**: 头像预览和操作按钮上下堆叠；间距使用 `var(--space-md)`；按钮宽度 100%

### Scenario 19: 双主题 - 头像容器

- **GIVEN**: 切换到浅色/深色主题
- **WHEN**: 头像容器（边框、阴影、占位色）重新渲染
- **THEN**: 容器颜色跟随主题；头像图片本身不变

### Scenario 20: 路由守卫

- **GIVEN**: 未登录用户访问 `/me/profile`
- **WHEN**: 路由匹配
- **THEN**: 重定向到 `/login?redirect=/me/profile`

### Scenario 21: AppHeader 用户菜单新增入口

- **GIVEN**: 已登录用户点击右上角用户菜单
- **WHEN**: 菜单展开
- **THEN**: 看到"个人资料"项（点击跳转 `/me/profile`）

### Scenario 22: 缓存破坏 - 换头像即时刷新

- **GIVEN**: 用户在 A 页面刚显示旧头像
- **WHEN**: 切换到 B 页面或刷新
- **THEN**: 新头像 URL 带 `?v=新时间戳`，浏览器/CDN 不会命中旧缓存

### Scenario 23: 屏幕阅读器 - alt 文本

- **GIVEN**: `<UserAvatar :user="user" />` 渲染
- **WHEN**: 屏幕阅读器读取
- **THEN**: `alt` 文本 = "用户的头像"（或 `{username} 的头像`），不应为空
