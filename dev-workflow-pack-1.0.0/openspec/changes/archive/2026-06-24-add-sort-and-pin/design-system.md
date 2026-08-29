# Design System: add-sort-and-pin（双主题）

> 引用全局设计系统 `design-system/CodingHub/MASTER.md`，仅列出本次变更涉及的 UI 组件、交互状态与可访问性约束。

## 1. 全局样式引用

### 字体

| 角色 | 字体 | CSS 变量 |
|------|------|----------|
| 标题/按钮/正文 | Sora (300–800 weight) | `var(--font-display)` |
| 代码/统计数字 | Space Mono (400, 700 weight) | `var(--font-mono)` |

**导入：**
```css
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');
```

### 圆角

| 元素 | 值 |
|------|-----|
| 按钮、输入框、徽章、Tab 选项 | `8px` |
| 卡片、模态框 | `16px` |

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

### 新增 Token（本次变更专用）

| 角色 | 暗色主题 | 亮色主题 | CSS 变量 |
|------|----------|----------|----------|
| 火苗颜色 | `#F59E0B` | `#D97706` | `--color-hot` |
| 置顶颜色 | `#8b5cf6` | `#7c3aed` | `--color-pinned` |
| Tab 激活背景 | `rgba(139,92,246,0.15)` | `rgba(124,58,237,0.1)` | `--tab-active-bg` |

### 暗色主题背景效果

```css
[data-theme="dark"] body::before {
  background:
    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(139,92,246,0.15), transparent),
    radial-gradient(ellipse 60% 40% at 80% 50%, rgba(6,182,212,0.08), transparent),
    radial-gradient(ellipse 50% 30% at 20% 80%, rgba(236,72,153,0.06), transparent);
}
```

### 亮色主题背景效果

```css
[data-theme="light"] body::before {
  background:
    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(124,58,237,0.08), transparent),
    radial-gradient(ellipse 60% 40% at 80% 50%, rgba(8,145,178,0.05), transparent);
}
```

---

## 3. 涉及组件清单

| 组件/页面 | 用途 | 状态覆盖 |
|-----------|------|----------|
| `SortTab.vue`（新增） | "热度 \| 最新" 排序切换 Tab | normal / active / hover / focus |
| `ToolCard.vue`（修改） | 工具卡片，新增置顶/火苗图标、管理员置顶按钮 | normal / hover / pinned / hot / admin-view |
| `PostCard.vue`（修改） | 论坛帖子卡片，新增置顶/火苗图标、管理员置顶按钮 | normal / hover / pinned / hot / admin-view |
| `VideoCard.vue`（修改） | 微课卡片，新增置顶/火苗图标、管理员置顶按钮 | normal / hover / pinned / hot / admin-view |
| `HomePage.vue`（修改） | 工具列表页，集成 SortTab、适配 hot-top5 | normal / loading / empty |
| `PostListPage.vue`（修改） | 论坛帖子列表页，集成 SortTab、适配 hot-top5 | normal / loading / empty |
| `VideoListPage.vue`（修改） | 微课列表页，集成 SortTab、适配 hot-top5 | normal / loading / empty |

---

## 4. 交互状态（双主题）

### 4.1 `SortTab` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); color: var(--text-secondary); border: 1px solid var(--border-color); border-radius: 8px; padding: 6px 0;` |
| active tab | `background: rgba(139,92,246,0.15); color: var(--accent-1); font-weight: 600; border-bottom: 2px solid var(--accent-1);` |
| hover (inactive) | `color: var(--text-primary); background: rgba(255,255,255,0.05);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |

### 4.2 `SortTab` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); color: var(--text-secondary); border: 1px solid var(--border-color); border-radius: 8px;` |
| active tab | `background: rgba(124,58,237,0.1); color: var(--accent-1); font-weight: 600; border-bottom: 2px solid var(--accent-1);` |
| hover (inactive) | `color: var(--text-primary); background: rgba(0,0,0,0.03);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |

### 4.3 置顶图标 `ArrowUp` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `color: #8b5cf6; size: 16px;` 位于卡片左上角 |
| hover | `color: #a78bfa; transform: scale(1.1); transition: 0.2s ease;` |

### 4.4 置顶图标 `ArrowUp` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `color: #7c3aed; size: 16px;` |
| hover | `color: #6d28d9; transform: scale(1.1); transition: 0.2s ease;` |

### 4.5 火苗图标 `Flame` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `color: #F59E0B; size: 16px;` 位于卡片右上角 |
| hover | `color: #FBBF24; transition: 0.2s ease;` |

### 4.6 火苗图标 `Flame` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `color: #D97706; size: 16px;` |
| hover | `color: #B45309; transition: 0.2s ease;` |

### 4.7 管理员置顶按钮 `Pin` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal (unpinned) | `color: var(--text-muted); background: transparent; border: none; cursor: pointer; size: 14px;` |
| hover (unpinned) | `color: var(--accent-1); transition: 0.2s ease;` |
| normal (pinned) | `color: #8b5cf6;` |
| hover (pinned) | `color: #a78bfa;` |
| loading | `opacity: 0.5; cursor: not-allowed;` |

### 4.8 管理员置顶按钮 `Pin` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal (unpinned) | `color: var(--text-muted); background: transparent; border: none; cursor: pointer;` |
| hover (unpinned) | `color: var(--accent-1); transition: 0.2s ease;` |
| normal (pinned) | `color: #7c3aed;` |
| hover (pinned) | `color: #6d28d9;` |
| loading | `opacity: 0.5; cursor: not-allowed;` |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 768px` (mobile) | SortTab 全宽，卡片单列，图标缩小到 14px |
| `≥ 768px` (tablet) | SortTab 自适应宽度，卡片 2-3 列网格 |
| `≥ 1024px` (desktop) | SortTab 内联，卡片 3-4 列，图标正常 16px |

---

## 6. 可访问性要求

- [x] SortTab 每个选项有可读文字（"热度"、"最新"）
- [x] 置顶图标 `ArrowUp` 为装饰性 → `aria-hidden="true"`
- [x] 火苗图标 `Flame` 为装饰性 → `aria-hidden="true"`
- [x] 管理员置顶按钮为纯图标按钮 → 必须有 `aria-label="置顶"` / `aria-label="取消置顶"`
- [x] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px
- [x] 颜色对比度：火苗 `#F59E0B` 在 `#09090b` 上对比度 7.2:1 ✅ AA
- [x] 置顶 `#8b5cf6` 在 `#09090b` 上对比度 5.7:1 ✅ AA
- [x] `prefers-reduced-motion: reduce` 下关闭 hover scale 动画

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 置顶标识（已置顶状态） | `ArrowUp` | `aria-hidden="true"` |
| 热度前5标识 | `Flame` | `aria-hidden="true"` |
| 管理员置顶操作（未置顶） | `Pin` | `aria-label="置顶"` |
| 管理员取消置顶操作（已置顶） | `PinOff` | `aria-label="取消置顶"` |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题
- ✅ 所有状态变化有 200ms 过渡动画
- ✅ `cursor: pointer` 在所有可点击元素上
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移（图标使用 `transform: scale(1.1)` 但不影响周围布局）
- ✅ 纯 CSS + scoped style，无 Tailwind 类名
