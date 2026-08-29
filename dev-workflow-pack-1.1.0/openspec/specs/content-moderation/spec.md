## ADDED Requirements（新增需求）

### Requirement: 内容审核权限

系统 SHALL 允许管理员（ADMIN/SUPER_ADMIN）删除和编辑任何用户创建的工具、帖子、微课，与创建者享有同等的删除和编辑权限。非创建者且非管理员的用户 SHALL 无法操作他人内容。

权限判断规则：`canModify = isOwner || (role == ADMIN || role == SUPER_ADMIN)`。删除和编辑使用相同的权限判断（权限对称）。

#### Scenario: 管理员删除他人创建的工具
- **WHEN** 角色为 ADMIN 的用户对他人创建的工具调用 `DELETE /api/v1/tools/{id}`
- **THEN** 工具状态标记为 DELETED，返回 200 成功响应

#### Scenario: 超级管理员删除他人创建的帖子
- **WHEN** 角色为 SUPER_ADMIN 的用户对他人创建的帖子调用 `DELETE /api/forum/posts/{id}`
- **THEN** 帖子状态标记为 DELETED，返回 204 成功响应

#### Scenario: 管理员编辑他人创建的微课
- **WHEN** 角色为 ADMIN 的用户对他人创建的微课调用 `PUT /api/v1/videos/{id}`，传入新的 title
- **THEN** 微课标题更新成功，返回 200 成功响应

#### Scenario: 普通用户无法删除他人内容
- **WHEN** 角色为 USER 的用户对他人创建的工具调用 `DELETE /api/v1/tools/{id}`
- **THEN** 返回 403 Forbidden，工具状态不变

#### Scenario: 普通用户无法编辑他人内容
- **WHEN** 角色为 USER 的用户对他人创建的帖子调用 `PUT /api/forum/posts/{id}`
- **THEN** 返回 403 Forbidden，帖子内容不变

#### Scenario: 创建者仍可删除和编辑自己的内容
- **WHEN** 创建者对自己的工具调用 `DELETE` 或 `PUT`
- **THEN** 操作成功，行为与变更前一致

### Requirement: 前端内容操作按钮显示规则

前端 SHALL 根据当前用户角色和内容归属，在列表页卡片（hover 态）和详情页显示编辑/删除按钮。无权限时 SHALL 不显示任何操作按钮。

按钮显示条件：
- `canEdit = isLoggedIn && (currentUserId === ownerId || isAdmin)`
- `canDelete = canEdit`（权限对称）

列表页卡片按钮采用半透明（`opacity: 0.35`）默认态，卡片 hover 时高亮（`opacity: 1`），确保移动端无 hover 时仍可见。

#### Scenario: 创建者在列表页 hover 看到自己内容的操作按钮
- **WHEN** 已登录的创建者浏览列表页，鼠标 hover 到自己创建的内容卡片上
- **THEN** 卡片右上角显示半透明→高亮的编辑（Pencil 图标）和删除（Trash2 图标）按钮

#### Scenario: 管理员在列表页 hover 看到任意内容的操作按钮
- **WHEN** 已登录的管理员浏览列表页，鼠标 hover 到任意用户创建的内容卡片上
- **THEN** 卡片右上角显示编辑和删除按钮

#### Scenario: 普通用户在列表页看不到他人内容的操作按钮
- **WHEN** 已登录的普通用户（USER 角色）浏览列表页，鼠标 hover 到他人创建的内容卡片上
- **THEN** 卡片不显示任何编辑/删除按钮

#### Scenario: 未登录用户在列表页看不到操作按钮
- **WHEN** 未登录游客浏览列表页
- **THEN** 所有卡片均不显示编辑/删除按钮

#### Scenario: 创建者在详情页看到编辑和删除按钮
- **WHEN** 已登录的创建者访问自己内容的详情页
- **THEN** 详情页操作区显示编辑按钮和删除按钮

#### Scenario: 管理员在详情页看到任意内容的编辑和删除按钮
- **WHEN** 已登录的管理员访问任意内容的详情页
- **THEN** 详情页操作区显示编辑按钮和删除按钮

#### Scenario: 普通用户在详情页看不到他人内容的操作按钮
- **WHEN** 已登录的普通用户访问他人内容的详情页
- **THEN** 详情页不显示编辑/删除按钮

### Requirement: 删除操作二次确认

所有内容的删除操作 SHALL 弹出确认对话框，用户确认后才执行删除。确认对话框使用项目现有的 `ConfirmDialog` 组件。

#### Scenario: 点击删除按钮弹出确认对话框
- **WHEN** 有权限的用户点击工具/帖子/微课的删除按钮
- **THEN** 弹出 ConfirmDialog，标题为"删除{内容类型}"，描述提示删除不可恢复，含"取消"和"确认删除"按钮

#### Scenario: 确认删除后内容被软删除
- **WHEN** 用户在确认对话框点击"确认删除"且后端返回成功
- **THEN** 对话框关闭，toast 提示删除成功，列表页移除该项或详情页跳转回列表

#### Scenario: 取消删除不执行操作
- **WHEN** 用户在确认对话框点击"取消"或按 Esc
- **THEN** 对话框关闭，内容不被删除

### Requirement: 帖子编辑功能

系统 SHALL 提供帖子编辑页面，支持创建者和管理员编辑已有帖子的标题、分类和内容。编辑模式通过路由 `/forum/posts/:id/edit` 访问。

#### Scenario: 创建者进入帖子编辑页
- **WHEN** 创建者访问 `/forum/posts/{id}/edit`
- **THEN** 页面加载并回填帖子的标题、分类、内容，标题显示"编辑帖子"

#### Scenario: 管理员进入他人帖子编辑页
- **WHEN** 管理员访问他人帖子的 `/forum/posts/{id}/edit`
- **THEN** 页面加载并回填帖子内容，可编辑并提交

#### Scenario: 普通用户访问他人帖子编辑页被拒绝
- **WHEN** 普通用户访问他人帖子的 `/forum/posts/{id}/edit`
- **THEN** 重定向回帖子详情页或列表页，提示无权编辑

#### Scenario: 提交编辑成功
- **WHEN** 用户修改内容后点击"发布"按钮，后端返回 200
- **THEN** 跳转回帖子详情页，显示更新后的内容

### Requirement: 微课编辑功能

系统 SHALL 提供微课编辑页面，支持创建者和管理员编辑已有微课的标题和简介。微课视频文件本身不可替换。编辑模式通过路由 `/videos/:id/edit` 访问。

#### Scenario: 创建者进入微课编辑页
- **WHEN** 创建者访问 `/videos/{id}/edit`
- **THEN** 页面加载并回填微课的标题和简介，不显示视频文件上传区域

#### Scenario: 管理员进入他人微课编辑页
- **WHEN** 管理员访问他人微课的 `/videos/{id}/edit`
- **THEN** 页面加载并回填微课内容，可编辑并提交

#### Scenario: 提交微课编辑成功
- **WHEN** 用户修改标题/简介后点击提交，后端返回 200
- **THEN** 跳转回微课详情页，显示更新后的内容

#### Scenario: 微课编辑不替换视频文件
- **WHEN** 用户在微课编辑页提交修改
- **THEN** 仅 title 和 description 字段更新，视频文件路径和大小不变
