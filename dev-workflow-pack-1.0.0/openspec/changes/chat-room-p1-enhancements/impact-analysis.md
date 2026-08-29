# Impact Analysis

> 基于 `design.md` 中的文件/类/测试清单执行静态扫描（本机 CodeGraph MCP 未连接，采用 grep + 文件结构分析替代），确认技术设计的实际影响范围。
>
> **位置**：在 `design` 之后、`tasks` 之前生成。
>
> **触发条件**：`design.md` 涉及修改现有代码（chat_message 实体、ChatService、ChatWsController、ChatRoom.vue 等），故必选。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | 11 | `backend/.../model/ChatReaction.java`、`backend/.../dto/ChatReactionDTO.java`、`backend/.../dto/TypingEventDTO.java`、`backend/.../dto/ReactionActionPayload.java`、`backend/.../dto/EditPayload.java`、`backend/.../dto/RecallPayload.java`、`backend/.../repository/ChatReactionRepository.java`、`backend/.../resources/db/migration/V10__chat_room_p1.sql`、`frontend/src/components/chat/TypingIndicator.vue`、`frontend/src/components/chat/MessageReactions.vue`、`frontend/src/components/chat/MessageMarkdown.vue`、`frontend/src/components/chat/ReplyQuote.vue` |
| 修改 | 9 | `backend/.../model/ChatMessage.java`、`backend/.../dto/ChatMessageDTO.java`、`backend/.../dto/ChatEventDTO.java`、`backend/.../service/ChatService.java`、`backend/.../controller/ChatWsController.java`、`backend/.../controller/ChatController.java`、`frontend/src/types/chat.ts`、`frontend/src/stores/chat.ts`、`frontend/src/components/chat/ChatRoom.vue` |
| 删除 | 0 | 无 |

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `ChatWsController.handleMessage` → `ChatService.handleMessage` | `controller/ChatWsController.java:32` | L2（协议扩展） |
| `ChatController.deleteMessage` → `ChatService.softDelete` | `controller/ChatController.java:35` | L2（补 deletedType） |
| 新增 `ChatWsController.handleReact/handleTyping/handleEdit/handleRecall` → 对应 `ChatService` 方法 | 新增映射 | L2 |
| `ChatRoom.vue` → `useChatStore` 订阅/发送 | `components/chat/ChatRoom.vue` | L2（前端契约） |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

- `ChatHandshakeInterceptor` 注入 `ChatPrincipal`（userId/ipHash）→ P1 的 edit/recall/reaction 均依赖该 principal 鉴权。
- `ChatPresenceListener` 维护在线人数，与 typing 独立，不受影响。

### 2.3 反向调用图（被谁调用）

```
ChatService
  ├── ChatWsController (@MessageMapping 入口)
  ├── ChatController (REST 历史/删除)
  └── ChatServiceTest (单元覆盖)
        └── ChatControllerTest (集成)

ChatMessage (实体)
  ├── ChatMessageRepository (findRecentByRoomId / softDeleteById)
  ├── ChatReactionRepository (新增, 依 message_id)
  └── ChatMessageDTO.toDTO (扩展字段)
        └── ChatRoom.vue / stores/chat.ts 消费
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `ChatMessageRepository` | 数据访问层 | L2（需新增 replyTo 关联查询与 reaction 聚合查询） |
| `ChatPrincipal` / `ChatHandshakeInterceptor` | 鉴权 | L0（只读复用） |
| `XssSanitizer` | 工具 | L0（复用） |
| `SimpMessagingTemplate` | 消息广播 | L0（复用） |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| `frontend/components/chat/ChatRoom.vue` | DTO 结构变化（replyTo/edited/deletedType/reactions）需同步渲染 |
| `frontend/stores/chat.ts` | 新增 4 个 topic 订阅 + 发送方法 |
| `frontend/types/chat.ts` | `ChatMessage` 接口新增字段 |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| `backend/.../service/ChatServiceTest.java` | 单元 | 需更新 | 新增 reaction/edit/recall/typing 用例 |
| `backend/.../controller/ChatControllerTest.java` | 集成 | 需更新 | 校验 softDelete 现置 `deletedType=ADMIN` |
| `backend/.../config/ChatHandshakeInterceptorTest.java` | 单元 | 仍有效 | 无需改动 |
| `backend/.../config/ChatPresenceListenerTest.java` | 单元 | 仍有效 | 无需改动 |
| 新增 `ChatReactionRepository` 测试 | 单元 | 新增 | toggle 唯一约束验证 |

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L0** | 纯新增 `chat_reaction` 表与实体 | 无 |
| **L1** | `ChatMessageDTO` 增加字段（前端契约变更） | 全量回归 + 前端同步 |
| **L2** | DB schema 变更（`chat_message` 加列）+ WebSocket 协议新增目的地 + 业务规则（编辑/撤回窗口、游客校验） | 完整测试套件 + 双库迁移验证 + 灰度发布 |

**本次改动风险等级**: **L2**（涉及数据库 schema 变更、实时协议契约变更、跨模块业务规则）

---

## 6. 层级依赖校验 (Layer Dependency Check)

> 校验后端是否仍满足 `controller → service → repository → model` 单向依赖。

```bash
bash scripts/lint-arch.sh
```

**结果**: 待执行（apply 阶段运行；新增 `ChatReactionRepository` 仅被 `ChatService` 依赖，仍满足单向依赖）

---

## 7. 回归测试建议 (Regression Suggestions)

- [ ] `ChatServiceTest.toggleReaction_TogglesCorrectly` —— 覆盖添加/取消与聚合，位于 `backend/.../service/ChatServiceTest.java`
- [ ] `ChatServiceTest.recall_OnlyAuthorWithinWindow` —— 覆盖作者/非作者/超窗，位于同文件
- [ ] `ChatServiceTest.edit_OnlyAuthorWithinWindow` —— 覆盖编辑窗口与净化，位于同文件
- [ ] `ChatControllerTest.softDelete_SetsDeletedTypeAdmin` —— 覆盖 `deletedType=ADMIN`，位于 `backend/.../controller/ChatControllerTest.java`
- [ ] 前端：reaction toggle 后计数刷新；markdown 渲染不执行脚本；撤回文案区分。

---

## 8. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方
- [x] 已列出上游/下游依赖
- [x] 已评估风险等级（L2）
- [ ] `scripts/lint-arch.sh` 校验通过（apply 阶段执行）
- [x] 已列出回归测试清单
- [x] （L2 风险）已通知相关模块负责人（chat-room 维护者）

---

**生成工具**: 静态 grep + 文件结构分析（替代 CodeGraph MCP，MCP 未连接）
**生成时间**: 2026-07-26
**基础**: openspec/changes/chat-room-p1-enhancements/proposal.md
