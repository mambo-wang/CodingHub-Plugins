# Tasks - User Nickname Feature

## Atomic TDD Task List

### Backend Tasks

#### Feature: User 实体添加 nickname 字段

- [ ] RED: 编写 UserTest——测试 nickname 字段存在且可读写
- [ ] GREEN: User 实体添加 nickname 字段（VARCHAR 50, nullable）
- [ ] REFACTOR: 清理测试代码

#### Feature: User 模型添加 nickname 唯一索引

- [ ] RED: 编写 UserTest——测试 nickname 唯一性约束
- [ ] GREEN: User 实体 nickname 字段添加 unique=true 约束
- [ ] REFACTOR: 清理测试代码

#### Feature: RegisterRequest 添加 nickname 字段和校验

- [ ] RED: 编写 RegisterRequestTest——测试 nickname 必填、长度2-10、格式校验
- [ ] GREEN: RegisterRequest 添加 nickname 字段和 @Size、@Pattern 校验注解
- [ ] REFACTOR: 清理测试代码

#### Feature: AuthService.register() 处理 nickname

- [ ] RED: 编写 AuthServiceTest——测试注册时保存 nickname
- [ ] GREEN: AuthService.register() 构建 User 时包含 nickname
- [ ] REFACTOR: 清理测试代码

#### Feature: AuthService.register() 昵称唯一性校验

- [ ] RED: 编写 AuthServiceTest——测试昵称重复时注册失败
- [ ] GREEN: AuthService.register() 添加昵称重复校验，抛出 NicknameAlreadyExistsException
- [ ] REFACTOR: 清理测试代码

#### Feature: UserRepository 添加 nickname 查找方法

- [ ] RED: 编写 UserRepositoryTest——测试按 nickname 查找用户
- [ ] GREEN: UserRepository 添加 findByNickname 方法
- [ ] REFACTOR: 清理测试代码

#### Feature: LoginResponse 包含 nickname

- [ ] RED: 编写 LoginResponseTest——测试登录返回 nickname
- [ ] GREEN: LoginResponse 添加 nickname 字段
- [ ] REFACTOR: 清理测试代码

#### Feature: UserDTO 包含 nickname

- [ ] RED: 编写 UserDTOTest——测试用户信息包含 nickname
- [ ] GREEN: UserDTO 添加 nickname 字段
- [ ] REFACTOR: 清理测试代码

### Frontend Tasks

#### Feature: User 类型添加 nickname 字段

- [ ] RED: 编写 UserTypeTest——测试 User 类型包含 nickname
- [ ] GREEN: 前端 User 类型添加 nickname?: string
- [ ] REFACTOR: 清理测试代码

#### Feature: 注册页面添加昵称输入框

- [ ] RED: 编写 RegisterPageTest——测试注册表单包含 nickname 输入
- [ ] GREEN: RegisterPage.vue 添加 nickname 输入框和相关校验
- [ ] REFACTOR: 清理测试代码

#### Feature: 右上角显示昵称

- [ ] RED: 编写 AppHeaderTest——测试右上角显示用户昵称
- [ ] GREEN: AppHeader.vue 右上角用户信息显示 authStore.user?.nickname || username
- [ ] REFACTOR: 清理测试代码

#### Feature: 工具详情页作者信息格式化

- [ ] RED: 编写 ToolDetailTest——测试作者信息显示"昵称(账号)"格式
- [ ] GREEN: ToolDetail.vue 作者区域显示 `nickname(username)` 或仅 `username`
- [ ] REFACTOR: 清理测试代码

#### Feature: 帖子详情页作者信息格式化

- [ ] RED: 编写 PostDetailTest——测试作者信息显示"昵称(账号)"格式
- [ ] GREEN: PostDetail.vue 作者区域显示 `nickname(username)` 或仅 `username`
- [ ] REFACTOR: 清理测试代码

#### Feature: 帖子列表作者信息格式化

- [ ] RED: 编写 PostListTest——测试帖子列表作者显示"昵称(账号)"
- [ ] GREEN: PostList 相关组件作者显示 `nickname(username)` 或仅 `username`
- [ ] REFACTOR: 清理测试代码

### Database Tasks

#### Feature: 添加 nickname 字段迁移

- [ ] 创建数据库迁移脚本，添加 nickname 字段（VARCHAR 50, nullable, unique）
- [ ] 测试迁移脚本在开发环境执行成功
