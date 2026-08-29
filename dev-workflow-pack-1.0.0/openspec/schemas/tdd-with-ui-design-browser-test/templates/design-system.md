# Design System: [变更名称]（双主题）

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
| `--shadow-sm` | `<暗色值>` | `<亮色值>` |
| `--shadow-md` | `<暗色值>` | `<亮色值>` |
| `--shadow-glow` | `<暗色值>` | `<亮色值>` |

---

## 2. 双主题 Tokens 映射

| 角色 | 暗色主题 | 亮色主题 | CSS 变量 |
|------|----------|----------|----------|
| 页面背景 | `#09090b` | `#f8fafc` | `--bg-primary` |
| 面板/侧栏 | `#0f0f12` | `#f1f5f9` | `--bg-secondary` |
| 卡片背景 | `<暗色值>` | `<亮色值>` | `--bg-card` |
| 毛玻璃 | `<暗色值>` | `<亮色值>` | `--bg-glass` |
| 主色 (紫) | `#8b5cf6` | `#7c3aed` | `--accent-1` |
| 辅助色 (青) | `#06b6d4` | `#0891b2` | `--accent-2` |
| 第三色 (粉) | `#ec4899` | `#db2777` | `--accent-3` |
| 主文字 | `#fafafa` | `#0f172a` | `--text-primary` |
| 次文字 | `#a1a1aa` | `#475569` | `--text-secondary` |
| 辅助文字 | `#52525b` | `#94a3b8` | `--text-muted` |
| 边框色 | `<暗色值>` | `<亮色值>` | `--border-color` |
| 发光边框 | `<暗色值>` | `<亮色值>` | `--border-glow` |
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
| `<ComponentName.vue>`（新增/修改） | `<用途描述>` | normal / hover / focus / disabled / loading / empty / error |

---

## 4. 交互状态（双主题）

### 4.1 `<组件名>` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `<CSS 样式>` |
| hover | `<CSS 样式>` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |
| disabled / loading | `<CSS 样式>` |

### 4.2 `<组件名>` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `<CSS 样式>` |
| hover | `<CSS 样式>` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |
| disabled / loading | `<CSS 样式>` |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 640px` (mobile) | `<布局行为>` |
| `≥ 640px` (tablet) | `<布局行为>` |
| `≥ 1024px` (desktop) | `<布局行为>` |

---

## 6. 可访问性要求

- [ ] 所有按钮有可读文字标签或 `aria-label`
- [ ] 纯图标按钮必须有 `aria-label`
- [ ] 模态组件使用 `role="dialog"` + `aria-modal="true"` + `aria-labelledby`
- [ ] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px，`outline: 2px solid`
- [ ] 颜色对比度满足 WCAG AA
- [ ] `prefers-reduced-motion: reduce` 媒体查询下关闭动画
- [ ] 错误提示使用 `role="alert"`
- [ ] 键盘可达：Tab 循环、Esc 关闭、Enter 触发
- [ ] 装饰图标 `aria-hidden="true"`

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| `<用途>` | `<IconName>` | `aria-hidden="true"` |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题
- ✅ 所有状态变化有过渡动画
- ✅ `cursor: pointer` 在按钮上
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移
