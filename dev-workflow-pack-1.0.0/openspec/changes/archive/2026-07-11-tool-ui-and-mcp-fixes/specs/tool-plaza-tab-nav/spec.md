## MODIFIED Requirements（修改需求）

### Requirement: 工具上传弹窗

系统 SHALL 在 filter bar 最右侧提供上传工具图标按钮，点击后弹出 Modal 进行工具上传。

#### Scenario: 点击上传按钮打开 Modal
- **WHEN** 已登录用户点击上传图标按钮
- **THEN** 弹出上传 Modal，表单包含：工具名称、分类选择、版本号、简短描述、描述（Markdown）、文件上传区域

#### Scenario: 未登录用户点击上传按钮
- **WHEN** 未登录用户点击上传图标按钮
- **THEN** 跳转到登录页面 `/login`，携带 `redirect` 参数

#### Scenario: 上传成功后刷新数据
- **WHEN** 用户在 Modal 中成功上传工具
- **THEN** Modal 关闭，当前 Tab 数据自动刷新（重新调用对应 API），分页重置为第 0 页

#### Scenario: 上传 Modal 表单验证
- **WHEN** 用户提交表单时缺少必填字段（名称、描述、版本号）
- **THEN** 提交按钮禁用，不允许提交

#### Scenario: 上传 Modal 简短描述字段
- **WHEN** 用户在 Modal 中填写简短描述字段
- **THEN** 输入内容绑定到 `uploadForm.description`，最大 200 字符，选填，placeholder 为"一句话介绍这个工具（选填）"

#### Scenario: 上传 Modal 关闭
- **WHEN** 用户点击 Modal 遮罩层或关闭按钮
- **THEN** Modal 关闭，表单数据清空

### Requirement: 工具卡片版本号展示

系统 SHALL 在工具广场的工具卡片上，工具名称（`.tool-name`）之后以 badge 形式展示版本号。badge 文本为 `v{version}`，使用 `font-family: var(--font-mono)` 和 accent-2 配色。当 `tool.version` 为 null 或空时不显示 badge。

#### Scenario: 工具卡片显示版本号
- **GIVEN** 工具 "MyTool" 的 version 为 "2.1.0"
- **WHEN** 工具卡片渲染
- **THEN** 工具名称后显示 badge "v2.1.0"，使用青色（accent-2）配色，Space Mono 字体

#### Scenario: 工具无版本号时不显示 badge
- **GIVEN** 工具的 version 为 null 或空字符串
- **WHEN** 工具卡片渲染
- **THEN** 工具名称后不显示版本号 badge

#### Scenario: 版本号超长截断
- **GIVEN** 工具的 version 为 "1.0.0-beta-rc1-snapshot-20260710"
- **WHEN** 工具卡片渲染
- **THEN** 版本号 badge 最大宽度 120px，超出部分以 ellipsis 截断，hover 时显示完整版本号（title 属性）

## ADDED Requirements（新增需求）

### Requirement: 快捷上传弹窗简短描述字段

HomePage 的快捷上传弹窗 SHALL 包含 `description`（简短描述）输入字段，与独立 UploadPage 的表单字段保持一致。字段位于"版本号"之后、"工具介绍"之前。

#### Scenario: 快捷上传弹窗包含简短描述输入框
- **WHEN** 已登录用户打开快捷上传弹窗
- **THEN** 表单中包含"简短描述"文本输入框，label 文本为"简短描述"，placeholder 为"一句话介绍这个工具（选填）"

#### Scenario: 简短描述字段数据绑定
- **WHEN** 用户在简短描述输入框中输入文本
- **THEN** 文本绑定到 `uploadForm.description`，随表单提交发送到 `POST /api/v1/tools`
