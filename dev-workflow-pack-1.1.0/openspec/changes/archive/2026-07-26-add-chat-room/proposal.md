## 为什么（Why）

CodingHub 已有论坛、微课、工具广场等**异步**社区能力，但缺少一个"即时、轻量、全站可达"的实时交流入口，用户无法就使用心得、临时问题进行低门槛的即时讨论。阶段 0（MVP）目标是以最小可用方式上线**一个全局公共聊天室**，验证实时通信技术栈与产品需求，为后续多房间/私聊等能力打基础。

## 变更内容（What Changes）

- 新增**全局单一公共聊天室**，基于 WebSocket + STOMP 实时收发消息（`room_id` 默认 `global`，为多房间预留字段）
- 新增 `chat_message` 表持久化消息，进房加载最近 50 条历史
- 支持**登录用户**（真实身份）与**游客**（自定义昵称）发言；鉴权通过握手参数 `ws://…/ws?token=<jwt>`，登录**可选、不强制**
- 消息正文经 `XssSanitizer.sanitize()` 净化并限制 **≤1000 字**
- 发言**频率限制**（登录按 `userId`、游客按 IP，每 2 秒 1 条）
- 管理员可**软删除**消息（`status = DELETED`）
- 实时广播**在线人数**（`/topic/chat.presence`）
- 前端**双入口**：`/chat` 全屏页 + 全站悬浮抽屉，二者复用 `ChatRoom.vue` 与 `chatStore`
- **未读角标**由前端本地维护，不接入 notification 模块
- **双主题**（暗/亮）适配

**范围界定**：阶段 0 仅公共聊天室。私聊、多房间、@提及、图片/文件消息、消息撤回、Redis 多实例广播等为后续阶段（P1），本次不实现——但技术选型保留其扩展点。

## 能力清单（Capabilities）

### 新增能力（New Capabilities）
- `chat-room`: 全站实时公共聊天室——WebSocket/STOMP 实时收发、历史消息加载、游客/登录发言、在线人数广播、发言频率限制、管理员软删除。

### 修改能力（Modified Capabilities）
（无——聊天室为独立新增模块，不改变现有能力的规格级行为。）

## 影响范围（Impact）

- **后端**：新增 `config/WebSocketConfig`、`config/ChatHandshakeInterceptor`、`model/ChatMessage`、`repository/ChatMessageRepository`、`service/ChatService`、`controller/ChatController`（REST）、`controller/ChatWsController`（STOMP `@MessageMapping`）、`config/ChatPresenceListener`；`SecurityConfig` 放行 `/ws/**` 与 `GET /api/v1/chat/messages`；`build.gradle` 新增 `spring-boot-starter-websocket`。
- **数据库**：新增 `chat_message` 表（Hibernate `ddl-auto: update` 自动建表，MySQL / PostgreSQL 双库共存）。
- **前端**：新增 `pages/ChatPage.vue`、`components/chat/ChatRoom.vue`、`components/chat/ChatLauncher.vue`（全站悬浮入口/抽屉）、`stores/chat.ts`、`services/chat.ts`、`types/chat.ts`；`router` 新增 `/chat`；全局布局（`App.vue`）挂载悬浮入口；导航栏增加"聊天室"入口；`package.json` 新增 `@stomp/stompjs`。
- **依赖**：后端 `org.springframework.boot:spring-boot-starter-websocket`；前端 `@stomp/stompjs`。
- **不复用统一互动模块**：聊天为实时推送流，与 `UnifiedComment`（绑定 TOOL/FORUM_POST/VIDEO 目标、REST 持久化）语义不同，故独立建模（详见 design.md 决策）。
