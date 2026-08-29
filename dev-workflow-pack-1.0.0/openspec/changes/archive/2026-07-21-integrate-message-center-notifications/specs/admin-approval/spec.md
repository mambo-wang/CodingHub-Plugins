## ADDED Requirements

### Requirement: 审批结果通知申请人
系统在 `UserService.approveUser` / `rejectUser` 完成审批（更新用户 status）后，MUST 向被审批用户生成 `ADMIN_APPROVED` 或 `ADMIN_REJECTED` 通知。

#### Scenario: 审批通过通知申请人
- **WHEN** 超级管理员通过 userId=U 的注册审批（status 变为 ACTIVE）
- **THEN** 系统调用 `NotificationService.createAdminNotification(U, ADMIN_APPROVED)` 写入通知

#### Scenario: 审批拒绝通知申请人
- **WHEN** 超级管理员拒绝 userId=U 的注册审批（status 变为 REJECTED）
- **THEN** 系统调用 `NotificationService.createAdminNotification(U, ADMIN_REJECTED)` 写入通知

#### Scenario: 通知失败不中断审批
- **WHEN** 审批已完成但通知写入抛出异常
- **THEN** 审批仍返回成功结果，异常被吞掉不向上传播
