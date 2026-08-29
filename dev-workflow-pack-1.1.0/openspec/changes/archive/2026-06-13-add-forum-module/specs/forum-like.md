# Spec: Forum Like System

## Scenarios

### Scenario 1: Logged-in user likes post
- GIVEN: 用户已登录
- WHEN: 提交 `POST /api/forum/likes`，body={postId: 1}
- THEN: 创建点赞记录，userId 为当前用户，post 的 likeCount 加 1

### Scenario 2: Anonymous user likes post
- GIVEN: 用户未登录
- WHEN: 提交 `POST /api/forum/likes`，body={postId: 1}
- THEN: 创建点赞记录，userId 为 null，ipHash 存储 IP 的 hash 值

### Scenario 3: Duplicate like by same user
- GIVEN: 用户已点赞帖子 id=1
- WHEN: 用户再次提交点赞帖子 id=1
- THEN: 返回 409 Conflict 或忽略重复请求

### Scenario 4: Duplicate like by same IP
- GIVEN: IP 192.168.1.1 已点赞帖子 id=1
- WHEN: 同一 IP 用户再次点赞帖子 id=1
- THEN: 返回 409 Conflict 或忽略重复请求

### Scenario 5: User unlikes
- GIVEN: 用户已点赞帖子 id=1
- WHEN: 提交 `DELETE /api/forum/likes`，body={postId: 1}
- THEN: 删除点赞记录，post 的 likeCount 减 1

### Scenario 6: Anonymous user unlikes via IP
- GIVEN: 匿名用户通过 IP hash 点赞了帖子 id=1
- WHEN: 提交 `DELETE /api/forum/likes`，body={postId: 1}
- THEN: 删除点赞记录（通过 IP hash 识别）

### Scenario 7: Like a comment
- GIVEN: 用户已登录
- WHEN: 提交 `POST /api/forum/likes`，body={commentId: 5}
- THEN: 创建点赞记录，comment 的 likeCount 加 1

### Scenario 8: Mutual exclusion post/comment
- GIVEN: 用户尝试同时点赞 post 和 comment
- WHEN: 提交 `POST /api/forum/likes`，body={postId: 1, commentId: 5}
- THEN: 返回 400 Bad Request（postId 和 commentId 互斥）