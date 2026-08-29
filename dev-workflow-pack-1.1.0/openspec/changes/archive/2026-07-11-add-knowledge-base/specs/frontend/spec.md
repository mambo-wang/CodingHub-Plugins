## ADDED Requirements（新增需求）

### Requirement: 知识库路由注册

系统 SHALL 在前端路由表中注册知识库相关路由，包括列表页、详情页、创建页和编辑页。创建和编辑路由 SHALL 设置 `meta: { requiresAuth: true }`。

#### Scenario: 导航到知识库列表
- **WHEN** 用户访问 `/knowledge`
- **THEN** 路由匹配到 KnowledgeListPage 组件

#### Scenario: 未登录访问创建页面
- **WHEN** 未登录用户访问 `/knowledge/create`
- **THEN** 路由守卫拦截，重定向到登录页（携带 redirect 参数）

#### Scenario: 导航到知识库详情
- **WHEN** 用户访问 `/knowledge/42`
- **THEN** 路由匹配到 KnowledgeDetailPage 组件

### Requirement: AppHeader 知识库导航

系统 SHALL 在 AppHeader 的导航链接中新增"知识库"入口，指向 `/knowledge` 路径。

#### Scenario: 导航栏显示知识库链接
- **WHEN** 任意用户查看顶部导航栏
- **THEN** 导航链接中包含"知识库"按钮，点击跳转到 `/knowledge`
