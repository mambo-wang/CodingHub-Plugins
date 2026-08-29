# Spec: Forum Post Management

## Scenarios

### Scenario 1: Guest browses post list
- GIVEN: 数据库中有多个帖子，包含不同分类和标签
- WHEN: 游客访问 `GET /api/forum/posts?page=0&size=10`
- THEN: 返回帖子列表（分页），每条包含 id、title、authorName、categoryName、createdAt，不包含 content

### Scenario 2: Guest views post detail
- GIVEN: 数据库中存在 id=1 的帖子，内容为 Markdown 格式
- WHEN: 游客访问 `GET /api/forum/posts/1`
- THEN: 返回完整帖子信息，content 为原始 Markdown

### Scenario 3: User creates post
- GIVEN: 用户已登录，token 有效
- WHEN: 用户提交 `POST /api/forum/posts`，包含 title、content、categoryId、tagIds
- THEN: 创建帖子，返回 201，帖子的 authorId 为当前用户

### Scenario 4: Author updates own post
- GIVEN: 用户 A 拥有 id=1 的帖子
- WHEN: 用户 A 提交 `PUT /api/forum/posts/1`，更新 title 和 content
- THEN: 帖子更新成功，返回 200
- WHEN: 用户 B 提交 `PUT /api/forum/posts/1`
- THEN: 返回 403 Forbidden

### Scenario 5: Author deletes own post
- GIVEN: 用户 A 拥有 id=1 的帖子
- WHEN: 用户 A 提交 `DELETE /api/forum/posts/1`
- THEN: 帖子状态标记为 DELETED，返回 204

### Scenario 6: Filter by category
- GIVEN: 数据库中有多个分类的帖子
- WHEN: 访问 `GET /api/forum/posts?category=2`
- THEN: 只返回 categoryId=2 的帖子

### Scenario 7: Filter by tag
- GIVEN: 数据库中有多个标签的帖子
- WHEN: 访问 `GET /api/forum/posts?tag=5`
- THEN: 只返回包含 tagId=5 的帖子

### Scenario 8: Search by title keyword
- GIVEN: 数据库中有标题包含 "Spring" 的帖子
- WHEN: 访问 `GET /api/forum/posts?keyword=Spring`
- THEN: 返回标题包含 "Spring" 的帖子（模糊匹配）

### Scenario 9: Paginated results
- GIVEN: 数据库中有 25 个帖子
- WHEN: 访问 `GET /api/forum/posts?page=2&size=10`
- THEN: 返回第 3 页的 10 条数据，包含 totalPages=3, totalElements=25

### Scenario 10: Increment view count
- GIVEN: 帖子 id=1 当前 viewCount=100
- WHEN: 任何用户访问 `GET /api/forum/posts/1`
- THEN: viewCount 递增 1