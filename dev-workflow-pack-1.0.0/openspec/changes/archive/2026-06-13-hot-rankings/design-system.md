# Design System

> 本设计系统为热榜页面提供视觉规范，延续项目现有的赛博朋克暗色主题。

## 1. Design Style

| 属性 | 值 |
|------|------|
| **Style Name** | Cyberpunk Glassmorphism |
| **Keywords** | Dark mode, neon accents, glass effect, data dashboard, hot ranking |
| **Best For** | 数据展示页面、热榜排名、统计看板 |

## 2. Color Palette

| Role | Hex | CSS Variable | Usage |
|------|-----|--------------|-------|
| Background | #0D0D0D | --color-bg | 页面背景 |
| Surface | #0F172A | --color-surface | 卡片/容器背景 |
| Primary | #00FFFF | --color-primary | Cyan 主色调 |
| Secondary | #FF00FF | --color-secondary | Magenta 辅助色 |
| Accent | #00FF88 | --color-accent | Matrix Green 强调 |
| Text | #F8FAFC | --color-text | 主文字 |
| Text Muted | #94A3B8 | --color-text-muted | 次要文字 |
| Border | rgba(255,255,255,0.08) | --color-border | 边框色 |

## 3. Typography

| 用途 | 字体 | 字重 |
|------|------|------|
| 标题 | Fira Code, monospace | 600-700 |
| 正文 | Fira Sans, sans-serif | 400-500 |
| 辅助/标签 | Fira Code | 400 |

## 4. Spacing System

| Token | Value |
|-------|-------|
| `--space-xs` | 4px |
| `--space-sm` | 8px |
| `--space-md` | 16px |
| `--space-lg` | 24px |
| `--space-xl` | 32px |

## 5. Effects

| Token | Value | Usage |
|-------|-------|-------|
| `--radius-sm` | 8px | 小圆角 |
| `--radius-md` | 12px | 中圆角 |
| `--radius-lg` | 20px | 大圆角 |
| `--shadow-glow-cyan` | 0 0 20px rgba(0,255,255,0.3) | Cyan 光晕 |
| `--shadow-glow-magenta` | 0 0 20px rgba(255,0,255,0.3) | Magenta 光晕 |

## 6. Component Specs

### StatsCard

```css
.stats-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  transition: all 300ms ease;
  cursor: default;
}

.stats-card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-glow-cyan);
}
```

### RankList (ToolRankList / PostRankList)

```css
.rank-list {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.rank-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  padding: var(--space-md);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 200ms ease;
}

.rank-item:hover {
  background: rgba(255,255,255,0.05);
}
```

### Tab Chips

```css
.tab-chip {
  padding: var(--space-sm) var(--space-md);
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-muted);
  background: transparent;
  border: 1px solid var(--color-border);
  border-radius: 20px;
  cursor: pointer;
  transition: all 200ms ease;
}

.tab-chip:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.tab-chip.active {
  background: var(--color-primary);
  border-color: transparent;
  color: var(--color-bg);
  font-weight: 600;
}
```

## 7. Icon Specification

| 用途 | Icon Name |
|------|-----------|
| 用户统计 | Users |
| 帖子统计 | MessageSquare |
| 工具统计 | Wrench |
| 工具热榜 | Flame |
| 帖子热榜 | MessageCircle |

**规则**: 使用 @lucide/vue-next 图标库，禁止 emoji 作为图标。

## 8. Anti-Patterns

- ❌ 使用 emoji 作为 UI 图标
- ❌ 缺少 `cursor-pointer` 在可点击元素上
- ❌ 悬停状态使用 scale 变换导致布局位移
- ❌ 过度的装饰动画（扫描线、脉冲指示灯）
- ❌ 文字对比度低于 4.5:1
- ❌ 状态变化无过渡动画

## 9. Pre-Delivery Checklist

- [ ] 无 emoji 作为图标
- [ ] 可点击元素有 `cursor-pointer`
- [ ] 悬停状态有平滑过渡 (150-300ms)
- [ ] 文字对比度 ≥ 4.5:1
- [ ] 移除过度装饰动画
- [ ] 响应式布局正常 (375px, 768px, 1024px, 1440px)
