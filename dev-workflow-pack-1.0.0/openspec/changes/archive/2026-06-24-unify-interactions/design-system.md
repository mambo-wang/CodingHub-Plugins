## 1. 全局样式引用

### 字体
- **Display / 标题**: Sora (400/600/700)
- **Mono / 代码**: Space Mono (400/700)
- **Fallback**: system-ui, -apple-system, sans-serif

### 圆角
- 组件: `8px` (var(--radius))
- 卡片/面板: `16px` (var(--radius-lg))

### 阴影

| 角色 | 暗色主题 | 亮色主题 |
|------|---------|---------|
| sm | `0 2px 8px rgba(0,0,0,0.3)` | `0 2px 8px rgba(0,0,0,0.08)` |
| md | `0 4px 16px rgba(0,0,0,0.4)` | `0 4px 16px rgba(0,0,0,0.12)` |
| lg | `0 8px 32px rgba(0,0,0,0.5)` | `0 8px 32px rgba(0,0,0,0.16)` |
| glow (accent) | `0 0 20px rgba(139,92,246,0.3)` | `0 0 20px rgba(139,92,246,0.15)` |

## 2. 双主题 Tokens 映射

| 角色 | 暗色主题 | 亮色主题 | CSS 变量 |
|------|---------|---------|----------|
| 页面背景 | `#0a0a0f` | `#f5f5f7` | `--bg-page` |
| 面板/卡片 | `rgba(255,255,255,0.03)` | `rgba(255,255,255,0.8)` | `--bg-card` |
| 毛玻璃 | `rgba(255,255,255,0.05)` + `backdrop-filter: blur(20px)` | `rgba(255,255,255,0.7)` + `backdrop-filter: blur(20px)` | `--bg-glass` |
| 主色 (accent) | `#8b5cf6` | `#7c3aed` | `--accent` |
| 主色 hover | `rgba(139,92,246,0.15)` | `rgba(124,58,237,0.1)` | `--accent-hover` |
| 辅助色 | `#06b6d4` | `#0891b2` | `--accent-secondary` |
| 文字主色 | `#e4e4e7` | `#18181b` | `--text-primary` |
| 文字次色 | `#a1a1aa` | `#52525b` | `--text-secondary` |
| 文字弱色 | `#71717a` | `#a1a1aa` | `--text-muted` |
| 边框色 | `rgba(255,255,255,0.08)` | `rgba(0,0,0,0.08)` | `--border-color` |
| 危险色 | `#ef4444` | `#dc2626` | `--danger` |
| 成功色 | `#22c55e` | `#16a34a` | `--success` |

## 3. 涉及组件清单

| 组件/页面 | 用途 | 状态覆盖 |
|----------|------|---------|
| GeneralizedSidebar | 左侧导航栏，三个模块共用 | normal / active / hover / focus |
| UnifiedLikeButton | 统一点赞按钮 | normal / liked / hover / focus / loading |
| UnifiedCommentSection | 统一评论区（列表 + 编辑器 + 嵌套回复） | normal / empty / loading / submitting |
| UnifiedFavoriteButton | 统一收藏按钮 | normal / favorited / hover / focus / loading |
| MyToolFavoritesPage | 工具收藏列表 | normal / empty / loading |
| MyVideosPage | 我的微课列表 | normal / empty / loading |
| MyVideoFavoritesPage | 微课收藏列表 | normal / empty / loading |

## 4. 交互状态（双主题）

### GeneralizedSidebar

**暗色主题：**
- normal: `background: var(--bg-glass); border: 1px solid var(--border-color); width: 200px; border-radius: 16px;`
- hover (nav item): `background: rgba(139,92,246,0.1); color: var(--accent);`
- active (当前路由): `background: rgba(139,92,246,0.15); color: var(--accent); font-weight: 600; border-left: 3px solid var(--accent);`
- focus: `outline: 2px solid var(--accent); outline-offset: 2px;`

**亮色主题：**
- normal: `background: rgba(255,255,255,0.7); backdrop-filter: blur(20px); border: 1px solid rgba(0,0,0,0.08);`
- hover: `background: rgba(124,58,237,0.08); color: var(--accent);`
- active: `background: rgba(124,58,237,0.12); border-left: 3px solid #7c3aed;`
- focus: `outline: 2px solid #7c3aed; outline-offset: 2px;`

### UnifiedLikeButton

**暗色主题：**
- normal: `color: var(--text-muted); background: transparent; border: none;`
- liked: `color: #ef4444; fill: #ef4444;` (心形图标填充)
- hover: `color: #ef4444; transform: scale(1.1);`
- loading: `opacity: 0.5; pointer-events: none;` 显示 spinner
- focus: `outline: 2px solid var(--accent); outline-offset: 2px;`

**亮色主题：**
- normal: `color: #a1a1aa;`
- liked: `color: #dc2626; fill: #dc2626;`
- hover: `color: #dc2626; transform: scale(1.1);`

### UnifiedCommentSection

**暗色主题：**
- 评论卡片: `background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 8px; padding: 16px;`
- 嵌套回复缩进: `margin-left: 40px; border-left: 2px solid rgba(139,92,246,0.3);`
- 编辑器: `background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 8px;`
- 编辑器 focus: `border-color: var(--accent); box-shadow: 0 0 0 3px rgba(139,92,246,0.2);`

**亮色主题：**
- 评论卡片: `background: rgba(255,255,255,0.8); border: 1px solid rgba(0,0,0,0.08);`
- 嵌套回复缩进: `border-left: 2px solid rgba(124,58,237,0.2);`
- 编辑器 focus: `border-color: #7c3aed; box-shadow: 0 0 0 3px rgba(124,58,237,0.15);`

### UnifiedFavoriteButton

**暗色主题：**
- normal: `color: var(--text-muted);` 书签图标描边
- favorited: `color: #f59e0b; fill: #f59e0b;` (书签图标填充)
- hover: `color: #f59e0b; transform: scale(1.1);`

**亮色主题：**
- normal: `color: #a1a1aa;`
- favorited: `color: #d97706; fill: #d97706;`

## 5. 响应式策略

| 断点 | 布局行为 |
|------|---------|
| ≥ 1024px | sidebar (200px) + content (flex: 1)，标准双栏布局 |
| 768px - 1023px | sidebar 缩小为 icon-only (48px) + content，hover 展开 tooltip |
| ≤ 767px | sidebar 隐藏，改为顶部 tab bar（水平滚动），content 全宽 |

## 6. 可访问性要求

- [x] 所有交互元素有 `focus-visible` 焦点环
- [x] 暗色焦点环: `outline: 2px solid #8b5cf6; outline-offset: 2px;`
- [x] 亮色焦点环: `outline: 2px solid #7c3aed; outline-offset: 2px;`
- [x] SidebarNav 使用 `<nav aria-label="页面导航">`
- [x] LikeButton 有 `aria-label="点赞"` / `aria-pressed="true/false"`
- [x] FavoriteButton 有 `aria-label="收藏"` / `aria-pressed="true/false"`
- [x] CommentSection 使用 `role="feed"` 包裹评论列表
- [x] 颜色对比度 ≥ 4.5:1 (AA) 用于正文文本
- [x] 颜色对比度 ≥ 3:1 (AA) 用于大标题和图标

## 7. 图标清单

| 图标 (Lucide) | 组件 | aria-label |
|---------------|------|-----------|
| LayoutGrid | GeneralizedSidebar - 列表 | "查看列表" |
| FileText | GeneralizedSidebar - 我的XX | "我的内容" |
| PlayCircle | GeneralizedSidebar - 我的微课 | "我的微课" |
| Bookmark | GeneralizedSidebar - 收藏 | "我的收藏" |
| Heart | UnifiedLikeButton | "点赞" |
| MessageCircle | UnifiedCommentSection | "评论" |
| Bookmark | UnifiedFavoriteButton | "收藏" |
| Reply | UnifiedCommentSection - 回复 | "回复评论" |
| Send | UnifiedCommentSection - 提交 | "发送评论" |

## 8. Antipatterns 检查

| 规则 | 合规 |
|------|------|
| 不使用 Tailwind | ✅ 使用纯 CSS + CSS 变量 |
| 不使用 emoji 图标 | ✅ 使用 Lucide 内联 SVG |
| 不使用 `!important` | ✅ |
| 使用 `@lucide/vue` 图标库 | ✅ |
| 毛玻璃使用 `backdrop-filter` | ✅ |
| 组件使用 `<script setup lang="ts">` | ✅ |
| 所有 props 和 emits 有类型定义 | ✅ |
