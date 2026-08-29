## ADDED Requirements

### Requirement: 个人中心互动聚合展示
系统必须在个人中心（ProfilePage）提供「我的评论 / 我的收藏 / 我的点赞」三个互动板块，以标签页形式内嵌展示，聚合用户在平台上的互动痕迹。

#### Scenario: 已登录用户打开个人中心
- **WHEN** 已登录用户访问个人中心页面
- **THEN** 系统展示三个互动标签（我的评论 / 我的收藏 / 我的点赞），默认进入「我的评论」

#### Scenario: 各板块按目标类型分列
- **WHEN** 用户切换至「我的收藏」或「我的点赞」标签
- **THEN** 系统按 TOOL / FORUM_POST / VIDEO 三种类型分别展示最近 N 条（默认 10），并支持「查看全部」展开

#### Scenario: 空状态
- **WHEN** 某板块当前用户无对应互动数据
- **THEN** 系统展示空状态提示（图标 + 文案），不报错

### Requirement: 互动项点击跳转详情页
系统必须使每条互动项可点击，跳转至对应目标详情页；点击行为需对三种 targetType 均生效。

#### Scenario: 点击工具类互动项
- **WHEN** 用户点击 targetType=TOOL 的互动项
- **THEN** 系统跳转至 `/tools/:id`（ToolDetail）

#### Scenario: 点击帖子类互动项
- **WHEN** 用户点击 targetType=FORUM_POST 的互动项
- **THEN** 系统跳转至 `/forum/posts/:id`（ForumPostDetail）

#### Scenario: 点击微课类互动项
- **WHEN** 用户点击 targetType=VIDEO 的互动项
- **THEN** 系统跳转至 `/videos/:id`（VideoDetail）

### Requirement: 评论条目展示目标标题
系统必须在「我的评论」列表中展示每条评论所属目标的标题，使跳转目标明确。

#### Scenario: 评论项渲染
- **WHEN** 系统加载「我的评论」列表
- **THEN** 每条评论显示目标类型图标、目标标题、评论内容片段与创建时间
