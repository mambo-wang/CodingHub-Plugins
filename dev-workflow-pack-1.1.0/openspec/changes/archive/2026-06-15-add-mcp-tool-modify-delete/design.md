# Design

## Architecture Overview
两个新 MCP 工具均位于后端 MCP 层，不涉及前端或数据库变更。复用现有的 `ToolService.updateTool()` 和 `ToolFileService.deleteToolFile()` 方法。

```
MCP Client
  │
  ├── h3_coding_hub_tool_modify ──→ IaihubToolHandler.handleToolModify()
  │     ├─ 1. userService.login(username, password) → userId
  │     ├─ 2. searchService.getToolById(toolId) → 验证存在性 + 当前版本
  │     ├─ 3. incrementVersion() 如果 version 参数为空
  │     └─ 4. toolService.updateTool(toolId, request, userId)
  │           └─ 内部验证归属权（uploader.getId().equals(userId)）
  │
  └── h3_coding_hub_tool_file_delete ──→ IaihubToolHandler.handleToolFileDelete()
        ├─ 1. userService.login(username, password) → userId
        └─ 2. toolFileService.deleteToolFile(toolId, fileId, userId)
              └─ 内部验证归属权 + 物理删除 + 数据库删除
```

## Files to Create/Modify

### Modified Files
| 文件路径 | 变更说明 |
|----------|----------|
| `backend/src/main/java/com/iaihub/toolbox/mcp/IaihubToolHandler.java` | 新增 `handleToolModify`、`handleToolFileDelete`、`incrementVersion` 方法；注入 `ToolFileService` |
| `backend/src/main/java/com/iaihub/toolbox/mcp/McpSdkServerConfig.java` | 注册 `h3_coding_hub_tool_modify` 和 `h3_coding_hub_tool_file_delete` 两个新工具，更新日志计数 |

### New Files
无新增文件。

## Data Model
无数据库变更。复用现有 `tool` 和 `tool_file` 表。

## API / Interface

### h3_coding_hub_tool_modify
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| toolId | integer | 是 | 要修改的工具ID |
| name | string | 否 | 新的工具名称 |
| categoryId | integer | 否 | 新的分类ID |
| content | string | 否 | 新的工具描述/文档 |
| version | string | 否 | 版本号，不传则自动递增最后一位 |
| username | string | 是 | 登录账号 |
| password | string | 是 | 登录密码 |

**版本号自动递增策略**：
- 解析版本号 "x.y.z" → 最后一位 +1
- "1.0.0" → "1.0.1"，"1.0.9" → "1.0.10"
- 后缀保留： "1.0.0-beta" → "1.0.1-beta"
- 非数字后缀： "1.0.alpha" → "1.0.alpha.1"
- 空/null： "1.0.1"

**响应**：成功返回 `ToolDetailDTO` JSON，失败返回 error JSON

### h3_coding_hub_tool_file_delete
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| toolId | integer | 是 | 工具ID |
| fileId | integer | 是 | 要删除的文件ID |
| username | string | 是 | 登录账号 |
| password | string | 是 | 登录密码 |

**响应**：成功返回 `{toolId, fileId, deleted: true}`，失败返回 error JSON

## Dependencies
```
McpSdkServerConfig
  └── IaihubToolHandler (新增方法)
        ├── UserService.login()          ← 已有
        ├── McpSearchService.getToolById() ← 已有
        ├── ToolService.updateTool()     ← 已有
        ├── ToolFileService.deleteToolFile() ← 已有
        └── incrementVersion()           ← 新增（私有方法）
```
