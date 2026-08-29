# Design System - User Nickname Feature

## UI Components

### 1. NicknameInput Component

**Purpose:** 注册页面昵称输入框

**Props:**
```typescript
interface NicknameInputProps {
  modelValue: string
  error?: string
  disabled?: boolean
}
```

**States:**
- Default: 灰色边框，输入框空白
- Focus: 紫色边框高亮
- Error: 红色边框 + 错误提示文字
- Disabled: 半透明不可编辑

**Visual:**
```
┌─────────────────────────────────────┐
│ 昵称                                 │
│ ┌─────────────────────────────────┐ │
│ │ 输入一个好听的昵称                 │ │
│ └─────────────────────────────────┘ │
│ 2-10个字符，可使用中文、字母、数字     │
└─────────────────────────────────────┘
```

**Styling:**
- 标签字体: 14px, `var(--text-secondary)`
- 输入框: 16px, `var(--bg-input)`, border-radius 12px
- 占位符: `var(--text-placeholder)`
- 错误提示: 12px, `var(--error)`

---

### 2. AuthorBadge Component

**Purpose:** 通用作者信息展示组件，用于工具/帖子列表和详情页

**Props:**
```typescript
interface AuthorBadgeProps {
  username: string
  nickname?: string | null
  size?: 'sm' | 'md' | 'lg'
  showTooltip?: boolean
}
```

**Display Format:**
- 有昵称: `昵称(账号)` → 如 `王宝(wangbao)`
- 无昵称: `账号` → 如 `wangbao`

**States:**
- Default: 显示格式化后的作者名
- Hover: 显示完整 tooltip，包含账号

**Visual:**
```
尺寸规格:
- sm: 12px (列表小字)
- md: 14px (正文)
- lg: 16px (标题旁)

Tooltip 提示:
"账号: wangbao"
```

**Styling:**
- 容器: inline-flex, align-items: center
- 字体: `var(--text-secondary)`
- Hover: `var(--text-primary)`, cursor: pointer

---

### 3. UserDisplay Component

**Purpose:** 右上角用户信息展示

**Display Logic:**
```typescript
const displayName = authStore.user?.nickname || authStore.user?.username
// 有昵称显示昵称，无昵称显示账号
```

**Visual:**
```
┌─────────────────────────────────────┐
│                        👤 王宝  ▼   │  ← 昵称
└─────────────────────────────────────┘

未设置昵称时:
┌─────────────────────────────────────┐
│                        👤 wangbao ▼ │
└─────────────────────────────────────┘
```

**Dropdown Menu:**
- 用户名 (账号)
- 昵称 (如果有)
- 分隔线
- 我的工具
- 我的帖子
- 我的收藏
- 退出登录

---

## Page Layouts

### Register Page (注册页)

**Structure:**
```
┌────────────────────────────────────────┐
│           [装饰背景]                     │
│  ┌──────────────────────────────────┐  │
│  │  👤 创建账号                      │  │
│  │                                  │  │
│  │  用户名                          │  │
│  │  ┌────────────────────────────┐  │  │
│  │  │ 选择一个好听的名字          │  │  │
│  │  └────────────────────────────┘  │  │
│  │                                  │  │
│  │  昵称 ← 新增                      │  │
│  │  ┌────────────────────────────┐  │  │
│  │  │ 输入一个好听的昵称          │  │  │
│  │  └────────────────────────────┘  │  │
│  │  2-10个字符，可使用中文          │  │
│  │                                  │  │
│  │  密码                            │  │
│  │  ┌────────────────────────────┐  │  │
│  │  │ ••••••••                   │  │  │
│  │  └────────────────────────────┘  │  │
│  │                                  │  │
│  │  [        注册        ]          │  │
│  │                                  │  │
│  │  已有账号? 登录                  │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

---

### AppHeader (顶部导航栏)

**Structure:**
```
┌────────────────────────────────────────────────────────────┐
│ 🏠 工具广场  │ 📖 论坛  │ 📊 热榜  │ [更多▼]  │  [🌙/☀️] │
│                                              │ [登录/注册] │ ← 未登录
│                                              │ 👤 王宝 ▼  │ ← 已登录
└────────────────────────────────────────────────────────────┘
```

**User Dropdown (已登录):**
```
┌─────────────────────────┐
│ 👤 王宝 (wangbao)       │ ← 昵称(账号)
│    ─────────────────    │
│ 📦 我的工具             │
│ 📝 我的帖子             │
│ ⭐ 我的收藏             │
│    ─────────────────    │
│ 🚪 退出登录             │
└─────────────────────────┘
```

---

## Tool/Post Author Display

### Tool Card (工具卡片)
```
┌─────────────────────────────┐
│ [工具图标]  工具名称         │
│                             │
│ 描述描述描述...              │
│                             │
│ 👍 123  💬 45  👤 王宝(wangbao) │ ← 作者信息
└─────────────────────────────┘
```

### Post Card (帖子卡片)
```
┌─────────────────────────────┐
│ 帖子标题                    │
│ 帖子内容摘要...             │
│                             │
│ 📅 2026-06-01  👤 王宝(wangbao) │
└─────────────────────────────┘
```

### Tool/Post Detail Author Section
```
┌─────────────────────────────┐
│ 上传者                      │
│ ┌─────────────────────────┐ │
│ │ 👤 王宝(wangbao)        │ │ ← AuthorBadge 组件
│ │ hover: 账号: wangbao    │ │
│ └─────────────────────────┘ │
│ 上传时间: 2026-06-01        │
└─────────────────────────────┘
```

---

## Responsive Strategy

| Breakpoint | AuthorBadge 尺寸 | Header |
|------------|-----------------|--------|
| >= 768px (Desktop) | md (14px) | 显示完整用户名 |
| < 768px (Mobile) | sm (12px) | 截断显示，超长省略 |

---

## Error States

### Register Form Errors

| 场景 | 提示文案 |
|------|---------|
| 昵称为空 | 昵称不能为空 |
| 昵称太短 | 昵称长度需在2-10字符之间 |
| 昵称太长 | 昵称长度需在2-10字符之间 |
| 昵称已存在 | 昵称已被使用 |
| 昵称格式错误 | 昵称只能使用中文、字母、数字 |

---

## Animation

- 输入框 Focus: border-color 0.2s ease
- AuthorBadge Hover: color 0.15s ease
- Dropdown: fadeIn 0.15s ease, translateY(-4px → 0)