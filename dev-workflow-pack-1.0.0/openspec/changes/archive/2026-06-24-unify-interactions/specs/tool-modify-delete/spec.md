## MODIFIED Requirements

### Requirement: MCP 工具修改（h3_coding_hub_tool_modify）

系统 SHALL 通过 MCP 工具 `h3_coding_hub_tool_modify` 提供工具元数据的修改能力，调用方需传入 username/password 进行认证。

> **变更说明**：MCP 工具端点本身不变，但底层 ToolService 的 like/comment 方法已迁移到 UnifiedInteractionService。MCP 层不调用统一交互 API，仍通过各模块 Service 访问数据。

#### Scenario: 修改自己创建的工具的描述
- GIVEN: 用户已通过 `h3_coding_hub_tool_create` 创建了一个工具（toolId=42，version="1.0.0"）
- WHEN: 用户调用 `h3_coding_hub_tool_modify`，传入 toolId=42, content="新的描述", username和password正确，不传 version
- THEN: 工具描述更新为"新的描述"，版本号自动递增为 "1.0.1"，返回更新后的工具详情

### Requirement: MCP 工具认证

MCP 工具 SHALL 在每次调用时验证调用方传入的 username/password，拒绝未通过认证的请求。

> **变更说明**：无变化。MCP 认证机制独立于统一交互层。
