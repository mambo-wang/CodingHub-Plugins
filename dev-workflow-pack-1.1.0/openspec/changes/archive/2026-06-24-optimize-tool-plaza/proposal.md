## 为什么（Why）

工具广场页面当前使用左侧侧边栏（GeneralizedSidebar）在「工具列表」「我的工具」「我的收藏」三个独立页面之间导航，同时上方还有分类 pills 做类别筛选。这种双层导航结构导致页面层级过深，工具列表无法利用全宽空间展示更多卡片，视觉效率低下。将其合并为单页面 Tab 切换可以提升浏览效率和信息密度。

## 变更内容（What Changes）

- **移除**：工具广场页面的 GeneralizedSidebar 左侧导航栏，工具列表改为全宽展示
- **移除**：`/me/tools` 和 `/me/favorites` 两个独立路由，以及对应的 `MyToolsPage.vue`、`MyToolFavoritesPage.vue` 页面组件
- **移除**：AppHeader 顶部导航栏中的「我的工具」按钮和下拉菜单项
- **新增**：在分类 pills 行右侧增加「我的收藏」「我的工具」两个 Tab pill，与分类 pills 同行展示
- **新增**：pill 行最右侧增加上传工具图标按钮，点击弹出上传 Modal（样式复用现有 `/tools/upload` 页面）
- **修改**：HomePage.vue 改为单页面 Tab 切换架构，activeTab 控制数据源切换，不刷新页面只刷新数据
- **权限**：未登录用户不展示「我的收藏」和「我的工具」pill，但展示上传图标按钮

## 能力清单（Capabilities）

### 新增能力（New Capabilities）

- `tool-plaza-tab-nav`: 工具广场页面的 Tab 导航系统，将侧边栏导航改为水平 pill Tab 切换，包含全部/我的收藏/我的工具三个视图的数据加载逻辑和上传弹窗入口

### 修改能力（Modified Capabilities）

- `frontend`: 移除 AppHeader 中的「我的工具」导航项

## 影响范围（Impact）

- **前端页面**：`HomePage.vue`（重构为单页面 Tab 切换）、`AppHeader.vue`（移除导航项）
- **删除文件**：`MyToolsPage.vue`、`MyToolFavoritesPage.vue`
- **路由**：`router/index.ts` 删除 `/me/tools`、`/me/favorites` 路由
- **组件**：`GeneralizedSidebar.vue` 不再被工具页面引用（论坛/微课仍使用）
- **API 调用**：前端改用 `GET /api/v1/tools`、`GET /api/v1/tools/my`、`GET /api/interactions/favorites?targetType=TOOL` 三个接口在同一页面内切换
- **后端**：无变更
