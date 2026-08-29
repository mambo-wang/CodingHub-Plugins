# Chat Room P1 Enhancements 规范（chat-room-p1）

> 本文件定义「阶段 1 · P1 增强」六项交互能力的用户故事与验收场景。
> 这些能力构建于已归档的 `chat-room`（MVP）能力之上，作为独立能力 `chat-room-p1` 管理。
> 基础协议 / 数据模型约束见 `proposal.md` 与 `design.md`。

## ADDED Requirements

### Requirement: 正在输入提示（Typing Indicator）

系统 SHALL 在用户于聊天输入框输入时，向同房间其他在线用户展示「正在输入…」状态。客户端对 typing 事件做节流（≥1s），服务端在收到 typing 后于超时窗口（默认 4s）无新事件时自动广播清除该状态。该状态不持久化。

#### Scenario: 开始输入广播

- **WHEN** 用户停止输入超过节流间隔（≥1s）且输入框非空
- **THEN** 客户端发送 typing 事件（`/app/chat.typing`，携带 `roomId`、`userId`/`displayName`）
- **AND** 服务端向 `/topic/chat.typing.{roomId}` 广播 `TypingEvent{userId, displayName, isTyping:true}`
- **AND** 同房间其他客户端在消息列表顶部/输入框上方展示「{displayName} 正在输入…」

#### Scenario: 超时自动清除

- **WHEN** 某用户停止输入且 4s 内未收到其新的 typing 事件
- **THEN** 服务端向房间广播 `TypingEvent{userId, isTyping:false}`
- **AND** 前端清除该用户的「正在输入…」提示

#### Scenario: 仅同房可见

- **WHEN** 用户在房间 A 输入
- **THEN** 仅订阅 `/topic/chat.typing.A` 的客户端收到提示
- **AND** 房间 B 的客户端不受任何影响

#### Scenario: 发送或失焦即清除

- **WHEN** 用户发送消息或将焦点移出输入框
- **THEN** 客户端立即发送 `isTyping:false`
- **AND** 前端本地即时清除自身提示

---

### Requirement: 表情回应（Reactions）

系统 SHALL 允许用户对单条消息添加 emoji 表情回应。回应存储于新增的 `chat_reaction` 表（含 `message_id`、`owner_key`、`emoji`、`created_at`）。对同一 emoji 再次点击 SHALL 切换为取消（toggle）。服务端实时广播聚合计数，历史接口返回消息时附带该消息的 reaction 汇总与「当前用户是否已回应」。

#### Scenario: 登录用户添加并 toggle 取消

- **WHEN** 登录用户对某消息点击 emoji `👍`
- **IF** 该用户此前未回应此 emoji
- **THEN** 新增 `chat_reaction` 记录（`owner_key = 用户ID`）并向房间广播聚合 +1
- **IF** 该用户此前已回应此 emoji
- **THEN** 删除该记录并向房间广播聚合 -1（计数归零则该 emoji 不再展示）

#### Scenario: 游客按 owner_key 计数

- **WHEN** 游客（无 userId）对某消息点击 emoji
- **THEN** 以 `owner_key = ip_hash` 写入 `chat_reaction`（唯一约束 `message_id + owner_key + emoji`）
- **AND** 该游客的回应计入聚合计数，刷新后依 `ip_hash` 恢复「已回应」高亮

#### Scenario: 历史加载返回反应

- **WHEN** 客户端调用 `GET /api/v1/chat/messages?roomId=...`
- **THEN** 每条消息附带 `reactions: {emoji: count}` 与 `myReactions: string[]`（依当前登录用户或 `ip_hash` 计算）
- **AND** 前端渲染 emoji 计数徽章，已回应的 emoji 高亮

#### Scenario: 实时同步

- **WHEN** 任意用户新增/取消某消息的回应
- **THEN** 服务端向 `/topic/chat.reactions.{roomId}` 广播该消息最新聚合
- **AND** 所有在线客户端即时刷新该消息的计数与高亮，无需刷新历史

---

### Requirement: 回复引用（Quote / Reply）

系统 SHALL 允许用户在发送消息时引用（回复）一条已有消息。`chat_message` 新增可空自关联外键 `reply_to`；被引用消息在发送端展示摘要（昵称 + 截断正文），点击可跳转至原消息。

#### Scenario: 发起回复

- **WHEN** 用户点击某消息的「回复」操作
- **THEN** 输入框进入引用态并展示被引摘要
- **AND** 发送时 payload 携带 `replyTo`，新消息 `reply_to = 被引消息 id`
- **AND** 广播与历史均包含 `replyTo`、`replyToDisplayName`、`replyToContentPreview`（正文截断至 80 字）

#### Scenario: 引用已删除消息

- **WHEN** 被引用消息已被删除或撤回
- **THEN** 前端渲染引用占位「原消息已删除/已撤回」
- **AND** 引用块仍可点击但跳转目标不存在时不报错

#### Scenario: 实时与历史一致

- **WHEN** 带引用的消息被广播或被历史接口返回
- **THEN** 其 `replyTo` 与引用摘要结构与发送时一致
- **AND** 刷新后历史接口返回相同引用数据

---

### Requirement: Markdown 与代码块渲染

系统 SHALL 在前端对消息正文进行 Markdown 渲染（支持加粗、斜体、行内代码、代码块、链接），并在渲染前对内容进行安全净化以阻断 XSS；代码块提供语法高亮与一键复制。

#### Scenario: 代码块渲染

- **WHEN** 用户发送被 ```` ```lang ```` 包裹的代码块
- **THEN** 前端渲染为带语言标识与语法高亮的代码块
- **AND** 提供「复制」按钮，点击后复制原始代码

#### Scenario: XSS 净化

- **WHEN** 消息正文包含 `<script>`、`onerror=` 等脚本载荷
- **THEN** 服务端 `XssSanitizer` 入库前净化，前端安全 Markdown 解析禁止原始 HTML 注入（DOMPurify 兜底）
- **AND** 脚本不会被执行，用户仅看到经净化的纯文本/结构化内容

#### Scenario: 链接安全打开

- **WHEN** 消息包含 Markdown 链接
- **THEN** 渲染的 `<a>` 默认 `rel="noopener noreferrer"` 并以新标签页打开
- **AND** 避免反向 Tabnabbing

---

### Requirement: 消息编辑（Edit）

系统 SHALL 允许消息作者在发送后限定时间窗（默认 5 分钟）内编辑自己的消息。编辑后内容经净化与长度校验，并打上 `edited` 标记；编辑事件通过 `/topic/chat.edit.{roomId}` 广播，前端展示「（已编辑）」。

#### Scenario: 作者在窗口内编辑

- **WHEN** 作者在自己消息的编辑窗口内点击「编辑」并提交新内容
- **THEN** 客户端发送 `/app/chat.edit`（携带 `id`、新 `content`）
- **AND** 服务端校验作者本人且 `now - createdAt <= 5min`，重新净化后更新 `content`、置 `edited=true`
- **AND** 向房间广播更新后的 `ChatMessageDTO`，前端原地刷新并展示「（已编辑）」

#### Scenario: 非作者或超窗被拒

- **WHEN** 非作者或已超出编辑窗口请求编辑
- **THEN** 服务端返回业务错误（`ChatEvent{type:ERROR}`）
- **AND** 前端提示「无法编辑该消息」且不在本地修改

#### Scenario: 历史加载显示标记

- **WHEN** 历史接口返回 `edited=true` 的消息
- **THEN** 前端展示「（已编辑）」标识

---

### Requirement: 消息撤回（Recall）

系统 SHALL 允许消息作者在限定窗口内撤回（删除）自己的消息。撤回复用 `status=DELETED`，但新增 `deleted_type=SELF` 以区别于管理员删除（`deleted_type=ADMIN`）；广播后前端展示「该消息已被撤回」。

#### Scenario: 作者撤回

- **WHEN** 作者在自己消息的窗口内点击「撤回」
- **THEN** 客户端发送 `/app/chat.recall`（携带 `id`）
- **AND** 服务端校验作者且未超窗，置 `status=DELETED`、`deleted_type=SELF`
- **AND** 向房间广播 `ChatEvent{type:RECALL, id}`，前端将消息体替换为「该消息已被撤回」，并保留引用占位

#### Scenario: 非作者或超窗被拒

- **WHEN** 非作者或已超出撤回窗口请求撤回
- **THEN** 服务端返回业务错误
- **AND** 前端提示「无法撤回该消息」

#### Scenario: 与管理员删除区分

- **WHEN** 管理员通过既有 `DELETE /api/v1/chat/messages/{id}` 删除消息
- **THEN** 服务端置 `deleted_type=ADMIN`，广播 `ChatEvent{type:DELETE}`
- **AND** 前端对 `SELF` 显示「该消息已被撤回」、对 `ADMIN` 显示「该消息已被删除」，文案与权限语义不同
- **AND** 历史中 `deleted_type=null` 的存量 `DELETED` 行按 `ADMIN` 解释（向后兼容）
