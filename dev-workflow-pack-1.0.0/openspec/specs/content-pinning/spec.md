# Content Pinning

## ADDED Requirements

### Requirement: 内容实体包含 pinned 字段

Tool、ForumPost、Video 三个实体 SHALL 各新增一个 `pinned` 布尔字段，默认值为 `false`。

#### Scenario: 新建内容项默认 unpinned

- WHEN: 创建一条新的 Tool、ForumPost 或 Video 记录
- THEN: 该记录的 `pinned` 字段值为 `false`

#### Scenario: 数据库迁移添加 pinned 列

- WHEN: V3 迁移脚本执行
- THEN: tool、forum_post、video 三张表各新增 `pinned` BOOLEAN NOT NULL DEFAULT FALSE 列

### Requirement: 管理员可置顶内容

拥有 ADMIN 或 SUPER_ADMIN 角色的用户 SHALL 能够通过 `POST /{id}/pin` 端点将内容项置顶。

#### Scenario: 管理员置顶工具

- WHEN: ADMIN 用户请求 `POST /api/v1/tools/{id}/pin`
- THEN: 该工具的 pinned 字段更新为 true，接口返回成功

#### Scenario: 管理员置顶帖子

- WHEN: SUPER_ADMIN 用户请求 `POST /api/forum/posts/{id}/pin`
- THEN: 该帖子的 pinned 字段更新为 true，接口返回成功

#### Scenario: 管理员置顶微课

- WHEN: ADMIN 用户请求 `POST /api/v1/videos/{id}/pin`
- THEN: 该微课的 pinned 字段更新为 true，接口返回成功

### Requirement: 管理员可取消置顶

拥有 ADMIN 或 SUPER_ADMIN 角色的用户 SHALL 能够通过 `DELETE /{id}/pin` 端点取消内容项置顶。

#### Scenario: 管理员取消工具置顶

- WHEN: ADMIN 用户请求 `DELETE /api/v1/tools/{id}/pin`
- THEN: 该工具的 pinned 字段更新为 false，接口返回成功

#### Scenario: 管理员取消帖子置顶

- WHEN: SUPER_ADMIN 用户请求 `DELETE /api/forum/posts/{id}/pin`
- THEN: 该帖子的 pinned 字段更新为 false，接口返回成功

#### Scenario: 管理员取消微课置顶

- WHEN: ADMIN 用户请求 `DELETE /api/v1/videos/{id}/pin`
- THEN: 该微课的 pinned 字段更新为 false，接口返回成功

### Requirement: 置顶端点需要 ADMIN 或 SUPER_ADMIN 权限

Pin/Unpin 端点 SHALL 仅对具有 ADMIN 或 SUPER_ADMIN 角色的用户开放，普通 USER 角色 MUST NOT 能访问。

#### Scenario: 普通用户尝试置顶被拒绝

- WHEN: USER 角色用户请求 `POST /api/v1/tools/{id}/pin`
- THEN: 接口返回 403 Forbidden，pinned 字段不变

#### Scenario: 未登录用户尝试置顶被拒绝

- WHEN: 未携带 JWT Token 请求 `DELETE /api/forum/posts/{id}/pin`
- THEN: 接口返回 401 Unauthorized

### Requirement: 置顶项显示 ArrowUp 图标

前端列表中 pinned=true 的内容项 SHALL 在卡片上显示 ArrowUp 图标（置顶图标），以视觉方式标识该内容已被管理员置顶。

#### Scenario: 置顶工具卡片显示 ArrowUp 图标

- WHEN: 工具列表中某工具的 pinned=true
- THEN: 该工具卡片上显示 ArrowUp 图标

#### Scenario: 非置顶项不显示 ArrowUp 图标

- WHEN: 列表中某内容项的 pinned=false
- THEN: 该卡片上不显示 ArrowUp 图标

### Requirement: 置顶按钮仅管理员可见

列表页卡片上的置顶/取消置顶操作按钮 SHALL 仅对具有管理员权限的用户可见。

#### Scenario: 管理员在卡片上看到置顶按钮

- WHEN: 已登录的 ADMIN 或 SUPER_ADMIN 用户浏览列表页
- THEN: 每张卡片上显示置顶/取消置顶操作按钮

#### Scenario: 普通用户在卡片上看不到置顶按钮

- WHEN: USER 角色用户或未登录用户浏览列表页
- THEN: 卡片上不显示置顶/取消置顶操作按钮

### Requirement: 前端置顶操作后刷新列表

前端 SHALL 在调用 pin/unpin API 成功后自动刷新当前列表，使排序变化立即反映。

#### Scenario: 置顶成功后列表刷新

- WHEN: 管理员点击置顶按钮且 API 请求成功
- THEN: 前端重新请求列表接口，刷新展示内容，被置顶项移至顶部（热度排序下）

#### Scenario: 取消置顶成功后列表刷新

- WHEN: 管理员点击取消置顶按钮且 API 请求成功
- THEN: 前端重新请求列表接口，刷新展示内容，被取消置顶项回到正常排序位置
