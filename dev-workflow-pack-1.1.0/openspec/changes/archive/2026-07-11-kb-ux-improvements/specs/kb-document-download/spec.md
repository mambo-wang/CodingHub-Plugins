## ADDED Requirements（新增需求）

### Requirement: 文档源文件下载

知识库文档列表必须支持源文件下载功能，用户可以点击下载按钮获取上传时的原始文件。

#### Scenario: 下载已存在的源文件

- **WHEN** 用户点击文档列表中状态为 READY 的文档的下载按钮
- **THEN** 系统必须向 RAG 服务发起 `GET /api/collections/{col}/documents/download?filepath={filepath}` 请求，触发浏览器原生文件下载

#### Scenario: 下载不存在的源文件

- **WHEN** 用户尝试下载一个源文件已被删除或未保存的文档（如历史文本文件）
- **THEN** 系统必须显示友好提示"源文件不可用，请重新上传"，不触发下载

#### Scenario: 下载按钮可见性

- **WHEN** 文档列表加载完成
- **THEN** 每个文档项必须显示下载按钮图标，与现有删除按钮并列排列

#### Scenario: 下载请求经过代理

- **WHEN** 在生产环境（Nginx 代理）或开发环境（Vite dev server 代理）
- **THEN** 下载请求必须通过 `/rag/` 前缀正确代理到 RAG 服务（`:8000`），Nginx 和 Vite 均需正确配置代理规则

### Requirement: RAG 服务文件下载 API

RAG 服务必须提供文件下载 REST API endpoint，根据 filepath 参数返回存储在 `_uploads/` 目录下的原始文件。

#### Scenario: 合法文件路径下载

- **WHEN** 收到 `GET /api/collections/{name}/documents/download?filepath=data/_uploads/{col}/{filename}` 请求且文件存在
- **THEN** 系统必须以 `application/octet-stream` Content-Type 返回文件内容，`Content-Disposition` 头包含原始文件名

#### Scenario: 路径遍历攻击防护

- **WHEN** 收到包含 `../` 或路径遍历尝试的 filepath 参数
- **THEN** 系统必须拒绝请求并返回 403 Forbidden，不读取任何文件

#### Scenario: 文件不存在

- **WHEN** 请求的 filepath 对应文件在磁盘上不存在
- **THEN** 系统必须返回 404 Not Found 和错误消息

#### Scenario: filepath 参数缺失

- **WHEN** 下载请求未包含 filepath 参数
- **THEN** 系统必须返回 400 Bad Request 和错误消息

### Requirement: 文本文件上传时保存原文件

RAG 服务的 `ingest_content` 函数必须在处理文本文件时将原始内容保存到 `_uploads/` 目录，使文本文件与二进制文件一样可以被下载。

#### Scenario: 上传文本文件并保存原文件

- **WHEN** 用户通过 REST API 上传文本类型文件（.md, .txt, .py 等）
- **THEN** 系统必须将原始文本内容写入 `data/_uploads/{collection}/{filename}`，同时执行分块和向量化

#### Scenario: 重复上传同名文本文件

- **WHEN** 用户重新上传同名文本文件
- **THEN** 系统必须覆盖 `_uploads/` 下的旧文件，与现有幂等性逻辑一致
