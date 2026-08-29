# Tasks

## Atomic TDD Task List

### Feature: 收藏功能后端 API

- [ ] RED: 编写 PostFavoriteRepositoryTest——测试收藏实体创建和唯一索引约束
- [ ] GREEN: 实现 PostFavorite 实体类——包含 id, userId, postId, createdAt 字段
- [ ] RED: 编写 PostFavoriteServiceTest——测试添加收藏、取消收藏、查询收藏列表
- [ ] GREEN: 实现 PostFavoriteService——实现收藏业务逻辑，校验登录状态
- [ ] RED: 编写 PostFavoriteControllerTest——测试收藏 API 端点
- [ ] GREEN: 实现 PostFavoriteController——提供 POST/DELETE/GET 收藏接口

### Feature: 前端收藏功能

- [ ] RED: 编写 PostCard.spec.ts——测试收藏按钮渲染和点击行为
- [ ] GREEN: 修改 PostCard.vue——添加收藏按钮，支持点击收藏/取消
- [ ] RED: 编写 PostDetailPage.spec.ts——测试详情页收藏按钮
- [ ] GREEN: 修改 PostDetailPage.vue——添加收藏按钮，校验登录状态

### Feature: 左侧导航栏

- [ ] RED: 编写 PostListPage.spec.ts——测试左侧导航栏显示和点击行为
- [ ] GREEN: 修改 PostListPage.vue——添加左侧导航栏（我的帖子、我的收藏）
- [ ] RED: 编写 MyPostsPage.spec.ts——测试我的帖子页面
- [ ] GREEN: 实现 MyPostsPage.vue——显示当前用户发布的帖子

### Feature: 我的收藏页面

- [ ] RED: 编写 MyFavoritesPage.spec.ts——测试我的收藏页面
- [ ] GREEN: 实现 MyFavoritesPage.vue——显示当前用户收藏的帖子

### Feature: 顶部菜单栏修改

- [ ] RED: 编写 AppHeader.spec.ts——测试菜单栏不显示上传工具按钮
- [ ] GREEN: 修改 AppHeader.vue——移除上传工具按钮，只保留工具和论坛导航

### Feature: 路由配置

- [ ] RED: 编写 router.spec.ts——测试新路由配置
- [ ] GREEN: 修改 router/index.ts——添加 /forum/my-posts 和 /forum/my-favorites 路由

### Feature: API 服务

- [ ] RED: 编写 api.spec.ts——测试收藏 API 调用
- [ ] GREEN: 修改 services/api.ts——添加收藏相关的 API 方法