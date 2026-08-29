# Tasks: Add Forum Module

## Atomic TDD Task List

---

### Feature: Database Schema - Forum Tables

- [ ] RED: 编写 SQL 迁移测试——验证 forum_category, forum_tag, forum_post, forum_post_tag, forum_comment, forum_like 表可创建
- [ ] GREEN: 最小实现——执行 database migration 创建所有 forum 相关表

---

### Feature: Model Layer - JPA Entities

#### ForumPost Entity
- [ ] RED: 编写 ForumPost 实体测试——验证字段映射、状态枚举、关联关系
- [ ] GREEN: 最小实现——创建 ForumPost.java 实体类

#### ForumCategory Entity
- [ ] RED: 编写 ForumCategory 实体测试——验证字段映射
- [ ] GREEN: 最小实现——创建 ForumCategory.java 实体类

#### ForumTag Entity
- [ ] RED: 编写 ForumTag 实体测试——验证字段映射
- [ ] GREEN: 最小实现——创建 ForumTag.java 实体类

#### ForumPostTag Entity (Join Table)
- [ ] RED: 编写 ForumPostTag 实体测试——验证复合主键
- [ ] GREEN: 最小实现——创建 ForumPostTag.java 实体类

#### ForumComment Entity
- [ ] RED: 编写 ForumComment 实体测试——验证楼中楼关联（parentId, rootId）
- [ ] GREEN: 最小实现——创建 ForumComment.java 实体类

#### ForumLike Entity
- [ ] RED: 编写 ForumLike 实体测试——验证 postId/commentId 互斥约束
- [ ] GREEN: 最小实现——创建 ForumLike.java 实体类

---

### Feature: Repository Layer

#### ForumPostRepository
- [ ] RED: 编写 ForumPostRepository 测试——验证分页查询、分类筛选、标签筛选、关键词搜索
- [ ] GREEN: 最小实现——创建 ForumPostRepository 接口

#### ForumCategoryRepository
- [ ] RED: 编写 ForumCategoryRepository 测试——验证按 sortOrder 排序
- [ ] GREEN: 最小实现——创建 ForumCategoryRepository 接口

#### ForumTagRepository
- [ ] RED: 编写 ForumTagRepository 测试——验证按 postCount 排序、模糊搜索
- [ ] GREEN: 最小实现——创建 ForumTagRepository 接口

#### ForumCommentRepository
- [ ] RED: 编写 ForumCommentRepository 测试——验证树形结构查询
- [ ] GREEN: 最小实现——创建 ForumCommentRepository 接口

#### ForumLikeRepository
- [ ] RED: 编写 ForumLikeRepository 测试——验证用户重复点赞、IP hash 重复点赞检测
- [ ] GREEN: 最小实现——创建 ForumLikeRepository 接口

---

### Feature: Service Layer

#### ForumPostService
- [ ] RED: 编写 ForumPostService 测试——验证创建帖子、标签关联、权限检查、软删除
- [ ] GREEN: 最小实现——创建 ForumPostService.java

#### ForumCategoryService
- [ ] RED: 编写 ForumCategoryService 测试——验证分类列表返回（含帖子数量）
- [ ] GREEN: 最小实现——创建 ForumCategoryService.java

#### ForumTagService
- [ ] RED: 编写 ForumTagService 测试——验证标签创建、热门标签查询
- [ ] GREEN: 最小实现——创建 ForumTagService.java

#### ForumCommentService
- [ ] RED: 编写 ForumCommentService 测试——验证楼中楼逻辑、评论计数更新
- [ ] GREEN: 最小实现——创建 ForumCommentService.java

#### ForumLikeService
- [ ] RED: 编写 ForumLikeService 测试——验证点赞去重（用户 + IP hash）、计数更新
- [ ] GREEN: 最小实现——创建 ForumLikeService.java

---

### Feature: Controller Layer - ForumPostController

- [ ] RED: 编写帖子列表 API 测试——验证分页、分类/标签筛选、关键词搜索
- [ ] GREEN: 最小实现——创建 ForumPostController.java，GET /api/forum/posts
- [ ] RED: 编写帖子详情 API 测试——验证返回 Markdown 内容、浏览数递增
- [ ] GREEN: 最小实现——创建 ForumPostController.java，GET /api/forum/posts/{id}
- [ ] RED: 编写创建帖子 API 测试——验证登录要求、标签关联
- [ ] GREEN: 最小实现——创建 ForumPostController.java，POST /api/forum/posts
- [ ] RED: 编写更新帖子 API 测试——验证作者权限校验
- [ ] GREEN: 最小实现——创建 ForumPostController.java，PUT /api/forum/posts/{id}
- [ ] RED: 编写删除帖子 API 测试——验证作者权限校验、软删除
- [ ] GREEN: 最小实现——创建 ForumPostController.java，DELETE /api/forum/posts/{id}

---

### Feature: Controller Layer - ForumCategoryController & ForumTagController

- [ ] RED: 编写分类列表 API 测试——验证返回所有分类（含帖子数量）
- [ ] GREEN: 最小实现——创建 ForumCategoryController.java，GET /api/forum/categories
- [ ] RED: 编写标签列表 API 测试——验证返回所有标签、热门标签、模糊搜索
- [ ] GREEN: 最小实现——创建 ForumTagController.java，GET /api/forum/tags, GET /api/forum/tags/hot
- [ ] RED: 编写创建标签 API 测试——验证登录要求、名称唯一性
- [ ] GREEN: 最小实现——创建 ForumTagController.java，POST /api/forum/tags

---

### Feature: Controller Layer - ForumCommentController

- [ ] RED: 编写评论列表 API 测试——验证返回树形结构
- [ ] GREEN: 最小实现——创建 ForumCommentController.java，GET /api/forum/posts/{id}/comments
- [ ] RED: 编写创建评论 API 测试——验证登录/匿名、楼中楼关系、IP 缓存
- [ ] GREEN: 最小实现——创建 ForumCommentController.java，POST /api/forum/posts/{id}/comments
- [ ] RED: 编写删除评论 API 测试——验证作者权限
- [ ] GREEN: 最小实现——创建 ForumCommentController.java，DELETE /api/forum/comments/{id}

---

### Feature: Controller Layer - ForumLikeController

- [ ] RED: 编写点赞 API 测试——验证登录/匿名点赞、互斥约束、重复点赞拦截
- [ ] GREEN: 最小实现——创建 ForumLikeController.java，POST /api/forum/likes
- [ ] RED: 编写取消点赞 API 测试——验证通过 userId 或 ipHash 识别
- [ ] GREEN: 最小实现——创建 ForumLikeController.java，DELETE /api/forum/likes

---

### Feature: DTO Layer

- [ ] RED: 编写 ForumPostDTO 测试——验证字段映射、作者昵称、分类名称
- [ ] GREEN: 最小实现——创建 ForumPostDTO.java
- [ ] RED: 编写 ForumCommentDTO 测试——验证树形结构构建
- [ ] GREEN: 最小实现——创建 ForumCommentDTO.java
- [ ] RED: 编写其他 DTO 测试——ForumPostCreateRequest, ForumCommentCreateRequest, ForumLikeRequest, ForumCategoryDTO, ForumTagDTO
- [ ] GREEN: 最小实现——创建相应 DTO 类

---

### Feature: Frontend - Services & Types

- [ ] RED: 编写 forum.ts API 服务测试——验证所有端点调用
- [ ] GREEN: 最小实现——创建 frontend/src/services/forum.ts
- [ ] RED: 编写 forum.ts 类型定义测试——验证类型正确性
- [ ] GREEN: 最小实现——创建 frontend/src/types/forum.ts

---

### Feature: Frontend - Components

#### PostCard Component
- [ ] RED: 编写 PostCard.vue 测试——验证帖子信息展示、跳转链接
- [ ] GREEN: 最小实现——创建 PostCard.vue 组件

#### PostContent Component
- [ ] RED: 编写 PostContent.vue 测试——验证 Markdown 渲染、工具链接 target="_blank"、外部链接标记
- [ ] GREEN: 最小实现——创建 PostContent.vue 组件

#### CommentList Component
- [ ] RED: 编写 CommentList.vue 测试——验证评论树形渲染
- [ ] GREEN: 最小实现——创建 CommentList.vue 组件

#### CommentItem Component
- [ ] RED: 编写 CommentItem.vue 测试——验证楼中楼样式、回复按钮
- [ ] GREEN: 最小实现——创建 CommentItem.vue 组件

#### CommentEditor Component
- [ ] RED: 编写 CommentEditor.vue 测试——验证匿名/登录模式切换、昵称输入
- [ ] GREEN: 最小实现——创建 CommentEditor.vue 组件

#### TagInput Component
- [ ] RED: 编写 TagInput.vue 测试——验证标签输入、联想、创建
- [ ] GREEN: 最小实现——创建 TagInput.vue 组件

#### CategoryFilter Component
- [ ] RED: 编写 CategoryFilter.vue 测试——验证分类筛选
- [ ] GREEN: 最小实现——创建 CategoryFilter.vue 组件

---

### Feature: Frontend - Pages

#### PostListPage
- [ ] RED: 编写 PostListPage.vue 测试——验证帖子列表、分类/标签筛选、搜索、分页
- [ ] GREEN: 最小实现——创建 PostListPage.vue 页面

#### PostDetailPage
- [ ] RED: 编写 PostDetailPage.vue 测试——验证帖子详情、Markdown 渲染、评论、点赞
- [ ] GREEN: 最小实现——创建 PostDetailPage.vue 页面

#### PostEditorPage
- [ ] RED: 编写 PostEditorPage.vue 测试——验证 Tiptap 编辑器、分类选择、标签选择、发布
- [ ] GREEN: 最小实现——创建 PostEditorPage.vue 页面

---

### Feature: Frontend - Store

- [ ] RED: 编写 forum store 测试——验证状态管理、分页状态
- [ ] GREEN: 最小实现——创建 frontend/src/stores/forum.ts

---

### Feature: Frontend - UI Design

> UI 设计由 frontend-design skill 负责，具体任务待设计完成后补充

- [ ] 待补充：UI 设计任务

---

## 执行顺序

1. **Database Schema** → Model Entities → Repositories → Services → Controllers → DTOs
2. **Frontend Services/Types** → Components → Pages → Store
3. **UI Design** 穿插在 Frontend 组件开发期间

**总计约 80+ 原子任务**