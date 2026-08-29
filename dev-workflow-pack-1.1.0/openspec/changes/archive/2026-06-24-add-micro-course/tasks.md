# Tasks: 微课模块（视频共享）

## 1. 数据库 & 配置

- [x] 1.1 创建数据库迁移脚本 `scripts/migrations/add-video-tables.sql`：video、video_comment、video_like、video_favorite 四张表，含索引和唯一约束
- [x] 1.2 执行迁移脚本，验证表结构创建成功
- [x] 1.3 修改 Spring 配置：`spring.servlet.multipart.max-file-size=1GB`、`max-request-size=1GB`、`file-size-threshold=2MB`
- [x] 1.4 新增 `VideoStorageConfig.java`：配置视频存储根路径 `uploads/videos/`，启动时自动创建目录

## 2. 后端 Model 层

- [x] 2.1 创建 `VideoStatus.java` 枚举（NORMAL, DELETED）
- [x] 2.2 创建 `Video.java` 实体：含 title、description、filePath、fileName、fileSize、duration、coverUrl、uploaderId、status、viewCount、likeCount、commentCount、createdAt、updatedAt，以及 `@PrePersist`/`@PreUpdate` 生命周期钩子
- [x] 2.3 创建 `VideoComment.java` 实体：含 videoId、userId、content、createdAt
- [x] 2.4 创建 `VideoLike.java` 实体：含 videoId、userId、createdAt，唯一约束 (videoId, userId)
- [x] 2.5 创建 `VideoFavorite.java` 实体：含 videoId、userId、createdAt，唯一约束 (videoId, userId)

## 3. 后端 Repository 层

- [x] 3.1 创建 `VideoRepository.java`：含 `findByStatusAndCreatedAtDesc`（分页）、`findByUploaderIdAndStatus`、`findByIdAndStatus` 方法
- [x] 3.2 创建 `VideoCommentRepository.java`：含 `findByVideoIdOrderByCreatedAtDesc`（分页）方法
- [x] 3.3 创建 `VideoLikeRepository.java`：含 `findByVideoIdAndUserId`、`existsByVideoIdAndUserId`、`deleteByVideoIdAndUserId` 方法
- [x] 3.4 创建 `VideoFavoriteRepository.java`：含 `findByUserIdOrderByCreatedAtDesc`（分页）、`findByVideoIdAndUserId`、`existsByVideoIdAndUserId`、`deleteByVideoIdAndUserId` 方法

## 4. 后端 DTO 层

- [x] 4.1 创建 `VideoUploadRequest.java`：title（@NotBlank, max 200）、description（可选）
- [x] 4.2 创建 `VideoUpdateRequest.java`：title（@NotBlank, max 200）、description（可选）
- [x] 4.3 创建 `VideoResponse.java`：视频详情响应（含 userLiked、userFavorited 字段）
- [x] 4.4 创建 `VideoListItem.java`：列表精简响应（id、title、coverUrl、duration、viewCount、likeCount、commentCount、uploaderName、createdAt）
- [x] 4.5 创建 `VideoCommentRequest.java`：content（@NotBlank）
- [x] 4.6 创建 `VideoCommentResponse.java`：id、content、userId、userNickname、userAvatarUrl、createdAt
- [x] 4.7 创建 `VideoInteractionResponse.java`：liked/favorited 状态 + 计数

## 5. 后端 Service 层 — 视频核心

- [x] 5.1 创建 `VideoService.java`：实现 `uploadVideo()` — 校验 MP4 格式、保存文件到 `uploads/videos/{userId}/{videoId}/`、创建 Video 记录
- [x] 5.2 实现 `getVideoList()` — 分页查询 NORMAL 状态视频，按 createdAt 倒序，关联查询上传者昵称
- [x] 5.3 实现 `getVideoDetail()` — 查询视频详情，自动 viewCount +1，若登录则查询 userLiked/userFavorited 状态
- [x] 5.4 实现 `updateVideo()` — 校验上传者权限，更新 title 和 description
- [x] 5.5 实现 `deleteVideo()` — 校验上传者权限，软删除（status = DELETED）
- [x] 5.6 实现 `streamVideo()` — 返回 `Resource` 对象，支持 HTTP Range（使用 `UrlResource` + `ResourceRegion`）
- [x] 5.7 实现 `getMyVideos()` — 查询当前登录用户上传的视频列表

## 6. 后端 Service 层 — 互动功能

- [x] 6.1 创建 `VideoInteractionService.java`：实现 `toggleLike()` — toggle 模式，存在则删除（取消），不存在则创建（点赞），同步更新 Video.likeCount
- [x] 6.2 实现 `addComment()` — 校验 content 非空，XSS 过滤，创建 VideoComment，同步更新 Video.commentCount
- [x] 6.3 实现 `getComments()` — 分页查询评论列表，关联查询用户昵称和头像
- [x] 6.4 实现 `toggleFavorite()` — toggle 模式，同步更新收藏状态
- [x] 6.5 实现 `getMyFavorites()` — 分页查询当前用户收藏的 NORMAL 状态视频

## 7. 后端 Controller 层

- [x] 7.1 创建 `VideoController.java`：POST /api/videos、GET /api/videos、GET /api/videos/{id}、PUT /api/videos/{id}、DELETE /api/videos/{id}、GET /api/videos/{id}/stream、GET /api/videos/my
- [x] 7.2 创建 `VideoInteractionController.java`：POST /api/videos/{id}/like、POST /api/videos/{id}/favorite、GET /api/videos/{id}/comments、POST /api/videos/{id}/comments、GET /api/videos/my/favorites
- [x] 7.3 更新 `SecurityConfig.java`：将 GET /api/videos/**、GET /api/videos/{id}/stream、GET /api/videos/{id}/comments 加入白名单（免登录）

## 8. 后端单元测试

- [x] 8.1 编写 VideoService 单元测试：上传成功、格式校验失败、超大文件、权限校验
- [x] 8.2 编写 VideoInteractionService 单元测试：点赞 toggle、评论 XSS 过滤、收藏 toggle、计数同步
- [x] 8.3 验证 HTTP Range 流式播放：完整请求返回 200、Range 请求返回 206、越界返回 416

## 9. 前端类型 & Service 层

- [x] 9.1 创建 `frontend/src/types/video.ts`：VideoListItem、VideoDetail、VideoComment、VideoUploadRequest 等 TypeScript 类型
- [x] 9.2 创建 `frontend/src/services/video.ts`：封装所有视频相关 API 调用（upload、getList、getDetail、stream、update、delete、getMyVideos、toggleLike、toggleFavorite、getComments、addComment、getMyFavorites）

## 10. 前端 — 视频列表页

- [x] 10.1 创建 `VideoCard.vue` 组件：视频封面/标题/播放量/点赞数/上传者/时间，遵循 design-system.md 双主题规范
- [x] 10.2 创建 `VideoListPage.vue`：网格布局展示视频卡片，支持分页加载（滚动或按钮），空状态展示
- [x] 10.3 路由配置：添加 `/videos` 路由指向 VideoListPage
- [x] 10.4 AppHeader 导航：添加「微课」入口链接

## 11. 前端 — 视频详情页

- [x] 11.1 创建 `VideoPlayer.vue` 组件：封装 HTML5 `<video>` 标签，设置 `src` 指向 stream 接口，支持 controls
- [x] 11.2 创建 `VideoCommentList.vue` 组件：评论列表（分页），评论输入框，发评论功能
- [x] 11.3 创建 `VideoDetailPage.vue`：视频播放器 + 标题/描述/统计信息 + 点赞按钮（toggle） + 收藏按钮（toggle） + 评论区
- [x] 11.4 路由配置：添加 `/videos/:id` 路由指向 VideoDetailPage

## 12. 前端 — 视频上传页

- [x] 12.1 创建 `VideoUploadPage.vue`：拖拽/点击上传区域，标题输入框（必填），描述输入框（可选），上传进度条，MP4 格式校验，文件大小提示（≤1GB）
- [x] 12.2 路由配置：添加 `/videos/upload` 路由（需登录守卫）

## 13. 前端 — 用户中心扩展

- [x] 13.1 修改 `ProfilePage.vue`：添加「我的视频」tab 和「我的收藏」tab
- [x] 13.2 实现「我的视频」列表：调用 GET /api/videos/my，展示视频卡片，支持删除操作
- [x] 13.3 实现「我的收藏」列表：调用 GET /api/videos/my/favorites，展示视频卡片

## 14. 集成验证

- [x] 14.1 启动后端，手动执行数据库迁移，验证表结构
- [x] 14.2 测试视频上传流程：上传 MP4 → 列表出现 → 点击播放 → 点赞 → 评论 → 收藏
- [x] 14.3 测试流式播放：浏览器 `<video>` 标签正常边下边播，拖动进度条不卡顿
- [x] 14.4 测试权限控制：未登录可播放但无法点赞/评论/收藏，非上传者无法编辑/删除
- [x] 14.5 测试边界情况：非 MP4 上传拒绝、超大文件拒绝、空评论拒绝、XSS 过滤生效
- [x] 14.6 双主题 UI 验证：暗色/亮色主题下所有页面样式符合 design-system.md 规范
