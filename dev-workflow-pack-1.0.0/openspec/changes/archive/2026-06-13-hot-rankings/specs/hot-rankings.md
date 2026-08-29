# Spec: 热榜页面优化

## Scenarios

### Scenario 1: 页面标题显示
- GIVEN: 用户访问 `/overview` 页面
- WHEN: 页面加载完成
- THEN: 页面标题显示为"热榜"或"Hot Rankings"

### Scenario 2: Tool 新增统计字段
- GIVEN: 数据库初始化
- WHEN: Tool 表被创建时
- THEN: 包含以下字段：
  - `view_count` INTEGER DEFAULT 0
  - `like_count` INTEGER DEFAULT 0
  - `comment_count` INTEGER DEFAULT 0
  - `score` DECIMAL(10,2) DEFAULT 0

### Scenario 3: ForumPost 新增 score 字段
- GIVEN: 数据库初始化
- WHEN: ForumPost 表被创建时
- THEN: 包含 `score` 字段（DECIMAL(10,2)，默认值为 0）

### Scenario 4: score 计算更新
- GIVEN: 工具或帖子有 viewCount、likeCount、commentCount
- WHEN: 调用 updateScore 方法时
- THEN: score = viewCount * 1 + likeCount * 3 + commentCount * 5

### Scenario 5: 工具浏览量更新
- GIVEN: 用户查看工具详情
- WHEN: 工具详情页被访问时
- THEN: Tool.viewCount + 1，调用 updateScore()

### Scenario 6: 工具点赞量更新
- GIVEN: 用户点赞工具
- WHEN: 点赞操作成功时
- THEN: Tool.likeCount + 1，调用 updateScore()

### Scenario 7: 工具评论数更新
- GIVEN: 用户评论工具
- WHEN: 评论操作成功时
- THEN: Tool.commentCount + 1，调用 updateScore()

### Scenario 8: 帖子浏览量更新
- GIVEN: 用户查看帖子详情
- WHEN: 帖子详情页被访问时
- THEN: ForumPost.viewCount + 1，调用 updateScore()

### Scenario 9: 帖子点赞量更新
- GIVEN: 用户点赞帖子
- WHEN: 点赞操作成功时
- THEN: ForumPost.likeCount + 1，调用 updateScore()

### Scenario 10: 帖子评论数更新
- GIVEN: 用户评论帖子
- WHEN: 评论操作成功时
- THEN: ForumPost.commentCount + 1，调用 updateScore()

### Scenario 11: 工具热榜按 score 排序
- GIVEN: 工具热榜有多个工具数据
- WHEN: 工具热榜渲染时
- THEN: 工具按 `score` 降序排列，score 越高排名越靠前

### Scenario 12: 帖子热榜按 score 排序
- GIVEN: 帖子热榜有多个帖子数据
- WHEN: 帖子热榜渲染时
- THEN: 帖子按 `score` 降序排列，score 越高排名越靠前

### Scenario 13: 使用真实分类名称
- GIVEN: 数据库中存在工具分类和帖子分类
- WHEN: 热榜条目显示分类标签
- THEN: 使用数据库中真实的分类名称（如"AI助手"、"编程工具"等）

### Scenario 14: 数据为空时显示占位
- GIVEN: 热榜数据为空
- WHEN: 热榜列表渲染时
- THEN: 显示"暂无数据"占位提示，不显示空列表

### Scenario 15: 点击工具条目跳转详情页
- GIVEN: 用户在工具热榜中看到工具列表
- WHEN: 用户点击某个工具条目
- THEN: 页面跳转到 `/tools/{id}`，显示该工具的详情

### Scenario 16: 点击帖子条目跳转详情页
- GIVEN: 用户在帖子热榜中看到帖子列表
- WHEN: 用户点击某个帖子条目
- THEN: 页面跳转到 `/forum/posts/{id}`，显示该帖子的详情

### Scenario 17: 移除过度装饰动画
- GIVEN: 页面正在渲染
- WHEN: 动画效果处理时
- THEN: 移除扫描线动画、脉冲指示灯等过度装饰，使用简洁的加载状态

### Scenario 18: Tab 分类过滤功能
- GIVEN: 热榜有多个分类
- WHEN: 用户点击某个分类 Tab
- THEN: 只显示该分类下的条目，"全部" Tab 显示所有条目

### Scenario 19: 统计卡片数据正确
- GIVEN: 数据库中有用户、帖子、工具数据
- WHEN: 页面加载时
- THEN: 统计卡片正确显示用户总数、帖子总数、工具总数

### Scenario 20: 工具详情页显示统计
- GIVEN: 用户访问工具详情页 `/tools/{id}`
- WHEN: 页面加载时
- THEN: 显示 viewCount、likeCount、commentCount

### Scenario 21: 工具详情页点赞功能
- GIVEN: 用户已登录且未点赞该工具
- WHEN: 用户点击点赞按钮
- THEN: 工具点赞数 + 1，score 更新，用户头像出现在点赞列表

### Scenario 22: 工具详情页取消点赞
- GIVEN: 用户已登录且已点赞该工具
- WHEN: 用户再次点击点赞按钮
- THEN: 工具点赞数 - 1，score 相应减少，移除点赞状态

### Scenario 23: 工具详情页评论功能
- GIVEN: 用户已登录且在工具详情页
- WHEN: 用户提交评论表单
- THEN: 评论成功保存，工具评论数 + 1，score 更新，评论列表刷新显示新评论

### Scenario 24: 工具详情页未登录提示
- GIVEN: 用户未登录
- WHEN: 用户点击点赞按钮或提交评论
- THEN: 提示用户先登录

### Scenario 25: 工具详情页点赞列表
- GIVEN: 工具已有多个用户点赞
- WHEN: 用户访问工具详情页
- THEN: 显示点赞用户列表（头像或用户名）