# Design

## File Structure

### Frontend (Vue 3 + TypeScript)

**Modified Files:**
- `frontend/src/components/AppHeader.vue` - 移除上传工具按钮，保留工具/论坛导航
- `frontend/src/components/forum/PostCard.vue` - 添加收藏按钮
- `frontend/src/pages/forum/PostListPage.vue` - 添加左侧导航栏（我的帖子/我的收藏）
- `frontend/src/pages/forum/PostDetailPage.vue` - 添加收藏按钮和点赞登录校验
- `frontend/src/services/api.ts` - 添加收藏 API

**New Files:**
- `frontend/src/pages/forum/MyPostsPage.vue` - 我的帖子页面
- `frontend/src/pages/forum/MyFavoritesPage.vue` - 我的收藏页面
- `frontend/src/router/index.ts` - 添加新路由

### Backend (Java 17 + Spring Boot)

**New Files:**
- `backend/src/main/java/com/iaihub/toolbox/model/PostFavorite.java` - 收藏实体
- `backend/src/main/java/com/iaihub/toolbox/repository/PostFavoriteRepository.java` - 收藏数据访问
- `backend/src/main/java/com/iaihub/toolbox/service/PostFavoriteService.java` - 收藏业务逻辑
- `backend/src/main/java/com/iaihub/toolbox/controller/PostFavoriteController.java` - 收藏 API 控制器

## Test Strategy

### Backend Tests
- `PostFavoriteRepositoryTest.java` - 单元测试，测试收藏 CRUD 操作
- `PostFavoriteServiceTest.java` - 单元测试，测试业务逻辑（登录校验、收藏状态切换）
- 使用 JUnit 5 + Mockito

### Frontend Tests
- 使用 Vitest 单元测试
- `PostCard.spec.ts` - 测试收藏按钮渲染和点击行为
- `PostListPage.spec.ts` - 测试左侧导航栏显示和点击行为

## Source Files & Test Files Mapping

| 源码文件 | 测试文件 |
|---------|---------|
| PostFavoriteRepository.java | PostFavoriteRepositoryTest.java |
| PostFavoriteService.java | PostFavoriteServiceTest.java |
| PostCard.vue | PostCard.spec.ts |
| PostListPage.vue | PostListPage.spec.ts |

## API Endpoints

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/post-favorites/{postId}` | 添加收藏 |
| DELETE | `/api/post-favorites/{postId}` | 取消收藏 |
| GET | `/api/post-favorites` | 获取当前用户收藏列表 |
| GET | `/api/post-favorites/check/{postId}` | 检查帖子是否已收藏 |

## Test Run Commands

```bash
# Backend
cd backend && ./gradlew test --tests "*PostFavorite*"

# Frontend
cd frontend && npm test -- --run
```

## Implementation Notes

1. 收藏状态用唯一索引 (user_id, post_id) 防止重复收藏
2. 前端收藏按钮点击时检查登录状态，未登录提示登录
3. 左侧导航栏对未登录用户显示但点击提示登录