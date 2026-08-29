# Design System: profile-my-interactions（双主题）

> 引用全局设计系统 `design-system/CodingHub/MASTER.md`，仅列出本次变更涉及的 UI 组件、交互状态与可访问性约束。本次为个人中心新增「我的评论 / 我的收藏 / 我的点赞」三个互动板块。

## 1. 全局样式引用

### 字体
| 角色 | 字体 | CSS 变量 |
|------|------|----------|
| 标题/按钮/正文 | Sora (300–800 weight) | `var(--font-display)` |
| 代码/统计数字 | Space Mono (400, 700 weight) | `var(--font-mono)` |

**导入：** 见 MASTER.md（已在全局 `main.css` 注入，无需重复）。

### 圆角
| 元素 | 值 |
|------|-----|
| 标签 chip、输入框、按钮 | `8px` |
| 卡片、互动项、面板 | `16px` |

### 阴影
| Level | 暗色值 | 亮色值 |
|-------|--------|--------|
| `--shadow-sm` | `0 2px 8px rgba(0,0,0,0.3)` | `0 2px 8px rgba(0,0,0,0.08)` |
| `--shadow-md` | `0 8px 24px rgba(0,0,0,0.4)` | `0 8px 24px rgba(0,0,0,0.12)` |
| `--shadow-glow` | `0 0 40px rgba(139,92,246,0.15)` | `0 0 40px rgba(124,58,237,0.1)` |

---

## 2. 双主题 Tokens 映射

| 角色 | 暗色主题 | 亮色主题 | CSS 变量 |
|------|----------|----------|----------|
| 页面背景 | `#09090b` | `#f8fafc` | `--bg-primary` |
| 面板/侧栏 | `#0f0f12` | `#f1f5f9` | `--bg-secondary` |
| 卡片背景 | `rgba(15,15,20,0.7)` | `rgba(255,255,255,0.9)` | `--bg-card` |
| 毛玻璃 | `rgba(255,255,255,0.03)` | `rgba(255,255,255,0.8)` | `--bg-glass` |
| 主色 (紫) | `#8b5cf6` | `#7c3aed` | `--accent-1` |
| 辅助色 (青) | `#06b6d4` | `#0891b2` | `--accent-2` |
| 第三色 (粉) | `#ec4899` | `#db2777` | `--accent-3` |
| 主文字 | `#fafafa` | `#0f172a` | `--text-primary` |
| 次文字 | `#a1a1aa` | `#475569` | `--text-secondary` |
| 辅助文字 | `#52525b` | `#94a3b8` | `--text-muted` |
| 边框色 | `rgba(255,255,255,0.08)` | `rgba(0,0,0,0.08)` | `--border-color` |
| 发光边框 | `rgba(139,92,246,0.3)` | `rgba(124,58,237,0.3)` | `--border-glow` |
| 焦点环 | `#00FFFF` | `#7c3aed` | `--focus-ring` |
| 危险/错误 | `#EF4444` | `#EF4444` | — |

### 暗色主题背景效果
沿用 MASTER.md：`body::before` 三色径向渐变 + `#app::before` 60px 网格叠加。

### 亮色主题背景效果
沿用 MASTER.md：`[data-theme="light"] body::before` 紫/青径向渐变。

---

## 3. 涉及组件清单

| 组件/页面 | 用途 | 状态覆盖 |
|-----------|------|----------|
| `pages/ProfilePage.vue`（修改） | 新增互动区容器：标签切换（评论/收藏/点赞）+ 各类型子标签 + 列表 | normal / hover / focus / loading / empty / error |
| 互动项 `InteractionItem`（内联或新增小组件） | 单条互动展示：类型图标 + 标题/内容片段 + 时间，可点击跳转 | normal / hover / focus |
| 类型筛选 chip | 切换 TOOL / FORUM_POST / VIDEO（收藏/点赞板块用） | normal / active |
| 空状态 / 加载骨架 | 列表 loading 与空数据展示 | loading / empty |

复用既有样式：`.glass-card`、`.btn`、`.btn-primary`、`.alert`、`.spinner`、`.fade-enter-active`。

---

## 4. 交互状态（双主题）

### 4.1 类型筛选 chip / 标签切换 — 暗色主题
| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); color: var(--text-secondary); border: 1px solid var(--border-color); border-radius: 8px;` |
| active | `background: linear-gradient(135deg, var(--accent-1), var(--accent-2)); color: #fff;` |
| hover | `border-color: var(--accent-1); color: var(--text-primary);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |

### 4.2 类型筛选 chip / 标签切换 — 亮色主题
| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); color: var(--text-secondary); border: 1px solid rgba(0,0,0,0.1);` |
| active | `background: linear-gradient(135deg, var(--accent-1), var(--accent-2)); color: #fff;` |
| hover | `border-color: var(--accent-1);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |

### 4.3 互动项 InteractionItem — 暗色主题
| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); border-radius: 16px; padding: 16px; color: var(--text-primary); cursor: pointer; transition: all 0.2s ease;` |
| hover | `border-color: var(--border-glow); box-shadow: var(--shadow-glow); transform: translateY(-2px);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |

### 4.4 互动项 InteractionItem — 亮色主题
| 状态 | 样式 |
|------|------|
| normal | `background: rgba(255,255,255,0.9); border: 1px solid rgba(0,0,0,0.08); border-radius: 16px; padding: 16px; cursor: pointer;` |
| hover | `border-color: rgba(124,58,237,0.4); box-shadow: 0 0 40px rgba(124,58,237,0.1); transform: translateY(-2px);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 768px` (mobile) | 互动项单列、全宽；类型切换改为横向可滚动 chip 行 |
| `≥ 768px` (tablet) | 列表单列或两列网格 |
| `≥ 1024px` (desktop) | 沿用 ProfilePage 现有 `max-width: 960px` 容器，列表单列纵向排列 |

---

## 6. 可访问性要求

- [ ] 所有可点击互动项有可读文字或 `aria-label`（如「查看 工具 X」）
- [ ] 纯图标按钮 / 类型图标 `aria-hidden="true"`
- [ ] 标签切换使用 `role="tab"` + `aria-selected`，面板 `role="tabpanel"`
- [ ] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px，`outline: 2px solid`
- [ ] 颜色对比度满足 WCAG AA（沿用 MASTER 对比度表）
- [ ] `prefers-reduced-motion: reduce` 下关闭 `translateY` 位移与 spin 动画（沿用 ProfilePage 现有写法）
- [ ] 错误提示使用 `role="alert"`
- [ ] 键盘可达：Tab 循环、Enter 触发跳转

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 我的评论 | `MessageCircle` | `aria-hidden="true"` |
| 我的收藏 | `Bookmark` | `aria-hidden="true"` |
| 我的点赞 | `Heart` | `aria-hidden="true"` |
| 工具类型标识 | `Wrench` | `aria-hidden="true"` |
| 帖子类型标识 | `FileText` | `aria-hidden="true"` |
| 微课类型标识 | `Video` | `aria-hidden="true"` |
| 加载 | `Loader2` | `aria-hidden="true"` |
| 空状态 | `Inbox` | `aria-hidden="true"` |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题
- ✅ 所有状态变化有过渡动画（150–300ms）
- ✅ `cursor: pointer` 在互动项与按钮上
- ✅ hover 仅 `translateY(-2px)`，无导致布局位移的 scale
- ❌ 避免 `!important`
- ❌ 避免 Tailwind 类名（项目纯 CSS + scoped style）
