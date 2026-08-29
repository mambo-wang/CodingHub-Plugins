# Spec: Forum Comment System

## Scenarios

### Scenario 1: Guest views comment tree
- GIVEN: 帖子 id=1 有多条评论，包括楼中楼结构
- WHEN: 访问 `GET /api/forum/posts/1/comments`
- THEN: 返回评论树结构，root 评论在前，其 reply 在 children 数组中

### Scenario 2: Logged-in user comments
- GIVEN: 用户已登录，token 有效
- WHEN: 用户提交 `POST /api/forum/posts/1/comments`，content="测试评论"
- THEN: 创建评论，authorId 为当前用户，authorName 为用户昵称，返回 201

### Scenario 3: Anonymous user comments
- GIVEN: 用户未登录
- WHEN: 提交 `POST /api/forum/posts/1/comments`，authorName="访客小明"，content="匿名评论"
- THEN: 创建评论，authorId 为 null，authorName 存储输入的昵称

### Scenario 4: Anonymous user with cached nickname
- GIVEN: 用户之前用 IP=192.168.1.1 评论过，昵称缓存为 "常客"
- WHEN: 同一 IP 用户提交评论，authorName 输入 "常客"
- THEN: 后端识别 IP hash 匹配，直接使用缓存的昵称

### Scenario 5: Reply to existing comment (楼中楼)
- GIVEN: 帖子 id=1 的评论 id=10 是顶层评论
- WHEN: 用户提交 `POST /api/forum/posts/1/comments`，parentId=10，content="回复内容"
- THEN: 新评论的 parentId=10，rootId=10（指向顶层），形成楼中楼结构

### Scenario 6: Reply to nested comment
- GIVEN: 帖子 id=1 有评论 id=15 是评论 id=10 的回复（rootId=10）
- WHEN: 用户提交回复 parentId=15
- THEN: 新评论 parentId=15，rootId=10（保持指向原始顶层评论）

### Scenario 7: Author deletes own comment
- GIVEN: 用户 A 拥有评论 id=20
- WHEN: 用户 A 提交 `DELETE /api/forum/comments/20`
- THEN: 删除评论，帖子的 commentCount 减 1

### Scenario 8: Non-author cannot delete
- GIVEN: 用户 B 拥有评论 id=20
- WHEN: 用户 A（不是作者）提交 `DELETE /api/forum/comments/20`
- THEN: 返回 403 Forbidden

### Scenario 9: Comment count sync
- GIVEN: 帖子 id=1 当前 commentCount=5
- WHEN: 创建 3 条新评论
- THEN: 帖子的 commentCount 更新为 8