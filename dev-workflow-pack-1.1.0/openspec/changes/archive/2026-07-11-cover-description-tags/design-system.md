# Design System: cover-description-tags（双主题）

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

### 暗色主题背景效果

```css
[data-theme="dark"] body::before,
:root:not([data-theme="light"]) body::before {
  background:
    radial-gradient(ellipse 80% 50% at 50% -20%, rgba(139,92,246,0.15), transparent),
    radial-gradient(ellipse 60% 40% at 80% 50%, rgba(6,182,212,0.08), transparent),
    radial-gradient(ellipse 50% 30% at 20% 80%, rgba(236,72,153,0.06), transparent);
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
| `ToolCard.vue`（修改） | 工具列表卡片，新增描述行 | normal / hover |
| `TagSelector.vue`（新增） | 通用标签选择器，跨模块复用 | normal / hover / focus / loading / empty / error |
| `TagBadge.vue`（新增） | 标签展示徽章，用于卡片和详情页 | normal |
| `VideoCoverPicker.vue`（新增） | 微课封面截屏选择器 | normal / hover / loading / empty / error |
| `ToolEditorPage.vue`（修改） | 工具创建/编辑表单，新增描述输入和标签选择 | normal / focus |
| `VideoUploadPage.vue`（修改） | 微课上传/编辑页，新增封面选择和标签选择 | normal |
| `PostEditorPage.vue`（修改） | 帖子编辑器，接入标签选择器 | normal |

---

## 4. 交互状态（双主题）

### 4.1 `TagSelector` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; color: #fafafa;` |
| hover | `border-color: rgba(139,92,246,0.3); box-shadow: 0 0 12px rgba(139,92,246,0.1);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |
| loading | `opacity: 0.6; cursor: wait;` 内部显示 spinner |
| empty | 显示占位文字 "选择或创建标签..." `color: #52525b;` |
| error | `border-color: #EF4444;` 下方显示红色错误文字 |

### 4.2 `TagSelector` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: rgba(255,255,255,0.9); border: 1px solid rgba(0,0,0,0.08); border-radius: 8px; color: #0f172a;` |
| hover | `border-color: rgba(124,58,237,0.3); box-shadow: 0 0 12px rgba(124,58,237,0.08);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |
| loading | `opacity: 0.6; cursor: wait;` |
| empty | 占位文字 `color: #94a3b8;` |
| error | `border-color: #EF4444;` |

### 4.3 `TagBadge` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: rgba(139,92,246,0.15); color: #8b5cf6; border-radius: 8px; padding: 2px 8px; font-size: 12px;` |

### 4.4 `TagBadge` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: rgba(124,58,237,0.1); color: #7c3aed; border-radius: 8px; padding: 2px 8px; font-size: 12px;` |

### 4.5 `VideoCoverPicker` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal (empty) | `border: 2px dashed rgba(255,255,255,0.08); border-radius: 16px; min-height: 200px; display: flex; align-items: center; justify-content: center; color: #52525b;` |
| hover | `border-color: rgba(139,92,246,0.3);` |
| loading | 显示进度条 + "正在截取封面..." |
| has-cover | 封面图片预览 + 右上角"重新选择"按钮 |
| error | `border-color: #EF4444;` 错误提示 |

### 4.6 `VideoCoverPicker` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal (empty) | `border: 2px dashed rgba(0,0,0,0.08); border-radius: 16px; color: #94a3b8;` |
| hover | `border-color: rgba(124,58,237,0.3);` |
| loading | 显示进度条 |
| has-cover | 封面预览 + "重新选择" |
| error | `border-color: #EF4444;` |

### 4.7 `ToolCard`（描述行）— 暗色主题

| 状态 | 样式 |
|------|------|
| normal | 描述行 `font-size: 13px; color: #a1a1aa; line-height: 1.4; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 100%;` |

### 4.8 `ToolCard`（描述行）— 亮色主题

| 状态 | 样式 |
|------|------|
| normal | 描述行 `font-size: 13px; color: #475569;` |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 640px` (mobile) | TagSelector 全宽；封面选择器单列；ToolCard 描述行最多 1 行 ellipsis |
| `≥ 640px` (tablet) | TagSelector 内联；封面选择器与表单并排 |
| `≥ 1024px` (desktop) | ToolCard 描述行最多 2 行 ellipsis；标签最多展示 5 个，超出 "+N" |

---

## 6. 可访问性要求

- [ ] 所有按钮有可读文字标签或 `aria-label`
- [ ] TagSelector 下拉列表使用 `role="listbox"` + `role="option"`
- [ ] TagBadge 使用 `role="list"` 容器 + `aria-label="标签列表"`
- [ ] VideoCoverPicker 的"选择封面"按钮有 `aria-label="从视频截取封面"`
- [ ] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px，`outline: 2px solid`
- [ ] 颜色对比度满足 WCAG AA（暗色 `#8b5cf6` on `rgba(139,92,246,0.15)` 对比度 > 4.5:1；亮色 `#7c3aed` on `rgba(124,58,237,0.1)` 对比度 > 4.5:1）
- [ ] `prefers-reduced-motion: reduce` 媒体查询下关闭过渡动画
- [ ] 键盘可达：Tab 进入标签选择器，上下箭头导航，Enter 选择，Esc 关闭下拉
- [ ] 装饰图标 `aria-hidden="true"`

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 标签图标 | `Tag` | `aria-hidden="true"` |
| 删除标签 | `X` | `aria-hidden="true"` |
| 添加标签 | `Plus` | `aria-hidden="true"` |
| 封面图标 | `Image` | `aria-hidden="true"` |
| 重新截取 | `RefreshCw` | `aria-hidden="true"` |
| 上传封面 | `Upload` | `aria-hidden="true"` |
| 加载中 | `Loader2` | `aria-hidden="true"` |

---

## 8. Antipatterns 检查

- 使用 Lucide 图标，无 emoji
- 使用 CSS 变量实现双主题（`:root:not([data-theme="light"])` 暗色，`[data-theme="light"]` 亮色）
- 所有状态变化有 `transition: all 0.2s ease` 过渡动画
- `cursor: pointer` 在所有可点击元素上
- 避免 `!important`
- 避免悬停 scale 导致布局位移（使用 `box-shadow` 替代 `transform: scale`）
- 标签徽章使用 `display: inline-flex` 避免行内元素间距问题
