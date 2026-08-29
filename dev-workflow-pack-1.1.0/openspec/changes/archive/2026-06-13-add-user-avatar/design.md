# Design: User Avatar Feature

## File Structure

### Backend (新增)

```
backend/src/main/java/com/iaihub/toolbox/
├── config/
│   └── UploadConfig.java                # 改造: 新增 avatarSubdir / avatarMaxSize / avatarAllowedExtensions
├── controller/
│   ├── UserController.java              # 改造: 新增 POST /me/avatar, DELETE /me/avatar, GET /{id}
│   └── AvatarStaticController.java      # 新增: GET /api/v1/static/avatars/{userId}
├── service/
│   └── UserService.java                 # 改造: 新增 uploadAvatar / deleteAvatar / getPublicProfile
├── dto/
│   ├── UserDTO.java                     # 改造: 新增 avatarUrl 字段
│   ├── PublicUserDTO.java               # 新增: 公开用户信息（不含 password/email）
│   └── AvatarUploadResponse.java        # 新增: { avatarUrl, fileSize, uploadedAt }
├── exception/
│   ├── AvatarValidationException.java   # 新增: 头像校验失败
│   └── UserNotFoundException.java       # 新增: 用户不存在
├── model/
│   └── User.java                        # 改造: 新增 avatarUrl 字段
└── util/
    └── AvatarUtil.java                  # 新增: 文件名校验、MIME 探测、路径安全

backend/src/main/resources/db/migration/
└── V20260610__add_user_avatar.sql       # 新增: ALTER TABLE user ADD COLUMN avatar_url

backend/src/test/java/com/iaihub/toolbox/
├── model/
│   └── UserAvatarTest.java              # 新增: avatarUrl 字段读写 + 长度限制
├── service/
│   └── UserServiceAvatarTest.java       # 新增: uploadAvatar / deleteAvatar / getPublicProfile
├── controller/
│   ├── UserControllerAvatarTest.java    # 新增: POST /me/avatar 集成测试
│   └── AvatarStaticControllerTest.java  # 新增: 静态资源 + 路径穿越防护
├── util/
│   └── AvatarUtilTest.java              # 新增: 文件名校验、MIME 探测
└── exception/
    └── AvatarValidationExceptionTest.java # 新增: 错误消息
```

### Frontend (新增/修改)

```
frontend/src/
├── components/
│   ├── UserAvatar.vue                   # 新增: 通用头像组件（URL + 降级 + 哈希色兜底）
│   ├── AuthorBadge.vue                  # 改造: 接收 avatarUrl prop
│   └── AppHeader.vue                    # 改造: 右上角改用 UserAvatar + 用户菜单新增"个人资料"项
├── pages/
│   ├── ProfilePage.vue                  # 新增: 个人资料页（头像上传/移除）
│   └── MyToolsPage.vue                  # 改造（可选）: 增加入口"个人资料"
├── router/
│   └── index.ts                         # 改造: 注册 /me/profile 路由
├── types/
│   └── index.ts                         # 改造: User / ToolSummary / ToolDetail / PostAuthor 等类型加 avatarUrl
├── stores/
│   └── auth.ts                          # 改造: User 类型同步
└── services/
    └── api.ts                           # 改造: 不需要新增（用现成 axios）

frontend/src/__tests__/
├── components/
│   ├── UserAvatar.test.ts               # 新增: 渲染 / 降级 / 哈希色
│   ├── AuthorBadge.test.ts              # 改造: 测试有/无 avatarUrl
│   └── AppHeader.test.ts                # 改造: 测试 UserAvatar 集成
├── pages/
│   └── ProfilePage.test.ts              # 新增: 上传 / 移除 / 错误状态
└── stores/
    └── auth.test.ts                     # 改造: avatarUrl 持久化
```

---

## Test Strategy

### 后端测试

| 测试文件 | 类型 | 策略 |
|---------|------|------|
| `UserAvatarTest` | 单元 | 直接测 `User` 实体，验证 `avatarUrl` 字段注解（`@Column(length=255)`） |
| `UserServiceAvatarTest` | 单元 + 集成 | `@SpringBootTest` 测 `uploadAvatar` 落盘 + 覆盖逻辑；`@Mock` 测 `deleteAvatar` 与 `getPublicProfile` |
| `UserControllerAvatarTest` | 集成 | `@WebMvcTest` + `MockMvc`，测 4 个端点的 HTTP 行为、状态码、错误信息 |
| `AvatarStaticControllerTest` | 集成 | `@WebMvcTest` 测 200 / 404 / 路径穿越拦截 |
| `AvatarUtilTest` | 单元 | 测 MIME 白名单、文件名校验、`..` 过滤 |
| `AvatarValidationExceptionTest` | 单元 | 测错误消息格式 |

**运行命令：**
```bash
cd backend && ./gradlew test --tests "*UserAvatar*" --tests "*Avatar*" --tests "*UserService*"
```

### 前端测试

| 测试文件 | 类型 | 策略 |
|---------|------|------|
| `UserAvatar.test.ts` | 组件 | Vitest + Vue Test Utils，验证：(1) 有 URL 渲染 img；(2) 无 URL 渲染首字母；(3) 加载失败切换兜底；(4) 哈希色基于 id |
| `AuthorBadge.test.ts` | 组件 | 验证 `avatarUrl` prop 影响渲染 |
| `AppHeader.test.ts` | 组件 | 验证 `UserAvatar` 集成 |
| `ProfilePage.test.ts` | 页面 | 验证：(1) 上传文件；(2) 格式校验；(3) 大小校验；(4) Loading 态；(5) 错误提示 |
| `auth.test.ts` | Store | 验证 `setUser` 持久化 `avatarUrl` |

**运行命令：**
```bash
cd frontend && npm run test -- --run src/__tests__/components/UserAvatar.test.ts
```

---

## Implementation Details

### 1. 数据库迁移

```sql
-- V20260610__add_user_avatar.sql
ALTER TABLE user
    ADD COLUMN avatar_url VARCHAR(255) NULL COMMENT '头像URL, 格式: /api/v1/static/avatars/{userId}.{ext}';

-- 老用户 avatar_url 默认为 NULL, 不需要 backfill
```

### 2. User 实体

```java
@Entity
@Table(name = "user", indexes = {
    @Index(name = "idx_user_username", columnList = "username", unique = true),
    @Index(name = "idx_user_nickname", columnList = "nickname", unique = true)
})
public class User {
    // ... existing fields

    @Column(name = "avatar_url", length = 255)
    private String avatarUrl;
}
```

### 3. UploadConfig 扩展

```java
@Data
@Configuration
@ConfigurationProperties(prefix = "app.upload")
public class UploadConfig {
    // existing
    private String baseDir;
    private String maxFileSize = "50MB";
    private String maxRequestSize = "200MB";
    private List<String> allowedExtensions;

    // 新增: 头像专属配置
    private String avatarSubdir = "avatars";
    private String avatarMaxFileSize = "2MB";
    private List<String> avatarAllowedExtensions = List.of("jpg", "jpeg", "png", "webp", "gif");

    @PostConstruct
    public void init() {
        // ... existing
        // 确保 avatar 子目录存在
        Path avatarPath = Paths.get(baseDir, avatarSubdir);
        if (!Files.exists(avatarPath)) Files.createDirectories(avatarPath);
    }
}
```

### 4. AvatarUtil 工具类

```java
public class AvatarUtil {
    private static final Set<String> ALLOWED_MIME = Set.of(
        "image/jpeg", "image/png", "image/webp", "image/gif"
    );
    private static final Set<String> ALLOWED_EXT = Set.of(
        "jpg", "jpeg", "png", "webp", "gif"
    );
    private static final Set<String> DANGEROUS_EXT = Set.of("svg", "html", "htm", "xml");

    public static String validateAndGetExtension(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new AvatarValidationException("请选择头像文件");
        }
        String original = file.getOriginalFilename();
        if (original == null) throw new AvatarValidationException("文件名无效");
        String ext = extractExtension(original).toLowerCase();
        if (DANGEROUS_EXT.contains(ext)) {
            throw new AvatarValidationException("出于安全考虑, 不支持 " + ext + " 格式");
        }
        if (!ALLOWED_EXT.contains(ext)) {
            throw new AvatarValidationException("仅支持 jpg / png / webp / gif 格式");
        }
        String mime = file.getContentType();
        if (mime == null || !ALLOWED_MIME.contains(mime.toLowerCase())) {
            throw new AvatarValidationException("文件类型与扩展名不匹配");
        }
        return ext;
    }

    public static void validatePathSafe(String userIdStr) {
        if (!userIdStr.matches("^\\d+$")) {
            throw new AvatarValidationException("无效的用户 ID");
        }
    }

    private static String extractExtension(String filename) {
        int dot = filename.lastIndexOf('.');
        return dot < 0 ? "" : filename.substring(dot + 1);
    }
}
```

### 5. UserService.uploadAvatar

```java
@Transactional
public AvatarUploadResponse uploadAvatar(Long userId, MultipartFile file) {
    // 1. 校验
    String ext = AvatarUtil.validateAndGetExtension(file);
    long maxBytes = parseSize(uploadConfig.getAvatarMaxFileSize());
    if (file.getSize() > maxBytes) {
        throw new AvatarValidationException(
            "头像文件不能超过 " + uploadConfig.getAvatarMaxFileSize());
    }

    // 2. 找 user
    User user = userRepository.findById(userId)
        .orElseThrow(() -> new UserNotFoundException("用户不存在"));

    // 3. 删除旧文件（如果存在）
    Path avatarDir = Paths.get(uploadConfig.getBaseDir(), uploadConfig.getAvatarSubdir());
    deleteExistingAvatars(avatarDir, userId);

    // 4. 写新文件
    Path target = avatarDir.resolve(userId + "." + ext);
    Files.copy(file.getInputStream(), target, StandardCopyOption.REPLACE_EXISTING);

    // 5. 更新 user
    user.setAvatarUrl("/api/v1/static/avatars/" + userId + "." + ext);
    user.setUpdatedAt(LocalDateTime.now()); // 用于 URL 缓存破坏
    userRepository.save(user);

    // 6. 构造返回
    long timestamp = user.getUpdatedAt().atZone(ZoneId.systemDefault()).toInstant().toEpochMilli();
    return AvatarUploadResponse.builder()
        .avatarUrl(user.getAvatarUrl() + "?v=" + timestamp)
        .fileSize(file.getSize())
        .uploadedAt(user.getUpdatedAt())
        .build();
}

private void deleteExistingAvatars(Path dir, Long userId) {
    if (!Files.exists(dir)) return;
    try (DirectoryStream<Path> stream = Files.newDirectoryStream(dir, userId + ".*")) {
        for (Path p : stream) Files.deleteIfExists(p);
    } catch (IOException e) {
        log.warn("Failed to delete old avatar for user {}: {}", userId, e.getMessage());
    }
}
```

### 6. UserController 端点

```java
@PostMapping(value = "/me/avatar", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
public ApiResponse<AvatarUploadResponse> uploadAvatar(
        @RequestParam("avatar") MultipartFile file,
        @AuthenticationPrincipal User currentUser) {
    AvatarUploadResponse response = userService.uploadAvatar(currentUser.getId(), file);
    return ApiResponse.success("头像上传成功", response);
}

@DeleteMapping("/me/avatar")
public ApiResponse<Void> deleteAvatar(@AuthenticationPrincipal User currentUser) {
    userService.deleteAvatar(currentUser.getId());
    return ApiResponse.success("头像已移除", null);
}

@GetMapping("/{id}")
public ApiResponse<PublicUserDTO> getPublicProfile(@PathVariable Long id) {
    return ApiResponse.success(userService.getPublicProfile(id));
}
```

### 7. AvatarStaticController 静态服务

```java
@RestController
@RequestMapping("/api/v1/static/avatars")
public class AvatarStaticController {

    private final Path avatarDir;
    private final List<String> probeOrder = List.of("jpg", "jpeg", "png", "webp", "gif");

    public AvatarStaticController(UploadConfig config) {
        this.avatarDir = Paths.get(config.getBaseDir(), config.getAvatarSubdir());
    }

    @GetMapping("/{userId}")
    public ResponseEntity<Resource> getAvatar(@PathVariable String userId) {
        AvatarUtil.validatePathSafe(userId);
        for (String ext : probeOrder) {
            Path candidate = avatarDir.resolve(userId + "." + ext);
            if (Files.exists(candidate)) {
                Resource resource = new FileSystemResource(candidate);
                return ResponseEntity.ok()
                    .contentType(MediaType.parseMediaType("image/" + ext))
                    .cacheControl(CacheControl.maxAge(Duration.ofHours(1)).cachePublic())
                    .body(resource);
            }
        }
        return ResponseEntity.notFound().build();
    }
}
```

### 8. 前端 UserAvatar 组件

```vue
<script setup lang="ts">
import { computed, ref } from 'vue'

const props = withDefaults(defineProps<{
  user: { id: number; username: string; avatarUrl?: string | null }
  size?: 'sm' | 'md' | 'lg'
}>(), { size: 'md' })

const PALETTE = ['#8b5cf6', '#06b6d4', '#ec4899', '#f59e0b', '#3b82f6', '#10b981']
const sizeMap = { sm: 24, md: 32, lg: 40 }

const sizePx = computed(() => sizeMap[props.size])
const initial = computed(() => props.user.username?.charAt(0).toUpperCase() ?? '?')
const paletteColor = computed(() => PALETTE[props.user.id % PALETTE.length])
const imgError = ref(false)

const showImage = computed(() => !!props.user.avatarUrl && !imgError.value)
const fontSize = computed(() => Math.floor(sizePx.value * 0.5))

const onError = () => { imgError.value = true }
</script>

<template>
  <div
    class="user-avatar"
    :class="[`user-avatar--${size}`]"
    :style="{ width: `${sizePx}px`, height: `${sizePx}px`, fontSize: `${fontSize}px` }"
    :title="`${user.username} 的头像`"
    role="img"
    :aria-label="`${user.username} 的头像`"
  >
    <img
      v-if="showImage"
      :src="user.avatarUrl!"
      :alt="`${user.username} 的头像`"
      class="user-avatar__img"
      @error="onError"
    />
    <span
      v-else
      class="user-avatar__initial"
      :style="{ background: paletteColor }"
    >{{ initial }}</span>
  </div>
</template>

<style scoped>
.user-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  overflow: hidden;
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
  flex-shrink: 0;
  position: relative;
}
.user-avatar__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}
.user-avatar__initial {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 600;
  font-family: var(--font-display);
}
@media (prefers-reduced-motion: reduce) {
  .user-avatar { animation: none; }
}
</style>
```

### 9. AuthorBadge 改造

```vue
<script setup lang="ts">
import UserAvatar from './UserAvatar.vue'

const props = withDefaults(defineProps<{
  username: string
  nickname?: string | null
  avatarUrl?: string | null
  avatarSize?: 'sm' | 'md' | 'lg'
  size?: 'sm' | 'md' | 'lg'
}>(), {
  size: 'md',
  avatarSize: 'sm'
})

const displayName = computed(() =>
  props.nickname ? `${props.nickname}(${props.username})` : props.username
)

const fakeUser = computed(() => ({
  id: 0,  // 兜底色不依赖具体 id
  username: props.username,
  avatarUrl: props.avatarUrl
}))
</script>

<template>
  <span class="author-badge" :class="[`author-badge--${size}`]" :title="`账号: ${username}`">
    <UserAvatar v-if="avatarUrl" :user="fakeUser" :size="avatarSize" />
    <span class="author-badge__text">{{ displayName }}</span>
  </span>
</template>
```

### 10. ProfilePage 上传逻辑

```typescript
async function handleFileChange(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  // 客户端校验
  const allowedExt = ['jpg', 'jpeg', 'png', 'webp', 'gif']
  const ext = file.name.split('.').pop()?.toLowerCase() ?? ''
  if (!allowedExt.includes(ext)) {
    error.value = '仅支持 jpg / png / webp / gif 格式'
    return
  }
  if (file.size > 2 * 1024 * 1024) {
    error.value = '头像文件不能超过 2MB'
    return
  }

  // 预览
  const reader = new FileReader()
  reader.onload = (e) => { previewUrl.value = e.target?.result as string }
  reader.readAsDataURL(file)
  selectedFile.value = file
  error.value = ''
}

async function handleUpload() {
  if (!selectedFile.value) return
  uploading.value = true
  error.value = ''
  try {
    const formData = new FormData()
    formData.append('avatar', selectedFile.value)
    const response = await api.post('/users/me/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    const newAvatarUrl: string = response.data.data.avatarUrl

    // 更新 auth store
    if (authStore.user) {
      authStore.user.avatarUrl = newAvatarUrl
      authStore.setUser(authStore.user)
    }

    success.value = true
    setTimeout(() => { success.value = false }, 2000)
    selectedFile.value = null
    previewUrl.value = null
  } catch (e: any) {
    error.value = e.response?.data?.message || '上传失败, 请重试'
  } finally {
    uploading.value = false
  }
}
```

---

## API 契约汇总

### 端点清单

| Method | Path | 鉴权 | 用途 |
|--------|------|------|------|
| POST | `/api/v1/users/me/avatar` | 必须登录 | 上传头像 |
| DELETE | `/api/v1/users/me/avatar` | 必须登录 | 移除头像 |
| GET | `/api/v1/users/me` | 必须登录 | 当前用户信息（已含 avatarUrl） |
| GET | `/api/v1/users/{id}` | 公开 | 用户公开信息（不含敏感字段） |
| GET | `/api/v1/static/avatars/{userId}` | 公开 | 头像静态资源 |

### 响应示例

**POST /me/avatar 成功：**
```json
{
  "code": 200,
  "message": "头像上传成功",
  "data": {
    "avatarUrl": "/api/v1/static/avatars/2.jpg?v=1718013600000",
    "fileSize": 153600,
    "uploadedAt": "2026-06-10T10:00:00Z"
  }
}
```

**GET /users/2：**
```json
{
  "code": 200,
  "data": {
    "id": 2,
    "username": "wangbao",
    "nickname": "王宝",
    "avatarUrl": "/api/v1/static/avatars/2.jpg?v=1718013600000",
    "createdAt": "2026-01-01T00:00:00Z"
  }
}
```

**错误响应：**
```json
{
  "code": 400,
  "message": "仅支持 jpg / png / webp / gif 格式",
  "data": null
}
```

---

## 跨层依赖校验

后端分层 (沿用既有约束)：

```
controller → service → repository → model
```

- `UserController` / `AvatarStaticController` → L4
- `UserService` / `AvatarUtil` → L3 / L0
- `User` / DTOs → L1
- `UploadConfig` / `AvatarUtil` → L0

无循环依赖。**风险等级：L1**（修改 user 表 schema + 新增公共 API 端点 + 改造现有组件）。

---

## 兼容性

- `avatar_url` 字段 nullable，老用户零数据迁移
- 前端 `User.avatarUrl` 为可选字段，未上传时 `null`，降级到首字母兜底
- 现有 `AppHeader` 文案不变，仅把内部实现从硬编码 div 替换为 `UserAvatar` 组件
- `AuthorBadge` 新 prop 默认值 = undefined，未传时行为不变

---

## 性能与缓存

- 静态资源 `Cache-Control: public, max-age=3600`
- 客户端 URL 加 `?v={updatedAt-millis}` 防止换头像后命中旧缓存
- 图片 `loading="lazy"`（列表场景）
- 头像尺寸 32/40px，无需服务端缩放（浏览器渲染）

---

## 不在本次范围

- 头像历史版本
- CDN 加速
- 服务端图片压缩 / WebP 自动转换
- 头像审核 / NSFW 检测
- 群组头像
- Gravatar
- 第三方登录头像

---

**设计完成日期**: 2026-06-10
**作者**: AI Agent
**依赖**: `user-nickname-feature`（提供昵称基础）、`update-auth-fields`（auth 框架）
