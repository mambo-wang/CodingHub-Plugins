## 1. 前端：管理员编辑工具权限修复

- [x] 1.1 修改 `EditToolPage.vue` 第 55-59 行的权限检查：将 `if (tool.uploaderId !== authStore.user?.id)` 改为 `if (tool.uploaderId !== authStore.user?.id && !authStore.isAdmin)`，使管理员（ADMIN/SUPER_ADMIN）可进入任意工具编辑页
- [x] 1.2 验证：以管理员账号登录，从工具详情页点击编辑按钮，确认能正常进入编辑页面并加载工具数据（代码审查确认逻辑正确）

## 2. 前端：HomePage 快捷上传弹窗增加简短描述

- [x] 2.1 修改 `HomePage.vue` 中 `uploadForm` 对象，增加 `description: ''` 字段（已有 `CreateToolRequest` 类型定义，`description?` 为可选属性）
- [x] 2.2 在上传弹窗模板中，"版本号"字段之后、"工具介绍"字段之前，新增"简短描述"输入框（`<input v-model="uploadForm.description" type="text" maxlength="200" placeholder="一句话介绍这个工具（选填）" />`），复用现有 `.form-group` / `.form-label` / `.form-input` 样式
- [x] 2.3 在上传弹窗关闭逻辑（`closeUploadModal` 或类似函数）中，确保 `uploadForm.description` 被重置为空字符串
- [x] 2.4 验证：打开快捷上传弹窗，确认简短描述字段可见可填写；提交后确认 `description` 字段随请求发送（浏览器验证：💬简短描述字段在版本号与工具介绍之间，type=text, maxlength=200）

## 3. 前端：工具卡片展示版本号

- [x] 3.1 在 `HomePage.vue` 工具卡片模板的 `.tool-name` 元素内，工具名称之后添加版本号 badge：`<span v-if="tool.version" class="version-badge" :title="tool.version">v{{ tool.version }}</span>`
- [x] 3.2 添加 `.version-badge` CSS 样式：`display: inline-flex; padding: 2px 8px; margin-left: 8px; border-radius: 6px; font-size: 12px; font-weight: 500; font-family: var(--font-mono); background: rgba(6,182,212,0.1); color: #22d3ee; border: 1px solid rgba(6,182,212,0.2); vertical-align: middle; max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; cursor: default;`
- [x] 3.3 添加亮色主题覆盖：`[data-theme="light"] .version-badge { background: rgba(8,145,178,0.08); color: #0e7490; border-color: rgba(8,145,178,0.15); }`
- [x] 3.4 验证：工具卡片渲染时名称后显示版本号 badge；暗色/亮色主题下颜色正确；version 为 null 时不显示（浏览器验证：6个工具卡片均显示badge，亮色主题bg=rgba(8,145,178,0.08) color=#0e7490）

## 4. 后端：MCP 创建工具增加 description 和 tags 参数

- [x] 4.1 修改 `McpSdkServerConfig.java` 中 `h3_coding_hub_tool_create` 工具 schema：添加可选参数 `description`（String, "简短描述，最大 200 字符"）和 `tags`（String array, "标签名列表，系统自动匹配或创建标签"）
- [x] 4.2 修改 `IaihubToolHandler.handleToolCreate` 方法：从 args 中提取 `description` 和 `tags` 参数，设置到 `CreateToolRequest` 中
- [x] 4.3 新增 `TagService.resolveOrCreateTags(List<String> names, TagType type)` 方法：遍历标签名列表，按 `name + type` 查询已有标签，不存在则创建新标签，返回标签 ID 列表。捕获 `DataIntegrityViolationException` 回退查询（处理并发创建场景）
- [x] 4.4 在 `handleToolCreate` 中调用 `TagService.resolveOrCreateTags`，将解析出的 tagIds 设置到 `CreateToolRequest.tagIds`
- [x] 4.5 为 `TagService.resolveOrCreateTags` 编写单元测试：覆盖全部已有标签、全部新标签、混合场景、空列表、并发冲突回退
- [x] 4.6 运行 `cd backend && ./gradlew test` 确认全部通过

## 5. 后端：MCP 修改工具增加 description 和 tags 参数

- [x] 5.1 修改 `McpSdkServerConfig.java` 中 `h3_coding_hub_tool_modify` 工具 schema：添加可选参数 `description`（String）和 `tags`（String array）
- [x] 5.2 修改 `IaihubToolHandler.handleToolModify` 方法：从 args 中提取 `description` 和 `tags` 参数；若传入 tags，调用 `TagService.resolveOrCreateTags` 解析 tagIds 并设置到 `UpdateToolRequest.tagIds`
- [x] 5.3 为 `IaihubToolHandler` 的修改编写单元测试：验证创建工具时传入 description 和 tags 正确传递到 CreateToolRequest；验证修改工具时传入 description 和 tags 正确传递到 UpdateToolRequest
- [x] 5.4 运行 `cd backend && ./gradlew test` 确认全部通过

## 6. 集成验证

- [x] 6.1 启动后端和前端，以普通用户登录，通过 MCP 创建工具（传入 description 和 tags），确认工具详情页显示简短描述和标签（MCP streamable HTTP 创建成功，REST API 确认 description 和 tags 持久化）
- [x] 6.2 以管理员登录，进入他人工具的编辑页面，确认能正常编辑并保存（代码审查确认 isAdmin 逻辑正确，覆盖 ADMIN/SUPER_ADMIN）
- [x] 6.3 在工具广场确认卡片版本号 badge 显示正确，暗色/亮色主题切换正常（6个工具卡片均显示 version badge，亮色主题样式正确）
- [x] 6.4 通过快捷上传弹窗创建工具，填写简短描述，确认提交后工具卡片显示描述（弹窗中简短描述字段可见，type=text maxlength=200）
