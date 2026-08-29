## 1. 数据库迁移

- [x] 1.1 创建 V3 迁移脚本 `V3__add_sort_and_pin.sql`：tool/forum_post/video 三表添加 `pinned BOOLEAN NOT NULL DEFAULT FALSE`；video 表添加 `score DECIMAL(10,2) NOT NULL DEFAULT 0`；创建索引 `idx_tool_pinned`、`idx_forum_post_pinned`、`idx_video_pinned`、`idx_video_score`

## 2. 后端 Entity 层

- [x] 2.1 Tool 实体添加 `pinned` 字段（Boolean, default false）
- [x] 2.2 ForumPost 实体添加 `pinned` 字段（Boolean, default false）
- [x] 2.3 Video 实体添加 `pinned` 字段（Boolean, default false）+ `score` 字段（BigDecimal）+ `updateScore()` 方法（公式: viewCount×1 + likeCount×3 + commentCount×5），在 `incrementViewCount()`、`incrementLikeCount()`、`decrementLikeCount()`、`incrementCommentCount()`、`decrementCommentCount()` 中自动调用 `updateScore()`

## 3. 后端 Repository 层

- [x] 3.1 ToolRepository 添加热度排序查询方法 `findByFiltersOrderByHot`（JPQL: ORDER BY t.pinned DESC, t.score DESC）和 `findTop5ByStatusOrderByScoreDesc`
- [x] 3.2 ForumPostRepository 添加热度排序查询方法（支持 keyword/category 筛选 + ORDER BY pinned DESC, score DESC）和 `findTop5ByStatusOrderByScoreDesc`
- [x] 3.3 VideoRepository 添加热度排序查询方法（ORDER BY pinned DESC, score DESC）和 `findTop5ByStatusOrderByScoreDesc`
- [x] 3.4 三个 Repository 添加 `pinById` / `unpinById` 更新方法（`@Modifying @Query UPDATE ... SET pinned = true/false WHERE id = ?`）

## 4. 后端 Service 层

- [x] 4.1 ToolService 列表方法添加 `sortBy` 参数分支：`hot` 调用热度查询，`latest` 调用时间查询，默认 `hot`
- [x] 4.2 ForumPostService 列表方法添加 `sortBy` 参数分支，重构为支持排序切换
- [x] 4.3 VideoService 列表方法添加 `sortBy` 参数分支
- [x] 4.4 三个 Service 添加 `pin(id)` 和 `unpin(id)` 方法，校验内容存在后调用 Repository
- [x] 4.5 三个 Service 添加 `getHotTop5()` 方法，调用 Repository 返回 `List<Long>`
- [ ] 4.6 为 Service 层编写单元测试：覆盖 pin/unpin 逻辑、sortBy 分支、hot-top5 返回、Video updateScore 计算，运行 `cd backend && ./gradlew test` 确认通过

## 5. 后端 DTO 层

- [x] 5.1 ToolSummaryDTO 添加 `score`（BigDecimal）、`pinned`（Boolean）、`viewCount`（Integer）、`likeCount`（Integer）、`commentCount`（Integer）字段，更新 ToolService 的 DTO 映射
- [x] 5.2 ForumPostDTO（record 类型）添加 `score`（BigDecimal）、`pinned`（Boolean）字段，更新 ForumPostService 的 `toDTO()` 方法传入新字段值
- [x] 5.3 Video 列表 DTO（VideoSummaryDTO 或 VideoDTO）添加 `score`（BigDecimal）、`pinned`（Boolean）字段，更新 VideoService 的 DTO 映射

## 6. 后端 Controller 层

- [x] 6.1 ToolController：修改 `GET /api/v1/tools` 的 `sortBy` 默认值从 `"latest"` 改为 `"hot"`，传递到 Service 层
- [x] 6.2 ToolController：添加 `POST /api/v1/tools/{id}/pin` 和 `DELETE /api/v1/tools/{id}/pin` 端点（@PreAuthorize ADMIN/SUPER_ADMIN）
- [x] 6.3 ToolController：添加 `GET /api/v1/tools/hot-top5` 端点（公开访问）
- [x] 6.4 ForumPostController：添加 `sortBy` 查询参数（默认 `"hot"`），传递到 Service 层
- [x] 6.5 ForumPostController：添加 `POST /api/forum/posts/{id}/pin` 和 `DELETE /api/forum/posts/{id}/pin` 端点
- [x] 6.6 ForumPostController：添加 `GET /api/forum/posts/hot-top5` 端点
- [x] 6.7 VideoController：添加 `sortBy` 查询参数（默认 `"hot"`），传递到 Service 层
- [x] 6.8 VideoController：添加 `POST /api/v1/videos/{id}/pin` 和 `DELETE /api/v1/videos/{id}/pin` 端点
- [x] 6.9 VideoController：添加 `GET /api/v1/videos/hot-top5` 端点
- [ ] 6.10 为 Controller 层编写集成测试或使用 MockMvc 测试：验证 sortBy 参数、pin/unpin 权限（403/200）、hot-top5 公开访问，运行 `cd backend && ./gradlew test` 确认通过

## 7. 后端安全配置

- [x] 7.1 SecurityConfig 中添加 hot-top5 端点到公开访问白名单（`/api/v1/tools/hot-top5`、`/api/forum/posts/hot-top5`、`/api/v1/videos/hot-top5`）
- [x] 7.2 确认 pin/unpin 端点受 JWT + @PreAuthorize 保护（ADMIN/SUPER_ADMIN）

## 8. 前端类型定义

- [x] 8.1 `types/index.ts` 中 ToolSummary 类型添加 `score`、`pinned`、`viewCount`、`likeCount`、`commentCount` 字段
- [x] 8.2 `types/forum.ts` 中 ForumPostDTO 类型添加 `score`、`pinned` 字段
- [x] 8.3 `types/video.ts` 中 Video 列表类型添加 `score`、`pinned` 字段

## 9. 前端 Service 层

- [x] 9.1 `services/tool.ts`：列表请求添加 `sortBy` 参数；新增 `pinTool(id)`、`unpinTool(id)`、`getHotTop5()` 方法
- [x] 9.2 `services/forum.ts`：列表请求添加 `sortBy` 参数；新增 `pinPost(id)`、`unpinPost(id)`、`getHotTop5()` 方法
- [x] 9.3 `services/video.ts`：列表请求添加 `sortBy` 参数；新增 `pinVideo(id)`、`unpinVideo(id)`、`getHotTop5()` 方法

## 10. 前端共享组件

- [x] 10.1 创建 `components/common/SortTab.vue`：`defineProps<{ modelValue: string }>`，`defineEmits<{ (e: 'update:modelValue', value: string) }>`，"热度 | 最新" 双 Tab 切换，遵循 design-system.md 样式规范，双主题 CSS 变量

## 11. 前端卡片组件改造

- [x] 11.1 修改 ToolCard 组件：添加 `pinned` prop，pinned=true 时显示 ArrowUp 图标；添加 `isHot` prop，isHot=true 时显示 Flame 图标；添加管理员可见的 Pin/PinOff 按钮（判断 authStore 角色），点击触发 pin/unpin API 并 emit 刷新事件
- [x] 11.2 修改 PostCard 组件：同上添加 ArrowUp 图标、Flame 图标、管理员 Pin/PinOff 按钮
- [x] 11.3 修改 VideoCard 组件：同上添加 ArrowUp 图标、Flame 图标、管理员 Pin/PinOff 按钮

## 12. 前端列表页集成

- [x] 12.1 HomePage（工具列表）：引入 SortTab 组件，添加 `sortBy` ref（默认 `"hot"`），列表请求携带 sortBy 参数；页面加载时请求 hot-top5 缓存为 Set；传递 `pinned` 和 `isHot` 给 ToolCard；替换原有 sortBy select 为 SortTab
- [x] 12.2 PostListPage（论坛列表）：引入 SortTab 组件，添加 `sortBy` ref，修改 forumStore 或 service 调用携带 sortBy；页面加载时请求 hot-top5；传递标识给 PostCard
- [x] 12.3 VideoListPage（微课列表）：引入 SortTab 组件，添加 `sortBy` ref；页面加载时请求 hot-top5；传递标识给 VideoCard；注意 VideoListPage 使用"加载更多"分页，切换排序时需清空列表重新请求

## 13. 全量验证

- [x] 13.1 运行后端全量测试 `cd backend && ./gradlew test`，确认所有单元测试通过
- [x] 13.2 启动后端+前端，手动验证三个列表页：热度排序（置顶在前）、最新排序、排序切换、管理员置顶/取消置顶、置顶图标显示、火苗图标显示
- [x] 13.3 验证双主题（暗色/亮色）下置顶图标和火苗图标颜色正确
- [x] 13.4 验证权限控制：普通用户无法看到置顶按钮，未登录用户访问 pin 接口返回 401，USER 角色访问返回 403
- [x] 13.5 运行 `bash scripts/lint-arch.sh` 确认后端层级依赖未被破坏
