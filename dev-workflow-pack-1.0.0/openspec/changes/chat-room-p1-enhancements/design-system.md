# Design System: Chat Room P1 Enhancements（双主题）

> 引用全局设计系统 `design-system/CodingHub/MASTER.md`，仅列出本次 P1 变更涉及的 UI 组件、交互状态与可访问性约束。

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
| 按钮、输入框、徽章、reaction 气泡 | `8px` |
| 卡片、引用块、代码块 | `16px` |

### 阴影

| Level | 暗色值 | 亮色值 |
|-------|--------|--------|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.4)` | `0 1px 2px rgba(15,23,42,0.1)` |
| `--shadow-md` | `0 4px 16px rgba(0,0,0,0.5)` | `0 4px 16px rgba(15,23,42,0.12)` |
| `--shadow-glow` | `0 0 20px rgba(139,92,246,0.4)` | `0 0 20px rgba(124,58,237,0.3)` |

---

## 2. 双主题 Tokens 映射

| 角色 | 暗色主题 | 亮色主题 | CSS 变量 |
|------|----------|----------|----------|
| 页面背景 | `#09090b` | `#f8fafc` | `--bg-primary` |
| 面板/侧栏 | `#0f0f12` | `#f1f5f9` | `--bg-secondary` |
| 卡片背景 | `#0f0f12cc` | `#ffffffe6` | `--bg-card` |
| 毛玻璃 | `rgba(255,255,255,0.03)` | `rgba(255,255,255,0.8)` | `--bg-glass` |
| 主色 (紫) | `#8b5cf6` | `#7c3aed` | `--accent-1` |
| 辅助色 (青) | `#06b6d4` | `#0891b2` | `--accent-2` |
| 第三色 (粉) | `#ec4899` | `#db2777` | `--accent-3` |
| 主文字 | `#fafafa` | `#0f172a` | `--text-primary` |
| 次文字 | `#a1a1aa` | `#475569` | `--text-secondary` |
| 辅助文字 | `#52525b` | `#94a3b8` | `--text-muted` |
| 边框色 | `rgba(255,255,255,0.08)` | `rgba(0,0,0,0.08)` | `--border-color` |
| 发光边框 | `rgba(139,92,246,0.3)` | `rgba(124,58,237,0.3)` | `--border-glow` |
| 焦点评点环 | `#00FFFF` | `#7c3aed` | `--focus-ring` |

---

## 3. 涉及组件清单

| 组件/页面 | 用途 | 状态覆盖 |
|-----------|------|----------|
| `components/chat/ChatRoom.vue`（修改） | 消息列表容器，接入 typing/reactions/edit/recall 渲染与订阅 | loading / empty / error |
| `components/chat/TypingIndicator.vue`（新增） | 展示「{displayName} 正在输入…」动画 | normal / hidden |
| `components/chat/MessageReactions.vue`（新增） | emoji 计数徽章 + 表情面板入口 | normal / hover / active(已回应) |
| `components/chat/MessageMarkdown.vue`（新增） | Markdown/代码块安全渲染 | normal / code-block / copy |
| `components/chat/ReplyQuote.vue`（新增） | 引用摘要块（可点击跳转） | normal / deleted(占位) |
| `components/chat/MessageActions.vue`（新增或并入 ChatRoom） | 悬浮操作菜单：回复 / 表情 / 编辑 / 撤回 | normal / hover / open / disabled |

---

## 4. 交互状态（双主题）

### 4.1 `MessageReactions` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | 半透明徽章 `rgba(255,255,255,0.05)`，`--text-secondary` |
| hover | 边框 `--border-glow`，轻微提亮 |
| active（已回应） | 背景 `rgba(139,92,246,0.18)`，文字 `--accent-1`，`--shadow-sm` |

### 4.2 `MessageReactions` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `rgba(15,23,42,0.04)`，文字 `--text-secondary` |
| hover | 边框 `--border-glow` |
| active（已回应） | 背景 `rgba(124,58,237,0.14)`，文字 `--accent-1` |

### 4.3 `TypingIndicator` — 双主题

| 状态 | 样式 |
|------|------|
| normal | 三点跳动动画（CSS keyframes），文字 `--text-muted` |
| hidden | `display:none` |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 640px` (mobile) | 操作菜单改为长按/长按气泡弹出；reaction 面板半屏底部抽屉 |
| `≥ 640px` (tablet) | 操作菜单 hover 气泡右侧显示；引用块内联 |
| `≥ 1024px` (desktop) | 完整布局，代码块最大宽度受限并横向滚动 |

---

## 6. 可访问性要求

- [ ] 所有操作按钮有可读文字或 `aria-label`（表情/编辑/撤回/回复）
- [ ] 纯图标按钮必须有 `aria-label`
- [ ] 模态（表情面板）使用 `role="dialog"` + `aria-modal="true"`
- [ ] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px
- [ ] 颜色对比度满足 WCAG AA
- [ ] `prefers-reduced-motion: reduce` 下关闭 typing 动画与高亮过渡
- [ ] 代码块复制按钮 `aria-label="复制代码"`
- [ ] 键盘可达：Tab 循环、Esc 关闭表情面板、Enter 发送
- [ ] 装饰图标 `aria-hidden="true"`

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 回复 | `Reply` | `aria-hidden="true"` |
| 表情 | `Smile` | `aria-hidden="true"` |
| 编辑 | `Pencil` | `aria-hidden="true"` |
| 撤回 | `Undo2` | `aria-hidden="true"` |
| 复制代码 | `Copy` | `aria-label="复制代码"` |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji 作为 UI 图标（emoji 仅作为用户回应内容）
- ✅ 使用 CSS 变量实现双主题
- ✅ 所有状态变化有过渡动画
- ✅ `cursor: pointer` 在可点击元素上
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移
- ❌ 禁止 `v-html` 渲染未经 DOMPurify 净化的内容（XSS 红线）
