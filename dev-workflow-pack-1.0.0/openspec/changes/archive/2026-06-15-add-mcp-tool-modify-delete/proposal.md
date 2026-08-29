# Proposal

## Problem
当前 MCP Server 提供了 9 个工具，覆盖了**创建**工具（`h3_coding_hub_tool_create`）和**查询**工具（搜索、详情、文件列表），但缺少两个核心能力：

1. **暂无修改工具的能力**：用户通过 MCP 创建工具后，如果要更新工具描述、名称、分类或版本号，没有对应的 MCP 工具可用
2. **暂无删除文件的能力**：用户通过 MCP 上传文件后，如果传错了或需要替换，无法通过 MCP 删除文件

这使得 MCP 客户端无法完成工具的完整生命周期管理（创建 → 修改 → 上传文件 → 删除文件）。

## Solution Overview
为 MCP Server 新增两个工具，实现工具的修改和文件删除功能：

1. **`h3_coding_hub_tool_modify`** — 修改已创建的工具，支持修改：
   - 工具描述（content）
   - 工具名称（name）
   - 分类（categoryId）
   - 版本号（version）— 如果客户端不传版本号，则自动在现有版本号基础上最后一位 +1（如 `1.0.0` → `1.0.1`）
   - 需要传入账号密码认证，只能修改自己创建的工具

2. **`h3_coding_hub_tool_file_delete`** — 删除指定工具下的指定文件
   - 需要传入账号密码认证，只能删除自己创建的文件的工具
   - 同时删除物理文件和数据库记录

两个工具都复用现有的后端 Service 层（`ToolService.updateTool`、`ToolFileService.deleteToolFile`），MCP Handler 负责认证封装和版本号自动递增逻辑。

## Scope
- **后端**：
  - `IaihubToolHandler`：新增 `handleToolModify` 和 `handleToolFileDelete` 方法
  - `McpSdkServerConfig`：注册两个新 MCP 工具
- **前端**：无变更
- **数据库**：无变更

## Acceptance Criteria
- [ ] 通过 `h3_coding_hub_tool_modify` 可修改自己创建的工具的描述、名称、分类
- [ ] 修改工具时若不传 version，版本号最后一位自动 +1
- [ ] 修改工具时若传了 version，使用指定的版本号
- [ ] 修改他人创建的工具时返回错误（归属权校验）
- [ ] 通过 `h3_coding_hub_tool_file_delete` 可删除自己工具下的指定文件
- [ ] 删除文件时同时移除物理文件和数据库记录
- [ ] 删除他人工具下的文件时返回错误
- [ ] 两个新工具均在 MCP 工具列表中可见
