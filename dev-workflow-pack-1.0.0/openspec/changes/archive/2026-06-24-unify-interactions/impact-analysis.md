# 代码影响范围分析

## 改动类型评估

**风险等级：L2**（修改 schema + 修改公共 API + 修改业务规则）

本次变更涉及 10 张旧表废弃、3 张新表创建、统一 API 端点替换、前端多页面改造。属于大规模重构。

## 后端影响分析

### 直接受影响的 Service（将被废弃/迁移）

| Service | 受影响方法 | 调用方 |
|---------|-----------|--------|
| ToolService | likeTool, unlikeTool, isLikedByUser, addComment, getComments | ToolController |
| ForumLikeService | likePost, unlikePost, likeComment | ForumLikeController |
| ForumCommentService | getCommentsByPostId, createComment, createReply, deleteComment | ForumCommentController |
| PostFavoriteService | addFavorite, removeFavorite, getUserFavorites, isFavorited, getUserFavoritePosts | PostFavoriteController |
| VideoInteractionService | toggleLike, addComment, getComments, toggleFavorite, getMyFavorites | VideoController |

### 隐藏依赖（design.md 未列出但受影响）

| 文件 | 依赖关系 | 影响说明 |
|------|---------|---------|
| **VideoService.java** | 直接注入 VideoLikeRepository 和 VideoFavoriteRepository，用于查询 userLiked/userFavorited 标记视频详情 | 旧 Repository 废弃后，VideoService 需改为查询 unified_like/unified_favorite |
| **PostCard.vue** | 前端组件内调用 postFavoriteApi.toggleFavorite() | 需改用统一收藏 API |
| **HomePage.vue** | 工具详情页引用 ToolLikeButton、ToolCommentEditor | 需替换为 Unified 组件 |

### MCP 层影响

| 组件 | 是否受影响 | 说明 |
|------|-----------|------|
| IaihubToolHandler | ❌ 不受影响 | 仅调用 ToolService.createTool/updateTool，不调用 like/comment 方法 |
| McpSdkServerConfig | ❌ 不受影响 | 无直接依赖被废弃的 Service |

### 受影响的 Repository（将被废弃）

| Repository | 依赖实体 |
|-----------|---------|
| ToolLikeRepository | ToolLike → unified_like |
| ToolCommentRepository | ToolComment → unified_comment |
| ForumLikeRepository | ForumLike → unified_like |
| ForumCommentRepository | ForumComment → unified_comment |
| PostFavoriteRepository | PostFavorite → unified_favorite |
| VideoLikeRepository | VideoLike → unified_like |
| VideoCommentRepository | VideoComment → unified_comment |
| VideoFavoriteRepository | VideoFavorite → unified_favorite |

### 受影响的测试文件

| 测试文件 | 状态 | 处理建议 |
|---------|------|---------|
| ToolServiceTest.java | 需更新 | 移除 likeTool/unlikeTool/addComment 相关测试用例 |
| PostFavoriteServiceTest.java | 需重写 | 替换为 UnifiedFavoriteService 测试 |
| VideoInteractionServiceTest.java | 需重写 | 拆分为 UnifiedLikeService + UnifiedCommentService + UnifiedFavoriteService 测试 |
| PostFavoriteRepositoryTest.java | 需删除 | 旧 Repository 废弃 |

## 前端影响分析

### 受影响的页面

| 页面 | 改动类型 | 复杂度 |
|------|---------|--------|
| HomePage.vue | 添加 GeneralizedSidebar + 替换交互组件 | 中 |
| DetailPage.vue | 替换 ToolLikeButton/ToolCommentList/ToolCommentEditor + 添加收藏 | 高 |
| MyToolsPage.vue | 添加 GeneralizedSidebar 布局 | 低 |
| PostListPage.vue | SidebarNav → GeneralizedSidebar | 低 |
| MyPostsPage.vue | SidebarNav → GeneralizedSidebar | 低 |
| MyFavoritesPage.vue | SidebarNav → GeneralizedSidebar + 统一收藏 API | 中 |
| PostDetailPage.vue | 替换点赞/评论/收藏组件 | 高 |
| VideoListPage.vue | 添加 GeneralizedSidebar | 低 |
| VideoDetailPage.vue | 替换点赞/评论/收藏组件 | 高 |
| ProfilePage.vue | 移除视频/收藏 tab | 低 |

### 受影响的组件

| 组件 | 处理 |
|------|------|
| ToolLikeButton.vue | 废弃 → UnifiedLikeButton |
| ToolCommentList.vue | 废弃 → UnifiedCommentSection |
| ToolCommentEditor.vue | 废弃 → UnifiedCommentSection 内置 |
| SidebarNav.vue (forum) | 废弃 → GeneralizedSidebar |
| VideoCommentList.vue | 废弃 → UnifiedCommentSection |
| PostCard.vue | 改造：替换 postFavoriteApi 调用 |

## 设计修正建议

design.md 遗漏了以下受影响文件，建议补充：

1. **VideoService.java** — 需要在任务中增加：修改 VideoService 中的 userLiked/userFavorited 查询逻辑，改用 UnifiedLikeRepository/UnifiedFavoriteRepository
2. **PostCard.vue** — 需要在任务中增加：替换 postFavoriteApi 调用为统一收藏 API
3. **VideoServiceTest.java** — 测试文件列表中未列出，但实际受影响
4. **ToolServiceTest.java** — 需移除 likeTool 相关测试用例

## 架构层级检查

```
✓ 架构层级检查通过
```

新增的 UnifiedInteractionController (L4) → UnifiedLikeService/CommentService/FavoriteService (L3) → UnifiedLikeRepository/CommentRepository/FavoriteRepository (L2) → 实体 (L1)，层级依赖合法。

## 回归测试建议

| 测试范围 | 优先级 | 说明 |
|---------|--------|------|
| 统一点赞 API (登录 + 匿名) | P0 | 核心新功能 |
| 统一评论 API (顶层 + 嵌套) | P0 | 核心新功能 |
| 统一收藏 API (三个模块) | P0 | 核心新功能 + 工具收藏是新功能 |
| 视频详情页 userLiked/userFavorited | P1 | 隐藏依赖，容易遗漏 |
| PostCard 收藏按钮 | P1 | 隐藏依赖 |
| MCP 工具创建/修改 | P2 | 理论上不受影响，但需冒烟验证 |
| 数据迁移完整性 | P0 | 新旧表数据量对比 |
