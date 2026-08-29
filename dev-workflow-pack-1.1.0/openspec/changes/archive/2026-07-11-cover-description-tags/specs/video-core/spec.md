## ADDED Requirements（新增需求）

### Requirement: 视频标签关联

系统 SHALL 支持视频与标签的多对多关联，通过统一的 `Tag` 实体（type=VIDEO）和 `video_tag` 关联表实现。

#### Scenario: 上传视频时设置标签
- **WHEN** 已登录用户上传视频，请求参数包含 `tagIds`
- **THEN** 视频创建成功，`video_tag` 表写入关联记录，对应标签的 usage_count 加 1

#### Scenario: 更新视频时修改标签
- **GIVEN** 视频 videoId=10 当前关联标签 [1, 2]
- **WHEN** 上传者更新视频，传入 `tagIds: [2, 5]`
- **THEN** 移除标签 1 关联（usage_count -1），新增标签 5 关联（usage_count +1），保留标签 2

#### Scenario: 视频列表返回标签信息
- **WHEN** 用户请求视频列表 `GET /api/v1/videos`
- **THEN** 每条 `VideoListItem` 响应中包含 `tags` 数组，每项含 `id` 和 `name`

#### Scenario: 视频详情返回标签信息
- **WHEN** 用户请求视频详情 `GET /api/v1/videos/{id}`
- **THEN** `VideoResponse` 响应中包含 `tags` 数组

### Requirement: 视频封面设置

系统 SHALL 支持用户在微课上传或编辑时设置封面图片，详见 `video-cover` 规格。

> 本 delta 仅标注 video-core 模块需集成封面功能，完整需求定义见 `specs/video-cover/spec.md`。
