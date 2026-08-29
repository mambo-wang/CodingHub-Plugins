# Tasks

## A. Atomic TDD Task List

### Feature: Tool 新增 viewCount 字段

- [x] RED: 编写失败测试——测试 Tool 实体包含 viewCount 字段，默认值为 0
- [x] GREEN: 最小实现——修改 Tool.java 添加 `viewCount` 字段（Integer 类型，默认 0）

---

### Feature: Tool 新增 likeCount 字段

- [x] RED: 编写失败测试——测试 Tool 实体包含 likeCount 字段，默认值为 0
- [x] GREEN: 最小实现——修改 Tool.java 添加 `likeCount` 字段（Integer 类型，默认 0）

---

### Feature: Tool 新增 commentCount 字段

- [x] RED: 编写失败测试——测试 Tool 实体包含 commentCount 字段，默认值为 0
- [x] GREEN: 最小实现——修改 Tool.java 添加 `commentCount` 字段（Integer 类型，默认 0）

---

### Feature: Tool 新增 score 字段

- [x] RED: 编写失败测试——测试 Tool 实体包含 score 字段，默认值为 BigDecimal.ZERO
- [x] GREEN: 最小实现——修改 Tool.java 添加 `score` 字段（BigDecimal 类型，默认 0）

---

### Feature: Tool 新增 updateScore 方法

- [x] RED: 编写失败测试——测试 Tool.updateScore() 正确计算 score = viewCount*1 + likeCount*3 + commentCount*5
- [x] GREEN: 最小实现——修改 Tool.java 添加 `updateScore()` 方法

---

### Feature: ForumPost 新增 score 字段

- [x] RED: 编写失败测试——测试 ForumPost 实体包含 score 字段，默认值为 BigDecimal.ZERO
- [x] GREEN: 最小实现——修改 ForumPost.java 添加 `score` 字段（BigDecimal 类型，默认 0）

---

### Feature: ForumPost 新增 updateScore 方法

- [x] RED: 编写失败测试——测试 ForumPost.updateScore() 正确计算 score
- [x] GREEN: 最小实现——修改 ForumPost.java 添加 `updateScore()` 方法

---

### Feature: ToolLike 实体创建

- [x] RED: 编写失败测试——测试 ToolLike 实体可以保存和查询
- [x] GREEN: 最小实现——创建 ToolLike.java 实体和 ToolLikeRepository

---

### Feature: 工具点赞功能

- [x] RED: 编写失败测试——测试 ToolService.likeTool() 正确增加 likeCount 和 score
- [x] GREEN: 最小实现——实现 ToolService.likeTool() 方法

---

### Feature: 工具取消点赞功能

- [x] RED: 编写失败测试——测试 ToolService.unlikeTool() 正确减少 likeCount 和 score
- [x] GREEN: 最小实现——实现 ToolService.unlikeTool() 方法

---

### Feature: 工具详情页浏览量更新

- [x] RED: 编写失败测试——测试访问工具详情时 viewCount 增加
- [x] GREEN: 最小实现——实现访问工具详情时调用 viewCount + 1

---

### Feature: 工具评论功能

- [x] RED: 编写失败测试——测试评论成功后 commentCount 增加
- [x] GREEN: 最小实现——实现评论成功后更新 commentCount 和 score

---

### Feature: 工具热榜按 score 排序

- [x] RED: 编写失败测试——测试工具按 score 降序排列
- [x] GREEN: 最小实现——修改 OverviewServiceImpl.getToolRanks() 按 score 排序

---

### Feature: 帖子热榜按 score 排序

- [x] RED: 编写失败测试——测试帖子按 score 降序排列
- [x] GREEN: 最小实现——修改 OverviewServiceImpl.getPostRanks() 按 score 排序

---

### Feature: ToolRankDto 添加 id 和 score 字段

- [x] RED: 编写失败测试——测试 ToolRankDto 包含 id 和 score 字段
- [x] GREEN: 最小实现——修改 ToolRankDto.java 添加 id、score 字段

---

### Feature: PostRankDto 添加 id 和 score 字段

- [x] RED: 编写失败测试——测试 PostRankDto 包含 id 和 score 字段
- [x] GREEN: 最小实现——修改 PostRankDto.java 添加 id、score 字段

---

## B. UI Implementation Tasks

### UI: StatsCard 组件优化

- [x] 实现 StatsCard——移除过度装饰动画，保持简洁的 hover 效果，参考 ui-preview.html
- [x] 验证 StatsCard——检查是否符合 design-system.md 规范

---

### UI: ToolRankList 组件优化

- [x] 实现 ToolRankList——添加点击跳转功能（router.push('/tools/' + item.id)），简化加载动画，移除脉冲指示灯
- [x] 验证 ToolRankList——检查点击条目是否能正确跳转

---

### UI: PostRankList 组件优化

- [x] 实现 PostRankList——添加点击跳转功能（router.push('/forum/posts/' + item.id)），简化加载动画，移除脉冲指示灯
- [x] 验证 PostRankList——检查点击条目是否能正确跳转

---

### UI: OverviewPage 主页面优化

- [x] 实现 OverviewPage——标题改为"热榜"，移除扫描线动画和动态网格背景，保持简洁布局
- [x] 验证 OverviewPage——检查页面标题和整体布局

---

### UI: DetailPage 工具详情页改造

- [x] 实现 DetailPage——添加点赞按钮、评论区域，显示 viewCount、likeCount、commentCount
- [x] 验证 DetailPage——检查点赞和评论功能是否正常

---

### UI: ToolLikeButton 点赞按钮组件

- [x] 实现 ToolLikeButton——点赞按钮组件，支持点赞/取消点赞状态切换
- [x] 验证 ToolLikeButton——检查按钮状态是否正确显示

---

### UI: ToolCommentList 评论列表组件

- [x] 实现 ToolCommentList——显示工具的评论列表
- [x] 验证 ToolCommentList——检查评论列表是否正确显示

---

### UI: ToolCommentEditor 评论编辑器组件

- [x] 实现 ToolCommentEditor——评论输入和提交组件
- [x] 验证 ToolCommentEditor——检查评论提交是否成功

---

### UI: 前端类型更新

- [x] 实现 overview.ts 类型更新——添加 id、score 字段到 ToolRankDto 和 PostRankDto 接口
- [x] 验证 overview.ts——检查类型定义与后端 DTO 一致

---

## D. Database Migration

> 需手动执行数据库迁移脚本

- [x] 执行 migration——为 tool 表添加 view_count, like_count, comment_count, score 字段
- [x] 执行 migration——为 forum_post 表添加 score 字段
- [x] 执行 migration——创建 tool_like 表
- [x] 执行 migration——为 score 字段添加索引