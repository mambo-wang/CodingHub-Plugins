## REMOVED Requirements

### Requirement: 论坛点赞系统
**原因**：论坛点赞功能已迁移到统一的 `unified-interactions` 能力，通过 `/api/v1/interactions/likes` 端点提供服务，forum_like 表废弃。

**迁移方案**：
- API 迁移：`POST /api/forum/likes` → `POST /api/v1/interactions/likes`（body 中 `postId` 改为 `targetType: "FORUM_POST", targetId`）
- API 迁移：`DELETE /api/forum/likes` → `POST /api/v1/interactions/likes`（统一为 toggle 模式）
- 匿名点赞：ip_hash 机制保留，统一到 unified_like 表
- 评论点赞（Scenario 7/8）：功能移除，不再支持评论级别的点赞
