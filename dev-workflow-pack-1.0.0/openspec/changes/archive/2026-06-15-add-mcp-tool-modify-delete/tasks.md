# Tasks

## Implementation Tasks

### 1. IaihubToolHandler - 新增 modify 和 delete 方法
- [x] 注入 `ToolFileService` 依赖到 `IaihubToolHandler` 构造函数 — _依赖: 无_
- [x] 新增 `incrementVersion(String)` 私有方法，实现版本号最后一位 +1 逻辑 — _依赖: 1.1_
- [x] 新增 `handleToolModify(Long toolId, String name, Long categoryId, String content, String version, String username, String password)` 方法 — _依赖: 1.2_
- [x] 新增 `handleToolFileDelete(Long toolId, Long fileId, String username, String password)` 方法 — _依赖: 1.1_

### 2. McpSdkServerConfig - 注册新 MCP 工具
- [x] 注册 `h3_coding_hub_tool_modify` 工具，定义 JSON Schema 和调用处理器 — _依赖: 1.3_
- [x] 注册 `h3_coding_hub_tool_file_delete` 工具，定义 JSON Schema 和调用处理器 — _依赖: 1.4_
- [x] 更新日志计数从 "9 tools" 改为 "11 tools" — _依赖: 2.2_

## Verification
- [x] 编译通过：`cd backend && gradlew compileJava`
- [ ] 启动后端，确认日志显示 "MCP Server initialized with 11 tools"
- [ ] 通过 MCP 客户端测试 `h3_coding_hub_tool_modify`：修改自己的工具、验证版本号自动递增
- [ ] 通过 MCP 客户端测试 `h3_coding_hub_tool_file_delete`：删除自己工具下的文件
- [ ] 验证归属权：尝试修改/删除他人的工具/文件，应返回错误
