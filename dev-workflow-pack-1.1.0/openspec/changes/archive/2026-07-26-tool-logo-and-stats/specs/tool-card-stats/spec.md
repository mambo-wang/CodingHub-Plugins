## ADDED Requirements

### Requirement: 工具卡片统计数据

系统 MUST 在 `ToolSummaryDTO` 中返回工具的浏览量、点赞量、收藏量、下载量四项统计，供前端工具卡片底部统计行渲染。浏览量与点赞量取自 `tool` 现有字段，收藏量从 `unified_favorite` 聚合，下载量从 `tool_file.download_count` 聚合。

#### Scenario: 列表接口返回统计字段
- **WHEN** 客户端调用 `GET /api/v1/tools`
- **THEN** 每条 `ToolSummaryDTO` 包含 `viewCount`、`likeCount`、`favoriteCount`、`downloadCount` 四个非负整数字段

#### Scenario: 收藏量来自统一收藏表
- **WHEN** 某工具在 `unified_favorite` 中有 N 条 `targetType=TOOL` 记录
- **THEN** 该工具 DTO 的 `favoriteCount` 等于 N

#### Scenario: 下载量来自文件下载计数聚合
- **WHEN** 某工具关联的多个 `tool_file` 的 `download_count` 之和为 M
- **THEN** 该工具 DTO 的 `downloadCount` 等于 M

#### Scenario: 无收藏无下载的工具
- **WHEN** 工具在 `unified_favorite` 无记录且关联文件 `download_count` 全为 0
- **THEN** DTO 的 `favoriteCount` 与 `downloadCount` 均为 0（非 null）

### Requirement: 统计计数批量查询

系统 MUST 以当前页 toolId 集合批量查询收藏量与下载量（`IN` 分组聚合），避免逐条 N+1 查询。

#### Scenario: 分页列表批量聚合
- **WHEN** `getTools` 返回一页含 K 个工具
- **THEN** 系统对收藏量与下载量各执行一次按 toolId 分组的批量查询，再映射到各 DTO

### Requirement: 文件下载计数自增

系统 MUST 在 `ToolFileService.downloadFile` 成功定位文件后，对该 `tool_file` 的 `download_count` 执行原子自增（`UPDATE ... SET download_count = download_count + 1`）。

#### Scenario: 下载文件计数加一
- **WHEN** 用户成功下载某工具的某个文件
- **THEN** 该 `tool_file` 记录的 `download_count` 在原有基础上加 1

#### Scenario: 文件不存在不计数
- **WHEN** 下载请求对应的文件不存在
- **THEN** 系统抛出 404，不修改任何 `download_count`

### Requirement: 数字格式化展示

前端 MUST 使用统一的 `formatCount` 函数格式化统计数字：`n >= 10000` 显示为 `(n/10000)` 保留一位小数加「万」，`n >= 1000` 显示为 `(n/1000)` 保留一位小数加「k」，其余原样显示。

#### Scenario: 万级数字格式化
- **WHEN** 统计值为 165000
- **THEN** 前端显示 `16.5万`

#### Scenario: 千级数字格式化
- **WHEN** 统计值为 1200
- **THEN** 前端显示 `1.2k`

#### Scenario: 小数级原样显示
- **WHEN** 统计值为 207
- **THEN** 前端显示 `207`

### Requirement: 统计行图标与可访问性

前端统计行 MUST 为四项统计分别使用 Lucide 图标（浏览量 `Eye`、点赞量 `Heart`、收藏量 `Bookmark`、下载量 `Download`），图标 `aria-hidden="true"`，数字使用等宽字体。

#### Scenario: 统计行渲染四项
- **WHEN** 工具卡片渲染统计行
- **THEN** 依次展示浏览量、点赞量、收藏量、下载量四项，每项含图标与格式化数字，图标为装饰性 `aria-hidden`
