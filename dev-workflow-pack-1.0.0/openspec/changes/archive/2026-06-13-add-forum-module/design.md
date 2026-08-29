# Design: Add Forum Module

## File Structure

### Backend - Java/Spring Boot

```
backend/src/main/java/com/iaihub/toolbox/
├── controller/forum/
│   ├── ForumPostController.java      # /api/forum/posts
│   ├── ForumCategoryController.java  # /api/forum/categories
│   ├── ForumTagController.java       # /api/forum/tags
│   ├── ForumCommentController.java   # /api/forum/comments, /api/forum/posts/{id}/comments
│   └── ForumLikeController.java      # /api/forum/likes
├── service/forum/
│   ├── ForumPostService.java
│   ├── ForumCategoryService.java
│   ├── ForumTagService.java
│   ├── ForumCommentService.java
│   └── ForumLikeService.java
├── repository/forum/
│   ├── ForumPostRepository.java
│   ├── ForumCategoryRepository.java
│   ├── ForumTagRepository.java
│   ├── ForumCommentRepository.java
│   └── ForumLikeRepository.java
├── model/forum/
│   ├── ForumPost.java               # JPA Entity
│   ├── ForumCategory.java           # JPA Entity
│   ├── ForumTag.java                # JPA Entity
│   ├── ForumPostTag.java            # JPA Entity (ManyToMany join table)
│   ├── ForumComment.java           # JPA Entity
│   └── ForumLike.java               # JPA Entity
└── dto/forum/
    ├── ForumPostDTO.java
    ├── ForumPostCreateRequest.java
    ├── ForumCommentDTO.java
    ├── ForumCommentCreateRequest.java
    ├── ForumLikeRequest.java
    ├── ForumCategoryDTO.java
    └── ForumTagDTO.java
```

```
backend/src/test/java/com/iaihub/toolbox/
├── controller/forum/
│   ├── ForumPostControllerTest.java
│   ├── ForumCommentControllerTest.java
│   └── ForumLikeControllerTest.java
└── service/forum/
    ├── ForumPostServiceTest.java
    ├── ForumCommentServiceTest.java
    └── ForumLikeServiceTest.java
```

### Frontend - Vue 3/TypeScript

```
frontend/src/
├── pages/forum/
│   ├── PostListPage.vue             # 帖子列表页
│   ├── PostDetailPage.vue           # 帖子详情页
│   └── PostEditorPage.vue          # 帖子编辑器页
├── components/forum/
│   ├── PostCard.vue                 # 帖子卡片组件
│   ├── PostContent.vue              # Markdown 渲染内容（处理工具链接）
│   ├── CommentList.vue              # 评论列表组件
│   ├── CommentItem.vue              # 单条评论（楼中楼）
│   ├── CommentEditor.vue            # 评论输入框
│   ├── TagInput.vue                 # 标签输入组件
│   ├── CategoryFilter.vue           # 分类筛选组件
│   └── ExternalLinkMarker.vue        # 外部链接标记组件
├── services/
│   └── forum.ts                     # Forum API 调用
├── stores/
│   └── forum.ts                     # Forum 状态管理
└── types/
    └── forum.ts                     # Forum 类型定义
```

## Test Strategy

### Backend Tests

| Test File | Type | Strategy |
|-----------|------|----------|
| `ForumPostControllerTest.java` | Integration | MockMvc 测试所有 CRUD API 端点，验证分页/筛选/搜索逻辑 |
| `ForumCommentControllerTest.java` | Integration | 测试评论创建（登录/匿名）、楼中楼结构、删除权限 |
| `ForumLikeControllerTest.java` | Integration | 测试点赞创建/取消，重复点赞拦截 |
| `ForumPostServiceTest.java` | Unit | 使用 Mockito 测试业务逻辑：创建帖子、标签关联、权限检查 |
| `ForumCommentServiceTest.java` | Unit | 测试楼中楼逻辑、评论计数更新 |
| `ForumLikeServiceTest.java` | Unit | 测试点赞去重逻辑（用户 + IP hash） |

**测试命令**:
```bash
cd backend
./gradlew test --tests "*Forum*"
```

### Frontend Tests

| Test File | Type | Strategy |
|-----------|------|----------|
| `PostContent.spec.ts` | Unit | 测试 Markdown 渲染、工具链接识别、外部链接标记 |
| `forum.services.spec.ts` | Unit | 测试 API 调用层 |

**测试命令**:
```bash
cd frontend
npm run test -- --grep "Forum"
```

## Database Schema (MySQL)

```sql
-- 帖子分类
CREATE TABLE forum_category (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(255),
    sort_order INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 标签（系统预设 + 用户自创）
CREATE TABLE forum_tag (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE,
    post_count INT DEFAULT 0,
    is_system BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 帖子表
CREATE TABLE forum_post (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author_id BIGINT NOT NULL,
    category_id BIGINT NOT NULL,
    view_count INT DEFAULT 0,
    like_count INT DEFAULT 0,
    comment_count INT DEFAULT 0,
    status ENUM('NORMAL', 'DELETED', 'HIDDEN') DEFAULT 'NORMAL',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES user(id),
    FOREIGN KEY (category_id) REFERENCES forum_category(id),
    INDEX idx_forum_post_author (author_id),
    INDEX idx_forum_post_category (category_id),
    INDEX idx_forum_post_created (created_at)
);

-- 帖子-标签关联
CREATE TABLE forum_post_tag (
    post_id BIGINT NOT NULL,
    tag_id BIGINT NOT NULL,
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES forum_post(id),
    FOREIGN KEY (tag_id) REFERENCES forum_tag(id)
);

-- 评论（楼中楼）
CREATE TABLE forum_comment (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    post_id BIGINT NOT NULL,
    author_id BIGINT,
    author_name VARCHAR(50),
    parent_id BIGINT,
    root_id BIGINT,
    content TEXT NOT NULL,
    like_count INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES forum_post(id),
    FOREIGN KEY (author_id) REFERENCES user(id),
    INDEX idx_forum_comment_post (post_id),
    INDEX idx_forum_comment_root (root_id)
);

-- 点赞
CREATE TABLE forum_like (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    post_id BIGINT,
    comment_id BIGINT,
    user_id BIGINT,
    ip_hash VARCHAR(64),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CHECK (post_id IS NOT NULL OR comment_id IS NOT NULL)
);
```

## Key Implementation Notes

### 1. Anonymous Comment IP Caching
- 使用 `HttpServletRequest.getRemoteAddr()` 获取 IP
- 对 IP 进行 SHA-256 hash 存储（保护隐私）
- 首次评论时让用户输入昵称，后续同一 IP 自动填充

### 2. Markdown Tool Link Detection (Frontend)
```typescript
// PostContent.vue 处理
const processedHtml = computed(() => {
  const html = renderMarkdown(props.content)
  // 识别 /tools/\d+ 链接并添加 target="_blank"
  return html.replace(/href="(\/tools\/\d+)"/g, 'href="$1" target="_blank" rel="noopener"')
})
```

### 3. External Link Marking (Frontend)
- 识别非本站点的链接（如 `http://`, `https://` 开头且不含本域名的）
- 添加外部链接图标和样式

### 4. Tag Autocomplete
- 前端实现标签输入联想
- 调用 `GET /api/forum/tags?keyword=<input>` 获取匹配标签

### 5. Tiptap Editor Integration
- 使用 `@tiptap/vue-3` 包
- 配置基础富文本功能 + Markdown 源码模式切换