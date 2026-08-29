## ADDED Requirements（新增需求）

### Requirement: MCP 知识库列表

MCP 客户端 SHALL 能够通过 `h3_coding_hub_kb_list` 工具获取知识库分页列表。

#### Scenario: 获取默认列表
- **WHEN** 客户端调用 `h3_coding_hub_kb_list` 不传任何参数
- **THEN** 系统返回最新排序的知识库列表，默认 page=0, size=20

#### Scenario: 按热度排序
- **WHEN** 客户端调用 `h3_coding_hub_kb_list` 传入 `sortBy="hot"`
- **THEN** 系统返回按热度排序的知识库列表

#### Scenario: 分页参数
- **WHEN** 客户端调用 `h3_coding_hub_kb_list` 传入 `page=1, size=10`
- **THEN** 系统返回第 2 页、每页 10 条的知识库列表

### Requirement: MCP 知识库语义搜索

MCP 客户端 SHALL 能够通过 `h3_coding_hub_kb_search` 工具对指定知识库执行语义搜索。此操作无需认证。

#### Scenario: 成功搜索
- **WHEN** 客户端调用 `h3_coding_hub_kb_search` 传入 `kbId` 和 `query`
- **THEN** 系统返回语义搜索结果列表，每项包含 text、source、score、chunkIndex

#### Scenario: 自定义 topK
- **WHEN** 客户端调用 `h3_coding_hub_kb_search` 传入 `topK=3`
- **THEN** 系统最多返回 3 条搜索结果

#### Scenario: 知识库不存在
- **WHEN** 客户端调用 `h3_coding_hub_kb_search` 传入不存在的 `kbId`
- **THEN** 系统返回错误信息，isError=true

### Requirement: MCP 创建知识库

MCP 客户端 SHALL 能够通过 `h3_coding_hub_kb_create` 工具创建新知识库。此操作需要认证。

#### Scenario: 成功创建
- **WHEN** 客户端传入 `name`、`username`、`password` 以及可选的 `description`、`chunkMode`、`chunkSize`、`chunkOverlap`、`rerank`
- **THEN** 系统创建知识库 MySQL 记录并初始化 RAG collection 配置，返回 KbResponse（含 id、name、ragCollection 等）

#### Scenario: 认证失败
- **WHEN** 客户端传入错误的 username 或 password
- **THEN** 系统返回错误信息 "认证失败"，isError=true

#### Scenario: 名称重复
- **WHEN** 客户端传入已存在的知识库名称
- **THEN** 系统返回错误信息 "知识库名称已存在"，isError=true

#### Scenario: 名称为空
- **WHEN** 客户端不传 name 或 name 为空字符串
- **THEN** 系统返回错误信息，isError=true

### Requirement: MCP 更新知识库

MCP 客户端 SHALL 能够通过 `h3_coding_hub_kb_update` 工具更新知识库的名称、描述和 RAG 配置参数。此操作需要认证。

#### Scenario: 成功更新描述
- **WHEN** 客户端传入 `kbId`、`username`、`password` 和 `description`
- **THEN** 系统更新知识库描述并同步到 RAG config，返回更新后的 KbResponse

#### Scenario: 成功更新 RAG 配置参数
- **WHEN** 客户端传入 `kbId`、`username`、`password` 以及可选的 `chunkMode`、`chunkSize`、`chunkOverlap`、`rerank`
- **THEN** 系统调用 `knowledgeBaseService.updateConfig()` 更新 RAG collection 配置，返回更新后的 KbResponse

#### Scenario: 同时更新名称和配置
- **WHEN** 客户端传入 `kbId`、`username`、`password`、`name`、`description`、`chunkSize` 等多个字段
- **THEN** 系统先调用 `updateKnowledgeBase()` 更新名称/描述，再调用 `updateConfig()` 更新 RAG 配置参数，返回更新后的 KbResponse

#### Scenario: 非所有者更新
- **WHEN** 非知识库所有者且非管理员调用此工具
- **THEN** 系统返回错误信息 "无权操作此知识库"，isError=true

### Requirement: MCP 删除知识库

MCP 客户端 SHALL 能够通过 `h3_coding_hub_kb_delete` 工具删除知识库。此操作需要认证。

#### Scenario: 成功删除
- **WHEN** 知识库所有者传入 `kbId`、`username`、`password`
- **THEN** 系统软删除知识库（status=DELETED）并删除 RAG collection，返回成功响应

#### Scenario: 非所有者删除
- **WHEN** 非知识库所有者且非管理员调用此工具
- **THEN** 系统返回错误信息 "无权操作此知识库"，isError=true

### Requirement: MCP 上传文档

MCP 客户端 SHALL 能够通过 `h3_coding_hub_kb_upload_document` 工具获取 RAG Python 服务的文档直传地址。此工具返回 RAG 服务的上传 API URL，客户端通过 HTTP multipart POST 直传文件到 RAG，无需认证。

> **注**：本需求由 `direct-rag-document-api` 变更从「返回 Java 代理上传接口（需认证）」修改为「返回 RAG 直传地址（无需认证）」。

#### Scenario: 获取 RAG 直传信息
- **WHEN** 客户端传入 `kbId`
- **THEN** 系统返回 RAG 直传接口信息，包含：`uploadUrl`（完整 RAG URL，如 `http://localhost:8000/api/collections/vdi/documents`）、`httpMethod: "POST"`、`contentType: "multipart/form-data"`、`formFields: "file (必填)"`、`requiresAuth: "无需认证"`、`curlExample`（指向 RAG 地址的 curl 示例）

#### Scenario: 知识库不存在
- **WHEN** 客户端传入不存在的 `kbId`
- **THEN** 系统返回错误信息 "知识库不存在"，isError=true
