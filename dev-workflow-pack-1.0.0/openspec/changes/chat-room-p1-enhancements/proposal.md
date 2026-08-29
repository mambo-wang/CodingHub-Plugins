## Why

聊天室 MVP（阶段 0，已落地）已实现游客/登录双模式、WebSocket 实时收发、在线人数、历史加载、管理员软删除与 XSS 净化。交接文档 `codinghub-chat-room-handoff.md` 的「阶段 1 · P1 增强」定义了六项交互增强，是提升聊天室可用性、互动性与信息表达力的关键能力：

- 正在输入提示（typing indicator）
- 表情回应（reactions）
- 回复引用（quote / reply）
- Markdown / 代码块渲染
- 消息编辑（edit，带 `edited` 标记）
- 消息撤回（recall，复用 `status=DELETED`）

这些能力此前仅有文件级规划，尚未沉淀为可评审、可落地的 OpenSpec 用户故事与技术规范。本变更将其固化为 `chat-room-p1` 能力的 ADDED Requirements，作为 `/opsx:apply` 实现的唯一依据。

## What Changes

### 修改能力

- **chat-room（MVP 能力，已归档）** —— P1 在其实体、服务与协议之上扩展，但作为独立能力 `chat-room-p1` 管理：
  - `chat_message` 表新增 `reply_to`（自关联外键）、`edited`（布尔）、`deleted_type`（ADMIN/SELF 枚举，用于区分管理员删除与作者撤回）。
  - WebSocket 协议新增 `/app/chat.typing`、`/app/chat.react`、`/app/chat.edit`、`/app/chat.recall` 目的地，以及对应广播 topic。
  - `ChatMessageDTO` 扩展字段（引用摘要、edited、deletedType、reactions 聚合）。

### 新增能力

- **chat-room-p1**（本变更核心）：承载上述六项交互增强的用户故事与验收场景。
- 新增 `chat_reaction` 表与 `ChatReaction` 实体，支撑表情回应（含登录用户与游客按 owner_key 区分的唯一约束）。
- 前端新增交互组件：`TypingIndicator`、`MessageReactions`、`MessageMarkdown`、`ReplyQuote`，以及消息气泡上的「编辑 / 撤回 / 回复 / 表情」操作菜单。

### 删除能力

- 无（不删除任何既有能力；MVP 的发送/在线/历史/管理员删除行为保持不变）。

## Impact

- **后端（Java / Spring Boot）**：`model/ChatMessage.java`、`dto/ChatMessageDTO.java`、新增 `model/ChatReaction.java`、新增 `dto/{ChatReactionDTO,TypingEventDTO,ReactionActionPayload}.java`、`service/ChatService.java`、`controller/ChatWsController.java`、`controller/ChatController.java`（软删除补 `deleted_type=ADMIN`）、新增 `repository/ChatReactionRepository.java`、Flyway 迁移脚本（双库 MySQL/PostgreSQL）。
- **前端（Vue 3 / TypeScript）**：`types/chat.ts`、`stores/chat.ts`、`components/chat/ChatRoom.vue`、新增 `components/chat/{TypingIndicator,MessageReactions,MessageMarkdown,ReplyQuote}.vue`；新增依赖 `marked`、`dompurify`、`highlight.js`。
- **数据库**：`chat_message` 加列；新增 `chat_reaction` 表（双库兼容迁移）。
- **实时协议**：新增 4 个 WebSocket 目的地与 4 个广播 topic，前后端需同步；属于跨模块契约变更，风险等级 L2。
- **依赖与构建**：前端新增 3 个 npm 包；`make frontend` 构建需重新解析依赖。
- **无需**：新增独立部署、消息中间件（沿用 MVP 的 SimpleBroker）。

> 详细技术设计见 `design.md`；改动范围与风险评估见 `impact-analysis.md`；双主题 UI 规范见 `design-system.md`；视觉验收见 `ui-preview.html`。
