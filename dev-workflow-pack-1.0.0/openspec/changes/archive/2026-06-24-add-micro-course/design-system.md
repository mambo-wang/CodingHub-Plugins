# Design System: 微课模块（双主题）

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
| 危险色 | `#EF4444` | `#EF4444` | — |

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
| `VideoCard.vue`（新增） | 视频列表卡片，显示封面/标题/统计 | normal / hover / loading / empty |
| `VideoPlayer.vue`（新增） | 视频播放器封装 | normal / loading / error |
| `VideoCommentList.vue`（新增） | 评论列表+输入框 | normal / loading / empty / error |
| `VideoListPage.vue`（新增） | 视频列表页（网格布局） | normal / loading / empty |
| `VideoDetailPage.vue`（新增） | 视频播放详情页 | normal / loading / error |
| `VideoUploadPage.vue`（新增） | 视频上传页（拖拽+进度条） | idle / uploading / success / error |
| `ProfilePage.vue`（修改） | 新增「我的视频」「我的收藏」tab | normal / loading / empty |

---

## 4. 交互状态（双主题）

### 4.1 `VideoCard` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); border-radius: 16px; backdrop-filter: blur(20px);` |
| hover | `border-color: var(--border-glow); box-shadow: var(--shadow-glow); transform: translateY(-2px);` |
| loading | 骨架屏：`background: linear-gradient(90deg, rgba(139,92,246,0.05) 25%, rgba(139,92,246,0.1) 50%, rgba(139,92,246,0.05) 75%); animation: shimmer 1.5s infinite;` |

### 4.2 `VideoCard` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; box-shadow: var(--shadow-sm);` |
| hover | `border-color: var(--border-glow); box-shadow: var(--shadow-md); transform: translateY(-2px);` |
| loading | 骨架屏：`background: linear-gradient(90deg, rgba(124,58,237,0.05) 25%, rgba(124,58,237,0.08) 50%, rgba(124,58,237,0.05) 75%); animation: shimmer 1.5s infinite;` |

### 4.3 `VideoPlayer` — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: #000; border-radius: 16px; border: 1px solid var(--border-color);` |
| loading | 中央 `Loader2` 旋转图标 + `var(--accent-2)` 颜色 |
| error | 中央 `AlertCircle` 图标 + `#EF4444` + 错误提示文字 `var(--text-secondary)` |

### 4.4 `VideoPlayer` — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: #000; border-radius: 16px; border: 1px solid var(--border-color);` |
| loading | 中央 `Loader2` 旋转图标 + `var(--accent-2)` 颜色 |
| error | 中央 `AlertCircle` 图标 + `#EF4444` + 错误提示文字 `var(--text-secondary)` |

### 4.5 `VideoUploadPage` 上传区域 — 暗色主题

| 状态 | 样式 |
|------|------|
| idle (drop zone) | `border: 2px dashed var(--border-color); border-radius: 16px; background: var(--bg-glass); cursor: pointer;` |
| dragover | `border-color: var(--accent-1); background: rgba(139,92,246,0.05);` |
| uploading | 进度条 `background: linear-gradient(90deg, var(--accent-1), var(--accent-2));` + 百分比文字 |
| success | `CheckCircle` + `var(--accent-2)` + 成功提示 |
| error | `XCircle` + `#EF4444` + 错误提示，`role="alert"` |

### 4.6 `VideoUploadPage` 上传区域 — 亮色主题

| 状态 | 样式 |
|------|------|
| idle (drop zone) | `border: 2px dashed var(--border-color); border-radius: 16px; background: var(--bg-card); cursor: pointer;` |
| dragover | `border-color: var(--accent-1); background: rgba(124,58,237,0.05);` |
| uploading | 进度条 `background: linear-gradient(90deg, var(--accent-1), var(--accent-2));` + 百分比文字 |
| success | `CheckCircle` + `var(--accent-2)` + 成功提示 |
| error | `XCircle` + `#EF4444` + 错误提示，`role="alert"` |

### 4.7 点赞/收藏按钮 — 暗色主题

| 状态 | 样式 |
|------|------|
| normal (未激活) | `color: var(--text-muted); background: transparent; border: 1px solid var(--border-color); border-radius: 8px; cursor: pointer;` |
| hover | `color: var(--text-primary); border-color: rgba(255,255,255,0.15);` |
| active (已点赞/收藏) | 点赞 `color: #ec4899; border-color: rgba(236,72,153,0.3);` 收藏 `color: #8b5cf6; border-color: rgba(139,92,246,0.3);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |

### 4.8 点赞/收藏按钮 — 亮色主题

| 状态 | 样式 |
|------|------|
| normal (未激活) | `color: var(--text-muted); background: transparent; border: 1px solid var(--border-color); border-radius: 8px; cursor: pointer;` |
| hover | `color: var(--text-primary); border-color: rgba(0,0,0,0.15);` |
| active (已点赞/收藏) | 点赞 `color: #db2777; border-color: rgba(219,39,119,0.3);` 收藏 `color: #7c3aed; border-color: rgba(124,58,237,0.3);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |

### 4.9 评论输入框 — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); border-radius: 8px; color: var(--text-primary);` |
| focus | `border-color: var(--accent-1); box-shadow: 0 0 0 3px rgba(139,92,246,0.2);` |
| error | `border-color: #EF4444; box-shadow: 0 0 0 3px rgba(239,68,68,0.2);` + `role="alert"` 错误提示 |

### 4.10 评论输入框 — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 8px; color: var(--text-primary);` |
| focus | `border-color: var(--accent-1); box-shadow: 0 0 0 3px rgba(124,58,237,0.2);` |
| error | `border-color: #EF4444; box-shadow: 0 0 0 3px rgba(239,68,68,0.2);` + `role="alert"` 错误提示 |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 640px` (mobile) | 视频列表单列；详情页播放器全宽；评论区全宽 |
| `≥ 640px` (tablet) | 视频列表 2 列网格；详情页播放器 + 侧栏信息 |
| `≥ 1024px` (desktop) | 视频列表 3-4 列网格；详情页宽播放器 + 侧栏统计/互动 |

---

## 6. 可访问性要求

- [ ] 所有按钮有可读文字标签或 `aria-label`
- [ ] 纯图标按钮（点赞、收藏、删除）必须有 `aria-label`
- [ ] 视频播放器区域使用 `aria-label="视频播放器"`
- [ ] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px，`outline: 2px solid`
- [ ] 颜色对比度满足 WCAG AA（所有文字 ≥ 4.5:1）
- [ ] `prefers-reduced-motion: reduce` 媒体查询下关闭过渡动画
- [ ] 上传错误提示使用 `role="alert"`
- [ ] 键盘可达：Tab 循环、Enter 触发上传/点赞
- [ ] 装饰图标（播放量/评论数前的图标）`aria-hidden="true"`
- [ ] 视频 `<video>` 标签需有 `aria-label` 描述视频标题

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 播放量统计 | `Eye` | `aria-hidden="true"` |
| 点赞 | `Heart` | `aria-hidden="true"` |
| 评论 | `MessageCircle` | `aria-hidden="true"` |
| 收藏 | `Bookmark` | `aria-hidden="true"` |
| 上传 | `Upload` | `aria-hidden="true"` |
| 视频/播放 | `Play` | `aria-hidden="true"` |
| 时长 | `Clock` | `aria-hidden="true"` |
| 删除视频 | `Trash2` | `aria-label="删除视频"` |
| 编辑视频 | `Edit` | `aria-label="编辑视频"` |
| 上传完成 | `CheckCircle` | `aria-hidden="true"` |
| 上传失败 | `XCircle` | `aria-hidden="true"` |
| 加载中 | `Loader2` | `aria-hidden="true"` |
| 空状态 | `VideoOff` | `aria-hidden="true"` |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题（`var(--bg-*)` / `var(--text-*)` / `var(--accent-*)`）
- ✅ 所有状态变化有过渡动画（`transition: all 0.2s ease`）
- ✅ `cursor: pointer` 在所有可点击元素上
- ✅ scoped `<style>` 中使用 CSS 变量
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移（VideoCard hover 用 `translateY(-2px)` 而非 scale）
- ❌ 禁止使用 Tailwind CSS 类名（项目使用纯 CSS）
