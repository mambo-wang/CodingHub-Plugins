# Design System: RAG 自适应切片（双主题）

> 引用全局设计系统 `design-system/CodingHub/MASTER.md`，仅列出本次变更涉及的 UI 组件、交互状态与可访问性约束。

## 1. 全局样式引用

### 字体

| 角色 | 字体 | CSS 变量 |
|------|------|----------|
| 标题/按钮/正文 | Sora (300–800 weight) | `var(--font-display)` |
| 代码/统计数字/chunk 字符数 | Space Mono (400, 700 weight) | `var(--font-mono)` |

### 圆角

| 元素 | 值 |
|------|-----|
| 按钮、输入框、徽章 | `8px` |
| 卡片、模态框、预览面板 | `16px` |
| chunk 卡片 | `12px` |

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
| 成功/通过 | `#10b981` | `#059669` | `--success` |
| 警告/碎片 | `#f59e0b` | `#d97706` | `--warning` |
| 错误/拒绝 | `#EF4444` | `#EF4444` | `--destructive` |

---

## 3. 涉及组件清单

| 组件/页面 | 用途 | 状态覆盖 |
|-----------|------|----------|
| `ChunkingPreviewPanel.vue`（新增） | 分片调试预览面板：输入样本文本 → 展示切片结果 | normal / loading / empty / error |
| `ChunkCard.vue`（新增） | 单个 chunk 卡片：序号、内容预览、字符数、context_header 标签 | normal / hover / expanded |
| `StrategyBadge.vue`（新增） | 策略标签：显示 auto/structural/semantic/recursive 及颜色编码 | normal |
| `ChunkStatsBar.vue`（新增） | 统计条：total_chunks / avg / min / max / stddev | normal |
| `KnowledgeSettingsPage.vue`（修改） | 知识库设置页：新增分片预览折叠面板 + strategy 选择器 | normal / hover / focus |
| `DocumentListView.vue`（修改） | 文档列表：新增 chunk_count / strategy / status 列 | normal / loading / empty |

---

## 4. 交互状态（双主题）

### 4.1 `ChunkingPreviewPanel` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; backdrop-filter: blur(12px);` |
| loading | 骨架屏 shimmer：`background: linear-gradient(90deg, var(--bg-glass) 25%, rgba(139,92,246,0.05) 50%, var(--bg-glass) 75%); animation: shimmer 1.5s infinite;` |
| empty | 居中图标 + 提示文字 `color: var(--text-muted); font-size: 14px;` |
| error | `border-color: var(--destructive);` + 错误消息 `color: var(--destructive); role="alert"` |

### 4.2 `ChunkingPreviewPanel` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; box-shadow: var(--shadow-sm);` |
| loading | 骨架屏 shimmer：`background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);` |
| empty | 同暗色，文字色 `var(--text-muted)` 亮色值 `#94a3b8` |
| error | 同暗色 |

### 4.3 `ChunkCard` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); border-radius: 12px; padding: 12px 16px;` |
| hover | `border-color: var(--border-glow); box-shadow: var(--shadow-glow); transform: translateY(-1px);` |
| expanded | `max-height: none; border-color: var(--accent-1);` 内容区展开完整文本 |

### 4.4 `ChunkCard` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: #ffffff; border: 1px solid rgba(0,0,0,0.06); border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);` |
| hover | `border-color: rgba(124,58,237,0.3); box-shadow: 0 4px 12px rgba(124,58,237,0.08);` |
| expanded | `border-color: var(--accent-1);` |

### 4.5 `StrategyBadge` — 双主题

| 策略 | 暗色 | 亮色 |
|------|------|------|
| auto | `background: rgba(139,92,246,0.15); color: #a78bfa; border: 1px solid rgba(139,92,246,0.3);` | `background: rgba(124,58,237,0.1); color: #6d28d9;` |
| structural | `background: rgba(6,182,212,0.15); color: #67e8f9; border: 1px solid rgba(6,182,212,0.3);` | `background: rgba(8,145,178,0.1); color: #0e7490;` |
| semantic | `background: rgba(236,72,153,0.15); color: #f9a8d4; border: 1px solid rgba(236,72,153,0.3);` | `background: rgba(219,39,119,0.1); color: #be185d;` |
| recursive | `background: rgba(255,255,255,0.05); color: var(--text-secondary); border: 1px solid var(--border-color);` | `background: rgba(0,0,0,0.04); color: var(--text-secondary);` |

### 4.6 文本输入区（样本文本）— 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); color: var(--text-primary); font-family: var(--font-mono); font-size: 13px;` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px; border-color: var(--accent-2);` |
| disabled | `opacity: 0.5; cursor: not-allowed;` |

### 4.7 文本输入区 — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: #ffffff; border: 1px solid rgba(0,0,0,0.12); color: var(--text-primary);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px; border-color: var(--accent-1);` |
| disabled | `opacity: 0.5; cursor: not-allowed;` |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 640px` (mobile) | 预览面板全宽；chunk 卡片单列堆叠；统计条垂直排列；输入区高度 120px |
| `≥ 640px` (tablet) | 预览面板全宽；chunk 卡片双列网格；统计条水平排列 |
| `≥ 1024px` (desktop) | 预览面板嵌入知识库设置页右侧折叠区；chunk 卡片双列；输入区高度 200px |

---

## 6. 可访问性要求

- [ ] 「运行预览」按钮有文字标签 + `aria-label="运行分片预览"`
- [ ] 策略选择器使用 `<select>` 或 `role="listbox"` + `aria-label="切片策略"`
- [ ] chunk 卡片列表使用 `role="list"` + 每个卡片 `role="listitem"`
- [ ] 加载状态使用 `aria-busy="true"` + `aria-live="polite"` 通知结果
- [ ] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px
- [ ] 颜色对比度满足 WCAG AA（策略徽章文字 vs 背景）
- [ ] `prefers-reduced-motion: reduce` 下关闭 shimmer 动画和 hover transform
- [ ] 错误提示使用 `role="alert"`
- [ ] 键盘可达：Tab 遍历 chunk 卡片，Enter 展开/收起
- [ ] 装饰图标 `aria-hidden="true"`

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 运行预览 | `Play` | `aria-hidden="true"` |
| 切片策略 | `Scissors` | `aria-hidden="true"` |
| chunk 序号 | `Hash` | `aria-hidden="true"` |
| 展开 chunk | `ChevronDown` / `ChevronUp` | `aria-hidden="true"` |
| 统计信息 | `BarChart3` | `aria-hidden="true"` |
| 空状态 | `FileText` | `aria-hidden="true"` |
| 错误状态 | `AlertTriangle` | `aria-hidden="true"` |
| 加载中 | `Loader2` (spin) | `aria-hidden="true"` |
| 折叠面板 | `PanelRightClose` / `PanelRightOpen` | `aria-hidden="true"` |
| 文档状态 | `CheckCircle` / `Clock` / `XCircle` | `aria-hidden="true"` |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题
- ✅ 所有状态变化有过渡动画（`transition: all 0.2s ease`）
- ✅ `cursor: pointer` 在可交互元素上
- ✅ chunk 内容截断使用 `line-clamp` 而非固定高度
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移（使用 translateY）
- ❌ 避免在 chunk 卡片内使用 `overflow: hidden` 截断代码块（应允许横向滚动）
