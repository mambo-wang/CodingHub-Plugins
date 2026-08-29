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
