# Design: 热榜页面优化

## File Structure

### Backend (Java Spring Boot)

| 文件路径 | 说明 | 类型 |
|----------|------|------|
| `src/main/java/com/iaihub/toolbox/model/Tool.java` | 修改：添加 viewCount, likeCount, commentCount, score | 实体 |
| `src/main/java/com/iaihub/toolbox/model/forum/ForumPost.java` | 修改：添加 score 字段 | 实体 |
| `src/main/java/com/iaihub/toolbox/dto/ToolRankDto.java` | 修改：添加 `id`、`score` 字段 | DTO |
| `src/main/java/com/iaihub/toolbox/dto/PostRankDto.java` | 修改：添加 `id`、`score` 字段 | DTO |
| `src/main/java/com/iaihub/toolbox/service/OverviewServiceImpl.java` | 修改：按 `score` 排序，使用真实分类 | Service |
| `src/main/java/com/iaihub/toolbox/service/ToolService.java` | 修改：添加点赞、评论、更新 score 逻辑 | Service |
| `src/main/java/com/iaihub/toolbox/controller/ToolController.java` | 修改：添加点赞/取消点赞 API | Controller |
| `src/main/java/com/iaihub/toolbox/repository/ToolRepository.java` | 检查：是否需要添加 score 排序查询 | Repository |
| `src/main/java/com/iaihub/toolbox/repository/forum/ForumPostRepository.java` | 检查：是否需要添加 score 排序查询 | Repository |
| `src/main/java/com/iaihub/toolbox/repository/ToolLikeRepository.java` | 新增：工具点赞数据访问 | Repository |

### Frontend (Vue 3 + TypeScript)

| 文件路径 | 说明 |
|----------|------|
| `frontend/src/pages/OverviewPage.vue` | 修改：标题改为"热榜"，简化装饰 |
| `frontend/src/components/StatsCard.vue` | 修改：移除过度动画 |
| `frontend/src/components/ToolRankList.vue` | 修改：添加点击跳转，简化样式 |
| `frontend/src/components/PostRankList.vue` | 修改：添加点击跳转，简化样式 |
| `frontend/src/pages/DetailPage.vue` | 修改：添加点赞按钮、评论区域，显示统计数 |
| `frontend/src/components/ToolLikeButton.vue` | 新增：点赞按钮组件 |
| `frontend/src/components/ToolCommentList.vue` | 新增：工具评论列表组件 |
| `frontend/src/components/ToolCommentEditor.vue` | 新增：工具评论编辑器组件 |
| `frontend/src/services/tool.ts` | 修改：添加点赞、评论 API 调用 |
| `frontend/src/types/overview.ts` | 修改：添加 `id`、`score` 字段到类型定义 |

### Database Migration

| 文件路径 | 说明 |
|----------|------|
| `src/main/resources/db/migration/V*.sql` | 新增：为 tool 和 forum_post 表添加统计字段 |

## Data Model Changes

### Tool.java 字段变更

| 字段名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| viewCount | Integer | 0 | 浏览次数 |
| likeCount | Integer | 0 | 点赞次数 |
| commentCount | Integer | 0 | 评论次数 |
| score | BigDecimal | BigDecimal.ZERO | 综合热度评分 |

### ForumPost.java 字段变更

| 字段名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| score | BigDecimal | BigDecimal.ZERO | 综合热度评分（ForumPost已有 viewCount, likeCount, commentCount） |

### ToolLike.java 新增实体

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | Long | 主键 |
| toolId | Long | 工具 ID |
| userId | Long | 用户 ID |
| createdAt | LocalDateTime | 点赞时间 |

## Score 计算规则

```
score = viewCount * 1 + likeCount * 3 + commentCount * 5
```

| 指标 | 权重 | 说明 |
|------|------|------|
| viewCount | × 1 | 浏览量权重最低 |
| likeCount | × 3 | 点赞量权重中等 |
| commentCount | × 5 | 评论量权重最高，代表参与度 |

## API 设计

### 工具相关 API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/tools/{id}/like` | 点赞工具 |
| DELETE | `/api/tools/{id}/like` | 取消点赞 |
| POST | `/api/tools/{id}/view` | 增加浏览量（访问详情页时调用） |
| GET | `/api/tools/{id}/likes` | 获取点赞列表 |
| GET | `/api/tools/{id}/like-status` | 获取当前用户点赞状态 |

### 工具评论相关 API（复用现有评论 API 或新增）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/tools/{id}/comments` | 添加评论 |
| GET | `/api/tools/{id}/comments` | 获取评论列表 |

## Test Strategy

### Backend Tests

- **ToolTest.java**: 测试 Tool 实体统计字段和 score 计算
- **ToolServiceTest.java**: 测试点赞、评论、updateScore 逻辑
- **ToolControllerTest.java**: 测试点赞/取消点赞 API
- **OverviewControllerTest.java**: 测试 3 个 API 端点返回正确数据
- **OverviewServiceTest.java**: 测试统计数据和 score 排序逻辑

### Frontend Tests

- **DetailPage.test.ts**: 测试工具详情页点赞、评论功能
- **ToolLikeButton.test.ts**: 测试点赞按钮状态切换
- **OverviewPage.test.ts**: 测试页面标题和布局渲染

### Test Commands

```bash
# Backend
cd backend && ./gradlew test --tests "*Tool*" -v

# Frontend
cd frontend && npm run test
```

## Implementation Changes

### 1. Tool.java Entity Changes

```java
@Entity
@Table(name = "tool", indexes = {
    @Index(name = "idx_tool_score", columnList = "score"),
    @Index(name = "idx_tool_category", columnList = "category_id, status")
})
public class Tool {

    @Column(name = "view_count")
    @Builder.Default
    private Integer viewCount = 0;

    @Column(name = "like_count")
    @Builder.Default
    private Integer likeCount = 0;

    @Column(name = "comment_count")
    @Builder.Default
    private Integer commentCount = 0;

    @Column(name = "score", precision = 10, scale = 2)
    @Builder.Default
    private BigDecimal score = BigDecimal.ZERO;

    // 更新 score 的方法
    public void updateScore() {
        this.score = BigDecimal.valueOf(this.viewCount)
            .multiply(BigDecimal.valueOf(1))
            .add(BigDecimal.valueOf(this.likeCount).multiply(BigDecimal.valueOf(3)))
            .add(BigDecimal.valueOf(this.commentCount).multiply(BigDecimal.valueOf(5)));
    }

    public void incrementViewCount() {
        this.viewCount++;
        updateScore();
    }

    public void incrementLikeCount() {
        this.likeCount++;
        updateScore();
    }

    public void decrementLikeCount() {
        if (this.likeCount > 0) this.likeCount--;
        updateScore();
    }

    public void incrementCommentCount() {
        this.commentCount++;
        updateScore();
    }
}
```

### 2. ForumPost.java Entity Changes

```java
@Entity
@Table(name = "forum_post", indexes = {
    @Index(name = "idx_forum_post_score", columnList = "score")
})
public class ForumPost {

    @Column(name = "score", precision = 10, scale = 2)
    @Builder.Default
    private BigDecimal score = BigDecimal.ZERO;

    // 更新 score 的方法
    public void updateScore() {
        this.score = BigDecimal.valueOf(this.viewCount)
            .multiply(BigDecimal.valueOf(1))
            .add(BigDecimal.valueOf(this.likeCount).multiply(BigDecimal.valueOf(3)))
            .add(BigDecimal.valueOf(this.commentCount).multiply(BigDecimal.valueOf(5)));
    }
}
```

### 3. ToolLike.java 新增实体

```java
@Entity
@Table(name = "tool_like", uniqueConstraints = {
    @UniqueConstraint(name = "uk_tool_like_tool_user", columnNames = {"tool_id", "user_id"})
})
public class ToolLike {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "tool_id", nullable = false)
    private Long toolId;

    @Column(name = "user_id", nullable = false)
    private Long userId;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
    }
}
```

### 4. ToolController 新增 API

```java
@PostMapping("/{id}/like")
public ResponseEntity<Void> likeTool(@PathVariable Long id, @AuthenticationPrincipal User user) {
    toolService.likeTool(id, user.getId());
    return ResponseEntity.ok().build();
}

@DeleteMapping("/{id}/like")
public ResponseEntity<Void> unlikeTool(@PathVariable Long id, @AuthenticationPrincipal User user) {
    toolService.unlikeTool(id, user.getId());
    return ResponseEntity.ok().build();
}

@GetMapping("/{id}/like-status")
public ResponseEntity<Boolean> getLikeStatus(@PathVariable Long id, @AuthenticationPrincipal User user) {
    boolean isLiked = toolService.isLikedByUser(id, user.getId());
    return ResponseEntity.ok(isLiked);
}
```

### 5. ToolService 新增方法

```java
@Service
public class ToolService {

    public void likeTool(Long toolId, Long userId) {
        Tool tool = toolRepository.findByIdAndStatusNormal(toolId)
            .orElseThrow(() -> new ResourceNotFoundException("Tool not found"));

        // 检查是否已点赞
        if (toolLikeRepository.existsByToolIdAndUserId(toolId, userId)) {
            return; // 已点赞，直接返回
        }

        // 保存点赞记录
        ToolLike like = ToolLike.builder()
            .toolId(toolId)
            .userId(userId)
            .build();
        toolLikeRepository.save(like);

        // 更新工具统计
        tool.incrementLikeCount();
        toolRepository.save(tool);
    }

    public void unlikeTool(Long toolId, Long userId) {
        Tool tool = toolRepository.findByIdAndStatusNormal(toolId)
            .orElseThrow(() -> new ResourceNotFoundException("Tool not found"));

        Optional<ToolLike> like = toolLikeRepository.findByToolIdAndUserId(toolId, userId);
        if (like.isPresent()) {
            toolLikeRepository.delete(like.get());
            tool.decrementLikeCount();
            toolRepository.save(tool);
        }
    }

    public boolean isLikedByUser(Long toolId, Long userId) {
        return toolLikeRepository.existsByToolIdAndUserId(toolId, userId);
    }
}
```

### 6. DTO Changes

**ToolRankDto.java**:
```java
public class ToolRankDto {
    private Long id;
    private String category;
    private String toolName;
    private BigDecimal score;
}
```

**PostRankDto.java**:
```java
public class PostRankDto {
    private Long id;
    private String category;
    private String postTitle;
    private BigDecimal score;
}
```

### 7. Frontend Changes

**DetailPage.vue**:
- 显示 viewCount、likeCount、commentCount
- 添加点赞按钮（带登录验证）
- 添加评论区域（带登录验证）

**ToolLikeButton.vue**:
```vue
<template>
  <button :class="['like-btn', { 'liked': isLiked }]" @click="handleClick">
    <ThumbsUp :size="18" />
    <span>{{ likeCount }}</span>
  </button>
</template>
```

**ToolCommentList.vue**:
- 显示评论列表
- 支持分页

**ToolCommentEditor.vue**:
- 评论输入框
- 提交按钮

### 8. Database Migration

```sql
-- 为 tool 表添加统计字段
ALTER TABLE tool ADD COLUMN view_count INT DEFAULT 0;
ALTER TABLE tool ADD COLUMN like_count INT DEFAULT 0;
ALTER TABLE tool ADD COLUMN comment_count INT DEFAULT 0;
ALTER TABLE tool ADD COLUMN score DECIMAL(10,2) DEFAULT 0;

-- 为 forum_post 表添加 score 字段
ALTER TABLE forum_post ADD COLUMN score DECIMAL(10,2) DEFAULT 0;

-- 新增 tool_like 表
CREATE TABLE tool_like (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    tool_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    created_at DATETIME,
    CONSTRAINT uk_tool_like_tool_user UNIQUE (tool_id, user_id),
    CONSTRAINT fk_tool_like_tool FOREIGN KEY (tool_id) REFERENCES tool(id),
    CONSTRAINT fk_tool_like_user FOREIGN KEY (user_id) REFERENCES user(id)
);

-- 为 score 字段添加索引（优化排序查询）
CREATE INDEX idx_tool_score ON tool(score DESC);
CREATE INDEX idx_forum_post_score ON forum_post(score DESC);

-- 初始化已有数据的 score
UPDATE tool SET score = 0;
UPDATE forum_post SET score = (COALESCE(view_count, 0) * 1 + COALESCE(like_count, 0) * 3 + COALESCE(comment_count, 0) * 5);
```

## UI Component Specification

### Page Layout - 工具详情页

```
┌─────────────────────────────────────────────────────┐
│  [返回]  工具名称                              [编辑] │
├─────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────┐  │
│  │ 工具描述内容                                   │  │
│  │                                               │  │
│  └──────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────┤
│  👁 1,234   👍 56   💬 12          分享              │
├─────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────┐  │
│  │  [👍 点赞]  [💬 评论]                        │  │
│  └──────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────┤
│  评论区                                            │
│  ┌──────────────────────────────────────────────┐  │
│  │ 评论1 - 用户A - 2024-01-01                   │  │
│  │ 评论内容...                                   │  │
│  ├──────────────────────────────────────────────┤  │
│  │ 评论2 - 用户B - 2024-01-02                   │  │
│  │ 评论内容...                                   │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │ [发表评论...]                        [发送]  │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### Responsive Strategy

- **Desktop (≥1024px)**: 双列热榜布局
- **Tablet (768px-1023px)**: 单列热榜
- **Mobile (<768px)**: 单列统计卡片，单列热榜