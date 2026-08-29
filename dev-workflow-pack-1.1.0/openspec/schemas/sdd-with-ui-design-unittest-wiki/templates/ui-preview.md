# UI Preview: [变更名称]（双主题）

> 本预览基于 design-system.md 与 ui-ux-pro-max 设计规范生成，作为视觉验收标准。
> 参考 `openspec/changes/add-post-delete/ui-preview.html` 的双主题实现模式。

## 预览文件

**路径:** `ui-preview.html`

## 双主题 CSS 变量方案

```css
:root {
  /* 暗色主题（默认） */
  --bg-primary: #09090b;
  --bg-secondary: #0f0f12;
  --bg-card: rgba(15,15,20,0.7);
  --bg-glass: rgba(255,255,255,0.03);
  --accent-1: #8b5cf6;
  --accent-2: #06b6d4;
  --accent-3: #ec4899;
  --text-primary: #fafafa;
  --text-secondary: #a1a1aa;
  --text-muted: #52525b;
  --border-color: rgba(255,255,255,0.08);
  --border-glow: rgba(139,92,246,0.3);
  --focus-ring: #00FFFF;
  /* ... 其他暗色变量 */
}

[data-theme="light"] {
  /* 亮色主题覆盖 */
  --bg-primary: #f8fafc;
  --bg-secondary: #f1f5f9;
  --bg-card: rgba(255,255,255,0.9);
  --bg-glass: rgba(255,255,255,0.8);
  --accent-1: #7c3aed;
  --accent-2: #0891b2;
  --accent-3: #db2777;
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  --border-color: rgba(0,0,0,0.08);
  --border-glow: rgba(124,58,237,0.3);
  --focus-ring: #7c3aed;
  /* ... 其他亮色变量 */
}
```

## 页面结构

```
<html data-theme="dark">
  <head>内联 <style> 全部 CSS + 双主题变量</head>
  <body>
    <div class="grid-overlay"></div>
    <div class="container">
      <!-- 页面头部 -->
      <div class="page-header">
        渐变标题 + 副标题 + 主题切换按钮
      </div>

      <!-- 组件 1 状态预览 -->
      <h2>1. 组件A</h2>
      <h3>1.1 状态行 <span class="theme-badge theme-badge-dk">暗色</span></h3>
      <div class="state-row">normal / hover / focus / loading</div>
      <h3>1.2 状态行 <span class="theme-badge theme-badge-lt">浅色</span></h3>
      <div class="state-row">normal / hover / focus / loading</div>

      <!-- 组件 2 ... -->

      <!-- 响应式预览 -->
      <h2>响应式预览</h2>
      <div class="responsive-grid">
        Desktop / Tablet / Mobile 三列
      </div>

      <!-- 可访问性检查清单 -->
      <h2>可访问性 (a11y) 检查</h2>
      <ul class="checklist">...</ul>
    </div>
    <script>toggleTheme() 切换 data-theme</script>
  </body>
</html>
```

## 截图

### Desktop (≥1024px) — 暗色主题

### Desktop (≥1024px) — 亮色主题

### Tablet (768px - 1023px)

### Mobile (<768px)

## 关键组件

| 组件 | 状态 | 暗色效果 | 亮色效果 |
|------|------|----------|----------|
| `<component>` | normal / hover / loading / empty | `<描述>` | `<描述>` |

## 交互验证

| 元素 | 交互 | 暗色预期 | 亮色预期 |
|------|------|----------|----------|
| 主题切换按钮 | click | 切换到亮色 | 切换到暗色 |
| `<element>` | hover / focus | `<暗色行为>` | `<亮色行为>` |

## 合规性检查

- [ ] 配色方案符合 design-system.md 双主题 token 映射
- [ ] 字体系统一致（Sora + Space Mono）
- [ ] 间距系统一致
- [ ] 暗色/亮色组件样式分别匹配
- [ ] 图标使用内联 SVG（Lucide），无 emoji
- [ ] 响应式布局三断点正常
- [ ] 悬停/聚焦状态双主题均正常
- [ ] 焦点环暗色 #00FFFF / 亮色 #7c3aed
- [ ] 主题切换平滑过渡（transition: background .4s, color .4s）
- [ ] prefers-reduced-motion 已处理
