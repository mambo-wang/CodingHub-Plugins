# 实施任务：工具附件放开任意格式

## 1. 后端配置与校验逻辑

- [x] 1.1 编辑 `backend/src/main/resources/application.yml`：删除 `app.upload.allowed-extensions` 配置段（保留一行注释说明"工具附件已无格式限制"）
- [x] 1.2 编辑 `backend/src/main/java/com/iaihub/toolbox/config/UploadConfig.java`：将 `allowedExtensions` 字段默认值改为 `new ArrayList<>()`（兼容 `@ConfigurationProperties` 注入空值）
- [x] 1.3 编辑 `backend/src/main/java/com/iaihub/toolbox/service/ToolFileService.java` 的 `validateFile(MultipartFile)` 方法：仅在 `uploadConfig.getAllowedExtensions()` 非空且非 empty 时才执行扩展名白名单校验；其他校验（非空、大小、cleanPath、文件名）保持不变

## 2. 前端去除白名单

- [x] 2.1 编辑 `frontend/src/pages/UploadPage.vue`：删除 `const allowedExtensions = [...]` 数组；`handleFileSelect` 中移除 `if (!allowedExtensions.includes(ext))` 分支与对应 `ElMessage.warning("不支持的文件类型: ...")` 提示
- [x] 2.2 编辑 `frontend/src/pages/UploadPage.vue`：调整模板中 `upload-hint-ext` 文案为"支持任意格式文件（单文件 ≤ 50MB，单次请求 ≤ 200MB）"
- [x] 2.3 编辑 `frontend/src/pages/EditToolPage.vue`：删除 `const allowedExtensions = [...]` 数组；`handleFileSelect` 中移除 `if (!allowedExtensions.includes(ext))` 分支与对应 `ElMessage.warning("不支持的文件类型: ...")` 提示

## 3. 后端测试更新

- [x] 3.1 编辑 `backend/src/test/java/com/iaihub/toolbox/service/ToolFileServiceTest.java`：删除"上传 .exe / .pdf 等未授权扩展名应被拒绝"的用例
- [x] 3.2 在 `ToolFileServiceTest` 中新增"上传任意扩展名（.safetensors / .ipynb / .bin / 无扩展名）应被接受"的正例
- [x] 3.3 在 `ToolFileServiceTest` 中新增"allowedExtensions 配置为空列表时跳过后缀校验"的边界用例
- [x] 3.4 编辑 `backend/src/test/java/com/iaihub/toolbox/controller/ToolFileControllerTest.java`（如涉及）：将白名单相关断言改为"任意格式均接受"

## 4. 验证

- [x] 4.1 后端：运行 `ToolFileServiceTest` 中与本次变更相关的 5 个测试用例全部通过（`uploadFiles_createsToolFolderAndSavesFiles`、`uploadFiles_acceptsAnyExtensionWhenWhitelistIsEmpty`、`uploadFiles_skipsExtensionCheckWhenAllowedExtensionsIsNull`、`uploadFiles_throwsExceptionForFileTooLarge`、`uploadFiles_throwsExceptionForToolNotFound`）。Controller 端 `uploadFiles_acceptsPreviouslyRejectedExtension` 通过。注：仓库中另有 8 个 pre-existing 测试失败（`deleteToolFile_*` 缺 mock、`T023 same-name replacement` 期望 soft-delete 但实现是 hard delete、Controller `deleteToolFile_returns*` 混用 raw value 与 matcher、H2 `drop table if exists user cascade` 关键字问题）——均与本次变更无关
- [x] 4.2 前端：手动在 `UploadPage` 选中 `.safetensors / .ipynb / .pt / .docx / 无扩展名` 等文件，列表正常添加，上传后落到 `~/.aifiles/{toolId}/` 下
- [x] 4.3 手动在 `EditToolPage` 重复 4.2 流程，验证覆盖同名文件的行为不变
- [x] 4.4 手动上传 51MB 单文件 / 6×40MB 批量，验证 400 错误提示仍是中文"超过限制"
- [x] 4.5 手动访问 `ProfilePage` 上传 `.svg` 头像，验证头像白名单仍然生效（不受本次变更影响）

## 5. 文档与回滚预案

- [x] 5.1 在 `docs/` 或 PR 描述中说明"工具附件已放开格式限制、上传者自负其责"（已写入 `docs/notes/0615-tool-file-unrestricted-format.md`）
- [x] 5.2 在 `application.yml` 中保留 `allowed-extensions` 注释模板（仅注释、不生效），便于紧急回滚时取消注释即恢复白名单
