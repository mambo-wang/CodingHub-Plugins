# Design System: 实时公共聊天室（双主题）

> 引用全局设计系统 `design-system/CodingHub/MASTER.md`，仅列出本次变更涉及的 UI 组件、交互状态与可访问性约束。

## 1. 全局样式引用

### 字体

| 角色 | 字体 | CSS 变量 |
|------|------|----------|
| 标题/按钮/正文 | Sora (300–800 weight) | `var(--font-display)` |
| 代码/统计数字/在线人数 | Space Mono (400, 700 weight) | `var(--font-mono)` |

**导入：**
```css
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');
```

### 圆角

| 元素 | 值 |
|------|-----|
| 按钮、输入框、消息气泡、徽章 | `8px` |
| 聊天卡片、抽屉容器、模态框 | `16px` |

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
| 毛玻璃（抽屉/气泡） | `rgba(255,255,255,0.03)` | `rgba(255,255,255,0.8)` | `--bg-glass` |
| 主色 (紫) | `#8b5cf6` | `#7c3aed` | `--accent-1` |
| 辅助色 (青) | `#06b6d4` | `#0891b2` | `--accent-2` |
| 第三色 (粉) | `#ec4899` | `#db2777` | `--accent-3` |
| 主文字 | `#fafafa` | `#0f172a` | `--text-primary` |
| 次文字 | `#a1a1aa` | `#475569` | `--text-secondary` |
| 辅助文字 | `#52525b` | `#94a3b8` | `--text-muted` |
| 边框色 | `rgba(255,255,255,0.08)` | `rgba(0,0,0,0.08)` | `--border-color` |
| 发光边框 | `rgba(139,92,246,0.3)` | `rgba(124,58,237,0.3)` | `--border-glow` |
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
| `ChatPage.vue`（新增，`/chat`） | 全屏聊天页，入口：顶部导航栏"聊天室" | normal / loading / empty / error |
| `ChatLauncher.vue`（新增，全站悬浮） | 右下角悬浮按钮 + 侧滑抽屉，入口：任意页面右下角 | normal / hover / focus / 未读角标 / open |
| `ChatRoom.vue`（新增，被上二者复用） | 消息列表 + 输入框 + 在线人数 | normal / loading / empty / error / 断线重连 |
| 消息气泡 `MessageBubble`（`ChatRoom.vue` 内） | 单条消息（自己/他人/游客/管理删除态） | self / other / guest / hover(管理员显删除) |
| 发送输入框 `ChatInput`（`ChatRoom.vue` 内） | 输入并发送 | normal / focus / disabled(限流中) / error(超长) |

---

## 4. 交互状态（双主题）

### 4.1 `ChatLauncher` 悬浮按钮 — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); box-shadow: var(--shadow-md); color: var(--accent-1);` |
| hover | `border-color: var(--border-glow); box-shadow: var(--shadow-glow);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |
| 未读角标 | 右上角 `background: var(--accent-3); color: #fff;` 圆点显示未读数 |

### 4.2 `ChatLauncher` 悬浮按钮 — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); box-shadow: var(--shadow-md); color: var(--accent-1);` |
| hover | `border-color: var(--border-glow); box-shadow: var(--shadow-glow);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |
| 未读角标 | 右上角 `background: var(--accent-3); color: #fff;` |

### 4.3 `ChatInput` 输入框 — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); color: var(--text-primary);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px; border-color: var(--border-glow);` |
| disabled / loading（限流中） | `opacity: 0.5; cursor: not-allowed;` + 计数提示 |
| error（超长 >1000） | `border-color: var(--accent-3);` + `role="alert"` 提示 |

### 4.4 `ChatInput` 输入框 — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); color: var(--text-primary);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px; border-color: var(--border-glow);` |
| disabled / loading（限流中） | `opacity: 0.5; cursor: not-allowed;` |
| error（超长 >1000） | `border-color: var(--accent-3);` + `role="alert"` |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 640px` (mobile) | `/chat` 全屏占满；`ChatLauncher` 抽屉全宽（100vw）从底部或右侧滑入；输入框固定底部 |
| `≥ 640px` (tablet) | `ChatLauncher` 抽屉宽 `380px` 右侧滑入；`/chat` 消息列表居中最大宽 `860px` |
| `≥ 1024px` (desktop) | `/chat` 两栏可选（消息区 + 在线信息侧栏）；抽屉宽 `420px` |

---

## 6. 可访问性要求

- [ ] 所有按钮有可读文字标签或 `aria-label`
- [ ] 纯图标按钮（悬浮入口、发送、关闭）必须有 `aria-label`
- [ ] 抽屉使用 `role="dialog"` + `aria-modal="true"` + `aria-labelledby`
- [ ] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px，`outline: 2px solid`
- [ ] 颜色对比度满足 WCAG AA（气泡文字 vs 背景）
- [ ] `prefers-reduced-motion: reduce` 下关闭抽屉滑入与消息淡入动画
- [ ] 限流/超长错误提示使用 `role="alert"`
- [ ] 键盘可达：Enter 发送、Shift+Enter 换行、Esc 关闭抽屉、Tab 循环
- [ ] 消息列表 `aria-live="polite"`，新消息可被屏幕阅读器播报
- [ ] 装饰图标 `aria-hidden="true"`

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 悬浮聊天入口 | `MessageCircle` | `aria-label="打开聊天室"` |
| 发送消息 | `Send` | `aria-label="发送"` |
| 关闭抽屉 | `X` | `aria-label="关闭聊天室"` |
| 在线人数 | `Users` | `aria-hidden="true"` |
| 连接状态（已连/重连中） | `Wifi` / `WifiOff` | `aria-hidden="true"` |
| 管理员删除消息 | `Trash2` | `aria-label="删除消息"` |
| 游客标识 | `UserRound` | `aria-hidden="true"` |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题
- ✅ 抽屉滑入、消息淡入均有过渡动画
- ✅ `cursor: pointer` 在按钮上
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移
