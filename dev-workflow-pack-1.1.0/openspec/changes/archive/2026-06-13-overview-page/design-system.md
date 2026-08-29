# Design System

> 本设计系统由 ui-ux-pro-max skill 生成，定义概览页面的视觉规范。

## 1. Design Style

| 属性 | 值 |
|------|------|
| **Style Name** | Cyberpunk UI |
| **Keywords** | Neon, dark mode, terminal, HUD, sci-fi, glitch, futuristic, matrix |
| **Best For** | Gaming platforms, tech products, crypto apps, dashboards, developer tools |

## 2. Color Palette

| Role | Hex | CSS Variable | Usage |
|------|-----|--------------|-------|
| Primary | #0F172A | `--color-primary` | 深色卡片背景 |
| Secondary | #1E293B | `--color-secondary` | 次级背景 |
| Background | #020617 | `--color-background` | 页面背景 |
| Surface | #0F172A | `--color-surface` | 卡片/容器背景 |
| Text | #F8FAFC | `--color-text` | 主文字 |
| Text Muted | #94A3B8 | `--color-text-muted` | 次要文字 |
| Border | #1E293B | `--color-border` | 边框色 |
| Accent Cyan | #00FFFF | `--color-accent-cyan` | 强调色-青色 |
| Accent Magenta | #FF00FF | `--color-accent-magenta` | 强调色-品红 |
| Accent Green | #22C55E | `--color-accent-green` | 成功/CTA |

## 3. Typography

| 用途 | 字体 | 字重 |
|------|------|------|
| 标题 | Fira Code, monospace | 600-700 |
| 正文 | Fira Sans, sans-serif | 400-500 |
| 辅助 | Fira Sans, sans-serif | 300-400 |

**Google Fonts:**
```css
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@300;400;500;600;700&display=swap');
```

## 4. Spacing System

| Token | Value |
|-------|-------|
| `--space-xs` | 4px |
| `--space-sm` | 8px |
| `--space-md` | 16px |
| `--space-lg` | 24px |
| `--space-xl` | 32px |
| `--space-2xl` | 48px |

## 5. Effects

| Token | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | 0 1px 2px rgba(0,0,0,0.5) | 轻微阴影 |
| `--shadow-md` | 0 4px 6px rgba(0,0,0,0.5) | 卡片/按钮 |
| `--shadow-glow-cyan` | 0 0 20px rgba(0,255,255,0.3) | 青色发光 |
| `--shadow-glow-magenta` | 0 0 20px rgba(255,0,255,0.3) | 品红发光 |
| `--radius-sm` | 4px | 小圆角 |
| `--radius-md` | 8px | 中圆角 |
| `--radius-lg` | 12px | 大圆角 |
| `--radius-xl` | 16px | 超大圆角 |

## 6. Component Specs

### StatsCard (统计卡片)

```css
.stats-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  backdrop-filter: blur(10px);
  transition: all 200ms ease;
  cursor: pointer;
}

.stats-card:hover {
  border-color: var(--color-accent-cyan);
  box-shadow: var(--shadow-glow-cyan);
}

.stats-card .icon {
  width: 40px;
  height: 40px;
  color: var(--color-accent-cyan);
}

.stats-card .value {
  font-family: 'Fira Code', monospace;
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text);
}

.stats-card .label {
  font-size: 0.875rem;
  color: var(--color-text-muted);
}
```

### RankList (热榜列表)

```css
.rank-list {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-md);
  transition: all 200ms ease;
}

.rank-list:hover {
  border-color: var(--color-accent-magenta);
  box-shadow: var(--shadow-glow-magenta);
}

.rank-list .category-title {
  font-family: 'Fira Code', monospace;
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-accent-cyan);
  margin-bottom: var(--space-md);
}
```

### RankItem (热榜条目)

```css
.rank-item {
  display: flex;
  align-items: center;
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-sm);
  transition: all 150ms ease;
  cursor: pointer;
}

.rank-item:hover {
  background: var(--color-secondary);
}

.rank-item .rank {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Fira Code', monospace;
  font-size: 0.75rem;
  font-weight: 600;
  background: var(--color-accent-cyan);
  color: var(--color-primary);
  border-radius: var(--radius-sm);
  margin-right: var(--space-sm);
}

.rank-item .title {
  flex: 1;
  font-size: 0.875rem;
  color: var(--color-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.rank-item .count {
  font-family: 'Fira Code', monospace;
  font-size: 0.75rem;
  color: var(--color-text-muted);
}
```

### CategoryTab (类别 Tab 切换)

```css
.category-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  border: 1.5px solid var(--color-border);
  border-radius: 25px;
  background: var(--color-surface);
  color: var(--color-text-muted);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.category-tab:hover {
  border-color: var(--color-accent-cyan);
  color: var(--color-accent-cyan);
  background: rgba(0, 255, 255, 0.05);
}

.category-tab.active {
  background: linear-gradient(135deg, var(--color-accent-cyan), var(--color-accent-magenta));
  border-color: transparent;
  color: var(--color-primary);
  font-weight: 600;
  box-shadow: 0 4px 20px rgba(0, 255, 255, 0.3);
}
```

### ContentPanel (内容面板)

```css
.content-panel {
  background: var(--color-surface);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-top: none;
  border-radius: 0 0 var(--radius-xl) var(--radius-xl);
  padding: var(--space-md);
  min-height: 380px;
}
```

## 7. Icon Specification

| 用途 | Icon Name |
|------|-----------|
| 用户统计 | Users (Lucide) |
| 帖子统计 | MessageSquare (Lucide) |
| 工具统计 | Wrench (Lucide) |
| 热榜标识 | Flame (Lucide) |
| 加载中 | Loader2 (Lucide) |
| 重试 | RefreshCw (Lucide) |
| 错误 | AlertCircle (Lucide) |

**规则**: 使用 SVG 图标库（Lucide），禁止 emoji 作为图标。

## 8. Glassmorphism Effects

```css
.glass-card {
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-lg);
}

.neon-glow-cyan {
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3),
              0 0 40px rgba(0, 255, 255, 0.1);
}

.neon-glow-magenta {
  box-shadow: 0 0 20px rgba(255, 0, 255, 0.3),
              0 0 40px rgba(255, 0, 255, 0.1);
}
```

## 9. Anti-Patterns

- ❌ 使用 emoji 作为 UI 图标
- ❌ 缺少 `cursor-pointer` 在可点击元素上
- ❌ 悬停状态使用 scale 变换导致布局位移
- ❌ 文字对比度低于 4.5:1
- ❌ 状态变化无过渡动画
- ❌ focus 状态不可见
- ❌ 在暗色主题中使用浅色背景卡片

## 10. Pre-Delivery Checklist

- [ ] 无 emoji 作为图标
- [ ] 可点击元素有 `cursor-pointer`
- [ ] 悬停状态有平滑过渡 (150-300ms)
- [ ] 文字对比度 ≥ 4.5:1
- [ ] focus 状态可见
- [ ] 响应式布局正常 (375px, 768px, 1024px, 1440px)
- [ ] 霓虹发光效果正确显示
- [ ] 玻璃态效果正常渲染