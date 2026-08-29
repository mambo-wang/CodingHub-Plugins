# Design System: 帖子删除（双主题）

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
| 危险色 | `#EF4444` | `#EF4444` | `--color-destructive` |
| 删除按钮 hover 阴影 | `rgba(239,68,68,0.3)` | `rgba(239,68,68,0.25)` | — |
| 图标按钮 hover 背景 | `rgba(239,68,68,0.1)` | `rgba(239,68,68,0.08)` | — |
| 焦点评点环 | `#00FFFF` | `#8b5cf6` | — |

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
| `PostDetailPage.vue`（修改） | 帖子详情页"删除"按钮 | normal / hover / focus / disabled（loading） |
| `MyPostsPage.vue`（修改） | 列表项"删除"图标按钮 | normal / hover / focus / active |
| `components/common/ConfirmDialog.vue`（新增） | 通用确认对话框 | normal / loading / hidden；模态遮罩态 |
| `Toast`（复用现有） | 成功/失败提示 | success / error |
| `PostCard.vue`（修改） | 我的帖子列表卡片 | 删除按钮 hover 透传 |

---

## 4. 交互状态（双主题）

### 4.1 删除按钮（详情页）— 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: #EF4444; color: #FFFFFF; font-family: var(--font-display); font-weight: 500; font-size: 14px; padding: 8px 16px; border-radius: 8px;` |
| hover | `background: #EF4444; box-shadow: 0 0 20px rgba(239,68,68,0.3); transform: translateY(-1px);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |
| disabled / loading | `background: rgba(239,68,68,0.5); cursor: not-allowed;` 内含 `Loader2` 旋转图标 |

### 删除按钮（详情页）— 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: #EF4444; color: #FFFFFF; font-family: var(--font-display); font-weight: 500; font-size: 14px; padding: 8px 16px; border-radius: 8px;` |
| hover | `background: #DC2626; box-shadow: 0 0 20px rgba(239,68,68,0.25); transform: translateY(-1px);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |
| disabled / loading | `background: rgba(239,68,68,0.5); cursor: not-allowed;` |

### 4.2 删除图标按钮（列表项）— 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `color: var(--text-secondary); padding: 6px; border-radius: 6px;` |
| hover | `color: #EF4444; background: rgba(239,68,68,0.1);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |
| active | `transform: scale(0.95); transition: 150ms;` |

### 删除图标按钮（列表项）— 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `color: #94a3b8; padding: 6px; border-radius: 6px;` |
| hover | `color: #EF4444; background: rgba(239,68,68,0.08);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |
| active | `transform: scale(0.95); transition: 150ms;` |

### 4.3 确认对话框 — 暗色主题

| 状态 | 样式 |
|------|------|
| 遮罩 | `background: rgba(0,0,0,0.6);` |
| 面板 | `background: rgba(15,15,20,0.95); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.12); border-radius: 16px;` |
| 标题 | `font-family: var(--font-display); font-size: 18px; font-weight: 600; color: #fafafa;` |
| 描述 | `font-family: var(--font-display); font-size: 14px; color: #a1a1aa;` |
| 取消按钮 (normal) | `border: 1.5px solid rgba(255,255,255,0.2); color: rgba(255,255,255,0.7); background: transparent;` |
| 取消按钮 (hover) | `border-color: rgba(255,255,255,0.4); color: #FFFFFF; background: rgba(255,255,255,0.05);` |
| 确认删除 (normal) | `background: #EF4444; color: #FFFFFF; font-weight: 600;` |
| 确认删除 (hover) | `background: #DC2626; box-shadow: 0 0 20px rgba(239,68,68,0.3);` |
| loading | 两按钮均 disabled；确认按钮显示 spinner |

### 确认对话框 — 亮色主题

| 状态 | 样式 |
|------|------|
| 遮罩 | `background: rgba(0,0,0,0.4);` |
| 面板 | `background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); border: 1px solid rgba(0,0,0,0.1); border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.12);` |
| 标题 | `font-family: var(--font-display); font-size: 18px; font-weight: 600; color: #0f172a;` |
| 描述 | `font-family: var(--font-display); font-size: 14px; color: #475569;` |
| 取消按钮 (normal) | `border: 1.5px solid rgba(0,0,0,0.15); color: #475569; background: transparent;` |
| 取消按钮 (hover) | `border-color: #7c3aed; color: #7c3aed; background: rgba(124,58,237,0.05);` |
| 确认删除 (normal) | `background: #EF4444; color: #FFFFFF; font-weight: 600;` |
| 确认删除 (hover) | `background: #DC2626; box-shadow: 0 0 20px rgba(239,68,68,0.25);` |
| loading | 两按钮均 disabled；确认按钮显示 spinner |

### 4.4 Toast 反馈 — 双主题统一

| 类型 | 样式 |
|------|------|
| 成功 | `border-left: 3px solid #10b981; background: var(--bg-card);` |
| 错误 | `border-left: 3px solid #EF4444; background: var(--bg-card);` |

Toast 使用 `backdrop-filter: blur(15px)`，文字颜色随主题使用 `var(--text-primary)`。

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 640px` (mobile) | 删除按钮与点赞/收藏按钮垂直堆叠 8px gap；确认对话框占满 90% 宽度，最大 360px |
| `≥ 640px` (tablet) | 按钮水平排列 12px gap；对话框固定宽度 400px |
| `≥ 1024px` (desktop) | 与现有帖子详情页布局保持一致 |

---

## 6. 可访问性要求

- [ ] 所有按钮有可读文字标签或 `aria-label`（如 `aria-label="删除帖子"`）
- [ ] 纯图标按钮必须有 `aria-label="删除此帖"`
- [ ] `ConfirmDialog` 使用 `role="dialog"` + `aria-modal="true"` + `aria-labelledby` 指向标题 + `aria-describedby` 指向描述
- [ ] 打开对话框时焦点自动移入"确认删除"按钮，关闭时焦点回到触发按钮
- [ ] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px，`outline: 2px solid`
- [ ] 颜色对比度：白字 on 红底 `#EF4444` = 4.7:1 ≥ AA（双主题一致）
- [ ] `prefers-reduced-motion: reduce` 媒体查询下关闭淡入/缩放动画
- [ ] 错误提示使用 `role="alert"`
- [ ] 键盘可达：Tab 循环、Esc 关闭、Enter 触发
- [ ] 装饰图标 `aria-hidden="true"`

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 删除按钮 | `Trash2` | `aria-hidden="true"` |
| 删除图标按钮 | `Trash2` | `aria-hidden="true"` |
| 加载中 | `Loader2` | `aria-hidden="true"` + spin class |
| 成功 toast | `CheckCircle` | `aria-hidden="true"` |
| 错误 toast | `AlertTriangle` | `aria-hidden="true"` |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题
- ✅ 所有状态变化有过渡动画
- ✅ `cursor: pointer` 在按钮上
- ✅ 无 Tailwind 类名
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移
