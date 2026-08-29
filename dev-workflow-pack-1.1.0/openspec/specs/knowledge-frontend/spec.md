## ADDED Requirements（新增需求）

### Requirement: 知识库列表页面

系统 SHALL 提供 KnowledgeListPage（`/knowledge` 路径），展示所有知识库的卡片列表。页面 SHALL 包含 GeneralizedSidebar 侧栏导航、SortTab 排序切换、知识库卡片网格和分页加载。

#### Scenario: 未登录用户访问知识库列表
- **WHEN** 未登录用户导航到 `/knowledge`
- **THEN** 页面正常显示知识库列表，侧栏中"我的知识库"项隐藏，"创建知识库"按钮隐藏

#### Scenario: 已登录用户访问知识库列表
- **WHEN** 已登录用户导航到 `/knowledge`
- **THEN** 页面显示知识库列表，侧栏中显示"我的知识库"项，顶部显示"创建知识库"按钮

#### Scenario: 知识库列表为空
- **WHEN** 数据库中没有任何知识库
- **THEN** 页面显示空状态：Database 图标 + "暂无知识库" + 创建按钮（仅登录可见）

### Requirement: 知识库详情页

系统 SHALL 提供 KnowledgeDetailPage（`/knowledge/:id` 路径），展示知识库详情、语义搜索、文档列表和配置管理。页面 SHALL 包含返回按钮、知识库信息卡片、搜索区域、文档列表和配置面板（Tab 切换）。

#### Scenario: 未登录用户访问知识库详情
- **WHEN** 未登录用户导航到 `/knowledge/42`
- **THEN** 页面显示知识库信息和搜索功能，"管理文档"和"配置"Tab 隐藏，删除/编辑按钮隐藏

#### Scenario: 所有者访问知识库详情
- **WHEN** 知识库所有者导航到 `/knowledge/42`
- **THEN** 页面显示完整功能：搜索、文档管理（含上传/删除）、配置修改、编辑/删除知识库按钮

#### Scenario: 搜索知识库内容
- **WHEN** 用户在搜索框输入查询并回车或点击搜索按钮
- **THEN** 页面调用搜索 API，显示搜索结果卡片列表（来源文档名 + 文本片段 + 相关度指示）

#### Scenario: 搜索结果为空
- **WHEN** 搜索返回空结果
- **THEN** 页面显示 Search 图标 + "未找到相关内容"

### Requirement: 知识库创建/编辑页面

系统 SHALL 提供 KnowledgeEditorPage（`/knowledge/create` 和 `/knowledge/:id/edit` 路径），包含知识库名称、描述输入和可折叠的高级配置区域。此页面 SHALL 需要登录才能访问。

#### Scenario: 创建知识库表单
- **WHEN** 已登录用户导航到 `/knowledge/create`
- **THEN** 页面显示名称（必填）、描述输入框，高级配置默认折叠，底部"取消"和"创建"按钮

#### Scenario: 展开高级配置
- **WHEN** 用户点击"高级配置"折叠区域
- **THEN** 展开显示 chunkMode 下拉选择、chunkSize/chunkOverlap 数字输入、rerank 开关，默认值为 structural/800/50/true

#### Scenario: 提交创建表单
- **WHEN** 用户填写名称后点击"创建"
- **THEN** 页面调用创建 API，成功后跳转到新知识库详情页

#### Scenario: 创建名称冲突
- **WHEN** 用户填写的名称与已有知识库重复
- **THEN** 页面显示错误提示"知识库名称已存在"，表单保留用户输入

#### Scenario: 编辑已有知识库
- **WHEN** 所有者导航到 `/knowledge/:id/edit`
- **THEN** 页面回填知识库的 name 和 description，提交后更新并跳转回详情页

### Requirement: 知识库卡片组件

系统 SHALL 提供 KnowledgeCard 组件，展示知识库摘要信息，点击可跳转到详情页。

#### Scenario: 知识库卡片展示
- **WHEN** 知识库列表页渲染 KnowledgeCard
- **THEN** 卡片显示知识库名称、描述（截断）、作者昵称、文档数量、创建时间，使用 glass-card 样式

#### Scenario: 点击知识库卡片
- **WHEN** 用户点击 KnowledgeCard
- **THEN** 导航到 `/knowledge/:id` 详情页

## MODIFIED Requirements（修改需求）

### Requirement: 知识库设置页增加分片配置区
知识库设置页（KnowledgeBaseDetailPage）MUST 在现有配置表单中新增以下控件：
1. 切片策略选择器（`<select>`）：选项为 auto / structural / recursive（semantic 标注为"高级"）
2. 分片预览折叠面板（ChunkingPreviewPanel 组件）

设置变更通过 RAG REST API `PUT /api/collections/{name}/config` 持久化。

#### Scenario: 用户切换切片策略
- **WHEN** 用户在知识库设置页将策略从 "auto" 切换为 "structural" 并保存
- **THEN** 系统调用 PUT /config 更新 strategy 字段，提示"配置已更新，新上传的文档将使用新策略"

#### Scenario: 策略变更不影响已有文档
- **WHEN** 用户修改策略后查看文档列表
- **THEN** 已有文档的 chunk 数据不变（不自动重新切分），仅新上传文档使用新策略

### Requirement: 文档列表展示增强
知识库文档列表 MUST 新增以下列：
1. Chunks 列：显示文档的 chunk 数量（数字 + "chunks" 后缀）
2. 策略列：显示该文档使用的切分策略（StrategyBadge 组件）
3. 状态列：显示处理状态图标（ready=绿色对勾 / processing=旋转加载 / failed=红色叉）

数据来源：RAG REST API `GET /api/collections/{name}/documents` 响应中新增 chunk_count / strategy / status 字段。

#### Scenario: 文档列表正常展示
- **WHEN** 用户打开知识库详情页
- **THEN** 文档列表每行显示：文件名、大小、chunk 数量、策略徽章、状态图标、上传时间、操作按钮

#### Scenario: 文档无 chunk 数据（旧文档）
- **WHEN** 文档在 chunk_count 字段引入之前上传，API 返回 chunk_count=null
- **THEN** Chunks 列显示 "—"，策略列显示 "—"
