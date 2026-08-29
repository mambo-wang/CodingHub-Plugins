# Rag Protected Patterns

## ADDED Requirements（新增需求）

### Requirement: 保护区域识别
系统 MUST 在切分前对文档文本执行正则预扫描，识别以下 6 类不可切断的原子内容区域：
1. LaTeX 块公式（`$$...$$`）
2. Markdown 图片（`![alt](url)`）
3. Markdown 链接（`[text](url)`）
4. 表格头+分隔行（`| col | col |\n| --- | --- |`）
5. 表格数据行（`| ... |`）
6. 围栏代码块（` ```lang ... ``` `）

保护区域以 byte offset span 列表形式返回，按 start 排序，重叠区域取最长匹配。

#### Scenario: 文档包含 Markdown 图片
- **WHEN** 文档文本包含 `![架构图](https://example.com/arch.png)`
- **THEN** 该图片标记的 byte 范围被加入保护 span 列表，切分时不会在 `[` 和 `)` 之间断开

#### Scenario: 文档包含 LaTeX 公式
- **WHEN** 文档文本包含 `$$E = mc^2$$` 块公式
- **THEN** 整个公式（含 `$$` 定界符）被标记为保护区域，切分时保持完整

#### Scenario: 文档包含围栏代码块
- **WHEN** 文档文本包含 ` ```python\nprint("hello")\n``` ` 围栏代码块
- **THEN** 从开头 ` ``` ` 到结尾 ` ``` ` 的全部内容包括语言标记被标记为一个保护区域

#### Scenario: 文档包含表格
- **WHEN** 文档文本包含连续多行 `| col1 | col2 |` 格式的表格
- **THEN** 表头行+分隔行+所有数据行各自作为独立保护 span，切分不在行中间断开

### Requirement: 切分跳过保护区域
系统 MUST 在递归切分和结构切分时，仅在非保护区域内选择切分点。保护区域作为原子单元参与 chunk 合并。

#### Scenario: 保护区域跨越 chunk 边界
- **WHEN** 一个保护区域（如代码块）的起始位置在当前 chunk 内，但完整内容超出 chunk_size
- **THEN** 系统将该保护区域整体保留在当前 chunk 中（允许 chunk 略微超出 chunk_size），而非在保护区域中间切断

#### Scenario: 超大保护区域强制切分
- **WHEN** 单个保护区域超过 7500 字符（absoluteMaxSize）
- **THEN** 系统在该保护区域内部的换行符或空格处强制切分，每段不超过 7500 字符

#### Scenario: 非保护区域正常切分
- **WHEN** 两个保护区域之间存在普通文本且总长超过 chunk_size
- **THEN** 系统在非保护区域内按正常分隔符优先级（`\n\n` > `\n` > `。`）选择切分点

### Requirement: 保护区域不影响 semantic 模式
系统 MUST NOT 在 semantic 切片模式下执行保护区域扫描。semantic 模式按句子粒度切分，句子提取逻辑本身不会切断行内元素。

#### Scenario: semantic 模式跳过保护扫描
- **WHEN** collection config 的 chunk_mode 为 "semantic"
- **THEN** 切分流程不调用 protected_spans()，直接执行句子编码和相似度断点切分
