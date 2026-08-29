## 1. 数据库与迁移

- [x] 1.1 创建 Flyway 迁移脚本 `V8__create_feedback_table.sql`，包含 `feedback_message` 表（id, content, nickname, contact, category, user_id, ip_hash, status, admin_reply, replied_by, replied_at, created_at, updated_at）和索引
- [x] 1.2 在 Makefile `db` target 中添加 `feedback_message` 建表 SQL
- [x] 1.3 执行 `make db` 验证表创建成功

## 2. 后端模型与 DTO

- [x] 2.1 创建 `FeedbackCategory` 枚举（SUGGESTION, BUG_REPORT, PRAISE, OTHER）于 `model/feedback/`
- [x] 2.2 创建 `FeedbackMessage` JPA 实体（@Data, @Builder, @PrePersist/@PreUpdate 时间戳，status 默认 NORMAL）于 `model/feedback/`
- [x] 2.3 创建 `FeedbackDTO` record（id, content, nickname, contact, category, createdAt, adminReply, repliedAt）于 `dto/feedback/`
- [x] 2.4 创建 `FeedbackCreateRequest` record（content, nickname, contact, category + @NotBlank content 校验）于 `dto/feedback/`
- [x] 2.5 创建 `FeedbackReplyRequest` record（adminReply + @NotBlank 校验）于 `dto/feedback/`

## 3. 后端数据访问层

- [x] 3.1 创建 `FeedbackMessageRepository` 接口（extends JpaRepository），包含分页查询方法：findByStatusOrderByCreatedAtDesc、findByCategoryAndStatusOrderByCreatedAtDesc，以及 existsByIdAndStatus 校验方法

## 4. 后端业务逻辑层

- [x] 4.1 创建 `FeedbackService`，实现 submit 方法：解析当前用户（可选），计算 ipHash（匿名时），XSS 清洗 content/nickname/contact，持久化并返回 DTO
- [x] 4.2 实现 list 方法：分页查询，支持 category 筛选，过滤 DELETED 状态，toDTO 转换时不暴露 ipHash/userId
- [x] 4.3 实现 reply 方法：校验留言存在且 status=NORMAL，更新 adminReply/repliedBy/repliedAt
- [x] 4.4 实现 delete 方法：软删除，将 status 设为 DELETED

## 5. 后端 API 与安全配置

- [x] 5.1 创建 `FeedbackController`（@RestController, @RequestMapping("/api/v1/feedback")），实现 4 个端点：GET（分页列表）、POST（提交留言）、PUT /{id}/reply（管理员回复）、DELETE /{id}（管理员删除）
- [x] 5.2 修改 `SecurityConfig`：POST /api/v1/feedback 和 GET /api/v1/feedback 设为 permitAll；PUT /api/v1/feedback/*/reply 和 DELETE /api/v1/feedback/* 设为 hasAnyRole("ADMIN", "SUPER_ADMIN")

## 6. 后端单元测试

- [x] 6.1 创建 `FeedbackServiceTest`（JUnit 5 + Mockito），覆盖 spec 场景：匿名提交（userId=null + ipHash）、已登录提交（userId 关联）、内容为空拒绝、XSS 清洗、分类枚举校验、默认分类
- [x] 6.2 覆盖 list 场景：默认分页、分类筛选、软删除过滤
- [x] 6.3 覆盖 admin 场景：管理员回复成功、非管理员拒绝、留言不存在 404、管理员删除成功
- [x] 6.4 执行 `cd backend && ./gradlew test` 确认全部通过

## 7. 前端类型与 API 服务

- [x] 7.1 创建 `types/feedback.ts`：定义 FeedbackMessage、FeedbackCreateRequest、FeedbackCategory 等 TypeScript 接口
- [x] 7.2 创建 `services/feedback.ts`：独立 axios 实例（baseURL: /api/v1/feedback），实现 getFeedbacks（分页+筛选）、createFeedback、replyFeedback（管理员）、deleteFeedback（管理员）

## 8. 前端组件与页面

- [x] 8.1 创建 `components/feedback/FeedbackForm.vue`：留言提交表单（textarea + 昵称 + 联系方式 + 分类下拉 + 提交按钮），已登录时隐藏昵称输入框，提交后清空表单
- [x] 8.2 创建 `components/feedback/FeedbackCard.vue`：留言卡片（分类徽章 + 昵称 + 时间 + 内容 + 管理员回复区域），管理员可见回复/删除按钮
- [x] 8.3 创建 `pages/feedback/FeedbackPage.vue`：留言板主页面，组合 FeedbackForm + FeedbackCard 列表，分页加载，分类筛选 chips
- [x] 8.4 在 `router/index.ts` 中添加 `/feedback` 路由（公开，lazy import FeedbackPage）

## 9. 验证与收尾

- [x] 9.1 前端构建验证：`vue-tsc --noEmit` 无类型错误，`vite build` 成功
- [x] 9.2 后端编译验证：`./gradlew compileJava` 成功
- [x] 9.3 启动后端+前端，手动验证：匿名提交留言、列表展示、管理员回复、管理员删除、分类筛选
