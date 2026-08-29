## 1. 数据库 Schema 迁移

- [x] 1.1 编写 SQL 迁移脚本：`tool` 表新增 `description` VARCHAR(200) 列
- [x] 1.2 编写 SQL 迁移脚本：创建 `tag` 表（id, name, tag_type, usage_count, created_at），唯一约束 (name, tag_type)
- [x] 1.3 编写 SQL 迁移脚本：创建 `tool_tag` 关联表（tool_id, tag_id 复合主键 + 外键）
- [x] 1.4 编写 SQL 迁移脚本：创建 `video_tag` 关联表（video_id, tag_id 复合主键 + 外键）
- [x] 1.5 处理 `forum_post_tag`：清空旧数据并添加指向新 tag 表的外键，或创建 `forum_post_tag_v2` 关联新 tag 表
- [x] 1.6 执行迁移脚本并在 Makefile 中更新 `make db` target

## 2. 统一标签后端核心（Tag Entity / Repository / Service / Controller / DTO）

- [x] 2.1 创建 `Tag` 实体：`model/tag/Tag.java`，包含 id、name（VARCHAR 50）、tagType（枚举 TOOL/FORUM/VIDEO）、usageCount、createdAt
- [x] 2.2 创建 `TagType` 枚举：TOOL, FORUM, VIDEO
- [x] 2.3 创建 `TagRepository`：`repository/tag/TagRepository.java`，含 findByTagType、findByNameAndTagType、findTopByTagTypeOrderByUsageCountDesc
- [x] 2.4 创建 `TagDTO`：`dto/tag/TagDTO.java`（id, name, tagType, usageCount）
- [x] 2.5 创建 `CreateTagRequest`：`dto/tag/CreateTagRequest.java`（name, type），含校验注解
- [x] 2.6 创建 `TagService`：`service/tag/TagService.java`，实现 createOrGet(name, type)、getTagsByType(type)、getHotTags(type, limit)、incrementUsage(tagId)、decrementUsage(tagId)
- [x] 2.7 创建 `TagController`：`controller/tag/TagController.java`，端点 GET /api/v1/tags（?type=）、GET /api/v1/tags/hot（?type=&limit=）、POST /api/v1/tags
- [x] 2.8 更新 SecurityConfig 放行标签查询接口（GET /api/v1/tags 和 /api/v1/tags/hot 无需认证）
- [ ] 2.9 后端单元测试：为 TagService 编写测试（创建标签、重复创建幂等、同名不同类、热门排序），运行 `cd backend && ./gradlew test` 确认通过

## 3. 工具描述字段（后端）

- [x] 3.1 `Tool.java` 新增 `description` 字段（VARCHAR 200, nullable），加 @Column 注解
- [x] 3.2 `CreateToolRequest.java` 新增 `description` 字段（@Size(max=200), 可选）
- [x] 3.3 `UpdateToolRequest.java` 新增 `description` 字段（@Size(max=200), 可选）
- [x] 3.4 `ToolSummaryDTO.java` 新增 `description` 字段
- [x] 3.5 `ToolDetailDTO.java` 新增 `description` 字段
- [x] 3.6 `ToolService.java` 更新 createTool()：读取并保存 description
- [x] 3.7 `ToolService.java` 更新 updateTool()：支持 description 更新
- [x] 3.8 `ToolService.java` 更新 toSummaryDTO() 和 toDetailDTO()：填充 description
- [ ] 3.9 后端单元测试：验证创建/更新工具的 description 字段，验证摘要 DTO 包含 description，运行测试确认通过

## 4. 工具标签关联（后端）

- [x] 4.1 创建 `ToolTag` 实体：`model/tag/ToolTag.java`，复合主键 (toolId, tagId)
- [x] 4.2 创建 `ToolTagRepository`：`repository/tag/ToolTagRepository.java`，含 findByToolId、deleteByToolId
- [x] 4.3 `ToolService.java` 注入 TagRepository 和 ToolTagRepository
- [x] 4.4 `ToolService.createTool()` 增加标签关联逻辑：遍历 tagIds，创建 ToolTag 记录，调用 TagService.incrementUsage
- [x] 4.5 `ToolService.updateTool()` 增加标签替换逻辑：删除旧关联，创建新关联，更新 usageCount
- [x] 4.6 `CreateToolRequest.java` 和 `UpdateToolRequest.java` 新增 `tagIds` 字段（List<Long>, 可选）
- [x] 4.7 `ToolSummaryDTO.java` 和 `ToolDetailDTO.java` 新增 `tags` 字段（List<TagDTO>）
- [x] 4.8 `ToolService.toSummaryDTO()` 和 `toDetailDTO()` 查询并填充关联标签
- [ ] 4.9 后端单元测试：验证创建带标签的工具、更新工具标签替换、摘要 DTO 返回标签列表，运行测试确认通过

## 5. 微课视频标签关联（后端）

- [x] 5.1 创建 `VideoTag` 实体：`model/tag/VideoTag.java`，复合主键 (videoId, tagId)
- [x] 5.2 创建 `VideoTagRepository`：`repository/tag/VideoTagRepository.java`，含 findByVideoId、deleteByVideoId
- [x] 5.3 `VideoService.java` 注入 TagRepository 和 VideoTagRepository
- [x] 5.4 `VideoController.uploadVideo()` 新增 `tagIds` 参数（@RequestParam, 可选），传递给 VideoService
- [x] 5.5 `VideoService.uploadVideo()` 增加标签关联逻辑
- [x] 5.6 `VideoUpdateRequest.java` 新增 `tagIds` 字段（List<Long>, 可选）
- [x] 5.7 `VideoService.updateVideo()` 增加标签替换逻辑
- [x] 5.8 `VideoResponse.java` 和 `VideoListItem.java` 新增 `tags` 字段（List<TagDTO>）
- [x] 5.9 `VideoService.toVideoResponse()` 和 `toVideoListItem()` 查询并填充关联标签
- [ ] 5.10 后端单元测试：验证上传/更新视频带标签、列表/详情返回标签，运行测试确认通过

## 6. 微课封面上传（后端）

- [x] 6.1 `VideoController.java` 新增端点 `POST /api/v1/videos/{id}/cover`，接收 MultipartFile（JPEG/PNG, ≤5MB）
- [x] 6.2 `VideoService.java` 新增 `uploadCover(videoId, userId, file)` 方法：验证文件类型和大小，保存到 `{uploadBaseDir}/covers/{videoId}.jpg`，更新 Video.coverUrl
- [x] 6.3 配置封面图片的静态资源服务（StaticController 或 WebMvcConfigurer 添加资源映射）
- [x] 6.4 权限校验：仅上传者（isOwner）或管理员可设置封面
- [ ] 6.5 后端单元测试：验证封面上传成功、格式校验（非 JPEG/PNG 拒绝）、大小校验（>5MB 拒绝）、权限校验（非上传者拒绝），运行测试确认通过

## 7. 论坛帖子标签补全（后端）

- [x] 7.1 更新 `ForumPostDTO`（Java record）：新增 `tags`（List<TagDTO>）作为最后一个位置参数
- [x] 7.2 `ForumPostService.toDTO()` 更新：查询 ForumPostTagRepository 获取帖子关联标签，填充 tags 字段
- [x] 7.3 `ForumPostService.updatePost()` 增加标签替换逻辑：接收 tagIds，更新关联关系和 usageCount
- [x] 7.4 `ForumPostController.updatePost()` 传递 `ForumPostUpdateRequest` 中的 tagIds 到 Service
- [x] 7.5 优化 N+1 查询：列表接口批量获取帖子标签（一次查询所有 postId 的标签关联）
- [ ] 7.6 后端单元测试：验证帖子 DTO 返回标签、更新帖子标签、批量查询标签无 N+1，运行测试确认通过

## 8. MCP Handler 适配

- [x] 8.1 `IaihubToolHandler.handleToolCreate()` 适配：构造 CreateToolRequest 时 description 传 null、tagIds 传 null（MCP 不需要这些字段）
- [x] 8.2 `IaihubToolHandler.handleToolModify()` 适配：构造 UpdateToolRequest 时 description 和 tagIds 传 null
- [x] 8.3 编译验证：`cd backend && ./gradlew compileJava` 确认无编译错误

## 9. 修复预存在的测试 Bug

- [ ] 9.1 修复 `ToolServiceTest.java`：更新构造函数参数匹配生产代码的 4 参数签名
- [ ] 9.2 修复 `VideoServiceTest.java`：替换 VideoLikeRepository/VideoFavoriteRepository 为 UnifiedLikeRepository/UnifiedFavoriteRepository
- [ ] 9.3 运行全量测试：`cd backend && ./gradlew test` 确认所有测试通过

## 10. 前端类型与服务更新

- [x] 10.1 `types/tool.ts`（或 `types/index.ts`）：ToolSummary 和 ToolDetail 接口新增 `description?: string`
- [x] 10.2 `types/index.ts`：新增 `Tag` 接口（id, name, tagType, usageCount）
- [x] 10.3 `types/tool.ts`：ToolSummary/ToolDetail 新增 `tags?: Tag[]`，CreateToolRequest/UpdateToolRequest 新增 `tagIds?: number[]`
- [x] 10.4 `types/video.ts`：VideoListItem/VideoDetail 新增 `tags?: Tag[]`，VideoUploadRequest/VideoUpdateRequest 新增 `tagIds?: number[]`
- [x] 10.5 `types/forum.ts`：ForumPost 接口新增 `tags?: Tag[]`
- [x] 10.6 `services/` 新增标签 API 方法：getTags(type?)、getHotTags(type, limit)、createTag(name, type)
- [x] 10.7 `services/video.ts` 新增封面上传方法：uploadCover(videoId, file)

## 11. 前端 TagSelector 组件

- [x] 11.1 创建 `components/TagSelector.vue`：通用标签选择器，props: modelValue (Tag[]), tagType (string)
- [x] 11.2 TagSelector 实现：加载已有标签、展示已选标签（带删除）、搜索过滤、下拉热门/最近使用、输入新标签名创建
- [x] 11.3 TagSelector 样式：遵循 design-system.md 双主题 token 映射（暗色/亮色 normal/hover/focus/loading/empty/error 状态）
- [x] 11.4 TagSelector 可访问性：role="listbox"、role="option"、键盘导航（上下箭头、Enter、Esc）

## 12. 前端 TagBadge 组件

- [x] 12.1 创建 `components/TagBadge.vue`：标签展示徽章，props: tag (Tag), removable (boolean)
- [x] 12.2 TagBadge 样式：遵循 design-system.md（暗色/亮色状态）
- [x] 12.3 TagBadge 可移除模式：显示 X 按钮，emit remove 事件

## 13. 前端 VideoCoverPicker 组件

- [x] 13.1 创建 `components/VideoCoverPicker.vue`：props: videoSrc (string), coverUrl (string | null)
- [x] 13.2 实现视频加载 + Canvas 截帧逻辑：video 元素加载视频源，拖动 slider 选择时间点，canvas.drawImage() 截帧
- [x] 13.3 实现封面预览：截取后展示预览图，提供"重新选择"和"上传图片"按钮
- [x] 13.4 实现上传图片 fallback：用户可选择本地图片文件作为封面
- [x] 13.5 emit 事件：cover-capture（截帧成功，传出 Blob）、cover-upload（上传文件）、cover-remove
- [x] 13.6 VideoCoverPicker 样式：空态虚线边框、有封面时预览+操作按钮、双主题适配
- [x] 13.7 VideoCoverPicker 错误处理：视频无法加载时提示"视频编码不支持预览，请上传图片作为封面"

## 14. 前端工具卡片描述展示

- [x] 14.1 `pages/HomePage.vue`：在工具卡片模板中，名称下方添加描述行（`tool.description`），使用 `--text-secondary` 颜色，单行 ellipsis
- [x] 14.2 描述为空时不渲染描述行（v-if 条件渲染）
- [x] 14.3 工具卡片中展示标签：使用 TagBadge 组件，最多展示 3 个标签，超出显示 "+N"

## 15. 前端工具创建/编辑页面

- [x] 15.1 工具创建页面（UploadPage.vue 或等效）：新增"简短描述"输入框（maxlength=200, placeholder）
- [x] 15.2 工具创建页面：接入 TagSelector 组件（tagType="TOOL"）
- [x] 15.3 提交时将 description 和 tagIds 加入请求体
- [x] 15.4 工具编辑页面（EditToolPage.vue）：同步增加描述和标签编辑功能
- [x] 15.5 编辑页面加载时回填已有 description 和已选标签

## 16. 前端微课上传/编辑页面

- [x] 16.1 `pages/video/VideoUploadPage.vue`：在视频上传表单下方添加 VideoCoverPicker 区域
- [x] 16.2 视频上传成功后获取 videoId，激活 VideoCoverPicker（传入视频流地址）
- [x] 16.3 用户截取/上传封面后，调用 uploadCover(videoId, blob/file) API
- [x] 16.4 接入 TagSelector 组件（tagType="VIDEO"），上传和编辑时传递 tagIds
- [x] 16.5 `pages/video/VideoEditPage.vue`：同步添加封面选择和标签编辑

## 17. 前端论坛帖子编辑器标签集成

- [x] 17.1 `pages/forum/PostEditorPage.vue`：在分类选择器下方接入 TagSelector 组件（tagType="FORUM"）
- [x] 17.2 创建帖子时 publish() 方法增加 tagIds 参数
- [x] 17.3 编辑帖子时加载已有标签并预填充 TagSelector

## 18. 集成验证

- [x] 18.1 启动后端 + 前端，手动验证：创建工具带描述和标签 → 列表卡片显示描述和标签
- [x] 18.2 手动验证：上传微课视频 → 截取封面 → 选择标签 → 列表展示封面和标签
- [x] 18.3 手动验证：创建论坛帖子 → 选择标签 → 帖子列表/详情显示标签
- [x] 18.4 手动验证：编辑工具/微课/帖子 → 修改描述/封面/标签 → 更新生效
- [x] 18.5 运行 `bash scripts/lint-arch.sh` 确认架构层级无违规
- [x] 18.6 运行 `cd backend && ./gradlew compileJava` 确认后端编译通过
- [x] 18.7 运行 `cd frontend && npm run build` 确认前端编译无错误
