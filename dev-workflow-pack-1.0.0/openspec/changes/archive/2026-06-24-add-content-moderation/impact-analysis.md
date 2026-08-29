# Impact Analysis

> 基于 `design.md` 中的文件/类/测试清单执行 codegraph 扫描，确认技术设计的实际影响范围。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | 3 | `frontend/src/composables/useContentPermissions.ts`、`frontend/src/pages/video/VideoEditPage.vue`、`frontend/src/pages/forum/PostEditorPage.vue`（编辑模式补齐，视为新增逻辑） |
| 修改 | 12 | 后端：`ToolService.java`、`ForumPostService.java`、`VideoService.java`、`ToolController.java`、`ForumPostController.java`、`VideoController.java`、`IaihubToolHandler.java`（MCP 调用方）；前端：`PostCard.vue`、`VideoCard.vue`、`HomePage.vue`、`DetailPage.vue`、`PostDetailPage.vue`、`VideoDetailPage.vue`、`PostEditorPage.vue`、`router/index.ts` |
| 删除 | 0 | — |

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `ToolController.deleteTool` | `ToolController.java:65` | L1 |
| `ToolController.updateTool` | `ToolController.java:56` | L1 |
| `IaihubToolHandler.handleToolModify` | `mcp/IaihubToolHandler.java:323` | L1 |
| `ForumPostController.deletePost` | `forum/ForumPostController.java:92` | L1 |
| `ForumPostController.updatePost` | `forum/ForumPostController.java:81` | L1 |
| `VideoController.deleteVideo` | `video/VideoController.java:112` | L1 |
| `VideoController.updateVideo` | `video/VideoController.java:100` | L1 |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

- MCP 客户端通过 `IaihubToolHandler.handleToolModify` → `ToolService.updateTool` 调用工具修改。签名变更需同步适配 MCP Handler，但 MCP Handler 内部已通过用户名密码登录获取 User 对象，可直接传递。

### 2.3 反向调用图（被谁调用）

```
ToolService.updateTool
  ├── ToolController.updateTool (ToolController.java:56)
  │     └── REST API PUT /api/v1/tools/{id}
  └── IaihubToolHandler.handleToolModify (IaihubToolHandler.java:323)
        └── MCP 工具 h3_coding_hub_tool_modify

ToolService.deleteTool
  └── ToolController.deleteTool (ToolController.java:65)
        └── REST API DELETE /api/v1/tools/{id}

ForumPostService.deletePost
  └── ForumPostController.deletePost (ForumPostController.java:92)
        └── REST API DELETE /api/forum/posts/{id}

ForumPostService.updatePost
  └── ForumPostController.updatePost (ForumPostController.java:81)
        └── REST API PUT /api/forum/posts/{id}

VideoService.deleteVideo
  └── VideoController.deleteVideo (VideoController.java:112)
        └── REST API DELETE /api/v1/videos/{id}

VideoService.updateVideo
  └── VideoController.updateVideo (VideoController.java:100)
        └── REST API PUT /api/v1/videos/{id}
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `toolRepository` | 数据访问层 | L0（无变更） |
| `postRepository` | 数据访问层 | L0（无变更） |
| `videoRepository` | 数据访问层 | L0（无变更） |
| `toolFileService` | 工具文件服务 | L0（无变更） |
| `User.getRole()` | 模型层 | L0（字段已存在，仅新增读取） |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| `ToolController` / `ForumPostController` / `VideoController` | 传参从 `currentUser.getId()` 改为 `currentUser` |
| `IaihubToolHandler` | `updateTool` 调用需适配新签名（传 User 而非 userId） |
| 前端 6 个页面/组件 | 新增操作按钮，依赖 `useContentPermissions` composable |
| 前端路由 | 新增 `/forum/posts/:id/edit` 和 `/videos/:id/edit` |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| `backend/src/test/java/com/iaihub/toolbox/service/ToolServiceTest.java` | 单元 | 需更新 | 修改 `updateTool`/`deleteTool` 测试的方法签名 mock（传 User 而非 Long），新增管理员权限测试用例 |
| ForumPostService 测试 | 单元 | 不存在 | **新增** `ForumPostServiceTest.java`，覆盖创建者/管理员/无权限场景 |
| VideoService 测试 | 单元 | 不存在 | **新增** `VideoServiceTest.java`，覆盖创建者/管理员/无权限场景 |
| 前端组件测试 | 组件 | 不存在 | 可选：为 `useContentPermissions` composable 新增单元测试 |

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L0** | 纯新增，不影响现有代码 | 无 |
| **L1** | 修改函数签名/公共 API | 全量回归 + 通知调用方 |
| **L2** | 修改数据库 schema / 业务规则 / 跨模块契约 | 完整测试套件 + 灰度发布 |

**本次改动风险等级**: L1

理由：修改了 6 个 Service 方法的签名（`Long userId` → `User user`），影响 7 个直接调用方（含 1 个 MCP Handler）。不涉及数据库 schema 变更，不修改跨模块契约（REST API 路径和请求/响应体不变），权限规则扩展是向后兼容的（原创建者权限保留，新增管理员权限）。

---

## 6. 层级依赖校验 (Layer Dependency Check)

```bash
bash scripts/lint-arch.sh
```

**结果**: PASS

> 注：脚本输出中 `PostFavoriteController` 和 `AvatarStaticController` 的违规为既有问题，与本次变更无关。本次变更不引入新的层级违规：Controller 仍依赖 Service，Service 仍依赖 Repository/Model。

---

## 7. 回归测试建议 (Regression Suggestions)

- [ ] `ToolServiceTest` —— 更新 `updateTool_shouldThrowForbiddenWhenNotOwner` 为 `updateTool_shouldThrowForbiddenWhenNotOwnerAndNotAdmin`，新增 `updateTool_shouldAllowAdminToUpdateOthersTool`、`deleteTool_shouldAllowAdminToDeleteOthersTool`
- [ ] `ForumPostServiceTest`（新增）—— 覆盖创建者删除/更新、管理员删除/更新、无权限删除/更新、不存在帖子
- [ ] `VideoServiceTest`（新增）—— 覆盖创建者删除/更新、管理员删除/更新、无权限删除/更新、不存在视频
- [ ] `IaihubToolHandler` 相关测试 —— 验证 MCP 工具修改接口适配新签名后仍正常工作
- [ ] 前端手动验证 —— 三类内容列表页 hover 按钮显示、详情页按钮显示、编辑页跳转、删除确认流程

---

## 8. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方（含 MCP Handler）
- [x] 已列出上游/下游依赖
- [x] 已评估风险等级（L1）
- [x] `scripts/lint-arch.sh` 校验通过
- [x] 已列出回归测试清单
- [x] （L1 风险）已识别所有需同步修改的调用方

---

## 9. 设计修正建议

1. **`IaihubToolHandler` 需纳入改动范围**：`design.md` 未显式提及 MCP Handler 的适配。`ToolService.updateTool` 签名变更后，`IaihubToolHandler.handleToolModify`（`IaihubToolHandler.java:323`）需同步修改传参。MCP Handler 内部已通过用户名密码登录获取 User 对象，可直接传递，无需额外查询。**建议在 tasks.md 中增加 MCP Handler 适配任务。**

2. **`ForumPostService` 和 `VideoService` 缺少测试**：本次权限变更涉及这两个 Service，但它们目前无测试文件。建议在实现时同步新增单元测试，避免权限逻辑无回归保障。

---

**生成工具**: Task(code-explorer) 子代理 + scripts/lint-arch.sh 静态分析
**生成时间**: 2026-06-20 08:11
**基础**: openspec/changes/add-content-moderation/proposal.md
