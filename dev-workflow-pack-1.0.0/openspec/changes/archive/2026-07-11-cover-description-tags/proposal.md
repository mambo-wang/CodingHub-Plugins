## 为什么（Why）

当前 CodingHub 平台存在三个体验短板：

1. **微课缺少封面**：视频列表中 `coverUrl` 字段始终为空，用户无法直观预览视频内容，降低点击率。
2. **工具卡片信息不足**：工具列表仅展示名称和分类，缺少简短描述，用户需进入详情页才能了解工具用途，浏览效率低。
3. **标签体系不完整**：论坛已有 `ForumTag` 半成品（后端存在但前端未接入），工具和微课完全没有标签，无法跨模块进行内容分类与发现。

本次变更将一次性补齐上述能力，提升平台内容的可发现性与用户体验。

## 变更内容（What Changes）

- **新增**：微课封面设置功能——前端通过 `<video>` + `<canvas>` 截取视频帧，以图片形式上传至后端，存储为封面
- **新增**：`Tool` 实体的 `description` 字段（VARCHAR 200，纯文本短描述），独立于现有 `content`（Markdown 正文）
- **新增**：统一标签体系——跨模块共享的 `Tag` 实体（`type` 字段区分 TOOL/FORUM/VIDEO），各模块独立关联表（`tool_tag`、`video_tag`），复用现有 `forum_post_tag`
- **新增**：前端通用 `TagSelector` 组件，支持选择已有标签和创建新标签
- **修改**：工具创建/编辑表单增加"描述"输入框
- **修改**：工具卡片组件名称下方展示描述文字
- **修改**：微课创建/编辑界面增加封面选择区域（视频帧预览 + 上传）
- **修改**：论坛帖子编辑器接入标签选择器，帖子详情/列表接口返回标签信息
- **修改**：工具、微课的创建/更新请求及列表/详情响应均携带标签信息

## 能力清单（Capabilities）

### 新增能力（New Capabilities）

- `video-cover`: 微课封面功能——前端 Canvas 截屏 + 封面图片上传 + 后端存储与访问
- `unified-tag`: 统一标签体系——跨模块 Tag 实体、标签 CRUD API、前端 TagSelector 组件、各模块标签关联

### 修改能力（Modified Capabilities）

- `tool-modify-delete`: 工具创建/更新接口新增 `description` 字段，列表/详情接口返回 `description`
- `video-core`: 微课创建/更新流程集成封面设置与标签关联
- `forum-post`: 论坛帖子创建/更新流程集成标签选择器，帖子 DTO 返回标签列表

## 影响范围（Impact）

**后端代码**：
- `model/Tool.java` — 新增 `description` 字段
- `model/tag/Tag.java` — 新增统一标签实体
- `model/tag/ToolTag.java`、`model/tag/VideoTag.java` — 新增关联表实体
- `dto/CreateToolRequest.java`、`dto/UpdateToolRequest.java` — 新增 `description`、`tagIds`
- `dto/ToolSummaryDTO.java`、`dto/ToolDetailDTO.java` — 新增 `description`、`tags`
- `dto/video/VideoUploadRequest.java`、`dto/video/VideoUpdateRequest.java` — 新增 `tagIds`
- `dto/video/VideoResponse.java`、`dto/video/VideoListItem.java` — 新增 `tags`
- `dto/forum/ForumPostDTO.java` — 新增 `tags` 字段
- `service/ToolService.java` — 处理 description 和标签关联
- `service/video/VideoService.java` — 处理封面上传和标签关联
- `service/tag/TagService.java` — 新增统一标签服务
- `controller/tag/TagController.java` — 新增标签 API
- `controller/ToolController.java` — 接口适配新字段
- `controller/video/VideoController.java` — 新增封面上传端点
- `repository/` — 新增 TagRepository、ToolTagRepository、VideoTagRepository
- `config/` — 可能需要新增封面图片的静态资源服务配置
- 数据库：`tool` 表新增 `description` 列；新增 `tag`、`tool_tag`、`video_tag` 表

**前端代码**：
- `components/TagSelector.vue` — 新增通用标签选择组件
- `components/ToolCard.vue` — 展示 description
- `pages/ToolCreatePage.vue`（或等效页面） — 增加描述输入框和标签选择器
- `pages/video/VideoUploadPage.vue` — 增加封面截屏/上传区域和标签选择器
- `pages/forum/PostEditorPage.vue` — 接入标签选择器
- `services/api.ts`、`services/video.ts`、`services/forum.ts` — 适配新字段和 API
- `types/` — 相关类型定义更新

**API 变更**：
- `POST /api/v1/tools` — 请求体新增 `description`、`tagIds`
- `PUT /api/v1/tools/{id}` — 请求体新增 `description`、`tagIds`
- `GET /api/v1/tools` — 响应新增 `description`、`tags`
- `GET /api/v1/tools/{id}` — 响应新增 `description`、`tags`
- `POST /api/v1/videos/{id}/cover` — 新增封面上传端点
- `POST /api/v1/videos` — 请求体新增 `tagIds`
- `PUT /api/v1/videos/{id}` — 请求体新增 `tagIds`
- `GET /api/v1/videos` — 响应新增 `tags`
- `GET /api/v1/videos/{id}` — 响应新增 `tags`
- `GET /api/v1/tags?type=TOOL|FORUM|VIDEO` — 新增统一标签查询
- `POST /api/v1/tags` — 新增标签创建
- `GET /api/forum/posts` — 响应新增 `tags`
- `GET /api/forum/posts/{id}` — 响应新增 `tags`
- `POST /api/forum/posts` — 请求体 `tagIds` 行为对齐（已定义但未生效）
- `PUT /api/forum/posts/{id}` — 请求体新增 `tagIds`

**依赖**：无新增外部依赖（前端 Canvas API 为浏览器原生能力）
