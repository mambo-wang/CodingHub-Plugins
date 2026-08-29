## REMOVED Requirements

### Requirement: 论坛评论系统
**原因**：论坛评论功能已迁移到统一的 `unified-interactions` 能力，通过 `/api/v1/interactions/comments` 端点提供服务，forum_comment 表废弃。

**迁移方案**：
- API 迁移：`GET /api/forum/posts/{id}/comments` → `GET /api/v1/interactions/comments?targetType=FORUM_POST&targetId={id}`
- API 迁移：`POST /api/forum/posts/{id}/comments` → `POST /api/v1/interactions/comments`（body 中包含 targetType, targetId）
- API 迁移：`DELETE /api/forum/comments/{id}` → `DELETE /api/v1/interactions/comments/{id}`
- 嵌套回复：parentId/rootId 机制保留，迁移到 unified_comment 表
- 匿名评论：authorName 字段保留为 unified_comment.user_name
- 评论点赞计数（likeCount）：保留在 unified_comment 表中但点赞功能已移除（likeCount 将始终为 0）
