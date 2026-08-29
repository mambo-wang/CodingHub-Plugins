# Design: 微课模块（视频共享）

## 背景（Context）

CodingHub 已有完整的用户体系（User）、工具模块（Tool/ToolFile）和论坛模块（ForumPost/ForumComment/ForumLike/PostFavorite）。微课模块是全新的视频共享功能，参考论坛模块的互动模式构建。

**约束条件：**
- 技术栈：Java 17 / Spring Boot 3.2.5 + Vue 3 / TypeScript + Pure CSS（无 Tailwind）
- 数据库：MySQL 8.x，JPA/Hibernate
- 认证：JWT，Bearer Token
- 已有 XSS 防护工具：`XssSanitizer`
- UI 风格：Cyberpunk Glassmorphism 双主题（暗色/亮色）
- 已有论坛互动模式（点赞、收藏）可供参考

**MVP 阶段决策：**
- 存储：本地磁盘（`uploads/videos/`）
- 播放：直接 MP4，不转码，HTTP Range 支持
- 上传限制：单文件 ≤ 1GB，仅允许 MP4 格式
- 不包含：弹幕、视频分类、分片上传、OSS

## 目标 / 非目标（Goals / Non-Goals）

**Goals：**
- 实现视频上传、列表、详情、流式播放的完整闭环
- 实现点赞、评论、收藏互动功能
- 播放体验：支持边下边播（HTTP Range）
- 复用已有架构模式，保持代码一致性
- UI 遵循双主题设计系统（暗色/亮色）

**Non-Goals：**
- 不实现视频转码 / HLS 自适应码率
- 不实现弹幕系统（Phase 3）
- 不实现视频分类（暂不需要）
- 不实现分片上传（MVP 用配置放大限制）
- 不接入 OSS / CDN

## 文件结构

### Backend (Java Spring Boot)

| 文件路径 | 类型 | 操作 |
|----------|------|------|
| `model/video/Video.java` | 实体 | 新增 |
| `model/video/VideoComment.java` | 实体 | 新增 |
| `model/video/VideoLike.java` | 实体 | 新增 |
| `model/video/VideoFavorite.java` | 实体 | 新增 |
| `model/video/VideoStatus.java` | 枚举 | 新增 |
| `repository/video/VideoRepository.java` | Repository | 新增 |
| `repository/video/VideoCommentRepository.java` | Repository | 新增 |
| `repository/video/VideoLikeRepository.java` | Repository | 新增 |
| `repository/video/VideoFavoriteRepository.java` | Repository | 新增 |
| `dto/video/VideoUploadRequest.java` | DTO | 新增 |
| `dto/video/VideoUpdateRequest.java` | DTO | 新增 |
| `dto/video/VideoResponse.java` | DTO | 新增 |
| `dto/video/VideoListItem.java` | DTO | 新增 |
| `dto/video/VideoCommentRequest.java` | DTO | 新增 |
| `dto/video/VideoCommentResponse.java` | DTO | 新增 |
| `dto/video/VideoInteractionResponse.java` | DTO | 新增 |
| `service/video/VideoService.java` | Service | 新增 |
| `service/video/VideoInteractionService.java` | Service | 新增 |
| `controller/video/VideoController.java` | Controller | 新增 |
| `controller/video/VideoInteractionController.java` | Controller | 新增 |
| `config/VideoStorageConfig.java` | Config | 新增 |
| `config/SecurityConfig.java` | Config | **修改** |
| `application.yaml` | 配置 | **修改** |

### Frontend (Vue 3 + TypeScript)

| 文件路径 | 操作 |
|----------|------|
| `pages/video/VideoListPage.vue` | 新增 |
| `pages/video/VideoDetailPage.vue` | 新增 |
| `pages/video/VideoUploadPage.vue` | 新增 |
| `components/video/VideoCard.vue` | 新增 |
| `components/video/VideoPlayer.vue` | 新增 |
| `components/video/VideoCommentList.vue` | 新增 |
| `services/video.ts` | 新增 |
| `types/video.ts` | 新增 |
| `router/index.ts` | **修改** |
| `components/Header.vue` | **修改** |
| `pages/ProfilePage.vue` | **修改** |

### 数据库迁移

| 文件 | 说明 |
|------|------|
| `scripts/migrations/add-video-tables.sql` | 新增 4 张表 + 索引 + 唯一约束 |

## 数据模型

### Video 实体

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 主键 |
| title | VARCHAR(200) | NOT NULL | 视频标题 |
| description | TEXT | NULL | 视频描述 |
| file_path | VARCHAR(500) | NOT NULL | 磁盘存储路径 |
| file_name | VARCHAR(255) | NOT NULL | 原始文件名 |
| file_size | BIGINT | NOT NULL | 文件大小（字节） |
| duration | INT | DEFAULT 0 | 视频时长（秒），前端上报 |
| cover_url | VARCHAR(500) | NULL | 封面图 URL（可选） |
| uploader_id | BIGINT | FK → user(id), NOT NULL | 上传者 |
| status | ENUM('NORMAL','DELETED') | DEFAULT 'NORMAL' | 软删除状态 |
| view_count | INT | DEFAULT 0 | 播放次数 |
| like_count | INT | DEFAULT 0 | 点赞次数（冗余计数） |
| comment_count | INT | DEFAULT 0 | 评论次数（冗余计数） |
| created_at | DATETIME | NOT NULL | 创建时间 |
| updated_at | DATETIME | NOT NULL | 更新时间 |

**索引：** `idx_video_uploader (uploader_id, status)`、`idx_video_status_created (status, created_at DESC)`

### VideoComment 实体

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 主键 |
| video_id | BIGINT | FK → video(id), NOT NULL | 所属视频 |
| user_id | BIGINT | FK → user(id), NOT NULL | 评论者 |
| content | TEXT | NOT NULL | 评论内容（XSS 过滤后） |
| created_at | DATETIME | NOT NULL | 创建时间 |

**索引：** `idx_video_comment_video (video_id, created_at DESC)`

### VideoLike 实体

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 主键 |
| video_id | BIGINT | FK → video(id), NOT NULL | 所属视频 |
| user_id | BIGINT | FK → user(id), NOT NULL | 点赞者 |
| created_at | DATETIME | NOT NULL | 点赞时间 |

**唯一约束：** `uk_video_like (video_id, user_id)`

### VideoFavorite 实体

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | BIGINT | PK, AUTO_INCREMENT | 主键 |
| video_id | BIGINT | FK → video(id), NOT NULL | 收藏视频 |
| user_id | BIGINT | FK → user(id), NOT NULL | 收藏者 |
| created_at | DATETIME | NOT NULL | 收藏时间 |

**唯一约束：** `uk_video_favorite (video_id, user_id)`

## API 设计

### 视频核心 API

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | `/api/videos` | ✅ | 上传视频（multipart/form-data） |
| GET | `/api/videos` | ❌ | 视频列表（分页） |
| GET | `/api/videos/{id}` | 可选 | 视频详情（含互动状态，viewCount +1） |
| PUT | `/api/videos/{id}` | ✅ | 更新标题/描述（仅上传者） |
| DELETE | `/api/videos/{id}` | ✅ | 软删除（仅上传者） |
| GET | `/api/videos/{id}/stream` | ❌ | 流式播放（HTTP Range） |
| GET | `/api/videos/my` | ✅ | 我上传的视频 |

### 视频互动 API

| 方法 | 路径 | 认证 | 说明 |
|------|------|------|------|
| POST | `/api/videos/{id}/like` | ✅ | 点赞/取消点赞（toggle） |
| POST | `/api/videos/{id}/favorite` | ✅ | 收藏/取消收藏（toggle） |
| GET | `/api/videos/{id}/comments` | ❌ | 评论列表（分页） |
| POST | `/api/videos/{id}/comments` | ✅ | 发表评论 |
| GET | `/api/videos/my/favorites` | ✅ | 我的收藏列表（分页） |

## 关键技术决策

### D1: 视频流式播放 — HTTP Range

使用 Spring `ResourceRegion` 实现 HTTP Range 请求。`VideoController.streamVideo()` 返回 `ResponseEntity<ResourceRegion>`，支持 200（完整）/ 206（Partial）/ 416（越界）三种状态码。

### D2: 大文件上传 — 配置放大

```yaml
spring.servlet.multipart:
  max-file-size: 1GB
  max-request-size: 1GB
  file-size-threshold: 2MB  # 超过 2MB 写临时文件，避免 OOM
```

**扩展预留：** `VideoService.upload()` 接收 `MultipartFile`，后续分片上传新增 `VideoChunkController` 即可。

### D3: 存储路径

```
uploads/videos/{userId}/{videoId}/original.mp4
```

按两级目录组织，路径存储于 `Video.filePath`。

### D4: 点赞/收藏 — Toggle 模式

同一 POST 接口，存在记录则删除（取消），不存在则创建。返回 `{liked/favorited: true/false}` 更新前端状态。

### D5: Security 配置更新

免登录白名单新增：
- `GET /api/videos`
- `GET /api/videos/{id}`
- `GET /api/videos/{id}/stream`
- `GET /api/videos/{id}/comments`

## 风险 / 权衡（Risks / Trade-offs）

| 风险 | 缓解措施 |
|------|----------|
| 1GB 文件上传占用内存 | `file-size-threshold=2MB` 写临时文件；后续可加分片上传 |
| 本地磁盘空间有限 | MVP 可接受；后续通过 `VideoStorageService` 接口迁移 OSS |
| MP4 编码兼容性（H.265） | 前端提示「建议 H.264 编码」；后续加转码解决 |
| 播放量无防刷 | MVP 可接受；后续 IP 限频或 session 去重 |

## 迁移计划（Migration Plan）

1. 执行 `scripts/migrations/add-video-tables.sql` 创建 4 张表
2. 修改 `application.yaml` 增大 multipart 限制
3. 部署后端（Security 配置自动生效）
4. 部署前端（新增路由和页面）

**回滚策略：** 微课模块完全独立，删除新增表 + 恢复 SecurityConfig 即可回滚，不影响现有功能。

## 待定问题（Open Questions）

（当前无未解决问题，所有关键决策已在探索阶段确认）
