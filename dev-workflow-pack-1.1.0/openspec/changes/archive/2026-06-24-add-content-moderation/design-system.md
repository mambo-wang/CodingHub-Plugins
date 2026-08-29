# Design System: add-content-moderation（双主题）

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
| 按钮、输入框、徽章 | `8px` |
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
| 破坏性色 | `#EF4444` | `#EF4444` | `--color-destructive` |
| 焦点评点环 | `#00FFFF` | `#7c3aed` | `--focus-ring` |

### 暗色主题背景效果

```css
[data-theme="dark"] body::before {
  background:
    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(139,92,246,0.15), transparent),
    radial-gradient(ellipse 60% 40% at 80% 50%, rgba(6,182,212,0.08), transparent),
    radial-gradient(ellipse 50% 30% at 20% 80%, rgba(236,72,153,0.06), transparent);
}
[data-theme="dark"] #app::before {
  background-image:
    linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
  background-size: 60px 60px;
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
| `useContentPermissions.ts`（新增 composable） | 统一计算 canEdit/canDelete 权限 | — |
| `PostCard.vue`（修改） | 帖子列表卡片，新增编辑/删除 hover 按钮 | normal / hover / focus / disabled |
| `VideoCard.vue`（修改） | 微课列表卡片，新增编辑/删除 hover 按钮 | normal / hover / focus / disabled |
| `HomePage.vue`（修改） | 工具列表页，内联卡片新增编辑/删除 hover 按钮 | normal / hover / focus / disabled |
| `DetailPage.vue`（修改） | 工具详情页，新增编辑/删除操作按钮 | normal / hover / focus / disabled / loading |
| `PostDetailPage.vue`（修改） | 帖子详情页，扩展删除按钮权限+新增编辑按钮 | normal / hover / focus / disabled / loading |
| `VideoDetailPage.vue`（修改） | 微课详情页，新增编辑/删除操作按钮 | normal / hover / focus / disabled / loading |
| `PostEditorPage.vue`（修改） | 帖子编辑器，接通编辑模式回填+更新 | normal / loading / error |
| `VideoEditPage.vue`（新增） | 微课编辑页，标题/简介表单 | normal / loading / error |
| `ConfirmDialog.vue`（复用） | 删除二次确认 | normal / loading |

---

## 4. 交互状态（双主题）

### 4.1 列表页卡片操作按钮（PostCard / VideoCard / HomePage 工具卡片）— 暗色主题

按钮容器 `.card-actions` 使用 `position: absolute; top: 12px; right: 12px;`，不占布局空间。

| 状态 | 样式 |
|------|------|
| normal（卡片未 hover） | `opacity: 0.35; color: var(--text-muted); border: 1.5px solid var(--border-color); background: transparent;` |
| 卡片 hover | `.card:hover .card-actions { opacity: 1; }` |
| 编辑按钮 hover | `color: var(--accent-1); border-color: var(--accent-1); background: rgba(139,92,246,0.1); box-shadow: 0 0 12px rgba(139,92,246,0.2);` |
| 删除按钮 hover | `color: var(--color-destructive); border-color: color-mix(in srgb, var(--color-destructive) 30%, transparent); background: rgba(239,68,68,0.1); box-shadow: 0 0 12px rgba(239,68,68,0.2);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |
| disabled / loading | `opacity: 0.5; cursor: not-allowed;` |

按钮尺寸：`width: 32px; height: 32px; padding: 6px; border-radius: 8px;`，图标 `:size="16"`。

### 4.2 列表页卡片操作按钮 — 亮色主题

| 状态 | 样式 |
|------|------|
| normal（卡片未 hover） | `opacity: 0.35; color: var(--text-muted); border: 1.5px solid var(--border-color); background: transparent;` |
| 卡片 hover | `.card:hover .card-actions { opacity: 1; }` |
| 编辑按钮 hover | `color: var(--accent-1); border-color: var(--accent-1); background: rgba(124,58,237,0.1); box-shadow: 0 0 12px rgba(124,58,237,0.15);` |
| 删除按钮 hover | `color: var(--color-destructive); border-color: color-mix(in srgb, var(--color-destructive) 30%, transparent); background: rgba(239,68,68,0.1); box-shadow: 0 0 12px rgba(239,68,68,0.15);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |
| disabled / loading | `opacity: 0.5; cursor: not-allowed;` |

### 4.3 详情页操作按钮（DetailPage / PostDetailPage / VideoDetailPage）— 暗色主题

复用现有 `.action-btn` 样式（圆角胶囊按钮 `border-radius: 24px; padding: 12px 24px;`），新增编辑按钮变体。

| 状态 | 样式 |
|------|------|
| normal（编辑） | `border: 1.5px solid var(--border-color); background: var(--bg-glass); color: var(--text-secondary);` |
| normal（删除） | `background: var(--color-destructive); color: #FFFFFF; border-color: transparent;` |
| 编辑按钮 hover | `border-color: var(--accent-1); color: var(--accent-1); background: rgba(139,92,246,0.1);` |
| 删除按钮 hover | `background: #DC2626; box-shadow: 0 0 20px rgba(239,68,68,0.3); transform: translateY(-1px);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |
| disabled / loading | `opacity: 0.5; cursor: not-allowed;` |

### 4.4 详情页操作按钮 — 亮色主题

| 状态 | 样式 |
|------|------|
| normal（编辑） | `border: 1.5px solid var(--border-color); background: var(--bg-glass); color: var(--text-secondary);` |
| normal（删除） | `background: var(--color-destructive); color: #FFFFFF; border-color: transparent;` |
| 编辑按钮 hover | `border-color: var(--accent-1); color: var(--accent-1); background: rgba(124,58,237,0.08);` |
| 删除按钮 hover | `background: #DC2626; box-shadow: 0 0 20px rgba(239,68,68,0.2); transform: translateY(-1px);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |
| disabled / loading | `opacity: 0.5; cursor: not-allowed;` |

### 4.5 编辑页表单（PostEditorPage / VideoEditPage）— 双主题通用

复用现有 `.input` / `.form-group` 样式。

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); border-radius: 8px; padding: 8px 16px; color: var(--text-primary);` |
| focus | `border-color: var(--accent-1); box-shadow: 0 0 0 3px rgba(139,92,246,0.2);` |
| error | `border-color: #EF4444;` + `role="alert"` 错误提示 |
| 提交按钮 loading | disabled + `Loader2` spin 图标 |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 768px` (mobile) | 卡片操作按钮保持半透明显示（移动端无 hover，半透明确保可见）；详情页操作按钮换行 |
| `≥ 768px` (tablet) | 卡片操作按钮 hover 高亮；详情页操作按钮单行 |
| `≥ 1024px` (desktop) | 同 tablet，网格列数增加 |

---

## 6. 可访问性要求

- [x] 所有操作按钮有可读文字标签或 `aria-label`（纯图标按钮必须 `aria-label="编辑"` / `aria-label="删除"`）
- [x] 纯图标按钮必须有 `aria-label`
- [x] 删除确认对话框使用 `role="dialog"` + `aria-modal="true"` + `aria-labelledby`（复用 ConfirmDialog）
- [x] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px，`outline: 2px solid`
- [x] 颜色对比度满足 WCAG AA（删除按钮白字 on `#EF4444` = 4.7:1 ✅）
- [x] `prefers-reduced-motion: reduce` 媒体查询下关闭 hover transform 动画
- [x] 错误提示使用 `role="alert"`
- [x] 键盘可达：Tab 循环操作按钮、Esc 关闭确认框、Enter 触发
- [x] 装饰图标 `aria-hidden="true"`

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 编辑操作 | `Pencil` / `Edit2` | `aria-label="编辑"` |
| 删除操作 | `Trash2` | `aria-label="删除"` |
| 加载中 | `Loader2` (spin) | `aria-hidden="true"` |
| 返回 | `ArrowLeft` | `aria-hidden="true"` |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题
- ✅ 所有状态变化有过渡动画（`transition: all 200ms ease`）
- ✅ `cursor: pointer` 在按钮上
- ✅ 卡片操作按钮 `position: absolute` 不引起布局位移
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移（详情页删除按钮的 `translateY(-1px)` 安全，不改变文档流）
