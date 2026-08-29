## 为什么（Why）

工具（Tool）、论坛（Forum）、微课（Video）三个模块的点赞、评论、收藏功能各自独立实现，存在 10 张结构高度相似的数据库表、3 套重复的 Service/Repository 代码、以及 3 种不一致的前端导航布局。工具模块甚至缺少收藏功能。这种碎片化增加了维护成本，且导致用户体验不一致。现在是内容审核刚完成、模块结构相对稳定的窗口期，适合做一次统一重构。

## 变更内容（What Changes）

- **新增** `unified_like`、`unified_comment`、`unified_favorite` 三张通用表，使用 `target_type`（VARCHAR）+ `target_id` 多态设计，替代现有 10 张独立表
- **新增** 统一交互 API `/api/v1/interactions/*`（likes、comments、favorites），替代三个模块各自独立的点赞/评论/收藏端点
- **新增** `GeneralizedSidebar` 通用侧边栏组件，替代论坛专属的 `SidebarNav`，工具/微课页面统一采用左导航布局（列表/我的/收藏）
- **新增** 工具收藏功能（之前不存在）
- **新增** 工具和微课评论支持嵌套回复（对齐论坛的 parentId/rootId 模式）
- **新增** 全模块匿名点赞支持（对齐论坛的 ip_hash 模式）
- **BREAKING** 移除评论点赞功能（简化统一表结构）
- **BREAKING** 现有 10 张交互表数据需迁移到 3 张新表，旧表标记废弃
- **BREAKING** 现有三个模块的点赞/评论/收藏 API 端点废弃，统一收口到 `/api/v1/interactions/*`

## 能力清单（Capabilities）

### 新增能力（New Capabilities）

- `unified-interactions`: 统一的点赞/评论/收藏后端能力，包含 3 张通用表、统一 Service 层、统一 REST API（`/api/v1/interactions/*`），支持匿名点赞和嵌套评论
- `unified-sidebar-nav`: 通用侧边栏导航组件 `GeneralizedSidebar`，三个模块共用的前端导航布局（列表/我的XX/我的收藏）

### 修改能力（Modified Capabilities）

- `forum-like`: 论坛点赞逻辑迁移到 unified-interactions，原 forum_like 表废弃
- `forum-comment`: 论坛评论逻辑迁移到 unified-interactions，移除评论点赞，原 forum_comment 表废弃
- `forum-favorites-and-nav`: 论坛收藏和导航迁移到统一方案，原 post_favorites 表废弃，SidebarNav 替换为 GeneralizedSidebar
- `tool-modify-delete`: 工具模块新增收藏能力，工具评论新增嵌套回复，工具点赞迁移到统一方案

## 影响范围（Impact）

**数据库**：新增 3 张表，废弃 10 张旧表（tool_like、tool_comment、forum_like、forum_comment、post_favorites、video_like、video_comment、video_favorite），需要数据迁移脚本

**后端**：新增 UnifiedInteractionController、UnifiedLikeService、UnifiedCommentService、UnifiedFavoriteService 及其 Repository；废弃 ToolService 中的 likeTool/unlikeTool/addComment、ForumLikeService、ForumCommentService、PostFavoriteService、VideoInteractionService 中的 toggleLike/toggleFavorite/addComment 等方法和对应 Controller 端点

**前端**：新增 GeneralizedSidebar 组件、工具收藏页面（/my-favorites）、微课我的视频页面（/videos/my-videos）、微课收藏页面（/videos/my-favorites）；改造 HomePage、VideoListPage 加入侧边栏布局；MyToolsPage 路由合并；ProfilePage 移除「我的视频」「我的收藏」tab；所有详情页的点赞/评论/收藏组件改用统一 API

**API 兼容性**：旧端点（`/api/v1/tools/{id}/like`、`/api/forum/likes`、`/api/v1/videos/{id}/like` 等）需标记废弃并在过渡期保留，新端点统一为 `/api/v1/interactions/*`
