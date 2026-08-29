## Why

工具广场目前对工具附件设置了白名单（仅允许 `zip / tar / gz / py / js / ts / md / txt / json / yaml / yml / toml / xml / html / css` 等 15 种后缀），导致用户上传 AI 工具时无法附带模型权重（.pt / .bin / .safetensors / .onnx）、数据集（.csv / .parquet / .h5）、训练脚本依赖（.ipynb / .r / .sh）、Office 文档（.docx / .xlsx / .pptx）、图片素材（.png / .jpg / .svg）、可执行文件（.exe / .whl）等常见资源，严重限制了工具的完整分发能力。本次变更放开附件格式限制，改为支持任意格式的单文件上传（仍保留 50MB 单文件 / 200MB 总请求的大小约束），让上传者可以一站式交付工具全部资产。

## What Changes

- 移除后端工具附件后缀白名单（`app.upload.allowed-extensions`），不再按扩展名拒绝文件
- `UploadConfig.allowedExtensions` 字段保留为可空配置；当为空/缺失时，跳过扩展名校验
- `ToolFileService.validateFile()` 不再抛出"不支持的文件类型"异常，仅校验文件名、文件大小
- 前端 `UploadPage.vue` / `EditToolPage.vue` 移除 `allowedExtensions` 数组与 `handleFileSelect` 中的扩展名分支，将"格式不支持"提示改为通用警告
- 调整 `application.yml` 注释：明确说明工具附件已无格式限制
- 同步更新 `ToolFileServiceTest` / `ToolFileControllerTest`：删除"拒绝未授权扩展名"的用例，新增"任意扩展名通过校验"的用例
- 文件大小（单文件 50MB / 总请求 200MB）、文件名安全（防路径穿越）、存储路径规则**保持不变**

> 备注：头像上传（`avatar-allowed-extensions`）仍受白名单限制，**不在本次变更范围**——它服务于"图像"这一独立能力，需独立规格。

## Capabilities

### New Capabilities

- `tool-file-unrestricted-format`：工具附件（`POST /api/v1/tools/{toolId}/files`）放开扩展名限制，理论上允许任意 MIME / 任意后缀的二进制文件通过校验；保留单文件 ≤50MB、单次请求 ≤200MB 的体积约束，保留文件名 `cleanPath` 与 `Path` 写入安全检查。

### Modified Capabilities

（无。本次变更前，工具附件功能没有独立的 spec，故无需修改已有能力；如未来引入 `tool-file-upload` 全量规范，本次新增的 `tool-file-unrestricted-format` 应被该规范包含。）

## Impact

- **后端**：
  - `backend/src/main/resources/application.yml`（删除 `allowed-extensions` 列表）
  - `backend/src/main/java/com/iaihub/toolbox/config/UploadConfig.java`（字段语义改为可选）
  - `backend/src/main/java/com/iaihub/toolbox/service/ToolFileService.java`（`validateFile` 流程调整）
  - `backend/src/test/.../service/ToolFileServiceTest.java`（用例改造）
  - `backend/src/test/.../controller/ToolFileControllerTest.java`（如涉及）
- **前端**：
  - `frontend/src/pages/UploadPage.vue`（移除白名单、调整提示文案）
  - `frontend/src/pages/EditToolPage.vue`（同上）
- **API 契约**：`POST /api/v1/tools/{toolId}/files` 仍以 `multipart/form-data` 接收 `files[]`，响应结构不变；客户端错误码 `400 "不支持的文件类型: .xxx"` 改为仅在更严重输入错误时出现
- **存储与下载**：`ToolFile` 表与文件落盘路径不变；下载接口保持原样
- **安全**：仍然依赖 Spring 框架的 Multipart 解析与 `StringUtils.cleanPath` 防止路径穿越；头像等独立能力的白名单未受影响
