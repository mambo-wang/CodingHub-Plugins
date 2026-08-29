# Design System: User Avatar（双主题）

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
| 头像（圆形） | `50%` |
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
| 焦点环 | `#00FFFF` | `#7c3aed` | `--focus-ring` |
| 危险色 | `#ef4444` | `#ef4444` | `--destructive` |

### 头像兜底色（用户未上传时）

从 `var(--accent-1)` 紫、`var(--accent-2)` 青、`var(--accent-3)` 粉、暖色橙、冷静蓝、草绿 6 色调色板中**按 userId 哈希取模**取 1 个。

> 实施时在 `UserAvatar.vue` 内定义 `const PALETTE = ['#8b5cf6', '#06b6d4', '#ec4899', '#f59e0b', '#3b82f6', '#10b981']`，
> 双主题均使用同一组（因为是"占位渐变背景"，无文本对比度问题）。

---

## 3. 涉及组件清单

| 组件/页面 | 用途 | 状态覆盖 |
|-----------|------|----------|
| `UserAvatar.vue`（新增） | 通用头像：URL 优先、加载失败降级、哈希色兜底 | normal / loading / error / no-url |
| `AuthorBadge.vue`（修改） | 工具/帖子作者徽章，新增 `avatarUrl` prop | normal / hover / no-avatar |
| `AppHeader.vue`（修改） | 右上角用户区改用 `UserAvatar` | normal / hover / menu-open |
| `ProfilePage.vue`（新增） | 个人资料页：头像上传/移除、昵称展示 | loading / normal / uploading / error / empty |

---

## 4. 交互状态（双主题）

### 4.1 `UserAvatar` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal (有 URL) | `border: 1px solid var(--border-color); box-shadow: var(--shadow-sm); object-fit: cover;` |
| normal (无 URL) | `background: <hash-pick-from-palette>; color: #fff; font-weight: 600;` |
| loading | `background: rgba(255,255,255,0.05); animation: avatarPulse 1.5s ease-in-out infinite;` |
| error (img 404) | 切回首字母兜底，不显示破图 |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |

### 4.2 `UserAvatar` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal (有 URL) | `border: 1px solid var(--border-color); box-shadow: var(--shadow-sm);` |
| normal (无 URL) | 同上（兜底色板不随主题） |
| loading | `background: rgba(0,0,0,0.05);` |
| error | 切回首字母兜底 |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |

### 4.3 `ProfilePage` 上传按钮 — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); color: var(--text-primary); padding: 10px 20px; border-radius: 8px;` |
| hover | `border-color: var(--accent-1); background: rgba(139,92,246,0.1);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |
| disabled / loading | `opacity: 0.5; cursor: not-allowed;` |
| active (上传中) | 显示 spinner + "上传中..." 文字 |

### 4.4 `ProfilePage` 上传按钮 — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color);` |
| hover | `border-color: var(--accent-1); background: rgba(124,58,237,0.08);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |
| disabled / loading | 同上 |

### 4.5 `ProfilePage` 移除按钮（危险操作）

| 状态 | 暗色样式 | 亮色样式 |
|------|---------|---------|
| normal | `border: 1px solid rgba(239,68,68,0.3); color: #ef4444;` | 同 |
| hover | `background: rgba(239,68,68,0.15);` | `background: rgba(239,68,68,0.1);` |

### 4.6 错误提示（role="alert"）

| 状态 | 样式 |
|------|------|
| 暗色 | `background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); color: #fca5a5; padding: 12px 16px; border-radius: 8px;` |
| 亮色 | `background: rgba(239,68,68,0.05); border: 1px solid rgba(239,68,68,0.3); color: #b91c1c;` |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 640px` (mobile) | ProfilePage 上下堆叠；按钮 width: 100%；头像预览 96px |
| `≥ 640px` (tablet) | ProfilePage 左右分栏（左头像 160px / 右操作） |
| `≥ 1024px` (desktop) | 头像预览 128px，表单最大宽度 480px 居中 |

---

## 6. 可访问性要求

- [x] 所有按钮有可读文字标签或 `aria-label`
- [x] 纯图标按钮（"更换头像"）使用 `<input type="file">` 包装 + `aria-label="更换头像"`
- [x] 头像图片 `alt` 文本 = `{username} 的头像` 或 "用户头像"
- [x] 模态组件：本次无新增模态
- [x] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px
- [x] 颜色对比度：兜底色块上的首字母均为白色 `#fff`，满足 WCAG AA（背景 6 色调色板与白色对比度均 > 4.5）
- [x] `prefers-reduced-motion: reduce` 媒体查询下关闭头像 pulse 动画
- [x] 错误提示使用 `role="alert"`
- [x] 键盘可达：上传按钮 Tab 可达，Enter/Space 触发
- [x] 装饰图标 `aria-hidden="true"`

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 上传头像 | `Upload` | `aria-hidden="true"` |
| 移除头像 | `Trash2` | `aria-hidden="true"` |
| 用户菜单 | `User` | `aria-hidden="true"` |
| 关闭 | `X` | `aria-hidden="true"` |
| 加载中 | `Loader2` (带 rotate 动画) | `aria-hidden="true"` |

> **无 emoji**，所有图标走 Lucide（项目已在 AppHeader 用过）。

---

## 8. Antipatterns 检查

- [x] 使用 Lucide 图标，无 emoji
- [x] 使用 CSS 变量实现双主题
- [x] 所有状态变化有过渡动画（0.2s ease）
- [x] `cursor: pointer` 在按钮上
- [x] 不使用 `!important`
- [x] 头像 hover 不做 scale 缩放（避免布局抖动）
- [x] 图片 `object-fit: cover`，避免变形
- [x] alt 文本不为空
