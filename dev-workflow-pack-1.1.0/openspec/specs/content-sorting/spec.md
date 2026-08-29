# Content Sorting

## ADDED Requirements

### Requirement: 后端列表接口支持 sortBy 参数

三个模块的列表接口（Tool、ForumPost、Video）SHALL 统一接受 `sortBy` 查询参数，支持 `hot` 和 `latest` 两个值，默认值为 `hot`。

#### Scenario: Tool 列表接口接受 sortBy 参数

- WHEN: 客户端请求 `GET /api/v1/tools?sortBy=hot`
- THEN: 后端返回按热度排序的工具列表（pinned 优先 + score 降序）

#### Scenario: ForumPost 列表接口接受 sortBy 参数

- WHEN: 客户端请求 `GET /api/forum/posts?sortBy=latest`
- THEN: 后端返回按创建时间降序排列的帖子列表

#### Scenario: Video 列表接口接受 sortBy 参数

- WHEN: 客户端请求 `GET /api/v1/videos?sortBy=hot`
- THEN: 后端返回按热度排序的微课列表（pinned 优先 + score 降序）

#### Scenario: 未提供 sortBy 参数时使用默认值

- WHEN: 客户端请求列表接口但未提供 `sortBy` 参数
- THEN: 后端 SHALL 默认使用 `sortBy=hot` 进行排序

### Requirement: 热度排序使用 pinned + score 复合排序

当 `sortBy=hot` 时，后端 SHALL 使用 JPQL `ORDER BY pinned DESC, score DESC` 实现复合排序，置顶项优先展示，非置顶项按 score 降序排列。

#### Scenario: 热度排序时置顶项排在最前

- WHEN: 列表中存在 pinned=true 和 pinned=false 的内容项，且 sortBy=hot
- THEN: 所有 pinned=true 的项排在 pinned=false 的项之前

#### Scenario: 热度排序时同级别按 score 降序

- WHEN: 多个内容项具有相同的 pinned 值，且 sortBy=hot
- THEN: 同级别内按 score 降序排列，score 高的排在前面

### Requirement: 最新排序按创建时间降序

当 `sortBy=latest` 时，后端 SHALL 使用 `ORDER BY createdAt DESC` 排序，忽略 pinned 字段。

#### Scenario: 最新排序忽略置顶状态

- WHEN: 列表中存在 pinned=true 的内容项，且 sortBy=latest
- THEN: 排序仅按 createdAt 降序，pinned 项不会优先展示

#### Scenario: 最新排序按创建时间降序

- WHEN: 客户端请求 sortBy=latest
- THEN: 返回列表按创建时间从新到旧排列

### Requirement: 前端显示排序切换 Tab

三个列表页（HomePage、PostListPage、VideoListPage）SHALL 显示"热度 | 最新"Tab 切换组件，用户可切换排序方式。

#### Scenario: 列表页默认显示热度 Tab 激活

- WHEN: 用户首次进入列表页
- THEN: "热度" Tab 处于激活状态，列表按热度排序

#### Scenario: 用户切换到最新 Tab

- WHEN: 用户点击"最新" Tab
- THEN: Tab 样式切换为激活"最新"，列表重新请求并展示 sortBy=latest 的结果

#### Scenario: 用户切换回热度 Tab

- WHEN: 用户在"最新" Tab 激活时点击"热度" Tab
- THEN: Tab 样式切换回激活"热度"，列表重新请求并展示 sortBy=hot 的结果

### Requirement: Tool 列表页 sortBy 参数兼容

Tool 列表接口当前已有 `sortBy` 参数（支持 `latest`、`name`），新增 `hot` 值后 SHALL 保持向后兼容。

#### Scenario: Tool 列表原有 sortBy=latest 行为不变

- WHEN: 客户端请求 `GET /api/v1/tools?sortBy=latest`
- THEN: 返回按创建时间降序排列的工具列表，行为与变更前一致

#### Scenario: Tool 列表默认改为 hot 排序

- WHEN: 客户端请求 `GET /api/v1/tools` 未指定 sortBy
- THEN: 返回按热度排序的工具列表（pinned 优先 + score 降序），而非原来的默认排序

### Requirement: 排序状态作为组件内 ref 管理

前端排序状态 `sortBy` SHALL 作为各列表页组件的 `ref` 管理，不存入 Pinia store。切换时重新请求列表接口。

#### Scenario: 切换排序触发列表重新请求

- WHEN: 用户切换排序 Tab
- THEN: 组件内 sortBy ref 更新，触发列表接口重新请求并刷新页面数据
