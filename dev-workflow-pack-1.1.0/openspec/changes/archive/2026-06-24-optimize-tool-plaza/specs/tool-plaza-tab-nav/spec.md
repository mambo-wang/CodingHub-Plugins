## ADDED Requirements（新增需求）

### Requirement: 工具广场 Tab Pill 导航

系统 SHALL 在工具广场页面（`/`）的 filter bar 中提供水平 Tab pill 导航，替代原有的左侧侧边栏导航。Tab pills 分为「全部」「我的收藏」「我的工具」三个视图，在同一页面内切换数据源，不触发页面刷新。

#### Scenario: 默认显示全部工具
- **WHEN** 用户访问工具广场页面 `/`
- **THEN** 默认选中「全部」Tab pill，调用 `GET /api/v1/tools` 加载工具列表，工具卡片网格全宽展示（无侧边栏）

#### Scenario: 切换到我的收藏
- **WHEN** 已登录用户点击「我的收藏」pill
- **THEN** `activeTab` 切换为 `favorites`，分页重置为第 0 页，分类筛选重置为 null，调用 `GET /api/interactions/favorites?targetType=TOOL` 加载数据

#### Scenario: 切换到我的工具
- **WHEN** 已登录用户点击「我的工具」pill
- **THEN** `activeTab` 切换为 `myTools`，分页重置为第 0 页，分类筛选重置为 null，调用 `GET /api/v1/tools/my` 加载数据

#### Scenario: Tab 切换保持搜索和排序
- **WHEN** 用户在「全部」视图输入搜索关键词后切换到「我的收藏」
- **THEN** 搜索关键词保留，新视图数据按关键词过滤

#### Scenario: 切换回全部 Tab
- **WHEN** 用户在「我的收藏」或「我的工具」视图点击「全部」pill
- **THEN** 调用 `GET /api/v1/tools` 加载全部工具，分页重置

### Requirement: 未登录用户 Tab 可见性

系统 SHALL 根据用户登录状态控制「我的收藏」和「我的工具」Tab pill 的可见性。

#### Scenario: 未登录用户不显示个人 Tab
- **WHEN** 未登录用户访问工具广场
- **THEN** filter bar 中仅显示「全部」pill 和分类 pills，「我的收藏」和「我的工具」pill 不可见

#### Scenario: 登录后个人 Tab 出现
- **WHEN** 用户登录成功后访问工具广场
- **THEN** filter bar 中显示「我的收藏」和「我的工具」pill

### Requirement: Tab Pill 布局位置

系统 SHALL 将个人 Tab pills（「我的收藏」「我的工具」）放置在分类 pills 的右侧，上传按钮位于最右侧。

#### Scenario: Pill 行排列顺序
- **WHEN** filter bar 渲染
- **THEN** 从左到右依次为：搜索框 → 「全部」+ 分类 pills → 弹性间距 → 「我的收藏」「我的工具」→ 上传按钮

#### Scenario: 窄屏响应式
- **WHEN** 视口宽度 < 640px
- **THEN** filter bar 纵向堆叠，分类 pills 隐藏，仅保留 Tab pills + 搜索框 + 上传按钮

### Requirement: 工具上传弹窗

系统 SHALL 在 filter bar 最右侧提供上传工具图标按钮，点击后弹出 Modal 进行工具上传。

#### Scenario: 点击上传按钮打开 Modal
- **WHEN** 已登录用户点击上传图标按钮
- **THEN** 弹出上传 Modal，表单包含：工具名称、分类选择、版本号、描述（Markdown）、文件上传区域

#### Scenario: 未登录用户点击上传按钮
- **WHEN** 未登录用户点击上传图标按钮
- **THEN** 跳转到登录页面 `/login`，携带 `redirect` 参数

#### Scenario: 上传成功后刷新数据
- **WHEN** 用户在 Modal 中成功上传工具
- **THEN** Modal 关闭，当前 Tab 数据自动刷新（重新调用对应 API），分页重置为第 0 页

#### Scenario: 上传 Modal 表单验证
- **WHEN** 用户提交表单时缺少必填字段（名称、描述、版本号）
- **THEN** 提交按钮禁用，不允许提交

#### Scenario: 上传 Modal 关闭
- **WHEN** 用户点击 Modal 遮罩层或关闭按钮
- **THEN** Modal 关闭，表单数据清空

### Requirement: 工具卡片编辑删除操作

系统 SHALL 在工具广场页面的工具卡片上保留编辑和删除操作按钮（当前用户拥有或管理员身份）。

#### Scenario: 在「我的工具」Tab 下编辑工具
- **WHEN** 用户在「我的工具」视图点击卡片上的编辑按钮
- **THEN** 跳转到 `/me/tools/{id}/edit` 编辑页面

#### Scenario: 在「全部」Tab 下编辑自己的工具
- **WHEN** 用户在「全部」视图点击自己工具的编辑按钮
- **THEN** 跳转到 `/me/tools/{id}/edit` 编辑页面

### Requirement: 移除独立路由

系统 SHALL 移除不再使用的「我的工具」和「我的收藏」独立路由。

#### Scenario: 移除的路由
- **WHEN** 用户尝试访问 `/me/tools` 或 `/me/favorites`
- **THEN** 返回 404 页面（路由已不存在）

#### Scenario: 保留的路由
- **WHEN** 用户访问 `/me/tools/:id/edit`
- **THEN** 正常加载工具编辑页面（该路由保留不变）

### Requirement: 编辑页重定向修正

系统 SHALL 在工具编辑页（EditToolPage）保存、删除、取消操作后重定向到工具广场首页。

#### Scenario: 编辑保存后跳转
- **WHEN** 用户在编辑页成功保存工具修改
- **THEN** 跳转到工具广场首页 `/`（原为 `/me/tools`）

#### Scenario: 编辑删除后跳转
- **WHEN** 用户在编辑页成功删除工具
- **THEN** 跳转到工具广场首页 `/`（原为 `/me/tools`）

#### Scenario: 编辑取消后跳转
- **WHEN** 用户在编辑页点击取消
- **THEN** 跳转到工具广场首页 `/`（原为 `/me/tools`）
