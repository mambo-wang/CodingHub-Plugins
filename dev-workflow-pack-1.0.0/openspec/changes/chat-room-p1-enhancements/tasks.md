# Tasks: Chat Room P1 Enhancements（chat-room-p1）

> 实现顺序遵循依赖：`后端数据模型/迁移 → 后端服务与协议 → 前端类型与状态 → 前端组件 → 测试`。
> 每阶段交付后应满足 `spec.md` 中对应 Requirement 的 Scenario。

## 1. 后端：数据模型与迁移

- [ ] 1.1 `ChatMessage.java`：新增字段 `replyTo`（`@ManyToOne` 自引用 `@JoinColumn(name="reply_to")`，可空）、`edited`（`boolean`，默认 false）、`deletedType`（`String`，可空，值 `ADMIN`/`SELF`）。
- [ ] 1.2 新增 `ChatReaction.java`（`id, messageId, ownerKey, emoji, createdAt`），唯一约束 `(messageId, ownerKey, emoji)`。
- [ ] 1.3 新增 `ChatReactionRepository.java`：`findByMessageId`、`countByMessageIdGroupByEmoji`、`existsByMessageIdAndOwnerKeyAndEmoji`、`deleteByMessageIdAndOwnerKeyAndEmoji`。
- [ ] 1.4 新增 Flyway 迁移 `V10__chat_room_p1.sql`（双库兼容）：`chat_message` 加列 + 建 `chat_reaction` 表 + 唯一索引/外键。

## 2. 后端：DTO 扩展

- [ ] 2.1 `ChatMessageDTO.java`：新增 `replyTo, replyToDisplayName, replyToContentPreview, edited, deletedType, reactions(Map<String,Integer>), myReactions(List<String>)`。
- [ ] 2.2 新增 `ChatReactionDTO.java`、`TypingEventDTO.java`、`ReactionActionPayload.java`、`EditPayload.java`、`RecallPayload.java`。
- [ ] 2.3 `ChatEventDTO.java`：新增 `type=RECALL` 支持与 `deletedType` 字段。

## 3. 后端：服务与协议

- [ ] 3.1 `ChatService.java` 扩展：
  - `toggleReaction(messageId, ownerKey, emoji)` —— 事务内 toggle + 聚合后广播 `/topic/chat.reactions.{roomId}`。
  - `editMessage(id, principal, newContent)` —— 校验作者+窗口(5min)，净化+长度校验，置 `edited=true`，广播 `/topic/chat.edit.{roomId}`。
  - `recallMessage(id, principal)` —— 校验作者+窗口，置 `status=DELETED`+`deletedType=SELF`，广播 `ChatEvent{type:RECALL}`。
  - `handleTyping(principal, isTyping)` —— 维护 `ConcurrentHashMap` 超时调度，广播 `/topic/chat.typing.{roomId}`。
  - `toDTO` 组装 reply 摘要与 reactions 聚合；`getHistory` 附带 reactions。
- [ ] 3.2 `ChatWsController.java`：新增 `@MessageMapping("/chat.react"|"/chat.edit"|"/chat.recall"|"/chat.typing")`，复用 `ChatPrincipal` 鉴权。
- [ ] 3.3 `ChatController.java`：`softDelete` 调用补 `deletedType=ADMIN`（保持既有管理员删除语义）。

## 4. 前端：类型与状态

- [ ] 4.1 `types/chat.ts`：`ChatMessage` 增加 `replyTo, replyToDisplayName, replyToContentPreview, edited, deletedType, reactions, myReactions`；新增 `TypingEvent`、`ReactionEvent`、`EditEvent`、`RecallEvent` 类型并入 `ChatEvent` 联合类型；新增 `ReactionActionPayload`/`EditPayload`/`RecallPayload`。
- [ ] 4.2 `services/chat.ts`：新增 `react/typing/edit/recall` 的 STOMP 发布封装（如需）。
- [ ] 4.3 `stores/chat.ts`：订阅 `/topic/chat.typing.{roomId}`、`/topic/chat.reactions.{roomId}`、`/topic/chat.edit.{roomId}`、`/topic/chat.recall.{roomId}`；新增 `sendTyping/react/edit/recall` 动作；处理 RECALL/EDIT/REACTION 事件更新 `messages`。

## 5. 前端：组件与渲染

- [ ] 5.1 新增 `MessageMarkdown.vue`：marked + DOMPurify 安全渲染 + highlight.js 代码块高亮 + 复制按钮（双主题、遵守 design-system）。
- [ ] 5.2 新增 `MessageReactions.vue`：emoji 计数徽章 + 表情面板，点击调用 `react`，已回应高亮。
- [ ] 5.3 新增 `ReplyQuote.vue`：引用摘要块（昵称 + 截断正文），点击跳转；被删显示占位。
- [ ] 5.4 新增 `TypingIndicator.vue`：三点跳动「正在输入…」动画，`prefers-reduced-motion` 关闭。
- [ ] 5.5 修改 `ChatRoom.vue`：消息气泡接入 Markdown/Reactions/Reply/Actions 菜单（回复/表情/编辑/撤回，按作者与窗口禁用）；编辑内联输入框；撤回后文案区分「已被撤回/已被删除」；typing 提示挂接。

## 6. 测试与校验

- [ ] 6.1 后端单测：`ChatServiceTest` 覆盖 toggleReaction / edit（作者·窗口·净化）/ recall（作者·窗口·区分 ADMIN）/ typing 超时。
- [ ] 6.2 后端集成：`ChatControllerTest` 校验 softDelete 置 `deletedType=ADMIN`；reaction/edit/recall 经 WS 的端到端。
- [ ] 6.3 新增 `ChatReactionRepository` 唯一约束测试。
- [ ] 6.4 运行 `bash scripts/lint-arch.sh` 校验层级依赖。
- [ ] 6.5 前端：手动验证双主题、XSS 不执行、reaction 实时同步、撤回文案区分、响应式三断点。

## 7. 联调与文档

- [ ] 7.1 双库（MySQL/PostgreSQL）迁移脚本执行验证，`ddl-auto: update` 一致。
- [ ] 7.2 更新 `docs/research/chat-room-features.md` 勾选 P1 完成项（如适用）。
- [ ] 7.3 标注 `codinghub-chat-room-handoff.md` 中 P1 用户故事已落盘为 OpenSpec（本变更）。
