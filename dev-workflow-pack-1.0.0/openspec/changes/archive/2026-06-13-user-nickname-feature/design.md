# Design - User Nickname Feature

## File Structure

### Backend

#### Test Files
```
backend/src/test/java/com/iaihub/toolbox/
├── model/
│   └── UserTest.java                    # 测试 nickname 字段存在、读写、唯一性
├── repository/
│   └── UserRepositoryTest.java          # 测试 findByNickname 方法
├── service/
│   └── AuthServiceTest.java             # 测试注册/登录含 nickname
├── controller/
│   └── AuthControllerTest.java          # 测试注册 API nickname 参数
└── dto/
    └── LoginResponseTest.java           # 测试 nickname 字段序列化
```

#### Source Files
```
backend/src/main/java/com/iaihub/toolbox/
├── model/
│   └── User.java                        # 新增 nickname 字段 + 唯一索引
├── dto/
│   ├── RegisterRequest.java            # 新增 nickname 字段 + 校验注解
│   ├── LoginResponse.java               # 新增 nickname 字段
│   └── UserDTO.java                     # 新增 nickname 字段
├── repository/
│   └── UserRepository.java             # 新增 findByNickname 方法
└── service/
    └── AuthService.java                 # 注册时保存 nickname、校验昵称唯一性
```

#### Database Migration
```
backend/src/main/resources/db/migration/
└── V{date}__add_user_nickname.sql       # ALTER TABLE user ADD COLUMN nickname
```

---

### Frontend

#### Test Files
```
frontend/src/
├── __tests__/
│   ├── components/
│   │   ├── AppHeader.test.ts            # 测试右上角显示 nickname
│   │   └── AuthorBadge.test.ts         # 测试作者信息 "昵称(账号)" 格式
│   ├── pages/
│   │   ├── RegisterPage.test.ts         # 测试注册表单 nickname 字段
│   │   ├── ToolDetail.test.ts          # 测试工具详情页作者信息
│   │   └── PostDetail.test.ts          # 测试帖子详情页作者信息
│   └── stores/
│       └── auth.test.ts                 # 测试 authStore user 类型含 nickname
```

#### Source Files
```
frontend/src/
├── types/
│   └── index.ts                         # User 类型新增 nickname?: string
├── stores/
│   └── auth.ts                         # User 类型同步
├── pages/
│   └── RegisterPage.vue                # 新增 nickname 输入框
├── components/
│   ├── AppHeader.vue                   # 右上角显示 authStore.user?.nickname || username
│   └── AuthorBadge.vue                # 新增通用作者信息组件，显示 "昵称(账号)"
└── services/
    └── api.ts                          # 类型同步（如果需要）
```

---

## Test Strategy

### Backend Tests

| Test File | Type | Strategy |
|-----------|------|----------|
| UserTest | 单元测试 | 直接测试 JPA 实体，验证 nickname 字段注解正确 |
| UserRepositoryTest | 单元测试 | 使用 @DataJpaTest，验证 findByNickname 查询正确 |
| AuthServiceTest | 单元测试 | 使用 @Mocking，验证业务逻辑 |
| AuthControllerTest | 集成测试 | 使用 @WebMvcTest，验证 API 端点 |
| LoginResponseTest | 单元测试 | 验证 DTO 序列化/反序列化 |

**运行命令：**
```bash
cd backend && ./gradlew test --tests "*UserTest" --tests "*UserRepositoryTest" --tests "*AuthServiceTest"
```

### Frontend Tests

| Test File | Type | Strategy |
|-----------|------|----------|
| AppHeader.test.ts | 组件测试 | Vitest + Vue Test Utils，测试 nickname 显示逻辑 |
| AuthorBadge.test.ts | 组件测试 | 测试 "昵称(账号)" 格式化 |
| RegisterPage.test.ts | 页面测试 | 测试 nickname 输入框渲染和校验 |
| auth.test.ts | Store 测试 | 测试 user 状态的 nickname 字段 |

**运行命令：**
```bash
cd frontend && npm run test -- --run src/__tests__/components/AppHeader.test.ts
```

---

## Implementation Details

### 1. User Entity
```java
@Entity
@Table(name = "user", indexes = {
    @Index(name = "idx_user_username", columnList = "username", unique = true),
    @Index(name = "idx_user_nickname", columnList = "nickname", unique = true)  // 新增
})
public class User {
    // ... existing fields
    
    @Column(length = 50)
    private String nickname;  // nullable
}
```

### 2. RegisterRequest DTO
```java
public class RegisterRequest {
    @NotBlank
    @Size(min = 4, max = 20)
    @Pattern(regexp = "^\\w+$")
    private String username;
    
    @NotBlank  // 新增
    @Size(min = 2, max = 10)
    @Pattern(regexp = "^[\\u4e00-\\u9fa5a-zA-Z0-9\\u3002\\uff0c\\u2014]+$")
    private String nickname;
    
    @NotBlank
    @Size(min = 6)
    private String password;
}
```

### 3. AuthorBadge Component
```vue
<script setup lang="ts">
const props = defineProps<{
  username: string
  nickname?: string | null
}>()

const displayName = computed(() => 
  props.nickname ? `${props.nickname}(${props.username})` : props.username
)
</script>

<template>
<span class="author-badge" :title="`账号: ${username}`">
  {{ displayName }}
</span>
</template>
```

### 4. AppHeader User Display
```vue
<script setup lang="ts">
const displayUsername = computed(() => 
  authStore.user?.nickname || authStore.user?.username
)
</script>

<template>
<!-- 右上角用户信息 -->
<span class="user-display">{{ displayUsername }}</span>
</template>
```

---

## Database Migration

```sql
-- V20260602_add_user_nickname.sql
ALTER TABLE user 
ADD COLUMN nickname VARCHAR(50) NULL AFTER username,
ADD UNIQUE INDEX idx_user_nickname (nickname);
```

---

## API Response Examples

### Register Response
```json
{
  "code": 200,
  "data": {
    "user": {
      "id": 1,
      "username": "wangbao",
      "nickname": "王宝"
    },
    "accessToken": "eyJ...",
    "refreshToken": "eyJ..."
  }
}
```

### Login Response
```json
{
  "code": 200,
  "data": {
    "user": {
      "id": 1,
      "username": "wangbao",
      "nickname": "王宝"
    },
    "accessToken": "eyJ..."
  }
}
```

### Get Current User Response
```json
{
  "code": 200,
  "data": {
    "id": 1,
    "username": "wangbao",
    "nickname": "王宝"
  }
}
```

---

## Backward Compatibility

- `nickname` 字段设置为 nullable，数据库迁移不影响现有用户
- 前端使用 `nickname || username` 降级策略，未设置昵称时显示账号
- API 响应保持原有结构，仅新增 nickname 字段