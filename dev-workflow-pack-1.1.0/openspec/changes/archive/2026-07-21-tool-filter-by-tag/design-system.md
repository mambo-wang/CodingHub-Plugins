# Design System: tool-filter-by-tag（双主题）

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
| 标签 Pill（按钮类） | `8px` |
| 筛选栏容器 | `16px` |

### 阴影

| Level | 暗色值 | 亮色值 |
|-------|--------|--------|
| `--shadow-sm` | `0 2px 8px rgba(0,0,0,0.3)` | `0 2px 8px rgba(0,0,0,0.08)` |
| `--shadow-glow` | `0 0 40px rgba(139,92,246,0.15)` | `0 0 40px rgba(124,58,237,0.1)` |

---

## 2. 双主题 Tokens 映射

| 角色 | 暗色主题 | 亮色主题 | CSS 变量 |
|------|----------|----------|----------|
| 页面背景 | `#09090b` | `#f8fafc` | `--bg-primary` |
| 毛玻璃 | `rgba(255,255,255,0.03)` | `rgba(255,255,255,0.8)` | `--bg-glass` |
| 主色 (紫) | `#8b5cf6` | `#7c3aed` | `--accent-1` |
| 辅助色 (青) | `#06b6d4` | `#0891b2` | `--accent-2` |
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
| `HomePage.vue`（修改） | 搜索栏旁新增标签下拉选择框 | closed / open / hover / selected / loading |
| `TagBadge.vue`（修改） | 工具卡片标签增加可选点击交互 | normal / hover / clickable |

---

## 4. 交互状态（双主题）

### 4.1 标签下拉选择框（触发器）— 暗色主题

| 状态 | 样式 |
|------|------|
| closed (未选中) | `background: var(--bg-glass); border: 1px solid var(--border-color); color: var(--text-secondary); border-radius: 8px; padding: 10px 16px; font-size: 14px;` 显示"标签: 全部标签" + chevron 图标 |
| closed (已选中) | 同上，文字变为 `color: var(--accent-1); font-weight: 500;` 显示"标签: {标签名}" |
| hover | `border-color: var(--accent-1); color: var(--accent-1);` |
| open | `border-color: var(--accent-1); box-shadow: 0 0 0 3px rgba(139,92,246,0.1);` chevron 旋转 180° |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |
| loading | `opacity: 0.6; pointer-events: none;` |

### 4.2 标签下拉选择框（触发器）— 亮色主题

| 状态 | 样式 |
|------|------|
| closed (未选中) | `background: var(--bg-glass); border: 1px solid var(--border-color); color: var(--text-secondary); border-radius: 8px; padding: 10px 16px; font-size: 14px;` 显示"标签: 全部标签" + chevron 图标 |
| closed (已选中) | 同上，文字变为 `color: var(--accent-1); font-weight: 500;` 显示"标签: {标签名}" |
| hover | `border-color: var(--accent-1); color: var(--accent-1);` |
| open | `border-color: var(--accent-1); box-shadow: 0 0 0 3px rgba(124,58,237,0.08);` chevron 旋转 180° |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |
| loading | `opacity: 0.6; pointer-events: none;` |

### 4.3 下拉面板（选项列表）— 暗色主题

| 状态 | 样式 |
|------|------|
| 面板容器 | `background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 12px; box-shadow: var(--shadow-md); padding: 8px; max-height: 320px; overflow-y: auto;` |
| 选项 normal | `padding: 10px 14px; border-radius: 8px; color: var(--text-secondary); font-size: 14px;` 左侧 radio 圆圈 `border: 1.5px solid var(--text-muted);` |
| 选项 hover | `background: rgba(139,92,246,0.08); color: var(--text-primary);` |
| 选项 selected | `color: var(--accent-1); font-weight: 600;` radio 填充 `background: var(--accent-1);` |

### 4.4 下拉面板（选项列表）— 亮色主题

| 状态 | 样式 |
|------|------|
| 面板容器 | `background: #ffffff; border: 1px solid var(--border-color); border-radius: 12px; box-shadow: var(--shadow-md); padding: 8px; max-height: 320px; overflow-y: auto;` |
| 选项 normal | `padding: 10px 14px; border-radius: 8px; color: var(--text-secondary); font-size: 14px;` 左侧 radio 圆圈 `border: 1.5px solid var(--text-muted);` |
| 选项 hover | `background: rgba(124,58,237,0.06); color: var(--text-primary);` |
| 选项 selected | `color: var(--accent-1); font-weight: 600;` radio 填充 `background: var(--accent-1);` |

### 4.5 TagBadge（可点击模式）— 暗色主题

| 状态 | 样式 |
|------|------|
| normal | 现有 TagBadge 样式不变 |
| hover (clickable) | `cursor: pointer; border-color: var(--accent-1); transform: translateY(-1px);` |

### 4.6 TagBadge（可点击模式）— 亮色主题

| 状态 | 样式 |
|------|------|
| normal | 现有 TagBadge 样式不变 |
| hover (clickable) | `cursor: pointer; border-color: var(--accent-1); transform: translateY(-1px);` |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 640px` (mobile) | 下拉选择框与搜索框纵向堆叠（各占一行） |
| `≥ 640px` (tablet) | 下拉选择框与搜索框同行，选择框固定宽度 |
| `≥ 1024px` (desktop) | 同 tablet |

---

## 6. 可访问性要求

- [x] 触发器使用 `<button>` 元素，`aria-haspopup="listbox"` + `aria-expanded`
- [x] 面板使用 `role="listbox"`，选项使用 `role="option"` + `aria-selected`
- [x] 键盘操作：Enter/Space 展开，方向键导航，Esc 关闭
- [x] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px
- [x] 颜色对比度满足 WCAG AA
- [x] `prefers-reduced-motion: reduce` 下关闭动画
- [x] 装饰图标 `aria-hidden="true"`

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 下拉触发器 chevron | `ChevronDown` | `aria-hidden="true"` |
| 标签筛选标识（可选） | `Tag` | `aria-hidden="true"` |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题
- ✅ 所有状态变化有过渡动画（`transition: all 0.2s`）
- ✅ `cursor: pointer` 在可点击元素上
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移（仅用 `translateY(-1px)`）
