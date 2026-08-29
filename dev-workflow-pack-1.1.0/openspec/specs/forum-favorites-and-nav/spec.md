## REMOVED Requirements

### Requirement: 论坛收藏与导航
**原因**：论坛收藏功能已迁移到统一的 `unified-interactions` 能力，导航组件已替换为通用的 `GeneralizedSidebar`（由 `unified-sidebar-nav` 能力提供），post_favorites 表和 SidebarNav 组件废弃。

**迁移方案**：
- 收藏 API 迁移：`POST /api/v1/post-favorites/{postId}` → `POST /api/v1/interactions/favorites`（body 中 `targetType: "FORUM_POST", targetId`）
- 收藏列表迁移：`GET /api/v1/post-favorites/posts` → `GET /api/v1/interactions/favorites?targetType=FORUM_POST`
- 收藏状态迁移：`GET /api/v1/post-favorites/check/{postId}` → `GET /api/v1/interactions/favorites/status?targetType=FORUM_POST&targetId={id}`
- 导航组件：SidebarNav.vue 废弃，替换为 GeneralizedSidebar（props 传入论坛导航项配置）
- Scenario 3/6（未登录点赞/收藏提示）：由前端 UnifiedLikeButton 和 UnifiedFavoriteButton 组件统一处理
