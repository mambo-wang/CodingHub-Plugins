## 1. 数据库迁移

- [x] 1.1 编写 SQL 迁移脚本：创建 unified_like、unified_comment、unified_favorite 三张新表（含索引和唯一约束）
- [x] 1.2 编写数据迁移 SQL：将 tool_like、forum_like（仅帖子点赞）、video_like 数据迁移到 unified_like
- [x] 1.3 编写数据迁移 SQL：将 tool_comment、forum_comment、video_comment 数据迁移到 unified_comment（保留 parentId/rootId）
- [x] 1.4 编写数据迁移 SQL：将 post_favorites、video_favorite 数据迁移到 unified_favorite
- [x] 1.5 编写旧表 RENAME 语句：10 张旧表改名为 *_deprecated
- [x] 1.6 在开发环境执行完整迁移脚本并验证数据完整性

## 2. 后端 Model + Repository

- [x] 2.1 创建 TargetType 枚举类（TOOL / FORUM_POST / VIDEO）和校验工具
- [x] 2.2 创建 UnifiedLike 实体类（映射 unified_like 表）
- [x] 2.3 创建 UnifiedComment 实体类（映射 unified_comment 表）
- [x] 2.4 创建 UnifiedFavorite 实体类（映射 unified_favorite 表）
- [x] 2.5 创建 UnifiedLikeRepository（含 existsBy/findBy/deleteBy 方法，支持 user_id 和 ip_hash 两种查询）
- [x] 2.6 创建 UnifiedCommentRepository（含 findByTargetType+TargetId 分页查询、findById 用于嵌套回复查找）
- [x] 2.7 创建 UnifiedFavoriteRepository（含 toggle 查询方法和 findByUserId+TargetType 分页查询）

## 3. 后端 Service 层

- [x] 3.1 实现 UnifiedLikeService：toggleLike 方法（支持登录/匿名用户，同步更新主表 likeCount）
- [x] 3.2 实现 UnifiedLikeService：getLikeStatus 方法（按 targetType+targetId+userId/ipHash 查询）
- [x] 3.3 实现 UnifiedCommentService：addComment 方法（顶层评论 + 嵌套回复，XSS 过滤，同步 commentCount）
- [x] 3.4 实现 UnifiedCommentService：getComments 方法（分页查询，返回含 parentId/rootId 的扁平列表）
- [x] 3.5 实现 UnifiedCommentService：deleteComment 方法（isOwner || isAdmin 权限校验，同步 commentCount）
- [x] 3.6 实现 UnifiedFavoriteService：toggleFavorite 方法（登录用户，校验资源存在性）
- [x] 3.7 实现 UnifiedFavoriteService：getMyFavorites 方法（按 targetType 分页查询，返回对应模块 DTO）
- [x] 3.8 实现 UnifiedFavoriteService：getFavoriteStatus 方法
- [x] 3.9 为 UnifiedLikeService 编写单元测试（覆盖 spec.md 中全部 Scenario：登录点赞/取消、匿名点赞/取消、资源不存在 404）
- [x] 3.10 为 UnifiedCommentService 编写单元测试（覆盖：顶层评论、嵌套回复、匿名评论、XSS 过滤、分页查询、权限删除、不存在 404）
- [x] 3.11 为 UnifiedFavoriteService 编写单元测试（覆盖：收藏/取消、未登录 401、收藏列表、已删除资源 404）
- [x] 3.12 运行 `cd backend && ./gradlew test` 确认全部通过

## 4. 后端 Controller 层

- [x] 4.1 创建 InteractionRequest DTO 和 InteractionResponse DTO
- [x] 4.2 创建 UnifiedInteractionController：POST /api/v1/interactions/likes（点赞 toggle）
- [x] 4.3 创建 UnifiedInteractionController：GET /api/v1/interactions/likes/status（查询点赞状态）
- [x] 4.4 创建 UnifiedInteractionController：GET/POST /api/v1/interactions/comments（评论列表/创建）
- [x] 4.5 创建 UnifiedInteractionController：DELETE /api/v1/interactions/comments/{id}（删除评论）
- [x] 4.6 创建 UnifiedInteractionController：POST /api/v1/interactions/favorites（收藏 toggle）
- [x] 4.7 创建 UnifiedInteractionController：GET /api/v1/interactions/favorites（我的收藏列表）
- [x] 4.8 创建 UnifiedInteractionController：GET /api/v1/interactions/favorites/status（收藏状态）
- [x] 4.9 更新 SecurityConfig：允许匿名访问 likes 和 comments 端点（GET/POST），favorites 端点要求认证

## 5. 前端通用组件

- [x] 5.1 创建 GeneralizedSidebar.vue 组件（props: items 数组，200px sticky 毛玻璃侧边栏，登录态控制，路由高亮）
- [x] 5.2 创建 UnifiedLikeButton.vue 组件（调用统一点赞 API，支持登录/匿名态切换，显示 likeCount）
- [x] 5.3 创建 UnifiedCommentSection.vue 组件（评论列表 + 评论编辑器 + 嵌套回复渲染，支持匿名评论）
- [x] 5.4 创建 UnifiedFavoriteButton.vue 组件（调用统一收藏 API，toggle 状态）
- [x] 5.5 创建 useInteraction.ts composable（封装统一交互 API 调用逻辑）
- [x] 5.6 更新 frontend/src/services/api.ts：添加统一交互 API 方法

## 6. 前端页面改造 — 工具模块

- [x] 6.1 改造 HomePage.vue：添加 GeneralizedSidebar 布局（导航项：工具列表/我的工具/我的收藏）
- [x] 6.2 改造 DetailPage.vue：替换 ToolLikeButton → UnifiedLikeButton，替换 ToolCommentList → UnifiedCommentSection，添加 UnifiedFavoriteButton
- [x] 6.3 改造 MyToolsPage.vue：合并到新路由 /my-tools，添加 GeneralizedSidebar 布局
- [x] 6.4 创建 MyToolFavoritesPage.vue：工具收藏列表页，调用 GET /api/v1/interactions/favorites?targetType=TOOL
- [x] 6.5 更新 router/index.ts：添加 /my-favorites 路由

## 7. 前端页面改造 — 论坛模块

- [x] 7.1 改造 PostListPage.vue：替换 SidebarNav → GeneralizedSidebar（导航项：帖子列表/我的帖子/我的收藏）
- [x] 7.2 改造 MyPostsPage.vue：替换 SidebarNav → GeneralizedSidebar
- [x] 7.3 改造 MyFavoritesPage.vue：替换 SidebarNav → GeneralizedSidebar，改用统一收藏 API（targetType=FORUM_POST）
- [x] 7.4 改造 PostDetailPage.vue：替换点赞/评论/收藏组件为 Unified 组件
- [x] 7.5 废弃 SidebarNav.vue（删除或标记 deprecated）

## 8. 前端页面改造 — 微课模块

- [x] 8.1 改造 VideoListPage.vue：添加 GeneralizedSidebar 布局（导航项：微课列表/我的微课/我的收藏）
- [x] 8.2 改造 VideoDetailPage.vue：替换点赞/评论/收藏组件为 Unified 组件
- [x] 8.3 创建 MyVideosPage.vue：我的微课列表页（从 ProfilePage 迁出）
- [x] 8.4 创建 MyVideoFavoritesPage.vue：微课收藏列表页
- [x] 8.5 更新 router/index.ts：添加 /videos/my-videos 和 /videos/my-favorites 路由
- [x] 8.6 改造 ProfilePage.vue：移除「我的视频」和「我的收藏」tab，仅保留个人资料

## 9. 旧代码清理

- [x] 9.1 废弃旧 Service 方法：ToolService.likeTool/unlikeTool/addComment、ForumLikeService、ForumCommentService、PostFavoriteService、VideoInteractionService.toggleLike/toggleFavorite/addComment
- [x] 9.2 废弃旧 Controller 端点：/api/v1/tools/{id}/like、/api/forum/likes、/api/v1/videos/{id}/like、/api/v1/videos/{id}/favorite 等
- [x] 9.3 废弃旧前端组件：ToolLikeButton、ToolCommentList、ToolCommentEditor、VideoCommentList
- [x] 9.4 废弃旧 Model 和 Repository：ToolLike、ToolComment、ForumLike、ForumComment、PostFavorite、VideoLike、VideoComment、VideoFavorite

## 10. 集成测试与验证

- [x] 10.1 启动后端服务，使用 curl/Postman 测试统一 API 端点（点赞/评论/收藏的 CRUD）
- [x] 10.2 测试匿名点赞和匿名评论功能
- [x] 10.3 测试嵌套评论的创建和列表查询
- [x] 10.4 验证数据迁移结果：新表数据量与旧表一致
- [x] 10.5 运行 `make lint` 确认架构层级检查和代码质量检查通过
