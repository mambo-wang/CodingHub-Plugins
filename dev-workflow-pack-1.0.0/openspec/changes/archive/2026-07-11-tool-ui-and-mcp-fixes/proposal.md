## 为什么（Why）

工具广场存在 4 个影响用户体验和功能完整性的问题：管理员无法编辑他人工具（权限检查过严）、首页快捷上传缺失简短描述字段、工具卡片不展示版本号、MCP 创建工具接口缺失描述和标签能力。这些问题影响管理员运维效率和 MCP 生态的自动化管理。

## 变更内容（What Changes）

- **修复** EditToolPage.vue 的权限检查逻辑，管理员（ADMIN/SUPER_ADMIN）可进入任意工具的编辑页面
- **修复** HomePage 快捷上传弹窗，增加「简短描述」输入字段，与独立 UploadPage 保持一致
- **增强** 工具广场卡片，在工具名称后展示版本号标签
- **增强** MCP Server 的 `tool_create` 和 `tool_modify` 工具方法，新增 `description`（简短描述）和 `tags`（标签名列表）参数；后端根据标签名自动匹配已有标签 ID，不存在的标签自动创建

## 能力清单（Capabilities）

### 新增能力（New Capabilities）

- `mcp-tool-tag-auto-resolve`: MCP 工具创建/修改时接受标签名列表，后端自动按名称查找或创建标签并关联到工具

### 修改能力（Modified Capabilities）

- `tool-modify-delete`: 管理员编辑工具的权限检查从仅允许所有者修改为所有者或管理员均可修改
- `tool-plaza-tab-nav`: 工具卡片增加版本号展示

## 影响范围（Impact）

- **前端**: `EditToolPage.vue`（权限检查）、`HomePage.vue`（上传弹窗表单字段 + 工具卡片模板）
- **后端 MCP**: `IaihubToolHandler.java`（handleToolCreate / handleToolModify 参数扩展）、`McpSdkServerConfig.java`（工具 schema 扩展）
- **后端 Service**: `TagService.java`（新增或扩展按名称查找/创建标签的方法）、`ToolService.java`（MCP 路径的标签关联逻辑）
- **DTO**: `CreateToolRequest.java`（可能无需修改，已有 description 和 tagIds 字段）
- **数据库**: 无 schema 变更，tag 表已支持 TOOL 类型标签
