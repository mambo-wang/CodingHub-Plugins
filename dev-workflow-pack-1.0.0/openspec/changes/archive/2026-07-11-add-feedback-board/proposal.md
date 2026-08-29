## 为什么（Why）

CodingHub 目前缺少一个让用户提交意见和建议的轻量渠道。论坛适合深度讨论，但不适合"随手留个建议"这种场景。需要一个类似博客留言板的模块——用户填完就走，管理员能看到并回复，支持匿名提交以降低门槛。

## 变更内容（What Changes）

- **新增** `feedback_message` 数据表，存储留言内容、昵称、联系方式、分类、管理员回复等
- **新增** 后端 REST API（`/api/v1/feedback`）：公开提交 + 分页查询，管理员回复 + 软删除
- **新增** 前端留言板页面（`/feedback`）：提交表单 + 留言列表 + 管理员回复
- **新增** Flyway 迁移脚本 `V8__create_feedback_table.sql`
- **修改** `SecurityConfig`：留言提交和查询接口设为 `permitAll`，回复和删除接口限管理员

## 能力清单（Capabilities）

### 新增能力（New Capabilities）

- `feedback-submit`: 用户提交留言（支持匿名），包含内容、可选昵称、可选联系方式、分类
- `feedback-list`: 分页查询留言列表，公开可见，支持按分类筛选
- `feedback-admin`: 管理员回复留言和软删除留言

### 修改能力（Modified Capabilities）

无。留言板是独立模块，不修改现有能力的需求规格。

## 影响范围（Impact）

- **后端**：新增 `controller/feedback/`、`service/feedback/`、`model/feedback/`、`repository/feedback/`、`dto/feedback/` 子包；修改 `SecurityConfig` 添加权限规则
- **数据库**：新增 `feedback_message` 表（Flyway V8 迁移 + Makefile `db` target）
- **前端**：新增 `types/feedback.ts`、`services/feedback.ts`、`pages/feedback/`、`components/feedback/`；修改 `router/index.ts` 添加路由
- **API**：新增 4 个端点（GET/POST `/api/v1/feedback`，PUT `/api/v1/feedback/{id}/reply`，DELETE `/api/v1/feedback/{id}`）
- **不涉及**：统一交互系统（TargetType 不变）、标签系统、文件上传
