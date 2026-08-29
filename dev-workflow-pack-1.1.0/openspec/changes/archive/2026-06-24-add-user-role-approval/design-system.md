# Design System: add-user-role-approval（双主题）

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
| 焦点评点环 | `#00FFFF` | `#7c3aed` | `--focus-ring` |
| 危险色 | `#EF4444` | `#EF4444` | — |
| 警告色 | `#FFB020` | `#FFB020` | — |
| 成功色 | `#10b981` | `#10b981` | — |

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
| `RegisterPage.vue`（修改） | 注册表单新增角色选择（USER/ADMIN 单选卡片） | normal / hover / focus / selected / disabled / loading / error |
| `LoginPage.vue`（修改） | 登录失败时展示 PENDING/REJECTED/DISABLED 状态提示 | normal / error / loading |
| `ApprovalPage.vue`（新增） | 超管审批待审管理员注册申请列表 | normal / loading / empty / error / success-toast |
| `UserListPage.vue`（新增） | 管理员/超管查看用户列表，超管可封禁/解禁/删除 | normal / loading / empty / error / confirm-dialog |
| `NavBar.vue`（修改） | 按角色显示「审批管理」「用户管理」入口 | normal / hover / active / hidden |
| `RoleSelector.vue`（新增子组件） | 注册页角色选择卡片组 | normal / hover / selected / focus |

---

## 4. 交互状态（双主题）

### 4.1 RoleSelector — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); border-radius: 8px; padding: 16px; cursor: pointer; transition: all 0.25s ease;` |
| hover | `border-color: var(--border-glow); box-shadow: var(--shadow-sm); transform: translateY(-1px);` |
| focus | `outline: 2px solid #00FFFF; outline-offset: 2px;` |
| selected | `border-color: var(--accent-1); background: rgba(139,92,246,0.1); box-shadow: 0 0 0 3px rgba(139,92,246,0.15);` |
| disabled | `opacity: 0.5; cursor: not-allowed;` |

### 4.2 RoleSelector — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-glass); border: 1px solid var(--border-color); border-radius: 8px; padding: 16px; cursor: pointer; transition: all 0.25s ease;` |
| hover | `border-color: var(--border-glow); box-shadow: var(--shadow-sm); transform: translateY(-1px);` |
| focus | `outline: 2px solid #7c3aed; outline-offset: 2px;` |
| selected | `border-color: var(--accent-1); background: rgba(124,58,237,0.08); box-shadow: 0 0 0 3px rgba(124,58,237,0.12);` |
| disabled | `opacity: 0.5; cursor: not-allowed;` |

### 4.3 ApprovalPage 审批卡片 — 暗色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; padding: 20px; backdrop-filter: blur(20px);` |
| hover | `border-color: var(--border-glow); box-shadow: var(--shadow-md);` |
| loading | `opacity: 0.7; pointer-events: none;` + spinner |
| empty | 居中图标 `UserCheck` + 「暂无待审批申请」+ `var(--text-muted)` |
| error | `border-color: #EF4444;` + `role="alert"` 错误条 |

### 4.4 ApprovalPage 审批卡片 — 亮色主题

| 状态 | 样式 |
|------|------|
| normal | `background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 16px; padding: 20px; backdrop-filter: blur(20px);` |
| hover | `border-color: var(--border-glow); box-shadow: var(--shadow-md);` |
| loading | `opacity: 0.7; pointer-events: none;` + spinner |
| empty | 居中图标 `UserCheck` + 「暂无待审批申请」+ `var(--text-muted)` |
| error | `border-color: #EF4444;` + `role="alert"` 错误条 |

### 4.5 审批操作按钮 — 双主题通用

| 按钮 | 暗色样式 | 亮色样式 |
|------|----------|----------|
| 通过 | `background: linear-gradient(135deg, #10b981, #059669); color: white;` | 同暗色 |
| 拒绝 | `background: transparent; border: 1.5px solid #EF4444; color: #EF4444;` | 同暗色 |
| 通过 hover | `box-shadow: 0 4px 16px rgba(16,185,129,0.4); transform: translateY(-1px);` | 同暗色 |
| 拒绝 hover | `background: rgba(239,68,68,0.1); box-shadow: 0 4px 16px rgba(239,68,68,0.2);` | 同暗色 |

### 4.6 UserListPage 用户表格行 — 双主题通用

| 状态 | 暗色样式 | 亮色样式 |
|------|----------|----------|
| normal | `background: var(--bg-card); border-bottom: 1px solid var(--border-color);` | 同暗色 |
| hover | `background: rgba(139,92,246,0.05);` | `background: rgba(124,58,237,0.04);` |
| 状态徽章-ACTIVE | `background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.3);` | 同暗色 |
| 状态徽章-PENDING | `background: rgba(255,176,32,0.15); color: #FFB020; border: 1px solid rgba(255,176,32,0.3);` | 同暗色 |
| 状态徽章-REJECTED | `background: rgba(239,68,68,0.15); color: #EF4444; border: 1px solid rgba(239,68,68,0.3);` | 同暗色 |
| 状态徽章-DISABLED | `background: rgba(161,161,170,0.15); color: var(--text-muted); border: 1px solid var(--border-color);` | 同暗色 |
| 角色徽章-USER | `background: var(--bg-glass); color: var(--text-secondary); border: 1px solid var(--border-color);` | 同暗色 |
| 角色徽章-ADMIN | `background: rgba(6,182,212,0.15); color: var(--accent-2); border: 1px solid rgba(6,182,212,0.3);` | `background: rgba(8,145,178,0.12); color: var(--accent-2);` |
| 角色徽章-SUPER_ADMIN | `background: rgba(139,92,246,0.15); color: var(--accent-1); border: 1px solid rgba(139,92,246,0.3);` | `background: rgba(124,58,237,0.12); color: var(--accent-1);` |

### 4.7 NavBar 管理入口 — 双主题通用

| 状态 | 样式 |
|------|------|
| normal | `color: var(--text-secondary); padding: 8px 16px; border-radius: 8px; cursor: pointer; transition: all 0.2s ease;` |
| hover | `color: var(--text-primary); background: var(--bg-glass);` |
| active | `color: var(--accent-1); background: rgba(139,92,246,0.1);` |
| hidden | `display: none;`（角色不匹配时不渲染） |

---

## 5. 响应式策略

| 断点 | 行为 |
|------|------|
| `< 768px` (mobile) | 审批卡片单列全宽；用户表格改为卡片堆叠（每行一张卡片）；RoleSelector 单列 |
| `≥ 768px` (tablet) | 审批卡片单列居中最大宽 600px；用户表格正常显示；RoleSelector 双列 |
| `≥ 1024px` (desktop) | 审批卡片单列最大宽 720px；用户表格全宽；RoleSelector 双列并排 |

---

## 6. 可访问性要求

- [ ] 所有按钮有可读文字标签或 `aria-label`
- [ ] 纯图标按钮（删除/封禁）必须有 `aria-label`
- [ ] 审批确认弹窗使用 `role="dialog"` + `aria-modal="true"` + `aria-labelledby`
- [ ] 暗色焦点环 `#00FFFF` / 亮色焦点环 `#7c3aed`，offset 2px，`outline: 2px solid`
- [ ] 颜色对比度满足 WCAG AA
- [ ] `prefers-reduced-motion: reduce` 媒体查询下关闭动画
- [ ] 错误提示使用 `role="alert"`
- [ ] 键盘可达：Tab 循环、Esc 关闭弹窗、Enter 触发审批
- [ ] 装饰图标 `aria-hidden="true"`
- [ ] RoleSelector 使用 `role="radiogroup"` + `role="radio"` + `aria-checked`
- [ ] 用户表格状态徽章有 `aria-label` 描述完整状态

---

## 7. 图标清单

| 用途 | Lucide 图标 | aria |
|------|-------------|------|
| 普通用户角色 | `User` | `aria-hidden="true"` |
| 管理员角色 | `Shield` | `aria-hidden="true"` |
| 超级管理员角色 | `Crown` | `aria-hidden="true"` |
| 审批通过按钮 | `Check` | `aria-label="通过审批"` |
| 审批拒绝按钮 | `X` | `aria-label="拒绝审批"` |
| 待审批列表空状态 | `UserCheck` | `aria-hidden="true"` |
| 用户列表空状态 | `Users` | `aria-hidden="true"` |
| 封禁用户按钮 | `Ban` | `aria-label="封禁用户"` |
| 解禁用户按钮 | `Unlock` | `aria-label="解禁用户"` |
| 删除用户按钮 | `Trash2` | `aria-label="删除用户"` |
| 导航-审批管理 | `ClipboardCheck` | `aria-hidden="true"` |
| 导航-用户管理 | `Users` | `aria-hidden="true"` |
| 状态-等待中 | `Clock` | `aria-hidden="true"` |
| 状态-已拒绝 | `XCircle` | `aria-hidden="true"` |
| 状态-已禁用 | `Ban` | `aria-hidden="true"` |
| 状态-正常 | `CheckCircle` | `aria-hidden="true"` |
| 搜索用户 | `Search` | `aria-hidden="true"` |
| 加载中 | `Loader2` | `aria-hidden="true"` + spin |

---

## 8. Antipatterns 检查

- ✅ 使用 Lucide 图标，无 emoji
- ✅ 使用 CSS 变量实现双主题
- ✅ 所有状态变化有过渡动画（0.2s-0.3s ease）
- ✅ `cursor: pointer` 在所有可点击元素上
- ✅ RoleSelector 使用语义化 `role="radio"` 而非纯 div
- ✅ 状态徽章同时用颜色+文字+图标三重表达（不依赖颜色单一通道）
- ❌ 避免 `!important`
- ❌ 避免悬停 scale 导致布局位移（使用 translateY）
- ❌ 避免表格在移动端水平滚动（改为卡片堆叠）
