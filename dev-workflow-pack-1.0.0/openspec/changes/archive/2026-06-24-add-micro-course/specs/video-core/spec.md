# Video Core

## ADDED Requirements

### Requirement: 视频上传

系统 SHALL 允许已登录用户上传 MP4 格式的视频文件，单个文件大小不超过 1GB。视频文件存储于服务器本地磁盘 `uploads/videos/{userId}/{videoId}/` 目录下。

#### Scenario: 登录用户上传视频成功
- **WHEN** 已登录用户提交 `POST /api/videos`，携带 title、description 和 MP4 文件
- **THEN** 系统创建 Video 记录，状态为 NORMAL，文件保存至本地磁盘，返回视频 ID

#### Scenario: 上传非 MP4 格式文件
- **WHEN** 用户上传的文件不是 MP4 格式（如 .avi, .mov, .txt）
- **THEN** 系统返回 400 Bad Request，提示"仅支持 MP4 格式视频"

#### Scenario: 上传超过 1GB 的文件
- **WHEN** 用户上传的视频文件大小超过 1GB
- **THEN** 系统返回 413 Payload Too Large，提示"视频文件大小不能超过 1GB"

#### Scenario: 未登录用户上传视频
- **WHEN** 未登录用户尝试提交 `POST /api/videos`
- **THEN** 系统返回 401 Unauthorized

#### Scenario: 上传视频缺少必填字段
- **WHEN** 用户上传视频时未提供 title（必填字段）
- **THEN** 系统返回 400 Bad Request，提示"title 不能为空"

### Requirement: 视频列表查询

系统 SHALL 提供视频列表接口，支持分页查询，按创建时间倒序排列，无需登录即可访问。

#### Scenario: 分页获取视频列表
- **WHEN** 用户请求 `GET /api/videos?page=1&size=20`
- **THEN** 返回状态为 NORMAL 的视频列表，按 createdAt 倒序，包含分页信息（totalElements, totalPages, currentPage）

#### Scenario: 视频列表返回字段
- **WHEN** 获取视频列表
- **THEN** 每条视频 SHALL 返回 id、title、coverUrl、duration、viewCount、likeCount、commentCount、uploaderName、createdAt

#### Scenario: 空视频列表
- **WHEN** 系统中没有任何视频
- **THEN** 返回空列表，totalElements = 0

### Requirement: 视频详情查询

系统 SHALL 提供视频详情接口，无需登录即可访问。访问详情页时自动将播放量（viewCount）加 1。

#### Scenario: 获取视频详情
- **WHEN** 用户请求 `GET /api/videos/{id}`
- **THEN** 返回视频完整信息：id、title、description、videoUrl、coverUrl、duration、fileSize、viewCount、likeCount、commentCount、uploaderId、uploaderName、createdAt

#### Scenario: 访问详情自动增加播放量
- **WHEN** 用户请求 `GET /api/videos/{id}`
- **THEN** 该视频的 viewCount SHALL 自动加 1

#### Scenario: 视频不存在
- **WHEN** 请求的 video id 不存在或状态为 DELETED
- **THEN** 返回 404 Not Found

### Requirement: 视频流式播放

系统 SHALL 提供视频流式播放接口，支持 HTTP Range 请求（`Accept-Ranges: bytes`），实现边下边播。无需登录即可访问。

#### Scenario: 正常播放视频
- **WHEN** 用户请求 `GET /api/videos/{id}/stream`
- **THEN** 返回 200 OK，Content-Type 为 `video/mp4`，响应头包含 `Accept-Ranges: bytes`

#### Scenario: 播放器发送 Range 请求
- **WHEN** 用户请求携带 `Range: bytes=1000-2000` 头
- **THEN** 系统返回 206 Partial Content，只返回请求范围内的字节数据，响应头包含 `Content-Range: bytes 1000-2000/{totalSize}`

#### Scenario: Range 请求超出文件大小
- **WHEN** 用户请求的 Range 起始位置超过文件总大小
- **THEN** 系统返回 416 Range Not Satisfiable

#### Scenario: 视频文件不存在于磁盘
- **WHEN** 视频记录存在但磁盘上文件缺失
- **THEN** 系统返回 404 Not Found

### Requirement: 更新视频信息

系统 SHALL 允许视频上传者更新自己视频的标题和描述。

#### Scenario: 上传者更新视频标题和描述
- **WHEN** 视频上传者提交 `PUT /api/videos/{id}`，携带新的 title 和 description
- **THEN** 视频信息更新成功，返回更新后的视频详情

#### Scenario: 非上传者尝试更新视频
- **WHEN** 非上传者用户尝试 `PUT /api/videos/{id}`
- **THEN** 返回 403 Forbidden

### Requirement: 删除视频

系统 SHALL 允许视频上传者删除自己的视频（软删除，将 status 改为 DELETED）。

#### Scenario: 上传者删除视频
- **WHEN** 视频上传者提交 `DELETE /api/videos/{id}`
- **THEN** 视频状态变为 DELETED，从列表中消失，返回 204 No Content

#### Scenario: 非上传者尝试删除视频
- **WHEN** 非上传者用户尝试 `DELETE /api/videos/{id}`
- **THEN** 返回 403 Forbidden

### Requirement: 我的视频列表

系统 SHALL 提供已登录用户查看自己上传的视频列表。

#### Scenario: 获取我的视频列表
- **WHEN** 已登录用户请求 `GET /api/videos/my`
- **THEN** 返回当前用户上传的所有 NORMAL 状态视频，按 createdAt 倒序

#### Scenario: 未登录访问我的视频
- **WHEN** 未登录用户请求 `GET /api/videos/my`
- **THEN** 返回 401 Unauthorized
