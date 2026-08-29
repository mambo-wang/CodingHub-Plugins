# Spec: 帖子删除

## Scenarios

### Scenario 1: 作者在帖子详情页看到删除按钮
- GIVEN: 已登录用户 A 访问自己创建的帖子详情页
- WHEN: 页面加载完成
- THEN: 在"点赞 / 收藏"按钮组旁显示一个红色"删除"按钮，使用 Lucide `Trash2` 图标 + 文字"删除"

### Scenario 2: 非作者在帖子详情页看不到删除按钮
- GIVEN: 已登录用户 B 访问用户 A 创建的帖子详情页
- WHEN: 页面加载完成
- THEN: 不显示"删除"按钮

### Scenario 3: 未登录用户在帖子详情页看不到删除按钮
- GIVEN: 游客访问任意帖子详情页
- WHEN: 页面加载完成
- THEN: 不显示"删除"按钮

### Scenario 4: 作者点击删除弹出确认对话框
- GIVEN: 作者在帖子详情页
- WHEN: 作者点击"删除"按钮
- THEN: 弹出 `ConfirmDialog`，标题"删除帖子"，描述"删除后无法恢复，确定要删除吗？"，含"取消"与"确认删除"两按钮；焦点自动落在"确认删除"按钮上

### Scenario 5: 作者在确认对话框点击取消
- GIVEN: 确认对话框已打开
- WHEN: 作者点击"取消"或按 Esc 或点击遮罩
- THEN: 对话框关闭，不调用任何 API，帖子状态保持 `NORMAL`

### Scenario 6: 作者成功删除帖子
- GIVEN: 作者在确认对话框中
- WHEN: 作者点击"确认删除"且后端返回 204
- THEN: 对话框关闭，路由跳转到 `/forum`，toast 提示"帖子已删除"，帖子状态在数据库变为 `DELETED`

### Scenario 7: 删除时未登录返回 401
- GIVEN: 作者在确认对话框中（token 恰好过期）
- WHEN: 作者点击"确认删除"且后端返回 401
- THEN: 提示"请先登录"，对话框保持打开，帖子不被删除

### Scenario 8: 删除非自己帖子返回 403
- GIVEN: 用户 B（伪装作者）发起删除用户 A 的帖子
- WHEN: 后端返回 403
- THEN: 提示"您不是该帖子的作者，无权删除"，对话框保持打开

### Scenario 9: 帖子不存在返回 404
- GIVEN: 帖子在打开页面后被其他会话删除
- WHEN: 作者点击"确认删除"且后端返回 404
- THEN: 提示"帖子不存在或已被删除"，对话框关闭，跳转回 `/forum`

### Scenario 10: 我的帖子页列表显示删除按钮
- GIVEN: 已登录用户访问 `/forum/my-posts`
- WHEN: 列表渲染完成
- THEN: 每条 `PostCard` 右上角显示一个 Lucide `Trash2` 图标按钮，hover 态变红

### Scenario 11: 我的帖子页删除成功后移除
- GIVEN: 用户在 `/forum/my-posts` 列表中
- WHEN: 用户点击某条"删除"图标，在确认对话框中点击"确认删除"且后端返回 204
- THEN: 该条立即从列表中消失，toast 提示"帖子已删除"，无需跳转

### Scenario 12: 确认对话框键盘可访问
- GIVEN: 确认对话框打开
- WHEN: 用户按 Esc
- THEN: 对话框关闭（等同"取消"）
- WHEN: 用户按 Tab
- THEN: 焦点在"取消"和"确认删除"两按钮之间循环
- WHEN: 用户按 Enter（在"确认删除"按钮聚焦时）
- THEN: 触发删除

### Scenario 13: 加载态禁用按钮
- GIVEN: 确认对话框打开
- WHEN: 用户点击"确认删除"且请求进行中
- THEN: "确认删除"按钮 disabled 并显示 spinner；"取消"按钮 disabled 防止误操作

### Scenario 14: 网络异常处理
- GIVEN: 确认对话框打开
- WHEN: 用户点击"确认删除"且发生网络错误（非 401/403/404）
- THEN: 提示"删除失败，请稍后重试"，按钮恢复可点击，对话框保持打开

### Scenario 15: 后端幂等性
- GIVEN: 帖子 `id=1` 状态为 `DELETED`
- WHEN: 任何用户调用 `DELETE /api/forum/posts/1`
- THEN: 后端按"找不到或非 NORMAL 状态"路径处理，UI 给出"帖子不存在或已被删除"提示
