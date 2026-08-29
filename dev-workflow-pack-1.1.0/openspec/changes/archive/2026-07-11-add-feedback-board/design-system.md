# Design System: add-feedback-board（双主题）

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
| 焦点环 | `#00FFFF` | `#7c3aed` | `--focus-ring` |
| 错误色 | `#EF4444` | `#EF4444` | — |

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
| `FeedbackPage.vue`（新增） | 留言板主页面，包含表单和列表 | normal / loading / empty / error |
| `FeedbackForm.vue`（新增） | 留言提交表单（内容+昵称+联系方式+分类） | normal / submitting / success / error |
| `FeedbackCard.vue`（新增） | 单条留言卡片（含管理员回复区域） | normal / replied / deleted(admin) |
| `CategoryBadge.vue`（新增） | 分类标签徽章 | normal |

---

## 4. 交互状态（双主题）

### 4.1 `FeedbackForm` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | textarea: `background: var(--bg-glass); border: 1px solid var(--border-color); border-radius: 8px; color: var(--text-primary);` |
| hover | `border-color: rgba(255,255,255,0.15);` |
| focus | `border-color: var(--accent-1); box-shadow: 0 0 0 3px rgba(139,92,246,0.2);` |
| submitting | 提交按钮显示 `Loader2` spin，按钮 disabled |
| success | 表单清空，顶部 toast 成功提示（`var(--accent-2)` 色） |
| error | textarea `border-color: #EF4444; box-shadow: 0 0 0 3px rgba(239,68,68,0.2);` |

### 4.2 `FeedbackForm` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | textarea: `background: var(--bg-glass); border: 1px solid var(--border-color); border-radius: 8px; color: var(--text-primary);` |
| hover | `border-color: rgba(0,0,0,0.15);` |
| focus | `border-color: var(--accent-1); box-shadow: 0 0 0 3px rgba(124,58,237,0.15);` |
| submitting | 同暗色 |
| success | 同暗色 |
| error | 同暗色 |

### 4.3 `FeedbackCard` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); border-radius: 16px; backdrop-filter: blur(20px);` |
| hover | `border-color: var(--border-glow); box-shadow: var(--shadow-glow); transform: translateY(-2px);` |
| replied | 回复区域：`background: rgba(139,92,246,0.06); border-left: 3px solid var(--accent-1); padding: 12px 16px; border-radius: 0 8px 8px 0;` |
| admin-hover | 回复/删除按钮浮现，`color: var(--text-muted);` hover 变 `var(--text-primary)` |

### 4.4 `FeedbackCard` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); border-radius: 16px;` |
| hover | `border-color: var(--border-glow); box-shadow: var(--shadow-glow); transform: translateY(-2px);` |
| replied | 回复区域：`background: rgba(124,58,237,0.05); border-left: 3px solid var(--accent-1); padding: 12px 16px; border-radius: 0 8px 8px 0;` |
| admin-hover | 同暗色 |

### 4.5 `CategoryBadge` — 双主题

| 状态 | 样式 |
|------|------|
| SUGGESTION | `background: rgba(139,92,246,0.12); color: var(--accent-1); border: 1px solid rgba(139,92,246,0.2);` |
| BUG_REPORT | `background: rgba(239,68,68,0.1); color: #EF4444; border: 1px solid rgba(239,68,68,0.2);` |
| PRAISE | `background: rgba(6,182,212,0.12); color: var(--accent-2); border: 1px solid rgba(6,182,212,0.2);` |
| OTHER | `background: var(--bg-glass); color: var(--text-secondary); border: 1px solid var(--border-color);` |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 768px` (mobile) | 单列布局，表单全宽，卡片全宽，分类筛选改为横向滚动 chips |
| `≥ 768px` (tablet) | 内容区最大宽度 `720px` 居中，表单和卡片保持舒适阅读宽度 |
| `≥ 1024px` (desktop) | 同 tablet 宽度，留言列表区域不扩展更宽 |

---

## 6. 可访问性要求

- [x] 所有按钮有可读文字标签或 `aria-label`
- [x] 纯图标按钮（管理员删除）必须有 `aria-label="删除留言"`
- [x] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px，`outline: 2px solid`
- [x] 颜色对比度满足 WCAG AA（正文 ≥ 4.5:1）
- [x] 错误提示使用 `role="alert"`
- [x] 键盘可达：Tab 循环表单字段，Enter 提交
- [x] 装饰图标 `aria-hidden="true"`
- [x] textarea 有 `<label>` 关联

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 页面标题 | `MessageSquareText` | `aria-hidden="true"` |
| 提交按钮 | `Send` | `aria-hidden="true"` |
| 管理员回复 | `Reply` | `aria-hidden="true"` |
| 管理员删除 | `Trash2` | `aria-label="删除留言"` |
| 已回复标记 | `CheckCircle` | `aria-hidden="true"` |
| 空状态 | `MessageSquareOff` | `aria-hidden="true"` |
| 加载中 | `Loader2` | `aria-label="加载中"` |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题
- ✅ 所有状态变化有过渡动画（150-300ms）
- ✅ `cursor: pointer` 在所有可点击元素上
- ✅ 使用 `.glass-card` 全局样式作为卡片基础
- ✅ 提交按钮三态：idle → loading → success/error
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移
- ❌ 不使用 Tailwind（纯 CSS + CSS 变量）
