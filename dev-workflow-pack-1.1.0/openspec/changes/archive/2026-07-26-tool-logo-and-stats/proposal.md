## 为什么（Why）

工具广场当前所有工具卡片使用统一的占位图标，缺乏视觉辨识度，用户难以快速区分不同工具和分类。同时卡片仅展示名称和描述，缺少点击量、点赞量、收藏量、下载量等热度指标，用户无法直观判断工具的受欢迎程度。参考主流 SkillHub 平台的卡片设计（logo + 统计数据行），需要为工具增加 logo 支持和统计数据展示，提升广场的信息密度和视觉吸引力。

## 变更内容（What Changes）

- **工具 Logo**：Tool 表新增 `logo_url` 字段，支持上传自定义 logo；未上传时回退到所属分类的默认 logo
- **分类默认 Logo**：Category 表新增 `logo_url` 字段，每个分类配置一个默认 logo 图片；管理端可修改
- **Logo 上传接口**：复用现有图片上传机制（`~/.aifiles/images/`），新增工具 logo 上传端点
- **卡片统计行**：工具卡片底部新增统计数据行，展示浏览量、点赞量、收藏量、下载量，配图标和格式化数字（如 1.2k、16.5 万）
- **统计数据来源**：浏览量/点赞量取自 Tool 现有字段；收藏量从 unified_favorite 聚合；下载量从 tool_file 下载记录聚合
- **DTO 扩展**：ToolSummaryDTO 新增 logoUrl、favoriteCount、downloadCount 字段

## 能力清单（Capabilities）

### 新增能力（New Capabilities）
- `tool-logo`: 工具 logo 上传、存储、回退逻辑（自定义 logo → 分类默认 logo → 系统占位图）
- `tool-card-stats`: 工具卡片统计数据展示（浏览量、点赞量、收藏量、下载量的聚合查询与前端渲染）

### 修改能力（Modified Capabilities）
- `category`: Category 实体新增 `logo_url` 字段，分类 CRUD 接口支持 logo 管理

## 影响范围（Impact）

- **数据库**：tool 表加 `logo_url` 列，category 表加 `logo_url` 列（DDL via ddl-auto:update）
- **后端**：Tool/Category 实体、ToolSummaryDTO/CategoryDTO、ToolService（统计聚合）、ToolController（logo 上传端点）、ToolFileService（下载计数）
- **前端**：HomePage.vue 工具卡片（logo 渲染 + 统计行）、ToolDetailPage.vue（logo 展示）、上传/编辑表单（logo 上传组件）、管理端分类管理（默认 logo 设置）
- **API**：GET /api/v1/tools 响应新增字段（向后兼容），新增 POST /api/v1/tools/{id}/logo 上传端点
