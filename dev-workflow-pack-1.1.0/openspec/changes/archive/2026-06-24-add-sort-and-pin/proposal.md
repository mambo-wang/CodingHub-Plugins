## 为什么（Why）

当前三个内容模块（工具、论坛、微课）的列表页仅支持按创建时间排序，用户无法发现高质量内容；同时缺少管理员置顶机制，重要内容无法获得优先展示。这导致社区活跃度受限，优质工具/帖子/微课容易被淹没。

## 变更内容（What Changes）

- **新增热度排序**：三个模块的列表接口新增 `sortBy=hot|latest` 参数，默认按热度（score）降序排列，可切换为最新排序
- **新增置顶功能**：三张内容表新增 `pinned` 字段，管理员/超级管理员可在列表页卡片上操作置顶/取消置顶
- **新增热度 Top5 接口**：每个模块提供轻量 `/hot-top5` 端点，返回全局热度前5的 ID 列表
- **前端排序切换 UI**："热度 | 最新" Tab 样式切换
- **前端标识图标**：置顶项显示向上箭头图标，全局热度前5显示火苗图标
- **Video 实体补全 score 字段**：微课实体目前没有 score 字段和计算公式，需与 Tool/ForumPost 对齐

## 能力清单（Capabilities）

### 新增能力（New Capabilities）

- `content-sorting`: 三模块统一的内容排序能力——热度排序（pinned 优先 + score DESC）与最新排序（createdAt DESC），包含后端接口参数和前端切换 UI
- `content-pinning`: 三模块统一的内容置顶能力——管理员置顶/取消置顶操作、pinned 字段管理、置顶图标展示
- `hot-ranking`: 热度前5排名能力——全局 Top5 ID 接口、火苗图标展示、Video score 公式补全

### 修改能力（Modified Capabilities）

（无现有规格需要修改）

## 影响范围（Impact）

- **数据库**：tool、forum_post、video 三张表新增字段和索引，需编写 V3 迁移脚本
- **后端**：3 个 Entity、3 个 Repository（新增查询方法）、3 个 Service（新增 pin/unpin + 排序逻辑）、3 个 Controller（新增 sortBy 参数 + pin 端点 + top5 端点）、相关 DTO 扩展字段
- **前端**：3 个列表页组件（排序 Tab）、3 个卡片组件（置顶/火苗图标 + 管理员操作按钮）、3 个 Service 文件（新接口调用）、相关 Type 定义更新
- **安全**：pin/unpin 端点需要 ADMIN 或 SUPER_ADMIN 权限，复用现有 JWT + SecurityConfig 机制
