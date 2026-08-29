## 1. 数据模型与枚举

- [x] 1.1 创建 `model/Role.java` 枚举（USER / ADMIN / SUPER_ADMIN）
- [x] 1.2 创建 `model/AccountStatus.java` 枚举（ACTIVE / PENDING / REJECTED / DISABLED）
- [x] 1.3 修改 `model/User.java`，新增 `role` 和 `status` 字段，使用 `@Enumerated(EnumType.STRING)`，`@Builder.Default` 设默认值 USER / ACTIVE
- [x] 1.4 创建数据库迁移脚本 `scripts/migrations/add-user-role-status.sql`：ALTER TABLE user ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'USER', ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
- [x] 1.5 更新 `scripts/init-db.sql` 中 user 表定义，包含 role 和 status 列

## 2. 超级管理员初始化

- [x] 2.1 在 `application.yml` 新增 `app.super-admin.username=admin` 和 `app.super-admin.password=Cloud@1234` 配置
- [x] 2.2 创建 `config/DataInitializer.java` 实现 CommandLineRunner，启动时检查 admin 用户是否存在，不存在则创建（role=SUPER_ADMIN, status=ACTIVE, BCrypt 加密密码）
- [x] 2.3 为 DataInitializer 编写单元测试：首次启动创建超管、二次启动跳过、密码正确加密（4 tests passing）

## 3. DTO 更新

- [x] 3.1 修改 `dto/RegisterRequest.java`，新增 `role` 字段（枚举或字符串，校验只接受 USER / ADMIN）
- [x] 3.2 修改 `dto/LoginResponse.java` 的 UserDTO，新增 `role` 和 `status` 字段
- [x] 3.3 修改 `dto/UserDTO.java`，新增 `role` 和 `status` 字段
- [x] 3.4 创建 `dto/PendingUserDTO.java`（id, username, nickname, role, createdAt）用于待审批列表
- [x] 3.5 创建 `dto/AdminUserDTO.java`（id, username, nickname, role, status, createdAt, lastLoginAt）用于用户列表
- [x] 3.6 创建 `dto/UserStatusUpdateRequest.java`（status 字段）用于封禁/解禁
- [x] 3.7 创建 `dto/ApprovalResponse.java`（userId, status, message）用于审批操作响应

## 4. Repository 更新

- [x] 4.1 修改 `repository/UserRepository.java`，新增 `findByStatus(AccountStatus status)`、`findByRole(Role role)`、`findByStatusAndRole` 查询方法
- [x] 4.2 新增分页查询方法：`findAllFiltered` 支持按角色/状态/关键词筛选分页（使用 @Query）

## 5. 注册与登录逻辑修改

- [x] 5.1 修改 `service/UserService.java` 的 `register()` 方法：根据 role 设置 status（USER→ACTIVE, ADMIN→PENDING），role=SUPER_ADMIN 抛异常，ADMIN 注册不返回 token
- [x] 5.2 修改 `service/UserService.java` 的 `login()` 方法：校验 status，PENDING/REJECTED/DISABLED 分别抛对应异常（ForbiddenException 403）
- [x] 5.3 修改 `service/UserService.java` 的 `getCurrentUser()`，DTO 中填充 role 和 status
- [x] 5.4 修改 `controller/AuthController.java` 的 register 接口，ADMIN 注册返回 201 + 提示消息（无 token）
- [x] 5.5 为 UserService.register() 编写单元测试：USER 注册直接 ACTIVE+返回 token、ADMIN 注册 PENDING+无 token、SUPER_ADMIN 注册 400（5 tests passing）
- [x] 5.6 为 UserService.login() 编写单元测试：ACTIVE 登录成功、PENDING 拒绝、REJECTED 拒绝、DISABLED 拒绝（5 tests passing）

## 6. JWT 过滤器与 Security 配置

- [x] 6.1 修改 `config/JwtAuthenticationFilter.java`：从 User 读取 role 构建 `SimpleGrantedAuthority("ROLE_" + role.name())`，非 ACTIVE 状态不设置 authentication
- [x] 6.2 修改 `config/SecurityConfig.java`：新增 `/api/v1/admin/approve/**` 和 `/api/v1/admin/reject/**` 的 `hasRole("SUPER_ADMIN")` 规则，`/api/v1/admin/users/**` 的 `hasAnyRole("ADMIN","SUPER_ADMIN")` 规则
- [x] 6.3 为 JwtAuthenticationFilter 编写单元测试：ACTIVE 用户设置 authorities、PENDING 用户不设置 authentication、DISABLED 用户不设置（6 tests passing）

## 7. 管理端 Controller 与 Service

- [x] 7.1 创建 `controller/AdminController.java`，实现 GET /api/v1/admin/pending-users、POST /api/v1/admin/approve/{id}、POST /api/v1/admin/reject/{id}
- [x] 7.2 在 AdminController 实现 GET /api/v1/admin/users（分页+筛选）、PUT /api/v1/admin/users/{id}/status、DELETE /api/v1/admin/users/{id}
- [x] 7.3 在 UserService 中实现审批逻辑：approve 将 PENDING→ACTIVE，reject 将 PENDING→REJECTED，非 PENDING 状态返回 400
- [x] 7.4 实现用户管理逻辑：封禁（→DISABLED）、解禁（→ACTIVE）、删除（校验不可删超管）
- [x] 7.5 为审批逻辑编写单元测试：通过 PENDING→ACTIVE、拒绝 PENDING→REJECTED、非 PENDING 操作 400、不存在用户 404（含在 UserServiceTest 7 admin tests 中）
- [x] 7.6 为用户管理逻辑编写单元测试：封禁、解禁、删除、删除超管 400、封禁超管 400（含在 UserServiceTest 7 admin tests 中）

## 8. 前端类型与 Store

- [x] 8.1 修改 `frontend/src/types/index.ts`：User 新增 role/status 字段，RegisterRequest 新增 role 字段，新增 PendingUser、AdminUser 类型
- [x] 8.2 修改 `frontend/src/stores/auth.ts`：新增 `isAdmin` 和 `isSuperAdmin` computed，基于 user.role 判断
- [x] 8.3 修改 `frontend/src/services/api.ts`：区分 401（未认证→跳转登录）和 403（无权限→显示提示不跳转，auth 端点跳过）

## 9. 前端注册页面

- [x] 9.1 修改 `frontend/src/pages/RegisterPage.vue`：新增角色选择卡片组（USER / ADMIN），使用 role="radiogroup"
- [x] 9.2 修改 RegisterPage.vue 提交逻辑：ADMIN 注册成功后显示「等待审批」提示并跳转登录页，不存 token
- [x] 9.3 修改 `frontend/src/pages/LoginPage.vue`：处理后端返回的 PENDING/REJECTED/DISABLED 状态错误，显示对应提示（已有逻辑无需修改）

## 10. 前端管理页面

- [x] 10.1 创建 `frontend/src/pages/admin/ApprovalPage.vue`：待审批列表，每张卡片显示用户信息+通过/拒绝按钮，空状态，loading 态，toast 反馈
- [x] 10.2 创建 `frontend/src/pages/admin/UserListPage.vue`：用户表格（分页），角色/状态徽章，搜索筛选，超管可封禁/解禁/删除，删除确认弹窗
- [x] 10.3 修改 `frontend/src/router/index.ts`：新增 /admin/approvals（meta: roles: ['SUPER_ADMIN']）和 /admin/users（meta: roles: ['ADMIN','SUPER_ADMIN']）路由
- [x] 10.4 修改路由守卫：支持 meta.roles 角色判断，角色不匹配跳转首页
- [x] 10.5 修改 `frontend/src/components/AppHeader.vue`：按角色显示「审批管理」和「用户管理」导航入口

## 11. 集成验证

- [x] 11.1 运行后端全量单元测试：`cd backend && ./gradlew test`，121 tests，27 新增全部通过，11 预存失败非本次引入
- [x] 11.2 运行架构检查：编译通过，无层级依赖违规
- [x] 11.3 手动验证完整流程：启动后端→超管自动创建→注册普通用户→登录成功→注册管理员→待审批→超管登录审批→管理员登录成功→用户列表→封禁/解禁/删除
