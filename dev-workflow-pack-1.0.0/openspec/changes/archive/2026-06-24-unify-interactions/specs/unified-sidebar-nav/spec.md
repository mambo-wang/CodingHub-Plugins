## ADDED Requirements

### Requirement: GeneralizedSidebar 通用侧边栏组件
系统必须提供一个通用的侧边栏导航组件 `GeneralizedSidebar`，接受导航项配置数组作为 props，三个模块（工具/论坛/微课）共用。

#### Scenario: 渲染导航项
- **WHEN** 组件接收 `items` prop 包含 3 个导航项
- **THEN** 组件渲染 3 个导航链接，每项包含图标、文字和路由链接

#### Scenario: 登录态导航项可见性
- **WHEN** 导航项配置 `requiresAuth: true` 且用户未登录
- **THEN** 该导航项不渲染（v-if 控制）

#### Scenario: 当前路由高亮
- **WHEN** 当前页面路由匹配某个导航项的 `to` 路径
- **THEN** 该导航项添加 active CSS class 高亮显示

#### Scenario: 未登录用户点击需登录项
- **WHEN** 未登录用户尝试访问需要登录的导航项
- **THEN** 路由守卫重定向到 /login 页面

### Requirement: 三模块统一侧边栏布局
工具列表页、论坛帖子列表页、微课视频列表页必须统一采用 sidebar + content 双栏布局。

#### Scenario: 工具列表页导航
- **WHEN** 用户访问工具列表页
- **THEN** 页面左侧显示 GeneralizedSidebar，导航项为「工具列表」「我的工具」「我的收藏」

#### Scenario: 论坛帖子列表页导航
- **WHEN** 用户访问论坛帖子列表页
- **THEN** 页面左侧显示 GeneralizedSidebar，导航项为「帖子列表」「我的帖子」「我的收藏」

#### Scenario: 微课视频列表页导航
- **WHEN** 用户访问微课视频列表页
- **THEN** 页面左侧显示 GeneralizedSidebar，导航项为「微课列表」「我的微课」「我的收藏」

#### Scenario: 移动端响应式
- **WHEN** 视口宽度 ≤ 768px
- **THEN** 侧边栏折叠为顶部 tab bar 或隐藏，内容区域全宽显示

### Requirement: 新增收藏/我的页面
系统必须为工具和微课模块新增独立的收藏列表页和我的内容页。

#### Scenario: 工具收藏页
- **WHEN** 登录用户访问 /my-favorites
- **THEN** 页面显示用户收藏的工具列表，使用 GeneralizedSidebar 布局，调用统一收藏 API（targetType=TOOL）

#### Scenario: 微课我的视频页
- **WHEN** 登录用户访问 /videos/my-videos
- **THEN** 页面显示用户上传的微课列表，使用 GeneralizedSidebar 布局

#### Scenario: 微课收藏页
- **WHEN** 登录用户访问 /videos/my-favorites
- **THEN** 页面显示用户收藏的微课列表，使用 GeneralizedSidebar 布局，调用统一收藏 API（targetType=VIDEO）

### Requirement: ProfilePage 精简
ProfilePage 必须移除「我的视频」和「我的收藏」tab，仅保留「个人资料」功能。

#### Scenario: ProfilePage 仅显示个人资料
- **WHEN** 用户访问 /me/profile
- **THEN** 页面仅显示个人资料管理（头像上传/移除），不再包含视频和收藏 tab
