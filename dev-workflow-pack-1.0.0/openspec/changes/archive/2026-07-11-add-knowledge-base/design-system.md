# Design System: add-knowledge-base（双主题）

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
| 焦点环 | `#00FFFF` | `#7c3aed` | — |
| 错误色 | `#EF4444` | `#EF4444` | — |

---

## 3. 涉及组件清单

| 组件/页面 | 用途 | 状态覆盖 |
|-----------|------|----------|
| `KnowledgeListPage.vue`（新增） | 知识库列表页，含侧栏+卡片网格 | normal / loading / empty / error |
| `KnowledgeCard.vue`（新增） | 知识库列表卡片 | normal / hover / focus |
| `KnowledgeDetailPage.vue`（新增） | 知识库详情+搜索+文档列表+配置 | normal / loading / error / search-loading / search-empty |
| `KnowledgeEditorPage.vue`（新增） | 创建/编辑知识库表单 | normal / loading / error / submitting |
| `DocumentList.vue`（新增） | 文档列表（详情页内嵌 Tab） | normal / loading / empty / uploading |
| `DocumentUpload.vue`（新增） | 文档上传组件（拖拽/点击） | idle / dragging / uploading / success / error |
| `KnowledgeSearch.vue`（新增） | 搜索问答组件 | idle / searching / results / empty |
| `ConfigPanel.vue`（新增） | 知识库参数配置面板 | normal / saving / saved |
| `ConfirmDialog.vue`（复用） | 删除确认弹窗 | normal / loading |
| `GeneralizedSidebar.vue`（复用） | 侧栏导航 | normal |
| `SortTab.vue`（复用） | 排序切换 | normal |

---

## 4. 交互状态（双主题）

### 4.1 KnowledgeCard — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); border-radius: 16px; backdrop-filter: blur(20px);` |
| hover | `border-color: var(--border-glow); box-shadow: var(--shadow-glow); transform: translateY(-2px);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |

### 4.2 KnowledgeCard — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); border-radius: 16px;` |
| hover | `border-color: var(--border-glow); box-shadow: var(--shadow-glow); transform: translateY(-2px);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |

### 4.3 DocumentUpload — 暗色主题

| 状态 | 样式 |
|------|------|
| idle | `border: 2px dashed var(--border-color); border-radius: 16px; background: var(--bg-glass);` |
| dragging | `border-color: var(--accent-1); background: rgba(139,92,246,0.05);` |
| uploading | `border-color: var(--accent-2);` + progress bar + spinner |
| success | `border-color: var(--accent-2);` + CheckCircle icon `var(--accent-2)` |
| error | `border-color: #EF4444;` + XCircle icon `#EF4444` |

### 4.4 DocumentUpload — 亮色主题

| 状态 | 样式 |
|------|------|
| idle | `border: 2px dashed var(--border-color); border-radius: 16px; background: var(--bg-glass);` |
| dragging | `border-color: var(--accent-1); background: rgba(124,58,237,0.05);` |
| uploading | `border-color: var(--accent-2);` + progress bar + spinner |
| success | `border-color: var(--accent-2);` + CheckCircle icon `var(--accent-2)` |
| error | `border-color: #EF4444;` + XCircle icon `#EF4444` |

### 4.5 KnowledgeSearch — 暗色主题

| 状态 | 样式 |
|------|------|
| idle | 搜索输入框 `input` 样式 |
| searching | `Loader2` 旋转图标 + "搜索中..." 文字 |
| results | 结果卡片列表，每个卡片含来源文档名 + chunk 文本 + score |
| empty | `Search` 图标 + "未找到相关内容" + 建议文字 |

### 4.6 KnowledgeSearch — 亮色主题

| 状态 | 样式 |
|------|------|
| idle | 搜索输入框 `input` 样式（与暗色一致使用 CSS 变量） |
| searching | `Loader2` 旋转图标 |
| results | 结果卡片列表 |
| empty | `Search` 图标 + 提示文字 |

### 4.7 ConfigPanel — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | 折叠区域 `glass-card` 样式，表单使用 `input` 样式 |
| saving | 保存按钮 loading spinner |
| saved | CheckCircle 图标 `var(--accent-2)` + "已保存" 提示 |

### 4.8 ConfigPanel — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | 与暗色一致使用 CSS 变量 |
| saving | 保存按钮 loading spinner |
| saved | CheckCircle 图标 `var(--accent-2)` + "已保存" 提示 |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 768px` (mobile) | 知识库列表单列全宽，侧栏隐藏，搜索框全宽，详情页文档列表纵向堆叠 |
| `≥ 768px` (tablet) | 知识库列表 2 列网格，侧栏显示为图标模式，详情页搜索和文档并排 |
| `≥ 1024px` (desktop) | 知识库列表 3 列网格，完整侧栏，详情页完整双栏布局 |

---

## 6. 可访问性要求

- [x] 所有按钮有可读文字标签或 `aria-label`
- [x] 纯图标按钮（删除文档、删除知识库）必须有 `aria-label`
- [x] 确认弹窗使用 `role="dialog"` + `aria-modal="true"` + `aria-labelledby`
- [x] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px，`outline: 2px solid`
- [x] 颜色对比度满足 WCAG AA（正文 ≥ 4.5:1）
- [x] 错误提示使用 `role="alert"`
- [x] 键盘可达：Tab 循环、Esc 关闭弹窗、Enter 提交搜索
- [x] 装饰图标 `aria-hidden="true"`

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 知识库（侧栏/导航） | `Database` | `aria-hidden="true"` |
| 创建知识库 | `Plus` | `aria-hidden="true"` |
| 搜索 | `Search` | `aria-hidden="true"` |
| 文档列表 | `FileText` | `aria-hidden="true"` |
| 上传文档 | `Upload` | `aria-hidden="true"` |
| 删除文档 | `Trash2` | `aria-label="删除此文档"` |
| 删除知识库 | `Trash2` | `aria-label="删除知识库"` |
| 配置 | `Settings` | `aria-hidden="true"` |
| 返回 | `ArrowLeft` | `aria-hidden="true"` |
| 加载中 | `Loader2` | `aria-hidden="true"` |
| 空状态 | `Database` | `aria-hidden="true"` |
| 文档数 | `Files` | `aria-hidden="true"` |
| 折叠/展开高级配置 | `ChevronDown` / `ChevronUp` | `aria-hidden="true"` |
| 搜索结果来源 | `FileText` | `aria-hidden="true"` |
| 相关度 | `Zap` | `aria-hidden="true"` |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题
- ✅ 所有状态变化有过渡动画（`transition: all 0.3s`）
- ✅ `cursor: pointer` 在所有可点击元素上
- ✅ 使用 `glass-card` 样式保持视觉一致性
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移（使用 `translateY`）
- ❌ 避免 Tailwind 类名（项目使用纯 CSS + scoped style）
