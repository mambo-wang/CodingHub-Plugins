## 为什么（Why）

当前系统所有用户权限完全相同，没有角色区分，也没有任何管理手段。随着平台内容（工具、视频、帖子）增长，需要管理员角色来审核和管理内容，同时需要超级管理员来管控管理员准入。引入三级角色（普通用户/管理员/超级管理员）和注册审批机制，是建立平台治理能力的第一步。

## 变更内容（What Changes）

- **新增** User 实体 `role` 字段（枚举：`USER` / `ADMIN` / `SUPER_ADMIN`），单角色模型
- **新增** User 实体 `status` 字段（枚举：`ACTIVE` / `PENDING` / `REJECTED` / `DISABLED`），表示账号状态
- **修改** 注册接口：请求体新增 `role` 字段，注册表单只暴露 `USER` 和 `ADMIN` 两个选项（`SUPER_ADMIN` 不可注册）
- **修改** 注册逻辑：选择 `USER` 角色直接 `ACTIVE` 可登录；选择 `ADMIN` 角色进入 `PENDING` 状态等待审批
- **修改** 登录逻辑：校验账号状态，`PENDING` / `REJECTED` / `DISABLED` 状态拒绝登录并返回对应提示
- **新增** 超级管理员内置账号：应用启动时通过 `DataInitializer` 自动初始化 `admin / Cloud@1234`（`SUPER_ADMIN` / `ACTIVE`），配置项放 `application.yml`
- **新增** 注册审批功能：超级管理员可查看待审批列表，执行「通过」或「拒绝」操作
- **新增** 用户管理功能：管理员和超级管理员可查看用户列表（分页），超级管理员可封禁/解禁/删除用户
- **修改** JWT 认证过滤器：从数据库读取 User 的 `role` 和 `status`，构建带 `GrantedAuthority` 的 `Authentication`（现有 filter 已在查库，零额外开销）
- **修改** Spring Security 配置：管理接口按角色鉴权（`hasRole`）
- **新增** 前端注册页面角色选择 UI
- **新增** 前端注册审批页面（仅超级管理员可见）
- **新增** 前端用户列表页面（管理员和超级管理员可见）
- **修改** 前端路由守卫：支持 `roles` meta 字段做角色级访问控制
- **修改** 前端导航栏：按角色显示管理入口
- **BREAKING** `LoginResponse.UserDTO` 新增 `role` 和 `status` 字段（前端需同步更新类型）

## 能力清单（Capabilities）

### 新增能力（New Capabilities）

- `user-role`: 用户角色与账号状态模型——定义三级角色枚举和四种账号状态枚举，以及注册时角色选择与状态流转规则
- `admin-approval`: 管理员注册审批——超级管理员查看待审批用户列表，通过或拒绝管理员注册申请
- `admin-user-management`: 用户管理——管理员和超级管理员查看用户列表，超级管理员封禁/解禁/删除用户

### 修改能力（Modified Capabilities）

- `auth`: 注册流程变更（新增角色选择、审批状态流转）和登录流程变更（账号状态校验）
- `auth-api`: 注册请求新增 `role` 字段，登录响应新增 `role` 和 `status` 字段，新增管理端 API
- `user-model`: User 实体新增 `role` 和 `status` 字段

## 影响范围（Impact）

### 后端

- `model/User.java` — 新增 `role`、`status` 枚举字段
- `dto/RegisterRequest.java` — 新增 `role` 字段
- `dto/LoginResponse.java` — `UserDTO` 新增 `role`、`status`
- `dto/UserDTO.java` — 新增 `role`、`status`
- `dto/` — 新增审批和用户管理相关 DTO
- `service/UserService.java` — 修改 `register()`、`login()`，新增审批和用户管理方法
- `controller/AuthController.java` — 注册接口变更
- `controller/` — 新增 `AdminController`
- `config/SecurityConfig.java` — 新增 `hasRole` 鉴权规则
- `config/JwtAuthenticationFilter.java` — 从 User 读 role 构建 `GrantedAuthority`
- `config/DataInitializer.java` — 新增，启动时初始化超级管理员
- `repository/UserRepository.java` — 新增 `findByStatus`、`findByRole` 等查询
- `application.yml` — 新增 `app.super-admin.*` 配置
- `scripts/init-db.sql` — user 表新增 `role`、`status` 列
- `scripts/migrations/` — 新增 migration SQL

### 前端

- `types/index.ts` — `User` 新增 `role`、`status`，`RegisterRequest` 新增 `role`
- `stores/auth.ts` — 新增 `role` 判断、`isAdmin` / `isSuperAdmin` computed
- `pages/RegisterPage.vue` — 新增角色选择 UI
- `pages/LoginPage.vue` — 处理 `PENDING` / `REJECTED` 状态错误
- `pages/admin/ApprovalPage.vue` — 新增审批页面
- `pages/admin/UserListPage.vue` — 新增用户列表页面
- `router/index.ts` — 新增 admin 路由 + 角色守卫
- `components/NavBar.vue` — 按角色显示管理入口
