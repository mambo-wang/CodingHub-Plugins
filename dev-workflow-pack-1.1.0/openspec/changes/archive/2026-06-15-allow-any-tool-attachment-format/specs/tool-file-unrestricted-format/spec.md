# tool-file-unrestricted-format

## Purpose

TBD - 工具附件上传放开扩展名限制，支持任意格式文件。

## Requirements

### Requirement: 工具附件支持任意扩展名

工具附件上传接口 MUST 接受任意扩展名（包括无扩展名、含多点的复合名、罕见或自定义后缀）的二进制文件，不以前端/后端白名单拒绝任何文件。

#### Scenario: 上传常见压缩包
- **WHEN** 上传者通过 `POST /api/v1/tools/{toolId}/files` 上传 `model.zip`（2MB）
- **THEN** 后端返回 200，响应中 `files[0].originalName = "model.zip"`，文件落盘到 `${baseDir}/{toolId}/model.zip`，`tool_file` 表插入记录

#### Scenario: 上传模型权重
- **WHEN** 上传者上传 `weights.safetensors`（30MB）
- **THEN** 后端接受并保存，不抛出"不支持的文件类型"异常

#### Scenario: 上传 Jupyter Notebook
- **WHEN** 上传者上传 `analysis.ipynb`（1MB）
- **THEN** 后端接受并保存

#### Scenario: 上传 Office 文档
- **WHEN** 上传者上传 `requirements.docx` / `data.xlsx`（各 < 5MB）
- **THEN** 后端接受并保存

#### Scenario: 上传无扩展名文件
- **WHEN** 上传者上传 `Dockerfile`（无扩展名，1KB）
- **THEN** 后端接受并保存，`files[0].originalName = "Dockerfile"`

#### Scenario: 上传含多点的复合名
- **WHEN** 上传者上传 `model.v2.final.bin`（20MB）
- **THEN** 后端接受并保存，扩展名按"最后一个点之后"解析为 `bin`

#### Scenario: 批量上传混合扩展名
- **WHEN** 上传者一次提交 5 个文件：`a.zip`、`b.pt`、`c.ipynb`、`d.xlsx`、`e.svg`
- **THEN** 后端全部接受并保存，每个文件独立落盘 + 落库

### Requirement: 保留单文件与总请求大小约束

工具附件上传 MUST 仍然强制单文件 ≤ 50MB、单次请求所有文件总大小 ≤ 200MB；超出部分返回 400 + 中文错误提示。

#### Scenario: 单文件超 50MB
- **WHEN** 上传者上传 51MB 的 `big.bin`
- **THEN** 后端抛出 `FileValidationException("文件大小超过限制 (50MB): big.bin")`，HTTP 状态码 400

#### Scenario: 总大小超 200MB
- **WHEN** 上传者一次提交 6 个 40MB 的文件（总 240MB）
- **THEN** 后端在写入前抛出 `FileValidationException("总上传大小超过限制 (200MB)")`，HTTP 状态码 400，不写入任何文件

### Requirement: 保留文件名与路径安全检查

工具附件上传 MUST 仍然使用 `StringUtils.cleanPath` 校验原始文件名，拒绝路径穿越与空文件名。

#### Scenario: 路径穿越攻击
- **WHEN** 上传者提交 `originalName = "../../etc/passwd"`
- **THEN** 后端要么返回 400 错误"文件名无效"，要么经 `cleanPath` 规整后只保留文件名段（不得跳出 `${baseDir}/{toolId}/`）

#### Scenario: 空文件名
- **WHEN** 上传者提交 `originalName = ""`
- **THEN** 后端返回 400 错误"文件名无效"

#### Scenario: 空文件
- **WHEN** 上传者提交 0 字节文件
- **THEN** 后端返回 400 错误"文件不能为空"

### Requirement: 保留所有权与可见性约束

工具附件上传 MUST 仍然只允许工具上传者本人操作；其他用户调用必须返回 403。

#### Scenario: 非上传者上传文件
- **WHEN** 用户 B 调用 `POST /api/v1/tools/{toolId}/files`（`toolId` 属于用户 A）
- **THEN** 后端返回 403 错误"您只能上传文件到自己的工具"

#### Scenario: 上传到不存在的工具
- **WHEN** 用户上传到 `toolId = 999999`（不存在）
- **THEN** 后端返回 404 错误"工具不存在或已删除"

### Requirement: 前端不进行扩展名预过滤

前端 `UploadPage` 与 `EditToolPage` MUST 移除"允许扩展名"硬编码数组；`handleFileSelect` 不再按扩展名分支拒绝文件，仅按大小（单文件 50MB、总 200MB）预检。

#### Scenario: 用户选择任意扩展名文件
- **WHEN** 用户在上传页选择 `model.safetensors`（30MB）
- **THEN** 文件被加入 `selectedFiles` 列表，不弹"不支持的文件类型"警告

#### Scenario: 用户选择超大单文件
- **WHEN** 用户选择 60MB 的 `huge.bin`
- **THEN** 前端弹 `ElMessage.warning("文件 huge.bin 超过50MB限制")`，不加入列表

#### Scenario: 提示文案更新
- **WHEN** 用户查看上传页"上传文件"区域
- **THEN** 提示文案为"支持任意格式文件（单文件 ≤ 50MB，单次请求 ≤ 200MB）"或同等语义，不再列举具体扩展名

### Requirement: 头像附件的白名单不受影响

用户头像上传 (`POST /api/v1/users/me/avatar`) MUST 仍然受 `avatar-allowed-extensions` 白名单约束（`jpg / jpeg / png / webp / gif`）；本规范不改变头像上传行为。

#### Scenario: 上传非白名单头像
- **WHEN** 用户上传 `avatar.svg` 到头像接口
- **THEN** 后端返回 400"仅支持 jpg / png / webp / gif"，与变更前一致
