## unify-interactions E2E 测试报告

测试时间: 2026-06-21 15:45 ~ 15:52
测试环境: Chrome (opencli browser v1.8.0) / Frontend localhost:5173 / Backend localhost:8082
测试方式: opencli 浏览器自动化 + curl API 验证

---

### 总体结果: 21 项通过 / 1 项警告 / 1 项发现

---

### A. 工具模块

| # | 测试项 | 结果 | 详情 |
|---|--------|------|------|
| A1 | 首页 GeneralizedSidebar | PASS | `.generalized-sidebar` 存在，内容: 工具列表/我的工具/我的收藏 |
| A2a | 详情页 UnifiedLikeButton | PASS | `.unified-like-btn` 存在，aria-label="点赞"，计数=2 |
| A2b | 详情页 UnifiedFavoriteButton | PASS | `.unified-fav-btn` 存在，aria-label="收藏" |
| A2c | 详情页 UnifiedCommentSection | PASS | `.unified-comment-section` 存在，评论(8)，含回复/删除按钮 |
| A3 | 匿名点赞 toggle | PASS | 计数 2→3→2，class 切换 `liked`，aria-pressed 正确切换 |
| A4 | 匿名评论提交 | PASS | 评论数 8→9，新评论文本在页面中可见 |

### B. 论坛模块

| # | 测试项 | 结果 | 详情 |
|---|--------|------|------|
| B1 | 列表页 GeneralizedSidebar | PASS | 内容: 帖子列表/我的帖子/我的收藏 |
| B2a | 帖子详情 UnifiedLikeButton | PASS | 计数=0（帖子12无点赞） |
| B2b | 帖子详情 UnifiedFavoriteButton | PASS | aria-label="收藏" |
| B2c | 帖子详情 UnifiedCommentSection | PASS | 评论(0)，空状态文案"暂无评论，快来抢沙发吧" |
| B3 | 嵌套评论回复按钮 | WARN | 帖子12无评论，无回复按钮（预期行为） |

### C. 微课模块

| # | 测试项 | 结果 | 详情 |
|---|--------|------|------|
| C1 | 列表页 GeneralizedSidebar | PASS | 内容: 微课列表/我的微课/我的收藏 |
| C2a | 视频详情 UnifiedLikeButton | PASS | 计数=1 |
| C2b | 视频详情 UnifiedFavoriteButton | PASS | aria-label="收藏" |
| C2c | 视频详情 UnifiedCommentSection | PASS | 评论(0) |
| C3 | 视频匿名点赞 toggle | PASS | 计数 1→2→1，aria-label/aria-pressed 正确切换 |

### D. 权限守卫与路由

| # | 测试项 | 结果 | 详情 |
|---|--------|------|------|
| D1a | /me/favorites 未登录守卫 | FINDING | 未跳转 /login，页面直接加载（hasToken=false） |
| D1b | /forum/my-favorites 未登录守卫 | FINDING | 同上 |
| D1c | /videos/my-videos 未登录守卫 | FINDING | 同上 |
| D1d | /videos/my-favorites 未登录守卫 | FINDING | 同上 |
| D1e | /forum/my-posts 未登录守卫 | FINDING | 同上 |
| D2 | 收藏按钮未登录行为 | FINDING | 点击后 API 返回 403，但页面未跳转到 /login |

### E. API 端点验证

| # | 测试项 | 结果 | 详情 |
|---|--------|------|------|
| E1a | GET /interactions/likes/status | PASS | code=200, data={liked:false, likeCount:2} |
| E1b | GET /interactions/comments | PASS | code=200, totalElements=9 |
| E1c | GET /interactions/favorites/status | PASS | HTTP 403（未认证，预期行为） |
| E1d | 旧版 API 已废弃 | PASS | 旧端点返回 403（Spring Security 拦截） |
| E1e | 前端无旧版 API 调用 | PASS | network 中未发现 /tools/{id}/like 等旧端点调用 |

### F. 侧边栏一致性

| # | 测试项 | 结果 | 详情 |
|---|--------|------|------|
| F1a | / 使用 GeneralizedSidebar | PASS | 3 个 nav-item |
| F1b | /forum 使用 GeneralizedSidebar | PASS | 3 个 nav-item |
| F1c | /videos 使用 GeneralizedSidebar | PASS | 3 个 nav-item |
| F1d | 旧版 SidebarNav 已移除 | PASS | 三个模块均无 `.sidebar-nav` |

---

### 发现的问题

**FINDING-1: 受保护路由缺少前端守卫跳转**

现象: 在未登录状态（localStorage 无 token），访问 `/me/favorites`、`/forum/my-favorites`、`/videos/my-videos`、`/videos/my-favorites`、`/forum/my-posts` 等需要认证的路由时，页面直接加载而未跳转到 `/login`。

后端验证: `/api/v1/interactions/favorites` 的 POST 请求正确返回 403 Forbidden，说明后端权限校验正常。

影响: 用户在受保护页面看到空白或加载错误，而非被引导去登录。UnifiedFavoriteButton 组件在收到 403 响应后也未执行跳转。

建议: 检查 `router/index.ts` 中这些路由的 `beforeEnter` 或全局 `router.beforeEach` 守卫是否覆盖了新增路由（`/me/favorites`、`/videos/my-videos`、`/videos/my-favorites`）。同时检查 UnifiedFavoriteButton 的错误处理逻辑，403 响应时应 `router.push('/login')`。

---

### 测试脚本

完整测试脚本: `scripts/test-unify-interactions-e2e.sh`
运行方式: `bash scripts/test-unify-interactions-e2e.sh`
