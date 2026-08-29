## Context

工具广场（AI Tool Square）允许上传者以 ZIP 压缩包 / 散落脚本 / 配置文件的形式分发自己的 AI 工具。`ToolFileService.uploadFiles()` 接收 `MultipartFile[]` 后，会调用 `validateFile()` 对每个文件做三项校验：非空、单文件 ≤ 50MB、扩展名 ∈ 后端白名单。扩展名白名单由 `application.yml` 的 `app.upload.allowed-extensions` 提供（当前为 15 种后缀）。

白名单限制了 AI 工具的典型附件形态：模型权重（`.pt / .bin / .safetensors / .onnx`）、数据集（`.csv / .parquet / .h5`）、Jupyter Notebook（`.ipynb`）、Office 文档（`.docx / .xlsx / .pptx`）、图像资源（`.png / .jpg / .svg`）、Python wheel（`.whl`）、shell 脚本（`.sh`）等一律被拒。本次变更将这些"格式安全"责任从"扩展名白名单"前移到"运行时按需校验 / 下载方按 MIME 自决"，由上传者自行承担"分发内容合法性"，平台仅守住大小、路径、归属。

## Goals / Non-Goals

**Goals：**
- 工具附件的上传与存储流程对扩展名 / MIME 完全透明；任意后缀（包括无后缀）的文件都可以保存
- 保留现有所有不变量：单文件 ≤ 50MB、单次请求 ≤ 200MB、防路径穿越、所有权校验、覆盖同名文件的语义
- 前端不再做"扩展名预过滤"，仅保留大小 / 总容量预检，UI 提示文案改为通用上传提示
- 既有 API 契约（`POST /api/v1/tools/{toolId}/files`）的请求 / 响应结构、错误码体系向下兼容
- 不引入新依赖（无新的过滤器、无新的安全中间件）

**Non-Goals：**
- 不做"恶意内容扫描"（病毒 / WebShell 静态扫描、超大炸弹检测等），那是后续独立的"安全上传"能力
- 不修改头像上传的扩展名白名单（`avatar-allowed-extensions` 保持 `jpg/jpeg/png/webp/gif`）
- 不调整 50MB / 200MB 上限（即使放开格式，这些体积约束仍然有效）
- 不动 `tool_file` 表结构、存储目录规则、下载接口实现
- 不修改 MCP 客户端旁路登录的匿名上传分支行为

## Decisions

### Decision 1: 用"白名单可空"代替"删除白名单"作为可配置语义

`UploadConfig.allowedExtensions` 字段保留为 `List<String>` 类型，但**默认值改为空列表**（`new ArrayList<>()`）而非当前的 `null`。`application.yml` 不再写 `allowed-extensions` 段。`ToolFileService.validateFile()` 改为：

```java
List<String> allowed = uploadConfig.getAllowedExtensions();
if (allowed != null && !allowed.isEmpty()) {
    String ext = getFileExtension(originalName).toLowerCase();
    if (!allowed.contains(ext)) {
        throw new FileValidationException("不支持的文件类型: ." + ext);
    }
}
```

**理由**：保留可空配置 → 未来想再加回白名单（"白名单模式"）只需改 `application.yml` 一行配置，无须改代码。空列表 / null 等价于"无白名单"。
**替代方案**：直接删除 `allowedExtensions` 字段 → 改动更小但失去"按需启用白名单"的弹性，不选。
**替代方案**：用 `List<String> blockedExtensions`（黑名单）→ 黑名单永远列举不完，无意义，不选。

### Decision 2: 前端不维护"允许列表"变量，仅保留大小预检

`UploadPage.vue` / `EditToolPage.vue` 删除 `const allowedExtensions = [...]` 数组和 `handleFileSelect()` 中对 `allowedExtensions.includes(ext)` 的判断；当文件超过 50MB 时仍然弹 `ElMessage.warning`，否则直接将 `File` 推入 `selectedFiles`。提示文案由 `"支持 .zip, .tar, .gz, .py, .js, .ts, .md 等格式"` 改为 `"支持任意格式文件（单文件 ≤ 50MB，单次请求 ≤ 200MB）"`。

**理由**：客户端预过滤对**任意格式支持**是矛盾的——既然服务端放开了，客户端没必要再守一份副本，省去前后端列表漂移问题。
**替代方案**：前端根据后端 `/api/v1/config` 动态拉白名单 → 引入新接口、新状态机、缓存失效问题，得不偿失，不选。

### Decision 3: 错误码与"400 不支持的文件类型"文案处理

保留 `FileValidationException` 类与"不支持的文件类型"错误文案作为"白名单模式"下的兜底。当前默认配置（白名单为空）下该分支永远不会被触发，但通过配置开启白名单时仍然可用。测试用例需新增"上传任意扩展名（包括无后缀）通过"的正例。

**理由**：避免在"无白名单默认"模式下抛出无意义异常，同时给将来"开启白名单"留好接口。
**替代方案**：完全删除 `FileValidationException` 与"不支持的文件类型"分支 → 不可逆、不可回退，不选。

### Decision 4: 头像白名单独立保留

`UploadConfig.avatarAllowedExtensions` 与 `AvatarUtil`（如有）的格式校验**不受本次变更影响**。头像属于"用户身份资源"维度，扩展名控制对应"防 XSS / 防 SVG 注入"等安全考量，与工具附件的"分发资源"维度是不同问题。

**理由**：单一职责，避免本次顺手修改带来未审计的副作用。
**替代方案**：在 `AvatarUtil` 里直接复用 `UploadConfig.allowedExtensions` → 破坏关注点隔离，引入耦合，不选。

## Risks / Trade-offs

- **[风险] 任意扩展名 → 落地任意二进制** → 上传者可能误传/故意散布可执行脚本（`.exe / .sh / .bat`），下载方运行风险
  - 缓解：在 `proposal.md` 中明确"下载方自负其责"；后续可叠加"按文件 hash 查重 / 病毒扫描"等独立能力

- **[风险] 失去扩展名预过滤，前端 UX 退化** → 用户选择超大视频（`.mov 500MB`）才被服务端 400 拒绝，体验不佳
  - 缓解：前端仍保留 50MB 单文件、200MB 总请求的预检；UI 提示文案已包含上限

- **[风险] `cleanPath` 之外的扩展名滥用** → 例如 `file.config.json` 变成 `file.config.json` 后仍可能含 `../` 风格
  - 缓解：保持现有 `StringUtils.cleanPath` + `Path.resolve` 双重防护；新增"无扩展名 / 仅含点"等边界测试用例

- **[权衡] 删除白名单配置后，运维侧"防止不合法资源"失去一道护栏** → 改为按运行时审计 / 举报机制处理
  - 接受：工具广场定位为低门槛分享平台，运维责任下沉到"内容治理"层

## Migration Plan

- 部署步骤：
  1. 后端 `application.yml` 移除 `allowed-extensions` 段（保留注释说明"工具附件已无格式限制"）
  2. 后端 `UploadConfig` 字段默认值调整
  3. 后端 `ToolFileService.validateFile()` 分支调整
  4. 前端 `UploadPage.vue` / `EditToolPage.vue` 移除白名单数组、调整提示文案
  5. 重启后端 + 重新构建前端
- 回滚策略：保留 `application.yml` 中 `allowed-extensions` 配置的注释模板（仅注释，不生效），紧急回滚只需取消注释并重启；前端可还原 `allowedExtensions` 数组
- 数据兼容：`tool_file` 表无结构变更；存量记录不受影响；历史被拒文件可重新上传

## Open Questions

- 是否需要在下载接口响应头中加入 `X-Content-Type-Options: nosniff` 以缓解浏览器嗅探执行风险？（建议接入，但属独立 PR）
- 是否引入"按 file_size × extension 的二维配额"（例如 `.exe` 类可执行文件单文件 ≤ 5MB）以更细粒度防滥用？（暂缓，等真实滥用数据再评估）
