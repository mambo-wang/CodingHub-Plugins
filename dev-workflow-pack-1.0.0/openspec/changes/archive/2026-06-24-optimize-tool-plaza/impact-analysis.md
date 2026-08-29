# Impact Analysis

> 基于 `design.md` 中的文件清单执行 codegraph 扫描，确认技术设计的实际影响范围。

---

## 1. 改动范围 (Change Surface)

| 类型 | 数量 | 文件列表 |
|------|------|----------|
| 新增 | 0 | — |
| 修改 | 4 | `frontend/src/pages/HomePage.vue` |
| | | `frontend/src/components/AppHeader.vue` |
| | | `frontend/src/router/index.ts` |
| | | `frontend/src/pages/EditToolPage.vue` |
| 删除 | 2 | `frontend/src/pages/MyToolsPage.vue` |
| | | `frontend/src/pages/MyToolFavoritesPage.vue` |

---

## 2. 调用图 (Call Graph)

### 2.1 直接调用方 (Direct Callers)

| 调用方 | 位置 | 风险等级 |
|--------|------|----------|
| `EditToolPage.vue` — `router.push('/me/tools')` | L55, L68, L146, L155, L297 | **L1** |
| `HomePage.vue` — sidebarItems 定义 `/me/tools`, `/me/favorites` | L15-19 | L0 (删除) |
| `HomePage.vue` — `router.push('/me/tools/${toolId}/edit')` | L134 | L0 (保留) |
| `AppHeader.vue` — `goToMyTools → router.push('/me/tools')` | L51 | L0 (删除) |
| `DetailPage.vue` — `router.push('/me/tools/${tool.value.id}/edit')` | L39 | L0 (保留) |

### 2.2 反向调用图（被谁调用）

```
/my/tools 路由
  ├── AppHeader.vue goToMyTools (L51) — 删除
  ├── HomePage.vue sidebarItems (L17) — 删除
  ├── EditToolPage.vue (L55, L68, L146, L155, L297) — 需改为 router.push('/')
  └── MyToolsPage.vue (页面组件) — 删除

/me/favorites 路由
  ├── HomePage.vue sidebarItems (L18) — 删除
  └── MyToolFavoritesPage.vue (页面组件) — 删除

/me/tools/:id/edit 路由
  ├── HomePage.vue handleToolEdit (L134) — 保留
  └── DetailPage.vue (L39) — 保留
```

---

## 3. 依赖链 (Dependency Chain)

### 3.1 上游依赖 (Upstream)

| 依赖项 | 类型 | 风险 |
|--------|------|------|
| `services/api.ts` — `GET /api/v1/tools` | API 调用 | L0 (不变) |
| `services/api.ts` — `GET /api/v1/tools/my` | API 调用 | L0 (不变) |
| `services/api.ts` — `GET /api/interactions/favorites` | API 调用 | L0 (不变) |
| `services/api.ts` — `fileUploadApi` | API 调用 | L0 (不变) |
| `stores/auth.ts` — `useAuthStore` | 状态管理 | L0 (不变) |

### 3.2 下游影响 (Downstream)

| 受影响模块 | 触发场景 |
|------------|----------|
| `EditToolPage.vue` | 保存/删除/取消后重定向到 `/me/tools` → 需改为 `/` |
| `GeneralizedSidebar` | 工具页面不再引用，但论坛/微课 6 个页面仍在使用，无影响 |

---

## 4. 受影响的测试 (Affected Tests)

| 测试文件 | 类型 | 状态 | 行动 |
|----------|------|------|------|
| 无现有测试覆盖受影响组件 | — | — | — |

现有测试仅覆盖论坛模块和通用组件，无 HomePage、AppHeader、EditToolPage、MyToolsPage、MyToolFavoritesPage 的测试。

---

## 5. 风险评估 (Risk Assessment)

| 风险等级 | 触发条件 | 缓解措施 |
|----------|----------|----------|
| **L1** | `EditToolPage.vue` 5 处 `router.push('/me/tools')` 路由失效 | 统一改为 `router.push('/')` |
| L0 | `DetailPage.vue` 使用 `/me/tools/:id/edit` | 该路由保留，无影响 |
| L0 | `GeneralizedSidebar` 组件孤立 | 论坛/微课仍在使用 |

**本次改动风险等级**: **L1** — 修改路由导致 `EditToolPage.vue` 重定向失效

---

## 6. 层级依赖校验 (Layer Dependency Check)

```bash
bash scripts/lint-arch.sh
```

**结果**: ✅ PASS

---

## 7. 设计修正建议 (Design Amendment)

- **`EditToolPage.vue`** 未在原始 design.md 中列为修改文件，但包含 5 处 `/me/tools` 路由引用，必须修改为 `router.push('/')`

---

## 8. 回归测试建议 (Regression Suggestions)

- [ ] 验证从 EditToolPage 保存/删除/取消后正确跳转到工具广场首页
- [ ] 验证工具广场三个 Tab（全部/我的收藏/我的工具）数据切换正确
- [ ] 验证未登录用户看不到「我的收藏」和「我的工具」pill
- [ ] 验证上传 Modal 打开/关闭/提交成功后刷新数据
- [ ] 验证 AppHeader 中「我的工具」按钮和下拉项已移除

---

## 9. 检查清单 (Checklist)

- [x] 已识别所有直接/传递调用方
- [x] 已列出上游/下游依赖
- [x] 已评估风险等级 (L1)
- [x] `scripts/lint-arch.sh` 校验通过
- [x] 已列出回归测试清单
- [x] 已发现设计修正建议 (EditToolPage.vue)

---

**生成时间**: 2026-06-22
**基础**: openspec/changes/optimize-tool-plaza/proposal.md + design.md
