# Impact Analysis: 微课模块

> 基于 `design.md` 中的文件/类/测试清单执行 codegraph 扫描，确认技术设计的实际影响范围。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | 22 | `model/video/*.java`、`repository/video/*.java`、`dto/video/*.java`、`service/video/*.java`、`controller/video/*.java`、`config/VideoStorageConfig.java`、`pages/video/*.vue`、`components/video/*.vue`、`services/video.ts`、`types/video.ts` |
| 修改 | 5 | `config/SecurityConfig.java`、`application.yaml`、`pages/ProfilePage.vue`、`components/AppHeader.vue`、`router/index.ts` |
| 删除 | 0 | — |

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `SecurityFilterChain` | `config/SecurityConfig.java:30` | L0（新增 permitAll 条目，不修改现有规则） |
| `router.beforeEach` | `router/index.ts` | L0（新增路由，不影响现有路由守卫） |
| `AppHeader.vue` 模板 | `components/AppHeader.vue` | L0（新增导航链接，不影响现有链接） |
| `ProfilePage.vue` 模板 | `pages/ProfilePage.vue` | L0（新增 tab，不影响现有 tab） |

### 2.2 传递调用方 (Transitive Callers, depth 2-3)

- `JwtAuthenticationFilter` 通过 `SecurityFilterChain` 加载，本次只新增 permitAll 条目，不影响 Filter 行为
- `App.vue` 通过 `router-view` 渲染页面，新增路由自动生效
- `App.vue` 引入 `AppHeader.vue`，新增导航链接不影响现有渲染

### 2.3 反向调用图（被谁调用）

```
SecurityConfig.securityFilterChain()
  ├── Spring Security FilterChain（框架自动加载）
  │     └── JwtAuthenticationFilter（注入到 FilterChain）
  └── 新增 video GET 白名单条目（不影响现有鉴权逻辑）

router/index.ts
  └── App.vue → <router-view>
        └── 新增 /videos/* 路由（独立路由组，不影响现有路由）

AppHeader.vue
  └── App.vue → <AppHeader />
        └── 新增"微课"导航链接（不影响现有链接）

ProfilePage.vue
  └── router → ProfilePage 路由组件
        └── 新增"我的视频"/"我的收藏" tab（独立 tab，不影响现有 tab）
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `UserRepository` | 数据访问层 | L0（VideoService 通过 uploaderId 查询 User，只读依赖） |
| `XssSanitizer` | 工具类 | L0（评论 XSS 过滤，只读调用） |
| `JwtUtil` | 工具类 | L0（认证 Filter 使用，本次不修改） |
| `application.yaml` | 配置 | L0（仅新增 multipart 配置项） |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| 微课视频 API（新增） | 前端新增页面调用，不影响现有 API |
| 前端路由（新增） | 新增 `/videos/*` 路由，现有路由不变 |
| ProfilePage 扩展 | 新增 tab 面板，现有 tab 不受影响 |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| `tests/unit/stores/auth.spec.ts` | 单元 | 仍有效 | 无需改动 |
| `tests/unit/pages/forum/*.spec.ts` | 单元 | 仍有效 | 无需改动 |
| `backend/src/test/` | 单元/集成 | 仍有效 | 无需改动（本次新增模块） |

> 本次微课模块为纯新增，现有测试文件无需修改。新增测试将在 tasks.md 第 8 节创建。

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L0** | 纯新增，不影响现有代码 | 无 |
| **L1** | 修改函数签名/公共 API | 全量回归 + 通知调用方 |
| **L2** | 修改数据库 schema / 业务规则 / 跨模块契约 | 完整测试套件 + 灰度发布 |

**本次改动风险等级**: **L0**

- `SecurityConfig.java` 仅新增 permitAll 条目，现有鉴权规则完全不变
- `application.yaml` 仅增大 multipart 限制，不影响现有上传逻辑
- `AppHeader.vue` 仅新增导航链接，现有链接不变
- `ProfilePage.vue` 仅新增 tab，现有 tab 不变
- `router/index.ts` 仅新增路由，现有路由不变

---

## 6. 层级依赖校验 (Layer Dependency Check)

> 校验后端是否仍满足 `controller → service → repository → model` 单向依赖。

```bash
bash scripts/lint-arch.sh
```

**结果**: PASS（现有 2 个 L0 级别警告为历史遗留，非本次引入；新增 video 模块文件均符合层级规范）

---

## 7. 回归测试建议 (Regression Suggestions)

- [ ] 验证现有工具上传功能正常（multipart 配置变更后）
- [ ] 验证现有工具/论坛 API 鉴权不变（SecurityConfig 新增条目后）
- [ ] 验证 ProfilePage 现有 tab（我的工具/我的帖子/我的收藏）功能正常
- [ ] 验证 AppHeader 现有导航链接正常
- [ ] 验证前端路由跳转正常（现有页面无 404）

---

## 8. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方
- [x] 已列出上游/下游依赖
- [x] 已评估风险等级（L0）
- [x] `scripts/lint-arch.sh` 校验通过
- [x] 已列出回归测试清单
- [ ] （L2 风险）不适用——本次为 L0 风险

---

**生成时间**: 2026-06-17
**基础**: openspec/changes/add-micro-course/proposal.md + design.md
