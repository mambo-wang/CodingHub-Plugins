## ADDED Requirements（新增需求）

### Requirement: 微课封面设置

系统 SHALL 允许用户在微课上传或编辑时设置视频封面图片。封面通过前端 `<video>` + `<canvas>` 截取视频帧生成，以图片形式上传至后端。封面存储于服务器 `{uploadBaseDir}/covers/{videoId}.jpg`，路径写入 `Video.coverUrl` 字段。

#### Scenario: 上传视频后截取封面
- **GIVEN** 用户已上传一个 MP4 视频（videoId=10），视频可正常播放
- **WHEN** 用户在前端拖动视频进度条到某一帧，点击"设为封面"
- **THEN** 前端通过 Canvas 截取该帧为 JPEG 图片，上传至 `POST /api/v1/videos/10/cover`，后端保存到 `covers/10.jpg`，`Video.coverUrl` 更新为封面路径

#### Scenario: 封面图片格式与大小限制
- **WHEN** 用户上传封面图片
- **THEN** 系统 SHALL 仅接受 JPEG/PNG 格式，文件大小不超过 5MB
- **WHEN** 上传的文件不符合格式或大小要求
- **THEN** 返回 400 Bad Request，提示"封面图片仅支持 JPEG/PNG 格式，大小不超过 5MB"

#### Scenario: 替换已有封面
- **GIVEN** 视频 videoId=10 已有封面图片
- **WHEN** 用户重新截取并上传新封面
- **THEN** 新封面覆盖旧文件（`covers/10.jpg`），`Video.coverUrl` 更新

#### Scenario: 未登录用户无法设置封面
- **WHEN** 未登录用户尝试 `POST /api/v1/videos/{id}/cover`
- **THEN** 返回 401 Unauthorized

#### Scenario: 非上传者无法修改封面
- **WHEN** 非视频上传者尝试 `POST /api/v1/videos/{id}/cover`
- **THEN** 返回 403 Forbidden

### Requirement: 微课封面展示

系统 SHALL 在视频列表和视频详情中返回封面图片 URL，前端展示封面缩略图。

#### Scenario: 视频列表展示封面
- **WHEN** 用户请求视频列表 `GET /api/v1/videos`
- **THEN** 每条视频的 `coverUrl` 字段 SHALL 返回封面图片的访问路径（若已设置封面）或 null（未设置封面）

#### Scenario: 视频详情展示封面
- **WHEN** 用户请求视频详情 `GET /api/v1/videos/{id}`
- **THEN** 返回的 `coverUrl` 字段为封面图片访问路径或 null

#### Scenario: 封面图片静态访问
- **WHEN** 客户端请求封面图片 URL
- **THEN** 系统 SHALL 通过静态资源服务返回封面图片文件

### Requirement: 封面上传 Fallback

当前端 Canvas 截帧失败（如视频编码不兼容）时，系统 SHALL 允许用户手动上传封面图片文件作为替代。

#### Scenario: 前端截帧失败后手动上传
- **GIVEN** 用户尝试 Canvas 截帧但失败（视频编码不兼容）
- **WHEN** 前端显示截帧失败提示
- **THEN** 用户可选择本地图片文件上传作为封面，走相同的 `POST /api/v1/videos/{id}/cover` 接口
