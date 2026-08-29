# Category Spec

## Scenarios

### Scenario 1: 查询分类列表

- GIVEN: 数据库中存在分类 Skill、MCP、API、Prompt、其他
- WHEN: 调用 GET /api/categories 获取分类列表
- THEN: 返回的分类列表只包含 Skill、MCP、Prompt、其他，API 类型已被移除

### Scenario 2: 工具列表不包含 API 类型工具

- GIVEN: 数据库中存在多个分类的工具
- WHEN: 调用 GET /api/tools 查询工具列表
- THEN: 返回的工具列表中，所有工具的分类都是 Skill、MCP、Prompt、其他 之一