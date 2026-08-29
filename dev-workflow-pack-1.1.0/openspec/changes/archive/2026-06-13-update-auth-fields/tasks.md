# Tasks

## Atomic TDD Task List

### Feature: User 实体添加 username 唯一字段

- [x] RED: 编写 UserTest——测试 username 字段唯一性约束
- [x] GREEN: User 实体添加 username 字段并设置唯一索引

### Feature: LoginRequest 支持用户名登录

- [x] RED: 编写 LoginRequestTest——测试 username 字段验证
- [x] GREEN: LoginRequest 字段改为 username

### Feature: RegisterRequest 简化密码校验（无需邮箱）

- [x] RED: 编写 RegisterRequestTest——测试只需 username 和密码长度 >= 6
- [x] GREEN: RegisterRequest 移除 email 字段，只保留 username 和密码校验

### Feature: AuthService 支持用户名登录

- [x] RED: 编写 AuthServiceTest——测试使用用户名登录成功
- [x] GREEN: AuthService.login() 支持 username 字段查找用户

### Feature: AuthController 登录接口调整

- [x] RED: 编写 AuthControllerTest——测试 username 登录 API
- [x] GREEN: AuthController 登录接口参数从 email 改为 username

### Feature: AuthService 注册逻辑调整

- [x] RED: 编写 AuthServiceTest——测试注册时密码长度 >= 6 通过
- [x] GREEN: AuthService.register() 调整密码校验规则

### Feature: UserRepository 添加 username 查找方法

- [x] RED: 编写 UserRepositoryTest——测试按 username 查找用户
- [x] GREEN: UserRepository 添加 findByUsername 方法

### Feature: 移除 API 工具分类

- [x] RED: 编写 CategoryServiceTest——测试分类列表不包含 API
- [x] GREEN: 数据库预置数据移除 API 类型分类

### Feature: 前端登录页面调整

- [x] RED: 编写 LoginPageTest——测试用户名输入
- [x] GREEN: Login.vue 将邮箱输入改为用户名输入

### Feature: 前端注册页面调整

- [x] RED: 编写 RegisterPageTest——测试密码只需长度 >= 6
- [x] GREEN: Register.vue 调整密码校验规则提示