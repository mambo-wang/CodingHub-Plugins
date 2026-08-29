# Impact Analysis

> 基于 `design.md` 中的文件/类/测试清单执行 codegraph 扫描，确认技术设计的实际影响范围。
>
> **位置**：在 `design` 之后、`tasks` 之前生成。
>
> **触发条件**：仅当 `design.md` 涉及**修改现有代码**时必选；纯新增模块/页面时跳过此 artifact。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | 12 | `model/tag/Tag.java`, `model/tag/ToolTag.java`, `model/tag/VideoTag.java`, `repository/tag/TagRepository.java`, `repository/tag/ToolTagRepository.java`, `repository/tag/VideoTagRepository.java`, `service/tag/TagService.java`, `controller/tag/TagController.java`, `dto/tag/TagDTO.java`, `components/TagSelector.vue`, `components/TagBadge.vue`, `components/VideoCoverPicker.vue` |
| 修改 | 23 | 见下方详细清单 |
| 删除 | 0 | — |

### 修改文件清单

**后端 (16 files)：**
- `model/Tool.java` — 新增 `description` 字段
- `dto/CreateToolRequest.java` — 新增 `description`, `tagIds`
- `dto/UpdateToolRequest.java` — 新增 `description`, `tagIds`
- `dto/ToolSummaryDTO.java` — 新增 `description`, `tags`
- `dto/ToolDetailDTO.java` — 新增 `description`, `tags`
- `service/ToolService.java` — 处理 description + 标签关联
- `controller/ToolController.java` — 适配新字段
- `controller/video/VideoController.java` — 新增封面上传端点
- `service/video/VideoService.java` — 处理封面上传 + 标签关联
- `dto/video/VideoUploadRequest.java` — 新增 `tagIds`
- `dto/video/VideoUpdateRequest.java` — 新增 `tagIds`
- `dto/video/VideoResponse.java` — 新增 `tags`
- `dto/video/VideoListItem.java` — 新增 `tags`
- `dto/forum/ForumPostDTO.java` — 新增 `tags`（Java record，需更新位置参数）
- `service/forum/ForumPostService.java` — 在 toDTO() 中查询并填充标签
- `controller/forum/ForumPostController.java` — 传递 tagIds 到 updatePost
- `mcp/IaihubToolHandler.java` — handleToolCreate/Modify 需适配新 DTO 字段

**前端 (7 files)：**
- `pages/HomePage.vue` — 工具卡片增加描述展示（注：ToolCard 是内联渲染，非独立组件）
- `pages/forum/PostEditorPage.vue` — 接入标签选择器
- `types/index.ts` — 新增描述字段、标签类型
- `types/tool.ts` — 新增描述字段
- `types/video.ts` — 新增标签类型
- `types/forum.ts` — ForumPost 接口新增 tags
- `services/video.ts` — 新增封面上传 API 方法
- `services/forum.ts` — 适配标签查询 API

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `ToolService.createTool()` | `service/ToolService.java` | L2 |
| `ToolService.updateTool()` | `service/ToolService.java` | L2 |
| `ToolService.toSummaryDTO()` | `service/ToolService.java` | L1 |
| `ToolService.toDetailDTO()` | `service/ToolService.java` | L1 |
| `VideoService.toVideoResponse()` | `service/video/VideoService.java` | L1 |
| `VideoService.toVideoListItem()` | `service/video/VideoService.java` | L1 |
| `ForumPostService.toDTO()` | `service/forum/ForumPostService.java` | L2 |
| `IaihubToolHandler.handleToolCreate()` | `mcp/IaihubToolHandler.java:221` | L1 |
| `IaihubToolHandler.handleToolModify()` | `mcp/IaihubToolHandler.java:323` | L1 |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

- `McpSdkServerConfig` 通过 `IaihubToolHandler` 调用 `ToolService`/`ForumPostService`
- `McpResourceHandler` 通过 `McpSdkServerConfig` 调用 `IaihubToolHandler`
- `VideoInteractionService` (@Deprecated) 通过 `VideoService` 获取 `VideoListItem`
- `UserController` 通过 `ToolService` 获取用户工具列表（含 `ToolSummaryDTO`）
- `UnifiedFavoriteService` 通过 `ToolService` 获取收藏的工具摘要

### 2.3 反向调用图（被谁调用）

```
ToolService
  ├── ToolController (HTTP)
  ├── UserController (HTTP, 用户工具列表)
  ├── IaihubToolHandler (MCP)
  │     ├── McpSdkServerConfig
  │     └── McpResourceHandler
  └── UnifiedFavoriteService (收藏关联)

VideoService
  ├── VideoController (HTTP)
  └── VideoInteractionService (@Deprecated)
        └── VideoInteractionController (@Deprecated)

ForumPostService
  ├── ForumPostController (HTTP)
  └── IaihubToolHandler (MCP)
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `ToolRepository` | 数据访问层 | L0（不改） |
| `CategoryRepository` | 数据访问层 | L0 |
| `UserRepository` | 数据访问层 | L0 |
| `ForumPostTagRepository` | 数据访问层 | L0（已有，复用） |
| `UploadConfig` | 配置 | L0 |
| `VideoStorageConfig` | 配置 | L0 |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| `GET /api/v1/tools` | 响应 JSON 新增 description、tags 字段（additive） |
| `POST /api/v1/tools` | 请求体新增 description、tagIds（optional，向后兼容） |
| `GET /api/v1/videos` | 响应 JSON 新增 tags 字段 |
| `POST /api/v1/videos/{id}/cover` | 新增端点 |
| `GET /api/forum/posts` | 响应 JSON 新增 tags 字段 |
| 前端 HomePage.vue | 工具卡片 UI 变化 |
| 前端 PostEditorPage.vue | 新增标签选择器 UI |
| 前端 VideoUploadPage.vue | 新增封面选择器 UI |
| MCP IaihubToolHandler | DTO 构造需适配新字段 |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| `ToolServiceTest.java` | 单元 | **BROKEN（预存在）** — 构造函数 6 参数 vs 生产代码 4 参数 | 必须先修复，再适配新逻辑 |
| `VideoServiceTest.java` | 单元 | **BROKEN（预存在）** — 使用 VideoLikeRepository/VideoFavoriteRepository vs 生产代码 UnifiedLikeRepository/UnifiedFavoriteRepository | 必须先修复 |
| `VideoStreamTest.java` | 集成 | 未知 | 需验证 |
| `ForumPostServiceTest.java` | 单元 | 正常 | 适配 ForumPostDTO record 新增 tags 参数 |
| 前端无测试文件 | — | — | — |

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L0** | 纯新增（Tag 相关新文件） | 无 |
| **L1** | 修改 DTO 字段（additive） | 向后兼容，JSON 消费方无需改动 |
| **L2** | 修改 DB schema + ForumPostDTO record 结构 | 完整回归 + 修复预存在测试 bug |

**本次改动综合风险等级**: **L2**（数据库 schema 变更 + ForumPostDTO record 位置参数变化）

---

## 6. 层级依赖校验 (Layer Dependency Check)

```bash
bash scripts/lint-arch.sh
```

**结果**: **PASS** — 架构层级检查通过，无违规依赖。

---

## 7. 设计修正建议 (Design Corrections)

| # | 问题 | 建议 |
|---|------|------|
| 1 | `ToolCard.vue` 不存在 | 将前端改动目标改为 `HomePage.vue`（内联工具卡片模板，约 420-446 行） |
| 2 | `IaihubToolHandler` 未列入修改清单 | 必须更新 `handleToolCreate()` 和 `handleToolModify()` 中对 DTO 新字段的处理（传 null 即可，MCP 不需要描述和标签） |
| 3 | `ForumPostDTO` 是 Java record | 新增 `tags` 参数意味着所有构造调用必须更新（`ForumPostService.toDTO()` 15 参数 → 16 参数） |
| 4 | 两个测试文件预存在 bug | 建议在实现前修复 `ToolServiceTest.java` 和 `VideoServiceTest.java` 的构造函数不匹配问题 |
| 5 | `VideoUploadRequest` 未被 Controller 使用 | Controller 当前用 `@RequestParam`，新增 `tagIds` 也应作为 `@RequestParam` 而非 DTO body |
| 6 | N+1 查询风险 | `ForumPostService` 列表查询时批量获取标签（batch fetch 或 JOIN），避免 N+1 |

---

## 8. 回归测试建议 (Regression Suggestions)

- [ ] `testCreateToolWithDescription` — 覆盖创建工具时传入 description，位于 `ToolServiceTest.java`
- [ ] `testUpdateToolWithTags` — 覆盖更新工具时传入 tagIds，位于 `ToolServiceTest.java`
- [ ] `testUploadCoverImage` — 覆盖封面图片上传成功和格式校验，位于 `VideoServiceTest.java`
- [ ] `testForumPostDTOWithTags` — 覆盖帖子 DTO 包含标签列表，位于 `ForumPostServiceTest.java`
- [ ] `testTagCRUD` — 覆盖标签的创建、查询、删除，位于 `TagServiceTest.java`（新增）
- [ ] `testToolSummaryIncludesDescription` — 覆盖工具摘要 DTO 包含 description，位于 `ToolServiceTest.java`

---

## 9. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方
- [x] 已列出上游/下游依赖
- [x] 已评估风险等级
- [x] `scripts/lint-arch.sh` 校验通过
- [x] 已列出回归测试清单
- [x] 已识别设计修正点（ToolCard.vue → HomePage.vue、IaihubToolHandler 等）
- [ ] （L2 风险）已通知相关模块负责人

---

**生成时间**: 2026-06-25
**基础**: openspec/changes/cover-description-tags/proposal.md + design.md
