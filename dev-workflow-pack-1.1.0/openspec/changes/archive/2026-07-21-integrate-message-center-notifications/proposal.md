## 为什么（Why）

消息中心（通知中心）的读取、未读计数、标记已读接口（`NotificationController` + `NotificationService`）已全部就绪，但经全量代码审查确认：负责「写入」通知的三个方法 `createCommentNotification` / `createLikeNotification` / `createAdminNotification` 在整个后端**没有任何调用点**，`NotificationService` 也未被任何业务类注入。结果是 `notification` 表永远为空，消息中心恒显示「暂无通知」。

本次变更将通知写入真正接入到评论、点赞与注册审批的业务链路，使消息中心产生实际内容、对终端用户可用。

## 变更内容（What Changes）

- 在统一评论服务 `UnifiedCommentService.addComment` 成功保存后，向目标资源所有者发送 `COMMENT_REPLY` 通知（仅登录用户评论他人内容时；不通知自己、不通知匿名评论）。
- 在统一点赞服务 `UnifiedLikeService.toggleLike` 点赞成功（`liked=true`）后，向目标资源所有者发送 `LIKE` 通知（仅登录用户；不通知自己、不含匿名点赞；取消点赞不通知）。
- 在 `UserService.approveUser` / `rejectUser` 审批完成后，向被审批用户发送 `ADMIN_APPROVED` / `ADMIN_REJECTED` 通知。
- 修复前端 `NotificationBell.vue` 的图标/颜色映射，使其与后端枚举（`LIKE` / `COMMENT_REPLY` / `ADMIN_APPROVED` / `ADMIN_REJECTED`）对齐——当前前端使用 `COMMENT` / `FAVORITE` / `FOLLOW`，与后端不一致，导致所有通知都走 `default` 图标分支。
- 所有通知写入复用既有 `NotificationService` 内部方法，不改 `notification` 表结构、不改现有对外 API 契约，属非破坏性增量。

## 能力清单（Capabilities）

### 新增能力（New Capabilities）
- `message-center-notifications`: 在评论 / 点赞 / 注册审批等业务事件发生时，自动生成并写入「消息中心」通知，使消息中心真正可用。

### 修改能力（Modified Capabilities）
- `unified-interactions`: 点赞 / 评论创建流程新增副作用——成功后为目标资源所有者生成通知。
- `admin-approval`: 注册审批流程新增副作用——审批通过 / 拒绝后向申请人推送通知。

## 影响范围（Impact）

- **后端**
  - `service/notification/NotificationService`：既有 `createCommentNotification` / `createLikeNotification` / `createAdminNotification` 方法本次新增调用方（方法本身不改）。
  - `service/UnifiedCommentService.addComment`：新增注入 `NotificationService`，成功保存后解析目标所有者并发送评论通知。
  - `service/UnifiedLikeService.toggleLike`：新增注入 `NotificationService`，点赞成功后解析目标所有者并发送点赞通知。
  - `service/UserService.approveUser` / `rejectUser`：新增注入 `NotificationService`，审批后发送管理员通知。
  - 三个服务均已有 `ToolRepository` / `ForumPostRepository` / `VideoRepository` / `UserRepository`（评论/点赞服务）或 `UserRepository`（用户服务），用于解析目标所有者，无需新增仓库依赖。
- **前端**
  - `components/common/NotificationBell.vue`：修正 `getNotificationIcon` / `getNotificationIconColor` 的 type 分支，对齐后端枚举（新增 `COMMENT_REPLY` / `ADMIN_APPROVED` / `ADMIN_REJECTED`，移除后端不存在的 `FAVORITE` / `FOLLOW`）。
- **测试**
  - `UnifiedCommentServiceTest` / `UnifiedLikeServiceTest` / `UserServiceTest`：因服务新增 `NotificationService` 构造参数，需同步加入 `@Mock NotificationService` 并补到构造调用，否则编译失败。
- **约束**
  - 继承既有 XSS 防护、JWT 鉴权、软删除与单向依赖规则；通知写入为最佳努力（best-effort）副作用，失败不应中断主流程。
