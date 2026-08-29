## 1. 后端：我的点赞查询（`unified-interactions`）

- [x] 1.1 在 `UnifiedLikeRepository` 新增 `Page<UnifiedLike> findByUserIdAndTargetTypeOrderByCreatedAtDesc(Long userId, String targetType, Pageable pageable)`
- [x]1.2 在 `UnifiedLikeService` 新增 `getMyLikes(targetType, userId, page, size)`：复用 `ToolSummaryDTO` / `ForumPostSummaryDTO` / `VideoListItem` 构建（镜像 `getMyFavorites`），并仅返回 status=NORMAL 的目标，跳过已删除项
- [x]1.3 在 `UnifiedInteractionController` 新增 `GET /interactions/likes/mine?targetType=&page=&size=`，未登录返回 401，调用 `likeService.getMyLikes`
- [x]1.4 为 `UnifiedLikeService.getMyLikes` 编写单元测试（`src/test/java/.../service/UnifiedLikeServiceTest.java`）：覆盖登录查询、过滤已删除目标、未登录 401 分支，运行 `cd backend && ./gradlew test` 确认通过

## 2. 后端：我的评论查询（`unified-interactions`）

- [x]2.1 在 `UnifiedCommentRepository` 新增 `Page<UnifiedComment> findByUserIdOrderByCreatedAtDesc(Long userId, Pageable pageable)`
- [x]2.2 在 `UnifiedCommentService` 新增 `getMyComments(userId, page, size)`：按 userId 分页查询，按类型解析 `targetTitle`（tool.name / forumPost.title / video.title），构建返回 DTO `{ id, targetType, targetId, targetTitle, content, createdAt }`，跳过目标已删除的评论
- [x]2.3 在 `UnifiedInteractionController` 新增 `GET /interactions/comments/mine?page=&size=`，未登录返回 401，调用 `commentService.getMyComments`
- [x]2.4 为 `UnifiedCommentService.getMyComments` 编写单元测试（`src/test/java/.../service/UnifiedCommentServiceTest.java`）：覆盖登录查询、targetTitle 解析（TOOL/FORUM_POST/VIDEO）、过滤已删除目标、未登录 401 分支，运行 `cd backend && ./gradlew test` 确认通过

## 3. 前端：服务层扩展

- [x]3.1 在 `services/interaction.ts` 新增 `getMyLikes(targetType, page=0, size=10)` 与 `getMyComments(page=0, size=10)`，分别对应 `/interactions/likes/mine`、`/interactions/comments/mine`，返回 `InteractionPageResponse`
- [x]3.2 定义评论列表项类型 `MyCommentItem { id; targetType; targetId; targetTitle; content; createdAt }` 于 `interaction.ts`

## 4. 前端：个人中心互动板块（`ProfilePage.vue`）

- [x]4.1 在 `ProfilePage.vue` 内新增「我的互动」区块：标签切换（我的评论 / 我的收藏 / 我的点赞），其中收藏/点赞板块内按 TOOL / FORUM_POST / VIDEO 子标签分组，各拉取最近 10 条并支持「查看全部」展开
- [x]4.2 实现加载/空/错误三态（loading 骨架、空状态图标+文案、错误提示 `role="alert"`），复用既有 `.glass-card` / `.btn` 样式
- [x]4.3 实现点击跳转：`router.push` 到 `/tools/:id` / `/forum/posts/:id` / `/videos/:id`，互动项使用 `role="tabpanel"` 语义并带 `aria-label`
- [x]4.4 在 `<style scoped>` 中为类型 chip、互动项补充双主题交互样式（normal/hover/focus，暗色焦点环 #00FFFF / 亮色 #7c3aed，hover `translateY(-2px)`），并保留 `prefers-reduced-motion` 处理

## 5. 受影响模块回归测试（基于 impact-analysis.md）

> impact-analysis 判定本次为 **L0**（纯增量新增，不修改既有方法签名与公共 API 行为），无既有调用方受影响。下列为验收与回归验证步骤。

- [x]5.1 运行 `cd backend && ./gradlew test`，确认全部新增单测与既有测试通过
- [x]5.2 手动验证新增端点：登录后 `GET /interactions/likes/mine?targetType=TOOL`、`GET /interactions/comments/mine` 返回预期结构；未登录返回 401
- [x]5.3 确认既有 `GET /interactions/favorites`（及模块页 `/forum/my-favorites`、`/videos/my-favorites`）行为未被破坏
- [x]5.4 前端三板块联调：加载 / 空 / 点击跳转 三态在暗色与亮色主题下均正常，无水平滚动
