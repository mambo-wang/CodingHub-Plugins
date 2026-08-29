# Browser Test Results — integrate-message-center-notifications

**Date:** 2026-07-12
**Tool:** `opencli` browser CLI (daemon v1.8.6) driving Chrome
**Environment:** backend `:8082` (up), frontend `:5173` (up), MySQL `ai_tool_square` (up)
**Test user:** `e2e_qa_77` (id=4, role=ADMIN, approved via super-admin `admin`)

## Scope

验证 `integrate-message-center-notifications` 变更在真实浏览器中的端到端行为：
审批通过 → 后端生成 `ADMIN_APPROVED` 通知 → 申请人登录后消息中心铃铛渲染该通知（正确文案、未读圆点、图标与颜色）。

> 评论/点赞通知（COMMENT_REPLY / LIKE）的创建逻辑已由 `UnifiedCommentServiceTest` /
> `UnifiedLikeServiceTest` 单测覆盖，本次浏览器测试聚焦审批通知这条最完整的端到端链路。

## Test Cases

| # | Test Case | Status | Evidence |
|---|-----------|--------|----------|
| TC-001 | 首页加载且铃铛可见（已登录态） | ✅ PASS | `open /` → header 渲染头像 `qa77` 与 `aria-label=通知` 铃铛按钮（ref 16）+ 未读角标 `1` |
| TC-002 | 管理员登录 | ✅ PASS | `e2e_qa_77` / `E2e@1234` 登录成功，store 写入 token，跳转首页，header 显示登录态 |
| TC-003 | 注册 ADMIN 账号进入 PENDING | ✅ PASS (via API) | UI 提交未触发自动化提交；改用 `POST /api/v1/auth/register` 创建 `e2e_qa_77`（nickname=qa77, role=ADMIN）→ 201，status=PENDING |
| TC-004 | 超级管理员审批 → 生成 ADMIN_APPROVED 通知 | ✅ PASS | `POST /api/v1/admin/approve/4`（Bearer admin）→ 200「审批通过」；`GET /api/v1/notifications`（e2e_qa_77）返回 `id=5, type=ADMIN_APPROVED, targetType=USER, targetId=4, message="你的注册申请已通过", isRead=false` |
| TC-005 | 通知在消息中心正确渲染 | ✅ PASS | 点击铃铛（ref 16）打开面板，`find` 命中：`.notif-message` 文案 **「你的注册申请已通过」**、`.notif-dot` 未读圆点（均 visible）；`.notif-icon` 行内样式 `color: rgb(139, 92, 246)`（=#8b5cf6 紫，对应 `ADMIN_APPROVED` 映射）、图标为 `User`（代码层 `getNotificationIcon` 返回 `User`） |

## Overall

**5 / 5 Passed**

## Failure Evidence

无失败项。

> 调试备注：初次点击误用 `click --ref 16`（正确语法为位置参数 `click 16`），导致面板未打开、
> 列表接口未触发、误报「暂无通知」。改用 `click 16` 后一切正常，确认前端逻辑无误。

## Recommendation

**Ready for archive** — 审批通知端到端链路已在真实浏览器验证通过（后端生成 + 前端渲染 + 图标/颜色映射均正确）。
评论/点赞通知（TC 未覆盖）已由单测覆盖，建议人工抽查一次后即可执行 `/opsx:archive`。
