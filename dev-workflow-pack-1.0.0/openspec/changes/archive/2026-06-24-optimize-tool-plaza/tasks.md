## 1. 删除废弃路由和页面

- [ ] 1.1 删除 `frontend/src/pages/MyToolsPage.vue` 文件
- [ ] 1.2 删除 `frontend/src/pages/MyToolFavoritesPage.vue` 文件
- [ ] 1.3 在 `frontend/src/router/index.ts` 中移除 `/me/tools` 和 `/me/favorites` 两条路由及其 `import` 语句（保留 `/me/tools/:id/edit` 路由不变）

## 2. 修改 AppHeader 移除「我的工具」入口

- [ ] 2.1 在 `frontend/src/components/AppHeader.vue` 中移除 `goToMyTools` 函数定义
- [ ] 2.2 移除顶部导航栏中「我的工具」按钮（`v-if="isLoggedIn"` 条件内的 `<button class="nav-btn">` ）
- [ ] 2.3 移除用户下拉菜单中「我的工具」菜单项（`<button class="user-dropdown-item">` ）

## 3. 修复 EditToolPage 路由重定向

- [ ] 3.1 在 `frontend/src/pages/EditToolPage.vue` 中，将所有 `router.push('/me/tools')` 替换为 `router.push('/')`（共 5 处：保存成功后、删除成功后、取消操作等场景）

## 4. 重构 HomePage — 移除侧边栏、添加 Tab Pill 导航

- [ ] 4.1 在 `frontend/src/pages/HomePage.vue` 中移除 `GeneralizedSidebar` 组件引用和 `sidebarItems` 定义，移除 `import` 语句
- [ ] 4.2 移除 `.tools-with-sidebar` 包裹层和对应的 CSS 样式，让 `.tools-content` 直接作为工具网格容器（全宽）
- [ ] 4.3 新增 `activeTab` ref（类型 `'all' | 'favorites' | 'myTools'`，默认 `'all'`），新增 `handleTabChange(tab)` 函数：切换 Tab 时重置分页到第 0 页、重置分类筛选为 null，调用对应数据加载函数
- [ ] 4.4 新增 `fetchFavorites()` 函数：调用 `GET /api/interactions/favorites?targetType=TOOL&page=0&size=12`，将结果赋值给 `tools` 和 `pagination`
- [ ] 4.5 新增 `fetchMyTools()` 函数：调用 `GET /api/v1/tools/my?page=0&size=12`（使用与 fetchTools 相同的 params 模式），将结果赋值给 `tools` 和 `pagination`
- [ ] 4.6 重构 `fetchTools()` 函数：增加对 `activeTab` 的判断分发逻辑——`all` 调现有 API，`favorites` 调 `fetchFavorites()`，`myTools` 调 `fetchMyTools()`
- [ ] 4.7 在 `.category-pills` 区域右侧添加个人 Tab pills：「我的收藏」（`Bookmark` 图标）和「我的工具」（`Wrench` 图标），使用现有 `.pill` / `.category-pill` 样式类，通过 `margin-left: auto` 包裹在 `.pills-right` 容器中推到右侧
- [ ] 4.8 Tab pills 受 `authStore.isLoggedIn` 控制：未登录时通过 `v-if` 隐藏「我的收藏」和「我的工具」pill
- [ ] 4.9 Tab pills 的 `active` 状态绑定到 `activeTab` 值，点击时调用 `handleTabChange`

## 5. 添加上传工具按钮和 Modal

- [ ] 5.1 在 `.pills-right` 容器中、Tab pills 之后添加上传图标按钮（Lucide `Upload` 图标），使用 `aria-label="上传工具"`，样式使用 `.upload-btn` 类（圆形渐变背景）
- [ ] 5.2 上传按钮点击行为：已登录用户打开 Modal（`showUploadModal = true`），未登录用户跳转 `/login?redirect=/`
- [ ] 5.3 新增上传 Modal 组件（内联在 HomePage 中，使用 `<Teleport to="body">`）：overlay + panel 结构，包含表单字段——工具名称（input）、分类选择（select）、版本号（input）、描述（textarea）、文件上传区域，复用 UploadPage 的表单逻辑和校验规则
- [ ] 5.4 Modal 关闭行为：点击 overlay 遮罩或关闭按钮时关闭 Modal 并重置表单
- [ ] 5.5 Modal 提交行为：验证必填字段（名称、描述、版本号），POST `/api/v1/tools` 创建工具，然后调用 `fileUploadApi.uploadFiles` 上传文件，成功后关闭 Modal、重置表单、刷新当前 Tab 数据
- [ ] 5.6 Modal 表单样式复用 UploadPage 的设计：`.glass-card` 容器、渐变提交按钮、虚线文件上传区域、进度条

## 6. 样式完善

- [ ] 6.1 添加 `.pills-right` CSS：`margin-left: auto; display: flex; gap: 8px; align-items: center;`
- [ ] 6.2 添加 `.upload-btn` CSS：36px 圆形、渐变背景、hover 发光效果，遵循 design-system.md 中定义的暗色/亮色双主题样式
- [ ] 6.3 更新响应式断点：`< 640px` 时 `.category-pills` 中隐藏分类 pills（仅显示「全部」），`.pills-right` 中保留 Tab pills 和上传按钮
- [ ] 6.4 移除不再使用的 `.tools-with-sidebar`、`.tools-content` 相关 CSS
- [ ] 6.5 确保所有新增样式使用 CSS 变量（`var(--border-color)` 等）支持双主题，无硬编码颜色值

## 7. 验证与回归测试

- [ ] 7.1 启动前端开发服务器 `make frontend`，验证页面正常加载无控制台报错
- [ ] 7.2 验证「全部」Tab：工具列表正常展示、分类筛选和搜索功能正常
- [ ] 7.3 验证「我的收藏」Tab：切换到收藏列表、分页重置、空状态展示
- [ ] 7.4 验证「我的工具」Tab：切换到我的工具列表、分页重置、卡片编辑/删除按钮正常
- [ ] 7.5 验证 Tab 切换不刷新页面：检查 Network 面板只有 API 请求，无页面导航
- [ ] 7.6 验证未登录用户：「我的收藏」「我的工具」pill 不可见，上传按钮可见，点击上传跳转登录页
- [ ] 7.7 验证上传 Modal：打开/关闭/表单验证/提交成功后数据刷新
- [ ] 7.8 验证 EditToolPage：保存/删除/取消后正确跳转到 `/` 而非 `/me/tools`
- [ ] 7.9 验证 AppHeader：「我的工具」按钮和下拉菜单项已移除，其他导航项正常
- [ ] 7.10 验证双主题：暗色和亮色模式下所有新增元素样式正确
- [ ] 7.11 验证响应式：移动端（< 640px）布局正常，分类 pills 隐藏
- [ ] 7.12 运行 `bash scripts/lint-arch.sh` 确认架构层级检查通过
