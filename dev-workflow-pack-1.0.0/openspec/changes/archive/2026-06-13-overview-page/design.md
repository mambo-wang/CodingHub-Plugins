# Design

## Overview

本次变更新增一个概览页面，展示平台热榜数据（工具热榜、帖子热榜）和统计信息（用户数、帖子总数、工具总数）。

## File Structure

### Backend (Java Spring Boot)

```
backend/src/main/java/com/iaihub/toolbox/
├── controller/
│   └── OverviewController.java          # 概览页面 API
├── service/
│   ├── OverviewService.java            # 概览业务逻辑
│   └── OverviewServiceImpl.java        # 实现
├── dto/
│   ├── StatsDto.java                    # 统计数据 DTO
│   ├── ToolRankDto.java                 # 工具热榜 DTO
│   └── PostRankDto.java                 # 帖子热榜 DTO
└── repository/
    └── (existing repositories)         # 复用现有 repository
```

**API 端点：**
- `GET /api/overview/stats` - 获取统计数据（用户总数、帖子总数、工具总数）
- `GET /api/overview/tool-ranks` - 获取工具热榜（按类别分组）
- `GET /api/overview/post-ranks` - 获取帖子热榜（按类别分组）

### Frontend (Vue 3 + TypeScript)

```
frontend/src/
├── pages/
│   └── OverviewPage.vue                # 概览页面主组件
├── components/
│   ├── StatsCard.vue                    # 统计卡片组件
│   ├── ToolRankList.vue                 # 工具热榜组件
│   ├── PostRankList.vue                 # 帖子热榜组件
│   └── RankItem.vue                     # 热榜条目组件
├── services/
│   └── overview.ts                      # 概览页 API 调用
└── types/
    └── overview.ts                     # TypeScript 类型定义
```

## Test Strategy

### Backend Tests

| 文件 | 测试策略 | 说明 |
|------|----------|------|
| `OverviewControllerTest.java` | 集成测试 | 测试 REST API 端点，使用 @WebMvcTest |
| `OverviewServiceTest.java` | 单元测试 | 使用 Mockito mock repository |

**测试用例：**
1. `GET /api/overview/stats` - 返回统计数据 JSON
2. `GET /api/overview/tool-ranks` - 返回按类别分组的工具列表
3. `GET /api/overview/post-ranks` - 返回按类别分组的帖子列表
4. 空数据时返回空数组而非 null

**运行命令：** `./gradlew test --tests "*Overview*"`

### Frontend Tests

| 文件 | 测试策略 | 说明 |
|------|----------|------|
| `OverviewPage.test.ts` | 组件测试 | 使用 Vitest + Vue Test Utils |
| `StatsCard.test.ts` | 组件单元测试 | 测试统计卡片渲染 |
| `ToolRankList.test.ts` | 组件测试 | 测试工具热榜列表 |

**测试用例：**
1. 页面加载时显示骨架屏
2. 数据加载成功后显示统计卡片
3. 工具热榜按类别分组展示
4. 错误状态显示重试按钮
5. 点击类别跳转对应列表

**运行命令：** `npm test -- --run`

## UI Component List

### 1. StatsCard (统计卡片)
- **用途：** 展示单一统计数据（用户数/帖子数/工具数）
- **状态：** default, loading (骨架屏)
- **设计：** 玻璃态卡片，暗色主题，霓虹强调色
- **Props：** `{ label: string, value: number, icon: string }`

### 2. RankItem (热榜条目)
- **用途：** 单个热榜项（工具或帖子）
- **状态：** default, hover
- **设计：** 水平布局，显示序号、标题、热度
- **Props：** `{ rank: number, title: string, count: number, link: string }`

### 3. RankList (热榜列表)
- **用途：** 展示某一类别的热榜列表
- **状态：** default, loading, empty, error
- **设计：** 垂直列表，类别标题 + 条目列表
- **Props：** `{ category: string, items: RankItem[], loading: boolean }`

### 4. ToolRankList (工具热榜容器)
- **用途：** 承载多个类别的工具热榜
- **状态：** default, loading, error
- **设计：** 网格布局，每行一个类别

### 5. PostRankList (帖子热榜容器)
- **用途：** 承载多个类别的帖子热榜
- **状态：** default, loading, error
- **设计：** 网格布局，每行一个类别

### 6. OverviewPage (主页面)
- **用途：** 概览页面容器，整合所有子组件
- **状态：** default, loading, error
- **布局：** 顶部统计卡片区 + 中部工具热榜 + 下部帖子热榜

## Page Layout

```
┌─────────────────────────────────────────────────────────────┐
│  概览                    [Platform Overview]                │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                     │
│  │ 👥 用户  │  │ 📝 帖子  │  │ 🛠️ 工具  │   StatsCards      │
│  │  1,234  │  │  5,678  │  │    89   │                     │
│  └─────────┘  └─────────┘  └─────────┘                     │
├─────────────────────────────────────────────────────────────┤
│  🔥 工具热榜                                                  │
│  ┌─────────────────────┐  ┌─────────────────────┐          │
│  │ AI 对话工具          │  │ 图像生成工具          │          │
│  │ 1. ChatGPT - 999热度 │  │ 1. Midjourney - 888  │          │
│  │ 2. Claude - 888热度  │  │ 2. DALL-E - 777热度  │          │
│  │ ...                  │  │ ...                  │          │
│  └─────────────────────┘  └─────────────────────┘          │
├─────────────────────────────────────────────────────────────┤
│  💬 帖子热榜                                                  │
│  ┌─────────────────────┐  ┌─────────────────────┐          │
│  │ 交流讨论            │  │ 技术问答              │          │
│  │ 1. xxx - 50评论     │  │ 1. xxx - 30评论      │          │
│  │ 2. xxx - 40评论     │  │ 2. xxx - 25评论      │          │
│  │ ...                  │  │ ...                  │          │
│  └─────────────────────┘  └─────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## Responsive Strategy

| 断点 | 布局 |
|------|------|
| < 640px (mobile) | 单列堆叠，统计卡片 1 列 |
| 640-1024px (tablet) | 统计卡片 2 列，热榜 1 列 |
| > 1024px (desktop) | 统计卡片 3 列，热榜 2 列 |

## Error Handling

- API 请求失败：显示错误消息 + 重试按钮
- 空数据：显示"暂无数据"提示
- 加载状态：骨架屏占位

## Dependencies

- 后端：复用现有的 UserRepository, ToolRepository, PostRepository
- 前端：复用现有的 @lucide/vue-next 图标库，Pinia 状态管理