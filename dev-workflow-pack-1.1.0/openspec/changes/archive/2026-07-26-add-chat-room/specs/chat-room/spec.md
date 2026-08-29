## ADDED Requirements

### Requirement: 实时消息收发
系统 SHALL 提供一个全局公共聊天室，用户通过 WebSocket + STOMP 实时收发消息。所有连接客户端订阅 `/topic/chat.{roomId}`（阶段 0 `roomId` 固定为 `global`），发送消息到 `/app/chat.send`，服务端持久化后将消息广播给全部订阅者。

#### Scenario: 登录用户发送消息并被广播
- **WHEN** 已登录用户在已建立 STOMP 连接后向 `/app/chat.send` 发送 `{roomId:"global", content:"你好"}`
- **THEN** 服务端以其真实身份（用户名、头像）持久化一条 `chat_message`，并向 `/topic/chat.global` 广播该消息，所有订阅客户端实时收到

#### Scenario: 消息实时到达其他在线用户
- **WHEN** 一条消息被成功广播到 `/topic/chat.global`
- **THEN** 所有当前订阅该主题的客户端（含全屏页与悬浮抽屉）无需刷新即可看到新消息

### Requirement: 游客与登录用户身份
系统 SHALL 允许游客（未登录）与登录用户同时使用聊天室。握手通过查询参数 `ws://…/ws?token=<jwt>` 传递 JWT，登录为可选。登录用户显示真实身份且忽略客户端传入的昵称；游客必须提供自定义昵称，昵称经净化后作为 `display_name`。

#### Scenario: 有效 token 识别为登录用户
- **WHEN** 客户端以 `?token=<有效JWT>` 建立握手
- **THEN** 服务端解析出 `userId` 并构造登录身份，其消息的 `display_name`/`avatar_url` 取自 `User` 记录，`user_id` 非空

#### Scenario: 无 token 或无效 token 识别为游客
- **WHEN** 客户端不带 token 或携带无效/过期 token 建立握手
- **THEN** 服务端不拒绝连接，将其视为游客，`user_id` 为空，`display_name` 取自消息载荷中的昵称

#### Scenario: 游客未提供昵称时拒绝发言
- **WHEN** 游客发送消息但载荷中 `displayName` 为空
- **THEN** 服务端不入库、不广播，并向发送者回送错误提示

### Requirement: 消息内容安全与长度限制
系统 SHALL 对所有消息正文与游客昵称执行 `XssSanitizer.sanitize()` 净化，并限制正文长度不超过 1000 字符。

#### Scenario: 正文超长被拒绝
- **WHEN** 用户发送长度超过 1000 字符的正文
- **THEN** 服务端不入库、不广播，并向发送者回送"内容过长"错误

#### Scenario: 含脚本的内容被净化
- **WHEN** 用户发送包含 HTML/脚本标签的正文或昵称
- **THEN** 服务端存储与广播的内容为经 `XssSanitizer.sanitize()` 净化后的安全文本

#### Scenario: 空白正文被拒绝
- **WHEN** 用户发送去除首尾空白后为空的正文
- **THEN** 服务端不入库、不广播

### Requirement: 历史消息加载
系统 SHALL 提供 REST 接口 `GET /api/v1/chat/messages?roomId=global&limit=50` 返回指定房间最近 50 条 `status=ACTIVE` 的消息（按时间升序），该接口公开可访问，供进入聊天室时加载历史。

#### Scenario: 进入聊天室加载最近历史
- **WHEN** 用户（含游客）打开 `/chat` 页或悬浮抽屉
- **THEN** 前端调用 `GET /api/v1/chat/messages?roomId=global&limit=50`，展示最近 50 条 ACTIVE 消息，按时间正序排列

#### Scenario: 已删除消息不出现在历史中
- **WHEN** 某条消息 `status=DELETED`
- **THEN** 历史接口返回结果中不包含该消息

### Requirement: 发言频率限制
系统 SHALL 对发言进行频率限制，登录用户按 `userId`、游客按 IP 计算，每 2 秒最多发送 1 条消息。命中限制的消息不入库、不广播。

#### Scenario: 2 秒内重复发送被限流
- **WHEN** 同一用户/游客在上一条消息发送后 2 秒内再次发送
- **THEN** 服务端拒绝该消息（不入库、不广播），并向发送者回送限流错误

#### Scenario: 间隔足够后正常发送
- **WHEN** 同一用户/游客距上次发送已超过 2 秒
- **THEN** 该消息被正常处理并广播

### Requirement: 管理员软删除消息
系统 SHALL 允许管理员（ADMIN/SUPER_ADMIN）通过 `DELETE /api/v1/chat/messages/{id}` 软删除消息（置 `status=DELETED`），并向 `/topic/chat.{roomId}` 广播删除事件，客户端据此移除对应消息。

#### Scenario: 管理员删除消息并实时同步
- **WHEN** 管理员对某条消息调用 `DELETE /api/v1/chat/messages/{id}`
- **THEN** 该消息 `status` 置为 `DELETED`，服务端广播 `{type:"DELETE", id}`，所有在线客户端移除该消息

#### Scenario: 非管理员无权删除
- **WHEN** 普通用户或游客尝试调用删除接口
- **THEN** 服务端返回 403 拒绝，消息状态不变

### Requirement: 在线人数广播
系统 SHALL 统计当前聊天室在线连接数，并在连接建立/断开时向 `/topic/chat.presence` 广播最新在线人数。

#### Scenario: 用户连接后在线数增加并广播
- **WHEN** 一个新客户端成功建立 STOMP 连接
- **THEN** 服务端在线计数加一，并向 `/topic/chat.presence` 广播 `{online: N}`

#### Scenario: 用户断开后在线数减少并广播
- **WHEN** 一个客户端断开连接
- **THEN** 服务端在线计数减一，并向 `/topic/chat.presence` 广播更新后的人数

### Requirement: 前端双入口与状态复用
系统 SHALL 提供两个进入聊天室的入口：`/chat` 全屏页与全站右下角悬浮抽屉；两者复用同一 `ChatRoom.vue` 组件与 `chatStore`，保证全站单一 WebSocket 连接与一致的消息/在线状态。抽屉关闭时到达的消息计入本地未读角标，打开时清零。

#### Scenario: 两入口共享同一连接与消息
- **WHEN** 用户先在悬浮抽屉中查看消息，再打开 `/chat` 全屏页
- **THEN** 全屏页展示与抽屉相同的消息列表与在线人数，不重复建立连接

#### Scenario: 抽屉关闭时累计未读，打开时清零
- **WHEN** 悬浮抽屉处于关闭状态且有新消息到达
- **THEN** 悬浮入口显示未读数角标；当用户打开抽屉后，未读数清零

### Requirement: 断线自动重连
系统 SHALL 在 WebSocket 连接意外断开时自动重连，并启用 STOMP 心跳保持连接活性；重连成功后重新订阅并可重新加载历史。

#### Scenario: 连接中断后自动恢复
- **WHEN** 客户端与服务端的 WebSocket 连接意外断开
- **THEN** 客户端自动尝试重连，恢复后重新订阅 `/topic/chat.global` 并可继续收发消息

### Requirement: 双主题适配
聊天室的所有 UI（全屏页、悬浮抽屉、消息气泡、输入框）SHALL 适配暗色（Cyberpunk Dark）与亮色（Glassmorphism Light）双主题，使用全局设计系统 CSS 变量。

#### Scenario: 切换主题后聊天室样式一致
- **WHEN** 用户切换全站主题
- **THEN** 聊天室各组件的背景、文字、边框、焦点环随主题正确切换，无硬编码颜色导致的视觉断裂
