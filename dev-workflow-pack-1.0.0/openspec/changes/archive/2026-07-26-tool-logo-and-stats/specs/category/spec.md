## ADDED Requirements

### Requirement: 分类默认 Logo

系统 MUST 支持为每个分类配置一个默认 logo 图片地址，保存于 `category.logo_url` 字段，并在 `CategoryDTO` 中返回。该默认 logo 作为工具未设置自定义 logo 时的回退来源。

#### Scenario: 分类列表返回 logoUrl
- **WHEN** 客户端调用 `GET /api/v1/categories`
- **THEN** 每个 `CategoryDTO` 包含 `logoUrl` 字段（无默认 logo 时为 null）

#### Scenario: 管理员设置分类默认 logo
- **WHEN** 管理员先通过 `POST /api/v1/uploads/images` 上传图片得到 url，再调用分类更新接口携带 `logoUrl`
- **THEN** 系统将 `category.logo_url` 更新为该 url

#### Scenario: 分类无默认 logo
- **WHEN** 分类未配置 `logo_url`
- **THEN** `category.logo_url` 为 null，工具回退链继续降级到前端系统占位图
