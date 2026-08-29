## 1. 后端：Repository 层扩展

- [x] 1.1 在 `ToolTagRepository` 新增 `findToolIdsByTagId(Long tagId)` 方法，返回 `List<Long>` toolIds
- [x] 1.2 在 `ToolRepository` 新增带 tagId 条件的查询方法（`findByFiltersWithTag`、`findByFiltersWithTagOrderByName`、`findByFiltersWithTagOrderByHot`），使用 EXISTS 子查询关联 tool_tag 表
- [x] 1.3 为 ToolTagRepository 和 ToolRepository 新方法编写单元测试并确认通过

## 2. 后端：Service 层适配

- [x] 2.1 修改 `ToolService.getTools()` 方法签名，新增 `Long tagId` 参数；当 tagId 非空时调用带标签条件的 Repository 方法
- [x] 2.2 为 ToolService.getTools 编写单元测试：覆盖 tagId 为空（向后兼容）、tagId 有值、tagId+categoryId+keyword 叠加、tagId 无关联工具返回空列表四个场景，确认通过

## 3. 后端：Controller 层适配

- [x] 3.1 修改 `ToolController.getTools()` 新增 `@RequestParam(required = false) Long tagId` 参数，透传给 Service
- [x] 3.2 为 ToolController 编写集成测试（MockMvc）：验证 GET /api/v1/tools?tagId=3 返回正确结果、不带 tagId 行为不变，确认通过

## 4. 前端：API 层与数据流

- [x] 4.1 修改 `frontend/src/services/tool.ts`（或对应 service），`getTools` 请求参数增加可选 `tagId`
- [x] 4.2 修改 `frontend/src/types/index.ts`（如需要），确保请求参数类型包含 `tagId?: number`

## 5. 前端：HomePage 标签筛选 UI

- [x] 5.1 在 `HomePage.vue` 中新增 `selectedTagId` 状态和标签列表数据（onMounted 时调用 `GET /api/v1/tags?type=TOOL` 获取）
- [x] 5.2 在搜索栏右侧新增标签下拉选择框，样式遵循 design-system.md（收起显示"标签: 全部标签"/"标签: {标签名}"，展开为 radio 单选列表，点击外部关闭）
- [x] 5.3 下拉选择逻辑：选择标签时设置 selectedTagId 并重新请求工具列表；选择"全部标签"取消筛选
- [x] 5.4 确保 tagId 与 categoryId、keyword 叠加传递给后端

## 6. 前端：TagBadge 可点击交互

- [x] 6.1 修改 `TagBadge.vue` 新增 `clickable` prop（默认 false），为 true 时添加 cursor:pointer、hover 样式、click emit
- [x] 6.2 在 `HomePage.vue` 的工具卡片中，将 TagBadge 设为 clickable，点击时设置 selectedTagId 触发筛选

## 7. MCP：工具搜索支持标签过滤

- [x] 7.1 修改 `McpSearchService.searchTools()` 签名新增 `String tag` 参数；当 tag 非空时，在已有 `resolveTagsForTools` 结果上按标签名称忽略大小写过滤（tag 存在时先按较大候选集查询再过滤，保证结果数量）
- [x] 7.2 修改 `IaihubToolHandler.handleToolSearch()` 签名新增 `String tag` 参数，透传给 McpSearchService
- [x] 7.3 修改 `McpSdkServerConfig` 中 `h3_coding_hub_tool_search` 的 input schema 新增 `"tag":{"type":"string","description":"标签名称（忽略大小写）"}`，参数提取处读取 tag 并传给 handler
- [x] 7.4 修改 `McpResourceHandler` 中 `searchTools(null, null, N)` 调用处适配新签名（tag 传 null）
- [x] 7.5 为 McpSearchService.searchTools 编写单元测试：覆盖 tag 为空（向后兼容）、tag 有值过滤、tag+query 叠加、大小写不敏感、tag 无匹配返回空列表五个场景，确认通过

## 8. Skill：文档与脚本同步更新

- [x] 8.1 更新 `.codebuddy/skills/codinghub/references/tool-reference.md`：`h3_coding_hub_tool_search` 行增加 `tag?` 参数说明
- [x] 8.2 更新 `.codebuddy/skills/codinghub/SKILL.md`：`tool-search` 子命令典型参数增加 `[--tag <标签名>]`，搜索工作流说明补充按标签搜索用法
- [x] 8.3 修改 `scripts/chub.cjs` 的 `tool-search` 子命令：增加 `--tag` flag，HTTP 通道先调 `GET /api/v1/tags?type=TOOL` 解析标签名→tagId，再传 tagId 给 `GET /api/v1/tools`
- [x] 8.4 修改 `scripts/chub.py` 同步增加 `--tag` 支持（与 chub.cjs 行为一致）

## 9. 受影响模块回归测试（基于 impact-analysis.md）

- [x] 9.1 验证不带 tagId 的 `GET /api/v1/tools` 行为不变（L1 风险 — ToolService.getTools 签名变更）
- [x] 9.2 验证 MCP 搜索不带 tag 参数时行为不变（L1 风险 — McpSearchService.searchTools 签名变更，McpResourceHandler 调用处已适配）
- [x] 9.3 前端验证：分类 Pills 和标签下拉框交互不冲突，详情页 TagBadge 仍为纯展示
- [x] 9.4 运行 `cd backend && ./gradlew test` 确认全部测试通过（9 个既有失败在 ToolFile/KB 测试中，与标签筛选无关）
