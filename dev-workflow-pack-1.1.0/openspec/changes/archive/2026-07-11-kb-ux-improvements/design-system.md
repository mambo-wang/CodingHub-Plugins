# Design System: kb-ux-improvements（双主题）

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
| 破坏性 | `#EF4444` | `#EF4444` | — |

---

## 3. 涉及组件清单

| 组件/页面 | 用途 | 状态覆盖 |
|-----------|------|----------|
| `KnowledgeSearch.vue`（修改） | 知识库语义搜索，结果卡片改用 Markdown 渲染 | normal / loading / empty / error |
| `DocumentList.vue`（修改） | 文档列表，新增下载按钮 | normal / hover / disabled（文件不可下载时）/ loading |

---

## 4. 交互状态（双主题）

### 4.1 搜索结果卡片 `.result-card` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); backdrop-filter: blur(20px); border: 1px solid var(--border-color); border-radius: 16px; padding: 16px;` |
| hover | `border-color: var(--border-glow);` |

### 4.2 搜索结果卡片 `.result-card` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-card); box-shadow: var(--shadow-sm); border: 1px solid var(--border-color); border-radius: 16px; padding: 16px;` |
| hover | `border-color: var(--border-glow);` |

### 4.3 Markdown 渲染区 `.result-text` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `font-size: 14px; line-height: 1.7; color: var(--text-secondary);` 内部元素：`h1-h6` 用 `var(--text-primary)`；`code` 用 `background: rgba(255,255,255,0.06); padding: 2px 6px; border-radius: 4px; font-family: var(--font-mono); font-size: 85%;` `pre` 用 `background: #0d1117; border-radius: 6px; padding: 12px;` |
| 代码高亮 | highlight.js github-dark 主题（与 PostContent 一致） |

### 4.4 Markdown 渲染区 `.result-text` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `font-size: 14px; line-height: 1.7; color: var(--text-secondary);` 内部元素：`h1-h6` 用 `var(--text-primary)`；`code` 用 `background: rgba(0,0,0,0.06); padding: 2px 6px; border-radius: 4px;` `pre` 用 `background: #f6f8fa; border-radius: 6px; padding: 12px;` |
| 代码高亮 | highlight.js github-light 主题 |

### 4.5 下载按钮 `.btn-download` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `width: 32px; height: 32px; border-radius: 8px; background: transparent; color: var(--text-muted); cursor: pointer;` |
| hover | `color: var(--accent-1); background: rgba(139,92,246,0.1);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |
| disabled | `opacity: 0.4; cursor: not-allowed;` |

### 4.6 下载按钮 `.btn-download` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `width: 32px; height: 32px; border-radius: 8px; background: transparent; color: var(--text-muted); cursor: pointer;` |
| hover | `color: var(--accent-1); background: rgba(124,58,237,0.1);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |
| disabled | `opacity: 0.4; cursor: not-allowed;` |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 640px` (mobile) | 搜索结果卡片全宽，文档列表垂直堆叠，下载按钮保持 32×32 |
| `≥ 640px` (tablet) | 搜索结果保持当前布局 |
| `≥ 1024px` (desktop) | 搜索结果保持当前布局 |

---

## 6. 可访问性要求

- [x] 下载按钮有 `aria-label="下载文档"` 属性（纯图标按钮）
- [x] 装饰图标（FileText、Download）设置 `aria-hidden="true"`
- [x] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px
- [x] Markdown 渲染区不用 `tabindex`，无需键盘聚焦
- [x] `prefers-reduced-motion: reduce` 下关闭 hover 过渡动画

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 下载文档 | `Download` | `aria-hidden="true"`，按钮加 `aria-label="下载文档"` |
| 文件图标（已有） | `FileText` | `aria-hidden="true"` |
| 搜索图标（已有） | `Search` | `aria-hidden="true"` |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题
- ✅ 所有状态变化有 `transition: all 0.2s ease` 过渡
- ✅ `cursor: pointer` 在下载按钮上
- ✅ Markdown 渲染用 `v-html` 限定在搜索结果卡片内，不扩散
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移
- ❌ 避免在搜索结果中渲染 mermaid 图表（chunk 片段不适合）
