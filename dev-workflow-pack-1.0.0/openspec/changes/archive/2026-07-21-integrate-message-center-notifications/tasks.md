## 1. 后端：评论通知接入（`unified-interactions` + `message-center-notifications`）

- [x] 1.1 在 `UnifiedCommentService` 注入 `NotificationService`（新增 `private final NotificationService notificationService;` 到 `@RequiredArgsConstructor` 字段列表）
- [x] 1.2 在 `addComment` 保存评论并 `incrementCommentCount` 之后，新增私有方法 `resolveTargetOwnerId(TargetType, targetId)`（TOOL→`toolRepository`、FORUM_POST→`forumPostRepository`、VIDEO→`videoRepository` 的所有者 userId），当 `userId != null && !ownerId.equals(userId)` 时用 `try { notificationService.createCommentNotification(ownerId, targetType.name(), targetId, userId, userNickname, sanitizedContent) } catch (Exception e) { log.warn(...) }` 发送 `COMMENT_REPLY` 通知
- [x] 1.3 更新 `UnifiedCommentServiceTest`：新增 `@Mock NotificationService notificationService` 字段，并加入 `new UnifiedCommentService(commentRepository, toolRepository, forumPostRepository, videoRepository, userRepository, notificationService)`；新增用例验证「评论他人资源时 `createCommentNotification` 被调用」「评论自己资源时不调用」
- [x] 1.4 运行 `cd backend && ./gradlew test --tests "*UnifiedCommentServiceTest"` 确认通过

## 2. 后端：点赞通知接入（`unified-interactions` + `message-center-notifications`）

- [x] 2.1 在 `UnifiedLikeService` 注入 `NotificationService`
- [x] 2.2 在 `toggleLike` 中，仅当 `liked == true && userId != null` 时解析 `ownerId = resolveTargetOwnerId(targetType, targetId)`，当 `!ownerId.equals(userId)` 时用 `try { notificationService.createLikeNotification(ownerId, targetType.name(), targetId, userId, <昵称>) } catch (...) { log.warn(...) }` 发送 `LIKE` 通知（`liked==false` 分支不发送）
- [x] 2.3 更新 `UnifiedLikeServiceTest`：新增 `@Mock NotificationService` 并加入构造调用；新增用例验证「点赞他人资源时 `createLikeNotification` 被调用」「取消点赞时不调用」
- [x] 2.4 运行 `cd backend && ./gradlew test --tests "*UnifiedLikeServiceTest"` 确认通过

## 3. 后端：审批通知接入（`admin-approval` + `message-center-notifications`）

- [x] 3.1 在 `UserService` 注入 `NotificationService`（`@RequiredArgsConstructor` 字段；注意 `approveUser` 当前无 `@Transactional`，`createAdminNotification` 自身已 `@Transactional`，无需额外事务注解）
- [x] 3.2 在 `approveUser` 的 `userRepository.save(user)` 之后用 `try { notificationService.createAdminNotification(userId, NotificationType.ADMIN_APPROVED) } catch (...) { log.warn(...) }`；在 `rejectUser` 同样位置发送 `ADMIN_REJECTED`
- [x] 3.3 更新 `UserServiceTest`：新增 `@Mock NotificationService` 并加入 `new UserService(userRepository, passwordEncoder, jwtUtil, uploadConfig, notificationService)`；新增用例验证「审批通过调用 `createAdminNotification(..., ADMIN_APPROVED)`」「审批拒绝调用 `ADMIN_REJECTED`」
- [x] 3.4 运行 `cd backend && ./gradlew test --tests "*UserServiceTest"` 确认通过

## 4. 前端：消息中心图标枚举对齐（`message-center-notifications`）

- [x] 4.1 修改 `NotificationBell.vue` 的 `getNotificationIcon`：将 `case 'COMMENT':` 改为 `case 'COMMENT_REPLY':`，新增 `case 'ADMIN_APPROVED':` / `case 'ADMIN_REJECTED':` 均返回 `User` 图标，移除后端不存在的 `FAVORITE` / `FOLLOW` 分支（保留 `LIKE`）
- [x] 4.2 同步修改 `getNotificationIconColor`：将 `case 'COMMENT':` 改为 `case 'COMMENT_REPLY':`，新增 `ADMIN_APPROVED` / `ADMIN_REJECTED` 颜色（如 `#8b5cf6`），移除 `FAVORITE` / `FOLLOW`
- [x] 4.3 确认 `import { ... User }` 已在 `lucide/vue` 导入列表中（当前已导入 `User`），无需新增依赖

## 5. 全量回归与验收（基于 impact-analysis.md）

- [x] 5.1 运行 `cd backend && ./gradlew test` 确认全部新增与既有测试通过（重点 L1：`UnifiedCommentServiceTest` / `UnifiedLikeServiceTest` / `UserServiceTest` 编译与断言均恢复）
- [x] 5.2 运行 `bash scripts/lint-arch.sh` 确认层级依赖校验 PASS
- [ ] 5.3 手动验证：登录用户 A 评论/点赞用户 B 的资源后，以 B 身份打开消息中心（`GET /api/v1/notifications`）能看到对应通知、未读计数 +1、点击可跳转到目标详情页（浏览器未覆盖，已由 `UnifiedCommentServiceTest`/`UnifiedLikeServiceTest` 单测覆盖，建议人工抽查）
- [x] 5.4 浏览器验证：超级管理员审批通过后，申请人（e2e_qa_77）登录可在消息中心看到「你的注册申请已通过」、`ADMIN_APPROVED` 类型、未读圆点（opencli 实测通过）
- [x] 5.5 浏览器验证：前端通知图标/颜色随类型显示——`ADMIN_APPROVED` 渲染 `User` 图标且 `color: rgb(139,92,246)`（=#8b5cf6 紫），不再走 default 铃铛图标（opencli 实测通过）
