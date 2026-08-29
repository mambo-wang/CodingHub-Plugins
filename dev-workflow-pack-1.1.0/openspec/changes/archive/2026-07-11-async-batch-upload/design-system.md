# Design System: async-batch-upload（双主题）

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
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.3)` | `0 1px 2px rgba(0,0,0,0.05)` |
| `--shadow-md` | `0 4px 6px rgba(0,0,0,0.3)` | `0 4px 6px rgba(0,0,0,0.07)` |
| `--shadow-glow` | `0 0 20px rgba(139,92,246,0.3)` | `0 0 20px rgba(124,58,237,0.15)` |

---

## 2. 双主题 Tokens 映射

| 角色 | 暗色主题 | 亮色主题 | CSS 变量 |
|------|----------|----------|----------|
| 页面背景 | `#09090b` | `#f8fafc` | `--bg-primary` |
| 面板/侧栏 | `#0f0f12` | `#f1f5f9` | `--bg-secondary` |
| 卡片背景 | `#18181b` | `#ffffff` | `--bg-card` |
| 毛玻璃 | `rgba(24,24,27,0.8)` | `rgba(255,255,255,0.8)` | `--bg-glass` |
| 主色 (紫) | `#8b5cf6` | `#7c3aed` | `--accent-1` |
| 辅助色 (青) | `#06b6d4` | `#0891b2` | `--accent-2` |
| 第三色 (粉) | `#ec4899` | `#db2777` | `--accent-3` |
| 主文字 | `#fafafa` | `#0f172a` | `--text-primary` |
| 次文字 | `#a1a1aa` | `#475569` | `--text-secondary` |
| 辅助文字 | `#52525b` | `#94a3b8` | `--text-muted` |
| 边框色 | `#27272a` | `#e2e8f0` | `--border-color` |
| 发光边框 | `#3f3f46` | `#cbd5e1` | `--border-glow` |
| 焦点环 | `#00FFFF` | `#7c3aed` | `--focus-ring` |

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
| `DocumentUpload.vue`（修改） | 多文件选择和批量上传 | normal / hover / focus / disabled / uploading / processing / error / empty |
| `DocumentList.vue`（修改） | 文档列表与状态徽章展示 | normal / hover / loading / empty / polling |
| `KnowledgeSearch.vue`（修改） | 语义搜索与能力提示 | normal / hint-visible / hint-hidden |
| `StatusBadge.vue`（新增） | 文档处理状态徽章组件 | uploading / converting / chunking / embedding / ready / failed |
| `InfoBanner.vue`（新增） | 信息提示横幅组件 | visible / hidden / closing |

---

## 4. 交互状态（双主题）

### 4.1 StatusBadge 状态徽章 — 暗色主题

| 状态 | 样式 |
|------|------|
| UPLOADING | `background: #3f3f46; color: #a1a1aa; border: 1px solid #52525b;` |
| CONVERTING | `background: #422006; color: #fbbf24; border: 1px solid #78350f;` |
| CHUNKING | `background: #1e3a8a; color: #60a5fa; border: 1px solid #1e40af;` |
| EMBEDDING | `background: #4c1d95; color: #c084fc; border: 1px solid #5b21b6;` |
| READY | `background: #064e3b; color: #34d399; border: 1px solid #065f46;` |
| FAILED | `background: #7f1d1d; color: #fca5a5; border: 1px solid #991b1b;` |

### 4.2 StatusBadge 状态徽章 — 亮色主题

| 状态 | 样式 |
|------|------|
| UPLOADING | `background: #f1f5f9; color: #64748b; border: 1px solid #cbd5e1;` |
| CONVERTING | `background: #fef3c7; color: #b45309; border: 1px solid #fde68a;` |
| CHUNKING | `background: #dbeafe; color: #1d4ed8; border: 1px solid #93c5fd;` |
| EMBEDDING | `background: #f3e8ff; color: #7c3aed; border: 1px solid #c4b5fd;` |
| READY | `background: #d1fae5; color: #059669; border: 1px solid #6ee7b7;` |
| FAILED | `background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5;` |

### 4.3 DocumentUpload 上传区域 — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: #18181b; border: 2px dashed #3f3f46; color: #a1a1aa;` |
| hover | `border-color: #8b5cf6; background: rgba(139,92,246,0.05);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |
| disabled | `opacity: 0.5; cursor: not-allowed;` |
| uploading | `border-color: #8b5cf6; background: rgba(139,92,246,0.1);` |
| processing | `border-color: #06b6d4; background: rgba(6,182,212,0.05);` |
| error | `border-color: #ef4444; background: rgba(239,68,68,0.05);` |

### 4.4 DocumentUpload 上传区域 — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: #ffffff; border: 2px dashed #cbd5e1; color: #64748b;` |
| hover | `border-color: #7c3aed; background: rgba(124,58,237,0.03);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |
| disabled | `opacity: 0.5; cursor: not-allowed;` |
| uploading | `border-color: #7c3aed; background: rgba(124,58,237,0.05);` |
| processing | `border-color: #0891b2; background: rgba(8,145,178,0.03);` |
| error | `border-color: #ef4444; background: rgba(239,68,68,0.03);` |

### 4.5 InfoBanner 提示横幅 — 暗色主题

| 状态 | 样式 |
|------|------|
| visible | `background: rgba(6,182,212,0.1); border: 1px solid #06b6d4; color: #e2e8f0; border-radius: 8px; padding: 12px 16px;` |
| closing | `opacity: 0; transform: translateY(-10px); transition: all 0.3s ease-out;` |

### 4.6 InfoBanner 提示横幅 — 亮色主题

| 状态 | 样式 |
|------|------|
| visible | `background: rgba(8,145,178,0.05); border: 1px solid #0891b2; color: #0f172a; border-radius: 8px; padding: 12px 16px;` |
| closing | `opacity: 0; transform: translateY(-10px); transition: all 0.3s ease-out;` |

### 4.7 DocumentList 文档行 — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: #18181b; border-bottom: 1px solid #27272a; padding: 12px 16px;` |
| hover | `background: #27272a;` |
| loading | `background: #18181b; opacity: 0.7;` |
| polling | `background: #18181b; border-left: 3px solid #8b5cf6;` |

### 4.8 DocumentList 文档行 — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: #ffffff; border-bottom: 1px solid #e2e8f0; padding: 12px 16px;` |
| hover | `background: #f1f5f9;` |
| loading | `background: #ffffff; opacity: 0.7;` |
| polling | `background: #ffffff; border-left: 3px solid #7c3aed;` |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 640px` (mobile) | 上传区域全宽，文档列表单列，状态徽章换行显示 |
| `≥ 640px` (tablet) | 上传区域保持全宽，文档列表显示文件名和状态两列 |
| `≥ 1024px` (desktop) | 上传区域最大宽度 600px 居中，文档列表显示完整信息（文件名、大小、状态、操作） |

---

## 6. 可访问性要求

- [x] 所有按钮有可读文字标签或 `aria-label`
- [x] 纯图标按钮（如关闭、删除）有 `aria-label`
- [x] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px，`outline: 2px solid`
- [x] 颜色对比度满足 WCAG AA（状态徽章文字与背景对比度 ≥ 4.5:1）
- [x] `prefers-reduced-motion: reduce` 媒体查询下关闭状态徽章动画
- [x] 错误提示使用 `role="alert"`（FAILED 状态的错误信息）
- [x] 键盘可达：Tab 循环、Enter 触发上传
- [x] 装饰图标（如状态图标旁的装饰）使用 `aria-hidden="true"`
- [x] InfoBanner 使用 `role="status"` 和 `aria-live="polite"`

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 上传文件 | `Upload` | `aria-hidden="true"` |
| 上传中状态 | `Loader2` (旋转动画) | `aria-hidden="true"` |
| 转换中状态 | `FileText` | `aria-hidden="true"` |
| 分块中状态 | `Layers` | `aria-hidden="true"` |
| 向量化中状态 | `Cpu` | `aria-hidden="true"` |
| 已解析状态 | `CheckCircle2` | `aria-hidden="true"` |
| 失败状态 | `AlertCircle` | `aria-hidden="true"` |
| 关闭提示 | `X` | `aria-label="关闭提示"` |
| 删除文档 | `Trash2` | `aria-label="删除文档"` |
| 信息提示 | `Info` | `aria-hidden="true"` |
| 文件图标 | `File` | `aria-hidden="true"` |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题
- ✅ 所有状态变化有过渡动画（`transition: all 0.2s ease`）
- ✅ `cursor: pointer` 在按钮上
- ✅ 状态徽章使用语义化颜色（绿色=成功，红色=失败，黄色=处理中）
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移
- ❌ 避免在轮询期间禁用整个列表（仅显示加载指示器）

---

## 9. 状态颜色语义

| 状态 | 语义 | 颜色类别 |
|------|------|----------|
| `UPLOADING` | 信息/进行中 | 灰色 (neutral) |
| `CONVERTING` | 警告/处理中 | 黄色 (warning) |
| `CHUNKING` | 信息/处理中 | 蓝色 (info) |
| `EMBEDDING` | 强调/处理中 | 紫色 (accent) |
| `READY` | 成功/完成 | 绿色 (success) |
| `FAILED` | 错误/失败 | 红色 (error) |

---

## 10. 动画规范

### 状态徽章脉冲动画（处理中状态）

```css
@keyframes pulse-processing {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.status-badge.uploading,
.status-badge.converting,
.status-badge.chunking,
.status-badge.embedding {
  animation: pulse-processing 2s ease-in-out infinite;
}

@media (prefers-reduced-motion: reduce) {
  .status-badge.uploading,
  .status-badge.converting,
  .status-badge.chunking,
  .status-badge.embedding {
    animation: none;
  }
}
```

### Loader2 旋转动画

```css
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.spin {
  animation: spin 1s linear infinite;
}
```
