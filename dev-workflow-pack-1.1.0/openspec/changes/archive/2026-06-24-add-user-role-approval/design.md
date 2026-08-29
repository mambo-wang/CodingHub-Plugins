## 背景（Context）

CodingHub 当前认证体系中，所有用户权限完全相同——`User` 实体无角色字段，`JwtAuthenticationFilter` 构建 `Authentication` 时 `authorities` 为空列表，`SecurityConfig` 仅区分「已登录」与「未登录」。随着平台内容增长，需要引入角色分层和管理员准入审批机制。

**现状关键约束：**
- `JwtAuthenticationFilter` 已在每次请求时 `userRepository.findById(userId)` 查库（零额外查询开销可利用）
- 密码加密使用 `BCryptPasswordEncoder`
- JWT token claims: `subject=userId`, `email=username`, `type=access|refresh`
- 数据库 `user` 表无 `role`、`status` 列
- 现有 1 条用户数据（id=1, username=wangbao）

## 目标 / 非目标（Goals / Non-Goals）

**目标：**
- 引入三级单角色：`USER` / `ADMIN` / `SUPER_ADMIN`
- 引入账号状态：`ACTIVE` / `PENDING` / `REJECTED` / `DISABLED`
- 注册时可选 `USER`（直接激活）或 `ADMIN`（待审批），`SUPER_ADMIN` 不可注册
- 超级管理员内置账号 `admin / Cloud@1234`，应用启动自动初始化
- 超级管理员可审批管理员注册申请（通过/拒绝）
- 管理员和超级管理员可查看用户列表；超级管理员可封禁/解禁/删除用户
- JWT filter 从数据库读取 role/status 构建权限，role/status 变更立即生效
- 前端新增审批页面和用户列表页面，路由按角色守卫

**非目标：**
- 不做多角色（一个用户只有一个 role）
- 不做细粒度 RBAC（不引入 role 表 + user_role 关联表）
- 不做邮件通知（审批结果用户需主动登录查看）
- 不做密码重置/找回功能
- 不做操作审计日志
- 不做管理员注册时的申请理由字段（当前信息足够）

## 决策（Decisions）

### 决策 1：角色存储——User 表加枚举字段（非独立 role 表）

**选择：** User 表新增 `role` 枚举列

**备选方案：**
- A) User 表加 `role` 枚举字段 ← **选定**
- B) 独立 `role` 表 + `user_role` 关联表（标准 RBAC）

**理由：** 需求是三级单角色，方案 B 是多对多 RBAC 的标准做法，但对单角色场景过度设计。方案 A 查询简单（无需 JOIN），JPA `@Enumerated(EnumType.STRING)` 直接映射，迁移成本低。

### 决策 2：账号状态——User 表加 status 枚举字段

**选择：** User 表新增 `status` 枚举列，值为 `ACTIVE` / `PENDING` / `REJECTED` / `DISABLED`

**理由：** 审批流程需要区分「待审」「已批」「已拒」「已禁用」四种状态。用单独字段比用 role 隐含状态更清晰——role 表示「是什么角色」，status 表示「账号能否使用」，正交关注点分离。

### 决策 3：超级管理员初始化——DataInitializer + application.yml 配置

**选择：** `CommandLineRunner` 实现 `DataInitializer`，启动时检查 `admin` 用户是否存在，不存在则创建。配置放 `application.yml`。

**备选方案：**
- A) DataInitializer (CommandLineRunner) + yml 配置 ← **选定**
- B) SQL 初始化脚本 `init-db.sql` 中 INSERT
- C) 硬编码在 Java 类中

**理由：** 方案 A 幂等（每次启动检查），密码可通过环境变量覆盖（`app.super-admin.password`），不硬编码在源码。方案 B 需要预生成 BCrypt hash 且不幂等（依赖 `INSERT IGNORE`）。方案 C 密码暴露在代码中不安全。

**配置结构：**
```yaml
app:
  super-admin:
    username: admin
    password: Cloud@1234
```

### 决策 4：JWT 策略——token 只放 userId，filter 查库读 role/status

**选择：** JWT claims 保持 `subject=userId` 不变，`JwtAuthenticationFilter` 从查到的 User 读取 `role` 和 `status`，构建带 `GrantedAuthority` 的 `Authentication`。

**备选方案：**
- A) token 只放 userId，filter 查库读 role/status ← **选定**
- B) role 放进 JWT claim

**理由：** 现有 filter 已经在每次请求时 `userRepository.findById(userId)` 查库，方案 A 零额外开销。方案 B 的问题是 role 变更后旧 token 仍带旧 role 直到过期，审批通过后用户无法立即登录（需要等旧 token 过期或重新登录）。方案 A 保证 role/status 变更立即生效。

**实现细节：**
- `JwtAuthenticationFilter` 中 `authorities` 改为 `List.of(new SimpleGrantedAuthority("ROLE_" + user.getRole().name()))`
- 同时校验 `user.getStatus() == ACTIVE`，非 ACTIVE 状态不设置 authentication（等同于未认证）
- `SecurityConfig` 使用 `.hasRole("SUPER_ADMIN")` / `.hasAnyRole("ADMIN", "SUPER_ADMIN")` 鉴权

### 决策 5：注册流程——角色选择决定状态流转

**选择：**
- 注册选 `USER` → `role=USER`, `status=ACTIVE` → 直接返回 token 可登录
- 注册选 `ADMIN` → `role=ADMIN`, `status=PENDING` → 不返回 token，提示「等待审批」
- 注册请求 `role` 字段只接受 `USER` / `ADMIN`，传 `SUPER_ADMIN` 返回 400

**理由：** 普通用户无需审批降低使用门槛；管理员有内容管理权限，需超管把关。`SUPER_ADMIN` 只能由系统内置，不可通过注册产生。

### 决策 6：REJECTED 用户处理——username 占用，不可重新注册

**选择：** REJECTED 状态的 username 仍被占用，同一 username 不可重新注册。超管可在用户列表中删除该记录后才能重新注册。

**理由：** 防止被拒绝的用户反复注册骚扰。超管删除是逃生通道。

### 决策 7：老用户迁移——默认 USER + ACTIVE

**选择：** migration SQL 为现有 user 表所有记录设置 `role='USER'`, `status='ACTIVE'`。新增列时使用 `DEFAULT 'USER'` 和 `DEFAULT 'ACTIVE'`。

**理由：** 现有用户（wangbao）降级为普通用户最安全。如果需要管理员权限，超管可在用户列表中提升。

### 决策 8：API 路径设计——`/api/v1/admin/**` 统一管理接口前缀

**选择：**
```
GET  /api/v1/admin/pending-users      待审批列表（SUPER_ADMIN）
POST /api/v1/admin/approve/{id}       通过审批（SUPER_ADMIN）
POST /api/v1/admin/reject/{id}        拒绝审批（SUPER_ADMIN）
GET  /api/v1/admin/users              用户列表分页（ADMIN, SUPER_ADMIN）
PUT  /api/v1/admin/users/{id}/status  封禁/解禁（SUPER_ADMIN）
DELETE /api/v1/admin/users/{id}       删除用户（SUPER_ADMIN）
```

**理由：** 统一前缀便于 SecurityConfig 配置 `hasRole` 规则，路径语义清晰。

## 风险 / 权衡（Risks / Trade-offs）

- **[超管密码泄露]** → 密码放 `application.yml`，生产环境通过环境变量覆盖 `APP_SUPER_ADMIN_PASSWORD`；代码中不出现明文密码
- **[PENDING 用户无法收到通知]** → 当前项目无邮件系统，用户需主动登录查看状态；登录时返回明确提示「账号等待审批中」
- **[老用户降级为 USER]** → 现有用户 wangbao 从「唯一用户」变为「普通用户」，如需管理权限需超管手动提升；migration 后超管登录即可操作
- **[filter 查库性能]** → 每次请求查一次 user 表，现有架构已是如此，不引入新开销；未来如需优化可加 Redis 缓存（非本次范围）
- **[REJECTED username 占用]** → 被拒绝用户无法用同名重新注册，可能造成困惑；超管可删除记录释放 username
- **[角色提升路径]** → 当前仅超管可审批 ADMIN 注册，无「USER 提升为 ADMIN」的流程；如未来需要，可在用户列表页增加提升操作（非本次范围）

## 迁移计划（Migration Plan）

### 部署步骤

1. **数据库迁移**（新增 migration SQL）：
   ```sql
   ALTER TABLE user ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'USER';
   ALTER TABLE user ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE';
   -- 老用户自动获得 USER + ACTIVE 默认值
   ```
2. **后端部署**：
   - User 实体新增 `role` / `status` 枚举字段
   - `DataInitializer` 启动时创建超管账号
   - `SecurityConfig` / `JwtAuthenticationFilter` 更新
   - 新增 `AdminController` + 审批/用户管理逻辑
3. **前端部署**：
   - 注册页新增角色选择
   - 新增审批页 + 用户列表页
   - 路由守卫支持角色判断
   - 导航栏按角色显示管理入口

### 回滚策略

- 数据库：`ALTER TABLE user DROP COLUMN role; ALTER TABLE user DROP COLUMN status;`
- 后端：回退代码版本（`DataInitializer` 是新增类，删除即可）
- 前端：回退代码版本

## 待定问题（Open Questions）

无——所有关键决策已在探索阶段与用户确认完毕。
