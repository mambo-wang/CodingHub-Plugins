# Proposal: Add Forum Module

## Problem

CodingHub目前只有工具管理功能，缺少社区互动能力。用户需要一个论坛模块来分享使用心得、教程、资源等内容，同时可以在文章中引用平台内的工具并链接到外部资源。

## Testable Behaviors

### 帖子管理
- WHEN `GET /api/forum/posts` 被调用 THEN 返回帖子列表（分页，默认按创建时间倒序）
- WHEN `GET /api/forum/posts?category=<id>` 被调用 THEN 返回该分类下的帖子
- WHEN `GET /api/forum/posts?tag=<id>` 被调用 THEN 返回包含该标签的帖子
- WHEN `GET /api/forum/posts?keyword=<word>` 被调用 THEN 返回标题包含关键词的帖子
- WHEN `GET /api/forum/posts/{id}` 被调用 THEN 返回帖子详情（内容以原始 Markdown 返回）
- WHEN `POST /api/forum/posts`（已登录）被调用 THEN 创建新帖子并返回
- WHEN `PUT /api/forum/posts/{id}`（作者）被调用 THEN 更新帖子标题/内容/分类/标签
- WHEN `DELETE /api/forum/posts/{id}`（作者）被调用 THEN 标记帖子为 DELETED

### 分类与标签
- WHEN `GET /api/forum/categories` 被调用 THEN 返回所有分类（含帖子数量）
- WHEN `GET /api/forum/tags` 被调用 THEN 返回所有标签（含使用次数）
- WHEN `GET /api/forum/tags/hot` 被调用 THEN 返回使用次数最高的 10 个标签
- WHEN `POST /api/forum/tags`（已登录）被调用 THEN 创建新标签（名称唯一）

### 评论系统（楼中楼）
- WHEN `GET /api/forum/posts/{id}/comments` 被调用 THEN 返回该帖子的评论树（root + 子评论）
- WHEN `POST /api/forum/posts/{id}/comments` 被调用 THEN 创建评论（登录用户用真实 author_id，匿名用 author_name 和 ip_hash）
- WHEN `DELETE /api/forum/comments/{id}`（作者）被调用 THEN 删除评论

### 点赞功能
- WHEN `POST /api/forum/likes` 被调用 THEN 创建点赞记录（帖子或评论，互斥）
- WHEN 已登录用户重复点赞同一内容 THEN 返回错误或忽略
- WHEN 匿名用户重复点赞（同一 IP hash）THEN 返回错误或忽略
- WHEN `DELETE /api/forum/likes` 被调用 THEN 移除点赞记录

### Markdown 渲染（前端）
- WHEN 帖子内容在前端渲染时 THEN 识别所有 `/tools/\d+` 链接并添加 `target="_blank"`
- WHEN 帖子内容在前端渲染时 THEN 识别外部链接并添加特殊标记样式（图标或颜色）

## Acceptance Criteria

1. **帖子 CRUD**：用户可以创建、编辑、删除自己的帖子；游客可以查看所有帖子
2. **分类浏览**：用户可以按分类查看帖子列表
3. **标签功能**：用户可以为帖子添加标签，系统预设热门标签，用户也可自创
4. **搜索**：用户可以通过标题关键词搜索帖子
5. **评论**：用户可以评论帖子，支持楼中楼回复；匿名用户可以评论（需输入昵称）
6. **点赞**：登录用户和匿名用户都可以点赞帖子或评论
7. **Markdown 渲染**：帖子内容以 Markdown 格式存储，前端正确渲染，工具链接可跳转
8. **编辑器**：使用 Tiptap 所见即所得编辑器
9. **UI 设计**：前端 UI 由 frontend-design skill 设计