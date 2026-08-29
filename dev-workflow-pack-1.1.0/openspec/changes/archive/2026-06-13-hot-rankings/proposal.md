# Proposal: 热榜页面优化

## Problem

当前概览页存在以下问题：
1. 页面名称为"数据概览"，但实际展示的是热榜内容，名称与功能不匹配
2. 工具 (Tool) 没有 viewCount、likeCount、commentCount、score 字段，无法计算热度
3. 工具详情页 (`/tools/{id}`) 没有点赞和评论功能，无法增加工具热度
4. 工具和帖子没有统一的 score 字段，排名规则不明确
5. 部分装饰性 UI 元素过于复杂（如扫描线动画、脉冲指示灯），影响用户体验
6. 热榜数据使用模拟数据，未与真实分类关联
7. 热榜条目点击后无法跳转至详情页，功能不完整

## Solution

### 1. 为 Tool 实体新增字段

| 字段名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| viewCount | Integer | 0 | 浏览次数 |
| likeCount | Integer | 0 | 点赞次数 |
| commentCount | Integer | 0 | 评论次数 |
| score | BigDecimal | 0 | 综合热度评分 |

### 2. 为 ForumPost 实体新增 score 字段

ForumPost 已有 viewCount、likeCount、commentCount，只需新增 score 字段。

### 3. score 计算规则

```
score = viewCount * 1 + likeCount * 3 + commentCount * 5
```

| 指标 | 权重 | 说明 |
|------|------|------|
| viewCount | × 1 | 浏览量权重最低 |
| likeCount | × 3 | 点赞量权重中等 |
| commentCount | × 5 | 评论量权重最高，代表参与度 |

### 4. 工具详情页新增点赞和评论功能

- 工具详情页添加点赞按钮，点击后更新 Tool.likeCount 和 score
- 工具详情页添加评论区域，评论成功后更新 Tool.commentCount 和 score
- 浏览工具详情时自动更新 Tool.viewCount 和 score

### 5. 帖子详情页更新 score

- 帖子详情页已有浏览/点赞/评论功能，需添加 updateScore 逻辑

## Testable Behaviors

### 页面基础功能
- WHEN 用户访问 `/overview` THEN 页面显示热榜内容
- WHEN 热榜数据加载完成 THEN 显示对应的工具和帖子列表

### 数据模型 - Tool
- WHEN 创建新工具时 THEN `viewCount` = 0, `likeCount` = 0, `commentCount` = 0, `score` = 0
- WHEN 工具被查看时 THEN `viewCount` + 1，`score` 按权重更新
- WHEN 工具被点赞时 THEN `likeCount` + 1，`score` 按权重更新
- WHEN 工具被评论时 THEN `commentCount` + 1，`score` 按权重更新

### 数据模型 - ForumPost
- WHEN 创建新帖子时 THEN `score` = 0
- WHEN 帖子被查看/点赞/评论时 THEN `score` 按权重累加

### 工具详情页 - 点赞功能
- WHEN 用户点击点赞按钮 THEN `Tool.likeCount` + 1，`score` 按权重更新
- WHEN 用户再次点击点赞按钮 THEN 取消点赞，`Tool.likeCount` - 1，`score` 相应减少
- WHEN 用户未登录时点击点赞按钮 THEN 提示登录

### 工具详情页 - 评论功能
- WHEN 用户提交评论 THEN `Tool.commentCount` + 1，`score` 按权重更新
- WHEN 评论成功后 THEN 显示评论列表更新

### 工具详情页 - 浏览量
- WHEN 用户访问工具详情页 THEN `Tool.viewCount` + 1，`score` 按权重更新

### 排名规则
- WHEN 工具热榜展示 THEN 按 `score` 降序排列
- WHEN 帖子热榜展示 THEN 按 `score` 降序排列
- WHEN score 相同时 THEN 按创建时间倒序排列

### 数据展示
- WHEN 工具热榜显示分类标签 THEN 使用真实的工具分类名称
- WHEN 帖子热榜显示分类标签 THEN 使用真实的帖子分类名称
- WHEN 数据为空时 THEN 显示"暂无数据"占位

### 交互功能
- WHEN 用户点击工具条目 THEN 跳转到工具详情页 `/tools/{id}`
- WHEN 用户点击帖子条目 THEN 跳转到帖子详情页 `/forum/posts/{id}`

### UI 简化
- WHEN 页面渲染 THEN 移除过度的装饰动画（扫描线、脉冲指示灯等）
- WHEN 页面加载 THEN 使用简洁的骨架屏加载状态

## Acceptance Criteria

1. **数据模型 - Tool**
   - [ ] Tool 实体新增 `viewCount` 字段（Integer，默认 0）
   - [ ] Tool 实体新增 `likeCount` 字段（Integer，默认 0）
   - [ ] Tool 实体新增 `commentCount` 字段（Integer，默认 0）
   - [ ] Tool 实体新增 `score` 字段（BigDecimal，默认 0）
   - [ ] Tool 实体新增 `updateScore()` 方法

2. **数据模型 - ForumPost**
   - [ ] ForumPost 实体新增 `score` 字段（BigDecimal，默认 0）
   - [ ] ForumPost 实体新增 `updateScore()` 方法

3. **工具详情页功能**
   - [ ] 工具详情页显示点赞数 (likeCount)
   - [ ] 工具详情页显示评论数 (commentCount)
   - [ ] 工具详情页有点赞按钮，点击后更新 Tool.likeCount 和 score
   - [ ] 工具详情页有评论区域，评论成功后更新 Tool.commentCount 和 score
   - [ ] 访问工具详情页时自动更新 viewCount 和 score

4. **帖子详情页功能**
   - [ ] 帖子详情页已有点赞/评论功能，添加 updateScore 逻辑

5. **排名功能**
   - [ ] 工具热榜按 `score` 降序排列
   - [ ] 帖子热榜按 `score` 降序排列

6. **页面优化**
   - [ ] 页面标题改为"热榜"或"Hot Rankings"
   - [ ] 分类标签使用数据库中的真实分类名称
   - [ ] 移除多余的装饰性动画

7. **交互功能**
   - [ ] 点击工具条目可正常跳转至工具详情页 `/tools/{id}`
   - [ ] 点击帖子条目可正常跳转至帖子详情页 `/forum/posts/{id}`

8. **UI 风格**
   - [ ] 保持现有的赛博朋克暗色主题风格