# Design System: tool-ui-and-mcp-fixes（双主题）

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
| 卡片、模态框 | `16px` |
| 模态框输入框 | `10px` |

### 阴影

| Level | 暗色值 | 亮色值 |
|-------|--------|--------|
| `--shadow-sm` | `0 2px 8px rgba(0,0,0,0.3)` | `0 2px 8px rgba(0,0,0,0.08)` |
| `--shadow-md` | `0 8px 24px rgba(0,0,0,0.4)` | `0 8px 24px rgba(0,0,0,0.12)` |
| `--shadow-glow` | `0 0 40px rgba(139,92,246,0.15)` | `0 0 40px rgba(124,58,237,0.1)` |

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

## 3. 涉及组件清单

| 组件/页面 | 变更类型 | 状态覆盖 |
|-----------|----------|----------|
| `HomePage.vue` — 上传模态框 | UI 新增 | normal / submitting / error |
| `HomePage.vue` — 工具卡片 | UI 新增 | normal / hover |
| `EditToolPage.vue` | 逻辑修复 | 无 UI 变更 |

## 4. 交互状态（双主题）

### 4.1 上传模态框 — "简短描述"输入框 — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 10px; padding: 12px 14px; color: var(--text-primary); font-size: 14px;` |
| focus | `border-color: rgba(139,92,246,0.5); box-shadow: 0 0 0 3px rgba(139,92,246,0.1);` |
| placeholder | `color: var(--text-muted);` — "一句话介绍这个工具（选填）" |

### 4.2 上传模态框 — "简短描述"输入框 — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: rgba(0,0,0,0.02); border: 1px solid var(--border-color);` |
| focus | `border-color: rgba(124,58,237,0.5); box-shadow: 0 0 0 3px rgba(124,58,237,0.1);` |

### 4.3 工具卡片 — 版本号 badge — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `padding: 2px 8px; border-radius: 6px; font-size: 12px; font-family: var(--font-mono); background: rgba(6,182,212,0.1); color: #22d3ee; border: 1px solid rgba(6,182,212,0.2);` |
| hover | `transform: translateY(-1px); box-shadow: 0 2px 8px rgba(6,182,212,0.2);` |

### 4.4 工具卡片 — 版本号 badge — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: rgba(8,145,178,0.08); color: #0e7490; border-color: rgba(8,145,178,0.15);` |
| hover | `box-shadow: 0 2px 8px rgba(8,145,178,0.15);` |

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 768px` (mobile) | 版本号 badge 内联显示，自动换行时跟随文本流 |
| `≥ 768px` (desktop) | 版本号 badge 保持内联，不挤压工具名称 |

## 6. 可访问性要求

- [x] 新增输入框有 `<label>` 关联
- [x] 版本号 badge 使用 `aria-hidden="true"`
- [x] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`
- [x] 颜色对比度满足 WCAG AA
- [x] 键盘可达：Tab 可聚焦新增输入框

## 7. 图标清单

| 用途 | 来源 | aria |
|------|------|------|
| 版本号 badge | 纯文本 `v{version}` | `aria-hidden="true"` |

## 8. Antipatterns 检查

- ✅ 使用 CSS 变量实现双主题
- ✅ 所有状态变化有过渡动画
- ✅ 版本号 badge 使用 `cursor: default`
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移
