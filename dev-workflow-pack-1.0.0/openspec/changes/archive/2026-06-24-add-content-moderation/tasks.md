## 1. 后端：ToolService 权限扩展

- [x] 1.1 修改 `ToolService.deleteTool` 方法签名：`Long userId` → `User user`，权限校验改为 `isOwner || isAdmin`（`user.getRole() == ADMIN || SUPER_ADMIN`）
- [x] 1.2 修改 `ToolService.updateTool` 方法签名：`Long userId` → `User user`，权限校验改为 `isOwner || isAdmin`
- [x] 1.3 修改 `ToolController.deleteTool` 和 `updateTool`：传参从 `currentUser.getId()` 改为 `currentUser`
- [x] 1.4 修改 `IaihubToolHandler.handleToolModify`（`IaihubToolHandler.java:323`）：适配 `updateTool` 新签名，传入已登录的 User 对象（MCP 层面权限不变，仍仅创建者可改）
- [x] 1.5 为 ToolService 编写/更新单元测试：更新 `ToolServiceTest` 中 `updateTool`/`deleteTool` 的 mock 签名，新增 `deleteTool_shouldAllowAdminToDeleteOthersTool`、`updateTool_shouldAllowAdminToUpdateOthersTool`、`deleteTool_shouldThrowForbiddenWhenNotOwnerAndNotAdmin` 测试用例，运行 `cd backend && ./gradlew test` 确认通过

## 2. 后端：ForumPostService 权限扩展

- [x] 2.1 修改 `ForumPostService.deletePost` 方法签名：`Long userId` → `User user`，权限校验改为 `isOwner || isAdmin`
- [x] 2.2 修改 `ForumPostService.updatePost` 方法签名：`Long userId` → `User user`，权限校验改为 `isOwner || isAdmin`
- [x] 2.3 修改 `ForumPostController.deletePost` 和 `updatePost`：传参从 `currentUser.getId()` 改为 `currentUser`
- [x] 2.4 新建 `ForumPostServiceTest.java`：覆盖创建者删除/更新、管理员删除/更新、普通用户 403、帖子不存在 404 场景，运行 `cd backend && ./gradlew test` 确认通过

## 3. 后端：VideoService 权限扩展

- [x] 3.1 修改 `VideoService.deleteVideo` 方法签名：`Long userId` → `User user`，权限校验改为 `isOwner || isAdmin`
- [x] 3.2 修改 `VideoService.updateVideo` 方法签名：`Long userId` → `User user`，权限校验改为 `isOwner || isAdmin`
- [x] 3.3 修改 `VideoController.deleteVideo` 和 `updateVideo`：传参从 `currentUser.getId()` 改为 `currentUser`
- [x] 3.4 新建 `VideoServiceTest.java`：覆盖创建者删除/更新、管理员删除/更新、普通用户 403、视频不存在 404 场景，运行 `cd backend && ./gradlew test` 确认通过

## 4. 前端：权限 composable

- [x] 4.1 新建 `frontend/src/composables/useContentPermissions.ts`：接收 `ownerId` 参数，返回 `canEdit` / `canDelete` 计算属性（`canEdit = isLoggedIn && (currentUserId === ownerId || isAdmin)`，`canDelete = canEdit`）

## 5. 前端：列表页卡片操作按钮

- [x] 5.1 修改 `PostCard.vue`：新增 `editable` prop，在卡片右上角添加半透明编辑/删除图标按钮（`opacity: 0.35`，卡片 hover 时 `opacity: 1`），编辑按钮 hover 变紫、删除按钮 hover 变红；按钮使用 `position: absolute` 不占布局空间
- [x] 5.2 修改 `VideoCard.vue`：新增 `editable` / `deletable` prop，添加与 PostCard 一致的 hover 操作按钮（注意 VideoCard 当前是 `router-link` 包裹，需调整结构使按钮可点击不触发导航）
- [x] 5.3 修改 `HomePage.vue`：在内联工具卡片中添加 hover 操作按钮（工具卡片非独立组件，需在页面内实现），使用 `useContentPermissions(tool.uploaderId)` 控制显示
- [x] 5.4 修改 `PostListPage.vue`：为 `PostCard` 传入 `editable` / `deletable` prop，使用 `useContentPermissions(post.authorId)` 计算
- [x] 5.5 修改 `VideoListPage.vue`：为 `VideoCard` 传入 `editable` / `deletable` prop，使用 `useContentPermissions(video.uploaderId)` 计算

## 6. 前端：详情页操作按钮

- [x] 6.1 修改 `DetailPage.vue`（工具详情）：在操作区添加编辑/删除按钮，使用 `useContentPermissions(tool.uploaderId)` 控制显示；编辑按钮跳转 `/me/tools/:id/edit`，删除按钮弹出 ConfirmDialog 确认后调 `DELETE /tools/:id`
- [x] 6.2 修改 `PostDetailPage.vue`：扩展删除按钮权限（从仅 `currentUserId === post.authorId` 改为 `canDelete`），新增编辑按钮跳转 `/forum/posts/:id/edit`；管理员可见他人帖子的删除/编辑按钮
- [x] 6.3 修改 `VideoDetailPage.vue`：在操作区添加编辑/删除按钮，使用 `useContentPermissions(video.uploaderId)` 控制显示；编辑跳转 `/videos/:id/edit`，删除弹出 ConfirmDialog 确认后调 `DELETE /api/v1/videos/:id`

## 7. 前端：帖子编辑功能补齐

- [x] 7.1 修改 `PostEditorPage.vue`：`onMounted` 中若 `route.params.id` 存在则调用 `forumService.getPostById` 回填标题/分类/内容；`publish()` 方法分支——编辑模式调 `forumService.updatePost(id, data)`，新建模式保持 `createPost`
- [x] 7.2 在 `router/index.ts` 新增路由 `/forum/posts/:id/edit`（name: `EditPost`，component: `PostEditorPage`），添加 `requiresAuth` meta

## 8. 前端：微课编辑页

- [x] 8.1 新建 `frontend/src/pages/video/VideoEditPage.vue`：包含标题和简介表单，`onMounted` 调 `videoService.getVideoDetail(id)` 回填，提交调 `videoService.updateVideo(id, { title, description })`（即 `PUT /api/v1/videos/:id`），不提供视频文件上传
- [x] 8.2 在 `router/index.ts` 新增路由 `/videos/:id/edit`（name: `EditVideo`，component: `VideoEditPage`），添加 `requiresAuth` meta

## 9. 前端：删除确认流程统一

- [x] 9.1 确保工具详情页和微课详情页的删除操作复用 `ConfirmDialog` 组件（帖子详情页已有），确认对话框标题为"删除{工具/帖子/微课}"，描述提示不可恢复
- [x] 9.2 删除成功后：列表页移除该项并 toast 提示；详情页跳转回对应列表页并 toast 提示
- [x] 9.3 删除失败（403）时 toast 提示"无权操作此内容"，对话框保持打开

## 10. 验证与收尾

- [x] 10.1 运行后端全量测试：`cd backend && ./gradlew test`，确认全部通过
- [x] 10.2 运行后端架构检查：`bash scripts/lint-arch.sh`，确认无新增违规
- [ ] 10.3 前端手动验证：以创建者登录验证自己内容的编辑/删除；以管理员登录验证任意内容的编辑/删除；以普通用户验证他人内容无按钮；未登录验证无按钮
- [ ] 10.4 前端双主题验证：暗色/亮色主题下卡片 hover 按钮、详情页按钮、编辑页表单、确认对话框样式正确
- [ ] 10.5 响应式验证：375px / 768px / 1024px 断点下操作按钮可见性和布局正常（移动端半透明按钮可见）
