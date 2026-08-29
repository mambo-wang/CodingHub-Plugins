# Design

## File Structure

### Backend (Java Spring Boot)

| 源码文件 | 测试文件 | 说明 |
|---------|---------|------|
| `backend/src/main/java/com/iaihub/toolbox/dto/LoginRequest.java` | `backend/src/test/java/com/iaihub/toolbox/dto/LoginRequestTest.java` | 登录请求 DTO |
| `backend/src/main/java/com/iaihub/toolbox/dto/RegisterRequest.java` | `backend/src/test/java/com/iaihub/toolbox/dto/RegisterRequestTest.java` | 注册请求 DTO |
| `backend/src/main/java/com/iaihub/toolbox/model/User.java` | `backend/src/test/java/com/iaihub/toolbox/model/UserTest.java` | 用户实体 |
| `backend/src/main/java/com/iaihub/toolbox/service/AuthService.java` | `backend/src/test/java/com/iaihub/toolbox/service/AuthServiceTest.java` | 认证服务 |
| `backend/src/main/java/com/iaihub/toolbox/controller/AuthController.java` | `backend/src/test/java/com/iaihub/toolbox/controller/AuthControllerTest.java` | 认证控制器 |
| `backend/src/main/java/com/iaihub/toolbox/repository/UserRepository.java` | - | 用户数据访问层 |

### Frontend (Vue 3 + TypeScript)

| 源码文件 | 说明 |
|---------|------|
| `frontend/src/services/auth.ts` | 认证 API 服务 |
| `frontend/src/pages/Login.vue` | 登录页面 |
| `frontend/src/pages/Register.vue` | 注册页面 |
| `frontend/src/types/index.ts` | 类型定义 |

## Test Strategy

### Backend

| 测试文件 | 测试类型 | 测试范围 |
|---------|---------|---------|
| `LoginRequestTest.java` | 单元测试 | 字段验证、username vs email 自动判断 |
| `RegisterRequestTest.java` | 单元测试 | 密码长度 >= 6 校验 |
| `UserTest.java` | 单元测试 | username 字段唯一性 |
| `AuthServiceTest.java` | 单元测试 | 登录逻辑（username/email）、注册逻辑 |
| `AuthControllerTest.java` | 集成测试 | REST API 端点测试 |

### Frontend

| 测试文件 | 测试类型 | 测试范围 |
|---------|---------|---------|
| Login.vue | 手动测试 | 表单输入、登录流程 |
| Register.vue | 手动测试 | 密码校验提示 |

## Test Commands

```bash
# Backend
cd backend && ./gradlew test --tests "*LoginRequestTest"
cd backend && ./gradlew test --tests "*RegisterRequestTest"
cd backend && ./gradlew test --tests "*AuthServiceTest"
cd backend && ./gradlew test --tests "*AuthControllerTest"

# Frontend
cd frontend && npm run dev
```

## Key Implementation Notes

1. **User 实体**：添加 `username` 字段，设置 `unique = true` 索引
2. **LoginRequest**：将 `email` 字段改为 `username`，支持用户名或邮箱格式自动判断
3. **RegisterRequest**：移除复杂密码校验规则，只保留长度 >= 6 的校验
4. **AuthService**：修改 `login()` 方法支持用户名方式查找用户
5. **Category**：数据库预置数据中移除 API 类型