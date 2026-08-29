## 为什么（Why）

工具广场已接入统一标签体系，工具卡片上展示了标签，但用户无法通过标签筛选工具。当工具数量增长后，仅靠分类（粗粒度）和关键词（需精确记忆）难以快速定位目标工具。标签是用户自然的心智模型——点击一个标签即可看到所有相关工具。

## 变更内容（What Changes）

- 后端 `GET /api/v1/tools` 新增可选参数 `tagId`，支持按单个标签筛选工具列表
- 前端工具广场页面（HomePage）在筛选栏增加标签选择器，选中后携带 `tagId` 请求后端
- 工具卡片上已有的 TagBadge 增加点击交互，点击后触发该标签的筛选
- MCP 工具搜索（`h3_coding_hub_tool_search`）新增可选参数 `tag`（标签名称），支持按标签过滤搜索结果
- CodingHub Skill 文档同步更新（SKILL.md、tool-reference.md、chub 脚本增加 `--tag` 选项）

## 能力清单（Capabilities）

### 新增能力（New Capabilities）

- `tool-tag-filter`: 工具广场按标签筛选工具的能力，涵盖后端查询参数扩展、Repository 联表查询、前端标签筛选 UI 及交互

### 修改能力（Modified Capabilities）

（无现有规格级别的需求变更）

## 影响范围（Impact）

- **后端**: `ToolController.getTools()` 新增 `tagId` 参数；`ToolService.getTools()` 增加标签过滤逻辑；`ToolRepository` 或 `ToolTagRepository` 新增按标签查询方法
- **MCP**: `McpSdkServerConfig` 工具 schema 新增 `tag` 参数；`IaihubToolHandler.handleToolSearch()` 透传；`McpSearchService.searchTools()` 增加标签过滤逻辑；`McpResourceHandler` 调用处适配新签名
- **Skill**: `.codebuddy/skills/codinghub/` 下 SKILL.md、references/tool-reference.md 文档更新；`scripts/chub.cjs` 和 `scripts/chub.py` 的 `tool-search` 子命令增加 `--tag` 选项
- **前端**: `HomePage.vue` 筛选栏增加标签选择 UI；`tool.ts` service 请求参数扩展；`TagBadge` 组件增加可选的点击事件
- **API**: `GET /api/v1/tools` 接口向后兼容（新参数可选），无破坏性变更
- **数据库**: 无 schema 变更，复用现有 `tool_tag` 关联表
