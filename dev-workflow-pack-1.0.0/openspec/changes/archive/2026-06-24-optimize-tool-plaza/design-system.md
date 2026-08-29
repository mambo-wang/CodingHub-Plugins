# Design System: optimize-tool-plaza（双主题）

> 引用全局设计系统 `design-system/CodingHub/MASTER.md`，仅列出本次变更涉及的 UI 组件、交互状态与可访问性约束。

## 1. 全局样式引用

### 字体

| 角色 | 字体 | CSS 变量 |
|------|------|----------|
| 标题/按钮/正文 | Sora (300–800 weight) | `var(--font-display)` |
| 代码/统计数字 | Space Mono (400, 700 weight) | `var(--font-mono)` |

### 圆角

| 元素 | 值 |
|------|-----|
| 按钮、输入框、徽章 | `8px` |
| Pill 标签 | `20px` |
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

---

## 3. 涉及组件清单

| 组件/页面 | 用途 | 状态覆盖 |
|-----------|------|----------|
| `HomePage.vue`（修改） | 工具广场主页面，新增 Tab pill 切换和上传 Modal | normal / loading / empty / tab-active |
| `AppHeader.vue`（修改） | 移除「我的工具」导航项 | normal |
| `UploadModal`（新增内联） | 上传工具弹窗，复用 UploadPage 表单 | normal / uploading / success / error |
| `GeneralizedSidebar`（不再引用） | 工具页面移除侧边栏引用 | — |

---

## 4. 交互状态（双主题）

### 4.1 Tab Pill（个人 pills: 我的收藏 / 我的工具） — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); color: #a1a1aa; border-radius: 20px;` |
| hover | `background: rgba(139,92,246,0.1); border-color: rgba(139,92,246,0.3); color: #fafafa;` |
| active | `background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(6,182,212,0.2)); border-color: rgba(139,92,246,0.4); color: #fafafa; box-shadow: 0 0 20px rgba(139,92,246,0.15);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |

### 4.2 Tab Pill — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: rgba(255,255,255,0.8); border: 1px solid rgba(0,0,0,0.08); color: #475569; border-radius: 20px;` |
| hover | `background: rgba(124,58,237,0.08); border-color: rgba(124,58,237,0.3); color: #0f172a;` |
| active | `background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(8,145,178,0.15)); border-color: rgba(124,58,237,0.4); color: #0f172a;` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |

### 4.3 上传图标按钮 — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(6,182,212,0.2)); border: 1px solid rgba(139,92,246,0.3); color: #8b5cf6; width: 36px; height: 36px; border-radius: 20px;` |
| hover | `background: linear-gradient(135deg, rgba(139,92,246,0.3), rgba(6,182,212,0.3)); border-color: rgba(139,92,246,0.5); box-shadow: 0 0 16px rgba(139,92,246,0.2);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |

### 4.4 上传图标按钮 — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: linear-gradient(135deg, rgba(124,58,237,0.15), rgba(8,145,178,0.15)); border: 1px solid rgba(124,58,237,0.3); color: #7c3aed;` |
| hover | `background: linear-gradient(135deg, rgba(124,58,237,0.25), rgba(8,145,178,0.25)); border-color: rgba(124,58,237,0.5);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |

### 4.5 上传 Modal — 暗色主题

| 状态 | 样式 |
|------|------|
| overlay | `background: rgba(0,0,0,0.7); backdrop-filter: blur(4px);` |
| modal | `background: var(--bg-glass); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; max-width: 720px; max-height: 85vh; overflow-y: auto;` |
| submitting | 提交按钮显示 loading spinner，`opacity: 0.5; pointer-events: none;` |

### 4.6 上传 Modal — 亮色主题

| 状态 | 样式 |
|------|------|
| overlay | `background: rgba(0,0,0,0.4); backdrop-filter: blur(4px);` |
| modal | `background: rgba(255,255,255,0.95); border: 1px solid rgba(0,0,0,0.08); border-radius: 16px;` |
| submitting | 同暗色 |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 640px` (mobile) | filter bar 改为纵向堆叠；分类 pills 隐藏，仅显示 Tab pills + 搜索 + 上传按钮 |
| `≥ 640px` (tablet) | filter bar 单行，pills 可换行；上传按钮保持在最右 |
| `≥ 1024px` (desktop) | 完整展示所有 pills，工具网格 `repeat(auto-fill, minmax(300px, 1fr))` |

---

## 6. 可访问性要求

- [x] 所有按钮有可读文字标签或 `aria-label`
- [x] 纯图标上传按钮必须有 `aria-label="上传工具"`
- [x] Modal 使用 `role="dialog"` + `aria-modal="true"` + `aria-labelledby`
- [x] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px，`outline: 2px solid`
- [x] 颜色对比度满足 WCAG AA（pills 文字对背景 ≥ 4.5:1）
- [x] `prefers-reduced-motion: reduce` 媒体查询下关闭动画
- [x] 键盘可达：Tab 循环在 Modal 内、Esc 关闭 Modal、Enter 触发提交
- [x] 装饰图标 `aria-hidden="true"`

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 上传工具 | `Upload` | `aria-label="上传工具"` |
| 我的收藏 pill | `Bookmark` | `aria-hidden="true"` |
| 我的工具 pill | `Wrench` | `aria-hidden="true"` |
| Modal 关闭 | `X` | `aria-label="关闭"` |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题
- ✅ 所有状态变化有 `transition` 动画
- ✅ `cursor: pointer` 在按钮上
- ✅ Pill 复用现有 `.category-pill` 样式类，保持视觉一致
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移
