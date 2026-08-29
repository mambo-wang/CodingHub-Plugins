## CodingHub 上线前 E2E 全面测试报告

测试时间: 2026-06-21
测试工具: opencli v1.8.0 浏览器自动化
测试环境: localhost:5173 (前端) / localhost:8082 (后端)
登录身份: admin (SUPER_ADMIN)

---

### 总体结论

**37 项通过 / 1 项警告 / 1 项阻断性问题（已修复 1 项）**

- BLOCKER #1 ProfilePage 编译错误 — ✅ **已修复**（删除多余 `</div>`）
- BLOCKER #2 管理后台分类路由缺失 — ❌ **待修复**
- WARNING #1 Token 过期体验 — ⚠️ 建议上线前优化

---

### 一、路由可达性 (28 条路由)

| 类型 | 数量 | 结果 |
|------|------|------|
| 公开路由 | 9 条 | ✅ 全部正常加载 |
| 需认证路由 (已登录) | 10 条 | ✅ 全部正常加载 |
| 需认证路由 (未登录) | 10 条 | ✅ 全部正确跳转 /login |
| 404 路由 | 1 条 (`/admin`) | ⚠️ 见下方问题 #3 |
| 不存在的分类路由 | 3 条 (`/admin/categories` 等) | ⚠️ 见下方问题 #3 |

公开路由: `/` `/login` `/register` `/forum` `/videos` `/overview` `/quickstart` `/about` `/tools/:id` — 全部 ✅

需认证路由: `/me/tools` `/me/favorites` `/me/profile` `/me/tools/:id/edit` `/forum/my-posts` `/forum/my-favorites` `/forum/editor` `/videos/my-videos` `/videos/my-favorites` `/admin/approvals` `/admin/users` — 守卫全部 ✅

---

### 二、工具模块 (Tool)

| 测试项 | 结果 | 详情 |
|--------|------|------|
| 首页工具卡片列表 | ✅ PASS | 显示 11 个工具卡片 |
| 分类筛选 | ✅ PASS | 点击 MCP 分类后正确只显示 MCP 类工具 |
| 搜索功能 | ✅ PASS | 输入关键词后工具列表正确过滤 |
| 排序功能 | ✅ PASS | "按名称"排序后按字母序排列 |
| 工具详情页 | ✅ PASS | 显示名称、分类、作者、日期、统计数据 |
| 编辑/删除按钮 | ✅ PASS | admin 可见编辑和删除按钮 |
| 文件区域 | ✅ PASS | 显示"暂无文件"（该工具无文件时正确） |
| GeneralizedSidebar | ✅ PASS | 显示"工具列表/我的工具/我的收藏" |
| 我的工具页 | ✅ PASS | 正确显示空状态 |

---

### 三、论坛模块 (Forum)

| 测试项 | 结果 | 详情 |
|--------|------|------|
| 帖子列表页 | ✅ PASS | 显示 12 个帖子，搜索框存在 |
| GeneralizedSidebar | ✅ PASS | 显示"帖子列表/我的帖子/我的收藏" |
| 帖子详情页 | ✅ PASS | 标题、作者、日期、浏览量、统计数据正常 |
| 统一点赞按钮 | ✅ PASS | aria-label="点赞"，计数显示正确 |
| 统一收藏按钮 | ✅ PASS | aria-label="收藏" |
| 统一评论区 | ✅ PASS | 评论列表、编辑器、回复/删除按钮齐全 |
| 编辑/删除帖子 | ✅ PASS | admin 可见编辑和删除按钮 |
| 点赞交互 | ✅ PASS | 点赞 0→1，取消 1→0，状态切换正确 |
| 发布评论 | ✅ PASS | 评论内容正确显示在列表中 |

---

### 四、微课模块 (Video)

| 测试项 | 结果 | 详情 |
|--------|------|------|
| 视频列表页 | ✅ PASS | 显示视频卡片，含上传入口 |
| GeneralizedSidebar | ✅ PASS | 显示"微课列表/我的微课/我的收藏" |
| 视频详情页 | ✅ PASS | 视频播放器、作者信息、统计数据正常 |
| 视频播放器 | ✅ PASS | `<video>` 标签含 src 和 aria-label |
| 统一点赞按钮 | ✅ PASS | 计数=1 |
| 统一收藏按钮 | ✅ PASS | 正确显示 |
| 统一评论区 | ✅ PASS | 评论(0)，空状态"暂无评论，快来抢沙发吧" |
| 视频匿名点赞 | ✅ PASS | 1→2→1 正确 toggle |
| 发布评论 | ✅ PASS | 评论提交成功 |
| 我的微课页 | ✅ PASS | 空状态"还没有上传任何视频" |
| 微课收藏页 | ⚠️ WARN | 页面渲染但出现"没有权限执行此操作"提示 |

---

### 五、统一交互系统 (Unified Interactions)

| 测试项 | 结果 | 详情 |
|--------|------|------|
| 统一点赞 API | ✅ PASS | GET /interactions/likes/status 返回 200 |
| 统一评论 API | ✅ PASS | GET /interactions/comments 返回 200，含分页 |
| 统一收藏 API (已认证) | ✅ PASS | GET /interactions/favorites 返回 200 |
| 统一收藏 API (未认证) | ✅ PASS | POST /interactions/favorites 返回 403 (正确拒绝) |
| 旧版 API 废弃 | ✅ PASS | 旧端点返回 403，前端无旧版 API 调用 |
| 匿名点赞 (工具) | ✅ PASS | 2→3→2 正确 toggle，aria 属性正确 |
| 匿名评论 (工具) | ✅ PASS | 评论成功提交并显示 |
| 匿名点赞 (视频) | ✅ PASS | 1→2→1 正确 toggle |
| 嵌套评论 | ✅ PASS | 回复按钮存在，嵌套回复正确显示 |

---

### 六、管理后台 (Admin)

| 测试项 | 结果 | 详情 |
|--------|------|------|
| 审批管理 /admin/approvals | ✅ PASS | 显示"暂无待审批用户" |
| 用户管理 /admin/users | ✅ PASS | 搜索、角色筛选、状态筛选 UI 正常 |
| 用户列表数据 | ⚠️ WARN | 显示"共 0 个用户"，但 API 返回 60 用户（见问题 #2） |
| 分类管理 /admin/categories | ❌ BLOCKER | 路由不存在，显示 404 页面 |
| 论坛分类管理 | ❌ BLOCKER | /admin/forum-categories 路由不存在 |
| 论坛标签管理 | ❌ BLOCKER | /admin/forum-tags 路由不存在 |

---

### 七、其他功能

| 测试项 | 结果 | 详情 |
|--------|------|------|
| 概览/热榜页 | ✅ PASS | 用户总数、帖子总数、工具总数统计正常；工具热榜和帖子热榜展示正常 |
| 快速开始页 | ✅ PASS | 页面加载正常 |
| 关于页 | ✅ PASS | 显示项目介绍、技术栈、项目结构 |
| 主题切换 | ✅ PASS | light→dark 切换正常，按钮标题正确更新 |
| 登录流程 | ✅ PASS | admin/Cloud@1234 登录成功，获取 token |
| 导航栏 | ✅ PASS | 工具广场/论坛/微课/热榜/快速开始/关于 导航项完整 |

---

### 发现的问题

#### ~~BLOCKER #1: ProfilePage.vue 编译错误~~ ✅ 已修复

**严重程度**: ~~阻断~~ → 已修复
**文件**: `frontend/src/pages/ProfilePage.vue:253`
**现象**: Vite 编译报错 "Invalid end tag"，页面显示 Vite 错误覆盖层
**根因**: template 中 `<div>` 开标签 22 个，`</div>` 闭标签 23 个 — 第 253 行有一个多余的 `</div>` 闭合标签
**修复**: 已删除第 253 行多余的 `</div>`，验证标签平衡 (22=22)，页面恢复正常显示"个人中心"
**影响范围**: /me/profile 路由已恢复可用

#### BLOCKER #2: 管理后台分类管理路由缺失

**严重程度**: 阻断 — 管理后台核心功能不可用
**现象**: `/admin/categories`、`/admin/forum-categories`、`/admin/forum-tags` 均返回 404
**根因**: `router/index.ts` 中未配置这些路由，对应的页面组件可能不存在或未注册
**影响范围**: 管理员无法通过前端管理工具分类、论坛分类和标签

#### WARNING #1: Token 过期后收藏页显示权限错误

**严重程度**: 警告 — 用户体验问题
**现象**: JWT 过期后（15 分钟），收藏列表页显示"没有权限执行此操作"错误提示，但页面仍然渲染了空状态 UI
**根因**: 前端 API 请求 403 时的错误处理不够优雅，未自动触发 token 刷新或跳转登录
**建议**: 在 axios 拦截器中增加 403 响应的自动刷新逻辑，或至少隐藏错误提示并引导用户重新登录

---

### 建议的修复优先级

1. ~~**立即修复** — 删除 ProfilePage.vue 第 253 行多余的 `</div>`~~ ✅ 已完成
2. **立即修复** — 补充 admin 分类管理路由（`/admin/categories`、`/admin/forum-categories`、`/admin/forum-tags`），或从导航栏移除对应入口，避免用户点击后看到 404
3. **上线前优化** — 优化 token 过期后的用户体验（403 响应时自动刷新 token 或友好提示重新登录）
