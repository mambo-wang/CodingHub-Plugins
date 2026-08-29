## ADDED Requirements

### Requirement: 工具自定义 Logo

系统 MUST 支持为每个工具上传并保存自定义 logo，logo 文件复用通用图片上传端点（`POST /api/v1/uploads/images`），`tool.logo_url` 仅保存返回的相对 URL。

#### Scenario: 上传者设置工具 logo
- **WHEN** 工具所有者先调用 `POST /api/v1/uploads/images` 上传图片得到 url，再调用 `POST /api/v1/tools/{id}/logo`，body 为 `{"logoUrl": url}`
- **THEN** 系统将 `tool.logo_url` 更新为该 url，返回成功

#### Scenario: 管理员设置工具 logo
- **WHEN** ADMIN 或 SUPER_ADMIN 对任意工具调用 `POST /api/v1/tools/{id}/logo`
- **THEN** 系统允许操作并更新 `tool.logo_url`

#### Scenario: 非所有者非管理员设置 logo 被拒绝
- **WHEN** 既非工具所有者也非管理员的用户调用 `POST /api/v1/tools/{id}/logo`
- **THEN** 系统返回 403 错误

#### Scenario: 对不存在的工具设置 logo
- **WHEN** 用户对不存在或已删除的 toolId 调用 `POST /api/v1/tools/{id}/logo`
- **THEN** 系统返回 404 错误

### Requirement: Logo 三级回退

系统 MUST 在组装 `ToolSummaryDTO` / `ToolDetailDTO` 时按「工具自定义 logo → 分类默认 logo → null」顺序解析 `logoUrl` 字段，由前端在 null 时渲染系统占位图。

#### Scenario: 工具有自定义 logo
- **WHEN** 工具的 `logo_url` 非空
- **THEN** DTO 的 `logoUrl` 等于工具自身的 `logo_url`

#### Scenario: 工具无自定义 logo 但分类有默认 logo
- **WHEN** 工具的 `logo_url` 为空且其分类的 `logo_url` 非空
- **THEN** DTO 的 `logoUrl` 等于分类的 `logo_url`

#### Scenario: 工具与分类均无 logo
- **WHEN** 工具的 `logo_url` 为空且分类的 `logo_url` 也为空
- **THEN** DTO 的 `logoUrl` 为 null，前端渲染系统占位图

### Requirement: Logo 裂图前端兜底

前端工具卡片与详情页的 logo `img` MUST 在加载失败（`@error`）时回退到系统占位图，避免显示破损图标。

#### Scenario: logo URL 失效
- **WHEN** DTO 返回的 `logoUrl` 对应文件不存在或网络加载失败
- **THEN** 前端 `img` 触发 error 后切换为系统占位图标渲染
