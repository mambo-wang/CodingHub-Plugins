# Design System: tool-logo-and-stats（双主题）

> 引用全局设计系统 `design-system/CodingHub/MASTER.md`，仅列出本次变更涉及的 UI 组件、交互状态与可访问性约束。
> 本次改动聚焦工具卡片：左上角 logo 区 + 卡片底部统计数据行（浏览量 / 点赞量 / 收藏量 / 下载量）。

## 1. 全局样式引用

### 字体

| 角色 | 字体 | CSS 变量 |
|------|------|----------|
| 标题/按钮/正文 | Sora (300–800 weight) | `var(--font-display)` |
| 统计数字 | Space Mono (400, 700 weight) | `var(--font-mono)` |

**导入：**
```css
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');
```

> 统计行的数值使用 `var(--font-mono)`（Space Mono），保证数字等宽、对齐稳定，呼应参考稿 SkillHub 的下载量数字风格。

### 圆角

| 元素 | 值 |
|------|-----|
| logo 容器 | `8px`（方形 logo）或 `12px`（参考稿圆角方块） |
| 工具卡片 | `16px` |
| 统计项徽章（可选 hover 底） | `8px` |

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
| logo 占位底色 | `rgba(255,255,255,0.05)` | `rgba(0,0,0,0.04)` | `--bg-glass`（复用） |
| 主色 (紫) | `#8b5cf6` | `#7c3aed` | `--accent-1` |
| 辅助色 (青) | `#06b6d4` | `#0891b2` | `--accent-2` |
| 第三色 (粉) | `#ec4899` | `#db2777` | `--accent-3` |
| 主文字 | `#fafafa` | `#0f172a` | `--text-primary` |
| 次文字 | `#a1a1aa` | `#475569` | `--text-secondary` |
| 统计数字色 | `#a1a1aa` | `#475569` | `--text-secondary` |
| 辅助文字/图标 | `#52525b` | `#94a3b8` | `--text-muted` |
| 边框色 | `rgba(255,255,255,0.08)` | `rgba(0,0,0,0.08)` | `--border-color` |
| 发光边框 | `rgba(139,92,246,0.3)` | `rgba(124,58,237,0.3)` | `--border-glow` |
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
| `HomePage.vue` 工具卡片（修改） | 卡片左上角渲染 logo，底部新增统计行 | normal / hover / loading(骨架) / empty / error(裂图兜底) |
| `ToolLogo.vue`（新增，可选） | 封装 logo 渲染 + 三级回退 + 裂图兜底 | normal / fallback(分类默认) / placeholder(系统占位) / error |
| `ToolDetailPage.vue`（修改） | 详情页标题区展示 logo | normal / fallback / placeholder |
| 工具上传/编辑表单（修改） | logo 上传入口（复用图片上传） | idle / uploading / success(预览) / error |
| 管理端分类管理（修改） | 分类默认 logo 设置 | idle / uploading / success / error |

---

## 4. 交互状态（双主题）

### 4.1 工具卡片 logo 区 — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `width:48px; height:48px; border-radius:12px; object-fit:cover; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.08);` |
| 占位（无 logo） | 同尺寸容器，居中放置 Lucide 图标 `Wrench`，`color:#52525b;` 或渲染分类默认 logo |
| hover（随卡片） | 卡片 `border-color:var(--border-glow); box-shadow:var(--shadow-glow); transform:translateY(-2px);` logo 区不单独变化 |
| error（裂图） | `img @error` 切换为系统占位图标，避免破图标 |

### 4.2 工具卡片 logo 区 — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `width:48px; height:48px; border-radius:12px; object-fit:cover; background:rgba(0,0,0,0.04); border:1px solid rgba(0,0,0,0.08);` |
| 占位（无 logo） | 居中 Lucide `Wrench`，`color:#94a3b8;` 或分类默认 logo |
| hover（随卡片） | 卡片 `border-color:var(--border-glow); box-shadow:var(--shadow-glow); transform:translateY(-2px);` |
| error（裂图） | `img @error` 回退系统占位图标 |

### 4.3 统计数据行 — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `display:flex; gap:16px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.08);` 每项 `display:flex; align-items:center; gap:4px;` 图标 `16px; color:#52525b;` 数字 `font-family:var(--font-mono); font-size:13px; color:#a1a1aa;` |
| hover | 统计行整体不响应 hover（卡片整体 hover），保持静态避免布局位移 |
| focus | 若统计项可点击（预留）：`outline:2px solid #00FFFF; outline-offset:2px;` |
| loading | 骨架占位：`height:13px;` 流光条，`background:linear-gradient(90deg, rgba(139,92,246,0.05) 25%, rgba(139,92,246,0.1) 50%, rgba(139,92,246,0.05) 75%); background-size:200% 100%; animation:shimmer 1.5s infinite;` |

### 4.4 统计数据行 — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `display:flex; gap:16px; padding-top:12px; border-top:1px solid rgba(0,0,0,0.08);` 图标 `16px; color:#94a3b8;` 数字 `font-family:var(--font-mono); font-size:13px; color:#475569;` |
| hover | 静态，不响应 |
| focus | 若可点击：`outline:2px solid #7c3aed; outline-offset:2px;` |
| loading | 骨架流光条，磁吸色 `rgba(124,58,237,0.05~0.1)` |

### 4.5 logo 上传控件（表单） — 暗色主题

| 状态 | 样式 |
|------|------|
| idle | 虚线框 `border:1px dashed rgba(255,255,255,0.15); border-radius:12px;` 居中 `Upload` 图标 + 「上传 logo」文字，`color:#a1a1aa; cursor:pointer;` |
| hover | `border-color:var(--accent-1); background:rgba(139,92,246,0.05);` |
| uploading | 显示 `Loader2` 旋转图标 + 「上传中…」，禁用点击 |
| success | 显示 logo 预览缩略图 + 「更换」按钮 |
| error | 边框 `#EF4444`，下方 `role="alert"` 错误文案 |

### 4.6 logo 上传控件（表单） — 亮色主题

| 状态 | 样式 |
|------|------|
| idle | `border:1px dashed rgba(0,0,0,0.15); border-radius:12px;` `color:#475569; cursor:pointer;` |
| hover | `border-color:var(--accent-1); background:rgba(124,58,237,0.05);` |
| uploading | `Loader2` 旋转 + 「上传中…」 |
| success | logo 预览 + 「更换」 |
| error | 边框 `#EF4444` + `role="alert"` |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 768px` (mobile) | 卡片单列全宽；logo 48px 保持；统计行四项保持 `gap:12px`，数字 12px，必要时图标与数字 `gap:3px` 防溢出 |
| `≥ 768px` (tablet) | 2-3 列网格；统计行 `gap:16px` |
| `≥ 1024px` (desktop) | 3-4 列网格；统计行完整展示 |

> 统计行四项（浏览/点赞/收藏/下载）在 375px 宽度下须完整可见，禁止水平滚动；空间不足时优先压缩 `gap` 而非隐藏项。

---

## 6. 可访问性要求

- [ ] 统计项若可点击须有可读文字标签或 `aria-label`（如 `aria-label="浏览量 1234"`）
- [ ] logo `img` 必须有 `alt`（工具名称），装饰性占位图标 `aria-hidden="true"`
- [ ] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，`outline:2px solid; outline-offset:2px;`
- [ ] 统计数字与背景对比度满足 WCAG AA（暗色 `#a1a1aa`/`#09090b`=12.2:1，亮色 `#475569`/`#f8fafc`≥4.5:1）
- [ ] logo 上传错误提示使用 `role="alert"` 并紧邻控件
- [ ] 上传控件键盘可达（Enter/Space 触发文件选择）
- [ ] `prefers-reduced-motion: reduce` 下关闭骨架流光与卡片 hover 位移

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 浏览量 | `Eye` | `aria-hidden="true"` |
| 点赞量 | `Heart` | `aria-hidden="true"` |
| 收藏量 | `Bookmark` | `aria-hidden="true"` |
| 下载量 | `Download` | `aria-hidden="true"` |
| 工具占位 logo | `Wrench` | `aria-hidden="true"` |
| logo 上传 | `Upload` | `aria-hidden="true"` |
| 上传中 | `Loader2`（spin） | `aria-hidden="true"` |

> 图标颜色统一 `var(--text-muted)`（暗色 `#52525b` / 亮色 `#94a3b8`），不使用彩色图标，保持统计行克制、与参考稿一致。

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题（`var(--text-*)` / `var(--bg-*)` / `var(--accent-*)`）
- ✅ 统计数字使用 `var(--font-mono)` 等宽对齐
- ✅ logo 裂图有 `@error` 兜底，避免破图
- ✅ 卡片 hover 用 `translateY(-2px)`，不引起布局位移
- ❌ 避免 `!important`
- ❌ 避免统计行 hover 用 scale 导致位移
- ❌ 避免在 375px 下统计项换行或水平滚动
