## ADDED Requirements（新增需求）

### Requirement: 搜索结果 Markdown 渲染

知识库搜索结果必须以 Markdown 格式渲染显示，将 RAG 返回的 Markdown 片段转换为格式化 HTML 展示，包括标题、列表、代码块（带语法高亮）、表格等元素。

#### Scenario: 正常渲染 Markdown 搜索结果

- **WHEN** 用户执行知识库搜索且返回包含 Markdown 语法的结果（如 `# 标题`、`- 列表项`、`` `代码` ``）
- **THEN** 系统必须将 `result.text` 通过 markdown-it 渲染为 HTML，使用 `v-html` 输出到 `.result-text` 容器，代码块使用 highlight.js 高亮

#### Scenario: 搜索结果不包含 Markdown 语法

- **WHEN** 用户执行知识库搜索且返回的结果为纯文本（无 Markdown 语法）
- **THEN** 系统必须正常显示纯文本内容，渲染效果与当前行为一致

#### Scenario: 搜索结果包含不完整的 Markdown 结构

- **WHEN** RAG 返回的 chunk 包含未闭合的 Markdown 结构（如未闭合的代码块 ``` 或未配对的列表）
- **THEN** 系统必须容错渲染，不产生页面崩溃或严重布局错乱

#### Scenario: 搜索结果包含潜在 XSS 内容

- **WHEN** 搜索结果文本中包含原始 HTML 标签（如 `<script>`、`<iframe>`）
- **THEN** 系统必须使用 `html: false` 配置 markdown-it，阻止原始 HTML 被渲染为可执行元素

#### Scenario: 双主题代码块样式

- **WHEN** 用户在暗色/亮色主题间切换
- **THEN** 搜索结果中的代码块必须跟随主题切换样式（暗色使用 github-dark，亮色使用 github-light 或等效浅色方案）
