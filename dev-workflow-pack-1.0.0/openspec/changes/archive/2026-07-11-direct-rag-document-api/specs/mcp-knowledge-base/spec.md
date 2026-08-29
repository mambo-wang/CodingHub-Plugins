## MODIFIED Requirements（修改需求）

### Requirement: MCP 上传文档
MCP 客户端 SHALL 能够通过 `h3_coding_hub_kb_upload_document` 工具获取 RAG Python 服务的文档直传地址。此工具返回 RAG 服务的上传 API URL，客户端通过 HTTP multipart POST 直传文件到 RAG，无需认证。

#### Scenario: 获取 RAG 直传信息
- **WHEN** 客户端传入 `kbId`
- **THEN** 系统返回 RAG 直传接口信息，包含：`uploadUrl`（完整 RAG URL，如 `http://localhost:8000/api/collections/vdi/documents`）、`httpMethod: "POST"`、`contentType: "multipart/form-data"`、`formFields: "file (必填)"`、`requiresAuth: "无需认证"`、`curlExample`（指向 RAG 地址的 curl 示例）

#### Scenario: 知识库不存在
- **WHEN** 客户端传入不存在的 `kbId`
- **THEN** 系统返回错误信息 "知识库不存在"，isError=true
