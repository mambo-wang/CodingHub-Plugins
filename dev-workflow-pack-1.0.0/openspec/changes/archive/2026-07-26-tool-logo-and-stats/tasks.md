## 1. 数据模型与 DDL

- [x] 1.1 `Tool` 实体新增 `logoUrl` 字段（`@Column(name = "logo_url", length = 512)`）
- [x] 1.2 `Category` 实体新增 `logoUrl` 字段（`@Column(name = "logo_url", length = 512)`）
- [x] 1.3 `ToolFile` 实体新增 `downloadCount` 字段（`@Column(name = "download_count") @Builder.Default Integer downloadCount = 0`）
- [ ] 1.4 启动后端验证 `ddl-auto:update` 自动添加 `tool.logo_url`、`category.logo_url`、`tool_file.download_count` 三列
- [x] 1.5 后端单元测试：在 `model/ToolFileTest.java` 补充 `downloadCount` 默认值为 0 的断言并确认通过

## 2. Repository 层聚合查询

- [x] 2.1 `UnifiedFavoriteRepository` 新增 `long countByTargetTypeAndTargetId(String targetType, Long targetId)`
- [x] 2.2 `UnifiedFavoriteRepository` 新增批量分组查询 `@Query` 按 targetId IN 集合返回 `List<Object[]>`（targetId, count），供列表页组装 Map
- [x] 2.3 `ToolFileRepository` 新增 `@Modifying @Query("UPDATE ToolFile f SET f.downloadCount = f.downloadCount + 1 WHERE f.id = :id")` 原子自增方法
- [x] 2.4 `ToolFileRepository` 新增按 toolId IN 集合分组求和 `download_count` 的 `@Query`（返回 toolId 与 sum）
- [x] 2.5 后端单元测试：扩展 `repository/ToolFileRepositoryTest.java` 覆盖分组求和查询（@DataJpaTest + H2），确认通过
- [x] 2.6 后端单元测试：新建 `repository/UnifiedFavoriteCountRepositoryTest.java` 覆盖按 targetType+targetId 计数与批量分组计数，确认通过

## 3. 下载计数自增

- [x] 3.1 `ToolFileService.downloadFile` 在成功定位文件后调用 `ToolFileRepository` 原子自增 `download_count`
- [x] 3.2 后端单元测试：新建 `service/ToolFileDownloadCountTest.java`（Mockito）验证下载成功触发自增、文件不存在抛 404 不自增，确认通过（不扩展历史损坏的 ToolFileServiceTest）

## 4. DTO 扩展

- [x] 4.1 `ToolSummaryDTO` 新增 `logoUrl`、`favoriteCount`、`downloadCount` 字段
- [x] 4.2 `ToolDetailDTO` 新增 `logoUrl`、`favoriteCount`、`downloadCount` 字段
- [x] 4.3 `CategoryDTO` 新增 `logoUrl` 字段，并在 `CategoryService` 组装处填充

## 5. ToolService 统计聚合与 logo 回退

- [x] 5.1 `ToolService` 构造器末尾追加注入 `UnifiedFavoriteRepository` 与 `ToolFileRepository`（保持既有位置参数顺序，新依赖放末尾）
- [x] 5.2 实现 logo 回退私有方法：`logoUrl = tool.logoUrl != null ? tool.logoUrl : tool.category.logoUrl`（皆空返回 null）
- [x] 5.3 `getTools` / `getMyTools` 在拿到当前页 toolIds 后批量查询收藏量 Map 与下载量 Map，传入映射方法
- [x] 5.4 `toSummaryDTO` / `toDetailDTO` 填充 `logoUrl`、`favoriteCount`、`downloadCount`（无数据填 0，非 null）
- [x] 5.5 后端单元测试：新建 `service/ToolServiceLogoStatsTest.java`（Mockito，按真实构造器顺序含新增依赖）覆盖三级回退、批量聚合、无收藏无下载填 0，确认通过

## 6. Logo 绑定端点

- [x] 6.1 `ToolController` 新增 `POST /api/v1/tools/{id}/logo`，body `{"logoUrl": "..."}`，鉴权 isOwner || isAdmin，写入 `tool.logo_url`
- [x] 6.2 复用 `POST /api/v1/uploads/images` 作为 logo 文件上传通道（不新建存储），前端先上传得到 url 再调用 6.1 绑定
- [x] 6.3 后端单元测试：新建 `controller/ToolControllerLogoTest.java`（MockMvc standaloneSetup）覆盖所有者设置成功、非所有者非管理员 403、工具不存在 404，确认通过

## 7. 前端工具卡片（HomePage.vue）

- [x] 7.1 `ToolSummary` 类型新增 `logoUrl`、`favoriteCount`、`downloadCount` 字段
- [x] 7.2 新增 `frontend/src/utils/format.ts` 的 `formatCount(n)`：≥10000 → `x.x万`，≥1000 → `x.xk`，否则原值
- [x] 7.3 工具卡片左上角渲染 logo `img`（`logoUrl` 非空），`@error` 回退系统占位图标，`alt` 为工具名
- [x] 7.4 卡片底部新增统计行：浏览量(Eye)/点赞量(Heart)/收藏量(Bookmark)/下载量(Download) 四项，图标 `aria-hidden`，数字用 `formatCount` + 等宽字体
- [x] 7.5 统计行样式遵循 design-system.md（`border-top` 分隔、`var(--text-muted)` 图标、`var(--text-secondary)` 数字），双主题自适应
- [x] 7.6 加载态骨架屏与空状态保持兼容，375px 下统计四项完整可见无水平滚动

## 8. 前端详情页与表单

- [x] 8.1 `ToolDetailPage.vue` 标题区展示 logo（同回退逻辑 + 裂图兜底）
- [x] 8.2 工具上传/编辑表单新增 logo 上传组件：复用图片上传端点，含 idle/uploading/success/error 四态与 `role="alert"` 错误提示
- [x] 8.3 上传成功后调用 `POST /api/v1/tools/{id}/logo` 绑定 logoUrl

## 9. 前端管理端分类默认 logo

- [x] 9.1 管理端分类管理页新增分类默认 logo 设置（上传后通过分类更新接口携带 `logoUrl`）
- [x] 9.2 分类列表/工具卡片正确消费 `CategoryDTO.logoUrl` 作为回退来源

## 10. 受影响模块回归测试（基于 impact-analysis.md，L2 风险）

- [x] 10.1 更新 `service/ToolServiceTagFilterTest.java` 的 `ToolService` 构造调用，末尾补充 `UnifiedFavoriteRepository`/`ToolFileRepository` mock，跑通既有标签过滤用例（L2 — 构造器签名变化）
- [x] 10.2 跑通 `controller/ToolControllerTagFilterTest.java`，确认 ToolController 新增 logo 端点不破坏既有用例（L1）
- [x] 10.3 跑通 `repository/ToolFileRepositoryTest.java`（含 2.5 新增聚合用例）（L1 — 新增查询）
- [x] 10.4 跑通 `model/ToolFileTest.java`（含 1.5 新增断言）（L1）
- [x] 10.5 跑通 `service/McpSearchServiceTagFilterTest.java`，确认 MCP 检索不受本次改动影响（L1）
- [x] 10.6 运行 `cd backend && ./gradlew test`，确认除既有 9 个历史损坏用例（ToolFileControllerTest 4 + ToolFileServiceTest 4 + IaihubToolHandlerKbTest 1，已 exclude）外全部通过
- [x] 10.7 运行等价层级校验（`scripts/lint-arch.sh` 或 Python 扫描）确认 `controller→service→repository→model` 单向依赖 PASS

## 11. 前端验收

- [x] 11.1 `node node_modules/vue-tsc/bin/vue-tsc.js --noEmit` 类型检查通过
- [ ] 11.2 手动回归：广场卡片 logo 三级回退、裂图兜底、统计行四项格式化（16.5万/1.2k/207）
- [ ] 11.3 手动回归：双主题切换（暗色/亮色）样式正确，375px/768px/1024px 三断点布局正常
- [ ] 11.4 对照 `ui-preview.html` 完成视觉验收
